from __future__ import unicode_literals
from resources.lib.modules import client,webutils,convert,control
from resources.lib.modules.log_utils import log
import re,urlparse,json,sys,os



AddonPath = control.addonPath
IconPath = AddonPath + "/resources/media/"
def icon_path(filename):
    return os.path.join(IconPath, filename)

class info():
    def __init__(self):
    	self.mode = 'rtlsada'
        self.name = 'RTL Sada'
        self.icon = icon_path('RTL sada.jpg')
        self.paginated = False
        self.categorized = True
        self.multilink = True
        self.paginated_links = False


class main():
	def __init__(self,url = 'http://www.sada.rtl.hr/programi/?group=category'):
		self.base = 'http://www.sada.rtl.hr/'
		self.url = url


	def categories(self):
		out=[]
		urls=[]
		html = client.request('http://www.sada.rtl.hr/programi/?group=category')
		items = re.findall('<li class="Dropdown-item">\s*<a href=[\"\']([^\"\']+)[\"\']>([^<]+)<',html,flags=re.UNICODE)
		for cat in items:
			url = self.base + 'sadrzaji/' + cat[0]
			url = url.replace('&amp;','&')
			title = cat[1]
			if url not in urls:
				out.append((url,title,icon_path(info().icon)))
				urls.append(url)
		return out

	def items(self):
		out = []
		if self.url == 'http://www.sada.rtl.hr/sadrzaji/?group=category':
			self.url = 'http://www.sada.rtl.hr/sadrzaji/?group=alphabet'
		html = client.request(self.url)
		try:
			eps = client.parseDOM(html,'ul',attrs={'class':'Container-content Media'})
		except:
			return out
		eps = client.parseDOM(eps,'li')
		for ep in eps:
			url = re.findall('<a.+?href=[\"\'](.+?)[\"\']',ep)[0]
			img = re.findall('<img.+?src=[\"\'](.+?)[\"\']',ep)[0]
			title = re.findall('News-title[\"\']>(.+?)<',ep)[0]
			out.append((title.encode('utf-8'),url,img))

		return out

	
	def links(self,url):
		out = []
		html = client.request(url)
		try:
			eps = client.parseDOM(html,'ul',attrs={'class':'Container-content Media'})
		except:
			return out
		eps = client.parseDOM(eps,'li')
		for ep in eps:
			url = re.findall('<a.+?href=[\"\'](.+?)[\"\']',ep)[0]
			img = re.findall('<img.+?src=[\"\'](.+?)[\"\']',ep)[0]
			title = re.findall('News-title[\"\']>(.+?)<',ep)[0]
			subtitle = ': ' + re.findall('Catchup-info[\"\']>\s*(.+?)\s*<',ep)[0]
			title = title + subtitle
			out.append((title.encode('utf-8'),url,img))

		return out
	def resolve(self,url):
		html = client.request(url+'?xml=1')
		url = re.findall('\[CDATA\[\s*(http.+?)\s*\]',html)[0]
		return url
		

	