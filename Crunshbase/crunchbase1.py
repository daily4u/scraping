from scrapex import *
import requests
import csv
import time
import random
import threading
active_threads = 0
tlock = threading.Lock()
so = Scraper(
    use_cache = False,
    retries = 3,
    timeout = 300,
)
current_proxies_pool = []
def load_lines(path):
    with open(path, 'rb') as f:
        return [line.strip() for line in
                f.read().decode('utf8').splitlines()
                if line.strip()]

ROTATING_PROXY_LIST = load_lines('proxies.txt')
AGENT_LIST  = load_lines('agents.txt')

def main():
    global active_threads
    global current_proxies_pool
    threads = []
    
    initial_url = 'https://www.crunchbase.com/app/search/investors'
    useragent = random.choice(AGENT_LIST)
    print useragent

    proxy = random.choice(ROTATING_PROXY_LIST)

    with open('investors.csv','r+') as bank_file:
        reader = csv.DictReader(bank_file)
        total = 0
        for idx, row in enumerate(reader):
            total +=1
            # t = threading.Thread(target=parse_detail, args=("http://webcache.googleusercontent.com/search?q=cache:" + row['Investor Name URL'],row['ID'],))
            t = threading.Thread(target=parse_detail, args=(row['Investor Name URL'],row['ID'],))
            threads.append(t)
        i = 1585
        while(i < total):
            if active_threads < 40:
                threads[i].start()
                active_threads += 1
                i += 1
                if (i % 10 == 0):
                    time.sleep(random.randint(50,90))
                    tlock.acquire()
                    
                    if len(current_proxies_pool) > 20:
                        print current_proxies_pool
                        current_proxies_pool = []

                    tlock.release()
            
        for thread in threads:
            thread.join()

def parse_detail(url, ind):
    global current_proxies_pool
    tlock.acquire()
    print "|=>=>=> ",url
    tlock.release()
    # url = 'https://www.crunchbase.com/organization/deep-space-ventures'
    item = []
    # invest_category = url.split('/')[6]
    invest_category = url.split('/')[3]
    # port=22225
    # session_id = random.random()
    # proxy = '46.101.204.69:3128'
    proxy = random.choice(ROTATING_PROXY_LIST)
    while True:
        if proxy in current_proxies_pool:
            proxy = random.choice(ROTATING_PROXY_LIST)
            current_proxies_pool.append(proxy)
        else:
            break
    

    proxies = dict(http='http://jm23:$cartbybot@'+proxy,https='http://jm23:$cartbybot@'+proxy)

    useragent = random.choice(AGENT_LIST)
    headers = {
        'Host':'www.crunchbase.com',
        'User-Agent':useragent,
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer':'https://www.crunchbase.com/',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'en-US,en;q=0.8'
    }

    s = requests.Session()
    s.cookies.clear()
    res = s.get(url,proxies=proxies, headers=headers)
    tlock.acquire()
    print "1:", proxy, ind, res.status_code
    tlock.release()

    doc = Doc(html=res.text)
    # doc = so.load(url)
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
    
    so.save(item, 'invest.csv',remove_existing_file=False)
    parse_investment(url, ind)
# 87, 96,   
def parse_investment(url, ind):
    global current_proxies_pool
    global active_threads
    time.sleep(random.randint(3,6))
    url = url + '/investments'
    # print url
    proxy = random.choice(ROTATING_PROXY_LIST)

    while True:
        if proxy in current_proxies_pool:
            proxy = random.choice(ROTATING_PROXY_LIST)
            current_proxies_pool.append(proxy)
        else:
            break
    proxies = dict(http='http://jm23:$cartbybot@'+proxy,https='http://jm23:$cartbybot@'+proxy)
    useragent = random.choice(AGENT_LIST)
    headers = {
        'Host':'www.crunchbase.com',
        'Connection':'keep-alive',
        'Cache-Control':'max-age=0',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':useragent,
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer':'https://www.crunchbase.com/',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'en-US,en;q=0.8'
    }
   
    s = requests.Session()
    s.cookies.clear()
    res = s.get(url, proxies=proxies, headers=headers)
    tlock.acquire()
    print "2:", proxy, ind, res.status_code
    tlock.release()
    doc = Doc(html=res.text)

    trs = doc.q('//table[@class="section-list table investors"]/tr')
    for row in trs:
        subitem = []
        subitem.append("ParentID")
        subitem.append(ind)
        org = row.x('td[2]/a/@href').trim()
        # companies.append(org)
        subitem.append("Companies")
        subitem.append(org)
        rnd = row.x('td[3]/a/@href').trim()
        # rounds.append(rnd)
        subitem.append("Rounds")
        subitem.append(rnd)
        so.save(subitem, 'subitem.csv',remove_existing_file=False)
    active_threads -= 1
if __name__ == '__main__':
    main()