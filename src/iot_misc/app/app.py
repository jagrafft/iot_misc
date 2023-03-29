import asyncio

from pathlib import Path
from sys import exit

async def main(config: dict) -> None:
    print("\n### main(config:dict) -> None ###")
    print(config)