#!/usr/bin/env python

import re, urlparse

from selenium import webdriver
from scrapex import *
from time import sleep
import requests
import json

link = 'https://www.ctownsupermarkets.com/Weekly-Circular'
sc = Scraper(
    use_cache=False,
    retries=3,
    timeout=300,
)

class CtownScraper(object):
    def __init__(self):
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1920, 1080)

    def parse(self):
        postal_code = "07675"
        # store_code = ['U41_196', 'U41_568', 'PU41_324', 'PU41_405', 'PS41_227']
        self.driver.get(link)
        print '------1-------'
        sleep(3)
        try:
            self.driver.find_element_by_id('postal_code_input').send_keys(postal_code)
        except:
            pass
        print '------2-------'
        sleep(1)
        try:
            self.driver.find_element_by_id('submit_postal_code').click()
        except:
            pass
        print '------3-------'
        sleep(3)
        try:
            self.driver.find_element_by_class_name('submit_store_select').click()
        except:
            pass
        print '------4-------'
        sleep(3)
        doc = sc.load_html('https://circular.ctownsupermarkets.com/flyers/ctown?type=2&postal_code=07675&store_code=U41_196&is_store_selection=true&auto_flyer=&sort_by=')
        
        flyBody = json.loads(re.search("window\[\'hostedStack\'\] = \[(.*?)\];", doc, re.S|re.M|re.I).group(1))
        
        flyer_run_id = flyBody['flyer_run_id']

        currenct_flyer_id = flyBody['current_flyer_id']

        itemdata = requests.get('https://circular.ctownsupermarkets.com/flyer_data/%s?locale=en-US' % currenct_flyer_id).json()
        for row in itemdata['items']:
            good_item = []
            good_item.append('brand')
            good_item.append(row['brand'])
            good_item.append('current_price')
            good_item.append(row['current_price'])
            good_item.append('description')
            good_item.append(row['description'])
            good_item.append('disclaimer_text')
            good_item.append(row['disclaimer_text'])
            good_item.append('discount_percent')
            good_item.append(row['discount_percent'])
            good_item.append('display_name')
            good_item.append(row['display_name'])
            good_item.append('flyer_id')
            good_item.append(row['flyer_id'])
            good_item.append('flyer_item_id')
            good_item.append(row['flyer_item_id'])
            good_item.append('flyer_run_id')
            good_item.append(row['flyer_run_id'])
            good_item.append('flyer_type_id')
            good_item.append(row['flyer_type_id'])
            good_item.append('in_store_only')
            good_item.append(row['in_store_only'])
            good_item.append('merchant_id')
            good_item.append(row['merchant_id'])
            good_item.append('name')
            good_item.append(row['name'])
            good_item.append('run_item_id')
            good_item.append(row['run_item_id'])
            good_item.append('sale_story')
            good_item.append(row['sale_story'])
            good_item.append('sku')
            good_item.append(row['sku'])
            good_item.append('url')
            good_item.append(row['url'])
            good_item.append('valid_from')
            good_item.append(row['valid_from'])
            good_item.append('valid_to')
            good_item.append(row['valid_to'])
            good_item.append('x_large_image_url')
            good_item.append(row['x_large_image_url'])
            good_item.append('large_image_url')
            good_item.append(row['large_image_url'])

            sc.save(good_item, 'product.csv')
        self.driver.quit()

if __name__ == '__main__':
    scraper = CtownScraper()
    scraper.parse()