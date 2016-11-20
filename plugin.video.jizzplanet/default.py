# -*- coding: utf-8 -*-

'''
    Jizz Planet Add-on

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
    from resources.lib.indexers import jizzplanet
    jizzplanet.indexer().root()

elif action == 'directory':
    from resources.lib.indexers import jizzplanet
    jizzplanet.indexer().get(url)

elif action == 'xdirectory':
    from resources.lib.indexers import jizzplanet
    jizzplanet.indexer().getx(url)

elif action == 'developer':
    from resources.lib.indexers import jizzplanet
    jizzplanet.indexer().developer()

elif action == 'play':
    from resources.lib.indexers import jizzplanet
    jizzplanet.player().play(url, content)

elif action == 'regex':
    from resources.lib.indexers import jizzplanet
    jizzplanet.player().play(url, content, False)

elif action == 'browser':
    from resources.lib.indexers import jizzplanet
    jizzplanet.resolver().browser(url)

elif action == 'search':
    from resources.lib.indexers import jizzplanet
    jizzplanet.indexer().search()

elif action == 'addSearch':
    from resources.lib.indexers import jizzplanet
    jizzplanet.indexer().addSearch(url)

elif action == 'delSearch':
    from resources.lib.indexers import jizzplanet
    jizzplanet.indexer().delSearch()

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
