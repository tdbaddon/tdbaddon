# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from resources.lib.modules.addon import Addon
import sys,os
import urlparse,urllib
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
from resources.lib.modules import control,radio
from resources.lib.modules.log_utils import log

addon = Addon('plugin.video.croatia_od', sys.argv)
addon_handle = int(sys.argv[1])


if not os.path.exists(control.dataPath):
    os.mkdir(control.dataPath)

AddonPath = addon.get_path()
IconPath = os.path.join(AddonPath , "resources/media/")
fanart = os.path.join(AddonPath + "/fanart.jpg")
def icon_path(filename):
    if 'http://' in filename:
        return filename
    return os.path.join(IconPath, filename)

args = urlparse.parse_qs(sys.argv[2][1:])
mode = args.get('mode', None)


if mode is None:
    from  resources.lib.resolvers import hrti
    hrti.get_live()
    addon.add_item({'mode': 'on_demand_tv'}, {'title':'Televizija na zahtjev'}, img=icon_path('TV.png'), fanart=fanart,is_folder=True)
    addon.add_item({'mode': 'live_tv'}, {'title':('Televizija uživo').encode('utf-8')}, img=icon_path('TV.png'), fanart=fanart,is_folder=True)
    addon.add_item({'mode': 'on_demand_radio'}, {'title':'Radio na zahtjev'}, img=icon_path('Radio.png'), fanart=fanart,is_folder=True)
    addon.add_item({'mode': 'live_radio'}, {'title':('Radio uživo').encode('utf-8')}, img=icon_path('Radio.png'), fanart=fanart,is_folder=True)
    addon.add_item({'mode': 'downloads'}, {'title':'Preuzimanja'}, img=icon_path('Downloads.png'), fanart=fanart,is_folder=True)
    addon.add_item({'mode': 'tools'}, {'title':'Alati'}, img=icon_path('tools.png'), fanart=fanart,is_folder=True)
    
    
    addon.end_of_directory()
    from resources.lib.modules import cache, control, changelog
    cache.get(changelog.get, 600000000, control.addonInfo('version'), table='changelog')
    
elif mode[0] == 'live_tv':
    sources = os.listdir(AddonPath + '/resources/lib/sources/live_tv')
    sources.remove('__init__.py')
    for source in sources:
        if '.pyo' not in source and '__init__' not in source:
            try:
                source = source.replace('.py','')
                exec "from resources.lib.sources.live_tv import %s"%source
                info = eval(source+".info()")
                addon.add_item({'mode': 'open_live_tv', 'site': info.mode}, {'title': info.name}, img=icon_path(info.icon), fanart=fanart,is_folder=True)
            except:
                pass
    addon.end_of_directory()

elif mode[0]=='live_radio':
    lista=radio.get_links_country('croatia')
    for i in range(1,len(lista)):
        if lista[i][1]!='':
            li = xbmcgui.ListItem('%s (%s)'%(lista[i][1],lista[i][3]), iconImage=icon_path('Radio.png'))
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=lista[i][0], listitem=li)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'on_demand_tv':
    sources = os.listdir(AddonPath + '/resources/lib/sources/on_demand_tv/')
    sources.remove('__init__.py')
    for source in sources:
        if '.pyo' not in source and '__init__' not in source:
            try:
                source = source.replace('.py','')
                exec "from resources.lib.sources.on_demand_tv import %s"%(source)
                info = eval(source+".info()")
                addon.add_item({'mode': 'open_demand_tv', 'site': info.mode}, {'title': info.name}, img=icon_path(info.icon), fanart=fanart,is_folder=True)
            except:
                pass
    addon.end_of_directory()

elif mode[0] == 'on_demand_radio':
    sources = os.listdir(AddonPath + '/resources/lib/sources/on_demand_radio/')
    sources.remove('__init__.py')
    for source in sources:
        if '.pyo' not in source and '__init__' not in source:
            try:
                source = source.replace('.py','')
                exec "from resources.lib.sources.on_demand_radio import %s"%(source)
                info = eval(source+".info()")
                addon.add_item({'mode': 'open_demand_radio', 'site': info.mode}, {'title': info.name}, img=icon_path(info.icon), fanart=fanart,is_folder=True)
            except:
                pass
    addon.end_of_directory()






