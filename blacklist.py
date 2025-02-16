##########################################################################
###################### First Latvian Fasker' Ripper ######################
#################### Copyright (c) 2024-2025 mr.Iceman ###################
##########################################################################
import re
import os
import time

class BlackList:
    def __init__(self, cfg, logger):
        self.cfg = cfg
        self.logger = logger
        self.lst = []
        self.patterns = []
        self.last_time = 0

    def readBlackList(self):
        try:
            t = os.path.getmtime(self.cfg.blacklist)
            # Temporary array of patterns
            ptt = []
            if t > self.last_time:
                self.last_time = t
                self.lst.clear()
                cnt = 0
                with open(self.cfg.blacklist) as f:
                    self.lst = f.read().splitlines()
                self.lst.sort()
                self.lst = list(filter(None, self.lst))
                for l in self.lst:
                    # Fill temporary array of patterns
                    ptt.append(re.compile(l))
                    cnt = cnt +1
                # Set patterns array
                self.patterns = ptt;
                self.logger.info('BlackList.readBlackList() loaded %u records', cnt)
        except Exception as err:
                self.logger.error('BlackList.readBlackList() error: %s', err)

    def inBlackList(self, url):
        found = False
        for p in self.patterns:
            if re.search(p,url) is not None:
                found = True
                break
        return found
