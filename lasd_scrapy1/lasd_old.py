from scrapex import *
import time
import sys
import csv
import re, random, base64
import json
import MySQLdb as mdb
from captcha2upload import CaptchaUpload
from datetime import datetime
import urllib
import pytz
import os.path
import os
# from pathlib import Path

captcha_api_key = "3124db5dec29ab4024f2a7357889651a"

# con = mdb.connect('localhost', 'root', 'root', 'lasd')
# con = mdb.connect('localhost', 'root', 'dnflgmlakd888', 'lasd')
con = mdb.connect('localhost', 'root', 'developsmith', 'lasd')
# with con:
# 	cur = con.cursor()
# 	cur.execute("DROP TABLE IF EXISTS lasd")
# 	cur.execute("CREATE TABLE lasd(Id INT PRIMARY KEY AUTO_INCREMENT, BookingNo VARCHAR(25), LastName VARCHAR(30), FirstName VARCHAR(30), MiddleName VARCHAR(30), Birthday VARCHAR(30), Age VARCHAR(10), Sex VARCHAR(10), Race VARCHAR(10), Hair VARCHAR(20), Eyes VARCHAR(20), Height VARCHAR(10), Weight VARCHAR(10), ArrestDate VARCHAR(25), ArrestTime VARCHAR(25), CapturedDate VARCHAR(25), CapturedTime VARCHAR(25), ArrestAgency VARCHAR(25), AgencyDescription VARCHAR(100), DateBooked VARCHAR(25), TimeBooked VARCHAR(25), BookingLocation VARCHAR(25), LocationDescription VARCHAR(100), TotalBailAmount VARCHAR(25), TotalHoldBailAmount VARCHAR(25), GrandTotal VARCHAR(25), HousingLocation VARCHAR(35), PermanentHousingAssignedDate VARCHAR(25), AssignedTime VARCHAR(25), VisitorStatus VARCHAR(10), Facility VARCHAR(45), Address VARCHAR(45), City VARCHAR(45))")

