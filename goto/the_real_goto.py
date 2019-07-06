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

from .commands import \
    usage \


# make sure we print in utf-8
try:
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
except:
    pass  # TODO: implement utf-8 encoding of py2.7

def main():
    if len(sys.argv) == 2:
        return usage()

    jfile = sys.argv[1]
    magic = GotoMagic(jfile)
    command = sys.argv[2]

    if  command in ['help', '-h', '/?', '--help']:
        return usage()


    if sys.argv[2] == 'add':
        try:
            magic.add_shortcut(sys.argv[3], sys.argv[4])
            magic.save()
            print('Added magic word %s' % sys.argv[3])
            exit(0)
        except IndexError:
            if len(sys.argv) > 3:
                print_text(
                    text.warning["missing_uri"],
                    magicword=sys.argv[3]
                )
                exit(1)
            else:
                print_text(
                    text.warning["missing_magicword_and_uri"]
                )
            exit(1)

    if sys.argv[2] == 'update':
        magic.update_shortcut(sys.argv[3], sys.argv[4])
        magic.save()
        print('Updated magic word %s' % sys.argv[3])
        exit(0)

    if sys.argv[2] == 'rm':
        try:
            magic.remove_shortcut(sys.argv[3])
            magic.save()
            print('Removed magic word %s' % sys.argv[3])
            exit(0)
        except Exception:
            print('Failed to remove magic word %s' % sys.argv[3])
            exit(1)

    if sys.argv[2] == 'show':
        try:
            magic.show_shortcut(sys.argv[3])
            exit(0)
        except IndexError:
            print_text(text.warning["show_missing_magicword"])
            exit(1)

    if sys.argv[2] == 'copy':
        copy_to_clipboard(str(magic.get_uri(sys.argv[3])))
        exit(0)

    if sys.argv[2] == 'list':
        magic.list_shortcuts(verbose=('-v' in sys.argv))
        exit(0)

    if sys.argv[2] == 'subl':
        try:
            open_sublime(magic['code'])
        except KeyError:
            print(text.warning["no_magicword_named_code"])
            exit(1)
        except subprocess.CalledProcessError:
            print(text.error["subl_launch_failed"])
            exit(1)
        exit(0)

    if sys.argv[2] == 'vscode':
        try:
            open_vscode(magic['code'])
        except KeyError:
            print(text.warning["no_magicword_named_code"])
            exit(1)
        except subprocess.CalledProcessError:
            print(text.error["vscode_launch_failed"])
            exit(1)
        exit(0)

    if sys.argv[2] in ['intellij', 'idea']:
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

    if sys.argv[2] == 'cd':
        open_terminal(magic.get_uri(sys.argv[3]))
        exit(0)
    # default
    url = magic.get_uri(sys.argv[2])
    if url is not None:
        if is_file(url):
            open_folder(url)
        else:
            open_link(magic[sys.argv[2]])


if __name__ == '__main__':
    main()
