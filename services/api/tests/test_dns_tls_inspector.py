"""Tests for DNS and TLS Inspector."""

import pytest
from urlsentinel.core.dns_tls_inspector import (
    inspect_dns_records,
    inspect_tls_certificate,
)
from urlsentinel.core.ssrf_guard import SSRFBlockedError


class TestDnsTlsInspector:
    def test_dns_blocks_private_rebinding(self):
        with pytest.raises(SSRFBlockedError):
            inspect_dns_records("127.0.0.1")

        with pytest.raises(SSRFBlockedError):
            inspect_dns_records("169.254.169.254")

    def test_dns_non_routable_domain(self):
        res = inspect_dns_records("this-domain-definitely-does-not-exist-12345.xyz")
        assert res.is_routable is False
        assert res.error is not None

    def test_tls_unreachable_target_fails_safely(self):
        cert = inspect_tls_certificate("192.0.2.1", port=443, timeout=0.5)
        assert cert.has_tls is False

