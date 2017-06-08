# -*- coding: utf-8 -*-
import urllib2,urllib,re,os
import sys
import time,datetime
import xbmcplugin,xbmcgui,xbmc, xbmcaddon, downloader, extract, time
from libs import kodi
from libs import speedtest
import maintool
import socket, base64, shutil
import freshstart
import  installer
import installer
from libs import addon_able
import backup
from libs import dom_parser
import htmlentitydefs
from libs import viewsetter
import TextViewer
import plugintools

addon_id=kodi.addon_id
addon = (addon_id, sys.argv)
artwork = xbmc.translatePath(os.path.join('special://home','addons',addon_id,'art/'))
fanart = artwork+'fanart.jpg'
messages = xbmc.translatePath(os.path.join('special://home','addons',addon_id,'resources','messages/'))
execute = xbmc.executebuiltin
hubpath=xbmc.translatePath(os.path.join('special://home','addons','repository.xbmchub'))
uploaderpath=xbmc.translatePath(os.path.join('special://home','addons','script.tvaddons.debug.log'))

oldinstaller =xbmc.translatePath(os.path.join('special://home','addons','plugin.program.addoninstaller'))
oldnotify = xbmc.translatePath(os.path.join('special://home','addons','plugin.program.xbmchub.notifications'))
oldmain = xbmc.translatePath(os.path.join('special://home','addons','plugin.video.xbmchubmaintenance'))
oldwiz =  xbmc.translatePath(os.path.join('special://home','addons','plugin.video.hubwizard'))
oldfresh =  xbmc.translatePath(os.path.join('special://home','addons','plugin.video.freshstart'))
oldmain2 = xbmc.translatePath(os.path.join('special://home','addons','plugin.video.hubmaintenance'))

def get_kversion():
    full_version_info = xbmc.getInfoLabel('System.BuildVersion')
    baseversion = full_version_info.split(".")
    intbase = int(baseversion[0])
    return  baseversion[0]




def main_menu():


    # sourcePath = xbmc.translatePath(os.path.join('special://home','userdata'))
    # newSource = sourcePath+"/sources.xml"
    #
    # with open(newSource) as f:
    #   file_str = f.read()
    #   if 'fusion' not in file_str:
    #       kodi.log("FUSION NOT FOUND")
    #
    #       # do stuff with file_str
    #       #kodi.log(file_str)
    #       with open(newSource, "w") as f:
    #           f.write(file_str)
    #   else:
    #       kodi.log("FUSION IS INSTALLED")

    ###########TRY POP########
    if len(kodi.get_setting('notify')) > 0:
        kodi.set_setting('notify', str(int(kodi.get_setting('notify')) + 1))
    else:
        kodi.set_setting('notify', "1")
    if int(kodi.get_setting('notify')) == 1:
        xbmcgui.Dialog().notification('Need Support?','www.tvaddons.ag',artwork+'icon.png',3000,False)
    elif int(kodi.get_setting('notify')) == 5:
        kodi.set_setting('notify', "0")
    #########END POP###########

    if kodi.get_setting('hasran')=='false':
        kodi.set_setting('hasran','true')

    if kodi.get_setting('set_rtmp')=='false':
        try:
            addon_able.set_enabled("inputstream.adaptive")
        except:
            pass
        time.sleep(0.5)
        try:
            addon_able.set_enabled("inputstream.rtmp")
        except:
            pass
        time.sleep(0.5)
        xbmc.executebuiltin("XBMC.UpdateLocalAddons()")
        kodi.set_setting('set_rtmp', 'true')
    try:
        if not os.path.exists(hubpath):
            installer.HUBINSTALL('TVADDONSRepo', 'http://offshoregit.com/xbmchub/xbmc-hub-repo/raw/master/repository.xbmchub/','repository.xbmchub')
            xbmc.executebuiltin("XBMC.UpdateLocalAddons()")
            addon_able.set_enabled("repository.xbmchub")
    except:
            pass
    try:
        if not os.path.exists(uploaderpath):
            installer.HUBINSTALL('TVADDONSLogUploader', 'https://offshoregit.com/xbmchub/xbmc-hub-repo/raw/master/script.tvaddons.debug.log/','script.tvaddons.debug.log')
            xbmc.executebuiltin("XBMC.UpdateLocalAddons()")
            addon_able.set_enabled("script.tvaddons.debug.log")
    except:
            pass

    if os.path.exists(oldinstaller):
        shutil.rmtree(oldinstaller)
    if os.path.exists(oldnotify):
        shutil.rmtree(oldnotify)
    if os.path.exists(oldmain):
        shutil.rmtree(oldmain)
    if os.path.exists(oldwiz):
        shutil.rmtree(oldwiz)
    if os.path.exists(oldfresh):
        shutil.rmtree(oldfresh)

    kodi.addDir("Addon Installer",'','call_installer',artwork+'addon_installer.png',description="It’s like an App Store for Kodi addons!")
    kodi.addDir("Maintenance Tools",'','call_maintool',artwork+'maintool.png',description="Keep your Kodi setup running at optimum performance!")
    #kodi.addDir("Kodi Librtmp Files",'','get_libs',artwork+'librtmp_files.png')
    kodi.addDir("Factory Restore",'','call_restore',artwork+'factory_restore.png',description="Start off fresh, wipe your Kodi setup clean!")
    kodi.addItem("Log Uploader",'','log_upload',artwork+'log_uploader.png',description="Easily upload your error logs for troubleshooting!")
    kodi.addDir("Network Speed Test",'','runspeedtest',artwork+'speed_test.png',description="How fast is your internet?")
    kodi.addDir("System Information",'','system_info',artwork+'system_info.png',description="Useful information about your Kodi setup!")
    kodi.addDir("Sports Listings",'','call_sports',artwork+'sports_list.png',description="Who’s playing what today?")
    kodi.addDir('Backup / Restore', '', 'backup_restore', artwork + 'backup_restore.png',description="Backup or restore your Kodi configuration in minutes!")
    kodi.addItem("Log Viewer", '', 'log_view', artwork + 'log_uploader.png',description="Easily view your error log without leaving Kodi!")
    if kodi.get_setting('notifications-on-startup') == 'false':
        kodi.addItem("Notifications (Opt Out)",'','enable_notify',artwork+'notification_optout.png',description="Unsubscribe from important TV ADDONS notifications!")
    if kodi.get_setting('notifications-on-startup') == 'true':
        kodi.addItem("Notifications (Opt In)",'','disable_notify',artwork+'notification_in.png',description="Subscribe to important TV ADDONS notifications!")

    viewsetter.set_view("sets")

