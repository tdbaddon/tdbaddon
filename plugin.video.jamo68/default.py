import menu, util
import xbmcplugin, xbmcaddon


sysarg=str(sys.argv[1])
ADDON_ID='plugin.video.jamo68'
addon = xbmcaddon.Addon(id=ADDON_ID)

parameters=util.parseParameters()
try:
    mode=int(parameters["mode"])
except:
    mode=None

if mode==1:
    # display the JAV censored specific sub menu
    util.addMenuItems(menu.jamoMenu)
elif mode==2:
    # display the Gravure specific sub menu
    util.addMenuItems(menu.jav68Menu)
elif mode==9:
    if addon.getSetting('download_path')=="":
        util.alert("Please configure download in Add-On Settings")
        exit()
    # simpledownloader taken (and then altered) from specto
    import simpledownloader
    xbmc.executebuiltin( "XBMC.Notification(%s,%s,%i,%s)" % ( parameters['name'].encode("utf-8") + ' - Preparing Download', 'Please Wait', 7000, parameters['poster'].encode("utf-8")))

    url=util.getVideoURL(parameters).replace("?mime=true", "")
    util.logError(url)
    if "openload" in url:
        import urllib2
        url=urllib2.urlopen(url).geturl()
        
    simpledownloader.download(parameters['name'], parameters['poster'], url, parameters['fanart'])
elif mode==11:
    util.jamoMenu('<a>Categories</a>', '<li class="parent">')
elif mode==12:
    util.jamoMenu('<a>Studios</a>', '</ul>')
elif mode==13:
    util.jamoModels(parameters['url'])
elif mode==111:
    util.jamoVideos(parameters)
elif mode==120:
    util.jamoGetSource(parameters)
elif mode==16:
    search=util.searchDialog()
    url=parameters['url'].replace('<search>', search)
    util.jamoVideos({'url':url})
elif mode==21:
    util.jav68Menu(parameters)
elif mode==211:
    util.jav68GetVideos(parameters)
elif mode==26:
    search=util.searchDialog()
    url=parameters['url'].replace('<search>', search)
    util.jav68GetVideos({'url':url})
elif mode==220:
    util.jav68GetSource(parameters)
else:
    # if we get here then there's nothing to do except display the main menu
    util.addMenuItems(menu.mainMenu)