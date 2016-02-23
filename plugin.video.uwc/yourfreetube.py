'''
    Ultimate Whitecream
    Copyright (C) 2015 mortael

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

def YFTMain():
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','http://www.yourfreetube.net/index.html',193,'','')
    utils.addDir('[COLOR hotpink]Search[/COLOR]','http://www.yourfreetube.net/search.php?keywords=',194,'','')
    YFTList('http://www.yourfreetube.net/newvideos.html')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def YFTList(url):
    listhtml = utils.getHtml(url, '')
    match = re.compile('<a href="([^"]+)"[^<]+<[^<]+<img src="([^"]+)" alt="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videopage, img, name in match:
        name = utils.cleantext(name)
        utils.addDownLink(name, videopage, 192, img, '')
    try:
        nextp=re.compile('<a href="([^"]+)">&raquo;', re.DOTALL | re.IGNORECASE).findall(listhtml)
        nextp = "http://www.yourfreetube.net/" + nextp[0]
        utils.addDir('Next Page', nextp, 191,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)

    
def YFTSearch(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 194)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title
        print "Searching URL: " + searchUrl
        YFTList(searchUrl)


def YFTCat(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('<ul class="pm-browse-ul-subcats">(.*?)</ul>', re.DOTALL | re.IGNORECASE).findall(cathtml)
    match1 = re.compile('<a href="([^"]+)" class="">([^<]+)<', re.DOTALL | re.IGNORECASE).findall(match[0])
    for catpage, name in match1:
        utils.addDir(name, catpage, 191, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)   


def YFTPlayvid(url, name, download=None):
    utils.PLAYVIDEO(url, name, download)

