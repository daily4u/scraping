from scrapex import *
import re
import csv
import json
import requests
import time
import os
import os.path

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common import exceptions as EX
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains


captcha_no = 0
session = None
driver = None
__USER_E_MAIL__      = "tdk1989@litto.co.uk"
__USER_PASSWD__      = "test123"
__PAYPAL_E_MAIL__    = "tdk1989@litto.co.uk"
__PAYPAL_PASSWD__    = "test123"

def main():
    global session
    global driver
    
    print """ 
*******************************************************************************************************************
***   File: cart_url.csv                                                                                          *
***   *******************                                                                                         *
***   Structure:                                                                                                  *
***       product_url,                                                                                    size    *
***       "http://shop.doverstreetmarket.com/nikelab-dsm-ldn/nikelab-air-max-1-royal-se-aa08691-001",     10.5    *
***       ...                                                                                                     *
*******************************************************************************************************************
    """
    with open('cart_urls.csv','rb') as cartfile:
        content = csv.DictReader(cartfile)
        product_contents = list(content)
    print """
*******************************************************************************************************************
***                                                                                                               *
*** Confirm product urls and sizes                                                                                *
***"""
    for row in product_contents:
        print "***",row['product_url'], "," , row['size']
    print """***
***                                                                                                               *
*******************************************************************************************************************
    """
    x = raw_input('Are you okay? (Y/N) ').upper()
    while not x == 'Y' and not x == 'N' and not x == '':
        print('Invalid Answer.Please try again.')
        x = input('Are you okay? (Y/N) ').upper()
    if x == 'N':
        print"""
*******************************************************************************************************************
***                                                ___END___                                                    ***
*******************************************************************************************************************
        """
        exit()
    print """
*******************************************************************************************************************
***                                               ___START___                                                   ***
*******************************************************************************************************************
    """
    session = requests.Session()
    session.cookies.clear()
    site_url = 'https://shop.doverstreetmarket.com'

    headers = {
        'Host': 'shop.doverstreetmarket.com',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://shop.doverstreetmarket.com',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
    }
    
    while (True):

        site_login_url = 'https://shop.doverstreetmarket.com/customer/account/login/referer/aHR0cDovL3Nob3AuZG92ZXJzdHJlZXRtYXJrZXQuY29tLw,,/'
        doc = session.request("GET", site_login_url).text
        html_doc = Doc(html=doc)
        # form_action_url         =   html_doc.x('//form[@id="login-form"]/@action')
        form_action_url             =   'https://shop.doverstreetmarket.com/customer/account/loginPost/referer/aHR0cDovL3Nob3AuZG92ZXJzdHJlZXRtYXJrZXQuY29tLw,,/'
        form_key                    =   html_doc.x('//form[@id="login-form"]/input[@name="form_key"]/@value')
        login_email                 =   __USER_E_MAIL__
        login_password              =   __USER_PASSWD__
        while True:
            try:
                g_recaptcha_response = get_g_recaptch_response()
                if g_recaptcha_response != None:
                    break
            except Exception as e:
                print e
            time.sleep(3)

        form_data = {
            "form_key"              :   form_key,
            "login[username]"       :   login_email,
            "login[password]"       :   login_password,
            "g-recaptcha-response"  :   g_recaptcha_response,
            "send"                  :   ""
        }
        cookies = requests.cookies.RequestsCookieJar()
        cookies.set('EXTERNAL_NO_CACHE', '1', domain='shop.doverstreetmarket.com', path='/customer/account/loginPost/referer/aHR0cDovL3Nob3AuZG92ZXJzdHJlZXRtYXJrZXQuY29tLw,,')
        res = session.request("POST", form_action_url, data=form_data, headers=headers, cookies=cookies, allow_redirects=False)
        print res.status_code
        curr_cookie = session.cookies.get_dict()
        print curr_cookie
        try:
            if res.status_code == 302 and curr_cookie['IS_LOGGED_IN'] == '1':
                break
        except Exception as e:
            print e

        time.sleep(3)

    res = session.request("GET",site_url, headers=headers)
    curr_cookie = session.cookies.get_dict()
    for row in product_contents:
        doc = session.request("GET", row['product_url'], headers=headers)
        html_doc = Doc(html=doc.text)
        form_cart_url  = html_doc.x('//form[@id="product_addtocart_form"]/@action').trim()
        
        cart_form_data = {}
        cart_form_data['product'] = html_doc.x('//input[@name="product"]/@value')
        cart_form_data['related_product'] = html_doc.x('//input[@name="related_product"]/@value')
        cart_form_data['is_multi_order'] = html_doc.x('//input[@name="is_multi_order"]/@value')

        product_qtys   = html_doc.q('//div[@class="productAttributes"]/div/div[@class="product_qty"]')
        product_sizes  = html_doc.q('//div[@class="productAttributes"]/div/div[@class="name-box"]')
        
        cart_index = -1
        for ind, size in enumerate(product_sizes):
            size_name = size.x('input/@name').trim()
            size_val = size.x('input/@value').trim()
            cart_form_data[size_name] = size_val
            psize = re.search('(\d+)', size.x('text()').trim()).group(1)
            if float(psize) == float(row['size']):
                cart_index = ind
        
        for ind, qty in enumerate(product_qtys):
            qty_name = qty.x('input/@name').trim()
            if ind == cart_index:
                cart_form_data[qty_name] = 1
            else:
                cart_form_data[qty_name] = 0

        res = session.request("POST", form_cart_url, data=cart_form_data, headers=headers, allow_redirects=False)
        if res.status_code == 302:
            res = session.request("GET", "http://shop.doverstreetmarket.com/checkout/cart/", data=cart_form_data, headers=headers, allow_redirects=False)
        else:
            print "Cart Error"
    
    """
        Cart End/Billing Start
    """
    res = session.request("GET","https://shop.doverstreetmarket.com/checkout/onepage/", headers=headers)
    driver = webdriver.Chrome()
    driver.get("https://shop.doverstreetmarket.com/")
    return
    driver.delete_all_cookies()
    for c in session.cookies:
        driver.add_cookie({'name': c.name, 'value': c.value, 'path': c.path, 'expiry': c.expires})

    driver.get(res.url)
    for c in session.cookies:
        driver.add_cookie({'name': c.name, 'value': c.value, 'path': c.path, 'expiry': c.expires})

    WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH, '//div[@id="checkout-step-billing"]')))
    # 2 - shipping address page : solve captcha
    while True:
        try:
            g_recaptcha_response = get_g_recaptch_response()
            if g_recaptcha_response != None:
                textarea_response = driver.find_element_by_xpath("//textarea[contains(@id, '{}')]".format('g-recaptcha-response'))
                script_str = "document.getElementById('{}').style.display='block';".format('g-recaptcha-response')
                driver.execute_script(script_str)

                script_str = "document.getElementById('{}').value='{}';".format('g-recaptcha-response', g_recaptcha_response)
                driver.execute_script(script_str)
                time.sleep(1)
                
                driver.execute_script('billing.save();')
                accept_alert(driver)
                time.sleep(1)
                if "Invalid" in driver.page_source:
                    continue
                else:
                    break
            time.sleep(3)
        except Exception as e:
            print e
    # click continue after solved

    # 3.shipping page - click 
    print "Shipping Method"
    WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH, '//div[@id="checkout-step-shipping_method"]')))
    time.sleep(1)
    # click continue
    driver.execute_script('shippingMethod.save();')
        # 4. Payment page - click paypal 
    # WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH, '//input[@id="p_method_paypal_express"]')))
    # driver.find_element_by_xpath('//input[@id="p_method_paypal_express"]').click()
    print "Paypal Setting"
    WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH, '//input[@id="p_method_paypal_express"]')))
    time.sleep(1)
    driver.find_element_by_id('p_method_paypal_express').click()
    driver.execute_script('payment.switchMethod("paypal_express");')
    # click continue
    print "Paypal Save"
    driver.execute_script('payment.save();')
    # click Login button on Paypal page
    WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH, '//div[@class="span11 alignRight baslLoginButtonContainer"]/a')))
    driver.find_element_by_xpath('//div[@class="span11 alignRight baslLoginButtonContainer"]/a').click()
    # input paypal email 
    WebDriverWait(driver,30).until(EC.presence_of_element_located((By.NAME, 'login_email')))
    time.sleep(1)
    driver.find_element_by_name('login_email').clear()
    driver.find_element_by_name('login_email').send_keys(__PAYPAL_E_MAIL__)
    # input password
    WebDriverWait(driver,30).until(EC.presence_of_element_located((By.NAME, 'login_password')))
    driver.find_element_by_name('login_password').clear()
    driver.find_element_by_name('login_password').send_keys(__PAYPAL_PASSWD__)
    # click login
    WebDriverWait(driver,30).until(EC.presence_of_element_located((By.ID, 'btnLogin')))
    driver.find_element_by_id('btnLogin').click()    
    # click No, thanks / Close button
    WebDriverWait(driver,30).until(EC.presence_of_element_located((By.CLASS_NAME, 'close')))
    driver.find_element_by_class_name('close').click()
    # confirm page input [@id=confirmButtonTop]
    WebDriverWait(driver,30).until(EC.presence_of_element_located((By.ID, 'confirmButtonTop')))
    driver.find_element_by_id('confirmButtonTop').click()
    # order Review page
    WebDriverWait(driver,30).until(EC.presence_of_element_located((By.ID, 'agreement-1]')))
    driver.find_element_by_id('agreement-1]').click()
    # click place order
    # place_order_btn = self.driver.find_element_by_id('review_button')
    # ActionChains(self.driver).move_to_element(place_order_btn).click().perform()

    # sleep(1000)

def get_g_recaptch_response():
    global captcha_no
    while(True):
        if os.path.exists('captcha_bank.csv'):
            print "File exists"
            break
        print "No File"
        time.sleep(3)
    time.sleep(3)
    print "---------------------1------------------------"
    with open('captcha_bank.csv','r+') as bank_file:
        reader = csv.DictReader(bank_file)
        for ind, row in enumerate(reader):
            print "Index", ind
            print "Captcha No", captcha_no
            if ind < captcha_no: 
                continue
            print "-----------------------2----------------------"
            print "Between time", time.time() - float(row['time'])
            if (time.time() - float(row['time'])) < 120:
                print row
                captcha_no = captcha_no + 1
                print captcha_no
                bank_file.close()
                return row['response']
    return None
# functon for processing alert
def accept_alert(driver):
    try:
        # Wait 10 seconds till alert is present
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        # Accepting alert.
        driver.switch_to.alert.accept();
    except Exception as e:
        print e
if __name__ == '__main__':
    main()
