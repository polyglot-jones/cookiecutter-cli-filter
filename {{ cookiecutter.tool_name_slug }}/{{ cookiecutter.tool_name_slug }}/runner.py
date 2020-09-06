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
from {{ cookiecutter.tool_name_slug }}.core.exceptions import {{ cookiecutter.tool_name_camel_case }}Error
from {{ cookiecutter.tool_name_slug }}.core.{{ cookiecutter.tool_name_slug }}_filter import {{ cookiecutter.tool_name_camel_case }}Filter
from {{ cookiecutter.tool_name_slug }}.gui.main import {{ cookiecutter.tool_name_slug }}Window
import argparse

__version__ = "{{ cookiecutter.project_version }}"

# In case we try to post a logging message before logging is actually set up
LOG = logging.getLogger("stub")

CONFIG: argparse.Namespace


def further_initialization():
    LOG.trace("Performing further initialization")
    if CONFIG.devmode:
        LOG.info("Running in dev mode.")
        # TODO special setup for dev mode (e.g. suppressing actual web service calls, not actually sending any emails)

    if CONFIG.infile:
        sys.stdin = CONFIG.infile.open("r")
        LOG.info(f"Input will be taken from {CONFIG.infile}, rather than stdin.")

    if CONFIG.outfile:
        sys.stdout = CONFIG.outfile.open("w")
        LOG.info(f"Output will be written to {CONFIG.outfile}, rather than stdout.")


def finish(exitcode=0, exception: Optional[Exception] = None):
    LOG.trace("Finishing")
    if exception:
        exitcode = 1
        if hasattr(exception, "exitcode"):
            exitcode = exception.exitcode
        LOG.uncaught(exception)
    LOG.diagnostic(f"Exit code = {exitcode}")


def run_gui() -> int:
    LOG.trace("Starting up the GUI")
    q_app = QApplication([])
    gui = {{ cookiecutter.tool_name_camel_case }}Window(q_app, CONFIG)
    gui.show()
    return q_app.exec_()


def main():
    global CONFIG, LOG
    switches = load_command_line(__version__, sys.argv[1:])
    LOG = setup_logging(loglevel=switches.loglevel, logfile=switches.logfile, nocolor=switches.nocolor)
    LOG.trace("(Previously) Loaded command line and set up logging.")

    try:
        CONFIG = load_config(switches.configfile, initial_config=switches)
        CONFIG.version = __version__
        further_initialization()

        if CONFIG.command == "gui":
            xcode = run_gui()
        else:
            with {{ cookiecutter.tool_name_camel_case }}Filter() as filter_group:
                xcode = filter_group.dispatch(CONFIG)
        finish(exitcode=xcode)
    except Exception as e:
        finish(exception=e)


if __name__ == "__main__":
    main()
