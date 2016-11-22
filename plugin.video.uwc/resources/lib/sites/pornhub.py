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

import xbmc
import xbmcplugin
import xbmcgui
from resources.lib import utils

progress = utils.progress
  

@utils.url_dispatcher.register('390')
def Main():
    utils.addDir('[COLOR hotpink]Search[/COLOR]','http://www.pornhub.com/video/search?o=mr&search=', 394, '', '')
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','http://www.pornhub.com/categories?o=al', 393, '', '')
    List('http://www.pornhub.com/video?o=cm')
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('391', ['url'])
def List(url):
    print "pornhub::List " + url
    try:
        listhtml = utils.getHtml(url, '')
    except:
        utils.notify('Oh oh','It looks like this website is down.')
        return None
    match = re.compile('<li class="videoblock.+?<a href="([^"]+)" title="([^"]+)".+?<var class="duration">([^<]+)</var>(.*?)</div.*?data-mediumthumb="([^"]+)"', re.DOTALL).findall(listhtml)
    for videopage, name, duration, hd, img in match:
        if hd.find('HD') > 0:
            hd = " [COLOR orange]HD[/COLOR] "
        else:
            hd = " "            
        name = utils.cleantext(name)
        name = name + hd + "[COLOR deeppink]" + duration + "[/COLOR]"
        utils.addDownLink(name, 'http://www.pornhub.com' + videopage, 392, img, '')
    try:
        nextp=re.compile('<li class="page_next"><a href="(.+?)" class="orangeButton">Next</a></li>', re.DOTALL).findall(listhtml)
        utils.addDir('Next Page', 'http://www.pornhub.com' + nextp[0].replace('&amp;','&'), 391,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('394', ['url'], ['keyword'])    
def Search(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 394)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title
        print "Searching URL: " + searchUrl
        List(searchUrl)


@utils.url_dispatcher.register('393', ['url'])
def Categories(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile(r'<div class="category-wrapper">\s*?<a href="([^"]+)"\s*?alt="([^"]+)">\s*?<img src="([^"]+)"', re.DOTALL).findall(cathtml)
    for catpage, name, img in match:
        if '?' in catpage:
            utils.addDir(name, 'http://www.pornhub.com' + catpage + "&o=cm", 391, img, '')
        else:
            utils.addDir(name, 'http://www.pornhub.com' + catpage + "?o=cm", 391, img, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('392', ['url', 'name'], ['download'])    
def Playvid(url, name, download=None):
    html = utils.getHtml(url, '')
    match = re.compile(r"var player_quality_(\w+)p = '([^']+)'", re.DOTALL | re.IGNORECASE).findall(html)
    match = sorted(match, key=lambda x: int(x[0]), reverse=True)
    videourl = match[0][1]
    if download == 1:
        utils.downloadVideo(videourl, name)
    else:
        iconimage = xbmc.getInfoImage("ListItem.Thumb")
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})
        xbmc.Player().play(videourl, listitem)