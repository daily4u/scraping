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
import argparse

import appconfig
import common_lib
import proxies
import agents

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common import exceptions as EX
from selenium.webdriver.chrome.options import Options

from scrapex import *
import threading
# *****************************************************************    
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
        # self.sobj = Scraper(use_cache=False, retries=3, timeout=300, log_post=True, log_headers=True)
    # end function for class
    # *****************************************************************    
    # define init function for Chrome web driver
    def init_chrome_driver(self, idx):
        # to set up arguments and extensions for chrome options
        co = webdriver.ChromeOptions()
        proxyauth_plugin_path = common_lib.init_proxies(idx)
        co.add_extension(proxyauth_plugin_path)
        co.add_extension(appconfig.__EXTENSION_NAME__)
        co.add_argument("--start-maximized")
        co.add_argument("--disable-infobars")
        co.add_argument("--disable-notifications")
        # driver = webdriver.Chrome(chrome_options = co, service_args=["--verbose", "--log-path=facebook.log"])
        driver = webdriver.Chrome(chrome_options = co)
        driver.implicitly_wait(common_lib.__SHORT_TIME__)
        return driver
    # end init function for Chrome web driver
    # *****************************************************************    
    # define init function for Firefox browser driver
    # Mozila Firefox
    # TODO: //
    # end init function for Firefox browser driver
    # *****************************************************************    
    # define init function for PhantomJS
    # PhantomJS
    # TODO: //
    # end init function for PhantomJS
    # *****************************************************************    
    # function for initialize chrome extensions
    def init_chrome_extension(self, driver):
        driver.get(appconfig.__OPTION_PATH__)
        common_lib.wait(common_lib.__SHORTEST_TIME__, "EXTENSION START")
        driver.find_element_by_id('inputUserId').send_keys(appconfig.__USER_ID_FOR_EXT__)
        common_lib.wait(common_lib.__SHORT_TIME__, "INPUT USER ID ON EXTENSION")
        driver.find_element_by_id('save').click()
        self.accept_alert(driver)
        common_lib.wait(common_lib.__SHORT_TIME__, "EXTENSION END")
    # end function
    # *****************************************************************    
    # functon for processing alert
    def accept_alert(self, driver):
        try:
            # Wait 10 seconds till alert is present
            WebDriverWait(driver, common_lib.__MIDDLE_TIME__).until(EC.alert_is_present())
            # Accepting alert.
            driver.switch_to.alert.accept();
        except Exception as e:
            print e
    # end function
    # *****************************************************************    
    # function for showing how to log in
    def log_in_facebook(self, driver):
        driver.get(appconfig.__APP_URL__)
        common_lib.wait(common_lib.__SHORT_TIME__, "BEFORE LOGIN")
        username = agents.accounts[self.thread_id].split(':')[0]
        password = agents.accounts[self.thread_id].split(':')[1]
        print username, password
        driver.find_element_by_id('email').send_keys(username)
        common_lib.wait(common_lib.__SHORT_TIME__, "INPUT EMAIL")
        driver.find_element_by_id('pass').send_keys(password)
        common_lib.wait(common_lib.__SHORT_TIME__, "INPUT PASSWORD")
        driver.find_element_by_xpath('//input[@data-testid="royal_login_button"]').click()
        common_lib.wait(common_lib.__MIDDLE_TIME__, "CLICK LOGIN BUTTON")
    # end function
    # *****************************************************************    
    # function for click not now
    def click_not_now(self, driver):
        driver.find_element_by_xpath('//*[contains(text(),"Not Now")]').click()
        common_lib.wait(common_lib.__MIDDLE_TIME__, "Click Not Now")
    # end function 
    # *****************************************************************    
    # function for click not now
    def click_homepage(self, driver):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Home")]')))
            driver.find_element_by_xpath('//*[contains(text(), "Home")]').click()
        except Exception as e:
            print e
            driver.find_element_by_xpath('//*[contains(text(),"Facebook")]').click()
        common_lib.wait(common_lib.__MIDDLE_TIME__, "")
    # end function 
    # *****************************************************************    
    # function for click like page
    def click_like_page(self, driver):
        try:
            self.driver.find_element_by_xpath('//div[@id="substream_1"]//*[contains(text(),"Like Page")]').click()
        except Exception as e:
            print e
        common_lib.wait(common_lib.__MIDDLE_TIME__, "Like Page - Thread %d" % self.thread_id)
    # end function 
    # *****************************************************************    
    # function for click page down
    def click_page_down(self, driver):
        for i in range(0, appconfig.get_number_of_scroll_page()):
            body = driver.find_element_by_css_selector('body')
            body.send_keys(Keys.PAGE_DOWN)
            common_lib.wait(common_lib.__SHORTEST_TIME__, "Page Down - Thread %d" % self.thread_id)
        common_lib.wait(common_lib.__MIDDLE_TIME__, "Page Down - Thread %d" % self.thread_id)
    # end function 
    # *****************************************************************    
    # function for scrolling up and down
    def scroll_page(self, driver, isdown):
        windowsHeight = int(float(driver.execute_script('return window.innerHeight')) * appconfig.get_height_ratio())
        if isdown:
            for i in range(0, windowsHeight, 50):
                scrollTop = int(driver.execute_script('return document.body.scrollTop'))
                scrollHeight = int(driver.execute_script('return document.body.scrollHeight'))
                top = min(scrollTop + 50, scrollHeight)
                driver.execute_script('window.scrollTo(0,'+str(top)+')')
                if i % 400 == 0:
                    common_lib.wait(common_lib.__SHORT_TIME__, "Scroll Down - Thread %d" % self.thread_id)
                else:
                    common_lib.wait(common_lib.__SHORTEST_TIME__, "Scroll Down - Thread %d" % self.thread_id)
        else:
            for i in range(0, windowsHeight, 100):            
                scrollTop = int(driver.execute_script('return document.body.scrollTop'))
                scrollHeight = int(driver.execute_script('return document.body.scrollHeight'))
                top = max(scrollTop - 100, 0)
                if top==0: break
                driver.execute_script('window.scrollTo(0,'+str(top)+')')
                if i % 600 == 0:
                    common_lib.wait(common_lib.__SHORT_TIME__, "Scroll UP - Thread %d" % self.thread_id)
                else:
                    common_lib.wait(common_lib.__SHORTEST_TIME__, "Scroll UP - Thread %d" % self.thread_id)
        
    # end function 
    # *****************************************************************    
    # function for getting time 
    def get_time_from_login(self, login_time):
        return time() - login_time
    # end function
    # *****************************************************************    
    # define thread run function
    # This is thread function user can customize
    # When user execute threadobj.start() function, it will run
    def run(self):
        
        while (True):
            self.night_time = appconfig.get_random_night_time()
            print "Thread " + str(self.thread_id) + "-Start Time - " + str(self.night_time) + "hr"
            while (True):
                if appconfig.is_night_time(self.night_time) == False:
                    break
                else:
                    print "It's Night"                    
                    sleep(3600)
            self.__callback()            
    # end thread run function
    # *****************************************************************    
    # define __callback function
    def __callback(self):
        # login time
        _login_time = time()
        try:
            __login_error__ = False
            try:
                self.driver = self.init_chrome_driver(self.thread_id)
                self.init_chrome_extension(self.driver)
            except Exception as e:
                print e
                __login_error__ = True
                return
            # log on facebook
            try:
                self.log_in_facebook(self.driver)
            except Exception as e:
                print e
                __login_error__ = True
                return
            # click not now button or homepage button
            try:
                self.click_not_now(self.driver)
            except Exception as e:
                print e
                self.click_homepage(self.driver)
            next_time = appconfig.get_next_click_time()
            while(True):
                if appconfig.is_night_time(self.night_time) == True:
                    break
                count_scroll = appconfig.get_number_of_scroll_page()
                if time() > next_time:
                    self.click_like_page(self.driver)
                    next_time = appconfig.get_next_click_time()
                
                while (count_scroll > 0):
                    count_scroll = count_scroll - 1
                    self.click_page_down(self.driver)
                    if appconfig.get_random_select():
                        count_scroll = count_scroll - 1
                        self.scroll_page(self.driver, False)
                
                common_lib.wait(common_lib.__LONGEST_TIME__, "REST - Thread %d" % self.thread_id)
                self.click_homepage(self.driver)

        except Exception as e:
            print e
        finally:
            print "Thread", self.thread_id, ":Stop", ", Running Hour(miniute):", self.get_time_from_login(_login_time)/60
            common_lib.wait(common_lib.__MIDDLE_TIME__, "Exit - Thread %d" % self.thread_id)
            if __login_error__ == False:
                self.driver.close()
                self.driver.quit()
