from urllib2 import Request, urlopen
import urllib2,urllib,re,os, shutil
import sys
import base64
import time,datetime
import xbmcplugin,xbmcgui,xbmc, xbmcaddon, downloader, extract, time
from libs import kodi
from libs import viewsetter
import plugintools

addon_id=kodi.addon_id
addon = (addon_id, sys.argv)
artwork = xbmc.translatePath(os.path.join('special://home','addons',addon_id,'art/'))
fanart = artwork+'fanart.jpg'
messages = xbmc.translatePath(os.path.join('special://home','addons',addon_id,'resources','messages/'))
execute = xbmc.executebuiltin
AddonTitle = 'Indigo'

thumbnailPath = xbmc.translatePath('special://userdata/Thumbnails');
cachePath = os.path.join(xbmc.translatePath('special://home'), 'cache')
tempPath = os.path.join(xbmc.translatePath('special://home'), 'temp')
ADDONS = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'))
databasePath = xbmc.translatePath('special://userdata/Database')
USERDATA = xbmc.translatePath('special://userdata/')
AddonData = xbmc.translatePath('special://userdata/addon_data')
dp = xbmcgui.DialogProgress()
Windows = xbmc.translatePath('special://home')
WindowsCache = xbmc.translatePath('special://home')
OtherCache = os.path.join(xbmc.translatePath('special://home'), 'temp')
dialog = xbmcgui.Dialog()

########PATHS###############################################
addonPath=xbmcaddon.Addon(id=addon_id).getAddonInfo('path')
addonPath=xbmc.translatePath(addonPath)
xbmcPath=os.path.join(addonPath,"..","..")
KodiPath=os.path.abspath(xbmcPath)
############################################################

def tool_menu():

    check_folders = plugintools.get_setting("maint_check_folders")

    HOME          =  xbmc.translatePath('special://home/')
    PACKAGES      =  xbmc.translatePath(os.path.join('special://home/addons','packages'))
    THUMBS        =  xbmc.translatePath(os.path.join('special://home/userdata','Thumbnails'))
    CACHE_FOLDER  =  xbmc.translatePath(os.path.join('special://home','cache'))
    TEMP_FOLDER   =  xbmc.translatePath(os.path.join('special://','temp'))
    CACHE         =  "NULL"

    if check_folders == "true":
        if os.path.exists(CACHE_FOLDER):
            CACHE = CACHE_FOLDER

        if os.path.exists(TEMP_FOLDER):
            CACHE = TEMP_FOLDER

        if not os.path.exists(PACKAGES):
            os.makedirs(PACKAGES)

        if CACHE == "NULL":
            try:
                PACKAGES_SIZE_BYTE = get_size(PACKAGES)
                THUMB_SIZE_BYTE    = get_size(THUMBS)
            except: pass
        else:
            try:
                CACHE_SIZE_BYTE    = get_size(CACHE)
                PACKAGES_SIZE_BYTE = get_size(PACKAGES)
                THUMB_SIZE_BYTE    = get_size(THUMBS)
            except: pass
        
        if CACHE == "NULL":
            try:
                PACKAGES_SIZE = convertSize(PACKAGES_SIZE_BYTE)
                THUMB_SIZE    = convertSize(THUMB_SIZE_BYTE)
            except: pass
        else:
            try:
                CACHE_SIZE    = convertSize(CACHE_SIZE_BYTE)
                PACKAGES_SIZE = convertSize(PACKAGES_SIZE_BYTE)
                THUMB_SIZE    = convertSize(THUMB_SIZE_BYTE)
            except: pass
        
        if CACHE == "NULL":
            CACHE_SIZE    =  "Error reading cache"

    startup_clean = plugintools.get_setting("acstartup")
    weekly_clean = plugintools.get_setting("clearday")

    if startup_clean == "false":
        startup_onoff = "Off"
    else:
        startup_onoff = "On"
    if weekly_clean == "0":
        weekly_onoff = "Off"
    else:
        weekly_onoff = "On"

    if check_folders == "true":
        try:
            kodi.addItem("Cache Size: [COLOR blue]" + str(CACHE_SIZE) + '[/COLOR] - Click To Clear','','clear_cache',artwork+'currentcache.png',description="Clear your device cache!")
            kodi.addItem("Packages Size: [COLOR blue]" + str(PACKAGES_SIZE) + '[/COLOR] - Click To Clear','','purgepackages',artwork+'currentpackages.png',description="Clear your device cache!")
            kodi.addItem("Thumbnail Size: [COLOR blue]" + str(THUMB_SIZE) + '[/COLOR] - Click To Clear','','clearthumbs',artwork+'currentthumbs.png',description="Clear your device cache!")
        except: pass

    kodi.addItem("Run Auto Maintenance",'','autoclean',artwork+'run_am.png',description="Clear your cache, packages and thumbnails in one click!")
    kodi.addDir("Install Custom Keymaps",'','customkeys',artwork+'custom_keymaps.png',description="Get the best experience out of your device-specific remote control!")    
    if _is_debugging() == True: kodi.addItem("Disable Debugging Mode",'','debug_onoff',artwork+'disabledebug.png',description="Disable Debugging!")
    else: kodi.addItem("Enable Debugging Mode",'','debug_onoff',artwork+'enabledebug.png',description="Enable Debugging!")
    kodi.addItem("Force Quit Kodi",'','foceclosekodi',artwork+'forceclose.png',description="Force close Kodi!")
    kodi.addItem("Delete Crash Logs",'','crashlogs',artwork+'clearcrash.png',description="Clear all crash logs from your device!")
    if weekly_clean == "0": kodi.addItem('Enable Weekly Auto Maintenance','','autocleanonoff',artwork+'enable_am_week.png',description="Set your device to perform maintenance on a given day each week!")
    else: kodi.addItem('Disable Weekly Auto Maintenance','','autocleanonoff',artwork+'disable_am_week.png',description="Disable maintenance on a given day each week!")
    if startup_clean == "false": kodi.addItem('Enable Auto Maintenance on Startup','','autocleanlaunch',artwork+'enable_am_startup.png',description="Perform maintenance on Kodi launch!")
    else: kodi.addItem('Disable Auto Maintenance on Startup','','autocleanlaunch',artwork+'disable_am_startup.png',description="Disable maintenance on Kodi launch!")
    if kodi.get_setting ('scriptblock') == 'true': kodi.addItem("Disable Malicious Scripts Blocker",'','disableblocker',artwork+'disable_MSB.png',description="Disable protection against malicious scripts!")
    if kodi.get_setting ('scriptblock') == 'false': kodi.addItem("Enable Malicious Scripts Blocker",'','enableblocker',artwork+'enable_MSB.png',description="Enable protection against malicious scripts!")
    kodi.addItem("Check Repo Health",'','repohealth',artwork+'repohealth.png',description="Check the health of all repositories!")
    kodi.addItem("Check Sources XML Health",'','sourcehealth',artwork+'sourcehealth.png',description="Check the Sources XML file for broken sources!")
    kodi.addItem("Wipe Addons",'','wipeaddons',artwork+'wipe_addons.png',description="Erase all your Kodi addons in one shot!")
    kodi.addItem("Force Update Addons",'','updateaddons',artwork+'forceupdateaddons.png',description="Force a reload of all Kodi addons and repositories!")
    kodi.addItem("Encode | Decode Base64",'','encdecbase64',artwork+'decodebase64.png',description="Encode / Decode any Base64 value!")
    kodi.addItem("Reload Current Skin",'','reloadskin',artwork+'reloadskin.png',description="Reload the skin!")

    viewsetter.set_view("sets")

