#!/usr/bin/env python
# coding: utf-8
'Goto - the magic project that takes you where you need to be, now.'
from __future__ import absolute_import, unicode_literals, print_function
from builtins import dict, str  # redefine dict and str to be py3-like in py2.
# http://johnbachman.net/building-a-python-23-compatible-unicode-sandwich.html

import re
import os
import sys
import codecs

from .settings import GOTOPATH
from .gotomagic import text
from .gotomagic.magic import GotoMagic
from .gotomagic.utils import healthcheck, print_utf8, fix_python2
from . import commands


command_map = {
    '--help':  commands.usage,
    '-h':  commands.usage,
    'help':  commands.usage,
    '/?':  commands.usage,

    'add': commands.add,
    'update': commands.update,
    'rm': commands.rm,
    'show': commands.show,
    'copy': commands.copy,
    'list': commands.list,
    'mv': commands.rename,
    'rename': commands.rename,

    'open': commands.open,
    '-o': commands.open,
    '--open': commands.open,

    '--migrate': commands.migrate,
    '--check-migrate': commands.check_migrate,

    'subl': commands.subl,
    'vscode': commands.vscode,
    'intelij': commands.intellij,
    'idea': commands.intellij,
}

def main():
    fix_python2()
    make_sure_we_read_and_write_in_utf8()
    exit_if_unhealthy()

    args = read_args(sys.argv, sys.stdin)
    exit_with_usage_if_needed(args)

    project = args[1]
    magic = GotoMagic(project)
    args = args[2:]

    command, args = parse_command(args)
    args = list(filter(lambda word: not word.startswith('-'), args))
    options = list(filter(lambda word: word.startswith('-'), args))

    if not command and len(args) == 0:
        output = commands.usage()
        print_utf8(output)
        exit(0)

    output, err = run_command(magic, command, args, options)

    if output:
        print_utf8(output)

    if err:
        print_utf8(err.message)
        exit(1)

    exit(0)


def read_args(cmd_args, stdin):
    stdin_is_empty = os.isatty(0)
    if stdin_is_empty:
        return cmd_args

    lines = stdin.readlines()
    stdin_args = " ".join(lines)
    stdin_args = re.sub(r'\s+', ' ', stdin_args)
    stdin_args = stdin_args.split(' ')
    stdin_args = filter(lambda x: x != "", stdin_args)

    return cmd_args + stdin_args


def parse_command(argv):
    for arg in argv:
        if arg in command_map.keys():
            command = arg
            argv.remove(arg)
            return command, argv

    return None, argv


def run_command(magic, command, args, options):
    if command:
        return command_map[command](magic, command, args, options)
    else:
        return commands.default(magic, None, args, options)


def exit_if_unhealthy():
    err = healthcheck()
    if err:
        print_utf8(err.message)
        exit(1)


def exit_with_usage_if_needed(args):
    if len(args) < 3:
        output = commands.usage()
        print_utf8(output)
        exit(0)


def make_sure_we_read_and_write_in_utf8():
    try:
        if sys.stdin.encoding != 'utf-8':
            sys.stdin = codecs.getwriter('utf-8')(sys.stdin.buffer, 'strict')

        if sys.stdout.encoding != 'utf-8':
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    except:
        pass  # TODO: implement utf-8 encoding of py2.7


if __name__ == '__main__':
    main()
