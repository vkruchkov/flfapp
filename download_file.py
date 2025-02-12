
from urllib.request import urlopen, Request
from PIL import Image
import os
from typing import Any


def download_file(url, file_name, logger, threshold, id):
    logger.debug('Thread %s - download_file(%s) started', id, url)
    rcode = 1
    hires = False
#    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    try:
#        request = urllib.request.Request(url, headers={'User-Agent': user_agent})  # type: Any
#        resource = urllib.request.urlopen(url)
        resource = urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}))
        out_file = open(file_name, 'wb')
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
