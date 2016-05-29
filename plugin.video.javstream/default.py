import menu, util, urllib
import xbmcplugin, xbmcaddon, xbmcgui
import search

sysarg=str(sys.argv[1])
ADDON_ID='plugin.video.javstream'
addon = xbmcaddon.Addon(id=ADDON_ID)

parameters=util.parseParameters()
try:
    mode=int(parameters["mode"])
except:
    mode=None
  
if mode==1:
    # display the JAV specific sub menu
    util.addMenuItems(menu.javMenu)
elif mode==2:
    # display the Gravure specific sub menu
    util.addMenuItems(menu.gravureMenu)
elif mode==3:
    #util.logError(str(parameters))
    try:
        if parameters['extras']=="force-search":
            f={"s":parameters['name']}
            util.findVideos(parameters['url']+"?"+urllib.urlencode(f))
        else:
            util.searchFilms(parameters)
    except:
        #util.logError(str(sys.exc_info()))
        util.searchMenu()
elif mode==4:
    # load the latest of a type
    #util.logError(parameters['url'])
    util.findVideos(parameters["url"])
elif mode==5:
    # a video has been chosen, lets hunt for sources
    util.huntVideo(parameters)
elif mode==6:
    url=util.getVideoURL(parameters)
    util.playMedia(parameters['extras2'], parameters['poster'], url, "Video")
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

    url=util.getVideoURL(parameters).replace("?mime=true", "")
    #util.logError(url)
    if "openload" in url:
        import urllib2
        url=urllib2.urlopen(url).geturl()
        
    simpledownloader.download(parameters['name'], parameters['poster'], url, parameters['fanart'])
elif mode==10:
    window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
    
    addon.setSetting("vidview", str(window.getFocusId()))
    util.notify(ADDON_ID, "Default view has been set ("+str(window.getFocusId())+").", True, 2000)
elif mode==31:
    util.deleteSearch(parameters)
elif mode==1000:
    # gravure main menu
    util.addMenuItems(menu.gravureMenu)
elif mode==1002:
    util.gravureIdols(parameters)
else:
    # if we get here then there's nothing to do except display the main menu
    util.addMenuItems(menu.mainMenu)