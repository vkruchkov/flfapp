##########################################################################
###################### First Latvian Fasker' Ripper ######################
#################### Copyright (c) 2024-2025 mr.Iceman ###################
##########################################################################
from page import Page, Options, webdriver, TimeoutException, NoSuchElementException, By
import threading
import time

def prescript(cfg, logger, id, blist):
    page = Page(cfg, logger, id)
    page.read_page(blist)
    if page.count > 0:
        page.download_page()

class PagesList:
    def __init__(self, cfg, logger, db, blist):
        self.id_list = []
        self.cfg = cfg
        self.logger = logger
        self.db = db
        self.blist = blist
        self.blist.readBlackList()

    def read_pages_list(self, url):
        """
        Retrieve and process link elements from the specified URL.
        
        This method sets up a headless Firefox browser using Selenium with configurations
        provided by self.cfg, navigates to the given URL, and extracts all <a> elements from the page.
        It filters these links to include only those whose 'href' attribute contains "lid=".
        For each filtered link, it extracts a substring starting at index 31 (if the href length is at least 31),
        or defaulting to "0" otherwise. The extracted substring is then checked against a database via
        self.db.exist_link; if the link does not already exist, it is appended to self.id_list for further processing.
        All actions and errors are logged using self.logger, and the browser is properly closed even if errors occur.
        
        Parameters:
            url (str): The URL of the page to scrape for links.
        
        Returns:
            None
        
        Notes:
            - A TimeoutException may occur if the page load exceeds the configured timeout; this is caught and logged.
            - A NoSuchElementException is caught and logged if no <a> elements are found on the page.
            - The method uses self.cfg.geckodriver_path for specifying the path to the geckodriver executable.
            - All browser operations are executed in headless mode.
        """
        self.logger.debug('PagesList.ReadPagesList() started')
        # Настройка Firefox для работы в headless-режиме
        options = Options()
        options.add_argument("--headless")  # Включаем headless-режим

        try:
            service = webdriver.FirefoxService(executable_path=self.cfg.geckodriver_path)
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
                link_exist = self.db.exist_link(el)
                if  link_exist == 0:
                    self.id_list.append(el)
                    self.logger.debug('PagesList.ReadPagesList(): found new element: %s ', el)
                elif link_exist == 1:
                    self.logger.debug('PagesList.ReadPagesList(): element %s already exists', el)
                else:
                    self.logger.error('PagesList.ReadPagesList(): Failed to verify that element %s exists', el)
        finally:
            # Закрываем браузер, даже если возникла ошибка
            if 'driver' in locals():
                driver.quit()
        self.logger.debug('PagesList.ReadPagesList() ended')

    def process_pages_list(self):
        """
        Process each page identifier in the instance's id_list concurrently using threads.
        
        This method continuously pops page identifiers from self.id_list and processes each one by:
          - Waiting until the number of active threads drops below the maximum allowed (determined by self.cfg.max_threads).
          - Logging debug messages to trace the processing stages.
          - Adding the identifier to the database via self.db.add_link.
          - Creating and starting a new thread that runs the prescript function with the current element and necessary context (configuration, logger, blacklist).
        
        The loop terminates when self.id_list is empty (i.e., a pop operation raises an IndexError). Throughout its execution, the method includes brief pauses (using time.sleep) to manage thread load and ensure that new threads are only started when capacity is available.
        
        Side Effects:
          - Launches new threads to process pages.
          - Updates the database with new page identifiers.
          - Logs detailed debug messages regarding the current processing state.
          
        Note:
          - This method does not return a value.
          - It relies on catching IndexError to detect when there are no more elements to process.
        """
        self.logger.debug('PagesList.ProcessPagesList() started')
        done = False
        while not done:
            try:
                element = self.id_list.pop()

                while (threading.activeCount() - 1) >= self.cfg.max_threads:
                    time.sleep(1)  # pause 1 second
                    self.logger.debug('PagesList.ProcessPagesList() waiting for empty thread...')
                self.logger.debug('PagesList.ProcessPagesList(): process element %s', element)
                self.db.add_link(element)
                thread1 = threading.Thread(target=prescript, args=(self.cfg, self.logger, element, self.blist))
                self.logger.debug('PagesList.ProcessPagesList(): Created thread %s', element)
                thread1.start()
            except IndexError:
                done = True
            time.sleep(1)  # pause 1 second
            self.logger.debug('PagesList.ProcessPagesList(): count of active threads = %i', threading.activeCount() - 1)

        self.logger.debug('PagesList.ProcessPagesList() ended')
