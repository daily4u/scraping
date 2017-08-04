# -*- coding: utf-8 -*-
import scrapy
from mwwinepark.items import ImageItem
import csv
import numpy as np
class MwwineimagespiderSpider(scrapy.Spider):
    name = 'mwwineimagespider'
    allowed_domains = ['www.mwwinepark.com']
    start_urls = ['http://www.mwwinepark.com/']

    def parse(self, response):
        with open('product.csv', 'rb') as f:
            reader = csv.reader(f)
            items_list = list(reader)        
        image_lists = np.array(items_list)
        image_item = ImageItem()
        # Current source image url column index of item.csv file is 4
        image_item['Ids'] = image_lists[:,0]
        image_item['Dirs'] = image_lists[:,10]
        image_item['image_urls'] = image_lists[:,14]
        yield image_item
