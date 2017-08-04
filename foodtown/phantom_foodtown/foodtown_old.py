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

        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1920, 1080)
    
    def parse_depart(self, depart_enable):
        try:
            self.driver.get(start_url)
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//div[@class='fp-make-my-store margin-top']/input[@class='fp-btn fp-btn-mystore']")))
            # print self.driver.page_source
            print "==> Click Make This My Store"
            self.driver.find_element_by_xpath("//div[@class='fp-make-my-store margin-top']/input[@class='fp-btn fp-btn-mystore']").click()
            sleep(10)
            print "==> Click Start Shopping"
            page = 1
            while (True):
                print page
                self.driver.get('https://www.foodtown.com/shopping#!/?page=%s&limit=48' % str(page))
                print "==> Go to Shopping"
                WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//ul[@class='fp-result-list fp-product-list fp-product-list-lg fp-responsive']")))
                print "==> Shopping Page"
                html_doc = Doc(html=self.driver.page_source)
                self.parse_items(html_doc)
                page = page + 1
            print "==> Success"
        except Exception as e:
            print e.message
        finally:
            print "==> End!"

        self.driver.quit()

    def parse_items(self, doc):

        li_items = doc.q('//ul[@class="fp-result-list fp-product-list fp-product-list-lg fp-responsive"]//li[@class="fp-item"]')
        for idx, row in enumerate(li_items):
            item_id = row.x('@data-product-id').trim()
            self.driver.get('https://www.foodtown.com/shopping#!/?id=' + str(item_id))
            
            # print ('https://www.foodtown.com/shopping#!/?id=' + str(item_id))
            # WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//div[@class='fp-item-image fp-item-image-large']")))
            # html_doc = Doc(html=self.driver.page_source)
            # self.parse_detail(html_doc)

        print "==> Row End"
    
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
        sc.save(item, 'item.csv')
    
if __name__ == '__main__':
    print "==> Start!"
    scraper = FoodTownScraper()
    scraper.parse_depart(True)

