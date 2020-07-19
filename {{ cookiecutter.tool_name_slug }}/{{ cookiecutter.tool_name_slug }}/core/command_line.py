# -*- coding: utf-8 -*-
import argparse, sys, logging
from {{ cookiecutter.tool_name }} import __version__

Log = logging.getLogger("{{ cookiecutter.tool_name }}")


def parse_args(args):
    """Parse any command line parameters.

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--version",action="version",version="{{ cookiecutter.tool_name }} {ver}".format(ver=__version__))
    parser.add_argument("-v","--verbose",dest="loglevel",help="set loglevel to INFO",action="store_const",const=logging.INFO)
    parser.add_argument("-vv","--very-verbose",dest="loglevel",help="set loglevel to DEBUG",action="store_const",const=logging.DEBUG)
	parser.add_argument("--devel", dest="devmode",help="turn on developer mode",action="store_const",const="dev")

    return parser.parse_args(args)


