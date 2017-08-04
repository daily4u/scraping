from scrapex import *
import argparse
import threading
import os
import os.path
import re
from time import sleep
s = Scraper(use_cache=False, retries=3, timeout=300, log_post=True, log_headers=True)
# define sprider class
class ThreadObj(threading.Thread):
    # init function for class
    def __init__(self, state):
        super(ThreadObj, self).__init__()
        self.state = state
        
    # end function for class

    def run(self):
        try:
            public_records_url = "http://publicrecords.netronline.com"
            state_template_url = "http://publicrecords.netronline.com/state/%s/"
            doc = s.load(url=state_template_url % self.state)
            counties = doc.q('//div[@class="hotbox-title"]/following-sibling::div[1]//ul/li/a')
            for county in counties:
                county_url  = county.x('@href').trim()
                county_text = county.x('text()').trim()
                doc_next = s.load(url=county_url)
                title  = doc_next.x('//title/text()').trim()
                title = re.sub('[^\x00-\x7F]+', ',', title.split(',')[0]).strip()
                state  = title.split(',')[1].strip()
                county  = title.split(',')[2].replace('Public Records', '').replace('County', '').strip()
                item = []
                item.append("County")
                item.append(county)
                # print state, county
                details = doc_next.q('//div[@class="hotbox-title"]/following-sibling::table[2]/tr')
                for ind,row in enumerate(details):
                    if ind == 0: continue
                    name = row.x('td[1]/text()').trim().replace(county, '').strip()
                    item.append("label" + str(ind))
                    item.append(name)
                    online = row.x('td[3]/a/@href').trim()
                    item.append("url" + str(ind))
                    item.append(online)
                s.save(item, "csv/"+state + ".csv", remove_existing_file=False)
                print self.state , item
            # threadLock.acquire()
            # threadLock.release()
        except Exception as e:
            print e
    # end thread run function
    
# end class
# *****************************************************************
# main function
if __name__ == '__main__':
    if os.path.exists("result.csv"):
        os.remove("result.csv")
    threads = []
    states = ['AK','AL','AR','AZ','CA','CO','CT','DC','DE','FL','GA','HI','IA','ID','IL','IN','KS','KY','LA','MA','MD','ME','MI','MN','MO','MS','MT','NC','ND','NE','NH','NJ','NM','NV','NY','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VA','VT','WA','WI','WV','WY']
    for state in states:
        
        thrd = ThreadObj(state)
        threads.append(thrd)
    print "run"
    for thrd in threads:
        thrd.start()
        # sleep(1)

    for thrd in threads:
        thrd.join()

# end main function
