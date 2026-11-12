"""Domain Intelligence Endpoints for URLSentinel."""

from typing import Dict, Any
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from ...core.ssrf_guard import validate_destination_safety, SSRFBlockedError
from ...core.dns_tls_inspector import inspect_dns_records, inspect_tls_certificate
from ...core.homoglyph_detector import detect_brand_impersonation
from ...core.feed_ingestion import query_threat_intel

router = APIRouter(prefix="/domain", tags=["Domain Intelligence"])


class DomainIntelResponse(BaseModel):
    domain: str
    is_routable: bool
    resolved_ipv4: list[str]
    resolved_ipv6: list[str]
    has_tls: bool
    tls_issuer: str | None = None
    tls_days_remaining: int | None = None
    impersonation_flags: list[dict[str, str]]
    active_threats_count: int


@router.get("/{domain}", response_model=DomainIntelResponse)
async def get_domain_intelligence(domain: str):
    """Retrieve deep DNS, TLS, and infrastructure intelligence for a domain."""
    clean_domain = domain.strip().lower()

    # Pre-validate against SSRF
    try:
        validate_destination_safety(f"https://{clean_domain}", resolve_dns=False)
    except SSRFBlockedError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Invalid Domain", "message": str(e)},
        )

    # 1. DNS Records
    dns = inspect_dns_records(clean_domain)

    # 2. TLS Certificate
    tls = inspect_tls_certificate(clean_domain, timeout=2.0)

    # 3. Homoglyph & Lookalikes
    homoglyphs = detect_brand_impersonation(clean_domain)
    flags = [
        {"target_brand": b[0], "brand_name": b[1], "detection_type": b[2]}
        for b in homoglyphs
    ]

    # 4. Threat Intel match count
    ti_matches = query_threat_intel("", clean_domain)

    return DomainIntelResponse(
        domain=clean_domain,
        is_routable=dns.is_routable,
        resolved_ipv4=dns.resolved_ipv4,
        resolved_ipv6=dns.resolved_ipv6,
        has_tls=tls.has_tls,
        tls_issuer=tls.issuer,
        tls_days_remaining=tls.days_remaining,
        impersonation_flags=flags,
        active_threats_count=len(ti_matches),
    )

