# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from myhammer.items import MyhammerItem
import re
import proxies
import agenties
import random, base64

class MyhammerspiderSpider(scrapy.Spider):
    name = 'myhammerspider'
    allowed_domains = ['www.my-hammer.de']
    parent_url = 'https://www.my-hammer.de'
    start_urls = [
        'https://www.my-hammer.de/empfehlung/b/in/Karlsruhe/?searchRadius=999&submittedByForm=1',
        'https://www.my-hammer.de/empfehlung/a/in/Karlsruhe/?searchRadius=999&submittedByForm=1',
        'https://www.my-hammer.de/empfehlung/d/in/Karlsruhe/?searchRadius=999&submittedByForm=1'
    ]

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
        profile_url = response.xpath('//a[@title="Profil anzeigen"]/@href').extract()
        for row in profile_url:
            try:
                req = self.set_proxies(self.parent_url + row,  self.parse_profile)
                # req = Request(url=self.parent_url + row,  callback=self.parse_profile, dont_filter=True)
                yield req
            except:
                pass
        
        next_url = response.xpath('//a[@title="Seite vor"]/@href').extract_first()
        if next_url:
            req = self.set_proxies(self.parent_url + next_url,  self.parse)
            # req = Request(url=self.parent_url + next_url,  callback=self.parse, dont_filter=True)
            yield req
    
    def parse_profile(self, response):
        website_url = response.xpath('//a[@class="directoryProfileUrlTracking"]/@href').extract_first()
        if website_url == None:
            return
        if 'google' in website_url:
            return
        try:
            req = Request(url=website_url, callback=self.parse_individual,  dont_filter=True)
            yield req
        except:
            return
    

    def parse_individual(self, response):
        print response.url
        iswp = False
        wordpress_version = ""
        if ("wp-content" in response.body) and ("wp-includes" in response.body):
            iswp = True
            try:
                wp_versions = response.xpath('//meta[@name="generator"]/@content').extract()
                for wp_vs in wp_versions:
                    if "wordpress" in wp_vs.lower():
                        try:
                            wordpress_version = re.search("(\d+\.\d+\.\d+)", wp_vs, re.M|re.S).group(1)
                            print wordpress_version
                            break
                        except:
                            wordpress_version = ""
            except:
                pass
        item = MyhammerItem()
        item['url'] = response.url
        item['iswp'] = iswp
        item['wp_version'] = wordpress_version
        yield item
