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
    show,\
    copy,\
    index,\
    subl,\
    vscode,\
    intellij,\
    open,\
    cd


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
        return usage(magic, args)

    if command == 'add':
        return add(magic, args)

    if command == 'update':
        return update(magic, args)

    if command == 'rm':
        return rm(magic, args)

    if command == 'show':
        return show(magic, args)

    if command == 'copy':
        return copy(magic, args)

    if command == 'list':
        return index(magic, args)

    if command == 'subl':
        return subl(magic, args)

    if command == 'vscode':
        return vscode(magic, args)

    if command in ['intellij', 'idea']:
        return intellij(magic, args)

    if '-o' in sys.argv or '--open' in sys.argv or 'open' in sys.argv:
        return open(magic, args)

    if command == 'cd':
        return cd(magic, args)

    # default
    url = magic.get_uri(command)
    if url is None:
        return

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


