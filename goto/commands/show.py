from ..gotomagic.text import Error


def show(magic, args):
    """
    Show magicword.
    """

    if (len(args) == 0):
        return None, Error("show_missing_magicword")

    word = args[0]
    magic.show_shortcut(word)

    return None, None
