# -*- coding: utf-8 -*-

import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin
import xbmcaddon
import urllib2
import re
from BeautifulSoup import BeautifulSoup as bs
import itertools
from lib.sources import *
from lib.modules.utils import *
from lib.modules.webutils import *
import xbmcvfs,os

my_addon = xbmcaddon.Addon()
addon_path = my_addon.getAddonInfo('path')
addon_id= my_addon.getAddonInfo('id')
IconPath = addon_path + "/resources/images/"
favourites_path = xbmc.translatePath("special://profile/addon_data/"+addon_id)
favourites_file= os.path.join(favourites_path,'favourites.xml')
if not os.path.exists(favourites_path):
    os.makedirs(favourites_path)

if not xbmcvfs.exists(favourites_file):
    f = xbmcvfs.File (favourites_file, 'w')
    f.close()

def icon_path(filename):
    return IconPath + filename


base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

mode=args.get('mode',None)


if mode is None :
    url = build_url({'mode': 'vod'})
    li = xbmcgui.ListItem('Televizija na zahtjev', iconImage=icon_path('TV.png'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'live1'})

    li = xbmcgui.ListItem('Televizija uživo', iconImage=icon_path('TV.png'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'radioNZ'})
    li = xbmcgui.ListItem('Radio na zahtjev', iconImage=icon_path('Radio.png'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'radio_live'})
    li = xbmcgui.ListItem('Radio uživo', iconImage=icon_path('Radio.png'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    
    url=my_addon.getSetting('downloads_folder')
    if url=='':
        pass


    else:
        li = xbmcgui.ListItem('Preuzimanja', iconImage=icon_path('Downloads.png'))
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)

    #url = build_url({'mode': 'favoriti'})
    #li = xbmcgui.ListItem('Favoriti', iconImage=icon_path('Favoriti.png'))
    #xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
    #                            listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)


elif mode[0]=='vod':
    url = build_url({'mode': 'rtl', 'foldername': 'RTL Sada'})
    li = xbmcgui.ListItem('RTL Sada', iconImage=icon_path('RTL Sada.jpg'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'hrt', 'foldername': 'HRT Emisije'})
    li = xbmcgui.ListItem('HRT Emisije' ,iconImage=icon_path('HRT.gif'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)


    url = build_url({'mode': 'mreza', 'foldername': 'Mreza TV'})
    li = xbmcgui.ListItem('Mreza TV' ,iconImage=icon_path('Mreza.jpg'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'jabuka', 'foldername': 'Jabuka TV'})
    li = xbmcgui.ListItem('Jabuka TV' ,iconImage=icon_path('Jabuka.png'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'n1', 'foldername': 'N1'})
    li = xbmcgui.ListItem('N1 Televizija' ,iconImage=icon_path('N1.png'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'aj_balkans', 'foldername': 'Al Jazeera'})
    li = xbmcgui.ListItem('Al Jazeera Balkans' ,iconImage=icon_path('AJB.png'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'shows', 'foldername': 'serije'})
    li = xbmcgui.ListItem('Serijex.com ' ,iconImage=icon_path('Serijex.jpg'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    url = build_url({'mode': 'serije_balkanje', 'foldername': 'serije'})
    li = xbmcgui.ListItem('Serije (Balkanje) ' ,iconImage=icon_path('Balkanje.png'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'serije_movienized', 'foldername': 'serije'})
    li = xbmcgui.ListItem('Serije (Movienized) ' ,iconImage=icon_path('Movienized.jpg'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'crtanionline', 'foldername': 'serije'})
    li = xbmcgui.ListItem('crtanionline.net' ,iconImage='')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)


#####################################################################################################################################################################
#RTL
#####################################################################################################################################################################


elif mode[0]=='rtl':

    url = build_url({'mode': 'rtl_az'})
    li = xbmcgui.ListItem('Cijeli program A-Ž' ,iconImage=icon_path('RTL Sada.jpg'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)

    url = build_url({'mode': 'rtl_cats'})
    li = xbmcgui.ListItem('Tip sadržaja' ,iconImage=icon_path('RTL Sada.jpg'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)

    url = build_url({'mode': 'rtl_kanali'})
    li = xbmcgui.ListItem('Kanali' ,iconImage=icon_path('RTL Sada.jpg'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)

    
    xbmcplugin.endOfDirectory(addon_handle)


elif mode[0]=='rtl_cats':
    cats=rtl_get_cats()
    for cat in cats:
        url = build_url({'mode': 'rtl_open_cat','tag':cat[1]})
        li = xbmcgui.ListItem(cat[0] ,iconImage=icon_path('RTL Sada.jpg'))
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)
    

    url = build_url({'mode': 'get_it_rtl', 'site':'http://www.sada.rtl.hr/filmovi/'})
    li = xbmcgui.ListItem('Filmovi' ,iconImage=icon_path('RTL Sada.jpg'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='rtl_kanali':
    cats=rtl_get_chans()
    for cat in cats:
        url = build_url({'mode': 'rtl_open_kan','tag':cat[1]})
        li = xbmcgui.ListItem(cat[0] ,iconImage=icon_path('RTL Sada.jpg'))
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)
    

    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0]=='rtl_open_cat':
    id=args['tag'][0]
    shows=rtl_get_from_cat(id)
    for i in range(len(shows)):
        url = build_url({'mode': 'get_it_rtl', 'site':'%s'%shows[i][1]})
        li = xbmcgui.ListItem('%s'%shows[i][0] ,iconImage=shows[i][2])
        #fav_uri = build_url({'mode': 'add_favourite', 'name': '%s'%(shows[i][0].encode('utf-8')), 'url': url, 'thumb':shows[i][2]})


        #li.addContextMenuItems([('Dodaj u favorite','RunPlugin(%s)'%fav_uri)])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='rtl_open_kan':
    id=args['tag'][0]
    shows=rtl_get_from_chan(id)
    for i in range(len(shows)):
        url = build_url({'mode': 'get_it_rtl', 'site':'%s'%shows[i][1]})
        li = xbmcgui.ListItem('%s'%shows[i][0] ,iconImage=shows[i][2])
        #fav_uri = build_url({'mode': 'add_favourite', 'name': '%s'%(shows[i][0].encode('utf-8')), 'url': url, 'thumb':shows[i][2]})


        #li.addContextMenuItems([ ('Dodaj u favorite','RunPlugin(%s)'%fav_uri)])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)


elif mode[0]=='rtl_az':
    shows=get_all_show_rtl()
    for i in range(len(shows)):
        name=shows[i][0].encode('utf-8')

        url = build_url({'mode': 'get_it_rtl', 'site':'%s'%shows[i][1]})
        li = xbmcgui.ListItem('%s'%shows[i][0] ,iconImage=shows[i][2])
        #fav_uri = build_url({'mode': 'add_favourite', 'name': name, 'url': url, 'thumb':shows[i][2]})


        #li.addContextMenuItems([ ('Dodaj u favorite','RunPlugin(%s)'%fav_uri)])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='get_it_rtl':
    site=args['site'][0]
    lista=rtl_get_it(site)
    for i in range(len(lista)):
        name=lista[i][1]
        name=name.encode('utf-8')


        li = xbmcgui.ListItem('%s'%lista[i][1], iconImage='%s'%lista[i][2])
        li.setProperty("Fanart_Image", lista[i][3])
        link=resolve_rtl_link(lista[i][0])

        down_uri = build_url({'mode': 'download_resolved', 'foldername': name, 'link': link})
        #fav_uri = build_url({'mode': 'add_favourite', 'name': name, 'url': link, 'thumb':lista[i][2]})


        li.addContextMenuItems([ ('Preuzmi video', 'RunPlugin(%s)'%down_uri)])#,
                                #('Dodaj u favorite','RunPlugin(%s)'%fav_uri)])
        
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=link, listitem=li)

    xbmcplugin.endOfDirectory(addon_handle)





elif mode[0]=='download_resolved':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link=dicti['link'][0]
    name=dicti['foldername'][0]
    uri=link
    #name=name.rstrip('.').replace(' ','_').replace('.','_').replace(':','_').replace(';','').replace("'",'').replace('"','').replace('__','_')

    download(name,uri)
#####################################################################################################################################################################
#HRT
#####################################################################################################################################################################
elif mode[0] == 'hrt':

    url = build_url({'mode': 'hrt_all'})
    li = xbmcgui.ListItem('Sve emisije' ,iconImage=icon_path('HRT.gif'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    letters=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','R','S','Š','T','V','Z']
    for i in range(len(letters)):
        url = build_url({'mode': 'hrt_open_letter','letter':'%s'%letters[i], 'foldername': 'letter'})
        li = xbmcgui.ListItem('%s'%letters[i] ,iconImage=icon_path('HRT.gif'))
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='hrt_all':
        # letters=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','R','S','Š','T','V','Z']
        # for letter in letters:
        shows=hrt_get_all()
        for i in range(len(shows)):
            url = build_url({'mode': 'open_show_hrt', 'link': '%s'%shows[i][0]})
            title=shows[i][1].encode('utf-8')

            li = xbmcgui.ListItem('%s'%shows[i][1] ,iconImage=icon_path('HRT.gif'))
            #fav_uri = build_url({'mode': 'add_favourite', 'name': '%s'%(title), 'url': url})


            #li.addContextMenuItems([ ('Dodaj u favorite','RunPlugin(%s)'%fav_uri)])
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)
        xbmcplugin.endOfDirectory(addon_handle)


elif mode[0]=='hrt_open_letter':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    letter=dicti['letter'][0]

    shows=hrt_get_shows_letter(letter)
    for i in range(len(shows)):
        url = build_url({'mode': 'open_show_hrt', 'link': '%s'%shows[i][0]})
        li = xbmcgui.ListItem('%s'%shows[i][1] ,iconImage=icon_path('HRT.gif'))
        title=shows[i][1].encode('utf-8')
        #fav_uri = build_url({'mode': 'add_favourite', 'name': title, 'url': url})
        #li.addContextMenuItems([ ('Dodaj u favorite','RunPlugin(%s)'%fav_uri)])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='open_show_hrt':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    url=dicti['link'][0]

    my_addon = xbmcaddon.Addon()
    broj_rez = my_addon.getSetting('broj_rezultata')

    episode=[]
    episode=get_episodes_hrt(url,broj_rez)
    if len(episode)!=0:
        name=get_show_name(url)


    for i in range(len(episode)):
        title=episode[i][1]
        title=remove_tags(title)
        try:
            li = xbmcgui.ListItem('%s: %s'%(name,title), iconImage=icon_path('HRT.gif'))
            down_uri = build_url({'mode': 'download_hrt', 'foldername': '%s: %s'%(name,title), 'link': '%s'%episode[i][0]})
        except:
            li = xbmcgui.ListItem('%s'%(title), iconImage=icon_path('HRT.gif'))
            down_uri = build_url({'mode': 'download_hrt', 'foldername': '%s'%(title), 'link': '%s'%episode[i][0]})

        #fav_uri = build_url({'mode': 'add_favourite', 'name': normal(title).encode('utf-8'), 'url': url})



        li.addContextMenuItems([ ('Preuzmi video', 'RunPlugin(%s)'%down_uri)])#,
            #('Dodaj u favorite','RunPlugin(%s)'%fav_uri)])

        #uri=a.get_episode_link(episode[i][0])
        try:
            uri = build_url({'mode': 'play_hrt', 'foldername': '%s: %s'%(name,title), 'link': '%s'%episode[i][0]})
        except:
            uri = build_url({'mode': 'play_hrt', 'foldername': '%s'%title, 'link': '%s'%episode[i][0]})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=uri, listitem=li, isFolder=True)


    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='play_hrt':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link=dicti['link'][0]
    name=dicti['foldername'][0]
    uri=get_episode_link(link)

    li = xbmcgui.ListItem('%s'%name)
    li.setInfo('video', { 'title': '%s'%name })
    player = xbmc.Player()
    player.play(item=uri, listitem=li)

elif mode[0]=='download_hrt':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link=dicti['link'][0]
    name=dicti['foldername'][0]
    uri=get_episode_link(link)
    #name=name.rstrip('.').replace(' ','_').replace('.','_').replace(':','_').replace(';','').replace("'",'').replace('"','').replace('__','_')

    download(name,uri)
#####################################################################################################################################################################
#MREZA
#####################################################################################################################################################################
elif mode[0]=='mreza':

    mreza_cats=[['Informativne emisije', 'videoteka v-info-emisije'], 
                ['Zabavno - mozaični program', 'videoteka v-zm-program'], ['Ostale emisije', 'videoteka v-ostale-emisije']]
    for i in range(len(mreza_cats)):
        url = build_url({'mode': 'open_mreza_cat', 'tag': '%s'%mreza_cats[i][1]})
        li = xbmcgui.ListItem('%s'%mreza_cats[i][0],iconImage=icon_path('Mreza.jpg'))
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)
        
    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0]=='open_mreza_cat':

    dicti=urlparse.parse_qs(sys.argv[2][1:])
    tag=dicti['tag'][0]
    emisije=get_shows_mreza(tag)
    
    for i in range(len(emisije)):    
        url = build_url({'mode': 'open_show_mreza', 'link':'%s'%emisije[i][0]})
        li = xbmcgui.ListItem('%s'%emisije[i][1] ,iconImage=emisije[i][2])
        #fav_uri = build_url({'mode': 'add_favourite', 'name': emisije[i][1].encode('utf-8'), 'url': url,'thumb':emisije[i][2]})
        #li.addContextMenuItems([ ('Dodaj u favorite','RunPlugin(%s)'%fav_uri)])

        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                               listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='open_show_mreza':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link=dicti['link'][0]

    epizode=get_episodes_mreza(link)

    for i in range (len(epizode)):
        li = xbmcgui.ListItem('%s'%(epizode[i][1].decode('utf-8')), iconImage='%s'%epizode[i][2])

        down_uri = build_url({'mode': 'download_resolved', 'foldername': '%s'%(epizode[i][1]), 'link': '%s'%epizode[i][0]})
        #fav_uri = build_url({'mode': 'add_favourite', 'name': normal(epizode[i][1]).encode('utf-8'), 'url': epizode[i][0],'thumb':epizode[i][2]})
        li.addContextMenuItems([('Preuzmi video', 'RunPlugin(%s)'%down_uri)])#, ('Dodaj u favorite','RunPlugin(%s)'%fav_uri)])


        xbmcplugin.addDirectoryItem(handle=addon_handle, url=epizode[i][0], listitem=li)
    xbmcplugin.endOfDirectory(addon_handle)
#####################################################################################################################################################################
#JABUKA
#####################################################################################################################################################################
elif mode[0]=='jabuka':
    otv_emisije=[ ['2 u 9','http://videoteka.jabukatv.hr/index.php?option=com_hwdmediashare&view=category&id=9&Itemid=114'],['Hrana i vino','http://videoteka.jabukatv.hr/index.php?option=com_hwdmediashare&view=category&id=10&Itemid=115'],
                    ['Veto','http://videoteka.jabukatv.hr/index.php?option=com_hwdmediashare&view=category&id=11&Itemid=116'] ]

    for i in range(len(otv_emisije)):
        url = build_url({'mode': 'open_jabuka', 'link': '%s'%otv_emisije[i][1]})
        li = xbmcgui.ListItem('%s'%otv_emisije[i][0] ,iconImage=icon_path('Jabuka.png'))
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='open_jabuka':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link=dicti['link'][0]
    lista=get_video_links_from_jabuka_show(link)
    
    for i in range(len(lista)):
        li = xbmcgui.ListItem(' %s'%lista[i][1], iconImage=icon_path('Jabuka.png'))
        link=resolve_otv_link(lista[i][0])

        down_uri = build_url({'mode': 'download_resolved', 'foldername': '%s'%(lista[i][1].encode('utf-8')), 'link': '%s'%link})
        li.addContextMenuItems([ ('Preuzmi video', 'RunPlugin(%s)'%down_uri)])

        xbmcplugin.addDirectoryItem(handle=addon_handle, url=link, listitem=li)

    xbmcplugin.endOfDirectory(addon_handle)

#####################################################################################################################################################################
#N1
#####################################################################################################################################################################
elif mode[0]=='n1':
    shows=n1_shows()
    for show in shows:
        url = build_url({'mode': 'n1_open_show','url':show[1]})
        li = xbmcgui.ListItem(show[0] ,iconImage=show[2])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)

    
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='n1_open_show':
    url=args['url'][0]
    eps=get_n1_eps(url)
    for ep in eps:
        url = build_url({'mode': 'n1_open_ep','url':ep[1]})
        li = xbmcgui.ListItem(ep[0] ,iconImage=ep[2])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)

    
    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0]=='n1_open_ep':
    url=args['url'][0]
    resolved=resolve_n1(url)
    xbmc.Player().play(resolved)
