from scrapex import *
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
def main():
    s = Scraper()
    start_url = 'http://tvcompetitions.com.au/channel-7-competitions/sunrise-cash-cow-win-10000or-code/'
    doc = s.load(url=start_url)
    item_text       = doc.x('//div[@class="entry-content"]/ul/li[1]/strong/text()').trim()
    try:
        item_date       = re.search('(.*?) SMS the codeword', item_text ,re.S|re.M).group(1).strip()
    except:
        item_date       = ''
    try:
        item_codeword   = re.sub('[^\x00-\x7F]+',' ',re.search('the codeword (.*)', item_text, re.S|re.M).group(1)).strip()
    except:
        item_codeword   = ''
    s.save(['Date', item_date, 'Codeword', item_codeword], 'result.csv', remove_existing_file=False)

    driver = webdriver.Chrome()
    driver.get('https://app.clickfunnels.com/for_domain/denmurphy.clickfunnels.com/optin14932131?updated_at=ca7ac4de2fdf73792ecc8bee08a6e8d5v2&track=0&preview=true')
    email_address = 'john@gmail.com'
    sleep(2)
    driver.find_element_by_name("email").send_keys(email_address)
    sleep(2)
    driver.find_element_by_name("email").send_keys(Keys.RETURN)
    sleep(10)
    driver.quit()
if __name__ == '__main__':
    main()
    