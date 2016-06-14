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
    	self.mode = 'aljazeera'
        self.name = 'Aljazeera Balkans'
        self.icon = icon_path('AJB.png')
        self.paginated = True
        self.categorized = True
        self.multilink = False
        self.paginated_links = False


class main():
	def __init__(self,url = 'http://balkans.aljazeera.net/video/posljednji/DOKUMENTARCI'):
		self.base = 'http://balkans.aljazeera.net/'
		self.url = url


	def categories(self):
		out=[]
		cats = [['Dokumentarci','http://balkans.aljazeera.net/video/posljednji/DOKUMENTARCI'],['Recite Aljazeeri','http://balkans.aljazeera.net/video/posljednji/RECITE%20ALJAZEERI'],
            ['Kontekst','http://balkans.aljazeera.net/video/posljednji/Kontekst'],['Oni pobjeđuju','http://balkans.aljazeera.net/video/posljednji/ONI%20POBJE%C4%90UJU'],
            ['Nove emisije','http://balkans.aljazeera.net/video/posljednji/NOVE%20EMISIJE']]
		for c in cats:
			url = c[1]
			title = c[0]
			out.append((url,title,icon_path(info().icon)))
		return out

	def items(self):
		out = []
		html = client.request(self.url)
		soup = webutils.bs(html)
		lis=soup.findAll('li')
		for li in lis:
			try:
				thumb=li.find('img')['src']
				url=self.base + li.findAll('a')[1]['href']
				title=li.find('h2').getText().encode('utf-8')
				out.append([title,url,thumb])
			except:
				pass
		return out

	def next_page(self):
		html = client.request(self.url)
		try:
			next = self.base + re.findall('pager-next[\"\']><a href=[\"\'](.+?)[\"\']',html)[0]
		except:
			next = None
		return next

	def yt_video_id(self,value):
		id = re.compile('((?<=(v|V)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)').findall(value)[0]
		return id[3]

	def resolve(self,url):
		html = client.request(url)
		soup = webutils.bs(html)

		try:
			rreg = '<param name="playerID" value="(.+?)" /><param name="@videoPlayer" value="(.+?)" />'
			ids = re.compile(rreg).findall(html)[0]
			l = 'http://c.brightcove.com/services/viewer/federated_f9?&width=690&height=388&flashID=bcExperienceObj0&bgcolor=%23FFFFFF&ConvivaConfig.events=%20%3CConvivaEventsMap%3E%20%3Cevent%20name%3D%22mediaPlay%22%20module%3D%22videoPlayer%22%20eventType%3D%22mediaPlay%22%3E%20%3C%2Fevent%3E%20%3Cevent%20name%3D%22mediaError%22%20module%3D%22videoPlayer%22%20eventType%3D%22mediaError%22%3E%20%3Cattr%20key%3D%22errorCode%22%20type%3D%22eventField%22%20value%3D%22code%22%2F%3E%20%3C%2Fevent%3E%20%3C%2FConvivaEventsMap%3E%20&playerID='+ids[0]+'&%40videoPlayer='+ids[1]+ '&isVid=true&isUI=true&playerKey=AQ~~%2CAAAA1DWaSzk~%2CCZSkTksiPhQqITLsbi03E4KbEIFdh_zL'
			
		except:
			link = soup.find('iframe',{'class':'media-youtube-player'})['src']
			yt_id = self.yt_video_id(link)
			l = 'http://www.youtube.com/watch?v=' + yt_id

		import YDStreamExtractor
		YDStreamExtractor.disableDASHVideo(True) 
		vid = YDStreamExtractor.getVideoInfo(l,quality=1) 
		resolved = vid.streamURL() 
		return resolved

