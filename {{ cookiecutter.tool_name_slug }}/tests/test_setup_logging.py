from {{ cookiecutter.tool_name_slug }}.core.exceptions import {{ cookiecutter.tool_name_camel_case }}Error
import pytest, logging, sys, time
from {{ cookiecutter.tool_name_slug }}.util.logger import setup_logging

# Notes:
# 1. The capsys fixture captures sys.stdout and sys.stderr for us
# 2. It's important that every test uses a different logger name (e.g. with_file vs. console_only); otherwise, you'll get errors trying to write to a closed file between one test to another.


def test_logging_stub(capsys):
    log = logging_stub()
    assert log.name == "stub"
    assert len(log.handlers) == 0
    sys.stderr.write("==START==\n")
    log.error("this will go nowhere.")
    log.diagnostic("this will go nowhere.")
    log.trace("this will go nowhere.")
    sys.stderr.write("==END==")
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "==START==\n==END=="

def test_setup_logging_with_file():
    setup_logging.cache_clear()
    assert setup_logging("with_file") is None
    log = logging.getLogger("nosuch")
    assert len(log.handlers) == 0
    log = logging.getLogger("with_file")
    assert len(log.handlers) == 2

def test_setup_logging_console_only():
    setup_logging.cache_clear()
    assert setup_logging("console_only", logfilename="") is None
    log = logging.getLogger("nosuch")
    assert len(log.handlers) == 0
    log = logging.getLogger("console_only")
    assert len(log.handlers) == 1


def test_logging_error_method(capsys):
    setup_logging.cache_clear()
    sys.stderr.write("==START==\n")
    setup_logging("error_method", logfilename="", nocolor=True)
    log = logging.getLogger("error_method")
    log.error("error")
    sys.stderr.write("==END==")
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "==START==\nERROR error\n==END=="


def test_logging_debug_method_quiet(capsys):
    setup_logging.cache_clear()
    sys.stderr.write("==START==\n")
    setup_logging("debug_q", logfilename="", nocolor=True)
    log = logging.getLogger("debug_q")
    log.debug("debug")
    sys.stderr.write("==END==")
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "==START==\n==END=="


def test_logging_debug_method_verbose(capsys):
    setup_logging.cache_clear()
    sys.stderr.write("==START==\n")
    setup_logging("debug_v", loglevel=DEBUG, logfilename="", nocolor=True)
    log = logging.getLogger("debug_v")
    log.debug("debug")
    sys.stderr.write("==END==")
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "==START==\nDEBUG debug\n==END=="


def test_logging_diagnostic_method_quiet(capsys):
    setup_logging.cache_clear()
    sys.stderr.write("==START==\n")
    setup_logging("diagnostic_q", logfilename="", nocolor=True)
    log = logging.getLogger("diagnostic_q")
    log.diagnostic("diagnostic")
    sys.stderr.write("==END==")
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "==START==\n==END=="


def test_logging_diagnostic_method_verbose(capsys):
    setup_logging.cache_clear()
    sys.stderr.write("==START==\n")
    setup_logging("diagnostic_v", loglevel=DIAGNOSTIC, logfilename="", nocolor=True)
    log = logging.getLogger("diagnostic_v")
    log.diagnostic("diagnostic")
    sys.stderr.write("==END==")
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "==START==\nDIAGNOSTIC diagnostic\n==END=="


def test_logging_trace_method_quiet(capsys):
    setup_logging.cache_clear()
    sys.stderr.write("==START==\n")
    setup_logging("trace_q", logfilename="", nocolor=True)
    log = logging.getLogger("trace_q")
    log.trace("trace")
    sys.stderr.write("==END==")
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "==START==\n==END=="


def test_logging_trace_method_verbose(capsys):
    setup_logging.cache_clear()
    sys.stderr.write("==START==\n")
    setup_logging("trace_v", loglevel=TRACE, logfilename="", nocolor=True)
    log = logging.getLogger("trace_v")
    log.trace("trace")
    sys.stderr.write("==END==")
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "==START==\nTRACE trace\n==END=="


def test_logging_exception_method(capsys):
    setup_logging.cache_clear()
    sys.stderr.write("==START==\n")
    setup_logging("exception_method", logfilename="", nocolor=True)
    log = logging.getLogger("exception_method")
    log.exception(JnlParseError("exception", loglevel=CRITICAL))
    sys.stderr.write("==END==")
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "==START==\nCRITICAL exception\n==END=="


def test_level_constants():
    assert CRITICAL == 50
    assert ERROR == 40
    assert WARNING == 30
    assert INFO == 20
    assert DIAGNOSTIC == 15
    assert DEBUG == 10
    assert TRACE == 5
    assert logging.getLevelName(DIAGNOSTIC) == "DIAGNOSTIC"
    assert logging.getLevelName(TRACE) == "TRACE"

