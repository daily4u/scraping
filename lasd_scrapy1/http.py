import sys, os, urlparse, time, zlib, json, re, codecs, logging, urllib2, urllib, httplib, contextlib, cookielib, random, socket, ssl, base64

from cStringIO import StringIO
from gzip import GzipFile

from scrapex import common, agent
from scrapex.node import Node

try:
	_create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
	# Legacy Python that doesn't verify HTTPS certificates by default
	pass
else:
	# Handle target environment that doesn't support HTTPS verification
	ssl._create_default_https_context = _create_unverified_https_context

meta_seperator = '=======META======'
class Proxy(object):
	def __init__(self, host, port, proxy_auth = None):
		self.host = host
		self.port = int(port)
		self.proxy_auth = proxy_auth
		
		self.auth_header = 'Basic ' + base64.b64encode(self.proxy_auth) if self.proxy_auth else None

		self.full_address = ( '%s@%s:%s' % (self.proxy_auth, self.host, self.port) ) if self.proxy_auth else ('%s:%s' % (self.host, self.port))


class ProxyManager(object):
	
	""" for proxy rotation controlling """

	def __init__(self, proxy_file, proxy_auth='', one_proxy=False):		
		self.proxy_file = proxy_file
		self.proxy_auth = proxy_auth
		self.proxies = []

		if ( one_proxy is True ):
			self.load_oneproxy()
		else:
			self.load_proxies()


	def load_oneproxy(self):		
		proxy_file = self.proxy_file

		if proxy_file:
			if not os.path.exists(proxy_file):
				raise Exception('proxy_file not found: {0}'.format(proxy_file))
			
			proxy_auth_found = False
			proxy_selected = False

			lines = common.read_lines(proxy_file)
			while ( True ):
				line = random.choice( lines )
				if 'proxy_auth' in line:
					if ( proxy_auth_found is False):
						self.proxy_auth = common.DataItem(line).rr('proxy_auth\s*=\s*').trim()
						proxy_auth_found = True
				else:
					if ( proxy_selected is False ):
						#support tab, commas separator as well
						line = line.replace('\t',':').replace(',',':')	
						self.proxies.append(line)
						proxy_selected = True

				if ( proxy_selected ):
					if ( proxy_auth_found ):
						break
					else:
						for line in lines:
							if 'proxy_auth' in line:
								self.proxy_auth = common.DataItem(line).rr('proxy_auth\s*=\s*').trim()
								proxy_auth_found = True
								break
						if ( proxy_auth_found ):
							break
		return self	

	def load_proxies(self):		
		proxy_file = self.proxy_file

		if proxy_file:
			if not os.path.exists(proxy_file):
				raise Exception('proxy_file not found: {0}'.format(proxy_file))
			

			for line in common.read_lines(proxy_file):
				if 'proxy_auth' in line:
					self.proxy_auth = common.DataItem(line).rr('proxy_auth\s*=\s*').trim()
					continue

				#support tab, commas separator as well
				line = line.replace('\t',':').replace(',',':')	
				self.proxies.append(line)		


		return self	

	def random_proxy(self):
		if not self.proxies:
			return None

		proxy = random.choice( self.proxies )	
		if self.proxy_auth and len(proxy.split(':')) == 2:
			return Proxy(host=proxy.split(':')[0], port=proxy.split(':')[1], proxy_auth=self.proxy_auth)
			
		#support proxy in ip:port:user:pass
		if len(proxy.split(':')) == 4:
			proxy = proxy.split(':')
			return Proxy(host=proxy[0], port=proxy[1], proxy_auth='%s:%s' % (proxy[2], proxy[3]))
			
			
		return None

	def get_proxy(self, url=None):

		return self.random_proxy()
		


class Status():
	""" Represents a http request response status """

	def __init__(self, code=0, final_url='', error=''):
		self.code = code
		self.final_url = final_url
		self.error = error

	def __str__(self):

		return str("code: %s, error: %s, final_url: %s" % (self.code, self.error, self.final_url) )

