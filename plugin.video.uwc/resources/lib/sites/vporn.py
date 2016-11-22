'''
    Ultimate Whitecream
    Copyright (C) 2015 Whitecream

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

import xbmc
import xbmcplugin
import xbmcgui
from resources.lib import utils

@utils.url_dispatcher.register('500')
def Main():
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','https://www.vporn.com/newest/',503,'','')
    utils.addDir('[COLOR hotpink]Search[/COLOR]','https://www.vporn.com/search?q=',504,'','')
    List('https://www.vporn.com/newest/')
    xbmcplugin.endOfDirectory(utils.addon_handle)

@utils.url_dispatcher.register('501', ['url'])
def List(url):
    xbmc.log("List: " + url)
    try:
        listhtml = utils.getHtml(url, '')
    except:
        utils.notify('Oh oh','It looks like this website is down.')
        return None
    match = re.compile(r'<a href="(.+?)" class="thumb"><img src="(.+?)" alt="(.+?)"').findall(listhtml)
    for videopage, img, name in match:
        name = utils.cleantext(name)
        utils.addDownLink(name, videopage, 502, img, '')
    try:
        nextp = re.compile('<a class="next" href="(.+?)">').findall(listhtml)
        utils.addDir('Next Page', url[:url.rfind('/')+1] + nextp[0], 501,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)

@utils.url_dispatcher.register('502', ['url', 'name'], ['download'])
def Playvid(url, name, download=None):
    if download == 1:
        utils.downloadVideo(url, name)
    else:
        page = utils.getHtml(url, '')
        match = re.compile(r'videoUrlMedium = "(.+?)"', re.DOTALL | re.IGNORECASE).findall(page)
        iconimage = xbmc.getInfoImage("ListItem.Thumb")
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})
        xbmc.Player().play(match[0], listitem)

@utils.url_dispatcher.register('503')
def Categories():
    cathtml = utils.getHtml('https://www.vporn.com/', '')
    match = re.compile('<li><a href="/cat/(.+?)"><img .*>(.+?)</a></li>').findall(cathtml)
    for catid, name in match[1:]:
        catpage = "https://www.vporn.com/cat/"+ catid
        utils.addDir(name, catpage, 501, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)
    
@utils.url_dispatcher.register('504', ['url'], ['keyword'])
def Search(url, keyword=None):
    searchUrl = url
    xbmc.log("Search: " + searchUrl)
    if not keyword:
        utils.searchDir(url, 504)
    else:
        title = keyword.replace(' ','_')
        searchUrl = searchUrl + title
        xbmc.log("Search: " + searchUrl)
        List(searchUrl)
