from ..gotomagic.text import GotoError

def add(magic, args):
    """
    Add magicword
    """

    if (len(args) == 0):
        return None, GotoError("missing_magicword_and_uri")

    if (len(args) == 1):
        return None, GotoError("missing_uri", magicword=args[0])

    magicword = args[0]
    uri = args[1]

    magic.add_shortcut(magicword, uri)
    magic.save()

    return 'Added magic word %s' % magicword, None
