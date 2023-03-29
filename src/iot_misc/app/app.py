import asyncio

# from app.logger import init_logger


async def main():
    from parsers.cli import arguments

    print(arguments)
