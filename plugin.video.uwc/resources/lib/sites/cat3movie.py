'''
    Ultimate Whitecream
    Copyright (C) 2015 Whitecream
    Copyright (C) 2015 anton40

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

import re
import base64

import xbmcplugin
from resources.lib import utils

progress = utils.progress

    
@utils.url_dispatcher.register('350')
def Main():
    utils.addDir('[COLOR hotpink]Search[/COLOR]','http://cat3movie.us/?s=', 353, '', '')
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','http://cat3movie.us', 354, '', '')
    List('http://cat3movie.us/page/1')
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('351', ['url'])
def List(url):
    try:
        listhtml = utils.getHtml(url, '')
    except:
        utils.notify('Oh oh','It looks like this website is down.')
        return None
    match = re.compile("<main(.*?)</main", re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
    match1 = re.compile('<a class="" href="([^"]+)" title="([^"]+)">\n<img src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(match)
    for videopage, name, img in match1:
        name = utils.cleantext(name)
        utils.addDownLink(name, videopage, 352, img, '')
    try:
        nextp=re.compile(r'<span class="active">\d+</span></li><li><a href="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
        utils.addDir('Next Page', nextp[0], 351,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('353', ['url'], ['keyword'])    
def Search(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 353)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title
        print "Searching URL: " + searchUrl
        List(searchUrl)


@utils.url_dispatcher.register('354', ['url'])
def Categories(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('menu-item-object-category[^>]+><a href="([^"]+)">([^<]+)</a></li>').findall(cathtml)
    for catpage, name in match:
        utils.addDir(name, catpage, 351, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('352', ['url', 'name'], ['download'])
def Playvid(url, name, download=None):
    progress.create('Play video', 'Searching videofile.')
    progress.update( 10, "", "Loading video page", "" )
    html = utils.getHtml(url, '')
    embedLinks = re.compile('<a href="([^"]+)" rel="nofollow" target="_blank">').findall(html)
    url = ''
    for link in embedLinks:
        if 'embedlink' in link:
            try:
                html = utils.getHtml(link, '')
                if 'Base64' in html:
                    base64str = re.compile(r'Base64\.decode\("([^"]+)"').findall(html)
                    url = url + " " + base64.b64decode(base64str[0])
            except: pass
    utils.playvideo(url, name, download, url)