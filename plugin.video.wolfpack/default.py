import urlparse,sys,re
import urllib, urllib2
from urlparse import parse_qsl
import requests
import xml.etree.ElementTree as ET
import xbmcaddon, os



params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))

action = params.get('action')

content = params.get('content')

name = params.get('name')

url = params.get('url')

image = params.get('image')

fanart = params.get('fanart')

addonPath = xbmcaddon.Addon().getAddonInfo("path")


def getVersion():
	req = urllib.urlopen("https://gist.githubusercontent.com/djsuicide2k11/a6c861724c7ea3b1d478ced3a25d26eb/raw/").read()
	print "req.version = " + req 
	if req == None:
		return 0
	else:
		return int(req)

def update():
	from resources.lib.indexers import wolfpack
	print "wolfpack.version = " + str(wolfpack.version)
	print "gitwolfpack.version = " + str(getVersion())
	if wolfpack.version < getVersion():
		req = urllib.urlopen("https://gist.githubusercontent.com/djsuicide2k11/ca8b62447588070ecbc117ee939e2c29/raw/").read()
		print "code got, updating NOW"
		if req == None:
			print "Something went wrong!"
		else:
			print "wolfpackfile.path = " + os.path.join(addonPath, "resources", "lib", "indexers", "wolfpack.py")
			with open(os.path.join(addonPath, "resources", "lib", "indexers", "wolfpack.py"), "wb") as filewriter:
				filewriter.write(req)

update()
if action == None:
	from resources.lib.indexers import wolfpack
	wolfpack.indexer().root()

elif action == 'directory':
	from resources.lib.indexers import wolfpack
	wolfpack.indexer().get(url)

elif action == 'qdirectory':
	from resources.lib.indexers import wolfpack
	wolfpack.indexer().getq(url)

elif action == 'xdirectory':
	from resources.lib.indexers import wolfpack
	wolfpack.indexer().getx(url)

elif action == 'developer':
	from resources.lib.indexers import wolfpack
	wolfpack.indexer().developer()

elif action == 'tvtuner':
	from resources.lib.indexers import wolfpack
	wolfpack.indexer().tvtuner(url)

elif 'youtube' in str(action):
	from resources.lib.indexers import wolfpack
	wolfpack.indexer().youtube(url, action)

elif action == 'play':
	from resources.lib.indexers import wolfpack
	wolfpack.player().play(url, content)

elif action == 'browser':
	from resources.lib.indexers import wolfpack
	wolfpack.resolver().browser(url)

elif action == 'search':
	from resources.lib.indexers import wolfpack
	wolfpack.indexer().search()

elif action == 'addSearch':
	from resources.lib.indexers import wolfpack
	wolfpack.indexer().addSearch(url)

elif action == 'delSearch':
	from resources.lib.indexers import wolfpack
	wolfpack.indexer().delSearch()

elif action == 'queueItem':
	from resources.lib.modules import control
	control.queueItem()

elif action == 'openSettings':
	from resources.lib.modules import control
	control.openSettings()

elif action == 'urlresolverSettings':
	from resources.lib.modules import control
	control.openSettings(id='script.module.urlresolver')

elif action == 'addView':
	from resources.lib.modules import views
	views.addView(content)

elif action == 'downloader':
	from resources.lib.modules import downloader
	downloader.downloader()

elif action == 'addDownload':
	from resources.lib.modules import downloader
	downloader.addDownload(name,url,image)

elif action == 'removeDownload':
	from resources.lib.modules import downloader
	downloader.removeDownload(url)

elif action == 'startDownload':
	from resources.lib.modules import downloader
	downloader.startDownload()

elif action == 'startDownloadThread':
	from resources.lib.modules import downloader
	downloader.startDownloadThread()

elif action == 'stopDownload':
	from resources.lib.modules import downloader
	downloader.stopDownload()

elif action == 'statusDownload':
	from resources.lib.modules import downloader
	downloader.statusDownload()

elif action == 'trailer':
	from resources.lib.modules import trailer
	trailer.trailer().play(name)

elif action == 'clearCache':
	from resources.lib.modules import cache
	cache.clear()