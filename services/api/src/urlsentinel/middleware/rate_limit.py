"""In-Memory Sliding Window Rate Limiting Middleware.

Complies with Blueprint §057 (Abuse Prevention) and §056 (DDoS Protection).
Prevents automated scanning abuse and resource exhaustion on public endpoints.
"""

from __future__ import annotations

import time
from collections import defaultdict
from typing import Dict, List
from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

# Endpoint rate limits: (requests_allowed, window_seconds)
RATE_LIMIT_RULES = {
    "/api/v1/scan": (60, 60),      # 60 scans per minute
    "/api/v1/report": (10, 60),    # 10 user false-positive reports per minute
}


class RateLimiterMiddleware(BaseHTTPMiddleware):
    """Sliding-window IP rate limiter middleware."""

    def __init__(self, app, exempt_paths: List[str] | None = None):
        super().__init__(app)
        self.exempt_paths = exempt_paths or ["/docs", "/redoc", "/openapi.json", "/api/v1/health"]
        # Storage: {ip_path_key: [timestamp_1, timestamp_2, ...]}
        self._history: Dict[str, List[float]] = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Bypass rate limiting for documentation and health checks
        if any(path.startswith(exempt) for exempt in self.exempt_paths):
            return await call_next(request)

        # Match path rule
        rule = None
        for rule_path, limit_tuple in RATE_LIMIT_RULES.items():
            if path.startswith(rule_path):
                rule = limit_tuple
                break

        if not rule:
            # Default rate limit for other endpoints: 120 req/min
            rule = (120, 60)

        limit_requests, window_seconds = rule
        client_ip = request.client.host if request.client else "127.0.0.1"
        key = f"{client_ip}:{path}"

        now = time.time()
        window_start = now - window_seconds

        # Prune expired timestamps
        history = self._history[key]
        self._history[key] = [t for t in history if t > window_start]
        current_count = len(self._history[key])

        if current_count >= limit_requests:
            retry_after = int(window_seconds - (now - self._history[key][0]))
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "error": "Rate Limit Exceeded",
                    "code": "RATE_LIMIT_EXCEEDED",
                    "message": f"Too many requests to {path}. Limit is {limit_requests} per {window_seconds}s.",
                    "details": {"retry_after_seconds": max(1, retry_after)},
                },
                headers={
                    "Retry-After": str(max(1, retry_after)),
                    "X-RateLimit-Limit": str(limit_requests),
                    "X-RateLimit-Remaining": "0",
                },
            )

        # Record this request
        self._history[key].append(now)
        remaining = max(0, limit_requests - (current_count + 1))

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(limit_requests)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        return response

