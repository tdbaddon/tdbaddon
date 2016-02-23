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

from jsunpack import unpack

import utils

progress = utils.progress
dialog = utils.dialog


def getHC(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', utils.USER_AGENT)
    response = urllib2.urlopen(req, timeout=60)
    data = response.read()
    response.close()
    return data

def HCList(url):
    utils.addDir('[COLOR hotpink]A-Z List[/COLOR] [COLOR white]Censored & Uncensored[/COLOR]','http://www.hentaicraving.com/hentai-list/',33,'','')
    link = utils.getHtml(url, '')
    match = re.compile("""<a href='([^']+)'><img.*?title="([^"]+)".*?src="([^"]+)".*?Description: </b> ([^<]+)<p>""", re.DOTALL | re.IGNORECASE).findall(link)
    for videourl, name, img, desc in match:
        addHCDir(name, videourl, 31, img, desc)
    xbmc.executebuiltin('Container.SetViewMode(503)')
    xbmcplugin.endOfDirectory(utils.addon_handle)
    
def HCA2Z(url):
    link = utils.getHtml(url, '')
    match = re.compile('hentai-series/([^/]+)/">([^<]+)', re.DOTALL | re.IGNORECASE).findall(link)
    for link, name in match:
        url = 'http://www.hentaicraving.com/hentai-series/' + link + '/'
        img = 'http://www.hentaicraving.com/images/' + link + '.jpg'
        addHCDir(name, url, 31, img, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)    
    
def HCEpisodes(url,name, img):
    link = utils.getHtml(url, '')
    eps = re.compile('<li><a href="([^"]+)">([^<]+)</a> <', re.DOTALL | re.IGNORECASE).findall(link)
    for url, name in eps:
        utils.addDownLink(name,url,32,img, '')
        
def HCPlayvid(url,name, download=None):
    progress.create('Play video', 'Searching videofile.')
    progress.update( 10, "", "Loading video page", "" )
    link = utils.getHtml(url,'')
    match = re.compile('<iframe.*? src="([^"]+)" FRAME', re.DOTALL | re.IGNORECASE).findall(link)
    if len(match) > 1:
        vh = dialog.select('Videohost:', match)
    else:
        vh = 0
    progress.update( 40, "", "Loading video host", "" )
    urldata2 = getHC(match[vh])
    if match[vh].find('hentaiupload') > 0:
        progress.update( 80, "", "Loading hentaiupload", "" )    
        try:
            match1 = re.compile('url: "([^"]+mp4)', re.DOTALL | re.IGNORECASE).findall(urldata2)
            url = match1[0]
        except: pass
        videourl = url + "|referer="+ match[vh]
    elif match[vh].find('hvidengine') > 0:
        progress.update( 80, "", "Loading hvidengine", "" )        
        try:
            match1 = re.compile('file: "([^"]+)', re.DOTALL | re.IGNORECASE).findall(urldata2)
            url = match1[0]
        except: pass
        videourl = url + "|referer="+ match[vh]
    else:
        progress.update( 80, "", "Loading video", "" )
        match2 = re.compile("<script type='text/javascript'>([^<]+)</sc", re.DOTALL | re.IGNORECASE).findall(urldata2)
        res = unpack(match2[0])
        match3 = re.compile("file.*?(http.*?mp4)", re.DOTALL | re.IGNORECASE).findall(res)
        videourl = match3[0]
    progress.close()
    if download == 1:
        utils.downloadVideo(videourl, name)
    else:    
        iconimage = xbmc.getInfoImage("ListItem.Thumb")
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})
        xbmc.Player().play(videourl, listitem)
    
def addHCDir(name,url,mode,iconimage,desc):
    u = (sys.argv[0] +
         "?url=" + urllib.quote_plus(url) +
         "&mode=" + str(mode) +
         "&name=" + urllib.quote_plus(name) +
         "&img=" + urllib.quote_plus(iconimage))
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={ "Title": name, "plot": desc, "plotoutline": desc })
    ok = xbmcplugin.addDirectoryItem(handle=utils.addon_handle, url=u, listitem=liz, isFolder=True)
    return ok

