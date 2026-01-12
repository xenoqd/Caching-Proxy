from fastapi.responses import Response
from fastapi import APIRouter, Request
import config

from core.logger import logger

from service.cache import make_cache_key, get_cached_response, set_cached_response
from service.proxy import forward_request

router = APIRouter()


@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy(path: str, request: Request):
    logger.info(f"INCOMING → {request.method} /{path}")

    if config.ORIGIN_URL is None:
        logger.error("ORIGIN_URL is not configured")
        return Response("Origin not configurated", status_code=500)

    query = request.url.query
    full_url = f"{config.ORIGIN_URL}/{path}"
    if query:
        full_url += f"?{query}"

    logger.info(f"FULL URL → {full_url}")

    cache_key = make_cache_key(request.method, full_url)
    logger.info(f"CACHE KEY → {cache_key}")

    cached = await get_cached_response(cache_key)
    if cached:
        logger.info("RESPONSE FROM CACHE")

        headers = cached["headers"]
        headers["X-Cache"] = "HIT"

        return Response(
            content=cached["content"],
            status_code=cached["status_code"],
            headers=headers,
        )

    logger.info("CACHE MISS → forwarding to origin")

    body = await request.body()

    resp = await forward_request(
        method=request.method,
        url=full_url,
        headers=dict(request.headers),
        body=body,
    )

    await set_cached_response(cache_key, resp)
    logger.info("RESPONSE SAVED TO CACHE")

    resp["headers"]["X-Cache"] = "MISS"

    return Response(
        status_code=resp["status_code"],
        content=resp["content"],
        headers=resp["headers"],
    )
