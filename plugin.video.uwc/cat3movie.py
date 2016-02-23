'''
    Ultimate Whitecream
    Copyright (C) 2015 mortael
    Copyright (C) 2015 anton40

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

import urllib, re, base64
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

import utils

progress = utils.progress

def Main():
    utils.addDir('[COLOR hotpink]Search[/COLOR]','http://cat3movie.us/?s=', 353, '', '')
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','http://cat3movie.us', 354, '', '')
    List('http://cat3movie.us')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def List(url):
    listhtml = utils.getHtml(url, '')
    match = re.compile('<a class="" href="(.+?)" title="(.+?)">\n<img src="(.+?)" class="has-image" alt=".+?"/>', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videopage, name, img in match:
        name = utils.cleantext(name)
        utils.addDownLink(name, videopage, 352, img, '')
    try:
        nextp=re.compile('<li class="disabled active"><span class="active">.+?</span></li><li><a href="(.+?)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
        utils.addDir('Next Page', nextp[0], 351,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)

    
def Search(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 353)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title
        print "Searching URL: " + searchUrl
        List(searchUrl)


def Categories(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('<li id=".+?" class=".+?menu-item-object-category.+?"><a href="(.+?)">(.+?)</a></li>', re.DOTALL | re.IGNORECASE).findall(cathtml)
    for catpage, name in match:
        utils.addDir(name, catpage, 351, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def Playvid(url, name, download=None):
    print "cat3movie::playvid " + url
    progress.create('Play video', 'Searching videofile.')
    progress.update( 10, "", "Loading video page", "" )
    html = utils.getHtml(url, '')
    embedLinks = re.compile('<a href="(.+?)" rel="nofollow" target="_blank">').findall(html)
    url = ''
    for link in embedLinks:
        html = utils.getHtml(link, '')
        base64str = re.compile('Base64.decode\("(.+?)"\)').findall(html)
        url = url + " " + base64.b64decode(base64str[0])
    utils.playvideo(url, name, download)