class Request(object):	
	""" Represents a http request """

	def __init__(self, url, post = None, **options):		
		#to avoid using invalid option names
		logger = logging.getLogger('__name__')
		allowed_option_names = 'one_proxy, log_file, use_logging_config, debug, max_redirects, accept_error_codes, return_type, cb, meta, log_time_and_proxy, proxy_url_filter, cache_only, merge_headers,cc, ref, ajax, cache_path, show_status_message, use_logging_config, debug, preserve_log, use_cache,use_cookie, use_requests, use_proxy, user_agent, proxy_file, proxy_auth, timeout, delay, retries, bin, headers, file_name, contain, dir, parse_log, html_clean, encoding'.replace(' ','').split(',')

		for o in options.keys():
			if o not in allowed_option_names:
				if not options.get('disable_option_name_warning'):
					logger.warn('invalid option name: %s', o)



		self.url = url.replace(' ', '%20')
		self.post = post
		self.options = options
		
		#update headers
		if 'headers' not in self.options:
			self.options['headers'] = {}

		if 'ref' in self.options:
			self.options['headers']['Referer'] = self.options['ref']
		if self.options.get('ajax') is True:
			self.options['headers']['X-Requested-With'] = 'XMLHttpRequest'

		self.is_normalized = False	
	
	def __getitem__(self, key):
		return self.get(key)

	def get(self, name, default = None):
		return self.options.get(name, default)
	def set(self, name, value):
		self.options[name]= value
		return self

	def update(self, dict2):
		self.options.update(dict2)
		return self

	def normalize(self, scraper):
		""" normalize this req with using the provided scraper's config """
		if self.is_normalized:
			return self

		#copy scraper-wide options if not set yet	
		self.options = common.combine_dicts(scraper.config, self.options)

		req = self

		self.url = common.normalize_url(self.url)
		# self.url = str(self.url)

		accept_error_codes = req.get('accept_error_codes')
		if accept_error_codes is None:
			accept_error_codes = []
			req.set('accept_error_codes', accept_error_codes)

		#default headers
		user_agent = req.get('user_agent', agent.firefox ) #default agent is firefox
		
		if user_agent == 'random':
			user_agent = agent.random_agent()

		headers = {
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
			"User-Agent": user_agent,
			"Accept-Language": "en-us,en;q=0.5",
			"Accept-Encoding": "gzip, deflate",			
			# "Connection": "close" #turn off keep-alive
			"Connection": "keep-alive"
		}

		if req.post:
			headers.update({"Content-Type": "application/x-www-form-urlencoded"})
			
		#update user-passed in headers
		if req.get('headers'):
			if req.get('merge_headers') is not False:
				#merge user defined headers with default headers
				headers.update(req.get('headers')) 
			else:
				#only use user defined headers
				headers = req.get('headers')	


		req.set('headers', headers)
			
		proxy = req.get('proxy') or scraper.proxy_manager.get_proxy(req.url)
		if proxy and req.get('proxy_url_filter'):
			#check if this url is qualified for using proxy
			if not re.compile(req.get('proxy_url_filter')).findall(req.url):
				#failed
				proxy = ''
				logger.debug('proxy not used for url: %s', req.url)

		req.set('proxy', proxy)
		
		
		#normalise the post
		if req.post and isinstance(req.post, common.MyDict):
			req.post = req.post.dict()
		if req.post and isinstance(req.post, dict):
			req.post = urllib.urlencode(sorted(req.post.items()))

		self.is_normalized = True	
		
		return self	

class Response(object):
	""" a wrapper for http response """
	def __init__(self, data, status):
		self.data = data
		self.status = status


