def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    import os, sys
    import .core.command_line

    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(1, parent_dir)
    import {{ cookiecutter.tool_name_slug }}

    __package__ = str("{{ cookiecutter.tool_name_slug }}")

    SWITCHES = core.command_line.parse_args(args)
    setup_logging(args.loglevel)
    LOG.trace("Starting job...")
    LOG.debug("SWITCHES.loglevel = {}".format(SWITCHES.loglevel))
    if (SWITCHES.devmode):
        LOG.info("Running in dev mode.")
    stdout << main_filter << stdin
    LOG.trace("Script ending.")


def run():
    """Entry point for console_scripts"""

    # Throw away argv[0] which is this program's name
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
