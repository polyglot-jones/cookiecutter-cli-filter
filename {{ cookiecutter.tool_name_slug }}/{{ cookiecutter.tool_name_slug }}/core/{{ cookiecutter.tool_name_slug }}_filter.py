import argparse
from contextlib import AbstractContextManager
from {{ cookiecutter.tool_name_slug }}.core.exceptions import {{ cookiecutter.tool_name_camel_case }}Error
from gwpycore import EX_OK
import sys, logging

LOG = logging.getLogger("main")
CONFIG: argparse.Namespace

class {{ cookiecutter.tool_name_camel_case }}Filter(AbstractContextManager):
    """
    This is the heart of the {{ cookiecutter.tool_name }}.
    """
    # This being a context manager, means we can invoke it via a "with ... as" statement.
    linecount = 0
    skipcount = 0
    commands = ["gui", "count", "latest"]

    def __init__(self):
        pass


    def show_results(self):
        LOG.info(f"Number of lines processed = {self.linecount}")
        LOG.info(f"Of those, number of lines skipped = {self.skipcount}")

    def dispatch(self, config: argparse.Namespace) -> int:
        global CONFIG
        CONFIG = config
        if CONFIG.command not in self.commands:
            raise {{ cookiecutter.tool_name_camel_case }}Error(f"Unexpected sub-command: '{CONFIG.command}'.")
        return getattr(self, CONFIG.command)()


    def count(self) -> int:
        """
        This example just counts the lines in a file.
        """
        # Example of one method: Process the stream (efficiently) line-by-line
        for line in sys.stdin.readlines():
            line = line.strip()
            self.linecount += 1
            if line == "" or line.startswith("#"):
                self.skipcount += 1
            else:
                # TODO Process line here
                pass
            sys.stdout.write(line)
        self.show_results()
        return EX_OK
        
    def latest(self) -> int:
        """
        This example filters out old/revised text.
        """
        # Example of another method: Load the whole contents of the stream into memory (e.g. if a look-ahead is required)
        lines = sys.stdin.readlines()
        new_text = []
        for index, line in enumerate(lines):
            # Look ahead to see if the current line was superseded.
            if lines[index+1].startswith("Revised: "):
                self.skipcount += 1
                continue
            # TODO Process line here
            new_text.append(line)
        sys.stdout.writelines(new_text)
        self.show_results()
        return EX_OK

    def close(self):
        # TODO Maybe do something here (e.g. release resources used).
        pass


    def __exit__(self, exception_type, exception, trace_back):
        """
        This method is called when the "with ... as" statement exits.
        """
        handled_here = False
        if exception:
        	# TODO handle the exception here (or not)
            handled_here = True
        self.close()
        return handled_here

__all__ = ("{{ cookiecutter.tool_name_camel_case }}Filter",)