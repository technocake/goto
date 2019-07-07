def list(magic, args):
    """
    List commands
    """

    magic.list_shortcuts(verbose=('-v' in args))

    return None, None
