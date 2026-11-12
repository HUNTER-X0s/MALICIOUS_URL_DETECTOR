"""Lexical and Structural URL Analyzer for URLSentinel.

Performs static feature extraction, Shannon entropy calculation, brand lookalike
similarity analysis, and suspicious token detection without active network I/O.
"""

import math
from dataclasses import dataclass, field
from typing import List, Dict, Any
from .url_normalizer import NormalizedURL

HIGH_VALUE_BRANDS = [
    "google",
    "microsoft",
    "apple",
    "amazon",
    "paypal",
    "netflix",
    "facebook",
    "instagram",
    "whatsapp",
    "chase",
    "wellsfargo",
    "bankofamerica",
    "citibank",
    "binance",
    "coinbase",
    "github",
    "dropbox",
    "adobe",
    "linkedin",
    "twitter",
    "steam",
]

KNOWN_URL_SHORTENERS = {
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "goo.gl",
    "ow.ly",
    "is.gd",
    "buff.ly",
    "adf.ly",
    "bit.do",
    "mcaf.ee",
    "rebrand.ly",
    "cutt.ly",
    "shorturl.at",
}

SUSPICIOUS_PATH_KEYWORDS = {
    "login",
    "signin",
    "sign-in",
    "log-in",
    "secure",
    "account",
    "verify",
    "verification",
    "update",
    "billing",
    "banking",
    "authenticate",
    "credential",
    "confirm",
    "wallet",
    "recover",
    "unlock",
    "webscr",
    "cmd=_login-run",
}


def calculate_entropy(text: str) -> float:
    """Calculate Shannon entropy for string randomness detection."""
    if not text:
        return 0.0
    freq: Dict[str, int] = {}
    for char in text:
        freq[char] = freq.get(char, 0) + 1
    entropy = 0.0
    text_len = len(text)
    for count in freq.values():
        p = count / text_len
        entropy -= p * math.log2(p)
    return round(entropy, 3)


def levenshtein_distance(s1: str, s2: str) -> int:
    """Compute the Levenshtein distance between two strings."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)

    previous_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


@dataclass
class LexicalSignals:
    url_length: int
    host_length: int
    path_depth: int
    query_param_count: int
    host_entropy: float
    digit_ratio: float
    is_ip_host: bool
    is_shortener: bool
    is_idn: bool
    subdomain_count: int
    suspicious_tokens_found: List[str] = field(default_factory=list)
    typosquat_matches: List[str] = field(default_factory=list)
    risk_score: int = 0
    anomalies: List[str] = field(default_factory=list)


def analyze_lexical(norm_url: NormalizedURL) -> LexicalSignals:
    """
    Extract structural and lexical features from a NormalizedURL.
    Calculates weighted risk score and anomalies list.
    """
    url_len = len(norm_url.normalized_url)
    host = norm_url.host
    host_len = len(host)
    path = norm_url.path
    
    # Path depth
    path_segments = [seg for seg in path.split("/") if seg]
    path_depth = len(path_segments)
    
    # Query count
    query_params = norm_url.query.split("&") if norm_url.query else []
    query_count = len([q for q in query_params if q])
    
    # Host entropy
    host_entropy = calculate_entropy(host)
    
    # Digit ratio in host
    digits = sum(1 for c in host if c.isdigit())
    alpha = sum(1 for c in host if c.isalpha())
    digit_ratio = round(digits / (digits + alpha), 3) if (digits + alpha) > 0 else 0.0
    
    # IP as host
    is_ip_host = False
    clean_host = host.strip("[]")
    parts = clean_host.split(".")
    if len(parts) == 4 and all(p.isdigit() and 0 <= int(p) <= 255 for p in parts):
        is_ip_host = True
    elif ":" in clean_host:
        is_ip_host = True
        
    # Shortener check
    is_shortener = host in KNOWN_URL_SHORTENERS
    
    # Subdomain depth
    subdomains = [s for s in norm_url.subdomain.split(".") if s]
    subdomain_count = len(subdomains)
    
    # Suspicious token extraction
    found_tokens: List[str] = []
    combined_path_query = (path + "?" + norm_url.query).lower()
    for token in SUSPICIOUS_PATH_KEYWORDS:
        if token in combined_path_query:
            found_tokens.append(token)
            
    # Typosquatting / lookalike analysis on registered domain label
    typosquats: List[str] = []
    domain_label = norm_url.registered_domain.split(".")[0] if norm_url.registered_domain else ""
    
    if domain_label:
        for brand in HIGH_VALUE_BRANDS:
            # Exact match with official brand is normal (unless subdomain abuse)
            if domain_label == brand:
                continue
            dist = levenshtein_distance(domain_label, brand)
            # Edit distance of 1 or 2 is a strong typosquatting indicator
            if dist in (1, 2) and abs(len(domain_label) - len(brand)) <= 2:
                typosquats.append(f"{brand} (distance: {dist})")
                
    # Calculate score & anomalies
    risk_score = 0
    anomalies: List[str] = []
    
    if is_ip_host:
        risk_score += 35
        anomalies.append("Hostname is a direct numeric IP address")
        
    if typosquats:
        risk_score += 40
        anomalies.append(f"Domain appears to impersonate brand: {', '.join(typosquats)}")
        
    if is_shortener:
        risk_score += 15
        anomalies.append("Uses generic URL shortener concealing actual destination")
        
    if norm_url.is_idn:
        risk_score += 25
        anomalies.append("Internationalized Domain Name (IDN/Punycode) detected (potential homoglyph)")
        
    if host_entropy > 4.2:
        risk_score += 20
        anomalies.append(f"High hostname Shannon entropy ({host_entropy}) indicates algorithmic generation")
        
    if digit_ratio > 0.4 and not is_ip_host:
        risk_score += 20
        anomalies.append(f"Abnormally high numeric character ratio ({digit_ratio * 100:.1f}%) in domain")
        
    if subdomain_count >= 3:
        risk_score += 15
        anomalies.append(f"Deep subdomain nesting ({subdomain_count} levels)")
        
    if found_tokens:
        risk_score += 10 * min(len(found_tokens), 3)
        anomalies.append(f"Suspicious security/credential tokens in path: {', '.join(found_tokens[:4])}")
        
    if url_len > 150:
        risk_score += 10
        anomalies.append(f"Excessive URL length ({url_len} characters)")
        
    # Cap risk score at 100
    risk_score = min(risk_score, 100)
    
    return LexicalSignals(
        url_length=url_len,
        host_length=host_len,
        path_depth=path_depth,
        query_param_count=query_count,
        host_entropy=host_entropy,
        digit_ratio=digit_ratio,
        is_ip_host=is_ip_host,
        is_shortener=is_shortener,
        is_idn=norm_url.is_idn,
        subdomain_count=subdomain_count,
        suspicious_tokens_found=found_tokens,
        typosquat_matches=typosquats,
        risk_score=risk_score,
        anomalies=anomalies,
    )

