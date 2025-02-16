##########################################################################
###################### First Latvian Fasker' Ripper ######################
#################### Copyright (c) 2024-2025 mr.Iceman ###################
##########################################################################
import sqlite3
import time

class LinksDB:
    def __init__(self, cfg, logger):
        self.cfg = cfg
        self.logger = logger
        self.conn = sqlite3.connect(self.cfg.database)

    def add_link(self, id):
        self.logger.debug('LinksDB.add_link(%s) started', id)
        try:
            cursor = self.conn.cursor()
            cursor.execute("insert into link_list(id,ts) values (?,?);",(id, time.time(),))
        except sqlite3.DatabaseError as err:
            self.logger.error('LinksDB.add_link() error: %s', err)
        else:
            self.conn.commit()
        self.logger.debug('LinksDB.add_link() ended')

    def exist_link(self, id):
        self.logger.debug('LinksDB.exist_link(%s) started', id)
        m = time.time() - (int(self.cfg.hold_days) * 60 * 60 * 24)
        try:
            cursor = self.conn.cursor()
            cursor.execute("select count(*) from link_list where id = (?);",(id,))
            (cnt,) = cursor.fetchone()
            cursor.execute("delete from link_list where ts < (?);",(m,))
        except sqlite3.DatabaseError as err:
            self.logger.error('LinksDB.exist_link() error: %s', err)
            cnt = 100
        self.logger.debug('LinksDB.exist_link() ended. Return %i', cnt)
        return cnt
