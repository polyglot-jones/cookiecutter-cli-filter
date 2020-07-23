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

    exitcode = 0
    SWITCHES = parse_args(args)
    if not SWITCHES:
        # Exiting early. (This must have been a --help or --version call, so there's nothing more to do.)
        sys.exit(exitcode)


    setup_logging(name="{{ cookiecutter.tool_name_slug }}", loglevel = SWITCHES.loglevel, logfile = SWITCHES.logfile, nocolor= SWITCHES.nocolor)

    LOG.diagnostic(f"SWITCHES.loglevel = {SWITCHES.loglevel}")
    LOG.trace("Starting job...")

    if SWITCHES.devmode:
        LOG.info("Running in dev mode.")
        # TODO special setup for dev mode (e.g. suppressing actual web service calls)


    try:
        filter_one_go()         # TODO <-- here's the beef
    except Exception as e:
        if hasattr(e, "loglevel"):
            LOG.log(e.loglevel,e)
        else:
            LOG.critical(e)

        exitcode = 1    
        if hasattr(e, "exitcode"):
            if e.exitcode > 0:
                exitcode = e.exitcode
            else:
                LOG.error("The warning exception above should have been caught and handled. Instead, it's causing this app to abort.")
    
    LOG.trace("Script ending.")
    LOG.diagnostic(f"Exit code = {exitcode}")
    sys.exit(exitcode)



def run():
    """Entry point for console_scripts"""

    # Throw away argv[0] which is this program's name ({{ cookiecutter.tool_name_slug }})
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
