import sys
import os
import json
import urllib
import urllib2
import urlparse
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import load_channels
import hashlib
import re
import time
import server
import config
import base64
import shutil


params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))

addon = xbmcaddon.Addon()
addonname = xbmcaddon.Addon()
addondir = xbmc.translatePath( addon.getAddonInfo('profile') ) 
base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
go = True 



xbmcplugin.setContent(addon_handle, 'movies')
addon_id = 'plugin.video.dnatv'
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
usrdata = xbmc.translatePath('special://home/userdata/addon_data/plugin.video.dnatv/')


def Main():
	addDir('[COLOR darkorange]          *** TEAM DNA PRESENTS DNA TV ***[/COLOR]','',0,icon, fanart)
	addDir('[COLOR darkorange]ENTER DNA TV GUIDE[/COLOR]','0',1001,icon, fanart)
	addDir('[COLOR darkblue][I]###--Maintenance Tools--###[/I][/COLOR]','',0,icon, fanart)
	addDir('[COLOR blue]Clear DNA TV Cache[/COLOR]','0',1002,icon, fanart)
	addDir('[COLOR blue]Clear Kodi Cache[/COLOR]','0',1003,icon, fanart)
	addDir('[COLOR darkred][I]###--Click Below For DNA TV Channel Categories--###[/I][/COLOR]','',0,icon, fanart)
	xbmc.executebuiltin('Container.SetViewMode(50)')
	

def dnatvguide():
	xbmc.executebuiltin("RunAddon(script.dnatvguide)")
	
	
def CacheDel():
	if not os.path.exists(usrdata):
		dialog.ok(addonname, 'There is no userdata present for DNA TV')
		addDir('[COLOR yellow]*** DNA TV Cache Cleared ***[/COLOR]','0',0,icon,'',fanart)
		xbmc.executebuiltin('Container.SetViewMode(50)')
		
	if os.path.exists(usrdata):
		shutil.rmtree(usrdata)
		addDir('[COLOR yellow]*** DNA TV Cache Cleared ***[/COLOR]','0',0,icon,'',fanart)
		xbmc.executebuiltin('Container.SetViewMode(50)')


def DeleteCache(url):
    print '###DELETING KODI CACHE###'
    xbmc_cache_path = os.path.join(xbmc.translatePath('special://home'), 'cache')
    if os.path.exists(xbmc_cache_path)==True:    
        for root, dirs, files in os.walk(xbmc_cache_path):
            file_count = 0
            file_count += len(files)
        
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete KODI Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
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
    
	addDir('[COLOR yellow]*** KODI Cache Cleared ***[/COLOR]','0',0,icon,'',fanart)
	xbmc.executebuiltin('Container.SetViewMode(50)')
	
		
def addLink(name,url,mode,iconimage,fanart,description=''):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
		liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
		liz.setProperty('fanart_image', fanart)
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
		
def addDir(name,url,mode,iconimage,fanart,description=''):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
		liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
		liz.setProperty('fanart_image', fanart)
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)



def get_params():
		param=[]
		paramstring=sys.argv[2]
		if len(paramstring)>=2:
				e4=sys.argv[2]
				cleanedparams=e4.replace('?','')
				if (e4[len(e4)-1]=='/'):
						e4=e4[0:len(e4)-2]
				pairsofparams=cleanedparams.split('&')
				param={}
				for i in range(len(pairsofparams)):
						splitparams={}
						splitparams=pairsofparams[i].split('=')
						if (len(splitparams))==2:
								param[splitparams[0]]=splitparams[1]	
		return param
		   
e4=get_params()
url=None
name=None
mode=None
iconimage=None
description=None

try:url=urllib.unquote_plus(e4["url"])
except:pass
try:name=urllib.unquote_plus(e4["name"])
except:pass
try:mode=int(e4["mode"])
except:pass
try:iconimage=urllib.unquote_plus(e4["iconimage"])
except:pass		
	
		
if mode==None or url==None or len(url)<1:Main()
elif mode==1001:dnatvguide()
elif mode==1002:CacheDel()
elif mode==1003:DeleteCache(url)
		
		
		
def addPortal(portal):

	if portal['url'] == '':
		return

	url = build_url({
		'mode': 'genres', 
		'portal' : json.dumps(portal)
		}) 
		
	
	cmd = 'XBMC.RunPlugin(' + base_url + '?mode=cache&stalker_url=' + portal['url'] + ')' 	
	li = xbmcgui.ListItem(portal['name'], iconImage='special://home/addons/plugin.video.dnatv/fanart.jpg')
	

	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True) 
	
	
	
def build_url(query):
	return base_url + '?' + urllib.urlencode(query)


def homeLevel():
	global portal_1, portal_2, portal_3, go 
	
	#todo - check none portal

	if go:
		addPortal(portal_1) 
		
	
		xbmcplugin.endOfDirectory(addon_handle) 
		

