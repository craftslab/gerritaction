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
        # TODO
        start = 0
        return self._gerrit.query_changes(search=self._config.gerrit_query, start=start)

    def _add_reviewer(self, accounts):
        for account in accounts:
            for change in self._changes:
                ret = self._gerrit.add_reviewer(change, account)
                if ret is None:
                    raise ActionException("failed to add reviewer")

    def _delete_reviewer(self, accounts):
        for account in accounts:
            for change in self._changes:
                ret = self._gerrit.delete_reviewer(change, account)
                if ret is None:
                    raise ActionException("failed to delete reviewer")

    def _add_attention(self, accounts):
        for account in accounts:
            for change in self._changes:
                ret = self._gerrit.add_attention(change, account)
                if ret is None:
                    raise ActionException("failed to add attention")

    def _remove_attention(self, accounts):
        for account in accounts:
            for change in self._changes:
                ret = self._gerrit.remove_attention(change, account)
                if ret is None:
                    raise ActionException("failed to remove attention")

    def run(self):
        for item in self._config.gerrit_action.split(Separator.GROUP):
            if len(item.split(Separator.ACTION)) != 2:
                raise ActionException("action invalid")
            action, accounts = item.split(Separator.ACTION)
            if action == Proto.DELETE_REVIEWER:
                self._delete_reviewer(accounts)
            elif action == Proto.REMOVE_ATTENTION:
                self._remove_attention(accounts)
            else:
                raise ActionException("action invalid")
