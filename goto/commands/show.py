# coding: utf-8
from __future__ import unicode_literals
from ..gotomagic.text import GotoError, GotoWarning

def help():
    return "{0:10}{1:30}{2}".format('show', '<magicword>', 'Show url of shortcut')


def names():
    return ['show','--show']


def run(magic, command, args, options):
    """
    Show magicword.
    """

    if (len(args) == 0):
        return None, GotoWarning("missing_magicword", command='show')

    magicword = args[0]
    uri = magic.get_uri(magicword)

    if uri:
        return uri, None
    else:
        return None, GotoWarning("magicword_does_not_exist", magicword=magicword)
