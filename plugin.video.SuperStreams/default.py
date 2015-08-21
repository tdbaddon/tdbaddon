import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os,json,base64
import urlparse
import random
import socket, sys, os
from resources.lib.BeautifulSoup import BeautifulStoneSoup, BeautifulSoup, BeautifulSOAP
icons = xbmc.translatePath("special://home/addons/plugin.video.SuperStreams/resources/icons/")
icon = xbmc.translatePath("special://home/addons/plugin.video.SuperStreams/icon.png")
plugin_handle = int(sys.argv[1])
mode = sys.argv[2]
 
base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
 
 
 
 
AddonID ='plugin.video.SuperStreams'
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + AddonID , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + AddonID, 'icon.png'))
   
 
def categorie():
    addDir('TV KANALEN', 'plugin://plugin.video.SuperStreams/?xcat9x',icon)
    addDir('SPORT KANALEN', 'plugin://plugin.video.SuperStreams/?xcat3x',icon)
    addDir('MUZIEK KANALEN', 'plugin://plugin.video.SuperStreams/?xcat5x',icon)
    addDir('KRAAKIES KANALEN', 'plugin://plugin.video.SuperStreams/?xcat4x',icon)
    addDir('NOT IN USE', 'plugin://plugin.video.SuperStreams/?xcat1x',icon)
    addDir('NOT IN USE', 'plugin://plugin.video.SuperStreams/?xcat6x',icon)
    addDir('NOT IN USE', 'plugin://plugin.video.SuperStreams/?xcat7x',icon)
    #addDir('NOT IN USE', 'plugin://plugin.video.SuperStreams/?xcat8x',icon)
    #addDir('NOT IN USE', 'plugin://plugin.video.SuperStreams/?xcat2x',icon)
    #addDir('NOT IN USE9', 'plugin://plugin.video.SuperStreams/?xcat9x',icon)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))    
 
def addLink(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
 
def add_video_item(title,url,img):
    #url = 'plugin://plugin.video.SuperStreams/?playcloud=' + url + '***' + title + '***' + img
    url = build_url({'playcloud':url, 'videotitle':title, 'thumbnail':img})
    listitem = xbmcgui.ListItem(title, iconImage=img, thumbnailImage=img)
    listitem.setProperty('IsPlayable', 'false')
    xbmcplugin.addDirectoryItem(plugin_handle, url, listitem)
    return
 
def playginico():
    xbmcPlayer = xbmc.Player()
    url = args.get('playcloud', None)[0]
    title = args.get('videotitle', None)[0]
    img = args.get('thumbnail', None)[0]
    xbmc.executebuiltin('XBMC.Notification('+title+' , Loading Stream! ,5000,'+img+')')
    playStream(url)
   
'''
(c) By Falco
'''
def playStream(stream):
    playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
    playlist.clear()
    playlist.add(stream)
    xbmc.Player().play( playlist)
   
'''
(c) by Falco
 USAGE: build_url({'key1': 'value1','key2': 'value2','key3': 'value3'})
 '''
def build_url(query):
    return base_url + '?' + urllib.urlencode(query)
   
def getUrlParams() :
    args = urlparse.parse_qs(sys.argv[2][1:])
 
def addDir(name,url,iconimage):
    liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    liz.setProperty( "Fanart_Image", icon )
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=True)
 
 
 
def getSourceUrl(name):
    url = getUrlByName(name)
    return url
 
 
def get_url(url):
        response = urllib2.urlopen(url)
        link=response.read()
        response.close()
        return link
 
def main():    
    xcat = 0
    if 'xcat1' in mode:
        url = "http://pastebin.com/raw.php?i=vzM7hxjn"
    elif 'xcat2' in mode:
        url = "http://pastebin.com/raw.php?i=vzM7hxjn"
    elif 'xcat3' in mode:
        url = "http://pastebin.com/raw.php?i=7dbMT1uL"
    elif 'xcat4' in mode:
        url = "http://pastebin.com/raw.php?i=mWk8R9ZU"
    elif 'xcat5' in mode:
        url = "http://pastebin.com/raw.php?i=uviee7uU"
    elif 'xcat6' in mode:
        url = "http://pastebin.com/raw.php?i=vzM7hxjn"
    elif 'xcat7' in mode:
        url = "http://pastebin.com/raw.php?i=vzM7hxjn"
    elif 'xcat8' in mode:
        url = "http://pastebin.com/raw.php?i=vzM7hxjn"
    elif 'xcat9' in mode:
        url = "http://pastebin.com/raw.php?i=RgSGn43e"
    else:
        categorie()
        sys.exit(0)
 
    link = get_url(url)
    soup = BeautifulSOAP(link, convertEntities=BeautifulStoneSoup.XML_ENTITIES)
 
    items = soup.findAll("item")
    for item in items:
            try:
                videoTitle=item.title.string
            except: pass
            try:
                if item.thumbnail.string == 'none': thumbnail = icon   
                elif 'http://' in item.thumbnail.string: thumbnail = item.thumbnail.string
                else: thumbnail = icons + item.thumbnail.string  
            except:
                thumbnail = icon
            try:
                url= item.link.string
            except: pass
 
            add_video_item(videoTitle,url,thumbnail)
    xbmcplugin.endOfDirectory(plugin_handle)
    sys.exit(0)
 
 
if 'playcloud' in mode:
    playginico()
else:
    main()