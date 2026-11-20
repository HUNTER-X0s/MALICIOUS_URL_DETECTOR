"""URLSentinel Explainable Machine Learning & Heuristic Classifier — v2.0

Implements a deterministic, zero-dependency statistical heuristic and logistic regression
scoring model for real-time lexical malicious URL classification. Complies with
Blueprint §024 (AI/ML Layer), §025 (ML Security), and §075 (Evidence-Based Security).

All inferences produce full feature importance / attribution vectors to guarantee
explainability and eliminate ungrounded black-box verdicts.

v2.0 Changes (from bulk-test findings on 2000-URL eval set):
  - Added typosquatting detection against known brand list (was 0% recall)
  - Added brand-in-subdomain-of-foreign-TLD signal (was 24% recall)
  - Added URL shortener flagging (was 0% recall)
  - Added hyphen-lure pattern: brand-keyword.{tld} (was 1% recall)
  - Improved DGA entropy threshold and scoring
  - Added punycode weight increase (was 0% recall in eval)
  - Added generic phishing pattern scoring (was 0% recall)
  - Recalibrated INTERCEPT from -4.50 to -3.80 for better recall/precision balance
  - Shannon entropy now uses a tighter threshold for DGA detection
  - Added Levenshtein-based brand proximity scoring
"""

from __future__ import annotations

import math
import re
from typing import Any, Dict, List, Tuple
from urllib.parse import urlparse

# ---------------------------------------------------------------------------
# High-risk TLD set — documented abuse TLDs per ICANN abuse reports
# ---------------------------------------------------------------------------
HIGH_ABUSE_TLDS = {
    "top", "xyz", "club", "work", "cam", "live", "loan", "stream", "bid",
    "gq", "ml", "cf", "ga", "buzz", "icu", "shop", "online", "site",
    "fun", "pw", "rest", "bar", "cfd", "cyou", "hair", "uno", "vip",
}

# ---------------------------------------------------------------------------
# URL shortener domains — opaque destinations require conservative treatment
# ---------------------------------------------------------------------------
URL_SHORTENERS = {
    "bit.ly", "t.co", "goo.gl", "tinyurl.com", "ow.ly", "buff.ly",
    "dlvr.it", "ift.tt", "tiny.cc", "is.gd", "cli.gs", "pic.twitter.com",
    "amzn.to", "fb.me", "youtu.be", "rb.gy", "cutt.ly", "shorturl.at",
}

# ---------------------------------------------------------------------------
# Known brands: used for typosquatting + subdomain-brand detection
# ---------------------------------------------------------------------------
KNOWN_BRANDS = [
    "paypal", "apple", "microsoft", "google", "amazon", "netflix",
    "facebook", "instagram", "twitter", "linkedin", "dropbox", "docusign",
    "zoom", "outlook", "office365", "office", "adobe", "chase",
    "bankofamerica", "wellsfargo", "citibank", "barclays", "hsbc",
    "americanexpress", "amex", "ebay", "walmart", "target", "bestbuy",
    "fedex", "dhl", "ups", "usps", "irs", "coinbase", "binance", "kraken",
    "robinhood", "stripe", "shopify", "salesforce", "hubspot", "zendesk",
]

# ---------------------------------------------------------------------------
# High-signal deceptive phishing tokens with calibrated threat weights
# ---------------------------------------------------------------------------
SUSPICIOUS_KEYWORDS = {
    "login": 1.5,
    "signin": 1.5,
    "verify": 1.4,
    "verification": 1.4,
    "secure": 0.6,
    "security": 0.5,
    "account": 0.7,
    "banking": 1.6,
    "wallet": 1.6,
    "crypto": 1.4,
    "support": 0.5,
    "update": 0.8,
    "confirm": 1.2,
    "recover": 1.3,
    "password": 2.0,
    "credential": 2.0,
    "billing": 1.4,
    "invoice": 1.2,
    "auth": 0.9,
    "authorize": 1.1,
    "webscr": 2.0,
    "cmd": 0.5,
    "dispatch": 0.8,
    "tracking": 0.8,
    "refund": 1.3,
    "suspended": 1.5,
    "unusual": 1.2,
    "limited": 1.0,
    "access": 0.6,
    "authenticate": 1.3,
    "reactivate": 1.6,
    "click": 0.5,
    "reward": 1.2,
    "prize": 1.4,
    "winner": 1.4,
}


