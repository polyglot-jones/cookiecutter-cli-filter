# -*- coding: utf-8 -*-

import os, sys
import logging
import logging.handlers

from colorlog import ColoredFormatter

CONSOLE_LEVEL = 1000
TRACE_LEVEL = 2000

# Currently, we are not doing anything multi-threaded, so the verbose format doesn't need thread info at this time
# VERBOSE_FORMAT = logging.Formatter("%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s")
VERBOSE_FORMAT = logging.Formatter("%(asctime)s [%(module)s] %(levelname)s %(message)s")
SIMPLE_FORMAT = logging.Formatter("%(levelname)s %(message)s")
SIMPLE_COLORED = ColoredFormatter("[ %(log_color)s*%(reset)s ] %(blue)s%(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'TRACE_LEVEL': 'gray',
            'DEBUG': 'cyan',
            'INFO': 'white',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
            'CONSOLE_LEVEL': 'green'
        },
        secondary_log_colors={},
        style='%'
    )

def setup_logging(name):
    """
    Setup initial logging configuration
    """

    assert isinstance(name, str)

    # Add console level
    logging.addLevelName(CONSOLE_LEVEL, "CONSOLE_LEVEL")
    logging.addLevelName(TRACE_LEVEL, "TRACE_LEVEL")

    def console(self, message, *args, **kws):  # pragma no cover
        # Note: logger takes its '*args' as 'args'.
        """
        Like INFO, but specifically directed to the console.
        """
        if self.isEnabledFor(CONSOLE_LEVEL):
            self._log(CONSOLE_LEVEL, message, args, **kws)

    def trace(self, message, *args, **kws):  # pragma no cover
        # Note: logger takes its '*args' as 'args'.
        """
        Even more verbose than DEBUG, trace logs might be scattered throughout the code, especially at entry and exit points.
        ("Killroy was here.")
        """
        if self.isEnabledFor(TRACE_LEVEL):
            self._log(TRACE_LEVEL, message, args, **kws)

    logging.Logger.console = console
    logging.Logger.raw_console = console
    logging.Logger.trace = trace
    logging.Logger.raw_trace = trace

    logger = logging.getLogger(name)
    # This should always be set to the chattiest level (individual handlers can be set to be less chatty)
    logger.setLevel(TRACE_LEVEL)
    logger.propagate = False

    # Note: stderr is a misnomer. It should be called stdinfo. Only The filtered stdin data should be passed on to stdout. All other information must go to stderr.
    log_console = logging.StreamHandler(stream=sys.stderr)
    log_console.setFormatter(SIMPLE_COLORED)
    # We don't normally need DEBUG and TRACE messages cluttering up the console.
    log_console.setLevel(logging.INFO)
    logger.addHandler(log_console)

    log_file = logging.FileHandler(filename=os.path.join(os.getcwd(), "{{ cookiecutter.tool_name }}.log"))
    log_file.setFormatter(VERBOSE_FORMAT)
    logger.addHandler(log_file)

def equivalent_log_level(verbosity: int) -> int:
    verbosity *= 10

    if verbosity > logging.CRITICAL:
        verbosity = logging.CRITICAL

    if verbosity < logging.DEBUG:
        verbosity = logging.DEBUG

    return (logging.CRITICAL - verbosity) + 10



__all__ = ("setup_logging", "setup_file_logger", "equivalent_log_level", "CONSOLE_LEVEL", "TRACE_LEVEL")
