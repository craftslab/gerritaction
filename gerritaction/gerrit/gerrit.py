# -*- coding: utf-8 -*-

import json
import requests

from ..proto.proto import Separator

from gerritaction.logger.logger import Logger


class GerritException(Exception):
    def __init__(self, info):
        super().__init__(self)
        self._info = info

    def __str__(self):
        return self._info


class Gerrit(object):
    _QUERY_LIMIT = 1000

    def __init__(self, config):
        if config is None or config.get("gerrit", None) is None:
            raise GerritException("config invalid")
        self._config = config["gerrit"]
        self._host = str(self._config.get("host", "http://127.0.0.1"))
        self._port = str(self._config.get("port", 8080))
        self._user = str(self._config.get("user", ""))
        self._pass = str(self._config.get("pass", ""))
        self._query = self._config.get("query", {"option": ["CURRENT_REVISION"]})
        if len(self._pass) != 0 and len(self._user) != 0:
            self._url = self._host + ":" + self._port + "/a"
        else:
            self._url = self._host + ":" + self._port

    def query_changes(self, search, start):
        def _helper(search, start):
            payload = {
                "o": self._query["option"],
                "q": search,
                "start": start,
                "n": self._QUERY_LIMIT,
            }
            if len(self._pass) != 0 and len(self._user) != 0:
                response = requests.get(
                    url=self._url + "/changes/",
                    auth=(self._user, self._pass),
                    params=payload,
                )
            else:
                response = requests.get(url=self._url + "/changes/", params=payload)
            if response.status_code != requests.codes.ok:
                Logger.error("failed to query change with search %s" % search)
                return None
            return json.loads(response.text.replace(")]}'", ""))

        buf = _helper(search, start)
        if buf is None or len(buf) == 0:
            return []
        if buf[-1].get("_more_changes", False) is False:
            return buf
        buf.extend(self.query_changes(search, start + len(buf)))
        return buf

    def get_detail(self, change):
        if len(self._pass) != 0 and len(self._user) != 0:
            response = requests.get(
                url=self._url + "/changes/" + str(change["_number"]) + "/detail",
                auth=(self._user, self._pass),
            )
        else:
            response = requests.get(
                url=self._url + "/changes/" + str(change["_number"]) + "/detail"
            )
        if response.status_code != requests.codes.ok:
            Logger.error("failed to get detail for change %s" % change["_number"])
            return None
        return json.loads(response.text.replace(")]}'", ""))

    def add_reviewer(self, change, account):
        args = {"reviewer": account}
        if len(self._pass) != 0 and len(self._user) != 0:
            response = requests.post(
                url=self._url + "/changes/" + str(change["_number"]) + "/reviewers",
                auth=(self._user, self._pass),
                json=args,
            )
        else:
            response = requests.post(
                url=self._url + "/changes/" + str(change["_number"]) + "/reviewers",
                json=args,
            )
        if response.status_code != requests.codes.ok:
            Logger.error(
                "failed to add reviewer %s to change %s" % (account, change["_number"])
            )
            return None
        return json.loads(response.text.replace(")]}'", ""))

    def delete_reviewer(self, change, account):
        if len(self._pass) != 0 and len(self._user) != 0:
            response = requests.delete(
                url=self._url
                + "/changes/"
                + str(change["_number"])
                + "/reviewers/"
                + str(account),
                auth=(self._user, self._pass),
            )
        else:
            response = requests.delete(
                url=self._url
                + "/changes/"
                + str(change["_number"])
                + "/reviewers/"
                + str(account)
            )
        if (
            response.status_code != requests.codes.ok
            and response.status_code != requests.codes.no_content
        ):
            Logger.error(
                "failed to delete reviewer %s from change %s"
                % (account, change["_number"])
            )
            return None
        return json.loads("{}")

    def add_attention(self, change, account):
        args = {"user": account, "reason": "attention"}
        if len(self._pass) != 0 and len(self._user) != 0:
            response = requests.post(
                url=self._url + "/changes/" + str(change["_number"]) + "/attention",
                auth=(self._user, self._pass),
                json=args,
            )
        else:
            response = requests.post(
                url=self._url + "/changes/" + str(change["_number"]) + "/attention",
                json=args,
            )
        if response.status_code != requests.codes.ok:
            Logger.error(
                "failed to add attention %s to change %s" % (account, change["_number"])
            )
            return None
        return json.loads(response.text.replace(")]}'", ""))

    def remove_attention(self, change, account):
        args = {"reason": "ignore"}
        if len(self._pass) != 0 and len(self._user) != 0:
            response = requests.delete(
                url=self._url
                + "/changes/"
                + str(change["_number"])
                + "/attention/"
                + str(account),
                auth=(self._user, self._pass),
                json=args,
            )
        else:
            response = requests.delete(
                url=self._url
                + "/changes/"
                + str(change["_number"])
                + "/attention/"
                + str(account),
                json=args,
            )
        if (
            response.status_code != requests.codes.ok
            and response.status_code != requests.codes.no_content
        ):
            Logger.error(
                "failed to remove attention %s from change %s"
                % (account, change["_number"])
            )
            return None
        return json.loads("{}")

    def approve_change(self, change, labels):
        def _helper(labels):
            buf = {}
            for item in labels:
                key, val = item.split(Separator.LABEL)
                buf[key] = int(val)
            return buf

        args = {
            "comments": {},
            "labels": _helper(labels),
            "message": "Approved by %s" % self._user,
            "tag": "",
        }
        if len(self._pass) != 0 and len(self._user) != 0:
            response = requests.post(
                url=self._url
                + "/changes/"
                + str(change["_number"])
                + "/revisions/"
                + str(change["current_revision"])
                + "/review",
                auth=(self._user, self._pass),
                json=args,
            )
        else:
            response = requests.post(
                url=self._url
                + "/changes/"
                + str(change["_number"])
                + "/revisions/"
                + str(change["current_revision"])
                + "/review",
                json=args,
            )
        if response.status_code != requests.codes.ok:
            Logger.error(
                "failed to approve change %s by account %s"
                % (change["_number"], self._user)
            )
            return None
        return json.loads(response.text.replace(")]}'", ""))

    def submit_change(self, change):
        if len(self._pass) != 0 and len(self._user) != 0:
            response = requests.post(
                url=self._url
                + "/changes/"
                + str(change["_number"])
                + "/revisions/"
                + str(change["current_revision"])
                + "/submit",
                auth=(self._user, self._pass),
                json=None,
            )
        else:
            response = requests.post(
                url=self._url
                + "/changes/"
                + str(change["_number"])
                + "/revisions/"
                + str(change["current_revision"])
                + "/submit",
                json=None,
            )
        if response.status_code != requests.codes.ok:
            Logger.error(
                "failed to submit change %s by account %s"
                % (change["_number"], self._user)
            )
            return None
        return json.loads(response.text.replace(")]}'", ""))
