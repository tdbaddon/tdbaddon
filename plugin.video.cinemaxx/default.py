"""
	cinemaxx.ro Addon for KODI (formerly knows as XBMC)
	Copyright (C) 2012-2015 krysty
	https://github.com/yokrysty/krysty-xbmc

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import sys, os, re
import urllib, urllib2
import xbmcplugin, xbmcgui
from bs4 import BeautifulSoup
import json
import plugin, db
from resources.lib.ga import track

URL = {}
URL['base']			= 'http://www.cinemaxx.rs/'
URL['search']		= 'http://www.cinemaxx.rs/search.php?keywords='
URL['newMovies']	= 'http://www.cinemaxx.rs/newvideos.html'

HEADERS = {
	'User-Agent': 	 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Accept': 		 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Cache-Control': 'no-transform'
}

ICON = {
	'movie':	'moviesicon.png',
	'search':	'searchicon.png',
	'settings': 'settingsicon.png'
}

PLUGIN_PATH = plugin.getPluginPath()

for k, v in ICON.iteritems():
	ICON[k] = os.path.join(PLUGIN_PATH, 'resources', 'media', v)

print plugin.getPluginVersion()

DB = db.DB()

track(plugin.getPluginVersion())


def MAIN():
	addDir('Categorii', URL['base'], 1, ICON['movie'])
	addDir('Adaugate Recent', URL['newMovies'], 11, ICON['movie'])
	addDir('Cautare', URL['base'], 2, ICON['search'])
	#addDir('Setari', URL['base'], 98, ICON['settings'])
	#addDir('Golire Cache', URL['base'], 99)
	
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


def categories(url):
	progress = xbmcgui.DialogProgress()
	progress.create('Incarcare', 'Asteptati...')
	progress.update(1, "", "Incarcare lista - 1%", "")
	
	html = BeautifulSoup(http_req(url)).find('ul', {'id': 'ul_categories'}).find_all('a')
	
	total = len(html)
	current = 1
	
	for tag in html:
		addDir(tag.get_text(), tag.get('href'), 10, '')
		
		if progress.iscanceled(): sys.exit()
		
		percent = int((current * 100) / total)
		message = "Incarcare lista - " + str(percent) + "%"
		progress.update(percent, "", message, "")
		
		current += 1
		
	progress.close()
	
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


def getMovies(url, limit=False):
	progress = xbmcgui.DialogProgress()
	progress.create('Incarcare', 'Asteptati...')
	progress.update(1, "", "Incarcare lista - 1%", "")

	soup = BeautifulSoup(http_req(url))
	
	pages = soup.find('ul', {'class': 'pagination'})
	if pages and not limit:
		pages = pages.find_all('a')
		pages = max(int(x) for x in re.findall('([\d]+)', str(pages)))
		page = int(re.search('\d+', url).group(0))
	else:
		pages = 1
		page = 1
	
	tags = soup.find('ul', {'class': 'videolist'}).find_all('a')
	
	total = len(tags)
	current = 0
	
	while current <= total - 1:
		img = tags[current].select('img')[0]
		name = nameFilter(img.get('alt').encode('utf-8'))
		link = tags[current].get('href')
		thumbnail = img.get('src')
		
		addDir(name, link, 3, thumbnail)
		
		if progress.iscanceled(): sys.exit()
		
		percent = int(((current + 1) * 100) / total)
		message = "Incarcare lista - " + str(percent) + "%"
		progress.update(percent, "", message, "")
		
		current += 1
		
	if not page == pages:
		url = re.sub('\d+', str(page + 1), url)
		addDir("Pagina Urmatoare >>", url, 10)
	
	progress.close()
	
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

	
def search():
	kb = xbmc.Keyboard('', 'Search', False)
	
	lastSearch = None
	try:
		lastSearch = plugin.loadData('search')
		if lastSearch: kb.setDefault(lastSearch)
	except: pass
	
	kb.doModal()
	
	if (kb.isConfirmed()):
		inputText = kb.getText()
		
		try: plugin.saveData('search', inputText)
		except: pass
		
		if inputText == '':
			dialog = xbmcgui.Dialog().ok('Cautare', 'Nimic de cautat.')
			sys.exit()
		
		url = URL['search'] + urllib.quote_plus(inputText)
		tags = BeautifulSoup(http_req(url)).find('ul', {'class': 'videolist'}).find_all('a')
		
		current = 0
		while current <= len(tags) - 1 and not current == 10:
			img = tags[current].select('img')[0]
			name = nameFilter(img.get('alt').encode('utf-8'))
			link = tags[current].get('href')
			thumbnail = img.get('src')
			
			addDir(name, link, 3, thumbnail)
			
			current += 1
	
	else: sys.exit()
	
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


def http_req(url, getCookie=False, data=None, customHeader=None):
	if data: data = urllib.urlencode(data)
	req = urllib2.Request(url, data, HEADERS)
	if customHeader:
		req = urllib2.Request(url, data, customHeader)
	response = urllib2.urlopen(req)
	source = response.read()
	response.close()
	if getCookie:
		cookie = response.headers.get('Set-Cookie')
		return {'source': source, 'cookie': cookie}
	return source


def playStream(url,title,thumbnail):
	win = xbmcgui.Window(10000)
	win.setProperty('cinemaxx.playing.title', title.lower())
	
	item = xbmcgui.ListItem(title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail)
	item.setInfo(type = "Video", infoLabels = {"title": title})
	
	xbmc.Player().play(item=url, listitem=item)
	
	return True


def selectSource(url, title='', thumbnail=''):
	progress = xbmcgui.DialogProgress()
	progress.create('Incarcare', 'Asteptati...')
	progress.update(1, "", "Cautare surse video...", "")
	
	sources = getSources(url)
	
	progress.close()
	
	if not sources:
		return xbmcgui.Dialog().ok("", "Sursele video nu au fost gasite.")
	
	labels = []
	
	for item in sources:
		labels.append(item['name'])
	
	dialog = xbmcgui.Dialog()
	
	index = dialog.select('Selectati sursa video', labels)
	if index > -1:
		playStream(sources[index]['url'], title, thumbnail)
	else:
		return


def getSources(url):
	sources = []
	
	soup = BeautifulSoup(http_req(url))
	
	params = {}
	
	try:
		params['vid'] = re.search(r'_([0-9a-z]+).html?', url).group(1)
	except:
		html = soup.find_all('script', {'type': 'text/javascript'})
		html = "".join(line.strip() for line in str(html).split("\n"))
		html = re.findall(r'\$\.ajax\({.+?data: {(.+?)}', html)
		html = html[1].replace('"', '').split(',')
	
		for parameter in html:
			key, value = parameter.split(':')
			params[key] = value.strip()
	
	mirrors = []
	
	multiMirrors = soup.find('ul', {'id': 'menu-bar'})
	if multiMirrors: multiMirrors = multiMirrors.find_all('a')
	
	if(multiMirrors):
		for i in range(len(multiMirrors)):
			mirrors.append('%sajax.php?p=custom&do=requestmirror&vid=%s&mirror=%s' % (URL['base'], params['vid'], i+1))
	else:
		if(soup.find('iframe')):
			mirrors.append(url)
		else:
			mirrors.append('%sajax.php?p=video&do=getplayer&vid=%s' % (URL['base'], params['vid']))
	
	mirrors.reverse()
	
	for mirror in mirrors:
		try:
			if(mirror == url):
				mirrorUrl = soup.find('iframe').attrs['src']
			else:
				mirrorUrl = BeautifulSoup(http_req(mirror)).find('iframe').attrs['src']
			mirrorUrl = re.sub(r'https?:\/\/(?:www\.)?.+?\.li/?\??', '', mirrorUrl)
		except:
			mirrorUrl = ''
		
		if(re.search(r'mail.ru', mirrorUrl)):
			try:
				source = BeautifulSoup(http_req(mirrorUrl)).find_all('script', {'type': 'text/javascript'})
				jsonUrl = re.search(r'"metadataUrl":"(.+?)"', str(source)).group(1)
				req = http_req(jsonUrl, True)
				jsonSource = json.loads(req['source'])
				
				for source in jsonSource['videos']:
					name = '%s %s' % ('[mail.ru]', source['key'])
					link = '%s|Cookie=%s' % (source['url'], urllib.quote_plus(req['cookie']))
					item = {'name': name, 'url': link}
					sources.append(item)
			except: pass
		
		elif(re.search(r'vk.com', mirrorUrl)):
			try:
				from resources.lib.getvk import getVkVideos
				for source in getVkVideos(http_req(mirrorUrl)):
					item = {'name': source[0], 'url': source[1]}
					sources.append(item)
			except: pass
		
		elif(re.search(r'ok.ru', mirrorUrl)):
			try:
				id = re.search('\d+', mirrorUrl).group(0)
				jsonUrl = 'http://ok.ru/dk?cmd=videoPlayerMetadata&mid=' + id
				jsonSource = json.loads(http_req(jsonUrl))
				
				for source in jsonSource['videos']:
					name = '%s %s' % ('[ok.ru]', plugin.en2ro(source['name']))
					link = '%s|User-Agent=%s&Accept=%s&Referer=%s'
					link = link % (source['url'], HEADERS['User-Agent'], HEADERS['Accept'], urllib.quote_plus(URL['base']))
					
					item = {'name': name, 'url': link}
					sources.append(item)
			except: pass
	return sources


def nameFilter(name):
	return re.sub('F?f?ilme? ?-?|vizioneaza|online|subtitrat', '', name).strip()


def addDir(name, url, mode, thumbnail='', folder=True):
	ok = True
	params = {'name': name, 'mode': mode, 'url': url, 'thumbnail': thumbnail}

	liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
	
	if not folder:
		liz.setProperty('isPlayable', 'true')
		liz.setProperty('resumetime', str(0))
		liz.setProperty('totaltime', str(1))
		
	liz.setInfo(type="Video", infoLabels = {"title": name})

	ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = set_params(params), listitem = liz, isFolder = folder)
	return ok


def clearCache():
	if plugin.clearCache():
		xbmcgui.Dialog().ok('', 'Cache-ul a fost curatat.')
	else:
		xbmcgui.Dialog().ok('', 'Eroare. Incercati din nou.')


def set_params(dict):
	out = {}
	for key, value in dict.iteritems():
		if isinstance(value, unicode):
			value = value.encode('utf8')
		elif isinstance(value, str):
			value.decode('utf8')
		out[key] = value
	return sys.argv[0] + '?' + urllib.urlencode(out)
	
	
def get_params():
	param = {'default': 'none'}
	paramstring = sys.argv[2]
	if len(paramstring) >= 2:
			params = sys.argv[2]
			cleanedparams = params.replace('?','')
			if (params[len(params)-1] == '/'):
				params = params[0:len(params)-2]
			pairsofparams = cleanedparams.split('&')
			param = {}
			for i in range(len(pairsofparams)):
				splitparams = {}
				splitparams = pairsofparams[i].split('=')
				if (len(splitparams)) == 2:
					param[splitparams[0]] = splitparams[1]
	return param


params = get_params()

mode = int(params.get('mode', 0))
url = urllib.unquote_plus(params.get('url', ''))
name = urllib.unquote_plus(params.get('name', ''))
thumbnail = urllib.unquote_plus(params.get('thumbnail', ''))


if mode: print 'Mode: ' + str(mode)
if url: print 'URL: ' + str(url)


if mode == 0 or not url or len(url) < 1: MAIN()
elif mode == 1: categories(url)
elif mode == 2: search()
elif mode == 3: selectSource(url, name, thumbnail)
elif mode == 10: getMovies(url)
elif mode == 11: getMovies(url, True)
elif mode == 98: plugin.openSettings()
elif mode == 99: clearCache()
