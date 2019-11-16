from flask import Flask, request
import os
import os.path as osp
import json

app = Flask(__name__)

root_dir = osp.dirname(osp.realpath(__file__))
config_dir = osp.join(root_dir, 'configs')


@app.route('/config', methods=['POST'])
def create_config_file():
    if not osp.exists(config_dir):
        os.makedirs(config_dir)
    config_obj = request.get_json(silent=True)
    if config_obj is None:
        return '', 409
    for field in ['name', 'major', 'minor', 'base_image',
                  'mounts', 'startup_script', 'startup_owner',
                  'startup_env']:
        if field not in config_obj:
            return '', 409
    config_path = osp.join(config_dir,
                           '{}-{}-{}.cfg'.
                           format(config_obj['name'],
                                  config_obj['major'],
                                  config_obj['minor']))

    if not osp.exists(config_path):
        with open(config_path, 'w') as fp:
            fp.write(request.data.decode('utf-8'))
        return '', 200
    else:
        return '', 409


@app.route('/cfginfo', methods=['GET'])
def list_config_files():
    res = {
        'files': sorted(os.listdir(config_dir))
    }
    return res, 200


if __name__ == '__main__':
    os.chdir(root_dir)
    if not osp.exists(config_dir):
        os.makedirs(config_dir)
    app.run(host='localhost', port=8080)
