import sys

def run(magic):
    magic.update_shortcut(sys.argv[3], sys.argv[4])
    magic.save()
    print('Updated magic word %s' % sys.argv[3])
    return 0