elif mode[0] == 'open_live_tv':
    site = args['site'][0]
    try:
        next_page = args['next'][0]
    except:
        next_page = None
    exec "from resources.lib.sources.live_tv import %s"%site
    info = eval(site+".info()")
    
    if not info.categorized:
        if next_page:
            source = eval(site+".main(url=next_page)")
        else:
            source = eval(site+".main()")
        channels = source.channels()
        try: special = info.special
        except: special = False
        for channel in channels:
            if not info.multilink:
                
                if not special:
                    addon.add_video_item({'mode': 'play_special', 'url': channel[0], 'title': channel[1], 'img':channel[2], 'site': site}, {'title': channel[1]}, img=channel[2], fanart=fanart)
                else:
                    addon.add_item({'mode': 'play_folder', 'url': channel[0], 'title': channel[1], 'img':channel[2], 'site': site}, {'title': channel[1]}, img=channel[2], fanart=fanart,is_folder=True)

            else:

                addon.add_item({'mode': 'get_tv_event', 'url': channel[0],'site':site , 'title':channel[1], 'img': channel[2]}, {'title': channel[1]}, img=channel[2], fanart=fanart,is_folder=True)

        if (info.paginated and source.next_page()):
            addon.add_item({'mode': 'open_live_tv', 'site': info.mode, 'next' : source.next_page()}, {'title': 'Next Page >>'}, img=icon_path(info.icon), fanart=fanart,is_folder=True)
    else:
        source = eval(site+".main()")
        categories  = source.categories()
        for cat in categories:
            thumb = cat[2]
            if not 'http' in thumb:
                thumb = icon_path(thumb)
            addon.add_item({'mode': 'open_tv_cat', 'url': cat[0], 'site': info.mode}, {'title': cat[1]}, img=thumb, fanart=fanart, is_folder=True)


    addon.end_of_directory()




elif mode[0] == 'open_demand_tv':
    site = args['site'][0]
    try:
        next_page = args['next'][0]
    except:
        next_page = None
    exec "from resources.lib.sources.on_demand_tv import %s"%(site)
    info = eval(site+".info()")
    if not info.categorized:
        if next_page:
            source = eval(site+".main(url=next_page)")
        else:
            source = eval(site+".main()")
        items = source.items()
        for item in items:
            if info.multilink:
                addon.add_item({'mode': 'open_od_item', 'url': item[1], 'title': item[0], 'img':item[2],'site': info.mode}, {'title': item[0]}, img=item[2], fanart=fanart,is_folder=True)
            else:
                context = [('[COLOR orange]Preuzmi[/COLOR]','RunPlugin(%s?mode=download_file&url=%s&title=%s&img=%s&site=%s)' % (sys.argv[0],urllib.quote(item[1]),urllib.quote(item[0]).decode('utf-8'),urllib.quote(item[2]),urllib.quote(info.mode)))]
                addon.add_item({'mode': 'play_od_item', 'url': item[1], 'title': item[0], 'img':item[2],'site': info.mode}, {'title': item[0]}, img=item[2], fanart=fanart, contextmenu_items=context)

        if (info.paginated and source.next_page()):
            addon.add_item({'mode': 'open_demand_tv','site': info.mode, 'next' : source.next_page()}, {'title': 'Next Page >>'}, img=icon_path(info.icon), fanart=fanart,is_folder=True)
    else:
        source = eval(site+".main()")
        categories  = source.categories()
        for c in categories:
            addon.add_item({'mode': 'open_demand_cat', 'url': c[0], 'site': info.mode}, {'title': c[1]}, img=icon_path(c[2]), fanart=fanart,is_folder=True)


    addon.end_of_directory()

