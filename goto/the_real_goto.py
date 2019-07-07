#!/usr/bin/env python
# code: utf-8
'Goto - the magic project that takes you where you need to be, now.'
from __future__ import absolute_import

import sys
import codecs

from .gotomagic import text
from .gotomagic.magic import GotoMagic

from . import commands

# make sure we print in utf-8
try:
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
except:
    pass  # TODO: implement utf-8 encoding of py2.7


def main():
    if len(sys.argv) < 3:
        output, _ = commands.usage()
        print(output)
        exit(0)

    jfile = sys.argv[1]
    magic = GotoMagic(jfile)
    command = sys.argv[2]
    args = sys.argv[3:]

    output, err = run_command(magic, command, args)
    if err:
        print(err.message)
        exit(1)
    if output:
        print(output)
        exit(0)


def run_command(magic, command, args):
    if command in ['help', '-h', '/?', '--help']:
        return commands.usage()

    if command == 'add':
        return commands.add(magic, args)

    if command == 'update':
        return commands.update(magic, args)

    if command == 'rm':
        return commands.rm(magic, args)

    if command == 'show':
        return commands.show(magic, args)

    if command == 'copy':
        return commands.copy(magic, args)

    if command == 'list':
        return commands.list(magic, args)

    if command == 'subl':
        return commands.subl(magic, args)

    if command == 'vscode':
        return commands.vscode(magic, args)

    if command in ['intellij', 'idea']:
        return commands.intellij(magic, args)

    if '-o' in sys.argv or '--open' in sys.argv or 'open' in sys.argv:
        return commands.open(magic, args)

    if command == 'cd':
        return commands.cd(magic, args)

    return commands.default(magic, command)


if __name__ == '__main__':
    main()
