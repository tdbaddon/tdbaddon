# -*- coding: utf-8 -*-
#code by Vania - Inspired by the plugin PlayList Loader by Avigdor 
import urllib2, urllib, sys, xbmcplugin ,xbmcgui, xbmcaddon, xbmc, os, json, shutil, time, zipfile, re, stat

AddonID = 'plugin.video.kodilivetv'
Addon = xbmcaddon.Addon(AddonID)
localizedString = Addon.getLocalizedString
AddonName = Addon.getAddonInfo("name")
icon = Addon.getAddonInfo('icon')

addonDir = Addon.getAddonInfo('path').decode("utf-8")

LOCAL_VERSION_FILE = os.path.join(os.path.join(addonDir), 'version.xml' )
REMOTE_VERSION_FILE = "http://kodilive.eu/repo/version.xml"

libDir = os.path.join(addonDir, 'resources', 'lib')

XML_FILE  = os.path.join(libDir, 'advancedsettings.xml' )
ACTIVESETTINGSFILE = os.path.join(xbmc.translatePath('special://profile'), 'advancedsettings.xml')
#ACTIVESETTINGSFILE = os.path.join(addonDir, 'advancedsettings.xml')

sys.path.insert(0, libDir)
import common

def checkforupdates(url,loc):
        xbmc.log('Start check for updates')
    	try:
		data = urllib2.urlopen(url).read()
		xbmc.log('read xml remote data:' + data)
	except:
		data = ""
		xbmc.log('fail read xml remote data:' + url )
    	try:
		f = open(loc,'r')
		data2 = f.read().replace("\n\n", "")
		f.close()
		xbmc.log('read xml local data:' + data2)
	except:
		data2 = ""
		xbmc.log('fail read xml local data')

        version_publicada = find_single_match(data,"<version>([^<]+)</version>").strip()
        tag_publicada = find_single_match(data,"<tag>([^<]+)</tag>").strip()

        version_local = find_single_match(data2,"<version>([^<]+)</version>").strip()
        tag_local = find_single_match(data,"<tag>([^<]+)</tag>").strip()

        try:
            numero_version_publicada = int(version_publicada)
            xbmc.log('number remote version:' + version_publicada)
            numero_version_local = int(version_local)
            xbmc.log('number local version:' + version_local)
        except:
            version_publicada = ""
            
            xbmc.log('number local version:' + version_local )
            xbmc.log('Check fail !@*')
        if version_publicada!="" and version_local!="":
            if (numero_version_publicada > numero_version_local):
                AddonID = 'plugin.video.kodilivetv'
                addon       = xbmcaddon.Addon(AddonID)
                addonname   = addon.getAddonInfo('name')
                extpath = os.path.join(xbmc.translatePath("special://home/addons/").decode("utf-8")) 
                addon_data_dir = os.path.join(xbmc.translatePath("special://userdata/addon_data" ).decode("utf-8"), AddonID) 
                dest = addon_data_dir + '/lastupdate.zip'                
                
                UPDATE_URL = 'http://kodilive.eu/repo/plugin.video.kodilivetv-' + tag_publicada + '.zip'
                xbmc.log('START DOWNLOAD UPDATE:' + UPDATE_URL)
                
                DownloaderClass(UPDATE_URL,dest)  

                import ziptools
                unzipper = ziptools.ziptools()
                unzipper.extract(dest,extpath)
                
                line7 = 'New version installed .....'
                line8 = 'Version: ' + tag_publicada 
                
                xbmcgui.Dialog().ok('Kodi Live TV', line7, line8)
                
                if os.remove( dest ): xbmc.log('TEMPORARY ZIP REMOVED') 
            else:
                AddonID = 'plugin.video.kodilivetv'
                addon = xbmcaddon.Addon(AddonID)
                addonname = addon.getAddonInfo('name')
                icon = xbmcaddon.Addon(AddonID).getAddonInfo('icon')
                xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,"Check updates: no update is available", 3200, icon))
                xbmc.log('No updates are available' )
        
        
