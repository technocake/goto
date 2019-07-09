from ..gotomagic.text import GotoWarning


def rename(magic, command, args):
    if len(args) == 0:
        return None, GotoWarning("missing_both_magicwords", command=command)

    from_magicword = args[0]

    if len(args) == 1:
        return None, GotoWarning("missing_to_magicword",
                                 command=command, magicword=from_magicword)

    to_magicword = args[1]
    overwrite = '-f' in args or '--force' in args

    err = magic.rename_shortcut(from_magicword, to_magicword, overwrite)
    if err:
        return None, err
    magic.save()

    return "Renamed {} to {}".format(from_magicword, to_magicword), None