#####################################################################################################################################################################
#AL JAZEERA
#####################################################################################################################################################################
elif mode[0]=='aj_balkans':
    shows=[['Dokumentarci','http://balkans.aljazeera.net/video/posljednji/DOKUMENTARCI'],['Recite Aljazeeri','http://balkans.aljazeera.net/video/posljednji/RECITE%20ALJAZEERI'],
            ['Kontekst','http://balkans.aljazeera.net/video/posljednji/Kontekst'],['Oni pobjeđuju','http://balkans.aljazeera.net/video/posljednji/ONI%20POBJE%C4%90UJU'],
            ['Nove emisije','http://balkans.aljazeera.net/video/posljednji/NOVE%20EMISIJE']]
    for show in shows:
        url = build_url({'mode': 'aj_open_show','url':show[1]})
        li = xbmcgui.ListItem(show[0] ,iconImage=icon_path('AJB.png'))
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)

    
    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0]=='aj_open_show':
    url=args['url'][0]
    urly=url
    eps,next_page=aj_get_eps(url)
    
    for show in eps:
        url = build_url({'mode': 'aj_open_ep','url':show[0], 'img':show[1]})
        li = xbmcgui.ListItem(show[2] ,iconImage=show[1])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)
    if next_page!=0:
        url = build_url({'mode': 'aj_open_show','url':next_page})
        li = xbmcgui.ListItem('Sljedeća stranica >>',iconImage=icon_path('AJB.png'))
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                        listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='aj_open_ep':
    url='http://balkans.aljazeera.net'+ args['url'][0]
    img=args['img'][0]
    link=resolve_aj(url)
    meta,desc=aj_get_meta(url)
    li = xbmcgui.ListItem(meta,iconImage=img)
    li.setThumbnailImage(img)
    li.setInfo('video' ,{'plot':desc,'plotoutline':desc})
    if 'brightcove' in link:
        import YDStreamExtractor
        YDStreamExtractor.disableDASHVideo(True) 
        vid = YDStreamExtractor.getVideoInfo(link,quality=1) 
        resolved = vid.streamURL() 
        xbmc.Player().play(listitem=li,item=resolved)

    else:
        resolved=link

        xbmc.Player().play(resolved)

