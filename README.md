# EnvIOT

## Whats it is

A project, specification and some implementation, to monitor some sensors and save the data, leveraging MQTT, FOG and Cloud. Some extras: REST API and Visualization.

## Dependencies

- perception
    - paho-mqtt (http://www.eclipse.org/paho/clients/python/)

- middleware
    - mosquitto (https://mosquitto.org/)

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