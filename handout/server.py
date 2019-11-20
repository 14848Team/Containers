"""
Author:
    Can Xia (canx)
    Chi Zhang (czhang5)

Implement several manipulations in container manager, including
 creating configuration file, listing existing configuration files, launching a
 instance, listing running instance, destroying a instance, and
 destroying all instances

This server basally use Flask as the http server to listen on http
request. The command "make manager" can run this server.
"""

from flask import Flask, request
import os
import os.path as osp
import json
import copy
import time
from collections import Counter, OrderedDict
from multiprocessing import Process

import signal

app = Flask(__name__)

root_dir = osp.dirname(osp.realpath(__file__))
config_dir = osp.join(root_dir, 'configs')
container_dir = osp.join(root_dir, 'containers')
instance_counter = Counter()
instances = OrderedDict()
container_dict = {}


@app.route('/config', methods=['POST'])
def create_config_file():
    """
    Create a configuration file
    """
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
        unlock(config_path)
        return '', 200
    else:
        return '', 409


@app.route('/cfginfo', methods=['GET'])
def list_config_files():
    """
    List all configuration files
    """
    res = {
        'files': sorted(os.listdir(config_dir))
    }
    return res, 200


@app.route('/launch', methods=['POST'])
def launch_container():
    """
    Launch a container
    """
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
    # Create floder
    instance_dir = osp.join(container_dir, instance_name)
    os.makedirs(instance_dir)
    unlock(instance_dir)
    # Untar the basic image
    os.system('tar -zxf base_images/basefs.tar.gz -C {}'.format(instance_dir))
    image_dir = osp.join(instance_dir, 'basefs')
    with open(osp.join(config_dir, '{}-{}-{}.cfg'.format(config_name,
                                                         major,
                                                         minor))) as fp:
        config_obj = json.load(fp)
    # Mount
    for mount_argv in config_obj['mounts']:
        execute_mount(mount_argv, image_dir)
    os.system('mount -t proc proc {}'.format(osp.join(image_dir, 'proc')))
    # Create child process and start instance
    container_process = Process(target=start_container, args=(image_dir, config_obj))
    container_dict[instance_name] = container_process
    container_process.start()
    # Set group id
    os.setpgid(container_process.pid, container_process.pid)
    time.sleep(3)
    return res, 200


@app.route('/list', methods=['GET'])
def list_instances():
    res = {
        'instances': list(instances.values())
    }
    return res, 200


@app.route('/destroy/<instance_name>', methods=['DELETE'])
def destroy_a_running_instance(instance_name):
    """
    Given a running container instance's name, destroy it.
    :param instance_name: the running instance's name
    :return: nothing in response body, if there is no instance matches the given name,
            response status code is 404, else 200
    """
    print('destroy {}'.format(instance_name))
    if instance_name not in instances:
        return "", 404
    teardown_container(instance_name)
    return "", 200


@app.route('/destroyall', methods=['DELETE'])
def destroy_all():
    """
    destroy all running container instances
    :return: a http response body with empty body and 200 status code
    """
    instance_names = copy.copy(list(instances.keys()))
    for instance_name in instance_names:
        teardown_container(instance_name)
    return "", 200


@app.route('/ps', methods=['GET'])
def ps():
    """
    helper function, list all subprocesses' pid created for containers
    :return: a http response body with body contains all a dict listing
                all running instances' names and their pid
    """
    return {instance_name: container_dict[instance_name].pid
            for instance_name in container_dict}, 200


def teardown_container(instance_name):
    """
    do the cleanup job for destroy a container instance
    :param instance_name: the name of destroyed container instance
    :return: None
    """
    image_dir = osp.join(container_dir, instance_name, 'basefs')
    instance_info = instances.pop(instance_name)
    container_process = container_dict.pop(instance_name)
    # kill the whole group of container process
    os.killpg(container_process.pid, signal.SIGKILL)

    with open(osp.join(config_dir, '{}-{}-{}.cfg'.format(instance_info['name'],
                                                         instance_info['major'],
                                                         instance_info['minor']))) as fp:
        config_obj = json.load(fp)
    # umount all mounted files
    mount_paths = [mount_config.split(' ')[1] for mount_config in config_obj['mounts']]
    mount_paths.sort()
    mount_paths.reverse()
    for mount_path in mount_paths:
        if mount_path[0] == '/':
            mount_path = mount_path[1:]
        mount_path = osp.join(image_dir, mount_path)
        os.system('umount -l {}'.format(mount_path))
    # umount proc
    os.system('chroot {} /bin/bash -c "umount proc"'.format(image_dir))
    # remove container directory
    os.system('rm -rf {}'.format(osp.join(container_dir, instance_name)))


def create_dir_if_not_exists(dir_path):
    """
    create a directory if not exists
    :param dir_path: the directory path
    :return: None
    """
    if not osp.exists(dir_path):
        os.makedirs(dir_path)
    unlock(dir_path)


def unlock(path):
    """
    Make a file or directory accessible to all users
    :param path: the path of the unlocked file or directory
    :return: None
    """
    os.system('sudo chmod 777 {}'.format(path))


def start_container(image_dir, config_obj):
    """
    The container subprocess
    :param image_dir: container's image directory
    :param config_obj: config object
    :return: None
    """
    startup_env = config_obj['startup_env']
    if startup_env[-1] != ';':
        startup_env = startup_env + ';'
    os.system('unshare -p -f --mount-proc={} chroot {} /bin/bash -c "export {} {}"'.format(osp.join(image_dir, 'proc'),
                                                                                           image_dir, startup_env,
                                                                                           config_obj[
                                                                                               'startup_script']))


def execute_mount(mount_argv, image_dir):
    """
    Mount files to the container image directory
    :param mount_argv: all mount config arguments
    :param image_dir: the path of container image directory
    :return: None
    """
    filename = mount_argv.split(" ")[0]
    file_folder = filename.split(".")[0]
    folder = mount_argv.split(" ")[1]
    if folder[0] == '/':
        folder = folder[1:]
    access = mount_argv.split(" ")[2]
    mountables_path = osp.join(os.getcwd(), "mountables")
    file_path = osp.join(mountables_path, filename)
    file_folder = osp.join(mountables_path, file_folder)
    folder_path = osp.join(image_dir, folder)
    if not osp.exists(folder_path):
        os.system('sudo mkdir {}'.format(folder_path))
    if not osp.exists(file_folder):
        os.system('tar -xf {} -C {}'.format(file_path, mountables_path))
    if access == "READ":
        os.system('sudo mount --bind -o ro {} {}'.format(file_folder, folder_path))
    else:
        os.system('sudo mount --bind -o rw {} {}'.format(file_folder, folder_path))


if __name__ == '__main__':
    os.chdir(root_dir)
    os.system('make clean')
    create_dir_if_not_exists(config_dir)
    create_dir_if_not_exists(container_dir)
    app.run(host='localhost', port=8080)
