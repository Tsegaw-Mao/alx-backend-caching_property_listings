from django.core.cache import cache
from .models import Property

def get_all_properties():
    # Try to get the cached queryset
    properties = cache.get("all_properties")
    if properties is None:
        # Not in cache, fetch from database
        properties = list(Property.objects.all().values(
            "id", "title", "description", "price", "location", "created_at"
        ))
        # Store in cache for 1 hour (3600 seconds)
        cache.set("all_properties", properties, 3600)
    return properties

import logging
from django_redis import get_redis_connection

logger = logging.getLogger(__name__)

def get_redis_cache_metrics():
    try:
        # Connect to Redis
        redis_conn = get_redis_connection("default")

        # Get keyspace hits and misses
        info = redis_conn.info()
        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)

        # Calculate hit ratio safely
        total_requests = hits + misses
        hit_ratio = hits / total_requests if total_requests > 0 else 0

        # Log metrics
        logger.info(f"Redis Cache Metrics: hits={hits}, misses={misses}, hit_ratio={hit_ratio:.2f}")

        return {
            "hits": hits,
            "misses": misses,
            "hit_ratio": hit_ratio
        }

    except Exception as e:
        logger.error(f"Error retrieving Redis cache metrics: {e}")
        return {
            "hits": 0,
            "misses": 0,
            "hit_ratio": 0
        }
