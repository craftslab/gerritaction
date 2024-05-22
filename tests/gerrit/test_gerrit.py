# -*- coding: utf-8 -*-

from gerritaction.gerrit.gerrit import Gerrit, GerritException


def test_exception():
    exception = GerritException("exception")
    assert str(exception) == "exception"


def test_gerrit():
    config = {
        "gerrit": {
            "host": "http://127.0.0.1",
            "port": "8080",
            "user": "admin",
            "pass": "D/uccEPCcItsY3Cti4unrkS/zsyW65MZBrEsiHiXpg",
        }
    }

    gerrit = Gerrit(config)
    assert gerrit is not None

    change = gerrit.query_change("change:41", 0)
    assert change is not None and len(change) == 1

    buf = gerrit.get_detail(change[0])
    assert buf is not None

    buf = gerrit.add_reviewer(change[0], "admin")
    assert buf is not None

    buf = gerrit.delete_reviewer(change[0], "admin")
    assert buf is not None

    buf = gerrit.add_attention(change[0], "admin")
    assert buf is not None

    buf = gerrit.remove_attention(change[0], "admin")
    assert buf is not None
