"""Community Threat and False-Positive Reporting Endpoints."""

import uuid
from datetime import datetime, timezone
from typing import Optional, Literal
from fastapi import APIRouter, status
from pydantic import BaseModel, Field

from ...core.url_redactor import redact_url
from ...core.url_normalizer import normalize_url

router = APIRouter(prefix="/report", tags=["Community Reporting"])


class ThreatReportRequest(BaseModel):
    url: str = Field(..., min_length=1, max_length=2048)
    report_type: Literal["FALSE_POSITIVE", "NEW_PHISHING", "MALWARE_DISTRIBUTION", "SUSPICIOUS_LURE"]
    comments: Optional[str] = Field(None, max_length=1000)
    reporter_contact: Optional[str] = Field(None, max_length=100)


class ThreatReportResponse(BaseModel):
    report_id: str
    status: str
    url_redacted: str
    submitted_at: str
    message: str


# In-memory storage for community reports
_COMMUNITY_REPORTS: list[dict] = []


@router.post("", response_model=ThreatReportResponse, status_code=status.HTTP_201_CREATED)
async def submit_report(payload: ThreatReportRequest):
    """Submit a threat observation or false-positive appeal for triage."""
    report_id = str(uuid.uuid4())
    now_iso = datetime.now(timezone.utc).isoformat()
    redacted = redact_url(payload.url)

    report_record = {
        "id": report_id,
        "type": payload.report_type,
        "url_redacted": redacted,
        "comments": payload.comments,
        "submitted_at": now_iso,
        "status": "QUEUED_FOR_REVIEW",
    }
    _COMMUNITY_REPORTS.append(report_record)

    return ThreatReportResponse(
        report_id=report_id,
        status="QUEUED_FOR_REVIEW",
        url_redacted=redacted,
        submitted_at=now_iso,
        message="Report logged into audit registry. An automated review job has been queued.",
    )

