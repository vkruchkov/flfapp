##########################################################################
###################### First Latvian Fasker' Ripper ######################
#################### Copyright (c) 2024-2025 mr.Iceman ###################
##########################################################################
from logging.handlers import TimedRotatingFileHandler

from config import *
from pages_list import *
from download_file import *
import logging
from database import *
import time
import blacklist
import signal

from pages_list import PagesList

def terminate(signalNumber, frame):
    logger.critical(f'Received {signalNumber}')
    raise KeyboardInterrupt

# Read configuration
cfg = Config()
cfg.read_config('FirstLatvianFusker.cfg')

signal.signal(signal.SIGABRT, terminate)
signal.signal(signal.SIGBREAK, terminate)
signal.signal(signal.SIGINT, terminate)
signal.signal(signal.SIGTERM, terminate)

logger = logging.getLogger("FirstLatvianFusker")
logger.setLevel(cfg.loglevel)

# create the logging file handler
# Time rotating logs
fh = TimedRotatingFileHandler(cfg.logname, 'midnight', 1, 6)
formatter = logging.Formatter('%(asctime)s - %(module)s:%(lineno)d - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

# add handler to logger object
logger.addHandler(fh)

logger.critical('Program started')

db = LinksDB(cfg,logger)
blist = blacklist.BlackList(cfg, logger)
done = False
while not done:
    try:
        list = PagesList(cfg, logger, db, blist)
        list.ReadPagesList(cfg.url)
        list.ProcessPagesList()
        if threading.activeCount() == 1 :
            logger.debug("Idle. Sleep 60 sec")
        else :
            logger.debug("Sleep 60 sec")
        time.sleep(60)    # pause 60 second
    except  KeyboardInterrupt:
        logger.critical("Program interrupt raised")
        done = True
    except Exception:
        logger.critical("Unexpected error: %s", str(e))
        done = True
logger.critical('Program finished')

