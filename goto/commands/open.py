from ..gotomagic.handlers import open_folder

def open(magic, args):
    if (len(args) == 0):
        return None, "show_missing_magicword"

    word = args[0]
    open_folder(magic.get_uri(word))
