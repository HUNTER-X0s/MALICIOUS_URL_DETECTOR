"""Tests for the SSRF Guard Subsystem."""

import pytest
from urlsentinel.core.ssrf_guard import (
    validate_destination_safety,
    parse_numeric_ip,
    SSRFBlockedError,
)


class TestSSRFGuard:
    def test_blocks_localhost_and_loopback(self):
        with pytest.raises(SSRFBlockedError) as exc:
            validate_destination_safety("http://127.0.0.1/admin", resolve_dns=False)
        assert exc.value.code == "PRIVATE_OR_METADATA_IP"

        with pytest.raises(SSRFBlockedError) as exc:
            validate_destination_safety("http://localhost/status", resolve_dns=False)
        assert exc.value.code == "INTERNAL_HOSTNAME"

        with pytest.raises(SSRFBlockedError) as exc:
            validate_destination_safety("http://[::1]/debug", resolve_dns=False)
        assert exc.value.code == "PRIVATE_OR_METADATA_IP"

    def test_blocks_private_networks(self):
        private_ips = [
            "http://10.0.0.1/config",
            "http://172.16.0.5/api",
            "http://192.168.1.1/router",
            "http://[fc00::1]/internal",
            "http://[fe80::1]/linklocal",
        ]
        for url in private_ips:
            with pytest.raises(SSRFBlockedError):
                validate_destination_safety(url, resolve_dns=False)

    def test_blocks_cloud_metadata_endpoints(self):
        metadata_targets = [
            "http://169.254.169.254/latest/meta-data/",
            "http://100.100.100.200/latest/meta-data/",
            "http://192.0.0.170/latest/meta-data/",
        ]
        for url in metadata_targets:
            with pytest.raises(SSRFBlockedError) as exc:
                validate_destination_safety(url, resolve_dns=False)
            assert exc.value.code == "PRIVATE_OR_METADATA_IP"

    def test_blocks_numeric_encoding_variants(self):
        # 0x7f000001 == 127.0.0.1
        with pytest.raises(SSRFBlockedError):
            validate_destination_safety("http://0x7f000001/bypass", resolve_dns=False)

        # 2130706433 == 127.0.0.1 in decimal integer
        with pytest.raises(SSRFBlockedError):
            validate_destination_safety("http://2130706433/bypass", resolve_dns=False)

        # 0177.0.0.1 == 127.0.0.1 in octal
        with pytest.raises(SSRFBlockedError):
            validate_destination_safety("http://0177.0.0.1/bypass", resolve_dns=False)

    def test_blocks_ipv4_mapped_ipv6(self):
        with pytest.raises(SSRFBlockedError):
            validate_destination_safety("http://[::ffff:127.0.0.1]/test", resolve_dns=False)

        with pytest.raises(SSRFBlockedError):
            validate_destination_safety("http://[::ffff:169.254.169.254]/test", resolve_dns=False)

    def test_blocks_prohibited_schemes(self):
        prohibited = [
            "file:///etc/passwd",
            "javascript:alert(1)",
            "ftp://files.example.com",
            "data:text/html,test",
            "gopher://example.com",
        ]
        for url in prohibited:
            with pytest.raises(SSRFBlockedError) as exc:
                validate_destination_safety(url, resolve_dns=False)
            assert exc.value.code == "UNSAFE_SCHEME"

    def test_blocks_prohibited_ports(self):
        with pytest.raises(SSRFBlockedError) as exc:
            validate_destination_safety("http://example.com:22/", resolve_dns=False)
        assert exc.value.code == "UNSAFE_PORT"

        with pytest.raises(SSRFBlockedError) as exc:
            validate_destination_safety("http://example.com:3306/", resolve_dns=False)
        assert exc.value.code == "UNSAFE_PORT"

    def test_allows_valid_public_origins(self):
        origin, ips = validate_destination_safety("https://example.com/test", resolve_dns=False)
        assert origin == "https://example.com"
        assert origin.startswith("https://")