#################
def do_log_uploader():
    xbmc.executebuiltin("RunAddon(script.tvaddons.debug.log)")

#################
#################
def what_sports():

    link = OPEN_URL('http://www.wheresthematch.com/tv/home.asp').replace('\r','').replace('\n','').replace('\t','')
    match = re.compile('href="http://www.wheresthematch.com/fixtures/(.+?).asp.+?class="">(.+?)</em> <em class="">v</em> <em class="">(.+?)</em>.+?time-channel ">(.+?)</span>').findall(link)
    for game,name1,name2,gametime in match:
        kodi.addItem('[COLOR gold][B]'+game+' '+'[/COLOR][/B]- [COLOR white]'+name1+' vs '+name2+' - '+gametime+' [/COLOR]','','',artwork+'icon.png',description='[COLOR gold][B]'+game+' '+'[/COLOR][/B]- [COLOR white]'+name1+' vs '+name2+' - '+gametime+' [/COLOR]')
        xbmc.executebuiltin("Container.SetViewMode(55)")
########AMERICAN###############
    link = OPEN_URL('http://www.tvguide.com/sports/live-today/').replace('\r', '').replace('\n', '').replace('\t', '')
    sections = dom_parser.parse_dom(link, 'div', {'class': "listings-program-content"})
    listings = dom_parser.parse_dom(sections, 'span', {'class': "listings-program-link"})
    for stuff in sections:
        match = re.compile(
            'class="listings-program-link">(.+?)</span></h3>.+?class="listings-program-link">.+?listings-program-airing-info">(.+?)</p><p.+?description">(.+?)</p>').findall(
            stuff)
        for name, time, description in match:
            kodi.addItem('[COLOR gold][B]' + name_cleaner(name) + ' ' + '[/COLOR][/B]- [COLOR white]' + ' - ' + time + ' [/COLOR]','', '', artwork + 'icon.png',description='[COLOR gold][B]' + name_cleaner(name) + ' ' + '[/COLOR][/B]- [COLOR white]' + ' - ' + time + ' [/COLOR]')
    viewsetter.set_view("files")


