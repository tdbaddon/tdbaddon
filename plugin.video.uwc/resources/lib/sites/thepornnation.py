'''
    Ultimate Whitecream
    Copyright (C) 2015 Whitecream
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

import re
import os.path

import xbmcplugin
from resources.lib import utils

progress = utils.progress


@utils.url_dispatcher.register('120', ['url'])
def TPNMain(url):
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','http://thepornempire.com/',123,'',1)
    utils.addDir('[COLOR hotpink]Search[/COLOR]','http://thepornempire.com/?s=',124,'','')
    utils.addDir('[COLOR hotpink]Movies[/COLOR]','http://thepornempire.com/category/movies/',125,'','')
    TPNList(url)
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('125', ['url'])
def TPNMainMovies(url):
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','http://thepornempire.com/',126,'',0)
    utils.addDir('[COLOR hotpink]Search[/COLOR]','http://thepornempire.com/?s=',124,'','')
    utils.addDir('[COLOR hotpink]Scenes[/COLOR]','http://thepornempire.com/category/videos/',120,'','')
    TPNList(url)
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('121', ['url'])
def TPNList(url):
    try:
        listhtml = utils.getHtml(url, '')
    except:
        utils.notify('Oh oh','It looks like this website is down.')
        return None
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


@utils.url_dispatcher.register('124', ['url'], ['keyword'])     
def TPNSearch(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 124)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title
        print "Searching URL: " + searchUrl
        TPNSearchList(searchUrl)


@utils.url_dispatcher.register('127', ['url'])
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


@utils.url_dispatcher.register('123', ['url', 'page'])
@utils.url_dispatcher.register('126', ['url', 'page'])
def TPNCat(url, index):
    cathtml = utils.getHtml(url, '')
    match = re.compile('<ul class="scrolling cat(.*?)</ul>', re.DOTALL | re.IGNORECASE).findall(cathtml)
    match1 = re.compile('href="([^"]+)[^>]+>([^<]+)<', re.DOTALL | re.IGNORECASE).findall(match[index])
    for catpage, name in match1:
        utils.addDir(name, catpage, 121, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('122', ['url', 'name'], ['download'])
def TPNPlayvid(url, name, download=None):
    utils.PLAYVIDEO(url, name, download)