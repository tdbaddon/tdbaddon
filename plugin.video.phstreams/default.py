# -*- coding: utf-8 -*-

'''
    Phoenix Add-on
    Copyright (C) 2015 Blazetamer
    Copyright (C) 2015 lambda

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


import urlparse,sys
params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))


try:
    action = params['action']
except:
    action = None
try:
    name = params['name']
except:
    name = '0'
try:
    url = params['url']
except:
    url = '0'
try:
    playable = params['playable']
except:
    playable = '0'
try:
    content = params['content']
except:
    content = '0'
try:
    tvshow = params['tvshow']
except:
    tvshow = '0'
try:
    audio = params['audio']
except:
    audio = '0'
try:
    image = params['image']
except:
    image = '0'
try:
    fanart = params['fanart']
except:
    fanart = '0'




if action == None:
    from resources.lib.indexers import phstreams
    phstreams.getCategory()

elif action == 'dmode' or action == 'ndmode':
    from resources.lib.indexers import phstreams
    phstreams.getDirectory(name, url, audio, image, fanart, playable, content)

elif action == 'subDirectory':
    from resources.lib.indexers import phstreams
    phstreams.subDirectory(name, url, audio, image, fanart, playable, tvshow, content)

elif action == 'localDirectory':
    from resources.lib.indexers import phstreams
    phstreams.localDirectory()

elif action == 'search':
    from resources.lib.indexers import phstreams
    phstreams.getSearch()

elif action == 'searchDirectory':
    from resources.lib.indexers import phstreams
    phstreams.searchDirectory()

elif action == 'searchDirectory2':
    from resources.lib.indexers import phstreams
    phstreams.searchDirectory(url)

elif action == 'clearSearch':
    from resources.lib.indexers import phstreams
    phstreams.clearSearch()

elif action == 'resolveUrl':
    from resources.lib.indexers import phstreams
    phstreams.resolveUrl(name, url, audio, image, fanart, playable, content)

elif action == 'openDialog':
    from resources.lib.libraries import phdialogs
    phdialogs.openDialog(url,audio)

elif action == 'openSettings':
    from resources.lib.libraries import control
    control.openSettings()

elif action == 'addView':
    from resources.lib.libraries import views
    views.addView(content)

elif action == 'downloader':
    from resources.lib.libraries import downloader
    downloader.downloader()

elif action == 'addDownload':
    from resources.lib.libraries import downloader
    downloader.addDownload(name,url,image)

elif action == 'removeDownload':
    from resources.lib.libraries import downloader
    downloader.removeDownload(url)

elif action == 'startDownload':
    from resources.lib.libraries import downloader
    downloader.startDownload()

elif action == 'startDownloadThread':
    from resources.lib.libraries import downloader
    downloader.startDownloadThread()

elif action == 'stopDownload':
    from resources.lib.libraries import downloader
    downloader.stopDownload()

elif action == 'statusDownload':
    from resources.lib.libraries import downloader
    downloader.statusDownload()

elif action == 'trailer':
    from resources.lib.libraries import trailer
    trailer.trailer().play(name)

elif action == 'clearCache':
    from resources.lib.libraries import cache
    cache.clear()

elif action == 'radioDirectory':
    from resources.lib.indexers import phradios
    phradios.radioDirectory()

elif action == 'radioResolve':
    from resources.lib.indexers import phradios
    phradios.radioResolve(name, url, image)

elif action == 'radio1fm':
    from resources.lib.indexers import phradios
    phradios.radio1fm(image, fanart)

elif action == 'radio181fm':
    from resources.lib.indexers import phradios
    phradios.radio181fm(image, fanart)

elif action == 'radiotunes':
    from resources.lib.indexers import phradios
    phradios.radiotunes(image, fanart)

elif action == 'Kickinradio':
    from resources.lib.indexers import phradios
    phradios.Kickinradio(image, fanart)

elif action == 'Kickinradiocats':
    from resources.lib.indexers import phradios
    phradios.Kickinradiocats(url, image, fanart)

elif action == 'CartoonDirectory':
    from resources.lib.indexers import phtoons
    phtoons.CartoonDirectory()
   
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


