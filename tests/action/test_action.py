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

    action = Action(config)
    assert action is not None
