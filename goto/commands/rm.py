# coding: utf-8
from __future__ import unicode_literals
from ..gotomagic.text import GotoError, GotoWarning


def rm(magic, command, args, options):
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
