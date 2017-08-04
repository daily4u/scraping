# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from fetchquick.items import ImageItem

import numpy as np
import json, csv

import sys

class FetchquickspiderSpider(scrapy.Spider):
    name = 'fetchquickspider'
    allowed_domains = ['fetchquick.com']
    start_urls = ['https://www.fetchquick.com']
  
    def parse(self, response):
        with open('item.csv', 'rb') as f:
            reader = csv.reader(f)
            items_list = list(reader)        
        image_lists = np.array(items_list)
        image_item = ImageItem()
        # Current source image url column index of item.csv file is 4
        image_item['Dirs'] = image_lists[:,1]
        image_item['image_urls'] = image_lists[:,4]
        yield image_item
