from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
from urllib.parse import urlparse
from download_file import *
import os
import config
import logging
import blacklist
import shutil

class Page:
    def __init__(self, cfg, logger, page_id):
        self.hostname = None
        self.url_list = []
        self.cfg = cfg
        self.logger = logger
        self.page_id = page_id

    def ReadPage(self, blist):
        self.logger.debug('Thread %s - Page.ReadPage(%s) started', self.page_id, self.page_id)
        self.url_list = []
        self.count = 0
        self.blist = blist
        url = self.cfg.pageurl + self.page_id

        # Настройка Firefox для работы в headless-режиме
        options = Options()
        options.add_argument("--headless")  # Включаем headless-режим

        service = webdriver.ChromeService(executable_path="/usr/local/bin/geckodriver")
        driver = webdriver.Firefox(options=options, service=service)
        # restrict time to wait for page
        driver.set_page_load_timeout(self.cfg.timeout)

        try:
            try:
                driver.get(url)
            except TimeoutException:
                pass
            except Exception as err:
                self.logger.error('Thread %s - Page.ReadPage(): error reading page: %s', self.page_id, str(err))

            # Получаем HTML-код страницы
            page_source = driver.page_source
            # Парсим страницу с помощью BeautifulSoup
            soup = BeautifulSoup(page_source, 'html.parser')
            # Ищем все теги <img> и извлекаем ссылки на изображения
            for img_tag in soup.find_all('img'):
                src = img_tag.get('src')
                if src:
                    self.url_list.append(src)
                    self.count += 1

            self.logger.debug('Thread %s - Page.ReadPage(): Found %i picture links', self.page_id, self.count)
            if self.count > 0:
                self.hostname = url = urlparse(self.url_list[0]).hostname
                self.logger.debug('Thread %s - Page.ReadPage(): Host name - %s', self.page_id, self.hostname)
            else:
                self.logger.error('Thread %s - Page.ReadPage(): Failed to collect image links', self.page_id)
        except Exception as err:
            self.logger.error('Thread %s - Page.ReadPage(): error: %s', self.page_id, str(err))
        finally:
            # Закрываем браузер, даже если возникла ошибка
            if 'driver' in locals():
                driver.quit()
        self.logger.debug('Thread %s - Page.ReadPage() ended', self.page_id)

    def DownloadPage(self):
        self.logger.debug('Thread %s - Page.DownloadPage() started', self.page_id)
        cnt = 0
        hires = 0

        if not self.blist.inBlackList(self.hostname):
            full_path = self.cfg.basepath + '/' + self.hostname + '/'+self.page_id

            if self.count > 0:
                # создаем директорию
                try:
                    os.makedirs(full_path)
                    self.logger.debug('Thread %s - Page.DownloadPage(): Created directory %s', self.page_id, full_path)
                except OSError:
                    self.logger.error('Thread %s - Page.DownloadPage(): Failed to create directory %s', self.page_id, full_path)

                for element in self.url_list:
                    self.logger.debug('Thread %s - Page.DownloadPage(): element %s', self.page_id, element)
                    cnt1, hires1 = download_file(element, full_path+'/'+get_file_name(element), self.logger, int(self.cfg.threshold), self.page_id)
                    cnt = cnt + cnt1
                    hires = hires + hires1
                if (cnt > 0) and (hires == 0):
                    self.logger.debug('Thread %s - No HIRES pictures', self.page_id)
                if (cnt == 0) or (hires == 0):
                    try:
                        shutil.rmtree(full_path, ignore_errors=False, onerror=None)
                        self.logger.debug('Thread %s - Page.DownloadPage(): Removed directory %s', self.page_id,
                                          full_path)
                    except OSError:
                        self.logger.error('Thread %s - Page.DownloadPage(): Failed to remove directory %s',
                                          self.page_id, full_path)
        else:
            self.logger.debug('Thread %s - Page.DownloadPage() in black list', self.page_id)
        self.logger.debug('Thread %s - Page.DownloadPage() finished', self.page_id)