################################
###       Clear Cache        ###
################################

def clear_cache():
    kodi.log('CLEAR CACHE ACTIVATED')
    xbmc_cache_path = os.path.join(xbmc.translatePath('special://home'), 'cache')
    confirm=xbmcgui.Dialog().yesno("Please Confirm","                     Please confirm that you wish to clear                     ","                           your Kodi application cache!","              ","Cancel","Clear")
    if confirm:
        if os.path.exists(xbmc_cache_path)==True:
            for root, dirs, files in os.walk(xbmc_cache_path):
                file_count = 0
                file_count += len(files)
                if file_count > 0:


                        for f in files:
                            try:
                                os.unlink(os.path.join(root, f))
                            except:
                                pass
                        for d in dirs:
                            try:
                                shutil.rmtree(os.path.join(root, d))
                            except:
                                pass


        dialog = xbmcgui.Dialog()
        dialog.ok(AddonTitle, "       Cache Cleared Successfully!")
        xbmc.executebuiltin("Container.Refresh()")

################################
###     End Clear Cache      ###
################################

def purge_packages():
    kodi.log('PURGE PACKAGES ACTIVATED')
    packages_path = xbmc.translatePath(os.path.join('special://home/addons/packages', ''))
    confirm=xbmcgui.Dialog().yesno("Please Confirm","                     Please confirm that you wish to delete                    ","                     your old addon installation packages!","              ","Cancel","Delete")
    if confirm:
        try:
            for root, dirs, files in os.walk(packages_path,topdown=False):
                for name in files :
                    os.remove(os.path.join(root,name))
                dialog = xbmcgui.Dialog()
                dialog.ok(AddonTitle, "                     Packages Folder Wiped Successfully!")
                xbmc.executebuiltin("Container.Refresh()")
        except:
            dialog = xbmcgui.Dialog()
            dialog.ok(AddonTitle, "Error Deleting Packages please visit TVADDONS.AG forums")

def wipe_addons():
    kodi.logInfo('WIPE ADDONS ACTIVATED')
    confirm=xbmcgui.Dialog().yesno("Please Confirm","                     Please confirm that you wish to uninstall                     ","                              all addons from your device!","              ","Cancel","Uninstall")
    if confirm:
        addonPath=xbmcaddon.Addon(id=addon_id).getAddonInfo('path')
        addonPath=xbmc.translatePath(addonPath)
        xbmcPath=os.path.join(addonPath,"..","..")
        xbmcPath=os.path.abspath(xbmcPath);

        addonpath = xbmcPath+'/addons/'
        mediapath = xbmcPath+'/media/'
        systempath = xbmcPath+'/system/'
        userdatapath = xbmcPath+'/userdata/'
        packagepath = xbmcPath+ '/addons/packages/'
        try:
            for root, dirs, files in os.walk(addonpath,topdown=False):
                print root
                if root != addonpath :
                    if 'plugin.program.indigo' not in root:
                        if 'metadata.album.universal' not in root:
                            if 'metadata.artists.universal' not in root:
                                if 'metadata.common.musicbrainz.org' not in root:
                                    if 'service.xbmc.versioncheck' not in root:
                                        shutil.rmtree(root)

            dialog = xbmcgui.Dialog()
            dialog.ok(AddonTitle, "Addons Wiped Successfully!  Click OK to exit Kodi and then restart to complete .")
            xbmc.executebuiltin('ShutDown')
        except:
            dialog = xbmcgui.Dialog()
            dialog.ok(AddonTitle, "Error Wiping Addons please visit TVADDONS.AG forums")

def disable_main():
    #kodi.log('DISABLE MAIN TOOL')
    confirm=xbmcgui.Dialog();
    if confirm.yesno('Automatic Maintenance ',"Please confirm that you wish to TURN OFF automatic maintenance! "," "):
        kodi.log ("Disabled AUTOMAIN")
        kodi.set_setting('automain','false')
        dialog = xbmcgui.Dialog()
        dialog.ok("Automatic Maintenance", "Settings Changed!  Click OK to exit Kodi and then restart to complete .")
        xbmc.executebuiltin('ShutDown')
    else:
        return

def enable_main():
    #kodi.log('ENABLE MAIN TOOL')
    confirm=xbmcgui.Dialog();
    if confirm.yesno('Automatic Maintenance ',"Please confirm that you wish to TURN ON automatic maintenance! "," "):
        kodi.log ("enabled AUTOMAIN")
        kodi.set_setting('automain','true')
        dialog = xbmcgui.Dialog()
        dialog.ok("Automatic Maintenance", "Settings Changed!  Click OK to exit Kodi and then restart to complete .")
        xbmc.executebuiltin('ShutDown')
    else:
        return

