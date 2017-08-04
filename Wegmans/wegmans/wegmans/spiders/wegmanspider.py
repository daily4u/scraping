# -*- coding: utf-8 -*-
import scrapy
from scrapex import *
from scrapy.http import Request
import json,csv
import requests
from wegmans.items import ImageItem
from wegmans.pipelines import MyImagesPipeline
import numpy as np

class WegmanspiderSpider(scrapy.Spider):
    name = 'wegmanspider'
    allowed_domains = ['www.wegmans.com']
    start_urls = ['https://www.wegmans.com/products.html']
    parent_url = 'https://www.wegmans.com'

    def start_requests(self):
        yield Request(
            url=self.start_urls[0],
            callback=self.parse_image,
            dont_filter=True
        )
    def parse_image(self, response):
        with open('product.csv', 'rb') as f:
            reader = csv.reader(f)
            items_list = list(reader)        
        image_lists = np.array(items_list)
        image_item = ImageItem()
        # Current source image url column index of item.csv file is 4
        image_item['Ids'] = image_lists[:,8]
        image_item['Dirs'] = image_lists[:,3]
        image_item['image_urls'] = image_lists[:,20]
        yield image_item