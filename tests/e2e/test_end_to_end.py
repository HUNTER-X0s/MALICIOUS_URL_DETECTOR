"""URLSentinel End-to-End Integration Test Suite.

Executes complete product lifecycle tests across FastAPI endpoints:
- Clean URL scan and cryptographic signature verification
- Active phishing lure and threat intel detection
- SSRF attack prevention and security boundary enforcement
- False positive reporting and dispute handling
- Domain intelligence and homoglyph inspection
"""

import pytest
from httpx import AsyncClient, ASGITransport
from urlsentinel.main import app


@pytest.mark.asyncio
async def test_e2e_clean_url_scan_and_verification():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        # 1. Submit scan for benign destination
        response = await client.post(
            "/api/v1/scan",
            json={"url": "https://example.org/about", "request_deep_scan": False},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["verdict"] in ("BENIGN", "UNKNOWN")
        assert data["risk_score"] < 40
        assert "evidence" in data
        assert "technical_details" in data
        scan_id = data["id"]

        # 2. Verify cryptographic proof of the generated verdict
        verify_resp = await client.get(f"/api/v1/verify/{scan_id}")
        assert verify_resp.status_code == 200
        verify_data = verify_resp.json()
        assert verify_data["is_valid"] is True
        assert verify_data["scan_id"] == scan_id
        assert "digital_signature" in verify_data
        assert verify_data["signature_algorithm"] == "HMAC-SHA256"


@pytest.mark.asyncio
async def test_e2e_phishing_lure_detection():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        # Target with high-abuse TLD, login lure keyword, and password parameter
        phish_url = "http://login-verify-account.bank-security.top/update/password?token=secret123"
        response = await client.post(
            "/api/v1/scan",
            json={"url": phish_url},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["verdict"] in ("MALICIOUS", "SUSPICIOUS")
        assert data["risk_score"] >= 75
        assert data["confidence"] in ("HIGH", "MEDIUM")
        assert any(ev["layer"] in ("lexical", "ml_statistical") for ev in data["evidence"])


@pytest.mark.asyncio
async def test_e2e_ssrf_attacks_strictly_blocked():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        # Test AWS/GCP metadata endpoint
        response = await client.post(
            "/api/v1/scan",
            json={"url": "http://169.254.169.254/latest/meta-data/"},
        )
        assert response.status_code == 400
        err = response.json()
        assert err["error"] == "Destination Security Violation"
        assert err["code"] == "PRIVATE_OR_METADATA_IP"

        # Test octal loopback bypass
        response_octal = await client.post(
            "/api/v1/scan",
            json={"url": "http://0177.0.0.1/admin"},
        )
        assert response_octal.status_code == 400
        assert "LOOPBACK" in response_octal.json()["code"] or "PRIVATE" in response_octal.json()["code"]


@pytest.mark.asyncio
async def test_e2e_false_positive_reporting_flow():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        report_payload = {
            "url": "https://legitimate-corp.example/portal",
            "report_type": "FALSE_POSITIVE",
            "reason": "This is our official customer service subdomain incorrectly flagged",
            "contact_email": "security@legitimate-corp.example",
        }
        response = await client.post("/api/v1/report", json=report_payload)
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "QUEUED_FOR_REVIEW"
        assert "report_id" in data


@pytest.mark.asyncio
async def test_e2e_domain_intelligence_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/api/v1/domain/paypa1.com")
        assert response.status_code == 200
        data = response.json()
        assert data["domain"] == "paypa1.com"
        assert "impersonation_flags" in data
        assert len(data["impersonation_flags"]) > 0
        assert "PayPal" in data["impersonation_flags"][0]["brand_name"]
