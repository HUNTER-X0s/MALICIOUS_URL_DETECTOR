"""Verdict Generation and Multi-Signal Decision Engine for URLSentinel.

Aggregates lexical signals, threat intelligence feeds, DNS/TLS certificates,
homoglyph lookalikes, isolated scanner DOM analysis, and ML heuristic classifiers
into an explainable verdict with calibrated confidence and evidence attribution.
"""

import uuid
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict

from .url_normalizer import NormalizedURL
from .lexical_analyzer import LexicalSignals
from .ml_classifier import MLClassifier


@dataclass
class EvidenceRecord:
    id: str
    layer: str
    signal_name: str
    source: str
    observed_at: str
    freshness: str
    contribution: str  # CRITICAL, HIGH, MEDIUM, LOW, INFORMATIONAL
    description: str
    technical_details: Optional[Dict[str, Any]] = None


@dataclass
class TechnicalDetailsRecord:
    scheme: str
    host: str
    port: Optional[int]
    path: str
    query_params_count: int
    entropy: float
    is_ip_host: bool
    is_shortener: bool
    suspicious_tokens: List[str]
    typosquatting_matches: List[str]
    punycode: Optional[str] = None
    resolved_ips: Optional[List[str]] = None
    has_tls: bool = False
    tls_issuer: Optional[str] = None
    tls_days_remaining: Optional[int] = None
    ml_probability: Optional[float] = None
    ml_risk_band: Optional[str] = None


@dataclass
class VerdictOutput:
    id: str
    url: str
    url_hash: str
    verdict: str  # MALICIOUS, SUSPICIOUS, UNKNOWN, BENIGN
    status: str   # COMPLETED, PARTIAL, FAILED
    risk_score: int
    confidence: str  # LOW, MEDIUM, HIGH
    summary: str
    evidence: List[Dict[str, Any]]
    limitations: List[str]
    technical_details: Dict[str, Any]
    recommended_action: str
    checked_at: str
    expires_at: str
    contract_version: str = "1.0.0"


