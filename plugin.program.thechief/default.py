#

import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,sys
import urllib, urllib2, re, glob
import shutil
import extras
import extract
import addonfix
import addons
import communitybuilds
import CheckPath
import cache
import time
import downloader
import plugintools
import zipfile
import ntpath

ADDON        =  xbmcaddon.Addon(id='plugin.program.thechief')
AddonID      =  'plugin.program.thechief'
AddonTitle   =  "[B]The Chief[/B]"
zip          =  ADDON.getSetting('zip')
localcopy    =  ADDON.getSetting('localcopy')
mastercopy   =  ADDON.getSetting('mastercopy')
dialog       =  xbmcgui.Dialog()
dp           =  xbmcgui.DialogProgress()
HOME         =  xbmc.translatePath('special://home/')
USERDATA     =  xbmc.translatePath(os.path.join('special://home/userdata',''))
MEDIA        =  xbmc.translatePath(os.path.join('special://home/media',''))
AUTOEXEC     =  xbmc.translatePath(os.path.join(USERDATA,'autoexec.py'))
AUTOEXECBAK  =  xbmc.translatePath(os.path.join(USERDATA,'autoexec_bak.py'))
ADDON_DATA   =  xbmc.translatePath(os.path.join(USERDATA,'addon_data'))
PLAYLISTS    =  xbmc.translatePath(os.path.join(USERDATA,'playlists'))
DATABASE     =  xbmc.translatePath(os.path.join(USERDATA,'Database'))
THUMBNAILS   =  xbmc.translatePath(os.path.join(USERDATA,'Thumbnails'))
ADDONS       =  xbmc.translatePath(os.path.join('special://home','addons',''))
CBADDONPATH  =  xbmc.translatePath(os.path.join(ADDONS,AddonID,'default.py'))
FANART       =  xbmc.translatePath(os.path.join(ADDONS,AddonID,'fanart.jpg'))
ICON         =  xbmc.translatePath(os.path.join(ADDONS,AddonID,'icon.png'))
INSTALL      =  xbmc.translatePath(os.path.join(USERDATA,'install.xml'))
FAVS         =  xbmc.translatePath(os.path.join(USERDATA,'favourites.xml'))
SOURCE       =  xbmc.translatePath(os.path.join(USERDATA,'sources.xml'))
ADVANCED     =  xbmc.translatePath(os.path.join(USERDATA,'advancedsettings.xml'))
PROFILES     =  xbmc.translatePath(os.path.join(USERDATA,'profiles.xml'))
KEYMAPS      =  xbmc.translatePath(os.path.join(USERDATA,'keymaps','keyboard.xml'))
USB          =  xbmc.translatePath(os.path.join(zip))
CBPATH       =  xbmc.translatePath(os.path.join(USB,'Chiefs Builds',''))
cookiepath   =  xbmc.translatePath(os.path.join(ADDON_DATA,AddonID,'cookiejar'))
startuppath  =  xbmc.translatePath(os.path.join(ADDON_DATA,AddonID,'startup.xml'))
tempfile     =  xbmc.translatePath(os.path.join(ADDON_DATA,AddonID,'temp.xml'))
idfile       =  xbmc.translatePath(os.path.join(ADDON_DATA,AddonID,'id.xml'))
idfiletemp   =  xbmc.translatePath(os.path.join(ADDON_DATA,AddonID,'idtemp.xml'))
notifyart    =  xbmc.translatePath(os.path.join(ADDONS,AddonID,'resources/'))
skin         =  xbmc.getSkinDir()
userdatafolder = xbmc.translatePath(os.path.join(ADDON_DATA,AddonID))
tempdbpath   =  xbmc.translatePath(os.path.join(USB,'Database'))
urlbase      =  'None'
USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
base='@TheChief_Kodi/'
VERSION = "2.0.1"
PATH = "[B]The Chief[/B]" 
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link  	
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Function to open addon settings
def Addon_Settings():
    ADDON.openSettings(sys.argv[0])
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Main category list
def Categories():
	sign = 0
	maintenance  =  ADDON.getSetting('maintenance')
	mainmenu  =  ADDON.getSetting('mainmenu')
	if mainmenu == 'true':
		extras.addDir('folder','[B]Chiefs Builds[/B]','none', 'buildmenu', 'build_menu.png','','','')
	if maintenance == 'true':
		extras.addDir('folder','[B]Chiefs Maintenance[/B]','none', 'tools', 'Tool.png','','','')
	if maintenance == 'true':	
		extras.addDir('','[B]Update My Add-ons (Force Refresh)[/B]', 'none', 'update', 'Tool.png','','','')
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------		
#Builds Section
def BuildMenu():
    link = OPEN_URL('https://archive.org/download/TheChiefKodi_201512/TheChief.txt').replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description in match:
        addDir(name,url,'wizard',iconimage,fanart,description)
    setView('movies', 'MAIN')
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def WIZARD(name,url,description):
            ret = dialog.yesno('[B]The Chief[/B]', 'For A Successful Update','Ensure You Have Wiped Your Kodi First','Do You Wish To Continue?','Cancel','Continue')
            if ret == 1:
                name = name.replace('[COLOR white]','').replace('[/COLOR]','')
                path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
                dp = xbmcgui.DialogProgress()
                dp.create("[B]Selected Chief Build Is Downloading[/B]","One Of The Chief Builds Is Downloading Be Patient",'', 'Please Wait')
                lib=os.path.join(path, name+'.zip')
                try:
                   os.remove(lib)
                except:
                   pass
                downloader.download(url, lib, dp)
                addonfolder = xbmc.translatePath(os.path.join('special://','home'))
                dp.update(0,"", "[B]Now Applying The Chief Builds Thanks For Waiting[/B]")
                extract.all(lib,addonfolder,dp)
                try:
                   os.remove(lib)
                except:
                   pass
                killxbmc()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Maintenance section
