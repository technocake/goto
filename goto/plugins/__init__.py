name='plugins'

from . import copy
from . import intellij
from . import open
from . import subl
from . import vscode

plugins = [
    copy,
    intellij,
    open,
    subl,
    vscode
]

plugin_map = {}

for plugin in plugins:
    for name in plugin.names():
        plugin_map[name] = plugin

__all__ = ['plugin_map', 'plugins']
