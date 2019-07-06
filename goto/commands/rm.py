
def run(magic, argv):
    try:
        magic.remove_shortcut(argv[3])
        magic.save()
        print('Removed magic word %s' % argv[3])
        return 0
    except Exception:
        print('Failed to remove magic word %s' % argv[3])
        return 1
