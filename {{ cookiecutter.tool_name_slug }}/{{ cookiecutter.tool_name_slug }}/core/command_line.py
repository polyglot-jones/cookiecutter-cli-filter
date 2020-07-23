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
    parser.add_argument("--devel", dest="devmode",help="turns on developer mode",action="store_true",default=False)
    parser.add_argument("--nocolor", dest="nocolor",help="turns off coloring the log messages that are sent to the console",action="store_true",default=False)
    parser.add_argument("--logfile", dest="logfile",help="specifies the name (and path) for the log file ({{ cookiecutter.tool_name_slug }}.log by default)",default="{{ cookiecutter.tool_name_slug }}.log")

    # Note: --version and --help are handled immediately as they are parsed.
    # In both cases, this return None
    return parser.parse_args(args)
