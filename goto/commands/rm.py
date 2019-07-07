def rm(magic, args):
    """
    Remove magicword
    """

    if (len(args) == 0):
        return None, "missing_magicword"

    word = args[0]

    magic.remove_shortcut(word)
    magic.save()
    return 'Removed magic word %s' % word, None

