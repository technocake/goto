from __future__ import unicode_literals

import subprocess
from ..gotomagic.utils import detect_platform
from ..gotomagic.text import GotoError, GotoWarning


def help():
    return "{0:40}{1}".format('idea', 'Opens Rider in code folder')


def names():
    return ['rider', '--rider',]


def run(magic, command, args, options):
    """
    Launch Rider. Open it in the code folder.
    """

    platform = detect_platform()

    if platform in ['osx', 'linux']:
        cmd = "rider"
    elif platform == 'win':
        cmd = "rider.exe"

    magicword = 'code' if len(args) == 0 else args[0]

    uri = magic.get_uri(magicword)
    if uri is None:
        return None, GotoWarning("magicword_does_not_exist", magicword=magicword)

    try:
        subprocess.check_call('%s "%s"' % (cmd, uri), shell=True)
    except subprocess.CalledProcessError:
        return None, GotoWarning("rider_launch_failed")

    return None, None
