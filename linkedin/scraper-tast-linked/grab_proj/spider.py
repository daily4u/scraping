from grab import Grab
import logging
import csv, json
import re
import sys
import threading
from urllib import urlencode
import pymysql.cursors
import time
from grab.spider import Spider, Task, Data
from scrapex import *
# reload(sys)
# sys.setdefaultencoding('utf8')

config = dict(
    timeout = 200,
    connect_timeout = 5,
    user_agent_file='agents.txt',
    common_headers={
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer':'https://www.google.com',
        'Connection': 'keep-alive'
    },
    selenium_wait = 3,
    proxy='46.101.204.69:3128',
    proxy_type='http',
    proxy_userpwd='ofirseo:a1qs2wd3ef4r',
)
MYSQL_CONFIG = dict(
    host='localhost',
    user='root',
    password='root',
    db='linkdb',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)
s = Scraper()
class LinkedingSpider(Spider):
   
    def task_generator(self):
        logging.debug("*****execute******")
        with open('directories.csv','rb') as f:
            content = csv.reader(f)
            directories = list(content)
        
        # directories = ['google']
        total = len(directories)
        logging.debug("*****{}******".format(total))
        i = 100
        total = 102
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        }

        test_url = 'https://www.google.com'

        while (True): 
            logging.debug("Index: {}".format(i))
            if i>=total:
                break
            g = Grab()
            g.clear_cookies()
            g.setup(**config)
            g.setup(headers=headers)
            logging.debug("CONFIG : {}".format(g.config))
            data = dict(
                slug = directories[i][0],
            )
            logging.info(data)
            while True:
                try:
                    print "------------------------"
                    g.go(test_url)
                    print g.doc.body
                    print "++++++++++++++++++++++++"
                    break
                except Exception as e:
                    print "************************"
                    logging.debug(e)
                    time.sleep(1)
            
            yield Task('init',grab=g, data = data)
            time.sleep(5)
            i += 1

    def task_init(self, grab, task):
        logging.debug("BODY")
        g = grab.clone()
        post_url = 'https://search.google.com/structured-data/testing-tool/validate'
        
        # headers
        headers = {
            'Accept':'*/*',
            'Content-Type':'application/x-www-form-urlencoded;charset=utf-8',
            'Referer':'https://search.google.com/structured-data/testing-tool'
        }

        bodies = urlencode({
            'g-recaptch-response':'',
            'url':'https://www.linkedin.com/company/{}'.format(task.data['slug'])
        })
        # print bodies
        
        time.sleep(5)

        while True:
            try:
                g.setup(headers=headers)
                g.setup(post=bodies)
                g.go(post_url)
                break
            except:
                print "Proxy Error"
                time.sleep(5)
        
        # yield Task('save', grab=g)
        self.save(grb=g)

    def task_save(self, grab, task):
        logging.debug("SAVE")
        
        try:
            linkd_html_txt = json.loads(grab.doc.body.replace(")]}'", ""))['html'].replace('\n','')
        except:
            print 'Invalid url.'
            return
        try:
            company_data = json.loads(re.search('<code id="stream-right-rail-embed-id-content"><!--(.*?)--></code>', linkd_html_txt, re.S|re.M).group(1))
        except:
            print 'No Content'
            return

        item = {}
        print "-----------------------------------------------"
        
        logging.debug(company_data)

        try:
            Slug = str(company_data["homeUrl"].split("/")[-1])
        except:
            Slug = None

        item["slug"] = Slug

        try:
            Name = str(company_data["companyName"])
        except:
            Name = None
        
        item["name"] = Name

        try:
            Logo = str(company_data["legacyLogo"])
        except:
            Logo = None
        item["logo_url"] = Logo
        
        try:
            Beta_id = str(company_data["companyId"])
        except:
            Beta_id = None
        item["betaId"] = Beta_id

        try:
            Description = str(company_data["description"].replace("\r\n"," ").strip())
        except:
            Description = None
        item["description"] = Description


        try:
            companyType = str(company_data["companyType"])
        except:
            companyType = None
        item["company_type"] = companyType

        try:
            Type = str(company_data["type"])
        except:
            Type = None
        item["type"] = Type

        try:
            Street1 = str(company_data["headquarters"]["street1"])
        except:
            Street1 = None
        item["street1"] = Street1

        try:
            Street2 = str(company_data["headquarters"]["street2"])
        except:
            Street2 = None
        item["street2"] = Street2

        try:
            City = str(company_data["headquarters"]["city"])
        except:
            City = None
        item["city"] = City

        try:
            State = str(company_data["headquarters"]["state"])
        except:
            State = None
        item["state"] = State

        try:
            Country = str(company_data["headquarters"]["country"])
        except:
            Country = None

        item["country"] = Country
        try:
            Postal_code = str(company_data["headquarters"]["zip"])
        except:
            Postal_code = None
        item["postalCode"] = Postal_code

        try:
            Industry = str(company_data["industry"])
        except:
            Industry = None
        item["industry"] = Industry

        try:
            Company_Size = str(company_data["size"])
            if Company_Size == "Myself Only":
                Company_Size = 1
        except:
            Company_Size = None
        item["size"] = Company_Size

        try:
            Founded = str(company_data["yearFounded"])
        except:
            Founded = None
        item["founded_year"] = Founded

        try:
            Specialties = str("," .join(company_data["specialties"]).strip())
        except:
            Specialties = None
        item["specialties"] = Specialties

        try:
            Website = str(company_data["website"])
        except:
            Website = None
        item["website"] = Website

        try:
            showcase =  str(','.join(str(ro["id"]) for ro in company_data["showcasePages"]).strip())
        except Exception as e:
            print e
            showcase = None

        item["showcase"] = showcase
        try:
            employees = str(json.dumps(company_data["employees"]))
        except:
            employees = None
        item["employees"] = employees
        try:
            related_orgs =  str(','.join(str(ro["id"]) for ro in company_data["alsoViewed"]).strip())
        except Exception as e:
            print e
            related_orgs = None
        item["related_orgs"] = related_orgs
        try:
            affiliated_orgs =  str(','.join(str(ro["id"]) for ro in company_data["affiliated"]).strip())
        except Exception as e:
            print e
            affiliated_orgs = None
        item["affiliated_orgs"] = affiliated_orgs
        save_items = []
        for (k, v) in item.iteritems():
            save_items.append[k]
            save_items.append[v]
        s.save(save_items, 'result.csv', remove_existing_file=False)
        # yield Task('save_to_db', grab, item = item)
        # self.save_to_db(item)
        # yield Data('save_to_db',item=item)
    
    def task_save_to_db(self, grab, task):
        logging.debug("MYSQL PART")

        item = task.item
        label_strings = ','.join([k for (k,v) in item.iteritems()])
        format_strings = ','.join(['%s'] * len(item))
        insert_sql = "INSERT IGNORE INTO companies({}) VALUES ({})".format(label_strings,format_strings)
        # print insert_sql
        try:
            connection = pymysql.connect(**MYSQL_CONFIG)
            with connection.cursor() as cursor:
                cursor.execute(insert_sql,tuple([v for (k,v) in item.iteritems()]))
            connection.commit()
        except Exception as e:
            print e
        finally:
            connection.close()
        
# def main():
#     initial_url = 'https://icanhazip.com'
#     # res = request(initial_url)`
#     g = Grab(timeout=timeout)
#     g.setup(proxy='46.101.204.69:3128',proxy_type='socks5')
#     g.setup(url=initial_url)
#     g.go()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("*****START******")
    bot = LinkedingSpider(thread_number=2, transport='threaded')
    bot.run()
