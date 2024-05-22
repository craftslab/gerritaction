# -*- coding: utf-8 -*-

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
        self._account = None
        self._change = None
        self._group = None
        self._project = None

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
        self._account = self._gerrit.query_account(
            search=self._config.account_query, start=0
        )
        if self._account is None:
            raise ActionException("account invalid")

    def _run_change_query(self):
        self._change = self._gerrit.query_change(
            search=self._config.change_query, start=0
        )
        if self._change is None:
            raise ActionException("change invalid")

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
        self._group = self._gerrit.query_group(search=self._config.group_query, start=0)
        if self._group is None:
            raise ActionException("group invalid")

    def _run_project_query(self):
        self._project = self._gerrit.query_project(
            search=self._config.project_query, start=0
        )
        if self._project is None:
            raise ActionException("project invalid")

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
