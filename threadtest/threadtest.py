# -*- coding: utf-8 -*-
# import packages
import sys
import re, urlparse
import os
import os.path
from time import sleep
from time import time
import requests
import json, csv
import random

import config
import proxies

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common import exceptions as EX
from selenium.webdriver.chrome.options import Options

from scrapex import *
import threading

# define global variables
threadLock = threading.Lock()
# end global varialbles
# *****************************************************************
# define sprider class
class ThreadObj(threading.Thread):
    # init function for class
    def __init__(self, idx):
        super(ThreadObj, self).__init__()
        self.thread_id = idx
        self.driver = self.init_chrome_driver(idx)
        self.sobj = Scraper(use_cache=False, retries=3, timeout=300, log_post=True, log_headers=True)
    # end function for class

    # define init function for Chrome web driver
    def init_chrome_driver(self, idx):
        # to set up arguments and extensions for chrome options
        co = webdriver.ChromeOptions()
        proxyauth_plugin_path = config.init_proxies(idx)
        co.add_extension(proxyauth_plugin_path)
        co.add_argument("--start-maximized")
        co.add_argument("--disable-infobars")
        co.add_argument("--disable-notifications")
        driver = webdriver.Chrome(chrome_options = co)
        driver.implicitly_wait(config.__SHORT_TIME__)
        return driver
    # end init function for Chrome web driver

    # define init function for Firefox browser driver
    # Mozila Firefox
    # TODO: //
    # end init function for Firefox browser driver

    # define init function for PhantomJS
    # PhantomJS
    # TODO: //
    # end init function for PhantomJS

    # define thread run function
    # This is thread function user can customize
    # When user execute threadobj.start() function, it will run
    def run(self):
        try:
            self.driver.get("https://google.com")
            WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//input[@id="lst-ib"]')))
            config.wait(config.__SHORT_TIME__ , str(self.thread_id))
            self.driver.find_element_by_xpath("//input[@id='lst-ib']").send_keys("What is my ip")
            config.wait(config.__SHORT_TIME__ , str(self.thread_id))
            self.driver.find_element_by_xpath("//input[@id='lst-ib']").send_keys(Keys.RETURN)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(),"Your public IP address")]')))
            config.wait(config.__SHORT_TIME__ , str(self.thread_id))
            sdoc = Doc(html=self.driver.page_source)
            ip_addr = sdoc.x('//*[contains(text(),"Your public IP address")]/preceding-sibling::div[1]/text()')
            threadLock.acquire()
            self.sobj.save(["IP Address",ip_addr],remove_existing_file = False)
            print self.thread_id, ":", ip_addr
            threadLock.release()

            # ip_addrs = re.findall(r'[0-9]+(?:\.[0-9]+){3}', self.driver.page_source)
            # ip_addrs = re.findall('\d+(?:\.\d+){3}', self.driver.page_source)
            # ip_addrs = re.findall('\d{1,3}(?:\.\d{1,3}){3}', self.driver.page_source)
            # ip_addrs = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', self.driver.page_source)
            # ip_addrs = re.findall('\d{1,3}(?:\.\d{1,3}){3}', self.driver.page_source)
            # for ip_addr in ip_addrs:
            #     threadLock.acquire()
            #     self.sobj.save(["IP Address",ip_addr],remove_existing_file = False)
            #     print self.thread_id, ":", ip_addr
            #     threadLock.release()
        except Exception as e:
            print e
    # end thread run function
    
# end class
# *****************************************************************
# main function

if __name__ == '__main__':
    if os.path.exists("result.csv"):
        os.remove("result.csv")
    threads = []
    # for i in range(5):
    #     thrd = ThreadObj(i)
    #     threads.append(thrd)

    # for thrd in threads:
    #     thrd.start()

    # for thrd in threads:
    #     thrd.join()

# end main function
