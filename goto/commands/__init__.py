name='commands'

from . import help
from . import default
from .commands import commands_list

commands_list = [help, default] + commands_list

commands = {}

for command in commands_list:
    for name in command.names():
        commands[name] = command


usage, _ = help.run(None,None,None,None)

__all__ = ['usage', 'commands', 'commands_list']