def rtmp_lib():
    liblist = "http://indigo.tvaddons.ag/librtmp/rtmplist.txt"
    link = OPEN_URL(liblist).replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?ersion="(.+?)"').findall(link)
    kodi.addItem('[COLOR gold][B]Files Will Be Donwloaded to the Kodi Home directory, You Will Need To Manually Install From There.[/COLOR][/B]','',100,'','','')
    #kodi.addItem('[COLOR gold]-----------------------------------------------------------[/COLOR]','',100,'','','')
    for name,url,description in match:
        kodi.addDir(name,url,"lib_installer",artwork+'icon.png')

    viewsetter.set_view("sets")



def enable_notify():
    confirm=xbmcgui.Dialog()
    if confirm.yesno('Community Notifications',"Please confirm that you wish to OPT-OUT of community notifications! "," "):
        kodi.logInfo ("disabled notifications")
        kodi.set_setting('notifications-on-startup','true')
        dialog = xbmcgui.Dialog()
        dialog.ok("Notifications Disabled", "                     You have unsubscribed from notifications!")
        xbmc.executebuiltin("Container.Refresh()")
    else:
        return

def disable_notify():
    confirm=xbmcgui.Dialog()
    if confirm.yesno('Community Notifications',"Please confirm that you wish to OPT-IN to community notifications! "," "):
        kodi.set_setting('notifications-on-startup','false')
        kodi.logInfo("enabled notifications")
        dialog = xbmcgui.Dialog()
        dialog.ok("Notifications Enabled", "                     You have subscribed to notifications!")
        xbmc.executebuiltin("Container.Refresh()")
    else:
        return