#####################################################################################################################################################################
#serijex.com
#####################################################################################################################################################################

elif mode[0]=='shows':
    shows=get_tvshows_sx()
    for i in range(len(shows)):
        title=shows[i][0]
        year=shows[i][1]
        slug=shows[i][2]
        imdb=shows[i][3]
        trakt=shows[i][4]
        thumb=shows[i][5]

        url = build_url({'mode': 'open_show', 'foldername': '%s'%title, 'slug':'%s'%slug, 'imdb':'%s'%imdb, 'trakt':'%s'%trakt, 'year':'%s'%year})
        li = xbmcgui.ListItem('%s (%s)'%(title,year), iconImage=thumb)

        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li,isFolder=True)

    
    
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='open_show':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    title_show=dicti['foldername'][0]
    slug=dicti['slug'][0]
    imdb=dicti['imdb'][0]
    trakt=dicti['trakt'][0]
    show_year=dicti['year'][0]

    seasons=get_seasons_sx(slug)

    for i in range(len(seasons)):

        title=seasons[i][0]
        if title!='Season 0':
            id=seasons[i][1]
            thumb=seasons[i][2]
            number=seasons[i][3]
            url = build_url({'mode': 'open_season', 'foldername': '%s'%title,'year':'%s'%show_year, 'show_title':'%s'%title_show,'id':'%s'%number, 'slug':'%s'%slug})
            li = xbmcgui.ListItem('%s'%title, iconImage=thumb)

            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                        listitem=li,isFolder=True)


    xbmcplugin.endOfDirectory(addon_handle)