# end class
# login class
class LoginSpider(object):
    def __init__(self, idx):
        self.idx = idx
        co = webdriver.ChromeOptions()
        proxyauth_plugin_path = common_lib.init_proxies(idx)
        co.add_extension(proxyauth_plugin_path)
        co.add_argument("--start-maximized")
        co.add_argument("--disable-infobars")
        co.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome(chrome_options = co)
        self.driver.implicitly_wait(common_lib.__SHORT_TIME__)
        
    def parse(self):
        self.driver.get(appconfig.__APP_URL__)
        common_lib.wait(common_lib.__SHORT_TIME__, "BEFORE LOGIN")
        username = agents.accounts[self.idx].split(':')[0]
        password = agents.accounts[self.idx].split(':')[1]
        print username, password
        self.driver.find_element_by_id('email').send_keys(username)
        common_lib.wait(common_lib.__SHORT_TIME__, "INPUT EMAIL")
        self.driver.find_element_by_id('pass').send_keys(password)
        common_lib.wait(common_lib.__SHORT_TIME__, "INPUT PASSWORD")
        self.driver.find_element_by_xpath('//input[@data-testid="royal_login_button"]').click()
        common_lib.wait(common_lib.__MIDDLE_TIME__, "CLICK LOGIN BUTTON")
        sleep(1000)
    # end function
# end class        
# *****************************************************************
# main function
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode",  type=str, help="mode: login/crawl")
    parser.add_argument("-i", "--idx", type=str, help="proxy id: proxy id must be same with agent id")
    args = parser.parse_args()
    try:
        mode =  re.search('\w+',args.mode).group()
    except Exception as e:
        print "Select correct mode."
    if mode == "crawl":
        print "Start"
        threads = []
        for i in range(common_lib.__THREAD_NUMBER__):
            thrd = ThreadObj(i)
            threads.append(thrd)

        for idx, thrd in enumerate(threads):
            thrd.start()

        for thrd in threads:
            thrd.join()
    elif mode == "login":
        print "Login"
        try:
            idx =  re.search('\d+',args.idx).group()
            spider = LoginSpider(int(idx)-1)
            spider.parse()
        except Exception as e:
            print e
    else:
        print "Error!!!"
# end main function
