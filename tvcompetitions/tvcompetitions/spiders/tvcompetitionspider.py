# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import re
from tvcompetitions.items import TvcompetitionsItem
class TvcompetitionspiderSpider(scrapy.Spider):
    name = 'tvcompetitionspider'
    allowed_domains = ['tvcompetitions.com.au']
    start_urls = ['http://tvcompetitions.com.au/channel-7-competitions/sunrise-cash-cow-win-10000or-code/']

    def start_requests(self):
        yield Request(url=self.start_urls[0], callback=self.parse, dont_filter=True)
    def parse(self, response):
        item_text       = response.xpath('//div[@class="entry-content"]/ul/li[1]/strong/text()').extract_first()
        item = TvcompetitionsItem()
        try:
            item_date       = re.search('(.*?) SMS the codeword', item_text ,re.S|re.M).group(1).strip()
            item['date']    = item_date
        except:
            item['date']    = ''
        try:
            item_codeword   = re.sub('[^\x00-\x7F]+',' ',re.search('the codeword (.*)', item_text, re.S|re.M).group(1)).strip()
            item['codeword']= item_codeword
        except:
            item['codeword']= ''
        yield item