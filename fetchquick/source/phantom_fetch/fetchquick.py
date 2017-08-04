#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from __future__ import print_function
import sys
import tornado
import re, urlparse
import os
import os.path
import time
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common import exceptions as EX

from scrapex import *
import numpy as np
from time import sleep
import requests
import json, csv

start_url = 'http://fetchquick.com/'

sc = Scraper(
    use_cache=False,
    retries=3,
    timeout=300,
)
sc_item = Scraper(
    use_cache=False,
    retries=3,
    timeout=300,
)

class AnyEc:
    """ Use with WebDriverWait to combine expected_conditions
        in an OR.
    """
    def __init__(self, *args):
        self.ecs = args

    def __call__(self, driver):
        for fn in self.ecs:
            try:
                if fn(driver): return True
            except:
                pass

class FetchQuickScraper(object):
    def __init__(self):
        # self.driver = webdriver.Chrome()

        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1920, 1080)
    
    def parse_depart(self, depart_enable):

        self.zipcode = '10010'
        try:
            self.driver.get(start_url)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@name='store_enter_zip_code']")))
            # print self.driver.page_source
            print "==> Input Zip Code"
            self.driver.find_element_by_xpath("//input[@name='store_enter_zip_code']").send_keys(self.zipcode)
            sleep(2)
            print "==> Click Start Shopping"
            self.driver.find_element_by_id('edit-submit').click()
            sleep(10)
            print "==> Enter Option Page"

            if depart_enable:
                self.parse_item()
                return

            self.driver.get(url='https://fetchquick.com/content/home')
            WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//section[@id="block-department-menu-department-tree"]')))
            print "==> Home Page"
            html_doc = Doc(html=self.driver.page_source)
            self.get_depart_of_items(html_doc)
            print "==> Success"
        except:
            print "==> Timeout!"
        finally:
            print "==> End!"
        self.parse_item()

    def get_depart_of_items(self, doc):
        
        print "Get Depart of Items:     =============> Processing"
        li_items = doc.q('//section[@id="block-department-menu-department-tree"]//div[@id="mCSB_1_container"]/ul/li')
        print "*********************"
        print len(li_items)

        for idx, row in enumerate(li_items):
            if idx<2: continue
            parent_name = row.x('a[@class="parent-item dc-mega"]/text()').trim()
            print "==> Row:%s : %s" % (str(idx), parent_name)
            parent_url    = row.x('a[@class="parent-item dc-mega"]/@href').trim()
            parent_no     = re.search("\/departments\/(.*?)\/", parent_url, re.S|re.M).group(1)
            
            child_items = row.q('.//div[@class="sub-container mega"]/ul/div/li/ul/li')
            if len(child_items) == 0:
                child_items = row.q('.//div[@class="sub-container mega dropdown_second_row"]/ul/div/li/ul/li')
            print "==> Childs Count: %s" % str(len(child_items))
            for col in child_items:
                print "==========> Col:%s" % str(idx)
                depart_item = []
                child_name  = col.x('a/text()').trim()
                child_url = col.x('a/@href').trim()
                child_no     = re.search("\/departments\/(.*?)\/", child_url, re.S|re.M).group(1)
                depart_item = ["PID" , parent_no, "CID" , child_no, "PNAME", parent_name,  "CNAME", child_name,"PURL", parent_url, "CURL", child_url]
                sc.save(depart_item, 'depart.csv')
                print "==========> Save %s:%s : %s" % (str(parent_no), str(child_no), child_name)
        print "==> Row End"
    
    def parse_item(self):
        print "==> Parse Items"
        start_row = 1
        if os.path.exists('item.csv'):
            with open('item.csv','rb') as item_file:
                item_reader = csv.reader(item_file)
                item_list = list(item_reader)
            item_list = np.array(item_list)
            item_list = item_list[:,:2]
            item_list = map(np.asarray, set(map(tuple, item_list)))
            start_row = len(item_list)
            os.rename("item.csv", time.strftime("item_%Y%m%d%H%M%S.csv"))

        with open('depart.csv','rb') as csvfile:
            reader = csv.reader(csvfile)
            categories = list(reader)        
        
        for idx, row in enumerate(categories):
            print "===>" + row[0] + ":" + row[1]
            if idx<start_row: continue
            
            self.driver.get(start_url + row[5])
            sleep(1)
            try:
                WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//ul[contains(@class,'pager pager--infinite-scroll')]")))
            except EX.TimeoutException:
                pass

            while True:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(1)
                try:
                    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'views_infinite_scroll-ajax-loader')]/img")))
                except EX.TimeoutException:
                    break
            print "===> Load all page"
            print "===> Get Data from loaded page"
            html_doc = Doc(html=self.driver.page_source)

            items = html_doc.q("//div['view-content']/div[contains(@class,'views-responsive-grid')]/div[contains(@class,'views-row')]/div[contains(@class,'views-column')]")

            print len(items)
            for col in items:
                item_image_url = col.x(".//div[@class='product_image']/a/img/@src").trim()
                item_price = col.x(".//div[@class='product_price']/a/text()").trim()
                item_name = col.x(".//div[@class='product_title']/a/text()").trim()
                good_item = ["Category",row[2],"Subcategory",row[3],"Item",item_name,"Price",item_price,"Image",item_image_url]
                sc_item.save(good_item, 'item.csv')
        self.driver.quit()
        return
    
if __name__ == '__main__':
    print "==> Start!"
    scraper = FetchQuickScraper()
    scraper.parse_depart(True)


# WebDriverWait(driver, 10).until(
#     AnyEc(
#         EC.presence_of_element_located((By.XPATH, '//ul[@cl="ctl00_BodyContent_MCRL_Grid"]/table/tbody/tr')),
#         EC.presence_of_element_located((By.XPATH, '//span[@id="ltlTechInfo"]/table'))
#     )
# )

