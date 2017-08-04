#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from __future__ import print_function
import sys
import tornado
import re, urlparse
import os
import os.path
import time, datetime

from scrapex import *
import numpy as np
from time import sleep
import requests
import json, csv

start_url = 'https://www.foodtown.com/stores/foodtown-of-old-tappan?next=/shopping#!/'

sc = Scraper(
    use_cache=False,
    retries=3,
    timeout=300,
)


class FoodTownScraper(object):
    def parse_depart(self):
        limit_count = 100
        total_url = "https://api.freshop.com/1/products?limit=0&store_id=73&app_key=foodtown"
        # total_url = "https://api.freshop.com/1/products?limit=0&token=0c98713eb71ce6c8737c15ea70faf469&store_id=73&app_key=foodtown"
        total = sc.load_json(url=total_url)['total']
        print total
        skip_count = 155
        depart_url = "https://api.freshop.com/1/products?include_departments=true&limit=0&include_offered_together=true&store_id=73&app_key=foodtown"
        departs = sc.load_json(url=depart_url)["departments"]
        depart = {}
        for dp in departs:
            depart[dp['id']] = dp['name']
        # print depart
        while (True):
            items_url = 'https://api.freshop.com/1/products?fields=id,identifier,reference_id,reference_ids,upc,name,department_id,size,cover_image,price,ale_price,sale_start_date,sale_finish_date,price_disclaimer,sale_price_disclaimer,is_favorite,relevance,popularity,shopper_walkpath,quantity_step,quantity_minimum,quantity_initial,quantity_label,quantity_label_singular,varieties,quantity_size_ratio_description,status,status_id,sale_configuration_type,fulfillment_type_id,other_attributes,clippable_offer,offered_together,sequence&include_offered_together=true&skip=%s&sort=popularity&limit=%s&store_id=73&popularity_sort=asc&app_key=foodtown' % (skip_count, limit_count)
            items = sc.load_json(url = items_url)['items']
            for row in items:
                print row
                print '--------------'
                item_id = row['id']
                name  = row['name'] #"Yellow Bananas"
                try:
                    identifier = row['identifier']
                except:
                    identifier = ''
                try:
                    department_id = row['department_id'][0]
                except:
                    department_id = ''
                try:
                    department_name = depart[row['department_id'][0]]
                except:
                    department_name = ''
                try:
                    quantity_label = row['quantity_label']
                except:
                    quantity_label = ''
                try:
                    quantity_size_ratio_description = row['quantity_size_ratio_description']
                except:
                    quantity_size_ratio_description = ''
                varieties = []
                try:
                    for col in row['varieties'][0]['options']:
                        varieties.append(col['label'])
                    varieties = ',' .join(varieties)
                except:
                    varieties = ''
                try:
                    upc = row['upc']
                except:
                    upc = ''
                try:
                    reference_id = row['reference_id'] #:"00000000040112"
                except:
                    reference_id = ''
                try:
                    size = row['size'] #:"LB"
                except:
                    size = ''
                try:
                    cover_image = row['cover_image'] #:"produce_bananas/d6b28f69c0414ca28c61935a591654d4" + "_medium.jpg"
                except:
                    cover_image = ''
                try:
                    popularity = row['popularity'] #:66
                except:
                    popularity = ''
                sc.save(['ID',item_id,"NAME",name,"IDENTIFIER",identifier,"DID",department_id,"DNAME",department_name,"QLABEL",quantity_label,"QDESC",quantity_size_ratio_description,"VAR",varieties,"UPC",upc,"RID",reference_id,"SIZE",size,"IMG",cover_image,"POP",popularity],'result_.csv')
                print '-------End-------'
            skip_count = skip_count + 100
            if (skip_count > total):
                break
    
if __name__ == '__main__':
    print "==> Start!"
    scraper = FoodTownScraper()
    ret = scraper.parse_depart() 
