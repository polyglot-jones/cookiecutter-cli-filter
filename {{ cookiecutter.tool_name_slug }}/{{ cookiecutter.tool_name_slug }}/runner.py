import argparse
from {{ cookiecutter.tool_name_slug }}.command_line import load_command_line
from {{ cookiecutter.tool_name_slug }}.config import load_config

from PyQt5.QtWidgets import QApplication
import sys
import logging
from pathlib import Path
from typing import Optional
from gwpycore import (
    ICON_ERROR,
    ICON_INFO,
    ICON_WARN,
    ask_user_to_confirm,
    inform_user_about_issue,
    normalizeName,
    setup_logging,
)
from sys import stdin, stdout, stderr
from .core.exceptions import *
from .core.{{ cookiecutter.tool_name_slug }}_filter import {{ cookiecutter.tool_name_camel_case }}Filter
from {{ cookiecutter.tool_name_slug }}.gui.main import {{ cookiecutter.tool_name_slug }}Window
import argparse

__version__ = "{{ cookiecutter.project_version }}"

# In case we try to post a logging message before logging is actually set up
LOG = logging.getLogger("stub")

SWITCHES: argparse.Namespace
CONFIG: argparse.Namespace


def further_initialization():
    LOG.trace("Performing further initialization")
    if SWITCHES.devmode:
        LOG.info("Running in dev mode.")
        # TODO special setup for dev mode (e.g. suppressing actual web service calls, not actually sending any emails)

    if SWITCHES.infile:
        sys.stdin = SWITCHES.infile.open("r")
        LOG.info(f"Input will be taken from {SWITCHES.infile}, rather than stdin.")

    if SWITCHES.outfile:
        sys.stdout = SWITCHES.outfile.open("w")
        LOG.info(f"Output will be written to {SWITCHES.outfile}, rather than stdout.")


def finish(exitcode=0, exception: Optional[Exception] = None):
    LOG.trace("Finishing")
    if exception:
        exitcode = 1
        if hasattr(exception, "exitcode"):
            exitcode = exception.exitcode
        LOG.uncaught(exception)
    LOG.diagnostic(f"Exit code = {exitcode}")


def run_gui():
    LOG.trace("Starting up the GUI")
    q_app = QApplication(sys.argv)
    GUI = {{ cookiecutter.tool_name_slug }}Window(q_app, SWITCHES, CONFIG)
    GUI.show()
    x = q_app.exec_()
    finish(exitcode=x)


def run_headless(command: str):
    with {{ cookiecutter.tool_name_camel_case }}Filter() as filter_group:
        if SWITCHES.command == "filter-one":
            x = filter_group.command_one()
        elif SWITCHES.command == "filter-two":
            x = filter_group.command_two()
        else:
            raise {{ cookiecutter.tool_name_camel_case }}Error(f"Unexpected sub-command: '{SWITCHES.command}'.")
    finish(exitcode=x)


def main():
    global SWITCHES, CONFIG, LOG
    SWITCHES = load_command_line(__version__, sys.argv[1:])
    LOG = setup_logging(loglevel=SWITCHES.loglevel, logfile=SWITCHES.logfile, nocolor=SWITCHES.nocolor)
    LOG.trace("(Previously) Loaded command line and set up logging.")

    try:
        CONFIG = load_config(SWITCHES)
        CONFIG.version = __version__
        further_initialization()

        if SWITCHES.command == "gui":
            run_gui()
        else:
            run_headless()
    except Exception as e:
        finish(exception=e)


if __name__ == "__main__":
    main()
