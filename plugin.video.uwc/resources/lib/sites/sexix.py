'''
    Ultimate Whitecream
    Copyright (C) 2016 Whitecream

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

import xbmcplugin
from resources.lib import utils
  

@utils.url_dispatcher.register('450')
def Main():
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','http://sexix.net/',453,'','')
    utils.addDir('[COLOR hotpink]Search[/COLOR]','http://sexix.net/?s=',454,'','')
    List('http://sexix.net/page/1/?orderby=date')
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('451', ['url'])
def List(url):
    try:
        listhtml = utils.getHtml(url, '')
    except:
        utils.notify('Oh oh','It looks like this website is down.')
        return None
    match = re.compile('<div id="main">(.*?)<div id="sidebar', re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
    match1 = re.compile(r'data-id="\d+" title="([^"]+)" href="([^"]+)".*?src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(match)
    for name, videopage, img in match1:
        name = utils.cleantext(name)
        utils.addDownLink(name, videopage, 452, img, '')
    try:
        nextp = re.compile('href="([^"]+)">Next', re.DOTALL | re.IGNORECASE).findall(match)
        utils.addDir('Next Page', nextp[0], 451,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('452', ['url', 'name'], ['download'])
def Playvid(url, name, download=None):
    videopage = utils.getHtml(url)
    plurl = re.compile('\?u=([^"]+)"', re.DOTALL | re.IGNORECASE).findall(videopage)[0]
    plurl = 'http://sexix.net/qaqqew/playlist.php?u=' + plurl
    plpage = utils.getHtml(plurl, url)
    videourl = re.compile('file="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(plpage)[0]
    if videourl:
        utils.playvid(videourl, name, download)
    else:
        utils.notify('Oh oh','Couldn\'t find a video')


@utils.url_dispatcher.register('453', ['url'])
def Categories(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('<a href="(http://sexix.net/videotag/[^"]+)"[^>]+>([^<]+)<', re.DOTALL | re.IGNORECASE).findall(cathtml)
    for catpage, name in match:
        utils.addDir(name, catpage, 451, '')    
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('454', ['url'], ['keyword'])
def Search(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 454)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title
        List(searchUrl)

