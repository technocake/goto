import webbrowser
from ..gotomagic.utils import is_file
from ..gotomagic.text import GotoError
from .open import open


def default(magic, magicwords):
    """
    Default behaviour when no commands are found in the first argument
    """
    output = ""
    for magicword in magicwords:
        url = magic.get_uri(magicword)
        if url is None:
            return None, GotoWarning('magicword_does_not_exist', magicword=magicword)

        if is_file(url):
            _output, err = open(magic, [magicword])
            if err:
                return None, err
            output += "%s\n" % _output
        else:
            try:
                webbrowser.open_new_tab(url)
                output += "Opened new browser tab: %s\n" % url
            except webbrowser.Error:
                return None, GotoError('open_browser_tab_error')

    return output, None
