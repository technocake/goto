# coding: utf-8
from __future__ import unicode_literals
from ..gotomagic.text import GotoError, GotoWarning

def help():
    return "{0:10}{1:30}{2}".format('rm', '<magicword>', 'Remove shortcut')


def names():
    return ['rm','--rm', 'remove','--remove']


def run(magic, command, args, options):
    """
    Remove magicword
    """

    if (len(args) == 0):
        return None, GotoWarning("missing_magicword", command='rm')

    word = args[0]

    err = magic.remove_shortcut(word)
    if err:
        return None, err

    # TODO: move save inside magic.
    err = magic.save()
    if err:
        return None, err
    return 'Removed magic word %s' % word, None
