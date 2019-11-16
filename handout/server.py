from flask import Flask, request
import os
import os.path as osp
import json

app = Flask(__name__)


@app.route('/config', methods=['POST'])
def create_config_file():
    config_obj = request.get_json()
    config_path = osp.join('configs', '{}.cfg'.format(config_obj['name']))
    if not osp.exists(config_path):
        with open(config_path, 'w') as fp:
            fp.write(request.data)
    return '', 200


if __name__ == '__main__':
    os.chdir(osp.dirname(osp.realpath(__file__)))
    if not osp.exists('configs'):
        os.makedirs('configs')
    app.run(host='localhost', port=8080)
