##########################################################################
###################### First Latvian Fasker' Ripper ######################
#################### Copyright (c) 2024-2025 mr.Iceman ###################
##########################################################################
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from urllib.parse import urlparse
from download_file import *
import os
import shutil

class Page:
    def __init__(self, cfg, logger, page_id):
        self.hostname = None
        self.url_list = []
        self.cfg = cfg
        self.logger = logger
        self.page_id = page_id

    def read_page(self, blist):
        """
        Read and parse the web page to extract image source URLs.
        
        This method constructs the target URL using the configuration and page ID, then launches a Firefox WebDriver in headless mode (with the geckodriver path provided in the configuration). It attempts to load the page with a specified timeout and, on success, retrieves the HTML content. Using BeautifulSoup, the method searches for all <img> tags and collects the 'src' attribute of each valid tag, updating the object's url_list and image count. If at least one image URL is found, the hostname of the first image is extracted and stored. All key steps and failures are logged using the instance's logger.
        
        Parameters:
            blist (Any): A blacklist object (or similar) used later to determine whether to skip image downloads.
        
        Returns:
            None
        
        Side Effects:
            - Updates self.url_list with the collected image source URLs.
            - Sets self.count to the number of extracted image links.
            - Assigns the hostname of the first image URL to self.hostname if any images are found.
            - Logs debug and error messages detailing the progress and any issues encountered.
            
        Exception Handling:
            Exceptions during page loading and parsing (e.g., timeouts or other errors) are caught and logged.
        """
        self.logger.debug('Thread %s - Page.ReadPage(%s) started', self.page_id, self.page_id)
        self.url_list = []
        self.count = 0
        self.blist = blist
        url = self.cfg.pageurl + self.page_id
        self.links = []

        # Настройка Firefox для работы в headless-режиме
        options = Options()
        options.add_argument("--headless")  # Включаем headless-режим

        try:
            service = webdriver.ChromeService(executable_path=self.cfg.geckodriver_path)
            with webdriver.Firefox(options=options, service=service) as driver:
                # restrict time to wait for page
                driver.set_page_load_timeout(self.cfg.timeout)

                try:
                    driver.get(url)
                except TimeoutException:
                    pass
                except Exception as err:
                    self.logger.error('Thread %s - Page.ReadPage(): error reading page: %s', self.page_id, str(err))

                # Получаем HTML-код страницы
                page_source = driver.page_source
                try:
                    links = driver.find_elements(By.TAG_NAME, "img")
                except NoSuchElementException:
                    links = []
                # Фильтрация ссылок, содержащих атрибуты src
                for link in links:
                    src = link.get_attribute("src")
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

    def download_page(self):
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
