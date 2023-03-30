import asyncio

from logging import Logger
from pathlib import Path
from sys import exit


async def main(config: dict, logger: Logger) -> None:
    logger.info("\n### main(config:dict) -> None ###")
    logger.info(config)
