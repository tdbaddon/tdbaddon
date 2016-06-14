from __future__ import unicode_literals
from resources.lib.modules import client,webutils,convert,control
from resources.lib.modules.log_utils import log
import re,urlparse,json,sys,os,xbmcgui



AddonPath = control.addonPath
IconPath = AddonPath + "/resources/media/"
def icon_path(filename):
    return os.path.join(IconPath, filename)

class info():
    def __init__(self):
    	self.mode = 'balkanje'
        self.name = 'Balkanje'
        self.icon = icon_path('Balkanje.png')
        self.paginated = False
        self.paginated_links = True
        self.categorized = True
        self.multilink = True


class main():
	def __init__(self,url = 'http://www.balkanje.com/index.html'):
		self.base = 'http://www.balkanje.com/'
		self.url = url


	def categories(self):
		out=[('newx','Novo/popularno',info().icon)]
		urls=[]
		html = client.request('http://www.balkanje.com/index.html')
		items = re.findall('<li class="dropdown-submenu"><a href="(.+?)" class="dropdown-submenu">(.+?)<',html,flags=re.UNICODE)
		for cat in items:
			url = cat[0]
			title = cat[1]
			if url not in urls:
				out.append((url,title,info().icon))
				urls.append(url)
		return out


	def items(self):
		out = []
		if self.url == 'newx':
			return [('Zadnje dodano','http://www.balkanje.com/newvideos.html',icon_path(info().icon)),
					('Popularno','http://www.balkanje.com/topvideos.html',icon_path(info().icon))]
		html = client.request(self.url)
		eps = client.parseDOM(html,'ul',attrs={'class':'list-inline'})
		eps = client.parseDOM(eps,'li')
		for ep in eps:
			url = re.findall('<a.+?href=[\"\'](.+?)[\"\']',ep)[0]
			img = info().icon
			title = client.parseDOM(ep,'a')[0]
			out.append((title.encode('utf-8'),url,img))

		return out

	
	def links(self,url):
		out=[]
		html = client.request(url)
		tag=client.parseDOM(html,'ul',attrs={'id':'pm-grid'})
		lis=client.parseDOM(tag,'li')
		for i in range(len(lis)):
			thumb = re.findall('[\"\']([^=]+thumb[^\"\']+)[\"\']',lis[i])[0]
			url = re.findall('href=[\"\'](.+?www[^\"\']+)[\"\']',lis[i])[0]
			title = re.findall('<img.+?alt=[\"\'](.+?)[\"\']',lis[i])[0].encode('utf-8')
			if 'ep' in url:
				out.append((title,url,thumb))
			
		return out

	def next_link_page(self,url):
		html = client.request(url)
		try:
			next = webutils.bs(html).find('li',{'class':'active'}).findNext('li').find('a')['href']
		except:
			next = False

		return next

	def resolve(self,url):
		out = []
		html = client.request(url)
		url2 = re.findall('(http://www.balkanje.com/embed.php[^\"\']+)[\"\']',html)[0]
		html = client.request(url2)
		try:
			url3 = re.findall('(http://www.balkanje.com/.+?tabserije[^\"\']+)',html)[0]
			html = client.request(url3)
		except:
			pass
		#dailymotion
		urls = re.findall('(https?://(?:www.)?dailymotion.com/embed/video/[^\"\']+)[\"\']',html)
		
		#youwatch
		urls+=re.findall('(http://youwatch.org/[^\"\']+)[\"\']',html)
		urls+=re.findall('(http://hqq.tv/[^\"\']+)[\"\']',html)
		urls+=re.findall('(vk.com/video[^\"\']+)',html)
		urls+=re.findall('(https?://(?:www.)?videoapi.my.mail.ru/videos/[^\"\']+)[\"\']',html)

		if len(urls)==1:
			url = urls[0]
			if url.startswith('vk.com'):
				url = 'http://' + url
			netloc = urlparse.urlparse(url).netloc
			netloc = netloc.replace('www.','').replace('config.','')
			netloc = re.sub(r'www\d+.','',netloc)
			if netloc in ['dailymotion.com','vk.com']:
				import urlresolver
				return urlresolver.resolve(url)
			if netloc=='youwatch.org':
				from resources.lib.resolvers import youwatch
				return youwatch.resolve(url)
		else:
			sources=[]
			for i in range(len(urls)):
				sources.append("%s. dio"%(i+1))
			dialog = xbmcgui.Dialog()
			index = dialog.select('Odaberite:', sources)
			if index==-1:
				return
			url = urls[index]
			if url.startswith('vk.com'):
				url = 'http://' + url
			netloc = urlparse.urlparse(url).netloc
			netloc = netloc.replace('www.','').replace('config.','')
			netloc = re.sub(r'www\d+.','',netloc)
			if netloc in ['dailymotion.com','vk.com','videoapi.my.mail.ru']:
				import urlresolver
				return urlresolver.resolve(url)
			if netloc=='youwatch.org':
				from resources.lib.resolvers import youwatch
				return youwatch.resolve(url)
		#out.append((title.encode('utf-8'),url,img))

		

	