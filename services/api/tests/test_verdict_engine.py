"""Tests for Verdict Engine."""

from urlsentinel.core.url_normalizer import normalize_url
from urlsentinel.core.lexical_analyzer import analyze_lexical
from urlsentinel.core.verdict_engine import evaluate_verdict


class TestVerdictEngine:
    def test_provider_outage_yields_unknown_never_benign(self):
        """CRITICAL INVARIANT: Provider outage or failure must never coerce to BENIGN."""
        norm = normalize_url("https://unknown-domain-test-12345.org")
        lex = analyze_lexical(norm)
        
        verdict = evaluate_verdict(
            norm_url=norm,
            lexical=lex,
            provider_errors=["ThreatIntel feed connection timed out after 5.0s"],
        )
        assert verdict.verdict == "UNKNOWN"
        assert verdict.status == "PARTIAL"
        assert any("External feed connection degraded" in lim for lim in verdict.limitations)

    def test_confirmed_threat_intel_match_yields_malicious(self):
        norm = normalize_url("https://malicious-lure.xyz/account/login")
        lex = analyze_lexical(norm)
        
        ti_matches = [
            {
                "threat_type": "phishing",
                "source": "OpenPhish Feed",
                "reported_at": "2026-11-03T00:00:00Z",
                "freshness": "1h",
                "details": "Active credential harvesting target",
            }
        ]
        
        verdict = evaluate_verdict(
            norm_url=norm,
            lexical=lex,
            ti_matches=ti_matches,
        )
        assert verdict.verdict == "MALICIOUS"
        assert verdict.confidence == "HIGH"
        assert verdict.risk_score >= 90
        assert len(verdict.evidence) > 0

    def test_benign_verdict_includes_explicit_caveats(self):
        norm = normalize_url("https://github.com/about")
        lex = analyze_lexical(norm)
        
        verdict = evaluate_verdict(
            norm_url=norm,
            lexical=lex,
            resolved_ips=["140.82.121.4"],
        )
        assert verdict.verdict == "BENIGN"
        assert len(verdict.limitations) > 0
        assert "cannot be guaranteed" in verdict.recommended_action or len(verdict.limitations) > 0

