from ..gotomagic.text import GotoError, GotoWarning

def help():
    return "{0:10}{1:30}{2}".format('update', '<magicword> <new url/path>', 'Update shortcut')


def names():
    return [
        'update',
        '--update'
    ]

def run(magic, command, args, options):
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

    err = magic.update_shortcut(word, uri)
    if err:
        return None, err

    err = magic.save()
    if err:
        return None, err

    return 'Updated magic word %s' % word, None
