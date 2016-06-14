# -*- coding: utf-8 -*-
from resources.lib.modules import client,webutils,convert,control
from resources.lib.modules.log_utils import log
import re,os


AddonPath = control.addonPath
IconPath = AddonPath + "/resources/media/"
def icon_path(filename):
    return os.path.join(IconPath, filename)

class info():
    def __init__(self):
    	self.mode = 'n1'
        self.name = 'N1'
        self.icon = icon_path('N1.png')
        self.paginated = False
        self.categorized = True
        self.multilink = False
        self.paginated_links = False


class main():
	def __init__(self,url = 'http://hr.n1info.com'):
		self.base = 'http://hr.n1info.com/'
		self.url = url


	def categories(self):
		out=[]
		cats = [['Pressing','http://hr.n1info.com/a3525/TV-Emisije/Pressing/Pressing.html','http://i.imgur.com/3nm5bcu.jpg'],
    ['Dnevnik u 19','http://hr.n1info.com/a3658/TV-Emisije/Dnevnik-u-19/Dnevnik-u-19h.html','http://i.imgur.com/LeS4fXI.jpg']]
		for c in cats:
			url = c[1]
			title = c[0]
			img = c[2]
			out.append((url,title,img))
		return out

	def items(self):
		out = []
		html = client.request(self.url)
		soup = webutils.bs(html)
		tag=soup.find('div',{'data-ajax-param':'Epizode'})
		eps=tag.findAll('article')
		out=[]
		for ep in eps:
			url=ep.find('a')['href']
			thumb=ep.find('img')['src']
			title=ep.find('h1').getText().encode('utf-8')
			out+=[[title,url,thumb]]
		return out

	

	def yt_video_id(self,value):
		id = re.compile('((?<=(v|V)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)').findall(value)[0]
		return id[3]

	def resolve(self,url):
		html = client.request(url)
		soup = webutils.bs(html)
		video=soup.find('iframe')['src']
		if 'youtube' in video:
			yt_id = self.yt_video_id(video)
			l = 'http://www.youtube.com/watch?v=' + yt_id

			import YDStreamExtractor
			YDStreamExtractor.disableDASHVideo(True) 
			vid = YDStreamExtractor.getVideoInfo(l,quality=1) 
			resolved = vid.streamURL() 
			return resolved

