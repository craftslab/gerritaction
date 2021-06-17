# -*- coding: utf-8 -*-

from gerritaction.cmd.banner import BANNER


def test_banner():
    assert BANNER is not None and len(BANNER) != 0
