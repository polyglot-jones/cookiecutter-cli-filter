from contextlib import AbstractContextManager
from {{ cookiecutter.tool_name_slug }}.core.exceptions import {{ cookiecutter.tool_name_camel_case }}Error
import logging

LOG = logging.getLogger("{{ cookiecutter.tool_name_slug }}")

class {{ cookiecutter.tool_name_camel_case }}Filter(AbstractContextManager):
    """
    This is the heart of the {{ cookiecutter.tool_name }}.

    (This being a context manager, means we can invoke it via a "with ... as" statement.)
    """
    instream = None
    outstream = None

    def __init__(self, instream, outstream):
        self.instream = instream
        self.outstream = outstream

    def run(self):
        try:
            linecount = 0
            skipcount = 0
            for line in self.instream.readlines():
                linecount += 1
                if line == "":
                    skipcount += 1
                else:
                    # do something for real here
                    pass

                self.outstream.writeline(line)
            LOG.info(f"Number of lines processed = {linecount}")
            LOG.info(f"Of those, number of lines skipped = {skipcount}")
        except {{ cookiecutter.tool_name_camel_case }}Error as e:
            LOG.error(f"Uncaught {{ cookiecutter.tool_name_camel_case }}Error detected. There is no good reason why we didn't handle it before {{ cookiecutter.tool_name_camel_case }}Filter finished running.")
            raise e

    def close(self):
    	outstream.close()
        # do something else here, if needed

    def __exit__(self, exception_type, exception, trace_back):
        """
        This method is always called when the "with ... as" statement exits.
        """
        we_handled_the_exception_here = False
        if exception:
        	# maybe handle the exception here
            # we_handled_the_exception_here = True
            pass

        self.close()

        return we_handled_the_exception_here
