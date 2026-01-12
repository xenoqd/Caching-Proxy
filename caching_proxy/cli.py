from service.cache import clear_cache
from core.logger import logger

import argparse
import config
import uvicorn
import asyncio


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--origin")
    parser.add_argument("--clear-cache", action="store_true")

    args = parser.parse_args()

    if args.clear_cache:
        asyncio.run(clear_cache())
        print("Cache cleared")
        return

    if not args.origin:
        parser.error("--origin is required when starting the server")

    config.ORIGIN_URL = args.origin

    uvicorn.run("main:app", host="127.0.0.1", port=args.port)

    logger.info(f"Proxy started on port {args.port}")
    logger.info(f"Origin → {args.origin}")
