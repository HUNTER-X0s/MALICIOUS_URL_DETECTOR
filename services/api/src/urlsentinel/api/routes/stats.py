"""Telemetry and Aggregated Detection Statistics Endpoint."""

from typing import Dict, Optional
from fastapi import APIRouter
from pydantic import BaseModel
from ...core.telemetry import telemetry

router = APIRouter(prefix="/stats", tags=["Operations"])


class StatsResponse(BaseModel):
    total_scans_today: int
    threats_detected_today: int
    average_latency_ms: float
    active_rules_count: int
    last_feed_sync: str
    clean_scans_today: Optional[int] = None
    ssrf_blocks_today: Optional[int] = None
    engine_status: Optional[str] = "Operational"
    uptime_seconds: Optional[float] = None
    last_scan_at: Optional[str] = None
    subsystems: Optional[Dict[str, str]] = None


@router.get("", response_model=StatsResponse)
async def get_system_stats():
    """Retrieve operational detection metrics without exposing user URLs or PII."""
    data = telemetry.get_stats()
    return StatsResponse(**data)
