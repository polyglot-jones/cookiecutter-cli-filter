import configparser, shutil, os, logging
from pathlib import Path

from .exceptions import *
from dataclasses import dataclass
from ..logic.config import Configuration as LogicConfiguration
from ..util.config_helpers import asPath


LOG = logging.getLogger("{{ cookiecutter.tool_name_slug }}")

BACKGROUND_COLORS = ["white","black","brown"] # better yet, use an enum for things like this -- this is just a quick example

@dataclass
class CoreConfiguration:
    """Child class for the core-specific configuration settings"""
    my_url: str = ""
    background_color: str = "white"

    def setParsedOptions(self, parser, issues):
        if parser.has_section('my_section'):
            self.my_url = parser.get('my_section','my_url', self.my_url)
            self.background_color = parser.get('my_section','background_color', self.background_color)
            if self.background_color not in BACKGROUND_COLORS:
                raise {{ cookiecutter.tool_name_camel_case }}ConfigError('[my_section]background_color', self.background_color, BACKGROUND_COLORS)

    def runtimeValidation(self,issues):
        """Look for non-passive problems in a running environment."""
        pass

@dataclass
class Configuration:
    """
    This is the parent class for all configuration settings.
    There are (to start) two child configs: CoreConfiguration (above), and logic.Configuration
    
    "Configs" are read-only (vs. "Settings" that get written back to storage).
    Configs includes things like the URLs to REST services.

    The logic subfolder has its own (child) Config object. 
    Be sure to follow that pattern when adding additional subfolders.
    """
    core: CoreConfiguration
    logic: LogicConfiguration

    def __init__(self):
        self.core =  CoreConfiguration()
        self.logic = LogicConfiguration()

    def setFromINIFile(self, configfilename: Path):
        try:
            with configfilename.open("rt") as configFile:
                ini = configFile.read()
            self.setFromINIContents(ini)
        except FileNotFoundError:
            pass
        except Exception as e:
            raise {{ cookiecutter.tool_name_camel_case }}ConfigError(f"Cannot read configuration file {configfilename}. {e}")


    def setFromINIContents(self, configfilecontents: str):
        ADDITIONAL_CONFIGPARSER_CONVERTERS = {
            'path': asPath
        }
        parser = configparser.ConfigParser(
            converters=ADDITIONAL_CONFIGPARSER_CONVERTERS)
        parser.read_string(configfilecontents)
        issues = []
        
        self.core.setParsedOptions(parser, issues)
        self.logic.setParsedOptions(parser, issues)

        if issues:
            raise {{ cookiecutter.tool_name_camel_case }}ConfigError("\n".join(issues))


    def runtimeValidation(self):
        issues = []
        self.core.runtimeValidation(issues)
        self.logic.runtimeValidation(issues)
        if issues:
            raise {{ cookiecutter.tool_name_camel_case }}ConfigError("\n".join(issues))



    