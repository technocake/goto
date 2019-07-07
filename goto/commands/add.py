
def add(magic, args):
    if (len(args) == 0):
        return None, "missing_magicword_and_uri"

    if (len(args) == 1):
        return None, "missing_uri"

    word = args[0]
    uri = args[1]

    magic.add_shortcut(word, uri)
    magic.save()
    return 'Added magic word %s' % word
