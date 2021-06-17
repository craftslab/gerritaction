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
        config.gerrit_action = 0
    except ConfigException as _:
        assert True
    else:
        assert False

    try:
        config.gerrit_action = ""
    except ConfigException as _:
        assert True
    else:
        assert False

    try:
        config.gerrit_action = (
            "delete-reviewer:{account-id,...},remove-attention:{account-id,...})"
        )
    except ConfigException as _:
        assert False
    else:
        assert True

    try:
        config.gerrit_query = 0
    except ConfigException as _:
        assert True
    else:
        assert False

    try:
        config.gerrit_query = ""
    except ConfigException as _:
        assert True
    else:
        assert False

    try:
        config.gerrit_query = "gerrit query (since:2021-01-01 until:2021-01-02)"
    except ConfigException as _:
        assert False
    else:
        assert True
