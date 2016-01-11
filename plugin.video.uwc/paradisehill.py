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

dialog = utils.dialog

def Main():
    utils.addDir('[COLOR yellow]Categories[/COLOR]','http://www.paradisehill.tv/en/',253,'','')
    List('http://www.paradisehill.tv/en/?page=1',1)
    xbmcplugin.endOfDirectory(utils.addon_handle)


def List(url, page):
    url = url.replace('page=1','page='+str(page))
    listhtml = utils.getHtml(url, '')
    match = re.compile('</h\d+>(.*?)class="pagination', re.DOTALL | re.IGNORECASE).findall(listhtml)
    match1 = re.compile('link" href="([^"]+)".*?bci-title">([^<]+)<.*?src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(match[0])
    for videopage, name, img in match1:
        name = utils.cleantext(name)
        img = "http://www.paradisehill.tv" + img
        videopage = "http://www.paradisehill.tv" + videopage
        utils.addDownLink(name, videopage, 252, img, '')
    if re.search('<li class="last">', listhtml, re.DOTALL | re.IGNORECASE):
        npage = page + 1        
        url = url.replace('page='+str(page),'page='+str(npage))
        utils.addDir('Next Page ('+str(npage)+')', url, 251, '', npage)
    xbmcplugin.endOfDirectory(utils.addon_handle)


def Cat(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile("Categories</h2>(.*?)<noindex>", re.DOTALL | re.IGNORECASE).findall(cathtml)
    match1 = re.compile('link" href="([^"]+)".*?bci-title">([^<]+)<.*?src="([^"]+)".*?cat-title">([^<]+)<', re.DOTALL | re.IGNORECASE).findall(match[0])
    for caturl, name, img, videos in match1:
        name = name + " [COLOR blue]" + videos + "[/COLOR]"
        img = "http://www.paradisehill.tv" + img
        catpage = "http://www.paradisehill.tv" + caturl + "?page=1"
        utils.addDir(name, catpage, 251, img, 1)
    xbmcplugin.endOfDirectory(utils.addon_handle)


def Playvid(url, name, download=None):
    videopage = utils.getHtml(url, '')
    match = re.compile('films="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(videopage)
    videos = match[0].split('|||')
    
    if len(videos) > 1:
        i = 1
        videolist = []
        for x in videos:
            videolist.append('Part ' + str(i))
            i += 1
        videopart = dialog.select('Multiple videos found', videolist)
        videourl = videos[videopart]
    else: videourl = videos[0]    
    
    videourl = videourl + "|referer="+ url

    if download == 1:
        utils.downloadVideo(videourl, name)
    else:
        iconimage = xbmc.getInfoImage("ListItem.Thumb")
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})
        xbmc.Player().play(videourl, listitem)
