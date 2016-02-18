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


import urlparse,sys,re
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
    phstreams.getDirectory(name, url, audio, image, fanart, content)

elif action == 'subDirectory':
    from resources.lib.indexers import phstreams
    phstreams.subDirectory(name, url, audio, image, fanart, tvshow, content)

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
    phstreams.resolveUrl(url)

elif action == 'openDialog':
    from resources.lib.modules import phdialogs
    phdialogs.openDialog(url,audio)

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

elif ('HH') in action:
    from resources.lib.modules import control
    mediaPath = control.addonInfo('path') + '/resources/lib/indexers/phhuddle.py'
    print action
    file = open(mediaPath, 'r')
    getter = file.read()
    file.close()
    list = re.findall('(HH.+?\(url\))', getter)
    for item in list:
        test = 'phhuddle.'+ item
        if item[:-5] == action:
            from resources.lib.indexers import phhuddle
            exec test       

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

elif action == 'AnimeCrazy':
    from resources.lib.indexers import phtoons
    phtoons.AnimeCrazy(image, fanart)

elif action == 'ACsearch':
    from resources.lib.indexers import phtoons
    phtoons.ACsearch(url, image, fanart)

elif action == 'ACcat':
    from resources.lib.indexers import phtoons
    phtoons.ACcat(url, image, fanart)

elif action == 'ACpart':
    from resources.lib.indexers import phtoons
    phtoons.ACpart(url, image, fanart)

elif action == 'ACstream':
    from resources.lib.indexers import phtoons
    phtoons.ACstream(url)

elif action == 'HuddleDirectory':
    from resources.lib.indexers import phhuddle
    phhuddle.HuddleDirectory()

elif action == 'Huddle_Main':
    from resources.lib.indexers import phhuddle
    phhuddle.Huddle_Main(url, image, fanart)

elif action == 'Archive_Main':
    from resources.lib.indexers import phhuddle
    phhuddle.Archive_Main(url, image, fanart)

elif action == 'Play_Main':
    from resources.lib.indexers import phhuddle
    phhuddle.Play_Main(url)

elif action == 'NBANFL_ARC':
    from resources.lib.indexers import phhuddle
    phhuddle.NBANFL_ARC(url, image, fanart)

elif action == 'NHL_ARC':
    from resources.lib.indexers import phhuddle
    phhuddle.NHL_ARC(url, image, fanart)

elif action == 'Huddle_Sites':
    from resources.lib.indexers import phhuddle
    phhuddle.Huddle_Sites(url, image, fanart)

elif action == 'NBANFL_Stream':
    from resources.lib.indexers import phhuddle
    phhuddle.NBANFL_Stream(url, image, fanart)

elif action == 'NHL_Stream':
    from resources.lib.indexers import phhuddle
    phhuddle.NHL_Stream(url)
    
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


