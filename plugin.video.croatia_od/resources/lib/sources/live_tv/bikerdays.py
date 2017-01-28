from __future__ import unicode_literals
from resources.lib.modules import m3u_parser,parental,control
import sys,os

AddonPath = control.addonPath
IconPath = AddonPath + "/resources/media/"
def icon_path(filename):
    return os.path.join(IconPath, filename)

class info():
    def __init__(self):
    	self.mode = 'bikerdays'
        self.name = 'Bikerdays TV Lista'
        self.icon = 'bikerdays.jpg'
        self.paginated = False
        self.categorized = False
        self.multilink = False

class main():
	def __init__(self,url = 'http://pastebin.com/raw.php?i=jmseyhvw'):
		self.base = 'http://pastebin.com/raw.php?i=jmseyhvw'
		self.url = url

	def channels(self):
		out = []
		tracks = m3u_parser.parseM3U(self.url)
		for track in tracks:
			title=track.title
			try:
				if 'ODRASLE' in title:
					if not parental.Parental().isVisible():
						return out
			except:
				pass
			url=track.path
			img = icon_path(info().icon)
			out.append((url,title,img))
		return out

	def resolve(self,url):
		return url
	


