from urllib2 import Request, urlopen
import urllib2,urllib,re,os, shutil
import sys
import time,datetime
import xbmcplugin,xbmcgui,xbmc, xbmcaddon, downloader, extract, time
from libs import kodi
from libs import viewsetter

addon_id=kodi.addon_id
addon = (addon_id, sys.argv)
artwork = xbmc.translatePath(os.path.join('special://home','addons',addon_id,'art/'))
fanart = artwork+'fanart.jpg'
messages = xbmc.translatePath(os.path.join('special://home','addons',addon_id,'resources','messages/'))
execute = xbmc.executebuiltin
AddonTitle = 'Indigo'


########PATHS###############################################
addonPath=xbmcaddon.Addon(id=addon_id).getAddonInfo('path')
addonPath=xbmc.translatePath(addonPath)
xbmcPath=os.path.join(addonPath,"..","..")
KodiPath=os.path.abspath(xbmcPath)
############################################################

def tool_menu():

	kodi.addItem("Clear Cache",'','clearcache',artwork+'clear_cache.png',description="Clear your device cache!")
	kodi.addItem("Purge Packages",'','purgepackages',artwork+'purge_packages.png',description="Erase old addon update files!")
	kodi.addItem("Wipe Addons",'','wipeaddons',artwork+'wipe_addons.png',description="Erase all your Kodi addons in one shot!")
	kodi.addDir("Install Custom Keymaps",'','customkeys',artwork+'custom_keymaps.png',description="Get the best experience out of your device-specific remote control!")
	if kodi.get_setting ('automain') == 'true':
		kodi.addItem("Disable Auto Maintenance ",'','disablemain',artwork+'disable_AM.png',description="Disable the periodic automated erasing of cache and packages!")
	if kodi.get_setting ('automain') == 'false':
		kodi.addItem("Enable Auto Maintenance ",'','enablemain',artwork+'enable_AM.png',description="Enable the periodic automated erasing of cache and packages!")
	if kodi.get_setting ('scriptblock') == 'true':
		kodi.addItem("Disable Malicious Scripts Blocker",'','disableblocker',artwork+'disable_MSB.png',description="Disable protection against malicious scripts!")
	if kodi.get_setting ('scriptblock') == 'false':
		kodi.addItem("Enable Malicious Scripts Blocker",'','enableblocker',artwork+'enable_MSB.png',description="Enable protection against malicious scripts!")

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