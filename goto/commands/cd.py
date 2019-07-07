import subprocess
import os
from ..gotomagic.text import GotoError, GotoWarning


def cd(magic, args):
    """
    Open a new terminal window and cd-s to the given path
    """

    if (len(args) == 0):
        return None, GotoWarning("missing_magicword", command='cd')

    word = args[0]
    url = magic.get_uri(word)
    url = os.path.expanduser(url)

    subprocess.call(
        """ osascript <<END
            tell app "Terminal" to do script "cd %s"
            END
        """ % url, shell=True)

    return None, None
