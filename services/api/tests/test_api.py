"""Integration Tests for URLSentinel API Endpoints."""

import pytest
from httpx import AsyncClient, ASGITransport
from urlsentinel.main import app


@pytest.mark.asyncio
async def test_health_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "services" in data


@pytest.mark.asyncio
async def test_stats_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["total_scans_today"] > 0


@pytest.mark.asyncio
async def test_scan_endpoint_valid_url():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/scan",
            json={"url": "https://example.com/test"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "verdict" in data
        assert "risk_score" in data
        assert "evidence" in data
        assert "limitations" in data
        assert "technical_details" in data


@pytest.mark.asyncio
async def test_scan_endpoint_blocks_ssrf_attempt():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/scan",
            json={"url": "http://169.254.169.254/latest/meta-data/"},
        )
        assert response.status_code == 400
        data = response.json()
        assert data["code"] == "PRIVATE_OR_METADATA_IP"
        assert "Destination Security Violation" in data["error"]


@pytest.mark.asyncio
async def test_threat_report_submission():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/report",
            json={
                "url": "https://evil-phish.com/login?token=secret123",
                "report_type": "NEW_PHISHING",
                "comments": "Observed in active spear-phishing campaign",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "QUEUED_FOR_REVIEW"
        assert "secret123" not in data["url_redacted"]


@pytest.mark.asyncio
async def test_cryptographic_verification_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # First perform scan
        scan_res = await client.post(
            "/api/v1/scan",
            json={"url": "https://example.com/verify-test"},
        )
        scan_id = scan_res.json()["id"]

        # Now verify integrity
        verify_res = await client.get(f"/api/v1/verify/{scan_id}")
        assert verify_res.status_code == 200
        vdata = verify_res.json()
        assert vdata["is_valid"] is True
        assert vdata["signature_algorithm"] == "HMAC-SHA256"
        assert len(vdata["digital_signature"]) == 64
