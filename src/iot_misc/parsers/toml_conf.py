import asyncio

from pathlib import Path
from pytomlpp import load


def load_toml_config(path: Path) -> dict:
    """Check that `path` exists and is a valid TOML file; raise `Exception` if not."""
    try:
        config = load(path)
    except Exception:
        raise
    else:
        return config

def toml_config(path: str) -> Path:
    try:
        p = Path(path)
    except Exception:
        raise
    else:
        if p.suffix == ".toml":
            return p.resolve() 
        else:
            raise ValueError("Path suffix not equal to '.toml'.")