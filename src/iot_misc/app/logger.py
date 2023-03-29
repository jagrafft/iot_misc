import logging

from pathlib import Path


# TODO Should be `async`?
def init_logger(
    log_path: Path,
    log_name: str,
    log_level: int = logging.DEBUG,
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    to_stdout: bool = True,
) -> logging.Logger:
    """Initialize then return a logger.

    Keyword arguments:
    log_level -- Logging Level to use
    log_format -- Logging format to use
    to_stdout -- Print to `stdout`
    """
    name = log_name
    stdout = to_stdout

    # Initiate logger
    logger = logging.getLogger(log_name)
    logger.setLevel(log_level)

    formatter = logging.Formatter(log_format)
    file_handler = logging.FileHandler(Path(log_path / f"{log_name}.log"))
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    if to_stdout:
        from sys import stdout
        
        stdout_handler = logging.StreamHandler(stdout)
        logger.addHandler(stdout_handler)

    return logger
