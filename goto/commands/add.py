from ..gotomagic.text import Error

def add(magic, args):
    """
    Add magicword
    """

    if (len(args) == 0):
        return None, Error("missing_magicword_and_uri")

    if (len(args) == 1):
        return None, Error("missing_uri")

    word = args[0]
    uri = args[1]

    magic.add_shortcut(word, uri)
    magic.save()

    return 'Added magic word %s' % word, None
