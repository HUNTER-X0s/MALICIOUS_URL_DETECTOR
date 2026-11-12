"""Unit tests for the periodic threat feed scheduler."""

import pytest
import asyncio
from urlsentinel.core.feed_scheduler import (
    start_feed_scheduler,
    shutdown_feed_scheduler,
    run_feed_refresh,
)


@pytest.mark.asyncio
async def test_scheduler_lifecycle():
    """Verify scheduler starts and stops gracefully without throwing."""
    sched = start_feed_scheduler()
    assert sched is not None
    assert sched.running is True

    # Calling start again returns the running instance (singleton)
    same_sched = start_feed_scheduler()
    assert same_sched is sched

    # Graceful shutdown
    shutdown_feed_scheduler()
    await asyncio.sleep(0.05)
    assert sched.running is False


@pytest.mark.asyncio
async def test_feed_refresh_execution():
    """Verify run_feed_refresh executes cleanly without uncaught exceptions."""
    # Runs the async gather over feeds with timeout isolation
    await run_feed_refresh()
