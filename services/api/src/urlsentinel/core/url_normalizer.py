"""URL Normalization and Decomposition Subsystem for URLSentinel."""

import hashlib
import idna
import re
from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlsplit, urlunsplit, quote, unquote
import publicsuffix2

# Module-level singleton to avoid expensive disk/PSL parsing on every invocation
_PSL = publicsuffix2.PublicSuffixList()


@dataclass(frozen=True)
class NormalizedURL:
    raw_url: str
    normalized_url: str
    url_hash: str
    scheme: str
    host: str
    port: Optional[int]
    path: str
    query: str
    fragment: str
    registered_domain: str
    subdomain: str
    public_suffix: str
    is_idn: bool
    punycode_host: str


def _remove_dot_segments(path: str) -> str:
    """Normalize RFC 3986 path dot segments (/./ and /../)."""
    if not path:
        return "/"
    
    segments = path.split("/")
    output = []
    
    for seg in segments:
        if seg == "." or seg == "":
            continue
        elif seg == "..":
            if output:
                output.pop()
        else:
            output.append(seg)
            
    res = "/" + "/".join(output)
    if path.endswith("/") and not res.endswith("/"):
        res += "/"
    return res


def normalize_url(raw_url: str) -> NormalizedURL:
    """
    Standardize and canonicalize a URL string.
    
    Performs scheme/host lowercasing, IDN conversion, port removal,
    path traversal resolution, and public suffix decomposition.
    """
    url_str = raw_url.strip()
    
    # If scheme missing, default to https:// for parsing
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9+\-.]*://", url_str):
        url_str = "https://" + url_str
        
    parts = urlsplit(url_str)
    
    scheme = parts.scheme.lower()
    
    # Process host
    raw_host = parts.hostname or ""
    is_idn = False
    punycode_host = raw_host
    
    try:
        # Check if IDN / decode or encode to punycode
        punycode_host = idna.encode(raw_host.lower()).decode("ascii")
        decoded_host = idna.decode(punycode_host)
        if punycode_host != decoded_host.lower():
            is_idn = True
        host = decoded_host.lower()
    except Exception:
        host = raw_host.lower()
        punycode_host = host
        
    # Strip trailing dot in host if present
    if host.endswith("."):
        host = host[:-1]
    if punycode_host.endswith("."):
        punycode_host = punycode_host[:-1]

    # Process port
    port = parts.port
    if (scheme == "http" and port == 80) or (scheme == "https" and port == 443):
        port = None

    # Process path
    path = parts.path or "/"
    path = _remove_dot_segments(path)
    
    # Clean query and fragment
    query = parts.query
    fragment = parts.fragment
    
    # Reassemble canonical authority
    if port:
        netloc = f"{host}:{port}"
    else:
        netloc = host
        
    canonical_url = urlunsplit((scheme, netloc, path, query, fragment))
    
    # SHA-256 hash of normalized canonical URL
    url_hash = hashlib.sha256(canonical_url.encode("utf-8")).hexdigest()
    
    # Extract registered domain and public suffix
    psl = _PSL
    registered_domain = psl.get_public_suffix(host) or host
    public_suffix = psl.get_tld(host) or ""
    
    if host == registered_domain:
        subdomain = ""
    elif host.endswith("." + registered_domain):
        subdomain = host[: -(len(registered_domain) + 1)]
    else:
        subdomain = ""

    return NormalizedURL(
        raw_url=raw_url,
        normalized_url=canonical_url,
        url_hash=url_hash,
        scheme=scheme,
        host=host,
        port=port,
        path=path,
        query=query,
        fragment=fragment,
        registered_domain=registered_domain,
        subdomain=subdomain,
        public_suffix=public_suffix,
        is_idn=is_idn,
        punycode_host=punycode_host,
    )

