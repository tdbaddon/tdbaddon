#

import urllib, urllib2, re, xbmcplugin, xbmcgui, xbmc, xbmcaddon, os, sys, time, xbmcvfs
import glob
import extract
import shutil
import subprocess
import datetime
import extras
import downloader
import popularpacks
import addonfix
import speedtest
import addons
import communitybuilds
import zipfile
import ntpath
import news
from addon.common.addon import Addon
from addon.common.net import Net

AddonID    = 'plugin.program.thechief'
BASEURL    = 'http://shadowcrew.info'
ADDON      =  xbmcaddon.Addon(id=AddonID)
HOME       =  xbmc.translatePath('special://home/')
ARTPATH    =  'http://shadowcrew.info/twins/Communtiy_Builds/art/' + os.sep
zip        =  ADDON.getSetting('zip')
dialog     =  xbmcgui.Dialog()
dp         =  xbmcgui.DialogProgress()
USERDATA   =  xbmc.translatePath(os.path.join('special://home/userdata',''))
ADDON_DATA =  xbmc.translatePath(os.path.join(USERDATA,'addon_data'))
ADDONS     =  xbmc.translatePath(os.path.join('special://home','addons'))
USB        =  xbmc.translatePath(os.path.join(zip))
log_path   =  xbmc.translatePath('special://logpath/')
skin       =  xbmc.getSkinDir()
net        =  Net()
notifyart  =  xbmc.translatePath(os.path.join(ADDONS,AddonID,'resources/'))
EXCLUDES     =  ['plugin.program.thechief','script.module.addon.common','addon.common.addon']
FANART       =  xbmc.translatePath(os.path.join(ADDONS,AddonID,'fanart.jpg'))
reseller     =  ADDON.getSetting('reseller')
resellername =  ADDON.getSetting('resellername')
resellerid   =  ADDON.getSetting('resellerid')
#-----------------------------------------------------------------------------------------------------------------    
#Popup class - thanks to whoever codes the help popup in TVAddons Maintenance for this section. Unfortunately there doesn't appear to be any author details in that code so unable to credit by name.
class SPLASH(xbmcgui.WindowXMLDialog):
    def __init__(self,*args,**kwargs): self.shut=kwargs['close_time']; xbmc.executebuiltin("Skin.Reset(AnimeWindowXMLDialogClose)"); xbmc.executebuiltin("Skin.SetBool(AnimeWindowXMLDialogClose)")
    def onFocus(self,controlID): pass
    def onClick(self,controlID): 
        if controlID==12: xbmc.Player().stop(); self._close_dialog()
    def onAction(self,action):
        if action in [5,6,7,9,10,92,117] or action.getButtonCode() in [275,257,261]: xbmc.Player().stop(); self._close_dialog()
    def _close_dialog(self):
        xbmc.executebuiltin("Skin.Reset(AnimeWindowXMLDialogClose)"); time.sleep( .4 ); self.close()
