"""Background Threat Feed Scheduler.

Leverages APScheduler to orchestrate non-blocking periodic ingestion
from upstream feeds (OpenPhish, URLhaus) with error isolation and telemetry logging.
"""

import logging
import asyncio
from typing import Optional
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from ..config import settings
from .feed_ingestion import ingest_openphish_feed, ingest_urlhaus_feed, get_threat_intel_metrics

logger = logging.getLogger("urlsentinel.scheduler")

_scheduler: Optional[AsyncIOScheduler] = None


async def run_feed_refresh():
    """Execute scheduled feed ingestion tasks across all threat intelligence sources."""
    logger.info("Starting background threat intelligence synchronization cycle...")
    try:
        openphish_count, urlhaus_count = await asyncio.gather(
            ingest_openphish_feed(timeout=settings.FEED_TIMEOUT_SECONDS),
            ingest_urlhaus_feed(timeout=settings.FEED_TIMEOUT_SECONDS),
            return_exceptions=True,
        )

        op_records = openphish_count if isinstance(openphish_count, int) else 0
        uh_records = urlhaus_count if isinstance(urlhaus_count, int) else 0

        metrics = get_threat_intel_metrics()
        logger.info(
            "Threat feed synchronization finished: +%d OpenPhish, +%d URLhaus. Total indexed hashes: %d",
            op_records,
            uh_records,
            metrics["indexed_url_hashes"],
        )
    except Exception as e:
        logger.error("Error during threat feed synchronization cycle: %s", e)


def start_feed_scheduler() -> Optional[AsyncIOScheduler]:
    """Initialize and start the background feed scheduler."""
    global _scheduler
    if _scheduler is not None and _scheduler.running:
        return _scheduler

    _scheduler = AsyncIOScheduler(timezone="UTC")

    # Schedule recurring job every N minutes
    interval_mins = max(settings.FEED_REFRESH_INTERVAL_MINUTES, 5)
    _scheduler.add_job(
        run_feed_refresh,
        trigger=IntervalTrigger(minutes=interval_mins),
        id="threat_feed_refresh_job",
        name="Refresh OpenPhish & URLhaus threat feeds",
        replace_existing=True,
        max_instances=1,
    )

    _scheduler.start()
    logger.info("Threat feed scheduler started (interval: every %d minutes)", interval_mins)
    return _scheduler


def shutdown_feed_scheduler():
    """Gracefully terminate background scheduler."""
    global _scheduler
    if _scheduler and _scheduler.running:
        try:
            _scheduler.shutdown(wait=False)
            logger.info("Threat feed scheduler stopped.")
        except Exception as e:
            logger.warning("Error stopping scheduler: %s", e)
        _scheduler = None