elif mode[0] == 'open_demand_radio':
    site = args['site'][0]
    try:
        next_page = args['next'][0]
    except:
        next_page = None
    exec "from resources.lib.sources.on_demand_radio import %s"%(site)
    info = eval(site+".info()")
    if not info.categorized:
        if next_page:
            source = eval(site+".main(url=next_page)")
        else:
            source = eval(site+".main()")
        items = source.items()
        for item in items:
            if info.multilink:
                addon.add_item({'mode': 'open_od_radio_item', 'url': item[1], 'title': item[0], 'img':item[2],'site': info.mode}, {'title': item[0]}, img=item[2], fanart=fanart,is_folder=True)
            else:
                context = [('[COLOR orange]Preuzmi[/COLOR]','RunPlugin(%s?mode=download_radio&url=%s&title=%s&img=%s&site=%s)' % (sys.argv[0],urllib.quote(item[1]),urllib.quote(item[0].encode('utf-8')),urllib.quote(item[2]),urllib.quote(info.mode)))]
                addon.add_item({'mode': 'play_od_radio_item', 'url': item[1], 'title': item[0], 'img':item[2],'site': info.mode}, {'title': item[0]}, img=item[2], fanart=fanart,contextmenu_items=context)

        if (info.paginated and source.next_page()):
            addon.add_item({'mode': 'open_demand_radio','site': info.mode, 'next' : source.next_page()}, {'title': 'Next Page >>'}, img=icon_path(info.icon), fanart=fanart,is_folder=True)
    else:
        source = eval(site+".main()")
        categories  = source.categories()
        for c in categories:
            addon.add_item({'mode': 'open_radio_demand_cat', 'url': c[0], 'site': info.mode}, {'title': c[1]}, img=icon_path(c[2]), fanart=fanart,is_folder=True)


    addon.end_of_directory()

elif mode[0] == 'open_demand_cat':
    site = args['site'][0]
    url = args['url'][0]
    try:
        next_page = args['next'][0]
    except:
        next_page = None
    exec "from resources.lib.sources.on_demand_tv import %s"%(site)
    info = eval(site+".info()")
    if next_page:
        source = eval(site+".main(url=next_page)")
    else:
        source = eval(site+".main(url=url)")
    items = source.items()
    for item in items:
        if info.multilink:
            addon.add_item({'mode': 'open_od_item', 'url': item[1], 'title': item[0], 'img':item[2],'site': info.mode}, {'title': item[0]}, img=item[2], fanart=fanart,is_folder=True)
        else:
            context = [('[COLOR orange]Preuzmi[/COLOR]','RunPlugin(%s?mode=download_file&url=%s&title=%s&img=%s&site=%s)' % (sys.argv[0],urllib.quote(item[1].encode('utf-8')),urllib.quote(item[0]).decode('utf-8'),urllib.quote(item[2]),urllib.quote(info.mode)))]
            addon.add_item({'mode': 'play_od_item', 'url': item[1], 'title': item[0], 'img':item[2],'site': info.mode}, {'title': item[0]}, img=item[2], fanart=fanart, contextmenu_items=context)

    if (info.paginated and source.next_page()):
        addon.add_item({'mode': 'open_demand_cat', 'url': source.next_page(), 'site': info.mode, 'next' : source.next_page()}, {'title': 'Next Page >>'}, img=icon_path(info.icon), fanart=fanart,is_folder=True)


    addon.end_of_directory()


elif mode[0]=='open_tv_cat':
    url = args['url'][0]
    site = args['site'][0]
    exec "from resources.lib.sources.live_tv import %s"%site
    info = eval(site+".info()")
    source = eval(site+".main()")
    channels = source.channels(url)
    try: special = info.special
    except: special = False
    for event in channels:
        if not info.multilink:
            if not special:
                addon.add_video_item({'mode': 'play_special', 'url': event[0], 'title': event[1], 'img':event[2], 'site': site}, {'title': event[1]}, img=event[2], fanart=fanart)
            else:
                addon.add_item({'mode': 'play_folder', 'url': event[0], 'title': event[1], 'img':event[2], 'site': site}, {'title': event[1]}, img=event[2], fanart=fanart,is_folder=True)

            
        else:
            addon.add_item({'mode': 'get_tv_event', 'url': event[0],'site':site , 'title':event[1], 'img': event[2]}, {'title': event[1]}, img=event[2], fanart=fanart,is_folder=True)
    
    if (info.paginated and source.next_page()):
        addon.add_item({'mode': 'open_tv_cat', 'site': info.mode, 'url': source.next_page()}, {'title': 'Next Page >>'}, img=icon_path(info.icon), fanart=fanart,is_folder=True)
    
    addon.end_of_directory()

