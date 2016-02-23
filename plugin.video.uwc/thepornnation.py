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


def TPNMain(url):
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','http://thepornempire.com/',123,'','')
    utils.addDir('[COLOR hotpink]Search[/COLOR]','http://thepornempire.com/?s=',124,'','')
    utils.addDir('[COLOR hotpink]Movies[/COLOR]','http://thepornempire.com/category/movies/',125,'','')
    TPNList(url)
    xbmcplugin.endOfDirectory(utils.addon_handle)


def TPNMainMovies(url):
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','http://thepornempire.com/',126,'','')
    utils.addDir('[COLOR hotpink]Search[/COLOR]','http://thepornempire.com/?s=',124,'','')
    utils.addDir('[COLOR hotpink]Scenes[/COLOR]','http://thepornempire.com/category/videos/',120,'','')
    TPNList(url)
    xbmcplugin.endOfDirectory(utils.addon_handle)


def TPNList(url):
    listhtml = utils.getHtml(url, '')
    match = re.compile('class="item">.*?<a href="([^"]+)".*?img src="([^"]+)" alt="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videopage, img, name in match:
        name = utils.cleantext(name)
        utils.addDownLink(name, videopage, 122, img, '')
    try:
        nextp=re.compile('link rel="next" href="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
        next = nextp[0]
        utils.addDir('Next Page', os.path.split(url)[0] + '/' + next, 121,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)

    
def TPNSearch(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 124)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title
        print "Searching URL: " + searchUrl
        TPNSearchList(searchUrl)


def TPNSearchList(url):
    listhtml = utils.getHtml(url, '')
    match = re.compile('class="item">.*?<a href="([^"]+)".*?src="([^"]+)" alt="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videopage, img, name in match:
        name = utils.cleantext(name)
        utils.addDownLink(name, videopage, 122, img, '')
    try:
        nextp=re.compile('link rel="next" href="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
        next = nextp[0]
        utils.addDir('Next Page', next, 127,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)


def TPNCat(url, index):
    cathtml = utils.getHtml(url, '')
    match = re.compile('<ul class="scrolling cat(.*?)</ul>', re.DOTALL | re.IGNORECASE).findall(cathtml)
    match1 = re.compile('href="([^"]+)[^>]+>([^<]+)<', re.DOTALL | re.IGNORECASE).findall(match[index])
    for catpage, name in match1:
        utils.addDir(name, catpage, 121, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def TPNPlayvid(url, name, download=None):
    utils.PLAYVIDEO(url, name, download)