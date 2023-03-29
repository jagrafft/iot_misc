import asyncio
import logging
import redis

async def write_to_xstream(rdb: redis.Redis, stream: str, row: dict, logger: logging.Logger) -> None:
    """Write `row` to Redis XStream."""
    try:
        logger.info(f"Write data to Redis Stream '{stream}'")
        redis_con.xadd(stream, row)
    except Exception:
        logger.exception("Could not write to stream")
    else:
        logger.info("SUCCESS")
        