elif mode[0]=='open_season':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    title_show=dicti['show_title'][0]
    slug=dicti['slug'][0]
    id=dicti['id'][0]
    show_year=dicti['year'][0]
    episodes=get_episodes_sx(slug,id)
    for i in range(len(episodes)):
        title=episodes[i][0]
        season=episodes[i][1]
        number=episodes[i][2]
        id=episodes[i][3]
        thumb=episodes[i][4]
        url = build_url({'mode': 'open_episode','foldername':'%s'%title, 'thumb':'%s'%thumb, 'id':'%s'%id,'slug':'%s'%slug, 'year':'%s'%show_year,'show_title':'%s'%title_show,'season':'%s'%season, 'number':'%s'%number})
        li = xbmcgui.ListItem('%sx%s %s'%(season,number,title), iconImage=thumb)

        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li,isFolder=True)


    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='open_episode':
    
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    title_show=dicti['show_title'][0]
    title=dicti['foldername'][0]
    slug=dicti['slug'][0]
    season=dicti['season'][0]
    number=dicti['number'][0]
    show_year=dicti['year'][0]
    thumb=dicti['thumb'][0]
    link=get_episode_link_sx(slug,season,number,show_year)
    
    links=get_links_sx(link)

    links=convert_linksx(links)
    hosts=get_host_names(links)
    dialog = xbmcgui.Dialog()
    index = dialog.select('Odaberite link:', hosts)

    prob=['Film je u vise djelova na youtube-u.','Posjetite filmovita.com']
    if index>-1 and links!=prob:
            try:
        
                link=links[index]
                import urlresolver
                resolved=urlresolver.resolve(link)

                li = xbmcgui.ListItem('%s'%title)
                li.setInfo('video', {'tvshowtitle':'%s'%title_show,
                                    'title':'%s'%title,
                                    'season':'%s'%season,
                                    'episode':'%s'%number
                                    
                                        })
                li.setThumbnailImage(thumb)
                
                li.setProperty('IsPlayable', 'true')

                xbmc.Player().play(item=resolved, listitem=li)
            except:
                Notify("small","Info","Video nije dostupan","")

    else:
        pass
