#!/usr/bin/env python
# code: utf-8
'Goto - the magic project that takes you where you need to be, now.'
from __future__ import absolute_import

import sys
import codecs

from .gotomagic import text
from .gotomagic.text import print_text
from .gotomagic.magic import GotoMagic

from .commands import\
    usage,\
    add,\
    update,\
    rm,\
    show,\
    copy,\
    list,\
    subl,\
    vscode,\
    intellij,\
    open,\
    cd,\
    default

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

    output, err = run_command(magic, command, args)

    if err:
        error_text = text.warning.get(err, err);
        print_text(error_text)

    if output:
        print(output)


def run_command(magic, command, args):
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
        return copy(magic, args)

    if command == 'list':
        return list(magic, args)

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

    return default(magic, command)


if __name__ == '__main__':
    main()