def disable_blocker():
    #kodi.log('DISABLE BLOCKER')
    confirm=xbmcgui.Dialog();
    if confirm.yesno('Malicious Script Blocker',"Please confirm that you wish to TURN OFF Malicious Script Blocker! "," "):
        kodi.log ("Disable Script Block")
        kodi.set_setting('scriptblock','false')
        dialog = xbmcgui.Dialog()
        dialog.ok("Script Blocker", "Settings Changed!  Click OK to exit Kodi and then restart to complete .")
        xbmc.executebuiltin('ShutDown')
    else:
        return

def enable_blocker():
    #kodi.log('ENABLE BLOCKER')
    confirm=xbmcgui.Dialog();
    if confirm.yesno('Malicious Script Blocker',"Please confirm that you wish to TURN ON Malicious Script Blocker! "," "):
        kodi.log ("Enable Script Block")
        kodi.set_setting('scriptblock','true')
        dialog = xbmcgui.Dialog()
        dialog.ok("Script Blocker", "Settings Changed!  Click OK to exit Kodi and then restart to complete .")
        xbmc.executebuiltin('ShutDown')
    else:
        return
        
def _is_debugging():
    command = {'jsonrpc': '2.0', 'id': 1, 'method': 'Settings.getSettings', 'params': {'filter': {'section': 'system', 'category': 'logging'}}}
    js_data = kodi.execute_jsonrpc(command)
    for item in js_data.get('result', {}).get('settings', {}):
        if item['id'] == 'debug.showloginfo':
            return item['value']
    
    return False

#######################################################################
#                       Cache Functions
#######################################################################

class Gui(xbmcgui.WindowXMLDialog):
    def __init__(self, *args, **kwargs):
        xbmcgui.WindowXMLDialog.__init__(self)
        self.header = kwargs.get("header")
        self.content = kwargs.get("content")

    def onInit(self):
        self.getControl(1).setLabel(self.header)
        self.getControl(5).setText(self.content)

path   = xbmcaddon.Addon().getAddonInfo('path').decode("utf-8")

class cacheEntry:
    def __init__(self, namei, pathi):
        self.name = namei
        self.path = pathi   

#######################################################################
#                       Maintenance Functions
#######################################################################
def setupCacheEntries():
    entries = 5 #make sure this refelcts the amount of entries you have
    dialogName = ["WTF", "4oD", "BBC iPlayer", "Simple Downloader", "ITV"]
    pathName = ["special://profile/addon_data/plugin.video.whatthefurk/cache", "special://profile/addon_data/plugin.video.4od/cache",
                    "special://profile/addon_data/plugin.video.iplayer/iplayer_http_cache","special://profile/addon_data/script.module.simple.downloader",
                    "special://profile/addon_data/plugin.video.itv/Images"]
                    
    cacheEntries = []
    
    for x in range(entries):
        cacheEntries.append(cacheEntry(dialogName[x],pathName[x]))
    
    return cacheEntries

#######################################################################
#                       Clear Cache
#######################################################################

def clearCache():
    
    confirm=xbmcgui.Dialog().yesno("Please Confirm","                     Please confirm that you wish to clear                     ","                           your Kodi application cache!","              ","Cancel","Clear")
    if confirm:
        if os.path.exists(cachePath)==True:    
            for root, dirs, files in os.walk(cachePath):
                file_count = 0
                file_count += len(files)
                if file_count > 0:
                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            checker = (os.path.join(root, d))
                            if not "archive_cache" in str(checker):
                                shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                            
                else:
                    pass
        if os.path.exists(tempPath)==True:    
            for root, dirs, files in os.walk(tempPath):
                file_count = 0
                file_count += len(files)
                if file_count > 0:
                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            checker = (os.path.join(root, d))
                            if not "archive_cache" in str(checker):
                                shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                            
                else:
                    pass
        if xbmc.getCondVisibility('system.platform.ATV2'):
            atv2_cache_a = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')
            
            for root, dirs, files in os.walk(atv2_cache_a):
                file_count = 0
                file_count += len(files)
            
                if file_count > 0:

                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            checker = (os.path.join(root, d))
                            if not "archive_cache" in str(checker):
                                shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                            
                else:
                    pass
            atv2_cache_b = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')
            
            for root, dirs, files in os.walk(atv2_cache_b):
                file_count = 0
                file_count += len(files)
            
                if file_count > 0:
                    active = True
                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            checker = (os.path.join(root, d))
                            if not "archive_cache" in str(checker):
                                shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
                else:
                    pass    
                    
        cacheEntries = setupCacheEntries()
                                             
        for entry in cacheEntries:
            clear_cache_path = xbmc.translatePath(entry.path)
            if os.path.exists(clear_cache_path)==True:    
                for root, dirs, files in os.walk(clear_cache_path):
                    file_count = 0
                    file_count += len(files)
                    if file_count > 0:
                        for f in files:
                            try:
                                if (f.endswith(".log")): continue
                                os.unlink(os.path.join(root, f))
                            except:
                                pass
                        for d in dirs:
                            try:
                                checker = (os.path.join(root, d))
                                if not "archive_cache" in str(checker):
                                    shutil.rmtree(os.path.join(root, d))
                            except:
                                pass
                            
                    else:
                        pass
    else: quit()            

    dialog = xbmcgui.Dialog()
    dialog.ok(AddonTitle, "Done Clearing Cache files")
    xbmc.executebuiltin("Container.Refresh")

#######################################################################
#                       Delete Thumbnails
#######################################################################
    
def deleteThumbnails():
    
    if os.path.exists(thumbnailPath)==True:  
            dialog = xbmcgui.Dialog()
            if dialog.yesno("Delete Thumbnails", "This option deletes all thumbnails", "Are you sure you want to do this?"):
                for root, dirs, files in os.walk(thumbnailPath):
                    file_count = 0
                    file_count += len(files)
                    if file_count > 0:                
                        for f in files:
                            try:
                                os.unlink(os.path.join(root, f))
                            except:
                                pass
            else: quit()
    else:
        pass
    
    text13 = os.path.join(databasePath,"Textures13.db")
    try:
        os.unlink(text13)
    except OSError:
        pass

    dialog.ok(AddonTitle, 'Thumbnails have been deleted.')
    xbmc.executebuiltin("Container.Refresh")

