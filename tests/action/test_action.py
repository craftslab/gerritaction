# -*- coding: utf-8 -*-

import os

from gerritaction.action.action import Action, ActionException
from gerritaction.config.config import Config


def test_exception():
    exception = ActionException("exception")
    assert str(exception) == "exception"


def test_action():
    config = Config()
    config.config_file = os.path.join(
        os.path.dirname(__file__), "../data/config.yml".replace("/", os.path.sep)
    )
    config.gerrit_query = "change:41"

    action = Action(config)

    accounts = ["admin"]

    try:
        action._add_reviewer(accounts)
    except ActionException as _:
        assert False
    else:
        assert True

    try:
        action._delete_reviewer(accounts)
    except ActionException as _:
        assert False
    else:
        assert True

    try:
        action._add_attention(accounts)
    except ActionException as _:
        assert False
    else:
        assert True

    try:
        action._remove_attention(accounts)
    except ActionException as _:
        assert False
    else:
        assert True
