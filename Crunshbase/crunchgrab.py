# encoding=utf8
import sys
# from grab import Grab
from grab.spider import Spider, Task
import logging
import csv
import json
import datetime
import urllib
import re

reload(sys)
sys.setdefaultencoding('utf8')

class LinkedinSpider(Spider):
    initial_urls = ['https://www.instagram.com/beautifuldestinations/',]
    def prepare(self):
        print "Prepare part"
        with open('result.csv', 'w') as f:
            fieldnames = ['Source profile being scraped','Reposted Post','Reposted Profile link','Reposted Username','Number of Followers','Date']
            self.result_file = csv.DictWriter(open('result.csv', 'w'),delimiter=',',fieldnames=fieldnames)
            self.result_file.writeheader()

        self.result_counter = 0
        self.query_ids = ['17852405266163336', '17863787143139595', '17875800862117404', '17865274345132052', '17888483320059182']
    def task_initial(self, grab, task):
        print "Initial Part"
        json_text = grab.doc.rex_search('window._sharedData = (.*?);').group(1)
        json_data = json.loads(json_text)
        
        for node in json_data["entry_data"]["ProfilePage"][0]["user"]["media"]["nodes"]:
            # print node
            soucefile_scraped = "https://www.instagram.com/{}".format(json_data["entry_data"]["ProfilePage"][0]["user"]["username"])
            reposted_post = "https://www.instagram.com/p/{}/?taken-by={}".format(node["code"],json_data["entry_data"]["ProfilePage"][0]["user"]["username"])

            try:
                reposted_profile_link = "https://www.instagram.com/{}".format(re.search("\: \@(.*?)\)",node["caption"]).group(1))
            except:
                reposted_profile_link = None
            try:
                reposted_usename = re.search("\: \@(.*)\)",node["caption"]).group(1)
            except:
                reposted_usename = None
                
            num_followers = node["likes"]["count"]
            
            try:
                date = datetime.datetime.fromtimestamp(int(node["date"])).strftime('%Y-%m-%d %H:%M:%S')
            except:
                date = None
            item = {'Source profile being scraped':soucefile_scraped,'Reposted Post':reposted_post,'Reposted Profile link':reposted_profile_link,'Reposted Username':reposted_usename,'Number of Followers':num_followers,'Date':date}
            self.save(item)
        print "Exit"
        # for script in grab.doc.select("//script/@src"):
        #     if "en_US_Commons" in script.text():
        #         script_url = "https://www.instagram.com{}".format(script.text())
        #         yield Task('get_query_id', script_url)
        id = json_data["entry_data"]["ProfilePage"][0]["user"]["id"]
        query_id = self.query_ids[4]
        end_cursor = json_data["entry_data"]["ProfilePage"][0]["user"]["media"]["page_info"]["end_cursor"]
        variables = json.dumps({"id":id,"first":12,"after":end_cursor})
        next_link = 'https://www.instagram.com/graphql/query/?query_id=%s&variables=%s' % (query_id, urllib.quote(variables))
        # yield Task('all_task', next_link)
        yield Task('next',next_link)

    def task_next(self, grab, task):
        print grab.cookies.get_dict()
        print grab.response.head()
        print grab.common_headers
        print grab.user_agent
        print grab.proxy
        print grab.webdriver
        print grab.selenium_wait
        # print grab.error
    #     print task.url
    #     for query_id in re.findall("(?<=queryId:\")[0-9]{17,17}", grab.doc.body):
    #         self.query_ids.append(query_id)
    #     print self.query_ids

    def save(self, item):
        self.result_file.writerow(item)
    

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    bot = LinkedinSpider()
    bot.run()
    