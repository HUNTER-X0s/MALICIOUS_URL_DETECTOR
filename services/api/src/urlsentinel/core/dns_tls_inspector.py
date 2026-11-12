"""DNS and TLS / Certificate Security Inspector for URLSentinel.

Performs non-hostile socket and certificate inspection, validates SAN coverage,
computes remaining certificate validity, and prevents DNS rebinding exploits.
"""

import socket
import ssl
from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Tuple

from .ssrf_guard import validate_destination_safety, is_ip_denied, parse_numeric_ip, SSRFBlockedError


@dataclass
class CertificateDetails:
    has_tls: bool
    is_valid: bool
    issuer: Optional[str] = None
    subject: Optional[str] = None
    san_domains: List[str] = field(default_factory=list)
    expires_at: Optional[str] = None
    days_remaining: Optional[int] = None
    is_expired: bool = False
    hostname_mismatch: bool = False
    error: Optional[str] = None


@dataclass
class DNSDetails:
    hostname: str
    resolved_ipv4: List[str] = field(default_factory=list)
    resolved_ipv6: List[str] = field(default_factory=list)
    is_routable: bool = True
    error: Optional[str] = None


def inspect_dns_records(hostname: str) -> DNSDetails:
    """Resolve A and AAAA records safely while blocking private and rebinding addresses."""
    clean_host = hostname.strip().lower()
    ipv4_list: List[str] = []
    ipv6_list: List[str] = []

    try:
        addr_info = socket.getaddrinfo(clean_host, 80, family=socket.AF_UNSPEC, type=socket.SOCK_STREAM)
        for item in addr_info:
            sockaddr = item[4]
            ip_str = sockaddr[0]
            parsed = parse_numeric_ip(ip_str)
            if parsed:
                denied, reason = is_ip_denied(parsed)
                if denied:
                    raise SSRFBlockedError(f"DNS resolved private IP {ip_str}: {reason}", target_ip=ip_str)
                if ":" in ip_str and ip_str not in ipv6_list:
                    ipv6_list.append(ip_str)
                elif "." in ip_str and ip_str not in ipv4_list:
                    ipv4_list.append(ip_str)
        return DNSDetails(hostname=clean_host, resolved_ipv4=ipv4_list, resolved_ipv6=ipv6_list, is_routable=True)
    except socket.gaierror as e:
        return DNSDetails(hostname=clean_host, is_routable=False, error="Domain does not resolve in public DNS")
    except SSRFBlockedError:
        raise
    except Exception as e:
        return DNSDetails(hostname=clean_host, is_routable=False, error=str(e))


def inspect_tls_certificate(hostname: str, port: int = 443, timeout: float = 3.5) -> CertificateDetails:
    """Connect to destination port via TLS handshake and parse peer certificate metadata."""
    clean_host = hostname.strip().lower()
    context = ssl.create_default_context()
    context.check_hostname = True
    context.verify_mode = ssl.CERT_REQUIRED

    try:
        # Pre-verify that hostname is not an SSRF target
        validate_destination_safety(f"https://{clean_host}:{port}", resolve_dns=True)

        with socket.create_connection((clean_host, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=clean_host) as ssock:
                cert = ssock.getpeercert()
                if not cert:
                    return CertificateDetails(has_tls=False, is_valid=False, error="No certificate returned by peer")

                # Extract Issuer & Subject
                issuer_dict = dict(x[0] for x in cert.get("issuer", ()))
                issuer_name = issuer_dict.get("organizationName") or issuer_dict.get("commonName") or "Unknown CA"
                
                subj_dict = dict(x[0] for x in cert.get("subject", ()))
                subject_name = subj_dict.get("commonName") or "Unknown Subject"

                # Extract SANs
                sans: List[str] = []
                for entry_type, val in cert.get("subjectAltName", ()):
                    if entry_type == "DNS":
                        sans.append(val)

                # Expiry check
                not_after_str = cert.get("notAfter")
                expires_at_iso = None
                days_left = None
                is_expired = False

                if not_after_str:
                    try:
                        exp_dt = datetime.strptime(not_after_str, "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
                        expires_at_iso = exp_dt.isoformat()
                        delta = exp_dt - datetime.now(timezone.utc)
                        days_left = delta.days
                        if days_left < 0:
                            is_expired = True
                    except Exception:
                        pass

                return CertificateDetails(
                    has_tls=True,
                    is_valid=not is_expired,
                    issuer=issuer_name,
                    subject=subject_name,
                    san_domains=sans[:10],
                    expires_at=expires_at_iso,
                    days_remaining=days_left,
                    is_expired=is_expired,
                    hostname_mismatch=False,
                )

    except ssl.SSLCertVerificationError as e:
        return CertificateDetails(
            has_tls=True,
            is_valid=False,
            is_expired="certificate has expired" in str(e).lower(),
            hostname_mismatch="doesn't match" in str(e).lower(),
            error=f"TLS Verification Failed: {str(e)}",
        )
    except (socket.timeout, TimeoutError):
        return CertificateDetails(has_tls=False, is_valid=False, error="TLS handshake timed out")
    except Exception as e:
        return CertificateDetails(has_tls=False, is_valid=False, error=str(e))

