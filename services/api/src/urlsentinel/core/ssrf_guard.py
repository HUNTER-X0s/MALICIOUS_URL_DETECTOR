"""SSRF Protection Subsystem for URLSentinel.

Enforces strict destination validation, private/loopback/cloud-metadata blocking,
protocol allowlisting, and port restrictions.
"""

import ipaddress
import socket
from urllib.parse import urlsplit
from typing import List, Tuple, Optional


class SSRFBlockedError(Exception):
    """Raised when a URL destination violates SSRF safety boundaries."""
    def __init__(self, message: str, code: str = "SSRF_BLOCKED", target_ip: Optional[str] = None):
        super().__init__(message)
        self.code = code
        self.target_ip = target_ip


# Allowed schemes and ports
ALLOWED_SCHEMES = {"http", "https"}
ALLOWED_PORTS = {80, 443, 8080, 8443}

# Cloud metadata addresses
CLOUD_METADATA_IPS = {
    ipaddress.ip_address("169.254.169.254"),  # AWS, GCP, Azure, OpenStack
    ipaddress.ip_address("100.100.100.200"),  # Alibaba Cloud
    ipaddress.ip_address("192.0.0.170"),      # Oracle Cloud metadata
}

# Blocked IPv4 and IPv6 networks
DENIED_NETWORKS = [
    # IPv4
    ipaddress.ip_network("0.0.0.0/8"),          # Current network (only valid as source)
    ipaddress.ip_network("10.0.0.0/8"),          # Private-Use (RFC 1918)
    ipaddress.ip_network("100.64.0.0/10"),       # Shared Address Space (RFC 6598 CGN)
    ipaddress.ip_network("127.0.0.0/8"),         # Loopback (RFC 1122)
    ipaddress.ip_network("169.254.0.0/16"),      # Link Local (RFC 3927)
    ipaddress.ip_network("172.16.0.0/12"),       # Private-Use (RFC 1918)
    ipaddress.ip_network("192.0.0.0/24"),        # IETF Protocol Assignments (RFC 6890)
    ipaddress.ip_network("192.0.2.0/24"),        # Documentation (TEST-NET-1, RFC 5737)
    ipaddress.ip_network("192.168.0.0/16"),      # Private-Use (RFC 1918)
    ipaddress.ip_network("198.18.0.0/15"),       # Benchmarking (RFC 2544)
    ipaddress.ip_network("198.51.100.0/24"),     # Documentation (TEST-NET-2, RFC 5737)
    ipaddress.ip_network("203.0.113.0/24"),      # Documentation (TEST-NET-3, RFC 5737)
    ipaddress.ip_network("224.0.0.0/4"),         # Multicast (RFC 5771)
    ipaddress.ip_network("240.0.0.0/4"),         # Reserved for Future Use (RFC 1112)
    ipaddress.ip_network("255.255.255.255/32"),  # Limited Broadcast (RFC 919)
    # IPv6
    ipaddress.ip_network("::1/128"),             # Loopback
    ipaddress.ip_network("::/128"),              # Unspecified
    ipaddress.ip_network("::ffff:0:0/96"),       # IPv4-mapped IPv6
    ipaddress.ip_network("64:ff9b::/96"),        # IPv4/IPv6 translation (RFC 6052)
    ipaddress.ip_network("100::/64"),            # Discard prefix (RFC 6666)
    ipaddress.ip_network("2001:db8::/32"),       # Documentation (RFC 3849)
    ipaddress.ip_network("fc00::/7"),            # Unique Local Address (ULA, RFC 4193)
    ipaddress.ip_network("fe80::/10"),           # Link-Local Unicast (RFC 4291)
    ipaddress.ip_network("ff00::/8"),            # Multicast (RFC 4291)
]


def parse_numeric_ip(host: str) -> Optional[ipaddress.IPv4Address | ipaddress.IPv6Address]:
    """Parse integer, octal, hex, or standard numeric IP representations."""
    clean_host = host.strip("[]")
    
    # Try direct parsing
    try:
        return ipaddress.ip_address(clean_host)
    except ValueError:
        pass

    # Try integer/hex/octal representation for IPv4
    try:
        # Check if integer or hex
        if clean_host.startswith("0x") or clean_host.startswith("0X"):
            int_val = int(clean_host, 16)
            if 0 <= int_val <= 0xFFFFFFFF:
                return ipaddress.IPv4Address(int_val)
        elif clean_host.isdigit():
            int_val = int(clean_host, 10)
            if 0 <= int_val <= 0xFFFFFFFF:
                return ipaddress.IPv4Address(int_val)
    except (ValueError, OverflowError):
        pass

    # Check octal dotted notation (e.g. 0177.0.0.1)
    parts = clean_host.split(".")
    if len(parts) == 4:
        try:
            byte_vals = []
            for p in parts:
                if p.startswith("0x") or p.startswith("0X"):
                    b = int(p, 16)
                elif p.startswith("0") and len(p) > 1:
                    b = int(p, 8)
                else:
                    b = int(p, 10)
                if not (0 <= b <= 255):
                    return None
                byte_vals.append(b)
            return ipaddress.IPv4Address(bytes(byte_vals))
        except (ValueError, OverflowError):
            pass

    return None


