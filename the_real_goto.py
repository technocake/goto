#!/usr/bin/env python
# code: utf-8
'Goto - the magic project that takes you where you need to be, now.'
import sys
from gotomagic.handlers import *
from gotomagic.magic import load_magic, save_magic


def list_shortcuts(magic, args):
    if "-v" in args:
        for k, v in magic.items():
            print("%16s --> %s" % (k, v))
    else:
        for k in magic.keys():
            print(k)


if __name__ == "__main__":
    jfile = sys.argv[1]
    magic = load_magic(jfile)

    if len(sys.argv) > 2:
        if sys.argv[2] == 'add':
            magic[sys.argv[3]] = sys.argv[4]
            save_magic(jfile, magic)
            print('Added magic word %s' % sys.argv[3])
            exit(0)

        if sys.argv[2] == 'rm':
            magic.pop(sys.argv[3])
            save_magic(jfile, magic)
            print('Removed magic word %s' % sys.argv[3])
            exit(0)

        if sys.argv[2] == 'show':
            print(magic[sys.argv[3]])
            exit(0)

        if sys.argv[2] == 'copy':
            copy_to_clipboard(str(magic[sys.argv[3]]))
            exit(0)

        if sys.argv[2] == 'list':
            list_shortcuts(magic, sys.argv)
            exit(0)

        if sys.argv[2] == 'subl':
            open_sublime(magic['code'])
            exit(0)

        if '-f' in sys.argv:
            open_folder(magic[sys.argv[3]])
            exit(0)

        if sys.argv[2] == 'cd':
            open_terminal(magic[sys.argv[3]])
            exit(0)
        # default
        open_link(magic[sys.argv[2]])
