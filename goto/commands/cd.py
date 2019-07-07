def cd(magic, args):
    if (len(args) == 0):
        return None, "show_missing_magicword"

    word = args[0]
    open_terminal(magic.get_uri(word))