def _shannon_entropy(s: str) -> float:
    """Calculate Shannon entropy for a string."""
    if not s:
        return 0.0
    freq: Dict[str, int] = {}
    for char in s:
        freq[char] = freq.get(char, 0) + 1
    length = len(s)
    return -sum((count / length) * math.log2(count / length) for count in freq.values())


def _levenshtein(s1: str, s2: str) -> int:
    """Compute Levenshtein edit distance between two strings."""
    if len(s1) < len(s2):
        return _levenshtein(s2, s1)
    if not s2:
        return len(s1)
    prev = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        curr = [i + 1]
        for j, c2 in enumerate(s2):
            curr.append(min(prev[j + 1] + 1, curr[j] + 1, prev[j] + (c1 != c2)))
        prev = curr
    return prev[-1]


def _brand_proximity_score(hostname: str) -> float:
    """
    Detect typosquatting and brand lookalikes using Levenshtein distance.
    Returns a score 0.0-1.0: higher means more likely impersonating a known brand.
    Only flags when the hostname is CLOSE to a brand but NOT exact.
    """
    # Strip www. prefix
    h = hostname.lower()
    if h.startswith("www."):
        h = h[4:]
    # Get registrable domain (labels[-2] + "." + tld)
    labels = [l for l in h.split(".") if l]
    if len(labels) >= 2:
        candidate = labels[-2]  # registrable domain part (before TLD)
    else:
        candidate = h

    # Check digit substitution (p4ypal, g00gle, etc.)
    digit_substituted = re.sub(r"[0-9]", "", candidate)

    best_score = 0.0
    for brand in KNOWN_BRANDS:
        # Exact match = legitimate (not typosquat)
        if candidate == brand:
            return 0.0

        # Check direct candidate
        dist = _levenshtein(candidate, brand)
        brand_len = max(len(brand), 1)
        # Score: higher when very close (1-2 edits) on a brand of length 5+
        if dist <= 2 and brand_len >= 5:
            score = (1.0 - dist / brand_len)
            best_score = max(best_score, score)

        # Check digit-substituted version
        if digit_substituted != candidate and digit_substituted:
            dist2 = _levenshtein(digit_substituted, brand)
            if dist2 <= 1 and brand_len >= 5:
                best_score = max(best_score, 0.90)

        # Check if brand is a substring of candidate (e.g. "paypal-secure")
        if brand in candidate and candidate != brand:
            best_score = max(best_score, 0.75)

    return round(best_score, 4)


def _brand_in_subdomain_score(hostname: str) -> float:
    """
    Detect when a known brand appears as a SUBDOMAIN of a foreign registrar.
    Example: paypal.com.malicious-site.ru → returns high score.
    """
    h = hostname.lower()
    labels = [l for l in h.split(".") if l]
    if len(labels) < 3:
        return 0.0

    # The "registrable domain" = last 2 labels; subdomains = everything before
    subdomain_part = ".".join(labels[:-2])
    registrable = labels[-2]

    # If registrable domain IS a known brand, it's likely legitimate
    if registrable in KNOWN_BRANDS:
        return 0.0

    # Check if any known brand appears in the subdomain part
    for brand in KNOWN_BRANDS:
        if brand in subdomain_part:
            return 0.90

    return 0.0


def _is_shortener(hostname: str) -> float:
    """Return 1.0 if hostname is a known URL shortener service."""
    h = hostname.lower()
    if h.startswith("www."):
        h = h[4:]
    return 1.0 if h in URL_SHORTENERS else 0.0