#-----------------------------------------------------------------------------------------------------------------    
#Add a standard directory and grab fanart and iconimage from artpath defined in global variables
def addDir(type,name,url,mode,iconimage = '',fanart = '',video = '',description = ''):
    if type != 'folder2' and type != 'addon':
        if len(iconimage) > 0:
            iconimage = ARTPATH + iconimage
        else:
            iconimage = 'DefaultFolder.png'
    if type == 'addon':
        if len(iconimage) > 0:
            iconimage = iconimage
        else:
            iconimage = 'http://totalxbmc.tv/addons/cache/images/4c79319887e240789ca125f144d989_addon-dummy.png'
    if fanart == '':
        fanart = FANART
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)+"&video="+urllib.quote_plus(video)+"&description="+urllib.quote_plus(description)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
    liz.setProperty( "Fanart_Image", fanart )
    liz.setProperty( "Build.Video", video )
    if (type=='folder') or (type=='folder2') or (type=='tutorial_folder') or (type=='news_folder'):
        ok=Add_Directory_Item(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    else:
        ok=Add_Directory_Item(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    return ok
#---------------------------------------------------------------------------------------------------
def Add_Directory_Item(handle, url, listitem, isFolder):
    xbmcplugin.addDirectoryItem(handle, url, listitem, isFolder) 
#----------------------------------------------------------------------------------------------------------------- 
def Add_Install_Dir(title,name,url,mode,iconimage = '',fanart = '',video = '',description = '',zip_link = '',repo_link = '',repo_id = '',addon_id = '',provider_name = '',forum = '',data_path = ''):
    if len(iconimage) > 0:
        iconimage = ARTPATH + iconimage
    else:
        iconimage = 'DefaultFolder.png'
    if fanart == '':
        fanart = FANART
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&zip_link="+urllib.quote_plus(zip_link)+"&repo_link="+urllib.quote_plus(repo_link)+"&data_path="+urllib.quote_plus(data_path)+"&provider_name="+str(provider_name)+"&forum="+str(forum)+"&repo_id="+str(repo_id)+"&addon_id="+str(addon_id)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)+"&video="+urllib.quote_plus(video)+"&description="+urllib.quote_plus(description)
    ok=True
    liz=xbmcgui.ListItem(title, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
    liz.setProperty( "Fanart_Image", fanart )
    liz.setProperty( "Build.Video", video )
    Add_Directory_Item(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
#-----------------------------------------------------------------------------------------------------------------  
#Function to delete crash logs
def Delete_Logs():  
    for infile in glob.glob(os.path.join(log_path, 'xbmc_crashlog*.*')):
         File=infile
         print infile
         os.remove(infile)
         dialog = xbmcgui.Dialog()
         dialog.ok("Crash Logs Deleted", "Your old crash logs have now been deleted.")
#-----------------------------------------------------------------------------------------------------------------    
#Function to delete the packages folder
def Delete_Packages():
    print '############################################################       DELETING PACKAGES             ###############################################################'
    packages_cache_path = xbmc.translatePath(os.path.join('special://home/addons/packages', ''))
    for root, dirs, files in os.walk(packages_cache_path):
        file_count = 0
        file_count += len(files)
    # Count files and give option to delete
        if file_count > 0:
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
#---------------------------------------------------------------------------------------------------
#Function to delete the userdata/addon_data folder
def Delete_Userdata():
    print '############################################################       DELETING USERDATA             ###############################################################'
    addon_data_path = xbmc.translatePath(os.path.join('special://home/userdata/addon_data', ''))
    for root, dirs, files in os.walk(addon_data_path):
        file_count = 0
        file_count += len(files)
    # Count files and give option to delete
        if file_count >= 0:
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))        
#-----------------------------------------------------------------------------------------------------------------  
#Function to do a full wipe.
def Destroy_Path(path):
    dp.create("[B]The Chief[/B] ","Wiping...",'', 'Please Wait')
    shutil.rmtree(path, ignore_errors=True)
#---------------------------------------------------------------------------------------------------
def Get_Keyboard( default="", heading="", hidden=False ):
    """ shows a keyboard and returns a value """
    keyboard = xbmc.Keyboard( default, heading, hidden )
    keyboard.doModal()
    if ( keyboard.isConfirmed() ):
        return unicode( keyboard.getText(), "utf-8" )
    return default
#-----------------------------------------------------------------------------------------------------------------  
def Get_Params():    
    if len(sys.argv[2]) < 2:
        return []

    param = []

    params        = sys.argv[2]
    cleanedparams = params.replace('?','')

    if (params[len(params)-1] == '/'):
        params = params[0:len(params)-2]

    pairsofparams = cleanedparams.split('&')
    param         = {}

    for i in range(len(pairsofparams)):
        splitparams = {}
        splitparams = pairsofparams[i].split('=')

        if (len(splitparams)) == 2:
            param[splitparams[0]] = splitparams[1]

    return param
#-----------------------------------------------------------------------------------------------------------------        
#Fix the blank on-screen keyboard when using Gotham skins on Helix.
#BIG THANKS TO MIKEY1234 FOR THIS SECTION OF CODE, IT HAS BEEN TAKEN FROM THE XUNITY MAINTENANCE ADDON.

def Helix():
    skin = xbmc.getSkinDir()
    path = xbmc.translatePath(os.path.join(ADDONS, skin))
    for root, dirs, files in os.walk(path):
       for f in files:
            if 'DialogKeyboard.xml' in f:
                skin= os.path.join(root, f)
                a=open(skin).read()
                CHANGE=a.replace('<control type="label" id="310"','<control type="edit" id="312"')
                f = open(skin, mode='w')
                f.write(CHANGE)
                f.close()     
                changekeys(skin)
                for i in range(48, 58):
                    changenumber(i,skin)
    dialog = xbmcgui.Dialog()
    dialog.ok("Skin Changes Successful", 'A BIG thank you to Mikey1234 for this fix. The', 'code used for this function was ported from the','Xunity Maintenance add-on')
    xbmc.executebuiltin('ReloadSkin()')   

def changenumber(u,skin):
    print skin
    left='<onleft>%s</onleft>'
    right='<onright>%s</onright>'
    up='<onup>%s</onup>'
    down='<ondown>%s</ondown>'
    button='<control type="button" id="%s">'
    if u < 49:
        NEW=u+ 61
    else:    
        NEW=u+ 51
    a=open(skin).read()
    CHANGE=a.replace(left%u,left%NEW).replace(right%u,right%NEW).replace(up%u,up%NEW).replace(down%u,down%NEW).replace(button%u,button%NEW)
    f = open(skin, mode='w')
    f.write(CHANGE)
    f.close()

def changekeys(skin):
    left='<onleft>%s</onleft>'
    right='<onright>%s</onright>'
    up='<onup>%s</onup>'
    down='<ondown>%s</ondown>'
    button='<control type="button" id="%s">'    
    LETTER=[('65','140'),('66','164'),('67','162'),('68','142'),('69','122'),('70','143'),('71','144'),('72','145'),('73','127'),('74','146'),('75','147'),('76','148'),('77','166'),('78','165'),('79','128'),('80','129'),('81','120'),('82','123'),('83','141'),('84','124'),('85','126'),('86','163'),('87','121'),('88','161'),('89','125'),('90','160')]
    for old , new in LETTER:
        a=open(skin).read()  
        CHANGE=a.replace(button%old,button%new).replace(left%old,left%new).replace(right%old,right%new).replace(up%old,up%new).replace(down%old,down%new)
        f = open(skin, mode='w')
        f.write(CHANGE)
        f.close()   
#-----------------------------------------------------------------------------------------------------------------
#Hide passwords in addon settings - THANKS TO MIKEY1234 FOR THIS CODE (taken from Xunity Maintenance)
def Hide_Passwords():
    dialog = xbmcgui.Dialog()
    if dialog.yesno("Hide Passwords", "This will hide all your passwords in your", "add-on settings, are you sure you wish to continue?"):
        for root, dirs, files in os.walk(ADDONS):
            for f in files:
                if f =='settings.xml':
                    FILE=open(os.path.join(root, f)).read()
                    match=re.compile('<setting id=(.+?)>').findall (FILE)
                    for LINE in match:
                        if 'pass' in LINE:
                            if not 'option="hidden"' in LINE:
                                try:
                                    CHANGEME=LINE.replace('/',' option="hidden"/') 
                                    f = open(os.path.join(root, f), mode='w')
                                    f.write(str(FILE).replace(LINE,CHANGEME))
                                    f.close()
                                except:
                                    pass
        dialog.ok("Passwords Hidden", "Your passwords will now show as stars (hidden), if you","want to undo this please use the option to unhide passwords.") 
#---------------------------------------------------------------------------------------------------
#Kill Commands - these will make sure guisettings.xml sticks.
#ANDROID ONLY WORKS WITH ROOT
def Kill_XBMC():
    dialog.ok('[B]The Chief[/B]','The system will now attempt to force close Kodi.','You may encounter a freeze, if that happens give it a minute','and if it doesn\'t close please restart your system.')
    if xbmc.getCondVisibility('system.platform.osx'):
        print "############   try osx force close  #################"
        try: os.system('killall -9 XBMC')
        except: pass
        try: os.system('killall -9 Kodi')
        except: pass
    elif xbmc.getCondVisibility('system.platform.linux'):
        print "############   try linux force close  #################"
        try: os.system('killall XBMC')
        except: pass
        try: os.system('killall Kodi')
        except: pass
        try: os.system('killall -9 xbmc.bin')
        except: pass
        try: os.system('killall -9 kodi.bin')
        except: pass
    elif xbmc.getCondVisibility('system.platform.android'):
        print "############   try android force close  #################"
        try: os.system('adb shell am force-stop org.xbmc.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc.xbmc')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc')
        except: pass        
    elif xbmc.getCondVisibility('system.platform.windows'):
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
    else: #ATV
        print "############   try atv force close  #################"
        try: os.system('killall AppleTV')
        except: pass
        print "############   try raspbmc force close  #################" #OSMC / Raspbmc
        try: os.system('sudo initctl stop kodi')
        except: pass
        try: os.system('sudo initctl stop xbmc')
        except: pass
    dialog.ok("WARNING  !!!", "If you\'re seeing this message it means the force close", "was unsuccessful. Please close Kodi via your operating system.",'')
#---------------------------------------------------------------------------------------------------
#Simple shortcut to create a notification
def Notify(title,message,times,icon):
    icon = notifyart+icon
    xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")
#---------------------------------------------------------------------------------------------------
#Function to create a text box
def Open_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link     = response.read()
    response.close()
    return link.replace('\r','').replace('\n','').replace('\t','')
#---------------------------------------------------------------------------------------------------
def Remove_Addons(url):
    data_path = str(url).replace(ADDONS,ADDON_DATA)
    if dialog.yesno("Remove", '', "Do you want to Remove"):
        for root, dirs, files in os.walk(url):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
        os.rmdir(url)
        try:
            for root, dirs, files in os.walk(data_path):
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
            os.rmdir(data_path)
        except: pass
        xbmc.executebuiltin('Container.Refresh')         
#---------------------------------------------------------------------------------------------------
def Text_Boxes(heading,anounce):
  class TextBox():
    WINDOW=10147
    CONTROL_LABEL=1
    CONTROL_TEXTBOX=5
    def __init__(self,*args,**kwargs):
      xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW, )) # activate the text viewer window
      self.win=xbmcgui.Window(self.WINDOW) # get window
      xbmc.sleep(500) # give window time to initialize
      self.setControls()
    def setControls(self):
      self.win.getControl(self.CONTROL_LABEL).setLabel(heading) # set heading
      try: f=open(anounce); text=f.read()
      except: text=anounce
      self.win.getControl(self.CONTROL_TEXTBOX).setText(str(text))
      return
  TextBox()  