#####################################################################################################################################################################
#BALKANJE
#####################################################################################################################################################################
elif mode[0]=='serije_balkanje':


    url = build_url({'mode': 'serije_novo1', 'foldername': 'serije'})
    li = xbmcgui.ListItem('Zadnje dodane epizode' ,iconImage=icon_path('Balkanje.png'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    
    url = build_url({'mode': 'serije_cat', 'foldername': 'hrv'})
    li = xbmcgui.ListItem('Domaće serije' ,iconImage=icon_path('Balkanje.png'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'serije_cat', 'foldername': 'esp'})
    li = xbmcgui.ListItem('Španjolske serije' ,iconImage=icon_path('Balkanje.png'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    url = build_url({'mode': 'serije_cat', 'foldername': 'tur'})
    li = xbmcgui.ListItem('Turske serije' ,iconImage=icon_path('Balkanje.png'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'lzn', 'foldername': 'lud'})
    li = xbmcgui.ListItem('Lud, zbunjen, normalan' ,iconImage='http://bh-info.com/wp-content/uploads/2015/04/lud.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='serije_cat':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    cat=dicti['foldername'][0]
    
    if cat=='hrv':
        serije_balk=get_show_list_cod('https://raw.githubusercontent.com/natko1412/cod/master/domace.txt')

    elif cat=='esp':
        serije_balk=get_show_list_cod('https://github.com/natko1412/cod/raw/master/spanjolske.txt')

    elif cat=='tur':
        serije_balk=get_show_list_cod('https://github.com/natko1412/cod/raw/master/turske.txt')

    for i in range(len(serije_balk)):
        url = build_url({'mode': 'otvori_seriju_balkanje', 'link':'%s'%serije_balk[i][1], 'page':'1'})
        li = xbmcgui.ListItem('%s'%serije_balk[i][0] ,iconImage='%s'%serije_balk[i][2])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)


    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0]=='otvori_seriju_balkanje':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link=dicti['link'][0]
    page=dicti['page'][0]

    url=link+'%s-date.html'%page
    nadi_epizode(url,page,link)

elif mode[0]=='serije_novo1':

    url='http://www.balkanje.com/newvideos.html'

    html=read_url(url)

    soup=bs(html)
    tag=soup.find('ul',{'class':'pm-ul-new-videos thumbnails'})

    lis=tag.findAll('li')
    results=[]
    for i in range(len(lis)):
        thumb=lis[i].find('img')['src']
        item=lis[i].find('h3').find('a')
        link=item['href']
        title=item['title']
        
        url = build_url({'mode': 'otvori_epizodu', 'link':'%s'%link, 'title':'%s'%title, 'thumb':'%s'%thumb})
        li = xbmcgui.ListItem('%s '%(title), iconImage=thumb)
        down_uri = build_url({'mode': 'download_epizodu', 'title': '%s'%(title.encode('ascii','ignore')), 'link': link})

        li.addContextMenuItems([ ('Preuzmi video', 'RunPlugin(%s)'%down_uri)])

        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li,isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)
    
elif mode[0]=='otvori_epizodu':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link=dicti['link'][0]
    title=dicti['title'][0]
    thumb=dicti['thumb'][0]

    otvori_epizodu(link,title,thumb)
elif mode[0]=='download_epizodu':
    url=args['link'][0]
    title=args['title'][0]
    download_epizodu(title,url)

elif mode[0]=='lzyn':
    godine=[2015,2014,2013,2012,2011,2010,2009,2008,2007]


    for i in range(len(godine)):
        url = build_url({'mode': 'otvori_lzn_godinu', 'godina': '%s'%str(godine[i])})
        li = xbmcgui.ListItem('%s'%str(godine[i]) ,iconImage='http://bh-info.com/wp-content/uploads/2015/04/lud.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0]=='lzn':
    # dicti=urlparse.parse_qs(sys.argv[2][1:])
    # godina=int(dicti['godina'][0])
    links=get_izet()
    
    for i in range(len(links)):
        url = build_url({'mode': 'otvori_lzn_ep','url':'%s'%links[i][0], 'ep':'%s'%links[i][1]})
        li = xbmcgui.ListItem('%s'%links[i][1].replace('LZN','Epizoda') ,iconImage='http://bh-info.com/wp-content/uploads/2015/04/lud.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    #xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL, 'A')
    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0]=='otvori_lzn_ep':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    url=dicti['url'][0]
    named=dicti['ep'][0].replace('LZN','Epizoda')
    name='Lud, zbunjen, normalan: '+ named

    import urlresolver
    resolved=urlresolver.resolve(get_izet_video(url))

    li = xbmcgui.ListItem('%s'%name)
    li.setInfo('video', { 'title': '%s'%name })
    
    xbmc.Player().play(item=resolved, listitem=li)


#####################################################################################################################################################################
#movinized
#####################################################################################################################################################################

elif mode[0]=='serije_movienized':
    cats=[['Arapske serije','http://movienized.com/arapske-serije/'],['Turske serije','http://movienized.com/turske-serije/'],['Španjolske serije','http://movienized.com/spanske-serije/'],
            ['Talijanske serije','http://movienized.com/italijanske-serije/'],['Domaće serije','http://movienized.com/domace-serije/']]

    for i in range(len(cats)):
        url = build_url({'mode': 'open_movienized_cat', 'cat': cats[i][1]})
        li = xbmcgui.ListItem(cats[i][0],iconImage=icon_path('Movienized.jpg'))
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='open_movienized_cat':
    cat=args['cat'][0]
    shows=get_shows_movinized(cat)
    for i in range(len(shows)):
        url = build_url({'mode': 'open_movienized_show', 'url': shows[i][0], 'next':0})
        li = xbmcgui.ListItem(shows[i][1],iconImage=shows[i][2])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='open_movienized_show':
    url=args['url'][0]
    next=int(args['next'][0])
    eps,next=get_movienized_eps(url,next)
    for i in range(len(eps)):
        url = build_url({'mode': 'open_movienized_ep', 'url': eps[i][0]})
        li = xbmcgui.ListItem(eps[i][1],iconImage=eps[i][2])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)
    if next!='0':
        url = build_url({'mode': 'open_movienized_show', 'url': next, 'next':1})
        li = xbmcgui.ListItem('Sljedeća stranica >>',iconImage=icon_path('Movienized.jpg'))
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                        listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='open_movienized_ep':
    url=args['url'][0]
    title,links,thumb=get_movinized_ep(url)
    li = xbmcgui.ListItem('%s'%title)
    li.setInfo('video', { 'title': '%s'%title})
    li.setThumbnailImage(thumb)
    if len (links)>1:
        sources=[]
        for i in range(len(links)):
            sources+=['%s. dio'%(i+1)]
        dialog = xbmcgui.Dialog()
        index = dialog.select('Odaberite:', sources)
        if index>-1:
            link=links[index]
            try:
                from lib.resolvers import dailymotion
                resolved=dailymotiong.resolve(link)
                resolved=resolved[0]['url']
                
            except:

                import urlresolver
                resolved=urlresolver.resolve(link)

    
            xbmc.Player().play(item=resolved, listitem=li)
    else:
        link=links[0]
        if 'moevideo' in link or 'playreplay' in link :
            import YDStreamExtractor
            YDStreamExtractor.disableDASHVideo(True) 
            vid = YDStreamExtractor.getVideoInfo(link,quality=1) 
            resolved = vid.streamURL() 
        else:
            try:
                    from lib.resolvers import dailymotion
                    resolved=dailymotiong.resolve(link)
                    resolved=resolved[0]['url']
                    
            except:

                    import urlresolver
                    resolved=urlresolver.resolve(link)

    
        xbmc.Player().play(item=resolved, listitem=li)
#####################################################################################################################################################################
#Live TV
#####################################################################################################################################################################
    
elif mode[0]=='live1':
    cats=[['Hrvatski','hrvatski','http://sprdex.com/wp-content/uploads/2012/07/RTL-televizija.jpg'],
        ['Dokumentarno','Dokumentarci-eng','http://cdn.fansided.com/wp-content/blogs.dir/280/files/2014/07/33506.jpg'],
        ['Sport','sport','http://www.hospitalityandcateringnews.com/wp-content/uploads/New-BT-Sport-TV-packages-for-hospitality-to-massively-undercut-Sky.jpg'],
        ['News','news','http://hub.tv-ark.org.uk/images/news/skynews/skynews_images/2001/skynews2001.jpg'],
        ['Filmovi/serije','film-serije','http://tvbythenumbers.zap2it.com/wp-content/uploads/2012/04/hbo_logo.jpg'],
        ['Lifestyle','lifestyle','http://pmcdeadline2.files.wordpress.com/2013/04/travelchannel_logo__130423191643.jpg'],
        ['Glazba','tv-music','http://www.hdtvuk.tv/mtv_logo.gif'],
        ['Djeca','djecji','http://upload.wikimedia.org/wikipedia/pt/archive/f/fe/20120623043934!Logo-TV_Kids.jpg'],
        ['Regionalni','regionalni','http://www.tvsrbija.net/wp-content/uploads/2013/01/pinktv.jpg'],
        ['Njemacki kanali','njemacki','http://upload.wikimedia.org/wikipedia/en/thumb/b/ba/Flag_of_Germany.svg/1280px-Flag_of_Germany.svg.png'],
        ['Ostalo','ostalo','http://www.globallistings.info/repository/image/6/445.jpg']]
    for i in range(len(cats)):
        url = build_url({'mode': 'open_live', 'tag': '%s'%cats[i][1]})
        li = xbmcgui.ListItem('%s'%cats[i][0],iconImage='%s'%cats[i][2])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)

    url = build_url({'mode': 'open_m3u', 'm3u': 'http://pastebin.com/raw.php?i=jmseyhvw'})
    li = xbmcgui.ListItem('Bikerdays TV lista (Svi kanali)',iconImage='http://www.bug.hr/_cache/01b378042cf2cabdf8dc4fe75f3e4cec.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)
    url = build_url({'mode': 'search_m3u', 'm3u': 'http://pastebin.com/raw.php?i=jmseyhvw'})
    li = xbmcgui.ListItem('Bikerdays TV lista (Pretraga)',iconImage='http://www.bug.hr/_cache/01b378042cf2cabdf8dc4fe75f3e4cec.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)
    url = build_url({'mode': 'serbiaplus'})
    li = xbmcgui.ListItem('serbiaplus.com')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)



elif mode[0]=='serbiaplus':
    base_uri = 'http://www.serbiaplus.com/'
    channels = get_all_channels_serbiaplus()

    for channel in channels:
        title = channel[1].replace('images/','').replace('.jpg','').replace('_',' ').title()
        urll='http://www.serbiaplus.com/' + channel[0]
        img= 'http://www.serbiaplus.com/' + urllib.quote(channel[1])
        url = build_url({'mode': 'open_plus','url':urll, 'name':title, 'img':img})
        li = xbmcgui.ListItem(title ,iconImage=img)
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0]=='open_plus':
    name=args['name'][0]
    url=args['url'][0]
    img = args['img'][0]
    import liveresolver
    resolved = liveresolver.resolve(url)
    player=xbmc.Player()
    li = xbmcgui.ListItem(name)
    li.setThumbnailImage(img)
    player.play(resolved,listitem=li)


elif mode[0]=='open_m3u':
    m3u=args['m3u'][0]
    from lib.modules import m3u_parser
    tracks = m3u_parser.parseM3U(m3u)
    for track in tracks:
        title=track.title
        url=track.path
        li = xbmcgui.ListItem(title,iconImage='')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li)
    

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='search_m3u':
    m3u=args['m3u'][0]
    keyboard = xbmc.Keyboard('', 'Pretraži TV kanale', False)
    keyboard.doModal()
    if keyboard.isConfirmed():
        query = keyboard.getText()
        from lib.modules import m3u_parser
        tracks = m3u_parser.parseM3U(m3u)
        tracks = search_m3u(query,tracks)

        for track in tracks:
            title=track.title
            url=track.path
            li = xbmcgui.ListItem(title,iconImage='')
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                        listitem=li)
    xbmcplugin.endOfDirectory(addon_handle)



