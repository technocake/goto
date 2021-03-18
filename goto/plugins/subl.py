# coding: utf-8
from __future__ import unicode_literals

import subprocess
from ..gotomagic.text import GotoError, GotoWarning


def help():
    return "{0:40}{1}".format('subl',  'Opens Sublime Text in code folder')  # noqa


def names():
    return ['subl', 'sublime', '--subl', '--sublime']


def run(magic, command, args, options):
    """
    Launch Sublime Text in the code folder
    """
    magicword = 'code' if len(args) == 0 else args[0]

    uri = magic.get_uri(magicword)

    if not uri:
        return None, GotoWarning("magicword_does_not_exist", magicword=magicword)

    try:
        subprocess.check_call('subl "%s"' % uri, shell=True)
    except subprocess.CalledProcessGotoError:
        return None, GotoError("subl_launch_failed")

    return None, None
