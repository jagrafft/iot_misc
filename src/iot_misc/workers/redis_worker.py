import asyncio

from logging import Logger
from redis import Redis

async def write_to_xstream(rdb: Redis, stream: str, data: dict, logger: Logger) -> None:
    """Write `data` to Redis XStream."""
    try:
        logger.info(f"Write data to Redis Stream '{stream}'")
        rdb.xadd(stream, data)
    except Exception:
        logger.exception("Could not write to stream")
        raise
    else:
        logger.info("SUCCESS")
        
