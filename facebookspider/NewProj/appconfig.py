#This is file for application configuration
from time import sleep
import time
import datetime 
import random
# *****************************************************************    
# special application information
__EXTENSION_NAME__  = "dekepakjdnlaafaceccgkjoiojgpgpkn.crx"
__USER_ID_FOR_EXT__ = "adicted2"
__APP_URL__         = "https://www.facebook.com"
__OPTION_PATH__     = 'chrome-extension://dekepakjdnlaafaceccgkjoiojgpgpkn/options.html'
__SCROLL_UP_PAGE__  = 2
__SCROLL_MIN_PAGE__ = 8
__SCROLL_MAX_PAGE__ = 15
__MIN_TIME_LIMIT__  = 30000
__MAX_TIME_LIMIT__  = 40000
# *****************************************************************    
# to get number of scroll page
def get_number_of_scroll_page():
    return random.randint(__SCROLL_MIN_PAGE__, __SCROLL_MAX_PAGE__)
# *****************************************************************    
# to get next click tme
def get_next_click_time():
    next_time_click_like_page = time.time() + random.randint(3000, 4000)
    return next_time_click_like_page
# *****************************************************************    
# to get random selection
def get_random_select():
    return random.random()*random.random() > 0.333
# *****************************************************************    
# to get height ratio
def get_height_ratio():
    return (random.random() + 0.5)/2
# *****************************************************************    
# to get randome night time
def get_random_night_time():
    night_hour = random.randint(7, 11)
    return night_hour
# *****************************************************************    
# is night time
def is_night_time(hr):
    now = datetime.datetime.now()
    now_time = now.time()
    if now_time >= datetime.time(hr+12,00) or now_time <= datetime.time(hr,00): 
        return True
    else:
        return False
# *****************************************************************        
