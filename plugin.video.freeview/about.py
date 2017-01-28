import xbmc,xbmcaddon,xbmcvfs,xbmcgui
import sys

ADDON = xbmcaddon.Addon(id='plugin.video.freeview')

path = xbmc.translatePath('special://home/addons/plugin.video.freeview/about.txt')

f = xbmcvfs.File(path,"rb")
data = f.read()
dialog = xbmcgui.Dialog()
dialog.textviewer('About This Add-on', data)