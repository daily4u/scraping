#This is file for application configuration
from time import sleep
import time
import datetime 
import random
import common_lib
import requests


# *****************************************************************    
# special application information
__APP_URL__ =  'http://shop.doverstreetmarket.com'

# *****************************************************************    
def solve_captcha(captcha_site_key, url):
    try:
        s = requests.Session()
        # here we post site key to 2captcha to get captcha ID (and we parse it here too)
        captcha_id = s.post("http://2captcha.com/in.php?key={}&method=userrecaptcha&googlekey={}&pageurl={}".format(common_lib.__RECAPTCHA_API__, captcha_site_key, url)).text.split('|')[1]
        print captcha_id
        # then we parse gresponse from 2captcha response
        recaptcha_answer = s.get("http://2captcha.com/res.php?key={}&action=get&id={}".format(common_lib.__RECAPTCHA_API__, captcha_id)).text
        print("***********************solving ref captcha************************")
        try_count = 0
        total_count = 0
        while 'CAPCHA_NOT_READY' in recaptcha_answer or 'ERROR_CAPTCHA_UNSOLVABLE' in recaptcha_answer:
            sleep(5)
            #logger.info( "Prev Answer: {}, Call 2Captcha....{}".format(recaptcha_answer, captcha_id))
            recaptcha_answer = s.get("http://2captcha.com/res.php?key={}&action=get&id={}".format(common_lib.__RECAPTCHA_API__, captcha_id)).text
            # if total_count == 10:
            #     print("Captcha ID count reached at limit value.")
            #     break

            if try_count == 6:
                break
                print( "Captcha ID was changed." )
                captcha_id = s.post("http://2captcha.com/in.php?key={}&method=userrecaptcha&googlekey={}&pageurl={}".format(common_lib.__RECAPTCHA_API__, captcha_site_key, url)).text.split('|')[1]
                total_count += 1
                try_count = 0

            try_count += 1
        
        if ('CAPCHA_NOT_READY' not in recaptcha_answer) and ('ERROR_CAPTCHA_UNSOLVABLE' not in recaptcha_answer):
            recaptcha_answer = recaptcha_answer.split('|')[1]
            print("^^^^^^^^^^^^^^^^^^^^^^^solved ref captcha^^^^^^^^^^^^^^^^^^^^^^^^^")
        else:
            print("-----------------------not solved ref captcha----------------------")
    except:
        recaptcha_answer = "CAPCHA_NOT_READY"
    print recaptcha_answer
    return recaptcha_answer