def CHECK_BROKEN_SOURCES():

    dialog = xbmcgui.Dialog()
    SOURCES_FILE =  xbmc.translatePath('special://home/userdata/sources.xml')

    if not os.path.isfile(SOURCES_FILE):
        dialog.ok(AddonTitle,'Error: It appears you do not currently have a sources.xml file on your system. We are unable to perform this test.')
        sys.exit(0)

    dp.create(AddonTitle,"Testing Internet Connection...",'', 'Please Wait...') 

    try:
        open_url("http://www.google.com")
    except:
        dialog.ok(AddonTitle,'Error: It appears you do not currently have an active internet connection. This will cause false positives in the test. Please try again with an active internet connection.')
        sys.exit(0)
    found = 0
    passed = 0
    dp.update(0,"Checking Sources...",'', 'Please Wait...') 
    a=open(SOURCES_FILE).read() 
    b=a.replace('\n','U').replace('\r','F')
    match=re.compile('<source>(.+?)</source>').findall(str(b))
    counter = 0
    if match:
        try:
            for item in match:
                name=re.compile('<name>(.+?)</name>').findall(item)[0]
                checker=re.compile('<path pathversion="1">(.+?)</path>').findall(item)[0]
                if "http" in str(checker):
                    dp.update(0,"","Checking: " + name, "")
                    try:
                        checkme = open_url(checker)
                    except:
                        checkme = "null"
                        pass
                    try:
                        error_out = 0
                        if not "this does not matter its just a test" in ("%s" % checkme):
                            error_out = 0
                    except:
                        error_out = 1

                    if error_out == 0:
                        if not ".zip" in ("%s" % checkme):     
                            if not "repo" in ("%s" % checkme):
                                if not "<title>Index of /</title>" in ("%s" % checkme):
                                    choice = dialog.select("Error connecting to " + name + " (" + checker + ")", ['Edit the source URL.','Remove the source.','Do Nothing (Leave the source)'])
                                    if choice == 0:
                                        found = 1
                                        counter = counter + 1
                                        string =''
                                        keyboard = xbmc.Keyboard(string, 'Enter New Source URL')
                                        keyboard.doModal()
                                        if keyboard.isConfirmed():
                                            string = keyboard.getText().replace(' ','')
                                        if len(string)>1:
                                            if not "http://" in string:
                                                if not "https://" in string:
                                                    string = "http://" + string
                                            h=open(SOURCES_FILE).read()
                                            i=h.replace('\n','U').replace('\r','F')
                                            j=i.replace(str(checker), str(string))
                                            k=j.replace('U','\n').replace('F','\r')
                                            f= open(SOURCES_FILE, mode='w')
                                            f.write(k)
                                            f.close()
                                        else: quit()
                                    elif choice == 1:
                                        found = 1
                                        counter = counter + 1
                                        h=open(SOURCES_FILE).read()
                                        i=h.replace('\n','U').replace('\r','F')
                                        j=i.replace(str(item), '')
                                        k=j.replace('U','\n').replace('F','\r')
                                        l=k.replace('<source></source>','').replace('        \n','')
                                        f= open(SOURCES_FILE, mode='w')
                                        f.write(l)
                                        f.close()
                                    else:
                                        found = 1
                                        counter = counter + 1
                                else:
                                    passed = passed + 1
                            else:
                                passed = passed + 1
                        else:
                            passed = passed + 1
                    else:
                        choice = dialog.select("Error connecting to " + name + " (" + checker + ")", ['Edit the source URL.','Remove the source.','Do Nothing (Leave the source)'])
                        if choice == 0:
                            found = 1
                            counter = counter + 1
                            string =''
                            keyboard = xbmc.Keyboard(string, 'Enter New Source URL')
                            keyboard.doModal()
                            if keyboard.isConfirmed():
                                string = keyboard.getText().replace(' ','')
                            if len(string)>1:
                                if not "http://" in string:
                                    if not "https://" in string:
                                        string = "http://" + string
                                h=open(SOURCES_FILE).read()
                                i=h.replace('\n','U').replace('\r','F')
                                j=i.replace(str(checker), str(string))
                                k=j.replace('U','\n').replace('F','\r')
                                f= open(SOURCES_FILE, mode='w')
                                f.write(k)
                                f.close()
                            else: quit()
                        elif choice == 1:
                            found = 1
                            counter = counter + 1
                            h=open(SOURCES_FILE).read()
                            i=h.replace('\n','U').replace('\r','F')
                            j=i.replace(str(item), '')
                            k=j.replace('U','\n').replace('F','\r')
                            l=k.replace('<source></source>','').replace('        \n','')
                            f= open(SOURCES_FILE, mode='w')
                            f.write(l)
                            f.close()
                        else:
                            found = 1
                            counter = counter + 1
                dp.update(0,"","","Working: " + str(passed) + "        Broken: " + str(counter))
                if dp.iscanceled():
                    dialog.ok(AddonTitle, 'The source check was cancelled')
                    dp.close()
                    quit()
        except:
            dialog.ok(AddonTitle, "Sorry we could not perform this test on your device.")
            dp.close()
            quit()
    else:
        dialog.ok(AddonTitle, "Sorry there are no sources present on your device.")
        dp.close()
        quit()
    dialog.ok(AddonTitle,'We have checked your sources and found:', 'Working Sources: ' + str(passed),'Broken Sources: ' + str(counter))

