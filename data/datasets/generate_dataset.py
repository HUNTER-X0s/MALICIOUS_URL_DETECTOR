"""
URLSentinel Dataset Generator
Generates a labeled URL dataset for training and evaluation.

Sources of URL patterns:
- Real-world phishing URL structures documented in security research
- Benign URLs from known legitimate services
- Edge cases that stress-test classifiers

IMPORTANT: This generates synthetic/pattern-based URLs based on documented
phishing techniques. No actual live malicious URLs are committed to the repo.
Labels are based on structural patterns, not live threat intelligence.
"""
from __future__ import annotations
import csv
import json
import random
import string
from pathlib import Path

random.seed(42)  # Reproducible

BENIGN_DOMAINS = [
    # Major tech
    "google.com", "youtube.com", "facebook.com", "twitter.com", "instagram.com",
    "linkedin.com", "microsoft.com", "apple.com", "amazon.com", "netflix.com",
    "github.com", "stackoverflow.com", "reddit.com", "wikipedia.org", "medium.com",
    # Banks / Finance
    "chase.com", "bankofamerica.com", "wellsfargo.com", "paypal.com", "stripe.com",
    "coinbase.com", "schwab.com", "fidelity.com", "vanguard.com", "tdameritrade.com",
    # Gov / Edu
    "irs.gov", "cdc.gov", "nih.gov", "mit.edu", "stanford.edu", "harvard.edu",
    # News
    "bbc.com", "nytimes.com", "reuters.com", "apnews.com", "theguardian.com",
    # E-commerce
    "ebay.com", "etsy.com", "shopify.com", "walmart.com", "target.com",
    # Productivity
    "notion.so", "slack.com", "zoom.us", "dropbox.com", "drive.google.com",
    # Security
    "cloudflare.com", "letsencrypt.org", "haveibeenpwned.com", "shodan.io",
]

BENIGN_PATHS = [
    "/", "/about", "/contact", "/help", "/faq", "/blog", "/news",
    "/products", "/services", "/pricing", "/docs", "/api/v1/status",
    "/search?q=python", "/account/settings", "/dashboard",
    "/2024/01/article-title", "/en/security/advisories",
]

PHISHING_BRANDS = [
    "paypal", "apple", "microsoft", "google", "amazon", "netflix",
    "chase", "bankofamerica", "wellsfargo", "instagram", "facebook",
    "linkedin", "dropbox", "docusign", "zoom", "outlook", "office365",
]

PHISHING_TLDS = [".xyz", ".top", ".club", ".loan", ".stream", ".bid", ".gq",
                 ".ml", ".cf", ".ga", ".buzz", ".work", ".cam", ".live"]

PHISHING_LEGITIMATE_TLDS = [".com", ".net", ".org", ".co", ".io"]  # Used in lookalikes

PHISHING_KEYWORDS = [
    "login", "signin", "verify", "secure", "account", "update",
    "confirm", "password", "credential", "banking", "wallet", "recover",
    "authenticate", "validation", "support", "auth", "billing",
]

HIGH_RISK_PATHS = [
    "/login", "/signin", "/verify-account", "/secure/login", "/account/verify",
    "/confirm-identity", "/password-reset", "/update-credentials",
    "/auth/callback", "/banking/login", "/wallet/connect",
]


def rand_str(length: int, chars: str = string.ascii_lowercase + string.digits) -> str:
    return "".join(random.choices(chars, k=length))


def rand_dga_domain() -> str:
    """Simulate DGA-generated domain: high entropy, mostly consonants."""
    length = random.randint(12, 24)
    return rand_str(length) + random.choice([".com", ".net", ".top", ".xyz"])


def rand_ip() -> str:
    return f"{random.randint(1, 254)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"


