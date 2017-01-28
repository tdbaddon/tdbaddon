#

import urllib, urllib2, re, xbmcplugin, xbmcgui, xbmc, xbmcaddon, os, sys, time, xbmcvfs
import extract
import extras
import shutil
import subprocess
import datetime
import extract
import downloader
import popularpacks
from addon.common.addon import Addon

ADDON_ID   = 'plugin.program.thechief'
BASEURL    = 'http://addons.totalxbmc.com/'
ADDON      =  xbmcaddon.Addon(id=ADDON_ID)
HOME       =  ADDON.getAddonInfo('path')
dialog     =  xbmcgui.Dialog()
dp         =  xbmcgui.DialogProgress()
USERDATA   =  xbmc.translatePath(os.path.join('special://home/userdata',''))
ADDON_DATA =  xbmc.translatePath(os.path.join(USERDATA,'addon_data'))
ADDONS     =  xbmc.translatePath(os.path.join('special://home','addons'))
ytlink     = 'http://gdata.youtube.com/feeds/api/users/"+YT_ID+"/playlists?start-index=1&max-results=25'
addonfolder      = xbmc.translatePath(os.path.join('special://','home/addons'))
packages         = xbmc.translatePath(os.path.join('special://home/addons','packages'))
username     =  ADDON.getSetting('username')
password     =  ADDON.getSetting('password')


def Update_Repo():
    xbmc.executebuiltin( 'UpdateLocalAddons' )
    xbmc.executebuiltin( 'UpdateAddonRepos' )    
    xbmcgui.Dialog().ok('Force Refresh Started Successfully', 'Depending on the speed of your device & your internet  it could take a few minutes for the updates to install.','','')
    return
#-----------------------------------------------------------------------------------------------------------------