import asyncio

from logging import Logger
from pathlib import Path


async def main(config: dict, logger: Logger) -> None:
    # TODO Based on `config`...
    # [ ] initialize workers
    # [ ] pair workers with output destinations
    # [ ] sample
    # [ ] "graceful" shutdown
    logger.info("### main(config: dict, logger: Logger) -> None ###")
    logger.info(config)
