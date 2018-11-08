import configparser
import multiprocessing
import os

from pluginbase import PluginBase

# Current module path
curr_mod_path = os.path.split(__file__)[0]

# Full path to configuration file and plugins folder
config_file = os.path.join(curr_mod_path, "application.ini")
plugins_path = os.path.join(curr_mod_path, "plugins")

# Reading configuration
config = configparser.ConfigParser()
config.read(config_file)

# Loading plugins
plugin_base = PluginBase(package="application.plugins")
plugin_source = plugin_base.make_plugin_source(searchpath=[plugins_path])
plugins = []

for plugin_name in plugin_source.list_plugins():
    plugins.append(plugin_source.load_plugin(plugin_name))


# Start each plugin (main function) into its own process
for plugin in plugins:
    proc = multiprocessing.Process(name=str(plugin), target=plugin.main, args=(config,))
    proc.start()
    proc.join()
