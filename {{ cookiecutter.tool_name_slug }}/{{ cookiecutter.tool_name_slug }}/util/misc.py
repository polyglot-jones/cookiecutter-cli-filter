"""
This file contains utils and reusable functions
"""

import logging

from collections import namedtuple
from contextlib import contextmanager

LOG = logging.getLogger('{{ cookiecutter.tool_name_slug }}')


def dict_to_obj(data):
    """
    Transform an input dict into a object.

    >>> data = dict(hello="world", bye="see you")
    >>> obj = dict_to_obj(data)
    >>> obj.hello
    'world'

    :param data: input dictionary data
    :type data: dict
    """
    assert isinstance(data, dict)

    if not data:
        return namedtuple("OBJ", [])

    obj = namedtuple("OBJ", list(data.keys()))

    return obj(**data)



@contextmanager
def run_in_console(debug=False):
    try:
        yield
    except Exception as e:
        LOG.critical(" !! {}".format(e))

        if debug:
            LOG.critical(e, exc_info=True)
    finally:
        LOG.debug("Shutdown...")


__all__ = ("dict_to_obj", "run_in_console")
