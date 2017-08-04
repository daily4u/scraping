# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import re
from netronline.items import NetronlineItem

class NetronlinespiderSpider(scrapy.Spider):
    name = 'netronlinespider'
    allowed_domains = ['www.netronline.com']
    start_urls = ['http://www.netronline.com/']
    public_records_url = "http://publicrecords.netronline.com"
    state_template_url = "http://publicrecords.netronline.com/state/%s/"
    county_template_url = "http://publicrecords.netronline.com/state/%s/county/%s/"
    states = ['AK','AL','AR','AZ','CA','CO','CT','DC','DE','FL','GA','HI','IA','ID','IL','IN','KS','KY','LA','MA','MD','ME','MI','MN','MO','MS','MT','NC','ND','NE','NH','NJ','NM','NV','NY','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VA','VT','WA','WI','WV','WY']
    
    def parse(self, response):
        for state in self.states:
            state_url = self.state_template_url % state
            req = Request(url=state_url, callback=self.parse_county, dont_filter=True)
            yield req

    def parse_county(self, response):
        counties = response.xpath('//div[@class="hotbox-title"]/following-sibling::div[1]//ul/li/a')
        for county in counties:
            county_url  = county.xpath('@href').extract_first()
            county_text = county.xpath('text()').extract_first()
            req = Request(url=self.public_records_url + county_url, callback=self.parse_detail, dont_filter=True)
            yield req
    
    def parse_detail(self, response):
        title  = response.xpath('//title/text()').extract_first()
        title = re.sub('[^\x00-\x7F]+', ',', title.split(',')[0]).strip()
        state  = title.split(',')[1].strip()
        county  = title.split(',')[2].replace('Public Records', '').strip()
        # print state, county
        details = response.xpath('//div[@class="hotbox-title"]/following-sibling::table[2]/tr')
        for ind,row in enumerate(details):
            item = NetronlineItem()
            if ind == 0: continue
            name = row.xpath('td[1]/text()').extract_first().replace(county, '').strip()
            item['name'] = name
            yield item
            # if "Recoder" in name:
            #     item['Recoder'] = name
            # elif "Assessor" in name:
            #     item['Assessor'] = name
            # elif "Treasurer" in name:
            #     item['Treasurer'] = name
            # elif "Mapping" in name:
            #     item['Mapping'] = name
            # phone = row.xpath('td[2]/text()').extract_first()
            # online = row.xpath('td[3]/a/@href').extract_first()
            # print name, phone, online
