
def rm(magic, args):
    if (len(args) == 0):
        return None, "missing_magicword"

    word = args[0]

    magic.remove_shortcut(word)
    magic.save()
    return 'Removed magic word %s' % word
