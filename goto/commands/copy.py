import pyperclip
from ..gotomagic.text import Error


def copy(magic, args):
    """
    Copy uri to clipboard
    """

    if (len(args) == 0):
        return None, Error("missing_magicword")

    word = args[0]
    url = str(magic.get_uri(word))

    pyperclip.copy(url)

    return None, None