def Tools():
    extras.addDir('folder','[B]Chiefs Tools[/B]', 'none', 'wipetools', 'Addon_Fixes.png','','','')
    extras.addDir('','[B]Force Close Kodi[/B]','url','kill_xbmc','Kill_XBMC.png','','','')
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
#Maintenance section
def Wipe_Tools():
    extras.addDir('','[B]Chiefs Clear Cache[/B]','url','clear_cache','Clear_Cache.png','','','')
    extras.addDir('','[B]Chiefs Clear My Cached Artwork[/B]', 'none', 'remove_textures', 'Delete_Cached_Artwork.png','','','')
    extras.addDir('','[B]Chiefs Delete Addon_Data[/B]','url','remove_addon_data','Delete_Addon_Data.png','','','')
    extras.addDir('','[B]Chiefs Delete Old Crash Logs[/B]','url','remove_crash_logs','Delete_Crash_Logs.png','','','')
    extras.addDir('','[B]Chiefs Delete Packages Folder[/B]','url','remove_packages','Delete_Packages.png','','','')
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Addon removal menu
def Addon_Removal_Menu():
    for file in glob.glob(os.path.join(ADDONS,'*')):
        name=str(file).replace(ADDONS,'[COLOR=white]REMOVE [/COLOR]').replace('plugin.','[COLOR=white](PLUGIN) [/COLOR]').replace('audio.','').replace('video.','').replace('skin.','[COLOR=yellow](SKIN) [/COLOR]').replace('repository.','[COLOR=orange](REPOSITORY) [/COLOR]').replace('script.','[COLOR=cyan](SCRIPT) [/COLOR]').replace('metadata.','[COLOR=gold](METADATA) [/COLOR]').replace('service.','[COLOR=pink](SERVICE) [/COLOR]').replace('weather.','[COLOR=green](WEATHER) [/COLOR]').replace('module.','[COLOR=gold](MODULE) [/COLOR]')
        iconimage=(os.path.join(file,'icon.png'))
        fanart=(os.path.join(file,'fanart.jpg'))
        extras.addDir('',name,file,'remove_addons',iconimage,fanart,'','')
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
#Function to clear all known cache files
def Clear_Cache():
    choice = xbmcgui.Dialog().yesno('Clear All Known Cache?', 'This will clear all known cache files and can help', 'if you\'re encountering kick-outs during playback.','as well as other random issues. There is no harm in using this.', nolabel='Cancel',yeslabel='Delete')
    if choice == 1:
        cache.Wipe_Cache()
        Remove_Textures()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
