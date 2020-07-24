# -*- coding: utf-8 -*-

import os, sys
import logging
import logging.handlers

from functools import lru_cache
from colorlog import ColoredFormatter

CRITICAL = logging.CRITICAL
ERROR = logging.ERROR
WARNING = logging.WARNING
INFO = logging.INFO
DIAGNOSTIC = INFO+1
DEBUG = logging.DEBUG
TRACE = DEBUG+1

# Currently, we are not doing anything multi-threaded, so the verbose format doesn't need thread info at this time
# VERBOSE_FORMAT = logging.Formatter("%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s")
VERBOSE_FORMAT = logging.Formatter("%(asctime)s [%(module)s] %(levelname)s %(message)s")
SIMPLE_FORMAT = logging.Formatter("%(levelname)s %(message)s")

# Color choices are: black, red, green, yellow, blue, purple, cyan, white
# Prefix choices are: bold_, thin_, bg_, bg_bold_
SIMPLE_COLORED = ColoredFormatter("[ %(log_color)s*%(reset)s ] %(blue)s%(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'TRACE': 'gray',
            'DEBUG': 'cyan',
            'DIAGNOSTIC': 'purple',
            'INFO': 'white',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white'
        },
        secondary_log_colors={},
        style='%'
    )


def logging_stub() -> logging.Logger:
    return logging.getLogger("stub")


@lru_cache(maxsize=32)
def setup_logging(name="{{ cookiecutter.tool_name_slug }}", loglevel=logging.INFO, logfilename="{{ cookiecutter.tool_name_slug }}.log", nocolor=False):
    """
    Setup initial logging configuration
    """

    if not sys.stderr.isatty:
        nocolor = True

    logging.addLevelName(DIAGNOSTIC, "DIAGNOSTIC")
    logging.addLevelName(TRACE, "TRACE")

    def diagnostic(self, message, *args, **kws):  # pragma no cover
        # Note: logger takes its '*args' as 'args'.
        """
        Halfway between INFO and DEBUG, this is a technical log entry (i.e. intended for the developer, not the user).
        Think of it as a special DEBUG entry that should be highlighted.
        """
        if self.isEnabledFor(DIAGNOSTIC):
            self._log(DIAGNOSTIC, message, args, **kws)

    def trace(self, message, *args, **kws):  # pragma no cover
        # Note: logger takes its '*args' as 'args'.
        """
        Even more verbose than DEBUG, trace logs might be scattered throughout the code, especially at entry and exit points.
        ("Killroy was here.")
        """
        if self.isEnabledFor(TRACE):
            self._log(TRACE, message, args, **kws)

    logging.Logger.diagnostic = diagnostic
    logging.Logger.raw_diagnostic = diagnostic
    logging.Logger.trace = trace
    logging.Logger.raw_trace = trace

    logger = logging.getLogger(name)
    # This should always be set to the chattiest level (individual handlers can be set to be less chatty)
    logger.setLevel(TRACE)
    logger.propagate = False

    # Note: stderr is a misnomer. It should be called stdinfo.
    # Only The filtered stdin data should be passed on to stdout.
    # All other information must go to stderr.
    log_console = logging.StreamHandler(stream=sys.stderr)
    if nocolor:
        log_console.setFormatter(SIMPLE_FORMAT)
    else:
        log_console.setFormatter(SIMPLE_COLORED)
    # We don't normally need DEBUG and TRACE messages cluttering up the console.
    if loglevel < logging.INFO:
        loglevel = logging.INFO
    log_console.setLevel(loglevel)
    logger.addHandler(log_console)

    if logfilename:
        log_file = logging.FileHandler(filename=os.path.join(os.getcwd(), logfilename))
        log_file.setFormatter(VERBOSE_FORMAT)
        logger.addHandler(log_file)

def loglevel_for_exception(e: Exception, otherwise=logging.ERROR):
    if hasattr(e, "loglevel"):
        return e.loglevel
    return otherwise

def equivalent_log_level(verbosity: int) -> int:
    verbosity *= 10

    if verbosity > logging.CRITICAL:
        verbosity = logging.CRITICAL

    if verbosity < logging.DEBUG:
        verbosity = logging.DEBUG

    return (logging.CRITICAL - verbosity) + 10



__all__ = ("logging_stub",
    "setup_logging",
    "loglevel_for_exception",
    "equivalent_log_level",
    "CRITICAL", "ERROR", "WARNING", "INFO", "DIAGNOSTIC", "DEBUG", "TRACE")
