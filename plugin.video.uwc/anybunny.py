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

# 320: anybunny.Main()
# 321: anybunny.List(url)
# 322: anybunny.Playvid(url, name, download)
# 323: anybunny.Categories(url)
# 324: anybunny.Search(url, keyword)
# 325: anybunny.Categories2(url)

def Main():
    utils.addDir('[COLOR hotpink]Top videos[/COLOR]','http://anybunny.com/top/',321,'','')
    utils.addDir('[COLOR hotpink]Categories - images[/COLOR]','http://anybunny.com/',323,'','')
    utils.addDir('[COLOR hotpink]Categories - all[/COLOR]','http://anybunny.com/',325,'','')
    utils.addDir('[COLOR hotpink]Search[/COLOR]','http://anybunny.com/new/',324,'','')
    List('http://anybunny.com/new/?p=1')
    xbmcplugin.endOfDirectory(utils.addon_handle)

def List(url):
    listhtml = utils.getHtml(url, '')
    match = re.compile(r"src='([^']+)' id=(\d+) alt='([^']+)'", re.DOTALL | re.IGNORECASE).findall(listhtml)
    for img, urlid, name in match:
        name = utils.cleantext(name)
        videopage = "https://vartuc.com/kt_player/player.php?id=" + urlid
        utils.addDownLink(name, videopage, 322, img, '')
    try:
        nextp = re.compile('href="([^"]+)">Next', re.DOTALL | re.IGNORECASE).findall(listhtml)
        utils.addDir('Next Page', nextp[0], 321,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)

def Playvid(url, name, download=None):
    videopage = utils.getHtml(url, url)
    video_url = re.compile("video_url:([^}]+)", re.DOTALL | re.IGNORECASE).findall(videopage)[0]
    match = re.compile(r'(ghb\w\w)="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(videopage)
    for repl, repl2 in match:
        video_url = video_url.replace(repl,repl2)
    video_url = video_url.replace("\"","")
    videourl = video_url.replace("+","")

    if download == 1:
        utils.downloadVideo(videourl, name)
    else:
        iconimage = xbmc.getInfoImage("ListItem.Thumb")
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})
        xbmc.Player().play(videourl, listitem)


def Categories(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile("<a href='/top/([^']+)'>.*?src='([^']+)' alt='([^']+)'", re.DOTALL | re.IGNORECASE).findall(cathtml)
    for catid, img, name in match:
        catpage = "http://anybunny.com/new/"+ catid
        utils.addDir(name, catpage, 321, img)
    xbmcplugin.endOfDirectory(utils.addon_handle)


def Categories2(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile(r"href='/top/([^']+)'>([^<]+)</a> <a>([^)]+\))", re.DOTALL | re.IGNORECASE).findall(cathtml)
    for catid, name, videos in match:
        name = name + " [COLOR deeppink]" + videos + "[/COLOR]"
        catpage = "http://anybunny.com/new/"+ catid
        utils.addDir(name, catpage, 321, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def Search(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 324)
    else:
        title = keyword.replace(' ','_')
        searchUrl = searchUrl + title
        print "Searching URL: " + searchUrl
        List(searchUrl)
