from __future__ import unicode_literals
from resources.lib.modules import client,live365
import re, urllib
import sys,xbmcgui,os
from addon.common.addon import Addon
from resources.lib.modules.log_utils import log

addon = Addon('plugin.video.croatia_od', sys.argv)

AddonPath = addon.get_path()
IconPath = AddonPath + "/resources/media/"
def icon_path(filename):
    return os.path.join(IconPath, filename)

class info():
    def __init__(self):
    	self.mode = 'live365'
        self.name = 'Sport raspored'
        self.icon = 'sport.jpg'
        self.paginated = False
        self.categorized = False
        self.multilink = False
class main():
	def __init__(self,url = ''):
		self.base = ''
		self.url = url

	

	def channels(self):
		links = live365.getLinks()
		out = []
		for link in links:
			time,name,quality,url,enabled = link
			title = '%s [B]%s[/B] %s'%(time,name.decode('utf-8'),quality)
			if not enabled:
				url="x"
			img = icon_path(info().icon)
			out.append((url,title.encode('utf-8'),img))

		return out

	
	def resolve(self,url):
		if url=='x':
			return None
		import base64
		url=base64.b64decode(url)
		url = url.split('Sports365:')[1]
		if url.startswith('cid:'): url=base64.b64decode('aHR0cDovL2ZlcnJhcmlsYi5qZW10di5jb20vaW5kZXgucGhwLzJfNS9neG1sL3BsYXkvJXM=')%url.replace('cid:','')		
		url=base64.b64decode(url)
		url = live365.selectMatch(url)
		return url



