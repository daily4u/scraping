# -*- coding: utf-8 -*-
import scrapy
import useragent
import proxylist
from scrapy.http import Request, FormRequest
from numberspider.items import NumberspiderItem
import time, datetime, csv, random, base64, re, json
from time import sleep


class NumSpider(scrapy.Spider):
    name = "num"

    useragent_lists = useragent.user_agent_list    
    proxy_lists = proxylist.proxys
    def set_proxies(self, url, callback, headers=None, body=None):

        req = Request(url=url, method="POST", callback=callback, dont_filter=True, headers= headers, body=body)

        proxy_url = self.proxy_lists[random.randrange(0,len(self.proxy_lists))]

        user_pass=base64.encodestring(b'jm23:$cartbybot').strip().decode('utf-8')
        req.meta['proxy'] = "http://" + proxy_url
        req.headers['Proxy-Authorization'] = 'Basic ' + user_pass

        user_agent = self.useragent_lists[random.randrange(0, len(self.useragent_lists))]
        req.headers['User-Agent'] = user_agent

        return req
    def start_requests(self):

        print "======= Start ========"

        headers = {
            'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0',
            'Accept':'*/*',
            'Accept-Language':'en-US,en;q=0.5',
            'Accept-Encoding':'gzip, deflate, br',
            'Content-Type':'application/x-www-form-urlencoded;charset=utf-8',
            'Referer':'https://search.google.com/structured-data/testing-tool/',
        }
        payload = "url=https://www.linkedin.com/company/%2776-to-present"
        url = "https://search.google.com/structured-data/testing-tool/validate"
        req = self.set_proxies(url, self.getData, headers, payload)
        yield req

    def getData(self, response):
        print "====== Get Data ======="
        print response.body
        return
