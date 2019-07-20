# coding: utf-8
from __future__ import unicode_literals

import subprocess
from ..gotomagic.text import GotoError, GotoWarning


def help():
    return "{0:10}{1}".format('subl',  'Opens Sublime Text in code folder')


def names():
    return ['subl', 'sublime', '--subl', '--sublime']


def run(magic, command, args, options):
    """
    Launch Sublime Text in the code folder
    """

    code = magic.get_uri('code')
    if code is None:
        return None, GotoWarning("no_magicword_named_code")

    try:
        subprocess.check_call('subl "%s"' % code, shell=True)
    except subprocess.CalledProcessGotoError:
        return None, GotoError("subl_launch_failed")

    return None, None
