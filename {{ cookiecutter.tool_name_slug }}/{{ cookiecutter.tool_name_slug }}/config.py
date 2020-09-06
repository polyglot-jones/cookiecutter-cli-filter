import argparse
import configparser
import logging
from pathlib import Path

from gwpycore import parse_config, as_path

LOG = logging.getLogger("main")

DEFAULT_DATA_DIR = "~/{{ cookiecutter.tool_name_slug }}_data"


def __storage_section(parser, config):
    config.dataDir = Path(DEFAULT_DATA_DIR)
    config.imagesDir = config.dataDir / "images"

    if parser.has_section("storage"):
        config.dataDir = parser["storage"].getpath("dataDir", config.dataDir)
        config.imagesDir = parser["storage"].getpath("imagesDir", config.imagesDir)


def load_config(SWITCHES, ini: str = "", config: argparse.Namespace = None) -> argparse.Namespace:
    """
    Parse the contents of the config (INI) file.

    Args:
      ini (optional) -- If not blank, than this text will be parsed, instead of the contents of SWITCHES.configfile.
      config (optional) -- An existing argparse.Namespace to be appended to

    Returns:
      An object of type argparse.Namespace. Access the settings as object attributes (e.g. config.datum).
    """
    LOG.trace("Loading config")
    LOG.debug(f"SWITCHES = {SWITCHES}")
    parser = parse_config(LOG, configfile=Path(SWITCHES.configfile), ini=ini)

    if not config:
        config = argparse.Namespace()

    # issues = []
    __storage_section(parser, config)

    # for issue in issues:
    #     LOG.exception(issue)

    LOG.debug(f"config = {config}")
    return config


__all__ = "load_config"
