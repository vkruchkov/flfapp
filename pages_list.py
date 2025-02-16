##########################################################################
###################### First Latvian Fasker' Ripper ######################
#################### Copyright (c) 2024-2025 mr.Iceman ###################
##########################################################################
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException
# from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
import re

from selenium.webdriver.firefox.service import Service

import config
import logging
import database
from page import *
import threading
import time
import blacklist


def prescript(cfg, logger, id, blist):
    page = Page(cfg, logger, id)
    page.ReadPage(blist)
    if page.count > 0:
        page.DownloadPage()

class PagesList:
    def __init__(self, cfg, logger, db, blist):
#        self.urls_tag = []
        self.id_list = []
        self.cfg = cfg
        self.logger = logger
        self.db = db
        self.blist = blist
        self.blist.readBlackList()

    def ReadPagesList(self, url):
        self.logger.debug('PagesList.ReadPagesList() started')
        # Настройка Firefox для работы в headless-режиме
        options = Options()
        options.add_argument("--headless")  # Включаем headless-режим

        try:
            service = webdriver.ChromeService(executable_path=self.cfg.geckodriver_path)
            driver = webdriver.Firefox(options=options,service=service)
            driver.set_page_load_timeout(self.cfg.timeout)

            try:
                driver.get(url)
                self.logger.debug('PagesList.ReadPagesList(): got page')
            except TimeoutException:
                self.logger.debug('PagesList.ReadPagesList(): got page partially after timeout')
            except Exception as err:
                self.logger.error('PagesList.ReadPagesList(): error reading page: %s', str(err))

            try:
                links = driver.find_elements(By.TAG_NAME, "a")
            except NoSuchElementException:
                self.logger.error('PagesList.ReadPagesList() error: no links found')
                links = []

            # Фильтрация ссылок, содержащих "lid=" в атрибуте href
            filtered_links = [link for link in links if
                              link.get_attribute("href") and "lid=" in link.get_attribute("href")]

            for link in filtered_links:
                href = link.get_attribute("href")
                # Извлекаем подстроку с 11 по 20 символы (индексы 10:20)
                el = href[31:] if len(href) >= 31 else "0"
                if self.db.exist_link(el) == 0:
                    self.id_list.append(el)
                    self.logger.debug('PagesList.ReadPagesList(): found new element: %s ', el)
                else:
                    self.logger.debug('PagesList.ReadPagesList(): element %s already exists', el)

        finally:
            # Закрываем браузер, даже если возникла ошибка
            if 'driver' in locals():
                driver.quit()
        self.logger.debug('PagesList.ReadPagesList() ended')

    def ProcessPagesList(self):
        self.logger.debug('PagesList.ProcessPagesList() started')
        done = False
        while not done:
            try:
                element = self.id_list.pop()

                while threading.activeCount() > int(self.cfg.max_threads) + 1:
                    time.sleep(1)  # pause 1 second
                    self.logger.debug('PagesList.ProcessPagesList() waiting for empty thread...')
                self.logger.debug('PagesList.ProcessPagesList(): process element %s', element)
                self.db.add_link(element)
                thread1 = threading.Thread(target=prescript, args=(self.cfg, self.logger, element, self.blist))
                self.logger.debug('PagesList.ProcessPagesList(): Created thread %s', element)
                thread1.start()
            except IndexError as err:
                done = True
            time.sleep(1)  # pause 1 second
            self.logger.debug('PagesList.ProcessPagesList(): count of active threads = %i', threading.activeCount())

        self.logger.debug('PagesList.ProcessPagesList() ended')
