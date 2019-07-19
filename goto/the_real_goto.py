#!/usr/bin/env python
# coding: utf-8
'Goto - the magic project that takes you where you need to be, now.'
from __future__ import absolute_import, unicode_literals, print_function
from builtins import dict, str  # redefine dict and str to be py3-like in py2.
# http://johnbachman.net/building-a-python-23-compatible-unicode-sandwich.html

import os
import sys
import codecs

from .settings import GOTOPATH
from .gotomagic import text
from .gotomagic.magic import GotoMagic
from .gotomagic.utils import healthcheck, print_utf8, fix_python2

from . import commands

# make sure we print in utf-8
try:
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
except:
    pass


def main():
    fix_python2()
    exit_if_unhealthy()
    exit_with_usage_if_needed()

    project = sys.argv[1]
    magic = GotoMagic(project)
    command = sys.argv[2]
    args = sys.argv[3:]

    output, err = run_command(magic, command, args)
    if err:
        if output:
            print_utf8(output)
        print_utf8(err.message)
        exit(1)
    if output:
        print_utf8(output)
        exit(0)


def exit_if_unhealthy():
    err = healthcheck()
    if err:
        print_utf8(err.message)
        exit(1)


def exit_with_usage_if_needed():
    if len(sys.argv) < 3:
        output, _ = commands.usage()
        print_utf8(output)
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

    if command in ['--migrate', '--check-migrate']:
        return commands.migrate(magic, command, args)

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

    if command in ['mv', 'rename']:
        return commands.rename(magic, command, args)

    return commands.default(magic, command)


if __name__ == '__main__':
    main()
