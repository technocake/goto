from functools import reduce

from .commands import commands_list
from ..plugins import plugins_list


def help():
    return "{0:10}{1}".format('help', 'Show this message again')


def names():
    return ['help', '--help', '-h', '/?']


def run(magic, command, args, options):
    """
    Get information about usage
    """
    header = """
Goto - the magic traveler, how may I help you?

Wondering how to change project?
    project help                  Consult my brother in command

Basic usage
    goto <magicword>      Go to shortcut
    goto [<magicword>...] Go to many shortcuts
"""

    commands_help = map(lambda x: x.help(), commands_list)
    commands_sorted = sorted(commands_help, key=lambda x: x.startswith('-'), reverse=False)
    commands_text = reduce(lambda x,y: x + "{0:>8} {1}\n".format('goto', y), commands_sorted, '\nCommands\n')

    plugins_help = map(lambda x: x.help(), plugins_list)
    plugins_sorted = sorted(plugins_help, key=lambda x: x.startswith('-'), reverse=False)
    plugins_text = reduce(lambda x,y: x + "{0:>8} {1}\n".format('goto', y), plugins_sorted, '\nPlugins\n')

    return "{}{}{}".format(header, commands_text, plugins_text), None
