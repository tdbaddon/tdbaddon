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

def Main():
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','http://www.xvideospanish.com/categorias/',133,'','')
    utils.addDir('[COLOR hotpink]Search[/COLOR]','http://www.xvideospanish.com/?s=',134,'','')
    List('http://www.xvideospanish.com/')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def List(url):
    listhtml = utils.getHtml(url, '')
    match = re.compile('<figure><a href="([^"]+)".*?data-original="([^"]+)".*?alt="([^"]+)">(?:<span>)?([^<]+)?(?:</span>)?</a>', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videopage, img, name, runtime in match:
        name = utils.cleantext(name[7:])
        if runtime:
            name = name + ' [COLOR deeppink]' + runtime + '[/COLOR]'
        utils.addDownLink(name, videopage, 132, img, '')
    try:
        nextp=re.compile('<a class="nextpostslink" rel="next" href="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
        utils.addDir('Next Page', nextp[0], 131,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)

    
def Search(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 134)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title
        print "Searching URL: " + searchUrl
        List(searchUrl)


def Categories(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('data-original="([^"]+)".*?href="([^"]+)">([^<]+)<.*?strong>([^<]+)<', re.DOTALL | re.IGNORECASE).findall(cathtml)
    for img, catpage, name, videos in match:
        name = name + ' [COLOR deeppink]' + videos + ' videos[/COLOR]'
        utils.addDir(name, catpage, 131, img)
    xbmcplugin.endOfDirectory(utils.addon_handle)   


def Playvid(url, name, download=None):
    utils.PLAYVIDEO(url, name, download)
