# -*- coding: utf-8 -*-

import os, sys
import logging
import logging.handlers

from colorlog import ColoredFormatter

TRACE = 2000
DIAGNOSTIC = 1500

# Currently, we are not doing anything multi-threaded, so the verbose format doesn't need thread info at this time
# VERBOSE_FORMAT = logging.Formatter("%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s")
VERBOSE_FORMAT = logging.Formatter("%(asctime)s [%(module)s] %(levelname)s %(message)s")
SIMPLE_FORMAT = logging.Formatter("%(levelname)s %(message)s")
SIMPLE_COLORED = ColoredFormatter("[ %(log_color)s*%(reset)s ] %(blue)s%(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'TRACE': 'gray',
            'DEBUG': 'cyan',
            'DIAGNOSTIC': 'magenta',
            'INFO': 'white',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white'
        },
        secondary_log_colors={},
        style='%'
    )

def setup_logging(name="{{ cookiecutter.tool_name_slug }}", loglevel=logging.INFO, logfilename="{{ cookiecutter.tool_name_slug }}.log", nocolor=False):
    """
    Setup initial logging configuration
    """

    assert isinstance(name, str)

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

    log_file = logging.FileHandler(filename=os.path.join(os.getcwd(), logfilename))
    log_file.setFormatter(VERBOSE_FORMAT)
    logger.addHandler(log_file)

def equivalent_log_level(verbosity: int) -> int:
    verbosity *= 10

    if verbosity > logging.CRITICAL:
        verbosity = logging.CRITICAL

    if verbosity < logging.DEBUG:
        verbosity = logging.DEBUG

    return (logging.CRITICAL - verbosity) + 10



__all__ = ("setup_logging", "setup_file_logger", "equivalent_log_level", "DIAGNOSTIC", "TRACE")
