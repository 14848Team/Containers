class MySupport:
    @staticmethod
    def url(hostname, port, path):
        portstr = str(port)
        url = "http://" + hostname + ":" + portstr + path
        return url

    @staticmethod
    def get_dict(which):
        if which == "invalid":
            return {
                "name": "sensiblename",
                "minor": "01",
                "base_image": "basefs.tar.gz",
                "mounts": [
                    "webserver.tar /webserver/ READ",
                    "homedir.tar /webserver/home READWRITE"
                ],
                "startup_script": "/webserver/tiny.sh",
                "startup_owner": "root",
                "startup_env": "PORT=8080;LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/var/lib"
            }
        
        elif which == "first_config":
            return {
                "name": "sensiblename",
                "major": "1",
                "minor": "01",
                "base_image": "basefs.tar.gz",
                "mounts": [
                    "potato.tar /webserver/potato READ",
                ],
                "startup_script": "/webserver/tiny.sh",
                "startup_owner": "root",
                "startup_env": "PORT=10000;LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/var/lib"
            }
        
        elif which == "first_launch":
            return {
                "name": "sensiblename",
                "major": "1",
                "minor": "01"
            }
        
        elif which == "second_config":
            return {
                "name": "terriblename",
                "major": "5",
                "minor": "23",
                "base_image": "basefs.tar.gz",
                "mounts": [
                    "cabbage.tar /webserver/cabbage READWRITE",
                    "potato.tar /webserver/cabbage/potato READWRITE",
                ],
                "startup_script": "/webserver/tiny.sh",
                "startup_owner": "root",
                "startup_env": "PORT=20000;LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/var/lib"
            }
        
        elif which == "second_launch":
            return {
                "name": "terriblename",
                "major": "5",
                "minor": "23",
            }
        
        elif which == "third_config":
            return {
                "name": "terriblename",
                "major": "5",
                "minor": "78",
                "base_image": "basefs.tar.gz",
                "mounts": [
                    "potato.tar /webserver/potato READWRITE",
                    "tomato.tar /webserver/tomato READWRITE",
                    "cabbage.tar /webserver/tomato/cabbage READ",
                ],
                "startup_script": "/webserver/tiny.sh",
                "startup_owner": "root",
                "startup_env": "PORT=30000;LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/var/lib;SILLYVAR=WOLOLO "
            }

        elif which == "third_launch":
            return {
                "name": "terriblename",
                "major": "5",
                "minor": "78",
            }
        else:
            return {}

