from time import sleep
import random
import proxies

# general information
__SHORTEST_TIME__   = 1   # sleep 0 ~ 1 second
__SHORTER_TIME__    = 3   # sleep 1 ~ 3 second
__SHORT_TIME__      = 5   # sleep 3 ~ 6 second
__MIDDLE_TIME__     = 10  # sleep 8 ~ 16 second
__LONG_TIME__       = 30  # sleep 15 ~ 30 second
__LONGER_TIME__     = 60  # sleep 30 ~ 60 second
__LONGEST_TIME__    = 120 # sleep 30 ~ 60 second
__THREAD_NUMBER__   = 1    # Thread number
__RECAPTCHA_API__   = '7673459b554c984ca2756ec53b17705b' # api from 2captcha.com

# define wait function
def wait(sleep_time, log_text=''):
    if sleep_time == __SHORTEST_TIME__:
        rand_sleep_time = (random.random() + 0.1) #sleep time set up randomly
    else:    
        rand_sleep_time = random.randrange(sleep_time/2, sleep_time) #sleep time set up randomly
    print log_text + ":", rand_sleep_time, "seconds" # log
    sleep(rand_sleep_time)  # sleep 

# end wait function
#******************************************************************
# define init proxies
def init_proxies(idx):
    proxy_host = proxies.proxies[idx].split(':')[0]
    proxy_port = proxies.proxies[idx].split(':')[1]
    proxy_username = __PROXY_USER__
    proxy_password = __PROXY_PWD__
    print "Proxy Info:", "IP:" + proxy_host, "PORT:" + str(proxy_port), "USER:" + proxy_username, "PWD:" + proxy_password
    proxyauth_plugin_path = create_proxyauth_extension(
        proxy_host=proxy_host,
        proxy_port=proxy_port,
        proxy_username=proxy_username,
        proxy_password=proxy_password
    )

    return proxyauth_plugin_path
# end init proxies
# *****************************************************************    
# proxy setting function
def create_proxyauth_extension(proxy_host, proxy_port,
                               proxy_username, proxy_password,
                               scheme='http', plugin_path=None):
    """Proxy Auth Extension
    args:
        proxy_host (str): domain or ip address, ie proxy.domain.com
        proxy_port (int): port
        proxy_username (str): auth username
        proxy_password (str): auth password
    kwargs:
        scheme (str): proxy scheme, default http
        plugin_path (str): absolute path of the extension       
    return str -> plugin_path
    """

    import string
    import zipfile

    if plugin_path is None:
        plugin_path = 'proxy_auth_plugin.zip'
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = string.Template(
    """
    var config = {
            mode: "fixed_servers",
            rules: {
              singleProxy: {
                scheme: "${scheme}",
                host: "${host}",
                port: parseInt(${port})
              },
              bypassList: ["foobar.com"]
            }
          };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "${username}",
                password: "${password}"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """
    ).substitute(
        host=proxy_host,
        port=proxy_port,
        username=proxy_username,
        password=proxy_password,
        scheme=scheme,
    )

    with zipfile.ZipFile(plugin_path, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    return plugin_path     
# end proxy setting function
# *****************************************************************