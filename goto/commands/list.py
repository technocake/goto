# coding: utf-8
from __future__ import unicode_literals

def list(magic, command, args, options):
    """
    List commands
    """
    verbose = '-v' in options or '--verbose' in options
    magic.list_shortcuts(verbose=verbose)

    return None, None
