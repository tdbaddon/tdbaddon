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

import urllib, urllib2, re, cookielib, os, sys, socket
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

import utils, sqlite3


def Main():
    utils.addDownLink('[COLOR red]Refresh Cam4 images[/COLOR]','',283,'','')
    utils.addDir('[COLOR hotpink]Featured[/COLOR]','http://www.cam4.com/featured/1',281,'',1)
    utils.addDir('[COLOR hotpink]Females[/COLOR]','http://www.cam4.com/female/1',281,'',1)
    utils.addDir('[COLOR hotpink]Couples[/COLOR]','http://www.cam4.com/couple/1',281,'',1)
    utils.addDir('[COLOR hotpink]Males[/COLOR]','http://www.cam4.com/male/1',281,'',1)
    utils.addDir('[COLOR hotpink]Transsexual[/COLOR]','http://www.cam4.com/shemale/1',281,'',1)
    xbmcplugin.endOfDirectory(utils.addon_handle)


def clean_database(showdialog=False):
    conn = sqlite3.connect(xbmc.translatePath("special://database/Textures13.db"))
    try:
        with conn:
            list = conn.execute("SELECT id, cachedurl FROM texture WHERE url LIKE '%%%s%%';" % ".systemcdn.net")
            for row in list:
                conn.execute("DELETE FROM sizes WHERE idtexture LIKE '%s';" % row[0])
                try: os.remove(xbmc.translatePath("special://thumbnails/" + row[1]))
                except: pass
            conn.execute("DELETE FROM texture WHERE url LIKE '%%%s%%';" % ".systemcdn.net")
            if showdialog:
                utils.notify('Finished','Cam4 images cleared')
    except:
        pass


def List(url, page):
    if utils.addon.getSetting("chaturbate") == "true":
        clean_database()
    listhtml = utils.getHtml(url, url)
    match = re.compile('profileDataBox"> <a href="([^"]+)".*?src="([^"]+)" title="Chat Now Free with ([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videourl, img, name in match:
        name = utils.cleantext(name)
        videourl = "http://www.cam4.com" + videourl
        utils.addDownLink(name, videourl, 282, img, '')
    if re.search('<link rel="next"', listhtml, re.DOTALL | re.IGNORECASE):
            npage = page + 1        
            url = url.replace('/'+str(page),'/'+str(npage))
            utils.addDir('Next Page ('+str(npage)+')', url, 281, '', npage)        
    xbmcplugin.endOfDirectory(utils.addon_handle)


def Playvid(url, name):
    listhtml = utils.getHtml(url, url)
    match = re.compile('data="([^"]+)".*?videoAppUrl=([^&]+)&.*?videoPlayUrl=([^&]+)&', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for swfUrl, videoAppUrl, videoPlayUrl in match:
        #videourl = '%s playpath=%s swfUrl=%s pageUrl=%s' % (videoAppUrl, videoPlayUrl, swfUrl, url)
        videourl = videoAppUrl + videoPlayUrl[videoPlayUrl.find("/", 30):]
    iconimage = xbmc.getInfoImage("ListItem.Thumb")
    listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})
    listitem.setProperty("IsPlayable","true")
    if int(sys.argv[1]) == -1:
        pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        pl.clear()
        pl.add(videourl, listitem)
        xbmc.Player().play(pl)
    else:
        listitem.setPath(str(videourl))
        xbmcplugin.setResolvedUrl(utils.addon_handle, True, listitem)