def evaluate_verdict(
    norm_url: NormalizedURL,
    lexical: LexicalSignals,
    resolved_ips: Optional[List[str]] = None,
    ti_matches: Optional[List[Dict[str, Any]]] = None,
    homoglyphs: Optional[List[Any]] = None,
    cert_details: Optional[Any] = None,
    scanner_result: Optional[Dict[str, Any]] = None,
    ml_prediction: Optional[Dict[str, Any]] = None,
    provider_errors: Optional[List[str]] = None,
) -> VerdictOutput:
    """
    Synthesize all signal layers into an honest, evidence-traced verdict.
    """
    now = datetime.now(timezone.utc)
    now_iso = now.isoformat()
    expires_iso = (now + timedelta(hours=24)).isoformat()
    scan_id = str(uuid.uuid4())

    evidence_list: List[EvidenceRecord] = []
    limitations: List[str] = [
        "Headless browser behavioral analysis is staged in isolated analysis worker.",
        "Reputation reflects feeds up to the last synchronization timestamp.",
    ]

    # 1. Evaluate Lexical & Structural Layer
    if lexical.anomalies:
        for idx, anomaly in enumerate(lexical.anomalies):
            evidence_list.append(
                EvidenceRecord(
                    id=f"ev_lex_{idx+1}",
                    layer="lexical",
                    signal_name="structural_anomaly",
                    source="URLSentinel Lexical Analyzer v1",
                    observed_at=now_iso,
                    freshness="realtime",
                    contribution="HIGH" if ("impersonate" in anomaly or "numeric IP" in anomaly) else "MEDIUM",
                    description=anomaly,
                )
            )

    # 2. Evaluate Homoglyph and Lookalike Matches
    if homoglyphs:
        for idx, (brand_key, brand_desc, detect_type) in enumerate(homoglyphs):
            evidence_list.append(
                EvidenceRecord(
                    id=f"ev_homo_{idx+1}",
                    layer="host_domain",
                    signal_name="brand_impersonation",
                    source="URLSentinel Homoglyph Engine",
                    observed_at=now_iso,
                    freshness="realtime",
                    contribution="CRITICAL" if "Homoglyph" in detect_type else "HIGH",
                    description=f"Deceptive mimicry targeting {brand_desc} via {detect_type}",
                )
            )

    # 3. Evaluate DNS / Resolved IPs
    if resolved_ips:
        evidence_list.append(
            EvidenceRecord(
                id="ev_dns_0",
                layer="dns",
                signal_name="destination_resolution",
                source="URLSentinel Safe DNS Resolver",
                observed_at=now_iso,
                freshness="realtime",
                contribution="INFORMATIONAL",
                description=f"Destination resolved to legitimate public address(es): {', '.join(resolved_ips[:3])}",
                technical_details={"ips": resolved_ips},
            )
        )
    else:
        limitations.append("DNS resolution was non-routable or destination was analyzed strictly statically.")

    # 4. Evaluate TLS Certificate
    has_tls = False
    tls_issuer = None
    tls_days_left = None

    if cert_details and cert_details.has_tls:
        has_tls = True
        tls_issuer = cert_details.issuer
        tls_days_left = cert_details.days_remaining

        if cert_details.is_expired:
            evidence_list.append(
                EvidenceRecord(
                    id="ev_tls_expired",
                    layer="tls",
                    signal_name="certificate_expired",
                    source="URLSentinel TLS Inspector",
                    observed_at=now_iso,
                    freshness="realtime",
                    contribution="HIGH",
                    description=f"TLS certificate expired ({cert_details.expires_at})",
                )
            )
        elif cert_details.is_valid:
            evidence_list.append(
                EvidenceRecord(
                    id="ev_tls_valid",
                    layer="tls",
                    signal_name="transport_encryption",
                    source="URLSentinel TLS Inspector",
                    observed_at=now_iso,
                    freshness="realtime",
                    contribution="INFORMATIONAL",
                    description=f"Valid TLS certificate issued by {tls_issuer} ({tls_days_left} days remaining). Note: TLS presence does not guarantee safe intent.",
                )
            )

    # 5. Evaluate Machine Learning & Heuristic Classification
    ml_eval = ml_prediction or MLClassifier.predict(norm_url.normalized_url)
    ml_prob = ml_eval.get("probability", 0.0)
    ml_band = ml_eval.get("risk_band", "LOW")

    if ml_band in ("CRITICAL", "HIGH"):
        top_reasons = "; ".join(ml_eval.get("top_indicators", [])) or "High statistical similarity to phishing datasets"
        evidence_list.append(
            EvidenceRecord(
                id="ev_ml_heuristic",
                layer="ml_statistical",
                signal_name="lexical_classifier_high_risk",
                source="URLSentinel Explainable ML Classifier v1",
                observed_at=now_iso,
                freshness="realtime",
                contribution="CRITICAL" if ml_prob >= 0.80 else "HIGH",
                description=f"Statistical ML heuristic identified high-risk indicators: {top_reasons}",
                technical_details={"probability": ml_prob, "risk_band": ml_band, "attributions": ml_eval.get("attributions")},
            )
        )
    elif ml_band == "ELEVATED":
        evidence_list.append(
            EvidenceRecord(
                id="ev_ml_heuristic",
                layer="ml_statistical",
                signal_name="lexical_classifier_elevated",
                source="URLSentinel Explainable ML Classifier v1",
                observed_at=now_iso,
                freshness="realtime",
                contribution="MEDIUM",
                description=f"Elevated lexical risk indicators detected ({int(ml_prob * 100)}% risk probability)",
                technical_details={"probability": ml_prob, "risk_band": ml_band},
            )
        )

    # 6. Evaluate Isolated Content / DOM Scan
    if scanner_result and scanner_result.get("scan_executed"):
        for idx, finding in enumerate(scanner_result.get("findings", [])):
            evidence_list.append(
                EvidenceRecord(
                    id=f"ev_content_{idx+1}",
                    layer="content_dom",
                    signal_name="dom_content_anomaly",
                    source="URLSentinel Isolated Scanner",
                    observed_at=now_iso,
                    freshness="realtime",
                    contribution=scanner_result.get("risk_contribution", "HIGH"),
                    description=finding,
                    technical_details=scanner_result.get("detected_features"),
                )
            )

    # 7. Evaluate Threat Intelligence Matches
    if ti_matches:
        for idx, match in enumerate(ti_matches):
            evidence_list.append(
                EvidenceRecord(
                    id=f"ev_ti_{idx+1}",
                    layer="threat_intel",
                    signal_name=match.get("threat_type", "known_malicious"),
                    source=match.get("source", "Threat Intelligence Feed"),
                    observed_at=match.get("reported_at", now_iso),
                    freshness=match.get("freshness", "< 24h"),
                    contribution="CRITICAL",
                    description=match.get("details", "Verified match in active malicious URL blacklist"),
                    technical_details={"reference": match.get("reference")},
                )
            )

    # 8. Handle Provider Outages / Errors
    has_provider_errors = bool(provider_errors)
    if has_provider_errors:
        for err in provider_errors:
            limitations.append(f"External feed connection degraded: {err}")

    # 9. Synthesize Risk Score & Final Decision Logic
    risk_score = lexical.risk_score
    if homoglyphs:
        risk_score = max(risk_score, 85)
    if cert_details and cert_details.is_expired:
        risk_score = min(risk_score + 30, 100)
    
    # Factor in ML probability
    ml_score = int(ml_prob * 100)
    if ml_score > risk_score:
        risk_score = max(risk_score, ml_score)

    if scanner_result and scanner_result.get("scan_executed"):
        contrib = scanner_result.get("risk_contribution")
        if contrib == "CRITICAL":
            risk_score = max(risk_score, 92)
        elif contrib == "HIGH":
            risk_score = max(risk_score, 75)

    status = "COMPLETED"

    # Rule A: Definite Threat Intel match -> MALICIOUS
    if ti_matches:
        verdict = "MALICIOUS"
        risk_score = max(risk_score, 94)
        confidence = "HIGH"
        summary = f"Confirmed threat detected in {ti_matches[0].get('source', 'threat intelligence')}: {ti_matches[0].get('threat_type', 'malicious')}"
        action = "Do not proceed. This link is actively distributed in credential phishing or malware operations."

    # Rule B: Homoglyph or High-confidence typosquatting lure -> MALICIOUS
    elif homoglyphs and (lexical.is_ip_host or lexical.suspicious_tokens_found or "Homoglyph" in str(homoglyphs)):
        verdict = "MALICIOUS"
        risk_score = max(risk_score, 90)
        confidence = "HIGH"
        target_name = homoglyphs[0][1]
        summary = f"Deceptive brand impersonation attempting to mimic {target_name}."
        action = "Block navigation. Destination is deliberately mimicking an established service to deceive visitors."

    # Rule C: Critical DOM scan finding (e.g. external credential form post) -> MALICIOUS
    elif scanner_result and scanner_result.get("risk_contribution") == "CRITICAL":
        verdict = "MALICIOUS"
        risk_score = max(risk_score, 92)
        confidence = "HIGH"
        summary = "Active credential harvesting or malicious DOM manipulation identified by isolated scanner."
        action = "Block navigation. Page attempts to exfiltrate submitted credentials to unauthorized third parties."

    # Rule D: Extreme ML phishing probability (>= 80%) with deceptive patterns -> MALICIOUS
    elif ml_prob >= 0.80 and (lexical.is_ip_host or lexical.suspicious_tokens_found or lexical.is_shortener):
        verdict = "MALICIOUS"
        risk_score = max(risk_score, 88)
        confidence = "HIGH"
        summary = f"High-confidence phishing pattern identified: {ml_eval.get('top_indicators', ['Structural lure'])[0]}"
        action = "Block navigation. Destination characteristics closely align with fraudulent phishing attacks."

    # Rule E: Suspicious threshold
    elif risk_score >= 45:
        verdict = "SUSPICIOUS"
        confidence = "MEDIUM"
        summary = "Multiple anomalous indicators detected. Destination structure matches known lure patterns."
        action = "Exercise strong caution. Avoid submitting passwords, MFA codes, or financial details."

    # Rule F: Provider errors with inconclusive signals -> UNKNOWN (NEVER BENIGN)
    elif has_provider_errors:
        verdict = "UNKNOWN"
        status = "PARTIAL"
        confidence = "LOW"
        risk_score = max(risk_score, 30)
        summary = "Inconclusive assessment due to upstream intelligence provider failure."
        action = "Proceed with caution. Threat intelligence validation was incomplete."

    # Rule G: High entropy domain without positive hits -> UNKNOWN
    elif lexical.host_entropy > 4.0 and not lexical.typosquat_matches:
        verdict = "UNKNOWN"
        confidence = "LOW"
        summary = "Insufficient historical threat data on this domain. No explicit threat detected, but safety cannot be guaranteed."
        action = "Verify link authenticity through trusted official channels before interacting."

    # Rule H: Clean structure & low risk score -> BENIGN with caveats
    else:
        verdict = "BENIGN"
        confidence = "MEDIUM"
        summary = "No known malicious signatures or deceptive structural indicators were detected."
        action = "No active threats detected in cataloged datasets. Always verify unfamiliar origins."

    tech_details = TechnicalDetailsRecord(
        scheme=norm_url.scheme,
        host=norm_url.host,
        port=norm_url.port,
        path=norm_url.path,
        query_params_count=lexical.query_param_count,
        entropy=lexical.host_entropy,
        is_ip_host=lexical.is_ip_host,
        is_shortener=lexical.is_shortener,
        suspicious_tokens=lexical.suspicious_tokens_found,
        typosquatting_matches=lexical.typosquat_matches,
        punycode=norm_url.punycode_host if norm_url.is_idn else None,
        resolved_ips=resolved_ips,
        has_tls=has_tls,
        tls_issuer=tls_issuer,
        tls_days_remaining=tls_days_left,
        ml_probability=ml_prob,
        ml_risk_band=ml_band,
    )

    return VerdictOutput(
        id=scan_id,
        url=norm_url.normalized_url,
        url_hash=norm_url.url_hash,
        verdict=verdict,
        status=status,
        risk_score=risk_score,
        confidence=confidence,
        summary=summary,
        evidence=[asdict(e) for e in evidence_list],
        limitations=limitations,
        technical_details=asdict(tech_details),
        recommended_action=action,
        checked_at=now_iso,
        expires_at=expires_iso,
    )
