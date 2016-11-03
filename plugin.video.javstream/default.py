import menu, util, urllib
import xbmcplugin, xbmcaddon, xbmcgui
import search, realdebrid


sysarg=str(sys.argv[1])
ADDON_ID='plugin.video.javstream'
addon = xbmcaddon.Addon(id=ADDON_ID)
parameters=util.parseParameters()
try:
    mode=int(parameters["mode"])
except:
    mode=None
  
xbmcplugin.setPluginFanart(int(sys.argv[1]), 'special://home/addons/plugin.video.javstream/fanart.jpg', color2='0xFFFF3300')

if mode==1:
    # display the JAV specific sub menu
    util.addMenuItems(menu.javMenu)
elif mode==2:
    # display the Gravure specific sub menu
    util.addMenuItems(menu.gravureMenu)
elif mode==3:
    try:
        if parameters['extras']=="force-search":
            f={"s":parameters['name']}
            util.findVideos(parameters['url']+"?"+urllib.urlencode(f))
        elif parameters['extras']=='true-search':
            util.searchFilms(parameters)
    except:
        util.searchMenu()
elif mode==4:
    # load the latest of a type
    #util.logError(parameters['url'])
    xbmcplugin.setContent(int(sysarg), "movies")
    util.findVideos(parameters["url"])
elif mode==5:
    # a video has been chosen, lets hunt for sources
    util.huntVideo(parameters)
elif mode==6:
    url=util.getVideoURL(parameters)
    util.playMedia(parameters['extras2'], parameters['poster'], url, "Video", False, parameters['name'])
elif mode==7:
    util.addMenuItems(util.getFavourites())
elif mode==8:
    util.addMenuItems(util.getFavourites())
elif mode==9:
    if addon.getSetting('download_path')=="":
        util.alert("Please configure download in Add-On Settings")
        exit()
    # simpledownloader taken (and then altered) from specto
    import simpledownloader
    xbmc.executebuiltin( "XBMC.Notification(%s,%s,%i,%s)" % ( parameters['name'].encode("utf-8") + ' - Preparing Download', 'Please Wait', 7000, parameters['poster'].encode("utf-8")))

    url=util.getVideoURL(parameters)#.replace("?mime=true", "")
    
    if url!=False:  
        simpledownloader.download(parameters['name'], parameters['poster'], url, parameters['fanart'])
elif mode==10:
    window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
    
    addon.setSetting("vidview", str(window.getFocusId()))
    util.notify(ADDON_ID, "Default view has been set ("+str(window.getFocusId())+").", True, 2000)
elif mode==11:
    util.addToLibrary(parameters)
elif mode==12:
    util.addToBookmarks(parameters)
elif mode==13:
    util.showBookmarks(parameters)
elif mode==14:
    util.deleteBookmark(parameters)
elif mode==31:
    util.deleteSearch(parameters)
elif mode==1000:
    # gravure main menu
    util.addMenuItems(menu.gravureMenu)
elif mode==1002:
    util.gravureIdols(parameters)
else: 
    try:
        if parameters['realdebrid']=="true":
            realdebrid.auth()
    except:
        try:
            if parameters['emptySearch']=="true":
                runDelete= xbmcgui.Dialog().yesno("Confirm Database Reset","Are you sure you want to delete ALL search terms?")
                if runDelete==True:
                    search.removeSearch(parameters)
                    util.notify("Search database reset")
        except:
            try:
                if parameters['emptyBookmarks']=="true":
                    runDelete= xbmcgui.Dialog().yesno("Confirm Database Reset","Are you sure you want to delete ALL of your favourites?")
                    if runDelete==True:
                        search.removeBookmarks(parameters)
                        util.notify("Favourites database reset")
            except:
                # if we get here then there's nothing to do except display the main menu
                util.addMenuItems(menu.mainMenu)