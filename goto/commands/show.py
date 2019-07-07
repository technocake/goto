
def show(magic, args):
    if (len(args) == 0):
        return None, "show_missing_magicword"

    word = args[0]
    magic.show_shortcut(word)

