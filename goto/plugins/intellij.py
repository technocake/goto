# coding: utf-8
from __future__ import unicode_literals

import subprocess
from ..gotomagic.utils import detect_platform
from ..gotomagic.text import GotoError, GotoWarning


def help():
    return "{0:40}{1}".format('idea', 'Opens IntelliJ in code folder')


def names():
    return ['intellij', '--intellij', 'idea', '--idea',]


def run(magic, command, args, options):
    """
    Launch IntelliJ. Open it in the code folder.
    """

    platform = detect_platform()

    if platform in ['osx', 'linux']:
        cmd = "idea"
    elif platform == 'win':
        cmd = "idea.exe"

    code = magic.get_uri('code')
    if code is None:
        return None, GotoWarning("no_magicword_named_code")

    try:
        subprocess.check_call('%s "%s"' % (cmd, code), shell=True)
    except subprocess.CalledProcessError:
        return None, GotoWarning("intellij_launch_failed")

    return None, None
