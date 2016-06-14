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
    	self.mode = 'movtex'
        self.name = 'movtex.net'
        self.icon = icon_path('movtex.png')
        self.paginated = True
        self.categorized = True
        self.multilink = False
        self.paginated_links = False


class main():
	def __init__(self,url = 'http://www.movtex.net'):
		self.base = 'http://www.movtex.net/'
		self.url = url


	def categories(self):
		out=[('http://www.movtex.net/videos','Zadnje epizode',icon_path(info().icon))]
		urls=[]
		html = client.request(self.base)
		items = re.findall('<a href=[\"\']([^\"\']+)[\"\']>\s*<div class="thumb-overlay">\s*<img src=[\"\']([^\"\']+)[\"\'] title=[\"\']([^\"\']+)[\"\']',html,flags=re.UNICODE)
		for cat in items:
			url = self.base + cat[0]
			title = cat[2]
			img = self.base + cat[1]
			if url not in urls:
				out.append((url,title,img))
				urls.append(url)
		return out

	def items(self):
		out = []
		
		html = client.request(self.url)
		eps = re.findall('<a href=[\"\']([^\"\']+)[\"\']>\s*<div.+?>\s*<img src=[\"\']([^\"\']+)[\"\']\s*title=[\"\']([^\"\']+)[\"\']',html)
		for ep in eps:
			title = ep[2]
			url = self.base + ep[0].decode('utf-8')
			img = ep[1]
			out.append((title,url,img))

		return out

	
	
	def resolve(self,url):
		html = client.request(url)
		try:
			url = re.findall('config=(http://www.movtex.net/media/nuevo/config.php[^\"\']+)',html)[0]
			html = client.request(url)
			url = re.findall('<file>\s*(.+?)\s*</file>',html)[0]
		except:
			url = 'http://' + re.findall('(www.movtex.+?/video(?:-embeded.php)?[^\"\']+)',html)[0]
			html = client.request(url)
			url =  'http:' +   re.findall('videoUrl\s*=\s*[\"\']([^\"\']+)[\"\']',html)[0]
			import urlresolver
			url = urlresolver.resolve(url)

		return url
		

	def next_page(self):
		html = client.request(self.url)
		try:
			next = re.findall('href=[\"\']([^\"\']+)[\"\'] class="prevnext">&raquo;',html)[0]
		except:
			next = None
		return next