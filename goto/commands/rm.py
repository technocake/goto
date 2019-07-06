import sys

def run(magic):
    try:
        magic.remove_shortcut(sys.argv[3])
        magic.save()
        print('Removed magic word %s' % sys.argv[3])
        return 0
    except Exception:
        print('Failed to remove magic word %s' % sys.argv[3])
        return 1
