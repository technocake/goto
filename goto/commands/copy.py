import pyperclip
from ..gotomagic.text import GotoError, GotoWarning


def copy(magic, args):
    """
    Copy uri to clipboard
    """

    if (len(args) == 0):
        return None, GotoWarning("missing_magicword", command='cd')

    word = args[0]
    url = str(magic.get_uri(word))

    pyperclip.copy(url)

    return None, None
