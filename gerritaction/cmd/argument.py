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
        self._parser.add_argument(
            "--gerrit-action",
            action="store",
            dest="gerrit_action",
            help="gerrit action (add-reviewer:{account-id,...} delete-reviewer:{account-id,...} add-attention:{account-id,...} remove-attention:{account-id,...})",
            required=True,
        )
        self._parser.add_argument(
            "--gerrit-query",
            action="store",
            dest="gerrit_query",
            help="gerrit query (status:open since:2021-01-01 until:2021-01-02)",
            required=True,
        )
        self._parser.add_argument(
            "-v", "--version", action="version", version=__version__
        )

    def parse(self, argv):
        return self._parser.parse_args(argv[1:])