def is_ip_denied(ip: ipaddress.IPv4Address | ipaddress.IPv6Address) -> Tuple[bool, str]:
    """Evaluate whether an IP address is in a denied/reserved range."""
    # Check specific metadata targets
    if ip in CLOUD_METADATA_IPS:
        return True, "Cloud metadata endpoint blocked"

    # Check IPv4-mapped IPv6
    if isinstance(ip, ipaddress.IPv6Address) and ip.ipv4_mapped:
        return is_ip_denied(ip.ipv4_mapped)

    # Check standard denied networks
    for net in DENIED_NETWORKS:
        if ip in net:
            return True, f"Target IP {ip} is within restricted network {net}"

    # Check built-in properties
    if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast or ip.is_reserved:
        return True, f"Target IP {ip} is private, loopback, or reserved"

    return False, ""


def validate_destination_safety(
    raw_url: str, 
    resolve_dns: bool = True
) -> Tuple[str, List[str]]:
    """
    Validate that a URL does not target prohibited destinations or bypass SSRF controls.
    
    Returns:
        Tuple of (canonical_scheme_and_host, list_of_resolved_ips)
    
    Raises:
        SSRFBlockedError: If destination violates safety rules.
    """
    if not raw_url or not isinstance(raw_url, str):
        raise SSRFBlockedError("URL cannot be empty", code="EMPTY_URL")

    # Split URL
    try:
        parts = urlsplit(raw_url.strip())
    except Exception as e:
        raise SSRFBlockedError(f"Malformed URL structure: {str(e)}", code="MALFORMED_URL")

    scheme = (parts.scheme or "").lower()
    if scheme not in ALLOWED_SCHEMES:
        raise SSRFBlockedError(
            f"Prohibited scheme '{scheme}'. Only {ALLOWED_SCHEMES} are allowed.",
            code="UNSAFE_SCHEME"
        )

    if not parts.netloc:
        raise SSRFBlockedError("URL missing hostname/authority", code="MISSING_HOST")

    hostname = parts.hostname
    if not hostname:
        raise SSRFBlockedError("Unable to extract valid hostname", code="INVALID_HOST")

    # Port restriction
    port = parts.port
    if port is not None and port not in ALLOWED_PORTS:
        raise SSRFBlockedError(
            f"Port {port} is prohibited. Allowed ports: {ALLOWED_PORTS}",
            code="UNSAFE_PORT"
        )

    # 1. Direct IP check (covers numeric literals, hex, octal, IPv6)
    parsed_ip = parse_numeric_ip(hostname)
    resolved_ips: List[str] = []

    if parsed_ip:
        denied, reason = is_ip_denied(parsed_ip)
        if denied:
            raise SSRFBlockedError(reason, code="PRIVATE_OR_METADATA_IP", target_ip=str(parsed_ip))
        resolved_ips.append(str(parsed_ip))
        return f"{scheme}://{hostname}", resolved_ips

    # Reject obvious internal names without DNS query
    lower_host = hostname.lower()
    if lower_host in {"localhost", "localhost.localdomain"} or lower_host.endswith(".local") or lower_host.endswith(".internal"):
        raise SSRFBlockedError(f"Local/internal hostname '{hostname}' is blocked", code="INTERNAL_HOSTNAME")

    # 2. DNS resolution and IP validation
    if resolve_dns:
        try:
            addr_info = socket.getaddrinfo(
                hostname, 
                port or (443 if scheme == "https" else 80),
                family=socket.AF_UNSPEC,
                type=socket.SOCK_STREAM
            )
            for item in addr_info:
                sockaddr = item[4]
                ip_str = sockaddr[0]
                resolved_ip = ipaddress.ip_address(ip_str)
                denied, reason = is_ip_denied(resolved_ip)
                if denied:
                    raise SSRFBlockedError(
                        f"Resolved IP {ip_str} for host '{hostname}' is blocked: {reason}",
                        code="DNS_RESOLVED_PRIVATE_IP",
                        target_ip=ip_str
                    )
                if ip_str not in resolved_ips:
                    resolved_ips.append(ip_str)

        except socket.gaierror as e:
            # Domain does not resolve - lexical scanning may continue, but active connections are blocked
            pass
        except SSRFBlockedError:
            raise
        except Exception as e:
            raise SSRFBlockedError(f"DNS validation error: {str(e)}", code="DNS_RESOLUTION_ERROR")

    return f"{scheme}://{hostname}", resolved_ips

