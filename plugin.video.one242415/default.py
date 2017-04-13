# -*- coding: utf-8 -*-

'''
    One242415 Add-on

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

action = params.get('action')

content = params.get('content')

name = params.get('name')

url = params.get('url')

image = params.get('image')

fanart = params.get('fanart')


if action == None:
    from resources.lib.indexers import onestreams
    onestreams.indexer().root()

elif action == 'directory':
    from resources.lib.indexers import onestreams
    onestreams.indexer().get(url)

elif action == 'parental':
    from resources.lib.indexers import onestreams
    onestreams.indexer().parental_controls()

elif action == 'qdirectory':
    from resources.lib.indexers import onestreams
    onestreams.indexer().getq(url)

elif action == 'xdirectory':
    from resources.lib.indexers import onestreams
    onestreams.indexer().getx(url)

elif action == 'developer':
    from resources.lib.indexers import onestreams
    onestreams.indexer().developer()

elif action == 'tvtuner':
    from resources.lib.indexers import onestreams
    onestreams.indexer().tvtuner(url)

elif 'youtube' in str(action):
    from resources.lib.indexers import onestreams
    onestreams.indexer().youtube(url, action)

elif action == 'play':
    from resources.lib.indexers import onestreams
    onestreams.player().play(url, content)

elif action == 'browser':
    from resources.lib.indexers import onestreams
    onestreams.resolver().browser(url)

elif action == 'search':
    from resources.lib.indexers import onestreams
    onestreams.indexer().search()

elif action == 'addSearch':
    from resources.lib.indexers import onestreams
    onestreams.indexer().addSearch(url)

elif action == 'delSearch':
    from resources.lib.indexers import onestreams
    onestreams.indexer().delSearch()

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


