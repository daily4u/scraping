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
import re
import math

import config

active_threads = 0

so = Scraper(
    use_cache = False,
    retries = 3,
    timeout = 300,
)
so2 = Scraper(
    use_cache = False,
    retries = 3,
    timeout = 300,
)

def load_lines(path):
    with open(path, 'rb') as f:
        return [line.strip() for line in
                f.read().decode('utf8').splitlines()
                if line.strip()]

ROTATING_PROXY_LIST = load_lines('proxies.txt')
AGENT_LIST  = load_lines('agents.txt')

def init_chrome_driver(idx):
    # to set up arguments and extensions for chrome options
    idx = random.randrange(1,20)
    co = webdriver.ChromeOptions()
    proxyauth_plugin_path = config.init_proxies(idx)
    co.add_extension(proxyauth_plugin_path)
    co.add_argument("--start-maximized")
    co.add_argument("--disable-infobars")
    co.add_argument("--disable-notifications")
    driver = webdriver.Chrome(chrome_options = co)
    driver.implicitly_wait(config.__SHORT_TIME__)
    return driver

def main():
    global active_threads
    threads = []
    # drivers = []
    # initial_url = 'https://www.crunchbase.com/app/search/investors'
    # s = requests.Session()
    # s.cookies.clear()
    # useragent = random.choice(AGENT_LIST)
    # headers = {
    #     'Host':'www.crunchbase.com',
    #     'Connection':'keep-alive',
    #     'Cache-Control':'max-age=0',
    #     'Upgrade-Insecure-Requests':'1',
    #     'User-Agent':useragent,
    #     'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    #     'Referer':'https://www.crunchbase.com/',
    #     'Accept-Encoding':'gzip, deflate, br',
    #     'Accept-Language':'en-US,en;q=0.8'
    # }
    # proxy = random.choice(ROTATING_PROXY_LIST)
    # proxy = dict(http='http://jm23:$cartbybot@'+proxy)
    # res = s.request('GET', 'http://lumtest.com/myip.json', proxies=proxy)
    # s.cookies.clear()
    # print "+++ IP address:", json.loads(res.text)["ip"]
    # res = s.request('GET', initial_url, headers=headers, proxies=proxy)
    # print res.text
    # parse_detail('https://www.crunchbase.com/organization/deep-space-ventures',0)
    # return
    with open('investors.csv','r+') as bank_file:
        reader = csv.DictReader(bank_file, delimiter=',')
        total = 0
        for idx, row in enumerate(reader):
            # driver = init_chrome_driver(int(ind) % 20) 
            total +=  1
            t = threading.Thread(target=parse_detail, args=(row['Investor Name URL'],row['ID'],))
            threads.append(t)
        ii = 0
        while(ii<total):
            if active_threads < 5:
                threads[ii].start()
                active_threads += 1
                ii += 1
                time.sleep(1)
            
        for thread in threads:
            thread.join()

