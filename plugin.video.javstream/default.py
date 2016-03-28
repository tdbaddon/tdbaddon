import urllib
import menu, util
import xbmcplugin, xbmcaddon

sysarg=str(sys.argv[1])
ADDON_ID='plugin.video.javstream'
addon = xbmcaddon.Addon(id=ADDON_ID)

# test accessing the addon settings
# util.notify(ADDON_ID, xbmcplugin.getSetting(int(sysarg), "language"))

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
    # lets start searching
    search=util.searchDialog()
    if (search):
        # something has been typed, lets search for it
        util.logError(parameters['url']+"?s="+search)
        util.findVideos(parameters['url']+"?s="+search)
elif mode==4:
    # load the latest of a type
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
else:
    # if we get here then there's nothing to do except display the main menu
    util.addMenuItems(menu.mainMenu)