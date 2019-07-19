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


input_commands = {
    '--help': 'usage',
    '-h': 'usage',
    'help': 'usage',
    '/?': 'usage',

    'add': 'add',
    'update': 'update',
    'rm': 'rm',
    'show': 'show',
    'copy': 'copy',
    'list': 'list',
    'mv': 'rename',
    'rename': 'rename',

    '--migrate': 'migrate',
    '--check-migrate': 'migrate',

    'subl': 'subl',
    'vscode': 'vscode',
    'intelij': 'intelij',
    'idea': 'intelij'
}

commands = set(input_commands.values())


def main():
    make_sure_we_print_in_utf8()

    fix_python2()
    exit_if_unhealthy()
    exit_with_usage_if_needed()

    project = sys.argv[1]
    magic = GotoMagic(project)
    argv = sys.argv[2:]

    command, argv = parse_command(argv)
    args = list(filter(lambda word: not word.startswith('-'), argv))
    options = list(filter(lambda word: word.startswith('-'), argv))

    if not command and len(args) == 0:
        print_utf8("No command or magicwords found") # TODO add warning text here
        exit(1)

    output, err = run_command(magic, command, args, options)

    if output:
        print_utf8(output)

    if err:
        print_utf8(err.message)
        exit(1)

    exit(0)


def parse_command(argv):

    for arg in argv:
        if arg in commands.map.keys():
            command = arg
            argv.remove(arg)
            return command, argv

    return None, argv


def run_command(magic, command, args, options):
    if command:
        return commands.map[command](magic, command, args, options)
    else:
        return commands.default(magic, None, args, options)


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

    exit(0)

def make_sure_we_print_in_utf8():
    try:
        if sys.stdout.encoding != 'utf-8':
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    except:
        pass  # TODO: implement utf-8 encoding of py2.7





if __name__ == '__main__':
    main()
