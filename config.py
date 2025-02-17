##########################################################################
###################### First Latvian Fusker' Ripper ######################
#################### Copyright (c) 2024-2025 mr.Iceman ###################
##########################################################################
import configparser
import logging
from contextlib import suppress

DEFAULT_URL = 'https://www.fusker.xxx/en/'
DEFAULT_LOG_PATH = 'FirstLatvianFusker.log'
DEFAULT_PAGE_URL = '?lid='
DEFAULT_BASE_PATH = 'files'
DEFAULT_DATABASE = 'flf.db'
DEFAULT_MAX_THREADS = 10
DEFAULT_BLACK_LIST = 'black.list'
DEFAULT_THRESHOLD = 1500
DEFAULT_HOLD_DAYS = 3
DEFAULT_TIMEOUT = 15
DEFAULT_GECKODRIVER_PATH = '/usr/local/bin/geckodriver'

class Config:
    def __init__(self):
        self.url = DEFAULT_URL
        self.logname = DEFAULT_LOG_PATH
        self.loglevel = logging.INFO
        self.basepath = DEFAULT_BASE_PATH
        self.pageurl = DEFAULT_PAGE_URL + DEFAULT_URL
        self.database = DEFAULT_DATABASE
        self.max_threads = DEFAULT_MAX_THREADS
        self.blacklist = DEFAULT_BLACK_LIST
        self.threshold = DEFAULT_THRESHOLD
        self.hold_days = DEFAULT_HOLD_DAYS
        self.timeout = DEFAULT_TIMEOUT
        self.geckodriver_path = DEFAULT_GECKODRIVER_PATH

    def read_config(self, config_name):
        config = configparser.ConfigParser()
        config.read(config_name)

        with suppress(configparser.Error):
            self.url = config.get("Settings", "url")

        with suppress(configparser.Error):
            self.logname = config.get("Settings", "logname")

        with suppress(configparser.Error):
            self.loglevel = config.get("Settings", "loglevel")


        with suppress(configparser.Error):
            self.basepath = config.get("Settings", "basepath")


        with suppress(configparser.Error):
            self.pageurl = self.url + config.get("Settings", "pageurl")

        with suppress(configparser.Error):
            self.database = config.get("Settings", "database")

        with suppress(configparser.Error):
            self.max_threads = config.get("Settings", "max_threads")

        with suppress(configparser.Error):
            self.blacklist = config.get("Settings", "blacklist")

        with suppress(configparser.Error):
            self.threshold = config.get("Settings", "threshold")

        with suppress(configparser.Error):
            self.hold_days = config.get("Settings", "hold_days")

        with suppress(configparser.Error):
            self.timeout = config.get("Settings", "timeout")