def CHECK_BROKEN_REPOS():

    dialog = xbmcgui.Dialog()

    dp.create(AddonTitle,"Testing Internet Connection...",'', 'Please Wait...') 

    try:
        open_url("http://www.google.com")
    except:
        dialog.ok(AddonTitle,'Error: It appears you do not currently have an active internet connection. This will cause false positives in the test. Please try again with an active internet connection.')
        sys.exit(0)
    passed = 0
    failed = 0
    HOME =  xbmc.translatePath('special://home/addons/')
    dp.update(0,"We are currently checking:",'',"Working: 0        Broken: 0")
    url = HOME
    for root, dirs, files in os.walk(url):
        for file in files:
            if file == "addon.xml":
                a=open((os.path.join(root, file))).read()   
                if "info compressed=" in str(a):
                    match = re.compile('<info compressed="false">(.+?)</info>').findall(a)
                    for checker in match:
                        dp.update(0,"","" + checker + "[/B][/COLOR]", "")
                        try:
                            open_url(checker)
                            passed = passed + 1
                        except:
                            try:
                                checkme = open_url(checker)
                            except:
                                pass
                        
                            try:
                                error_out = 0
                                if not "this does not matter its just a test" in ("%s" % checkme):
                                    error_out = 0
                            except:
                                error_out = 1

                            if error_out == 0:
                                if not "addon id=" in ("%s" % checkme):    
                                    failed = failed + 1
                                    match = re.compile('<addon id="(.+?)".+?ame="(.+?)" version').findall(a)
                                    for repo_id,repo_name in match:
                                        dialog = xbmcgui.Dialog()
                                        default_path = xbmc.translatePath("special://home/addons/")
                                        file_path = xbmc.translatePath(file)
                                        full_path = default_path + repo_id
                                        choice = xbmcgui.Dialog().yesno(AddonTitle,"The " + repo_name + " appears to be broken. We attempted to connect to the repo but it was unsuccessful.",'To remove this repository please click Yes',yeslabel='Yes',nolabel='No')
                                        if choice == 1:
                                            try:
                                                shutil.rmtree(full_path)
                                            except:
                                                dialog.ok(AddonTitle,"Sorry we were unable to remove " + repo_name)
                                else:
                                    passed = passed + 1
                            else:
                                failed = failed + 1
                                match = re.compile('<addon id="(.+?)".+?ame="(.+?)" version').findall(a)
                                for repo_id,repo_name in match:
                                    dialog = xbmcgui.Dialog()
                                    default_path = xbmc.translatePath("special://home/addons/")
                                    file_path = xbmc.translatePath(file)
                                    full_path = default_path + repo_id
                                    choice = xbmcgui.Dialog().yesno(AddonTitle,"The " + repo_name + " appears to be broken. We attempted to connect to the repo but it was unsuccessful.",'To remove this repository please click Yes',yeslabel='Yes',nolabel='No')
                                    if choice == 1:
                                        try:
                                            shutil.rmtree(full_path)
                                        except:
                                            dialog.ok(AddonTitle,"Sorry we were unable to remove " + repo_name)
            
                        if dp.iscanceled():
                            dialog = xbmcgui.Dialog()
                            dialog.ok(AddonTitle, 'The repository check was cancelled')
                            dp.close()
                            sys.exit()
                        dp.update(0,"","","Working: " + str(passed) + "        Broken: " + str(failed))
                        
    dialog.ok(AddonTitle,'We have checked your repositories and found:', 'Working Sources: ' + str(passed),'Broken Sources: ' + str(failed))

#######################################################################
#                       Delete Packages
#######################################################################

