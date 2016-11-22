'''
    Ultimate Whitecream
    Copyright (C) 2016 Whitecream, hdgdl
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

import urllib2
import os
import re
import sys

import xbmc
import xbmcplugin
import xbmcgui
from resources.lib import utils

cookie = {'Cookie': 'lang=en; search_video=%7B%22sort%22%3A%22da%22%2C%22duration%22%3A%22%22%2C%22channels%22%3A%22%3B0.1.2%22%2C%22quality%22%3A0%2C%22date%22%3A%22%22%7D;'}

@utils.url_dispatcher.register('505')
def Main():
    utils.addDir('[COLOR hotpink]Categories - Straight[/COLOR]','https://xhamster.com/channels.php',508,'','')
    utils.addDir('[COLOR hotpink]Categories - Gay[/COLOR]','https://xhamster.com/channels-gay',508,'','')
    utils.addDir('[COLOR hotpink]Categories - Shemale[/COLOR]','https://xhamster.com/channels-shemale',508,'','')
    utils.addDir('[COLOR hotpink]Search[/COLOR]','https://xhamster.com/search.php?q=',509,'','')
    List('https://xhamster.com/last50.php')
    xbmcplugin.endOfDirectory(utils.addon_handle)

	
@utils.url_dispatcher.register('506', ['url'])
def List(url):
    try:
        response = utils.getHtml(url, '', cookie)
    except:
        utils.notify('Oh oh','It looks like this website is down.')
        return None
    match = re.compile(r'<a href="([^"]+)[^>]+hRotator[^\']+\'([^\']+)[^"]+"([^"]+)[^<]+[^>]+><b>([0-9:]+)<', re.DOTALL | re.IGNORECASE).findall(response)
    for video, img, name, runtime in match:
        name = runtime + " - " + utils.cleantext(name)
        utils.addDownLink(name, video, 507, img, '', noDownload=True)
    currentpage = re.compile("class='pager'.*<span>([0-9]+)</span><a", re.DOTALL | re.IGNORECASE).findall(response)
    if currentpage:
       npage = int(currentpage[0]) + 1
       if ".html" in url: 
           next = url.replace('-'+str(currentpage[0])+'.html','-'+str(npage)+'.html') ##normal page
       else:
           if "page=" not in url:
               url = url + "&page=" + str(currentpage[0])
           next = url.replace('page='+str(currentpage[0]),'page='+str(npage)) ##search page
       utils.addDir('Next Page ('+str(npage)+')', next, 506, '', npage)
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('507', ['url', 'name'])
def Playvid(url, name):
    response = utils.getHtml(url)
    match = re.compile("file: '(http[^']+)", re.DOTALL | re.IGNORECASE).findall(response)
    if match:
       videourl = match[0]
       iconimage = xbmc.getInfoImage("ListItem.Thumb")
       listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
       listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})
       listitem.setProperty("IsPlayable","true")
       if int(sys.argv[1]) == -1:
         pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
         pl.clear()
         pl.add(videourl, listitem)
         xbmc.Player().play(pl)
       else:
         listitem.setPath(str(videourl))
         xbmcplugin.setResolvedUrl(utils.addon_handle, True, listitem)

@utils.url_dispatcher.register('508', ['url'])
def Categories(url):
    cathtml = utils.getHtml(url, '', cookie)
    match = re.compile('<a  href="(.+?)">([^<]+)<').findall(cathtml)
    for url, name in match[0:]:
        utils.addDir(name, url, 506, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)
    
@utils.url_dispatcher.register('509', ['url'], ['keyword'])
def Search(url, keyword=None):
    searchUrl = url
    xbmc.log("Search: " + searchUrl)
    if not keyword:
        utils.searchDir(url, 509)
    else:
        title = keyword.replace(' ','_')
        searchUrl = searchUrl + title
        xbmc.log("Search: " + searchUrl)
        List(searchUrl)