# -*- coding: utf-8 -*-

from ..gerrit.gerrit import Gerrit
from ..proto.proto import Proto, Separator

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
        self._changes = self._query_changes()
        if self._changes is None:
            raise ActionException("changes invalid")

    def _query_changes(self):
        return self._gerrit.query_changes(search=self._config.gerrit_query, start=0)

    def _add_reviewer(self, accounts):
        for account in accounts:
            for change in self._changes:
                _ = self._gerrit.add_reviewer(change, account)

    def _delete_reviewer(self, accounts):
        for account in accounts:
            for change in self._changes:
                _ = self._gerrit.delete_reviewer(change, account)

    def _add_attention(self, accounts):
        for account in accounts:
            for change in self._changes:
                _ = self._gerrit.add_attention(change, account)

    def _remove_attention(self, accounts):
        for account in accounts:
            for change in self._changes:
                _ = self._gerrit.remove_attention(change, account)

    def run(self):
        for item in self._config.gerrit_action.split(Separator.GROUP):
            if len(item.split(Separator.ACTION)) != 2:
                raise ActionException("action invalid")
            action, accounts = item.split(Separator.ACTION)
            if action == Proto.ADD_REVIEWER:
                self._add_reviewer(accounts.split(Separator.ACCOUNT))
            elif action == Proto.DELETE_REVIEWER:
                self._delete_reviewer(accounts.split(Separator.ACCOUNT))
            elif action == Proto.ADD_ATTENTION:
                self._add_attention(accounts.split(Separator.ACCOUNT))
            elif action == Proto.REMOVE_ATTENTION:
                self._remove_attention(accounts.split(Separator.ACCOUNT))
            else:
                raise ActionException("action invalid")
