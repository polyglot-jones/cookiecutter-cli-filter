import os, sys, logging
from os import name
from pathlib import Path
from sys import stdin, stdout, stderr
from typing import Optional
import typer

__package__ = str("{{ cookiecutter.tool_name_slug }}")
__version__ = "{{ cookiecutter.project_version }}"

from .core.command_line import parse_args
from .core.exceptions import *
from .core.config import Configuration
from .util.logger import setup_logging, DIAGNOSTIC, DEBUG, TRACE, INFO
from .logic.{{ cookiecutter.tool_name_slug }}_filter import {{ cookiecutter.tool_name_camel_case }}Filter

# In case we try to post a logging message before logging is actually set up
LOG = logging.getLogger("stub")


# Typer handles the command-line-interface (CLI) for us by automatically
# creating arguments and switches based on the arguments of main() and/or
# any sub-command methods.
# See the documentation in https://typer.tiangolo.com.
app = typer.Typer()

def load_configuration(configfile: Optional[Path]) -> Configuration:
    config = Configuration()
    if configfile and configfile.is_file():
        LOG.trace("Loading configuration file {configfile}")
        try:
            config.setFromINIFile(configfile)
            config.runtimeValidation()
        except {{ cookiecutter.tool_name_camel_case }}ConfigError as e:
            LOG.exception(e)
    return config

def show_version(value: bool):
    if value:
        typer.echo(f"{{ cookiecutter.tool_name }} {__version__}")
        raise typer.Exit(0)

@app.command()
def count_lines(skip: bool = typer.Option(..., help = "Skips blanks lines")):
    """
    Counts the lines of text.
    """
    try:
        with {{ cookiecutter.tool_name_camel_case }}Filter() as filter_group:
            filter_group.count_lines()
    except {{ cookiecutter.tool_name_camel_case }}Error as e:
        finish(e)
    finish()

@app.command()
def latest():
    """
    Filters out any lines that have been revised.
    (That is, lines that are followed by a "Revision:" line.)
    """
    try:
        with {{ cookiecutter.tool_name_camel_case }}Filter() as filter_group:
            filter_group.just_revised()
    except {{ cookiecutter.tool_name_camel_case }}Error as e:
        finish(e)
    finish()

def finish(exception: Optional[Exception] = None):
    LOG.trace("Finishing")
    exitcode = 0
    if exception:
        exitcode = 1
        if hasattr(exception, "exitcode"):
            exitcode = exception.exitcode
        LOG.uncaught(exception)

    LOG.diagnostic(f"Exit code = {exitcode}")
    raise typer.Exit(exitcode)


# This common code is executed first, before any sub-command
@app.callback()
def main(
    version: bool=typer.Option(None, "--version", callback=show_version, is_eager=True, help="Displays this tools's version number"),
    infile: Path = typer.Option(None, "-i", "--infile", help="specifies the name (and path) for the input (instead of stdin)"),
    outfile: Path = typer.Option(None, "-o", "--outfile", help="specifies the name (and path) for the output (instead of stdout)"),
    logfile: Optional[Path] = typer.Option(None, "-l", "--logfile", help="specifies the name (and path) for the log file (none by default)"),
    configfile: Optional[Path] = typer.Option(None, "-c", "--configfile", help="specifies the name (and path) for the configuration file (none by default)"),
    verbose: bool=typer.Option(None, "-v", "--verbose", help="sets loglevel to DIAGNOSTIC"),
    debug: bool=typer.Option(None, "--debug", help="sets loglevel to DEBUG (very verbose)"),
    trace: bool = typer.Option(None, "--trace", help="sets loglevel to TRACE (very, very verbose)"),
    nocolor: bool = typer.Option(None, "--nocolor", help="turns off coloring the log messages that are sent to the console"),
    devmode: bool = typer.Option(None, "-d", "--devel", help="turns on developer mode")):
    """
    TODO: This awesome tool filters text in one of several ways.
    (See the list of commands, below.)
    But first, here are the various options available that are common to all of the commands:
    """
    loglevel = DIAGNOSTIC if verbose else DEBUG if debug else TRACE if trace else INFO

    setup_logging(name="{{ cookiecutter.tool_name_camel_case }}", loglevel = loglevel, logfile = logfile, nocolor = nocolor)
    LOG = logging.getLogger("{{ cookiecutter.tool_name_camel_case }}")
    LOG.diagnostic(f"loglevel = {loglevel}")

    CONFIG = load_configuration(configfile)

    if devmode:
        LOG.info("Running in dev mode.")
        # TODO special setup for dev mode (e.g. suppressing actual web service calls, not actually sending any emails)

    if infile:
        sys.stdin = open(infile, "r")
        LOG.info(f"Input will be taken from {infile}, rather than stdin.")

    if outfile:
        sys.stdout = open(outfile, "w")
        LOG.info(f"Output will be written to {outfile}, rather than stdout.")

if __name__ == "__main__":
    # The Typer app handles parsing the commad-line arguments and then dispatching the appropriate sub-command handler
    app()
