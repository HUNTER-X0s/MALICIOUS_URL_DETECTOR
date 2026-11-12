"""URLSentinel Command Line Interface (CLI).

Complies with Blueprint §086 (CLI) and §087 (Security API for CI/CD).
Provides terminal commands for scanning URLs, checking domain reputation,
cryptographic verdict verification, and exporting SARIF security reports.

Exit Codes:
  0: BENIGN or UNKNOWN (clean)
  1: SUSPICIOUS
  2: MALICIOUS
  3: SSRF / Validation Security Error
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict, List
import httpx

API_BASE_DEFAULT = "http://127.0.0.1:8000/api/v1"

# ANSI Terminal formatting
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"


def format_sarif(verdict_data: Dict[str, Any]) -> Dict[str, Any]:
    """Convert URLSentinel verdict output into SARIF 2.1.0 format for CI/CD pipelines."""
    level = "none"
    if verdict_data.get("verdict") == "MALICIOUS":
        level = "error"
    elif verdict_data.get("verdict") == "SUSPICIOUS":
        level = "warning"

    rules = [
        {
            "id": "URLS001",
            "name": "MaliciousOrSuspiciousURL",
            "shortDescription": {"text": "Detected high-risk or malicious URL target"},
            "defaultConfiguration": {"level": level},
        }
    ]

    results = []
    if level in ("error", "warning"):
        results.append({
            "ruleId": "URLS001",
            "level": level,
            "message": {"text": f"URL {verdict_data.get('url')} classified as {verdict_data.get('verdict')}: {verdict_data.get('summary')}"},
            "properties": {
                "riskScore": verdict_data.get("risk_score"),
                "confidence": verdict_data.get("confidence"),
                "scanId": verdict_data.get("id"),
            },
        })

    return {
        "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "URLSentinel",
                        "semanticVersion": "1.0.0",
                        "rules": rules,
                    }
                },
                "results": results,
            }
        ],
    }


def cmd_scan(args: argparse.Namespace) -> int:
    """Execute scan against API endpoint or local core."""
    url = args.url
    payload = {"url": url, "request_deep_scan": args.deep}

    try:
        response = httpx.post(f"{args.api}/scan", json=payload, timeout=args.timeout)
    except Exception as e:
        # Fallback to local synchronous scanner if API daemon is offline
        from .core.ssrf_guard import validate_destination_safety, SSRFBlockedError
        from .core.url_normalizer import normalize_url
        from .core.lexical_analyzer import analyze_lexical
        from .core.homoglyph_detector import detect_brand_impersonation
        from .core.feed_ingestion import query_threat_intel
        from .core.verdict_engine import evaluate_verdict

        try:
            _, resolved_ips = validate_destination_safety(url, resolve_dns=True)
        except SSRFBlockedError as ssrf_err:
            print(f"{RED}{BOLD}ERROR:{RESET} SSRF Guard blocked scan destination: {ssrf_err}", file=sys.stderr)
            return 3

        norm = normalize_url(url)
        lexical = analyze_lexical(norm)
        homoglyphs = detect_brand_impersonation(norm.host)
        ti_matches = query_threat_intel(norm.url_hash, norm.host)
        verdict_obj = evaluate_verdict(
            norm_url=norm,
            lexical=lexical,
            resolved_ips=resolved_ips,
            ti_matches=ti_matches,
            homoglyphs=homoglyphs,
        )
        data = {
            "id": verdict_obj.id,
            "url": verdict_obj.url,
            "url_hash": verdict_obj.url_hash,
            "verdict": verdict_obj.verdict,
            "risk_score": verdict_obj.risk_score,
            "confidence": verdict_obj.confidence,
            "summary": verdict_obj.summary,
            "evidence": verdict_obj.evidence,
            "limitations": verdict_obj.limitations,
            "recommended_action": verdict_obj.recommended_action,
            "checked_at": verdict_obj.checked_at,
        }
        return _render_scan_output(data, args)

    if response.status_code == 400:
        err = response.json()
        print(f"{RED}{BOLD}SECURITY VIOLATION:{RESET} {err.get('message', 'Blocked')}", file=sys.stderr)
        return 3

    if response.status_code != 200:
        print(f"{RED}API Error ({response.status_code}): {response.text}{RESET}", file=sys.stderr)
        return 1

    data = response.json()
    return _render_scan_output(data, args)


def _render_scan_output(data: Dict[str, Any], args: argparse.Namespace) -> int:
    """Print scan results in requested format and return corresponding exit code."""
    if args.sarif:
        print(json.dumps(format_sarif(data), indent=2))
    elif args.json:
        print(json.dumps(data, indent=2))
    else:
        verdict = data.get("verdict", "UNKNOWN")
        score = data.get("risk_score", 0)

        color = GREEN
        if verdict == "MALICIOUS":
            color = RED
        elif verdict == "SUSPICIOUS":
            color = YELLOW
        elif verdict == "UNKNOWN":
            color = CYAN

        print(f"\n{BOLD}URLSentinel Security Scan Report{RESET}")
        print(f"{DIM}Scan ID: {data.get('id')}{RESET}\n")
        print(f"  Target URL:   {data.get('url')}")
        print(f"  Verdict:      {color}{BOLD}{verdict}{RESET}")
        print(f"  Risk Score:   {color}{score}/100{RESET}")
        print(f"  Confidence:   {data.get('confidence')}")
        print(f"  Summary:      {data.get('summary')}")
        print(f"  Action:       {data.get('recommended_action')}\n")

        evidence = data.get("evidence", [])
        if evidence:
            print(f"{BOLD}Detected Signals & Evidence ({len(evidence)}):{RESET}")
            for ev in evidence:
                contrib = ev.get("contribution", "INFORMATIONAL")
                ev_color = RED if contrib == "CRITICAL" else (YELLOW if contrib == "HIGH" else DIM)
                print(f"  • [{ev_color}{contrib}{RESET}] {ev.get('description')}")
        print()

    # Determine exit code
    v = data.get("verdict")
    if v == "MALICIOUS":
        return 2
    elif v == "SUSPICIOUS":
        return 1
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    """Verify cryptographic HMAC proof for a scan ID."""
    scan_id = args.scan_id
    try:
        response = httpx.get(f"{args.api}/verify/{scan_id}", timeout=args.timeout)
        if response.status_code == 404:
            print(f"{RED}Error: Scan ID '{scan_id}' not found.{RESET}", file=sys.stderr)
            return 1
        data = response.json()
        if args.json:
            print(json.dumps(data, indent=2))
        else:
            status_color = GREEN if data.get("valid") else RED
            print(f"\n{BOLD}Cryptographic Proof Verification{RESET}")
            print(f"  Scan ID:      {data.get('scan_id')}")
            print(f"  Signature:    {status_color}{data.get('signature')}{RESET}")
            print(f"  Algorithm:    {data.get('algorithm')}")
            print(f"  Status:       {status_color}{'AUTHENTIC' if data.get('valid') else 'INVALID'}{RESET}\n")
        return 0
    except Exception as e:
        print(f"{RED}Verification connection error: {e}{RESET}", file=sys.stderr)
        return 1


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="urlsentinel",
        description="URLSentinel - Security-first malicious URL detection & analysis CLI.",
    )
    parser.add_argument("--api", default=API_BASE_DEFAULT, help="URLSentinel API base endpoint")
    parser.add_argument("--timeout", type=float, default=5.0, help="HTTP request timeout in seconds")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # scan command
    p_scan = subparsers.add_parser("scan", help="Scan a URL for malicious indicators")
    p_scan.add_argument("url", help="Target URL to inspect")
    p_scan.add_argument("--deep", action="store_true", help="Request sandboxed DOM content inspection")
    p_scan.add_argument("--json", action="store_true", help="Output raw JSON verdict")
    p_scan.add_argument("--sarif", action="store_true", help="Output OASIS SARIF format for CI/CD")

    # verify command
    p_verify = subparsers.add_parser("verify", help="Verify cryptographic proof of a scan report")
    p_verify.add_argument("scan_id", help="Unique UUID of the scan to verify")
    p_verify.add_argument("--json", action="store_true", help="Output verification as JSON")

    # version command
    subparsers.add_parser("version", help="Show URLSentinel CLI and engine version")

    args = parser.parse_args(argv)

    if args.command == "version":
        print("URLSentinel CLI v1.0.0 (Engine: 1.0.0, Contracts: 1.0.0)")
        return 0
    elif args.command == "scan":
        return cmd_scan(args)
    elif args.command == "verify":
        return cmd_verify(args)

    return 0


if __name__ == "__main__":
    sys.exit(main())

