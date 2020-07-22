# The existence of this file makes this subfolder a "package"
"""
This package contains general-purpose code that is not necessarily specific to this application.
Don't be surprised if we move some/all of this code to an external library at some point.

IMPORTANT: The code in this package must not be dependent on any code in the other packages.
Dependencies should only go one-way.
"""
from .logger import *

setup_logging("{{ cookiecutter.tool_name_slug }}")
