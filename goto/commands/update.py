from ..gotomagic.text import GotoError


def update(magic, args):
    """
    Update magicword
    """

    if (len(args) == 0):
        return None, GotoError("missing_magicword_and_uri")

    if (len(args) == 1):
        return None, GotoError("missing_uri")

    word = args[0]
    uri = args[1]

    magic.update_shortcut(word, uri)
    magic.save()

    return 'Updated magic word %s' % word, None
