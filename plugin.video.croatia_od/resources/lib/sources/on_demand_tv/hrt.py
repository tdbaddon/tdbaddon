from __future__ import unicode_literals
from resources.lib.modules import client,webutils,convert,control
from resources.lib.modules.log_utils import log
import re,os

AddonPath = control.addonPath
IconPath = AddonPath + "/resources/media/"
def icon_path(filename):
    return os.path.join(IconPath, filename)

class info():
    def __init__(self):
    	self.mode = 'hrt'
        self.name = 'HRT na zahtjev'
        self.icon = icon_path('HRT.jpg')
        self.paginated = False
        self.categorized = True
        self.multilink = False
        self.paginated_links = False


class main():
	def __init__(self,url = 'http://www.hrt.hr/enz/dnevnik/'):
		self.base = 'http://www.hrt.hr/'
		self.url = url


	def categories(self):
		out=[]
		html = client.request(self.url)
		shows = client.parseDOM(html,'div', attrs={'class':'all_shows'})
		shows = client.parseDOM(shows, 'a',ret='href')
		for show in shows:
			soup = webutils.bs(show)
			url = 'http:' + soup.find('a')['href']
			title = soup.find('a').getText()
			out.append((url,title.encode('utf-8'),icon_path(info().icon)))
		return out

	def items(self):
		out = []
		html = client.request(self.url)
		try:
			eps = client.parseDOM(html,'td',attrs={'class':'episode_wrap'})[0]
		except:
			return out
		eps = client.parseDOM(eps,'select')[0]
		eps = re.findall('value=[\"\']([^\"\']+)[\"\']>([^<]+)<',eps,flags=re.UNICODE)
		show = re.findall('<td class="show_name"><h1>(.+?)</h1><',html,flags=re.UNICODE)[0]
		for ep in eps:
			url = self.url + ep[0]
			try:
				title = show.decode('utf-8') + ' ' + ep[1].decode('utf-8')
			except:
				try:
					title = show + ' ' + ep[1].decode('utf-8')
				except:
					title = show.decode('utf-8') + ' ' + ep[1]

			img = icon_path(info().icon)
			out.append((title.encode('utf-8'),url,img))

		return out

	
	

	def resolve(self,url):
		html = client.request(url)
		url = re.findall('(http:.+?.mp4)[\"\']',html)[0]
		return url
		

	