#-----------------------------------------------------------------------------------------------------------------
#Unhide passwords in addon settings - THANKS TO MIKEY1234 FOR THIS CODE (taken from Xunity Maintenance)
def Unhide_Passwords():
    dialog = xbmcgui.Dialog()
    if dialog.yesno("Make Add-on Passwords Visible?", "This will make all your add-on passwords visible.", "Are you sure you wish to continue?"):
        for root, dirs, files in os.walk(ADDONS):
            for f in files:
                if f =='settings.xml':
                    FILE=open(os.path.join(root, f)).read()
                    match=re.compile('<setting id=(.+?)>').findall (FILE)
                    for LINE in match:
                        if 'pass' in LINE:
                            if  'option="hidden"' in LINE:
                                try:
                                    CHANGEME=LINE.replace(' option="hidden"', '') 
                                    f = open(os.path.join(root, f), mode='w')
                                    f.write(str(FILE).replace(LINE,CHANGEME))
                                    f.close()
                                except:
                                    pass
        dialog.ok("Passwords Are now visible", "Your passwords will now be visible in your add-on settings.","If you want to undo this please use the option to","hide passwords.") 
#---------------------------------------------------------------------------------------------------
#Report back with the version of Kodi installed
def XBMC_Version(url):
    xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
    version=float(xbmc_version[:4])
    if version < 14:
        kodiorxbmc = 'You are running XBMC'
    else:
        kodiorxbmc = 'You are running Kodi'
    dialog=xbmcgui.Dialog()
    dialog.ok(kodiorxbmc, "Your version is: %s" % version)
