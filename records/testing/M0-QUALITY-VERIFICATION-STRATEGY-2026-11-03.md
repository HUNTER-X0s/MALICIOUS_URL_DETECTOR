# URLSentinel — Quality and Verification Strategy (M0)

**Date:** 2026-11-03  
**Reference:** `docs/08-quality/TEST_STRATEGY.md`, `docs/04-security/SECURITY_TEST_AUTHORIZATION.md`

---

## 1. Testing philosophy

- Tests must actually run; evidence must be saved — no claims of test passage without output
- Tests are planned and organized before implementation, not added as an afterthought
- Independent verification is required for critical security controls (SSRF guard, scanner isolation, verdict integrity)
- False positives and false negatives are distinct costs — both are tracked
- Security testing uses only authorized targets: synthetic fixtures, owned domains, explicitly authorized test targets

---

## 2. Test portfolio (layered)

### Layer 1: Static checks (every commit, CI gate)
| Check | Tool (TBD in ADR) | Acceptance |
|---|---|---|
| Code formatting | Prettier / Black | Zero diff |
| Linting | ESLint / Ruff | Zero errors |
| Type checking | TypeScript / mypy | Zero errors |
| Secret scanning | detect-secrets / gitleaks | Zero detected secrets |
| Dependency scanning (SCA) | npm audit / pip-audit | Zero critical/high unresolved |
| SAST | Semgrep / Bandit | Zero critical findings |

### Layer 2: Unit tests
| Component | Coverage target | Key scenarios |
|---|---|---|
| URL parser | 95% line | WHATWG edge cases, IPv4 variants, IDN, encoding, userinfo |
| SSRF guard | 100% of IP ranges | Every private/reserved/metadata range; numeric encoding; IPv6-mapped; redirect revalidation |
| Lexical signal engine | 90% line | Each signal type; edge cases; adversarial inputs |
| Verdict engine | 90% line | Every verdict state; provider failure → UNKNOWN; stale → UNKNOWN |
| Feed ingestion | 85% line | Parse, dedup, freshness; anomalous input |
| URL redaction | 100% | Credentials in query params; fragments with tokens |

### Layer 3: Integration tests
- URL submission → parsing → lexical analysis → verdict (no network mocking)
- Feed ingestion → cache population → reputation lookup
- Provider mock: timeout → UNKNOWN (not BENIGN) — CRITICAL test
- Provider mock: error → UNKNOWN (not BENIGN) — CRITICAL test
- Stale cache TTL expiry → UNKNOWN (not BENIGN)
- Database migration: up and down without data loss

### Layer 4: API contract tests
- Every API endpoint: happy path, validation errors, rate limit, auth failure
- Verdict response schema: validated against JSON schema
- API backward compatibility: new releases don't break documented contract

### Layer 5: End-to-end tests
- Web app: home → scan → result (MALICIOUS) → copy → back
- Web app: scan → result (UNKNOWN) → see limitations
- Web app: false positive report flow
- Extension: navigate to test URL → warning interstitial appears → Go Back works
- Extension: navigate to safe test URL → no friction

### Layer 6: Security tests (authorized targets only)

> [!CAUTION]
> Security tests must only run against: localhost, owned domains, synthetic test fixtures, or explicitly authorized staging environments. Never test against third-party targets without written authorization.

| Test | Method | When |
|---|---|---|
| SSRF bypass variants | Automated unit + integration test | Every build (M3+) |
| DNS rebinding | Integration test with controlled resolver mock | Every build (M6+) |
| SQL injection | Parameterized query verification + SAST | Every build |
| XSS in result pages | CSP validation + manual review | M7 milestone |
| Auth bypass | Integration test (M10) | Every build (M10+) |
| IDOR | Authorization test with multiple test accounts (M10) | Every build (M10+) |
| Rate limit enforcement | Load test with quota exhaustion | M7+ |
| Extension CSP | Automated CSP header analysis | M7 milestone |
| Extension message spoofing | Unit test with crafted messages | M7 milestone |
| Scanner escape (M9) | Independent security review | Before M9 release |
| Dependency vulnerabilities | SCA in CI | Every build |

