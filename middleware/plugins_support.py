import importlib.util
import os
import sys


def get_plugins(plugins_folder="plugins"):
    if not plugins_folder in sys.path:
        sys.path.append(plugins_folder)

    plugins = []
    possible_plugins = os.listdir(plugins_folder)

    for possible_plugin in possible_plugins:
        if ".py" not in possible_plugin:
            continue
        module = importlib.import_module(possible_plugin.replace(".py", ""))
        plugins.append(module)

    return plugins
