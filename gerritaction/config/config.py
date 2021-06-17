# -*- coding: utf-8 -*-

import os
import yaml


class ConfigFile:
    APIVERSION = "apiVersion"
    KIND = "kind"
    METADATA = "metadata"
    SPEC = "spec"


class MetaData:
    NAME = "name"


class ConfigException(Exception):
    def __init__(self, info):
        super().__init__(self)
        self._info = info

    def __str__(self):
        return self._info


class Config(object):
    def __init__(self):
        self._config_file = None
        self._gerrit_action = None
        self._gerrit_query = None

    @property
    def config_file(self):
        return self._config_file

    @config_file.setter
    def config_file(self, name):
        if not isinstance(name, str) or len(name.strip()) == 0:
            raise ConfigException("config invalid")
        name = name.strip()
        if not name.endswith(".yml") and not name.endswith(".yaml"):
            raise ConfigException("suffix invalid")
        if not os.path.exists(name):
            raise ConfigException("%s not found" % name)
        with open(name) as file:
            self._config_file = yaml.load(file, Loader=yaml.FullLoader)
        if self._config_file is None:
            raise ConfigException("config invalid")

    @property
    def gerrit_action(self):
        return self._gerrit_action

    @gerrit_action.setter
    def gerrit_action(self, data):
        if not isinstance(data, str) or len(data.strip()) == 0:
            raise ConfigException("action invalid")
        self._gerrit_action = data.strip()

    @property
    def gerrit_query(self):
        return self._gerrit_query

    @gerrit_query.setter
    def gerrit_query(self, data):
        if not isinstance(data, str) or len(data.strip()) == 0:
            raise ConfigException("query invalid")
        self._gerrit_query = data.strip()
