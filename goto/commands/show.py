from ..gotomagic.text import GotoError, GotoWarning


def show(magic, args):
    """
    Show magicword.
    """

    if (len(args) == 0):
        return None, GotoWarning("show_missing_magicword")

    word = args[0]
    magic.show_shortcut(word)

    return None, None
