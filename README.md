# EnvIOT

## Whats it is

A very simple, yet functional, framework to monitor environment conditions using IOT.
Split in three layers:

**Perception**
- Data collection from sensors

**Middleware**
- Intermediary storage
- Communcation with application layer
for data intermediary storage and communication with the application layer;

**Application**
- Storage
- Visualization
- REST API

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