'''
    Ultimate Whitecream
    Copyright (C) 2016 mortael

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


def Main():
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','http://czechhd.net/',313,'','')
    utils.addDir('[COLOR hotpink]Search[/COLOR]','http://czechhd.net/?s=',314,'','')
    List('http://czechhd.net/page/1/?orderby=date')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def List(url):
    listhtml = utils.getHtml(url, '')
    match = re.compile('<div id="main">(.*?)<div id="sidebar', re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
    match1 = re.compile(r'data-id="\d+" title="([^"]+)" href="([^"]+)".*?src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(match)
    for name, videopage, img in match1:
        name = utils.cleantext(name)
        utils.addDownLink(name, videopage, 312, img, '')
    try:
        nextp = re.compile('href="([^"]+)" >Next', re.DOTALL | re.IGNORECASE).findall(match)
        utils.addDir('Next Page', nextp[0], 311,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)


def Playvid(url, name, download):
    utils.PLAYVIDEO(url, name, download)


def Categories(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('<a href="(http://czechhd.net/category/[^"]+)" >([^<]+)<', re.DOTALL | re.IGNORECASE).findall(cathtml)
    for catpage, name in match:
        utils.addDir(name, catpage, 311, '')    
    xbmcplugin.endOfDirectory(utils.addon_handle)


def Search(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 314)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title
        List(searchUrl)

