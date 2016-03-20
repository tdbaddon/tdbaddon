# -*- coding: utf-8 -*-

'''
    Phoenix Add-on
    Copyright (C) 2016 Phoenix

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import urlparse,sys,re
params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))


try:
    action = params['action']
except:
    action = None
try:
    content = params['content']
except:
    content = None
try:
    name = params['name']
except:
    name = None
try:
    url = params['url']
except:
    url = None
try:
    image = params['image']
except:
    image = None
try:
    fanart = params['fanart']
except:
    fanart = None



if action == None:
    from resources.lib.indexers import phstreams
    phstreams.indexer().root()

elif action == 'directory':
    from resources.lib.indexers import phstreams
    phstreams.indexer().get(url)

elif action == 'developer':
    from resources.lib.indexers import phstreams
    phstreams.indexer().developer()

elif action == 'play':
    from resources.lib.indexers import phstreams
    phstreams.resolver().play(url)

elif action == 'browser':
    from resources.lib.indexers import phstreams
    phstreams.resolver().browser(url)

elif action == 'search':
    from resources.lib.indexers import phstreams
    phstreams.indexer().search()

elif action == 'addSearch':
    from resources.lib.indexers import phstreams
    phstreams.indexer().addSearch(url)

elif action == 'delSearch':
    from resources.lib.indexers import phstreams
    phstreams.indexer().delSearch()

elif action == 'openSettings':
    from resources.lib.modules import control
    control.openSettings()

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

elif action == 'radios':
    from resources.lib.indexers import phradios
    phradios.radios()

elif action == 'radioResolve':
    from resources.lib.indexers import phradios
    phradios.radioResolve(url)

elif action == 'radio1fm':
    from resources.lib.indexers import phradios
    phradios.radio1fm()

elif action == 'radio181fm':
    from resources.lib.indexers import phradios
    phradios.radio181fm()

elif action == 'radiocast':
    from resources.lib.indexers import phradios
    phradios.kickinradio()

elif action == 'kickinradiocats':
    from resources.lib.indexers import phradios
    phradios.kickinradiocats(url)

elif action == 'cartoon':
    from resources.lib.indexers import phtoons
    phtoons.cartoon()
   
elif action == 'CartoonCrazy':
    from resources.lib.indexers import phtoons
    phtoons.CartoonCrazy(image, fanart)

elif action == 'CCsearch':
    from resources.lib.indexers import phtoons
    phtoons.CCsearch(url, image, fanart)

elif action == 'CCcat':
    from resources.lib.indexers import phtoons
    phtoons.CCcat(url, image, fanart)

elif action == 'CCpart':
    from resources.lib.indexers import phtoons
    phtoons.CCpart(url, image, fanart)

elif action == 'CCstream':
    from resources.lib.indexers import phtoons
    phtoons.CCstream(url)

elif action == 'AnimeCrazy':
    from resources.lib.indexers import phtoons
    phtoons.AnimeCrazy(image, fanart)

elif action == 'ACsearch':
    from resources.lib.indexers import phtoons
    phtoons.ACsearch(url, image, fanart)

elif action == 'AClast':
    from resources.lib.indexers import phtoons
    phtoons.AClast(url, image, fanart)

elif action == 'ACcat':
    from resources.lib.indexers import phtoons
    phtoons.ACcat(url, image, fanart)

elif action == 'ACpart':
    from resources.lib.indexers import phtoons
    phtoons.ACpart(url, image, fanart)

elif action == 'ACstream':
    from resources.lib.indexers import phtoons
    phtoons.ACstream(url)

elif action == 'nhlDirectory':
    from resources.lib.indexers import nhlcom
    nhlcom.nhlDirectory()
        
elif action == 'nhlScoreboard':
    from resources.lib.indexers import nhlcom
    nhlcom.nhlScoreboard()

elif action == 'nhlArchives':
    from resources.lib.indexers import nhlcom
    nhlcom.nhlArchives()

elif action == 'nhlStreams':
    from resources.lib.indexers import nhlcom
    nhlcom.nhlStreams(name,url)

elif action == 'nhlResolve':
    from resources.lib.indexers import nhlcom
    nhlcom.nhlResolve(url)