def system_info():
    systime = xbmc.getInfoLabel('System.Time ')
    dns1 = xbmc.getInfoLabel('Network.DNS1Address')
    gateway = xbmc.getInfoLabel('Network.GatewayAddress')
    ipaddy = xbmc.getInfoLabel('Network.IPAddress')
    linkstate= xbmc.getInfoLabel('Network.LinkState').replace("Link:","")
    freespace =xbmc.getInfoLabel('System.FreeSpace')
    screenres = xbmc.getInfoLabel('system.screenresolution')
    totalspace = xbmc.getInfoLabel('System.TotalSpace')
    freemem = xbmc.getInfoLabel('System.FreeMemory')
    #######################################################################
    #           FIND WHAT VERSION OF KODI IS RUNNING
    #######################################################################


    xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
    versioni=xbmc_version[:4]

    # if version >= 11.0 and version <= 11.9:
    #   codename = 'Eden'
    # if version >= 12.0 and version <= 12.9:
    #   codename = 'Frodo'
    # if version >= 13.0 and version <= 13.9:
    #   codename = 'Gotham'
    # if version >= 14.0 and version <= 14.9:
    #   codename = 'Helix'
    # if version >= 15.0 and version <= 15.9:
    #   codename = 'Isengard'
    # if version >= 16.0 and version <= 16.9:
    #   codename = 'Jarvis'
    # if version >= 17.0 and version <= 17.9:
    #   codename = 'Krypton'


    VERSIONS = {10: 'Dharma', 11: 'Eden', 12: 'Frodo', 13: 'Gotham', 14: 'Helix', 15: 'Isengard', 16: 'Jarvis',17: 'Krypton'}
    v_str = versioni
    version = int(float(v_str.strip()))
    unknown = chr(version + 58) + '**'
    codename = VERSIONS.get(version, unknown)

    f = urllib.urlopen("http://www.canyouseeme.org/")
    html_doc = f.read()
    f.close()
    m = re.search('(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)',html_doc)

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
                PACKAGES_SIZE_BYTE = maintool.get_size(PACKAGES)
                THUMB_SIZE_BYTE    = maintool.get_size(THUMBS)
            except: pass
        else:
            try:
                CACHE_SIZE_BYTE    = maintool.get_size(CACHE)
                PACKAGES_SIZE_BYTE = maintool.get_size(PACKAGES)
                THUMB_SIZE_BYTE    = maintool.get_size(THUMBS)
            except: pass
        
        if CACHE == "NULL":
            try:
                PACKAGES_SIZE = maintool.convertSize(PACKAGES_SIZE_BYTE)
                THUMB_SIZE    = maintool.convertSize(THUMB_SIZE_BYTE)
            except: pass
        else:
            try:
                CACHE_SIZE    = maintool.convertSize(CACHE_SIZE_BYTE)
                PACKAGES_SIZE = maintool.convertSize(PACKAGES_SIZE_BYTE)
                THUMB_SIZE    = maintool.convertSize(THUMB_SIZE_BYTE)
            except: pass
        
        if CACHE == "NULL":
            CACHE_SIZE    =  "Error reading cache"

    PV = sys.version_info
    
    kodi.addItem('[COLOR ghostwhite]Version: [/COLOR][COLOR lime]%s' % codename + " " + str(versioni) + "[/COLOR]",'',100,artwork+'icon.png',"",description=" ")
    kodi.addItem('[COLOR ghostwhite]System Time: [/COLOR][COLOR lime]' + systime + '[/COLOR]','',100,artwork+'icon.png',"",description=" ")
    kodi.addItem('[COLOR ghostwhite]Gateway: [/COLOR][COLOR blue]' + gateway + '[/COLOR]','',100,artwork+'icon.png',"",description=" ")
    kodi.addItem('[COLOR ghostwhite]Local IP: [/COLOR][COLOR blue]' + ipaddy + '[/COLOR]','',100,artwork+'icon.png',"",description=" ")
    kodi.addItem('[COLOR ghostwhite]External IP: [/COLOR][COLOR blue]' + m.group(0) + '[/COLOR]','',100,artwork+'icon.png',"",description=" ")
    kodi.addItem('[COLOR ghostwhite]DNS 1: [/COLOR][COLOR blue]' + dns1 + '[/COLOR]','',100,artwork+'icon.png',"",description=" ")
    kodi.addItem('[COLOR ghostwhite]Network: [/COLOR][COLOR gold]'+linkstate + '[/COLOR]','',100,artwork+'icon.png',"",description=" ")
    kodi.addItem('[COLOR ghostwhite]Disc Space: [/COLOR][COLOR gold]'+str(totalspace) + '[/COLOR]','',100,artwork+'icon.png',"",description=" ")
    kodi.addItem('[COLOR ghostwhite]Disc Space: [/COLOR][COLOR gold]'+str(freespace) + '[/COLOR]','',100,artwork+'icon.png',"",description=" ")
    kodi.addItem('[COLOR ghostwhite]Free Memory: [/COLOR][COLOR gold]'+str(freemem) + '[/COLOR]','',100,artwork+'icon.png',"",description=" ")
    kodi.addItem('[COLOR ghostwhite]Resolution: [/COLOR][COLOR gold]' + str(screenres) + '[/COLOR]','',100,artwork+'icon.png',"",description=" ")
    kodi.addItem('[COLOR ghostwhite]Python Version: [/COLOR][COLOR lime]%d.%d.%d' % (PV[0],PV[1],PV[2]) + '[/COLOR]','',100,artwork+'icon.png',"",description=" ")
    if check_folders == "true":
        try:
            kodi.addItem("Cache Size: [COLOR blue]" + str(CACHE_SIZE) + '[/COLOR]','','null',artwork+'currentcache.png',description="Clear your device cache!")
            kodi.addItem("Packages Size: [COLOR blue]" + str(PACKAGES_SIZE) + '[/COLOR]','null','',artwork+'currentpackages.png',description="Clear your device cache!")
            kodi.addItem("Thumbnail Size: [COLOR blue]" + str(THUMB_SIZE) + '[/COLOR]','null','',artwork+'currentthumbs.png',description="Clear your device cache!")
        except: pass

    viewsetter.set_view("files")



def fullspeedtest():

    SpeedTest = base64.b64decode("aHR0cDovL2luZGlnby50dmFkZG9ucy5hZy9zcGVlZHRlc3Qvc3BlZWR0ZXN0ZmlsZS50eHQ=")
    link = OPEN_URL(SpeedTest).replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?ersion="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description in match:
        kodi.addItem('[COLOR ghostwhite]' + name + " | " + description + '[/COLOR]',url,"runtest",artwork+'speed_test.png',description=description)

    viewsetter.set_view("sets")


