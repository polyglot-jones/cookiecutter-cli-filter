from argparse import ArgumentParser, Namespace
from pathlib import Path
from gwpycore import basic_cli_parser

def load_command_line(version: str, args) -> Namespace:
    """
    Parses the command line arguments and returns a Namespace (switches) with the results.
    switches.command will be the command given (e.g. filter-one).
    If no command is given, then switches.command will be "gui".
    It will also contain the values of any optional arguments ("switches") given (e.g. --verbose).
    By calling basic_cli_parser() we quickly establish a set of common switches.
    """
    p: ArgumentParser = basic_cli_parser(
        version_text=version,
        command=True,
        devel=True,
        trace=True,
        infile=True,
        outfile=True,
        configfile_default="local\\{{ cookiecutter.tool_name_slug }}.ini",
        logfile_default="{{ cookiecutter.tool_name_slug }}.log",
    )
    switches = p.parse_args(args)  # noqa F811
    if switches.logfile:
        switches.logfile = Path(switches.logfile)
    if switches.configfile:
        switches.configfile = Path(switches.configfile)
    if switches.infile:
        switches.infile = Path(switches.infile)
    if switches.outfile:
        switches.outfile = Path(switches.outfile)
    return switches  # noqa F811

__all__ = ("load_command_line",)