# test_pages_list.py
import logging
import unittest
from logging import Logger
from unittest.mock import Mock, patch

from config import Config
from pages_list import PagesList

class TestPagesList(unittest.TestCase):
    def setUp(self):
        self.cfg = Config()
        self.cfg.max_threads = 2
        self.cfg.timeout = 10

        self.logger = logging.getLogger("FirstLatvianFusker")
        self.logger.setLevel(self.cfg.loglevel)
        # create the logging file handler
        # Time rotating logs
        fh = logging.FileHandler(self.cfg.logname)
        formatter = logging.Formatter('%(asctime)s - %(module)s:%(lineno)d - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        # add handler to logger object
        self.logger.addHandler(fh)

        self.db = Mock()
        self.db.exist_link.return_value = 0
        self.blist = Mock()
        self.pages_list = PagesList(self.cfg, self.logger, self.db, self.blist)

    def test_read_pages_list(self):
        self.pages_list.read_pages_list(self.cfg.url)
        self.assertEqual(len(self.pages_list.id_list), 60)
        
    @patch('threading.Thread')
    def test_process_pages_list(self, mock_thread):
        self.pages_list.id_list = ['123456']
        mock_thread_instance = Mock()
        mock_thread.return_value = mock_thread_instance
        
        self.pages_list.process_pages_list()
        mock_thread.assert_called_once()
        mock_thread_instance.start.assert_called_once()
