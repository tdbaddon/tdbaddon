from __future__ import unicode_literals
from resources.lib.modules import client, webutils
import re,sys,xbmcgui,os
from addon.common.addon import Addon
addon = Addon('plugin.video.castaway', sys.argv)

AddonPath = addon.get_path()
IconPath = AddonPath + "/resources/media/"
def icon_path(filename):
    return os.path.join(IconPath, filename)

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
           events.append((url,title,icon_path(info().icon)))
        events.sort(key=lambda x: x[1])
        return events
	
    def resolve(self,url):
        import liveresolver
        return liveresolver.resolve(url)