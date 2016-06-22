from __future__ import unicode_literals
from resources.lib.modules import client
import re


class info():
    def __init__(self):
    	self.mode = 'crichd'
        self.name = 'crichd.tv'
        self.icon = 'crichd.png'
        self.paginated = False
        self.categorized = False
        self.multilink = False
class main():
	def __init__(self):
		self.base = 'http://www.crichd.tv'

	def channels(self):
		html = client.request(self.base, referer=self.base)
		regex='<li><a <a class="menuitem" href="(.+?)"><img src="(.+?)".+?alt="(.+?)"/>'
		reg=re.compile(regex)
		channels = re.findall(regex,html)
		events = self.__prepare_channels(channels)
		return events

	def __prepare_channels(self,channels):
		new=[]
		channels.pop(0)
		for channel in channels:

			img = self.base + channel[1]
			url = self.base + channel[0]
			title = channel[2]
			new.append((url,title,img))
		return new



	def resolve(self,url):
		import liveresolver
		return liveresolver.resolve(url)