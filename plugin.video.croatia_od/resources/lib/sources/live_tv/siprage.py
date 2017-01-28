# -*- coding: utf-8 -*-
from resources.lib.modules import client,epg,convert,control
import re
from resources.lib.modules.log_utils import log
import sys,xbmcgui,os


class info():
    def __init__(self):
    	self.mode = 'siprage'
        self.name = 'sipragezabava.com'
        self.icon = 'TV.png'
        self.paginated = False
        self.categorized = True
        self.multilink = False
        
class main():
	def __init__(self,url = 'http://www.sipragezabava.com/'):
		self.base = 'http://www.sipragezabava.com/'
		self.url = url

	def categories(self):
		out = []
		cats=[['Hrvatski','http://www.sipragezabava.com/HRT_1_uzivo.php','http://sprdex.com/wp-content/uploads/2012/07/RTL-televizija.jpg'],
		['Sport','http://www.sipragezabava.com/kanal_2_yu.php','http://www.hospitalityandcateringnews.com/wp-content/uploads/New-BT-Sport-TV-packages-for-hospitality-to-massively-undercut-Sky.jpg'],
		['Glazba','http://www.sipragezabava.com/dm_sat_rs.php','http://vignette3.wikia.nocookie.net/90scartoons/images/b/bc/Mtv-logo-Logo.png/revision/latest?cb=20140219002555'],
		['Slovenski','http://www.sipragezabava.com/kanal_1_sl.php','http://livetvland.com/images/flags/xSlovenia-flag.png.pagespeed.ic.y5MQP9u4Hx.png'],
		['BiH','http://www.sipragezabava.com/BHT_1_uzivo.php','https://upload.wikimedia.org/wikipedia/en/c/ce/BHT_1_logo.png'],
		['Srpski','http://www.sipragezabava.com/kanal_1_rs.php','http://www.tvsrbija.net/wp-content/uploads/2013/01/pinktv.jpg']]
		for c in cats:
			out.append((c[1],c[0],c[2]))
		return out

	def channels(self,url):
		html = client.request(url)
		html = client.parseDOM(html, 'div', attrs={'style':'position:absolute;left:30px;top:260px.+?'})[0]
		channels = re.findall('<a href=[\"\']./([^\"\']+)[\"\'] target="_self">([^<]+)<',html)
		events = self.__prepare_channels(channels)
		return events

	def __prepare_channels(self,channels):
		img = control.icon_path(info().icon)
		new=[]
		for c in channels:
			url = self.base + c[0]
			title = convert.unescape(c[1])
			if '.ts' in url:
				url = 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&url=%s' %(urllib.quote(url))
			new.append((url,title.encode('utf-8'),img))
		return new


	def resolve(self,url):
		import liveresolver
		return liveresolver.resolve(url)
	


