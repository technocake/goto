
def run(magic, argv):
    magic.update_shortcut(argv[3], argv[4])
    magic.save()
    print('Updated magic word %s' % argv[3])
    return 0
