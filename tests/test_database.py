# test_database.py
import unittest
from unittest.mock import Mock, patch
import sqlite3
from database import LinksDB

class TestLinksDB(unittest.TestCase):
    def setUp(self):
        self.cfg = Mock()
        self.cfg.database = ':memory:'
        self.cfg.hold_days = 3
        self.logger = Mock()
        self.db = LinksDB(self.cfg, self.logger)
        
    def test_initialize_database(self):
        self.assertTrue(self.db.initialize_database())
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='link_list'")
        self.assertIsNotNone(cursor.fetchone())
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_link_list_id'")
        self.assertIsNotNone(cursor.fetchone())
        
    def test_add_link(self):
        self.db.initialize_database()
        self.db.add_link('test_id')
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT id FROM link_list WHERE id=?", ('test_id',))
        self.assertEqual(cursor.fetchone()[0], 'test_id')
        
    def test_exist_link_with_cleanup(self):
        self.db.initialize_database()
        self.db.add_link('test_id')
        self.assertTrue(self.db.exist_link('test_id') > 0)
