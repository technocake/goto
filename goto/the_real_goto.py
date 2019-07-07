#!/usr/bin/env python
# code: utf-8
'Goto - the magic project that takes you where you need to be, now.'
from __future__ import absolute_import

import sys
import codecs
import subprocess

from .gotomagic.handlers import *
from .gotomagic.magic import GotoMagic, is_file
from .gotomagic import text
from .gotomagic.text import print_text

from .commands import\
    usage,\
    add,\
    update,\
    rm,\
    show


# make sure we print in utf-8
try:
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
except:
    pass  # TODO: implement utf-8 encoding of py2.7

def main():
    if len(sys.argv) < 3:
        return usage()

    jfile = sys.argv[1]
    magic = GotoMagic(jfile)
    command = sys.argv[2]
    args = sys.argv[3:]

    if command in ['help', '-h', '/?', '--help']:
        return usage()

    if command == 'add':
        return add(magic, args)

    if command == 'update':
        return update(magic, args)

    if command == 'rm':
        return rm(magic, args)

    if command == 'show':
        return show(magic, args)

    if command == 'copy':
        copy_to_clipboard(str(magic.get_uri(sys.argv[3])))
        exit(0)

    if command == 'list':
        magic.list_shortcuts(verbose=('-v' in sys.argv))
        exit(0)

    if command == 'subl':
        try:
            open_sublime(magic['code'])
        except KeyError:
            print(text.warning["no_magicword_named_code"])
            exit(1)
        except subprocess.CalledProcessError:
            print(text.error["subl_launch_failed"])
            exit(1)
        exit(0)

    if command == 'vscode':
        try:
            open_vscode(magic['code'])
        except KeyError:
            print(text.warning["no_magicword_named_code"])
            exit(1)
        except subprocess.CalledProcessError:
            print(text.error["vscode_launch_failed"])
            exit(1)
        exit(0)

    if command in ['intellij', 'idea']:
        try:
            open_intellij(magic['code'])
        except KeyError:
            print(text.warning["no_magicword_named_code"])
            exit(1)
        except subprocess.CalledProcessError:
            print(text.error["intellij_launch_failed"])
            exit(1)
        exit(0)

    if '-o' in sys.argv or '--open' in sys.argv or 'open' in sys.argv:
        open_folder(magic.get_uri(sys.argv[3]))
        exit(0)

    if command == 'cd':
        open_terminal(magic.get_uri(sys.argv[3]))
        exit(0)
    # default
    url = magic.get_uri(command)
    if url is not None:
        if is_file(url):
            open_folder(url)
        else:
            open_link(magic[command])


if __name__ == '__main__':
    output, err = main()
    if err:
        print_text(text.warning[err])
    else:
        print(output)


