"""Pydantic schemas for the URLSentinel API."""

from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field


class ScanRequest(BaseModel):
    url: str = Field(
        ...,
        min_length=1,
        max_length=2048,
        description="The candidate target URL to analyze",
        examples=["https://example.com/login"],
    )
    request_deep_scan: bool = Field(
        default=False,
        description="Whether to queue for isolated sandbox execution if supported",
    )


class EvidenceItemSchema(BaseModel):
    id: str
    layer: str
    signal_name: str
    source: str
    observed_at: str
    freshness: str
    contribution: Literal["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFORMATIONAL"]
    description: str
    technical_details: Optional[Dict[str, Any]] = None


class TechnicalDetailsSchema(BaseModel):
    scheme: str
    host: str
    port: Optional[int] = None
    path: str
    query_params_count: int
    entropy: float
    is_ip_host: bool
    is_shortener: bool
    suspicious_tokens: List[str]
    typosquatting_matches: List[str]
    punycode: Optional[str] = None
    resolved_ips: Optional[List[str]] = None
    has_tls: bool = False
    tls_issuer: Optional[str] = None
    tls_days_remaining: Optional[int] = None
    ml_probability: Optional[float] = None
    ml_risk_band: Optional[str] = None


class VerdictResponse(BaseModel):
    id: str
    url: str
    url_hash: str
    verdict: Literal["MALICIOUS", "SUSPICIOUS", "UNKNOWN", "BENIGN"]
    status: Literal["QUEUED", "RUNNING", "COMPLETED", "PARTIAL", "FAILED", "EXPIRED"]
    risk_score: int = Field(..., ge=0, le=100)
    confidence: Literal["LOW", "MEDIUM", "HIGH"]
    summary: str
    evidence: List[EvidenceItemSchema]
    limitations: List[str]
    technical_details: TechnicalDetailsSchema
    recommended_action: str
    checked_at: str
    expires_at: str
    contract_version: str = "1.0.0"


class ErrorResponse(BaseModel):
    error: str
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: str
