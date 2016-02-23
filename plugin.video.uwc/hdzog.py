'''
    Ultimate Whitecream
    Copyright (C) 2015 mortael
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

import urllib, urllib2, re, cookielib, os.path, sys, socket
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

import utils

progress = utils.progress

def Main():
    utils.addDir('[COLOR hotpink]Search[/COLOR]','http://www.hdzog.com/search/?q=', 343, '', '')
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','http://www.hdzog.com/categories/', 344, '', '')
    utils.addDir('[COLOR hotpink]Channels[/COLOR]','http://www.hdzog.com/channels/', 345, '', '')
    utils.addDir('[COLOR hotpink]Models[/COLOR]','http://www.hdzog.com/models/', 346, '', '')
    List('http://www.hdzog.com/new/')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def List(url):
    listhtml = utils.getHtml(url, '')
    match = re.compile('<li>\n.+?<a href="(.+?)" title="(.+?)">\n.+?<div class="thumb thumb-paged" data-screen-main="1">\n\n.+?<img src="(.+?)"').findall(listhtml)
    for videopage, name, img in match:
        name = utils.cleantext(name)
        utils.addDownLink(name, videopage, 342, img, '')
    try:
        nextp=re.compile('<a href="(.+?)" title="Next Page" data-page-num.+?>Next page').findall(listhtml)
        utils.addDir('Next Page', 'http://www.hdzog.com' + nextp[0], 341,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)

    
def Search(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 343)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title
        print "Searching URL: " + searchUrl
        List(searchUrl)


def Categories(url):
    listhtml = utils.getHtml(url, '')
    match = re.compile('<a href="(.+?)" title=".+?">\n.+?<div class="thumb">\n.+?<img class="thumb" src="(.+?)" alt="(.+?)"/>').findall(listhtml)
    for catpage, img, name in match:
        name = utils.cleantext(name)
        utils.addDir(name, catpage, 341, img, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def Channels(url):
    listhtml = utils.getHtml(url, '')
    match = re.compile('<a href="(.+?)" title=".+?">.+?<div class="thumb">.+?<img src="(.+?)" alt="(.+?)" />', re.DOTALL).findall(listhtml)
    for catpage, img, name in match:
        name = utils.cleantext(name)
        utils.addDir(name, catpage, 341, img, '')
    try:
        nextp=re.compile('<a href="(.+?)" title="Next Page" data-page-num.+?>Next page').findall(listhtml)
        print "next: ", 'http://www.hdzog.com' + nextp[0]
        utils.addDir('Next Page', 'http://www.hdzog.com' + nextp[0], 345,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)

def Models(url):
    listhtml = utils.getHtml(url, '')
    match = re.compile('<a href="(.+?)" title="(.+?)">\n.+?<div class="thumb">\n.+?<img src="(.+?)"').findall(listhtml)
    for catpage, name, img in match:
        name = utils.cleantext(name)
        utils.addDir(name, catpage, 341, img, '')
    try:
        nextp=re.compile('<a href="(.+?)" title="Next Page" data-page-num.+?>Next page').findall(listhtml)
        print "next: ", 'http://www.hdzog.com' + nextp[0]
        utils.addDir('Next Page', 'http://www.hdzog.com' + nextp[0], 346,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)


def Playvid(url, name, download=None):
    videopage = utils.getHtml(url, '')
    videourl = re.compile("video_url: '(.+?)\/\?br", re.DOTALL | re.IGNORECASE).findall(videopage)
    videourl = videourl[0]
    if download == 1:
        utils.downloadVideo(videourl, name)
    else:    
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