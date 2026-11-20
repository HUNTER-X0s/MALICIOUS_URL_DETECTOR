"""URL Scanning Endpoints for URLSentinel."""

import dataclasses
import time
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from fastapi import APIRouter, HTTPException, status
from ...core.ssrf_guard import validate_destination_safety, SSRFBlockedError
from ...core.url_normalizer import normalize_url
from ...core.url_redactor import redact_url
from ...core.lexical_analyzer import analyze_lexical
from ...core.homoglyph_detector import detect_brand_impersonation
from ...core.feed_ingestion import query_threat_intel
from ...core.dns_tls_inspector import inspect_tls_certificate
from ...core.isolated_scanner import IsolatedScanner
from ...core.verdict_engine import evaluate_verdict, VerdictOutput
from ...core.telemetry import telemetry
from ...schemas.scan import ScanRequest, VerdictResponse, ErrorResponse
from ...cache.redis_cache import cache_manager

router = APIRouter(prefix="/scan", tags=["Scanning"])

# In-memory local cache as immediate sync fallback
_SCAN_CACHE_BY_ID: Dict[str, VerdictOutput] = {}
_SCAN_CACHE_BY_HASH: Dict[str, VerdictOutput] = {}


@router.post(
    "",
    response_model=VerdictResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "SSRF or validation rejection"},
        422: {"description": "Unprocessable input"},
    },
)
async def submit_scan(payload: ScanRequest):
    """
    Submit a URL for security inspection.

    Validates destination against SSRF restrictions, standardizes the URL,
    checks threat intelligence repositories, inspects lexical & homoglyph markers,
    executes optional isolated DOM sandboxing, and renders an evidence-based verdict.
    """
    raw_url = payload.url.strip()
    start_time = time.perf_counter()

    # Step 1: Enforce SSRF & Destination Safety Boundary
    try:
        canonical_origin, resolved_ips = validate_destination_safety(
            raw_url, resolve_dns=True
        )
    except SSRFBlockedError as e:
        telemetry.record_ssrf_block()
        now_iso = datetime.now(timezone.utc).isoformat()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "Destination Security Violation",
                "code": e.code,
                "message": str(e),
                "details": {"target_ip": e.target_ip} if e.target_ip else {},
                "timestamp": now_iso,
            },
        )

    # Step 2: Canonical URL Normalization
    norm_url = normalize_url(raw_url)

    # Step 3: Check cache by normalized hash (unless deep scan explicitly requested)
    if not payload.request_deep_scan:
        # Check in-memory sync cache first
        if norm_url.url_hash in _SCAN_CACHE_BY_HASH:
            cached_verdict = _SCAN_CACHE_BY_HASH[norm_url.url_hash]
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            telemetry.record_scan(cached_verdict.verdict, elapsed_ms)
            return cached_verdict

        # Check async Redis persistent cache
        cached_record = await cache_manager.get_verdict_by_hash(norm_url.url_hash)
        if cached_record:
            verdict_obj = VerdictOutput(**cached_record)
            _SCAN_CACHE_BY_HASH[norm_url.url_hash] = verdict_obj
            _SCAN_CACHE_BY_ID[verdict_obj.id] = verdict_obj
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            telemetry.record_scan(verdict_obj.verdict, elapsed_ms)
            return verdict_obj

    # Step 4: Lexical & Structural Feature Extraction
    lexical = analyze_lexical(norm_url)

    # Step 5: Homoglyph and Lookalike Analysis
    homoglyphs = detect_brand_impersonation(norm_url.host)

    # Step 6: Threat Intelligence Query
    ti_matches = query_threat_intel(norm_url.url_hash, norm_url.host)

    # Step 7: TLS Certificate Inspection (if HTTPS and not blocked)
    cert_details = None
    if norm_url.scheme == "https":
        try:
            cert_details = inspect_tls_certificate(norm_url.host, port=norm_url.port or 443, timeout=2.0)
        except Exception:
            pass

    # Step 8: Optional Isolated DOM Sandboxed Scan
    scanner_result = None
    if payload.request_deep_scan:
        try:
            scanner_result = await IsolatedScanner.analyze_target_content(
                norm_url.normalized_url, timeout_seconds=2.5
            )
        except Exception:
            pass

    # Step 9: Synthesize Final Verdict
    verdict_out = evaluate_verdict(
        norm_url=norm_url,
        lexical=lexical,
        resolved_ips=resolved_ips,
        ti_matches=ti_matches,
        homoglyphs=homoglyphs,
        cert_details=cert_details,
        scanner_result=scanner_result,
    )

    # Record execution telemetry
    elapsed_ms = (time.perf_counter() - start_time) * 1000
    telemetry.record_scan(verdict_out.verdict, elapsed_ms)

    # Cache result locally and persistently in Redis
    _SCAN_CACHE_BY_ID[verdict_out.id] = verdict_out
    _SCAN_CACHE_BY_HASH[verdict_out.url_hash] = verdict_out
    await cache_manager.store_verdict(
        verdict_out.url_hash,
        verdict_out.id,
        dataclasses.asdict(verdict_out),
    )

    return verdict_out


@router.get(
    "/{scan_id}",
    response_model=VerdictResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Scan report not found"},
    },
)
async def get_scan_report(scan_id: str):
    """Retrieve an existing scan verdict by its unique report ID."""
    if scan_id in _SCAN_CACHE_BY_ID:
        return _SCAN_CACHE_BY_ID[scan_id]

    cached_record = await cache_manager.get_verdict_by_id(scan_id)
    if cached_record:
        verdict_obj = VerdictOutput(**cached_record)
        _SCAN_CACHE_BY_ID[scan_id] = verdict_obj
        _SCAN_CACHE_BY_HASH[verdict_obj.url_hash] = verdict_obj
        return verdict_obj

    now_iso = datetime.now(timezone.utc).isoformat()
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={
            "error": "Report Not Found",
            "code": "REPORT_NOT_FOUND",
            "message": f"No scan record found matching ID '{scan_id}'",
            "timestamp": now_iso,
        },
    )