### Layer 7: Adversarial URL tests
- Corpus of ≥ 500 crafted URLs covering each SSRF bypass variant
- Corpus of ≥ 200 crafted URLs covering IDN, Unicode confusables, homoglyphs
- Corpus of ≥ 100 crafted URLs covering encoded/obfuscated patterns
- Regression: every new evasion technique found in research → add to corpus

### Layer 8: Performance tests
| Metric | Target | Tool |
|---|---|---|
| API P95 response (cached lookup) | < 500ms | k6 or Locust |
| API P95 response (full analysis) | < 2000ms | k6 or Locust |
| Web app LCP | ≤ 2.5s | Lighthouse CI |
| Web app INP | < 200ms | Lighthouse CI |
| Web app CLS | < 0.1 | Lighthouse CI |
| Extension navigation overhead | < 50ms P95 | Chrome DevTools trace |
| Extension memory footprint | < 50MB | Chrome Task Manager measurement |

### Layer 9: Accessibility tests
- axe-core automated: zero critical/serious issues in CI
- Manual keyboard navigation: complete tab order for all major flows
- Screen reader: NVDA + Chrome (Windows) spot-check on verdict display and warning interstitial
- Color contrast: all text ≥ 4.5:1 (3:1 for large text)
- Color independence: all verdict states have text labels; not color only

### Layer 10: Compatibility tests
| Browser | Extension | Web app |
|---|---|---|
| Chrome (latest stable) | ✓ Primary | ✓ |
| Edge (latest stable) | ✓ Secondary | ✓ |
| Firefox (latest stable) | ✓ Secondary | ✓ |
| Safari (latest stable) | N/A (extension) | ✓ |
| Chrome (latest - 1) | ✓ | ✓ |

### Layer 11: Privacy and data governance tests
- Verify no full URL appears in structured logs (redaction test)
- Verify no credentials/tokens in log output
- Verify scan result pages return `noindex` meta tag
- Verify data deletion removes URL and verdict from all storage layers
- Verify no URL sent to external providers without consent/policy alignment

### Layer 12: ML evaluation (M8+)
- Domain-grouped split: no domain appears in both train and test
- Time-based evaluation: test on data chronologically after training data
- Calibration test: confidence scores are calibrated (not just ranked)
- Adversarial evaluation: evasion corpus recall rate
- Poisoning simulation: inject mislabeled samples and measure model degradation

---

## 3. Test data governance

- Synthetic fixtures: crafted without real malicious content; labeled manually; version-controlled under `data/fixtures/synthetic/`
- Adjudicated corpus (M4+): verified positives from licensed feeds; verified negatives from top-domain lists; not committed to repo without license review
- No real user URLs in test data
- No live malware executed on host
- Adversarial URL corpus: inert strings only (crafted to test parser behavior, not execute)

---

## 4. Independent verification requirements

The following controls require independent verification — review by someone not involved in the implementation:

| Control | When | Reviewer |
|---|---|---|
| SSRF guard | M3 (before M4) | Security Engineering (separate from Backend Engineer who built it) |
| Verdict UNKNOWN-on-failure rule | M4 (before M5) | Quality Engineering |
| Scanner trust-zone design | M2 (before M9 starts) | External security assessor or independent internal reviewer |
| Scanner implementation | M9 (before M9 releases) | Independent security assessor (external preferred) |
| Auth and authorization | M10 | Security Engineering |
| Pre-launch security | M12 | External penetration tester |

---

## 5. Evidence requirements

Every test run must produce:
- Date and time of execution
- Tool name and version
- Command run (exact)
- Environment (dev/staging)
- Pass/fail/skip for each test case
- Error output for failures
- Summary statistics (coverage, pass rate, performance metrics)
- Known limitations or skipped tests with justification

Evidence is stored in `records/testing/` using the `TEMPLATE_TEST_REPORT.md` format.

---

## 6. Release quality gates

A milestone is not complete until:
1. All defined tests for that milestone ran and evidence is saved
2. Zero unresolved critical or high security findings
3. Performance targets met (measured, not estimated)
4. Accessibility requirements met (automated + manual check documented)
5. Independent review complete for security-critical controls
6. Documentation updated
7. Known limitations explicitly recorded

**These gates are not negotiable. No milestone advances on claim alone.**