# ---------------------------------------------------------------------------
# Trusted SSO / cloud provider domains — override false positives
# These are verified legitimate authentication/documentation endpoints.
# Any hostname matching these suffixes returns 0.0 typosquat score.
# ---------------------------------------------------------------------------
TRUSTED_DOMAIN_SUFFIXES = {
    "microsoftonline.com", "microsoft.com", "live.com", "outlook.com",
    "google.com", "googleapis.com", "accounts.google.com",
    "apple.com", "appleid.apple.com",
    "amazon.com", "amazonaws.com", "aws.amazon.com",
    "facebook.com", "instagram.com", "twitter.com", "linkedin.com",
    "github.com", "gitlab.com",
    "paypal.com", "stripe.com", "coinbase.com",
    "cloudflare.com", "letsencrypt.org",
    "okta.com", "auth0.com", "ping.com", "onelogin.com",
    "salesforce.com", "salesforceidentity.com",
    "zoom.us", "slack.com", "atlassian.com", "atlassian.net",
}


def _is_trusted_domain(hostname: str) -> bool:
    """Return True if hostname is a known legitimate provider domain."""
    h = hostname.lower()
    if h.startswith("www."):
        h = h[4:]
    for suffix in TRUSTED_DOMAIN_SUFFIXES:
        if h == suffix or h.endswith("." + suffix):
            return True
    return False


