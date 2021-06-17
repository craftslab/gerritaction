# -*- coding: utf-8 -*-

from gerritaction.cmd.argument import Argument


def test_argument():
    argument = Argument()
    assert argument is not None
