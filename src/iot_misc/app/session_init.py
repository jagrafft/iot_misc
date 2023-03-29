import asyncio

from pathlib import Path

def session_directory_init(path: Path, subdirs: list = []):
    print(f"\n\t- session_directory_init: {path}")

    if subdirs:
        print("\t- subdirs:")
        for subdir in subdirs:
            print(f"\t\t- {subdir}")
