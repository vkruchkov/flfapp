##########################################################################
###################### First Latvian Fusker' Ripper ######################
#################### Copyright (c) 2024-2025 mr.Iceman ###################
##########################################################################
import configparser
import logging
from contextlib import suppress
from urllib.parse import urljoin

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
        """
        Initialize a new configuration instance with default settings.
        
        This constructor sets configuration attributes using predefined constants:
        - url (str): Base URL from DEFAULT_URL.
        - logname (str): Log file path from DEFAULT_LOG_PATH.
        - loglevel (int): Logging level, set to logging.INFO.
        - basepath (str): Base directory path from DEFAULT_BASE_PATH.
        - pageurl (str): A URL segment that is appended to the main URL.
        - database (str): Database name/path from DEFAULT_DATABASE.
        - max_threads (int): Maximum number of threads from DEFAULT_MAX_THREADS.
        - blacklist (str): Path to the blacklist file from DEFAULT_BLACK_LIST.
        - threshold (int/float): Threshold value from DEFAULT_THRESHOLD.
        - hold_days (int): Number of days to hold data from DEFAULT_HOLD_DAYS.
        - timeout (int): Timeout duration in seconds from DEFAULT_TIMEOUT.
        - geckodriver_path (str): Path to the Geckodriver from DEFAULT_GECKODRIVER_PATH.
        """
        self.url: str = DEFAULT_URL
        self.logname: str = DEFAULT_LOG_PATH
        self.loglevel: str = logging.INFO
        self.basepath: str = DEFAULT_BASE_PATH
        self.pageurl: str = DEFAULT_PAGE_URL
        self.database: str = DEFAULT_DATABASE
        self.max_threads: int = DEFAULT_MAX_THREADS
        self.blacklist: str = DEFAULT_BLACK_LIST
        self.threshold: int = DEFAULT_THRESHOLD
        self.hold_days: int = DEFAULT_HOLD_DAYS
        self.timeout: int = DEFAULT_TIMEOUT
        self.geckodriver_path: str = DEFAULT_GECKODRIVER_PATH

    def read_config(self, config_name):
        """
        Read configuration settings from a file and update instance attributes.
        
        This method uses the configparser module to parse the configuration file specified by
        `config_name`. It attempts to read various settings from the "Settings" section, including:
        - `url`: Base URL for the application.
        - `logname`: Name or path for the log file.
        - `loglevel`: Logging level.
        - `basepath`: Base directory path.
        - `pageurl`: A URL segment that is appended to the main URL.
        - `database`: Database name or connection string.
        - `max_threads`: Maximum number of threads to utilize.
        - `blacklist`: Path or identifier for the blacklist file.
        - `threshold`: Threshold value for specific operations.
        - `hold_days`: The number of days for which certain operations are held.
        - `timeout`: Timeout value for operations.
        - 'geckodriver_path': path to geckodriver
        
        Each setting is retrieved within a context that suppresses any `configparser.Error` exceptions,
        leaving the corresponding attribute unchanged if the setting is missing or improperly formatted.
        
        Parameters:
            config_name (str): The path to the configuration file.
        
        Returns:
            None
        
        Example:
            >>> config = Config()
            >>> config.read_config("settings.ini")
            >>> print(config.url)
            http://example.com
        """
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
            self.pageurl = config.get("Settings", "pageurl")

        with suppress(configparser.Error):
            self.database = config.get("Settings", "database")

        with suppress(configparser.Error):
            self.max_threads = config.getint("Settings", "max_threads")

        with suppress(configparser.Error):
            self.blacklist = config.get("Settings", "blacklist")

        with suppress(configparser.Error):
            self.threshold = config.getint("Settings", "threshold")

        with suppress(configparser.Error):
            self.hold_days = config.getint("Settings", "hold_days")

        with suppress(configparser.Error):
            self.timeout = config.getint("Settings", "timeout")

        with suppress(configparser.Error):
            self.geckodriver_path = config.getint("Settings", "geckodriver_path")
        self.validate()

    def validate(self):
        """Проверяет корректность конфигурации."""
        if not self.url.startswith(('http://', 'https://')):
            raise ValueError(f"Некорректный URL: {self.url}")
        if self.max_threads < 1:
            raise ValueError(f"max_threads должно быть больше 0: {self.max_threads}")
        if self.threshold < 0:
            raise ValueError(f"threshold должно быть положительным: {self.threshold}")
        if self.hold_days < 0:
            raise ValueError(f"hold_days должно быть положительным: {self.hold_days}")
        if self.timeout < 0:
            raise ValueError(f"timeout должно быть положительным: {self.timeout}")