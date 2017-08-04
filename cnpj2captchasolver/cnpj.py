from scrapex import *
import os
import os.path
from captcha2upload import CaptchaUpload
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common import exceptions as EX
from time import sleep
from PIL import Image
import csv

sObj = Scraper(use_cache=True, timeout=300, retries=3)
data_url = 'http://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/Cnpjreva_Solicitacao2.asp'
captimg_url = 'http://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/captcha/gerarCaptcha.asp'
captcha_api_key = '3089fd2a0105fc43e44769486dc1e9c1'

class AnyEc:
    """ Use with WebDriverWait to combine expected_conditions
        in an OR.
    """
    def __init__(self, *args):
        self.ecs = args

    def __call__(self, driver):
        for fn in self.ecs:
            try:
                if fn(driver): return True
            except:
                pass

class CnpjScraper(object):
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.set_window_size(1920,1080)

    def get_captcha(self, driver, element, path):
        # now that we have the preliminary stuff out of the way time to get that image :D
        location = element.location
        size = element.size
        # saves screenshot of entire page
        driver.save_screenshot(path)

        # uses PIL library to open image in memory
        image = Image.open(path)

        left = location['x']
        top = location['y'] 
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']

        image = image.crop((left, top, right, bottom))  # defines crop points
        image.save(path, 'jpeg')  # saves new cropped image
        
    def parse(self):
        with open('cnpj_list.csv','rb') as f:
            csv_reader = csv.reader(f)
            item_list = list(csv_reader)
        for row in item_list:
            cnpj = row[0]

            self.driver.get(data_url)
            try:
                os.remove("captcha.jpg")
            except:
                pass

            sleep(1)
            img = self.driver.find_element_by_xpath("//img[@id='imgCaptcha']")
            self.get_captcha(self.driver, img, "captcha.jpg")
            captcha = CaptchaUpload(captcha_api_key)
            captcha_code = captcha.solve('captcha.jpg')
            captcha_code_old = captcha_code

            WebDriverWait(self.driver, 30).until(
                AnyEc(
                    EC.presence_of_element_located((By.XPATH, '//input[@id="cnpj"]')),
                    EC.presence_of_element_located((By.XPATH, '//input[@id="txtTexto_captcha_serpro_gov_br"]'))
                )
            )                

            self.driver.find_element_by_id('cnpj').send_keys(cnpj)
            self.driver.find_element_by_id('txtTexto_captcha_serpro_gov_br').send_keys(captcha_code_old)
            sleep(1)
            self.driver.find_element_by_id('submit1').click()
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//span[@class='Rodape']")))
            html_doc = Doc(html=self.driver.page_source)
            self.parse_detail(html_doc)

        self.driver.quit()
        # except:
        #     return
    def parse_detail(self, response):
        response_xpath = response.q('//div[@id="principal"]/table[2]/tbody/tr/td/table/tbody/tr/td')
        item = []
        for idx,row in enumerate(response_xpath):
            if idx<=1: continue
            try:
                val = row.q('font[2]//text()').join(' ').trim()
                print val
                lbl = row.q('font[1]//text()').join(' ').trim()
                print lbl
                if lbl != '':
                    item.append(lbl)
                    item.append(val)
            except:
                continue
        
        sObj.save(item, 'item.csv')

if __name__ == '__main__':
    scraper = CnpjScraper()
    scraper.parse()