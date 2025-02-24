# test_blacklist.py
import re
import unittest
from unittest.mock import Mock, patch
from blacklist import BlackList

class TestBlackList(unittest.TestCase):
    def setUp(self):
        self.cfg = Mock()
        self.cfg.blacklist = 'black.list'
        self.logger = Mock()
        self.blacklist = BlackList(self.cfg, self.logger)
    
    def test_init(self):
        self.assertEqual(self.blacklist.lst, [])
        self.assertEqual(self.blacklist.patterns, [])
        self.assertEqual(self.blacklist.last_time, 0)
        
    @patch('os.path.getmtime')
    @patch('builtins.open')
    def test_read_blacklist_success(self, mock_open, mock_getmtime):
        mock_getmtime.return_value = 123456789
        mock_open.return_value.__enter__.return_value.read.return_value = 'example.com\ntest.com'
        
        self.blacklist.readBlackList()
        self.assertEqual(len(self.blacklist.patterns), 2)
        self.assertEqual(self.blacklist.last_time, 123456789)
        
    def test_in_blacklist_match(self):
        self.blacklist.patterns = [re.compile(r'example\.com')]
        self.assertTrue(self.blacklist.inBlackList('http://example.com/image.jpg'))
        
    def test_in_blacklist_empty_url(self):
        self.blacklist.patterns = [re.compile(r'example\.com')]
        self.assertFalse(self.blacklist.inBlackList(''))
