from __future__ import unicode_literals
from resources.lib.modules import client, webutils,control
import re,sys,xbmcgui,os



class info():
    def __init__(self):
    	self.mode = 'usachannels'
        self.name = 'usachannels.tv'
        self.icon = 'usachannels.png'
        self.paginated = False
        self.categorized = False
        self.multilink = False

class main():
    def __init__(self):
        self.base = 'http://usachannels.tv/'
        
    def channels(self):
        html = client.request(self.base)
        soup = webutils.bs(html)
        channels = soup.find('div',{'id':'chanels'}).findAll('li')
        events = []
        for c in channels:
           url = self.base + c.find('a')['href'] 
           title = c.getText()
           events.append((url,title,control.icon_path(info().icon)))
        events.sort(key=lambda x: x[1])
        return events
	
    def resolve(self,url):
        import liveresolver
        return liveresolver.resolve(url)