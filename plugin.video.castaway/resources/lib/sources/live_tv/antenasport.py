from __future__ import unicode_literals
from resources.lib.modules import client,webutils,control,convert
from resources.lib.modules.log_utils import log
import re,os



class info():
    def __init__(self):
    	self.mode = 'antenasport'
        self.name = 'antenasport.org'
        self.icon = 'live.png'
        self.paginated = False
        self.categorized = False
        self.multilink = False

class main():
	def __init__(self):
		self.base = control.setting('antena_base')
		self.schedule = control.setting('antena_sch')

	def channels(self):

		html = client.request(self.base + self.schedule)
		channels = webutils.bs(html).findAll('a',{'target':'_top'})
		events = self.__prepare_channels(channels)
		return events

	def __prepare_channels(self,channels):
		
		urls=[]
		img= control.icon_path(info().icon)
		new=[('#schedule','Schedule',img)]
		for channel in channels:
			url = channel['href']
			if self.base not in url:
				if 'http:' in url:
					continue
				url = self.base + '/' + url
			title = channel.getText()
			if url not in urls and len(title)>0 and '***' not in title:

				new.append((url,title,img))
				urls.append(url)
		return new

	def show_schedule(self):
		text = ''
		html = client.request(self.base + self.schedule)
		content = re.findall('_top.>([^<]+)([^*]+)+',html)
		for x in content:
			items = re.findall('ws\d+.>([^<]+)',x[1])
			if len(items)!=0:
				text += '[B]%s[/B]\n'%x[0]
			for item in items:
				text +='%s\n'%convert.unescape(item.decode('ascii','ignore'))
			if len(items)!=0:
				text+='\n'
		webutils.show_text('Antena Sport Schedule',text)
		#import xbmcgui
		#xbmcgui.Dialog().textviewer('Antena Sport Schedule',text)

	def resolve(self,url):
		if url == '#schedule':
			self.show_schedule()
			return ''
		import liveresolver
		return liveresolver.resolve(url,cache_timeout=0)