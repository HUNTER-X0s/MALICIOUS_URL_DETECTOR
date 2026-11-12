"""URL Redaction Subsystem for URLSentinel.

Prevents leakage of authentication tokens, passwords, session identifiers,
and credentials in logs, telemetry, and threat reports.
"""

from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

SENSITIVE_PARAM_NAMES = {
    "token",
    "access_token",
    "auth",
    "key",
    "api_key",
    "password",
    "pwd",
    "secret",
    "client_secret",
    "session",
    "session_id",
    "jwt",
    "refresh_token",
    "code",
    "passcode",
    "pin",
    "signature",
    "sig",
    "bearer",
}


def redact_url(url_str: str) -> str:
    """
    Remove passwords/userinfo and redact sensitive query parameter values.
    
    Example:
        https://admin:secret@bank.com/reset?token=xyz123&user=john
        -> https://bank.com/reset?token=%5BREDACTED%5D&user=john
    """
    if not url_str:
        return ""
        
    try:
        parts = urlsplit(url_str.strip())
        
        # 1. Clean userinfo (username:password) from netloc
        host = parts.hostname or ""
        port = parts.port
        if port:
            netloc = f"{host}:{port}"
        else:
            netloc = host
            
        # 2. Redact sensitive query parameters
        if parts.query:
            query_tuples = parse_qsl(parts.query, keep_blank_values=True)
            redacted_tuples = []
            for k, v in query_tuples:
                lower_k = k.lower()
                if lower_k in SENSITIVE_PARAM_NAMES or any(term in lower_k for term in ("token", "pass", "secret", "auth")):
                    redacted_tuples.append((k, "[REDACTED]"))
                else:
                    redacted_tuples.append((k, v))
            new_query = urlencode(redacted_tuples)
        else:
            new_query = ""
            
        # 3. Fragments might contain access tokens in OAuth implicit flows (#access_token=...)
        new_fragment = ""
        if parts.fragment:
            if any(term in parts.fragment.lower() for term in ("token", "key", "auth", "session")):
                new_fragment = "redacted_fragment"
            else:
                new_fragment = parts.fragment
                
        return urlunsplit((parts.scheme, netloc, parts.path, new_query, new_fragment))
    except Exception:
        # If parsing fails, return a safe masked placeholder rather than leaking
        return "[UNPARSEABLE_URL_MASKED]"

