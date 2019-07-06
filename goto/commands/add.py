
def run(magic, argv, print_text, text):
    try:
        magic.add_shortcut(argv[3], argv[4])
        magic.save()
        print('Added magic word %s' % argv[3])
        return 0
    except IndexError:
        if len(sys.argv) > 3:
            print_text(
                text.warning["missing_uri"],
                magicword = argv[3]
            )
            return 1
        else:
            print_text(
                text.warning["missing_magicword_and_uri"]
            )
        return 1
