import webbrowser
from ..gotomagic.utils import is_file
from ..gotomagic.text import Error
from .open import open


def default(magic, magicword):
    """
    Default behaviour when no commands are found in the first argument
    """

    url = magic.get_uri(magicword)
    if url is None:
        return None, Error('magicword_not_found')

    if is_file(url):
        return open(magic, [magicword])
    else:
        webbrowser.open(magic[magicword])

    return None, None
