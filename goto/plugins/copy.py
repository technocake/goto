# coding: utf-8
from __future__ import unicode_literals
import pyperclip
from ..gotomagic.text import GotoError, GotoWarning


def help():
    return "{0:10}{1:30}{2}".format('copy', '<magicword>', 'Copy magicword to the clipboard')


def names():
    return ['copy','--copy']


def run(magic, command, args, options):
    """
    Copy uri to clipboard
    """

    if (len(args) == 0):
        return None, GotoWarning("missing_magicword", command='copy')

    word = args[0]
    uri = str(magic.get_uri(word))

    if uri:
        pyperclip.copy(uri)
        return "Copied uri to clipboard", None
    else:
        return None, GotoWarning("magicword_does_not_exist", magicword=word)