def purgePackages():
    
    purgePath = xbmc.translatePath('special://home/addons/packages')
    dialog = xbmcgui.Dialog()
    for root, dirs, files in os.walk(purgePath):
            file_count = 0
            file_count += len(files)
    if dialog.yesno("Delete Package Cache Files", "%d packages found."%file_count, "Delete Them?"):  
        for root, dirs, files in os.walk(purgePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:            
                try:
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                except: pass
                dialog = xbmcgui.Dialog()
                dialog.ok(AddonTitle, "Deleting Packages all done")
            else:
                dialog = xbmcgui.Dialog()
                dialog.ok(AddonTitle, "No Packages to Purge")

    xbmc.executebuiltin("Container.Refresh")

#######################################################################
#                       Autoclean Function
#######################################################################
def setupCacheEntries():
    entries = 5 #make sure this refelcts the amount of entries you have
    dialogName = ["WTF", "4oD", "BBC iPlayer", "Simple Downloader", "ITV"]
    pathName = ["special://profile/addon_data/plugin.video.whatthefurk/cache", "special://profile/addon_data/plugin.video.4od/cache",
                    "special://profile/addon_data/plugin.video.iplayer/iplayer_http_cache","special://profile/addon_data/script.module.simple.downloader",
                    "special://profile/addon_data/plugin.video.itv/Images"]
                    
    cacheEntries = []
    
    for x in range(entries):
        cacheEntries.append(cacheEntry(dialogName[x],pathName[x]))
    
    return cacheEntries

#######################################################################
#                       Delete Crash Log Function
#######################################################################

def DeleteCrashLogs():  

    HomeDir = xbmc.translatePath('special://home')
    WindowsCache = os.path.join(xbmc.translatePath('special://home'), 'cache')
    OtherCache = xbmc.translatePath('special://temp')
    
    if os.path.exists(HomeDir)==True:   
        dialog = xbmcgui.Dialog()
        if dialog.yesno(AddonTitle, '', "Do you want to delete old crash logs?"):
            path=Windows
            import glob
            for infile in glob.glob(os.path.join(path, '*.dmp')):
                File=infile
                print infile
                os.remove(infile)
                
            for infile in glob.glob(os.path.join(path, '*.txt')):
                File=infile
                print infile
                os.remove(infile)
                
        if os.path.exists(WindowsCache)==True:   
            path=WindowsCache
            import glob
            for infile in glob.glob(os.path.join(path, '*.dmp')):
                File=infile
                print infile
                os.remove(infile)
                
            for infile in glob.glob(os.path.join(path, '*.txt')):
                File=infile
                print infile
                os.remove(infile)

        if os.path.exists(OtherCache)==True:   
            path=OtherCache
            import glob
            for infile in glob.glob(os.path.join(path, '*.dmp')):
                File=infile
                print infile
                os.remove(infile)
                
            for infile in glob.glob(os.path.join(path, '*.txt')):
                File=infile
                print infile
                os.remove(infile)
        
        dialog = xbmcgui.Dialog()
        dialog.ok(AddonTitle, "Crash logs deleted")
    else:
        dialog = xbmcgui.Dialog()
        dialog.ok(AddonTitle, "An error occured")

def autocleanask():
    
    choice = xbmcgui.Dialog().yesno(AddonTitle, 'Selecting Yes will delete your cache, thumbnails and packages.','Do you wish to continue?', yeslabel='Yes',nolabel='No')
    if choice == 1:
        autocleannow()
    
def autocleannow():

    HomeDir = xbmc.translatePath('special://home')
    WindowsCache = os.path.join(xbmc.translatePath('special://home'), 'cache')
    OtherCache = os.path.join(xbmc.translatePath('special://home'), 'temp')
    
    if os.path.exists(HomeDir)==True:   
        path=Windows
        import glob
        for infile in glob.glob(os.path.join(path, '*.dmp')):
            File=infile
            print infile
            os.remove(infile)
            
        for infile in glob.glob(os.path.join(path, '*.txt')):
            File=infile
            print infile
            os.remove(infile)
                
        if os.path.exists(WindowsCache)==True:   
            path=WindowsCache
            import glob
            for infile in glob.glob(os.path.join(path, '*.dmp')):
                File=infile
                print infile
                os.remove(infile)
                
            for infile in glob.glob(os.path.join(path, '*.txt')):
                File=infile
                print infile
                os.remove(infile)

        if os.path.exists(OtherCache)==True:   
            path=OtherCache
            import glob
            for infile in glob.glob(os.path.join(path, '*.dmp')):
                File=infile
                print infile
                os.remove(infile)
                
            for infile in glob.glob(os.path.join(path, '*.txt')):
                File=infile
                print infile
                os.remove(infile)

    if os.path.exists(cachePath)==True:    
        for root, dirs, files in os.walk(cachePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            checker = (os.path.join(root, d))
                            if not "archive_cache" in str(checker):
                                shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
                
    if os.path.exists(tempPath)==True:    
        for root, dirs, files in os.walk(tempPath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            checker = (os.path.join(root, d))
                            if not "archive_cache" in str(checker):
                                shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
    if xbmc.getCondVisibility('system.platform.ATV2'):
        atv2_cache_a = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')
        
        for root, dirs, files in os.walk(atv2_cache_a):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:                
                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            checker = (os.path.join(root, d))
                            if not "archive_cache" in str(checker):
                                shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
        atv2_cache_b = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')
        
        for root, dirs, files in os.walk(atv2_cache_b):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:
                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            checker = (os.path.join(root, d))
                            if not "archive_cache" in str(checker):
                                shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass    
                
    cacheEntries = setupCacheEntries()
                                         
    for entry in cacheEntries:
        clear_cache_path = xbmc.translatePath(entry.path)
        if os.path.exists(clear_cache_path)==True:    
            for root, dirs, files in os.walk(clear_cache_path):
                file_count = 0
                file_count += len(files)
                if file_count > 0:
                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            checker = (os.path.join(root, d))
                            if not "archive_cache" in str(checker):
                                shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                            
                else:
                    pass
        
    if os.path.exists(thumbnailPath)==True:  
                for root, dirs, files in os.walk(thumbnailPath):
                    file_count = 0
                    file_count += len(files)
                    if file_count > 0:                
                        for f in files:
                            try:
                                os.unlink(os.path.join(root, f))
                            except:
                                pass
    else:
        pass
    
    text13 = os.path.join(databasePath,"Textures13.db")
    try:
        os.unlink(text13)
    except OSError:
        pass
        
    purgePath = xbmc.translatePath('special://home/addons/packages')
    dialog = xbmcgui.Dialog()
    for root, dirs, files in os.walk(purgePath):
            file_count = 0
            file_count += len(files)
    for root, dirs, files in os.walk(purgePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:            
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))

    xbmc.executebuiltin("Container.Refresh")

    xbmcgui.Dialog().ok(AddonTitle,"Auto clean finished.","Your cache, thumbnails and packages have all been deleted")

def AUTO_CLEAR_CACHE_MB():

    HomeDir = xbmc.translatePath('special://home')
    WindowsCache = os.path.join(xbmc.translatePath('special://home'), 'cache')
    OtherCache = os.path.join(xbmc.translatePath('special://home'), 'temp')

    if os.path.exists(cachePath)==True:    
        for root, dirs, files in os.walk(cachePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            checker = (os.path.join(root, d))
                            if not "archive_cache" in str(checker):
                                shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
                
    if os.path.exists(tempPath)==True:    
        for root, dirs, files in os.walk(tempPath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            checker = (os.path.join(root, d))
                            if not "archive_cache" in str(checker):
                                shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
    if xbmc.getCondVisibility('system.platform.ATV2'):
        atv2_cache_a = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')
        
        for root, dirs, files in os.walk(atv2_cache_a):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:                
                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            checker = (os.path.join(root, d))
                            if not "archive_cache" in str(checker):
                                shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
        atv2_cache_b = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')
        
        for root, dirs, files in os.walk(atv2_cache_b):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:
                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            checker = (os.path.join(root, d))
                            if not "archive_cache" in str(checker):
                                shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass    
                
    cacheEntries = setupCacheEntries()
                                         
    for entry in cacheEntries:
        clear_cache_path = xbmc.translatePath(entry.path)
        if os.path.exists(clear_cache_path)==True:    
            for root, dirs, files in os.walk(clear_cache_path):
                file_count = 0
                file_count += len(files)
                if file_count > 0:
                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            checker = (os.path.join(root, d))
                            if not "archive_cache" in str(checker):
                                shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                            
                else:
                    pass

    xbmc.executebuiltin("Container.Refresh")

def AUTO_CLEAR_PACKAGES_MB():

    time.sleep(60)

    purgePath = xbmc.translatePath('special://home/addons/packages')
    dialog = xbmcgui.Dialog()
    for root, dirs, files in os.walk(purgePath):
            file_count = 0
            file_count += len(files)
    for root, dirs, files in os.walk(purgePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                try:
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                except: pass

def AUTO_CLEAR_THUMBS_MB():

    if os.path.exists(thumbnailPath)==True:  
                for root, dirs, files in os.walk(thumbnailPath):
                    file_count = 0
                    file_count += len(files)
                    if file_count > 0:                
                        for f in files:
                            try:
                                os.unlink(os.path.join(root, f))
                            except:
                                pass
    else:
        pass
    
    text13 = os.path.join(databasePath,"Textures13.db")
    try:
        os.unlink(text13)
    except OSError:
        pass

def Auto_Startup():

    AutoThumbs()
    AutoCache()
    time.sleep(60)
    AutoPackages()

def AutoCache():

    if os.path.exists(cachePath)==True:    
        for root, dirs, files in os.walk(cachePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            checker = (os.path.join(root, d))
                            if not "archive_cache" in str(checker):
                                shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
                
    if os.path.exists(tempPath)==True:    
        for root, dirs, files in os.walk(tempPath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            checker = (os.path.join(root, d))
                            if not "archive_cache" in str(checker):
                                shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
    if xbmc.getCondVisibility('system.platform.ATV2'):
        atv2_cache_a = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')
        
        for root, dirs, files in os.walk(atv2_cache_a):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:                
                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            checker = (os.path.join(root, d))
                            if not "archive_cache" in str(checker):
                                shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
        atv2_cache_b = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')
        
        for root, dirs, files in os.walk(atv2_cache_b):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:
                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            checker = (os.path.join(root, d))
                            if not "archive_cache" in str(checker):
                                shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
            else:
                pass    
                
    cacheEntries = setupCacheEntries()
                                         
    for entry in cacheEntries:
        clear_cache_path = xbmc.translatePath(entry.path)
        if os.path.exists(clear_cache_path)==True:    
            for root, dirs, files in os.walk(clear_cache_path):
                file_count = 0
                file_count += len(files)
                if file_count > 0:
                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            checker = (os.path.join(root, d))
                            if not "archive_cache" in str(checker):
                                shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                            
                else:
                    pass

def AutoThumbs():

    if os.path.exists(thumbnailPath)==True:  
                for root, dirs, files in os.walk(thumbnailPath):
                    file_count = 0
                    file_count += len(files)
                    if file_count > 0:                
                        for f in files:
                            try:
                                os.unlink(os.path.join(root, f))
                            except: pass
    else: pass
    
    text13 = os.path.join(databasePath,"Textures13.db")
    try:
        os.unlink(text13)
    except: pass

def AutoPackages():

    time.sleep(60)
    purgePath = xbmc.translatePath('special://home/addons/packages')
    for root, dirs, files in os.walk(purgePath):
            file_count = 0
            file_count += len(files)
    for root, dirs, files in os.walk(purgePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:            
                try:
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                except: pass

def AutoCrash():  

    HomeDir = xbmc.translatePath('special://home')
    WindowsCache = os.path.join(xbmc.translatePath('special://home'), 'cache')
    OtherCache = os.path.join(xbmc.translatePath('special://home'), 'temp')
    
    if os.path.exists(HomeDir)==True:   
        path=Windows
        import glob
        for infile in glob.glob(os.path.join(path, '*.dmp')):
            File=infile
            print infile
            os.remove(infile)
                
        for infile in glob.glob(os.path.join(path, '*.txt')):
            File=infile
            print infile
            os.remove(infile)
                
    if os.path.exists(WindowsCache)==True:   
        path=WindowsCache
        import glob
        for infile in glob.glob(os.path.join(path, '*.dmp')):
            File=infile
            print infile
            os.remove(infile)
                
        for infile in glob.glob(os.path.join(path, '*.txt')):
            File=infile
            print infile
            os.remove(infile)

    if os.path.exists(OtherCache)==True:   
        path=OtherCache
        import glob
        for infile in glob.glob(os.path.join(path, '*.dmp')):
            File=infile
            print infile
            os.remove(infile)
                
        for infile in glob.glob(os.path.join(path, '*.txt')):
            File=infile
            print infile
            os.remove(infile)

def BASE64_ENCODE_DECODE():

    dialog = xbmcgui.Dialog()
    choice = dialog.select(AddonTitle, ['Encode A String','Decode A String'])
    if choice == 0:
        vq = _get_keyboard( heading="Enter String to Encode" )
        if ( not vq ): return False, 0
        input = str(vq)
        output = base64.b64encode(input)
        dialog.ok(AddonTitle, 'Orignal String: ' + input, 'Encrypted String: ' + output)
    else:
        vq = _get_keyboard( heading="Enter String to Decode" )
        if ( not vq ): return False, 0
        input = str(vq)
        output = base64.b64decode(vq)
        dialog.ok(AddonTitle, 'Encrypted String: ' + input, 'Original String: ' + output)

#######################################################################
#               TURN AUTO CLEAN ON|OFF
####################################################################### 

def AUTO_CLEAN_ON_OFF():

    startup_clean = plugintools.get_setting("acstartup")

    if startup_clean == 'true':
        choice = xbmcgui.Dialog().yesno(AddonTitle, 'Please confirm that you wish to disable automated maintenance on startup.')
        if choice == 1:
            CURRENT = '    <setting id="acstartup" value="true" />'
            NEW     = '    <setting id="acstartup" value="false" />'
        else: quit()
    else:
        choice = xbmcgui.Dialog().yesno(AddonTitle, 'Please confirm that you wish to enable automated maintenance on startup.')
        if choice == 1:
            CURRENT = '    <setting id="acstartup" value="false" />'
            NEW     = '    <setting id="acstartup" value="true" />'
        else: quit()

    HOME         =  xbmc.translatePath('special://userdata/addon_data/plugin.program.indigo')
    for root, dirs, files in os.walk(HOME):  #Search all xml files and replace physical with special
        for file in files:
            if file == "settings.xml":
                 a=open((os.path.join(root, file))).read()
                 b=a.replace(CURRENT, NEW)
                 f = open((os.path.join(root, file)), mode='w')
                 f.write(str(b))
                 f.close()

    xbmc.executebuiltin("Container.Refresh")

#######################################################################
#               TURN WEEKLY AUTO CLEAN ON|OFF
####################################################################### 

def AUTO_WEEKLY_CLEAN_ON_OFF():

    startup_clean = plugintools.get_setting("clearday")

    if startup_clean == '0':
        choice = xbmcgui.Dialog().yesno(AddonTitle, 'Please confirm that you wish to enable weekly automated maintenance.')
        if choice == 1:
            CURRENT = '    <setting id="clearday" value="0" />'
            NEW     = '    <setting id="clearday" value="1" />'
        else: quit()
    else:
        choice = xbmcgui.Dialog().yesno(AddonTitle, 'Please confirm that you wish to disable weekly automated maintenance.')
        if choice == 1:
            if startup_clean == '1':
                CURRENT = '    <setting id="clearday" value="1" />'
                NEW     = '    <setting id="clearday" value="0" />'
            elif startup_clean == '2':
                CURRENT = '    <setting id="clearday" value="2" />'
                NEW     = '    <setting id="clearday" value="0" />'
            elif startup_clean == '3':
                CURRENT = '    <setting id="clearday" value="3" />'
                NEW     = '    <setting id="clearday" value="0" />'
            elif startup_clean == '4':
                CURRENT = '    <setting id="clearday" value="4" />'
                NEW     = '    <setting id="clearday" value="0" />'
            elif startup_clean == '5':
                CURRENT = '    <setting id="clearday" value="5" />'
                NEW     = '    <setting id="clearday" value="0" />'
            elif startup_clean == '6':
                CURRENT = '    <setting id="clearday" value="6" />'
                NEW     = '    <setting id="clearday" value="0" />'
            elif startup_clean == '7':
                CURRENT = '    <setting id="clearday" value="7" />'
                NEW     = '    <setting id="clearday" value="0" />'
        else: quit()


    HOME         =  xbmc.translatePath('special://userdata/addon_data/plugin.program.indigo')
    for root, dirs, files in os.walk(HOME):  #Search all xml files and replace physical with special
        for file in files:
            if file == "settings.xml":
                 a=open((os.path.join(root, file))).read()
                 b=a.replace(CURRENT, NEW)
                 f = open((os.path.join(root, file)), mode='w')
                 f.write(str(b))
                 f.close()

    xbmc.executebuiltin("Container.Refresh")
    
def _get_keyboard( default="", heading="", hidden=False ):
    """ shows a keyboard and returns a value """
    keyboard = xbmc.Keyboard( default, heading, hidden )
    keyboard.doModal()
    if ( keyboard.isConfirmed() ):
        return unicode( keyboard.getText(), "utf-8" )
    return default

def get_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def convertSize(size):
   import math
   if (size == 0):
       return '0 MB'
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size,1024)))
   p = math.pow(1024,i)
   s = round(size/p,2)
   if size_name[i] == "B":
        return '%s %s' % (s,size_name[i]) + ''
   if size_name[i] == "KB":
        return '%s %s' % (s,size_name[i]) + ''
   if size_name[i] == "GB":
        return '%s %s' % (s,size_name[i]) + ''
   if size_name[i] == "TB":
        return '%s %s' % (s,size_name[i]) + ''
   if s < 50:
        return '%s %s' % (s,size_name[i]) + ''
   if s >= 50:
        if s < 100:
            return '%s %s' % (s,size_name[i]) + ''
   if s >= 100:
        return '%s %s' % (s,size_name[i]) + ''

def convertSizeInstall(size):
   import math
   if (size == 0):
       return '0 MB'
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size,1024)))
   p = math.pow(1024,i)
   s = round(size/p,2)
   if size_name[i] == "B":
        return '%s %s' % (s,size_name[i]) + ''
   if size_name[i] == "KB":
        return '%s %s' % (s,size_name[i]) + ''
   if size_name[i] == "TB":
        return '%s %s' % (s,size_name[i]) + ''
   if s < 1000:
        return '%s %s' % (s,size_name[i]) + ''
   if s >= 1000:
        if s < 1500:
            return '%s %s' % (s,size_name[i]) + ''
   if s >= 1500:
        return '%s %s' % (s,size_name[i]) + ''

def open_url(url):

    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36')
    response = urllib2.urlopen(req, timeout = 15)
    link=response.read()
    response.close()
    return link
 
def KillKodi():
    myplatform = platform()
    print "Platform: " + str(myplatform)
    if myplatform == 'osx': # OSX
        print "############   try osx force close  #################"
        try: os._exit(1)
        except: pass
        try: os.system('killall -9 XBMC')
        except: pass
        try: os.system('killall -9 Kodi')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!!", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=white]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'linux': #Linux
        print "############   try linux force close  #################"
        try: os._exit(1)
        except: pass
        try: os.system('killall XBMC')
        except: pass
        try: os.system('killall Kodi')
        except: pass
        try: os.system('killall -9 xbmc.bin')
        except: pass
        try: os.system('killall -9 kodi.bin')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!!", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=white]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'android': # Android  
        print "############   try android force close  #################"
        try: os._exit(1)
        except: pass
        try: os.system('adb shell am force-stop org.xbmc.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc.xbmc')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc')
        except: pass     
        try: os.system('adb shell am force-stop com.semperpax.spmc16')
        except: pass
        try: os.system('adb shell am force-stop com.spmc16')
        except: pass            
        try: os.system('adb shell am force-stop com.semperpax.spmc')
        except: pass
        try: os.system('adb shell am force-stop com.spmc')
        except: pass    
        try: os.system('adb shell am force-stop uk.droidbox.dbmc')
        except: pass
        try: os.system('adb shell am force-stop uk.dbmc')
        except: pass   
        try: os.system('adb shell am force-stop com.perfectzoneproductions.jesusboxmedia')
        except: pass
        try: os.system('adb shell am force-stop com.jesusboxmedia')
        except: pass 
        dialog.ok("[COLOR=red][B]WARNING  !!!", "Your system has been detected as Android, you ", "[COLOR=yellow][B]MUST force close XBMC/Kodi. [COLOR=white]DO NOT[/COLOR] exit cleanly via the menu.","Pulling the power cable is the simplest method to force close.")
    elif myplatform == 'windows': # Windows
        print "############   try windows force close  #################"
        try: os._exit(1)
        except: pass
        try:
            os.system('@ECHO off')
            os.system('tskill XBMC.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('tskill Kodi.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im Kodi.exe /f')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im XBMC.exe /f')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!!", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=white]DO NOT[/COLOR] exit cleanly via the menu.","Use task manager and NOT ALT F4")
    else: #ATV
        print "############   try atv force close  #################"
        try: os._exit(1)
        except: pass
        try: os.system('killall AppleTV')
        except: pass
        print "############   try raspbmc force close  #################" #OSMC / Raspbmc
        try: os.system('sudo initctl stop kodi')
        except: pass
        try: os.system('sudo initctl stop xbmc')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!!", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=white]DO NOT[/COLOR] exit via the menu.","Your platform could not be detected so just pull the power cable.")    
        
##########################
###DETERMINE PLATFORM#####
##########################
        
def platform():
    if xbmc.getCondVisibility('system.platform.android'):
        return 'android'
    elif xbmc.getCondVisibility('system.platform.linux'):
        return 'linux'
    elif xbmc.getCondVisibility('system.platform.windows'):
        return 'windows'
    elif xbmc.getCondVisibility('system.platform.osx'):
        return 'osx'
    elif xbmc.getCondVisibility('system.platform.atv2'):
        return 'atv2'
    elif xbmc.getCondVisibility('system.platform.ios'):
        return 'ios'
		