class Doc(Node):
	def __init__(self, url='', html='<html></html>', html_clean=None, status=None):
		logger = logging.getLogger('__name__')		
		if html_clean:
			html = html_clean(html)

		Node.__init__(self, html)
		self.url = common.DataItem( url )
		self.status = status or Status(final_url=url)
		

		
		
		#resolve relative urls
		baseurl = self.x("//base/@href").tostring()
		if not baseurl:
			baseurl = self.url
		try:
			for n in self.q('//a[@href and not(contains(@href, "javascript")) and not(starts-with(@href, "#")) and not(contains(@href, "mailto:"))]'):					
				if n.href().trim() == '': continue
				n.set('href', urlparse.urljoin(baseurl, n.get('href').tostring()))

			for n in self.q('//iframe[@src]'):					
				if n.src().trim() == '': continue
				n.set('src', urlparse.urljoin(baseurl, n.src()))
		


			for n in self.q('//form[@action]'):					
				n.set('action', urlparse.urljoin(baseurl, n.get('action').tostring()))	
			for n in self.q('//img[@src]'):					
				n.set('src', urlparse.urljoin(baseurl, n.get('src').tostring()))
		except Exception as e:
			logger.warn('there was error while init the Doc object: %s', self.url)
			logger.exception(e)
							
	def form_data(self, xpath=None):
		data = dict()
		for node in self.q(xpath or "//input[@name and @value]"):
			data.update(dict( ( (node.name(), node.value(),), ) ))

		return data	
	def aspx_vs(self):
		return self.x("//input[@id='__VIEWSTATE']/@value").urlencode() or self.html().sub('__VIEWSTATE|','|').urlencode()
	def aspx_ev(self):
		return self.x("//input[@id='__EVENTVALIDATION']/@value").urlencode() or self.html().sub('__EVENTVALIDATION|','|').urlencode()
	def aspx_prepage(self):
		return self.x("//input[@id='__PREVIOUSPAGE']/@value").urlencode() or self.html().sub('__PREVIOUSPAGE|','|').urlencode()	


def create_opener(use_cookie=True, cj=None):
	if use_cookie:
		cj = cj or cookielib.CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor( cj ))
		opener.cj = cj
		return opener
	else:
		return urllib2.build_opener()	