#Get params and clean up into string or integer
def Get_Params():
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
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Function to clear the addon_data
def Remove_Addon_Data():
    choice = xbmcgui.Dialog().yesno('Delete Addon_Data Folder?', 'This will free up space by deleting your addon_data', 'folder. This contains all addon related settings', 'including username and password info.', nolabel='Cancel',yeslabel='Delete')
    if choice == 1:
        extras.Delete_Userdata()
        dialog.ok("Addon_Data Removed", '', 'Your addon_data folder has now been removed.','')
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Function to clear the packages folder
def Remove_Crash_Logs():
    choice = xbmcgui.Dialog().yesno('Remove All Crash Logs?', 'There is absolutely no harm in doing this, these are', 'log files generated when Kodi crashes and are','only used for debugging purposes.', nolabel='Cancel',yeslabel='Delete')
    if choice == 1:
        extras.Delete_Logs()
        dialog.ok("[B]The Chief[/B]", "Your Crash Log Files Have Now Been Removed", "[COLOR white]Brought To You By @TheChief_Kodi[/COLOR]")
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Function to clear the packages folder
def Remove_Packages():
    choice = xbmcgui.Dialog().yesno('Delete Packages Folder?', 'This will free up space by deleting the zip install', 'files of your addons. The only downside is you\'ll no', 'longer be able to rollback to older versions.', nolabel='Cancel',yeslabel='Delete')
    if choice == 1:
        extras.Delete_Packages()
        dialog.ok("[B]The Chief[/B]", "Your Packages Have Now Been Removed", "[COLOR white]Brought To You By @TheChief_Kodi[/COLOR]")
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Function to clear the packages folder
def Remove_Textures():
    choice = xbmcgui.Dialog().yesno('Clear Cached Images?', 'This will clear your textures13.db file and remove', 'your Thumbnails folder. These will automatically be', 'repopulated after a restart.', nolabel='Cancel',yeslabel='Delete')
    if choice == 1:
        cache.Remove_Textures()
        extras.Destroy_Path(THUMBNAILS)
        choice = xbmcgui.Dialog().yesno('[B]The Chief Quit Kodi Now?[/B]', 'Cache has been successfully deleted.', '[COLOR white]Brought To You By @TheChief_Kodi You must now restart Kodi, would you like to quit now?[/COLOR]','', nolabel='I\'ll restart later',yeslabel='Yes, quit')
        if choice == 1:
            killxbmc()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def Wipe_Kodi():
    mybackuppath = xbmc.translatePath(os.path.join(USB,'Chiefs Builds','My Builds'))
    choice = xbmcgui.Dialog().yesno("ABSOLUTELY CERTAIN?!!!", 'Are you absolutely certain you want to wipe?', '', 'All addons and settings will be completely wiped!', yeslabel='Yes',nolabel='No')
    if choice == 1:
        if skin!= "skin.confluence":
            dialog.ok('[B]The Chief[/B]','Please switch to the default Confluence skin','before performing a wipe.','')
            xbmc.executebuiltin("ActivateWindow(appearancesettings)")
            return
        else:
            choice = xbmcgui.Dialog().yesno("VERY IMPORTANT", 'This will completely wipe your install.', 'Would you like to create a backup before proceeding?', '', yeslabel='No', nolabel='Yes')
            if choice == 0:
                if not os.path.exists(mybackuppath):
                    os.makedirs(mybackuppath)
                vq = extras.Get_Keyboard( heading="Enter a name for this backup" )
                if ( not vq ): return False, 0
                title = urllib.quote_plus(vq)
                backup_zip = xbmc.translatePath(os.path.join(mybackuppath,title+'.zip'))
                exclude_dirs_full =  ['plugin.program.thechief']
                exclude_files_full = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log",'.DS_Store','.setup_complete','XBMCHelper.conf']
                message_header = "Creating full backup of existing build"
                message1 = "Archiving..."
                message2 = ""
                message3 = "Please Wait"
                communitybuilds.Archive_Tree(HOME, backup_zip, message_header, message1, message2, message3, exclude_dirs_full, exclude_files_full)
            choice = xbmcgui.Dialog().yesno("Remove The Chief?", 'Do you also want to remove The Chief', 'add-on and have a complete fresh start or would you', 'prefer to keep this on your system?', yeslabel='Remove',nolabel='Keep')
            if choice == 0:
                cache.Remove_Textures()
                trpath = xbmc.translatePath(os.path.join(ADDONS,AddonID,''))
                trtemp = xbmc.translatePath(os.path.join(HOME,'..','thechief.zip'))
                communitybuilds.Archive_File(trpath, trtemp)
                deppath = xbmc.translatePath(os.path.join(ADDONS,'script.module.addon.common',''))
                deptemp = xbmc.translatePath(os.path.join(HOME,'..','thechief.zip'))
                communitybuilds.Archive_File(deppath, deptemp)
                extras.Destroy_Path(HOME)
                if not os.path.exists(trpath):
                    os.makedirs(trpath)
                if not os.path.exists(deppath):
                    os.makedirs(deppath)
                time.sleep(1)
                communitybuilds.Read_Zip(trtemp)
                dp.create("[B]The Chief[/B]","Checking ",'', 'Please Wait')
                dp.update(0,"", "Extracting Zip Please Wait")
                extract.all(trtemp,trpath,dp)
                communitybuilds.Read_Zip(deptemp)
                extract.all(deptemp,deppath,dp)
                dp.update(0,"", "Extracting Zip Please Wait")
                dp.close()
                time.sleep(1)
                extras.Kill_XBMC()
            elif choice == 1:
                cache.Remove_Textures()
                extras.Destroy_Path(HOME)
                dp.close()
                extras.Kill_XBMC()
            else: return
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------   
def killxbmc():
    choice = xbmcgui.Dialog().yesno('Force Close Kodi', 'You are about to close Kodi', 'Would you like to continue?', nolabel='No, Cancel',yeslabel='Yes, Close')
    if choice == 0:
        return
    elif choice == 1:
        pass
    myplatform = platform()
    print "Platform: " + str(myplatform)
    if myplatform == 'osx': # OSX
        print "############   try osx force close  #################"
        try: os.system('killall -9 XBMC')
        except: pass
        try: os.system('killall -9 Kodi')
        except: pass
        dialog.ok("The Chief", "The Chief configuration", "[COLOR orangered]PLEASE DISCONNECT THE POWER FROM YOUR DEVICE[/COLOR]")
    elif myplatform == 'linux': #Linux
        print "############   try linux force close  #################"
        try: os.system('killall XBMC')
        except: pass
        try: os.system('killall Kodi')
        except: pass
        try: os.system('killall -9 xbmc.bin')
        except: pass
        try: os.system('killall -9 kodi.bin')
        except: pass
        dialog.ok("The Chief", "The Chief configuration", "[COLOR orangered]PLEASE DISCONNECT THE POWER FROM YOUR DEVICE[/COLOR]")
    elif myplatform == 'android': # Android  
        print "############   try android force close  #################"
        try: os.system('adb shell am force-stop org.xbmc.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc.xbmc')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc')
        except: pass        
        dialog.ok("The Chief", "The Chief configuration", "[COLOR orangered]PLEASE DISCONNECT THE POWER FROM YOUR DEVICE[/COLOR]")
    elif myplatform == 'windows': # Windows
        print "############   try windows force close  #################"
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
        dialog.ok("The Chief", "The Chief configuration", "[COLOR orangered]PLEASE DISCONNECT THE POWER FROM YOUR DEVICE[/COLOR]")
    else: #ATV
        print "############   try atv force close  #################"
        try: os.system('killall AppleTV')
        except: pass
        print "############   try raspbmc force close  #################" #OSMC / Raspbmc
        try: os.system('sudo initctl stop kodi')
        except: pass
        try: os.system('sudo initctl stop xbmc')
        except: pass
        dialog.ok("The Chief", "The Chief configuration", "[COLOR orangered]PLEASE DISCONNECT THE POWER FROM YOUR DEVICE[/COLOR]") 
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def addDir(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Addon starts here
params=Get_Params()
addon_id=None
audioaddons=None
author=None
buildname=None
data_path=None
description=None
DOB=None
email=None
fanart=None
forum=None
iconimage=None
link=None
local=None
messages=None
mode=None
name=None
posts=None
programaddons=None
provider_name=None
repo_id=None
repo_link=None
skins=None
sources=None
updated=None
unread=None
url=None
version=None
video=None
videoaddons=None
welcometext=None
zip_link=None

try:    addon_id=urllib.unquote_plus(params["addon_id"])
except: pass
try:    adult=urllib.unquote_plus(params["adult"])
except: pass
try:    audioaddons=urllib.unquote_plus(params["audioaddons"])
except: pass
try:    author=urllib.unquote_plus(params["author"])
except: pass
try:    buildname=urllib.unquote_plus(params["buildname"])
except: pass
try:    data_path=urllib.unquote_plus(params["data_path"])
except: pass
try:    description=urllib.unquote_plus(params["description"])
except: pass
try:    DOB=urllib.unquote_plus(params["DOB"])
except: pass
try:    email=urllib.unquote_plus(params["email"])
except: pass
try:    fanart=urllib.unquote_plus(params["fanart"])
except: pass
try:    forum=urllib.unquote_plus(params["forum"])
except: pass
try:    guisettingslink=urllib.unquote_plus(params["guisettingslink"])
except: pass
try:    iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try:    link=urllib.unquote_plus(params["link"])
except: pass
try:    local=urllib.unquote_plus(params["local"])
except: pass
try:    messages=urllib.unquote_plus(params["messages"])
except: pass
try:    mode=str(params["mode"])
except: pass
try:    name=urllib.unquote_plus(params["name"])
except: pass
try:    pictureaddons=urllib.unquote_plus(params["pictureaddons"])
except: pass
try:    posts=urllib.unquote_plus(params["posts"])
except: pass
try:    programaddons=urllib.unquote_plus(params["programaddons"])
except: pass
try:    provider_name=urllib.unquote_plus(params["provider_name"])
except: pass
try:    repo_link=urllib.unquote_plus(params["repo_link"])
except: pass
try:    repo_id=urllib.unquote_plus(params["repo_id"])
except: pass
try:    skins=urllib.unquote_plus(params["skins"])
except: pass
try:    sources=urllib.unquote_plus(params["sources"])
except: pass
try:    updated=urllib.unquote_plus(params["updated"])
except: pass
try:    unread=urllib.unquote_plus(params["unread"])
except: pass
try:    url=urllib.unquote_plus(params["url"])
except: pass
try:    version=urllib.unquote_plus(params["version"])
except: pass
try:    video=urllib.unquote_plus(params["video"])
except: pass
try:    videoaddons=urllib.unquote_plus(params["videoaddons"])
except: pass
try:    zip_link=urllib.unquote_plus(params["zip_link"])
except: pass

print str(PATH)+': '+str(VERSION)
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)


