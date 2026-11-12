"""Tests for URL Normalization Subsystem."""

from urlsentinel.core.url_normalizer import normalize_url, _remove_dot_segments


class TestURLNormalizer:
    def test_basic_normalization(self):
        norm = normalize_url("HTTP://EXAMPLE.COM:80/path/to/page?b=2&a=1#section")
        assert norm.scheme == "http"
        assert norm.host == "example.com"
        assert norm.port is None  # Port 80 stripped for http
        assert norm.path == "/path/to/page"
        assert norm.normalized_url == "http://example.com/path/to/page?b=2&a=1#section"

    def test_strip_default_https_port(self):
        norm = normalize_url("https://example.com:443/test")
        assert norm.port is None
        assert norm.normalized_url == "https://example.com/test"

    def test_preserve_non_standard_port(self):
        norm = normalize_url("https://example.com:8443/api")
        assert norm.port == 8443
        assert ":8443" in norm.normalized_url

    def test_dot_segment_traversal_resolution(self):
        assert _remove_dot_segments("/a/b/../c") == "/a/c"
        assert _remove_dot_segments("/a/./b/./c") == "/a/b/c"
        assert _remove_dot_segments("/a/b/../../c") == "/c"

    def test_public_suffix_decomposition(self):
        norm = normalize_url("https://sub.portal.example.co.uk/login")
        assert norm.registered_domain == "example.co.uk"
        assert norm.subdomain == "sub.portal"
        assert norm.public_suffix == "co.uk"

    def test_hash_generation(self):
        norm1 = normalize_url("https://example.com/test")
        norm2 = normalize_url("https://example.com/test")
        assert norm1.url_hash == norm2.url_hash
        assert len(norm1.url_hash) == 64

