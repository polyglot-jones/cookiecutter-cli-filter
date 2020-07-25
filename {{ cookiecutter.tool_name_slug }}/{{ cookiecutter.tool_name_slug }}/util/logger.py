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
DIAGNOSTIC = INFO - 5
DEBUG = logging.DEBUG
TRACE = DEBUG - 5

# TODO If this app does anything multi-threaded, then include thread info in VERBOSE_FORMAT
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


    def diagnostic(self, message, *args, **kws):  # pragma no cover
        # Note: logger takes its '*args' as 'args'.
        """
        Halfway between INFO and DEBUG, this is a technical log entry (i.e. intended for the developer, not the user).
        Think of it as a special DEBUG entry that should be highlighted.
        """
        if self.isEnabledFor(DIAGNOSTIC):
            self._log(DIAGNOSTIC, message, args, **kws)

    logging.addLevelName(DIAGNOSTIC, "DIAGNOSTIC")
    logging.Logger.diagnostic = diagnostic

    
    def trace(self, message, *args, **kws):  # pragma no cover
        # Note: logger takes its '*args' as 'args'.
        """
        Even more verbose than DEBUG, trace logs might be scattered throughout the code, especially at entry and exit points.
        ("Killroy was here.")
        """
        if self.isEnabledFor(TRACE):
            self._log(TRACE, message, args, **kws)

    logging.addLevelName(TRACE, "TRACE")
    logging.Logger.trace = trace


    def per_exception(self, e:Exception, *args, **kws):  # pragma no cover
        # Note: logger takes its '*args' as 'args'.
        """
        Logs the given exception at the appropriate level (ERROR unless there's a loglevel attribute on the exception itself to say otherwise).
        Note: logging.Logger already has an exception() method, but it's just a synonym for error().
        This replaces it with something a tad smarter.
        """
        level = ERROR
        if hasattr(e, "loglevel"):
            level = e.loglevel
        if self.isEnabledFor(level):
            self._log(level, e, args, **kws)

    logging.Logger.exception = per_exception


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
    log_console.setLevel(loglevel)
    logger.addHandler(log_console)

    if logfilename:
        log_file = logging.FileHandler(filename=os.path.join(os.getcwd(), logfilename))
        log_file.setFormatter(VERBOSE_FORMAT)
        logger.addHandler(log_file)


__all__ = ("logging_stub",
    "setup_logging",
    "CRITICAL", "ERROR", "WARNING", "INFO", "DIAGNOSTIC", "DEBUG", "TRACE")
