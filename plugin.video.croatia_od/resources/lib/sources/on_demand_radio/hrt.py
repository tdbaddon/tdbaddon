# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from resources.lib.modules import client,webutils,convert,control
from resources.lib.modules.log_utils import log
import re,os

AddonPath = control.addonPath
IconPath = AddonPath + "/resources/media/"
def icon_path(filename):
    return os.path.join(IconPath, filename)

radio_prvi=[['http://radio.hrt.hr/arhiva/glazbena-kutijica/106/','Glazbena kutijica','http://radio.hrt.hr/data/show/small/000106_dc8c3b107ed03fe1d72a.png'],
    ['http://radio.hrt.hr/arhiva/katapultura/124/','Katapultura','http://radio.hrt.hr/data/show/small/000124_7f8a2fc760da4ffb13fd.jpg'],
    ['http://radio.hrt.hr/arhiva/kutija-slova/121/','Kutija slova','http://radio.hrt.hr/data/show/small/000121_c915aa04c682cd4ceae9.png'],
    ['http://radio.hrt.hr/arhiva/lica-i-sjene/131/','Lica i sjene','http://radio.hrt.hr/data/show/small/000131_f1fccaf5f9deb049a2a8.png'],
    ['http://radio.hrt.hr/arhiva/oko-znanosti/123/','Oko znanosti','http://radio.hrt.hr/data/show/small/000123_9d42ba1671b607c73749.png'],
    ['http://radio.hrt.hr/arhiva/pod-reflektorima/103/','Pod reflektorima','http://radio.hrt.hr/data/show/small/000103_00f27f731e2db0a017b1.png'],
    ['http://radio.hrt.hr/arhiva/povijest-cetvrtkom/126/','Povijest cetvrtkom','http://radio.hrt.hr/data/show/small/000126_d237561e30ad805abd1b.png'],
    ['http://radio.hrt.hr/arhiva/putnici-kroz-vrijeme/582/','Putnici kroz vrijeme','http://radio.hrt.hr/data/show/small/000582_17ce2778878d5f74d4c5.png'],
    ['http://radio.hrt.hr/arhiva/slusaj-kako-zemlja-dise/120/','Slusaj kako zemlja dise','http://radio.hrt.hr/data/show/small/000120_1fa05c0fdaa00afca3a9.png'],
    ['http://radio.hrt.hr/arhiva/u-sobi-s-pogledom/112/','U sobi s pogledom','http://radio.hrt.hr/data/show/small/000112_587e449519318aa90b41.png'],
    ['http://radio.hrt.hr/arhiva/zasto-tako/114/','Zasto tako?','http://radio.hrt.hr/data/show/small/000114_176003cffe60b893e589.png'],
    ['http://radio.hrt.hr/arhiva/znanjem-do-zdravlja/117/','Znanjem do zdravlja','http://radio.hrt.hr/data/show/small/000117_582f3d27a0e52c7e78be.png']]
radio_drugi=[['http://radio.hrt.hr/arhiva/andromeda/18/','Andromeda','http://radio.hrt.hr/data/show/000018_f48cf7a1b19bf447b1e5.png'],
    ['http://radio.hrt.hr/arhiva/drugi-pogled/993/','Drugi pogled','http://radio.hrt.hr/data/show/small/000993_6fa6ff53c88f1ed3e50e.jpg'],
    ['http://radio.hrt.hr/arhiva/gladne-usi/700/','Gladne usi','http://radio.hrt.hr/data/show/small/000700_cdcdeaf6c30f86069ffd.png'],
    ['http://radio.hrt.hr/arhiva/globotomija/817/','Globotomija','http://radio.hrt.hr/data/show/small/000817_ec6bddd7f2754bb19eb5.jpg'],
    ['http://radio.hrt.hr/arhiva/homo-sapiens/812/','Homo sapiens','http://radio.hrt.hr/data/show/small/000812_9d0f8f96fca9b3826dbf.jpg']]
radio_treci=[['http://radio.hrt.hr/arhiva/bibliovizor/713/','Bibliovizor','http://radio.hrt.hr/data/show/small/000713_e1aaeb9afcb944db39ca.jpg'],
    ['http://radio.hrt.hr/arhiva/filmoskop/98/','Filmoskop','http://radio.hrt.hr/data/show/small/000098_0fbee68352530480fe0e.jpg'],
    ['http://radio.hrt.hr/arhiva/glazba-i-obratno/614/','Glazba i obratno','http://radio.hrt.hr/data/show/small/000614_8155a16df37fd274d77f.jpg'],
    ['http://radio.hrt.hr/arhiva/lica-okolice/717/','Lica okolice','http://radio.hrt.hr/data/show/small/000717_e5af40b1d5af68406fc3.jpg'],
    ['http://radio.hrt.hr/arhiva/mikrokozmi/102/','Mikrokozmi','http://radio.hrt.hr/data/show/small/000102_2f995b3b984cdd82f923.jpg'],
    ['http://radio.hrt.hr/arhiva/moj-izbor/91/','Moj izbor','http://radio.hrt.hr/emisija/moj-izbor/91/'],
    ['http://radio.hrt.hr/arhiva/na-kraju-tjedna/196/','Na kraju tjedna','http://radio.hrt.hr/data/show/small/000196_7c5997025a9bfcf45967.jpg'],
    ['http://radio.hrt.hr/arhiva/poezija-naglas/720/','Poezija naglas','http://radio.hrt.hr/data/show/small/000720_c2495423cd72b180482f.jpg'],
    ['http://radio.hrt.hr/arhiva/znanost-i-drustvo/950/','Znanost i drustvo','http://radio.hrt.hr/data/show/small/000950_6dd01f01230facbf40b0.jpg']]


class info():
    def __init__(self):
    	self.mode = 'hrt'
        self.name = 'HRT Radio na zahtjev'
        self.icon = icon_path('HR.png')
        self.paginated = False
        self.categorized = True
        self.multilink = True
        self.paginated_links = False


class main():
	def __init__(self,url = 'http://www.hrt.hr/enz/dnevnik/'):
		self.base = 'http://radio.hrt.hr/'
		self.url = url


	def categories(self):
		out=[('prvi','Prvi Program',icon_path(info().icon)),
		('drugi','Drugi Program',icon_path(info().icon)),
		('treci','Treći Program',icon_path(info().icon))]
		
		return out

	def channels(self,url):
		out = []
		exec('lista = radio_%s'%url)
		for li in lista:
			title = li[1]
			url = li[0]
			img = li[2]
			out.append((url,title.encode('utf-8'),img))

		return out

	def links(self,url):
		html = client.request(url)
		soup = webutils.bs(html)
		rows=soup.findAll('div',{'class':'row'})
		out=[]
		rows.pop(0)
		rows.pop(-1)
		for row in rows:
			item=row.find('div',{'class':'media-body'})
			url='http://radio.hrt.hr' + item.findAll('a')[1]['href']
			subtitle=item.find('small').getText().encode('utf-8').replace('Drugi program','').replace('Prvi program','').replace('Treći program','').lstrip('—').lstrip('\n')
			title=soup.find('h1',{'class':'page-title'}).getText().encode('utf-8')
			title = re.sub(u'Arhiva slušaonice - ','',title)
			title='%s (%s)'%(title.decode('utf-8'),subtitle.decode('utf-8'))

			out+=[[title.replace('\n',' ').replace('&mdash;',''),url,icon_path(info().icon)]]
		return out

	def resolve(self,url):
		html = client.request(url)
		soup = webutils.bs(html)
		resolved='http://radio.hrt.hr' + soup.find('a',{'class':'attachment-file'})['href']
		return(resolved)