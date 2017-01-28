from resources.lib.modules import client,webutils,control,convert,cache
from resources.lib.modules.log_utils import log
import sys,os,re,requests,pickle
AddonPath = control.addonPath
IconPath = AddonPath + "/resources/media/"
def icon_path(filename):
    return os.path.join(IconPath, filename)

USER_AGENT = 'Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
COOKIE = os.path.join(control.dataPath,'loginSultanCookie')
HEADERS = {'User-agent':USER_AGENT}
lista = os.path.join(control.dataPath,'liste.cl')
lista3 = os.path.join(control.dataPath,'moja.m3u')

class info():
    def __init__(self):
    	self.mode = 'sultanovic'
        self.name = 'sultanovic.net'
        self.icon = 'sultan.png'
        self.paginated = False
        self.categorized = True
        self.multilink = False
        self.special=True



class main():
	def __init__(self):
		self.base = 'http://www.sultanovic.net/forum/12-1580-1'
		self.lll = ''
		self.config = {
			'email' : control.setting('sultan_user'),
			'password' : control.setting('sultan_pass')
			}

	def categories(self):
		out = []
		html = client.request(self.base)
		last_page = int(re.findall('class=[\"\']switchDigit[\"\'] href=[\"\']([^\"\']+)',html)[-1].split('-')[-1])
		img = control.icon_path(info().icon)
		for i in range(last_page,last_page-21,-1):
			url = 'http://www.sultanovic.net/forum/12-1580-' + str(i)
			title = 'Stranica %s'%i
			out.append((url,title,img))
		return out

	def channels(self,url):
		if self.config['email'] != '':
			html = self.login_get_html(url)
		else:
			html = client.request(url)


		urls = []
		links = []
		spoilers = client.parseDOM(html,'div',attrs={'class':'uSpoilerText'})
		for s in spoilers:
			s = self.remove_tags(s)
			if '#ext' in s.lower():
				self.parse_m3u(s)
			else:
				s = s.replace('http:',' http:')
				lines = s.split()
				for l in lines:
					l = l.lstrip()
					if l.startswith('http'):
						if 'get.php' in l or 'm3u' in l and 'm3u8' not in l:
							try:
								if requests.get(l).status_code == 200:
									l = l.replace('m3u_plus','m3u')
									content = cache.get(client.request,10000,u)
									self.parse_m3u(content)
							except:
								pass
		

		out = []
		from resources.lib.modules import m3u_parser
		self.lll = '#EXTM3U\n' + self.lll
		links =  m3u_parser.parseM3U(self.lll.encode('utf-8'))
		for l in links:
			out.append((l.path,l.title,control.icon_path(info().icon)))
		return out				

		
		

	def login_get_html(self,url):
		s = self.start_session()
		html = s.get(url).text
		return html

	def parse_m3u(self,content):
		content = convert.unescape(content)
		content = re.sub('(^.+?)#EXTINF','#EXTINF',content,flags=re.DOTALL)
		self.lll = content + '\n' + self.lll
	
	
	def login(self):
		post_url = 'http://login.uid.me/dolog/'
		post_data = {'email':self.config['email'],'pass':self.config['password'],'ajax':'1','goto':'url','url':'http://login.uid.me/?site=6sultanovici&ref=http://www.sultanovic.net','secmode':'1','_tp_':'xml','Accept':'application/xml, text/xml, */*; q=0.01'}
		headers = {'User-agent':USER_AGENT,'X-Requested-With':'XMLHttpRequest', 'Origin':'http://login.uid.me', 'Host':'login.uid.me','Referer':'http://login.uid.me/?site=6sultanovici&ref=http://www.sultanovic.net'}
		s = requests.session()
		
		s.post(post_url, data=post_data,headers=headers)
		s.headers.update(HEADERS)
		a = s.get('http://login.uid.me/?site=6sultanovici&ref=http%3A%2F%2Fwww.sultanovic.net')
		with open(COOKIE, 'wb') as f:
			pickle.dump(s.cookies, f)

	def start_session(self):
		session = requests.Session()
		cookies = self.load_cookies()
		if not cookies:
			self.login()
			cookies = self.load_cookies()
		session.cookies = cookies
		r = session.get('http://www.sultanovic.net/forum/12-1580-1')
		logged_in = b'Prijavljeni ste kao' in r.content
		if not logged_in:
			self.login()
			cookies = self.load_cookies()
		session.cookies = cookies
		return session

	def load_cookies(self):
		try:
			with open(COOKIE,'rb') as f:
				cookies = pickle.load(f)
				return cookies
		except:
			return False

	def remove_tags(self,text):
		text = re.sub('<\s*br>','\n',text)
		text = re.sub('<\s*br\s*/\s*>','\n',text)
		TAG_RE = re.compile(r'<[^>]+>')
		return TAG_RE.sub('', text)


	def resolve(self,url,title='Video',icon='x'):
		if url.endswith('.ts'):
			import liveresolver
			return liveresolver.resolve(url,title=title,icon=icon)
		return url
