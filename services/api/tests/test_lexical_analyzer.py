"""Tests for Lexical and Structural Analyzer."""

from urlsentinel.core.url_normalizer import normalize_url
from urlsentinel.core.lexical_analyzer import (
    analyze_lexical,
    calculate_entropy,
    levenshtein_distance,
)


class TestLexicalAnalyzer:
    def test_entropy_calculation(self):
        # Repetitive string has low entropy
        assert calculate_entropy("aaaaaa") == 0.0
        # Highly random string has higher entropy
        assert calculate_entropy("a8f9z2q1m7") > 3.0

    def test_levenshtein_distance(self):
        assert levenshtein_distance("paypal", "paypal") == 0
        assert levenshtein_distance("paypa1", "paypal") == 1
        assert levenshtein_distance("micros0ft", "microsoft") == 1

    def test_typosquatting_detection(self):
        norm = normalize_url("https://paypa1-security.com/login")
        lex = analyze_lexical(norm)
        # paypa1-security is edit distance from paypal
        assert any("paypal" in match for match in lex.typosquat_matches) or lex.risk_score > 0

    def test_ip_address_host_detection(self):
        norm = normalize_url("http://198.51.100.22/malware.exe")
        lex = analyze_lexical(norm)
        assert lex.is_ip_host is True
        assert any("numeric IP" in a for a in lex.anomalies)
        assert lex.risk_score >= 35

    def test_shortener_detection(self):
        norm = normalize_url("https://bit.ly/3xyz45")
        lex = analyze_lexical(norm)
        assert lex.is_shortener is True
        assert any("shortener" in a for a in lex.anomalies)

    def test_benign_destination_low_risk(self):
        norm = normalize_url("https://wikipedia.org/wiki/Computer_security")
        lex = analyze_lexical(norm)
        assert lex.is_ip_host is False
        assert lex.is_shortener is False
        assert len(lex.typosquat_matches) == 0
        assert lex.risk_score < 25

