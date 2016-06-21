# -*- coding: utf-8 -*-
from resources.lib.modules import client,webutils,convert,control
from resources.lib.modules.log_utils import log
import re,os,xbmcgui


AddonPath = control.addonPath
IconPath = AddonPath + "/resources/media/"
def icon_path(filename):
    return os.path.join(IconPath, filename)

class info():
    def __init__(self):
    	self.mode = 'serijex'
        self.name = 'serijex.com'
        self.icon = icon_path('serijex.png')
        self.paginated = False
        self.categorized = True
        self.multilink = True
        self.paginated_links = False


class main():
	def __init__(self,url = 'http://www.serijex.com'):
		self.base = 'http://www.serijex.com'
		self.url = url
		self.lista = 'https://raw.githubusercontent.com/natko1412/cod/master/serijex'
		self.sez = {'prva': '1. Sezona', 'druga': '2. Sezona', 'treca':'3. Sezona', 'cetvrta':'4. Sezona', 'peta':'5. Sezona', 'sesta':'6. Sezona', 'sedma':'7. Sezona', 'osma':'8. Sezona','deveta':'9. Sezona'}


	def categories(self):
		out=[]
		cats = eval(client.request(self.lista))
		for c in cats:
			url = c[1]
			title = c[0]
			out.append((url,title,c[2]))
		out.sort(key=lambda x: x[1])
		return out

		

	def items(self):
		out = []
		html = client.request(self.base)
		html = html.replace('/originals-','/the-originals-').replace('/vampire-diaries-','/the-vampire-diaries-').replace('/blacklist-','/the-blacklist-')
		thumb = re.findall("%s[\"\']\s*,\s*'(http://thetvdb.com.+?.jpg)"%self.url,client.request(self.lista))[0]
		seasons = re.findall('(http://www.serijex.com/%s-(.+?)-sezona)'%self.url,html)
		seasons = set(seasons)
		for s in seasons:
			sz = self.sez[s[1]]
			out.append([sz,s[0],thumb])
		out.sort(key=lambda x: x[0])
		return out

	def links(self,url):
		out = []
		html = client.request(self.base).replace('/originals-','/the-originals-').replace('/vampire-diaries-','/the-vampire-diaries-').replace('/blacklist-','/the-blacklist-')
		slug = re.findall('serijex.com/(.+?)-[^-]+-sezona',url)[0]
		thumb = re.findall("%s[\"\']\s*,\s*'(http://thetvdb.com.+?.jpg)"%slug,client.request(self.lista))[0]
		sezona = self.sez[re.findall('-([^-]+)-sezona',url)[0]]
		episodes = re.findall('(%s-epizoda-(\d+)[^\"\']+)'%url,html)
		episodes = set(episodes)
		for s in episodes:
			title = 'Epizoda %02d'%int(s[1])
			out.append([title,s[0],thumb])
		out.sort(key=lambda x: x[0])
		return out


	def _resolve_serijex(self,url):
		html = client.request(url)
		
		try:
			enigma = re.findall('data-enigmav\s*=\s*[\"\']([^\"\']+)',html)[0].replace(r'-',r'\u00')
			enigma = enigma.decode('unicode-escape')
			url = re.findall('frame.+?src=[\"\']([^\"\']+)',enigma,flags=re.I)[0]
			return url
		except:
			return ''




	def resolve(self,url):
		html = client.request(url)
		if html is None:
			url = url.replace('the-','')
			html = client.request(url)
		urls = []
		choices = []
		vm = re.findall('[\"\'](http://videomega.tv/validatehash[^\"\']+)',html)
		urls += vm
		for i in range(len(vm)):
			choices.append('videomega.tv')

		ostali = re.findall('href=[\"\']([^\"\']+)[\"\'] target=[\"\']_blank[\"\'] rel=[\"\']nofollow[\"\']>Gledaj na',html)
		for o in ostali:
			urls.append(o)
			title = o.split('-')[-1].rstrip('/')
			choices.append(title)
		dialog = xbmcgui.Dialog()
		index = dialog.select('Odaberite:', choices)
		if index==-1:
			return
		url = urls[index]

		if 'serijex' in url:
			url = self._resolve_serijex(url)
		import urlresolver
		return urlresolver.resolve(url)

