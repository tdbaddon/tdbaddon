# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from resources.lib.modules import client,webutils,convert,control
from resources.lib.modules.log_utils import log
import re,os,urlparse

AddonPath = control.addonPath
IconPath = AddonPath + "/resources/media/"
def icon_path(filename):
    return os.path.join(IconPath, filename)

class info():
    def __init__(self):
    	self.mode = 'jockan'
        self.name = 'JockanTV Crtani'
        self.icon = icon_path('jockan.png')
        self.paginated = False
        self.categorized = True
        self.multilink = True
        self.paginated_links = False


class main():
	def __init__(self,url = 'http://jockantv.pondi.hr/sinkronizirani-crtici/popis-crtica.html'):
		self.base = 'http://jockantv.pondi.hr/'
		self.url = url

	def categories(self):
		cats = [
		('http://jockantv.com/sinkronizirani-crtici/popis-crtica.html','Sinkronizirani crtići',icon_path(info().icon)),
		('http://jockantv.com/strani-crtici.html','Strani crtići',icon_path(info().icon))
		]

		return cats

	def items(self):
		out = []
		html = client.request(self.url)
		img = icon_path(info().icon)
		if 'sinkronizirani' in self.url:
			items = re.findall('(http://adf.ly/.+?)[\"\'] target=[\"\']_blank.+?>([^<]+)<',html)
		else:
			items = re.findall('(http://adf.ly/.+?)[\"\'] target=[\"\']_blank[\"\']>\s*<img alt=[\"\']([^\"\']+)[\"\'].+?src=[\"\']([^\"\']+)[\"\']',html)
		for item in items:
			if 'strani' in self.url:
				img = item[2]
			out.append((item[1],item[0],img))


		return out

	def links(self,url):
		out = []
		url = webutils.adfly(url)
		html = client.request(url)
		title = re.findall('<title>([^<]+)<',html)[0]
		title = re.sub(u'- Online sinkronizirani crtići','',title).rstrip()
		links = re.findall('href=[\"\']([^\"\']+)[\"\'].+?id="btn_',html)

		img = icon_path(info().icon)
		name = re.findall('<title>([^-]+)',html,flags=re.UNICODE)[0]
		i = 1
		for link in links:
			base = urlparse.urlparse(link).netloc.replace('www.','').upper()
			
			title = '[B]%s %s[/B]'%(name.decode('utf-8','ignore'),base)
			if base.strip() == '':
				continue
			out.append((title.encode('utf-8'),link,img))
			i += 1

		i = 0

		if len(out)==0:
			import urlresolver
			links = re.findall('src=[\"\']([^\"\']+)[\"\']',html)
			for link in links:
				try:
					resolved = urlresolver.resolve(link)
					if resolved:
						base = urlparse.urlparse(link).netloc.replace('www.','').upper()
						title = '[B]%s %s[/B]'%(name.decode('utf-8','ignore'),base)
						if base.strip() == '':
							continue
						out.append((title.encode('utf-8'),link,img))
						i += 1
				except:
					pass
		return out


	def resolve(self,url):
		if 'jockan' in url.decode('ascii','ignore'):
			url = re.findall('src=[\"\']([^\"\']+)[\"\']',client.request(url))[0]
		import urlresolver
		return urlresolver.resolve(url)
		

	