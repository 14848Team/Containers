from flask import Flask, request
import os
import os.path as osp
import json
from collections import Counter, OrderedDict
from multiprocessing import Process

app = Flask(__name__)

root_dir = osp.dirname(osp.realpath(__file__))
config_dir = osp.join(root_dir, 'configs')
container_dir = osp.join(root_dir, 'containers')
instance_counter = Counter()
instances = OrderedDict()
subprocess_dict = {}


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


@app.route('/launch', methods=['POST'])
def launch_container():
    create_dir_if_not_exists(container_dir)
    payload = request.get_json(silent=True)
    if payload is None:
        return '', 409
    for field in ['name', 'major', 'minor']:
        if field not in payload:
            return '', 409
    config_name = payload['name']
    major = payload['major']
    minor = payload['minor']
    if not osp.exists(osp.join(config_dir, '{}-{}-{}.cfg'.format(config_name,
                                                                 major,
                                                                 minor))):
        return '', 409
    instance_counter.update([config_name])
    instance_name = '{}_{}'.format(config_name, instance_counter[config_name])
    res = {
        'instance': instance_name,
        'name': config_name,
        'major': major,
        'minor': minor,
    }
    instances[instance_name] = res
    instance_dir = osp.join(container_dir, instance_name)
    os.makedirs(instance_dir)
    os.system('tar -zxf base_images/basefs.tar.gz -C {}'.format(instance_dir))
    image_dir = osp.join(instance_dir, 'basefs')
    with open(osp.join(config_dir, '{}-{}-{}.cfg'.format(config_name,
                                                         major,
                                                         minor))) as fp:
        config_obj = json.load(fp)

    subprocess = Process(target=start_container, args=(image_dir, config_obj))
    subprocess_dict[instance_name] = subprocess
    subprocess.start()
    return res, 200


@app.route('/list', methods=['GET'])
def list_instances():
    res = {
        'instances': list(instances.values())
    }
    return res, 200


@app.route('/destroy/<instance_name>', methods=['DELETE'])
def destroy_a_running_instance(instance_name):
    print(instance_name)
    if instance_name not in instances:
        return "", 404

    del instances[instance_name]
    return "", 200


@app.route('/destroyall', methods=['DELETE'])
def destroy_all():
    instances.clear()
    return "", 200


def create_dir_if_not_exists(dir_path):
    if not osp.exists(dir_path):
        os.makedirs(dir_path)


def start_container(image_dir, config_obj):
    os.chroot(image_dir)
    os.chdir('/')
    os.system('export {}'.format(config_obj['startup_env']))


if __name__ == '__main__':
    os.chdir(root_dir)
    create_dir_if_not_exists(config_dir)
    create_dir_if_not_exists(container_dir)
    app.run(host='localhost', port=8080)
