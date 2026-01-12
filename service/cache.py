import json
import base64
from redis.asyncio import Redis, RedisError
from core.logger import logger


redis = Redis(
    host="localhost",
    port=6379,
    decode_responses=False,
    socket_timeout=1.2,
    socket_connect_timeout=1.2,
    retry_on_timeout=True,
    health_check_interval=10,
)


def make_cache_key(method: str, url: str) -> str:
    logger.info(f"CACHE KEY {method}: {url}")
    return f"cache:{method}:{url}"


async def get_cached_response(key: str):
    try:
        data = await redis.get(key)
        if not data:
            logger.info(f"CACHE MISS → {key}")
            return None
        logger.info(f"CACHE HIT → {key}")
        cached = json.loads(data)

        cached["content"] = base64.b64decode(cached["content"])
        return cached
    except RedisError:
        logger.warning(f"Redis unavailable during GET → skipping cache ({str(e)})")
        return None
    except Exception as e:
        logger.error(f"Unexpected error reading cache: {str(e)}", exc_info=True)
        return None


async def set_cached_response(key: str, response: dict, ttl: int = 6000):
    try:
        response_to_store = response.copy()
        response_to_store["content"] = base64.b64encode(response["content"]).decode()

        await redis.set(
            key,
            json.dumps(response_to_store),
            ex=ttl,
        )
    except RedisError as e:
        logger.warning(f"Redis unavailable during SET → cache write skipped ({str(e)})")
    except Exception as e:
        logger.error(f"Unexpected error writing to cache: {str(e)}", exc_info=True)


async def clear_cache():
    try:
        keys = await redis.keys("cache:*")
        if keys:
            await redis.delete(*keys)
    except RedisError:
        logger.warning("Redis unavailable → cache clear skipped")
    except Exception as e:
        logger.error(f"Error during cache clear: {str(e)}", exc_info=True)
