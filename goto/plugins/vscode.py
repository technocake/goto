# coding: utf-8
from __future__ import unicode_literals

import subprocess
from ..gotomagic.text import GotoError, GotoWarning


def help():
    return "{0:40}{1}".format('vscode', 'Opens Visual Studio Code in code folder')


def names():
    return ['vscode', '--vscode']

def run(magic, command, args, options):
    """
    Launch Visual Studio Code in the code folder
    """
    magicword = 'code' if len(args) == 0 else args[0]

    uri = magic.get_uri(magicword)

    if uri is None:
        return None, GotoWarning("no_magicword_named_code")

    try:
        subprocess.check_call('code "%s"' % uri, shell=True)
    except subprocess.CalledProcessError:
        return None, GotoError("vscode_launch_failed")

    return None, None
