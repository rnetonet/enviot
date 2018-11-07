import configparser
import os

import paho.mqtt.client as paho
from pluginbase import PluginBase

# Current module path
curr_mod_path = os.path.split(__file__)[0]

# Full path to configuration file and plugins folder
config_file = os.path.join(curr_mod_path, "middleware.ini")
plugins_path = os.path.join(curr_mod_path, "plugins")

# Reading configuration
config = configparser.ConfigParser()
config.read(config_file)

# Loading plugins
plugin_base = PluginBase(package="middleware.plugins")
plugin_source = plugin_base.make_plugin_source(searchpath=[plugins_path])
plugins = []

for plugin_name in plugin_source.list_plugins():
    plugins.append(plugin_source.load_plugin(plugin_name))

# Gives each plugin the opportunity to handle the mssage
def on_message(client, userdata, message):
    payload_decoded = message.payload.decode("utf8")
    for plugin in plugins:
        plugin.handle(payload_decoded)


# Paho setup
client = paho.Client()
client.on_message = on_message
client.connect(config["middleware"]["broker_host"])
client.subscribe("enviot/#")
client.loop_forever()
