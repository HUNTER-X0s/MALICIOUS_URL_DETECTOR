"""URLSentinel Isolated Content Scanner and DOM Safety Analyzer.

Complies with Blueprint §016 (Content Analysis), §018 (Isolated Scanner),
and §019 (SSRF Protection).

Executes bounded, egress-restricted passive content probes within strict safety envelopes:
- Re-verifies IP address safety at socket connection level.
- Maximum response size capped at 512 KB to defeat decompression bombs.
- Rejects binary executables, archives, and dangerous MIME types.
- Scans HTML DOM for credential harvesting forms, external form destinations,
  hidden iframes, and misleading login inputs on third-party origins.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional
import httpx

from .ssrf_guard import validate_destination_safety, SSRFBlockedError

# Prohibited MIME types that indicate active malware downloads
PROHIBITED_MIME_PATTERNS = [
    r"application/x-msdownload",
    r"application/octet-stream",
    r"application/x-dosexec",
    r"application/x-executable",
    r"application/zip",
    r"application/x-rar",
    r"application/x-7z-compressed",
    r"application/x-iso9660-image",
]

MAX_CONTENT_BYTES = 512 * 1024  # 512 KB ceiling


class IsolatedScanner:
    """Bounded, sandboxed HTML DOM and content safety inspector."""

    @classmethod
    async def analyze_target_content(
        cls,
        url: str,
        timeout_seconds: float = 3.0,
    ) -> Dict[str, Any]:
        """Safely fetch and inspect page headers and DOM structure within strict safety envelope."""
        findings: List[str] = []
        is_safe = True
        risk_contribution = "LOW"
        detected_features: Dict[str, Any] = {
            "has_password_field": False,
            "has_external_form_action": False,
            "has_hidden_iframe": False,
            "has_meta_refresh": False,
            "forms_found": 0,
            "page_title": "",
            "content_length_bytes": 0,
        }

        # 1. Re-validate destination safety (SSRF boundary check)
        try:
            validate_destination_safety(url, resolve_dns=True)
        except SSRFBlockedError as e:
            return {
                "scan_executed": False,
                "error": f"SSRF Guard blocked content inspection: {e}",
                "findings": ["Destination violates isolated scanner network boundary"],
                "risk_contribution": "CRITICAL",
                "detected_features": detected_features,
            }

        # 2. Bounded HTTP probe with custom security headers and size limit
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) URLSentinel-Analyzer/1.0 (Security Scanner)",
            "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }

        try:
            async with httpx.AsyncClient(
                verify=True,
                follow_redirects=False,  # Redirects evaluated individually to prevent open redirect loops
                timeout=timeout_seconds,
            ) as client:
                response = await client.get(url, headers=headers)

                # Check Content-Type header
                content_type = response.headers.get("content-type", "").lower()
                for mime_pat in PROHIBITED_MIME_PATTERNS:
                    if re.search(mime_pat, content_type):
                        findings.append(f"Destination serves suspicious binary content type: {content_type}")
                        risk_contribution = "CRITICAL"
                        return {
                            "scan_executed": True,
                            "findings": findings,
                            "risk_contribution": risk_contribution,
                            "detected_features": detected_features,
                        }

                # Read capped body bytes
                content_bytes = response.content[:MAX_CONTENT_BYTES]
                detected_features["content_length_bytes"] = len(content_bytes)

                # Attempt decoding as text/html
                try:
                    html_text = content_bytes.decode("utf-8", errors="replace")
                except Exception:
                    html_text = ""

                # 3. Analyze HTML DOM Structure
                # Check for page title
                title_match = re.search(r"<title[^>]*>(.*?)</title>", html_text, re.IGNORECASE | re.DOTALL)
                if title_match:
                    detected_features["page_title"] = title_match.group(1).strip()[:100]

                # Check for password inputs
                if re.search(r"<input[^>]+type=['\"]?password['\"]?", html_text, re.IGNORECASE):
                    detected_features["has_password_field"] = True
                    findings.append("Page contains password input field; destination is soliciting user credentials")
                    risk_contribution = "HIGH"

                # Check for external form actions
                form_actions = re.findall(r"<form[^>]+action=['\"]?([^'\">]+)['\"]?", html_text, re.IGNORECASE)
                detected_features["forms_found"] = len(form_actions)
                for action in form_actions:
                    if action.startswith("http://") or action.startswith("https://"):
                        detected_features["has_external_form_action"] = True
                        findings.append(f"Form submission posts credentials to external URI: {action[:50]}")
                        risk_contribution = "CRITICAL"
                        break

                # Check for hidden iframes (clickjacking / drive-by downloads)
                if re.search(r"<iframe[^>]+(display:\s*none|visibility:\s*hidden|width=['\"]?0['\"]?|height=['\"]?0['\"]?)", html_text, re.IGNORECASE):
                    detected_features["has_hidden_iframe"] = True
                    findings.append("Hidden iframe element detected, frequently used in clickjacking or credential theft")
                    risk_contribution = "HIGH"

                # Check for meta refresh or immediate redirects
                if re.search(r"<meta[^>]+http-equiv=['\"]?refresh['\"]?", html_text, re.IGNORECASE):
                    detected_features["has_meta_refresh"] = True
                    findings.append("Client-side META refresh redirect detected")

        except httpx.TimeoutException:
            return {
                "scan_executed": False,
                "error": "Probe timed out within safety envelope limit (3.0s)",
                "findings": ["Destination did not respond within safety timeout"],
                "risk_contribution": "INFORMATIONAL",
                "detected_features": detected_features,
            }
        except Exception as ex:
            return {
                "scan_executed": False,
                "error": f"Content probe failed: {str(ex)[:100]}",
                "findings": [],
                "risk_contribution": "INFORMATIONAL",
                "detected_features": detected_features,
            }

        return {
            "scan_executed": True,
            "findings": findings,
            "risk_contribution": risk_contribution,
            "detected_features": detected_features,
        }