def find_single_match(data,patron,index=0):
    try:
        matches = re.findall( patron , data , flags=re.DOTALL )
        return matches[index]
    except:
        return ""
    
#url = 'http://vaniarupeni.altervista.org/repo/plugin.video.kodilivetv-1.1.0.zip'
percent = 0
def DownloaderClass(url,dest):
    dp = xbmcgui.DialogProgress()
    dp.create("Kodi Live TV ZIP DOWNLOADER","Downloading File",url)
    urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
 
def _pbhook(numblocks, blocksize, filesize, url=None,dp=None):
    try:
        percent = min((numblocks*blocksize*100)/filesize, 100)
        dp.update(percent)
    except: 
        percent = 100
        dp.update(percent)
        time.sleep(20)
        dp.close()
    if dp.iscanceled(): 
        dp.close()

addon_data_dir = os.path.join(xbmc.translatePath("special://userdata/addon_data" ).decode("utf-8"), AddonID)


if not os.path.exists(addon_data_dir):
	os.makedirs(addon_data_dir)

def clean_cache():

    for i in os.listdir("/" + addon_data_dir):    
        rf = format(i)
        if bool('.txt' in i):
            if not bool('favorites.txt' in i) and not bool('time.txt' in i):
                os.remove( os.path.join( addon_data_dir , i ) )
                xbmc.log('*** Delete file : ' + rf )
        else:
            pass


def write_file(file_name, file_contents):
    fh = None
    try:
        fh = open(file_name, "wb")
        fh.write(file_contents)
        return True
    except:
        return False
    finally:
	if fh is not None:
	    fh.close()

Tfile = os.path.join(addon_data_dir, 'time.txt')

if os.path.isfile(Tfile):
        t = time.time() - os.path.getmtime(Tfile)
        if t > 172800 :
            checkforupdates(REMOTE_VERSION_FILE, LOCAL_VERSION_FILE)
            write_file(Tfile , '*')
            
else: write_file(Tfile  , '*')

	
playlistsFile = os.path.join(addonDir, "playLists.txt")
Italian = os.path.join(addonDir, "italian.txt")
French = os.path.join(addonDir, "french.txt")
German = os.path.join(addonDir, "german.txt")
English = os.path.join(addonDir, "english.txt")
tmpListFile = os.path.join(addon_data_dir, 'tempList.txt')
favoritesFile = os.path.join(addon_data_dir, 'favorites.txt')
if  not (os.path.isfile(favoritesFile)):
	f = open(favoritesFile, 'w') 
	f.write('[]') 
	f.close() 



def write_xml():
        
    if os.path.isfile( ACTIVESETTINGSFILE ):
            if not os.path.isfile( os.path.join(addon_data_dir, 'advancedsettings.xml' ) ):        
                shutil.move( ACTIVESETTINGSFILE , addon_data_dir )
    
    shutil.copyfile( XML_FILE , ACTIVESETTINGSFILE )
    

def restore_xml():
    
    if os.path.isfile( os.path.join(addon_data_dir, 'advancedsettings.xml' ) ): 
        
        if os.path.isfile( ACTIVESETTINGSFILE ) : os.remove( ACTIVESETTINGSFILE )

        shutil.copyfile( os.path.join(addon_data_dir, 'advancedsettings.xml' ) , ACTIVESETTINGSFILE )
        #os.remove( os.path.join(addon_data_dir, 'advancedsettings.xml' ) )
    elif os.path.isfile( ACTIVESETTINGSFILE ) : os.remove( ACTIVESETTINGSFILE ) 

    

def remove_xml():

     if os.path.isfile( ACTIVESETTINGSFILE ) : os.remove( ACTIVESETTINGSFILE )
        

