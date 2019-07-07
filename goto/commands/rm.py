from ..gotomagic.text import GotoError, GotoWarning


def rm(magic, args):
    """
    Remove magicword
    """

    if (len(args) == 0):
        return None, GotoWarning("missing_magicword", command='rm')

    word = args[0]

    magic.remove_shortcut(word)
    magic.save()
    return 'Removed magic word %s' % word, None