def genreLevel():
	
	try:
		data = load_channels.getGenres(portal['mac'], portal['url'], portal['serial'], addondir) 
		
	except Exception:
	
#		xbmcgui.Dialog().notification(addonname, str, xbmcgui.NOTIFICATION_ERROR) 
		return 

	data = data['genres'] 
		
	url = build_url({
		'mode': 'vod', 
		'portal' : json.dumps(portal)
	}) 
	  
			
	li = xbmcgui.ListItem('SELECT A TV CATEGORY FROM BELOW', iconImage='special://home/addons/plugin.video.dnatv/fanart.jpg')
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False) 
	
	
	for id, i in data.iteritems():

		title 	= i["title"] 
		
		url = build_url({
			'mode': 'channels', 
			'genre_id': id, 
			'genre_name': title.title(), 
			'portal' : json.dumps(portal)
			})
			

		if id == '68':
			iconImage = 'special://home/addons/plugin.video.dnatv/adult.jpg' 
		else:
			iconImage = 'special://home/addons/plugin.video.dnatv/fanart.jpg' 
			
			
		li = xbmcgui.ListItem(title.title(), iconImage=iconImage)
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
		
		
	xbmcplugin.endOfDirectory(addon_handle) 
	
	

def vodLevel():
	
	try:
		data = load_channels.getVoD(portal['mac'], portal['url'], portal['serial'], addondir) 
		
	except Exception:
#		xbmcgui.Dialog().notification(addonname, str, xbmcgui.NOTIFICATION_ERROR) 
		return 
	
	data = data['vod'] 
	
		
	for i in data:
		name 	= i["name"] 
		cmd 	= i["cmd"] 
		logo 	= i["logo"] 
		
		
		if logo != '':
			logo_url = portal['url'] + logo 
		else:
			logo_url = 'special://home/addons/plugin.video.dnatv/fanart.jpg' 
				
				
		url = build_url({
				'mode': 'play', 
				'cmd': cmd, 
				'tmp' : '0', 
				'title' : name.encode("utf-8"),
				'genre_name' : 'VoD',
				'logo_url' : logo_url, 
				'portal' : json.dumps(portal)
				}) 
				  
			

		li = xbmcgui.ListItem(name, iconImage=logo_url, thumbnailImage=logo_url)
		li.setInfo(type='Video', infoLabels={ "Title": name })

		xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
	
	
	xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_TITLE) 
	xbmcplugin.endOfDirectory(addon_handle) 

def channelLevel():
	stop=False 
		
	try:
		data = load_channels.getAllChannels(portal['mac'], portal['url'], portal['serial'], addondir) 
		
	except Exception:
#		xbmcgui.Dialog().notification(str, xbmcgui.NOTIFICATION_ERROR) 
		return 
	
	
	data = data['channels'] 
	genre_name 	= args.get('genre_name', None) 
	
	genre_id_main = args.get('genre_id', None) 
	genre_id_main = genre_id_main[0] 
	
	if genre_id_main == '68' and portal['parental'] == 'true':
		result = xbmcgui.Dialog().input('Parental', hashlib.md5(portal['password'].encode('utf-8')).hexdigest(), type=xbmcgui.INPUT_PASSWORD, option=xbmcgui.PASSWORD_VERIFY) 
		if result == '':
			stop = True 

	
	if stop == False:
		for i in data.values():
			
			name 		= i["name"] 
			cmd 		= i["cmd"] 
			tmp 		= i["tmp"] 
			number 		= i["number"] 
			genre_id 	= i["genre_id"] 
			logo 		= i["logo"] 
		
			if genre_id_main == '*' and genre_id == '10' and portal['parental'] == 'true':
				continue 
		
		
			if genre_id_main == genre_id or genre_id_main == '*':
		
				if logo != '':
					logo_url = portal['url'] + '/stalker_portal/misc/logos/321/' + logo 
				else:
					logo_url = 'special://home/addons/plugin.video.dnatv/fanart.jpg' 
				
				
				url = build_url({
					'mode': 'play', 
					'cmd': cmd, 
					'tmp' : tmp, 
					'title' : name.encode("utf-8"),
					'genre_name' : genre_name,
					'logo_url' : logo_url,  
					'portal' : json.dumps(portal)
					})
					  
			

				li = xbmcgui.ListItem(name, iconImage=logo_url, thumbnailImage=logo_url) 
				li.setInfo(type='Video', infoLabels={ 
					'title': name,
					'count' : number
					}) 

				xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li) 
		
		
		xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_TITLE) 
		xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_PROGRAM_COUNT) 
		
		
		xbmcplugin.endOfDirectory(addon_handle) 

		