def Categories():
    
	AddDir("[COLOR cyan][B][ {0} ][/B][/COLOR]".format(localizedString(10003).encode('utf-8')), "favorites" ,30 ,os.path.join(addonDir, "resources", "images", "bright_yellow_star.png"))	
	AddDir("[COLOR gold][B]{0}[/B][/COLOR]".format(localizedString(10020).encode('utf-8')), "italian" ,35 ,os.path.join(addonDir, "resources", "images", "it.png"))
	AddDir("[COLOR gold][B]{0}[/B][/COLOR]".format(localizedString(10021).encode('utf-8')), "french" ,36 ,os.path.join(addonDir, "resources", "images", "fr.png"))
	AddDir("[COLOR gold][B]{0}[/B][/COLOR]".format(localizedString(10022).encode('utf-8')), "german" ,37 ,os.path.join(addonDir, "resources", "images", "de.png"))
	AddDir("[COLOR gold][B]{0}[/B][/COLOR]".format(localizedString(10023).encode('utf-8')), "english" ,38 ,os.path.join(addonDir, "resources", "images", "uk.png"))
	list = common.ReadList(playlistsFile)
	for item in list:
		mode = 1 if item["url"].find(".plx") > 0 else 2
		#name = common.GetEncodeString(item["name"])
		#AddDir("[COLOR gold]{0}[/COLOR]".format(name) ,item["url"], mode, "")
		image = item.get('image', '')
		icon = os.path.join(addonDir, "resources", "images", image.encode("utf-8"))
		name = localizedString(item["name"])
		cname = "[COLOR gold][B]{0}[/B][/COLOR]".format(name)
		
		
		if name == localizedString(10070).encode('utf-8') :
                    cname = "[COLOR violet][B]{0}[/B][/COLOR]".format(name)
                elif name == localizedString(10050).encode('utf-8') :
                    cname = "[COLOR pink][B]{0}[/B][/COLOR]".format(name)
		elif name == localizedString(10051).encode('utf-8') :
                    cname = "[COLOR FED9DB93][B]{0}[/B][/COLOR]".format(name)                    
                AddDir(cname ,item["url"], mode , icon)
            
  
def AddNewList():
	listName = GetKeyboardText(localizedString(10004).encode('utf-8')).strip()
	if len(listName) < 1:
		return

	method = GetSourceLocation(localizedString(10002).encode('utf-8'), [localizedString(10016).encode('utf-8'), localizedString(10017).encode('utf-8')])	
	#print method
	if method == -1:
		return
	elif method == 0:
		listUrl = GetKeyboardText(localizedString(10005).encode('utf-8')).strip()
	else:
		listUrl = xbmcgui.Dialog().browse(int(1), localizedString(10006).encode('utf-8'), 'myprograms','.plx|.m3u').decode("utf-8")
		if not listUrl:
			return
	
	if len(listUrl) < 1:
		return

	list = common.ReadList(playlistsFile)
	for item in list:
		if item["url"].lower() == listUrl.lower():
			xbmc.executebuiltin('Notification({0}, "{1}" {2}, 5000, {3})'.format(AddonName, listName, localizedString(10007).encode('utf-8'), icon))
			return
	list.append({"name": listName.decode("utf-8"), "url": listUrl})
	if common.SaveList(playlistsFile, list):
		xbmc.executebuiltin("XBMC.Container.Update('plugin://{0}')".format(AddonID))
	
def RemoveFromLists(url):
	list = common.ReadList(playlistsFile)
	for item in list:
		if item["url"].lower() == url.lower():
			list.remove(item)
			if common.SaveList(playlistsFile, list):
				xbmc.executebuiltin("XBMC.Container.Refresh()")
			break
			
def PlxCategory(url):
	tmpList = []
	list = common.plx2list(url)
	background = list[0]["background"]
	for channel in list[1:]:
		iconimage = "" if not channel.has_key("thumb") else common.GetEncodeString(channel["thumb"])
		name = common.GetEncodeString(channel["name"])
		if channel["type"] == 'playlist':
			AddDir("[COLOR gold]{0}[/COLOR]".format(name) ,channel["url"], 1, iconimage, background=background)
		else:
			AddDir(name, channel["url"], 3, iconimage, isFolder=False, background=background)
			tmpList.append({"url": channel["url"], "image": iconimage, "name": name.decode("utf-8")})
                
                
                common.SaveList(tmpListFile, tmpList)
		
	
	
