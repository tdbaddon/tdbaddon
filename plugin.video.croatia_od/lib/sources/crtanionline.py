from lib.modules import client
import re,os
from lib.modules.webutils import bs



class crtani():
	def __init__(self,url):
		self.base = 'http://crtanionline.net/'
		self.url = url
		self.html = client.request(self.url, referer=self.base)
		import HTMLParser
		self.html = HTMLParser.HTMLParser().unescape(self.html.decode('utf-8'))

	def get_movie_list(self):
		reg=re.compile('<a href="([^"]+)">\s*<img src="(.+?)" alt=".+?" title="(.+?)">')
		movies = re.findall(reg,self.html)
		movies = list(set(movies))
		return movies

	def next_page(self):
		try: next_page = re.compile('<a\s*class="nextpostslink"\s*rel="next"\s*href="(.+?)">').findall(self.html)[0]
		except: return
		return next_page


	def get_links(self):
		soup = bs(self.html)
		player = soup.find('div',{'id':'player'})
		try:
			url = player.find('iframe')['src']
			if 'http' not in url: url = 'http:' + url
			return url,None
		except:
			url = re.compile('proxy.link=(.+?)\s*&').findall(self.html)[0]
			try:	subtitle = re.compile('captions.file=(.+?)\s*&').findall(self.html)[0]
			except: 
				try: subtitle = re.compile('(http://.+?.(?:srt|sub))').findall(self.html)[0]
				except:
					subtitle = None

			return url, subtitle



	@staticmethod
	def get_categories():
		cats = [('http://crtanionline.net/crtanifilmovi/dugometrazni-crtani/', 'Dugometra\xc5\xbeni crtani '), ('http://crtanionline.net/crtanifilmovi/kratkometrazni-crtani/', 'Kratkometra\xc5\xbeni crtani '), ('http://crtanionline.net/crtanifilmovi/crtani-sa-prijevodom/', 'Crtani sa prijevodom '), ('http://crtanionline.net/crtanifilmovi/sinkronizirani-crtici/', 'Sinkronizirani crti\xc4\x87i '), ('http://crtanionline.net/crtanifilmovi/crtani-najmladje/', 'Crtani za najmla\xc4\x91e ')]

		return cats
