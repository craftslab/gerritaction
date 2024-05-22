# -*- coding: utf-8 -*-

import os

from gerritaction.config.config import Config, ConfigException


def test_exception():
    exception = ConfigException("exception")
    assert str(exception) == "exception"


def test_config():
    config = Config()

    try:
        config.config_file = 0
    except ConfigException as _:
        assert True
    else:
        assert False

    try:
        config.config_file = ""
    except ConfigException as _:
        assert True
    else:
        assert False

    try:
        config.config_file = "config.json"
    except ConfigException as _:
        assert True
    else:
        assert False

    try:
        config.config_file = "foo.yml"
    except ConfigException as _:
        assert True
    else:
        assert False

    try:
        config.config_file = os.path.join(
            os.path.dirname(__file__), "../data/config.yml".replace("/", os.path.sep)
        )
    except ConfigException as _:
        assert False
    else:
        assert True

    try:
        config.account_query = 0
    except ConfigException as _:
        assert True
    else:
        assert False

    try:
        config.account_query = ""
    except ConfigException as _:
        assert True
    else:
        assert False

    try:
        config.account_query = ("account query (name:john email:example.com)",)
    except ConfigException as _:
        assert False
    else:
        assert True

    try:
        config.change_query = 0
    except ConfigException as _:
        assert True
    else:
        assert False

    try:
        config.change_query = ""
    except ConfigException as _:
        assert True
    else:
        assert False

    try:
        config.change_query = "change query (since:2024-01-01 until:2024-01-02)"
    except ConfigException as _:
        assert False
    else:
        assert True

    try:
        config.change_action = 0
    except ConfigException as _:
        assert True
    else:
        assert False

    try:
        config.change_action = ""
    except ConfigException as _:
        assert True
    else:
        assert False

    try:
        config.change_action = (
            "delete-reviewer:{account-id,...},remove-attention:{account-id,...})"
        )
    except ConfigException as _:
        assert False
    else:
        assert True

    try:
        config.group_query = 0
    except ConfigException as _:
        assert True
    else:
        assert False

    try:
        config.group_query = ""
    except ConfigException as _:
        assert True
    else:
        assert False

    try:
        config.group_query = ("group query (name:admin member:john)",)
    except ConfigException as _:
        assert False
    else:
        assert True

    try:
        config.project_query = 0
    except ConfigException as _:
        assert True
    else:
        assert False

    try:
        config.project_query = ""
    except ConfigException as _:
        assert True
    else:
        assert False

    try:
        config.project_query = ("project query (name:test state:active)",)
    except ConfigException as _:
        assert False
    else:
        assert True