def m3uCategory(url):	
        tmp = TempFileName (url)
	#tmpList = []
	tcache = 18000
	
	if os.path.isfile(tmp):
            t = time.time() - os.path.getmtime(tmp)
        else :
            t = 0
	
	if os.path.isfile(tmp) and t < tcache :
                list = common.m3u2list(tmp)
        else :       
                list = common.m3u2list(url)
                
	for channel in list:
		name = common.GetEncodeString(channel["display_name"])
		#logo = common.GetEncodeString(channel["params"])
                #logo = logo.replace(' ', '')
                if channel.get("tvg_logo", ""): 
                    logo = channel.get("tvg_logo", "")
                else :
                    logo = "tv.png"
                
                iconname = "http://kodilive.eu/logo/" + logo
                #iconname = "http://kodilive.site88.net/logo/" + logo
                
		AddDir(name ,channel["url"], 3, iconname, isFolder=False)
		#tmpList.append({"url": channel["url"], "image": "", "name": name.decode("utf-8")})
        
        xbmc.log( "*** tmp file time : " + format(t) )
        
        if not os.path.isfile(tmp) or t > tcache :
                content = common.OpenURL(url)
                if len(content) > 10 :
                    write_file(tmp, content) 
                    xbmc.log('Write temp list : ' + tmp + '- size : ' + format( len(content) ) )
      


def TempFileName (url):
    if url.find("regionali") >= 0:
        return os.path.join(addon_data_dir, 'regionali.txt')    
    if url.find("l=it") >= 0:
        return os.path.join(addon_data_dir, 'it.txt')
    if url.find("l=chit") >= 0:
        return os.path.join(addon_data_dir, 'chit.txt') 
    if url.find("radioit2") >= 0:
        return os.path.join(addon_data_dir, 'radioit2.txt')
    if url.find("radiofr") >= 0:
        return os.path.join(addon_data_dir, 'radiofr.txt')    
    if url.find("mediaset") >= 0:
        return os.path.join(addon_data_dir, 'mediaset.txt')
    if url.find("vpnchit") >= 0:
        return os.path.join(addon_data_dir, 'w_it.txt')     
    if url.find("l=fr") >= 0:
        return os.path.join(addon_data_dir, 'fr.txt')
    if url.find("l=chfr") >= 0:
        return os.path.join(addon_data_dir, 'chfr.txt')    
    if url.find("vpnchfr") >= 0:
        return os.path.join(addon_data_dir, 'w_fr.txt')
    if url.find("l=chde") >= 0:
        return os.path.join(addon_data_dir, 'chde.txt')    
    if url.find("l=de") >= 0:
        return os.path.join(addon_data_dir, 'de.txt')
    if url.find("vpnchde") >= 0:
        return os.path.join(addon_data_dir, 'w_de.txt') 
    if url.find("radiode") >= 0:
        return os.path.join(addon_data_dir, 'radiode.txt')
    if url.find("l=chen") >= 0:
        return os.path.join(addon_data_dir, 'chen.txt')    
    if url.find("l=en") >= 0:
        return os.path.join(addon_data_dir, 'en.txt')
    if url.find("vpnchen") >= 0:
        return os.path.join(addon_data_dir, 'w_en.txt')
    if url.find("radioen") >= 0:
        return os.path.join(addon_data_dir, 'radioen.txt')   
    if url.find("bbc_radio") >= 0:
        return os.path.join(addon_data_dir, 'bbc_radio.txt')    
    if url.find("l=tr") >= 0:
        return os.path.join(addon_data_dir, 'tr.txt')       
    if url.find("l=es") >= 0:
        return os.path.join(addon_data_dir, 'es.txt')        
    if url.find("l=pt") >= 0:
        return os.path.join(addon_data_dir, 'pt.txt')        
    if url.find("l=ru") >= 0:
        return os.path.join(addon_data_dir, 'ru.txt')
    if url.find("l=ro") >= 0:
        return os.path.join(addon_data_dir, 'ro.txt')
    if url.find("l=gr") >= 0:
        return os.path.join(addon_data_dir, 'gr.txt')
    if url.find("l=ar") >= 0:
        return os.path.join(addon_data_dir, 'ar.txt')
    if url.find("l=bu") >= 0:
        return os.path.join(addon_data_dir, 'bu.txt')
    if url.find("l=cz") >= 0:
        return os.path.join(addon_data_dir, 'cz.txt')
    if url.find("l=pl") >= 0:
        return os.path.join(addon_data_dir, 'pl.txt')   
    if url.find("l=mu") >= 0:
        return os.path.join(addon_data_dir, 'mu.txt')    
    
    
