##########################################################################
###################### First Latvian Fasker' Ripper ######################
#################### Copyright (c) 2024-2025 mr.Iceman ###################
##########################################################################
import threading
from logging.handlers import TimedRotatingFileHandler
from config import Config
import logging
from database import *
import time
import blacklist
import signal
import
from pages_list import PagesList
from remove_empty_dirs import remove_empty_subdirectories


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
    logger.critical(f'Received signal {signal_number}')
    raise KeyboardInterrupt

# Read configuration
cfg = Config()
cfg.read_config('FirstLatvianFusker.cfg')

for sig in [signal.SIGABRT, signal.SIGINT, signal.SIGTERM]:
    signal.signal(sig, terminate)

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
flag_idle_ft = True
while not done:
    try:
        plist = PagesList(cfg, logger, db, blist)
        plist.read_pages_list(cfg.url)
        plist.process_pages_list()
        if threading.activeCount() == 1 :
            if flag_idle_ft :
                flag_idle_ft = False
                remove_empty_subdirectories(cfg.basepath, logger)
            logger.debug("Idle. Sleep %i sec", cfg.repeat)
        else :
            flag_idle_ft = True
            logger.debug("Sleep %i sec", cfg.repeat)
        time.sleep(cfg.repeat)    # pause 
    except  KeyboardInterrupt:
        logger.critical("Program interrupt raised")
        done = True
    except Exception as e:
        logger.critical("Unexpected error: %s", str(e))
        done = True
logger.critical('Program finished')

