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

import urllib, urllib2, re, cookielib, os, sys, socket
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

import utils, sqlite3


def Main():
    utils.addDownLink('[COLOR red]Refresh Chaturbate images[/COLOR]','',223,'','')
    utils.addDir('[COLOR hotpink]Featured[/COLOR]','https://chaturbate.com/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]Female[/COLOR]','https://chaturbate.com/female-cams/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]Couple[/COLOR]','https://chaturbate.com/couple-cams/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]Male[/COLOR]','https://chaturbate.com/male-cams/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]Transsexual[/COLOR]','https://chaturbate.com/transsexual-cams/?page=1',221,'','')
    #age
    utils.addDir('[COLOR hotpink]Teen Cams (18+)[/COLOR]','https://chaturbate.com/teen-cams/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]Teen Cams (18+) - Female[/COLOR]','https://chaturbate.com/teen-cams/female/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]Teen Cams (18+) - Couple[/COLOR]','https://chaturbate.com/teen-cams/couple/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]Teen Cams (18+) - Male[/COLOR]','https://chaturbate.com/teen-cams/male/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]Teen Cams (18+) - Transsexual[/COLOR]','https://chaturbate.com/teen-cams/transsexual/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]18 to 21 Cams[/COLOR]','https://chaturbate.com/18to21-cams/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]18 to 21 Cams - Female[/COLOR]','https://chaturbate.com/18to21-cams/female/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]18 to 21 Cams - Couple[/COLOR]','https://chaturbate.com/18to21-cams/couple/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]18 to 21 Cams - Male[/COLOR]','https://chaturbate.com/18to21-cams/male/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]18 to 21 Cams - Transsexual[/COLOR]','https://chaturbate.com/18to21-cams/transsexual/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]20 to 30 Cams[/COLOR]','https://chaturbate.com/20to30-cams/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]20 to 30 Cams - Female[/COLOR]','https://chaturbate.com/20to30-cams/female/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]20 to 30 Cams - Couple[/COLOR]','https://chaturbate.com/20to30-cams/couple/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]20 to 30 Cams - Male[/COLOR]','https://chaturbate.com/20to30-cams/male/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]20 to 30 Cams - Transsexual[/COLOR]','https://chaturbate.com/20to30-cams/transsexual/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]30 to 50 Cams[/COLOR]','https://chaturbate.com/30to50-cams/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]30 to 50 Cams - Female[/COLOR]','https://chaturbate.com/30to50-cams/female/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]30 to 50 Cams - Couple[/COLOR]','https://chaturbate.com/30to50-cams/couple/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]30 to 50 Cams - Male[/COLOR]','https://chaturbate.com/30to50-cams/male/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]30 to 50 Cams - Transsexual[/COLOR]','https://chaturbate.com/30to50-cams/transsexual/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]Mature Cams (50+)[/COLOR]','https://chaturbate.com/mature-cams/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]Mature Cams (50+) - Female[/COLOR]','https://chaturbate.com/mature-cams/female/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]Mature Cams (50+) - Couple[/COLOR]','https://chaturbate.com/mature-cams/couple/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]Mature Cams (50+) - Male[/COLOR]','https://chaturbate.com/mature-cams/male/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]Mature Cams (50+) - Transsexual[/COLOR]','https://chaturbate.com/mature-cams/transsexual/?page=1',221,'','')    
    #status
    utils.addDir('[COLOR hotpink]HD Cams[/COLOR]','https://chaturbate.com/hd-cams/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]HD Cams - Female[/COLOR]','https://chaturbate.com/hd-cams/female/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]HD Cams - Couple[/COLOR]','https://chaturbate.com/hd-cams/couple/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]HD Cams - Male[/COLOR]','https://chaturbate.com/hd-cams/male/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]HD Cams - Transsexual[/COLOR]','https://chaturbate.com/hd-cams/transsexual/?page=1',221,'','')   
    #region
    utils.addDir('[COLOR hotpink]North American Cams[/COLOR]','https://chaturbate.com/north-american-cams/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]North American Cams - Female[/COLOR]','https://chaturbate.com/north-american-cams/female/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]North American Cams - Couple[/COLOR]','https://chaturbate.com/north-american-cams/couple/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]North American Cams - Male[/COLOR]','https://chaturbate.com/north-american-cams/male/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]North American Cams - Transsexual[/COLOR]','https://chaturbate.com/north-american-cams/transsexual/?page=1',221,'','') 
    utils.addDir('[COLOR hotpink]Other Region Cams[/COLOR]','https://chaturbate.com/other-region-cams/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]Other Region Cams - Female[/COLOR]','https://chaturbate.com/other-region-cams/female/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]Other Region Cams - Couple[/COLOR]','https://chaturbate.com/other-region-cams/couple/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]Other Region Cams - Male[/COLOR]','https://chaturbate.com/other-region-cams/male/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]Other Region Cams - Transsexual[/COLOR]','https://chaturbate.com/other-region-cams/transsexual/?page=1',221,'','') 
    utils.addDir('[COLOR hotpink]Euro Russian Cams[/COLOR]','https://chaturbate.com/euro-russian-cams/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]Euro Russian Cams - Female[/COLOR]','https://chaturbate.com/euro-russian-cams/female/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]Euro Russian Cams - Couple[/COLOR]','https://chaturbate.com/euro-russian-cams/couple/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]Euro Russian Cams - Male[/COLOR]','https://chaturbate.com/euro-russian-cams/male/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]Euro Russian Cams - Transsexual[/COLOR]','https://chaturbate.com/euro-russian-cams/transsexual/?page=1',221,'','') 
    utils.addDir('[COLOR hotpink]Philippines Cams[/COLOR]','https://chaturbate.com/philippines-cams/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]Philippines Cams - Female[/COLOR]','https://chaturbate.com/philippines-cams/female/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]Philippines Cams - Couple[/COLOR]','https://chaturbate.com/philippines-cams/couple/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]Philippines Cams - Male[/COLOR]','https://chaturbate.com/philippines-cams/male/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]Philippines Cams - Transsexual[/COLOR]','https://chaturbate.com/philippines-cams/transsexual/?page=1',221,'','') 
    utils.addDir('[COLOR hotpink]Asian Cams[/COLOR]','https://chaturbate.com/asian-cams/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]Asian Cams - Female[/COLOR]','https://chaturbate.com/asian-cams/female/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]Asian Cams - Couple[/COLOR]','https://chaturbate.com/asian-cams/couple/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]Asian Cams - Male[/COLOR]','https://chaturbate.com/asian-cams/male/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]Asian Cams - Transsexual[/COLOR]','https://chaturbate.com/asian-cams/transsexual/?page=1',221,'','') 
    utils.addDir('[COLOR hotpink]South American Cams[/COLOR]','https://chaturbate.com/south-american-cams/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]South American Cams - Female[/COLOR]','https://chaturbate.com/south-american-cams/female/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]South American Cams - Couple[/COLOR]','https://chaturbate.com/south-american-cams/couple/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]South American Cams - Male[/COLOR]','https://chaturbate.com/south-american-cams/male/?page=1',221,'','')
    utils.addDir('[COLOR hotpink]South American Cams - Transsexual[/COLOR]','https://chaturbate.com/south-american-cams/transsexual/?page=1',221,'','')    
    xbmcplugin.endOfDirectory(utils.addon_handle)


