##########################################################################
###################### First Latvian Fasker' Ripper ######################
#################### Copyright (c) 2024-2025 mr.Iceman ###################
##########################################################################
from logging.handlers import TimedRotatingFileHandler

from config import *
from pages_list import *
import logging
from database import *
import time
import blacklist
import signal

from pages_list import PagesList

def terminate(signal_number, frame):
    """
    Terminate the program in response to a received signal.
    
    This function logs a critical message with the received signal number and then raises a KeyboardInterrupt to initiate graceful termination.
    
    Parameters:
        signal_number (int): The signal identifier that triggered the termination.
        frame (FrameType): The current stack frame (unused).
        
    Raises:
        KeyboardInterrupt: Always raised to interrupt the program execution.
    """
    logger.critical(f'Received {signal_number}')
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
    except Exception as e:
        logger.critical("Unexpected error: %s", str(e))
        done = True
logger.critical('Program finished')

