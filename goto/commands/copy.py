from ..gotomagic.handlers import copy_to_clipboard

def copy(magic, args):
    if (len(args) == 0):
        return None, "missing_magicword"

    word = args[0]
    copy_to_clipboard(str(magic.get_uri(word)))
