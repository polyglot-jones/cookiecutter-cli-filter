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


    def run(self):
        try:
            self.actual_filter_code()
            # self.actual_filter_code_take_2()

            LOG.info(f"Number of lines processed = {self.linecount}")
            LOG.info(f"Of those, number of lines skipped = {self.skipcount}")
        except {{ cookiecutter.tool_name_camel_case }}Error as e:
            LOG.error(f"Uncaught {{ cookiecutter.tool_name_camel_case }}Error detected. There is no good reason why we didn't handle it before {{ cookiecutter.tool_name_camel_case }}Filter finished running.")
            raise e


    def actual_filter_code(self):
        """
        Method #1: Process the stream (efficiently) line-by-line
        """
        for line in sys.stdin.readlines():
            line = line.strip()
            self.linecount += 1
            if line.startswith("#"):
                self.skipcount += 1
            else:
                # TODO Process line here
                pass
            sys.stdout.write(line)


    def actual_filter_code_take_2(self):
        """
        Method #2: Load the whole contents of the stream into memory (e.g. if a look-ahead is required)
        """
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


    def close(self):
        # do something else here, if needed
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
