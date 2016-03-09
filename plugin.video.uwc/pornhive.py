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

from jsunpack import unpack

progress = utils.progress

def PHMain():
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','http://www.pornhive.tv/en/movies/all',73,'','')
    utils.addDir('[COLOR hotpink]Search[/COLOR]','http://www.pornhive.tv/en/search?title=',74,'','')
    PHList('http://www.pornhive.tv/en/movies/all')
    xbmcplugin.endOfDirectory(utils.addon_handle)



def PHList(url):
    listhtml = utils.getHtml(url, '')
    match = re.compile('panel-img">.*?<a href="([^"]+)" title="([^"]+)".*?src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videopage, name, img in match:
        name = utils.cleantext(name)
        utils.addDownLink(name, videopage, 72, img, '')
    try:
        nextp=re.compile('<a href="([^"]+)">Next', re.DOTALL | re.IGNORECASE).findall(listhtml)
        utils.addDir('Next Page', nextp[0],71,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)

    
def PHSearch(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 74)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title
        print "Searching URL: " + searchUrl
        PHList(searchUrl)


def PHCat(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('<ul class="dropdown-menu my-drop">(.*?)</ul>', re.DOTALL | re.IGNORECASE).findall(cathtml)
    match1 = re.compile('href="([^"]+)[^>]+>([^<]+)<', re.DOTALL | re.IGNORECASE).findall(match[0])
    for catpage, name in match1:
        utils.addDir(name, catpage, 71, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)   


def PHVideo(url, name, download=None):
    progress.create('Play video', 'Searching videofile.')
    progress.update( 10, "", "Loading video page", "" )
    Supported_hosts = ['Openload.io', 'StreamCloud', 'NowVideo', 'FlashX', 'www.flashx.tv', 'streamcloud.eu', 'streamin.to']
    videopage = utils.getHtml(url, '')
    match = re.compile(r'<li id="link-([^"]+).*?xs-12">\s+Watch it on ([\w\.]+)', re.DOTALL | re.IGNORECASE).findall(videopage)
    if len(match) > 1:
        sites = []
        vidurls = []
        for videourl, site in match:
            if site in Supported_hosts:
                sites.append(site)
                vidurls.append(videourl)
        if len(sites) ==  1:
            sitename = match[0][1]
            siteurl = match[0][0]
        else:
            site = utils.dialog.select('Select video site', sites)
            sitename = sites[site]
            siteurl = vidurls[site]
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
        playurl = getFlashX(outurl)
    elif sitename == "NowVideo":
        progress.update( 30, "", "Getting NowVideo", "" )
        playurl = getNowVideo(outurl)        
    elif "Openload" in sitename:
        progress.update( 30, "", "Getting Openload", "" )
        progress.close()
        utils.PLAYVIDEO(outurl, name, download)
        return
    elif "streamin" in sitename:
        progress.update( 30, "", "Getting Streamin", "" )
        streaming = utils.getHtml(outurl, '')
        outurl=re.compile("action='([^']+)'").findall(streaming)[0]
        progress.close()
        utils.playvideo(outurl, name, download)
        return
    else:
        progress.close()
        utils.notify('Sorry','This host is not supported.')
        return
    progress.update( 90, "", "Playing video", "" )
    progress.close()
    if download == 1:
        utils.downloadVideo(playurl, name)
    else:
        iconimage = xbmc.getInfoImage("ListItem.Thumb")
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})
        xbmc.Player().play(playurl, listitem)


def getFlashX(url):
    phpage = utils.getHtml(url, '')
    progress.update( 50, "", "Opening FlashX page", "" )
    flashxurl = re.compile(r"//(?:www\.)?flashx\.tv/(?:embed-)?([0-9a-zA-Z]+)", re.DOTALL | re.IGNORECASE).findall(phpage)
    flashxurl = 'http://flashx.tv/embed-%s-670x400.html' % flashxurl[0]    
    flashxsrc = utils.getHtml2(flashxurl)
    progress.update( 60, "", "Grabbing video file", "" )
    flashxurl2 = re.compile('<a href="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(flashxsrc)
    flashxsrc2 = utils.getHtml2(flashxurl2[0])
    progress.update( 70, "", "Grabbing video file", "" )
    flashxjs = re.compile("<script type='text/javascript'>([^<]+)</sc", re.DOTALL | re.IGNORECASE).findall(flashxsrc2)
    try: flashxujs = unpack(flashxjs[0])
    except: flashxujs = flashxjs[0]
    videourl = re.compile(r'\[{\s?file:\s?"([^"]+)",', re.DOTALL | re.IGNORECASE).findall(flashxujs)
    progress.update( 80, "", "Returning video file", "" )
    videourl = videourl[0]
    return videourl


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
    videourl = re.compile('file: "(.+?)",', re.DOTALL | re.IGNORECASE).findall(newscpage)
    progress.update( 80, "", "Returning video file", "" )  
    return videourl[0]


def getNowVideo(url):
    progress.update( 50, "", "Opening NowVideo page", "" )
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
