"""Tests for URL Redactor Subsystem."""

from urlsentinel.core.url_redactor import redact_url


class TestURLRedactor:
    def test_redacts_credentials_in_authority(self):
        url = "https://user:SuperSecretPassword123@secure.bank.com/dashboard"
        redacted = redact_url(url)
        assert "SuperSecretPassword123" not in redacted
        assert "user" not in redacted
        assert redacted == "https://secure.bank.com/dashboard"

    def test_redacts_sensitive_query_parameters(self):
        url = "https://api.example.com/v1/auth?client_id=123&token=secret_jwt_token_xyz&redirect=https://app.com"
        redacted = redact_url(url)
        assert "secret_jwt_token_xyz" not in redacted
        assert "token=%5BREDACTED%5D" in redacted or "token=[REDACTED]" in redacted
        assert "client_id=123" in redacted

    def test_safe_urls_preserved(self):
        url = "https://example.com/search?q=cybersecurity&page=2"
        redacted = redact_url(url)
        assert "cybersecurity" in redacted
        assert "page=2" in redacted