def List(url, page=None):
    if utils.addon.getSetting("chaturbate") == "true":
        clean_database()
    listhtml = utils.getHtml2(url)
    match = re.compile(r'<li>\s+<a href="([^"]+)".*?src="([^"]+)".*?<div[^>]+>([^<]+)</div>.*?href[^>]+>([^<]+)<.*?age[^>]+>([^<]+)<', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videopage, img, status, name, age in match:
        name = utils.cleantext(name)
        status = status.replace("\n","").strip()
        name = name + " [" + status + "] Age: [COLOR deeppink]" + age + "[/COLOR]"
        videopage = "https://chaturbate.com" + videopage
        utils.addDownLink(name, videopage, 222, img, '')
    if len(match) == 90:
        try:
            page = page + 1
            nextp=re.compile('<a href="([^"]+)" class="next', re.DOTALL | re.IGNORECASE).findall(listhtml)
            next = "https://chaturbate.com" + nextp[0]
            utils.addDir('Next Page ('+str(page)+')', next, 221,'', page)
        except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)


def clean_database(showdialog=False):
    conn = sqlite3.connect(xbmc.translatePath("special://database/Textures13.db"))
    try:
        with conn:
            list = conn.execute("SELECT id, cachedurl FROM texture WHERE url LIKE '%%%s%%';" % ".highwebmedia.com")
            for row in list:
                conn.execute("DELETE FROM sizes WHERE idtexture LIKE '%s';" % row[0])
                try: os.remove(xbmc.translatePath("special://thumbnails/" + row[1]))
                except: pass
            conn.execute("DELETE FROM texture WHERE url LIKE '%%%s%%';" % ".highwebmedia.com")
            if showdialog:
                utils.notify('Finished','Chaturbate images cleared')
    except:
        pass


def Playvid(url, name):
    listhtml = utils.getHtml2(url)
    match = re.compile("<video.*?src='([^']+)'", re.DOTALL | re.IGNORECASE).findall(listhtml)
    if match:
        videourl = match[0]
        videourl = videourl + '|User-Agent=' + utils.USER_AGENT
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
    else:
        utils.notify('Oh oh','Couldn\'t find a playable webcam link')

