import pytomlpp

from pathlib import Path


# TODO Use `asyncio`
def toml_config(path: str):
    """Check that `path` exists and is a valid TOML file; raise `Exception` if not."""
    print(path)
    try:
        p = Path(path)
    except Exception:
        raise
    else:
        if p.is_file():
            return p
        else:
            raise ValueError("Path is not a file")
