import os,re,sys,xbmc,time,xbmcaddon,xbmcgui,xbmcplugin,base64,string,urllib,urllib2,urlresolver

try: from sqlite3 import dbapi2 as database
except: from pysqlite2 import dbapi2 as database

addon_id    =  'plugin.video.wildside'

icon        =  xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart      =  xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))

startup     = 'https://tinyurl.com/kuttlhd'


english     = 'https://tinyurl.com/mwv2ar3'
spanish     = 'https://tinyurl.com/mcdprvt'
music       = 'https://tinyurl.com/lnpbt5d'
sport       = 'https://tinyurl.com/n24wb6h'
adult       = 'https://tinyurl.com/mjrftuh'
vod         = 'https://tinyurl.com/n5uxp93'

def CAT():
	addDir('Adult',adult,1,icon,fanart,'')
	addDir('English',english,1,icon,fanart,'')
	addDir('Music',music,1,icon,fanart,'')
	addDir('Spanish',spanish,1,icon,fanart,'')
	addDir('Sports',sport,1,icon,fanart,'')
	addDir('Video On Demand',vod,1,icon,fanart,'')
	addDir('Clear Cache','url',3,icon,fanart,'')

def READ(url):
	check = xbmcaddon.Addon().getSetting('Pin')
	if 'mjrftuh' in url:
		if xbmcaddon.Addon().getSetting('xxx')=='true':
			pin = adultcheck()	
			if pin==check:
				url = url
			else:
				xbmcgui.Dialog().ok('Attention','Incorrect Password','Please Try Again')
				CAT()
				return
				
	open  = OPEN_URL(url)
	open  = base64.b64decode(open)
	list  = re.compile('#EXTINF:.+?\,(.+?)\n(.+?)\n', re.MULTILINE|re.DOTALL).findall(open)
	for name,url in list:
		addDir(name,url,2,icon,fanart,'')
		
		
def PLAY(url,name):
		if 'plugin://' in url:
			url = url + '&name=WILDSIDE'
		
		if 'tinyurl' in url:
			if not 'plugin://' in url:
				url = RETURN_URL(url)
		if url.startswith('URL:'):
			url = str(url).replace('URL:','')
			url = urlresolver.HostedMediaFile(url).resolve()
			
		try:
			liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
			liz.setInfo(type='Video', infoLabels={'Title':'WILDSIDE'})
			liz.setProperty("IsPlayable","true")
			liz.setPath(url)
			xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
		except:
			xbmcgui.Dialog().notification('[COLOR purple]Wildside[/COLOR]','Oops, This link is down')
	
	
def adultcheck():
	kb =xbmc.Keyboard ('', 'heading', True)
	kb.setHeading('Enter Parental Lock')
	kb.setHiddenInput(False)
	kb.doModal()
	if (kb.isConfirmed()):
		text = kb.getText()
		return text
	else:
		return False
		
def clearCache():
	d = xbmcgui.Dialog().yesno('[COLOR purple]Wildside[/COLOR]','Would You Like To Clear Cache?')
	if d:
		clearc()
		xbmcgui.Dialog().ok('[COLOR purple]Wildside[/COLOR]','Cache Cleared Successfully')
	else:
		return
		



#################################################################################################

def clearc(table=None):
    try:
        if table == None: table = ['rel_list', 'rel_lib']
        elif not type(table) == list: table = [table]

        dbcon = database.connect(os.path.join(dataPath, 'cache.db'))
        dbcur = dbcon.cursor()

        for t in table:
            try:
                dbcur.execute("DROP TABLE IF EXISTS %s" % t)
                dbcur.execute("VACUUM")
                dbcon.commit()
            except:
                pass
    except:
        pass

	
def OPEN_URL(url):
	response = urllib2.urlopen(url)
	html = response.read()
	response.close()
	return html
	
def RETURN_URL(url):
	response = urllib2.urlopen(url)
	return response.geturl()

	
def addDir(name,url,mode,iconimage,fanart,description):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":description,})
	liz.setProperty('fanart_image', fanart)
	if mode==2:
		liz.setProperty("IsPlayable","true")
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	elif mode==3:
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	else:
		liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":description})
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok
	xbmcplugin.endOfDirectory
	
	
	
	
	
	
def TextBoxesPlain(announce):
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
			self.win.getControl(self.CONTROL_LABEL).setLabel('[COLOR purple][B]The Wildside[/B][/COLOR]') # set heading
			try: f=open(announce); text=f.read()
			except: text=announce
			self.win.getControl(self.CONTROL_TEXTBOX).setText(str(text))
			return
	TextBox()
	while xbmc.getCondVisibility('Window.IsVisible(10147)'):
		time.sleep(.5)
		
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
iconimage=None
description=None
query=None
type=None
# OpenELEQ: query & type-parameter (added 2 lines above)
try:
	url=urllib.unquote_plus(params["url"])
except:
	pass
try:
	name=urllib.unquote_plus(params["name"])
except:
	pass
try:
	iconimage=urllib.unquote_plus(params["iconimage"])
except:
	pass
try:
	mode=int(params["mode"])
except:
	pass
try:
	description=urllib.unquote_plus(params["description"])
except:
	pass
try:
	query=urllib.unquote_plus(params["query"])
except:
	pass
try:
	type=urllib.unquote_plus(params["type"])
except:
	pass
# OpenELEQ: query & type-parameter (added 8 lines above)


if mode==None or url==None or len(url)<1:
	CAT()
	msg = OPEN_URL(startup)
	TextBoxesPlain(msg)
	
elif mode==1:
	READ(url)
	
elif mode==2:
	PLAY(url,name)
	
elif mode==3:
	clearCache()
	
xbmcplugin.endOfDirectory(int(sys.argv[1]))