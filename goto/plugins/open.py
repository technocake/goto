# coding: utf-8
from __future__ import unicode_literals

import os
import subprocess
from ..gotomagic.utils import detect_platform
from ..gotomagic.text import GotoError, GotoWarning


def help():
    return "{0:10}{1:30}{2}".format('open', '<magicword>', 'Open magicword in window')


def names():
    return ['open', '--open']


def run(magic, command, args, options):
    """
    Open folder
    """
    command = command if command else ''
    verbose = '-v' in options or '--verbose' in options

    if (len(args) == 0):
        return None, GotoWarning("missing_magicword", command)

    magicword = args[0]
    uri = magic.get_uri(magicword)

    if uri is None:
        return None, GotoWarning("magicword_does_not_exist", magicword=magicword)

    uri = os.path.expanduser(uri)
    platform = detect_platform()

    try:
        if platform == 'linux':
            subprocess.call('xdg-open "%s"' % uri, shell=True)
        elif platform == 'osx':
            subprocess.call('open "%s"' % uri, shell=True)
        elif platform == 'win':
            subprocess.call('start "%s"' % uri, shell=True)

    except subprocess.CalledProcessError as e:
        return None, GotoError("open_failed", message=e.message)

    return uri if verbose else None, None
