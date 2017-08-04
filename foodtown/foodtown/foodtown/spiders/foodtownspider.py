# -*- coding: utf-8 -*-
import scrapy
import requests
import numpy as np
class FoodtownspiderSpider(scrapy.Spider):
    name = 'foodtownspider'
    allowed_domains = ['www.foodtown.com']
    start_urls = ['https://www.foodtown.com/stores/foodtown-of-old-tappan?next=/shopping#!/']
    def parse(self, response):
        limit_count = 100
        total_url = "https://api.freshop.com/1/products?fields=id,identifier,reference_id,reference_ids,upc,name,department_id,size,cover_image,price,sale_price,sale_start_date,sale_finish_date,price_disclaimer,sale_price_disclaimer,is_favorite,relevance,popularity,shopper_walkpath,quantity_step,quantity_minimum,quantity_initial,quantity_label,quantity_label_singular,varieties,quantity_size_ratio_description,status,status_id,sale_configuration_type,fulfillment_type_id,other_attributes,clippable_offer,offered_together,sequence&include_offered_together=true&sort=popularity&limit=0&token=0c98713eb71ce6c8737c15ea70faf469&store_id=73&popularity_sort=asc&app_key=foodtown"
        total = requests.get(url=total_url).json()['total']
        print total
        skip_count = 0
        while (True):
            items_url = 'https://api.freshop.com/1/products?fields=id,identifier,reference_id,reference_ids,upc,name,department_id,size,cover_image,price,sale_price,sale_start_date,sale_finish_date,price_disclaimer,sale_price_disclaimer,is_favorite,relevance,popularity,shopper_walkpath,quantity_step,quantity_minimum,quantity_initial,quantity_label,quantity_label_singular,varieties,quantity_size_ratio_description,status,status_id,sale_configuration_type,fulfillment_type_id,other_attributes,clippable_offer,offered_together,sequence&include_offered_together=true&skip=%s&sort=popularity&limit=%s&token=0c98713eb71ce6c8737c15ea70faf469&store_id=73&popularity_sort=asc&app_key=foodtown' % (skip_count, limit_count)
            items = requests.get(url = items_url).json()['items']
            for row in items:
                item_id = row['id']
                name  = row['name'] #"Yellow Bananas"
                identifier = row['identifier']
                department_id = row['department_id'][0]
                quantity_label = row['quality_label']
                quantity_size_ratio_description = row['quantity_size_ratio_description']
                varieties = ','.join(np.array(row['varieties']['options'])[:,0]).strip()
                upc = row['upc']
                reference_id = row['reference_id'] #:"00000000040112"
                # reference_ids:Array
                size = row['size'] #:"LB"
                cover_image = row['cover_image'] #:"produce_bananas/d6b28f69c0414ca28c61935a591654d4" + "_medium.jpg"
                popularity = row['popularity'] #:66
                
        # get_url = 'https://api.freshop.com/1/products?fields=id,identifier,reference_id,reference_ids,upc,name,department_id,size,cover_image,price,sale_price,sale_start_date,sale_finish_date,price_disclaimer,sale_price_disclaimer,is_favorite,relevance,popularity,shopper_walkpath,quantity_step,quantity_minimum,quantity_initial,quantity_label,quantity_label_singular,varieties,quantity_size_ratio_description,status,status_id,sale_configuration_type,fulfillment_type_id,other_attributes,clippable_offer,offered_together,sequence&include_offered_together=true&skip=%s&sort=popularity&limit=%s&token=0c98713eb71ce6c8737c15ea70faf469&store_id=73&popularity_sort=asc&app_key=foodtown' % (skip_count, limit_count)
        # depart_url = 'https://api.freshop.com/1/products?include_departments=true&limit=0&include_offered_together=true&token=0c98713eb71ce6c8737c15ea70faf469&store_id=73&app_key=foodtown'
