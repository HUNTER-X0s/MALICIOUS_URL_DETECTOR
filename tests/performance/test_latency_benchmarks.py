"""Performance and Detection Latency Benchmarks for URLSentinel.

Validates that critical path operations meet defined performance budgets:
- Synchronous lexical + typosquatting + homoglyph + ML scoring: < 50.0 ms
- Target compliant with Blueprint §049 (Fast path detection SLA)
"""

import time
import pytest
from urlsentinel.core.url_normalizer import normalize_url
from urlsentinel.core.lexical_analyzer import analyze_lexical
from urlsentinel.core.homoglyph_detector import detect_brand_impersonation
from urlsentinel.core.ml_classifier import MLClassifier
from urlsentinel.core.verdict_engine import evaluate_verdict


class TestLatencyBenchmarks:
    """Latency benchmark suite ensuring fast synchronous execution budgets."""

    def test_pipeline_latency_budget(self):
        sample_urls = [
            "https://www.google.com/search?q=cybersecurity+threats",
            "http://login-verify-account.bank-security.top/update/password?token=secret123",
            "https://paypa1-security-verification.com/signin",
            "https://en.wikipedia.org/wiki/Transport_Layer_Security",
            "http://198.51.100.22/malware.exe",
        ]

        # Warm up
        for url in sample_urls:
            norm = normalize_url(url)
            analyze_lexical(norm)
            detect_brand_impersonation(norm.host)
            MLClassifier.predict(url)

        # Benchmark 50 iterations
        start_time = time.perf_counter()
        iterations = 50

        for _ in range(iterations):
            for url in sample_urls:
                norm = normalize_url(url)
                lexical = analyze_lexical(norm)
                homo = detect_brand_impersonation(norm.host)
                ml = MLClassifier.predict(norm.normalized_url)
                evaluate_verdict(norm, lexical, homoglyphs=homo, ml_prediction=ml)

        total_time = time.perf_counter() - start_time
        total_evaluations = iterations * len(sample_urls)
        avg_latency_ms = (total_time / total_evaluations) * 1000

        print(f"\nAverage evaluation latency: {avg_latency_ms:.3f} ms per URL ({total_evaluations} evaluations)")

        # Target: under 50.0 milliseconds per URL evaluation
        assert avg_latency_ms < 50.0, f"Average latency {avg_latency_ms:.2f}ms exceeded SLA budget of 50.0ms"
