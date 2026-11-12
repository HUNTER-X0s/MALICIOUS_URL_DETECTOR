# URLSentinel — Detection Strategy (M0)

**Date:** 2026-11-03  
**Status:** Initial strategy — refine with provider research and evaluation data in M5+  
**Reference:** `docs/05-detection/DETECTION_TAXONOMY.md`, `docs/05-detection/VERDICT_STATE_MACHINE.md`, `docs/05-detection/EVALUATION_AND_METRICS.md`

---

## 1. Detection pipeline overview

URLSentinel uses **layered, evidence-traced detection** with explicit uncertainty. No single signal is authoritative. Every verdict is explainable through a chain from verdict → signals → evidence → sources → timestamp.

### Core invariants
- **UNKNOWN is valid.** Absence of known threats is not proof of safety.
- **HTTPS ≠ Safe.** TLS presence is never a positive safety signal.
- **Provider failure → UNKNOWN.** Never coerce to BENIGN on timeout/outage.
- **Staleness → UNKNOWN.** Expired cached verdicts must not serve as current assessments.
- **One source is never sufficient** for MALICIOUS verdict (except very high-confidence feeds with corroboration).

---

## 2. Layered signal groups

| Layer | Signals | Network required | Latency | Milestone |
|---|---|---|---|---|
| 1. Exact reputation | URL/domain/IP hash lookup in TI cache | Redis (no external) | <5ms | M5 |
| 2. Scheme/structure | Scheme, port, IP-literal, format validity | None | <1ms | M4 |
| 3. Lexical/structural | URL length, entropy, path depth, suspicious patterns, encoded content, parameter count | None | <10ms | M4 |
| 4. Host/domain lexical | Typosquatting similarity (Levenshtein/DL), IDN/Punycode confusables, brand token matching, subdomain depth | None | <20ms | M4/M8 |
| 5. DNS/infrastructure | A/AAAA record resolution, domain age (where available), ASN reputation, NS patterns | DNS query | 50–200ms | M6 |
| 6. TLS/certificate | Certificate validity, age, issuer, hostname coverage, CT presence, chain depth | TLS handshake (no content) | 100–500ms | M6 |
| 7. TI provider lookup | Google Web Risk, URLhaus, PhishTank, OpenPhish (licensed) | HTTPS to provider | 100–500ms | M5 |
| 8. ML model | Lexical model, domain features, graph features | None (model inference) | 10–100ms | M8+ |
| 9. Deep content (scanner) | DOM analysis, form detection, script analysis, behavior | Full HTTP + browser | 5–60s | M9+ |

---

## 3. Verdict state machine

### Scan execution states (separate from threat verdict)
```
QUEUED → RUNNING → COMPLETED
                  → PARTIAL (some signals unavailable)
                  → FAILED
        → EXPIRED (result too old, re-scan needed)
        → CANCELLED
```

### Threat verdict states
```
MALICIOUS     — confirmed threat indicator from high-confidence source(s)
SUSPICIOUS    — signals suggest risk but evidence insufficient for MALICIOUS
UNKNOWN       — insufficient evidence; never coerce this to BENIGN
BENIGN        — available evidence found no threat indicators; not a guarantee of safety
UNDER_REVIEW  — human analyst has the case; verdict pending
FALSE_POSITIVE — previously flagged, now verified as legitimate
```

> [!IMPORTANT]
> Verdict labels require a formal ADR (ADR-004) before any code is written. The exact public-facing labels, internal representations, and API schema must be frozen before M4 implementation.

### Verdict assignment rules
| Condition | Verdict |
|---|---|
| High-confidence TI provider + corroborated signal | MALICIOUS |
| Single TI provider match, unconfirmed | SUSPICIOUS |
| Multiple suspicious lexical signals, no TI match | SUSPICIOUS |
| No TI match, no suspicious signals, evidence checked | BENIGN (with limitations noted) |
| Provider timeout/error, no cached verdict | UNKNOWN |
| Stale cached verdict (> TTL) | UNKNOWN (re-scan triggered) |
| Unsupported scheme or unparseable URL | UNKNOWN (with explanation) |
| All signals inconclusive | UNKNOWN |
| Human analyst assigned | UNDER_REVIEW |

---

## 4. Evidence and explainability

Every verdict must include:
```json
{
  "verdict": "SUSPICIOUS",
  "risk_score": 65,
  "confidence": "MEDIUM",
  "evidence": [
    {
      "signal": "newly_registered_domain",
      "source": "WHOIS_PROVIDER",
      "observed": "2026-10-30",
      "freshness": "48h",
      "contribution": "HIGH"
    },
    {
      "signal": "phishtank_match",
      "source": "PhishTank",
      "observed": "2026-10-31",
      "freshness": "24h",
      "contribution": "HIGH"
    }
  ],
  "limitations": ["Content analysis not available", "ML model not yet deployed"],
  "recommended_action": "Do not enter credentials. Verify the destination through a trusted source.",
  "checked_at": "2026-11-03T02:00:00Z",
  "expires_at": "2026-11-04T02:00:00Z",
  "contract_version": "v1"
}
```

**Plain-language explanation requirements:**
- Non-expert friendly: no jargon unless "technical details" is explicitly expanded
- What was checked ✓
- What was not checked (limitations) ✓
- What the user should do ✓
- What information may be at risk ✓
- Which sources flagged it (without revealing evasion-enabling heuristics) ✓