elif mode[0]=='open_live':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link=dicti['tag'][0]

    reg='url="(.+?)"'
    pat=re.compile(reg)
    reg2='ime="(.+?)"'
    pat2=re.compile(reg2)
    reg3='img="(.+?)"'
    pat3=re.compile(reg3)
    pat4=re.compile('epg="(.+?)"')

    urll='https://raw.githubusercontent.com/natko1412/liveStreams/master/%s.txt'%link
    a=urllib2.urlopen(urll)
    html=a.read().decode('utf-8')
    urls=[]
    urls=re.findall(pat,html)
    imena=[]
    imena=re.findall(pat2,html)
    thumbs=[]
    thumbs=re.findall(pat3,html)
    epg=re.findall(pat4,html)
    
    for i in range(len(imena)):
        if 'bleb-' not in epg[i]:
            a= get_current_epg(epg[i])
        else:
            a= get_current_bleb(epg[i])
        url=build_url({'mode':'open_livee','url':urls[i], 'thumb':thumbs[i], 'name':imena[i].encode('utf-8')})
        
        
        epg_uri=build_url({'mode':'view_epg','title':imena[i].encode('utf-8'), 'epg':epg[i]})

        
        li = xbmcgui.ListItem('[B]%s[/B] - [I][COLOR green]%s[/COLOR][/I]'%(imena[i].encode('utf-8'),a), iconImage='%s'%thumbs[i])
        li.addContextMenuItems([ ('Otvori EPG', 'RunPlugin(%s)'%epg_uri)])
        
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    
    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0]=='open_livee':
    url=args['url'][0]
    name=args['name'][0]
    thumb=args['thumb'][0]
    urls = url.split('||')
    li = xbmcgui.ListItem(name, iconImage=thumb)
    li.setThumbnailImage(thumb)
    player=xbmc.Player()

    if 'hrt.live' in url:
        try:
            username = my_addon.getSetting('username')
            password = my_addon.getSetting('password')
            if username=='' or password =='':
                username = 'test'
                password = 'stream'
            from lib.sources import hrtihr
            hrty = hrtihr.hrtiLogin(username,password,10000)
            token = hrty.stream_token
            url=[url + token]
        except:
            #Notify("small","Info","Pogreska pri prijavi na HRTi","")
            pass

    for url in urls:
        #try:
            import liveresolver
            resolved=liveresolver.resolve(url)
            player.play(resolved,listitem=li)
            break
        #except:
         #   pass

