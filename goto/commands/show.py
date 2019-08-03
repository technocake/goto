# coding: utf-8
from __future__ import unicode_literals
from ..gotomagic.text import GotoError, GotoWarning


def show(magic, command, args, options):
    """
    Show magicword.
    """

    if (len(args) == 0):
        return None, GotoWarning("missing_magicword", command='show')

    uris = ''
    for arg in args:
        uri = magic.get_uri(arg)

        if uri:
            uris += uri + '\n';
        else:
            return None, GotoWarning("magicword_does_not_exist", magicword=arg)

    return uris, None
