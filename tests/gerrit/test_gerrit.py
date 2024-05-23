# -*- coding: utf-8 -*-

import json
import os
import yaml

from gerritaction.gerrit.gerrit import Gerrit, GerritException


def test_exception():
    exception = GerritException("exception")
    assert str(exception) == "exception"


def test_gerrit():
    account_name = "admin"
    change_number = 1
    group_name = "Administrators"
    project_name = "test"

    name = os.path.join(
        os.path.dirname(__file__), "../data/config.yml".replace("/", os.path.sep)
    )

    config = yaml.load(name)

    gerrit = Gerrit(config["spec"]["gerrit"])
    assert gerrit is not None

    account = gerrit.query_account("name:" + account_name, 0)
    assert account is not None

    print(json.dumps(account))

    change = gerrit.query_change("change:" + str(change_number), 0)
    assert change is not None

    print(json.dumps(change))

    sshkey = gerrit.get_sshkey(account[0])
    assert sshkey is not None

    print(json.dumps(sshkey))

    detail = gerrit.get_detail(change[0])
    assert detail is not None

    print(json.dumps(detail))

    ret = gerrit.add_reviewer(change[0], account_name)
    assert ret is not None

    ret = gerrit.delete_reviewer(change[0], account_name)
    assert ret is not None

    ret = gerrit.add_attention(change[0], account_name)
    assert ret is not None

    ret = gerrit.remove_attention(change[0], account_name)
    assert ret is not None

    group = gerrit.query_group("name:" + group_name, 0)
    assert group is not None

    print(json.dumps(group))

    project = gerrit.query_project("name:" + project_name, 0)
    assert project is not None

    print(json.dumps(project))
