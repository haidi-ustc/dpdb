#/usr/bin/env python
# coding: utf-8
# Copyright (c) The Dpmodeling Team.

import os
import json
from elasticsearch_dsl import Search, Q
from elasticsearch import Elasticsearch
from monty.serialization import loadfn,dumpfn 

# Constants for keys
HOST_KEY = "host"
PORT_KEY = "port"
INDEX_NAME = "index_name"
INDEX_TYPE = "index_type"
USER_KEY = "user"
PASS_KEY = "password"
PATH_KEY = "path"

class ConfigurationFileError(Exception):
    def __init__(self, filename, err):
        msg = "reading '{}': {}".format(filename, err)
        Exception.__init__(self, msg)

class DBConfig:
    """Database configuration.
    """

    DEFAULT_PORT = 9200
    DEFAULT_FILE = 'db.yaml'
    ALL_SETTINGS = [
        HOST_KEY,
        PORT_KEY,
        INDEX_NAME,
        INDEX_TYPE,
    ]
    DEFAULT_SETTINGS = [
        (HOST_KEY, "localhost"),
        (PORT_KEY, DEFAULT_PORT),
        (INDEX_NAME, "dpm"),
        (INDEX_TYPE, "vasp"),
        (USER_KEY, None),
        (PASS_KEY, None), 
        (PATH_KEY, ""),
    ]


    def __init__(self, config_file=None, config_dict=None):
        self._cfg = dict(self.DEFAULT_SETTINGS)
        settings = {}
        if config_dict:
            settings = config_dict.copy()
        else:
            # Try to use DEFAULT_FILE if no config_file
            if config_file is None:
                if os.path.exists(self.DEFAULT_FILE):
                    config_file = self.DEFAULT_FILE
            # If there was a config_file, parse it
            if config_file is not None:
                try:
                    settings = get_settings(config_file)
                except Exception as err:
                    path = _as_file(config_file).name
                    raise ConfigurationFileError(path, err)
        self._cfg.update(settings)


    def __str__(self):
        return str(self._cfg)

    def copy(self):
        """Return a copy of self (internal settings are copied).
        """
        return DBConfig(config_dict=self._cfg.copy())

    @property
    def settings(self):
        return self._cfg
 
    def save_settings(self):
        dumpfn(self._cfg,'db.yaml')

    @property
    def host(self):
        return self._cfg.get(HOST_KEY, None)

    @property
    def port(self):
        return self._cfg.get(PORT_KEY, self.DEFAULT_PORT)

    @property
    def dbname(self):
        """Name of the database."""
        return self._cfg.get(INDEX_NAME, None)

    @dbname.setter
    def dbname(self, value):
        self._cfg[DB_KEY] = value

    @property
    def doc_type(self):
        return self._cfg.get(INDEX_TYPE, None)

    @doc_type.setter
    def doc_type(self, value):
        self._cfg[INDEX_TYPE] = value

    @property
    def user(self):
        return self._cfg.get(USER_KEY, None)

    @property
    def password(self):
        return self._cfg.get(PASS_KEY, None)

def get_settings(config_file):
    cfg = loadfn(config_file)
    return cfg


def get_database(d, **kwargs):
    if d['user'] and d['password']: 
       es=Elasticsearch([d['host']],
                        http_auth=(d['user'], d['password']),
                        port=d['pord'])
    else:
       es = Elasticsearch([d['host']])
    return es

def _as_file(f, mode='r'):
    if isinstance(f, str):
        return open(f, mode)
    return f
                   
