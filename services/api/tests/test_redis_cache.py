"""Unit tests for the Redis and in-memory persistent caching layer."""

import pytest
from urlsentinel.cache.redis_cache import RedisCacheManager, cache_manager


@pytest.mark.asyncio
async def test_memory_fallback_cache():
    """Verify that caching operations succeed seamlessly in local memory mode."""
    mgr = RedisCacheManager()
    
    # Store a dummy verdict
    dummy_verdict = {
        "id": "scan_test_123",
        "url": "https://example.com/test",
        "url_hash": "hash_test_123",
        "verdict": "BENIGN",
        "risk_score": 5,
        "confidence": "HIGH",
    }
    
    await mgr.store_verdict(
        url_hash=dummy_verdict["url_hash"],
        scan_id=dummy_verdict["id"],
        verdict_dict=dummy_verdict,
    )
    
    # Retrieve by hash
    res_hash = await mgr.get_verdict_by_hash("hash_test_123")
    assert res_hash is not None
    assert res_hash["id"] == "scan_test_123"
    assert res_hash["verdict"] == "BENIGN"
    
    # Retrieve by ID
    res_id = await mgr.get_verdict_by_id("scan_test_123")
    assert res_id is not None
    assert res_id["url_hash"] == "hash_test_123"
    
    # Non-existent key returns None
    missing = await mgr.get_verdict_by_hash("non_existent_hash")
    assert missing is None