def name_cleaner(name):
    name = name.replace('&#8211;', '')
    name = name.replace("&#8217;", "")
    name = name.replace("&#039;s", "'s")
    name = name.replace('&uacute;', 'u')
    name = name.replace('&eacute;', 'e')
    # name = name.replace('<', '&lt;'),
    # name = name.replace('&', '&amp;')
    # name = unicode(name, errors='ignore')
    return (name)

def cleanse_title(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])

            except KeyError:
                pass

        # replace nbsp with a space
        text = text.replace(u'\xa0', u' ')
        return text

    if isinstance(text, str):
        try:
            text = text.decode('utf-8')
        except:
            pass

    return re.sub("&#?\w+;", fixup, text.strip())

def OPEN_URL(url):
    req=urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Linux; U; Android 4.2.2; en-us; AFTB Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30')
    response=urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link

def OPEN_SPEED(url):
    req = urllib2.Request(url)
    ###GET URL HEADER#########
    req.add_header('User-Agent', base64.b64decode(b'VGhlV2l6YXJkSXNIZXJl'))
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link

def _is_debugging():
    command = {'jsonrpc': '2.0', 'id': 1, 'method': 'Settings.getSettings', 'params': {'filter': {'section': 'system', 'category': 'logging'}}}
    js_data = kodi.execute_jsonrpc(command)
    for item in js_data.get('result', {}).get('settings', {}):
        if item['id'] == 'debug.showloginfo':
            return item['value']
    
    return False

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]

        return param


params=get_params()

url=None
name=None
mode=None
thumb = None


try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass

try:
        thumb=urllib.unquote_plus(params["thumb"])
except:
        pass

try:
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:
        description=urllib.unquote_plus(params["description"])
except:
        pass

try:
        filetype=urllib.unquote_plus(params["filetype"])
except:
        pass


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass


try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=urllib.unquote_plus(params["mode"])
except:
        pass

try:
        repourl=urllib.unquote_plus(params["repourl"])
except:
        pass

try:
        xmlurl=urllib.unquote_plus(params["xmlurl"])
except:
        pass

try:
        dataurl=urllib.unquote_plus(params["dataurl"])
except:
        pass



#ext = addon.queries.get('ext', '')


if kodi.get_setting('debug') == "true":
    print "Mode: "+str(mode)
    print "URL: "+str(url)
    print "Name: "+str(name)
    print "Thumb: "+str(thumb)


if mode==None :
        main_menu()


elif mode=='system_info':
        system_info()

elif mode=='get_libs':
        rtmp_lib()

elif mode=='call_sports':
        what_sports()

elif mode=='log_upload':
        do_log_uploader()

elif mode=='log_view':
        TextViewer.text_view('log')

######MAIN TOOL
elif mode=='call_maintool':
        maintool.tool_menu()

elif mode=='clear_cache':
        maintool.clearCache()

elif mode=='debug_onoff':

    if _is_debugging() == True:
        choice = xbmcgui.Dialog().yesno('Indigo', 'Please confirm that you wish to disable log debugging mode immediately')
        if choice == 1:
            xbmc.executebuiltin("ToggleDebug")
            xbmc.executebuiltin("Container.Refresh")
        else: quit()
    else:
        choice = xbmcgui.Dialog().yesno('Indigo', 'Please confirm that you wish to enable log debugging mode immediately')
        if choice == 1:
            xbmc.executebuiltin("ToggleDebug")
            xbmc.executebuiltin("Container.Refresh")
        else: quit()

elif mode=='purgepackages':
        maintool.purge_packages()

elif mode=='wipeaddons':
        maintool.wipe_addons()

elif mode=='disablemain':
        maintool.disable_main()

elif mode=='enablemain':
        maintool.enable_main()

elif mode=='disableblocker':
        maintool.disable_blocker()

elif mode=='enableblocker':
        maintool.enable_blocker()

elif mode== 'autoclean':
    maintool.autocleanask()
    
elif mode== 'clearthumbs':
    maintool.deleteThumbnails()

elif mode== 'crashlogs':
    maintool.DeleteCrashLogs()
    
elif mode== 'autocleanonoff':
    maintool.AUTO_WEEKLY_CLEAN_ON_OFF()
    
elif mode== 'autocleanlaunch':
    maintool.AUTO_CLEAN_ON_OFF()
    
elif mode== 'autocleanmb':
    plugintools.open_settings_dialog()
    
elif mode== 'repohealth':
    maintool.CHECK_BROKEN_REPOS()
    
