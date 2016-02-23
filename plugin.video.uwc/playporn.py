'''
    Ultimate Whitecream
    Copyright (C) 2015 mortael
    Copyright (C) 2015 Fr33m1nd

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

import urllib, re
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

import utils

progress = utils.progress

def Main():
    utils.addDir('[COLOR hotpink]Search[/COLOR]','http://playporn.to/?submit=Search&s=', 234, '', '')
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','http://playporn.to/', 235, '', '')
    utils.addDir('[COLOR hotpink]Movies[/COLOR]','http://playporn.to/category/xxx-movie-stream/', 231, '', '')
    List('http://playporn.to/category/xxx-clips-scenes-stream/')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def MainMovies():
    utils.addDir('[COLOR hotpink]Search[/COLOR]','http://playporn.to/?submit=Search&s=', 234, '', '')
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','http://playporn.to/', 236, '', '')
    utils.addDir('[COLOR hotpink]Scenes[/COLOR]','http://playporn.to/category/xxx-clips-scenes-stream/', 230, '', '')
    List('http://playporn.to/category/xxx-movie-stream/')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def List(url):
    listhtml = utils.getHtml(url, '')
    match = re.compile('<div class="photo-thumb-image.*?href="([^"]+)".*?title="([^"]+)".*?src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videopage, name, img in match:
        name = utils.cleantext(name)
        utils.addDownLink(name, videopage, 233, img, '')
    try:
        nextp=re.compile('<a class="nextpostslink" rel="next" href="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
        nextp = nextp[0].replace("&#038;", "&")
        utils.addDir('Next Page', nextp, 232,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)

    
def Search(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 234)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title
        print "Searching URL: " + searchUrl
        List(searchUrl)


def Categories(url, index=0):
    cathtml = utils.getHtml(url, '')
    match = re.compile("<ul class='children'>(.*?)</ul>", re.DOTALL | re.IGNORECASE).findall(cathtml)
    match1 = re.compile('href="([^"]+)[^>]+>([^<]+)<', re.DOTALL | re.IGNORECASE).findall(match[index])
    for catpage, name in match1:
        utils.addDir(name, catpage, 232, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def Playvid(url, name, download=None):
    utils.PLAYVIDEO(url, name, download)