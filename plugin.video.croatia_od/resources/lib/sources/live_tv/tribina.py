from resources.lib.modules import client,webutils,control
import sys,os,re
from resources.lib.modules.log_utils import log
AddonPath = control.addonPath
IconPath = AddonPath + "/resources/media/"
def icon_path(filename):
    return os.path.join(IconPath, filename)

class info():
    def __init__(self):
    	self.mode = 'tribina'
        self.name = 'tribina.net'
        self.icon = 'sport.jpg'
        self.paginated = False
        self.categorized = False
        self.multilink = True

class main():
	def __init__(self):
		self.base = 'http://www.tribina.net/'

	def channels(self):
		html = client.request('http://www.tribina.net/index.html')
		events = re.findall('<h3>([^<]+)<span.+?class="matchtime">([^<]+)[^>]+>([^<]+)\s*</h3>',html,flags=re.DOTALL)
		events = self.__prepare_channels(events)
		return events

	def __prepare_channels(self,channels):
		new=[]
		urls=[]
		words = ['webmaster','asistencije']
		for ch in channels:
			if any(word in ch[2].lower() for word in words):
				continue
			date = ch[0].strip()
			time = ch[1].strip()
			title = ch[2].strip()
			title = '[COLOR orange][B][%s %s][/B][/COLOR] %s'%(date,time,title)
			url = ch[2]
			if url not in urls:

				urls.append(url)
				new.append((url,title,icon_path(info().icon)))
		#new.pop(-1)
		return new

	def links(self,url):
		out = []
		url = url.replace('(','\(').replace(')','\)').replace(' ','\s*')
		html = client.request('http://www.tribina.net/index.html')
		rg = '%s</h3>(.+?)<h3'%url
		area = re.findall(rg,html,flags=re.DOTALL)[0]
		links = re.findall('<a href=[\"\']([^\"\']+)[\"\'].+?>([^<]+)</a>',area)
		for l in links:
			out.append((l[0],l[1],control.icon_path(info().icon)))
		return out

	def resolve(self,url):
		import liveresolver
		return liveresolver.resolve(url)