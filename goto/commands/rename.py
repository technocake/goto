from ..gotomagic.text import GotoWarning


def rename(magic, command, args):
    if len(args) == 0:
        return None, GotoWarning("missing_both_magicwords", command=command)

    from_magicword = args[0]

    if len(args) == 1:
        return None, GotoWarning("missing_to_magicword", command=command, magicword=from_magicword)

    to_magicword = args[1]

    if from_magicword not in magic.magic:
        return None, GotoWarning("magicword_does_not_exist", magicword=from_magicword)

    if to_magicword in magic.magic:
        return None, GotoWarning("adding_existing_magicword_short", magicword=to_magicword, uri=magic[to_uri])

    from_uri = magic[from_magicword]
    del magic[from_magicword]
    magic[to_magicword] = from_uri
    magic.save()

    return "Renamed %s to %s" % (from_magicword, to_magicword), None
