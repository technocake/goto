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
        output = commands.usage()
        print(output)
        exit(0)

    jfile = sys.argv[1]
    magic = GotoMagic(jfile)
    argv = sys.argv[2:]

    options = list(filter(lambda word: word.startswith('-'), argv))
    args = list(filter(lambda word: not word.startswith('-'), argv))

    if len(args) == 0:
        print(commands.usage())
        exit(0)

    command = args[0]
    args = args[1:]

    output, err = run_command(magic, command, args, options)
    if err:
        print(err.message)
        exit(1)
    if output:
        print(output)
        exit(0)

    exit(0)


def run_command(magic, command, args, options):

    if command == 'help':
        return commands.usage(), None

    if command == 'add':
        return commands.add(magic, command, args, options)

    if command == 'update':
        return commands.update(magic, command, args, options)

    if command == 'rm':
        return commands.rm(magic, command, args, options)

    if command == 'show':
        return commands.show(magic, command, args, options)

    if command == 'copy':
        return commands.copy(magic, command, args, options)

    if command == 'list':
        return commands.list(magic, command, args, options)

    if command == 'subl':
        return commands.subl(magic, command, args, options)

    if command == 'vscode':
        return commands.vscode(magic, command, args, options)

    if command in ['intellij', 'idea']:
        return commands.intellij(magic, command, args, options)

    if command == 'open':
        return commands.open(magic, command, args, options)

    if command == 'cd':
        return commands.cd(magic, command, args, options)

    if command in ['mv', 'rename']:
        return commands.rename(magic, command, args, options)

    args = [command] + args
    return commands.default(magic, args, options)


if __name__ == '__main__':
    main()
