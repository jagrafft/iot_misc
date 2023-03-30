import asyncio

from pathlib import Path
from time import localtime, strftime
from sys import exit

from app import init_logger, main, session_directory_init, slugify
from parsers.cli import arguments
from parsers.toml_conf import load_toml_config

if __name__ == "__main__":
    app_start_localtime = strftime("%Y-%m-%dT%H%M%S", localtime())

    # Attempt to load TOML configuration file #
    try:
        print(f"Attempting to load '{arguments['config']}'...")
        config = load_toml_config(arguments["config"])
    except Exception as e:
        print("EXCEPTION")
        print(repr(e))
        print("EXITING")
        exit()
    else:
        print("CONFIGURATION LOADED SUCCESSFULLY")
    ##

    # TODO Implement validation
    # Validate TOML configuration file #
    ##

    # Initialize output directory for session #
    session_name = f"{slugify(config['name'])}_{app_start_localtime}"
    app_outfile = Path(f"{config['path']}/{session_name}")

    try:
        print(f"Initializing session output directory at '{app_outfile}'...")
        # TODO refactor
        subdirs = ["images"] if "fswebcam" in config["sources"] else []

        session_directory_init(app_outfile, subdirs)
    except Exception as e:
        print("EXCEPTION")
        print(repr(e))
        print("EXITING")
        exit()
    else:
        config["session_name"] = session_name
        config["output_paths"] = {"app": app_outfile}

        # TODO refactor so 'fswebcam' is not hard-coded
        if "fswebcam" in config["sources"]:
            config["output_paths"]["fswebcam"] = Path(app_outfile / "images")

        print("OUTPUT DIRECTORY INITIALIZED")
    ##

    print("Initializing logger...")
    logger = init_logger(app_outfile, f"{config['session_name']}", to_stdout=True)
    logger.info(
        "LOGGER INITIALIZED: Switching from `print` statements to Logger for reporting"
    )

    asyncio.run(main(config, logger))
