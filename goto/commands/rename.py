# coding: utf-8
from __future__ import unicode_literals
from ..gotomagic.text import GotoWarning


def help():
    return "{0:10}{1:30}{2}".format('rename', '<magicword> <new name>', 'Rename shortcut')


def names():
    return ['rename', '--rename']


def run(magic, command, args, options):
    if len(args) == 0:
        return None, GotoWarning("missing_both_magicwords", command=command)

    from_magicword = args[0]

    if len(args) == 1:
        return None, GotoWarning("missing_to_magicword",
                                 command=command, magicword=from_magicword)

    to_magicword = args[1]
    overwrite = '-f' in options or '--force' in options

    err = magic.rename_shortcut(from_magicword, to_magicword, overwrite)
    if err:
        return None, err
    magic.save()

    return "Renamed {} to {}".format(from_magicword, to_magicword), None