def PlayUrl(name, url, iconimage=None):
	print '--- Playing "{0}". {1}'.format(name, url)
	listitem = xbmcgui.ListItem(path=url, thumbnailImage=iconimage)
	listitem.setInfo(type="Video", infoLabels={ "Title": name })
	#xbmc.executebuiltin( "PlayerControl(repeat)" )
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
		

def AddDir(name, url, mode, iconimage, description="", isFolder=True, background=None):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)

	liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": description})
	liz.setArt({'fanart': Addon.getAddonInfo('fanart')})
	
	if background:
		liz.setProperty('fanart_image', background)
	#if mode == 1 or mode == 2:
		#liz.addContextMenuItems(items = [('{0}'.format(localizedString(10008).encode('utf-8')), 'XBMC.RunPlugin({0}?url={1}&mode=22)'.format(sys.argv[0], urllib.quote_plus(url)))])
	if mode == 3:
		liz.setProperty('IsPlayable', 'true')
		liz.addContextMenuItems(items = [('{0}'.format(localizedString(10009).encode('utf-8')), 'XBMC.RunPlugin({0}?url={1}&mode=31&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), iconimage, name))])
	elif mode == 32:
		liz.setProperty('IsPlayable', 'true')
		liz.addContextMenuItems(items = [('{0}'.format(localizedString(10010).encode('utf-8')), 'XBMC.RunPlugin({0}?url={1}&mode=33&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), iconimage, name))])
		
	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=isFolder)
	

def GetKeyboardText(title = "", defaultText = ""):
	keyboard = xbmc.Keyboard(defaultText, title)
	keyboard.doModal()
	text =  "" if not keyboard.isConfirmed() else keyboard.getText()
	return text

def GetSourceLocation(title, list):
	dialog = xbmcgui.Dialog()
	answer = dialog.select(title, list)
	return answer
	
def AddFavorites(url, iconimage, name):
	favList = common.ReadList(favoritesFile)
	for item in favList:
		if item["url"].lower() == url.lower():
			xbmc.executebuiltin("Notification({0}, '{1}' {2}, 5000, {3})".format(AddonName, name, localizedString(10011).encode('utf-8'), icon))
			return
    
	list = common.ReadList(tmpListFile)	
	for channel in list:
		if channel["name"].lower() == name.lower():
			url = channel["url"]
			iconimage = channel["image"]
			break
			
	if not iconimage:
		iconimage = ""
		
	data = {"url": url, "image": iconimage, "name": name.decode("utf-8")}
	
	favList.append(data)
	common.SaveList(favoritesFile, favList)
	xbmc.executebuiltin("Notification({0}, '{1}' {2}, 5000, {3})".format(AddonName, name, localizedString(10012).encode('utf-8'), icon))
	
	
def ListFavorites():
	AddDir("[COLOR yellow][B]{0}[/B][/COLOR]".format(localizedString(10013).encode('utf-8')), "favorites" ,34 ,os.path.join(addonDir, "resources", "images", "bright_yellow_star.png"), isFolder=False)
	list = common.ReadList(favoritesFile)
	for channel in list:
		name = channel["name"].encode("utf-8")
		iconimage = channel["image"].encode("utf-8")
		AddDir(name, channel["url"], 32, iconimage, isFolder=False) 

def ListSub(lng):
	list = common.ReadList(lng)
	for item in list:
		mode =  2
		image = item.get('image', '')
		icon = os.path.join(addonDir, "resources", "images", image.encode("utf-8"))
		name = localizedString(item["name"])
		cname = "[COLOR gold][B]{0}[/B][/COLOR]".format(name)
                AddDir(cname ,item["url"], mode , icon, "")



def RemoveFavorties(url):
	list = common.ReadList(favoritesFile) 
	for channel in list:
		if channel["url"].lower() == url.lower():
			list.remove(channel)
			break
			
	common.SaveList(favoritesFile, list)
	xbmc.executebuiltin("XBMC.Container.Refresh()")
	

def AddNewFavortie():
	chName = GetKeyboardText("{0}".format(localizedString(10014).encode('utf-8'))).strip()
	if len(chName) < 1:
		return
	chUrl = GetKeyboardText("{0}".format(localizedString(10015).encode('utf-8'))).strip()
	if len(chUrl) < 1:
		return
		
	favList = common.ReadList(favoritesFile)
	for item in favList:
		if item["url"].lower() == url.lower():
			xbmc.executebuiltin("Notification({0}, '{1}' {2}, 5000, {3})".format(AddonName, chName, localizedString(10011).encode('utf-8'), icon))
			return
			
	data = {"url": chUrl, "image": "", "name": chName.decode("utf-8")}
	
	favList.append(data)
	if common.SaveList(favoritesFile, favList):
		xbmc.executebuiltin("XBMC.Container.Update('plugin://{0}?mode=30&url=favorites')".format(AddonID))

def get_params():
	param = []
	paramstring = sys.argv[2]
	if len(paramstring) >= 2:
		params = sys.argv[2]
		cleanedparams = params.replace('?','')
		if (params[len(params)-1] == '/'):
			params = params[0:len(params)-2]
		pairsofparams = cleanedparams.split('&')
		param = {}
		for i in range(len(pairsofparams)):
			splitparams = {}
			splitparams = pairsofparams[i].split('=')
			if (len(splitparams)) == 2:
				param[splitparams[0].lower()] = splitparams[1]
	return param

	
params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None

try:
	url = urllib.unquote_plus(params["url"])
except:
	pass
try:
	name = urllib.unquote_plus(params["name"])
except:
	pass
try:
	iconimage = urllib.unquote_plus(params["iconimage"])
except:
	pass
try:        
	mode = int(params["mode"])
except:
	pass
try:        
	description = urllib.unquote_plus(params["description"])
except:
	pass

	
if mode == None or url == None or len(url) < 1:
	Categories()
elif mode == 1:
	PlxCategory(url)
elif mode == 2:
	m3uCategory(url)
elif mode == 3 or mode == 32:
	PlayUrl(name, url, iconimage)
elif mode == 20:
	AddNewList()
elif mode == 22:
	RemoveFromLists(url)
elif mode == 30:
	ListFavorites()
elif mode == 31: 
	AddFavorites(url, iconimage, name) 
elif mode == 33:
	RemoveFavorties(url)
elif mode == 34:
	AddNewFavortie()
elif mode == 35:
	ListSub(Italian)
elif mode == 36:
	ListSub(French)
elif mode == 37:
	ListSub(German)
elif mode == 38:
	ListSub(English)	
elif mode == 40:
	common.DelFile(playlistsFile)
	sys.exit()
elif mode == 41:
	common.DelFile(favoritesFile)
	sys.exit()
elif mode == 42:
        write_xml()
        sys.exit()
elif mode == 43:
        restore_xml()
        sys.exit()   
elif mode == 44:
        remove_xml()
        sys.exit()
elif mode == 45:        
        clean_cache()
        sys.exit()
elif mode == 46:       
        checkforupdates(REMOTE_VERSION_FILE, LOCAL_VERSION_FILE)
        write_file(Tfile , '*')        
        sys.exit()
elif mode == 47:
        xbmc.executebuiltin("StopPVRManager")
        xbmc.executebuiltin("StartPVRManager") 
        sys.exit()
    
xbmcplugin.endOfDirectory(int(sys.argv[1]))
