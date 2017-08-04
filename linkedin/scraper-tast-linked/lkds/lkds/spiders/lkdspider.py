# -*- coding: utf-8 -*-
import scrapy
import useragent
import proxylist
from scrapy.http import Request, FormRequest
from scrapy.http.cookies import CookieJar
from scrapy.selector import Selector
import time, datetime, csv, random, base64, re, json
from time import sleep
from lkds.items import LkdsItem
import requests
import random
# import txt_dict

class LkdspiderSpider(scrapy.Spider):
    name = 'lkdspider'
    useragent_lists = useragent.user_agent_list    
    proxy_lists = proxylist.proxys
    
    start_urls = ('https://search.google.com/structured-data/testing-tool/u/0/')
    current_number = 200
    def set_proxies(self, url, method , callback, body=None):
        print "++++++++++++++++++++++++++++++"
        req = scrapy.Request(url=url, method=method, callback=callback, body=body,dont_filter=True,meta={'dont_merge_cookies': True})
        proxy_url = self.proxy_lists[random.randrange(0,len(self.proxy_lists))]
        user_pass=base64.b64encode('ofirseo:a1qs2wd3ef4r').strip().decode('utf-8')
        req.meta['proxy'] = "http://46.101.204.69:3128"  
        req.headers['Proxy-Authorization'] = 'Basic ' + user_pass
        user_agent = self.useragent_lists[random.randrange(0, len(self.useragent_lists))]
        req.headers['User-Agent'] = user_agent
        return req
    
    def start_requests(self):
        req = self.set_proxies(self.start_urls, 'POST', self.parse)
        yield req
    def parse(self, response):
        print "+++++++++++++++++++++++++++++++++"
        # print response.body

        with open('directories.csv','rb') as f:
            content = csv.reader(f)
            directories = list(content)
            for ind, row in enumerate(directories):
                if self.current_number >= ind:
                    continue
                if ind % random.randint(6,20) == 4:
                    time.sleep(random.randint(10, 60))
                    self.current_number = ind
                    req = self.set_proxies(self.start_urls, 'POST', self.parse)
                    yield req
                    return

                slug_url = row[0]

                payload = "url=https://www.linkedin.com/company/%s" % row[0]
                url = "https://search.google.com/structured-data/testing-tool/validate"

                req = self.set_proxies(url, 'POST', self.getData, payload)
                req.meta["slug"] = slug_url

                req.headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8'
                req.headers['Referer'] = 'https://search.google.com/structured-data/testing-tool/'
                time.sleep(random.randint(3, 40))
                yield req
                print "-----------------------------------"

    def getData(self, response):
        print '**********************************'
        print response.body
        if response.status != 200 or "not-found-404" in response.body:
            item = LkdsItem()
            Slug = response.meta['slug']
            yield item
            return
        print "====== Get Data ======="
        # print response.body
        try:
            if json.loads(response.body.replace(")]}'", ""))['fetchError'].strip() == "NOT_FOUND":
                print "Invalid URL"
                return
        except Exception as e:
            print e
        try:
            linkd_html_txt = json.loads(response.body.replace(")]}'", ""))['html'].replace('\n','')
        except: 
            print 'Invalid URL'
            return

        # linkd_html_doc = Selector(text = linkd_html_txt)
        try:
            company_data = json.loads(re.search('<code id="stream-right-rail-embed-id-content"><!--(.*?)--></code>', linkd_html_txt, re.S|re.M).group(1))
        except:
            print 'No Content'
            return
        item = LkdsItem()
        try:
            Slug = company_data["homeUrl"].split("/")[-1]
        except:
            Slug = None
        item["slug"] = Slug
        try:
            Name = company_data["companyName"]
        except:
            Name = None
        item["name"] = Name

        try:
            Logo = company_data["legacyLogo"]
        except:
            Logo = None
        item["logo_url"] = Logo
        
        try:
            Beta_id = company_data["companyId"]
        except:
            Beta_id = None
        item["betaId"] = Beta_id

        try:
            Description = company_data["description"].replace("\r\n"," ").strip()
        except:
            Description = None
        item["description"] = Description


        try:
            companyType = company_data["companyType"]
        except:
            companyType = None
        item["company_type"] = companyType

        try:
            Type = company_data["type"]
        except:
            Type = None
        item["type"] = Type

        try:
            Street1 = company_data["headquarters"]["street1"]
        except:
            Street1 = None
        item["street1"] = Street1

        try:
            Street2 = company_data["headquarters"]["street2"]
        except:
            Street2 = None
        item["street2"] = Street2

        try:
            City = company_data["headquarters"]["city"]
        except:
            City = None
        item["city"] = City

        try:
            State = company_data["headquarters"]["state"]
        except:
            State = None
        item["state"] = State

        try:
            Country = company_data["headquarters"]["country"]
        except:
            Country = None

        item["country"] = Country
        try:
            Postal_code = company_data["headquarters"]["zip"]
        except:
            Postal_code = None
        item["postalCode"] = Postal_code

        try:
            Industry = company_data["industry"]
        except:
            Industry = None
        item["industry"] = Industry

        try:
            Company_Size = company_data["size"]
            if Company_Size == "Myself Only":
                Company_Size = 1
        except:
            Company_Size = None
        item["size"] = Company_Size

        try:
            Founded = company_data["yearFounded"]
        except:
            Founded = None
        item["founded_year"] = Founded

        try:
            Specialties = "," .join(company_data["specialties"]).strip()
        except:
            Specialties = None
        item["specialties"] = Specialties

        try:
            Website = company_data["website"]
        except:
            Website = None
        item["website"] = Website

        try:
            print company_data["showcasePages"]
            showcase =  ','.join(str(ro["id"]) for ro in company_data["showcasePages"]).strip()
        except Exception as e:
            print e
            showcase = None

        item["showcase"] = showcase
        try:
            employees = json.dumps(company_data["employees"])
        except:
            employees = None
        item["employees"] = employees
        try:
            print company_data["alsoViewed"]
            related_orgs =  ','.join(str(ro["id"]) for ro in company_data["alsoViewed"]).strip()
        except Exception as e:
            print e
            related_orgs = None
        item["related_orgs"] = related_orgs
        try:
            print company_data["affiliated"]
            affiliated_orgs =  ','.join(str(ro["id"]) for ro in company_data["affiliated"]).strip()
        except Exception as e:
            print e
            affiliated_orgs = None
        item["affiliated_orgs"] = affiliated_orgs
        
        yield item

        print '/////////////////////////////////////'