EX_OK = 0
# EX_WARNING = 1 # Execution completed, but there were warning(s) reported
EX_ERROR = 2 # Execution failed (with an unspecified reason)
# EX_USAGE = 64 # The command was used incorrectly (bad arguments, bad flag, etc.)
# EX_DATAERR = 65 # Bad input data
# EX_NOINPUT = 66 # Input file doesn't exist/unreadable.
# EX_NOUSER = 67
# EX_NOHOST = 68
# EX_UNAVAILABLE = 69 # A service is unavailable.
EX_SOFTWARE = 70 # An internal software error has been detected.
# EX_OSERR = 71 # An operating system error has been detected.
# EX_OSFILE = 72 # Some system file does not exist/unreadable/has syntax error.
# EX_CANTCREAT = 73 # A (user specified) output file cannot be created.
# EX_IOERR = 74 # An error occurred while doing I/O on some file.
# EX_TEMPFAIL = 75 # Temporary failure, indicating something that is not really an error.
# EX_PROTOCOL = 76 # The remote system returned something that was not possible during a protocol exchange.
# EX_NOPERM = 77 # Insufficient permission.
EX_CONFIG = 78 # Something was found in an unconfigured or miscon­figured state.


CONFIG_OPTION_ERROR = "Error: The configuration setting of '{0} = {1}' is invalid."
POSSIBLE_VALUES_ARE = " Possible values are: {0}"

class {{ cookiecutter.tool_name_camel_case }}Error(Exception):
    """
    Generic error.

    Attributes:
        message -- explanation of the error
    """
    exitcode = EX_ERROR

    def __init__(self, message):
        self.message = message


class {{ cookiecutter.tool_name_camel_case }}ValueError(ValueError):
    exitcode = EX_ERROR


class {{ cookiecutter.tool_name_camel_case }}TypeError(TypeError):
    exitcode = EX_SOFTWARE

class {{ cookiecutter.tool_name_camel_case }}ConfigError({{ cookiecutter.tool_name_camel_case }}ConfigError):
    """
    Exception raised because of bad data in a config file or something wrong with our operating environment.

    Attributes:
        message -- explanation of the error(s)
    
    Alternate Attributes:
        key -- the name of the setting
        attempted_value -- the value that is in error
        possible_values -- (optional) a list of valid choices
    """
    exitcode = EX_CONFIG

    def __init__(self, message):
        self.message = message

    @overload
    def __init__(self, key, attempted_value, possible_values=None):
        self.message = CONFIG_OPTION_ERROR.format(key, attempted_value)
        if possible_values:
            self.message += POSSIBLE_VALUES_ARE.format(possible_values)


__all__ = ("{{ cookiecutter.tool_name_camel_case }}Error", 
	"{{ cookiecutter.tool_name_camel_case }}ValueError", 
	"{{ cookiecutter.tool_name_camel_case }}TypeError",
	"{{ cookiecutter.tool_name_camel_case }}ConfigError")
