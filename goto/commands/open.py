import os
import subprocess
from ..gotomagic.utils import detect_platform
from ..gotomagic.text import GotoError, GotoWarning


def open(magic, args):
    """
    Open folder
    """

    if (len(args) == 0):
        return None, GotoWarning("missing_magicword", command='open')

    magicword = args[0]
    url = magic.get_uri(magicword)
    url = os.path.expanduser(url)
    platform = detect_platform()

    try:
        if platform == 'linux':
            subprocess.call('xdg-open "%s"' % url, shell=True)
        elif platform == 'osx':
            subprocess.call('open "%s"' % url, shell=True)
        elif platform == 'win':
            subprocess.call('start "%s"' % url, shell=True)

    except subprocess.CalledProcessError as e:
        return None, GotoError("open_failed", message=e.message)

    return None, None
