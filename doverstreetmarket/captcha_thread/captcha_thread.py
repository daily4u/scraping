# Reference  - 'https://github.com/hunterbdm/ANBAIO2captcha'
# https://github.com/athre0z/twocaptcha-api/tree/master/twocaptchaapi

import requests
import time
import threading
import webbrowser
import random
import datetime
import re
from scrapex import *
import os
import os.path

proxies = []
apikey = None
site = 0

active_threads = 0
captchas_sent = 0

site_urls = ['https://shop.doverstreetmarket.com/customer/account/login/referer/aHR0cDovL3Nob3AuZG92ZXJzdHJlZXRtYXJrZXQuY29tLw,,/',]
s = Scraper(
    use_cache = False,
    retries = 3, 
    timeout = 300
)
def main():
    global apikey

    # Get 2captcha APIKEY
    try:
        apikey_file = open('apikey.txt')
        apikey = apikey_file.read().replace('\n', '').strip()
        apikey_file.close()
    except:
        print('Unable to read apikey.txt')
        exit()

    print('Got APIKEY:', apikey)
    print('Balance:', get_balance())

    # Get proxies
    try:
        proxy_file = open('proxies.txt')
        for proxy in proxy_file.read().splitlines():
            # No lines should have spaces, so remove all of them
            proxy = proxy.replace(' ', '')
            # Now that we removed extra spaces, if there is nothing remaining on that line, we wont add it to the list.
            if not proxy == '':
                proxies.append(proxy)
        proxy_file.close()
        print(len(proxies), 'proxies found.')
        print(proxies)
    except:
        print('Unable to read proxies.txt, continuing without proxies.')

    sitekey = get_sitekey()
    print('Got sitekey', sitekey)

    print(
"""
--  Modes  --
1. Normal        (Request X amount of captchas now, and stop after.)
2. Never Ending. (Request X amount of captchas every Y minutes.)
"""
    )
    mode = get_integer('Select a mode: ')

    if mode == 2:
        print('Using Never Ending mode.')
        # Get how often we should request captchas.
        minutes = get_float('How often to request new captchas(in minutes): ')
        sleep_time = minutes * 60
        request_amount = get_integer('How many captchas to request every ' + str(minutes) + ' minutes: ')

        print('Requesting', str(request_amount), 'captchas every', str(minutes), 'minutes.')

        while True:
            # Since we are not requesting all at once, we will check if AIO bot changed the sitekey on the solver page.
            new_sitekey = get_sitekey()
            if not new_sitekey == sitekey:
                print(get_time(), '- Sitekey changed:', new_sitekey)
                sitekey = new_sitekey
            for i in range(0, request_amount-1):
                t = threading.Thread(target=get_token_from_2captcha, args=(sitekey,))
                t.daemon = True
                t.start()
                time.sleep(0.1)
            print(get_time(), '-', 'Requested', str(request_amount), 'captchas.')
            time.sleep(sleep_time)
    else:
        print('Using Normal Mode.')
        while True:
            x = int(input('How many captchas?: '))

            for i in range(0, int(x)):
                t = threading.Thread(target=get_token_from_2captcha, args=(sitekey,))
                t.daemon = True
                t.start()
                time.sleep(0.1)
            print('Requested ' + str(x) + ' captcha(s).')
            while not active_threads == 0:
                print('-------------------------')
                print('Active Threads          -', active_threads)
                print('Captchas Sent to ANBAIO -', captchas_sent)
                time.sleep(5)

            print('-------------------------')
            print('Active Threads          -', active_threads)
            print('Captchas Sent to ANBAIO -', captchas_sent)


# def check_updates():
#     # Check if the current version is outdated
#     try:
#         response = requests.get('https://raw.githubusercontent.com/hunterbdm/ANBAIO2captcha/master/README.md')
#     except:
#         print('here')
#         print('Unable to check for updates.')
#         return

#     # If for some reason I forget to add the version to readme I dont want it to fuck up
#     if 'Latest Version' in response.text:
#         # Grab first line in readme. Will look like this 'Latest Version: 1.0.0.0'
#         latest = (response.text.split('\n')[0])
#         # Will remove 'Latest Version: ' from string so we just have the version number
#         latest = latest[(latest.index(':') + 2):]
#         if not latest == current_version:
#             print('You are not on the latest version.')
#             print('Your version:', current_version)
#             print('Latest version:', latest)
#             x = input('Would you like to download the latest version? (Y/N) ').upper()
#             while not x == 'Y' and not x == 'N':
#                 print('Invalid input.')
#                 x = input('Would you like to download the latest version? (Y/N) ').upper()
#             if x == 'N':
#                 return
#             print('You can find the latest version here https://github.com/hunterbdm/ANBAIO2captcha')
#             webbrowser.open('https://github.com/hunterbdm/ANBAIO2captcha')
#             exit()
#         print('No updates currently available. Version:', current_version)
#         return
#     print('Unable to check for updates.')
#     return


