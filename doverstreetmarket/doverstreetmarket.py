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
import argparse

import appconfig
import common_lib
import proxies
import agents
import requests
# from twocaptchaapi import TwoCaptchaApi

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common import exceptions as EX
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

from scrapex import *
import threading
# *****************************************************************    
# define global variables
threadLock = threading.Lock()
# end global varialbles
# *****************************************************************
# define sprider class
class ThreadObj(threading.Thread):
    # init function for class
    def __init__(self, idx, url, size):
        super(ThreadObj, self).__init__()
        self.thread_id    = idx
        self.checkout_url = url
        self.product_size = size
        self.sobj = Scraper(use_cache=False, retries=3, timeout=300, log_post=True, log_headers=True)
        self.driver = self.init_chrome_driver()
        # self.api = TwoCaptchaApi(common_lib.__RECAPTCHA_API__)
    # end function for class
    # *****************************************************************    
    # define init function for Chrome web driver
    def init_chrome_driver(self):
        # to set up arguments and extensions for chrome options
        co = webdriver.ChromeOptions()
        # proxyauth_plugin_path = common_lib.init_proxies(self.thread_id)
        # co.add_extension(proxyauth_plugin_path)
        co.add_argument("--start-maximized")
        co.add_argument("--disable-infobars")
        co.add_argument("--disable-notifications")
        # driver = webdriver.Chrome(chrome_options = co, service_args=["--verbose", "--log-path=facebook.log"])
        driver = webdriver.Chrome(chrome_options = co)
        driver.implicitly_wait(common_lib.__SHORT_TIME__)
        return driver
    # end init function for Chrome web driver
    # *****************************************************************    
    # define init function for Firefox browser driver
    # Mozila Firefox
    # TODO: //
    # end init function for Firefox browser driver
    # *****************************************************************    
    # define init function for PhantomJS
    # PhantomJS
    # TODO: //
    # end init function for PhantomJS
    # *****************************************************************    
    # define thread run function
    # This is thread function user can customize
    # When user execute threadobj.start() function, it will run
    def run(self):
        self.__callback()            
    # end thread run function
    # *****************************************************************    
    # define __callback function
    def __callback(self):
        # go to check out url
        # http://shop.doverstreetmarket.com/nikelab-dsm-ldn/nikelab-air-max-1-royal-se-aa08691-001
        try:
            self.driver.get(self.checkout_url)
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//button[@id="product-addtocart-button"]')))
            # search product size
            product_sizes  = self.driver.find_elements_by_xpath('//div[@class="productAttributes"]/div/div[@class="name-box"]')
            for ps in product_sizes:
                psize = re.search('(\d+)', ps.text).group(1)
                if float(psize) == float(self.product_size):
                    break
            # input quantity of product
            ps_qty = ps.find_elements_by_xpath('preceding-sibling::div[@class="product_qty"]/input')[-1]
            ps_qty.send_keys(Keys.BACK_SPACE)
            ps_qty.send_keys('1')
            # click buy button
            self.driver.find_element_by_id('product-addtocart-button').click() #Click Buy button
            # go to checkout page
            # http://shop.doverstreetmarket.com/checkout/cart/
            try:
                # click proceed to checkout
                WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//button[@title="Proceed to Checkout"]')))
                self.driver.execute_script('window.location="https://shop.doverstreetmarket.com/checkout/onepage/";')
            except Exception as e:
                print e
            # https://shop.doverstreetmarket.com/checkout/onepage/
            self.driver.refresh()
            # login - input email and password
            self.driver.find_element_by_id('login-email').send_keys(agents.accounts[self.thread_id].split(':')[0])
            self.driver.find_element_by_id('login-password').send_keys(agents.accounts[self.thread_id].split(':')[1])
            # captcha processing
            while(True):
                if self.solve_recaptcha("g-recaptcha-response") == False:
                    self.driver.refresh()
                    self.driver.find_element_by_id('login-email').send_keys(agents.accounts[self.thread_id].split(':')[0])
                    self.driver.find_element_by_id('login-password').send_keys(agents.accounts[self.thread_id].split(':')[1])
                else:
                    break
            # end captcha processing
            # if captcha solved, click login button
            self.driver.execute_script('onepageLogin(this);')
            # confirm cart page
            try:
                while (True):
                    WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH,'//table[@id="shopping-cart-table"]/tbody/tr')))
                    cart_table = self.driver.find_elements_by_xpath('//table[@id="shopping-cart-table"]/tbody/tr')

                    if len(cart_table) == 1:
                        print "update 1"
                        WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH,'//td[@class="product-cart-actions"]/input')))
                        self.driver.find_element_by_xpath('//td[@class="product-cart-actions"]/input').clear()
                        self.driver.find_element_by_xpath('//td[@class="product-cart-actions"]/input').send_keys('1')
                        update_button = self.driver.find_element_by_name('update_cart_action')
                        ActionChains(self.driver).move_to_element(update_button).click().perform()
                        print "update 2"
                        break
                    else:
                        print "remove_button 1"
                        WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH,'//td[@class="product-cart-actions"]/li/a')))
                        remove_button = self.driver.find_element_by_xpath('//td[@class="product-cart-actions"]/li/a')
                        remove_button.click()
                        print "remove_button 2"
                self.driver.execute_script('window.location="https://shop.doverstreetmarket.com/checkout/onepage/";')
            except:
                pass
            WebDriverWait(self.driver,30).until(EC.presence_of_element_located((By.XPATH, '//div[@id="checkout-step-billing"]')))
            # 2 - shipping address page : solve captcha
            while(True):
                if self.solve_recaptcha("g-recaptcha-response") == False:
                    self.driver.refresh()
                else:
                    break
            # click continue after solved
            self.driver.execute_script('billing.save();')
            # 3.shipping page - click 
            WebDriverWait(self.driver,30).until(EC.presence_of_element_located((By.XPATH, '//div[@id="checkout-shipping-method-load"]')))
            # click continue
            self.driver.execute_script('shippingMethod.save();')
            # 4. Payment page - click paypal 
            WebDriverWait(self.driver,30).until(EC.presence_of_element_located((By.XPATH, '//input[@id="p_method_paypal_express"]')))
            self.driver.find_element_by_xpath('//input[@id="p_method_paypal_express"]').click()
            # click continue
            self.driver.execute_script('payment.save();')
            # click Login button on Paypal page
            WebDriverWait(self.driver,30).until(EC.presence_of_element_located((By.XPATH, '//div[@class="span11 alignRight baslLoginButtonContainer"]/a')))
            self.driver.find_element_by_xpath('//div[@class="span11 alignRight baslLoginButtonContainer"]/a').click()
            # input paypal email 
            WebDriverWait(self.driver,30).until(EC.presence_of_element_located((By.NAME, 'login_email')))
            self.driver.find_element_by_name('login_email').clear()
            self.driver.find_element_by_name('login_email').send_keys('tdk1989@litto.co.uk')
            # input password
            WebDriverWait(self.driver,30).until(EC.presence_of_element_located((By.NAME, 'login_password')))
            self.driver.find_element_by_name('login_password').clear()
            self.driver.find_element_by_name('login_password').send_keys('test123')
            # click login
            WebDriverWait(self.driver,30).until(EC.presence_of_element_located((By.ID, 'btnLogin')))
            self.driver.find_element_by_id('btnLogin').click()
            # after processing
            # ????
            sleep(20)
        except Exception as e:
            print e
        # finally:
        #     # self.driver.quit()
        #     # exit()

    def solve_recaptcha(self, answer_id):
        try:
            html = Doc(html=self.driver.page_source)
            # iframe_url = html.q('//div[@id="g-recaptcha-1"]//iframe')[0].x("@src").strip()
            # print iframe_url
            # sitekey = re.search("k\=(.*?)\&", iframe_url).group(1)
            # print sitekey
            # print "6LdMlR0UAAAAANGX2TtfgCpfT3250zN1mBKAsmDc"

            sitekey = '6LdMlR0UAAAAANGX2TtfgCpfT3250zN1mBKAsmDc'
            captcha_answer = ""
            if sitekey != "":
                captcha_answer = appconfig.solve_captcha(sitekey, 'https://shop.doverstreetmarket.com/checkout/onepage/')
            else:
                print "Site key is not valid"
                return False
            
            if "CAPCHA_NOT_READY" in captcha_answer:
                print "captcha is not solved"
                return False

            else:
                textarea_response = self.driver.find_element_by_xpath("//textarea[contains(@id, '{}')]".format(answer_id))
                script_str = "document.getElementById('{}').style.display='block';".format(answer_id)
                self.driver.execute_script(script_str)

                script_str = "document.getElementById('{}').value='{}';".format(answer_id, captcha_answer)
                self.driver.execute_script(script_str)
                sleep(1)
        except Exception as e:
            # self.put_screenshot("captcha.png")
            # self.show_exception_detail(e)
            return False

        return True
