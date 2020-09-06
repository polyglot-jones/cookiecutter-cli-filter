from contextlib import AbstractContextManager
from {{ cookiecutter.tool_name_slug }}.core.exceptions import {{ cookiecutter.tool_name_camel_case }}Error
import sys, logging

LOG = logging.getLogger("{{ cookiecutter.tool_name_slug }}")

class {{ cookiecutter.tool_name_camel_case }}Filter(AbstractContextManager):
    """
    This is the heart of the {{ cookiecutter.tool_name }}.
    """
    # This being a context manager, means we can invoke it via a "with ... as" statement.
    linecount = 0
    skipcount = 0


    def __init__(self):
        pass


    def show_results(self):
        LOG.info(f"Number of lines processed = {self.linecount}")
        LOG.info(f"Of those, number of lines skipped = {self.skipcount}")


    def count_lines(self):
        """
        This does the actual work for the COUNT-LINES command.
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


    def just_revised(self):
        """
        This does the actual work for the LATEST command.
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


    def close(self):
        # do something here (release resources used, etc.), if needed.
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
