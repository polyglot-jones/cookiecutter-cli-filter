import os, sys, logging

def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    from sys import stdin, stdout, stderr
    from .core.command_line import parse_args
    from .util.logger import setup_logging
    from .logic import filter_one

    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(1, parent_dir)
    import {{ cookiecutter.tool_name_slug }}

    __package__ = str("{{ cookiecutter.tool_name_slug }}")
    LOG = logging.getLogger(__package__.split('.', maxsplit=1)[0])


    SWITCHES = parse_args(args)
    setup_logging(SWITCHES.loglevel)
    LOG.trace("Starting job...")
    LOG.debug("SWITCHES.loglevel = {}".format(SWITCHES.loglevel))
    if (SWITCHES.devmode):
        LOG.info("Running in dev mode.")
    stdout << filter_one() << stdin
    LOG.trace("Script ending.")


def run():
    """Entry point for console_scripts"""

    # Throw away argv[0] which is this program's name
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
