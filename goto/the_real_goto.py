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
from .gotomagic.utils import healthcheck, print_utf8, fix_python2, make_sure_we_print_in_utf8
from .commands import commands, usage
from .plugins import plugins



def main():
    fix_python2()
    make_sure_we_print_in_utf8()
    exit_if_unhealthy()
    exit_with_usage_if_needed()

    project = sys.argv[1]
    magic = GotoMagic(project)
    argv = sys.argv[2:]

    commands.update(plugins)

    command, args, options = parse_args(argv, commands.keys())
    exit_if_no_command_and_no_args(command, args)

    output, err = commands[command].run(magic, command, args, options)
    if output:
        print_utf8(output)
    if err:
        print_utf8(err.message)
        exit(1)

    exit(0)


def parse_args(argv, command_names):
    command = None
    for arg in argv:
        if arg in command_names:
            command = arg
            argv.remove(arg)
            break

    args = list(filter(lambda word: not word.startswith('-'), argv))
    options = list(filter(lambda word: word.startswith('-'), argv))

    return command, args, options


def exit_if_unhealthy():
    err = healthcheck()
    if err:
        print_utf8(err.message)
        exit(1)


def exit_with_usage_if_needed():
    if len(sys.argv) < 3:
        print_usage()
        exit(0)


def exit_if_no_command_and_no_args(command, args):
    if not command and len(args) == 0:
        print_usage()
        exit(0)


def print_usage():
    print_utf8(usage())

if __name__ == '__main__':
    main()
