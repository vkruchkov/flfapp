# test_config.py
import configparser
import os
import unittest
from config import Config, DEFAULT_URL, DEFAULT_MAX_THREADS

TEST_CONFIGNAME = 'test.cfg'

class TestConfig(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        cfg = configparser.ConfigParser()
        cfg['Settings'] = {'url': 'https://www.ixbt.com',
                     'max_threads': '1',
                     'threshold': '2000'}
        with open(TEST_CONFIGNAME, 'w') as configfile:
            cfg.write(configfile)
    
    def test_init_default_values(self):
        self.assertEqual(self.config.url, DEFAULT_URL)
        self.assertEqual(self.config.max_threads, DEFAULT_MAX_THREADS)

    def test_read_config_success(self):
        self.config.read_config('test.cfg')
        self.assertEqual(self.config.url, 'https://www.ixbt.com')
        
    def test_validate_invalid_url(self):
        self.config.url = 'invalid_url'
        with self.assertRaises(ValueError):
            self.config.validate()
        
    def test_validate_invalid_max_threads(self):
        self.config.max_threads = 0
        with self.assertRaises(ValueError):
            self.config.validate()

    def tearDown(self):
        os.remove('test.cfg')