def get_balance():
    s.clear_cookies()
    while True:
        data = {
            'key': apikey,
            'action': 'getbalance',
            'json': 1,
        }
        try:
            response = s.load_json(url='http://2captcha.com/res.php', post=data)
            if response['status'] == 1:
                balance = response['request']
                return balance
        except:
            print('Incorrect APIKEY, exiting.')
            exit()

def get_token_from_2captcha(sitekey):
    """
    All credit here to https://twitter.com/solemartyr, just stole this from his script
    """
    global active_threads

    active_threads += 1
    s.clear_cookies()
    pageurl = site_urls[site]

    while True:
        data = {
            'key': apikey,
            'action': 'getbalance',
            'json': 1,
        }
        try:
            response = s.load_json(url='http://2captcha.com/res.php', post=data)
        except:
            print('Incorrect APIKEY, exiting.')
            exit()

        captchaid = None
        proceed = False
        while not proceed:
            data = {
                'key': apikey,
                'method': 'userrecaptcha',
                'googlekey': sitekey,
                'proxy': 'localhost',
                'proxytype': 'HTTP',
                'pageurl': pageurl,
                'json': 1
            }

            if not len(proxies) == 0:
                # We will just pick randomly from the list because it doesn't matter if we use one more than others.
                data['proxy'] = random.choice(proxies)

            # response = session.post(url='http://2captcha.com/in.php', data=data)
            try:
                json = s.load_json(url='http://2captcha.com/in.php', post=data)
            except:
                time.sleep(3)
                continue

            if json['status'] == 1:
                captchaid = json['request']
                proceed = True
            else:
                time.sleep(3)
        time.sleep(3)
        print captchaid
        token = None
        proceed = False
        k = 0
        while not proceed:
            data = {
                'key': apikey,
                'action': 'get',
                'json': 1,
                'id': captchaid,
            }
            
            json = s.load_json(url='http://2captcha.com/res.php', post=data)
            if json['status'] == 1:
                token = json['request']
                proceed = True
            else:
                time.sleep(3)
                k = k + 1
                if k == 6:
                    break

        if token is not None:
            send_captcha(token)
            return


def get_sitekey():
    try:
        s.clear_cookies()
        resp    = s.load_html(url=site_urls[site])
        sitekey = re.findall("'sitekey' : '(.*?)',", resp)[0]
        if sitekey is None:
            print('Unable to get sitekey, server may be down.')
            return None
        return sitekey
    except:
        print('Unable to get sitekey, server may be down.')
        return None


def send_captcha(captcha_response):
    global active_threads
    global captchas_sent
    s.save(["time", time.time(),"response", captcha_response,"used", "0"], 'captcha_bank.csv', remove_existing_file=False)
    print time.time(), "Captcha response Saved."
    active_threads -= 1
    captchas_sent += 1
    print(get_time(), '- Captcha sent to AIO Bot.')
    return
    # try:
    #     session = requests.Session()
    #     session.verify = False
    #     session.cookies.clear()

    #     post_url = post_urls[site]
    #     data_name = post_url[(post_url.index('54785/') + 6):]

    #     data = {
    #         data_name: captcha_response
    #     }
    #     resp = session.post(post_url, data=data)
    #     if resp.status_code is 200:
    #         active_threads -= 1
    #         captchas_sent += 1
    #         print(get_time(), '- Captcha sent to AIO Bot.')
    #         return
    # except:
    #     print('Unable to send captcha, server may be down.')
    #     active_threads -= 1
    #     return None


def get_integer(text):
    while True:
        try:
            response = int(input(text))
            break
        except:
            print('Invalid input, should be a number.')
            continue
    return response


def get_float(text):
    while True:
        try:
            response = float(input(text))
            break
        except:
            print('Invalid input, should be a number.')
            continue
    return response


def get_time():
    ctime = str(datetime.datetime.fromtimestamp(time.time()))
    return (ctime[11: (len(ctime) - 3)])

if __name__ == "__main__":
    if os.path.exists('captcha_bank.csv'):
        os.remove('captcha_bank.csv')
    
    main()