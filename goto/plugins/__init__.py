name='plugins'

from . import intellij
from . import subl
from . import vscode

plugins = [intellij, subl, vscode]
plugin_map = {}

for plugin in plugins:
    for name in plugin.names():
        plugin_map[name] = plugin

__all__ = ['plugin_map', 'plugins']