def generate_benign_urls(count: int) -> list[dict]:
    urls = []

    # Simple domain + path
    for _ in range(int(count * 0.4)):
        domain = random.choice(BENIGN_DOMAINS)
        path = random.choice(BENIGN_PATHS)
        scheme = "https"
        url = f"{scheme}://{domain}{path}"
        urls.append({"url": url, "label": 0, "category": "benign_simple"})

    # With www subdomain
    for _ in range(int(count * 0.15)):
        domain = random.choice(BENIGN_DOMAINS)
        path = random.choice(BENIGN_PATHS)
        url = f"https://www.{domain}{path}"
        urls.append({"url": url, "label": 0, "category": "benign_www"})

    # API and app subdomains
    for _ in range(int(count * 0.1)):
        domain = random.choice(BENIGN_DOMAINS)
        sub = random.choice(["api", "app", "docs", "help", "support", "status", "cdn"])
        path = random.choice(BENIGN_PATHS)
        url = f"https://{sub}.{domain}{path}"
        urls.append({"url": url, "label": 0, "category": "benign_subdomain"})

    # URLs with query parameters (common in legit sites)
    for _ in range(int(count * 0.1)):
        domain = random.choice(BENIGN_DOMAINS)
        query = f"id={random.randint(1000, 9999)}&ref=homepage&lang=en"
        url = f"https://{domain}/search?{query}"
        urls.append({"url": url, "label": 0, "category": "benign_query"})

    # Legitimate URLs that have security-related words (edge case)
    edge_cases = [
        "https://support.google.com/accounts/answer/185833",
        "https://www.microsoft.com/en-us/security/business/identity-access",
        "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_passwords.html",
        "https://haveibeenpwned.com/account/verify",
        "https://github.com/login?return_to=%2Fjoin",
        "https://accounts.google.com/signin/v2/identifier",
        "https://login.microsoftonline.com/common/oauth2/authorize",
        "https://www.paypal.com/signin",
        "https://appleid.apple.com/account/manage",
        "https://www.bankofamerica.com/online-banking/sign-in-overview.go",
        "https://secure.chase.com/web/auth/dashboard",
        "https://www.amazon.com/ap/signin",
        "https://www.facebook.com/login",
        "https://twitter.com/i/flow/login",
        "https://www.linkedin.com/login",
    ]
    for url in edge_cases:
        urls.append({"url": url, "label": 0, "category": "benign_auth_edge"})

    # Fill remainder
    while len(urls) < count:
        domain = random.choice(BENIGN_DOMAINS)
        url = f"https://{domain}/"
        urls.append({"url": url, "label": 0, "category": "benign_root"})

    return urls[:count]


def generate_phishing_urls(count: int) -> list[dict]:
    urls = []

    # Pattern 1: Brand name in subdomain of foreign TLD
    for _ in range(int(count * 0.12)):
        brand = random.choice(PHISHING_BRANDS)
        tld = random.choice(PHISHING_TLDS)
        host = f"{brand}.{rand_str(8)}{tld}"
        path = random.choice(HIGH_RISK_PATHS)
        url = f"http://{host}{path}"
        urls.append({"url": url, "label": 1, "category": "phishing_brand_subdomain"})

    # Pattern 2: Typosquatting (extra chars, transposition)
    typo_patterns = [
        ("paypal", ["paypa1", "paypai", "paypa-l", "paypa1l", "paaypal", "paypa.l"]),
        ("google", ["googIe", "g00gle", "gooogle", "googlle", "goog1e"]),
        ("apple", ["app1e", "aple", "appIe", "appie", "appl3"]),
        ("microsoft", ["m1crosoft", "micros0ft", "microsofft", "miicrosoft"]),
        ("amazon", ["amaz0n", "amazoon", "arnazon", "amozon"]),
    ]
    for _ in range(int(count * 0.1)):
        brand, typos = random.choice(typo_patterns)
        typo = random.choice(typos)
        tld = random.choice([".com", ".net", ".org", ".co"])
        path = random.choice(HIGH_RISK_PATHS)
        url = f"https://{typo}{tld}{path}"
        urls.append({"url": url, "label": 1, "category": "phishing_typosquat"})

    # Pattern 3: IP address host
    for _ in range(int(count * 0.08)):
        ip = rand_ip()
        path = random.choice(HIGH_RISK_PATHS)
        url = f"http://{ip}{path}"
        urls.append({"url": url, "label": 1, "category": "phishing_ip_host"})

    # Pattern 4: Long URL with many keywords
    for _ in range(int(count * 0.1)):
        brand = random.choice(PHISHING_BRANDS)
        kw1 = random.choice(PHISHING_KEYWORDS)
        kw2 = random.choice(PHISHING_KEYWORDS)
        tld = random.choice(PHISHING_TLDS)
        host = f"{brand}-{kw1}{tld}"
        token = rand_str(16)
        url = f"http://{host}/{kw2}/{kw1}?token={token}&redirect=true"
        urls.append({"url": url, "label": 1, "category": "phishing_keyword_rich"})

    # Pattern 5: Legitimate domain lookalike with hyphen
    for _ in range(int(count * 0.1)):
        brand = random.choice(PHISHING_BRANDS)
        suffix = random.choice(["secure", "verify", "login", "account", "update", "confirm"])
        tld = random.choice(PHISHING_LEGITIMATE_TLDS)
        path = random.choice(HIGH_RISK_PATHS)
        url = f"https://{brand}-{suffix}{tld}{path}"
        urls.append({"url": url, "label": 1, "category": "phishing_hyphen_lure"})

    # Pattern 6: DGA domain
    for _ in range(int(count * 0.08)):
        domain = rand_dga_domain()
        path = random.choice(HIGH_RISK_PATHS)
        url = f"http://{domain}{path}"
        urls.append({"url": url, "label": 1, "category": "phishing_dga"})

    # Pattern 7: Subdomain brand stuffing
    for _ in range(int(count * 0.1)):
        brand = random.choice(PHISHING_BRANDS)
        kw = random.choice(PHISHING_KEYWORDS)
        attacker = rand_str(10, string.ascii_lowercase) + ".com"
        path = random.choice(HIGH_RISK_PATHS)
        url = f"http://{brand}.{kw}.{attacker}{path}"
        urls.append({"url": url, "label": 1, "category": "phishing_subdomain_stuffing"})

    # Pattern 8: Punycode/homoglyph
    punycode_examples = [
        "https://xn--pple-43d.com/signin",             # аpple.com (Cyrillic a)
        "https://xn--googIe-p18d.com/login",
        "https://xn--pypal-4ve.com/account/verify",    # paypal with homoglyph
        "http://xn--amzn-moa.com/ap/signin",
        "https://xn--mcrosoft-q2a.com/en-us/signin",
    ]
    for url in punycode_examples:
        urls.append({"url": url, "label": 1, "category": "phishing_punycode"})

    # Pattern 9: @ symbol credential lure
    for _ in range(int(count * 0.05)):
        brand = random.choice(PHISHING_BRANDS)
        attacker = rand_str(12) + ".com"
        url = f"http://{brand}.com@{attacker}/login"
        urls.append({"url": url, "label": 1, "category": "phishing_at_lure"})

    # Pattern 10: Short URL service abuse (structural signal only)
    shortener_patterns = [
        f"http://bit.ly/{rand_str(7)}",
        f"http://t.co/{rand_str(10)}",
        f"http://goo.gl/{rand_str(6)}",
        f"http://tinyurl.com/{rand_str(8)}",
        f"http://ow.ly/{rand_str(5)}",
    ]
    for _ in range(int(count * 0.05)):
        url = random.choice(shortener_patterns)
        # Short URLs are SUSPICIOUS, not definitively malicious (label=0 would be wrong here)
        # We label ambiguously used short URLs as 1 for conservative detection
        urls.append({"url": url, "label": 1, "category": "phishing_shorturl"})

    # Pattern 11: Hex-encoded credentials
    for _ in range(int(count * 0.05)):
        brand = random.choice(PHISHING_BRANDS)
        encoded = "".join(f"%{ord(c):02x}" for c in rand_str(5))
        tld = random.choice(PHISHING_TLDS)
        url = f"http://{brand}{tld}/login?redirect={encoded}&verify=true"
        urls.append({"url": url, "label": 1, "category": "phishing_hex_encoded"})

    # Pattern 12: High abuse TLD with keyword
    for _ in range(int(count * 0.07)):
        kw = random.choice(PHISHING_KEYWORDS)
        tld = random.choice(PHISHING_TLDS)
        host = f"{kw}-{rand_str(6)}{tld}"
        path = random.choice(HIGH_RISK_PATHS)
        url = f"http://{host}{path}"
        urls.append({"url": url, "label": 1, "category": "phishing_tld_keyword"})

    # Fill remainder
    while len(urls) < count:
        brand = random.choice(PHISHING_BRANDS)
        tld = random.choice(PHISHING_TLDS)
        url = f"http://{brand}-secure{tld}/verify"
        urls.append({"url": url, "label": 1, "category": "phishing_generic"})

    return urls[:count]


