"""URLSentinel FastAPI Application Entrypoint."""

import asyncio
import time
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from .config import settings
from .middleware.rate_limit import RateLimiterMiddleware
from .core.feed_ingestion import initialize_threat_intel_seeds
from .core.feed_scheduler import start_feed_scheduler, shutdown_feed_scheduler, run_feed_refresh
from .cache.redis_cache import cache_manager
from .api.routes import scan, health, stats, domain, report, verify


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context for startup initialization and graceful shutdown."""
    # 1. Initialize curated threat intelligence seed database
    initialize_threat_intel_seeds()

    # 2. Connect / warm up Redis persistence cache
    await cache_manager.get_client()

    # 3. Start background periodic threat feed refresh scheduler
    start_feed_scheduler()

    # 4. Asynchronously trigger initial feed sync without blocking startup
    asyncio.create_task(run_feed_refresh())

    yield

    # Shutdown cleanup
    shutdown_feed_scheduler()
    await cache_manager.close()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Security-first real-time malicious URL detection, lexical analysis, and verdict engine.",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Sliding Window Rate Limiting Middleware
app.add_middleware(RateLimiterMiddleware)


@app.middleware("http")
async def security_and_tracing_middleware(request: Request, call_next):
    """Add security headers and tracing telemetry."""
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    start_time = time.perf_counter()

    response = await call_next(request)

    process_time_ms = round((time.perf_counter() - start_time) * 1000, 2)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Response-Time-MS"] = str(process_time_ms)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"

    return response


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    now_iso = datetime.now(timezone.utc).isoformat()
    if isinstance(exc.detail, dict):
        return JSONResponse(status_code=exc.status_code, content=exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTP Error",
            "code": f"HTTP_{exc.status_code}",
            "message": str(exc.detail),
            "timestamp": now_iso,
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    now_iso = datetime.now(timezone.utc).isoformat()
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "code": "INVALID_REQUEST_PAYLOAD",
            "message": "Input validation failed on request body",
            "details": {"errors": exc.errors()},
            "timestamp": now_iso,
        },
    )


# Register routes
app.include_router(scan.router, prefix=settings.API_V1_PREFIX)
app.include_router(health.router, prefix=settings.API_V1_PREFIX)
app.include_router(stats.router, prefix=settings.API_V1_PREFIX)
app.include_router(domain.router, prefix=settings.API_V1_PREFIX)
app.include_router(report.router, prefix=settings.API_V1_PREFIX)
app.include_router(verify.router, prefix=settings.API_V1_PREFIX)


@app.get("/", tags=["Root"])
async def root():
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "operational",
        "documentation": "/docs",
    }
