# -*- coding: utf-8 -*-
from resources.lib.modules import client,epg,convert,control
import re
from resources.lib.modules.log_utils import log
import sys,xbmcgui,os


class info():
    def __init__(self):
    	self.mode = 'live_my'
        self.name = 'Live TV'
        self.icon = 'TV.png'
        self.paginated = False
        self.categorized = True
        self.multilink = False
        
class main():
	def __init__(self,url = 'http://www.serbiaplus.club/menu1.html'):
		self.base = 'https://github.com/natko1412/liveStreams/raw/master/'
		self.url = url

	def categories(self):
		cats=[['Hrvatski','hrvatski','http://sprdex.com/wp-content/uploads/2012/07/RTL-televizija.jpg'],
		['Dokumentarci','Dokumentarci-eng','http://cdn.fansided.com/wp-content/blogs.dir/280/files/2014/07/33506.jpg'],
		['Sport','sport','http://www.hospitalityandcateringnews.com/wp-content/uploads/New-BT-Sport-TV-packages-for-hospitality-to-massively-undercut-Sky.jpg'],
		['News','news','http://hub.tv-ark.org.uk/images/news/skynews/skynews_images/2001/skynews2001.jpg'],
		['Filmovi/serije','film-serije','http://www.fox.com/sites/default/files/fox_logo_1.jpg'],
		['Lifestyle','lifestyle','http://pmcdeadline2.files.wordpress.com/2013/04/travelchannel_logo__130423191643.jpg'],
		['Glazba','tv-music','http://vignette3.wikia.nocookie.net/90scartoons/images/b/bc/Mtv-logo-Logo.png/revision/latest?cb=20140219002555'],
		['Dječji programi','djecji','http://upload.wikimedia.org/wikipedia/pt/archive/f/fe/20120623043934!Logo-TV_Kids.jpg'],
		['Slovenski','slovenski','http://livetvland.com/images/flags/xSlovenia-flag.png.pagespeed.ic.y5MQP9u4Hx.png'],
		['Regionalni','regionalni','http://www.tvsrbija.net/wp-content/uploads/2013/01/pinktv.jpg']]
		out = []
		for cat in cats:
			title = cat[0]
			url = self.base +  cat[1] + '.txt'
			img = cat[2]
			out.append((url,title,img))
		return out

	def channels(self,url):
		html = client.request(url)
		urls = re.findall('url\s*=\s*"(.+?)"',html)
		imgs = re.findall('img\s*=\s*"(.+?)"',html)
		titles = re.findall('ime\s*=\s*"(.+?)"',html,flags=re.UNICODE)
		epgs = re.findall('epg\s*=\s*"(.+?)"',html)
		events = self.__prepare_channels(urls,titles,imgs,epgs)
		return events

	def __prepare_channels(self,urls,titles,imgs,epgs):
		new=[]
		for i in range(len(urls)):
			url = urls[i]
			img = imgs[i]
			title = titles[i].decode('utf-8')
			epgx = self.get_epg(epgs[i])
			title = '[B]%s[/B] - [I][COLOR green]%s[/COLOR][/I]'%(title,epgx)
			title = convert.unescape(title)
			new.append((url,title.encode('utf-8'),img))
		return new

	def get_epg(self,epgx):
		return epg.get_current_epg(epgx)

	def resolve(self,url):
		urls = url.split('##')
		choices = ['Link %s'%(i+1) for i in range(len(urls))]
		
		if len(choices)==1:
			index=0
		else:
			index = control.selectDialog(choices,'Odaberite link:')
		if index>-1:
			url = urls[index]
			if 'morescreens' in url:
				from resources.lib.resolvers import hrti
				return hrti.resolve(url)

			if 'streamlive.to' in url:
				log('using my')
				from resources.lib.resolvers import streamlive
				return streamlive.resolve(url)

			#nova tv, doma tv
			specy = {'http://www.sipragezabava.com/kanal_3_hr.php':'http://prvenstvoliga.blogspot.hr/2014/12/nova-tv.html',
					'http://www.netraja.net/2014/05/doma-tv.html':'http://www.prvenstvoliga.blogspot.hr/2014/05/doma-tv.html'}
			if url in specy.keys():
				urlx = []
				src = []
				html = client.request(specy[url],referer='http://prvenstvoliga.blogspot.com/search/label/Hrvatska')
				urls = re.findall('target=[\"\']([^\"\']+)[\"\'].+?</embed>',html)
				i=0
				for url in urls:
					i+=1
					src+=['Link %s'%i]
					
				dialog = xbmcgui.Dialog()
				index = dialog.select('Odaberite:', src)
				if index==-1:
					return ''
				return urlx[index]

			import liveresolver
			return liveresolver.resolve(url)
	


		return ''