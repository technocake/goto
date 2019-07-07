import pyperclip
from ..gotomagic.text import GotoError


def copy(magic, args):
    """
    Copy uri to clipboard
    """

    if (len(args) == 0):
        return None, GotoError("missing_magicword")

    word = args[0]
    url = str(magic.get_uri(word))

    pyperclip.copy(url)

    return None, None
