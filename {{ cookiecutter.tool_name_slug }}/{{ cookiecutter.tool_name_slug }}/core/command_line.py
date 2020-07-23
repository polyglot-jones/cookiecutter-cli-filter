# -*- coding: utf-8 -*-
import argparse, sys
from {{ cookiecutter.tool_name_slug }} import __version__

# KEEP IN MIND: logging has not been set up yet. Don't try to make logging calls in here.

def parse_args(args):
    """Parse any command line parameters.

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      An object of type argparse.Namespace (access it like a dict)
    """
    ver=__version__
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--version",action="version",version=f"{{ cookiecutter.tool_name }} {ver}")
    parser.add_argument("-v","--verbose",dest="loglevel",help="sets loglevel to DIAGNOSTIC",action="store_const",const=logging.DIAGNOSTIC,default=logging.INFO)
    parser.add_argument("--debug",dest="loglevel",help="sets loglevel to DEBUG",action="store_const",const=logging.DEBUG)
    parser.add_argument("--trace",dest="loglevel",help="sets loglevel to TRACE",action="store_const",const=logging.TRACE)
    parser.add_argument("--nocolor", dest="nocolor",help="turns off coloring the log messages that are sent to the console",action="store_true",default=False)
    parser.add_argument("-l", "--logfile", dest="logfile",help="specifies the name (and path) for the log file ({{ cookiecutter.tool_name_slug }}.log by default)",default="{{ cookiecutter.tool_name_slug }}.log")
    parser.add_argument("--nologfile", dest="nologfile",help="suppresses using a log file, relying on just the console",action="store_true",default=False)
    
    # The following options are defined only in case you need them.
    # The initial code provided by this template does nothing with them (other than log that they were invoked).
    parser.add_argument("-d", "--devel", dest="devmode",help="turns on developer mode",action="store_true",default=False)
    parser.add_argument("-i", "--infile", dest="infile",help="specifies the name (and path) for the input (instead of stdin)",default="")
    parser.add_argument("-o", "--outfile", dest="outfile",help="specifies the name (and path) for the output (instead of stdout)",default="")

    # Note: --version and --help are handled immediately as they are parsed.
    # In both cases, parse_args will return None
    return parser.parse_args(args)