if __name__ == '__main__':
	proxy_file_name = 'proxy_Chris.txt'
	s = Scraper(use_cache=False, retries=3, timeout=30, proxy_file=proxy_file_name, one_proxy=True)
	# s = Scraper(use_cache=False, retries=3, timeout=30)
	logger = s.logger

	tz = pytz.timezone('US/Hawaii')

	iindex = 0
	jindex = 0
	if (os.path.isfile('config.txt')):
		config_file = open('config.txt','r')
		config_txt = config_file.read()
		# config_txt = Path('config.txt').read_text()
		print config_txt
		try:
			iindex = int(re.search('i\=([0-9]*)\,j\=([0-9]*),', config_txt,re.M|re.I|re.S).group(1))
			jindex = int(re.search('i\=([0-9]*)\,j\=([0-9]*),', config_txt,re.M|re.I|re.S).group(2))
			logger.info('iindex= %s' %iindex)
			logger.info('jindex= %s' %jindex)
		except:
			pass

	with open('lastname.json') as json_data:
		last_name_list = json.load(json_data)
		name_str = "abcdefghijklmnopqrstuvwxyz"
		# name_str = "abcd"
		first_name_list = list(name_str)
		
		# logger.info('len_last_name_list= %s' %(len(last_name_list)-1))
		# logger.info('len_first_name_list= %s' %(len(first_name_list)-1))
	while (True):
		

		for i in range(iindex, len(last_name_list)):
			for j in range(jindex, len(first_name_list)):
				logger.info('i= %s' %i)
				logger.info('j= %s' %j)

				if os.access('config.txt', os.W_OK):
					config_file.close()
				config_file = open('config.txt','w')
				config_file.write('i=%s,'%i)
				config_file.write('j=%s,'%j)
				iindex = i
				jindex = j
				
				s = Scraper(use_cache=False, retries=3, timeout=30, proxy_file=proxy_file_name, one_proxy=True)
				# s = Scraper(use_cache=False, retries=3, timeout=30)
				try:
					lasd_url = 'http://app4.lasd.org/iic/ajis_search.cfm'
					doc = s.load(lasd_url)
				except:
					pass
				# currentdate = datetime.now().strftime('%Y-%m-%d')
				# currenttime = datetime.now().strftime('%H:%M')
				currentdate = datetime.now(tz).strftime('%Y-%m-%d')
				currenttime = datetime.now(tz).strftime('%H:%M')
				logger.info('Current date: %s' % currentdate)
				logger.info('Current time: %s' % currenttime)

				formdata = {
					'method': 'post',
					'currentdate':currentdate,
					'currenttime':currenttime,
					'startdate': '03/05/2014',
					'starttime':'08:00',
					'enddate':'03/05/2014',
					'endtime':'12:00',
					'last_name':str(last_name_list[i]['LastName']),
					'first_name':str(first_name_list[j]),
					'middle_name':'',
					'dob':'',
					'search':'Search'
				}
				logger.info('Last Name -> %s' % str(last_name_list[i]['LastName']))
				logger.info('First Name -> %s' % str(first_name_list[j]))
				
				try:
					url = "http://app4.lasd.org/iic/iverifysearch.cfm"
					doc = s.load(url, post=formdata)
					logger.info(doc.status.final_url)
					# logger.info(doc)
					img_url = doc.x('//img[@alt="Captcha image"]/@src')
					logger.info('img_url -> %s' % img_url)
				except:
					pass

				# img_url = doc.x('//img[@alt="Captcha image"]/@src')
				# logger.info('img_url -> %s' % img_url)

				if len(img_url) > 0:
					ckey = doc.x('//input[@name="ckey"]/@value')
					logger.info('ckey -> %s' % ckey)
					
					u = s.client.opener.open(img_url)
					f = open('captcha.png', 'wb')
					block_sz = 8192
					while True:
						buf = u.read(block_sz)
						if not buf:
							break
						f.write(buf)
					f.close()
					try:
						captcha = CaptchaUpload(captcha_api_key)
						captcha_code = captcha.solve('captcha.png')
						captcha_code_old = captcha_code
						logger.info('1st_captcha2_code -> %s' %captcha_code)
						# print ("-----1st_captcha2_code------", captcha_code)
					except:
						pass
					formdata = {
						"key" : captcha_code,
						"ckey" : captcha_code,
						"submit" : "Submit"
					}
					try:
						doc = s.load("http://app4.lasd.org/iic/iverifysearch.cfm", post=formdata)
					
						booking_no = doc.q("//table[@class='Grid']//tr/td/a")[-1].x('text()')
						booking_url = doc.q("//table[@class='Grid']//tr/td/a")[-1].x('@href')
						form_action_url = doc.x("//form/@action")
						captchaText = doc.x("//form[@name='inm_lst']/input[@name='captchaText']/@value")
						comment1 = doc.x("//form[@name='inm_lst']/input[@name='comment1']/@value")
						logger.info('booking_no -> %s' % booking_no)
						logger.info('booking_url -> %s' % booking_url)
						logger.info('form_action_url -> %s' % form_action_url)
						logger.info('captchaText -> %s' % captchaText)
						logger.info('comment1 -> %s' % comment1)
						tmp = booking_url.split("javascript:getsupport('", 1)
						# print ("*****************************")
						rtmp = tmp[1].split("')", 1)
						
						logger.info('bkgno -> %s' % rtmp[0])

						formdata = {
							"captchaText" : captchaText,
							"comment1" : comment1,
							"supporttype" : rtmp[0],
							"bkgno" : rtmp[0],
						}
					except:
						form_action_url = ""
						formdata = {
							"captchaText" : "",
							"comment1" : "",
							"supporttype" : "",
							"bkgno" : "",
						}
						
					try:
						doc = s.load(form_action_url, post=formdata)

						img_url = doc.x('//img[@alt="Captcha image"]/@src')
						logger.info('img_url -> %s' % img_url)
					except:
						pass

					if len(img_url) > 0:
						
						u = s.client.opener.open(img_url)
						f = open('captcha2.png', 'wb')
						block_sz = 8192
						while True:
							buf = u.read(block_sz)
							if not buf:
								break
							f.write(buf)
						f.close()
						try:
							captcha = CaptchaUpload(captcha_api_key)
							captcha_code = captcha.solve('captcha2.png')
							logger.info('2st_captcha2_code -> %s' %captcha_code)

							formdata = {
								"ckey" : captcha_code_old,
								"key" : captcha_code,
								"submit" : "Submit"
							}
						
							headers	= {
								"Host" : "app4.lasd.org",
								"User-Agent" : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0",
								"Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
								"Accept-Language" : "en-US,en;q=0.5",
								"Accept-Encoding" : "gzip, deflate, br",
								"Referer" : form_action_url,
								"Upgrade-Insecure-Requests": "1"
							}
						
							doc = s.load(form_action_url, post=formdata, headers=headers, merge_headers = True)
							# doc = s.load_html(form_action_url, post=formdata, headers=headers, merge_headers = True)
							# print(doc)
						except:
							pass

						logger.info('captcha_code_old -> %s' %captcha_code_old)
						logger.info('captcha_code -> %s' %captcha_code)
						logger.info('form_action_url -> %s' %form_action_url)

						BookingNo = doc.x("//form[@name='bkg_detail']/input[@name='bkg_booking_no']/@value").strip()
						LastName = doc.x("//form[@name='bkg_detail']/input[@name='bkg_inmate_last_name']/@value").strip()
						FirstName = doc.x("//form[@name='bkg_detail']/input[@name='bkg_inmate_first_name']/@value").strip()
						MiddleName = doc.x("//form[@name='bkg_detail']/input[@name='bkg_inmate_middle_name']/@value").strip()
						Birthday = doc.x("//form[@name='bkg_detail']/input[@name='bkg_date_of_birth']/@value").strip()
						Age = doc.x("//form[@name='bkg_detail']/input[@name='bkg_age']/@value").strip()
						Sex = doc.x("//form[@name='bkg_detail']/input[@name='bkg_sex']/@value").strip()
						Race = doc.x("//form[@name='bkg_detail']/input[@name='bkg_race']/@value").strip()
						Hair = doc.x("//form[@name='bkg_detail']/input[@name='bkg_hair']/@value").strip()
						Eyes = doc.x("//form[@name='bkg_detail']/input[@name='bkg_eyes']/@value").strip()
						Height = doc.x("//form[@name='bkg_detail']/input[@name='bkg_height']/@value").strip()
						Weight = doc.x("//form[@name='bkg_detail']/input[@name='bkg_weight']/@value").strip()

						# booking_url = doc.q("//table[@class='Grid']//tr/td/a")[-1].x('@href')

						contents = doc.q("//tr[@class='Caption2']/td[@align='center']")
						contents = ''.join([item.html() for item in contents])
						# logger.info('Contents -> %s' %contents)
						
						# contents = str(contents).replace('\\r', '').replace('\\n', '').replace('\\t', '')
						# print ('------Contents--------',contents)
						try:
							ArrestDateStr=re.search('Arrest Date: (\<strong\>)?([^\<.*]*)\<[\/]?strong[\/]?\>', contents, re.M|re.I|re.S).group(2).strip()
							ArrestDateStr = ArrestDateStr.split('/')
							y = ArrestDateStr.pop()
							d = ArrestDateStr.pop()
							m = ArrestDateStr.pop()
							ArrestDate = y+"-"+m+"-"+d
							ArrestTimeStr=re.search('Arrest Time: (\<strong\>)?([^\<.*]*)\<[\/]?strong[\/]?\>', str(contents), re.M|re.I|re.S).group(2).strip()
							ArrestTime = ArrestTimeStr[:2]+":"+ArrestTimeStr[2:]
							CapturedDate=currentdate
							CapturedTime=currenttime
							ArrestAgency=re.search('Arrest Agency: (\<strong\>)?([^\<.*]*)\<[\/]?strong[\/]?\>', str(contents), re.M|re.I|re.S).group(2).strip()
							AgencyDescription=re.search('Agency Description: (\<strong\>)?([^\<.*]*)\<[\/]?strong[\/]?\>', str(contents), re.M|re.I|re.S).group(2).strip()
							DateBooked=re.search('Date Booked: (\<strong\>)?([^\<.*]*)\<[\/]?strong[\/]?\>', str(contents), re.M|re.I|re.S).group(2).strip()
							TimeBooked=re.search('Time Booked: (\<strong\>)?([^\<.*]*)\<[\/]?strong[\/]?\>', str(contents), re.M|re.I|re.S).group(2).strip()
							# DateBooked=currentdate
							# TimeBooked=currenttime
							BookingLocation=re.search('Booking Location: (\<strong\>)?([^\<.*]*)\<[\/]?strong[\/]?\>', str(contents), re.M|re.I|re.S).group(2).strip()
							LocationDescription=re.search('Location Description: (\<strong\>)?([^\<.*]*)\<[\/]?strong[\/]?\>', str(contents), re.M|re.I|re.S).group(2).strip()
							TotalBailAmount=re.search('Total Bail Amount: (\<strong\>)?([.\,\w\s]*)\<[\/]?strong[\/]?\>', str(contents), re.M|re.I|re.S).group(2).strip()
							TotalHoldBailAmount=re.search('Total Hold Bail Amount: (\<strong\>)?([.\,\w\s]*)\<[\/]?strong[\/]?\>', str(contents), re.M|re.I|re.S).group(2).strip()
							GrandTotal=re.search('Grand Total: (\<strong\>)?([.\,\w\s]*)\<[\/]?strong[\/]?\>', str(contents), re.M|re.I|re.S).group(2).strip()
							HousingLocation=re.search('Housing Location: (\<strong\>)?([^\<.*]*)\<[\/]?strong[\/]?\>', str(contents), re.M|re.I|re.S).group(2).strip()
							PermanentHousingAssignedDate=re.search('Permanent Housing Assigned Date: (\<strong\>)?([^\<.*]*)\<[\/]?strong[\/]?\>', str(contents), re.M|re.I|re.S).group(2).strip()
							AssignedTime=re.search('Assigned Time: (\<strong\>)?([^\<.*]*)\<[\/]?strong[\/]?\>', str(contents), re.M|re.I|re.S).group(2).strip()
							# PermanentHousingAssignedDate=currentdate
							# AssignedTime=currenttime
							
							VisitorStatus=re.search('Visitor Status: (\<strong\>)?([^\<.*]*)\<[\/]?strong[\/]?\>', str(contents), re.M|re.I|re.S).group(2).strip()
							Facility=re.search('Facility: (\<strong\>)?([^\<.*]*)\<[\/]?strong[\/]?\>', str(contents), re.M|re.I|re.S).group(2).strip()
							Address=re.search('Address: (\<strong\>)?([^\<.*]*)\<[\/]?strong[\/]?\>', str(contents), re.M|re.I|re.S).group(2).strip()
							City=re.search('City: (\<strong\>)?([^\<.*]*)\<[\/]?strong[\/]?\>', str(contents), re.M|re.I|re.S).group(2).strip()

							logger.info('BookingNo -> %s' %BookingNo)
							logger.info('LastName -> %s' %LastName)
							logger.info('FirstName -> %s' %FirstName)
							logger.info('MiddleName -> %s' %MiddleName)
							logger.info('Birthday -> %s' %Birthday)
							logger.info('Age -> %s' %Age)
							logger.info('Sex -> %s' %Sex)
							logger.info('Race -> %s' %Race)
							logger.info('Hair -> %s' %Hair)
							logger.info('Eyes -> %s' %Eyes)
							logger.info('Height -> %s' %Height)
							logger.info('Weight -> %s' %Weight)
							logger.info('ArrestDate -> %s' %ArrestDate)
							logger.info('ArrestTime -> %s' %ArrestTime)
							logger.info('CapturedDate -> %s' %CapturedDate)
							logger.info('CapturedTime -> %s' %CapturedTime)
							logger.info('ArrestAgency -> %s' %ArrestAgency)
							logger.info('AgencyDescription -> %s' %AgencyDescription)
							logger.info('DateBooked -> %s' %DateBooked)
							logger.info('TimeBooked -> %s' %TimeBooked)
							logger.info('BookingLocation -> %s' %BookingLocation)
							logger.info('LocationDescription -> %s' %LocationDescription)
							logger.info('TotalBailAmount -> %s' %TotalBailAmount)
							logger.info('TotalHoldBailAmount -> %s' %TotalHoldBailAmount)
							logger.info('GrandTotal -> %s' %GrandTotal)
							logger.info('HousingLocation -> %s' %HousingLocation)
							logger.info('PermanentHousingAssignedDate -> %s' %PermanentHousingAssignedDate)
							logger.info('AssignedTime -> %s' %AssignedTime)
							logger.info('VisitorStatus -> %s' %VisitorStatus)
							logger.info('Facility -> %s' %Facility)
							logger.info('Address -> %s' %Address)
							logger.info('City -> %s' %City)

							# con = mdb.connect('localhost', 'root', 'root', 'lasd');
							# con = mdb.connect('localhost', 'root', 'dnflgmlakd888', 'lasd')
							con = mdb.connect('localhost', 'root', 'developsmith', 'lasd')
							with con:
								cur = con.cursor()
								sql = "SELECT * FROM dashboard_lasd WHERE BookingNo='"+BookingNo+"'"
								print ("----sql---",sql)
								cur.execute(sql)
								result = cur.fetchall()
								print ("----result---",result)
								if (len(result) > 0):
									print ("-------Update------")
									cur.execute("UPDATE dashboard_lasd set LastName='"+LastName+"',FirstName='"+FirstName+"',MiddleName='"+MiddleName+"',Birthday='"+Birthday+"',Age='"+Age+"',Sex='"+Sex+"',Race='"+Race+"',Hair='"+Hair+"',Eyes='"+Eyes+"',Height='"+Height+"',Weight='"+Weight+"',ArrestDate='"+ArrestDate+"',ArrestTime='"+ArrestTime+"',CapturedDate='"+CapturedDate+"',CapturedTime='"+CapturedTime+"',ArrestAgency='"+ArrestAgency+"',AgencyDescription='"+AgencyDescription+"',DateBooked='"+DateBooked+"',TimeBooked='"+TimeBooked+"',BookingLocation='"+BookingLocation+"',LocationDescription='"+LocationDescription+"',TotalBailAmount='"+TotalBailAmount+"',TotalHoldBailAmount='"+TotalHoldBailAmount+"',GrandTotal='"+GrandTotal+"',HousingLocation='"+HousingLocation+"',PermanentHousingAssignedDate='"+PermanentHousingAssignedDate+"',AssignedTime='"+AssignedTime+"',VisitorStatus='"+VisitorStatus+"',Facility='"+Facility+"',Address='"+Address+"',City='"+City+"' where BookingNo='"+BookingNo+"'")
								else: 
									print ("-------Insert------")
									cur.execute("INSERT INTO dashboard_lasd(BookingNo, LastName, FirstName, MiddleName, Birthday, Age, Sex, Race, Hair, Eyes, Height, Weight, ArrestDate, ArrestTime, CapturedDate, CapturedTime, ArrestAgency, AgencyDescription, DateBooked, TimeBooked, BookingLocation, LocationDescription, TotalBailAmount, TotalHoldBailAmount, GrandTotal, HousingLocation, PermanentHousingAssignedDate, AssignedTime, VisitorStatus, Facility, Address, City) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % 
										(
											BookingNo, LastName, FirstName, MiddleName, Birthday, Age, Sex, Race, Hair, Eyes, Height, Weight, ArrestDate, ArrestTime, CapturedDate, CapturedTime, ArrestAgency, AgencyDescription, DateBooked, TimeBooked, BookingLocation, LocationDescription, TotalBailAmount, TotalHoldBailAmount, GrandTotal, HousingLocation, PermanentHousingAssignedDate, AssignedTime, VisitorStatus, Facility, Address, City
									))
						except:
							pass

				if (iindex == (len(last_name_list)-1)):
					iindex = 0
				if (jindex == (len(first_name_list)-1)):
					jindex = 0

				logger.info('lastnameindex: %s' %iindex)
				logger.info('firstnameindex: %s' %jindex)


				print ("----------------------RESTART-----------------------------")





