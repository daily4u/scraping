# -*- coding: utf-8 -*-
# import packages
import sys
import re, urlparse
import os
import os.path
from time import sleep
from time import time
import requests
import json, csv
import random

import proxies

# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
# from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
# from selenium.common import exceptions as EX
# from selenium.webdriver.chrome.options import Options

from scrapex import *
import threading
from scrapex.http import *
# define global variables
threadLock = threading.Lock()
# end global varialbles
# *****************************************************************
# define sprider class
"""
https://www.beautyboutique.ca/Categories/Makeup/c/MakeUp
https://www.beautyboutique.ca/Categories/Skin-Care/c/SkinCare
https://www.beautyboutique.ca/Categories/Derm-Skin-Care/c/Derm
https://www.beautyboutique.ca/Categories/Fragrance/c/Fragrance
https://www.beautyboutique.ca/Categories/Hair/c/Hair
https://www.beautyboutique.ca/Categories/Bath-&-Body/c/BathBody
https://www.beautyboutique.ca/Categories/Men/c/Men
https://www.beautyboutique.ca/Categories/Gifts-&-Sets/c/GiftsSets

https://www.beautyboutique.ca/category/offers

"""
categories = [
'https://www.beautyboutique.ca/Categories/Makeup/c/MakeUp',
'https://www.beautyboutique.ca/Categories/Skin-Care/c/SkinCare',
'https://www.beautyboutique.ca/Categories/Derm-Skin-Care/c/Derm',
'https://www.beautyboutique.ca/Categories/Fragrance/c/Fragrance',
'https://www.beautyboutique.ca/Categories/Hair/c/Hair',
'https://www.beautyboutique.ca/Categories/Men/c/Men',
'https://www.beautyboutique.ca/Categories/Bath-&-Body/c/BathBody',
'https://www.beautyboutique.ca/Categories/Gifts-&-Sets/c/GiftsSets',
]
__THREAD_NUMBER__ = 8
first_ajax_url = "https://api.bazaarvoice.com/data/batch.json?passkey=tsuy5y50qf1vuapwn42ip8f8h&apiversion=5.5&displaycode=12438-en_ca&resource.q0=products&filter.q0=id:eq:%s&stats.q0=reviews&filteredstats.q0=reviews&filter_reviews.q0=contentlocale:eq:en_CA,en_US&filter_reviewcomments.q0=contentlocale:eq:en_CA,en_US&resource.q1=reviews&filter.q1=isratingsonly:eq:false&filter.q1=productid:eq:%s&filter.q1=contentlocale:eq:en_CA,en_US&sort.q1=relevancy:a1&stats.q1=reviews&filteredstats.q1=reviews&include.q1=authors,products,comments&filter_reviews.q1=contentlocale:eq:en_CA,en_US&filter_reviewcomments.q1=contentlocale:eq:en_CA,en_US&filter_comments.q1=contentlocale:eq:en_CA,en_US&limit.q1=8&offset.q1=0&limit_comments.q1=3&resource.q2=reviews&filter.q2=productid:eq:%s&filter.q2=contentlocale:eq:en_CA,en_US&limit.q2=1&resource.q3=reviews&filter.q3=productid:eq:%s&filter.q3=isratingsonly:eq:false&filter.q3=issyndicated:eq:false&filter.q3=rating:gt:3&filter.q3=totalpositivefeedbackcount:gte:3&filter.q3=contentlocale:eq:en_CA,en_US&sort.q3=totalpositivefeedbackcount:desc&include.q3=authors,reviews,products&filter_reviews.q3=contentlocale:eq:en_CA,en_US&limit.q3=1&resource.q4=reviews&filter.q4=productid:eq:%s&filter.q4=isratingsonly:eq:false&filter.q4=issyndicated:eq:false&filter.q4=rating:lte:3&filter.q4=totalpositivefeedbackcount:gte:3&filter.q4=contentlocale:eq:en_CA,en_US&sort.q4=totalpositivefeedbackcount:desc&include.q4=authors,reviews,products&filter_reviews.q4=contentlocale:eq:en_CA,en_US&limit.q4=1&callback=BV._internal.dataHandler0"
next_ajax_url =  "https://api.bazaarvoice.com/data/batch.json?passkey=tsuy5y50qf1vuapwn42ip8f8h&apiversion=5.5&displaycode=12438-en_ca&resource.q0=reviews&filter.q0=isratingsonly:eq:false&filter.q0=productid:eq:%s&filter.q0=contentlocale:eq:en_CA,en_US&sort.q0=relevancy:a1&stats.q0=reviews&filteredstats.q0=reviews&include.q0=authors,products,comments&filter_reviews.q0=contentlocale:eq:en_CA,en_US&filter_reviewcomments.q0=contentlocale:eq:en_CA,en_US&filter_comments.q0=contentlocale:eq:en_CA,en_US&limit.q0=30&offset.q0=%s&limit_comments.q0=3"
s = Scraper(use_cache=False, retries=3, timeout=300, log_post=True, log_headers=True)
class BeautyBoutiqueSpider(threading.Thread):
    # init function for class
    def __init__(self, idx):
        super(BeautyBoutiqueSpider, self).__init__()
        self.thread_id = idx
        self.sobj = Scraper(use_cache=False, retries=3, timeout=300, log_post=True, log_headers=True)
        host = proxies.proxies[idx].split(':')[0]
        port = proxies.proxies[idx].split(':')[1]
        print host,port
        proxy = Proxy(host, port, 'silicons:1pRnQcg87F')
        print proxy
        self.sobj.proxy_manager.session_proxy = proxy
        self.category_url = categories[idx]
    # end function for class

    # define thread run function
    # This is thread function user can customize
    # When user execute BeautyBoutiqueSpider.start() function, it will run
    def run(self):
        try:
            page = 0
            paginate_nav_url = self.category_url
            while (True):
                doc = self.sobj.load(paginate_nav_url)
                product_urls = doc.q('//li[contains(@class,"product-tile category")]')
                for idx, row in enumerate(product_urls):
                    print self.thread_id, idx, row.x('a/@href')
                    product_sku = row.x('@data-productcode')
                    self.parse_review(product_sku)
                # exit()
                last_page = doc.q('//div[@class="pagination-nav"]')[0].x('ul/li[last()]//text()').trim()
                page = page + 1
                print self.thread_id, page
                if (str(page) == str(last_page)):
                    print "---OK----"
                    break
                paginate_nav_url =  self.category_url + "?page=%s&q=:trending&text=&sort=trending&facetType=" % str(page)
        except Exception as e:
            print e
    # # end thread run function
    def parse_review(self, sku):
        review_count = 0
        doc = self.sobj.load_html(url=first_ajax_url % (sku,sku,sku,sku,sku))
        return_first_page = json.loads(re.sub(r'[^\x00-\x7F]+',' ', re.search("BV._internal.dataHandler0\((.*)\)", doc, re.S|re.M).group(1)).replace("\n",""))

        total_result = return_first_page['BatchedResults']['q1']['TotalResults']
        print total_result
        
        limit_result = return_first_page['BatchedResults']['q1']['Limit']
        offset_result = return_first_page['BatchedResults']['q1']['Offset']

        try:
            Name = return_first_page['BatchedResults']['q1']['Includes']['Products'][sku]["Name"]
        except:
            Name = ""
        try:
            Description = return_first_page['BatchedResults']['q1']['Includes']['Products'][sku]["Description"]
        except:
            Description = ""
        try:
            Brand = return_first_page['BatchedResults']['q1']['Includes']['Products'][sku]["Brand"]["Name"]
        except:
            Brand = ""
        try:
            ProductPageUrl = return_first_page['BatchedResults']['q1']['Includes']['Products'][sku]["ProductPageUrl"]
        except:
            ProductPageUrl = ""
        try:
            OverallRatingRange = return_first_page['BatchedResults']['q1']['Includes']['Products'][sku]["ReviewStatistics"]["OverallRatingRange"]
        except:
            OverallRatingRange = ""

        try:
            OverallRatingRange = return_first_page['BatchedResults']['q1']['Includes']['Products'][sku]["ReviewStatistics"]["OverallRatingRange"]
        except:
            OverallRatingRange = ""

        try:
            OverallRatingRange = return_first_page['BatchedResults']['q1']['Includes']['Products'][sku]["ReviewStatistics"]["OverallRatingRange"]
        except:
            OverallRatingRange = ""

        try:
            SecondaryRatingsAveragesQuality = return_first_page['BatchedResults']['q1']['Includes']['Products'][sku]["ReviewStatistics"]["SecondaryRatingsAverages"]["Quality"]["AverageRating"]
        except:
            SecondaryRatingsAveragesQuality = ""

        try:
            SecondaryRatingsAveragesValue = return_first_page['BatchedResults']['q1']['Includes']['Products'][sku]["ReviewStatistics"]["SecondaryRatingsAverages"]["Value"]["AverageRating"]
        except:
            SecondaryRatingsAveragesValue = ""


        for row in return_first_page['BatchedResults']['q1']['Results']:
            review_count = review_count + 1
            print self.thread_id,"Review", review_count
            item = []
            item.append("Product Name")
            item.append(Name)
            item.append("Description")
            item.append(Description)
            item.append("Brand")
            item.append(Brand)
            item.append("ProductPageUrl")
            item.append(ProductPageUrl)
            item.append("OverallRatingRange")
            item.append(OverallRatingRange)
            item.append("SecondaryRatingsAveragesQuality")
            item.append(SecondaryRatingsAveragesQuality)
            item.append("SecondaryRatingsAveragesValue")
            item.append(SecondaryRatingsAveragesValue)
            try:
                Id = row["Id"]
                item.append("Id")
                item.append(Id)
            except:
                Id = ""
                item.append("Id")
                item.append(Id)
            try:
                CID = row["CID"]
                item.append("CID")
                item.append(CID)
            except:
                CID = ""
                item.append("CID")
                item.append(CID)
            try:
                SourceClient = row["SourceClient"]
                item.append("SourceClient")
                item.append(SourceClient)
            except:
                SourceClient = ""
                item.append("SourceClient")
                item.append(SourceClient)
            try:
                LastModificationTime = row["LastModificationTime"]
                item.append("LastModificationTime")
                item.append(LastModificationTime)
            except:
                LastModificationTime = ""
                item.append("LastModificationTime")
                item.append(LastModificationTime)
            try:
                LastModeratedTime = row["LastModeratedTime"]
                item.append("LastModeratedTime")
                item.append(LastModeratedTime)
            except:
                LastModeratedTime = ""
                item.append("LastModeratedTime")
                item.append(LastModeratedTime)
            try:
                ProductId = row["ProductId"]
                item.append("ProductId")
                item.append(ProductId)
            except:
                ProductId = ""
                item.append("ProductId")
                item.append(ProductId)
            try:
                CampaignId = row["CampaignId"]
                item.append("CampaignId")
                item.append(CampaignId)
            except:
                CampaignId = ""
                item.append("CampaignId")
                item.append(CampaignId)
            try:
                UserLocation = row["UserLocation"]
                item.append("UserLocation")
                item.append(UserLocation)
            except:
                UserLocation = ""
                item.append("UserLocation")
                item.append(UserLocation)
            try:
                AuthorId = row["AuthorId"]
                item.append("AuthorId")
                item.append(AuthorId)
            except:
                AuthorId = ""
                item.append("AuthorId")
                item.append(AuthorId)
            try:
                IsFeatured = row["IsFeatured"]
                item.append("IsFeatured")
                item.append(IsFeatured)
            except:
                IsFeatured = ""
                item.append("IsFeatured")
                item.append(IsFeatured)
            try:
                TotalClientResponseCount = row["TotalClientResponseCount"]
                item.append("TotalClientResponseCount")
                item.append(TotalClientResponseCount)
            except:
                TotalClientResponseCount = ""
                item.append("TotalClientResponseCount")
                item.append(TotalClientResponseCount)
            try:
                TotalCommentCount = row["TotalCommentCount"]
                item.append("TotalCommentCount")
                item.append(TotalCommentCount)
            except:
                TotalCommentCount = ""
                item.append("TotalCommentCount")
                item.append(TotalCommentCount)
            try:
                Rating = row["Rating"]
                item.append("Rating")
                item.append(Rating)
            except:
                Rating = ""
                item.append("Rating")
                item.append(Rating)
            try:
                IsRecommended = row["IsRecommended"]
                item.append("IsRecommended")
                item.append(IsRecommended)
            except:
                IsRecommended = ""
                item.append("IsRecommended")
                item.append(IsRecommended)
            try:
                Helpfulness = row["Helpfulness"]
                item.append("Helpfulness")
                item.append(Helpfulness)
            except:
                Helpfulness = ""
                item.append("Helpfulness")
                item.append(Helpfulness)
            try:
                TotalFeedbackCount = row["TotalFeedbackCount"]
                item.append("TotalFeedbackCount")
                item.append(TotalFeedbackCount)
            except:
                TotalFeedbackCount = ""
                item.append("TotalFeedbackCount")
                item.append(TotalFeedbackCount)
            try:
                TotalNegativeFeedbackCount = row["TotalNegativeFeedbackCount"]
                item.append("TotalNegativeFeedbackCount")
                item.append(TotalNegativeFeedbackCount)
            except:
                TotalNegativeFeedbackCount = ""
                item.append("TotalNegativeFeedbackCount")
                item.append(TotalNegativeFeedbackCount)
            try:
                TotalPositiveFeedbackCount = row["TotalPositiveFeedbackCount"]
                item.append("TotalPositiveFeedbackCount")
                item.append(TotalPositiveFeedbackCount)
            except:
                TotalPositiveFeedbackCount = ""
                item.append("TotalPositiveFeedbackCount")
                item.append(TotalPositiveFeedbackCount)
            try:
                ModerationStatus = row["ModerationStatus"]
                item.append("ModerationStatus")
                item.append(ModerationStatus)
            except:
                ModerationStatus = ""
                item.append("ModerationStatus")
                item.append(ModerationStatus)
            try:
                SubmissionTime = row["SubmissionTime"]
                item.append("SubmissionTime")
                item.append(SubmissionTime)
            except:
                SubmissionTime = ""
                item.append("SubmissionTime")
                item.append(SubmissionTime)
            try:
                ReviewText = row["ReviewText"]
                item.append("ReviewText")
                item.append(ReviewText)
            except:
                ReviewText = ""
                item.append("ReviewText")
                item.append(ReviewText)
            try:
                Title = row["Title"]
                item.append("Title")
                item.append(Title)
            except:
                Title = ""
                item.append("Title")
                item.append(Title)
            try:
                UserNickname = row["UserNickname"]
                item.append("UserNickname")
                item.append(UserNickname)
            except:
                UserNickname = ""
                item.append("UserNickname")
                item.append(UserNickname)
            try:
                SecondaryRatings_Value_Value    = row["SecondaryRatings"]["Value"]["Value"]
                item.append("SecondaryRatings_Value_Value")
                item.append(SecondaryRatings_Value_Value)
            except:
                SecondaryRatings_Value_Value    = ""
                item.append("SecondaryRatings_Value_Value")
                item.append(SecondaryRatings_Value_Value)
            try:
                SecondaryRatings_Quality_Value  = row["SecondaryRatings"]["Quality"]["Value"]
                item.append("SecondaryRatings_Quality_Value")
                item.append(SecondaryRatings_Quality_Value)
            except:
                SecondaryRatings_Quality_Value  = ""
                item.append("SecondaryRatings_Quality_Value")
                item.append(SecondaryRatings_Quality_Value)
            threadLock.acquire()
            s.save(item, str(self.thread_id) + ".csv")
            threadLock.release()
        # exit()
        offset_result = 8
        limit_result = 30        
        while (True):
            if total_result < offset_result:
                break
            print offset_result
            print next_ajax_url % (sku,offset_result)
            return_next_page = json.loads(self.sobj.load_html(url=next_ajax_url % (sku,str(offset_result))))
            print len(return_next_page['BatchedResults']['q0']['Results'])
            for row in return_next_page['BatchedResults']['q0']['Results']:
                review_count = review_count + 1
                print self.thread_id,"Review", review_count
                item = []
                item.append("Product Name")
                item.append(Name)
                item.append("Description")
                item.append(Description)
                item.append("Brand")
                item.append(Brand)
                item.append("ProductPageUrl")
                item.append(ProductPageUrl)
                item.append("OverallRatingRange")
                item.append(OverallRatingRange)
                item.append("SecondaryRatingsAveragesQuality")
                item.append(SecondaryRatingsAveragesQuality)
                item.append("SecondaryRatingsAveragesValue")
                item.append(SecondaryRatingsAveragesValue)
                
                try:
                    Id = row["Id"]
                    item.append("Id")
                    item.append(Id)
                except:
                    Id = ""
                    item.append("Id")
                    item.append(Id)
                try:
                    CID = row["CID"]
                    item.append("CID")
                    item.append(CID)
                except:
                    CID = ""
                    item.append("CID")
                    item.append(CID)
                try:
                    SourceClient = row["SourceClient"]
                    item.append("SourceClient")
                    item.append(SourceClient)
                except:
                    SourceClient = ""
                    item.append("SourceClient")
                    item.append(SourceClient)
                try:
                    LastModificationTime = row["LastModificationTime"]
                    item.append("LastModificationTime")
                    item.append(LastModificationTime)
                except:
                    LastModificationTime = ""
                    item.append("LastModificationTime")
                    item.append(LastModificationTime)
                try:
                    LastModeratedTime = row["LastModeratedTime"]
                    item.append("LastModeratedTime")
                    item.append(LastModeratedTime)
                except:
                    LastModeratedTime = ""
                    item.append("LastModeratedTime")
                    item.append(LastModeratedTime)
                try:
                    ProductId = row["ProductId"]
                    item.append("ProductId")
                    item.append(ProductId)
                except:
                    ProductId = ""
                    item.append("ProductId")
                    item.append(ProductId)
                try:
                    CampaignId = row["CampaignId"]
                    item.append("CampaignId")
                    item.append(CampaignId)
                except:
                    CampaignId = ""
                    item.append("CampaignId")
                    item.append(CampaignId)
                try:
                    UserLocation = row["UserLocation"]
                    item.append("UserLocation")
                    item.append(UserLocation)
                except:
                    UserLocation = ""
                    item.append("UserLocation")
                    item.append(UserLocation)
                try:
                    AuthorId = row["AuthorId"]
                    item.append("AuthorId")
                    item.append(AuthorId)
                except:
                    AuthorId = ""
                    item.append("AuthorId")
                    item.append(AuthorId)
                try:
                    IsFeatured = row["IsFeatured"]
                    item.append("IsFeatured")
                    item.append(IsFeatured)
                except:
                    IsFeatured = ""
                    item.append("IsFeatured")
                    item.append(IsFeatured)
                try:
                    TotalClientResponseCount = row["TotalClientResponseCount"]
                    item.append("TotalClientResponseCount")
                    item.append(TotalClientResponseCount)
                except:
                    TotalClientResponseCount = ""
                    item.append("TotalClientResponseCount")
                    item.append(TotalClientResponseCount)
                try:
                    TotalCommentCount = row["TotalCommentCount"]
                    item.append("TotalCommentCount")
                    item.append(TotalCommentCount)
                except:
                    TotalCommentCount = ""
                    item.append("TotalCommentCount")
                    item.append(TotalCommentCount)
                try:
                    Rating = row["Rating"]
                    item.append("Rating")
                    item.append(Rating)
                except:
                    Rating = ""
                    item.append("Rating")
                    item.append(Rating)
                try:
                    IsRecommended = row["IsRecommended"]
                    item.append("IsRecommended")
                    item.append(IsRecommended)
                except:
                    IsRecommended = ""
                    item.append("IsRecommended")
                    item.append(IsRecommended)
                try:
                    Helpfulness = row["Helpfulness"]
                    item.append("Helpfulness")
                    item.append(Helpfulness)
                except:
                    Helpfulness = ""
                    item.append("Helpfulness")
                    item.append(Helpfulness)
                try:
                    TotalFeedbackCount = row["TotalFeedbackCount"]
                    item.append("TotalFeedbackCount")
                    item.append(TotalFeedbackCount)
                except:
                    TotalFeedbackCount = ""
                    item.append("TotalFeedbackCount")
                    item.append(TotalFeedbackCount)
                try:
                    TotalNegativeFeedbackCount = row["TotalNegativeFeedbackCount"]
                    item.append("TotalNegativeFeedbackCount")
                    item.append(TotalNegativeFeedbackCount)
                except:
                    TotalNegativeFeedbackCount = ""
                    item.append("TotalNegativeFeedbackCount")
                    item.append(TotalNegativeFeedbackCount)
                try:
                    TotalPositiveFeedbackCount = row["TotalPositiveFeedbackCount"]
                    item.append("TotalPositiveFeedbackCount")
                    item.append(TotalPositiveFeedbackCount)
                except:
                    TotalPositiveFeedbackCount = ""
                    item.append("TotalPositiveFeedbackCount")
                    item.append(TotalPositiveFeedbackCount)
                try:
                    ModerationStatus = row["ModerationStatus"]
                    item.append("ModerationStatus")
                    item.append(ModerationStatus)
                except:
                    ModerationStatus = ""
                    item.append("ModerationStatus")
                    item.append(ModerationStatus)
                try:
                    SubmissionTime = row["SubmissionTime"]
                    item.append("SubmissionTime")
                    item.append(SubmissionTime)
                except:
                    SubmissionTime = ""
                    item.append("SubmissionTime")
                    item.append(SubmissionTime)
                try:
                    ReviewText = row["ReviewText"]
                    item.append("ReviewText")
                    item.append(ReviewText)
                except:
                    ReviewText = ""
                    item.append("ReviewText")
                    item.append(ReviewText)
                try:
                    Title = row["Title"]
                    item.append("Title")
                    item.append(Title)
                except:
                    Title = ""
                    item.append("Title")
                    item.append(Title)
                try:
                    UserNickname = row["UserNickname"]
                    item.append("UserNickname")
                    item.append(UserNickname)
                except:
                    UserNickname = ""
                    item.append("UserNickname")
                    item.append(UserNickname)
                try:
                    SecondaryRatings_Value_Value    = row["SecondaryRatings"]["Value"]["Value"]
                    item.append("SecondaryRatings_Value_Value")
                    item.append(SecondaryRatings_Value_Value)
                except:
                    SecondaryRatings_Value_Value    = ""
                    item.append("SecondaryRatings_Value_Value")
                    item.append(SecondaryRatings_Value_Value)
                try:
                    SecondaryRatings_Quality_Value  = row["SecondaryRatings"]["Quality"]["Value"]
                    item.append("SecondaryRatings_Quality_Value")
                    item.append(SecondaryRatings_Quality_Value)
                except:
                    SecondaryRatings_Quality_Value  = ""
                    item.append("SecondaryRatings_Quality_Value")
                    item.append(SecondaryRatings_Quality_Value)
                threadLock.acquire()
                s.save(item, str(self.thread_id) + ".csv")
                threadLock.release()            
            offset_result = limit_result + offset_result
        
# end class
# *****************************************************************
# main function

if __name__ == '__main__':
    if os.path.exists("result.csv"):
        os.remove("result.csv")
    threads = []
    for i in range(__THREAD_NUMBER__):
        thrd = BeautyBoutiqueSpider(i)
        threads.append(thrd)

    for thrd in threads:
        thrd.start()
        sleep(1)

    for thrd in threads:
        thrd.join()

# end main function
