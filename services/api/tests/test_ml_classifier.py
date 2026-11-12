"""Tests for URLSentinel Explainable Machine Learning & Heuristic Classifier."""

import pytest
from urlsentinel.core.ml_classifier import MLClassifier


class TestMLClassifier:
    """Test suite for ML feature extraction, logistic scoring, and attribution."""

    def test_benign_url_low_probability(self):
        url = "https://www.wikipedia.org/wiki/Computer_security"
        result = MLClassifier.predict(url)

        assert result["probability"] < 0.20
        assert result["risk_band"] == "LOW"
        assert result["features"]["is_ip_host"] == 0.0
        assert result["features"]["has_at_symbol"] == 0.0

    def test_phishing_lure_with_credentials_and_abuse_tld(self):
        url = "http://login-verify-account.bank-security.top/update/password?auth=verify"
        result = MLClassifier.predict(url)

        assert result["probability"] > 0.50
        assert result["risk_band"] in ("HIGH", "CRITICAL")
        assert result["features"]["high_abuse_tld"] == 1.0
        assert result["features"]["keyword_score"] > 1.0
        assert len(result["top_indicators"]) > 0

    def test_raw_ip_address_host_elevates_risk(self):
        url = "http://198.51.100.22/secure/banking/signin"
        result = MLClassifier.predict(url)

        assert result["features"]["is_ip_host"] == 1.0
        assert result["probability"] >= 0.50
        reasons = " ".join(result["top_indicators"])
        assert "Raw IP address" in reasons

    def test_punycode_and_homoglyph_detection(self):
        url = "https://xn--pple-43d.com/login"
        result = MLClassifier.predict(url)

        assert result["features"]["has_punycode"] == 1.0
        assert any("Punycode" in r for r in result["top_indicators"])

    def test_at_symbol_credential_lure(self):
        url = "http://support.apple.com@evil-phish.biz/verify"
        result = MLClassifier.predict(url)

        assert result["features"]["has_at_symbol"] == 1.0
        assert any("@" in r for r in result["top_indicators"])

    def test_feature_attributions_are_deterministic(self):
        url = "http://crypto-wallet-verify.club/signin"
        res1 = MLClassifier.predict(url)
        res2 = MLClassifier.predict(url)

        assert res1["probability"] == res2["probability"]
        assert res1["features"] == res2["features"]
        assert len(res1["attributions"]) == len(res2["attributions"])

