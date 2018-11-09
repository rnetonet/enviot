# EnvIOT

## What it is ?

EnvIOT is very simple, yer fully functional, framework to monitor environment conditions using IOT solutions.

It´s divided in three big layers:

**Perception**
- Data collection from sensors

**Middleware**
- Intermediary storage
- Periodic transfer of data to the cloud

**Application**
- Storage
- REST API
- Visualization

## Setup

Install `pip` and `virtualenv`:

```
sudo python3 -m pip install --upgrade pip
sudo python3 -m pip install --upgrade virtualenv
```

Inside the project folder, create a `virtualenv`:

```
python3 -m virtualenv .venv
```

Activate the `virtualenv`:

```
source .venv/bin/activate
```

Install the required packages:

```
pip install -r requirements.txt
```

Also, install **MongoDB**, follow this guide: 

[https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/)

## Usage


Before starting each layer, you will need to `activate` the `virtualenv`. Inside the project folder:

```
source .venv/bin/activate
```

### Start the Middleware layer

`python middleware/middleware.py`

```
(.venv) rnetonet@T440s:~/Workspace/enviot$ python middleware/middleware.py 
[D 181109 10:16:32 cloud_storage_mongodb:54] Loaded
[D 181109 10:16:32 fog_storage_mongodb:37] Loaded
```

The messages are the loaded plugins: fog temporary storage plugin and a fog to cloud sync plugin.

### Start the Perception layer

Actually the perception module simulates data collection using a historical dataset.

```
(.venv) rnetonet@T440s:~/Workspace/enviot$ python perception/perception_simulator.py 
[I 181109 10:21:44 perception_simulator:49] Sent: [{"reading_time":1528625503000,"temperature":27.0,"humidity":74.0,"count":1,"sound":487,"luminosity":1024,"client_id":"lab408"}]
[I 181109 10:21:49 perception_simulator:49] Sent: [{"reading_time":1532515576000,"temperature":26.0,"humidity":62.0,"count":16,"sound":490,"luminosity":294,"client_id":"lab408"}]
```

It will start sending requests to the `broker` (middleware).

## Start the Application layer

```
(.venv) rnetonet@T440s:~/Workspace/enviot$ python application/application.py 
[I 181109 10:27:07 rest:50] Loaded
 * Serving Flask app "pluginbase._internalspace._sp3e3d038c35cb8f10c62e7f9831b89267.rest" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
```

You can test the application layer through the REST service links, example: [http://localhost:5000/?count:int=10](http://localhost:5000/?count:int=10) (*The REST application supports some simple queries*).