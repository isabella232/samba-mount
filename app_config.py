#!/usr/bin/env python
# _*_ coding:utf-8 _*_
"""
Project-wide application configuration.

DO NOT STORE SECRETS, PASSWORDS, ETC. IN THIS FILE.
They will be exposed to users. Use environment variables instead.
See get_secrets() below for a fast way to access them.
"""

import logging
import os

PROJECT_SLUG = 'samba_mount'

"""
Logging
"""
LOG_FORMAT = '%(levelname)s:%(name)s:%(asctime)s: %(message)s'


def get_secrets():
    """
    A method for accessing our secrets.
    """
    secrets_dict = {}

    for k, v in os.environ.items():
        if k.startswith(PROJECT_SLUG):
            k = k[len(PROJECT_SLUG) + 1:]
            secrets_dict[k] = v

    return secrets_dict
