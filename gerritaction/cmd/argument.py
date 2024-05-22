# -*- coding: utf-8 -*-

import argparse

from gerritaction.__version__ import __version__


class Argument(object):
    def __init__(self):
        self._parser = argparse.ArgumentParser(description="Gerrit Action")
        self._add()

    def _add(self):
        self._parser.add_argument(
            "--config-file",
            action="store",
            dest="config_file",
            help="config file (.yml)",
            required=True,
        )
        exclusive_group = self._parser.add_mutually_exclusive_group()
        exclusive_group.add_argument(
            "--account-query",
            action="store",
            dest="account_query",
            help="account query (name:john email:example.com)",
            required=False,
        )
        exclusive_group.add_argument(
            "--change-query",
            action="store",
            dest="change_query",
            help="change query (status:open since:2024-01-01 until:2024-01-02)",
            required=False,
        )
        self._parser.add_argument(
            "--change-action",
            action="store",
            dest="change_action",
            help="change action (add-reviewer:account-id,... delete-reviewer:account-id,... add-attention:account-id,... remove-attention:account-id,... approve-change:Code-Review=+2,... delete-change submit-change)",
            required=False,
        )
        exclusive_group.add_argument(
            "--group-query",
            action="store",
            dest="group_query",
            help="group query (name:admin member:john)",
            required=False,
        )
        exclusive_group.add_argument(
            "--project-query",
            action="store",
            dest="project_query",
            help="project query (name:test state:active)",
            required=False,
        )
        self._parser.add_argument(
            "-v", "--version", action="version", version=__version__
        )

    def parse(self, argv):
        return self._parser.parse_args(argv[1:])
