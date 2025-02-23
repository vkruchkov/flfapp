# test_download_file.py
import os
import unittest
from unittest.mock import Mock, patch
from download_file import download_file, CONST_MAX_FILE_SIZE
from PIL import Image
import io

class TestDownloadFile(unittest.TestCase):
    def setUp(self):
        self.logger = Mock()
        self.threshold = 1000
        self.thread_id = 1
        
    @patch('urllib.request.urlopen')
    @patch('PIL.Image.open')
    def test_download_success(self, mock_image_open, mock_urlopen):
        mock_response = Mock()
        mock_response.getheader.return_value = '1000'
        mock_response.read.return_value = b'test data'
        mock_urlopen.return_value = mock_response
        
        mock_img = Mock()
        mock_img.size = (500, 300)
        mock_image_open.return_value = mock_img
        
        rcode, hires = download_file('https://www.fusker.xxx/assets/favicons/apple-touch-icon.png', 'test.jpg',
                                   self.logger, self.threshold, self.thread_id)
        self.assertEqual(rcode, 1)
        self.assertFalse(hires)
        
    @patch('urllib.request.urlopen')
    def test_download_file_too_large(self, mock_urlopen):
        mock_response = Mock()
        mock_response.headers.get.return_value = str(CONST_MAX_FILE_SIZE + 1)
        mock_urlopen.return_value = mock_response
        
        rcode, hires = download_file('https://www.fusker.xxx/assets/favicons/apple-touch-icon.png', 'test.jpg',
                                   self.logger, self.threshold, self.thread_id)
        self.assertEqual(rcode, 1)
        self.assertFalse(hires)

    def tearDown(self):
        os.remove('test.jpg')