elif mode[0]=='open_radio_demand_cat':
    url = args['url'][0]
    site = args['site'][0]
    exec "from resources.lib.sources.on_demand_radio import %s"%site
    info = eval(site+".info()")
    source = eval(site+".main()")
    channels = source.channels(url)

    for event in channels:
        if not info.multilink:
            context = [('[COLOR orange]Preuzmi[/COLOR]','RunPlugin(%s?mode=download_radio&url=%s&title=%s&img=%s&site=%s)' % (sys.argv[0],urllib.quote(event[0]),urllib.quote(event[1].encode('utf-8')),urllib.quote(event[2]),urllib.quote(info.mode)))]
            addon.add_video_item({'mode': 'play_od_radio_item', 'url': event[0],'title':event[1],'site':site, 'img': event[2]}, {'title': event[1]}, img=event[2], fanart=fanart,context=context)
        else:
            addon.add_item({'mode': 'open_od_radio_item', 'url': event[0],'site':site , 'title':event[1], 'img': event[2]}, {'title': event[1]}, img=event[2], fanart=fanart,is_folder=True)
    
    if (info.paginated and source.next_page()):
        addon.add_item({'mode': 'open_radio_demand_cat', 'site': info.mode, 'url': source.next_page()}, {'title': 'Next Page >>'}, img=icon_path(info.icon), fanart=fanart,is_folder=True)
    
    addon.end_of_directory()



elif mode[0]=='open_od_item':
    url = args['url'][0]
    title = args['title'][0]
    site = args['site'][0]
    exec "from resources.lib.sources.on_demand_tv import %s"%(site)
    info = eval(site+".info()")
    source = eval(site+".main()")
    links = source.links(url)
    for link in links:
        context = [('[COLOR orange]Preuzmi[/COLOR]','RunPlugin(%s?mode=download_file&url=%s&title=%s&img=%s&site=%s)' % (sys.argv[0],urllib.quote(link[1]),urllib.quote(link[0]).decode('utf-8'),urllib.quote(link[2]),urllib.quote(info.mode)))]
        addon.add_item({'mode': 'play_od_item', 'url': link[1], 'title': title, 'img':link[2],'site': info.mode}, {'title': link[0]}, img=link[2], fanart=fanart,contextmenu_items=context)
    
    if (info.paginated_links and source.next_link_page(url)):
        addon.add_item({'mode': 'open_od_item', 'site': info.mode, 'url': source.next_link_page(url),'title':title}, {'title': 'Next Page >>'}, img=icon_path(info.icon), fanart=fanart,is_folder=True)
    
    addon.end_of_directory()

elif mode[0]=='open_od_radio_item':
    url = args['url'][0]
    title = args['title'][0]
    site = args['site'][0]
    exec "from resources.lib.sources.on_demand_radio import %s"%(site)
    info = eval(site+".info()")
    source = eval(site+".main()")
    links = source.links(url)
    for link in links:
        context = [('[COLOR orange]Preuzmi[/COLOR]','RunPlugin(%s?mode=download_radio&url=%s&title=%s&img=%s&site=%s)' % (sys.argv[0],urllib.quote(link[1]),urllib.quote(link[0].encode('utf-8')),urllib.quote(link[2]),urllib.quote(info.mode)))]
        addon.add_item({'mode': 'play_od_radio_item', 'url': link[1], 'title': title, 'img':link[2],'site': info.mode}, {'title': link[0]}, img=link[2], fanart=fanart,contextmenu_items=context)
    
    if (info.paginated_links and source.next_link_page(url)):
        addon.add_item({'mode': 'open_od_radio_item', 'site': info.mode, 'url': source.next_link_page(url),'title':title}, {'title': 'Next Page >>'}, img=icon_path(info.icon), fanart=fanart,is_folder=True)
    
    addon.end_of_directory()