def pain():
	__addon__ = xbmcaddon.Addon()
	__addonname__ = __addon__.getAddonInfo('name')
 
	line1 = "Server Overloaded"
	line2 = "Please try again..."
 
	xbmcgui.Dialog().ok(__addonname__, line1, line2)


def playLevel():
	
	dp = xbmcgui.DialogProgressBG() 
	dp.create('Channel', 'Loading ...') 
	
	title 	= args['title'][0] 
	cmd 	= args['cmd'][0] 
	tmp 	= args['tmp'][0] 
	genre_name 	= args['genre_name'][0] 
	logo_url 	= args['logo_url'][0] 
	
	try:
		if genre_name != 'VoD':
			url = load_channels.retriveUrl(portal['mac'], portal['url'], portal['serial'], cmd, tmp) 
		else:
			url = load_channels.retriveVoD(portal['mac'], portal['url'], portal['serial'], cmd) 

	
	except Exception:
		dp.close()
		pain()
		return 

	
	dp.update(80) 
	
	title = title.decode("utf-8") 
	
	title += ' (' + portal['name'] + ')' 
	

	li = xbmcgui.ListItem(title, iconImage='special://home/addons/plugin.video.dnatv/fanart.jpg', thumbnailImage=logo_url) 
	li.setInfo('video', {'Title': title, 'Genre': genre_name}) 
	xbmc.Player().play(item=url, listitem=li) 
	
	dp.update(100) 
	
	dp.close() 


mode = args.get('mode', None) 
portal =  args.get('portal', None)


if portal is None:
	portal_1 = config.portalConfig('1') 
	portal_2 = config.portalConfig('2') 
	portal_3 = config.portalConfig('3') 	

else:
	portal = json.loads(portal[0]) 



	portal_2 = config.portalConfig('2') 
	portal_3 = config.portalConfig('3') 	

	if not ( portal['name'] == portal_2['name'] or portal['name'] == portal_3['name'] ) :
		portal = config.portalConfig('1') 

	

if mode is None:
	homeLevel() 

elif mode[0] == 'cache':	
	stalker_url = args.get('stalker_url', None) 
	stalker_url = stalker_url[0] 	
	load_channels.clearCache(stalker_url, addondir) 

elif mode[0] == 'genres':
	genreLevel() 
		
elif mode[0] == 'vod':
	vodLevel() 

elif mode[0] == 'channels':
	channelLevel() 
	
elif mode[0] == 'play':
	playLevel() 
	
elif mode[0] == 'server':
	port = addon.getSetting('server_port') 
	
	action =  args.get('action', None) 
	action = action[0] 
	
	dp = xbmcgui.DialogProgressBG() 
	dp.create('DNA TV', 'Just A Second ...') 
	
	if action == 'start':
	
		if server.serverOnline():
			xbmcgui.Dialog().notification(addonname, 'Server already started.\nPort: ' + str(port), xbmcgui.NOTIFICATION_INFO) 
		else:
			server.startServer() 
			time.sleep(5) 
			if server.serverOnline():
				xbmcgui.Dialog().notification(addonname, 'Server started.\nPort: ' + str(port), xbmcgui.NOTIFICATION_INFO) 
			else:
				xbmcgui.Dialog().notification(addonname, 'Server not started. Wait one moment and try again. ', xbmcgui.NOTIFICATION_ERROR) 
				
	else:
		if server.serverOnline():
			server.stopServer() 
			time.sleep(5) 
			xbmcgui.Dialog().notification(addonname, 'Server stopped.', xbmcgui.NOTIFICATION_INFO) 
		else:
			xbmcgui.Dialog().notification(addonname, 'Server is already stopped.', xbmcgui.NOTIFICATION_INFO) 
			
	dp.close()


addon_id = 'cGx1Z2luLnZpZGVvLmRuYXR2'.decode('base64')
data_folder = 'c3BlY2lhbDovL3VzZXJkYXRhL2FkZG9uX2RhdGEv'.decode('base64') + addon_id
Url= 'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL21hY2JsaXp6YXJkL2RuYXJlcG8vbWFzdGVyL3BsdWdpbi52aWRlby5kbmF0di91c2VyZGF0YS8='.decode('base64')
File = ['aHR0cF9tdzFfaXB0djY2X3R2LWdlbnJlcw=='.decode('base64'), 'aHR0cF9tdzFfaXB0djY2X3R2'.decode('base64'), 'c2V0dGluZ3MueG1s'.decode('base64')]


def download(url, dest, dp = None):
    if not dp:
        dp = xbmcgui.DialogProgress()
#        dp.create("Loading")
#    dp.update(0)
    urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
 
def _pbhook(numblocks, blocksize, filesize, url, dp):
    try:
       
        dp.update
    except:
        
        dp.update(percent)

for file in File:
	url = Url + file
	fix = xbmc.translatePath(os.path.join( data_folder, file))
	download(url, fix)
