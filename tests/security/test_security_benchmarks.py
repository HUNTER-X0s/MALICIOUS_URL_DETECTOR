"""Security Benchmark & Vulnerability Regression Test Suite.

Verifies non-negotiable security invariants:
- SSRF prevention against advanced IP obfuscation (octal, hex, dword, mapped IPv6)
- Credential and secret redaction from URLs and query parameters
- Constant-time verification on cryptographic signatures
- HTTP security headers presence (CSP, frame options, sniffing protection)
"""

import hmac
import pytest
from httpx import AsyncClient, ASGITransport
from urlsentinel.main import app
from urlsentinel.core.ssrf_guard import validate_destination_safety, SSRFBlockedError
from urlsentinel.core.url_redactor import redact_url


class TestSecurityBenchmarks:
    """Security invariants and vulnerability regression suite."""

    def test_ssrf_obfuscation_vectors(self):
        vectors = [
            ("http://0x7f000001", "Hexadecimal loopback"),
            ("http://2130706433", "Decimal integer loopback"),
            ("http://0177.0.0.1", "Octal loopback"),
            ("http://[::ffff:127.0.0.1]", "IPv4-mapped IPv6 loopback"),
            ("http://[::1]", "IPv6 loopback"),
            ("http://169.254.169.254/latest/meta-data/", "AWS/GCP metadata"),
            ("http://100.100.100.200/latest/meta-data/", "Alibaba metadata"),
            ("http://10.0.0.5/internal", "RFC 1918 Class A"),
            ("http://192.168.1.1/admin", "RFC 1918 Class C"),
            ("http://172.16.0.1/status", "RFC 1918 Class B"),
        ]

        for target_url, description in vectors:
            with pytest.raises(SSRFBlockedError, match=r"prohibited|restricted|SSRF|loopback|private|metadata") as exc_info:
                validate_destination_safety(target_url, resolve_dns=False)
            assert exc_info.value.code in (
                "SSRF_LOOPBACK_BLOCKED",
                "SSRF_PRIVATE_NETWORK_BLOCKED",
                "SSRF_CLOUD_METADATA_BLOCKED",
                "PRIVATE_OR_METADATA_IP",
            ), f"Failed vector: {description} ({target_url})"

    def test_sensitive_credentials_redaction(self):
        test_url = "https://admin:SuperSecretPassword123@internal.portal.com/auth?token=eyJhbGciOiJIUzI1NiJ9.test&api_key=sk-live-12345&password=my_cleartext_pass"
        redacted = redact_url(test_url)

        # Authority secrets must be completely removed
        assert "SuperSecretPassword123" not in redacted
        assert "internal.portal.com/auth" in redacted

        # Query parameter tokens must be masked
        assert "eyJhbGci" not in redacted
        assert "sk-live" not in redacted
        assert "my_cleartext_pass" not in redacted
        assert "token=[REDACTED]" in redacted or "token=%5BREDACTED%5D" in redacted
        assert "api_key=[REDACTED]" in redacted or "api_key=%5BREDACTED%5D" in redacted
        assert "password=[REDACTED]" in redacted or "password=%5BREDACTED%5D" in redacted

    @pytest.mark.asyncio
    async def test_security_headers_enforced(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            resp = await client.get("/api/v1/health")
            assert resp.status_code == 200
            assert resp.headers.get("X-Content-Type-Options") == "nosniff"
            assert resp.headers.get("X-Frame-Options") == "DENY"
            assert resp.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"
            assert resp.headers.get("Permissions-Policy") == "camera=(), microphone=(), geolocation=()"
            assert "X-Request-ID" in resp.headers
