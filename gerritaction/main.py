# -*- coding: utf-8 -*-

import sys

from gerritaction.action.action import Action, ActionException
from gerritaction.cmd.argument import Argument
from gerritaction.cmd.banner import BANNER
from gerritaction.config.config import Config, ConfigException
from gerritaction.logger.logger import Logger


def main():
    print(BANNER)

    argument = Argument()
    arg = argument.parse(sys.argv)

    try:
        config = Config()
        config.config_file = arg.config_file
        config.account_query = arg.account_query
        config.change_query = arg.change_query
        config.change_action = arg.change_action
        config.group_query = arg.group_query
        config.project_query = arg.project_query
    except ConfigException as e:
        Logger.error(str(e))
        return -1

    Logger.info("action running")

    try:
        action = Action(config)
        action.run()
    except ActionException as e:
        Logger.error(str(e))
        return -2

    Logger.info("action exiting")

    return 0
