# coding: utf-8
from __future__ import unicode_literals


def list(magic, args):
    """
    List commands
    """
    verbose = '-v' in args or '--verbose' in args
    magic.list_shortcuts(verbose=verbose)

    return None, None
