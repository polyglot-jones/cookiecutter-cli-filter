import os, sys, logging, pathlib
from sys import stdin, stdout, stderr

__package__ = str("{{ cookiecutter.tool_name_slug }}")

from .core.command_line import parse_args
from .core.exceptions import *
from .core.config import Configuration
from .util.logger import setup_logging, logging_stub
from .logic.{{ cookiecutter.tool_name_slug }}_filter import {{ cookiecutter.tool_name_camel_case }}Filter

# In case we try to post a logging message before logging is actually set up
LOG = logging_stub()

def load_switches(args):
    switches = parse_args(args)
    if not switches:
        # Exiting early. (This must have been a --help or --version call, so there's nothing more to do.)
        sys.exit(0)
    return switches

def load_configuration(configfile) -> Configuration:
    config = Configuration()
    if configfile:
        try:
            config.setFromINIFile(pathlib.Path(configfile))
            config.runtimeValidation()
        except {{ cookiecutter.tool_name_camel_case }}ConfigError as e:
            LOG.exception(e)
    return config

def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """

    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(1, parent_dir)
    import {{ cookiecutter.tool_name_slug }}

    exitcode = 0
    SWITCHES = load_switches(args)

    logfilename = ("" if SWITCHES.nologfile else SWITCHES.logfile)
    setup_logging(name="{{ cookiecutter.tool_name_slug }}", loglevel = SWITCHES.loglevel, logfilename = logfilename, nocolor= SWITCHES.nocolor)
    LOG = logging.getLogger("{{ cookiecutter.tool_name_slug }}")
    LOG.diagnostic(f"SWITCHES.loglevel = {SWITCHES.loglevel}")

    CONFIG = load_configuration(SWITCHES.configfile)

    LOG.trace("Starting job...")

    if SWITCHES.devmode:
        LOG.info("Running in dev mode.")
        # TODO special setup for dev mode (e.g. suppressing actual web service calls, not actually sending any emails)

    if SWITCHES.infile:
        sys.stdin = open(SWITCHES.infile, "r")
        LOG.info(f"Input will be taken from {SWITCHES.infile}, rather than stdin.")

    if SWITCHES.outfile:
        sys.stdout = open(SWITCHES.outfile, "w")
        LOG.info(f"Output will be written to {SWITCHES.outfile}, rather than stdout.")

    try:
        with JnlParserFilter() as f:
            f.run()                                                           # TODO <-- here's the beef
    except Exception as e:
        LOG.exception(e)

        exitcode = 1
        if hasattr(e, "exitcode"):
            if e.exitcode > 0:
                exitcode = e.exitcode
            else:
                LOG.error("The warning exception above should have been caught and handled. Instead, it's causing this app to abort.")

    LOG.trace("Script ending.")
    LOG.diagnostic(f"Exit code = {exitcode}")
    sys.exit(exitcode)



def run():
    """Entry point for console_scripts"""
    # Throw away argv[0] which is this program's name ({{ cookiecutter.tool_name_slug }})
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
