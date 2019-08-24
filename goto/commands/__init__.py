name='commands'

from . import help
from . import default
from .commands import commands_list

commands_list = [help, default] + commands_list

commands = {}

for command in commands_list:
    for name in command.names():
        commands[name] = command


def usage():
    '''
        Making this a procedure to avoid  that the help_text could
        be outdated if any later methods inject plugins or other commands.

        This will evaluate the help text for all
        installed commands.
    '''
    help_text, _ = help.run(None, None, None, None)
    return help_text


__all__ = ['usage', 'commands', 'commands_list']
