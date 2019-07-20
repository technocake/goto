name='plugins'

import os
import importlib

plugin_map = {}

__all__ = ['plugin_map']

#
# Import modules dynamically, and register the mapping between commands and modules
#
command_dir = os.listdir(os.path.dirname(os.path.realpath(__file__)))
module_names = list(filter(lambda file: file.endswith('.py') and not file == '__init__.py', command_dir))
module_names = list(map(lambda file: '.{}'.format(file.split('.')[0]), module_names))

for module_name in module_names:
    module = importlib.import_module(module_name, 'goto.plugins')
    for name in module.names():
        plugin_map[name] = module
