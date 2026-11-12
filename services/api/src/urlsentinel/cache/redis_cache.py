"""Redis Persistence and High-Performance Distributed Caching Layer.

Provides asynchronous Redis caching with graceful in-memory fallback,
automatic TTL expiration, and serialized verdict records.
"""

import json
import logging
from typing import Optional, Dict, Any
from ..config import settings

logger = logging.getLogger("urlsentinel.cache")

# Local in-memory fallback storage
_MEMORY_CACHE_BY_HASH: Dict[str, Dict[str, Any]] = {}
_MEMORY_CACHE_BY_ID: Dict[str, Dict[str, Any]] = {}


class RedisCacheManager:
    """Manages Redis connection lifecycle with graceful fallback."""

    def __init__(self):
        self._redis = None
        self._is_connected = False
        self._connection_attempted = False

    async def get_client(self):
        """Lazy initializer for Redis async client."""
        if not settings.REDIS_ENABLED:
            return None

        if self._redis is None and not self._connection_attempted:
            self._connection_attempted = True
            try:
                import redis.asyncio as aioredis
                self._redis = aioredis.from_url(
                    settings.REDIS_URL,
                    decode_responses=True,
                    socket_connect_timeout=2.0,
                    socket_timeout=2.0,
                )
                await self._redis.ping()
                self._is_connected = True
                logger.info("Successfully connected to Redis persistent cache at %s", settings.REDIS_URL)
            except Exception as e:
                logger.warning(
                    "Redis connection unavailable (%s). Operating in high-performance local memory fallback mode.",
                    str(e),
                )
                self._is_connected = False
                self._redis = None

        return self._redis if self._is_connected else None

    async def get_verdict_by_hash(self, url_hash: str) -> Optional[Dict[str, Any]]:
        """Retrieve a cached verdict by normalized URL hash."""
        client = await self.get_client()
        if client:
            try:
                val = await client.get(f"scan:hash:{url_hash}")
                if val:
                    return json.loads(val)
            except Exception as e:
                logger.debug("Redis read error on hash %s: %s", url_hash, e)

        # Fallback to in-memory store
        return _MEMORY_CACHE_BY_HASH.get(url_hash)

    async def get_verdict_by_id(self, scan_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a cached verdict by unique scan ID."""
        client = await self.get_client()
        if client:
            try:
                val = await client.get(f"scan:id:{scan_id}")
                if val:
                    return json.loads(val)
            except Exception as e:
                logger.debug("Redis read error on scan_id %s: %s", scan_id, e)

        # Fallback to in-memory store
        return _MEMORY_CACHE_BY_ID.get(scan_id)

    async def store_verdict(
        self,
        url_hash: str,
        scan_id: str,
        verdict_dict: Dict[str, Any],
        ttl_seconds: Optional[int] = None,
    ) -> None:
        """Store a verdict record indexed by both URL hash and scan ID."""
        ttl = ttl_seconds or settings.REDIS_CACHE_TTL_SECONDS
        serialized = json.dumps(verdict_dict, default=str)

        # Always update in-memory cache
        _MEMORY_CACHE_BY_HASH[url_hash] = verdict_dict
        _MEMORY_CACHE_BY_ID[scan_id] = verdict_dict

        client = await self.get_client()
        if client:
            try:
                pipe = client.pipeline()
                pipe.set(f"scan:hash:{url_hash}", serialized, ex=ttl)
                pipe.set(f"scan:id:{scan_id}", serialized, ex=ttl)
                await pipe.execute()
            except Exception as e:
                logger.warning("Failed to store verdict in Redis: %s", e)

    async def ping(self) -> bool:
        """Check if Redis backend is responsive."""
        client = await self.get_client()
        if client:
            try:
                return await client.ping()
            except Exception:
                return False
        return False

    async def close(self) -> None:
        """Close connection pools on shutdown."""
        if self._redis:
            try:
                await self._redis.close()
            except Exception:
                pass
            self._redis = None
            self._is_connected = False


# Global cache manager instance
cache_manager = RedisCacheManager()

