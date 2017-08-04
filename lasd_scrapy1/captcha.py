from scrapex import *
import time
import sys
import csv
import re, random, base64
import json
# import MySQLdb as mdb
import pymysql as mdb
from captcha2upload import CaptchaUpload
from datetime import datetime
import urllib
import pytz
import os.path
import os

captcha_api_key = "3124db5dec29ab4024f2a7357889651a"


if __name__ == '__main__':
	# logger = logger
	# lasd_url = 'http://app5.lasd.org/iic/'
	# print lasd_url
	captcha = CaptchaUpload(captcha_api_key)
	captcha_code = captcha.solve('captcha2.png')
	print captcha_code
	
	# captcha = CaptchaUpload(captcha_api_key)
	# print captcha.getbalance()
