import os
import sys
import subprocess
from ..gotomagic.utils import detect_platform

def open(magic, args):
    """
    Open folder
    """

    if (len(args) == 0):
        return None, "show_missing_magicword"

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

    except subprocess.CalledProcessError:
        return None, "open_failed"

    return None, None
