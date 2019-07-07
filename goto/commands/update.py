from ..gotomagic.text import GotoError, GotoWarning


def update(magic, args):
    """
    Update magicword
    """

    if (len(args) == 0):
        return None, GotoWarning("missing_magicword_and_uri", command='update')

    if (len(args) == 1):
        return None, GotoWarning("missing_uri",
                                 magicword=args[0],
                                 command='update')

    word = args[0]
    uri = args[1]

    magic.update_shortcut(word, uri)
    magic.save()

    return 'Updated magic word %s' % word, None
