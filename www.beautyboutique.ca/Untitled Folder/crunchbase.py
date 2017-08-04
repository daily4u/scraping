from scrapex import *
import requests
import csv

active_threads = 0

class Crunchspider(object):
    def __init__(self, *args):
        self.so = Scraper(
            use_cache = False,
            retries = 3,
            timeout = 300,
            proxy_file = 'proxies.txt',
            proxy_auth = 'silicons:1pRnQcg87F' 
        )
        
    def parse(self):
        with open('investors.csv','r+') as bank_file:
            reader = csv.DictReader(bank_file)
            for idx, row in enumerate(reader):
                if idx % 20:
                    sleep(10)
                print row['Investor Name URL']
                t = threading.Thread(target=self.parse_detail, args=(row['Investor Name URL'],idx,))
                # self.parse_detail(row['Investor Name URL'],idx)
                # return
    
    def parse_detail(self, url, ind):
    
        # url = 'https://www.crunchbase.com/organization/deep-space-ventures'
        item = []
        invest_category = url.split('/')[3]
        print invest_category
        doc = self.so.load(url)
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
        
        self.so.save(item, 'invest.csv')
        self.parse_investment(url, ind)

            
    def parse_investment(self, url, ind):
        print "SUBITEM"
        url = url + '/investments'
        # print url
        doc = self.so.load(url)
        # companies = []
        # rounds = []
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
            self.so.save(subitem, 'subitem.csv')

if __name__ == '__main__':
    scraper = Crunchspider()
    scraper.parse()
    threads = []
    for i in range(__THREAD_COUNT__):
        threads.append(threading.Thread(target=, args=()))
    for thread in threads:
        thread.start()
        active_threads += 1

    for i in range(__THREAD_COUNT__):
        threads.join()
        active_threads -= 1

    