"""Homoglyph, Unicode Confusable, and Brand Impersonation Subsystem for URLSentinel."""

import unicodedata
from typing import Dict, List, Tuple, Set

# Top high-value targeted brands globally
TARGET_BRANDS: Dict[str, str] = {
    # Tech & Cloud
    "google": "Google Services",
    "microsoft": "Microsoft 365 / Windows",
    "apple": "Apple ID / iCloud",
    "amazon": "Amazon Web Services / Shopping",
    "github": "GitHub",
    "dropbox": "Dropbox Cloud",
    "adobe": "Adobe Creative Cloud",
    "linkedin": "LinkedIn",
    "twitter": "X / Twitter",
    "meta": "Meta Platforms",
    "facebook": "Facebook",
    "instagram": "Instagram",
    "whatsapp": "WhatsApp",
    "telegram": "Telegram Messenger",
    "netflix": "Netflix Streaming",
    "spotify": "Spotify",
    "steam": "Valve Steam Gaming",
    "discord": "Discord",
    # Financial & Banking
    "paypal": "PayPal Payments",
    "chase": "JPMorgan Chase Bank",
    "wellsfargo": "Wells Fargo Bank",
    "bankofamerica": "Bank of America",
    "citibank": "Citibank",
    "capitalone": "Capital One",
    "barclays": "Barclays Bank",
    "hsbc": "HSBC Global Bank",
    "santander": "Santander Bank",
    "americanexpress": "American Express",
    "stripe": "Stripe Payments",
    "revolut": "Revolut FinTech",
    # Crypto Exchanges & Wallets
    "binance": "Binance Exchange",
    "coinbase": "Coinbase Crypto",
    "kraken": "Kraken Exchange",
    "metamask": "MetaMask Wallet",
    "ledger": "Ledger Hardware Wallet",
    "trezor": "Trezor Wallet",
    "trustwallet": "Trust Wallet",
    # Logistics & Government
    "dhl": "DHL Express Logistics",
    "fedex": "FedEx Shipping",
    "usps": "US Postal Service",
    "ups": "UPS Logistics",
}

# Common Cyrillic & Greek homoglyphs mapped to ASCII counterparts
HOMOGLYPH_MAP: Dict[str, str] = {
    # Cyrillic small letters
    "\u0430": "a",  # Cyrillic small a
    "\u0441": "c",  # Cyrillic small es (c)
    "\u0435": "e",  # Cyrillic small ie (e)
    "\u0456": "i",  # Cyrillic small Byelorussian-Ukrainian i
    "\u0458": "j",  # Cyrillic small je (j)
    "\u043e": "o",  # Cyrillic small o
    "\u0440": "p",  # Cyrillic small er (p)
    "\u0455": "s",  # Cyrillic small dze (s)
    "\u0445": "x",  # Cyrillic small ha (x)
    "\u0443": "y",  # Cyrillic small u (y)
    # Greek small letters
    "\u03b1": "a",  # Greek small alpha
    "\u03b5": "e",  # Greek small epsilon
    "\u03bf": "o",  # Greek small omicron
    "\u03c1": "p",  # Greek small rho
    # Visual digit/letter substitutions
    "0": "o",
    "1": "l",
    "3": "e",
    "4": "a",
    "5": "s",
    "@": "a",
}


def normalize_confusables(text: str) -> str:
    """Replace visually confusable characters with canonical Latin equivalents."""
    # Unicode NFKD normalization
    decomposed = unicodedata.normalize("NFKD", text)
    result = []
    for char in decomposed:
        if char in HOMOGLYPH_MAP:
            result.append(HOMOGLYPH_MAP[char])
        elif ord(char) < 128:
            result.append(char)
        else:
            # Check unicode name
            name = unicodedata.name(char, "")
            if "LATIN" in name:
                result.append(char)
    return "".join(result).lower()


def detect_brand_impersonation(domain_name: str) -> List[Tuple[str, str, str]]:
    """
    Check if a domain attempts to impersonate or look like a trusted brand.
    
    Returns:
        List of tuples: (brand_key, brand_description, detection_type)
    """
    matches: List[Tuple[str, str, str]] = []
    if not domain_name:
        return matches

    clean_domain = domain_name.lower().strip()
    # Extract labels
    labels = clean_domain.split(".")
    domain_body = labels[0] if labels else ""

    # Check homoglyph-normalized version
    normalized_body = normalize_confusables(domain_body)
    has_mixed_script = normalized_body != domain_body

    for brand_key, brand_desc in TARGET_BRANDS.items():
        # Exact match of main brand domain (e.g. google.com) is legitimate
        if clean_domain in (f"{brand_key}.com", f"{brand_key}.org", f"{brand_key}.net", f"{brand_key}.io"):
            continue

        # 1. Homoglyph substitution (e.g. 'pаypal' with Cyrillic 'а')
        if has_mixed_script and brand_key in normalized_body and brand_key not in domain_body:
            matches.append((brand_key, brand_desc, "Cyrillic/Greek Homoglyph Spoofing"))
            continue

        # 2. Typosquatting / Character substitution in domain label
        if brand_key in domain_body and clean_domain != f"{brand_key}.com":
            # e.g., paypal-verify.com, login-microsoft.net, secure-apple-account.com
            matches.append((brand_key, brand_desc, "Brand Name in Untrusted Domain Label"))
            continue

        # 3. Levenshtein edit distance check
        from .lexical_analyzer import levenshtein_distance
        dist = levenshtein_distance(domain_body, brand_key)
        if dist in (1, 2) and abs(len(domain_body) - len(brand_key)) <= 2:
            matches.append((brand_key, brand_desc, f"Typosquatting Edit Distance ({dist})"))

    return matches

