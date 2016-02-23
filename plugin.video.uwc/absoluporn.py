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

import urllib, urllib2, re, cookielib, os.path, sys, socket, hashlib
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

import utils


def Main():
    utils.addDir('[COLOR hotpink]Top Rated[/COLOR]','http://www.absoluporn.com/en/wall-note-1.html',301,'','')
    utils.addDir('[COLOR hotpink]Most Viewed[/COLOR]','http://www.absoluporn.com/en/wall-main-1.html',301,'','')
    utils.addDir('[COLOR hotpink]Longest[/COLOR]','http://www.absoluporn.com/en/wall-time-1.html',301,'','')
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','http://www.absoluporn.com/en',303,'','')
    utils.addDir('[COLOR hotpink]Search[/COLOR]','http://www.absoluporn.com/en/search-',304,'','')
    List('http://www.absoluporn.com/en/wall-date-1.html')
    xbmcplugin.endOfDirectory(utils.addon_handle)

def List(url):
    listhtml = utils.getHtml(url, '')
    match = re.compile('thumb-main-titre"><a href="..([^"]+)".*?title="([^"]+)".*?src="([^"]+)".*?<div class="thumb-info">(.*?)time">([^<]+)<', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videourl, name, img, hd, duration in match:
        name = utils.cleantext(name)
        if hd.find('hd') > 0:
            if hd.find('full') > 0:
                hd = " [COLOR yellow]FULLHD[/COLOR] "
            else:
                hd = " [COLOR orange]HD[/COLOR] "
        else:
            hd = " "
        videopage = "http://www.absoluporn.com" + videourl
        name = name + hd + "[COLOR deeppink]" + duration + "[/COLOR]"
        utils.addDownLink(name, videopage, 302, img, '')
    try:
        nextp=re.compile(r'<span class="text16">\d+</span> <a href="..([^"]+)"').findall(listhtml)
        utils.addDir('Next Page', 'http://www.absoluporn.com' + nextp[0], 301,'')
    except: pass    
    xbmcplugin.endOfDirectory(utils.addon_handle)


def Playvid(url, name, download=None):
    videopage = utils.getHtml(url, '')
    servervideo = re.compile("servervideo = '([^']+)'", re.DOTALL | re.IGNORECASE).findall(videopage)[0]
    vpath = re.compile("path = '([^']+)'", re.DOTALL | re.IGNORECASE).findall(videopage)[0]
    repp = re.compile(r"repp = codage\('([^']+)'", re.DOTALL | re.IGNORECASE).findall(videopage)[0]
    filee = re.compile("filee = '([^']+)'", re.DOTALL | re.IGNORECASE).findall(videopage)[0]
    repp = hashlib.md5(repp).hexdigest()
    videourl = servervideo + vpath + repp + filee
    if download == 1:
        utils.downloadVideo(videourl, name)
    else:
        iconimage = xbmc.getInfoImage("ListItem.Thumb")
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})
        xbmc.Player().play(videourl, listitem)


def Cat(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile("gories(.*?)titre18", re.DOTALL | re.IGNORECASE).findall(cathtml)
    match1 = re.compile(r'<a href="\.\.([^"]+)" class="link1">([^<]+)</a>', re.DOTALL | re.IGNORECASE).findall(match[0])
    for caturl, name in match1:
        catpage = 'http://www.absoluporn.com' + caturl
        utils.addDir(name, catpage, 301, '', '')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def Search(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 304)
    else:
        title = keyword.replace(' ','%20')
        searchUrl = searchUrl + title + '-1.html'
        print "Searching URL: " + searchUrl
        List(searchUrl)
