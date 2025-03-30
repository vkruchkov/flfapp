# test_download_file.py
import os
import unittest
from unittest.mock import Mock, patch

from config import Config
from download_file import download_file, CONST_MAX_FILE_SIZE
from PIL import Image
import io

class TestDownloadFile(unittest.TestCase):
    def setUp(self):
        self.logger = Mock()
        self.thread_id = 1
        
    def test_download_success(self):
        cfg = Config()
        cfg.delay = 0

        rcode, hires = download_file(cfg, 'https://www.fusker.xxx/assets/favicons/apple-touch-icon.png', 'test.jpg',
                                   self.logger, cfg.threshold, self.thread_id)
        self.assertEqual(rcode, 1)
        self.assertFalse(hires)

    def tearDown(self):
        try:
            os.remove('test.jpg')
        except FileNotFoundError:
            pass
