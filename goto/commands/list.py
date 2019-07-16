def list(magic, command, args):
    """
    List commands
    """
    verbose = '-v' in args or '--verbose' in args
    magic.list_shortcuts(verbose=verbose)

    return None, None
