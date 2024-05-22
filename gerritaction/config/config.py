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
        self._account_query = None
        self._change_query = None
        self._change_action = None
        self._group_query = None
        self._project_query = None

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
    def account_query(self):
        return self._account_query

    @account_query.setter
    def account_query(self, data):
        if not isinstance(data, str) or len(data.strip()) == 0:
            raise ConfigException("query invalid")
        self._account_query = data.strip()

    @property
    def change_query(self):
        return self._change_query

    @change_query.setter
    def change_query(self, data):
        if not isinstance(data, str) or len(data.strip()) == 0:
            raise ConfigException("query invalid")
        self._change_query = data.strip()

    @property
    def change_action(self):
        return self._change_action

    @change_action.setter
    def change_action(self, data):
        if not isinstance(data, str) or len(data.strip()) == 0:
            raise ConfigException("action invalid")
        self._change_action = data.strip()

    @property
    def group_query(self):
        return self._group_query

    @group_query.setter
    def group_query(self, data):
        if not isinstance(data, str) or len(data.strip()) == 0:
            raise ConfigException("query invalid")
        self._group_query = data.strip()

    @property
    def project_query(self):
        return self._project_query

    @project_query.setter
    def project_query(self, data):
        if not isinstance(data, str) or len(data.strip()) == 0:
            raise ConfigException("query invalid")
        self._project_query = data.strip()