def generate_dataset(total: int = 2000, phishing_ratio: float = 0.5) -> list[dict]:
    phishing_count = int(total * phishing_ratio)
    benign_count = total - phishing_count

    phishing = generate_phishing_urls(phishing_count)
    benign = generate_benign_urls(benign_count)

    all_data = phishing + benign
    random.shuffle(all_data)

    # Add index
    for i, item in enumerate(all_data):
        item["id"] = i

    return all_data


if __name__ == "__main__":
    out_dir = Path(__file__).parent
    data = generate_dataset(total=2000, phishing_ratio=0.5)

    # Write CSV
    csv_path = out_dir / "urlsentinel_eval_dataset.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "url", "label", "category"])
        writer.writeheader()
        writer.writerows(data)
    print(f"[OK] CSV written: {csv_path} ({len(data)} rows)")

    # Write JSON (smaller subset for unit tests)
    json_path = out_dir / "urlsentinel_eval_dataset.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"[OK] JSON written: {json_path}")

    # Print distribution
    labels = [d["label"] for d in data]
    phishing_n = sum(labels)
    print(f"\nDataset statistics:")
    print(f"  Total:    {len(data)}")
    print(f"  Phishing: {phishing_n} ({phishing_n/len(data)*100:.1f}%)")
    print(f"  Benign:   {len(data)-phishing_n} ({(len(data)-phishing_n)/len(data)*100:.1f}%)")
    cats = {}
    for d in data:
        cats[d["category"]] = cats.get(d["category"], 0) + 1
    print(f"\nCategories:")
    for cat, cnt in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"  {cat:40s}: {cnt}")

