#!/usr/bin/env python
# code: utf-8
'Goto - the magic project that takes you where you need to be, now.'
from __future__ import absolute_import, unicode_literals

import os
import sys
import codecs

from .gotomagic import text
from .gotomagic.magic import GotoMagic
from .gotomagic.utils import healthcheck
from . import commands


def main():
    # make sure we print in utf-8
    try:
        if sys.stdout.encoding != 'utf-8':
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    except:
        pass  # TODO: implement utf-8 encoding of py2.7

    err = healthcheck()
    if err:
        print(err.message)
        exit(2)

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

    exit(0)


def run_command(magic, command, args):
    if command in ['help', '-h', '/?', '--help']:
        return commands.usage()

    if command == 'add':
        return commands.add(magic, command, args)

    if command == 'update':
        return commands.update(magic, command, args)

    if command == 'rm':
        return commands.rm(magic, command, args)

    if command == 'show':
        return commands.show(magic, command, args)

    if command == 'copy':
        return commands.copy(magic, command, args)

    if command == 'list':
        return commands.list(magic, command, args)

    if command == 'subl':
        return commands.subl(magic, command, args)

    if command == 'vscode':
        return commands.vscode(magic, command, args)

    if command in ['intellij', 'idea']:
        return commands.intellij(magic, command, args)

    if command in ['-o', '--open', 'open']:
        return commands.open(magic, command, args)

    if command == 'cd':
        return commands.cd(magic, command, args)

    if command in ['mv', 'rename']:
        return commands.rename(magic, command, args)

    args = [command] + args
    return commands.default(magic, args)


if __name__ == '__main__':
    main()
