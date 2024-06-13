# -*- coding: utf-8 -*-

import json

from ..gerrit.gerrit import Gerrit
from ..proto.proto import Change, Separator

from gerritaction.config.config import ConfigFile


class ActionException(Exception):
    def __init__(self, info):
        super().__init__(self)
        self._info = info

    def __str__(self):
        return self._info


class Action(object):
    def __init__(self, config=None):
        if config is None or config.config_file.get(ConfigFile.SPEC, None) is None:
            raise ActionException("config invalid")
        self._config = config
        self._gerrit = Gerrit(self._config.config_file[ConfigFile.SPEC])
        self._change = None
        self._output = config.output_file

    def run(self):
        if self._config.account_query is not None:
            self._run_account_query()
        if self._config.change_query is not None:
            self._run_change_query()
        if self._config.change_action is not None:
            self._run_change_action()
        if self._config.group_query is not None:
            self._run_group_query()
        if self._config.project_query is not None:
            self._run_project_query()

    def _run_account_query(self):
        account = self._gerrit.query_account(search=self._config.account_query, start=0)
        if account is None:
            raise ActionException("account invalid")
        if self._output is None:
            print(json.dumps(account))
        else:
            with open(self._output, "w", encoding="utf-8") as f:
                json.dump(account, f, ensure_ascii=False, indent=4)

    def _run_change_query(self):
        self._change = self._gerrit.query_change(
            search=self._config.change_query, start=0
        )
        if self._change is None:
            raise ActionException("change invalid")
        if self._output is None:
            print(json.dumps(self._change))
        else:
            with open(self._output, "w", encoding="utf-8") as f:
                json.dump(self._change, f, ensure_ascii=False, indent=4)

    def _run_change_action(self):
        for item in self._config.change_action.split(Separator.GROUP):
            if len(item.split(Separator.ACTION)) > 2:
                raise ActionException("action invalid")
            if Change.DELETE_CHANGE in item:
                self._delete_change()
                continue
            if Change.SUBMIT_CHANGE in item:
                self._submit_change()
                continue
            action, content = item.split(Separator.ACTION)
            if action == Change.ADD_REVIEWER:
                self._add_reviewer(content.split(Separator.CONTENT))
            elif action == Change.DELETE_REVIEWER:
                self._delete_reviewer(content.split(Separator.CONTENT))
            elif action == Change.ADD_ATTENTION:
                self._add_attention(content.split(Separator.CONTENT))
            elif action == Change.REMOVE_ATTENTION:
                self._remove_attention(content.split(Separator.CONTENT))
            elif action == Change.APPROVE_CHANGE:
                self._approve_change(content.split(Separator.CONTENT))
            else:
                raise ActionException("action invalid")

    def _run_group_query(self):
        group = self._gerrit.query_group(search=self._config.group_query, start=0)
        if group is None:
            raise ActionException("group invalid")
        if self._output is None:
            print(json.dumps(group))
        else:
            with open(self._output, "w", encoding="utf-8") as f:
                json.dump(group, f, ensure_ascii=False, indent=4)

    def _run_project_query(self):
        def _config(data):
            for index in range(len(data)):
                data[index]["config"] = self._gerrit.get_config(data[index]["name"])
            return data

        def _branches(data):
            for index in range(len(data)):
                data[index]["branches"] = self._gerrit.get_branches(data[index]["name"])
            return data

        def _tags(data):
            for index in range(len(data)):
                data[index]["tags"] = self._gerrit.get_tags(data[index]["name"])
            return data

        project = self._gerrit.query_project(search=self._config.project_query, start=0)
        if project is None:
            raise ActionException("project invalid")
        project = _config(project)
        project = _branches(project)
        project = _tags(project)
        if self._output is None:
            print(json.dumps(project))
        else:
            with open(self._output, "w", encoding="utf-8") as f:
                json.dump(project, f, ensure_ascii=False, indent=4)

    def _add_reviewer(self, accounts):
        for account in accounts:
            for change in self._change:
                _ = self._gerrit.add_reviewer(change, account)

    def _delete_reviewer(self, accounts):
        for account in accounts:
            for change in self._change:
                _ = self._gerrit.delete_reviewer(change, account)

    def _add_attention(self, accounts):
        for account in accounts:
            for change in self._change:
                _ = self._gerrit.add_attention(change, account)

    def _remove_attention(self, accounts):
        for account in accounts:
            for change in self._change:
                _ = self._gerrit.remove_attention(change, account)

    def _approve_change(self, labels):
        for change in self._change:
            _ = self._gerrit.approve_change(change, labels)

    def _submit_change(self):
        for change in self._change:
            _ = self._gerrit.submit_change(change)

    def _delete_change(self):
        for change in self._change:
            _ = self._gerrit.delete_change(change)
