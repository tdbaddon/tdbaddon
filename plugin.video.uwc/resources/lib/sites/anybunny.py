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

import re

import xbmc
import xbmcplugin
import xbmcgui
from resources.lib import utils
    

vartuchdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
       'Accept': '*/*',
       'Accept-Encoding': 'gzip, deflate, sdch, br',
       'Accept-Language': 'en-US,en;q=0.8,nl;q=0.6',
       'Connection': 'keep-alive'}

vartuchdr2 = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
       'Accept': '*/*',
       'Accept-Encoding': 'gzip, deflate, sdch',
       'Accept-Language': 'en-US,en;q=0.8,nl;q=0.6',
       'X-Requested-With': 'ShockwaveFlash/22.0.0.209',
       'Connection': 'keep-alive'}        


@utils.url_dispatcher.register('320')
def Main():
    utils.addDir('[COLOR hotpink]Top videos[/COLOR]','http://anybunny.com/top/',321,'','')
    utils.addDir('[COLOR hotpink]Categories - images[/COLOR]','http://anybunny.com/',323,'','')
    utils.addDir('[COLOR hotpink]Categories - all[/COLOR]','http://anybunny.com/',325,'','')
    utils.addDir('[COLOR hotpink]Search[/COLOR]','http://anybunny.com/new/',324,'','')
    List('http://anybunny.com/new/?p=1')
    xbmcplugin.endOfDirectory(utils.addon_handle)

    
@utils.url_dispatcher.register('321', ['url'])
def List(url):
    try:
        listhtml = utils.getHtml(url, '')
    except:
        utils.notify('Oh oh','It looks like this website is down.')
        return None
    match = re.compile(r"<a href='([^']+).*?src='([^']+)' id=\d+ alt='([^']+)'", re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videopage, img, name in match:
        name = utils.cleantext(name)
        utils.addDownLink(name, videopage, 322, img, '')
    try:
        nextp = re.compile('href="([^"]+)">Next', re.DOTALL | re.IGNORECASE).findall(listhtml)
        utils.addDir('Next Page', nextp[0], 321,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('322', ['url', 'name'], ['download'])
def Playvid(url, name, download=None):
    abpage = utils.getHtml(url, url)
    vartucurl = re.compile('<iframe.*?src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(abpage)[0]
    embedpage = utils.getHtml(vartucurl, url)
    scripturl = re.compile("src='([^']+)", re.DOTALL | re.IGNORECASE).findall(embedpage)[0]
    scripturl = "https://vartuc.com" + scripturl
    videopage = utils.getHtml(scripturl, vartucurl, vartuchdr)
    video_url = re.compile("video_url:(.*?),video", re.DOTALL | re.IGNORECASE).findall(videopage)[0]
    match = re.compile(r'(gh\w\w\w)="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(videopage)
    for repl, repl2 in match:
        video_url = video_url.replace(repl,repl2)
    video_url = video_url.replace("\"","")
    videourl = video_url.replace("+","")
    
    videourl = utils.getVideoLink(videourl, '', vartuchdr2)

    if download == 1:
        utils.downloadVideo(videourl, name)
    else:
        iconimage = xbmc.getInfoImage("ListItem.Thumb")
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})
        xbmc.Player().play(videourl, listitem)


@utils.url_dispatcher.register('323', ['url'])
def Categories(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile("<a href='/top/([^']+)'>.*?src='([^']+)' alt='([^']+)'", re.DOTALL | re.IGNORECASE).findall(cathtml)
    for catid, img, name in match:
        catpage = "http://anybunny.com/new/"+ catid
        utils.addDir(name, catpage, 321, img)
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('325', ['url'])
def Categories2(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile(r"href='/top/([^']+)'>([^<]+)</a> <a>([^)]+\))", re.DOTALL | re.IGNORECASE).findall(cathtml)
    for catid, name, videos in match:
        name = name + " [COLOR deeppink]" + videos + "[/COLOR]"
        catpage = "http://anybunny.com/new/"+ catid
        utils.addDir(name, catpage, 321, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('324', ['url'], ['keyword'])
def Search(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 324)
    else:
        title = keyword.replace(' ','_')
        searchUrl = searchUrl + title
        print "Searching URL: " + searchUrl
        List(searchUrl)