# end class
    
# main function
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--url",  type=str, help="url: checkout url - e.g.,  http:// or https://")
    parser.add_argument("-s", "--size", type=str, help="size: product size - e.g., 10.5")
    args = parser.parse_args()
    # url argument
    try:
        protocol = re.search('(http|https)://[\w\-]+(\.[\w\-]+)+\S*', args.url, re.S|re.M).group(1)
        if protocol == 'http' or protocol == 'https':
            url = args.url
            if not appconfig.__APP_URL__ in url:
                raise
        else:
            raise
    except Exception as e:
        print "Invalid URL!"
        print "If checkout url is correct, please confirm command. You must type like following:"
        print "python doverstreetmarket.py --url http://example.com/checkout --size 10.5"
        exit()
    # size argument
    try:
        size = float(args.size)
    except:
        print "Invalid Size."
        print "If product size is correct, please confirm command. You must type like following:"
        print "python doverstreetmarket.py --url http://example.com/checkout --size 10.5"
        exit()
    print "Start"
    
    threads = []
    for i in range(common_lib.__THREAD_NUMBER__):
        thrd = ThreadObj(i, url, size)
        threads.append(thrd)

    for idx, thrd in enumerate(threads):
        thrd.start()

    for thrd in threads:
        thrd.join()

# end main function