def parse_detail(_url, ind):
    driver = init_chrome_driver(int(ind) % 20)
    driver.get(_url)

    print "++++++++++++++++1+++++++++++++++++"

    try:
        driver.WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//a[@title="All Investments"]')))
    except:
        pass
    print "++++++++++++++++++++++++++++++++++"
    item = []
    invest_category = _url.split('/')[3]
    # print invest_category
    # res = ses.request('GET',url, proxies=proxy, headers=headers)
    # print res.text
    doc = Doc(html=driver.page_source)
    name = doc.x('//h1[@id="profile_header_heading"]/a/text()')
    overviews = doc.q('//dt')
    headquarters =""
    website =""
    facebook_url =""
    twitter_url =""
    linkedin_url =""
    founded =""
    aliases =""
    contact =""
    investment_size =""
    ttype =""
    sectors =""
    regions =""

    for row in overviews:
        ttt = row.x("text()").trim()
        if ttt == "Headquarters:":
            headquarters = row.x("following-sibling::dd[1]/text()").trim()
        elif ttt == "Website:":
            website = row.q("following-sibling::dd[1]/a/@href").join(', ').trim()
        elif ttt == "Social:":
            facebook_url = row.x('following-sibling::dd[1]/a[@class="icons facebook"]/@href').trim()
            twitter_url = row.x('following-sibling::dd[1]/a[@class="icons twitter"]/@href').trim()
            linkedin_url = row.x('following-sibling::dd[1]/a[@class="icons linkedin"]/@href').trim()
        elif ttt == "Founded:":
            founded = row.x("following-sibling::dd[1]/text()").trim()
        elif ttt == "Aliases:":
            aliases = row.x("following-sibling::dd[1]/text()").trim()
        elif ttt == "Contact:":
            contact = row.x("following-sibling::dd[1]/span/a/text()").trim()
        elif ttt == "Type:":
            ttype = row.x("following-sibling::dd[1]/text()").trim()
        elif ttt == "Investment Size:":
            investment_size = row.x("following-sibling::dd[1]/text()").trim()
        elif ttt == "Sectors:":
            sectors = row.x("following-sibling::dd[1]/text()").trim()
        elif ttt == "Regions:":
            regions = row.x("following-sibling::dd[1]/text()").trim()

    item.append("ID")
    item.append(ind)
    item.append("Category")
    item.append(invest_category)
    item.append("Name")
    item.append(name)
    item.append("Headquarters")
    item.append(headquarters)
    item.append("Website")
    item.append(website)
    item.append("Facebook")
    item.append(facebook_url)
    item.append("Twitter")
    item.append(twitter_url)
    item.append("Linkedin")
    item.append(linkedin_url)
    item.append("Founded")
    item.append(founded)
    item.append("Aliases")
    item.append(aliases)
    item.append("Contact")
    item.append(contact)
    item.append("Type")
    item.append(ttype)
    item.append("Investment Size")
    item.append(investment_size)
    item.append("Sectors")
    item.append(sectors)
    item.append("Regions")
    item.append(regions)
    print item
    collection_count = re.search("\d+", doc.x('//h2[@id="investments"]/span[@class="collection-count"]/text()').replace(","), re.S|re.M).group()
    print collection_count
    print "+++++++++++++++2++++++++++++++++++"
    so.save(item, 'invest.csv')
    __url = _url + '/investments?page={}'
    parse_investment(__url, ind, driver, collection_count)
        
def parse_investment(_url, ind, driver, cnt):
    global active_threads
    print "SUBITEM"
    # print url
    # res = ses.request('GET',url, proxies=proxy)
    print "+++++++++++++++3++++++++++++++++++"
    for i in range(1, int(math.ceil(float(cnt)/40))):
        print i
        # curl = url "/investments?page={}".format(i))
        print _url
        driver.get(_url.format(str(i)))
        print "+++++++++"
        # driver.implicitly_wait(5)
        # time.sleep(3)
        try:
            driver.WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, '//h2[@id="investments"]')))
        except:
            print "Timeout"
        
        print "++++++++++++++++++4+++++++++++++++++++"
        doc = Doc(html=driver.page_source)
        # companies = []
        # rounds = []
        trs = doc.q('//table[@class="section-list table investors"]/tbody/tr')

        for row in trs:
            subitem = []
            aurl = row.q('td/a')
            org = "-"
            rnd = "-"
            psn = "-"
            for url in aurl:
                _xpath = url.x("@href").trim()
                if "organization" in _xpath:
                    org = _xpath
                elif "funding-round" in _xpath:
                    rnd = _xpath
                elif "person" in _xpath:
                    psn = _xpath
            subitem.append("ID")                    
            subitem.append(ind)                    
            subitem.append("Organization")
            subitem.append(org)                    
            subitem.append("Round")                    
            subitem.append(rnd)                    
            subitem.append("Person")
            subitem.append(psn)                 
            print subitem
            so2.save(subitem, 'subitem.csv')
        print "++++++++++++++++++5+++++++++++++++++++"
    print "++++++++++++++++++6+++++++++++++++++++"
    driver.close()
    driver.quit()
    active_threads -=1
if __name__ == '__main__':
    main()