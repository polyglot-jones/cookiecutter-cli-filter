from argparse import ArgumentParser, Namespace
from pathlib import Path

def load_command_line(args) -> Namespace:
    p: ArgumentParser = basic_cli_parser(
        version_text=__version__,
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