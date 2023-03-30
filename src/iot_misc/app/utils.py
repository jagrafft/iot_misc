import asyncio

from pathlib import Path
from re import sub as resub
from unicodedata import normalize as ucnormalize


def session_directory_init(path: Path, subdirs: list = []) -> None:
    try:
        print(f"Creating session directory at '{path}'...", end="")
        Path.mkdir(path)
    except Exception:
        print("EXCEPTION")
        raise
    else:
        print("SUCCESS")

    if subdirs:
        for subdir in subdirs:
            try:
                subdir_path = Path(path / subdir)
                print(f"\tCreating subdirectory {subdir_path}...", end="")
                Path.mkdir(subdir_path)
            except Exception:
                print("EXCEPTION")
                raise
            else:
                print("SUCCESS")


def slugify(value: str, allow_unicode=False) -> str:
    """From https://docs.djangoproject.com/en/4.1/_modules/django/utils/text/

    Documentation entry: https://docs.djangoproject.com/en/4.1/ref/utils/#django.utils.text.slugify"""
    value = str(value)

    if allow_unicode:
        value = ucnormalize("NFKC", value)
    else:
        value = ucnormalize("NFKC", value).encode("ascii", "ignore").decode("ascii")

    value = resub(r"[^\w\s-]", "", value.lower())

    return resub(r"[-\s]+", "-", value).strip("-_")
