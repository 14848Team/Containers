from flask import Flask, request
import os
import os.path as osp
import json

app = Flask(__name__)

root_dir = osp.dirname(osp.realpath(__file__))
config_dir = osp.join(root_dir, 'configs')


@app.route('/config', methods=['POST'])
def create_config_file():
    config_obj = request.get_json()
    config_path = osp.join(config_dir, '{}.cfg'.format(config_obj['name']))
    if not osp.exists(config_path):
        with open(config_path, 'w') as fp:
            fp.write(request.data.decode('utf-8'))
    return '', 200


if __name__ == '__main__':
    os.chdir(root_dir)
    if not osp.exists(config_dir):
        os.makedirs(config_dir)
    app.run(host='localhost', port=8080)
