from scrapex import *
import requests
import csv
import time
import random
import json
import threading
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common import exceptions as EX
from selenium.webdriver.chrome.options import Options
import logging
import sys

reload(sys)  
sys.setdefaultencoding('utf8')

lock = threading.Lock()

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
so = Scraper(
    use_cache = False,
    retries = 3,
    timeout = 300,
    proxy_file = 'proxies.txt',
    proxy_auth = 'silicons:1pRnQcg87F'
)

def load_lines(path):
    with open(path, 'rb') as f:
        return [line.strip() for line in
                f.read().decode('utf8').splitlines()
                if line.strip()]

# ROTATING_PROXY_LIST = load_lines('proxies.txt')
# AGENT_LIST  = load_lines('agents.txt')

def init_phantom_driver():
    # to set up arguments and extensions for chrome options
    # idx = random.randrange(1,20)
    service_args = [
        '--ignore-ssl-errors=true',
        '--ssl-protocol=any',
        '--proxy=46.101.204.69:3128',
        '--proxy-type=socks5',
        '--proxy-auth=ofirseo:a1qs2wd3ef4r'
    ]
    driver = webdriver.PhantomJS(service_args=service_args)
    driver.implicitly_wait(1)

    return driver

def main():
    threads_number = 1
    threads = []

    initial_urls = 'https://search.google.com/structured-data/testing-tool/u/0/'
    # with open('directories.csv','rb') as f:
    #     content = csv.reader(f)
    #     directories = list(content)
    directories = ["google","microsoft"]
    driver_lists = []

    for i in range(0, threads_number):
        driver_obj = init_phantom_driver()
        driver_lists.append(driver_obj)

    while len(directories) > 0:
        if len(threads) < threads_number:
            driver_obj = driver_lists[len(threads) % threads_number]
            item = directories.pop(0)

            thread_obj = threading.Thread(target=parse_detail,args=(item, driver_obj))
            threads.append(thread_obj)
            thread_obj.start()

        for thread in threads:  
            if not thread.is_alive():
                thread.join()
                threads.remove(thread)

def parse_detail(item, driver):
    slug = item
    print slug
    site_url = 'https://search.google.com/structured-data/testing-tool/u/0/#url=https://linkedin.com/company/{}'.format(slug)
    # site_url = 'https://icanhazip.com'
    print site_url
    driver.get(site_url)
    print "+++++++++++++++"
    try:
        WebDriverWait(driver, 20).until(EC.text_to_be_present_in_element_value((By.XPATH, '//div[@id="results-cell"]/div/div/div/div/span'),"Detected"))
    except Exception as e:
        print e
    print(driver.page_source.encode("utf-8"))        
    return
    print "---------------"
if __name__ == '__main__':
    main()