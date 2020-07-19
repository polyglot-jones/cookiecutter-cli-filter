# The existence of this file makes this subfolder a "package"
"""
This package contains general-purpose code that is not necessarily specific to this application.
Don't be surprised if we move some/all of this code to an external library at some point.
"""
from ..util.logger import *
from ..util.misc import *
from .exceptions import *

setup_logging("{{ cookiecutter.tool_name }}")
