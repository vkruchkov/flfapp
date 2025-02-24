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
        self.initialize_database()

    def initialize_database(self):
        """
        Initialize the database if it doesn't exist.
        Creates the necessary table structure for storing links.

        Returns:
            bool: True if initialization was successful, False otherwise
        """
        try:
            cursor = self.conn.cursor()
            self.conn.execute('BEGIN')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS link_list (
                    id TEXT NOT NULL UNIQUE,
                    ts REAL NOT NULL
                )
            ''')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_link_list_id ON link_list(id)')
            self.conn.commit()
            self.logger.info("Database initialized successfully")
            return True
        except sqlite3.Error as e:
            self.conn.rollback()
            self.logger.error(f"Failed to initialize database: {e}")
            return False

    def add_link(self, id):
        """
        Inserts a new link record into the database with the specified identifier and the current timestamp.
        
        This method logs the beginning and end of its execution. It attempts to insert a new row into the
        'link_list' table using the provided link identifier and the current UNIX timestamp. If a SQLite database
        error occurs during the insertion, the error is logged and the transaction is not committed. Otherwise,
        the transaction is committed to save the new link.
        
        Parameters:
            id (Any): The unique identifier for the link to be added. The expected type should match the database schema.
        
        Returns:
            None
        """
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
        """
            Check for the existence of a link and remove expired entries from the database.
        
            This method queries the database to count the number of records in the 'link_list' table that match the
            provided link identifier. It also deletes any records whose timestamp is older than a threshold computed based
            on the 'hold_days' configuration parameter (converted to seconds). If a database error occurs during these
            operations, the error is logged and a default count of 100 is returned.
        
            Parameters:
                id (Any): The identifier of the link to check in the database.
        
            Returns:
                int: The count of matching links found. If a database error occurs, returns 100.
            """
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
