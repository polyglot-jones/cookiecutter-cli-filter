import argparse
import configparser
import logging
from pathlib import Path

from gwpycore import parse_config

LOG = logging.getLogger("main")

DEFAULT_DATA_DIR = "~/{{ cookiecutter.tool_name_slug }}_data"


def __storage_section(parser, config):
    config.dataDir = Path(DEFAULT_DATA_DIR)
    config.imagesDir = config.dataDir / "images"

    if parser.has_section("storage"):
        config.dataDir = parser["storage"].getpath("dataDir", config.dataDir)
        config.imagesDir = parser["storage"].getpath("imagesDir", config.imagesDir)


def load_config(configfile, ini: str = "", initial_config: argparse.Namespace = None) -> argparse.Namespace:
    """
    Parse the contents of the config (INI) file.

    Args:
        ini -- (optional) If not blank, than this text will be parsed, instead of the
                contents of configfile.
        config -- (optional) An existing argparse.Namespace to be appended to (typically
                the command line args, so that all of the config settings are in one place).

    Returns:
      An object of type argparse.Namespace. Access the settings like object attributes (e.g. config.datum).
    """
    LOG.trace("Loading config")
    parser = parse_config(LOG, configfile=Path(configfile), ini=ini)
    config = initial_config if initial_config else argparse.Namespace()

    # issues = []
    __storage_section(parser, config)
    # for issue in issues:
    #     LOG.exception(issue)

    LOG.debug(f"config = {config}")
    return config


__all__ = "load_config"
