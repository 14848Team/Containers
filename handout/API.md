# IMPORTANT!!!!
In all cases, if the API call receives invalid data, always return `409 Bad Request`.

# Config
Create configuration file for a container.

**URL** : `/config`

**Method** : `POST`

**Input Data** : 
```json
{
    "name": "sensiblename",
    "major": "1",
    "minor": "01",
    "base_image": "basefs.tar.gz",
    "mounts": [
        "webserver.tar /webserver/ READ",
        "homedir.tar /webserver/home READWRITE"
    ],
    "startup_script": "/webserver/tiny.sh",
    "startup_owner": "root",
    "startup_env": "PORT=8080;LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/var/lib64"
}
```

## Responses

**Code** : `200 OK`

**Content** : NIL

**Result**: 

Creates a configuration file of name `sensiblename-1-01.cfg` with contents:
```json
{
    "name": "sensiblename",
    "major": "1",
    "minor": "01",
    "base_image": "basefs.tar.gz",
    "mounts": [
        "webserver.tar /webserver/ READ",
        "homedir.tar /webserver/home READWRITE"
    ],
    "startup_script": "/webserver/tiny.sh",
    "startup_owner": "root",
    "startup_env": "PORT=8080;LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/var/lib64"
}
```

# Configuration Info

Returns a listing of existing configfiles.

**URL** : `/cfginfo`

**Method** : `GET`

**Input Data** : NIL

## Responses

**Code** : `200 OK`

**Content** : 
``` json
{
    "files": []    
}
```

OR

``` json
{
    "files": [
        "sensiblename-1-01.cfg",
        "sensiblename-1-02.cfg",
        "sensiblename-5-09.cfg",
        "terriblename-1.23.cfg"
    ]    
}
```

**Result**: NIL

# Launch Container

Create ("launch") a running instance of a specific container.

**URL** : `/launch`

**Method** : `POST`

**Input Data** : 
``` json
{
    "name": "sensiblename",
    "major": "1",
    "minor": "01"
}
```

## Responses

**Code** : `200 OK`

**Content** : 
``` json
{
    "instance": "instance_name",
    "name": "sensiblename",
    "major": "1",
    "minor": "01"
}
```

**Result**: 
Launches a container based on the matching configuration file.

### OR

**Code** : `404 Not Found`

**Content** : NIL

**Result**: NIL

# List Instances

List running instances.

**URL** : `/list`

**Method** : `GET`

**Input Data** : NIL

## Responses

**Code** : `200 OK`

**Content** : 
```json
{
    "instances": []  
}
```

OR

```json
{
    "instances": [
        {
            "instance": "instance_name",
            "name": "sensiblename",
            "major": "1",
            "minor": "01"
        }, 
        {
            "instance": "another_name",
            "name": "sensiblename",
            "major": "1",
            "minor": "01"        
        },
        {
            "instance": "yet_another_name",
            "name": "terriblename",
            "major": "1",
            "minor": "23"        
        }
    ]  
}
```

**Result**: NIL

# Destroy A Running Instance

**URL** : `/destroy/:pk/`

**URL Parameters** : `pk=[string]` where `pk` is the instance name.

**Method** : `DELETE`

**Input Data** : NIL

## Responses

**Code** : `404 Not Found`

**Content** : NIL

**Result**: NIL

### OR

**Code** : `200 OK`

**Content** : NIL

**Result**: Kill the instance.

# Destroy All

**URL** : `/destroyall/`

**Method** : `DELETE`

**Input Data** : NIL

## Responses

**Code** : `200 OK`

**Content** : NIL

**Result**: Kill all runnings instances.
