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

#230: k18.Main()
#231: k18.List(url)
#232: k18.Playvid(url, name, download)
#233: k18.Cat(url)
#234: k18.Search(url, keyword)

progress = utils.progress

def Main():
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','http://k18.co/',233,'','')
    utils.addDir('[COLOR hotpink]Search[/COLOR]','http://k18.co/?s=',234,'','')
    List('http://k18.co/page/1/')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def List(url):
    listhtml = utils.getHtml(url, '')
    match = re.compile(r'class="content-list-thumb">\s+<a href="([^"]+)" title="([^"]+)">.*?src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videopage, name, img in match:
        name = utils.cleantext(name)
        utils.addDownLink(name, videopage, 232, img, '')
    try:
        nextp=re.compile('next page-numbers" href="([^"]+)">&raquo;', re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
        utils.addDir('Next Page', nextp, 231,'')
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


def Cat(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('0" value="([^"]+)">([^<]+)<', re.DOTALL | re.IGNORECASE).findall(cathtml)
    for catpage, name in match:
        catpage = 'http://k18.co/?cat=' + catpage
        utils.addDir(name, catpage, 231, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)   


def Playvid(url, name, download=None):
    utils.PLAYVIDEO(url, name, download)

