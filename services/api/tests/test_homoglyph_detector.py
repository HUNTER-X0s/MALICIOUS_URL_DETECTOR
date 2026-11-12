"""Tests for Homoglyph and Lookalike Brand Detection."""

from urlsentinel.core.homoglyph_detector import (
    detect_brand_impersonation,
    normalize_confusables,
)


class TestHomoglyphDetector:
    def test_cyrillic_homoglyph_normalization(self):
        # 'pаypal' with Cyrillic 'а' (\u0430)
        spoofed = "p\u0430ypal"
        normalized = normalize_confusables(spoofed)
        assert normalized == "paypal"

    def test_detects_cyrillic_brand_spoofing(self):
        # Cyrillic 'а' inside paypal domain label
        domain = "p\u0430ypal-secure.com"
        matches = detect_brand_impersonation(domain)
        assert len(matches) > 0
        assert any(b[0] == "paypal" for b in matches)

    def test_detects_brand_name_in_lure_domain(self):
        domain = "login-microsoft365-verify.com"
        matches = detect_brand_impersonation(domain)
        assert any(b[0] == "microsoft" for b in matches)

    def test_legitimate_brand_domain_not_flagged(self):
        legit_domains = ["google.com", "microsoft.com", "apple.com", "paypal.com"]
        for domain in legit_domains:
            matches = detect_brand_impersonation(domain)
            assert len(matches) == 0

