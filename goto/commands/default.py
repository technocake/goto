import webbrowser
from ..gotomagic.utils import is_file
from ..gotomagic.text import GotoWarning
from .open import open


def default(magic, magicword):
    """
    Default behaviour when no commands are found in the first argument
    """

    url = magic.get_uri(magicword)
    # for this time beeing, the get_uri is exiting and printing warning itself
    #  TODO:  it would be better to have that kind of logic up in here.

    if is_file(url):
        return open(magic, [magicword])
    else:
        webbrowser.open(magic[magicword])

    return None, None
