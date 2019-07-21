name='commands'

from . import default
from . import help
from .commands import commands

commands = [help] + commands

command_map = {}

for command in commands:
    for name in command.names():
        command_map[name] = command


__all__ = ['default', 'help', 'command_map', 'commands']
