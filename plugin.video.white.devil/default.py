# -*- coding: utf-8 -*-

'''
    White Devil.Streams Add-on
    Copyright (C) 2016 Wwhite Devil Streams

    This program is free software: no need to steal our content
    you can send us as msg @ https://www.facebook.com/groups/102660050086738/
    and ask to use our content in your addon
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
    from resources.lib.indexers import streams
    streams.indexer().root()

elif action == 'directory':
    from resources.lib.indexers import streams
    streams.indexer().get(url)

elif action == 'developer':
    from resources.lib.indexers import streams
    streams.indexer().developer()

elif action == 'play':
    from resources.lib.indexers import streams
    streams.resolver().play(url)

elif action == 'browser':
    from resources.lib.indexers import streams
    streams.resolver().browser(url)

elif action == 'search':
    from resources.lib.indexers import streams
    streams.indexer().search()

elif action == 'addSearch':
    from resources.lib.indexers import streams
    streams.indexer().addSearch(url)

elif action == 'delSearch':
    from resources.lib.indexers import streams
    streams.indexer().delSearch()

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


	


