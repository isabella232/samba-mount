samba-mount
===========

* [What is this?](#what-is-this)
* [Assumptions](#assumptions)
* [What's in here?](#whats-in-here)
* [Bootstrap the project](#bootstrap-the-project)
* [Geocode unstructured data](#geocode-unstructured-data)
* [Geocode structured data](#geocode-structured-data)
* [Geocode mixed data](#geocode-mixed-data)
* [Advanced configuration](#advanced-configuration)

What is this?
-------------

Mount samba servers in local filesystem using [Fabric](http://www.fabfile.org/).

Assumptions
-----------

The following things are assumed to be true in this documentation.
* You are running OSX.
* You are using Python 2.7. (Probably the version that came OSX.)
* You have virtualenv and virtualenvwrapper installed and working.
* You have postgres installed and running

For more details on the technology stack used with the app-template, see our [development environment blog post](http://blog.apps.npr.org/2013/06/06/how-to-setup-a-developers-environment.html).

This code should work fine in most recent versions of Linux, but package installation and system dependencies may vary.

What's in here?
---------------

The project contains the following folders and important files:

* ``fabfile`` -- Fabric tasks
* ``requirements.txt`` -- Python requirements.

Bootstrap the project
---------------------

To bootstrap the project:

```
git clone git@github.com:nprapps/samba-mount.git
cd samba-mount
mkvirtualenv samba-mount
pip install -r requirements.txt
```

Mount samba server into local filesystem
----------------------------------------

In order to mount a samba server path into our local filesystem, execute:

```
fab mount:server=$SMB_SERVER,path=$SMB_PATH,mount_point=$LOCAL_PATH
```

Where:
* `$SMB_SERVER`: is your samba server
* `$SMB_PATH`: is the path to mount from the server (defaults to `www`)
* `$LOCAL_PATH`: is the local filesystem mount point (defaults to `mnt`)

_If you do not pass a samba server parameter, you can define it also as an environment variable named `samba_mount_DEFAULT_SERVER`

Copy files to mounted folder
----------------------------

In order to recursively copy files into the mounted folder, execute:

```
fab deploy:src_folder=$SRC_FOLDER,mount_point=$LOCAL_PATH
```

Where:
* `$SRC_FOLDER`: is the local path to the files you want to deploy
* `$LOCAL_PATH`: is the local filesystem mounted point (defaults to `mnt`)

If you do not want to include the source folder root in the deployment, you can pass an optional flag:

```
fab deploy:src_folder=$SRC_FOLDER,mount_point=$LOCAL_PATH,include_root=False
```

In that case all files and subfolder inside the root folder will be deployed directly on the mount point.


Unmount samba server from local filesystem
----------------------------------------

In order to unmount a samba server path from our local filesystem, execute:

```
fab umount:$LOCAL_PATH
```

If you have a long mount process and it is taking too much time and you want to narrow down the mount path, you can force unmount like this:

```
fab umount:$LOCAL_PATH,force=True
```

Where:
* `$LOCAL_PATH`: is the local filesystem mounted point (defaults to `mnt`)

