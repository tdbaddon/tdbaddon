# -*- coding: utf-8 -*-
from resources.lib.modules import client,epg,convert,control
import re
from resources.lib.modules.log_utils import log
import sys,xbmcgui,os


class info():
    def __init__(self):
    	self.mode = 'extra'
        self.name = 'Extra'
        self.icon = 'TV.png'
        self.paginated = False
        self.categorized = True
        self.multilink = False
        
class main():
	def __init__(self,url = 'https://raw.githubusercontent.com/natko1412/cod/master/extra/'):
		self.base = 'https://raw.githubusercontent.com/natko1412/cod/master/extra/'
		self.url = url

	def categories(self):
		exec(client.request('https://raw.githubusercontent.com/natko1412/cod/master/extra/extra_categories').strip())
		return cats

	def channels(self,url):
		html = client.request(self.base + url)
		urls = re.findall('url\s*=\s*"(.+?)"',html)
		imgs = re.findall('img\s*=\s*"(.+?)"',html)
		titles = re.findall('ime\s*=\s*"(.+?)"',html,flags=re.UNICODE)
		events = self.__prepare_channels(urls,titles,imgs)

		if url=='euro.txt':
			html = client.request('http://wizhdsports.sx')
			urls = []
			ev2 = re.findall('href="(http://wizhdsports.sx/watch/Uefa-Euro-2016[^\"\']+)">Stream\s*\d+\s*\(([^\)]+)',html)
			ev2.sort(key=lambda x: x[1])
			for e in ev2:
				if e[1] not in urls:
					events.append((e[0],e[1],'https://pbs.twimg.com/profile_images/715249225508982785/kFUoDevy.jpg'))
					urls.append(e[1])

		return events

	def __prepare_channels(self,urls,titles,imgs):
		new=[]
		for i in range(len(urls)):
			url = urls[i]
			img = imgs[i]
			title = titles[i].decode('utf-8')
			new.append((url,title.encode('utf-8'),img))
		return new

	
	def resolve(self,url):
		ods = eval(client.request('https://raw.githubusercontent.com/natko1412/cod/master/extra/on_demands'))
		exts = ['.mp4','.mkv','.flv','.avi','plugin://']
		if any(word in url for word in ods):
			import urlresolver
			return urlresolver.resolve(url)
		elif 'playwire' in url:
			from resources.lib.resolvers import playwire
			return playwire.resolve(url)

		elif any(ext in url for ext in exts):
			return url

		else:
			import liveresolver
			return liveresolver.resolve(url)