elif mode[0]=='get_tv_event':
    url = args['url'][0]
    title = args['title'][0]
    site = args['site'][0]
    img = args['img'][0]
    exec "from resources.lib.sources.live_tv import %s"%site
    info = eval(site+".info()")
    source = eval(site+".main()")
    events = source.links(url)

    for event in events:
        addon.add_video_item({'mode': 'play_special', 'url': event[0],'title':title, 'img': img, 'site':site}, {'title': event[1]}, img=img, fanart=fanart)
    addon.end_of_directory()
    


elif mode[0] == 'play':
    url = args['url'][0]
    title = args['title'][0]
    img = args['img'][0]
    if url.endswith('.ts') or 'bit.ly' in url:
        resolved = url
    else:
        import liveresolver
        resolved = liveresolver.resolve(url,cache_timeout=0,title=title)
    li = xbmcgui.ListItem(title, path=resolved)
    li.setThumbnailImage(img)
    li.setLabel(title)
    li.setProperty('IsPlayable', 'true')
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)

elif mode[0] == 'play_special':
    url = args['url'][0]
    title = args['title'][0]
    img = args['img'][0]
    site = args['site'][0]
    exec "from resources.lib.sources.live_tv import %s"%(site)
    source = eval(site+'.main()')
    resolved = source.resolve(url)
    if resolved.startswith('plugin'):
        resolved = resolved.replace('&name=Video','&name=%s'%urllib.quote(title))
        control.player.play(resolved)
    else:
        li = xbmcgui.ListItem(title, path=resolved)
        li.setThumbnailImage(img)
        li.setLabel(title)
        handle = int(sys.argv[1])
        if handle > -1:
            xbmcplugin.endOfDirectory(handle, True, False, False)
        
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)

elif mode[0] == 'play_folder':
    url = args['url'][0]
    title = args['title'][0]
    img = args['img'][0]
    site = args['site'][0]
    exec "from resources.lib.sources.live_tv import %s"%(site)
    source = eval(site+'.main()')
    resolved = source.resolve(url,title = title,icon=img)
    li = xbmcgui.ListItem(title, path=resolved)
    li.setProperty('isPlayable','true')
    li.setThumbnailImage(img)
    li.setLabel(title)
    xbmc.Player().play(resolved, listitem=li)

elif mode[0] == 'play_special_sport':
    url = args['url'][0]
    title = args['title'][0]
    img = args['img'][0]
    site = args['site'][0]
    exec "from resources.lib.sources.live_sport import %s"%(site)
    source = eval(site+'.main()')
    resolved = source.resolve(url)
    li = xbmcgui.ListItem(title, path=resolved)
    li.setThumbnailImage(img)
    li.setLabel(title)
    li.setProperty('IsPlayable', 'true')
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)


elif mode[0]=='play_od_item':
    #try:
        url = args['url'][0]
        title = args['title'][0]
        site = args['site'][0]
        img = args['img'][0]
        exec "from resources.lib.sources.on_demand_tv import %s"%(site)
        info = eval(site+".info()")
        source = eval(site+".main()")
        resolved = source.resolve(url)
        li = xbmcgui.ListItem(title, path=resolved)
        li.setThumbnailImage(img)
        li.setLabel(title)
        li.setProperty('IsPlayable', 'true')
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)
    #except:
    #    pass

elif mode[0]=='play_od_radio_item':
    url = args['url'][0]
    title = args['title'][0]
    site = args['site'][0]
    img = args['img'][0]
    exec "from resources.lib.sources.on_demand_radio import %s"%(site)
    info = eval(site+".info()")
    source = eval(site+".main()")
    resolved = source.resolve(url)
    li = xbmcgui.ListItem(title, path=resolved)
    li.setThumbnailImage(img)
    li.setLabel(title)
    li.setProperty('IsPlayable', 'true')
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)
       

