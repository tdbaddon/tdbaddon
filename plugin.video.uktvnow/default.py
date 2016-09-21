import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os,json,random,string,base64,hashlib,pyaes
import net


AddonID ='plugin.video.uktvnow'
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + AddonID , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + AddonID, 'icon.png'))
artpath = xbmc.translatePath(os.path.join('special://home/addons/' + AddonID + '/resources/art/'))
dialog = xbmcgui.Dialog()
selfAddon = xbmcaddon.Addon(id=AddonID)
net = net.Net()
Username='-1'
	
def Main():
	addDir('All Channels','0',1,artpath+'all.PNG',fanart)
	addDir('Entertainment','1',1,artpath+'ent.PNG',fanart)
	addDir('Movies','2',1,artpath+'mov.PNG',fanart)
	addDir('Music','3',1,artpath+'mus.PNG',fanart)
	addDir('News','4',1,artpath+'news.PNG',fanart)
	addDir('Sports','5',1,artpath+'sport.PNG',fanart)
	addDir('Documentary','6',1,artpath+'doc.PNG',fanart)
	addDir('Kids Corner','7',1,artpath+'kids.PNG',fanart)
	addDir('Food','8',1,artpath+'food.PNG',fanart)
	addDir('Religious','9',1,artpath+'rel.PNG',fanart)
	addDir('USA Channels','10',1,artpath+'us.PNG',fanart)
	addDir('Others','11',1,artpath+'others.PNG',fanart)
	xbmc.executebuiltin('Container.SetViewMode(500)')
 	
def GetContent():
	token=GetToken('http://uktvnow.net/app2/v3/get_all_channels',Username)
	headers={'User-Agent':'USER-AGENT-UKTVNOW-APP-V2','app-token':token}
	postdata={'username':Username}
	channels = net.http_POST('http://uktvnow.net/app2/v3/get_all_channels',postdata, headers).content
	channels = channels.replace('\/','/')
        match=re.compile('"pk_id":"(.+?)","channel_name":"(.+?)","img":"(.+?)","http_stream":"(.+?)","rtmp_stream":"(.+?)","cat_id":"(.+?)"').findall(channels)
	return match

def GetToken(url,username):
	if 'get_valid_link' in url:
		s = "uktvnow-token--_|_-http://uktvnow.net/app2/v3/get_valid_link-uktvnow_token_generation-"+username+"-_|_-123456_uktvnow_654321-_|_-uktvnow_link_token"
	else:
		s = "uktvnow-token--_|_-"+url+"-uktvnow_token_generation-"+username+"-_|_-123456_uktvnow_654321"
	return hashlib.md5(s).hexdigest()

def GetChannels(url):
	match = GetContent()
	for channelid,name,iconimage,stream1,stream2,cat in match:
		thumb='https://app.uktvnow.net/'+iconimage+'|User-Agent=Dalvik/2.1.0 (Linux; U; Android 6.0.1; SM-G935F Build/MMB29K)'   
		if url=='0':addLink(name,'url',2,thumb,fanart,channelid)
		if cat==url:addLink(name,'url',2,thumb,fanart,channelid)
	xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)
	xbmc.executebuiltin('Container.SetViewMode(500)')

def GetStreams(name,iconimage,channelid):
        UAToken = GetToken('http://uktvnow.net/app2/v3/get_user_agent', Username)
        headers={'User-Agent':'USER-AGENT-UKTVNOW-APP-V2','app-token':UAToken}
        postdata={'User-Agent':'USER-AGENT-UKTVNOW-APP-V2','app-token':UAToken,'version':'5.7'}
        UAPage = net.http_POST('http://uktvnow.net/app2/v3/get_user_agent',postdata, headers).content
	UAString=re.compile('"msg":{".+?":"(.+?)"}}').findall(UAPage)[0]
	#UA=magicness(UAString)
        UA=UAString
	playlist_token = GetToken('http://uktvnow.net/app2/v3/get_valid_link', Username+channelid)
	postdata = {'useragent':UA,'username':Username,'channel_id':channelid,'version':'5.7'}	
	headers={'User-Agent':'USER-AGENT-UKTVNOW-APP-V2','app-token':playlist_token}
	channels = net.http_POST('http://uktvnow.net/app2/v3/get_valid_link',postdata, headers).content
	match=re.compile('"channel_name":"(.+?)","img":".+?","http_stream":"(.+?)","rtmp_stream":"(.+?)"').findall(channels)
	for name,stream1,stream2 in match:	  
		streamname=[]
                streamurl=[]
                streamurl.append( stream1 )
                streamurl.append( stream2 )
                streamname.append( 'Stream 1' )
                streamname.append( 'Stream 2' )
	select = dialog.select(name,streamname)
	if select == -1:return
	else:
		url=streamurl[select]
		url=magicness(url)
		if 'http' in url: url = url+"|User-Agent=EMVideoView 2.5.6 (25600) / Android 6.0.1 / SM-G935F"
		else: url = url+' timeout=10'
		ok=True
		liz=xbmcgui.ListItem(name, iconImage=iconimage,thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": name } )
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
		xbmc.Player().play(url, liz, False)
		return ok
	
def magicness(url):
        magic="1579547dfghuh,difj389rjf83ff90,45h4jggf5f6g,f5fg65jj46,gr04jhsf47890$93".split(',')
        decryptor = pyaes.new(magic[1], pyaes.MODE_CBC, IV=magic[4])
        url= decryptor.decrypt(url.decode("hex")).split('\0')[0]
        return url
     
def addLink(name,url,mode,iconimage,fanart,channelid=''):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&channelid="+str(channelid)+"&iconimage="+urllib.quote_plus(iconimage)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
		liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': channelid } )
		liz.setProperty('fanart_image', fanart)
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
		return ok

def addDir(name,url,mode,iconimage,fanart,channelid=''):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&channelid="+str(channelid)+"&iconimage="+urllib.quote_plus(iconimage)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
		liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': channelid } )
		liz.setProperty('fanart_image', fanart)
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
		return ok
	
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



def setView(content, viewType):
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if selfAddon.getSetting('auto-view')=='true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % selfAddon.getSetting(viewType) )
		   
params=get_params()
url=None
name=None
mode=None
iconimage=None
channelid=None

try:url=urllib.unquote_plus(params["url"])
except:pass
try:name=urllib.unquote_plus(params["name"])
except:pass
try:mode=int(params["mode"])
except:pass
try:iconimage=urllib.unquote_plus(params["iconimage"])
except:pass
try:channelid=urllib.unquote_plus(params["channelid"])
except:pass

if mode==None or url==None or len(url)<1:Main()
elif mode==1:GetChannels(url)
elif mode==2:GetStreams(name,iconimage,channelid)
elif mode==3:Schedule(url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
