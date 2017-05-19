#!/usr/bin/env python
# coding: utf-8
from __future__ import with_statement
from fabric.api import task, prompt, local, lcd, settings
import os
from termcolor import colored
from utils import confirm, prep_bool_arg
import logging
import app_config

LOG_FORMAT = '%(levelname)s:%(name)s:%(asctime)s: %(message)s'
LOG_LEVEL = logging.INFO
logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
# LOCAL PATHS
cwd = os.path.dirname(__file__)
SMB_MOUNT_TEMPLATE = 'mount -t smbfs //%s/%s %s'


@task
def mount(server=None, path='www', mount_point='mnt'):
    '''mount especiales server into local disk'''
    local_path = os.path.join(cwd, '..', mount_point)
    if os.path.exists(local_path):
        if os.listdir(local_path):
            logger.error('Mount point is not empty, choose other mount point')
            exit(1)
    else:
        os.makedirs(local_path)
    if not server:
        secrets = app_config.get_secrets()
        server = secrets.get('DEFAULT_SERVER',
                             app_config.PROJECT_SLUG)
    command = SMB_MOUNT_TEMPLATE % (server, path, local_path)
    local(command)
    return local_path


@task
def umount(mount_point='mnt', force=False):
    force = prep_bool_arg(force)
    with lcd(os.path.join(cwd, '..')):
        with settings(warn_only=True):
            if force:
                local('diskutil unmount force %s' % mount_point)
            else:
                local('umount %s' % mount_point)


@task
def deploy(src_folder=None, mount_point='mnt', include_root=True):
    '''deploy files recursively to mounted point'''
    # Parse boolean fabric args
    include_root = prep_bool_arg(include_root)
    src_path = os.path.abspath(os.path.join(cwd, '..', src_folder))
    if not os.path.exists(src_path):
        logger.error('Could not find %s' % src_path)
        exit(1)

    mount_path = os.path.join(cwd, '..', mount_point)

    # Create root source folder
    if not include_root:
        src_path += '%s*' % (os.path.sep)

    src_root_folder = src_path.split(os.path.sep)[-1]
    mount_root_path = os.path.join(mount_path, src_root_folder)
    if os.path.exists(mount_root_path):
        confirm(colored('The source folder exists on the mounted point. Existing files will be overwritten. continue?', 'red'))

    local('cp -v -r %s %s'
          % (src_path, mount_path))

    logger.info("Please don't forget to unmount the server when you are done. 'fab umount'")


# DEFAULT TASK
@task(default=True)
def default():
    '''list all fabric tasks'''
    local('fab --list')