elif mode== 'sourcehealth':
    maintool.CHECK_BROKEN_SOURCES()
    
elif mode== 'converttospecial':
    maintool.Fix_Special()
    
elif mode== 'reloadskin':
    choice = xbmcgui.Dialog().yesno('Indigo', 'Please confirm that you wish to reload the skin cache immediately.')
    if choice == 1:
        xbmc.executebuiltin("ReloadSkin()")
    else: quit()
    
elif mode== 'updateaddons':
    choice = xbmcgui.Dialog().yesno('Indigo', 'Please confirm that you wish to force update all addons and repositories immediately.')
    if choice == 1:
        xbmc.executebuiltin("UpdateAddonRepos")
        xbmc.executebuiltin("UpdateLocalAddons")    
    else: quit()

elif mode== 'encdecpasswords':

    choice = xbmcgui.Dialog().yesno('Indigo', 'Would you like to hide or unhide your passwords?',yeslabel='Hide',nolabel='Unhide')
    if choice == 1: maintool.HidePasswords()
    else: maintool.UnhidePasswords()

elif mode== 'encdecbase64':
    maintool.BASE64_ENCODE_DECODE()
    
elif mode== 'foceclosekodi':
    maintool.KillKodi()
    
#####KEYMAPS###############

elif mode=='install_keymap':
        installer.install_keymap(name, url)

elif mode=='uninstall_keymap':
        installer.uninstall_keymap()

elif mode=='customkeys':
        installer.keymaps()

###############SPEEDTEST#################
elif mode=="runspeedtest":
        fullspeedtest()

elif mode=="runtest":
        speedtest.runfulltest(url)


elif mode=='call_restore':
        freshstart.startup_freshstart()
##NOTIFICATIONS##############
elif mode=='enable_notify':
        enable_notify()

elif mode=='disable_notify':
        disable_notify()


#######WIZARD#########################


elif mode=="wizardstatus":
        print""+url
        items=configwizard.WIZARDSTATUS(url)
elif mode=='helpwizard':
        configwizard.HELPWIZARD(name,url,description,filetype)

##############Installer############
elif mode=='call_installer':
        installer.MAININDEX()

elif mode=='lib_installer':
        installer.libinstaller(name, url)

elif mode=='EnableRTMP':
    installer.EnableRTMP()

elif mode=='interrepolist':
    items=installer.List_Inter_Addons(url)

elif mode=='interrepos':
    items=installer.INTERNATIONAL_REPOS()

elif mode=='interaddons':
    items=installer.INTERNATIONAL_ADDONS()

elif mode=='interaddonslist':
    items=installer.INTERNATIONAL_ADDONS_LIST(url)

elif mode=='interlist':
    items=installer.INTERNATIONAL_ADDONS()

elif mode=='addonlist':
    items=installer.List_Addons(url)

elif mode=='splitlist':
    installer.Split_List(name,url)

elif mode=='addopensub':
    installer.OPENSUBINSTALL(url)

elif mode=='searchaddon':
    installer.SEARCHADDON(url)

elif mode=='getaddoninfo':
    installer.getaddoninfo(url, description, filetype)

elif mode=='InstallQuas':
    installer.INSTALLQUASAR(url)

elif mode=='addoninstall':
    #kodi.log("TRYING MODES")
    installer.ADDONINSTALL(name, url, description, filetype, repourl)

elif mode=='adultlist':
    items=installer.List_Indigo_Adult(url)


elif mode=='BrowseUrl':
    xbmc.executebuiltin("XBMC.System.Exec(%s)" % url)
###################################


elif mode=='enableall':
    addon_able.setall_enable()

elif mode=='teststuff':
    freshstart.remove_db()
#######################################
elif mode=='backup_restore':
    backup.BACKUPMENU()

elif mode=='full_backup':
    backup.FullBackup()

elif mode=='small_backup':
    backup.Backup()

elif mode=='do_backup_restore':
    backup.Restore()

elif mode=='display_backup_settings':
    kodi.openSettings(addon_id,id1=0,id2=0)

elif mode=='read_zip':
    backup.READ_ZIP(url)

elif mode=='del_backup':
    backup.ListBackDel()

elif mode== 'do_del_backup':
    backup.DeleteBackup(url)



xbmcplugin.endOfDirectory(int(sys.argv[1]))
