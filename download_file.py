##########################################################################
###################### First Latvian Fasker' Ripper ######################
#################### Copyright (c) 2024-2025 mr.Iceman ###################
##########################################################################
from urllib.request import urlopen, Request
from PIL import Image
import os
from typing import Any


def download_file(url, file_name, logger, threshold, id):
    """
    Download an image from a URL, save it locally, and check if its dimensions exceed a given threshold.
    
    This function sends an HTTP request to the specified URL using a custom User-Agent header, writes the received image data to a file in binary mode, and then opens the saved file using the PIL Image library to determine its dimensions. It computes the sum of the image's width and height, and if this sum is greater than the provided threshold, it marks the image as high resolution. The function logs debug, info, and error messages via the supplied logger, and all exceptions encountered during download or image processing are caught and logged without being re-raised.
    
    Parameters:
        url (str): The URL of the image to download.
        file_name (str): The path and name of the file where the image will be saved.
        logger (logging.Logger): Logger object used for recording debugging, informational, and error messages.
        threshold (int): The numeric threshold to compare against the sum of the image's width and height.
        id (any): An identifier for the executing thread (e.g., int or str) used for logging purposes.
    
    Returns:
        tuple: A tuple (rcode, hires), where:
            rcode (int): A status code (always 1 in this implementation).
            hires (bool): True if the sum of the image's dimensions exceeds the threshold, otherwise False.
    
    Exceptions:
        All exceptions are caught and logged; the function does not raise any exceptions.
    
    Example:
        >>> result = download_file('http://example.com/image.jpg', 'local_image.jpg', logger, 1000, 1)
        >>> print(result)
        (1, True)
    """
    logger.debug('Thread %s - download_file(%s) started', id, url)
    rcode = 1
    hires = False
    try:
        resource = urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}))
        with open(file_name, 'wb') as out_file:
            out_file.write(resource.read())
            out_file.close()

        img = Image.open(file_name,"r")
        sz = img.size
        dm = sz[0] + sz[1]
        img.close()
        logger.debug('Image %s dimensions: %u x %u', file_name, sz[0], sz[1])
        if dm > threshold:
            hires = True

    except Exception as e:
        logger.error('Thread %s - download_file(%s) error: %s',id, url, str(e))

    else:
        logger.info('Thread %s - Saved file %s', id, url)

    logger.debug('Thread %s - download_file() ended', id)
    return rcode, hires

def get_file_name(url):
    return url[url.rindex('/')+1:]
