from argparse import ArgumentParser, Namespace
from pathlib import Path
from gwpycore import basic_cli_parser
from {{ cookiecutter.tool_name_slug }}.core.{{ cookiecutter.tool_name_slug }}_filter import {{ cookiecutter.tool_name_camel_case }}Filter

def load_command_line(version: str, args) -> Namespace:
    """
    Parses the command line arguments and returns a Namespace with the results.
    All of the usual switches are allowed (--verbose, --debug, --logfile mylog.log, ...).
    The user can also specify an optional command (count or latest, for example).
    If a command is given, then the namespace will have a command attribute with a corresponding value.
    """
    parser: ArgumentParser = basic_cli_parser(
        version_text=version,
        command=True,
        devel=True,
        trace=True,
        infile=True,
        outfile=True,
        configfile_default="local\\{{ cookiecutter.tool_name_slug }}.ini",
        logfile_default="{{ cookiecutter.tool_name_slug }}.log",
    )
    parser.add_argument("command", choices={{ cookiecutter.tool_name_camel_case }}Filter.commands, nargs="?", default="gui", help=f"Filter commands availble: {', '.join({{ cookiecutter.tool_name_camel_case }}Filter.commands)}")
    switches = parser.parse_args(args)  # noqa F811
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