elif mode[0]=='view_epg':
    #try:
        heading=args['title'][0]
        epg=args['epg'][0]

        if 'bleb' not in epg:
            anounce=get_epg(epg)
        else:
            anounce=get_epg_bleb(epg)


        present_epg(heading,anounce)
        xbmcplugin.endOfDirectory(addon_handle)
    # except:
    #     heading=args['title'][0]
    #     present_epg(heading,'Nema informacija')
    #     xbmcplugin.endOfDirectory(addon_handle)

#####################################################################################################################################################################
#Radio HRT
#####################################################################################################################################################################
elif mode[0]=='radioNZ':
    url = build_url({'mode': 'open_radio', 'foldername': 'prvi'})
    li = xbmcgui.ListItem('Prvi program' ,iconImage=icon_path('HR.png'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    url = build_url({'mode': 'open_radio', 'foldername': 'drugi'})
    li = xbmcgui.ListItem('Drugi program' ,iconImage=icon_path('HR.png'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    url = build_url({'mode': 'open_radio', 'foldername': 'treci'})
    li = xbmcgui.ListItem('Treci program' ,iconImage=icon_path('HR.png'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='open_radio':
    radio_prvi=[['http://radio.hrt.hr/arhiva/glazbena-kutijica/106/','Glazbena kutijica','http://radio.hrt.hr/data/show/small/000106_dc8c3b107ed03fe1d72a.png'],
    ['http://radio.hrt.hr/arhiva/katapultura/124/','Katapultura','http://radio.hrt.hr/data/show/small/000124_7f8a2fc760da4ffb13fd.jpg'],
    ['http://radio.hrt.hr/arhiva/kutija-slova/121/','Kutija slova','http://radio.hrt.hr/data/show/small/000121_c915aa04c682cd4ceae9.png'],
    ['http://radio.hrt.hr/arhiva/lica-i-sjene/131/','Lica i sjene','http://radio.hrt.hr/data/show/small/000131_f1fccaf5f9deb049a2a8.png'],
    ['http://radio.hrt.hr/arhiva/oko-znanosti/123/','Oko znanosti','http://radio.hrt.hr/data/show/small/000123_9d42ba1671b607c73749.png'],
    ['http://radio.hrt.hr/arhiva/pod-reflektorima/103/','Pod reflektorima','http://radio.hrt.hr/data/show/small/000103_00f27f731e2db0a017b1.png'],
    ['http://radio.hrt.hr/arhiva/povijest-cetvrtkom/126/','Povijest cetvrtkom','http://radio.hrt.hr/data/show/small/000126_d237561e30ad805abd1b.png'],
    ['http://radio.hrt.hr/arhiva/putnici-kroz-vrijeme/582/','Putnici kroz vrijeme','http://radio.hrt.hr/data/show/small/000582_17ce2778878d5f74d4c5.png'],
    ['http://radio.hrt.hr/arhiva/slusaj-kako-zemlja-dise/120/','Slusaj kako zemlja dise','http://radio.hrt.hr/data/show/small/000120_1fa05c0fdaa00afca3a9.png'],
    ['http://radio.hrt.hr/arhiva/u-sobi-s-pogledom/112/','U sobi s pogledom','http://radio.hrt.hr/data/show/small/000112_587e449519318aa90b41.png'],
    ['http://radio.hrt.hr/arhiva/zasto-tako/114/','Zasto tako?','http://radio.hrt.hr/data/show/small/000114_176003cffe60b893e589.png'],
    ['http://radio.hrt.hr/arhiva/znanjem-do-zdravlja/117/','Znanjem do zdravlja','http://radio.hrt.hr/data/show/small/000117_582f3d27a0e52c7e78be.png']]
    radio_drugi=[['http://radio.hrt.hr/arhiva/andromeda/18/','Andromeda','http://radio.hrt.hr/data/show/000018_f48cf7a1b19bf447b1e5.png'],
    ['http://radio.hrt.hr/arhiva/drugi-pogled/993/','Drugi pogled','http://radio.hrt.hr/data/show/small/000993_6fa6ff53c88f1ed3e50e.jpg'],
    ['http://radio.hrt.hr/arhiva/gladne-usi/700/','Gladne usi','http://radio.hrt.hr/data/show/small/000700_cdcdeaf6c30f86069ffd.png'],
    ['http://radio.hrt.hr/arhiva/globotomija/817/','Globotomija','http://radio.hrt.hr/data/show/small/000817_ec6bddd7f2754bb19eb5.jpg'],
    ['http://radio.hrt.hr/arhiva/homo-sapiens/812/','Homo sapiens','http://radio.hrt.hr/data/show/small/000812_9d0f8f96fca9b3826dbf.jpg']]
    radio_treci=[['http://radio.hrt.hr/arhiva/bibliovizor/713/','Bibliovizor','http://radio.hrt.hr/data/show/small/000713_e1aaeb9afcb944db39ca.jpg'],
    ['http://radio.hrt.hr/arhiva/filmoskop/98/','Filmoskop','http://radio.hrt.hr/data/show/small/000098_0fbee68352530480fe0e.jpg'],
    ['http://radio.hrt.hr/arhiva/glazba-i-obratno/614/','Glazba i obratno','http://radio.hrt.hr/data/show/small/000614_8155a16df37fd274d77f.jpg'],
    ['http://radio.hrt.hr/arhiva/lica-okolice/717/','Lica okolice','http://radio.hrt.hr/data/show/small/000717_e5af40b1d5af68406fc3.jpg'],
    ['http://radio.hrt.hr/arhiva/mikrokozmi/102/','Mikrokozmi','http://radio.hrt.hr/data/show/small/000102_2f995b3b984cdd82f923.jpg'],
    ['http://radio.hrt.hr/arhiva/moj-izbor/91/','Moj izbor','http://radio.hrt.hr/emisija/moj-izbor/91/'],
    ['http://radio.hrt.hr/arhiva/na-kraju-tjedna/196/','Na kraju tjedna','http://radio.hrt.hr/data/show/small/000196_7c5997025a9bfcf45967.jpg'],
    ['http://radio.hrt.hr/arhiva/poezija-naglas/720/','Poezija naglas','http://radio.hrt.hr/data/show/small/000720_c2495423cd72b180482f.jpg'],
    ['http://radio.hrt.hr/arhiva/znanost-i-drustvo/950/','Znanost i drustvo','http://radio.hrt.hr/data/show/small/000950_6dd01f01230facbf40b0.jpg']]


    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link=dicti['foldername'][0]
    if link=='prvi':
        rdio=radio_prvi
    elif link=='drugi':
        rdio=radio_drugi

    elif link=='treci':
        rdio=radio_treci


    for i in range (len(rdio)):
        title=rdio[i][1]
        url=rdio[i][0]
        img=rdio[i][2]
        url = build_url({'mode':'open_emisija','url': '%s'%url, 'foldername': '%s'%title, 'img':'%s'%img})
        li = xbmcgui.ListItem('%s'%title ,iconImage=img)
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='open_emisija':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    title=dicti['foldername'][0]
    img=dicti['img'][0]
    url=dicti['url'][0]

    lista=find_episodes(url)
    
    for i in range (len(lista)):
        li = xbmcgui.ListItem('%s'%lista[i][0], iconImage='%s'%img)
        url = build_url({'mode':'play_emisija','url': '%s'%lista[i][1],'img':'%s'%img,'title': '%s'%lista[i][0]})
        down_uri = build_url({'mode': 'download_radio', 'title': '%s'%normal(lista[i][0]), 'url': lista[i][1]})
        li.addContextMenuItems([ ('Preuzmi audio', 'RunPlugin(%s)'%down_uri)])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0]=='play_emisija':
    url=args['url'][0]
    img=args['img'][0]
    title=args['title'][0]
    li = xbmcgui.ListItem(title,iconImage='%s'%img)
    li.setInfo('music', { 'title': '%s'%title })
    resolved=radio_resolve(url)
    xbmc.Player().play(listitem=li,item=resolved)
elif mode[0]=='download_radio':
    url=args['url'][0]
    title=args['title'][0]
    resolved=radio_resolve(url)
    download(title,resolved)

#####################################################################################################################################################################
#Radio uzivo
#####################################################################################################################################################################
elif mode[0]=='radio_live':
    
    lista=get_links_country('croatia')
    for i in range(1,len(lista)):
        if lista[i][1]!='':
            li = xbmcgui.ListItem('%s (%s)'%(lista[i][1],lista[i][3]), iconImage=icon_path('Radio.png'))
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=lista[i][0], listitem=li)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.endOfDirectory(addon_handle)
#####################################################################################################################################################################
#Favoriti
#####################################################################################################################################################################
elif mode[0]=='favoriti':
    f = open(favourites_file, 'r')
    xml=f.read()
    f.close()
    reg='<favourite>\s*<name>(.+?)<name>\s*<url>(.+?)</url>\s*<thumb>(.+?)</thumb>\s*</favourite>'
    regex=re.compile(reg)
    favourites=re.findall(regex,xml)
    for favourite in favourites:
        url=favourite[1]
        name=favourite[0]
        thumb=favourite[2]
        li = xbmcgui.ListItem(name ,iconImage=thumb)
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)



elif mode[0]=='add_favourite':
    url= args['url'][0]
    name=args['name'][0]
    try:
        thumb=args['thumb'][0]
    except:
        thumb=icon_path('Favoriti.png')
    fav_str='''#####################################
    <favourite>
    <name>%s<name>
    <url>%s</url>
    <thumb>%s</thumb>
    </favourite>'''%(name,url,thumb)


    #favourites_file
    f = open(favourites_file, 'a+')
    result = f.write(fav_str)
    f.close()
    print('Added to favs')

##crtanionline
elif mode[0]=='crtanionline':
    cats = crtani.get_categories()
    for cat in cats:
        url = build_url({'mode': 'open_crtani_cat', 'url':cat[0]})
        li = xbmcgui.ListItem(cat[1] ,iconImage='')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    

    xbmcplugin.endOfDirectory(addon_handle)


elif mode[0]=='open_crtani_cat':
    url=args['url'][0]

    cr = crtani(url)
    movies = cr.get_movie_list()
    for movie in movies:
        url = build_url({'mode': 'open_crtani_movie', 'url':movie[0].encode('utf-8'), 'title':movie[2].encode('utf-8'), 'img' : movie[1].encode('utf-8')})
        li = xbmcgui.ListItem(movie[2] ,iconImage=movie[1])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    
    if (cr.next_page()):
        url = build_url({'mode': 'open_crtani_cat', 'url':cr.next_page()})
        li = xbmcgui.ListItem('Sljedeća stranica >>' ,iconImage='')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    


    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='open_crtani_movie':
    url=args['url'][0]
    title = args['title'][0]
    img = args['img'][0]
    cr = crtani(url)
    url,sub = cr.get_links()
    sub = download_subs(sub)
    li = xbmcgui.ListItem(title)
    li.setThumbnailImage(img)
    player=xbmc.Player()
    try:
        import urlresolver
        resolved = urlresolver.resolve(url)
        player.play(resolved,listitem=li)
        player.setSubtitles(sub)
    except:
        pass
