# EnvIOT

## Whats it is

A very simple yet functional framework to monitor environment conditions using IOT.
Applying MQTT for communication, a gateway as a FOG component and a layer of applications: storage, REST API and visualization.

## Dependencies

- perception
    - paho-mqtt (http://www.eclipse.org/paho/clients/python/)

- middleware
    - mosquitto (https://mosquitto.org/)
    - paho-mqtt (http://www.eclipse.org/paho/clients/python/)

- application
    - MongoDB (https://www.mongodb.com/)
    - EVE (http://docs.python-eve.org/en/latest/)

## Structure

```
+---------------------+
|                     | * Storage
|     application     | * REST API
|                     | * Visualization
+---------------------+
|                     | * MQTT Server
|     middleware      | * Gateway for storage
|                     |
+---------------------+
|                     | * Simulation of sensors
|     perception      | 
|                     |
+---------------------+
```