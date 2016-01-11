import datetime
import os
import re
import sys

import xbmc,xbmcaddon,xbmcgui,xbmcplugin,xbmcgui

try:
    from addon.common.net import Net
    from addon.common.addon import Addon
except Exception, e:
    xbmc.log('Failed To Import Needed Module: %e') % e
    xbmcgui.Dialog().ok("XxTRUCOxX Import Failure", "Failed to import needed module",
                        "[COLOR red]%e[/COLOR]", "") % e

net = Net()

base_url = 'https://raw.githubusercontent.com/AiWABR/list2/master/Main.xml'
no_image = 'https://corsetsandcutlasses.files.wordpress.com/2013/12/cover-not-yet-available.jpg'
delImage = 'http://www.muziejusalka.lt/files/upload/big_D%C4%97mesio.png'
retry_image = 'http://cdn3.iconfinder.com/data/icons/3d-printing-icon-set/256/Refresh.png'

addon_id = 'plugin.video.xxtrucoxx'
addon = Addon(addon_id, sys.argv)
Addon = xbmcaddon.Addon(addon_id)

netError = os.path.join(addon.get_path(), 'resources', 'skins', 'Default', 'media', 'network_error.png')

sys.path.append(os.path.join(addon.get_path(), 'resources', 'lib'))
data_path = addon.get_profile()
cookie_file = os.path.join(data_path, 'bu.cookie')

name = addon.queries.get('name', '')
url = addon.queries.get('url', '')
alt = addon.queries.get('alt', '')
mode = addon.queries['mode']
img = addon.queries.get('img', '')

addon.log('Version %s'%addon.get_version())

import utils

def MAIN():
    Menu()


def Menu():

    html = GetUrl(base_url)
    match = 'description\=\*ANNOUNCEMENT\*\s+(\d+\/\d+\/\d+)\.(.*?)\/des'
    announce = re.search(r''+match+'', html, re.I|re.DOTALL)
    fanart = ''
    
    try:
        fanart = re.search(r'<wallpaper>(.*?)</wallpaper>', html, re.I).group(1)
    except:
        pass
    if announce:
        utils.Announce(announce.group(1),announce.group(2))
        menu = re.findall(r'<folder>(.*?)</folder>.*?<url>(.*?)</url>.*?<img>(.*?)</img>', html, re.I|re.DOTALL)
        for name, url, img in menu:
            addon.add_directory({'mode': 'CONTENT', 'url': url, 'alt': name}, {'title': name}, img=img,fanart=fanart, total_items=0)


def CONTENT(url, alt, favourite=True):
    Vitems = []
    fanart = ''
    folder_fanart = ''
    html = GetUrl(url)

    try:
        fanart = re.search(r'<wallpaper>(.*?)</wallpaper>', html, re.I|re.DOTALL).group(1)
        viewtype = str(re.search(r'<viewtype>(.*?)</viewtype>', html, re.I|re.DOTALL).group(1))
    except:
        pass


    folder_items = re.findall(r'<foldename>(.*?)</foldername>.*?<thumb>(.*?)</thumb>.*?<url>(.*?)</url>.*?<background>(.*?)</background>', html, re.I|re.DOTALL)
    items = re.findall(r'<name>(.*?)</name>.*?<thumb>(.*?)</thumb>.*?<url>(.*?)</url>', html, re.I|re.DOTALL)

    if folder_items:
        for folder_name, thumb, url, folder_fanart in folder_items:
            if folder_fanart == '':
                folder_fanart = fanart
            Vitems.append(['CONTENT', url, folder_name, '[COLOR blue]'+folder_name+'[/COLOR]', thumb, folder_fanart])

    if items:
        totalitems = len(items)
        for name, thumb, url in items:
            if thumb == '':
                thumb = no_image
            if 'NEW' in name:
                Vitems.insert(0,['resolve',url, alt, name, thumb, fanart])
            else:
                Vitems.append(['resolve',url, alt, name, thumb, fanart])
                
                
    AddMedia(Vitems)
    try:utils.SetViewType(viewtype)
    except:utils.SetViewType('50')
    
def AddMedia(Vitems):
    addon.log('AddMedia')
    totalitems = len(Vitems)
    
    for mode, url, alt, name, thumb, fanart in Vitems:
        print name
        
        if mode == 'resolve':
            addon.add_item({'mode': 'resolve', 'url': url, 'alt': alt}, {'title': name}, img = thumb, fanart=fanart, resolved=False,
                           total_items=totalitems, item_type='video', is_folder=False)
        else:
            addon.add_item({'mode': 'CONTENT', 'url': url, 'alt': alt}, {'title': alt},img=thumb,fanart=fanart, total_items=totalitems,
                           is_folder=True)            

            
def RESOLVE(url, img):
    alt_url = ''
    if re.search('\.mp4', url, re.I):
        play(url,img)

    elif re.search('\<ALT\>', url):
        r = re.split('\<ALT>', url)
        url = str(r[0])
        alt_url = str(r[1])

    '''Thank you to Eldorado and all the Users that have helped to
       keep Urlresolver updated.'''

    import urlresolver
    retry = 4
    stream_url = urlresolver.HostedMediaFile(url=url).resolve()

    if not stream_url or not isinstance(stream_url, basestring):
        if alt_url != '':
            addon.log( 'RESOLVE FAILED, %s, Using Alt, %s' %(url,alt_url)) 
            stream_url = urlresolver.HostedMediaFile(url=alt_url).resolve()

        else:
            addon.log('Resolver FAILED: %s, Trying internal'%url)
            html = net.http_GET(url).content

            if '180upload' in url:
                FNF = re.search(r'\d+px\;\"\>.*?<b\>(.*?)\<\/b\>', html,  re.I|re.DOTALL)
                if FNF:
                    addon.log('DEBUG: URL(%s)\n%s'%(url,FNF.group(1)))
                    try:addon.show_small_popup('180Upload.Com',FNF.group(1), 3000, delImage)
                    except:addon.show_small_popup('180Upload.Com','File Not Found Or Deleted', 10000, delImage)

            #print FNF.groups()                            

        #    while (retry > 0):
        #        try:
        #            retry -= 1
        #            
        #            addon.show_small_popup('Resolver Failed', 'Trying Again', 3000, retry_image)
        #            xbmc.sleep(4000)
        #            RESOLVE(url, img)
        #            addon.log('debug: Resolve Loop Attempt %s'%(str(retry)))
        #        except:
        #            pass#Need To Add Better Failed Notification Window

    play(stream_url, img)


def play(url, img):
    addon.log('PLAY: %s'%alt)
    listitem = xbmcgui.ListItem(path=str(url), iconImage=img, thumbnailImage=img)
    listitem.setProperty('IsPlayable', 'true')
    listitem.setPath(str(url))
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
    return True

def GetUrl(url):
    try:
        html = net.http_GET(url).content
    except:
        addon.show_small_popup('Network Error', 'Fetching Code Failed', 3000, netError)
        html = ''
    return html
            
if mode=='main':
    MAIN()
elif mode=='CONTENT':
    CONTENT(url, alt)
elif mode=='resolve':
    RESOLVE(url, img)
elif mode=='subs':
    SUBS(name,url,img)
elif mode=='add_fav':
    utils.add_favourite(name,url,img,alt)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

