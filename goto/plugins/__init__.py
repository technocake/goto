name='plugins'

from . import copy
from . import intellij
from . import open
from . import subl
from . import vscode

plugins_list = [
    copy,
    intellij,
    open,
    subl,
    vscode
]

plugins = {}

for plugin in plugins_list:
    for name in plugin.names():
        plugins[name] = plugin

__all__ = ['plugins', 'plugins_list']
