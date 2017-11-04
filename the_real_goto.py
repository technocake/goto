#!/usr/bin/env python
# code: utf-8
'Goto - the magic project that takes you where you need to be, now.'

import subprocess
import webbrowser
import json
import sys
import os


def open_sublime(code):
    "hack"
    subprocess.call('subl "%s"' % code, shell=True)


def open_folder(folder):
    "opens folders"
    folder = os.path.expanduser(folder)
    subprocess.call('open "%s"' % folder, shell=True)


def open_link(url):
    "Opens a link. Might do more stuff later."
    webbrowser.open(url)


def open_terminal(path):
    " Opens a new terminal window and cd-s to the given path "
    path = os.path.expanduser(path)
    subprocess.call(""" osascript <<END
                        tell app "Terminal" to do script "cd %s"
                        END
                    """ % path, shell=True)


def list_words(magic):
    for k, v in magic.items():
        print("%16s \t --> \t %s" % (k, v))


def load_magic(jfile):
    if os.path.isfile(jfile) and os.path.getsize(jfile) > 0:
        with open(jfile, 'r') as f:
            magic = json.load(f)
    else:
        magic = {}
    return magic


def save_magic(jfile, magic):
    with open(jfile, 'w+') as f:
        json.dump(magic, f, sort_keys=True, indent=4)


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

        if sys.argv[2] == 'list':
            list_words(magic)
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
        open_link(magic[sys.argv[2]])
