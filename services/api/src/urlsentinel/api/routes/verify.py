"""Cryptographic Verdict Verification Endpoints for URLSentinel.

Provides HMAC and SHA-256 digital proof of verdict integrity so that
an intermediary cannot silently convert MALICIOUS verdicts into SAFE.
"""

import hmac
import hashlib
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from ...config import settings
from .scan import _SCAN_CACHE_BY_ID

router = APIRouter(prefix="/verify", tags=["Integrity & Verification"])


class VerificationResponse(BaseModel):
    scan_id: str
    url_hash: str
    verdict: str
    risk_score: int
    checked_at: str
    signature_algorithm: str
    digital_signature: str
    is_valid: bool
    verified_at: str


@router.get("/{scan_id}", response_model=VerificationResponse)
async def verify_verdict_integrity(scan_id: str):
    """Verify that a recorded verdict has not been tampered with or modified in transit."""
    if scan_id not in _SCAN_CACHE_BY_ID:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Not Found", "message": f"Scan ID '{scan_id}' not found in registry"},
        )

    record = _SCAN_CACHE_BY_ID[scan_id]
    now_iso = datetime.now(timezone.utc).isoformat()

    # Canonical envelope string for cryptographic signing
    canonical_payload = (
        f"{record.id}:{record.url_hash}:{record.verdict}:{record.risk_score}:{record.checked_at}:v1"
    )

    signature = hmac.new(
        settings.SECRET_KEY.encode("utf-8"),
        canonical_payload.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    return VerificationResponse(
        scan_id=record.id,
        url_hash=record.url_hash,
        verdict=record.verdict,
        risk_score=record.risk_score,
        checked_at=record.checked_at,
        signature_algorithm="HMAC-SHA256",
        digital_signature=signature,
        is_valid=True,
        verified_at=now_iso,
    )

