from __future__ import unicode_literals
from resources.lib.modules import client, convert, webutils
import re,sys
from addon.common.addon import Addon
addon = Addon('plugin.video.castaway', sys.argv)

class info():
    def __init__(self):
    	self.mode = 'footballtarget'
        self.name = 'footballtarget'
        self.icon = 'footballtarget.png'
        self.categorized = False
        self.paginated = False
        self.multilink = False

class main():
	def __init__(self):
		self.base = 'http://www.footballtarget.com/football-news/'

	def articles(self):
		html = client.request(self.base, referer=self.base)
		html = convert.unescape(html.decode('utf-8'))
		items = re.findall('div class="widget-cat-img">\s*<a href="(.+?)" rel="bookmark" title="(.+?)"><img.+?lazy-src="(.+?)"', html)
		items = self.__prepare_articles(items)
		return items

	def content(self,url):
		html = client.request(url)
		html = convert.unescape(html.decode('utf-8'))
		text = webutils.bs(html).find('div',{'class':'entry-content'}).getText().encode('utf-8', 'xmlcharrefreplace')

		try:
			video = webutils.bs(html).find('div',{'class':'entry-content'}).find('iframe')['src']
			video = self.resolve(video)
		except:
			video = None

		return text,video

	def __prepare_articles(self,items):
		new = []
		for item in items:
			url = item[0]
			title = item[1].encode('utf-8', 'xmlcharrefreplace')
			img = item[2]
			new.append((url,title, img))
		return new

	def resolver(self,video):
		import urlresolver
		return urlresolver.resolve(video)