"""Tests for Threat Intelligence Ingestion and Lookup."""

from urlsentinel.core.feed_ingestion import (
    query_threat_intel,
    get_threat_intel_metrics,
    initialize_threat_intel_seeds,
)
from urlsentinel.core.url_normalizer import normalize_url


class TestFeedIngestion:
    def test_seed_initialization(self):
        initialize_threat_intel_seeds()
        metrics = get_threat_intel_metrics()
        assert metrics["indexed_url_hashes"] > 0
        assert metrics["indexed_domains"] > 0

    def test_exact_threat_url_match(self):
        norm = normalize_url("https://paypa1-security-verification.com/login")
        matches = query_threat_intel(norm.url_hash, norm.host)
        assert len(matches) > 0
        assert matches[0]["threat_type"] == "phishing"
        assert matches[0]["confidence"] == "CRITICAL"

    def test_domain_threat_match(self):
        norm = normalize_url("http://198.51.100.22/another-path")
        matches = query_threat_intel(norm.url_hash, norm.host)
        assert len(matches) > 0
        assert any("198.51.100.22" in m["details"] for m in matches)

    def test_clean_url_no_threat_match(self):
        norm = normalize_url("https://wikipedia.org/wiki/Main_Page")
        matches = query_threat_intel(norm.url_hash, norm.host)
        assert len(matches) == 0

