#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from __future__ import print_function
import sys
import tornado
import re, urlparse
import os
import os.path
import time, datetime
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

start_url = 'https://www.foodtown.com/stores/foodtown-of-old-tappan?next=/shopping#!/'

sc = Scraper(
    use_cache=False,
    retries=3,
    timeout=300,
)
sc_depart = Scraper(
    use_cache=False,
    retries=3,
    timeout=300,
)


class FoodTownScraper(object):
    def __init__(self):
        # self.driver = webdriver.Chrome()
        self.current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1920, 1080)
    
    def parse_depart(self):
        page = 1
        try:
            self.driver.get(start_url)
            WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//div[@class='fp-make-my-store margin-top']/input[@class='fp-btn fp-btn-mystore']")))
            # print self.driver.page_source
            print "==> Click Make This My Store"
            self.driver.find_element_by_xpath("//div[@class='fp-make-my-store margin-top']/input[@class='fp-btn fp-btn-mystore']").click()
            sleep(10)
            print "==> Click Start Shopping"
            read_page = open('page.tmp', 'r')
            page = int(read_page.readline())
            print page
            read_page.close()
            if (page ==0): page=1 
            retries = 0
            while (True):
                self.driver.get('https://www.foodtown.com/shopping#!/?page=%s' % str(page))
                print "==> Go to Shopping"
                print page
                # print self.driver.find_element_by_xpath("//a[@class='fp-is-selected/text()']").text
                print '------------'
                WebDriverWait(self.driver, 60).until(EC.text_to_be_present_in_element((By.XPATH, "//div[@class='fp-paging-list-container']//a[@class='fp-is-selected']"),str(page)))
                print "==> Shopping Page"
                html_doc = Doc(html=self.driver.page_source)
                ret_val = self.parse_items(html_doc)
                if ret_val==0:
                    print "Return value is 0"
                    self.driver.quit()
                    write_page = open('page.tmp', 'w')
                    write_page.write(str(page))
                    write_page.close()
                    print page
                    return -1
                page = page + 1
            print "==> Success"
        except Exception as e:
            print e.message
            write_page = open('page.tmp', 'w')
            write_page.write(str(page))
            write_page.close()
            print page
            print "==> End!"
            return -1

        self.driver.quit()
        return 0
    def parse_items(self, doc):

        li_items = doc.q('//ul[@class="fp-result-list fp-product-list fp-product-list-lg fp-responsive"]//li[@class="fp-item"]')
        for idx, row in enumerate(li_items):
            item_id = row.x('@data-product-id').trim()
            print item_id
            sc_depart.save(["item_id", item_id], 'depart.csv')
            # self.driver.get('https://www.foodtown.com/shopping#!/?id=' + str(item_id))
            # print ('https://www.foodtown.com/shopping#!/?id=' + str(item_id))
            # WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//div[@class='fp-item-image fp-item-image-large']")))
            # html_doc = Doc(html=self.driver.page_source)
            # self.parse_detail(html_doc)
        print "==> Row End"
        return len(li_items)
    
    def parse_detail(self, doc):
        breadcrumbs = doc.q("//ul[@class='fp-breadcrumb']/li/a")
        item = []
        for idx, category in enumerate(breadcrumbs):
            if idx==0: continue
            item.append("Category" + str(idx))
            item.append(category.x('text()').trim())
        item_image = doc.x("//div[@class='fp-item-image fp-item-image-large']/img/@src").trim()
        item.append("image")
        item.append(item_image)
        item_name  = doc.x("//div[@class='fp-item-name']/text()").trim()
        item.append("name")
        item.append(item_name)
        item_price = doc.x("//span[@class='fp-item-base-price']/text()").trim()
        item.append("price")
        item.append(item_price)
        item_size  = doc.x("//span[@class='fp-item-size']/text()").trim()
        item.append("size")
        item.append(item_size)
        item_upc   = doc.x("//div[@class='fp-margin-top-sm fp-item-upc']/text()").trim().replace("SKU/UPC:","").trim()
        item.append("upc")
        item.append(item_upc)
        sc.save(item, 'item_%s.csv' % self.current_time )
        # print "Save"

    
if __name__ == '__main__':
    print "==> Start!"
    while(True):
        scraper = FoodTownScraper()
        ret = scraper.parse_depart() 
        if (ret == 0):
            break
        print "Restart"
