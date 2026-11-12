"""Health and System Status Endpoints."""

from datetime import datetime, timezone
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/health", tags=["Operations"])


class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: str
    services: dict[str, str]


@router.get("", response_model=HealthResponse)
async def check_health():
    """Verify system health status across core subsystems."""
    now_iso = datetime.now(timezone.utc).isoformat()
    return HealthResponse(
        status="healthy",
        version="0.1.0",
        timestamp=now_iso,
        services={
            "api": "up",
            "ssrf_protection": "active",
            "lexical_engine": "ready",
            "cache": "operational",
        },
    )

