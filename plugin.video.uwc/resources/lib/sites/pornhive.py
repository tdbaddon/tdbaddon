'''
    Ultimate Whitecream
    Copyright (C) 2015 Whitecream

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

import urllib
import re

import xbmc
import xbmcplugin
import xbmcgui
from resources.lib import utils

progress = utils.progress


@utils.url_dispatcher.register('70')
def PHMain():
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','http://www.pornhive.tv/en/movies/all',73,'','')
    utils.addDir('[COLOR hotpink]Search[/COLOR]','http://www.pornhive.tv/en/search?title=',74,'','')
    PHList('http://www.pornhive.tv/en/movies/all')
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('71', ['url'])
def PHList(url):
    try:
        listhtml = utils.getHtml(url, '')
    except:
        utils.notify('Oh oh','It looks like this website is down.')
        return None
    match = re.compile(r'panel-img">\s+<a href="([^"]+)"><img data-src="([^"]+)".*?alt="([^"]+)', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videopage, img, name in match:
        name = utils.cleantext(name)
        utils.addDownLink(name, videopage, 72, img, '')
    try:
        nextp=re.compile('<a href="([^"]+)"[^>]+>Next', re.DOTALL | re.IGNORECASE).findall(listhtml)
        utils.addDir('Next Page', nextp[0],71,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('74', ['url'], ['keyword'])    
def PHSearch(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 74)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title
        print "Searching URL: " + searchUrl
        PHList(searchUrl)


@utils.url_dispatcher.register('73', ['url'])
def PHCat(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('<ul class="dropdown-menu my-drop">(.*?)</ul>', re.DOTALL | re.IGNORECASE).findall(cathtml)
    match1 = re.compile('href="([^"]+)[^>]+>([^<]+)<', re.DOTALL | re.IGNORECASE).findall(match[0])
    for catpage, name in match1:
        utils.addDir(name, catpage, 71, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)   


@utils.url_dispatcher.register('72', ['url', 'name'], ['download'])
def PHVideo(url, name, download=None):
    progress.create('Play video', 'Searching videofile.')
    progress.update( 10, "", "Loading video page", "" )
    Supported_hosts = ['Openload.io', 'StreamCloud', 'NowVideo', 'www.nowvideo.sx', 'FlashX', 'www.flashx.tv', 'flashx.tv',  'streamcloud.eu', 'streamin.to', 'videowood.tv', 'www.keeplinks.eu', 'openload.co', 'datoporn.com', 'gr8movies.org', 'pornoworld.freeforumzone.com']
    videopage = utils.getHtml(url, '')
    match = re.compile(r'data-id="([^"]+)" target="_blank" title="Watch it on ([\w.]+)', re.DOTALL | re.IGNORECASE).findall(videopage)
    if len(match) > 1:
        sites = []
        vidurls = []
        for videourl, site in match:
            if site in Supported_hosts:
                sites.append(site)
                vidurls.append(videourl)
        if len(sites) ==  1:
            sitename = sites[0]
            siteurl = vidurls[0]
        elif len(sites) > 1:
            site = utils.dialog.select('Select video site', sites)
            if site == -1:
                return
            sitename = sites[site]
            siteurl = vidurls[site]
        else:
            utils.notify('Sorry','No supported hosts found.')
            return
    else:
        sitename = match[0][1]
        siteurl = match[0][0]
    outurl = "http://www.pornhive.tv/en/out/" + siteurl
    progress.update( 20, "", "Getting video page", "" )
    if 'loud' in sitename:
        progress.update( 30, "", "Getting StreamCloud", "" )
        playurl = getStreamCloud(outurl)
    elif "lash" in sitename:
        progress.update( 30, "", "Getting FlashX", "" )
        progress.close()
        utils.PLAYVIDEO(outurl, name, download)
        return
    elif sitename == "NowVideo" or sitename == "www.nowvideo.sx":
        progress.update( 30, "", "Getting NowVideo", "" )
        playurl = getNowVideo(outurl)        
    elif "penload" in sitename:
        progress.update( 30, "", "Getting Openload", "" )
        outurl1 = utils.getVideoLink(outurl, '')
        utils.playvideo(outurl1, name, download, outurl)
        return
    elif "videowood" in sitename:
        progress.update( 30, "", "Getting Videowood", "" )
        progress.close()
        utils.PLAYVIDEO(outurl, name, download)
        return
    elif "gr8movies" in sitename:
        progress.update( 30, "", "Getting Gr8movies", "" )
        progress.close()
        utils.PLAYVIDEO(outurl, name, download)
        return
    elif "freeforumzone" in sitename:
        progress.update( 30, "", "Getting pornoworld", "" )
        progress.close()
        utils.PLAYVIDEO(outurl, name, download)
        return        
    elif "streamin" in sitename:
        progress.update( 30, "", "Getting Streamin", "" )
        streaming = utils.getHtml(outurl, '')
        outurl=re.compile("action='([^']+)'").findall(streaming)[0]
        progress.close()
        utils.playvideo(outurl, name, download, outurl)
        return
    elif 'keeplinks' in sitename:
        progress.update( 30, "", "Getting Keeplinks", "" )
        outurl2 = getKeeplinks(outurl)
        utils.playvideo(outurl2, name, download, outurl)
        return
    elif "datoporn" in sitename:
        progress.update( 30, "", "Getting Datoporn", "" )
        outurl1 = utils.getVideoLink(outurl, '')
        utils.playvideo(outurl1, name, download, outurl)
        return        
    else:
        progress.close()
        utils.notify('Sorry','This host is not supported.')
        return
    progress.update( 90, "", "Playing video", "" )
    progress.close()
    if playurl:
        if download == 1:
            utils.downloadVideo(playurl, name)
        else:
            iconimage = xbmc.getInfoImage("ListItem.Thumb")
            listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
            listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})
            xbmc.Player().play(playurl, listitem)


def getKeeplinks(url):
    kllink = utils.getVideoLink(url, '')
    kllinkid = kllink.split('/')[-1]
    klheader = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive',
       'Cookie': 'flag['+kllinkid+'] = 1;'} 
    klpage = utils.getHtml(kllink, url, klheader)
    return klpage


def getStreamCloud(url):
    progress.update( 40, "", "Opening Streamcloud", "" )
    scpage = utils.getVideoLink(url, '')
    progress.update( 50, "", "Getting Streamcloud page", "" )
    schtml = utils.postHtml(scpage)
    form_values = {}
    match = re.compile('<input.*?name="(.*?)".*?value="(.*?)">', re.DOTALL | re.IGNORECASE).findall(schtml)
    for name, value in match:
        form_values[name] = value.replace("download1","download2")
    progress.update( 60, "", "Grabbing video file", "" )    
    newscpage = utils.postHtml(scpage, form_data=form_values)
    videourl = re.compile('file:\s*"(.+?)",', re.DOTALL | re.IGNORECASE).findall(newscpage)
    progress.update( 80, "", "Returning video file", "" )  
    return videourl[0]


def getNowVideo(url):
    progress.update( 50, "", "Opening NowVideo page", "" )
    videopage = utils.getHtml(url, '')
    if not 'flashvars.file' in videopage:    
        videoid = re.compile('/video/([^"]+)').findall(videopage)[0]
        url = "http://embed.nowvideo.sx/embed/?v=" + videoid
        videopage = utils.getHtml(url, '')
    fileid=re.compile('flashvars.file="(.+?)";').findall(videopage)[0]
    codeid=re.compile('flashvars.cid="(.+?)";').findall(videopage)
    if(len(codeid) > 0):
         codeid=codeid[0]
    else:
         codeid=""
    keycode=re.compile('flashvars.filekey=(.+?);').findall(videopage)[0]
    keycode=re.compile('var\s*'+keycode+'="(.+?)";').findall(videopage)[0]
    videolink = "http://www.nowvideo.sx/api/player.api.php?codes="+urllib.quote_plus(codeid) + "&key="+urllib.quote_plus(keycode) + "&file=" + urllib.quote_plus(fileid)
    progress.update( 60, "", "Grabbing video file", "" ) 
    vidcontent = utils.getHtml(videolink, '')
    videourl = re.compile('url=(.+?)\&').findall(vidcontent)[0]
    progress.update( 80, "", "Returning video file", "" )      
    return videourl
