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

import urllib, re, os
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

import utils

progress = utils.progress


def Main():
    utils.addDir('[COLOR yellow]Categories[/COLOR]', 'http://www.videomegaporn.com/categories/', 163, '', '')
    utils.addDir('[COLOR yellow]Search[/COLOR]', 'http://www.videomegaporn.com/search-', 164, '', '')
    List('http://www.videomegaporn.com/index.html')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def List(url):
    listhtml = utils.getHtml(url, '')
    match = re.compile('<div class="runtime">([^<]+).*?href="([^"]+)".*?alt="([^"]+)".*?src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for runtime, videopage, name, img in match:
        name = utils.cleantext(name)
        if runtime:
            name = name + ' [COLOR blue]' + runtime + '[/COLOR]'
        utils.addDownLink(name, videopage, 162, img, '')
    try:
        nextp=re.compile("<a href='([^']+)' title='([^']+)'>&raquo;</a>", re.DOTALL | re.IGNORECASE).findall(listhtml)
        next = urllib.quote_plus(nextp[0][0])
        next = next.replace(' ','+')
        utils.addDir('Next Page', os.path.dirname(url) + '/' + next, 161,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)

    
def Search(url):
    searchUrl = url
    vq = utils._get_keyboard(heading="Searching for...")
    if (not vq): return False, 0
    title = urllib.quote_plus(vq)
    title = title.replace(' ','+')
    searchUrl = searchUrl + title + ".html"
    print "Searching URL: " + searchUrl
    List(searchUrl)


def Categories(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('<div class="menu">(.*?)</div>', re.DOTALL | re.IGNORECASE).findall(cathtml)
    match1 = re.compile('href="([^"]+)[^>]+>([^<]+)<', re.DOTALL | re.IGNORECASE).findall(match[0])
    for catpage, name in match1:
        utils.addDir(name, catpage, 161, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)   


def Playvid(url, name, download=None):
    utils.PLAYVIDEO(url, name, download)
