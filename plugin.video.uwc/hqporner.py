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


def HQMAIN():
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','http://hqporner.com/porn-categories.php',153,'','')
    utils.addDir('[COLOR hotpink]Studios[/COLOR]','http://hqporner.com/porn-studios.php',153,'','')
    utils.addDir('[COLOR hotpink]Girls[/COLOR]','http://hqporner.com/porn-actress.php',153,'','')
    utils.addDir('[COLOR hotpink]Search[/COLOR]','http://hqporner.com/?s=',154,'','')
    HQLIST('http://hqporner.com/hdporn/1')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def HQLIST(url):
    link = utils.getHtml(url, '')
    match = re.compile('<a href="([^"]+)" class="image featured non-overlay".*?<img id="[^"]+" src="([^"]+)" alt="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(link)
    for url, img, name in match:
        name = utils.cleantext(name)    
        videourl = "http://www.hqporner.com" + url
        utils.addDownLink(name, videourl, 152, img, '')
    try:
        nextp=re.compile('<a href="([^"]+)"[^>]+>Next', re.DOTALL | re.IGNORECASE).findall(link)
        nextp = "http://www.hqporner.com" + nextp[0]
        utils.addDir('Next Page', nextp,151,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)


def HQCAT(url):
    link = utils.getHtml(url, '')
    tags = re.compile('<a href="([^"]+)"[^<]+<img src="([^"]+)" alt="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(link)
    for caturl, catimg, catname in tags:
        caturl = "http://www.hqporner.com" + caturl
        catimg = "http://www.hqporner.com" + catimg        
        utils.addDir(catname,caturl,151,catimg)
    xbmcplugin.endOfDirectory(utils.addon_handle)


def HQSEARCH(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 154)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title
        print "Searching URL: " + searchUrl
        HQLIST(searchUrl)


def HQPLAY(url, name, download=None):
    videopage = utils.getHtml(url, url)
    iframeurl = re.compile(r'<iframe\swidth="\d+"\sheight="\d+"\ssrc="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(videopage)
    #if re.search('hqporner', iframeurl[0], re.DOTALL | re.IGNORECASE):
    #    videourl = getHQ(iframeurl[0])
    if re.search('bemywife', iframeurl[0], re.DOTALL | re.IGNORECASE):
        videourl = getBMW(iframeurl[0])
    elif re.search('5\.79', iframeurl[0], re.DOTALL | re.IGNORECASE):
        videourl = getIP(iframeurl[0])
    elif re.search('flyflv', iframeurl[0], re.DOTALL | re.IGNORECASE):
        videourl = getFly(iframeurl[0])
    else:
        utils.notify('Oh oh','Couldn\'t find a supported videohost')
        return
    utils.playvid(videourl, name, download)


def getBMW(url):
    videopage = utils.getHtml(url, '')
    #redirecturl = utils.getVideoLink(url, '')
    #videodomain = re.compile("http://([^/]+)/", re.DOTALL | re.IGNORECASE).findall(redirecturl)[0]
    videos = re.compile(r'file: "([^"]+mp4)", label: "\d', re.DOTALL | re.IGNORECASE).findall(videopage)
    videourl = videos[-2]
    return videourl

def getIP(url):
    videopage = utils.getHtml(url, '')
    videos = re.compile('file": "([^"]+)"', re.DOTALL | re.IGNORECASE).findall(videopage)
    videourl = videos[-1]
    return videourl

def getFly(url):
    videopage = utils.getHtml(url, '')
    videos = re.compile('fileUrl="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(videopage)
    videourl = videos[-1]
    return videourl
