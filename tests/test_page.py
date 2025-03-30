# test_page.py
import logging
import os
import shutil
import unittest
from unittest.mock import Mock, patch
import blacklist
from blacklist import BlackList
from config import DEFAULT_GECKODRIVER_PATH, DEFAULT_BASE_PATH, Config
from page import Page
from selenium.webdriver.common.by import By

TEST_DIR = 'files/www.mike-picture.at/3793395'
TEST_ID = '3793395'

class TestPage(unittest.TestCase):
    def setUp(self):
        self.cfg = Config()
        self.cfg.geckodriver_path = DEFAULT_GECKODRIVER_PATH
        self.cfg.basepath = DEFAULT_BASE_PATH
        self.cfg.timeout = 10
        self.cfg.threshold = 1000

        # Init logger
        self.logger = logging.getLogger("FirstLatvianFusker")
        self.logger.setLevel(self.cfg.loglevel)
        fh = logging.FileHandler(self.cfg.logname)
        formatter = logging.Formatter('%(asctime)s - %(module)s:%(lineno)d - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

        self.page_id = TEST_ID
        self.page = Page(self.cfg, self.logger, self.page_id)
        self.blacklist = BlackList(self.cfg,self.logger)

    def test_download_page(self):
        self.page.read_page(self.blacklist)
        self.assertEqual(len(self.page.url_list), 6)
        self.assertEqual(self.page.count, 6)

        self.page.download_page()
        self.assertEqual(len([name for name in os.listdir(TEST_DIR) if os.path.isfile(os.path.join(TEST_DIR, name))]),6)

    def tearDown(self):
        shutil.rmtree(TEST_DIR, ignore_errors=True, onerror=None)