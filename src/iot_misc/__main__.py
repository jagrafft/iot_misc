import asyncio

from pathlib import Path
from time import localtime, strftime
from sys import exit

from app import main, session_directory_init
from parsers.cli import arguments
from parsers.toml_conf import load_toml_config

if __name__ == "__main__":
    app_start_localtime = strftime("%Y-%m-%dT%H%M%S", localtime())

    # Attempt to load TOML configuration file #
    try:
        print(f"Attempting to load '{arguments['config']}'...", end="")
        config = load_toml_config(arguments["config"])
    except Exception as e:
        print("EXCEPTION")
        print(repr(e))
        print("EXITING")
        exit()
    else:
        print("SUCCESS")
    ##

    # Validate TOML configuration file #
    # TODO Implement validation
    ##

    # Initialize output directory #
    app_outfile = Path(f"{config['path']}/{app_start_localtime}")

    try:
        print(f"Initializing directory at '{app_outfile}'...", end="")
        # TODO refactor
        subdirs = ["images"] if "fswebcam" in config["sources"] else []
        session_directory_init(app_outfile, subdirs)
    except Exception as e:
        print("EXCEPTION")
        print(repr(e))
        print("EXITING")
        exit()
    else:
        config["output"] = { "filepaths": { "app": app_outfile }}

        # TODO refactor so 'fswebcam' is not hard-coded
        if "fswebcam" in config["sources"]:
            config["output"]["filepaths"]["fswebcam"] = Path(app_outfile / "images")

        print("SUCCESS")
    ##

    # from app.logger import init_logger
    # config["logger"] = init_logger("")

    asyncio.run(main(config))
