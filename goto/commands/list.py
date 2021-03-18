# coding: utf-8
from __future__ import unicode_literals


def help():
    return "{0:10}{1:30}{2}".format('list', '[-v]', 'List all shortcuts')


def names():
    return ['list', '--list']


def run(magic, command, args, options):
    """
    List commands
    """
    verbose = '-v' in options or '--verbose' in options
    magicwords = magic.list_shortcuts(verbose=verbose)

    if not magicwords:
        return None, None

    if verbose:
        output = ""
        for word in magicwords:
            uri = magic.get_uri(word)
            if uri is None:
                return None, GotoWarning("magicword_does_not_exist", magicword=word)
            output += "%16s --> %s\n" % (word, uri)
    else:
        output = "\n".join(magicwords)

    return output, None
