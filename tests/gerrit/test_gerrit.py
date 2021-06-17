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
            "query": {"option": ["CURRENT_REVISION"]},
        }
    }

    gerrit = Gerrit(config)
    assert gerrit is not None

    changes = gerrit.query_changes("change:41", 0)
    assert changes is not None and len(changes) == 1

    buf = gerrit.get_detail(changes[0])
    assert buf is not None

    buf = gerrit.add_reviewer(changes[0], "admin")
    assert buf is not None

    buf = gerrit.delete_reviewer(changes[0], "admin")
    assert buf is not None

    buf = gerrit.add_attention(changes[0], "admin")
    assert buf is not None

    buf = gerrit.remove_attention(changes[0], "admin")
    assert buf is not None
