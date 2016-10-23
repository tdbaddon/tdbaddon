# -*- coding: utf-8 -*-

'''
    NHL Streams Add-on

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


import urlparse,sys,re,xbmcgui
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

	if xbmcgui.Dialog().yesno("NHL Streams","[COLOR blue][B]NHL Streams[/B][/COLOR] needs to modify your Hosts file","This is required for this Add-on to function.", "Select [COLOR red][B]Yes[/B][/COLOR] to Continue, or [COLOR red][B]No[/B][/COLOR] to Cancel"):

		try :
			xbmc.executebuiltin('RunScript(special://home/addons/plugin.video.nhlstreams/HOSTS.py)')
		except :
			pass
			
		from resources.lib.indexers import nhlstreams
		nhlstreams.indexer().root()	

elif action == 'directory':
    from resources.lib.indexers import nhlstreams
    nhlstreams.indexer().get(url)

elif action == 'xdirectory':
    from resources.lib.indexers import nhlstreams
    nhlstreams.indexer().getx(url)

elif action == 'developer':
    from resources.lib.indexers import nhlstreams
    nhlstreams.indexer().developer()

elif action == 'play':
    from resources.lib.indexers import nhlstreams
    nhlstreams.player().play(url, content)

elif action == 'regex':
    from resources.lib.indexers import nhlstreams
    nhlstreams.player().play(url, content, False)

elif action == 'browser':
    from resources.lib.indexers import nhlstreams
    nhlstreams.resolver().browser(url)

elif action == 'search':
    from resources.lib.indexers import nhlstreams
    nhlstreams.indexer().search()

elif action == 'addSearch':
    from resources.lib.indexers import nhlstreams
    nhlstreams.indexer().addSearch(url)

elif action == 'delSearch':
    from resources.lib.indexers import nhlstreams
    nhlstreams.indexer().delSearch()

elif action == 'openSettings':
    from resources.lib.modules import control
    control.openSettings()

elif action == 'clearCache':
    from resources.lib.modules import cache
    cache.clear()
