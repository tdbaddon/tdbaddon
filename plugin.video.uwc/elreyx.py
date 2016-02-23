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

import urllib, urllib2, re, cookielib, os.path, sys, socket
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

import utils

progress = utils.progress

def EXMain():
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','http://elreyx.com/index1.html',113,'','')
    utils.addDir('[COLOR hotpink]Search[/COLOR]','http://elreyx.com/search-',114,'','')
    utils.addDir('[COLOR hotpink]Pornstars[/COLOR]','http://elreyx.com/index1.html',115,'','')
    utils.addDir('[COLOR hotpink]Movies[/COLOR]','http://elreyx.com/index1.html',116,'','')
    EXList('http://elreyx.com/index1.html')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def EXList(url):
    listhtml = utils.getHtml(url, '')
    match = re.compile('notice_image">.*?<a title="([^"]+)" href="([^"]+)".*?src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for name, videopage, img in match:
        utils.addDownLink(name, videopage, 112, img, '')
    try:
        nextp=re.compile("<a href='([^']+)' title='([^']+)'>&raquo;</a>", re.DOTALL | re.IGNORECASE).findall(listhtml)
        next = urllib.quote_plus(nextp[0][0])
        next = next.replace(' ','+')
        utils.addDir('Next Page', os.path.split(url)[0] + '/' + next, 111,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)

    
def EXSearch(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 114)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title + ".html"
        print "Searching URL: " + searchUrl
        EXList(searchUrl)


def EXCat(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('<div id="categories">(.*?)</div>', re.DOTALL | re.IGNORECASE).findall(cathtml)
    match1 = re.compile('href="([^"]+)[^>]+>([^<]+)<', re.DOTALL | re.IGNORECASE).findall(match[0])
    for catpage, name in match1:
        utils.addDir(name, catpage, 111, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)   


def EXPlayvid(url, name, download=None):
    utils.PLAYVIDEO(url, name, download)


def EXPornstars(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('<div id="pornstars">(.*?)</div>', re.DOTALL | re.IGNORECASE).findall(cathtml)
    match1 = re.compile('href="([^"]+)[^>]+>([^<]+)<', re.DOTALL | re.IGNORECASE).findall(match[0])
    for catpage, name in match1:
        utils.addDir(name, catpage, 111, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def EXMovies(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('<div id="movies">(.*?)</div>', re.DOTALL | re.IGNORECASE).findall(cathtml)
    match1 = re.compile('href="([^"]+)[^>]+>([^<]+)<', re.DOTALL | re.IGNORECASE).findall(match[0])
    for catpage, name in match1:
        utils.addDir(name, catpage, 117, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def EXMoviesList(url):
    listhtml = utils.getHtml(url, '')
    match = re.compile('<div class="container_news">(.*?)</div>', re.DOTALL | re.IGNORECASE).findall(listhtml)
    match1 = re.compile('<td.*?<a title="([^"]+)" href="([^"]+)".*?src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(match[0])
    for name, videopage, img in match1:
        utils.addDownLink(name, videopage, 112, img, '')
    try:
        nextp=re.compile("<a href='([^']+)' title='([^']+)'>&raquo;</a>", re.DOTALL | re.IGNORECASE).findall(listhtml)
        next = urllib.quote_plus(nextp[0][0])
        next = next.replace(' ','+')
        utils.addDir('Next Page', os.path.split(url)[0] + '/' + next, 117,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)
