# -*- coding: utf-8 -*-

import json
import requests


class GerritException(Exception):
    def __init__(self, info):
        super().__init__(self)
        self._info = info

    def __str__(self):
        return self._info


class Gerrit(object):
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
        payload = {"o": self._query["option"], "q": search, "start": start}
        if len(self._pass) != 0 and len(self._user) != 0:
            response = requests.get(
                url=self._url + "/changes/",
                auth=(self._user, self._pass),
                params=payload,
            )
        else:
            response = requests.get(url=self._url + "/changes/", params=payload)
        if response.status_code != requests.codes.ok:
            return None
        return json.loads(response.text.replace(")]}'", ""))

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
            return None
        return json.loads("{}")
