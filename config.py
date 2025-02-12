import configparser
import logging

class Config:
    def __init__(self):
        self.url = ''
        self.logname = 'FirstLatvianFusker.log'
        self.loglevel = logging.INFO
        self.basepath = ''
        self.pageurl = ''
        self.database = 'flf.db'
        self.max_threads = 10
        self.blacklist = 'black.list'
        self.timeout = 5

    def ReadConfig(self, configName):
        config = configparser.ConfigParser()
        config.read(configName)

        try:
            self.url = config.get("Settings", "url")
        except:
            self.url = 'https://www.fusker.xxx/en/'

        try:
            self.logname = config.get("Settings", "logname")
        except:
            self.logname = '/mnt/data/FirstLatvianFusker/FirstLatvianFusker.log'

        try:
            self.loglevel = config.get("Settings", "loglevel")
        except:
            self.loglevel = logging.INFO

        try:
            self.basepath = config.get("Settings", "basepath")
        except:
            self.basepath = 'files'

        try:
            self.pageurl = config.get("Settings", "pageurl")
        except:
             self.pageurl = 'https: // www.fusker.xxx / en /?lid='

        try:
            self.database = config.get("Settings", "database")
        except:
             self.database = 'flf.db'

        try:
            self.max_threads = config.get("Settings", "max_threads")
        except:
             self.max_threads = 10

        try:
            self.blacklist = config.get("Settings", "blacklist")
        except:
             self.blacklist = 'black.list'

        try:
            self.threshold = config.get("Settings", "threshold")
        except:
             self.threshold = '1500'

        try:
            self.hold_days = config.get("Settings", "hold_days")
        except:
             self.hold_days = 10

        try:
            self.timeout = config.get("Settings", "timeout")
        except:
             self.timeout = 5
