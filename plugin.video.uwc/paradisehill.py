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
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','http://www.paradisehill.tv/en/',253,'','')
    utils.addDir('[COLOR hotpink]Search[/COLOR]','http://www.paradisehill.tv/en/search_results.html?search=',254,'','')
    List('http://www.paradisehill.tv/en/?page=1',1)
    xbmcplugin.endOfDirectory(utils.addon_handle)


def List(url, page):
    if page == 1:
        url = url.replace('page=1','page='+str(page))
    listhtml = utils.getHtml(url, '')
    match = re.compile('</h\d+>(.*?)<footer>', re.DOTALL | re.IGNORECASE).findall(listhtml)
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
        name = name + " [COLOR deeppink]" + videos + "[/COLOR]"
        img = "http://www.paradisehill.tv" + img
        catpage = "http://www.paradisehill.tv" + caturl + "?page=1"
        utils.addDir(name, catpage, 251, img, 1)
    xbmcplugin.endOfDirectory(utils.addon_handle)


def Search(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 254)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title
        List(searchUrl, 1)


def Playvid(url, name, download=None):
    if utils.addon.getSetting("paradisehill") == "true": playall = True
    else: playall = ''
    videopage = utils.getHtml(url, '')
    match = re.compile('films="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(videopage)
    videos = match[0].split('|||')
    
    if playall == '':
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

    if download == 1 and playall == '':
        utils.downloadVideo(videourl, name)
    else:
        iconimage = xbmc.getInfoImage("ListItem.Thumb")
      
        if playall:
            pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
            pl.clear()
            i = 1
            for videourl in videos:
                newname = name + ' Part ' + str(i)
                listitem = xbmcgui.ListItem(newname, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
                listitem.setInfo('video', {'Title': newname, 'Genre': 'Porn'})
                listitem.setProperty("IsPlayable","true")
                videourl = videourl + "|referer="+ url
                pl.add(videourl, listitem)
                i += 1
                listitem = ''
            xbmc.Player().play(pl)
        else:
            listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
            listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})        
            xbmc.Player().play(videourl, listitem)
            