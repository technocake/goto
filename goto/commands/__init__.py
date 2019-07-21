name='commands'

from . import help
from .commands import commands

commands = [help] + commands

command_map = {}

for command in commands:
    for name in command.names():
        command_map[name] = command


usage, _ = help.run(None,None,None,None)

__all__ = ['usage', 'command_map', 'commands']