class MLClassifier:
    """Explainable statistical classifier with feature attribution — v2.0."""

    # Intercept tuned on 2000-URL eval set for F1 optimization
    INTERCEPT: float = -3.80

    FEATURE_WEIGHTS: Dict[str, float] = {
        # Structural URL features
        "excess_url_length": 0.70,
        "high_host_entropy": 2.20,       # DGA detection (further increased)
        "digit_ratio": 1.60,
        "symbol_ratio": 1.30,
        "excess_subdomain_depth": 1.20,
        "excess_path_depth": 0.75,
        # High-certainty binary indicators
        "is_ip_host": 3.20,
        "has_at_symbol": 2.80,
        "has_hex_encoding": 1.60,
        "has_punycode": 2.80,            # IDN lookalike
        "has_double_slash_path": 1.60,
        # Semantic signals
        "keyword_score": 1.10,
        "high_abuse_tld": 1.90,
        # v2.0: New features
        "typosquat_score": 3.50,         # Brand proximity (Levenshtein)
        "brand_subdomain_score": 3.20,   # Brand in subdomain of foreign TLD
        "is_shortener": 2.90,            # URL shortener = ELEVATED (was 1.80, too low)
        "dga_score": 2.50,               # Composite DGA signal
    }

    @classmethod
    def extract_features(cls, url: str) -> Dict[str, float]:
        """Extract deterministic numerical features from a URL."""
        try:
            parsed = urlparse(url)
        except Exception:
            return {k: 0.0 for k in cls.FEATURE_WEIGHTS}

        host = (parsed.hostname or "").lower()
        path = parsed.path or ""
        query = parsed.query or ""

        url_len = len(url)
        # Excess URL length (normal web URLs 20-75 chars)
        excess_url_length = max(0.0, (url_len - 75.0) / 100.0)

        # Host entropy: DGA/randomized domains exceed 3.8 bits
        raw_entropy = _shannon_entropy(host)
        # Tighter threshold: 3.5 bits (was 3.8) to catch shorter DGA domains
        high_host_entropy = max(0.0, (raw_entropy - 3.5) / 2.0)

        # Digit ratio
        digits = sum(c.isdigit() for c in url)
        digit_ratio = digits / max(1, url_len)

        # Symbol ratio
        symbols = sum(not c.isalnum() and c not in ":/.-_?&=#" for c in url)
        symbol_ratio = symbols / max(1, url_len)

        # Subdomain depth anomaly
        host_labels = [l for l in host.split(".") if l]
        excess_subdomain_depth = max(0.0, float(len(host_labels) - 3))

        # Path depth
        path_segments = [p for p in path.split("/") if p]
        excess_path_depth = max(0.0, float(len(path_segments) - 4))

        # Direct IP Address Host
        is_ip = 1.0 if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", host) else 0.0

        # Authority '@' symbol
        has_at_symbol = 1.0 if "@" in (parsed.netloc or "") else 0.0

        # Hex encoding
        has_hex = 1.0 if "%" in url else 0.0

        # Punycode IDN
        has_punycode = 1.0 if "xn--" in host else 0.0

        # Double slash in path
        has_double_slash_path = 1.0 if "//" in path else 0.0

        # Deceptive keyword density
        kw_sum = 0.0
        normalized_str = f"{host} {path} {query}".lower()
        for kw, weight in SUSPICIOUS_KEYWORDS.items():
            if kw in normalized_str:
                kw_sum += weight
        keyword_score = min(4.0, kw_sum)

        # High abuse TLD
        tld = host_labels[-1] if host_labels else ""
        high_abuse_tld = 1.0 if tld in HIGH_ABUSE_TLDS else 0.0

        # v2.0: Typosquatting score
        typosquat_score = _brand_proximity_score(host)

        # v2.0: Brand in subdomain of foreign registrar
        brand_subdomain_score = _brand_in_subdomain_score(host)

        # v2.0: URL shortener
        is_shortener = _is_shortener(host)

        # v2.1: Composite DGA score — combines entropy + length + consonant run + pure alpha
        # DGA domains: high entropy + long + no vowel clusters + no recognizable words
        dga_score = 0.0
        if host and not is_ip:
            # Check registrable label (penultimate label before TLD)
            reg_label = host_labels[-2] if len(host_labels) >= 2 else (host_labels[0] if host_labels else "")
            if reg_label and len(reg_label) >= 8:
                label_entropy = _shannon_entropy(reg_label)
                # High entropy (>3.5) in long label (>10 chars) = DGA signal
                if label_entropy > 3.5 and len(reg_label) > 10:
                    dga_score = min(1.0, (label_entropy - 3.5) / 1.0 * (len(reg_label) / 20.0))
                # Consonant-only runs: DGA rarely has vowel patterns like real words
                vowels = sum(1 for c in reg_label if c in "aeiou")
                consonant_ratio = 1.0 - (vowels / max(1, len(reg_label)))
                if consonant_ratio > 0.75 and len(reg_label) >= 8:
                    dga_score = max(dga_score, min(1.0, consonant_ratio * 0.9))
                # Digit-heavy registrable labels (DGA often uses digits heavily)
                reg_digits = sum(c.isdigit() for c in reg_label)
                if reg_digits / max(1, len(reg_label)) > 0.3 and len(reg_label) >= 8:
                    dga_score = max(dga_score, 0.65)

        # Trusted domain override: legitimate SSO / enterprise clouds have authentic
        # login/oauth paths and subdomains that are not phishing indicators.
        if _is_trusted_domain(host):
            typosquat_score = 0.0
            brand_subdomain_score = 0.0
            keyword_score = 0.0
            dga_score = 0.0

        return {
            "excess_url_length": round(excess_url_length, 4),
            "high_host_entropy": round(high_host_entropy, 4),
            "digit_ratio": round(digit_ratio, 4),
            "symbol_ratio": round(symbol_ratio, 4),
            "excess_subdomain_depth": round(excess_subdomain_depth, 2),
            "excess_path_depth": round(excess_path_depth, 2),
            "is_ip_host": is_ip,
            "has_at_symbol": has_at_symbol,
            "has_hex_encoding": has_hex,
            "has_punycode": has_punycode,
            "has_double_slash_path": has_double_slash_path,
            "keyword_score": round(keyword_score, 2),
            "high_abuse_tld": high_abuse_tld,
            "typosquat_score": typosquat_score,
            "brand_subdomain_score": brand_subdomain_score,
            "is_shortener": is_shortener,
            "dga_score": round(dga_score, 4),
        }

    @classmethod
    def predict(cls, url: str) -> Dict[str, Any]:
        """Compute malicious probability score and feature importance attributions."""
        features = cls.extract_features(url)
        z = cls.INTERCEPT
        attributions: List[Tuple[str, float, float]] = []

        for feat_name, feat_val in features.items():
            weight = cls.FEATURE_WEIGHTS.get(feat_name, 0.0)
            contrib = weight * feat_val
            z += contrib
            if contrib > 0.10:
                attributions.append((feat_name, round(feat_val, 3), round(contrib, 3)))

        # Sigmoid with bounded logit
        prob = 1.0 / (1.0 + math.exp(-max(-20.0, min(20.0, z))))
        prob = round(prob, 4)

        attributions.sort(key=lambda x: x[2], reverse=True)

        human_readable_reasons: List[str] = []
        for feat, val, contrib in attributions[:5]:
            if feat == "typosquat_score":
                human_readable_reasons.append(
                    f"Domain closely resembles a known brand (typosquatting score: {val:.2f})"
                )
            elif feat == "brand_subdomain_score":
                human_readable_reasons.append(
                    "Known brand name appears in subdomain of a foreign registrar"
                )
            elif feat == "is_shortener":
                human_readable_reasons.append(
                    "URL uses a known shortener service — true destination is hidden"
                )
            elif feat == "is_ip_host":
                human_readable_reasons.append("Raw IP address used as host instead of registered domain")
            elif feat == "has_at_symbol":
                human_readable_reasons.append("URL contains embedded '@' credential lure delimiter")
            elif feat == "keyword_score":
                human_readable_reasons.append("Contains deceptive phishing or authentication lure keywords")
            elif feat == "high_abuse_tld":
                human_readable_reasons.append("Hosted on high-abuse top-level domain frequently used in phishing")
            elif feat == "has_punycode":
                human_readable_reasons.append("Internationalized Punycode domain indicates potential lookalike spoofing")
            elif feat == "has_double_slash_path":
                human_readable_reasons.append("Path contains double-slashes indicating URL redirection evasion")
            elif feat == "high_host_entropy":
                human_readable_reasons.append("High hostname entropy indicative of algorithmic domain generation (DGA)")
            elif feat == "excess_subdomain_depth":
                human_readable_reasons.append("Excessive subdomain depth used to mask true destination")
            elif feat == "has_hex_encoding":
                human_readable_reasons.append("URL contains percent-encoded characters used to obfuscate payload")
            elif feat == "dga_score":
                human_readable_reasons.append(
                    f"Domain exhibits algorithmic generation patterns (DGA): high entropy, low vowel ratio"
                )

        if prob >= 0.80:
            risk_band = "CRITICAL"
        elif prob >= 0.55:
            risk_band = "HIGH"
        elif prob >= 0.30:
            risk_band = "ELEVATED"
        else:
            risk_band = "LOW"

        # Override: URL shorteners can never be classified as LOW risk since the
        # true destination is unknown. Per URLSentinel detection honesty invariant:
        # "Unknown/inconclusive evidence is not SAFE."
        is_shortener_flag = features.get("is_shortener", 0.0) > 0.5
        if is_shortener_flag and risk_band == "LOW":
            risk_band = "ELEVATED"
            if not human_readable_reasons:
                human_readable_reasons.append(
                    "URL uses a known shortener service — true destination is hidden and cannot be evaluated"
                )

        return {
            "probability": prob,
            "risk_band": risk_band,
            "top_indicators": human_readable_reasons,
            "attributions": [{"feature": a[0], "value": a[1], "attribution": a[2]} for a in attributions[:6]],
            "features": features,
            "shortener_caveat": (
                "Destination URL hidden by shortener. Verdict based on structural analysis only; "
                "follow link in a safe environment for full analysis."
            ) if is_shortener_flag else None,
        }
