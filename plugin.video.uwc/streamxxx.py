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
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','http://streamxxx.tv/', 177, '', '')
    utils.addDir('[COLOR hotpink]Tags[/COLOR]','http://streamxxx.tv/', 173, '', '')
    utils.addDir('[COLOR hotpink]Search Overall[/COLOR]','http://streamxxx.tv/?s=', 174, '', '')
    utils.addDir('[COLOR hotpink]Search Scenes[/COLOR]','http://streamxxx.tv/?cat=2210&s=', 174, '', '')
    utils.addDir('[COLOR hotpink]Movies[/COLOR]','http://streamxxx.tv/category/movies-xxx/', 175, '', '')
    utils.addDir('[COLOR hotpink]International Movies[/COLOR]','http://streamxxx.tv/category/movies-xxx/international-movies/', 176, '', '')
    List('http://streamxxx.tv/category/clips/')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def MainMovies():
    utils.addDir('[COLOR hotpink]Tags[/COLOR]','http://streamxxx.tv/', 173, '', '')
    utils.addDir('[COLOR hotpink]Search Overall[/COLOR]','http://streamxxx.tv/&s=', 174, '', '')
    utils.addDir('[COLOR hotpink]Search Movies[/COLOR]','http://streamxxx.tv/?cat=2207&s=', 174, '', '')
    utils.addDir('[COLOR hotpink]International Movies[/COLOR]','http://streamxxx.tv/category/movies-xxx/international-movies/', 176, '', '')
    utils.addDir('[COLOR hotpink]Scenes[/COLOR]','http://streamxxx.tv/category/clips/', 170, '', '')
    List('http://streamxxx.tv/category/movies-xxx/')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def MainInternationalMovies():
    utils.addDir('[COLOR hotpink]Tags[/COLOR]','http://streamxxx.tv/', 173, '', '')
    utils.addDir('[COLOR hotpink]Search Overall[/COLOR]','http://streamxxx.tv/?s=', 174, '', '')
    utils.addDir('[COLOR hotpink]Search International Movies[/COLOR]','http://streamxxx.tv/?cat=9&s=', 174, '', '')
    utils.addDir('[COLOR hotpink]Movies[/COLOR]','http://streamxxx.tv/category/movies/', 175, '', '')
    utils.addDir('[COLOR hotpink]Scenes[/COLOR]','http://streamxxx.tv/category/clips/', 170, '', '')
    List('http://streamxxx.tv/category/movies/international-movies/')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def List(url):
    listhtml = utils.getHtml(url, '')
    match = re.compile('<div id="post-.*?<div class="thumb">.*?href="([^"]+)".*?src="([^"]+)".*?alt="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videopage, img, name in match:
        name = utils.cleantext(name)
        utils.addDownLink(name, videopage, 172, img, '')
    try:
        nextp=re.compile('<a class="nextpostslink" rel="next" href="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
        nextp = nextp[0].replace("&#038;", "&")
        utils.addDir('Next Page', nextp, 171,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)

    
def Search(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 174)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title
        print "Searching URL: " + searchUrl
        List(searchUrl)


def Categories(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('Clips</a>.+<ul class="sub-menu">(.*?)</ul>', re.DOTALL | re.IGNORECASE).findall(cathtml)
    match1 = re.compile('href="([^"]+)[^>]+>([^<]+)<', re.DOTALL | re.IGNORECASE).findall(match[0])
    for catpage, name in match1:
        utils.addDir(name, catpage, 171, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def Tags(url):
    html = utils.getHtml(url, '')
    match = re.compile('<div class="tagcloud">(.*?)</div>', re.DOTALL | re.IGNORECASE).findall(html)
    match1 = re.compile("href='([^']+)[^>]+>([^<]+)<", re.DOTALL | re.IGNORECASE).findall(match[0])
    for catpage, name in match1:
        utils.addDir(name, catpage, 171, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def Playvid(url, name, download=None):
    utils.PLAYVIDEO(url, name, download)