elif mode[0]=='tools':
    addon.add_item({'mode': 'settings'}, {'title':'Postavke'}, img=icon_path('tools.png'), fanart=fanart,is_folder=True)
    addon.add_item({'mode': 'parental'}, {'title':'Roditeljska zastita'}, img=icon_path('tools.png'), fanart=fanart, is_folder=True)
    addon.add_item({'mode': 'clear_liveresolver_cache'}, {'title':'Ocisti cache'}, img=icon_path('tools.png'), fanart=fanart,is_folder=True)

    addon.end_of_directory()

elif mode[0]=='clear_liveresolver_cache':
    import shutil
    files = ['cache.db','loginSultanCookie','playlist.m3u','s365CookieFile.lwp','settings.db','data.zip']
    for file in files:
        filename = os.path.join(control.dataPath,file)
        if os.path.exists(filename):
            os.remove(filename)
  
    import liveresolver
    liveresolver.delete_cache()

elif mode[0]=='parental':
    from resources.lib.modules import parental
    parent = parental.Parental()
    parental_enabled = parent.isEnabled()
    adult_visible = parent.isVisible()

    
    tit2 = 'Sadrzaj nije vidljiv'
    m2 = 'Pokazi neprimjereni sadrzaj'
    color2='green'
    if adult_visible:
        tit2 = 'Sadrzaj vidljiv'
        m2 = 'Sakrij neprimjereni sadrzaj'
        color2 = 'red'

    addon.add_item({'mode': 'x'}, {'title':'[COLOR %s]%s[/COLOR]'%(color2,tit2)}, img=icon_path('tools.png'), fanart=fanart)
    password_set = parent.isPasswordSet()
    if password_set:
        addon.add_item({'mode': 'change_password'}, {'title':'Promijeni lozinku'}, img=icon_path('tools.png'), fanart=fanart, is_folder=True)
    else:
        addon.add_item({'mode': 'set_password'}, {'title':'Postavi lozinku'}, img=icon_path('tools.png'), fanart=fanart, is_folder=True)

    addon.add_item({'mode': 'toggle_visible'}, {'title':m2}, img=icon_path('tools.png'), fanart=fanart, is_folder=True)    


    addon.end_of_directory()

elif mode[0]=='toggle_visible':
    from resources.lib.modules import parental
    parent = parental.Parental()
    parental_enabled = parent.isVisible()
    if parental_enabled:
        parent.setVisible(0)
    else:
        parent.setVisible(1)



elif mode[0]=='set_password':
    from resources.lib.modules import parental
    parent = parental.Parental()
    parent.setPassword()

elif mode[0]=='change_password':
    from resources.lib.modules import parental
    parent = parental.Parental()
    parent.changePassword()


elif mode[0]=='settings':
    from resources.lib.modules import control
    control.openSettings()

######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################

elif mode[0]=='downloads':
    from resources.lib.modules import downloader
    downloader.downloader()

elif mode[0]=='stopDownload':
    from resources.lib.modules import downloader
    downloader.stopDownload()

elif mode[0]=='startDownload':
    from resources.lib.modules import downloader
    downloader.startDownload()

elif mode[0]=='startDownloadThread':
    from resources.lib.modules import downloader
    downloader.startDownloadThread()

elif mode[0]=='statusDownload':
    from resources.lib.modules import downloader
    downloader.statusDownload()

elif mode[0]=='removeDownload':
    url = args['url'][0]
    from resources.lib.modules import downloader
    downloader.removeDownload(url)

elif mode[0]=='download_file':
    url = args['url'][0]
    title = args['title'][0]
    image = args['img'][0]
    site = args['site'][0]

    exec "from resources.lib.sources.on_demand_tv import %s"%(site)
    info = eval(site+".info()")
    source = eval(site+".main()")
    url = source.resolve(url)
    log(url)
    from resources.lib.modules import downloader
    downloader.addDownload(title, url, image, resolved=True)

elif mode[0]=='download_radio':
    url = args['url'][0]
    title = args['title'][0]
    image = args['img'][0]
    site = args['site'][0]

    exec "from resources.lib.sources.on_demand_radio import %s"%(site)
    info = eval(site+".info()")
    source = eval(site+".main()")
    url = source.resolve(url)
    from resources.lib.modules import downloader
    downloader.addDownload(title, url, image, resolved=True)