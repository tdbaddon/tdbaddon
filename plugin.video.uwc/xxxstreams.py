'''
    Ultimate Whitecream
    Copyright (C) 2016 mortael
    Copyright (C) 2016 anton40

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
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','http://xxxstreams.eu/',413,'','')
    utils.addDir('[COLOR hotpink]Search[/COLOR]','http://xxxstreams.eu/?s=',414,'','')
    List('http://xxxstreams.eu/page/1')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def List(url):
    html = utils.getHtml(url, '')
    match = re.compile(r'data-id="\d+" title="([^"]+)" href="([^"]+)".*?src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(html)
    for name, videopage, img in match:
        name = utils.cleantext(name)
        utils.addDownLink(name, videopage, 412, img, '')
    try:
        nextp = re.compile('<a class="nextpostslink" rel="next" href="(.+?)">', re.DOTALL | re.IGNORECASE).findall(html)
        utils.addDir('Next Page', nextp[0], 411,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)


def Playvid(url, name, download):
    utils.PLAYVIDEO(url, name, download)


def Categories(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('<li.+?class=".+?menu-item-object-post_tag.+?"><a href="(.+?)">(.+?)</a></li>').findall(cathtml)
    for catpage, name in match:
        utils.addDir(name, catpage, 411, '')    
    xbmcplugin.endOfDirectory(utils.addon_handle)


def Search(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 414)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title
        List(searchUrl)