---

## 5. Threat intelligence source governance

| Provider | Use case | License status | Terms to verify |
|---|---|---|---|
| Google Web Risk | Malware, social engineering, unwanted software | **Commercial available** — MUST replace Safe Browsing for commercial use | API costs, quota, data usage rights |
| Google Safe Browsing | Same as above | **Non-commercial only** — do not use in commercial product | See terms |
| PhishTank | Phishing URLs | Unknown for commercial — must verify | phishtank.org/api_info.php |
| URLhaus | Malware URLs | Must verify commercial terms | urlhaus.abuse.ch/api/ |
| OpenPhish | Phishing feeds | Premium tier for commercial; free tier limited | openphish.com pricing |
| VirusTotal | Multi-engine verdicts | Must verify commercial terms; QUOTA limits strict | virustotal.com API terms |
| Spamhaus | Spam/malware domains | Must verify commercial terms | spamhaus.org terms |

> [!CAUTION]
> **No threat intelligence provider should be integrated before commercial licensing is verified.** Google Safe Browsing is explicitly documented as non-commercial. Using it in a commercial product is a terms violation.

### Feed freshness requirements
| Provider | Maximum staleness allowed | Stale behavior |
|---|---|---|
| Any TI provider | 24 hours | Mark source STALE; do not count as confirming evidence; UNKNOWN if only source |
| Phishing-specific feeds | 6 hours | Phishing campaigns are short-lived |
| Malware feeds | 24 hours | Malware infrastructure changes more slowly |
| Community reports | 1 hour | Verify before counting |

---

## 6. ML strategy (M8+)

> [!NOTE]
> ML is deferred until M8. Rules-based detection and TI reputation must be established first. ML is only justified when a labeled dataset is available, baseline performance is measured, and operational ML infrastructure can support it.

**Pre-conditions for ML (must all be met):**
1. Licensed labeled dataset (no scraped/unlicensed training data)
2. Domain-grouped train/test split (not random split — domains must not leak between train and test)
3. Time-based evaluation (train on earlier data, test on later)
4. Baseline rules performance measured (recall, precision, F1)
5. MLOps infrastructure for reproducible training, versioning, deployment
6. Calibration methodology (Platt scaling or isotonic regression for confidence)
7. Adversarial robustness evaluation (evasion test corpus)
8. Operational plan for model drift monitoring and retraining

**Candidate model approaches (in order of complexity):**
1. Logistic regression on lexical features (interpretable, fast, good baseline)
2. Random Forest / Gradient Boosting (LightGBM) for non-linear lexical + domain features
3. Character-level CNN/LSTM for URL sequence patterns
4. Ensemble: rules + TI + ML with calibrated combination
5. Transformer-based only if prior approaches have measurable gap and training data supports it

**ML security requirements:**
- Domain-grouped splits prevent train/test leakage
- Out-of-distribution testing for novel attack patterns
- Adversarial test corpus (crafted evasion URLs)
- Poisoning evaluation before deployment
- Distribution shift monitoring post-deployment
- Model rollback capability

---

## 7. False positive and false negative measurement

**Definitions:**
- **False positive (FP):** Legitimate URL classified as MALICIOUS or SUSPICIOUS
- **False negative (FN):** Malicious URL classified as BENIGN or UNKNOWN

**FP cost:** Loss of user trust; false reports of legitimate businesses; legal exposure
**FN cost:** User harmed by malicious URL; reputation damage; regulatory scrutiny

**Measurement methodology:**
- Maintain a curated labeled evaluation dataset (synthetic + adjudicated real examples)
- Evaluate FP rate and FN rate separately per signal layer and aggregate
- Track FP reports submitted by users (false-positive rate from production)
- Target (initial, to be calibrated):
  - FP rate on Alexa/Tranco top-1M domains: < 0.1%
  - FN rate on PhishTank/URLhaus verified positives: < 15% (expected without deep scanner)
  - Precision for MALICIOUS verdict: > 90% (high confidence in what we flag)
  - Recall for MALICIOUS verdict: > 75% at MALICIOUS threshold (understood gap; SUSPICIOUS catches borderline)

> [!WARNING]
> These are initial unvalidated targets. They must be calibrated against actual data in M4–M5. Do not publish these numbers as performance claims.

---

## 8. Evaluation and regression testing

**Required evaluation framework (M4):**
- Synthetic fixture corpus: crafted URLs covering each threat category (created without real malicious content; labeled manually)
- Adjudicated corpus: verified true positives from licensed feeds; verified true negatives from top-domain lists
- Regression tests: each merged change must not regress recall/precision by > 2% on the evaluation set
- Adversarial corpus: crafted evasion examples (encoded, IDN, IP-literal, redirect variations)
- Provider outage simulation: verify UNKNOWN (not BENIGN) is returned on feed failure

**Evaluation format:**
```
Evaluation date: YYYY-MM-DD
Dataset version: v1.2
Commit: abc1234
Precision@MALICIOUS: 92.3%
Recall@MALICIOUS: 71.4%
FP rate on top-1M: 0.08%
UNKNOWN rate: 24.1%
Provider outage → BENIGN coercion: 0 (PASS)
Stale feed → BENIGN coercion: 0 (PASS)
```