#---------------------------------------------------------------------------------------------------

params=Get_Params()
url=None
name=None
mode=None
iconimage=None
description=None
author=None
fanart=None
zip_link=None
repo_id=None
repo_link=None

try:    mode = urllib.unquote_plus(params['mode'])
except: mode = None

try:    url = urllib.unquote_plus(params['url'])
except: url = ''

try:    name = urllib.unquote_plus(params['name'])
except: name = ''

try:    type = urllib.unquote_plus(params['filetype'])
except: type = ''

try:    repo = urllib.unquote_plus(params['repourl'])
except: repo = ''

try:    author = urllib.unquote_plus(params['author'])
except: author = 'anonymous'

try:    iconimage=urllib.unquote_plus(params["iconimage"])
except: pass

try:    description=urllib.unquote_plus(params["description"])
except: pass

try:    fanart=urllib.unquote_plus(params["fanart"])
except: pass

try:    special=urllib.unquote_plus(params["special"])
except: pass

try:    repo_link=urllib.unquote_plus(params["repo_link"])
except: repo_link=''

try:    repo_id=urllib.unquote_plus(params["repo_id"])
except: repo_id=''

try:    zip_link=urllib.unquote_plus(params["zip_link"])
except: zip_link=''

if mode=='kill_xbmc' : Kill_XBMC()