def setView(content, viewType):
    # set content type so library shows more views and info
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if ADDON.getSetting('auto-view')=='true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )

if mode==None or url==None or len(url)<1:
        Categories()
elif mode == 'addon_removal_menu' : Addon_Removal_Menu()
elif mode == 'addonfix'           : addonfix.fixes()
elif mode == 'addonfixes'         : Addon_Fixes()
elif mode == 'addonmenu'          : Addon_Menu()
elif mode == 'addon_settings'     : Addon_Settings()
elif mode == 'buildmenu'		  : BuildMenu()
elif mode == 'categories'         : Categories()
elif mode == 'clear_cache'        : Clear_Cache()  
elif mode == 'remove_addon_data'  : Remove_Addon_Data()
elif mode == 'remove_addons'      : extras.Remove_Addons(url)
elif mode == 'remove_crash_logs'  : Remove_Crash_Logs()
elif mode == 'remove_packages'    : Remove_Packages()
elif mode == 'remove_textures'    : Remove_Textures()     
elif mode == 'tools'              : Tools()  
elif mode == 'update'             : addons.Update_Repo()
elif mode == 'wipetools'          : Wipe_Tools()
elif mode == 'wipe_xbmc'          : Wipe_Kodi()
elif mode ==  'wizard'            : WIZARD(name,url,description)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
