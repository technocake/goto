#!/usr/bin/env python
# coding: utf-8
'Goto - the magic project that takes you where you need to be, now.'
from __future__ import absolute_import, unicode_literals, print_function
from builtins import dict, str  # redefine dict and str to be py3-like in py2.
# http://johnbachman.net/building-a-python-23-compatible-unicode-sandwich.html

import os
import sys
import codecs
import importlib

from .settings import GOTOPATH
from .gotomagic import text
from .gotomagic.magic import GotoMagic
from .gotomagic.utils import healthcheck, print_utf8, fix_python2
from .commands import usage, default

command_map = {}

def main():
    fix_python2()
    make_sure_we_print_in_utf8()

    exit_if_unhealthy()
    exit_with_usage_if_needed()

    project = sys.argv[1]
    magic = GotoMagic(project)
    argv = sys.argv[2:]

    register_commands()

    command, argv = parse_command(argv)
    args = list(filter(lambda word: not word.startswith('-'), argv))
    options = list(filter(lambda word: word.startswith('-'), argv))

    if not command and len(args) == 0:
        output = usage.run()
        print_utf8(output)
        exit(0)

    output, err = run_command(magic, command, args, options)

    if output:
        print_utf8(output)

    if err:
        print_utf8(err.message)
        exit(1)

    exit(0)

def register_commands():
    global command_map
    command_dir = '{}/commands'.format(os.path.dirname(os.path.realpath(__file__)))
    module_names = list(filter(lambda file: file.endswith('.py') and not file == '__init__.py', os.listdir(command_dir)))
    module_names = list(map(lambda file: '.commands.{}'.format(file.split('.')[0]), module_names))

    for module_name in module_names:
        module = importlib.import_module(module_name, 'goto')
        for name in module.names():
            command_map[name] = module.run


def parse_command(argv):
    global command_map

    for arg in argv:
        if arg in command_map.keys():
            command = arg
            argv.remove(arg)
            return command, argv

    return None, argv


def run_command(magic, command, args, options):
    global command_map

    if command:
        return command_map[command](magic, command, args, options)
    else:
        return default.run(magic, None, args, options)


def exit_if_unhealthy():
    err = healthcheck()
    if err:
        print_utf8(err.message)
        exit(1)


def exit_with_usage_if_needed():
    if len(sys.argv) < 3:
        output = usage.run()
        print_utf8(output)
        exit(0)


def make_sure_we_print_in_utf8():
    try:
        if sys.stdout.encoding != 'utf-8':
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    except:
        pass  # TODO: implement utf-8 encoding of py2.7





if __name__ == '__main__':
    main()
