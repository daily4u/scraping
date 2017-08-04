# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest
import proxies
import agenties
import random
import base64
import re
class MartialspiderSpider(scrapy.Spider):
    name = 'martialspider'
    allowed_domains = ['www.martialartsclubs.co.uk']
    start_urls = ['http://www.martialartsclubs.co.uk/']

    proxy_lists = proxies.proxys
    ezproxy_lists = proxies.proxies
    useragent_lists = agenties.user_agent_list
    #Request with Proxy & User Agent
    
    def set_proxies(self, url, callback):
        req = Request(url=url, callback=callback,dont_filter=True)

        proxy_url = random.choice(self.proxy_lists)
        # proxy_url = random.choice(self.ezproxy_lists)
        user_pass=base64.encodestring('silicons:1pRnQcg87F').strip().decode('utf-8')
        req.meta['proxy'] = "http://" + proxy_url
        req.headers['Proxy-Authorization'] = 'Basic ' + user_pass
        user_agent = random.choice(self.useragent_lists)
        req.headers['User-Agent'] = user_agent
        return req
    
    def parse(self, response):
        first_url = 'http://www.martialartsclubs.co.uk/SearchResults.aspx'        
        req = self.set_proxies(first_url, self.parse_detail) 
        yield req
    def parse_detail(self,response):
        # print response.body
        res = response.xpath('//table[@id="dgClubs"]/tr')
        print res
        for idx, row in enumerate(res):
            if idx == 0: continue
            print row.xpath('td[4]/a/@href').extract_first()
            argument =re.search("javascript:__doPostBack\(\'(.*?)\'", row.xpath('td[4]/a/@href').extract_first()).group(1)
            print argument
            viewstate =  response.xpath('//input[@id="__VIEWSTATE"]/@value').extract_first()
            print viewstate

            form_data = {
                '__EVENTTARGET':argument,
                '__EVENTARGUMENT':'',
                '__VIEWSTATE':viewstate,
                'Header1$txtHeaderUserName':'',
                'Header1$txtHeaderPassword':'',
                'Search1$txtTown':'',
                'Search1$cboCounty':0,
                'Search1$cboMartialArt':0
            }
            yield FormRequest(url=response.url, formdata=form_data,)