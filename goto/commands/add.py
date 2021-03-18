# coding: utf-8
from __future__ import unicode_literals
from ..gotomagic.text import GotoError, GotoWarning


def help():
    return "{0:10}{1:30}{2}".format('add','<magicword> <url or path>','Add shortcut')

def names():
    return ['add','--add']


def run(magic, command, args, options):
    """
    Add magicword
    """

    if (len(args) == 0):
        return None, GotoWarning("missing_magicword_and_uri", command='add')

    if (len(args) == 1):
        return None, GotoWarning("missing_uri",
                                 magicword=args[0],
                                 command='add')

    magicword = args[0]
    uri = args[1]

    err = magic.add_shortcut(magicword, uri)
    if err:
        return None, err

    err = magic.save()
    if err:
        return None, err

    return 'Added magic word {}'.format(magicword), None
