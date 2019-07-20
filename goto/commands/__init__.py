name='commands'

from . import default
from . import add
from . import check_migrate
from . import copy
from . import list
from . import migrate
from . import open
from . import rename
from . import rm
from . import show
from . import update

commands = [add,check_migrate,copy,list,migrate,open,rename,rm,show,update]
command_map = {}

for command in commands:
    for name in command.names():
        command_map[name] = command

__all__ = ['default', 'command_map']