class Client(object):

	def __init__(self, scraper):

		self.scraper = scraper
		
		socket.setdefaulttimeout(self.scraper.config.get('timeout', 45) )

		self.logger = logging.getLogger(__name__)
		
		self.opener = create_opener(use_cookie=True)

		self.resp = None

		

		if scraper.config.get('use_requests') is True:
			import requests
			# print 'create new requests Session'
			self.requests_client = requests.Session()


	def load(self, req):
		""" returns a DOM Document"""
		html = self.load_html(req)
		doc = Doc(html=html, url = req.url, status= html.status)

		return doc

	def load_html(self, req):
		""" returns a unicode html object """
		cache = self.scraper.cache
		accept_error_codes = req.get('accept_error_codes')
		if accept_error_codes is None:
			accept_error_codes = []


		if cache and cache.exists(url = req.url, post=req.post, file_name=req.get('file_name')) and req.get('use_cache'):
			return self._read_from_cache(url=req.url, post=req.post, file_name=req.get('file_name'))

		if req.get('use_cache') and req.get('cache_only') and not cache.exists(url = req.url, post=req.post, file_name=req.get('file_name')):
			html = common.DataItem('<html/>')
			html.status = Status()
			return html 	
			
		res = self.fetch_data(req)

		html = common.DataItem( res.data or '')
		status = res.status

		if (status.code == 200 or status.code in accept_error_codes) and  cache and req.get('use_cache'):
			self._write_to_cache(url=req.url, post=req.post, data=html, status=status, file_name=req.get('file_name'))

		html.status = status

		return html	

		
	def load_json(self, req):
		""" returns a json object """
		data = self.load_html(req)
		try:
			return json.loads(data)

		except:
			self.logger.exception('json decode error for url: %s --  post: %s', req.url, req.post or '')
			return None	
		
	
	def fetch_data(self, req):
		""" processes a http request specified by the req object and returns a response object """
		req.normalize(self.scraper)

		accept_error_codes = req.get('accept_error_codes')

		
		time.sleep(self.scraper.config['delay'])
		opener = req.get('opener')
		if not opener:
			opener = create_opener(use_cookie=False) if req.get('use_cookie') is False else  self.opener


		headers = req.get('headers')
		
		if self.scraper.config.get('use_requests') is True:
			#use requests module instead of urllib2
			return self.requests_fetch_data(req,headers)

		proxy = req.get('proxy')
		
		if proxy and req.get('use_proxy') is not False:
			if req.url.lower().startswith('https://'):
				opener.add_handler(urllib2.ProxyHandler({'https' : proxy.full_address }))
			else:
				opener.add_handler(urllib2.ProxyHandler({'http' : proxy.full_address }))
		

		request = urllib2.Request(req.url, req.post, headers)
			
		tries = req.get('retries', 0)	
		
		status_code = 0
		error_message = ''
		final_url = None	

		if self.scraper.config['debug']:		
			self.logger.debug('loading %s', req.url)

		try:
			
			with contextlib.closing(opener.open(request,  timeout= req.get('timeout', self.scraper.config['timeout']))) as res:
				final_url = res.url
				status_code = res.code


				rawdata = res.read()

				self.resp = res
				
				if 'gzip' in res.headers.get('content-encoding','').lower():
					bytes = zlib.decompress(rawdata, 16+zlib.MAX_WBITS)
				elif 'deflate' in res.headers.get('content-encoding','').lower():	
					bytes = zlib.decompressobj(-zlib.MAX_WBITS).decompress(rawdata)	
				else:
					bytes = rawdata

				encoding = req.get('encoding') or  common.DataItem(res.headers.get('content-type') or '').subreg('charset\s*=([^;]+)')	or 'utf8'
				content_type = res.headers.get('content-type', '').lower()

				#self.logger.debug('content type: %s, encoding: %s', content_type, encoding)
				
				data = ''

				#default is text data
				
				is_binary_data = req.get('bin') or False
				if 'image' in content_type or 'pdf' in content_type:
					is_binary_data = True

				if  not is_binary_data:
					
					data = bytes.decode(encoding, 'ignore')

					#verify data
					#self.logger.debug('contain: %s', req.get('contain'))
					if req.get('contain') and req.get('contain') not in data:
						raise Exception("invalid html, not contain: %s" % req.get('contain'))

					if req.get('not_contain') and req.get('not_contain') in data:
						raise Exception("invalid html, contain negative string: %s" % req.get('not_contain'))
						
					verify = req.get('verify')
					
					if verify and (not verify(data)):
						raise Exception("invalid html")
				else:
					
					#binary content
					data = bytes		

				
				#log proxy and timestamp into the html file if asked
				if req.get('log_time_and_proxy'):
					
					data += '\n<log id="time_proxy"><time>{time}</time><proxy>{proxy}</proxy></log>'.format(time=time.time(), proxy=proxy if (proxy and req.get('use_proxy') is not False) else '')
	

				return Response(data=data, status= Status(code=status_code, final_url=final_url))	

		
		except Exception, e:
			if status_code == 0 and hasattr(e,'code'):
				status_code = e.code
			if hasattr(e, 'reason'):
				error_message = e.reason			

			elif hasattr(e, 'line'):
				error_message = 'BadStatusLine: %s' % e.line

			elif hasattr(e, 'message'):	
				error_message =  e.message

			

			if not error_message and hasattr(e, 'args'):
				try:				
					error_message = u", ".join([unicode(item) for item in e.args]).replace("''",'unknown')	
				except:
					pass
			
			if tries > 0 and status_code not in accept_error_codes:
				#try to open the request one again	
				self.logger.debug('data fetching error: %s %s', status_code if status_code !=0 else '', error_message)
				req.update({'retries': tries - 1})
				return self.fetch_data(req)
			else:
				self.logger.warn('data fetching error: %s %s', status_code if status_code !=0 else '', error_message)	
				if 'invalid html' in error_message:
					status_code = 0
				return Response(data=None, status = Status(code = status_code, final_url=final_url, error = error_message))


	def requests_fetch_data(self, req, headers):
		logger = logging.getLogger(__name__)
		
		proxy = req.get('proxy')

		proxies = None
		if proxy and req.get('use_proxy') is not False:
				
			proxies = {
						'http': 'http://{0}'.format(proxy.full_address),
						'https': 'http://{0}'.format(proxy.full_address)
					}
		if self.scraper.config['debug']:			
			logger.debug('loading %s', req.url)

		accept_error_codes = req.get('accept_error_codes')
		
		client = self.requests_client

		status_code = 0
		error_message = ''
		final_url = None	

		tries = req.get('retries', 0)	

		try:
			time.sleep(req.get('delay', 0.001))	
			r = None	
			if req.post:
				r = client.post(req.url, data = req.post, headers = headers, timeout = req.get('timeout'), proxies = proxies, verify = False, stream=True)
			else:	
				r = client.get(req.url, headers = headers, timeout = req.get('timeout'), proxies = proxies, verify = False, stream = True)
			
		
			status_code = r.status_code
			final_url = r.url
			if status_code != 200:
				if status_code not in accept_error_codes:
					raise Exception('Invalid status code: %s' % r.status_code)
			
			rawdata = r.raw.read()

			
			if 'gzip' in r.headers.get('content-encoding', ''):
				
				bytes = zlib.decompress(rawdata, 16+zlib.MAX_WBITS)
				
			elif 'deflate' in r.headers.get('content-encoding', ''):

				bytes = zlib.decompressobj(-zlib.MAX_WBITS).decompress(rawdata)	
			
			else:
				bytes = rawdata

			is_binary_data = req.get('bin') or False
			
			if is_binary_data:
				return Response(data=bytes, status= Status(code=status_code, final_url=final_url))


			html = bytes.decode(req.get('encoding', r.encoding or 'utf8'), 'ignore')

			#verify data
			if req.get('contain') and req.get('contain') not in html:
				raise Exception("invalid html, not contain: {0}".format(req.get('contain')))
			verify = req.get('verify')
			
			if verify and (not verify(html)):
				raise Exception("invalid html")

			#log proxy and timestamp into the html file if asked
			if req.get('log_time_and_proxy'):
				html += u'\n<log id="time_proxy"><time>{time}</time><proxy>{proxy}</proxy></log>'.format(time=time.time(), proxy=proxy if proxies else '')

			return Response(data=html, status= Status(code=status_code, final_url=final_url))	
			
				

		except Exception, e:			
			error_message = e.message
			
			if tries > 0 and status_code not in accept_error_codes:
				#try to open the request one again	
				logger.debug('data fetching error: %s %s', status_code if status_code !=0 else '', error_message)
				req.update({'retries': tries - 1})
				return self.requests_fetch_data(req, headers)
			else:
				logger.warn('data fetching error: %s %s', status_code if status_code !=0 else '', error_message)	
				if 'invalid html' in error_message:
					status_code = 0
				return Response(data=None, status = Status(code = status_code, final_url=final_url, error = error_message))

		

	def _read_from_cache(self, url, post, file_name=None):
		cache = self.scraper.cache

		cachedata = cache.read(url = url, post = post, file_name = file_name).split(meta_seperator)
		
		cachedhtml = None
		status = Status(code=200, final_url=None, error=None)
		if len(cachedata)==2:
			cachedhtml = cachedata[1]
			meta = json.loads( cachedata[0] )
			#reload status
			status = Status(code= meta['status']['code'], final_url = meta['status']['final_url'], error = meta['status'].get('error', '') )
		else:
			#no meta data
			cachedhtml = cachedata[0]
		html = common.DataItem(cachedhtml)	
		html.status = status

		return html

	def _write_to_cache(self, url, post, data, status, file_name=None):
		meta = {
				'url': url,
				'status': {
					'code': status.code,
					'final_url': status.final_url,
					'error': status.error
				}
			}
		
		self.scraper.cache.write(url=url, post=post, file_name=file_name, data=u''.join([json.dumps(meta), meta_seperator, data]) )	
	

		

if __name__ == '__main__':
	import core
	s = core.Scraper(use_cache=False)
	
	doc = s.load('https://librivox.org/what-i-believe-by-leo-tolstoy/')
	print doc.x("//title")
