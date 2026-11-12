# URLSentinel Chrome Web Store Listing & Submission Metadata

## Title
**URLSentinel — Real-Time Link & Phishing Protection**

## Short Description (max 132 chars)
Zero-trust real-time protection against malicious URLs, phishing portals, brand impersonation, and deceptive redirects.

## Detailed Description

### Browse the web completely tension-free.
URLSentinel protects you from fraudulent websites, credential harvesters, lookalike brand domains, and malicious downloads before they can harm your device or steal your sensitive data.

### 🛡️ Why URLSentinel is Different
Unlike traditional blacklists that update hours or days after an attack campaign starts, URLSentinel evaluates destination links using a multi-vector security engine:
- **Zero-Day Lexical Analysis**: Shannon entropy modeling detects obfuscated paths and algorithmically generated subdomains in sub-millisecond time.
- **Homoglyph & Punycode Shield**: Catches deceptive lookalike letters (such as Cyrillic `а` spoofing Latin `a` in `pаypal.com`).
- **Live Threat Intelligence**: Correlates against URLhaus (abuse.ch) and OpenPhish feeds every 15 minutes.
- **SSRF & Private Egress Guard**: Prevents intranet probing, loopback exploits, and cloud metadata theft.

### ⚡ Blazing Fast & Lightweight
- **Sub-5ms Evaluation Overhead**: Asynchronous background worker and local LRU cache ensure zero impact on your browsing speed.
- **Battery & Memory Efficient**: Built natively with modern Manifest V3 standards.

### 🔒 Privacy by Design (Zero User URL Logging)
- We believe your browsing history is none of our business.
- URLs are processed ephemerally in volatile memory and digested into irreversible SHA-256 hashes.
- No personal user browsing profiles, IP tracking, or search logs are ever stored or sold.

### 📋 Permissions Disclosures
- **storage**: Used strictly to maintain your local encrypted cache of verified clean domains.
- **activeTab / webNavigation**: Required to inspect the destination domain of links before navigation occurs.

### 🌟 Open Transparency
Visit our Transparency Center and view our source code and cryptographic verification proofs at:
https://urlsentinel.io/security

