from ..gotomagic.text import GotoWarning
from ..gotomagic.exceptions import warnings


def rename(magic, command, args):
    if len(args) == 0:
        return None, GotoWarning("missing_both_magicwords", command=command)

    from_magicword = args[0]

    if len(args) == 1:
        return None, GotoWarning("missing_to_magicword",
                                 command=command, magicword=from_magicword)

    to_magicword = args[1]
    overwrite = '-f' in args or '--force' in args

    try:
        magic.rename_shortcut(from_magicword, to_magicword, overwrite)
        magic.save()
    except warnings.GotoException as warning:
        return None, warning

    return "Renamed {} to {}".format(from_magicword, to_magicword), None
