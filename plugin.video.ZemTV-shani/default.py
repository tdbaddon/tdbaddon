import xbmc, xbmcgui, xbmcplugin
import urllib2,urllib,cgi, re, urlresolver  
import urlparse
import HTMLParser
import xbmcaddon
from operator import itemgetter
import traceback,cookielib
import base64,os,  binascii
import CustomPlayer,uuid
import checkbad
from time import time
import base64
try:
    from lxmlERRRORRRR import etree
    print("running with lxml.etree")
except ImportError:
    try:
        import xml.etree.ElementTree as etree
        print("running with ElementTree on Python 2.5+")
    except ImportError:
        try:
        # normal cElementTree install
            import cElementTree as etree
            print("running with cElementTree")
        except ImportError:
            try:
            # normal ElementTree install
                import elementtree.ElementTree as etree
                print("running with ElementTree")
            except ImportError:
                print("Failed to import ElementTree from any known place")
          
try:
    import json
except:
    import simplejson as json
    
__addon__       = xbmcaddon.Addon()
__addonname__   = __addon__.getAddonInfo('name')
__icon__        = __addon__.getAddonInfo('icon')
addon_id = 'plugin.video.ZemTV-shani'
selfAddon = xbmcaddon.Addon(id=addon_id)
profile_path =  xbmc.translatePath(selfAddon.getAddonInfo('profile'))
  
willowCommonUrl=''# this is where the common url will stay
#willowCommonUrl=''

addonPath = xbmcaddon.Addon().getAddonInfo("path")
addonversion =xbmcaddon.Addon().getAddonInfo("version")


WTVCOOKIEFILE='WTVCookieFile.lwp'
WTVCOOKIEFILE=os.path.join(profile_path, WTVCOOKIEFILE)
ZEMCOOKIEFILE='ZemCookieFile.lwp'
ZEMCOOKIEFILE=os.path.join(profile_path, ZEMCOOKIEFILE)
S365COOKIEFILE='s365CookieFile.lwp'
S365COOKIEFILE=os.path.join(profile_path, S365COOKIEFILE)
 
mainurl=base64.b64decode('aHR0cDovL3d3dy56ZW10di5jb20v')
liveURL=base64.b64decode('aHR0cDovL3d3dy56ZW10di5jb20vbGl2ZS1wYWtpc3RhbmktbmV3cy1jaGFubmVscy8=')

tabURL =base64.b64decode('aHR0cDovL3d3dy5lYm91bmRzZXJ2aWNlcy5jb206ODg4OC91c2Vycy9yZXgvbV9saXZlLnBocD9hcHA9JXMmc3RyZWFtPSVz')
DONOTCACHE=   selfAddon.getSetting( "donotcache" ) =="true"
if not selfAddon.getSetting( "dummy" )=="true":
    selfAddon.setSetting( "dummy" ,"true")

class NoRedirection(urllib2.HTTPErrorProcessor):
   def http_response(self, request, response):
       return response
   https_response = http_response

def ShowSettings(Fromurl):
	selfAddon.openSettings()
	
def addLink(name,url,iconimage):
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok


def addDir(name,url,mode,iconimage,showContext=False,showLiveContext=False,isItFolder=True, linkType=None):
#	print name
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )

	if showContext==True:
		cmd1 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "DM")
		cmd2 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "LINK")
		cmd3 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "Youtube")
		cmd4 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "PLAYWIRE")
		cmd5 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "EBOUND")
		cmd6 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "PLAYWIRE")
		cmd7 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "VIDRAIL")

		
		liz.addContextMenuItems([('Show All Sources',cmd6),('Play Vidrail video',cmd7),('Play Ebound video',cmd5),('Play Playwire video',cmd4),('Play Youtube video',cmd3),('Play DailyMotion video',cmd1),('Play Tune.pk video',cmd2)])
	if linkType:
		u="XBMC.RunPlugin(%s&linkType=%s)" % (u, linkType)
		
#	if showLiself.wfileveContext==True:
#		cmd1 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "RTMP")
#		cmd2 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "HTTP")
#		liz.addContextMenuItems([('Play RTMP Steam (flash)',cmd1),('Play Http Stream (ios)',cmd2)])
	
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isItFolder)
	return ok

def PlayChannel ( channelName ): 
#	print linkType
	url = tabURL.replace('%s',channelName);
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
#	print link
	
	match=re.compile('\"(http.*?playlist.m3u.*?)\"').findall(link)
#	print match

	strval = match[0]
#	print strval
	req = urllib2.Request(strval)
	req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
	req.add_header('Referer', base64.b64decode('aHR0cDovL3d3dy5lYm91bmRzZXJ2aWNlcy5jb206ODg4OC91c2Vycy9yZXgvbV9saXZlLnBocA=='))
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
#	print link
	match=re.compile('\"(http.*?hashAESkey=.*?)\"').findall(link)
#	print match
	strval = match[0]

	listitem = xbmcgui.ListItem(channelName)
	listitem.setInfo('video', {'Title': channelName, 'Genre': 'Live TV'})
	playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
	playlist.clear()
	playlist.add (strval)

	xbmc.Player().play(playlist)
	return

def getUrl(url, cookieJar=None,post=None, timeout=20, headers=None,jsonpost=False):

    cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
    opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
    #opener = urllib2.install_opener(opener)
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
    if headers:
        for h,hv in headers:
            req.add_header(h,hv)
    if jsonpost:
        req.add_header('Content-Type', 'application/json')
    response = opener.open(req,post,timeout=timeout)
    if response.info().get('Content-Encoding') == 'gzip':
            from StringIO import StringIO
            import gzip
            buf = StringIO( response.read())
            f = gzip.GzipFile(fileobj=buf)
            link = f.read()
    else:
        link=response.read()
    response.close()
    return link;

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


def DisplayChannelNames(url):
	req = urllib2.Request(mainurl)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
#	print link
#	 match=re.compile('<param name="URL" value="(.+?)">').findall(link)
#	match=re.compile('<a href="(.+?)"').findall(link)
#	match=re.compile('onclick="playChannel\(\'(.*?)\'\);">(.*?)</a>').findall(link)
#	match =re.findall('onclick="playChannel\(\'(.*?)\'\);">(.*?)</a>', link, re.DOTALL|re.IGNORECASE)


	match =re.findall('onclick="playChannel\(\'(.*?)\'\);".?>(.*?)</a>', link, re.DOTALL|re.IGNORECASE)
#	print match
#	print 'val is'
	match=sorted(match,key=itemgetter(1)   )
	for cname in match:
		if cname[0]<>'':
			addDir(cname[1] ,cname[0] ,1,'',isItFolder=False)
	return


def Addtypes():
	addDir('Latest Shows' ,'Shows' ,2,'')
	addDir('All Programs and Talk Shows' ,'ProgTalkShows' ,2,'')
	addDir('Pakistani Live Channels' ,'PakLive' ,2,'')
	addDir('Indian Live Channels' ,'IndianLive' ,2,'')
	addDir('Punjabi Live Channels' ,'PunjabiLive' ,2,'')
	addDir('Movies' ,'zemmovies',36,'')
	addDir('Sports' ,'Live' ,13,'')
	addDir('Settings' ,'Live' ,6,'',isItFolder=False)
	addDir('Clear Cache' ,'Live' ,54,'',isItFolder=False)

	return

def PlayFlashTv(url):
#    patt='(.*?)'
#    print link
#    match_url =re.findall(patt,link)[0]
    referer=[('Referer',base64.b64decode('aHR0cDovL3Nwb3J0czR1LnR2L2VtYmVkL1NreS1zcG9ydHMtMS5waHA='))]
    res=getUrl(url,headers=referer)
    stream_pat='streamer\',[\'"](.*?)[\'"]'
    playpath_pat='\'file\',\'(.*?)\''
    
    swf_url=base64.b64decode("aHR0cDovL2ZsYXNodHYuY28vZVBsYXllcnIuc3dm")
    pageUrl=base64.b64decode("aHR0cDovL2ZsYXNodHYuY28vZW1iZWRvLnBocD9saXZlPXNra3kxJnZ3PTY1MCZ2aD00ODA=")
    rtmp_url=re.findall(stream_pat,res)[0]
    play_path=re.findall(playpath_pat,res)[0]

    
    video_url= '%s playpath=%s pageUrl=%s swfUrl=%s token=%s timeout=20'%(rtmp_url,play_path,pageUrl,swf_url,'%ZZri(nKa@#Z')
    
    playlist = xbmc.PlayList(1)
    playlist.clear()
    listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
    playlist.add(video_url,listitem)
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(playlist) 
    
def PlayCricFree(url):
    progress = xbmcgui.DialogProgress()
    progress.create('Progress', 'Fetching Streaming Info')
    progress.update( 10, "", "Finding links..", "" )

    res=getUrl(url)
    patt='<iframe frameborder="0" marginheight="0".*?src="(.*?)" id="iframe"'
    url2=re.findall(patt,res)[0]
    referer=[('Referer',url)]
    res=getUrl(url2,headers=referer)
    urlToPlay=None
    supported=False
    if 'theactionlive.com/' in res:
        supported=True
        progress.update( 30, "", "Finding links..stage2", "" )
        patt="id='(.*?)'.*?width='(.*)'.*?height='(.*?)'"
        gid,wd,ht=re.findall(patt,res)[0]
        referer=[('Referer',url2)]
        url3='http://theactionlive.com/livegamecr2.php?id=%s&width=%s&height=%s&stretching='%(gid,wd,ht)
        res=getUrl(url3,headers=referer)    
        if 'biggestplayer.me' in res:
            progress.update( 50, "", "Finding links..stage3", "" )
            patt="id='(.*?)'.*?width='(.*)'.*?height='(.*?)'"
            gid,wd,ht=re.findall(patt,res)[0]
            referer=[('Referer',url3)]
            
            patt="src='(.*?)'"
            jsUrl=re.findall(patt,res)[0]
            jsData=getUrl(jsUrl)
            patt="\.me\/(.*?)\?"
            phpURL=re.findall(patt,jsData)[0]
            url4='http://biggestplayer.me/%s?id=%s&width=%s&height=%s'%(phpURL,gid,wd,ht)
            progress.update( 80, "", "Finding links..last stage", "" )
            res=getUrl(url4,headers=referer)    
            patt='file: "(.*?)"'
            urlToPlay=re.findall(patt,res)[0];
            referer=[('Referer',url4)]
            urlToPlay+='|Referer='+url4
    if 'www.reytv.co' in res:
        supported=True
        progress.update( 30, "", "Finding links..stage2", "" )
        patt="fid='(.*?)'.*?v_width=(.*?);.*?v_height=(.*?);"
        gid,wd,ht=re.findall(patt,res)[0]
        referer=[('Referer',url2)]
        url3='http://reytv.co/embedo.php?live=%s&width=%s&height=%s'%(gid,wd,ht)
        progress.update( 50, "", "Finding links..stage3", "" )
        res=getUrl(url3,headers=referer)
        
        patt='file: "(.*?)"'
        rtmp=re.findall(patt,res)[0]
        patt='securetoken: "(.*?)"'
        token=re.findall(patt,res)[0]           
        urlToPlay=rtmp + ' token=' + token + ' pageUrl='+url3+ ' swfUrl=http://p.jwpcdn.com/6/12/jwplayer.flash.swf'+' timeout=20'
    
    if urlToPlay and len(urlToPlay)>0:
        playlist = xbmc.PlayList(1)
        playlist.clear()
        listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
        playlist.add(urlToPlay,listitem)
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(playlist) 
    else:
        dialog = xbmcgui.Dialog()
        if not supported:
            ok = dialog.ok('Not Supported','This channel is not supported yet')
        
def sorted_nicely( l ): 
    """ Sort the given iterable in the way that humans expect.""" 
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key[1]) ] 
    return sorted(l, key = alphanum_key)  
def AddP3gSports(url):
    pat="pe='text\/javascript'>ch='(.*?)'"
    res=getUrl("http://c247.tv/")
    channels=re.findall(pat,res)
    channels=sorted(channels,key=lambda s: s[0].lower()   )

    
    for i in channels:
        addDir('%s P3G.Tv'%(i.replace('_','')) ,'http://c247.tv/live.php?ch=%s'%i,17,'', False, True,isItFolder=False)


        
def AddCricFree(url):
    pat='<li.*?><a href="(.*?)".*?channels-icon (.*?)"'
    res=getUrl("http://cricfree.sx/")
    channels=re.findall(pat,res)
    
    pat='<li><a href="(.*?)".*?\<span class="chclass3"\>(.*?)<'
    channels+=re.findall(pat,res)    
#    channels=sorted(channels,key=lambda s: s[1].lower()   )
    channels=sorted_nicely(channels)
    for u,n in channels:
        addDir(n.capitalize(),u,42,'', False, True,isItFolder=False)
    

##http://c247.tv/
#http://c247.tv/live.php?ch=Geo_Super
#http://c247.tv/

    
def AddFlashtv(url):
    addDir('ss 1' ,base64.b64decode('aHR0cDovL2ZsYXNodHYuY28vZW1iZWRvLnBocD9saXZlPXNra3kxJnZ3PTY1MCZ2aD00ODA='),32,'', False, True,isItFolder=False)
    addDir('ss 2' ,base64.b64decode('aHR0cDovL2ZsYXNodHYuY28vZW1iZWRvLnBocD9saXZlPXNra3kyJnZ3PTY1MCZ2aD00ODA=') ,32,'', False, True,isItFolder=False)
    addDir('ss 3' ,base64.b64decode('aHR0cDovL2ZsYXNodHYuY28vZW1iZWRvLnBocD9saXZlPXNra3kzJnZ3PTY1MCZ2aD00ODA='),32,'', False, True,isItFolder=False)
    addDir('ss 4' ,base64.b64decode('aHR0cDovL2ZsYXNodHYuY28vZW1iZWRvLnBocD9saXZlPXNra3k0JnZ3PTY1MCZ2aD00ODA=') ,32,'', False, True,isItFolder=False)
    addDir('ss 5' ,base64.b64decode('aHR0cDovL2ZsYXNodHYuY28vZW1iZWRvLnBocD9saXZlPXNra3k1JnZ3PTY1MCZ2aD00ODA='),32,'', False, True,isItFolder=False)

    
    
def AddSports(url):
    match=[]
    if 1==2:
        match.append((base64.b64decode('U2t5IFNwb3J0IDE=')+ ' [Not working]','manual',base64.b64decode('aHR0cDovL2pweG1sLmphZG9vdHYuY29tL3Z1eG1sLnBocC9qYWRvb3htbC9wbGF5LzMxNg=='),''))
        match.append((base64.b64decode('U2t5IFNwb3J0IDI=')+' [Not working]','manual',base64.b64decode('aHR0cDovL2pweG1sLmphZG9vdHYuY29tL3Z1eG1sLnBocC9qYWRvb3htbC9wbGF5LzMyNg=='),''))
        match.append((base64.b64decode('U2t5IFNwb3J0IDM=')+' [Not working]','manual',base64.b64decode('aHR0cDovL215amFkb290di5qYWRvb3R2LmNvbS9qbWFya3MvYm94L3BsYXlWaWRlby5waHA/cGxheVVybD1ydG1wOi8vcXVpbnplbGl2ZWZzLmZwbGl2ZS5uZXQvcXVpbnplbGl2ZS1saXZlL3NreXNwb3J0czMuc3RyZWFtP3NlY3VyaXR5dHlwZT0y'),''))
        match.append((base64.b64decode('U2t5IFNwb3J0IDQ=')+' [Not working]','manual',base64.b64decode('aHR0cDovL2pweG1sLmphZG9vdHYuY29tL3Z1eG1sLnBocC9qYWRvb3htbC9wbGF5LzMxNQ=='),''))
        match.append((base64.b64decode('U2t5IFNwb3J0IDU=')+' [Not working]','manual',base64.b64decode('aHR0cDovL215amFkb290di5qYWRvb3R2LmNvbS9qbWFya3MvYm94L3BsYXlWaWRlby5waHA/cGxheVVybD1ydG1wOi8vcXVpbnplbGl2ZWZzLmZwbGl2ZS5uZXQvcXVpbnplbGl2ZS1saXZlL3NreXNwb3J0czUuc3RyZWFtP3NlY3VyaXR5dHlwZT0y'),''))

    if 1==2:    
        match.append((base64.b64decode('U2t5IFNwb3J0IDE=')+' alt HD','gen',base64.b64decode('aHR0cDovL2Nkcy5hM2c2dDhtOS5od2Nkbi5uZXQvY2FsaXZlb3JpZ2luL3NreXNwb3J0czEuc3RyZWFtL3BsYXlsaXN0Lm0zdTg='),''))
        match.append((base64.b64decode('U2t5IFNwb3J0IDI=')+' alt HD','gen',base64.b64decode('aHR0cDovL2Nkcy5hM2c2dDhtOS5od2Nkbi5uZXQvY2FsaXZlb3JpZ2luL3NreXNwb3J0czIuc3RyZWFtL3BsYXlsaXN0Lm0zdTg='),''))
        match.append((base64.b64decode('U2t5IFNwb3J0IDM=')+' alt HD','gen',base64.b64decode('aHR0cDovL2Nkcy5hM2c2dDhtOS5od2Nkbi5uZXQvY2FsaXZlb3JpZ2luL3NreXNwb3J0czMuc3RyZWFtL3BsYXlsaXN0Lm0zdTg='),''))
        match.append((base64.b64decode('U2t5IFNwb3J0IDQ=')+' alt HD','gen',base64.b64decode('aHR0cDovL2Nkcy5hM2c2dDhtOS5od2Nkbi5uZXQvY2FsaXZlb3JpZ2luL3NreXNwb3J0czQuc3RyZWFtL3BsYXlsaXN0Lm0zdTg='),''))
        match.append((base64.b64decode('U2t5IFNwb3J0IDU=')+' alt HD','gen',base64.b64decode('aHR0cDovL2Nkcy5hM2c2dDhtOS5od2Nkbi5uZXQvY2FsaXZlb3JpZ2luL3NreXNwb3J0czUuc3RyZWFtL3BsYXlsaXN0Lm0zdTg='),''))
        match.append((base64.b64decode('R2VvIFN1cGVy')+' alt HD','gen',base64.b64decode('aHR0cDovL2Nkcy5pOHc3cjVqMi5od2Nkbi5uZXQvamRvcmlnaW4vamRHZW9zdXBlcjQ3Ni5zdHJlYW0vcGxheWxpc3QubTN1OA=='),''))

        

        
    if 1==2:
        match.append((base64.b64decode('U2t5IFNwb3J0IDU=')+' alt HD','gen',base64.b64decode('cnRtcDovLzE2Ny4xMTQuMTE3LjIwOC9saXZlL3NreTV2'),''))
        match.append((base64.b64decode('U2t5IFNwb3J0IGYx')+' alt HD','gen',base64.b64decode('cnRtcDovLzE2Ny4xMTQuMTE3LjIwOC9saXZlL3NreWYxdg=='),''))

    
    #v2
    if 1==2:
        match.append((base64.b64decode('U2t5IFNwb3J0IDE=')+' alt','manual',base64.b64decode('cnRtcGU6Ly80Ni4yNDYuMjkuMTYwOjE5MzUvbCBwbGF5cGF0aD1zc2t5czEgc3dmVXJsPWh0dHA6Ly9oZGNhc3Qub3JnL2VwbGF5ZXIuc3dmIGxpdmU9MSBwYWdlVXJsPWh0dHA6Ly93d3cuaGRjYXN0Lm9yZy9lbWJlZGxpdmU0LnBocD91PXNza3lzMSZ2dz02NTAmdmg9NDcwJmRvbWFpbj1jcmljYm94LnR2IHRva2VuPUZvNV9uMHc/VS5yQTZsMy03MHc0N2NoDQo='),''))
        match.append((base64.b64decode('U2t5IFNwb3J0IDI=')+' alt','manual',base64.b64decode('cnRtcGU6Ly80Ni4yNDYuMjkuMTYwOjE5MzUvbCBwbGF5cGF0aD1zc2t5czIgc3dmVXJsPWh0dHA6Ly9oZGNhc3Qub3JnL2VwbGF5ZXIuc3dmIGxpdmU9MSBwYWdlVXJsPWh0dHA6Ly93d3cuaGRjYXN0Lm9yZy9lbWJlZGxpdmU0LnBocD91PXNza3lzMSZ2dz02NTAmdmg9NDcwJmRvbWFpbj1jcmljYm94LnR2IHRva2VuPUZvNV9uMHc/VS5yQTZsMy03MHc0N2NoDQo='),''))
        match.append((base64.b64decode('U2t5IFNwb3J0IDI=')+' alt 2','manual',base64.b64decode('cnRtcDovLzE3OC4xOC4zMS41Mzo0NDMvbGl2ZXJlcGVhdGVyLzE5MDYxNCBzd2ZVcmw9aHR0cDovL2Jlcm5hcmRvdHYuY2x1Yi9mdWNraW5nY29weS5zd2YgcGFnZVVybD1odHRwOi8vYmlnZ2VzdHBsYXllci5tZS9zdHJlYW0ucGhwP2lkPTE5MDYxNCB0b2tlbj0jYXRkJSMkWkggbGl2ZT0xIHRpbWVvdXQ9MjA='),''))
        
        match.append((base64.b64decode('U2t5IFNwb3J0IDM=')+' alt','manual',base64.b64decode('cnRtcGU6Ly80Ni4yNDYuMjkuMTYwOjE5MzUvbCBwbGF5cGF0aD1zc2t5czMgc3dmVXJsPWh0dHA6Ly9oZGNhc3Qub3JnL2VwbGF5ZXIuc3dmIGxpdmU9MSBwYWdlVXJsPWh0dHA6Ly93d3cuaGRjYXN0Lm9yZy9lbWJlZGxpdmU0LnBocD91PXNza3lzMSZ2dz02NTAmdmg9NDcwJmRvbWFpbj1jcmljYm94LnR2IHRva2VuPUZvNV9uMHc/VS5yQTZsMy03MHc0N2NoDQo='),''))

        match.append((base64.b64decode('U2t5IFNwb3J0IDQ=')+' alt','manual',base64.b64decode('cnRtcGU6Ly80Ni4yNDYuMjkuMTYwOjE5MzUvbCBwbGF5cGF0aD1zc2t5czQgc3dmVXJsPWh0dHA6Ly9oZGNhc3Qub3JnL2VwbGF5ZXIuc3dmIGxpdmU9MSBwYWdlVXJsPWh0dHA6Ly93d3cuaGRjYXN0Lm9yZy9lbWJlZGxpdmU0LnBocD91PXNza3lzMSZ2dz02NTAmdmg9NDcwJmRvbWFpbj1jcmljYm94LnR2IHRva2VuPUZvNV9uMHc/VS5yQTZsMy03MHc0N2NoDQo='),''))
        match.append((base64.b64decode('U2t5IFNwb3J0IDU=')+' alt','manual',base64.b64decode('cnRtcGU6Ly80Ni4yNDYuMjkuMTYwOjE5MzUvbCBwbGF5cGF0aD1zc2t5czUgc3dmVXJsPWh0dHA6Ly9oZGNhc3Qub3JnL2VwbGF5ZXIuc3dmIGxpdmU9MSBwYWdlVXJsPWh0dHA6Ly93d3cuaGRjYXN0Lm9yZy9lbWJlZGxpdmU0LnBocD91PXNza3lzMSZ2dz02NTAmdmg9NDcwJmRvbWFpbj1jcmljYm94LnR2IHRva2VuPUZvNV9uMHc/VS5yQTZsMy03MHc0N2NoDQo='),''))
        match.append((base64.b64decode('U2t5IFNwb3J0IGYx')+' alt','manual',base64.b64decode('cnRtcGU6Ly80Ni4yNDYuMjkuMTYwOjE5MzUvbCBwbGF5cGF0aD1zc2t5c2YxIHN3ZlVybD1odHRwOi8vaGRjYXN0Lm9yZy9lcGxheWVyLnN3ZiBsaXZlPTEgcGFnZVVybD1odHRwOi8vd3d3LmhkY2FzdC5vcmcvZW1iZWRsaXZlNC5waHA/dT1zc2t5czEmdnc9NjUwJnZoPTQ3MCZkb21haW49Y3JpY2JveC50diB0b2tlbj1GbzVfbjB3P1UuckE2bDMtNzB3NDdjaA0K'),''))



    for m in match:
        cname=m[0]
        ty=m[1]
        curl=m[2]
        imgurl=''
        m=11 if ty=='manual' else 33
        addDir(Colored(cname.capitalize(),'ZM') ,base64.b64encode(curl) ,m,imgurl, False, True,isItFolder=False)		#name,url,mode,icon
    
#    addDir('IPTV Sports' ,'sss',46,'')
    addDir('IpBox sports (Beta1 requires F4mTester)' ,'sss',55,'')
    addDir('PTC sports' ,'sss',51,'')
    addDir('Paktv sports' ,'sss',52,'')
    addDir('UniTV sports' ,'sss',53,'')
    addDir('WTV sports' ,'sss',62,'')
    addDir('GTV sports' ,'sss',70,'')
    addDir('Pi sports' ,'sss',71,'')
    addDir('Mona' ,'sss',68,'')
    addDir('Sport365.live' ,'sss',56,'')
    addDir('SmartCric.com (Live matches only)' ,'Live' ,14,'')
    addDir('UKTVNow','sss' ,57,'')
    
#    addDir('Flashtv.co (Live Channels)' ,'flashtv' ,31,'')
    addDir('Willow.Tv (Subscription required, US Only or use VPN)' ,base64.b64decode('aHR0cDovL3d3dy53aWxsb3cudHYv') ,19,'')
    #addDir(base64.b64decode('U3VwZXIgU3BvcnRz') ,'sss',34,'')
    addDir('PV2 Sports' ,'zemsports',36,'')
    #addDir('Yupp Asia Cup','Live' ,60,'')
    addDir('CricHD.tv (Live Channels)' ,'pope' ,26,'')
    #addDir('cricfree.sx' ,'sss',41,'')
    addDir('WatchCric.com-Live matches only' ,base64.b64decode('aHR0cDovL3d3dy53YXRjaGNyaWMubmV0Lw==' ),16,'') #blocking as the rtmp requires to be updated to send gaolVanusPobeleVoKosat
    addDir('c247.tv-P3G.Tv' ,'P3G'  ,30,'')
    #addDir('Streams' ,'sss',39,'')

    
    
    
def PlayCricHD(pageurl):
    progress = xbmcgui.DialogProgress()
    progress.create('Progress', 'finding links')
    progress.update( 10, "", "Getting Urls..")

    req = urllib2.Request(pageurl)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36')
    response = urllib2.urlopen(req)
    videoPage =  response.read()
    response.close()
    pat='<a style="text-decoration: none" href="(.*?)"'
    matc=re.findall(pat,videoPage)
    newurl=matc[0]
    if len(matc)>1:
        newurl=matc[1]
    
    
    pat='var locations.*?"(.*?)"'
    print 'gett',newurl
    temppage=getUrl(newurl,headers=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'),('Referer',pageurl)])
    newurl2=re.findall(pat,temppage)[0]
    req = urllib2.Request(newurl2)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36')
    req.add_header('Referer',newurl)
    response = urllib2.urlopen(req)
    videoPage =  response.read()
    response.close()
    if 'scripts/p3g.js' in videoPage:
        PlayWatchCric(newurl)
        return 
    try:
        pat="fid=['\"](.*?)['\"].*width=([0-9]*).*?height=([0-9]*).*?src=['\"](.*?)['\"]"
        fid,wid,ht, jsurl=re.findall(pat,videoPage)[0]
    except:
        traceback.print_exc(file=sys.stdout)
        pat='IFRAME.*?SRC="(.*?)"'
        newurl=re.findall(pat,videoPage)[0]
        #PlayWatchCric(newurl)
        pat="fid=['\"](.*?)['\"].*width=([0-9]*).*?height=([0-9]*).*?src=['\"](.*?)['\"]"
        videoPage=getUrl(newurl)
        fid,wid,ht, jsurl=re.findall(pat,videoPage)[0]
    progress.update( 40, "", "Translating..")     
    req = urllib2.Request(jsurl)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36')
    response = urllib2.urlopen(req)
    jspage =  response.read()
    response.close()
    pat='(http.*?)\?'
    jsfinal=re.findall(pat,jspage)[0]
    
    
    newurl2="%s?live=%s&vw=%s&vh=%s"%(jsfinal,fid,wid,ht)
    
    req = urllib2.Request(newurl2)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36')
    req.add_header('Referer', newurl)
    
    response = urllib2.urlopen(req)
    videoPage =  response.read()
    response.close()
    if '"r","t","m"' in videoPage:
      print videoPage
      progress.update( 60, "", "decoding Urls..")
      pat='\((\["r".*?\]).*?\+ (.*?)\..*?getElementById\("(.*?)"'  
      pat2='var %s =.*?(\[.*?\])'
      pat3="file: .*?\+ '\/' \+(.*?)\(\)"
      pat4='function.*?%s.*?\{\s.*?\((\[.*?\])'
      pat_sk='securetoken: (.*?)\s'
      mainrtmp, firstarray,docelem=re.findall(pat,videoPage)[0]
      pat2=pat2%firstarray
      firstarray=re.findall(pat2,videoPage)[0]
      docElem='%s>(.*?)<'%docelem
      print docElem
      docElem=re.findall(docElem,videoPage)[0]
      print 'pat3',pat3
      hashname=re.findall(pat3,videoPage)[0]
      hashname=pat4%hashname
      print 'hashname',hashname
      hashcode=re.findall(hashname,videoPage)[0]
      print mainrtmp, firstarray ,docElem, hashcode
      url=''.join(eval(mainrtmp)).replace('\/','/')+''.join(eval(firstarray)) +docElem+'/'
      hashcode=''.join(eval(hashcode))
      sk=re.findall(pat_sk,videoPage)[0]
      sk_pat='var %s = "(.*?)"'%sk
      jspat='src="(.*jwplayer\.js.*?)"'
      jsurl=re.findall(jspat,videoPage)[0]
      skjs=getUrl(jsurl)
      print sk_pat,skjs
      sk=re.findall(sk_pat,skjs)[0]
      url+=' token=%s playpath=%s live=true timeout=20'%(sk,hashcode) +' swfUrl=http://www.hdcast.info/myplayer/jwplayer.flash.swf flashver=WIN\2021,0,0,182'+' pageUrl='+newurl2
      progress.update( 90, "", "almost done..")
      print url
      
    else:
        #NOT FUNCtional need to call existing functions
        fpat='file:.?.?"(.*?)"'
        spat='streamer:.?.?"(.*?)"'
        pat_sk='securetoken:.?.?"(.*?)"'
        fi=re.findall(fpat,videoPage)[0]
        streamer=re.findall(spat,videoPage)
        if len(streamer)>0: 
            streamer=' playpath='+streamer[0] 
        else:
            streamer=''            
        
        pat_sk=re.findall(pat_sk,videoPage)
        if len(pat_sk)>0: 
            pat_sk=' token='+pat_sk[0] 
        else:
            pat_sk=''            
            
            
        url='%s%s%s pageUrl=%s swfUrl=http://p.jwpcdn.com/6/12/jwplayer.flash.swf'%(fi.split('.flv')[0],streamer,pat_sk,newurl2)+' live=true timeout=20'

    

    playlist = xbmc.PlayList(1)
    #url='rtmp://rtmp.popeoftheplayers.pw:1935/redirect playpath='+url+base64.b64decode('IHN3ZlZmeT10cnVlIHN3ZlVybD1odHRwOi8vcG9wZW9mdGhlcGxheWVycy5wdy9hdGRlZGVhZC5zd2YgZmxhc2hWZXI9V0lOXDIwMTYsMCwwLDIzNSBwYWdlVXJsPWh0dHA6Ly9wb3Blb2Z0aGVwbGF5ZXJzLnB3L2F0ZGVkZWFkLnN3ZiBsaXZlPXRydWUgdGltZW91dD0yMCB0b2tlbj0jYXRkJSMkWkg=')
    

    playlist.clear()
    listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
    playlist.add(url,listitem)
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(playlist) 

##not in use        
def PlayPopeLive(url):
    playlist = xbmc.PlayList(1)
    #url='rtmp://rtmp.popeoftheplayers.pw:1935/redirect playpath='+url+base64.b64decode('IHN3ZlZmeT10cnVlIHN3ZlVybD1odHRwOi8vcG9wZW9mdGhlcGxheWVycy5wdy9hdGRlZGVhZC5zd2YgZmxhc2hWZXI9V0lOXDIwMTYsMCwwLDIzNSBwYWdlVXJsPWh0dHA6Ly9wb3Blb2Z0aGVwbGF5ZXJzLnB3L2F0ZGVkZWFkLnN3ZiBsaXZlPXRydWUgdGltZW91dD0yMCB0b2tlbj0jYXRkJSMkWkg=')
    url='rtmp://rtmp.popeoftheplayers.eu:1935/redirect playpath='+url+base64.b64decode(' swfVfy=true swfUrl=http://popeoftheplayers.eu/atdedead.swf flashVer=WIN\2016,0,0,235 pageUrl=http://popeoftheplayers.eu/atdedead.swf live=true timeout=20 token=#atd%#$ZH')

    playlist.clear()
    listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
    playlist.add(url,listitem)
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(playlist) 

    
def GetSSSEvents(url):
    try:
        url=base64.b64decode('aHR0cDovL3d3dy5zdXBlcnNwb3J0LmNvbS9saXZlLXZpZGVv')
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36')
        req.add_header('Cookie', 'User_IsMobile=False; supersportcookie=country=ZA&countryName=South Africa;')
        response = urllib2.urlopen(req)
        videoPage =  response.read()
        response.close()
        pat='setallLiveStreamsVideos\\(...({.*?})\\\\\"\\"\\);'
#        print videoPage
        channels_string=re.findall(pat,videoPage)[0]
        channels_string=channels_string.replace('\\\\r','')
        channels_string=channels_string=channels_string.replace('\\\\n','')
        channels_string=channels_string.replace('\\\\','\\')
        channels_string=channels_string.replace('\\"','"')
        channels_string=channels_string.replace('\\"','"')
#        print channels_string
        
#        print 'channels_string',channels_string
        channels = json.loads(channels_string)
        print channels

        
#            sid=series["Id"]
        addDir('Maxbitrate Settings' ,'Live' ,6,'',isItFolder=False)
  
        if 1==2:
            addDir(Colored('Live Events[NOT WORKING]','EB',True) ,'' ,-1,'', False, True,isItFolder=False)		#name,url,mode,icon   
            try:
                for channel in channels["EventLiveStreamNow"]:
                    if channel["IsLiveNow"]:
                        ptitle=channel["Title"]
                        cname=channel["Channel"]
                        link=channel["Link"]

            #            addDir(cname ,'a',27,'', False, True,isItFolder=False)
                        addDir('  '+cname + ' ' + ptitle ,link,35,'', False, False,isItFolder=False)
            except: traceback.print_exc(file=sys.stdout)

        addDir(Colored('Channels','EB',True) ,'' ,-1,'', False, True,isItFolder=False)		#name,url,mode,icon   
        try:
            for channel in channels["ChannelStream"]:

                ptitle=channel["NowPlaying"]["EventNowPlaying"]
                cname=channel["NowPlaying"]["Channel"]
                link=channel["NowPlaying"]["Link"]
#                print ptitle, cname,link
                if not link is None:
                    if ptitle is None: ptitle=''
        #            addDir(cname ,'a',27,'', False, True,isItFolder=False)
                    addDir(u'  '+cname + u' ' + ptitle ,link,35,'', False, False,isItFolder=False)
                                                                        

        except: traceback.print_exc(file=sys.stdout)
        
    except: traceback.print_exc(file=sys.stdout)
 

def getPV2Cats():
    ret=[]
    try:
        xmldata=getPV2Url()
        sources=etree.fromstring(xmldata)
        #print xmldata
        for source in sources.findall('items'):#Cricket#
            if not source.findtext('programCategory') in ret :
                    ret.append(source.findtext('programCategory'))   
        if len(ret)>0:
            ret=sorted(ret,key=lambda s: s[0].lower()   )
    except:
        traceback.print_exc(file=sys.stdout)
    return ret  

    
def AddPv2Sports(url):
    xmldata=getPV2Url()
    sources=etree.fromstring(xmldata)
    ret=[]
    isMovies=False
    colors=['blue']
    if 'zemmovies'== url:
        url='latest movies,indian movies,english movies'.split(',')
        colors=['blue','red','green']
        isMovies=True
    elif 'zemsports'== url:
        addDir(Colored('>>Click here for All Categories<<'.capitalize(),'red') ,"pv2",66 ,'', False, True,isItFolder=True)
        url=['sports']
    else:
        url=[url]
    res=[]
    for source in sources.findall('items'):
        if source.findtext('programCategory').lower() in url or source.findtext('programCategory') in url:
            cname=source.findtext('programTitle')
            cid=source.findtext('programURL')
            cimage=source.findtext('programImage')
            seq=cname
            if isMovies:
                seq=str(url.index(source.findtext('programCategory').lower()))
            ret.append((cname ,seq, cid ,cimage))   
                
        
    if len(ret)>0:
        ret=sorted(ret,key=lambda s: s[1].lower()   )

    seq=""
    prevseq="n"

    col=colors[0]
    for r in ret:
        seq=r[1]        
        if seq.isdigit() and prevseq<>seq:
            col=colors[int(seq)]
            addDir(Colored(url[int(seq)].capitalize(),col),'',37,'', False, True,isItFolder=True)            
        prevseq=seq    
        addDir (Colored(r[0].capitalize(),col) ,base64.b64encode(r[2]),37,r[3], False, True,isItFolder=False)
            
def AddPakTVSports(url=None):

    if url=="sss":
        cats=['CTG Stadium','T20 World Cup','Live Cricket','Ptv Sports','PSL','Pak VS NZ','IND VS AUS','ENG VS SA','India Sports','World Sports','Football Clubs','Pak Sports','Cricket','Footbal','Golf','Wrestling & Boxing','T20 Big Bash League']
        isSports=True
        addDir(Colored('>>Click here for All Categories<<'.capitalize(),'red') ,"paktv",66 ,'', False, True,isItFolder=True)
    else:
        cats=[url]
        isSports=False
        
    for cname,ctype,curl,imgurl in getPakTVChannels(cats,isSports):
        cname=cname.encode('ascii', 'ignore').decode('ascii')
        if ctype=='manual2':
            mm=37
        elif ctype=='manual3':
            mm=45
        else:
            mm=11
        addDir(Colored(cname.capitalize(),'ZM') ,base64.b64encode(curl) ,mm ,imgurl, False, True,isItFolder=False)		#name,url,mode,icon
    return    
                   
def AddPTCSports(url=None):
    if url=="sss":
        isSports=True
        cats=['PSL','IPL','Ptv Sports','Star Sports','Sports','BPL T20','Live Cricket','Live Footbal','Ten Sports','BT Sports','Euro Sports']
        addDir(Colored('>>Click here for All Categories<<'.capitalize(),'red') ,"ptc",66 ,'', False, True,isItFolder=True)
    else:
        cats=[url]
        isSports=False
    for cname,ctype,curl,imgurl in getptcchannels(cats,isSports):
        cname=cname.encode('ascii', 'ignore').decode('ascii')
        if ctype=='manual2':
            mm=37
        elif ctype=='manual3':
            mm=45
        else:
            mm=11
        addDir(Colored(cname.capitalize(),'ZM') ,base64.b64encode(curl) ,mm ,imgurl, False, True,isItFolder=False)		#name,url,mode,icon
    return    
    
def total_seconds(dt):
    # Keep backward compatibility with Python 2.6 which doesn't have
    # this method
    import datetime
    if hasattr(datetime, 'total_seconds'):
        return dt.total_seconds()
    else:
        return (dt.microseconds + (dt.seconds + dt.days * 24 * 3600) * 10**6) / 10**6
        
def getutfoffset():
    import time
    from datetime import datetime

    ts = time.time()
    utc_offset = total_seconds((   datetime.fromtimestamp(ts)-datetime.utcfromtimestamp(ts)))/60
              
    return int(utc_offset)


def unwise_func( w, i, s, e):
    lIll = 0;
    ll1I = 0;
    Il1l = 0;
    ll1l = [];
    l1lI = [];
    while True:
        if (lIll < 5):
            l1lI.append(w[lIll])
        elif (lIll < len(w)):
            ll1l.append(w[lIll]);
        lIll+=1;
        if (ll1I < 5):
            l1lI.append(i[ll1I])
        elif (ll1I < len(i)):
            ll1l.append(i[ll1I])
        ll1I+=1;
        if (Il1l < 5):
            l1lI.append(s[Il1l])
        elif (Il1l < len(s)):
            ll1l.append(s[Il1l]);
        Il1l+=1;
        if (len(w) + len(i) + len(s) + len(e) == len(ll1l) + len(l1lI) + len(e)):
            break;

    lI1l = ''.join(ll1l)#.join('');
    I1lI = ''.join(l1lI)#.join('');
    ll1I = 0;
    l1ll = [];
    for lIll in range(0,len(ll1l),2):
        #print 'array i',lIll,len(ll1l)
        ll11 = -1;
        if ( ord(I1lI[ll1I]) % 2):
            ll11 = 1;
        #print 'val is ', lI1l[lIll: lIll+2]
        l1ll.append(chr(    int(lI1l[lIll: lIll+2], 36) - ll11));
        ll1I+=1;
        if (ll1I >= len(l1lI)):
            ll1I = 0;
    ret=''.join(l1ll)
    if 'eval(function(w,i,s,e)' in ret:
#        print 'STILL GOing'
        ret=re.compile('eval\(function\(w,i,s,e\).*}\((.*?)\)').findall(ret)[0]
        return get_unwise(ret)
    else:
#        print 'FINISHED'
        return ret
def get_unwise( str_eval):
    page_value=""
    try:
        ss="w,i,s,e=("+str_eval+')'
        exec (ss)
        page_value=unwise_func(w,i,s,e)
    except: traceback.print_exc(file=sys.stdout)
    #print 'unpacked',page_value
    return page_value    
    
    
def AddSports365Channels(url=None):
    errored=True
    try:
        import live365
        
        addDir(Colored("All times in local timezone.",'red') ,"" ,0,"", False, True,isItFolder=False)		#name,url,mode,icon
        videos=live365.getLinks()
        for nm,link,active in videos:
            if active:
               
                addDir(Colored(nm  ,'ZM') ,link,11 ,"",isItFolder=False)
            else:
                addDir("[N/A]"+Colored(nm ,'blue') ,"",0 ,"",isItFolder=False)
            errored=False
    except: traceback.print_exc(file=sys.stdout)
    if errored:
       if RefreshResources([('live365.py','https://raw.githubusercontent.com/Shani-08/ShaniXBMCWork2/master/plugin.video.ZemTV-shani/live365.py')]):
            dialog = xbmcgui.Dialog()
            ok = dialog.ok('XBMC', 'No Links, so updated files dyamically, try again, just in case!')           
            print 'Updated files'
        
        
def RefreshResources(resources):
#	print Fromurl
    pDialog = xbmcgui.DialogProgress()
    ret = pDialog.create('XBMC', 'checking Updates...')
    totalFile=len(resources)
    fileno=0
    import hashlib
    updated=False
    try:
        for rfile in resources:
            if pDialog.iscanceled(): return
            progr = (fileno*80)/totalFile
            fname = rfile[0]
            fileToDownload = rfile[1]
            fileHash=hashlib.md5(fileToDownload+addonversion).hexdigest()
            lastFileTime=selfAddon.getSetting( "Etagid"+fileHash)  
            if lastFileTime=="": lastFileTime=None
            resCode=200
            #print fileToDownload
            eTag=None        
            try:
                req = urllib2.Request(fileToDownload)
                req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')

                if lastFileTime:
                    req.add_header('If-None-Match',lastFileTime)
                response = urllib2.urlopen(req)
                resCode=response.getcode()
                if resCode<>304:
                    try:
                        eTag=response.info().getheader('Etag')
                    except: pass
                    data=response.read()
            except Exception as e: 
                s = str(e)
                if 'Not Modified'.lower() in s.lower(): resCode=304
                data=''
            if ('Exec format error: exec' in data or 'A file permissions error has occurred' in data) and 'xbmcplugin' not in data:
                data=''

            if len(data)>0:
                with open(os.path.join(addonPath, fname), "wb") as filewriter:
                    filewriter.write(data)
                    updated=True
                    if eTag:
                        selfAddon.setSetting( id="Etagid"+fileHash ,value=eTag)    
                pDialog.update(20+progr, 'imported ...'+fname)
            elif resCode==304:
                pDialog.update(20+progr, 'No Change.. skipping.'+fname)
            else:            
                pDialog.update(20+progr, 'Failed..zero byte.'+fname)
            fileno+=1
    except: pass
    pDialog.close()
    return updated


def PlayUKTVNowChannels(url):
    jsondata=getUKTVPage()
    cc=[item for item in jsondata["msg"]["channels"]
            if item["pk_id"]== url]
            
    
    listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
    played=False
    ##DO YOU WANT ME TO STOP? lol
    try:
        import uktvplayer
        played=uktvplayer.play(listitem,cc)
            
    except: pass
    if not played:
        if RefreshResources([('uktvplayer.py','https://raw.githubusercontent.com/Shani-08/ShaniXBMCWork2/master/plugin.video.ZemTV-shani/uktvplayer.py')]):
            dialog = xbmcgui.Dialog()
            ok = dialog.ok('XBMC', 'Updated files dyamically, try again, just in case!')           
            print 'Updated files'
    return  

def getYuppSportsChannel(Live=True):
    ret=[]
    try:
        url="http://asiacup.api.yuppcdn.net/yuppcache.svc/asiacupdetails"
        post={'type':'2016'}
        if Live:
            post={'type':'live'}

        headers=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'),
                ('Referer','http://www.yupptv.com/cricket/asiacup.html')]

        post = urllib.urlencode(post)
        
        jdata=getUrl(url, post=post, headers=headers)
        jsondata=json.loads(jdata)
        for channel in jsondata["VODS"]:
            cname=channel["Description"]
            curl='direct:'+channel["URLpath"]
            cimage=channel["Imgpath"]
            
            ret.append((cname ,'manual', curl ,cimage))  
    except:
        traceback.print_exc(file=sys.stdout)
    return ret

def AddYuppSports(url=None):
    try:

        addDir(Colored("Live Streams".capitalize(),'ZM') ,"" ,-1,"", False, True,isItFolder=False)		#name,url,mode,icon
        channels=getYuppSportsChannel(Live=True)
        if len(channels)>0:
            for cname,ctype,curl,imgurl in channels:
                cname=cname.encode('ascii', 'ignore').decode('ascii')
                mm=11
        #        print repr(curl)      
                addDir(cname ,base64.b64encode(curl) ,mm ,imgurl, False, True,isItFolder=False)		#name,url,mode,icon
        else:
            addDir("-- No Live Streams Available" ,"" ,-1 ,imgurl, False, True,isItFolder=False)		#name,url,mode,icon
    except: pass
    try:

        addDir(Colored("Recorded/Highlights".capitalize(),'ZM') ,"" ,-1,"", False, True,isItFolder=False)		#name,url,mode,icon
        channels=getYuppSportsChannel(Live=False)
        if len(channels)>0:
            for cname,ctype,curl,imgurl in channels:
                cname=cname.encode('ascii', 'ignore').decode('ascii')
                mm=11
        #        print repr(curl)      
                addDir(cname ,base64.b64encode(curl) ,mm ,imgurl, False, True,isItFolder=False)		#name,url,mode,icon
        else:
            addDir("-- No Recorded Streams Available" ,"" ,-1 ,imgurl, False, True,isItFolder=False)		#name,url,mode,icon
    except: pass
                
        
        
    return   
def AddMonaChannels(url=None):
    cats=[]
    if url=="sss":
        cats='14'
        addDir(Colored('>>Click here for All Categories<<'.capitalize(),'red') ,"mona",66 ,'', False, True,isItFolder=True)

    else:
        cats=url
    for cname,ctype,curl,imgurl in getMonaChannels(cats):
        #cname=cname.encode('ascii', 'ignore').decode('ascii')
        mm=11
#        print repr(curl)
       
        #addDir(Colored(cname.capitalize(),'ZM') ,base64.b64encode(curl) ,mm ,imgurl, False, True,isItFolder=False)		#name,url,mode,icon
        addDir(cname.encode("utf-8") ,base64.b64encode(curl) ,mm ,imgurl, False, True,isItFolder=False)		#name,url,mode,icon
    return   
    
def AddUKTVNowChannels(url=None):
    cats=[]
    if url=="sss":
        cats=['sports']
        addDir(Colored('>>Click here for All Categories<<'.capitalize(),'red') ,"uktv",66 ,'', False, True,isItFolder=True)

    else:
        cats=[url]
    for cname,ctype,curl,imgurl in getUKTVChannels(cats):
        cname=cname.encode('ascii', 'ignore').decode('ascii')
        mm=11
#        print repr(curl)
       
        addDir(Colored(cname.capitalize(),'ZM') ,base64.b64encode(curl) ,mm ,imgurl, False, True,isItFolder=False)		#name,url,mode,icon
    return   

def AddIpBoxSources(url=None):
    for cname,curl in getIpBoxSources():
        try:
            #print cname
            cname=cname#cname.encode('ascii', 'ignore').decode('ascii')
           
            addDir(Colored(cname.capitalize(),'ZM') ,curl ,61 ,"", False, True,isItFolder=True)		#name,url,mode,icon
        except: traceback.print_exc(file=sys.stdout) 
    return
    
def AddIpBoxChannels(url=None):
    if not mode==67:
        addDir(Colored('>>Click Here for All Channels<<'.capitalize(),'red') ,url ,67 ,"", False, True,isItFolder=True)		#name,url,mode,icon

    for cname,ctype,curl,imgurl in getIpBoxChannels([url],True):
        try:
            #print cname
            cname=cname#cname.encode('ascii', 'ignore').decode('ascii')
            mm=11
    #        print repr(curl)
           
            addDir(Colored(cname.capitalize(),'ZM') ,base64.b64encode(curl) ,mm ,imgurl, False, True,isItFolder=False)		#name,url,mode,icon
        except: traceback.print_exc(file=sys.stdout) 
    return     
    
def AddWTVSports(url=None):

    if url=="sss":
        cats=['Extra Time Football','TSN','Cth Stadium','UFC','T20 World Cup','Horse Racing','Cricket','Footbal','Golf','Wrestling & Boxing','T20 Big Bash League','NFL Live','Footbal Clubs','Sports Time']
        isSports=True
        addDir(Colored('>>Click here for All Categories<<'.capitalize(),'red') ,"wtv",66 ,'', False, True,isItFolder=True)
    else:
        cats=[url]
        isSports=False

    for cname,ctype,curl,imgurl in getWTVChannels(cats,isSports):
        cname=cname.encode('ascii', 'ignore').decode('ascii')
        if ctype=='manual2':
            mm=37
        elif ctype=='manual3':
            mm=45
        else:
            mm=11
        addDir(Colored(cname.capitalize(),'ZM') ,base64.b64encode(curl) ,mm ,imgurl, False, True,isItFolder=False)		#name,url,mode,icon
    return      
    
def AddGTVSports(url=None):

    if url=="sss":
        cats=['Asto Sports','TSN Sports','OSN Sports','Sports Time TV','T20 World Cup','Horse Racing','Cricket Matches','Footbal','Golf','Boxing & Fight','T20 Big Bash League','NFL Live','Footbal Clubs','Sports HD','Sports Full HD','Global Sports']
        isSports=True
        addDir(Colored('>>Click here for All Categories<<'.capitalize(),'red') ,"gtv",66 ,'', False, True,isItFolder=True)
    else:
        cats=[url]
        isSports=False

    for cname,ctype,curl,imgurl in getGTVChannels(cats,isSports):
        cname=cname.encode('ascii', 'ignore').decode('ascii')
        if ctype=='manual2':
            mm=37
        elif ctype=='manual3':
            mm=45
        else:
            mm=11
        addDir(Colored(cname.capitalize(),'ZM') ,base64.b64encode(curl) ,mm ,imgurl, False, True,isItFolder=False)		#name,url,mode,icon
    return      
    
def AddPITVSports(url=None):

    if url=="sss":
        cats=['Barclays Premier League', 'CTH Stadium', 'Football', 'Football Clubs', 'Golf', 'Geo Super', 'Indian Premier League 9', 'Live Cricket', 'Netball Super League', 'National Badminton League',  'Pakistan Cup', 'PTV Sports', 'Premier League Darts', 'Racing', 'Rugby Union & League', 'World Sports', 'Wrestling & Boxing', 'World Seniors Snooker']
        isSports=True
        addDir(Colored('>>Click here for All Categories<<'.capitalize(),'red') ,"pitv",66 ,'', False, True,isItFolder=True)
    else:
        cats=[url]
        isSports=False

    for cname,ctype,curl,imgurl in getPITVChannels(cats,isSports):
        cname=cname.encode('ascii', 'ignore').decode('ascii')
        if ctype=='manual2':
            mm=37
        elif ctype=='manual3':
            mm=45
        else:
            mm=11
        addDir(Colored(cname.capitalize(),'ZM') ,base64.b64encode(curl) ,mm ,imgurl, False, True,isItFolder=False)		#name,url,mode,icon
    return  
    
def AddUniTVSports(url=None):   

    if url=="sss":
        cats=['Extra Time','TSN','Cth Stadium','UFC','T20 World Cup','Horse Racing','Cricket','Footbal','Sports','Golf','Boxing & Wrestling','T20 Big Bash League','NFL Live','Footbal Clubs','Sports Time']
        isSports=True
        addDir(Colored('>>Click here for All Categories<<'.capitalize(),'red') ,"unitv",66 ,'', False, True,isItFolder=True)
    else:
        cats=[url]
        isSports=False
    for cname,ctype,curl,imgurl in getUniTVChannels(cats,isSports):
        cname=cname.encode('ascii', 'ignore').decode('ascii')
        if ctype=='manual2':
            mm=37
        elif ctype=='manual3':
            mm=45
        else:
            mm=11
        addDir(Colored(cname.capitalize(),'ZM') ,base64.b64encode(curl) ,mm ,imgurl, False, True,isItFolder=False)		#name,url,mode,icon
    return        
    
def ShowAllCategories(url):
    cats=[]
    cmode=0
    if url=="unitv":
        cats=getUniTVCats()
        cmode=53
    elif url=="wtv":
        cats=getWTVCats()
        cmode=62
    elif url=="paktv":
        cats=getPakTVCats()
        cmode=52    
    elif url=="uktv":
        cats=getUKTVCats()
        cmode=57    
    elif url=="pv2":
        cats=getPV2Cats()
        cmode=36
    elif url=="mona":
        cats=getMonaCats()
        cmode=68
    elif url=="ptc":
        cats=getPTCCats()
        cmode=51   
    elif url=="gtv":
        cats=getGTVCats()
        cmode=70
    elif url=="pitv":
        cats=getPITVCats()
        cmode=71
    for cname in cats:
        print cname
        if type(cname).__name__ == 'tuple':
            cid,cname=cname
            cname=cname.encode("utf-8")
        else:
            cid=cname
        addDir(Colored(cname.capitalize(),'red') ,cid,cmode,'', False, True,isItFolder=True)
        

    
def AddStreamSports(url=None):
    jsondata=getUrl('http://videostream.dn.ua/list/GetLeftMenuShort?lng=en')
    sources= json.loads(jsondata)
    ret=[]
    addDir('Refresh' ,'Live' ,39,'')
    for source in sources["Value"]:
        cname=Colored(source["Sport"] ,'EB')
        #print 'source["VI"]',source["VI"],cname
        if not "cyber" in cname.lower() and not 'xgame' in source["VI"]:
            if "Opp1" in source and not source["Opp1"].encode('ascii','ignore')=="":
                cname+=" :" + source["Opp1"].encode('ascii','ignore') + " vs " +source["Opp2"].encode('ascii','ignore') 
            else:
                cname+=" :" + source["Liga"].encode('ascii','ignore')
            cid=source["VI"]
            addDir(cname ,base64.b64encode(cid),40,'', False, True,isItFolder=False)            

            
def AddCricHD(url):
    try:
        url="http://www.hdcric.com/other-sports-live-streaming"
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36')
        response = urllib2.urlopen(req)
        videoPage =  response.read()
        response.close()
        #pat='<li class="has-sub"><a href="(.*?)".*icon (.*?)"'
        #channels=re.findall(pat,videoPage)
        #for channel in channels:
#       #     print channel
        #    cname=channel[2]
        #    cid=channel[0]
        #    cimg=channel[1]
        #    
        #    if not cid.startswith('http'):cid=url+cid
        #    if not cimg.startswith('http'):cimg=url+cimg###

#            addDir(cname ,'a',27,'', False, True,isItFolder=False)
#            print 'adding'
#            addDir(cname ,cid,27,cimg, False, True,isItFolder=False)

        pat='<li class="has-sub"><a href="(.*?)".*icon (.*?)"'
        channels=re.findall(pat,videoPage)
        for channel in channels:
#            print channel
            cname=channel[1]
            cid=channel[0]
            cimg=""#;channel[2]
            
            if not cid.startswith('http'):cid=url+cid
            if not cimg.startswith('http'):cimg=url+cimg

#            addDir(cname ,'a',27,'', False, True,isItFolder=False)
#            print 'adding'
            addDir(cname.capitalize() ,cid,27,cimg, False, True,isItFolder=False)
            


    except: traceback.print_exc(file=sys.stdout)
    


    
def AddWillSportsOldSeries(url):
    try:
        url_host=base64.b64decode('aHR0cDovL3dpbGxvd2ZlZWRzLndpbGxvdy50di93aWxsb3dNYXRjaEFyY2hpdmUuanNvbg==')
        req = urllib2.Request(url_host)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36')
        response = urllib2.urlopen(req)
        if response.info().get('Content-Encoding') == 'gzip':
            from StringIO import StringIO
            import gzip
            buf = StringIO( response.read())
            f = gzip.GzipFile(fileobj=buf)
            res = f.read()
        else:
            res=response.read()

#        print repr(res[:100])
        res=res.split('Handle_WLSeriesDetailsObj(')[1][:-2]
        serieses = json.loads(res)
  
        response.close()

        
        for series in serieses:
            sname=series["Name"]
            sid=series["Id"]
            addDir(sname ,sid,24,'')		#name,url,mode,icon
    except: traceback.print_exc(file=sys.stdout)


def AddWillSportsOldSeriesMatches(url):
    addDir(Colored(name,'EB',True) ,'' ,-1,'', False, True,isItFolder=False)		#name,url,mode,icon
    try:
        url_host=base64.b64decode('aHR0cDovL3dpbGxvd2ZlZWRzLndpbGxvdy50di93aWxsb3dNYXRjaEFyY2hpdmUuanNvbg==')
        req = urllib2.Request(url_host)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36')
        response = urllib2.urlopen(req)
        if response.info().get('Content-Encoding') == 'gzip':
            from StringIO import StringIO
            import gzip
            buf = StringIO( response.read())
            f = gzip.GzipFile(fileobj=buf)
            res = f.read()
        else:
            res=response.read()

#        print repr(res[:100])
        res=res.split('Handle_WLSeriesDetailsObj(')[1][:-2]
        serieses = json.loads(res)
  
        response.close()

        
        for series in serieses:
            sname=series["Name"]
            sid=series["Id"]
            if url==sid:
                for match in series["MatchDetails"]:
                    mname=match["Name"]
                    matchid=match["Id"]
                    sdate=match["StartDate"]
                    addDir(sdate+' - '+mname ,matchid,23,'')		#name,url,mode,icon
    except: traceback.print_exc(file=sys.stdout)

def useMyOwnUserNamePwd():
    willow_username=selfAddon.getSetting( "WillowUserName" ) 
    return not willow_username==""
    
def get365CookieJar(updatedUName=False):
    cookieJar=None
    try:
        cookieJar = cookielib.LWPCookieJar()
        if not updatedUName:
            cookieJar.load(S365COOKIEFILE,ignore_discard=True)
    except: 
        cookieJar=None

    if not cookieJar:
        cookieJar = cookielib.LWPCookieJar()
    return cookieJar
    
def getZemCookieJar(updatedUName=False):
    cookieJar=None
    try:
        cookieJar = cookielib.LWPCookieJar()
        if not updatedUName:
            cookieJar.load(ZEMCOOKIEFILE,ignore_discard=True)
    except: 
        cookieJar=None

    if not cookieJar:
        cookieJar = cookielib.LWPCookieJar()
    return cookieJar
    
def getWTVCookieJar(updatedUName=False):
    cookieJar=None
    try:
        cookieJar = cookielib.LWPCookieJar()
        if not updatedUName:
            cookieJar.load(WTVCOOKIEFILE,ignore_discard=True)
    except: 
        cookieJar=None

    if not cookieJar:
        cookieJar = cookielib.LWPCookieJar()
    return cookieJar

def performWillowLogin():
    try:

        url=base64.b64decode('aHR0cDovL3d3dy53aWxsb3cudHYvRXZlbnRNZ210L0RlZmF1bHQuYXNw')
        willow_username=selfAddon.getSetting( "WillowUserName" ) 
        willow_pwd=selfAddon.getSetting( "WillowPassword" ) 
        willow_lasstusername=selfAddon.getSetting( "lastSuccessLogin" ) 
        cookieJar=getWTVCookieJar(willow_username!=willow_lasstusername)
        mainpage = getUrl(url,cookieJar=cookieJar)
        

        if 'Login/Register' in mainpage:
            print 'LOGIN NOW'
            url=base64.b64decode('aHR0cHM6Ly93d3cud2lsbG93LnR2L0V2ZW50TWdtdC9Vc2VyTWdtdC9Mb2dpbi5hc3A=')
            headers=[('Referer',"https://www.willow.tv/EventMgmt/UserMgmt/Login.asp"),('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'),('Origin','https://www.willow.tv')]                      
            post = {'Email':willow_username,'Password':willow_pwd,'LoginFormSubmit':'true'}
            post = urllib.urlencode(post)
            mainpage = getUrl(url,cookieJar=cookieJar,post=post,headers=headers )
            cookieJar.save (WTVCOOKIEFILE,ignore_discard=True)
            selfAddon.setSetting( id="lastSuccessLogin" ,value=willow_username)
        
        return not 'Login/Register' in mainpage,cookieJar
    except: 
            traceback.print_exc(file=sys.stdout)
    return False,None

def kodiJsonRequest(params):
    data = json.dumps(params)
    request = xbmc.executeJSONRPC(data)

    try:
        response = json.loads(request)
    except UnicodeDecodeError:
        response = json.loads(request.decode('utf-8', 'ignore'))

    try:
        if 'result' in response:
            return response['result']
        return None
    except KeyError:
        logger.warn("[%s] %s" % (params['method'], response['error']['message']))
        return None


def setKodiProxy(proxysettings=None):

    if proxysettings==None:
        print 'proxy set to nothing'
        xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"network.usehttpproxy", "value":false}, "id":1}')
    else:
        
        ps=proxysettings.split(':')
        proxyURL=ps[0]
        proxyPort=ps[1]
        proxyType=ps[2]
        proxyUsername=None
        proxyPassword=None
         
        if len(ps)>3 and '@' in proxysettings:
            proxyUsername=ps[3]
            proxyPassword=proxysettings.split('@')[-1]

        print 'proxy set to', proxyType, proxyURL,proxyPort
        xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"network.usehttpproxy", "value":true}, "id":1}')
        xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"network.httpproxytype", "value":' + str(proxyType) +'}, "id":1}')
        xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"network.httpproxyserver", "value":"' + str(proxyURL) +'"}, "id":1}')
        xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"network.httpproxyport", "value":' + str(proxyPort) +'}, "id":1}')
        
        
        if not proxyUsername==None:
            xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"network.httpproxyusername", "value":"' + str(proxyUsername) +'"}, "id":1}')
            xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"network.httpproxypassword", "value":"' + str(proxyPassword) +'"}, "id":1}')

        
def getConfiguredProxy():
    proxyActive = kodiJsonRequest({'jsonrpc': '2.0', "method":"Settings.GetSettingValue", "params":{"setting":"network.usehttpproxy"}, 'id': 1})['value']
    print 'proxyActive',proxyActive
    proxyType = kodiJsonRequest({'jsonrpc': '2.0', "method":"Settings.GetSettingValue", "params":{"setting":"network.httpproxytype"}, 'id': 1})['value']

    if proxyActive: # PROXY_HTTP
        proxyURL = kodiJsonRequest({'jsonrpc': '2.0', "method":"Settings.GetSettingValue", "params":{"setting":"network.httpproxyserver"}, 'id': 1})['value']
        proxyPort = unicode(kodiJsonRequest({'jsonrpc': '2.0', "method":"Settings.GetSettingValue", "params":{"setting":"network.httpproxyport"}, 'id': 1})['value'])
        proxyUsername = kodiJsonRequest({'jsonrpc': '2.0', "method":"Settings.GetSettingValue", "params":{"setting":"network.httpproxyusername"}, 'id': 1})['value']
        proxyPassword = kodiJsonRequest({'jsonrpc': '2.0', "method":"Settings.GetSettingValue", "params":{"setting":"network.httpproxypassword"}, 'id': 1})['value']

        if proxyUsername and proxyPassword and proxyURL and proxyPort:
            return proxyURL + ':' + str(proxyPort)+':'+str(proxyType) + ':' + proxyUsername + '@' + proxyPassword
        elif proxyURL and proxyPort:
            return proxyURL + ':' + str(proxyPort)+':'+str(proxyType)
    else:
        return None
        
def playmediawithproxy(media_url, name, iconImage,proxyip,port,progress):

    progress.create('Progress', 'Playing with custom proxy')
    progress.update( 50, "", "setting proxy..", "" )
    proxyset=False
    existing_proxy=''
    try:
        
        existing_proxy=getConfiguredProxy()
        print 'existing_proxy',existing_proxy
        #read and set here
        setKodiProxy( proxyip + ':' + port+':0')
        proxyset=True

        print 'proxy setting complete', getConfiguredProxy()
        
        progress.update( 80, "", "setting proxy complete, now playing", "" )
        progress.close()
        progress=None
        import  CustomPlayer
        player = CustomPlayer.MyXBMCPlayer()
        listitem = xbmcgui.ListItem( label = str(name), iconImage = iconImage, thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ), path=media_url )
        player.play( media_url,listitem)
        xbmc.sleep(1000)
        while player.is_active:
            xbmc.sleep(200)
    except:
        traceback.print_exc()
    if progress:
        progress.close()
    if proxyset:
        print 'now resetting the proxy back'
        setKodiProxy(existing_proxy)
        print 'reset here'
    return ''
    
def getwillow247(matchid,CJ):

    progress = xbmcgui.DialogProgress()
    progress.create('Progress', 'Willow 24x7')
    progress.update( 10, "", "Getting Urls..")
    
    liveUrl=base64.b64decode('aHR0cDovL20ud2lsbG93LnR2L2dldFN0cmVhbWluZ1VSTFMuYXNwP21pZD05OTk5OTk=')
    pat='"URL":"(.*?)"'
    headers=[('Referer',base64.b64decode('aHR0cDovL20ud2lsbG93LnR2L2lPU0hvbWUuYXNw')),('User-Agent','Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/11B554a')]
    htm=getUrl(liveUrl,cookieJar=CJ,headers=headers) 
    if 'Failure-Region' in htm:
        progress.update( 30, "", "Not in US? Using proxy" )

        proxyserver=selfAddon.getSetting('WillowProxy')
        proxyport=selfAddon.getSetting('WillowPort')
        ##use US proxy and play with it
        cookie_handler = urllib2.HTTPCookieProcessor(CJ)
        opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler(),urllib2.ProxyHandler({ 'http'  : '%s:%s'%(proxyserver,proxyport)}))
        req = urllib2.Request(liveUrl)
        req.add_header('User-Agent','Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/11B554a')
        req.add_header('Referer',base64.b64decode('aHR0cDovL20ud2lsbG93LnR2L2lPU0hvbWUuYXNw'))
        response = opener.open(req,timeout=20)
        link=response.read()
        response.close()
#        print link
        progress.update( 30, "", "Got the Link, Now playing with Using proxy" )
        final_url=re.findall(pat,link)[0]
        playmediawithproxy(final_url,'24x7 willow','',proxyserver,proxyport,progress)
        return ''
    else:
        progress.close()
        final_url=re.findall(pat,htm)[0]
        return final_url
    
def getMatchUrl(matchid):
    if not useMyOwnUserNamePwd():
        url_host=willowCommonUrl
        if len(url_host)>0:
            if mode==21:#live
                if ':' in matchid:
                    matchid,partNumber=matchid.split(':')
                    post = {'matchNumber':matchid,'type':'live','partNumber':partNumber,'debug':'1'}
                else:
                    post = {'matchNumber':matchid,'type':'live','debug':'1'}
            else:
                if ':' in matchid:
                    matchid,partNumber=matchid.split(':')
                    post = {'matchNumber':matchid,'type':'replay','partNumber':partNumber,'debug':'1'}
                else:
                    post = {'matchNumber':matchid,'type':'replay','debug':'1'}
            post = urllib.urlencode(post)
            req = urllib2.Request(url_host)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36')
            response = urllib2.urlopen(req,post)
            link=response.read()
            response.close()
            final_url= urllib2.unquote(link)  
            final_url=final_url.split('debug')[0]
            return final_url
        else:
            Msg="Common server is not available, Please enter your own login details."
            dialog = xbmcgui.Dialog()
            ok = dialog.ok('Login Failed', Msg)
            return ''

    else:
        loginworked,cookieJar= performWillowLogin();
        if loginworked:
            WLlive=False
            source_sectionid=''
            returnParts=False
            userid=''
            if matchid == '999999':
                return getwillow247(matchid,cookieJar)
            for i in cookieJar:

                s=repr(i)
                if 'CXMUserId' in s:
                    #print 'ssssssssssssss',s
                    userid=s.split('value=\'')[1].split('%')[0]
#            print 'userid',userid
            calltype='Live'
            if mode==21:
                WLlive=True
#                print 'matchid',matchid
                matchid,source_sectionid=matchid.split(':')
                st='LiveMatch'
                url=base64.b64decode('aHR0cDovL3d3dy53aWxsb3cudHYvRXZlbnRNZ210LyVzVVJMLmFzcD9taWQ9JXM=')%(st,matchid)
                pat='secureurl":"(.*?)".*?priority":%s,'%source_sectionid    
                calltype='Live'                
            else:
                if ':' in matchid:
                    matchid,source_sectionid=matchid.split(':')
                    st='Replay'
                    url=base64.b64decode('aHR0cHM6Ly93d3cud2lsbG93LnR2L0V2ZW50TWdtdC9SZXBsYXlVUkwuYXNwP21pZD0lcyZ1c2VySWQ9JXM=')%(matchid,userid)
                    pat='secureurl":"(.*?)".*?priority":%s,'%source_sectionid    
                    calltype='RecordOne'     
                else:
                    returnParts=True
                    st='Replay'
                    url=base64.b64decode('aHR0cHM6Ly93d3cud2lsbG93LnR2L0V2ZW50TWdtdC9SZXBsYXlVUkwuYXNwP21pZD0lcyZ1c2VySWQ9JXM=')%(matchid,userid)
                    pat='"priority":(.+?),"title":"(.*?)",'
                    calltype='RecordAll' 
            
            videoPage = getUrl(url,cookieJar=cookieJar)    

            final_url=''
        
#            print 'calltype',calltype,mode
#            print videoPage
#            print pat
            if calltype=='Live' or calltype=='RecordOne':
                videoPage='},\n{'.join(videoPage.split("},{"))
                final_url=re.findall(pat,videoPage)[0]
            else:
                final_url=re.findall(pat,videoPage)
                final_url2=''
                for u in final_url:
                    final_url2+='#'+str(u[0]) +' ' +u[1].replace(',','')+'='+u[0]+','
                final_url=final_url2[:-1]
  
            final_url= urllib2.unquote(final_url)  
            final_url=final_url.split('debug')[0]
            return final_url
            

        else:
            Msg="Login failed, please make sure the login details are correct."
            dialog = xbmcgui.Dialog()
            ok = dialog.ok('Login Failed', Msg)
        
def PlaySSSEvent(url):

    if 1==2:
        murl=base64.b64decode('aHR0cDovL3d3dy5zdXBlcnNwb3J0LmNvbS92aWRlby9wbGF5ZXJsaXZlanNvbi5hc3B4P3ZpZD0lcw==')
        matchid=url.split('/')[-1]
        match_url=murl%matchid
        match_json=getUrl(match_url)
        match=json.loads(match_json)
        matchurl=match['result']['services']['videoURL']
       
     
        matchurl="bcb10ea0b620b447dc8ed8afe9bea186c54bf0a31ad3e7f46e3436c08dbf57165e0f3f9b4099ba0f648d8742acefbc0c57d191e247457bc3c0697b5dd40f028f4e003da617fa4e6c3ddbe0d17ff981db"
        finalUrl=getdecSSMatchUrl(matchurl,'LIVE')
        print 'dec',finalUrl
       
#    print 'aaaaaaaaaaaaaaaaaaaa',name.strip()
    sts=["118c8a71c0dee1a743fbf8808e440397f26c2cea1c9bf351fb0b3c5417a8af9e07a2d8150dcf66b67f1690b03fa2885d7777a6f0253453dd1738fb7693d13f2a80f3c268fdcb5d69230f24f74af7bbbe",
        "bcb10ea0b620b447dc8ed8afe9bea186c54bf0a31ad3e7f46e3436c08dbf571652ffd197868c8ba23f74f8c6ed24d02157d191e247457bc3c0697b5dd40f028f4e003da617fa4e6c3ddbe0d17ff981db",
        "bcb10ea0b620b447dc8ed8afe9bea186c54bf0a31ad3e7f46e3436c08dbf5716dff663f438bc70808e422cef4c665cd357d191e247457bc3c0697b5dd40f028f4e003da617fa4e6c3ddbe0d17ff981db",
        "bcb10ea0b620b447dc8ed8afe9bea186c54bf0a31ad3e7f46e3436c08dbf57164b74e2107bd1b84b155d86c84b10113057d191e247457bc3c0697b5dd40f028f4e003da617fa4e6c3ddbe0d17ff981db",
        "bcb10ea0b620b447dc8ed8afe9bea186c54bf0a31ad3e7f46e3436c08dbf57169962732038b02c08b062a3391c1f13c057d191e247457bc3c0697b5dd40f028f4e003da617fa4e6c3ddbe0d17ff981db",
        "bcb10ea0b620b447dc8ed8afe9bea186c54bf0a31ad3e7f46e3436c08dbf571647dec4b1fa9327a801c77533ca16482d57d191e247457bc3c0697b5dd40f028f4e003da617fa4e6c3ddbe0d17ff981db",
        "bcb10ea0b620b447dc8ed8afe9bea186c54bf0a31ad3e7f46e3436c08dbf5716b55f6d0d5802a828a606fb76fa2c0d7757d191e247457bc3c0697b5dd40f028f4e003da617fa4e6c3ddbe0d17ff981db"]
    blitz="bcb10ea0b620b447dc8ed8afe9bea186c54bf0a31ad3e7f46e3436c08dbf57165b1423947b96824d87141cfa88e02f0f57d191e247457bc3c0697b5dd40f028f4e003da617fa4e6c3ddbe0d17ff981db"
    n=0
    finalUrl=""
    if name.strip().startswith('SS') and  "blitz" not  in name.lower():
       nm= int(name.strip().split(' ')[0].replace('SS',''))-1
       finalUrl=sts[nm]
    else:
        finalUrl=blitz
        
    finalUrl=getdecSSMatchUrl(finalUrl,'LIVE')
    print finalUrl
    #SS2_1@27052#
    if '.f4m' in finalUrl:
        maxbitrate='0'
        maxbitrate_settings=selfAddon.getSetting('defualtSSSBitRate')
        if (not maxbitrate_settings=='') and 'Max' not in maxbitrate_settings:
            maxbitrate=maxbitrate_settings
        finalUrl='plugin://plugin.video.f4mTester/?url=%s&maxbitrate=%s&name=%s&swf=%s'%(urllib.quote_plus(finalUrl),maxbitrate,str(name),base64.b64decode("aHR0cDovL2NvcmUuZHN0di5jb20vdmlkZW8vZmxhc2gvUGxheWVyRFN0dlNTLnN3Zj92PTEuMTk="))
#    print 'finalUrl',finalUrl
#    playlist = xbmc.PlayList(1)
#    playlist.clear()
#    listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
#    playlist.add(finalUrl,listitem)
#    xbmcPlayer = xbmc.Player()
#    xbmcPlayer.play(playlist) 
    xbmc.executebuiltin('XBMC.RunPlugin('+finalUrl+')') 
    

def getdecSSMatchUrl(strToDecrypt,type):
    DECRYPTION_KEY1 = "1233901199002223000111A2"
    DECRYPTION_KEY2 = "9685647821298987483258Z8"
    DECRYPTION_KEY_LIVE1 = "9685647821298987483258Z8"
    DECRYPTION_KEY_LIVE2 = "1233901199002223000111A2"
    DECRYPTION_KEY_VIDEO1 = "1233901199002223000111A2"
    DECRYPTION_KEY_VIDEO2 = "9685647821298987483258Z8"
    ds1 = ""
    if type == "LIVE": 
        import pyaes
        decryptor = pyaes.new(DECRYPTION_KEY_LIVE1, pyaes.MODE_ECB, IV='')
        ds1 = decryptor.decrypt(strToDecrypt.decode("hex")).replace('\x00', '')
        if ds1[:4] == "rtmp" or ds1[:4] == "http": return ds1
        else:
            decryptor = pyaes.new(DECRYPTION_KEY_LIVE2, pyaes.MODE_ECB, IV='')
            ds1 = decryptor.decrypt(strToDecrypt.decode("hex")).replace('\x00', '')
            if ds1[:4] == "rtmp" or ds1[:4] == "http": return ds1
    if type == "VIDEO": 
        decryptor = pyaes.new(DECRYPTION_KEY1, pyaes.MODE_ECB, IV='')
        ds1 = decryptor.decrypt(strToDecrypt.decode("hex")).replace('\x00', '')
        if ds1[:4] == "rtmp" or ds1[:4] == "http": return ds1
        else:
            decryptor = pyaes.new(DECRYPTION_KEY2, pyaes.MODE_ECB, IV='')
            ds1 = decryptor.decrypt(strToDecrypt.decode("hex")).replace('\x00', '')
            if ds1[:4] == "rtmp" or ds1[:4] == "http": return ds1
    return ds1
    
    
def PlayWillowMatch(url):
#    patt='(.*?)'
#    print link
#    match_url =re.findall(patt,link)[0]
    if not url.startswith('http'):
        match_url=getMatchUrl(url)
    else:
        match_url=url
    if match_url=='': return 
    keepplay=True
    if not 'www.youtube.com' in match_url:
        match_url=match_url+'|User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36'
    else:
        check_url='https://www.youtube.com/get_video_info?html5=1&video_id=%s'% match_url.split('embed/')[1].split('?')[0]
        match_url= 'plugin://plugin.video.youtube/play/?video_id=%s' % match_url.split('embed/')[1].split('?')[0]
        try:
            patt=''
            txt=getUrl(check_url)
            if not 'hlsvp=' in txt:
                #play via proxy
                keepplay=False
                progress = xbmcgui.DialogProgress()
                progress.create('Progress', 'Willow youtube')
                progress.update( 10, "", "Youtube link ??")
                
                ##now play with proxy
                progress.update( 30, "", "Not in US? Using proxy" )
                proxyserver=selfAddon.getSetting('WillowProxy')
                proxyport=selfAddon.getSetting('WillowPort')
                print 'playing with proxy'
                cookie_handler = urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar())
                opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler(),urllib2.ProxyHandler({ 'https'  : '%s:%s'%(proxyserver,proxyport)}))
                req = urllib2.Request(check_url)
                req.add_header('User-Agent','Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/11B554a')
                response = opener.open(req,timeout=20)
                link=response.read()
                response.close()
                print link
                progress.update( 30, "", "Got the Link, Now playing with Using proxy" )
                pat='hlsvp=(.*?)&'
                final_url=urllib.unquote(re.findall(pat,link)[0])
                print final_url
                match_url=final_url+'|User-Agent=VLC/2.2.1 LibVLC/2.2.1'
                keepplay=True
                #playmediawithproxy(final_url,str(name),'',proxyserver,proxyport,progress)
                print 'end playing with proxy'
                
        except: traceback.print_exc(file=sys.stdout)
    if keepplay:
        playlist = xbmc.PlayList(1)
        playlist.clear()
        listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
        playlist.add(match_url,listitem)
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(playlist) 

def AddWillowReplayParts(url):
    try:
    
        replays=getWillowHighlights(url)
        
        addDir(Colored(name,'EB',True) ,'' ,-1,'', False, True,isItFolder=False)		#name,url,mode,icon
        
        addDir(Colored('Highlights and Events','blue',True) ,'' ,-1,'', False, True,isItFolder=False)		#name,url,mode,icon
        if replays and len(replays)>0:
            for section in replays:
                addDir(section[0] ,section[1],22,section[2], False, True,isItFolder=False)		#name,url,mode,icon
            
        link=getMatchUrl(url)
        sections=link.split(',')
        
        addDir(Colored('Replay','red',True) ,'' ,-1,'', False, True,isItFolder=False)		#name,url,mode,icon
        for section in sections:
            sname,section_number=section.split('=')
            addDir(sname ,url+':'+section_number,22,'', False, True,isItFolder=False)		#name,url,mode,icon

            
    except: traceback.print_exc(file=sys.stdout)

def getWillowHighlights(matchid):
    try:
        req = urllib2.Request(base64.b64decode('aHR0cDovL3dpbGxvd2ZlZWRzLndpbGxvdy50di93aWxsb3dNYXRjaERldGFpbHMvTWF0Y2hKU09ORGF0YS0lcy5qcw==')%matchid)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36')
        response = urllib2.urlopen(req)
        if response.info().get('Content-Encoding') == 'gzip':
            from StringIO import StringIO
            import gzip
            buf = StringIO( response.read())
            f = gzip.GzipFile(fileobj=buf)
            link = f.read()
        else:
            link=response.read()

        response.close()
#        print repr(link)
        pat='(\{.*})'
        link=re.findall(pat,link)[0]
        matchdata=json.loads(link)
        
        r=[]
        for m in matchdata["result"]:
            if "BGUrl" in m and  (not m["BGUrl"]=="") and (base64.b64decode('d3p2b2Q6') in m["BGUrl"] or base64.b64decode('Ymd2b2Q=') in m["BGUrl"] ):
                rurl=m["BGUrl"]
                if base64.b64decode('d3p2b2Q6') in rurl:
                    rurl=rurl.replace(base64.b64decode('d3p2b2Q6Ly8='),base64.b64decode('aHR0cDovLzM4Ljk5LjY4LjE2MjoxOTM1L3dsbHd2b2QvX2RlZmluc3RfL3dsdm9kL3NtaWw6'));
                    rurl=rurl.replace('.mp4',base64.b64decode('X3dlYi5zbWlsL3BsYXlsaXN0Lm0zdTg='));
                else:
                    rurl=rurl.replace('bgvod:/','')
                    data={"bgvodurl":rurl}
                    rurl=getUrl('https://www.willow.tv/EventMgmt/webservices/getBGHgltUrl.asp?'+urllib.urlencode(data))
                    print rurl
                    rurl=json.loads(rurl)["url"]

                r.append([m["YTVideoName"],rurl,m["YTThumbId"]])
#        print 'replays',r
        return r
            
    except:
        print traceback.print_exc(file=sys.stdout)
        return None
def getUrlFromUS(urltoget):
    cJar=cookielib.LWPCookieJar()
    link=''
    try:
        getUrl('http://proxyusa.org/index.php',cJar);
        post={'u':urltoget,'encodeURL':'on','allowCookies':'on','stripJS':'on','stripObjects':'on'}
        post = urllib.urlencode(post)
        link= getUrl('http://proxyusa.org/includes/process.php?action=update',cJar,post, timeout=10)
    except:
        getUrl('http://webproxy.to/',cJar);
        post={'u':urltoget,'encodeURL':'on','allowCookies':'on','stripJS':'on','stripObjects':'on'}
        post = urllib.urlencode(post)
        link= getUrl('http://webproxy.to/includes/process.php?action=update',cJar,post,timeout=10) 
    return link
    
def AddWillowCric(url):
    try:
    
        #addDir(Colored('24x7 channel (US only, others use proxy so SLOW)','blue',True) ,'999999' ,21,'', False, True,isItFolder=False)		#name,url,mode,icon    
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        #patt='json_matchbox = (.*?);'
        #match_url =re.findall(patt,link)[0]
        #print 'match_url',match_url

        match_url=getUrl(base64.b64decode("aHR0cDovL2FwcGZlZWRzLndpbGxvdy50di9tb2JpbGVIb21lX3YxLmpzb24="),headers=[('User-Agent','Willow/3.2.4 CFNetwork/711.4.6 Darwin/14.0.0')])
        #print repr(match_url)
        matches=json.loads(match_url)
        
        #print matches

        addDir(Colored('Live Games','EB',True) ,'' ,-1,'', False, True,isItFolder=False)		#name,url,mode,icon
#        print 'matches',matches
        loginworked,cookieJar= performWillowLogin();
        for game in matches["result"]:
            if game["islive"]==1:
                match_name=game["mname"]
                match_id=game["mid"]
                MatchStartDate=game["date"]
                entry_name=MatchStartDate+' - '+match_name


                if loginworked:
                    st='LiveMatch'
                    url=base64.b64decode('aHR0cDovL3d3dy53aWxsb3cudHYvRXZlbnRNZ210LyVzVVJMLmFzcD9taWQ9JXM=')%(st,match_id)
                    videoPage = getUrl(url,cookieJar=cookieJar)
                    videos=json.loads(videoPage)
                    print 'videos',videos
                    if "roku" in videos:
                        for video in videos["roku"]["URL"]:
                            addDir(Colored('Source %s %s '%(str(video["priority"]), video["player"]),'ZM',True) +entry_name ,match_id+':'+str(video["priority"]),21,'', False, True,isItFolder=False)		#name,url,mode,icon

                
                
        addDir(Colored('Recently Finished Games','EB',True) ,'' ,-1,'', False, True,isItFolder=False)		#name,url,mode,icon

        for game in matches["result"]:
            if game["islive"]==0:
                match_name=game["mname"]
                match_id=game["mid"]
                MatchStartDate=game["date"]
                entry_name=MatchStartDate+' - '+match_name
                    
    #            addDir(entry_name ,match_id,23,'', False, True,isItFolder=True)		#name,url,mode,icon
                addDir(entry_name ,match_id,23,'')            
    except: traceback.print_exc(file=sys.stdout)
         
    addDir(Colored('All Recorded Series >>Click to load','ZM',True) ,base64.b64decode('aHR0cDovL3d3dy53aWxsb3cudHYvRXZlbnRNZ210L3Jlc3VsdHMuYXNw' ),20,'') #blocking as the rtmp requires to be updated to send gaolVanusPobeleVoKosat
    

    
def AddWatchCric(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    patt='<h1>(.*?)\s*</h1>(.*?)</div>'
    match_url =re.findall(patt,link,re.DOTALL)
    
    patt_sn='sn = "(.*?)"'
    for nm,div in match_url:
            curl=''
            cname=nm.split('<')[0]
            pat_options='<li><a href="(.*?)">(.*?)<'
            match_options =re.findall(pat_options,div)
            addDir(cname ,curl ,-1,'', False, True,isItFolder=False)		#name,url,mode,icon
            if match_options and len(match_options)>0:
                for u,n in match_options:
                    if not u.startswith('htt'):u=url+u
                    curl=u                
                    addDir('    -'+n ,curl ,17,'', False, True,isItFolder=False)		#name,url,mode,icon
            else:
                cname='No streams available'
                curl=''
                addDir('    -'+cname ,curl ,-1,'', False, True,isItFolder=False)		#name,url,mode,icon
                



def AddSmartCric(url):
    req = urllib2.Request(base64.b64decode('aHR0cDovL3d3dy5zbWFydGNyaWMuY29tLw=='))
    req.add_header('User-Agent', 'Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3')
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    import random,math
    rnd1=str(int(math.floor(random.random()*5) ))
    rnd2=str(int(math.floor(random.random()*1000000) ))
    rnd3=str(int(math.floor(random.random()*1000000) ))
    req.add_header('Cookie', '_ga=GA1.%s.%s.%s'%(rnd1,rnd2,rnd3))


    response = urllib2.urlopen(req)
    link=response.read()
#    print link
    response.close()
    patt='performGet\(\'(.+)\''
    match_url =re.findall(patt,link)[0]
    channeladded=False
    patt_sn='sn = "(.*?)"'
    patt_pk='(&pk=.*?)"'
    try:
        match_sn =re.findall(patt_sn,link)[0]
        match_pk =re.findall(patt_pk,link)[0]
        ref=[('User-Agent','Mozilla/5.0 (iPhone; CPU iPhone OS 9_0_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13A452 Safari/601.1'),
            ('Referer','http://smartcric.com/')]
        lburl=re.findall('(http.*?loadbalancer)',link)[0]
        fms=getUrl(lburl,headers=ref).split('=')[1]
        final_url=  match_url+   match_sn
        req = urllib2.Request(final_url)
        req.add_header('User-Agent', 'Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3')
        req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')

        req.add_header('Origin', base64.b64decode('aHR0cDovL3d3dy5zbWFydGNyaWMuY29t'))
        req.add_header('Referer', base64.b64decode('aHR0cDovL3d3dy5zbWFydGNyaWMuY29tLw=='))

        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        sources = json.loads(link)



        addDir('Refresh' ,'Live' ,144,'')
        
        for source in sources["channelsList"]:
            if 1==1:#ctype=='liveWMV' or ctype=='manual':
#                print source
                curl=''
                cname=source["caption"]
                #fms=source["fmsUrl"]
#                print curl
                #if ctype<>'': cname+= '[' + ctype+']'
                addDir(cname ,curl ,-1,'', False, True,isItFolder=False)		#name,url,mode,icon


                
                if 'streamsList' in source and source["streamsList"] and len(source["streamsList"])>0:
                    for s in source["streamsList"]:
                        cname=s["caption"]
                        curl=s["streamName"]
                        streamid=str(s["streamId"])
                        
                        curl1="http://"+fms+":8088/mobile/"+curl+"/playlist.m3u8?id="+streamid+match_pk+'|User-Agent=Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3';
                        addDir('    -'+cname +" (http)" ,curl1 ,15,'', False, True,isItFolder=False)		#name,url,mode,icon
                        #curl1="rtsp://"+"206.190.140.164"+":1935/mobile/"+curl+"?key="+match_sn+match_pk;
                        #curl1="rtsp://"+fms+":1935/mobile/"+curl+"?id="+streamid+"&key="+match_sn+match_pk;
                        #addDir('    -'+cname +" (rtsp)",curl1 ,15,'', False, True,isItFolder=False)		#name,url,mode,icon

                        channeladded=True
                else:
                    cname='No streams available'
                    curl=''
                    addDir('    -'+cname ,curl ,-1,'', False, True,isItFolder=False)		#name,url,mode,icon
    except: traceback.print_exc(file=sys.stdout)
    if not channeladded:
        cname='No streams available'
        curl=''
        addDir('    -'+cname ,curl ,-1,'', False, True,isItFolder=False)		#name,url,mode,icon 
    addDir('Refresh' ,'Live' ,144,'')
            

    return

def PlayWatchCric(url):
    progress = xbmcgui.DialogProgress()
    
    progress.create('Progress', 'Fetching Streaming Info')
    progress.update( 10, "", "Finding links..", "" )
    pat_ifram='<iframe.*?src=(.*?).?"?>'    
    if 'c247.tv' not in url and 'crichd.tv' not in url:
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match_url =re.findall(pat_ifram,link)[0]
    else:
        match_url=url
        url=base64.b64decode('aHR0cDovL2VtYmVkMjQ3LmNvbS9saXZlLnBocD9jaD1QdHZfU3BvcnRzMSZ2dz02MDAmdmg9NDAwJmRvbWFpbj13d3cuc2FtaXN0cmVhbS5jb20=')
        
    req = urllib2.Request(match_url)
    req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
    req.add_header('Referer', url)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
#    print 'match_url',match_url,link
        

    ccommand="";#'%s;TRUE;TRUE;'
    swfUrl=base64.b64decode('aHR0cDovL3d3dy5taXBzcGxheWVyLmNvbS9jb250ZW50L3NjcmlwdHMvZnBsYXllci5zd2Y=')
    sitename='www.mipsplayer.com'
    pat_e=' e=\'(.*?)\';'
    app='live'
    pat_js='channel=\'(.*?)\''
    loadbalanacername=sitename
    
    if 'liveflashplayer.net/resources' in link:
        c='kaskatijaEkonomista'
        swfUrl=base64.b64decode('aHR0cDovL3d3dy5saXZlZmxhc2hwbGF5ZXIubmV0L3Jlc291cmNlcy9zY3JpcHRzL2ZwbGF5ZXIuc3dm')
        sitename='www.liveflashplayer.net'
        loadbalanacername='www.liveflashpublisher.com'
        pat_e=' g=\'(.*?)\';'
        app='stream'
        pat_js='channel=\'(.*?)\''
        ccommand=""#dont need to send

    elif 'www.mipsplayer.com' in link:
        c='ignore'#gaolVanusPobeleVoKosata
        ccommand=""#'%s;FALSE;FALSE;' #stop sending and waiting
        
        swfUrl=base64.b64decode('aHR0cDovL3d3dy5taXBzcGxheWVyLmNvbS9jb250ZW50L3NjcmlwdHMvZnBsYXllci5zd2Y=')
        sitename='www.mipsplayer.com'
        loadbalanacername='cdn.mipspublisher.com'
        pat_e=' e=\'(.*?)\';'
        app='live'
        pat_js='channel=\'(.*?)\''
    elif 'www.streamifyplayer.com' in link:
        c='keGoVidishStambolSoseBardovci'
        ccommand='%s;TRUE;TRUE;'
        ccommand=""#'%s;FALSE;FALSE;' #stop sending and waiting
        swfUrl=base64.b64decode('aHR0cDovL3d3dy5zdHJlYW1pZnlwbGF5ZXIuY29tL3Jlc291cmNlcy9zY3JpcHRzL2VwbGF5ZXIuc3dm')
        sitename='www.streamifyplayer.com'
        loadbalanacername='www.streamifypublisher.com'
        pat_e='channel.*?g=\'(.*?)\''
        app='live'
        pat_js='channel=\'(.*?)\''
    elif 'c247.tv' or 'crichd.tv' in link:
        c='zenataStoGoPuknalaGavolot'
        ccommand=''
        swfUrl=base64.b64decode('aHR0cDovL3d3dy5wM2cudHYvcmVzb3VyY2VzL3NjcmlwdHMvZXBsYXllci5zd2Y=')
        sitename='www.p3g.tv'
        pat_e='channel.*?g=\'(.*?)\''
        loadbalanacername='www.p3gpublish.com'
        app='live'
        pat_js='channel=\'(.*?)\''
    elif 'zenexplayer.com' in link:
        c='zenataStoGoPuknalaGavolot'
        ccommand=''
        swfUrl=base64.b64decode('aHR0cDovL3d3dy56ZW5leHBsYXllci5jb20vZGF0YS9zY3JpcHRzL2ZwbGF5ZXIuc3dm')
        sitename='www.zenexplayer.com'
        loadbalanacername=sitename
        pat_e='channel.*?g=\'(.*?)\''
        app='zenex'
        pat_js='channel=\'(.*?)\''
        
    progress.update( 40, "", "Building request links..", "" )
        
    match_urljs =re.findall(pat_js,link)[0]
    match_code =match_urljs
    try:
        width='620'
        height='430'

        patt="width=([0-9]*).*?height=([0-9]*)"
        matc =re.findall(patt,link)
#        print 'matc',matc
        width, height=matc[0]
    except: pass

#    print 'width,height',width,height
    #print link
    match_e =re.findall(pat_e,link)[0]
#    print 'match_e',match_e,match_urljs
    match_urljs=('http://%s/embedplayer/'%sitename)+match_urljs+'/'+match_e+'/'+width+'/'+height
    
    
    req = urllib2.Request(match_urljs)
    req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
    req.add_header('Referer', match_url)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    
    pat_flash='FlashVars\',.?\'(.*?)\''
    match_flash =re.findall(pat_flash,link)[0]
    matchid=match_flash.split('id=')[1].split('&')[0]
    if 'pk=' in match_flash:
        matchid+="&pk="+match_flash.split('pk=')[1].split('\'')[0].split('\"')[0]
    
    lb_url='http://%s:1935/loadbalancer?%s'%(loadbalanacername,match_code)
        
    req = urllib2.Request(lb_url)
    req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
    req.add_header('Referer', match_urljs)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    ip=link.split('=')[1]
    

    sid=match_flash.split('s=')[1].split('&')[0]
    progress.update( 40, "", "Finalizing request..", "" )

    if not ccommand=="":
        ccommand="ccommand="+(ccommand%c)
#    print 'ccommand',ccommand
    url='rtmp://%s/%s playpath=%s?id=%s pageUrl=%s swfUrl=%s Conn=S:OK %s flashVer=WIN\2019,0,0,185 timeout=20'%(ip,app,sid,matchid,match_urljs,swfUrl,ccommand)
#    print url
    playlist = xbmc.PlayList(1)
    playlist.clear()
    listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
    playlist.add(url,listitem)
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(playlist) 

def getYPUrl(url):
    ret=None
    try:
        html=getUrl(url)
        rr='aspx\?cid=([0-9]*)'
        tmp=re.findall(rr,html)
        if len(tmp)==0:
        
            rr='script type.*?src=[\'"](.*?embed.*?js)[\'"]'
            emburl=re.findall(rr,html)[0]

            emhtm=getUrl(emburl)
            rr='\?id=([0-9]*)'
            videoid=re.findall(rr,emhtm)[0]
        else:
            videoid=tmp[0]
    
        pageurl='http://stream.yupptv.com/PreviewPaidChannel.aspx?cid=%s'%videoid  
        emhtm=getUrl(pageurl)
        rr='file:\'(http.*?)\''    
        finalUrl=re.findall(rr,emhtm)
        #if len(finalUrl)==0:
        #    
        #    pageurl='http://stream.yupptv.com/PreviewPaidChannel.aspx?cid=%s'%videoid  
        #    #emhtm=getUrl(pageurl)
        #    emhtm=getUrlFromUS(pageurl)
        #    rr='file:\'(http.*?)\''    
        #    finalUrl=re.findall(rr,emhtm)
        ret=finalUrl[0]
        
    except: pass
    return ret
    
def PlayYP(url):
    url = base64.b64decode(url)
    #print 'gen is '+url

    finalUrl=getYPUrl(url)
        
    finalUrl=urllib.quote_plus(finalUrl+'&g=FLONTKRDWKGI&hdcore=3.2.0&amp;plugin=jwplayer-3.2.0.1|Referer=http://stream.yupptv.com/PreviewPaidChannel.aspx?cid=195')
    finalUrl='plugin://plugin.video.f4mTester/?url='+finalUrl
        
        
    xbmc.executebuiltin("xbmc.PlayMedia("+finalUrl+")")

def PlayGen(url,checkUrl=False):
    url = base64.b64decode(url)
    print 'gen is '+url

    if url.startswith('plugin://'):
        xbmc.executebuiltin("xbmc.PlayMedia("+url+")")
        return
    
    if checkUrl and url.startswith('http') and '.m3u' in url:
        headers=[('User-Agent','AppleCoreMedia/1.0.0.13A452 (iPhone; U; CPU OS 9_0_2 like Mac OS X; en_gb)')]
        getUrl(url.split('|')[0],timeout=5,headers=headers)
    playlist = xbmc.PlayList(1)
    playlist.clear()
    listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
    playlist.add(url,listitem)
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(playlist) 
        
        
def PlaySmartCric(url):
    playlist = xbmc.PlayList(1)
    playlist.clear()
    listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
    playlist.add(url,listitem)
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(playlist) 
        
def AddEnteries(name, type=None):
#	print "addenT"
    if type=='Shows':
        AddShows(mainurl)
    elif type=='ProgTalkShows':
        AddProgramsAndShows(mainurl)
    elif name=='Next Page' or mode==43:
        AddShows(url)
    else:
        #addDir(Colored('ZemTv Channels','ZM',True) ,'ZEMTV' ,10,'', False, True,isItFolder=False)		#name,url,mode,icon
        #AddChannels();#AddChannels()
        isPakistani=(name=='Pakistani Live Channels')
        
        
        isYellowOff=selfAddon.getSetting( "isYellowOff" ) 
#        print 'isPakistani',isPakistani,isYellowOff
        ret_match=[]
        progress = xbmcgui.DialogProgress()
        progress.create('Progress', 'Fetching Streaming Info')
        progress.update( 10, "", "Loading Yellow Channels", "" )
        if isPakistani and not isYellowOff=="true":        
            #addDir(Colored('EboundServices Channels','EB',True) ,'ZEMTV' ,10,'', False, True,isItFolder=False)		#name,url,mode,icon
            try:
                
                ret_match=AddChannelsFromEbound();#AddChannels()
                progress.update( 20, "", "Loading Yellow Channels", "" )
                print 'ret_match',ret_match
            except:
                traceback.print_exc(file=sys.stdout)
                
                
#        addDir(Colored('Other sources','ZM',True) ,'ZEMTV' ,10,'', False, True,isItFolder=False)
        try:
            ctype=1 if name=='Pakistani Live Channels' else ( 2 if name=='Indian Live Channels' else 3)
            AddChannelsFromOthers(ctype,ret_match,progress)
        except:
            print 'somethingwrong'
            traceback.print_exc(file=sys.stdout)
        progress.close()
    return
    
def getPTCCats():
    ret=[]
    try:
        xmldata=getPTCUrl()
        for source in xmldata["channelsCategories"]:
            if not source["categoryName"] in ret :
                ret.append(source["categoryName"])
        if len(ret)>0:
            ret=sorted(ret,key=lambda s: s[0].lower()   )
    except:
        traceback.print_exc(file=sys.stdout)
    return ret
    
def getPakTVCats():
    ret=[]
    try:
        xmldata=getPakTVPage()
        for source in xmldata:
            if not source["categoryName"] in ret :
                ret.append(source["categoryName"])
        if len(ret)>0:
            ret=sorted(ret,key=lambda s: s[0].lower()   )
    except:
        traceback.print_exc(file=sys.stdout)
    return ret
            
def getPakTVChannels(categories, forSports=False):
    ret=[]
    try:
        xmldata=getPakTVPage()
        for source in xmldata:
            if source["categoryName"] in categories or (forSports):# and ('sport' in source["categoryName"].lower() or 'BarclaysPremierLeague' in source["categoryName"] )    ) :
                ss=source
                cname=ss["channelName"]
                if 'ebound.tv' in ss["channelLink"]:
                    #print ss["channelLink"]
                    curl='ebound2:'+ss["channelLink"].replace(':1935','')
                else:
                    curl='direct2:'+ss["channelLink"]+'|User-Agent=AppleCoreMedia/1.0.0.13A452 (iPhone; U; CPU OS 9_0_2 like Mac OS X; en_gb)'
                cimage=ss["categoryLogo"]
                
                if len([i for i, x in enumerate(ret) if x[2] ==curl ])==0:                    
                    ret.append((cname +' v7' ,'manual', curl ,cimage))   
        if len(ret)>0:
            ret=sorted(ret,key=lambda s: s[0].lower()   )
    except:
        traceback.print_exc(file=sys.stdout)
    return ret
def getCFChannels(category):
    ret=[]
    try:
        xmldata=getCFPage(category)
#        print xmldata
        for source in xmldata:

            ss=source
            cname=ss["Title"]
            cimage=ss["ThumbnailURL"]
            curl="CF:"+ss["ContentId"]
                    
            ret.append((cname +' CF' ,'manual', curl ,cimage))   
        if len(ret)>0:
            ret=sorted(ret,key=lambda s: s[0].lower()   )
    except:
        traceback.print_exc(file=sys.stdout)
    return ret  
    
def getYPChannels(url,progress):
    ret=[]
    try:
        
        xmldata=getYPPage(url,progress)
        for source in xmldata:

            ss=source
            cname=ss[2]
            cimage=ss[1]
            curl="YP:"+ss[0]
                    
            ret.append((cname +' YP' ,'manual', curl ,cimage))   
        if len(ret)>0:
            ret=sorted(ret,key=lambda s: s[0].lower()   )
    except:
        traceback.print_exc(file=sys.stdout)
    return ret    
    
def getDittoChannels(categories, forSports=False):
    ret=[]
    try:
        xmldata=getDittoPage()
#        print xmldata
        for source in xmldata:#Cricket#
            if 1==1:#source["categoryName"].strip() in categories or (forSports and ('sport' in source["categoryName"].lower() or 'BarclaysPremierLeague' in source["categoryName"] )    ) :
                ss=source
                cname=ss["name"]
                curl=base64.b64decode("ZGl0dG86aHR0cDovL3d3dy5kaXR0b3R2LmNvbS9saXZldHYvbGluaz9uYW1lPSVz")%urllib.quote_plus(cname)
                try:
                    cname+=" "+ss["manual"]
                except: pass
                
                cimage=ss["poster"].replace('\\/','/')
                
                
                if len([i for i, x in enumerate(ret) if x[2] ==curl ])==0:                    
                    ret.append((cname +' ditto' ,'manual', curl ,cimage))   
        if len(ret)>0:
            ret=sorted(ret,key=lambda s: s[0].lower()   )
    except:
        traceback.print_exc(file=sys.stdout)
    return ret    
    
def getIpBoxSources():
    ret=[]
    try:


        servers=getUrl("http://pastebin.com/raw/GrYKMHrF")
        servers=servers.splitlines()

        import time
        for ln in servers:
            if not ln.startswith("##") and len(ln)>0:
                try:
                    ##serial:mac:time:text
                    #print ln
                    servername,surl=ln.split('$')
                    
                    ret.append((servername, surl ))   
                except: traceback.print_exc(file=sys.stdout)
    except:
        traceback.print_exc(file=sys.stdout)
    return ret  

def getIpBoxChannels(url,forSports=False):
    ret=[]
    try:
        for u in url:
            try:
                html=getUrl(u)
                #print 'mmmmmmmmmmname',name
                #print xmldata
                if mode==67:
                    #print 'aaaaaaaaaaaaaaaaaaaaaa'
                    reg='#EXTINF:-1,(.*?(.).*)\s(.*)\s?'
                    forSports=True
                else:
                    if forSports:
                        reg='#EXTINF:-1,(.*?(sport|epl|Willow|CTH).*)\s(.*)\s?'
                    else:
                        reg='#EXTINF:-1,(Yupp|in):(.*)\s(.*)'
                xmldata=re.findall(reg,html,re.IGNORECASE)
                #print xmldata
                for source in xmldata:#Cricket#
                    try:
                        ss=source
                        cname=ss[0] if forSports else ss[1] 
                        #print repr(cname), repr(ss)
                        if '.ts' in ss[2]:
                            #curl='direct:'+ss[2].replace('.ts','.ts').replace('\r','')
                            #curl='direct:'+ss[2].replace('.ts','.m3u8').replace('\r','')
                            #curl='ipbox:'+ss[2].replace('\r','').replace('.ts','.ts')#+'|Mozilla/5.0 (Windows NT 6.1 WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36'
                            curl='ipbox:'+ss[2].replace('\r','').replace('.ts','.ts')+'|User-Agent=VLC/2.2.1 LibVLC/2.2.17&Icy-MetaData=1'
                            ##curl='ipbox:'+ss[2].replace('\r','').replace('.ts','.m3u8')+'|User-Agent=VLC/2.2.1 LibVLC/2.2.17&Icy-MetaData=1'
                            #print 'iptv',curl
                            ret.append((cname +' Ipbox' ,'manual', curl ,''))   
                    except: pass
            except: pass
            if len(ret)>0:
                ret=sorted(ret,key=lambda s: s[0].lower()   )
    except:
        traceback.print_exc(file=sys.stdout)
    return ret  
    
def getWTVCats():
    ret=[]
    try:
        xmldata=getWTVPage()
        #print xmldata
        for source in xmldata:#Cricket#
            if not source["categoryName"] in ret :
                    ret.append(source["categoryName"])   
        if len(ret)>0:
            ret=sorted(ret,key=lambda s: s[0].lower()   )
    except:
        traceback.print_exc(file=sys.stdout)
    return ret  

def getGTVCats():
    ret=[]
    try:
        xmldata=getGTVPage()
        #print xmldata
        for source in xmldata:#Cricket#
            if not source["categoryName"] in ret :
                    ret.append(source["categoryName"])   
        if len(ret)>0:
            ret=sorted(ret,key=lambda s: s[0].lower()   )
    except:
        traceback.print_exc(file=sys.stdout)
    return ret  
    
def getPITVCats():
    ret=[]
    try:
        xmldata=getPITVPage()
        #print xmldata
        for source in xmldata:#Cricket#
            if not source["categoryName"] in ret :
                    ret.append(source["categoryName"])   
        if len(ret)>0:
            ret=sorted(ret,key=lambda s: s[0].lower()   )
    except:
        traceback.print_exc(file=sys.stdout)
    print ret
    return ret  
    
def getWTVChannels(categories, forSports=False):
    ret=[]
    try:
        xmldata=getWTVPage()
        #print xmldata
        for source in xmldata:#Cricket#
            if source["categoryName"].strip() in categories or source["categoryName"] in categories or (forSports and ('sport' in source["categoryName"].lower() or 'BarclaysPremierLeague' in source["categoryName"] )    ) :

                ss=source
                cname=ss["channelName"]
                #print cname
                if 'ebound.tv' in ss["channelLink"]:
                    curl='ebound2:'+ss["channelLink"].replace(':1935','')
                else:
                    curl='direct2:'+ss["channelLink"]
                    if ss["channelLink"].startswith('http'): curl+='|User-Agent=AppleCoreMedia/1.0.0.13A452 (iPhone; U; CPU OS 9_0_2 like Mac OS X; en_gb)' 

                cimage=ss["categoryImageLink"]
                
                if len([i for i, x in enumerate(ret) if x[2] ==curl ])==0:                    
                    #print cname
                    ret.append((cname +' v9' ,'manual', curl ,cimage))   
        if len(ret)>0:
            ret=sorted(ret,key=lambda s: s[0].lower()   )
    except:
        traceback.print_exc(file=sys.stdout)
    return ret  

def getPITVChannels(categories, forSports=False):
    ret=[]
    try:
        xmldata=getPITVPage()
        #print xmldata
        
        
        for source in xmldata:#Cricket#
            
            if source["categoryName"].strip() in categories or source["categoryName"] in categories or (forSports and ('sport' in source["categoryName"].lower() or 'BarclaysPremierLeague' in source["categoryName"] )    ) :

                ss=source
                cname=ss["channelName"]
                #print cname
                if 'ebound.tv' in ss["channelLink"]:
                    curl='ebound2:'+ss["channelLink"].replace(':1935','')
                else:
                    curl='direct2:'+ss["channelLink"]
                    if ss["channelLink"].startswith('http'): curl+='|User-Agent=AppleCoreMedia/1.0.0.13A452 (iPhone; U; CPU OS 9_0_2 like Mac OS X; en_gb)' 

                cimage=ss["categoryLogo"]
                
                if len([i for i, x in enumerate(ret) if x[2] ==curl ])==0:                    
                    #print cname
                    ret.append((cname ,'manual', curl ,cimage))   
        if len(ret)>0:
            ret=sorted(ret,key=lambda s: s[0].lower()   )
    except:
        traceback.print_exc(file=sys.stdout)
    return ret  
    
def getGTVChannels(categories, forSports=False):
    ret=[]
    try:
        xmldata=getGTVPage()
        #print xmldata
        for source in xmldata:#Cricket#
            if source["categoryName"].strip() in categories or source["categoryName"] in categories or (forSports and ('sport' in source["categoryName"].lower() or 'BarclaysPremierLeague' in source["categoryName"] )    ) :

                ss=source
                cname=ss["channelName"]
                #print cname
                if 'ebound.tv' in ss["channelLink"]:
                    curl='ebound2:'+ss["channelLink"].replace(':1935','')
                else:
                    curl='direct2:'+ss["channelLink"]
                    if ss["channelLink"].startswith('http'): curl+='|User-Agent=AppleCoreMedia/1.0.0.13A452 (iPhone; U; CPU OS 9_0_2 like Mac OS X; en_gb)' 

                cimage=ss["categoryImageLink"]
                
                if len([i for i, x in enumerate(ret) if x[2] ==curl ])==0:                    
                    #print cname
                    ret.append((cname ,'manual', curl ,cimage))   
        if len(ret)>0:
            ret=sorted(ret,key=lambda s: s[0].lower()   )
    except:
        traceback.print_exc(file=sys.stdout)
    return ret  
    
    
def getUniTVCats():
    ret=[]
    try:
        xmldata=getUniTVPage()
        #print xmldata
        for source in xmldata:#Cricket#
            if not source["categoryName"] in ret :
                    ret.append(source["categoryName"])   
        if len(ret)>0:
            ret=sorted(ret,key=lambda s: s[0].lower()   )
    except:
        traceback.print_exc(file=sys.stdout)
    return ret  
        
def getUniTVChannels(categories, forSports=False):
    ret=[]
  
    try:
        xmldata=getUniTVPage()
        #print xmldata
        for source in xmldata:#Cricket#
            if source["categoryName"].strip() in categories or source["categoryName"] in categories or (forSports and ('sport' in source["categoryName"].lower() or 'BarclaysPremierLeague' in source["categoryName"] )    ) :

                ss=source
                cname=ss["channelName"]
                #print cname
                if 'ebound.tv' in ss["channelLink"]:
                    curl='ebound2:'+ss["channelLink"].replace(':1935','')
                    #print curl
                else:
                    curl='direct2:'+ss["channelLink"]
                    if ss["channelLink"].startswith('http'): curl+='|User-Agent=AppleCoreMedia/1.0.0.13A452 (iPhone; U; CPU OS 9_0_2 like Mac OS X; en_gb)' 
                cimage=ss["categoryImageLink"]
                
                if len([i for i, x in enumerate(ret) if x[2] ==curl ])==0:                    
                    #print cname
                    ret.append((cname +' v8' ,'manual', curl ,cimage))   
        if len(ret)>0:
            ret=sorted(ret,key=lambda s: s[0].lower()   )
    except:
        traceback.print_exc(file=sys.stdout)
    return ret  
    
    


def local_time(zone='Asia/Karachi'):
    from datetime import datetime
    from pytz import timezone
    other_zone = timezone(zone)
    other_zone_time = datetime.now(other_zone)
    return other_zone_time.strftime('%B-%d-%Y')
    
def getAPIToken( url,  username):
    print url,username
    from pytz import timezone
    dt=local_time()
    s = "uktvnow-token-"+ dt + "-"+ "_|_-" + url + "-" + username +"-" + "_|_"+ "-"+ base64.b64decode("MTIzNDU2IUAjJCVedWt0dm5vd14lJCNAITY1NDMyMQ==")
    
    print s
    import hashlib
    return hashlib.md5(s).hexdigest()

def getMonaKey():
    s=getUrl(base64.b64decode("aHR0cDovL3pvbmEtYXBwLmNvbS96b25hLWFwcC9hcGkucGhwP2FwaV9rZXk="),headers=[('User-Agent','Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-G920F Build/LMY47X')])
    return json.loads(s)["LIVETV"][0]["key"]
    
def getMonaPage(cat):
    fname='monapage_%s.json'%cat
    fname=os.path.join(profile_path, fname)
    try:
        jsondata=getCacheData(fname,60*60)
        if not jsondata==None:
            return jsondata
    except:
        print 'file getting error'
        traceback.print_exc(file=sys.stdout)
    
    if cat=="":
        url=base64.b64decode('aHR0cDovL3pvbmEtYXBwLmNvbS96b25hLWFwcC9hcGkucGhwP2tleT0lcw==')%(getMonaKey())
    else:
        url=base64.b64decode('aHR0cDovL3pvbmEtYXBwLmNvbS96b25hLWFwcC9hcGkucGhwP2NhdF9pZD0lcyZrZXk9JXM=')%(cat,getMonaKey())
    print url
    headers=[('User-Agent','Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-G920F Build/LMY47X)')]
    jsondata=getUrl(url,headers=headers)
    jsondata=json.loads(jsondata)
    
    try:
        if len(jsondata["LIVETV"])>0:
            storeCacheData(jsondata,fname)
    except:
        print 'uktv file saving error'
        traceback.print_exc(file=sys.stdout)
    return jsondata
    
def getUKTVPage():
    fname='uktvpage.json'
    fname=os.path.join(profile_path, fname)
    try:
        jsondata=getCacheData(fname,10*60)
        if not jsondata==None:
            return jsondata
    except:
        print 'file getting error'
        traceback.print_exc(file=sys.stdout)
    usernames=eval(base64.b64decode("WydTZXJnaW8nLCdEYXNoJywnRnJhemVyJywnWmVkJywnQWxhbicsJ0RvbWluaWMnLCdLZW50JywnSG93YXJkJywnRXJpYycsJ0plbidd"))
    import random
    username = random.choice(usernames)
    post = {'username':username}
    post = urllib.urlencode(post)
  
    #headers=eval(base64.b64decode("WygnVXNlci1BZ2VudCcsJ1VTRVItQUdFTlQtVUtUVk5PVy1BUFAtVjEnKSwoJ2FwcC10b2tlbicsJ2FmZjE2MTRiNTJhNTM3YmQ3YmEyZDMyODE0ODU1NmFmJyld"))
    headers=[('User-Agent','USER-AGENT-UKTVNOW-APP-V1'),('app-token',getAPIToken(base64.b64decode("aHR0cDovL2FwcC51a3R2bm93Lm5ldC92MS9nZXRfYWxsX2NoYW5uZWxz"),username))]
    jsondata=getUrl(base64.b64decode("aHR0cDovL2FwcC51a3R2bm93Lm5ldC92MS9nZXRfYWxsX2NoYW5uZWxz"),post=post,headers=headers)
    jsondata=json.loads(jsondata)
    
    try:
        if len(jsondata["msg"]["channels"])>0:
            storeCacheData(jsondata,fname)
    except:
        print 'uktv file saving error'
        traceback.print_exc(file=sys.stdout)
    return jsondata

def getUKTVCats():
    ret=[]
    try:
        jsondata=getUKTVPage()
        for channel in jsondata["msg"]["channels"]:
            if channel["cat_name"] not in ret:
                ret.append(channel["cat_name"])
        if len(ret)>0:
            ret=sorted(ret,key=lambda s: s[0].lower() )                        
    except:
        traceback.print_exc(file=sys.stdout)
    return ret    
    
def getMonaCats():
    ret=[]
    try:
        jsondata=getMonaPage('')
        for channel in jsondata["LIVETV"]:
            ret.append((channel["cid"],channel["category_name"]))
        if len(ret)>0:
            ret=sorted(ret,key=lambda s: s[0].lower() )                        
    except:
        traceback.print_exc(file=sys.stdout)
    return ret    


    
def getMonaChannels(cat):
    ret=[]
    try:

        jsondata=getMonaPage(cat)
        for channel in jsondata["LIVETV"]:
            cname=channel["channel_title"]#.encode("utf-8")
            #print cname.encode("utf-8")
            #print cname
            #print channel
            #print channel
            curl=channel["channel_url"]
            ua='Mozilla/5.0 (Linux; Android 5.1.1; en-GB; SM-G920F Build/LMY47X.G920FXXS3COK5) MXPlayer/1.7.40'
            if curl.startswith('vlc://'):
                curl=curl.split('vlc://')[1]
                #ua=""
            curl='direct:'+curl
            #print curl
            if 'wiseplay' in cname.lower():
                ua='Lavf/57.25.100'
            if  curl.startswith("direct:http"):
                curl+='|User-Agent='+ua
            cimage=channel["category_image"]
            if not cimage.startswith("http"):
                cimage=base64.b64decode('aHR0cDovL3pvbmEtYXBwLmNvbS96b25hLWFwcC9pbWFnZXMv')+cimage
            if cname==None: cname=curl
            if len([i for i, x in enumerate(ret) if x[2] ==curl  ])==0:                    
                ret.append((cname ,'manual', curl ,cimage))  
        if len(ret)>0:
            ret=sorted(ret,key=lambda s: s[0].lower() )                        
    except:
        traceback.print_exc(file=sys.stdout)
    return ret

def getUKTVChannels(categories=[], channels=[]):
    ret=[]
    try:

        jsondata=getUKTVPage()
        for channel in jsondata["msg"]["channels"]:
            if channel["cat_name"].strip().lower() in categories or  channel["cat_name"] in categories  or channel["channel_name"].strip().lower() in categories  :
                    cname=channel["channel_name"]
                    curl='uktvnow:'+channel["pk_id"]
                    cimage=channel["img"]
                    if not cimage.startswith("http"):
                        cimage='https://app.uktvnow.net/'+cimage
                    if cname==None: cname=curl
                    if len([i for i, x in enumerate(ret) if x[2] ==curl  ])==0:                    
                        ret.append((cname +' uktv' ,'manual', curl ,cimage))  
        if len(ret)>0:
            ret=sorted(ret,key=lambda s: s[0].lower() )                        
    except:
        traceback.print_exc(file=sys.stdout)
    return ret

def getptcchannels(categories, forSports=False):
    ret=[]
    try:
        import iptv
        xmldata=getPTCUrl()
        for source in xmldata["channelsCategories"]:
            if source["categoryName"].strip() in categories or source["categoryName"] in categories or (forSports):# and ('sport' in source["categoryName"].lower() or 'BarclaysPremierLeague' in source["categoryName"] )    ) :
                for ss in source["channels"]:
                    cname=ss["name"]
                    if 'ebound.tv' in ss["url"]:
                        
                        curl='ebound2:'+ss["url"].replace(':1935','')
                    else:
                        curl='ptc:'+ss["url"]
                    cimage=ss["imgurl"]
                    
                    if len([i for i, x in enumerate(ret) if x[2] ==curl  ])==0:                    
                        ret.append((cname +' v6' ,'manual', curl ,cimage))  
        if len(ret)>0:
            ret=sorted(ret,key=lambda s: s[0].lower() )                        
    except:
        traceback.print_exc(file=sys.stdout)
    return ret

    
def getiptvchannels(gen):
    
    ret=[]
    try:
        import iptv
        macid,ipurl=getiptvmac()
        xmldata=iptv.getAllChannels(macid,ipurl,None,profile_path)
        for source in xmldata["channels"]:
            ss=xmldata["channels"][source]
            #print pg,source.findtext('programCategory').lower()
            if ss["genre_title"].lower()==gen or (gen=='sports' and ss["name"][:3] in ['NFL','NHL','NBA','BOX']):
                cname=ss["name"]
                curl=json.dumps(ss)
                cimage=base64.b64decode('aHR0cDovL3BvcnRhbC5pcHR2cHJpdmF0ZXNlcnZlci50di9zdGFsa2VyX3BvcnRhbC9taXNjL2xvZ29zLzMyMC8=')+ss["logo"]
                ret.append((cname +' v5' ,'manual3', curl ,cimage))        
    except:
        traceback.print_exc(file=sys.stdout)
    return ret

def storeCacheData(data, fname):
    if DONOTCACHE: return
    now=time()
    sessiondata=json.loads('{"cache":[{"time":%s}]}'%str(now))
    sessiondata["cache"][0]["data"]=data
    with open(fname, 'w') as txtfile:
        json.dump(sessiondata, txtfile)
    print 'file saved',fname
    
def getCacheData(fname, timeout=0):
    if DONOTCACHE: return None
    with open(fname) as data_file:
        data = json.loads(data_file.read())
    currentime=0
    time_init = float(data["cache"][0]["time"]);
    now=time()
    # update 12h
    if (now - time_init)>timeout:
        return None
    else:
        print 'returning data'
        return data["cache"][0]["data"]
        
        
    
    
def AddChannelsFromOthers(cctype,eboundMatches=[],progress=None):

    isv3Off=selfAddon.getSetting( "isv3Off" )
    #isv3Off="true"
    isv5Off=selfAddon.getSetting( "isv5Off" )
    isv5Off="true"
    isv6Off=selfAddon.getSetting( "isv6Off" )
    isv7Off=selfAddon.getSetting( "isv7Off" )
    isv7Off="true"
    isv8Off=selfAddon.getSetting( "isv8Off" )
    isv9Off=selfAddon.getSetting( "isv9Off" )
    if isv9Off=="":isv9Off="true"#bydefault off
    isdittoOff=selfAddon.getSetting( "isdittoOff" )
    isCFOff=selfAddon.getSetting( "isCFOff" )  
    isIpBoxff=selfAddon.getSetting( "isIpBoxff" )
    #isIpBoxff="true"
    isYPgenOff= selfAddon.getSetting( "isYPOff" )
    isUKTVOff=selfAddon.getSetting( "isUKTVOff" )

    main_ch='(<section_name>Pakistani<\/section_name>.*?<\/section>)'
#    v4link='aHR0cDovL3N0YWdpbmcuamVtdHYuY29tL3FhLnBocC8yXzIvZ3htbC9jaGFubmVsX2xpc3QvMQ=='
    v4link='aHR0cDovL2ZlcnJhcmlsYi5qZW10di5jb20vaW5kZXgucGhwLzJfMi9neG1sL2NoYW5uZWxfbGlzdC8x'
    v4patt='<item>.*?<channel_id>(.*?)</channel_id>.*?<name>(.*?)<.*?<link>(.*?)<.*?channel_logo>(.*?)<'  
    v4patt='<channel><channel_number>(.*?)</channel_number>.*?<channel_name>(.*?)<.*?<channel_url>(.*?)<(.)' 
    usev4=False
    if cctype==2:
        main_ch='(<section_name>Hindi<\/section_name>.*?<\/section>)'
#        v4link='aHR0cDovL2ZlcnJhcmlsYi5qZW10di5jb20vaW5kZXgucGhwL3htbC9jaGFubmVsX2xpc3QvNC8='
        v4patt='<channel><channel_number>(.*?)</channel_number>.*?<channel_name>(.*?)<.*?<channel_url>(.*?)<(.)'  
        usev4=False
    if cctype==3:
        main_ch='(<section_name>Punjabi<\/section_name>.*?<\/section>)'
#        v4link='aHR0cDovL2ZlcnJhcmlsYi5qZW10di5jb20vaW5kZXgucGhwL3htbC9jaGFubmVsX2xpc3QvNjU5Lw=='
        v4patt='<channel><channel_number>(.*?)</channel_number>.*?<channel_name>(.*?)<.*?<channel_url>(.*?)<(.)'
        usev4=False
        

    patt='<item><name>(.*?)<.*?<link>(.*?)<.*?albumart>(.*?)<'
    match=[]    
    if 1==2:#enable it
        if cctype==1:
            url=base64.b64decode("aHR0cDovL2pweG1sLmphZG9vdHYuY29tL3Z1eG1sLnBocC9qYWRvb3htbC9pdGVtcy8xMzE0LyVkLw==")
        else:
            url=base64.b64decode("aHR0cDovL2pweG1sLmphZG9vdHYuY29tL3Z1eG1sLnBocC9qYWRvb3htbC9pdGVtcy8xMzE1LyVkLw==")

        pageIndex=0
        try:
            while True:
                newUrl=url%pageIndex
                pageIndex+=24
                req = urllib2.Request(newUrl)
                req.add_header('User-Agent', base64.b64decode('VmVyaXNtby1CbGFja1VJ'))
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                totalcountPattern='<totalitems>(.*?)<'
                totalcount =int(re.findall(totalcountPattern,link)[0])
                
                #match =re.findall(main_ch,link)[0]
                matchtemp =re.findall(patt,link)
                for cname,curl,imgurl in matchtemp:
                    match.append((cname,'plus',curl,imgurl))
                #match+=matchtemp
                if pageIndex>totalcount:
                    break
        except: pass

  
    if 1==2 and usev4:#new v4 links
        try:
                      
            url=base64.b64decode(v4link)
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36')
            req.add_header('Pragma', 'no-cache')
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            #print link

            if '<section_name>' in link:
                link =re.findall(main_ch,link)[0]
                
            match_temp=re.findall(v4patt,link)
            #print 'match_temp',match_temp

            for cid,cname,ctype,curl in match_temp:
                ctype=base64.b64decode('aHR0cDovL3N0YWdpbmcuamVtdHYuY29tL3FhLnBocC8yXzQvZ3htbC9wbGF5LyVz')%ctype.split('/play/')[1]
                match.append((cname + ' v4',ctype,ctype,''))

            #match +=re.findall(patt,match_temp)
        except: pass
         
    if 1==2:#stop for time being
        try:
            patt='<channel><channel_number>.*?<channel_name>(.+?[^<])</channel_name><channel_type>(.+?)</channel_type>.*?[^<"]<channel_url>(.+?[^<])</channel_url>.*?</channel>'
            patt='<item>.*?<id>(.*?)</id>.*?<name>(.*?)<.*?<link>(.*?)<.*?channel_logo>(.*?)<'  
            main_ch='(<items>.*?Pakistani.*?<\/items>)'
            url=base64.b64decode("aHR0cDovL2ZlcnJhcmlsYi5qZW10di5jb20vaW5kZXgucGhwL3htbC90aWVyMi8yLzEvVVMvc3M=")
            req = urllib2.Request(url)
            req.add_header('User-Agent', base64.b64decode('VmVyaXNtby1CbGFja1VJ'))
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            
            match_temp =re.findall(main_ch,link)[0]
            print 'match_temp',match_temp
            match_temp=re.findall(patt,match_temp)
            for id,cname,curl,iurl in match_temp:
                match.append((cname,'',curl,iurl))

            match +=re.findall(patt,match_temp)
        except: pass
        
    if 1==1:#stop for time being
        if cctype==1:
            if 1==2:
                match.append(('Ary digital','manual','cid:475',''))
                match.append(('Ary digital','manual','cid:981',''))
                match.append(('Ary digital Europe','manual','cid:587',''))
                match.append(('Ary digital World','manual','cid:589',''))
                match.append(('Ary News','manual','cid:474',''))
                match.append(('Ary News World','manual','cid:591',''))
                match.append(('Express News','manual','cid:275',''))
                match.append(('Express News','manual','cid:788',''))
                match.append(('Express Entertainment','manual','cid:260',''))
                match.append(('Express Entertainment','manual','cid:793',''))

            match.append(('ETV Urdu','manual','etv',''))
            match.append(('Ary Zindagi (website)','manual',base64.b64decode('aHR0cDovL2xpdmUuYXJ5emluZGFnaS50di8='),base64.b64decode('aHR0cDovL3d3dy5hcnl6aW5kYWdpLnR2L3dwLWNvbnRlbnQvdXBsb2Fkcy8yMDE0LzEwL0ZpbmFsLWxvZ28tMi5naWY=')))
            match.append(('Ary News (website)','manual',base64.b64decode('aHR0cDovL2xpdmUuYXJ5bmV3cy50di8='),base64.b64decode('aHR0cDovL2FyeW5ld3MudHYvZW4vd3AtY29udGVudC91cGxvYWRzLzIwMTQvMDYvZmluYWwuZ2lm')))
            match.append(('Ary Music (website)','manual',base64.b64decode('aHR0cDovL2xpdmUuYXJ5bXVzaWsudHYv'),base64.b64decode('aHR0cDovL2FyeW11c2lrLnR2L3dwLWNvbnRlbnQvdXBsb2Fkcy8yMDE0LzA4L2FyeW11c2lrLWxvZ28xLnBuZw==')))
            match.append(('Ary Digital (website)','manual',base64.b64decode('aHR0cDovL2xpdmUuYXJ5ZGlnaXRhbC50di8='),base64.b64decode('aHR0cDovL3d3dy5hcnlkaWdpdGFsLnR2L3dwLWNvbnRlbnQvdXBsb2Fkcy8yMDE0LzEyL2RpZ2l0YWwtbG9nby5naWY=')))
            match.append(('QTV (website)','manual',base64.b64decode('aHR0cDovL2xpdmUuYXJ5cXR2LnR2Lw=='),base64.b64decode('aHR0cDovL2FyeXF0di50di93cC1jb250ZW50L3VwbG9hZHMvMjAxNC8xMi9hcnktcXR2LTEtY29weS5qcGc=')))
            
            match.append((base64.b64decode('RHVueWEgKHdlYnNpdGUp'),'manual',base64.b64decode('aHR0cDovL2ltb2IuZHVueWFuZXdzLnR2OjE5MzUvbGl2ZS9zbWlsOnN0cmVhbS5zbWlsL3BsYXlsaXN0Lm0zdTg='),''))
            match.append((base64.b64decode('TmV3cyBvbmUgKHdlYnNpdGUp'),'manual','direct:'+base64.b64decode('aHR0cDovL2Nkbi5lYm91bmQudHYvdHYvbmV3c29uZS9wbGF5bGlzdC5tM3U4'),''))

            match.append((base64.b64decode('V2FzZWViICh3ZWJzaXRlKQ=='),'manual','direct:'+base64.b64decode('aHR0cDovL2Nkbi5lYm91bmQudHYvdHYvd2FzZWIvcGxheWxpc3QubTN1OA=='),''))

           
            
            
            match.append((base64.b64decode('Q2FwaXRhbCAod2Vic2l0ZSk='),'manual',base64.b64decode('ZWJvdW5kOmNhcGl0YWx0dg=='),''))
            match.append((base64.b64decode('RGF3biBuZXdzICh3ZWJzaXRlKQ=='),'manual',base64.b64decode('ZWJvdW5kOmRhd24='),''))
            match.append((base64.b64decode('Qm9sIHYy'),'manual',base64.b64decode('cHYyOkJvbCBOZXdz'),''))
            match.append((base64.b64decode('R2VvIE5ld3MgdjI='),'manual',base64.b64decode('cHYyOkdlbyBOZXdz'),''))
            match.append((base64.b64decode('R2VvIEVudGVydGFpbm1lbnQgdjI='),'manual',base64.b64decode('cHYyOkdlbyBFbnRlcnRhaW5tZW50'),''))
                        
            match.append((base64.b64decode('R2VvIEthaGFuaSB2Mg=='),'manual',base64.b64decode('cHYyOkdlbyBrYWhhbmk='),''))
            match.append((base64.b64decode('R2VvIFRleiB2Mg=='),'manual',base64.b64decode('cHYyOkdlbyB0ZXp6'),''))
            match.append((base64.b64decode('S1ROIHYy'),'manual',base64.b64decode('cHYyOktUTg=='),''))
            match.append((base64.b64decode('S1ROIE5FV1MgdjI='),'manual',base64.b64decode('cHYyOktUTiBORVdT'),''))
            
            match.append((base64.b64decode('S1ROIEVudC4gKHdlYnNpdGUp'),'manual','direct:'+"rtmp://103.24.96.74/ktn/ playpath=ktn swfUrl=http://ktntv.tv/wp-content/player/jwplayer.flash.swf pageUrl=http://www.ktntv.tv/ live=1",''))
            match.append((base64.b64decode('S1ROIE5FV1MgKHdlYnNpdGUp'),'manual','direct:'+"rtmp://103.24.96.74/ktn/ playpath=ktnnews swfUrl=http://ktntv.tv/wp-content/player/jwplayer.flash.swf pageUrl=http://www.ktnnews.tv/ live=1",''))
            match.append(('Makkah (youtube)','manual','','direct:plugin://plugin.video.youtube/?action=play_video&videoid=%s' %'ArVmnth5jB4'))
            match.append(('Madina (youtube)','manual','direct:plugin://plugin.video.youtube/?action=play_video&videoid=%s' %'4OoKpZWJASY',''))
            
  


        elif cctype==2:
            print 'no'
#            match.append(('Color','manual','cid:316',''))

        
#    match.append((base64.b64decode('U2t5IFNwb3J0IDE='),'manual',base64.b64decode('aHR0cDovL2pweG1sLmphZG9vdHYuY29tL3Z1eG1sLnBocC9qYWRvb3htbC9wbGF5LzMxNg=='),''))
     
#    match.append((base64.b64decode('U2t5IFNwb3J0IDI='),'manual',base64.b64decode('aHR0cDovL2pweG1sLmphZG9vdHYuY29tL3Z1eG1sLnBocC9qYWRvb3htbC9wbGF5LzMyNg=='),''))
#    match.append((base64.b64decode('U2t5IFNwb3J0IDM='),'manual',base64.b64decode('aHR0cDovL215amFkb290di5qYWRvb3R2LmNvbS9qbWFya3MvYm94L3BsYXlWaWRlby5waHA/cGxheVVybD1ydG1wOi8vcXVpbnplbGl2ZWZzLmZwbGl2ZS5uZXQvcXVpbnplbGl2ZS1saXZlL3NreXNwb3J0czMuc3RyZWFtP3NlY3VyaXR5dHlwZT0y'),''))
#    match.append((base64.b64decode('U2t5IFNwb3J0IDQ='),'manual',base64.b64decode('aHR0cDovL2pweG1sLmphZG9vdHYuY29tL3Z1eG1sLnBocC9qYWRvb3htbC9wbGF5LzMxNQ=='),''))
#    match.append((base64.b64decode('U2t5IFNwb3J0IDU='),'manual',base64.b64decode('aHR0cDovL215amFkb290di5qYWRvb3R2LmNvbS9qbWFya3MvYm94L3BsYXlWaWRlby5waHA/cGxheVVybD1ydG1wOi8vcXVpbnplbGl2ZWZzLmZwbGl2ZS5uZXQvcXVpbnplbGl2ZS1saXZlL3NreXNwb3J0czUuc3RyZWFtP3NlY3VyaXR5dHlwZT0y'),''))


    pg=None
    iptvgen=None
    ptcgen=None
    paktvgen=None
    unitvgen=None
    wtvgen=None
    dittogen=None
    CFgen=None
    ipBoxGen=None
    UKTVGenCat=[]
    UKTVGenCH=[]

    if cctype==1:
        pg='pakistan'
        iptvgen="pakistani"
        ptcgen=['News','Entertainment','Islamic','Cooking']
        paktvgen=['News','Islamic','Cooking']
        unitvgen=['News','Religious','Cooking','PAK&IND']
        wtvgen=['News','Religious','Cooking','Asian News','Entertainment']
        CFgen="4"
        YPgen=base64.b64decode("aHR0cDovL3d3dy55dXBwdHYuY29tL3VyZHUtdHYuaHRtbA==")
        UKTVGenCat,UKTVGenCH=['religious','news','food'], ['masala tv', 'ary digital', 'ary zindagi','hum tv','drama','express ent.']

    elif cctype==2:
        pg='indian'
        iptvgen="indian"
        ptcgen=['Indian']
        dittogen="ind"
        CFgen="6"
        ipBoxGen=1
        YPgen=base64.b64decode("aHR0cDovL3d3dy55dXBwdHYuY29tL2hpbmRpLXR2Lmh0bWw=")
        UKTVGenCat,UKTVGenCH=['movies'],['zee tv','colors','sony tv hd', 'star plus hd', 'zee tv']
    else:
        pg='punjabi'
        CFgen="1314"
        YPgen=base64.b64decode("aHR0cDovL3d3dy55dXBwdHYuY29tL3B1bmphYmktdHYuaHRtbA==")
        
    
    if isv3Off=='true': pg=None
    if isv5Off=='true': iptvgen=None
    if isv6Off=='true': ptcgen=None
    if isv7Off=='true': paktvgen=None
    if isv8Off=='true': unitvgen=None
    if isv9Off=='true': wtvgen=None
    if isdittoOff=='true': dittogen=None
    if isCFOff=='true': CFgen=None    
    if isIpBoxff=='true': ipBoxGen=None
    if isYPgenOff=='true': YPgen=None
    if isUKTVOff=='true': 
        UKTVGenCat=[]
        UKTVGenCH=[]

    if pg:
        try:
#            print 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx'
            progress.update( 20, "", "Loading v3", "" )
            xmldata=getPV2Url()
            sources=etree.fromstring(xmldata)
            ret=[]
            for source in sources.findall('items'):
                #print pg,source.findtext('programCategory').lower()
                if pg == source.findtext('programCategory').lower():
                    cname=source.findtext('programTitle')
                    cid=source.findtext('programURL')
                    cimage=source.findtext('programImage')
#                    addDir(cname ,base64.b64encode(cid),37,cimage, False, True,isItFolder=False)
                    match.append((cname +' v3' ,'manual2', cid ,cimage))
            
        except:
            traceback.print_exc(file=sys.stdout)

    if ptcgen:
        try:
            progress.update( 60, "", "Loading v6 Channels", "" )
            rematch=getptcchannels(ptcgen)
            if len(rematch)>0:
                match+=rematch
        except:
            traceback.print_exc(file=sys.stdout)        

    if paktvgen:
        try:
            progress.update( 70, "", "Loading v7 Channels", "" )
            rematch=getPakTVChannels(paktvgen)
            if len(rematch)>0:
                match+=rematch
        except:
            traceback.print_exc(file=sys.stdout)                

    if unitvgen:
        try:
            progress.update( 80, "", "Loading v8 Channels", "" )
            rematch=getUniTVChannels(unitvgen)
            if len(rematch)>0:
                match+=rematch
        except:
            traceback.print_exc(file=sys.stdout)   

    if wtvgen:
        try:
            progress.update( 80, "", "Loading v9 Channels", "" )
            rematch=getWTVChannels(wtvgen)
            if len(rematch)>0:
                match+=rematch
        except:
            traceback.print_exc(file=sys.stdout)   
            
    if dittogen:
        try:
            
            progress.update( 85, "", "Loading ditto Channels", "" )
            rematch=getDittoChannels(dittogen)
            if len(rematch)>0:
                match+=rematch
        except:
            traceback.print_exc(file=sys.stdout)     
    if CFgen:
        try:
            
            progress.update( 82, "", "Loading CF Channels", "" )
            rematch=getCFChannels(CFgen)
            if len(rematch)>0:
                match+=rematch
        except:
            traceback.print_exc(file=sys.stdout)   
    if len(UKTVGenCat)>0 or len(UKTVGenCH)>0:
        try:
            
            progress.update( 82, "", "Loading uktv Channels", "" )
            rematch=getUKTVChannels(UKTVGenCat,UKTVGenCH )
            if len(rematch)>0:
                match+=rematch
        except:
            traceback.print_exc(file=sys.stdout)          
    if YPgen:
        try:
            
            progress.update( 87, "", "Loading YP Channels", "" )
            
            rematch=getYPChannels(YPgen,progress)
            progress.update( 87, "", "Loading YP Channels loaded", "" )
            if len(rematch)>0:
                match+=rematch
        except:
            traceback.print_exc(file=sys.stdout)     
            
    if ipBoxGen:
        try:
            
            progress.update( 90, "", "Loading IpBox Channels", "" )
            for nm,url in getIpBoxSources():
                rematch=getIpBoxChannels([url])
                if len(rematch)>0:
                    match+=rematch
        except:
            traceback.print_exc(file=sys.stdout)

#    match=sorted(match,key=itemgetter(0)   )
    if len(eboundMatches)>0:
        match+=eboundMatches
    match=sorted(match,key=lambda s: s[0].lower()   )
    for cname,ctype,curl,imgurl in match:
        if 1==1:#ctype=='liveWMV' or ctype=='manual':
#            print curl
            #if ctype<>'': cname+= '[' + ctype+']'
            if isv3Off and curl.startswith('pv2:'):
                continue
            cname=cname.encode('ascii', 'ignore').decode('ascii')
            if ctype.startswith('ebmode:'):
                ctype=ctype.split(':')[1]
                addDir(Colored(cname.capitalize(),'EB') ,curl ,ctype,imgurl, False, True,isItFolder=False)
            else:            
                
                if ctype=='manual2':
                    mm=37
                elif ctype=='manual3':
                    mm=45
                else:
                    mm=11
                cc='green'
                if cname.endswith('v3'):
                    cc='green'
                elif cname.lower().endswith('ipbox'):
                    cc='ffcc00cc'
                elif cname.endswith('v6'):
                    cc='red'
                elif cname.endswith('v7'):
                    cc='orange'
                elif cname.endswith('v8'):
                    cc='purple'
                elif cname.lower().endswith(' ditto'):
                    cc='green'
                elif cname.lower().endswith(' cf'):
                    cc='blue'                
                elif cname.lower().endswith(' yp'):
                    cc='ffdc00cc'                
                elif cname.lower().endswith(' uktv'):
                    cc='ffdc1111'
                addDir(Colored(cname.capitalize(),cc) ,base64.b64encode(curl) ,mm ,imgurl, False, True,isItFolder=False)		#name,url,mode,icon
    return    
    
def addiptvSports(url):

    match=getiptvchannels('sports')
    match=sorted(match,key=lambda s: s[0].lower()   )
    
    for cname,ctype,curl,imgurl in match:
        mm=45
        cname=cname.encode('ascii', 'ignore').decode('ascii')
        addDir(cname,base64.b64encode(curl) ,mm ,imgurl, False, True,isItFolder=False)		#name,url,mode,icon

def re_me(data, re_patten):
    match = ''
    m = re.search(re_patten, data)
    if m != None:
        match = m.group(1)
    else:
        match = ''
    return match

def revist_dag(page_data):
    final_url = ''
    if '127.0.0.1' in page_data:
        final_url = re_me(page_data, '&ver_t=([^&]+)&') + ' live=true timeout=15 playpath=' + re_me(page_data, '\\?y=([a-zA-Z0-9-_\\.@]+)')
    if re_me(page_data, 'token=([^&]+)&') != '':
        final_url = final_url + '?token=' + re_me(page_data, 'token=([^&]+)&')
    elif re_me(page_data, 'wmsAuthSign%3D([^%&]+)') != '':
        final_url = re_me(page_data, '&ver_t=([^&]+)&') + '?wmsAuthSign=' + re_me(page_data, 'wmsAuthSign%3D([^%&]+)') + '==/mp4:' + re_me(page_data, '\\?y=([^&]+)&')
    else:
        final_url = re_me(page_data, 'HREF="([^"]+)"')

    if 'dag1.asx' in final_url:
        return get_dag_url(final_url)

    if 'devinlivefs.fplive.net' not in final_url:
        final_url = final_url.replace('devinlive', 'flive')
    if 'permlivefs.fplive.net' not in final_url:
        final_url = final_url.replace('permlive', 'flive')



    return final_url
    
def get_ferrari_url(page_data,progress):


#    print 'get_dag_url2',page_data
    if not page_data.startswith('http'):
        return page_data;
    page_data2=getUrl(page_data);
#    print 'page_data2',page_data2
    patt='(http.*)'
    patt2='adsid=(.*?)&'    
    
    if 'ams.jadootv.info' in page_data2:
        page_data2=re.compile(patt).findall(page_data2)[0]
        page_data2=getUrl(page_data2);
#        page_data2=re.compile(patt).findall(page_data2)[0]
        headers=[('User-Agent','Ipad')]
        page_data2=getUrl(page_data,headers=headers);
#        print 'iam here',page_data2
        

    if 'adsid=' in page_data2:
        page_data2=re.compile(patt).findall(page_data2)[0]
        page_data=page_data2;
    elif 'ttl=' in page_data2:
        page_data2=re.compile(patt).findall(page_data2)[0]
        return page_data2
        page_data=page_data2;        
        patt2='ttl=(.*?)&'
    else:
        return page_data+'|User-Agent=iPad'
        
    progress.update( 30, "", "Found Ads", "" )
    import uuid
    playback=str(uuid.uuid1()).upper()   
    i=0
    addval=0
    opener = urllib2.build_opener(NoRedirection)

    adsid=re.compile(patt2).findall(page_data)[0]
#    print 'adsid',adsid
    adsidnew=int(adsid)-20000000
    page_data=page_data.replace(adsid,str(adsidnew))
    from datetime import datetime
    t1 = datetime.now()
    while i<1:      
        if not 'EXT-X-DISCONTINUITY' in page_data2:
#            print page_data
            page_data2=getUrl(page_data);
#            print page_data2
            links=re.compile(patt).findall(page_data2)
 #           print links
            headers=[('X-Playback-Session-Id',playback)]
            for l in links:
                addval+=1;
                progress.update( 30+addval*5, "", "Fetching Ads links #" + str(addval), "" )
                try:
                        if 1==1 or 'getDataTracker' in l:
#                            print 'playing the link'+l
                            #page_datatemp=getUrl(l,headers=headers);

                            response = opener.open(l)
                            
                except: traceback.print_exc(file=sys.stdout)

        else:
            break
        i+=1
    t2 = datetime.now()
    delta = t2 - t1
#    timetowait=18000-(delta.seconds*1000)
#    progress.update( 90, "", "wait for "+ str(timetowait/1000) , "" )
    #xbmc.sleep(timetowait)
    progress.update( 90, "", "Almost completed" , "" )
    print 'work done here '+page_data
    
    if 'elasticbeanstalk.com' in page_data:
        try:
            opener = urllib2.build_opener(NoRedirection)
            print 'page_data go',page_data
            opener.addheaders = [('User-agent', 'iPad')]
            response = opener.open(page_data)
            
            redir = response.info().getheader('Location')
            if 'hwcdn.net/' in redir:
                page_data=base64.b64decode('aHR0cDovL2FtczIuamFkb28udHYv')+redir.split(base64.b64decode('aHdjZG4ubmV0Lw=='))[1]
        except: pass
        
    return page_data+'|User-Agent=iPad&X-Playback-Session-Id='+playback
    
def get_dag_url(page_data):
#    print 'get_dag_url',page_data
    if '127.0.0.1' in page_data:
        return revist_dag(page_data)
    elif re_me(page_data, 'wmsAuthSign%3D([^%&]+)') != '':
        final_url = re_me(page_data, '&ver_t=([^&]+)&') + '?wmsAuthSign=' + re_me(page_data, 'wmsAuthSign%3D([^%&]+)') + '==/mp4:' + re_me(page_data, '\\?y=([^&]+)&')
    else:
        final_url = re_me(page_data, 'href="([^"]+)"[^"]+$')
        if len(final_url)==0:
            final_url=page_data
    final_url = final_url.replace(' ', '%20')

    return final_url

def getPTCAuth():
    req = urllib2.Request( base64.b64decode("aHR0cDovL3N0cmVhbWZsYXJlLmNvbS9pb3MvaWFwcC5waHA="))
    req.add_header('Authorization', "Basic %s"%base64.b64decode('WVhWMGFIVnpaWEk2ZW1OVFpUSjNaWEk9')) 
    req.add_header(base64.b64decode("VXNlci1BZ2VudA=="),base64.b64decode("UGFrJTIwVFYlMjBDb25uZWN0aWZ5LzQuMyBDRk5ldHdvcmsvNzU4LjAuMiBEYXJ3aW4vMTUuMC4w")) 
    response = urllib2.urlopen(req)
    link=response.read()
    return link


def getPTCUrl():
    fname='ptcpage.json'
    fname=os.path.join(profile_path, fname)
    try:
        jsondata=getCacheData(fname,2*60*60)
        if not jsondata==None:
            return jsondata
    except:
        print 'file getting error'
        traceback.print_exc(file=sys.stdout)

    req = urllib2.Request( base64.b64decode('aHR0cDovL2NsdW9kYmFja2VuZGFwaS5hcHBzcG90LmNvbS9pb3MvcGFrdHYvcGFrdHYuanNvbg==') )      
    req.add_header(base64.b64decode("VXNlci1BZ2VudA=="),base64.b64decode("UGFrJTIwVFYlMjBDb25uZWN0aWZ5LzQuMyBDRk5ldHdvcmsvNzU4LjAuMiBEYXJ3aW4vMTUuMC4w")) 
    response = urllib2.urlopen(req)
    link=response.read()
    maindata=json.loads(link)
    print maindata
    decodeddata=maindata["Secret"]
    #decodeddata='ew0KDQogI'.join(decodeddata.split('ew0KDQogI')[:-1])
    #data=base64.b64decode(decodeddata)[:-1]
    decodeddata=decodeddata.replace('nbUioPLk6nbviOP0kjgfreWEur','')
    decodeddata=decodeddata+'='*(len(decodeddata) % 4)
    try:
        data=base64.b64decode(decodeddata)
        jsondata= json.loads(data)
    except:
        if '"categoryName":"appsetting"' in data:
            data=data.split('"categoryName":"appsetting"')[0]
            print 'xxxxxxxxxxxxxxxxx',data[-100:]
            print 'xxxxxxxxxxxxxxxxx end'
            pos = data.rfind(',')
            data=data[:pos]
            pos = data.rfind(',')
            data=data[:pos]
            data+=']}'
        else:
            pos = data.rfind(',')
            data=data[:pos]
            data+=']}]}'
        jsondata= json.loads(data)
    #print data 
    
    print jsondata
    try:
        storeCacheData(jsondata,fname)
    except:
        print 'ptc file saving error'
        traceback.print_exc(file=sys.stdout)
    return jsondata
def clearCache():

    files=[]
    fname='paktvpage.json'
    fname=os.path.join(profile_path, fname)
    files+=[fname]    

    fname='ptcpage.json'
    fname=os.path.join(profile_path, fname)
    files+=[fname]    

    fname='unitvpage.json'
    fname=os.path.join(profile_path, fname)
    files+=[fname]    
    
    fname='pv2tvpage.json'
    fname=os.path.join(profile_path, fname)
    files+=[fname]    
    fname='uktvpage.json'
    fname=os.path.join(profile_path, fname)
    files+=[fname]   
    
    fname='WTVCookieFile.lwp'
    fname=os.path.join(profile_path, fname)
    files+=[fname]  
    
    fname='wtvpage.json'
    fname=os.path.join(profile_path, fname)
    files+=[fname]       
    try:
        for cat in getMonaCats():
            fname='monapage_%s.json'%cat[0]
            fname=os.path.join(profile_path, fname)
            files+=[fname]    
    except: pass
    
    fname='monapage_.json'
    fname=os.path.join(profile_path, fname)
    files+=[fname]    
 
    fname='gtvpage.json'
    fname=os.path.join(profile_path, fname)
    files+=[fname]     
 
    fname='pitvpage.json'
    fname=os.path.join(profile_path, fname)
    files+=[fname]  
    for p in ['u','p','h']:
        fname='yptvpage_%s.json'%p
        fname=os.path.join(profile_path, fname)
        files+=[fname]       
    
    for f in files:
        try:
            delfile(f)
        except: pass

    line1 = "Cache cleared."
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1,3000  , __icon__))        
    
def delfile(fname):
    try:
        os.remove(fname)
    except: pass

def getDittoPage():
    r=[]
    try:
        html= getUrl(base64.b64decode('aHR0cDovL3d3dy5kaXR0b3R2LmNvbS9pbmRleC5waHA/cj1saXZlLXR2JTJGdmlldw=='))
        links=re.findall('liveTvs = (\[.*\])',html)[0]
        r+=eval(links)
        
    except:
        pass
    r+=eval(base64.b64decode('W3sibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDE5MiIsIm5hbWUiOidaZWUgVFYgSEQnLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDE5Mi5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDE4OSIsIm5hbWUiOicmVFYgSEQnLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDE4OS5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDE5MSIsIm5hbWUiOidaZWUgQ2luZW1hIEhEJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAxOTEuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAxOTAiLCJuYW1lIjonJlBpY3R1cmVzIEhEJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAxOTAuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAwMDMiLCJuYW1lIjonWmVlIENsYXNzaWMnLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDAwMy5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDAxMyIsIm5hbWUiOidMaXZpbmcgRm9vZHonLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDAxMy5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDE4NyIsIm5hbWUiOidabGl2aW5nJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAxODcuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAwMDUiLCJuYW1lIjonWmVlIEJ1c2luZXNzJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAwMDUuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAwMTAiLCJuYW1lIjonWmVlIE1hcmF0aGknLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDAxMC5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDE2NiIsIm5hbWUiOidaZWUgVGVsdWd1JywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAxNjYuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAxODUiLCJuYW1lIjonTWFzdGlpJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAxODUuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAxNTIiLCJuYW1lIjonRVRDJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAxNTIuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAwMDciLCJuYW1lIjonUmFqIFRWJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAwMDcuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAxNTciLCJuYW1lIjonUmFqIERpZ2l0YWwgUGx1cycsInBvc3RlciI6Imh0dHA6XC9cLzg5LjM1LjE1OC4zNFwvaW1hZ2VzX2RpdHRvXC9uZXdfaW1hZ2VzXC9saXZldHZcLzEwMTU3LmpwZyJ9LAogICAgeyJtYW51YWwiOiJtYW51YWwiLCJpZCI6IjEwMTk5IiwibmFtZSI6J0FsIEphemVlcmEnLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDE5OS5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDE5MyIsIm5hbWUiOidNYWtrYWwgVFYnLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDE5My5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDAxNCIsIm5hbWUiOidaZWUgQmFuZ2xhJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAwMTQuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAyMDMiLCJuYW1lIjonWmluZycsInBvc3RlciI6Imh0dHA6XC9cLzg5LjM1LjE1OC4zNFwvaW1hZ2VzX2RpdHRvXC9uZXdfaW1hZ2VzXC9saXZldHZcLzEwMjAzLmpwZyJ9XQ=='))
    r+=eval(base64.b64decode('W3sibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDE4MyIsIm5hbWUiOicmIFBpY3R1cmVzJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAxODMuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAxOTAiLCJuYW1lIjonJlBpY3R1cmVzIEhEJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAxOTAuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAwMDQiLCJuYW1lIjonJlRWJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAwMDQuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAxODkiLCJuYW1lIjonJlRWIEhEJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAxODkuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAwMTkiLCJuYW1lIjonMjQgR2hhbnRhJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAwMTkuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAxNTkiLCJuYW1lIjonQ1RWTiBBS0QgUGx1cycsInBvc3RlciI6Imh0dHA6XC9cLzg5LjM1LjE1OC4zNFwvaW1hZ2VzX2RpdHRvXC9uZXdfaW1hZ2VzXC9saXZldHZcLzEwMTU5LmpwZyJ9LAogICAgeyJtYW51YWwiOiJtYW51YWwiLCJpZCI6IjEwMTcxIiwibmFtZSI6J0RpdnlhIFRWJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAxNzEuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAxNTIiLCJuYW1lIjonRVRDJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAxNTIuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAwMjIiLCJuYW1lIjonSW5kaWEgMjR4NycsInBvc3RlciI6Imh0dHA6XC9cLzg5LjM1LjE1OC4zNFwvaW1hZ2VzX2RpdHRvXC9uZXdfaW1hZ2VzXC9saXZldHZcLzEwMDIyLmpwZyJ9LAogICAgeyJtYW51YWwiOiJtYW51YWwiLCJpZCI6IjEwMTYwIiwibmFtZSI6J0tvbGthdGEgVFYnLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDE2MC5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDAxMyIsIm5hbWUiOidMaXZpbmcgRm9vZHonLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDAxMy5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDE5MyIsIm5hbWUiOidNYWtrYWwgVFYnLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDE5My5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDE4NSIsIm5hbWUiOidNYXN0aWknLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDE4NS5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDE2MSIsIm5hbWUiOidSIFBsdXMnLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDE2MS5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDE1NyIsIm5hbWUiOidSYWogRGlnaXRhbCBQbHVzJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAxNTcuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAwMjUiLCJuYW1lIjonUmFqIE11c2ljJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAwMjUuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAwMTciLCJuYW1lIjonUmFqIE11c2l4JywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAwMTcuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAwMDkiLCJuYW1lIjonUmFqIE11c2l4IFRlbHVndScsInBvc3RlciI6Imh0dHA6XC9cLzg5LjM1LjE1OC4zNFwvaW1hZ2VzX2RpdHRvXC9uZXdfaW1hZ2VzXC9saXZldHZcLzEwMDA5LmpwZyJ9LAogICAgeyJtYW51YWwiOiJtYW51YWwiLCJpZCI6IjEwMDE2IiwibmFtZSI6J2FqIE5ld3MgMjR4NycsInBvc3RlciI6Imh0dHA6XC9cLzg5LjM1LjE1OC4zNFwvaW1hZ2VzX2RpdHRvXC9uZXdfaW1hZ2VzXC9saXZldHZcLzEwMDE2LmpwZyJ9LAogICAgeyJtYW51YWwiOiJtYW51YWwiLCJpZCI6IjEwMDI2IiwibmFtZSI6J1JhaiBOZXdzIEthbm5hZGEnLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDAyNi5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDAxOCIsIm5hbWUiOidSYWogTmV3cyBNYWxheWFsYW0nLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDAxOC5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDAwOCIsIm5hbWUiOidSYWogTmV3cyBUZWx1Z3UnLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDAwOC5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDAwNyIsIm5hbWUiOidSYWogVFYnLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDAwNy5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDE2MiIsIm5hbWUiOidUYWF6YSBUViAnLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDE2Mi5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDE2MyIsIm5hbWUiOidVdHRhciBCYW5nbGEgQUtEJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAxNjMuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAxNjciLCJuYW1lIjonVmlzc2EgVFYnLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDE2Ny5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDE1NCIsIm5hbWUiOidaRUUgMjQgVGFhcycsInBvc3RlciI6Imh0dHA6XC9cLzg5LjM1LjE1OC4zNFwvaW1hZ2VzX2RpdHRvXC9uZXdfaW1hZ2VzXC9saXZldHZcLzEwMTU0LmpwZyJ9LAogICAgeyJtYW51YWwiOiJtYW51YWwiLCJpZCI6IjEwMTY5IiwibmFtZSI6J1plZSBBZmxhbScsInBvc3RlciI6Imh0dHA6XC9cLzg5LjM1LjE1OC4zNFwvaW1hZ2VzX2RpdHRvXC9uZXdfaW1hZ2VzXC9saXZldHZcLzEwMTY5LmpwZyJ9LAogICAgeyJtYW51YWwiOiJtYW51YWwiLCJpZCI6IjEwMTcwIiwibmFtZSI6J1plZSBBbHdhbicsInBvc3RlciI6Imh0dHA6XC9cLzg5LjM1LjE1OC4zNFwvaW1hZ2VzX2RpdHRvXC9uZXdfaW1hZ2VzXC9saXZldHZcLzEwMTcwLmpwZyJ9LAogICAgeyJtYW51YWwiOiJtYW51YWwiLCJpZCI6IjEwMDE0IiwibmFtZSI6J1plZSBCYW5nbGEnLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDAxNC5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDE4OCIsIm5hbWUiOidaZWUgQmFuZ2xhIENpbmVtYScsInBvc3RlciI6Imh0dHA6XC9cLzg5LjM1LjE1OC4zNFwvaW1hZ2VzX2RpdHRvXC9uZXdfaW1hZ2VzXC9saXZldHZcLzEwMTg4LmpwZyJ9LAogICAgeyJtYW51YWwiOiJtYW51YWwiLCJpZCI6IjEwMDA1IiwibmFtZSI6J1plZSBCdXNpbmVzcycsInBvc3RlciI6Imh0dHA6XC9cLzg5LjM1LjE1OC4zNFwvaW1hZ2VzX2RpdHRvXC9uZXdfaW1hZ2VzXC9saXZldHZcLzEwMDA1LmpwZyJ9LAogICAgeyJtYW51YWwiOiJtYW51YWwiLCJpZCI6IjEwMTkxIiwibmFtZSI6J1plZSBDaW5lbWEgSEQnLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDE5MS5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDAwMyIsIm5hbWUiOidaZWUgQ2xhc3NpYycsInBvc3RlciI6Imh0dHA6XC9cLzg5LjM1LjE1OC4zNFwvaW1hZ2VzX2RpdHRvXC9uZXdfaW1hZ2VzXC9saXZldHZcLzEwMDAzLmpwZyJ9LAogICAgeyJtYW51YWwiOiJtYW51YWwiLCJpZCI6IjEwMTU1IiwibmFtZSI6J1plZSBLYWxpbmdhIE5ld3MnLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDE1NS5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDAzMSIsIm5hbWUiOidaZWUgS2FubmFkYScsInBvc3RlciI6Imh0dHA6XC9cLzg5LjM1LjE1OC4zNFwvaW1hZ2VzX2RpdHRvXC9uZXdfaW1hZ2VzXC9saXZldHZcLzEwMDMxLmpwZyJ9LAogICAgeyJtYW51YWwiOiJtYW51YWwiLCJpZCI6IjEwMDEwIiwibmFtZSI6J1plZSBNYXJhdGhpJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAwMTAuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAwMjAiLCJuYW1lIjonWmVlIE1QQ0cnLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDAyMC5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDAwNiIsIm5hbWUiOidaZWUgTmV3cycsInBvc3RlciI6Imh0dHA6XC9cLzg5LjM1LjE1OC4zNFwvaW1hZ2VzX2RpdHRvXC9uZXdfaW1hZ2VzXC9saXZldHZcLzEwMDA2LmpwZyJ9LAogICAgeyJtYW51YWwiOiJtYW51YWwiLCJpZCI6IjEwMTU2IiwibmFtZSI6J1plZSBQdW5qYWIgSGFyeWFuYSBIaW1hY2hhbCBQcmFkZXNoJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAxNTYuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAwMjMiLCJuYW1lIjonWmVlIFB1cnZhaXlhJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAwMjMuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAxOTQiLCJuYW1lIjonWmVlIFNhbGFhbScsInBvc3RlciI6Imh0dHA6XC9cLzg5LjM1LjE1OC4zNFwvaW1hZ2VzX2RpdHRvXC9uZXdfaW1hZ2VzXC9saXZldHZcLzEwMTk0LmpwZyJ9LAogICAgeyJtYW51YWwiOiJtYW51YWwiLCJpZCI6IjEwMDExIiwibmFtZSI6J1plZSBUYWxraWVzJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAwMTEuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAwMTUiLCJuYW1lIjonWmVlIFRhbWlsJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAwMTUuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAxNjYiLCJuYW1lIjonWmVlIFRlbHVndScsInBvc3RlciI6Imh0dHA6XC9cLzg5LjM1LjE1OC4zNFwvaW1hZ2VzX2RpdHRvXC9uZXdfaW1hZ2VzXC9saXZldHZcLzEwMTY2LmpwZyJ9LAogICAgeyJtYW51YWwiOiJtYW51YWwiLCJpZCI6IjEwMTkyIiwibmFtZSI6J1plZSBUViBIRCcsInBvc3RlciI6Imh0dHA6XC9cLzg5LjM1LjE1OC4zNFwvaW1hZ2VzX2RpdHRvXC9uZXdfaW1hZ2VzXC9saXZldHZcLzEwMTkyLmpwZyJ9LAogICAgeyJtYW51YWwiOiJtYW51YWwiLCJpZCI6IjEwMDEyIiwibmFtZSI6J1ppbmcgSW5kaWEnLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDAxMi5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDE4NyIsIm5hbWUiOidabGl2aW5nJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAxODcuanBnIn1d'))

    return r

def getYPPage(url,progress):
    

    p="u" if 'urdu' in url.lower() else 'h' if 'hindi' in url.lower() else 'p'
    
    fname='yptvpage_%s.json'%p
    fname=os.path.join(profile_path, fname)
    try:
        jsondata=getCacheData(fname,5*24*60*60)
        if not jsondata==None:
            return json.loads(jsondata)
    except:
        print 'file getting error'
        traceback.print_exc(file=sys.stdout)
        
    headers=[('User-Agent','CFUNTV/3.1 CFNetwork/758.0.2 Darwin/15.0.0Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36')]
    html= getUrl(url,headers=headers)
    links= re.findall('<a href="(.*?)".*?img.*?src="(.*?)".*?alt=\'(.*?)\'',html)
    ret=[]
    ln=0
    for l in links:
        ln+=1
        progress.update( int((ln*100)/len(links)), "", "Filtering YP links..%d of %d"%(ln, len(links) ))
        if progress.iscanceled(): return []
        if not getYPUrl(l[0])==None:
            ret+=[l]
    links=ret
    jj=json.dumps(links)
    try:
        storeCacheData(jj,fname)
    except:
        print 'yp file saving error'
        traceback.print_exc(file=sys.stdout)
    return links
 
    
def getCFPage(catId):
    headers=[('User-Agent',base64.b64decode('Q0ZVTlRWLzMuMSBDRk5ldHdvcmsvNzU4LjAuMiBEYXJ3aW4vMTUuMC4w'))]
    html= getUrl(base64.b64decode('aHR0cHM6Ly9jaW5lZnVudHYuY29tL3NtdGFsbmMvY29udGVudC5waHA/Y21kPWNvbnRlbnQmY2F0ZWdvcnlpZD0lcyZkZXZpY2U9aW9zJnZlcnNpb249MCZrZXk9Q1l4UElWRTlhZQ==')%catId,headers=headers)
    return json.loads(html)

    
def getPakTVPage():

    fname='paktvpage.json'
    fname=os.path.join(profile_path, fname)
    try:
        jsondata=getCacheData(fname,3*60*60)
        if not jsondata==None:
            return jsondata
    except:
        print 'file getting error'
        traceback.print_exc(file=sys.stdout)
    
    req = urllib2.Request( base64.b64decode('aHR0cDovL3NtYXJ0ZXJsb2dpeC5jb20vaW9zU2VjdXJlQXBwcy9QYWtUVi9WMS0zL21haW5Db250ZW50LnBocA==') )      
    req.add_header(base64.b64decode("VXNlci1BZ2VudA=="),base64.b64decode("UGFrVFYvMS4zLjAgQ0ZOZXR3b3JrLzc1OC4wLjIgRGFyd2luLzE1LjAuMA==")) 
    req.add_header(base64.b64decode("QXV0aG9yaXphdGlvbg=="),base64.b64decode("QmFzaWMgYWtGM1lURXdjenAwZHpGdWEyd3pRbUZ1UVc1Qk5qZzM=")) 
    response = urllib2.urlopen(req)
    link=response.read()
    import rc
    cryptor=rc.RNCryptor()
    d=base64.b64decode(link)    
    decrypted_data = cryptor.decrypt(d, base64.b64decode("YkFuZ3I0bDF0dGwzNTY3"))
    decrypted_data=json.loads(decrypted_data)
    dataUrl=decrypted_data[0]["dataUrl"]

    req = urllib2.Request( dataUrl)      
    req.add_header(base64.b64decode("VXNlci1BZ2VudA=="),base64.b64decode("UGFrVFYvMS4zLjAgQ0ZOZXR3b3JrLzc1OC4wLjIgRGFyd2luLzE1LjAuMA==")) 
    req.add_header(base64.b64decode("QXV0aG9yaXphdGlvbg=="),base64.b64decode("QmFzaWMgYWtGM1lURXdjenAwZHpGdWEyd3pRbUZ1UVc1Qk5qZzM=")) 
    print 'getting paktvpage'
    response = urllib2.urlopen(req)
    link=response.read()
    print 'reading paktvpage'
    d=base64.b64decode(link)    
    print 'decoded paktvpage'
    decrypted_data = cryptor.decrypt(d, base64.b64decode("YkFuZ3I0bDF0dGwzNTY3"))
    print 'decrypted paktvpage'
    #print decrypted_data
    jsondata=json.loads(decrypted_data)
    try:
        storeCacheData(jsondata,fname)
    except:
        print 'paktv file saving error'
        traceback.print_exc(file=sys.stdout)
    return jsondata
        

def getUniTVPage():
    fname='unitvpage.json'
    fname=os.path.join(profile_path, fname)
    try:
        jsondata=getCacheData(fname,1*60*60)
        if not jsondata==None:
            return jsondata
    except:
        print 'file getting error'
        traceback.print_exc(file=sys.stdout)
        
    req = urllib2.Request( base64.b64decode('aHR0cDovL3VuaXZlcnNhbHR2LmRkbnMubmV0L1VuaXZlcnNhbC1UVi1IRC9jbXMvWFZlci9nZXRDb250dFYxLTAucGhw') )      
    req.add_header(base64.b64decode("VXNlci1BZ2VudA=="),base64.b64decode("VW5pdmVyc2FsVFZIRC8xLjAgQ0ZOZXR3b3JrLzc1OC4wLjIgRGFyd2luLzE1LjAuMA==")) 
    req.add_header(base64.b64decode("QXV0aG9yaXphdGlvbg=="),base64.b64decode("QmFzaWMgYWpOMGRtVnljMkZzT21SeVFHY3diakZ2YzBBM09EWT0=")) 
    response = urllib2.urlopen(req)
    link=response.read()
    import rc
    cryptor=rc.RNCryptor()
    d=base64.b64decode(link)    
    decrypted_data = cryptor.decrypt(d, base64.b64decode("dGVsYzA5OVBAc3N3b3JkNzg2"))
    decrypted_data=json.loads(decrypted_data)
    dataUrl=decrypted_data[0]["LiveLink"]

    req = urllib2.Request( dataUrl)      
    req.add_header(base64.b64decode("VXNlci1BZ2VudA=="),base64.b64decode("VW5pdmVyc2FsVFZIRC8xLjAgQ0ZOZXR3b3JrLzc1OC4wLjIgRGFyd2luLzE1LjAuMA==")) 
    req.add_header(base64.b64decode("QXV0aG9yaXphdGlvbg=="),base64.b64decode("QmFzaWMgYWpOMGRtVnljMkZzT21SeVFHY3diakZ2YzBBM09EWT0=")) 
    response = urllib2.urlopen(req)
    link=response.read()

    d=base64.b64decode(link)    
    decrypted_data = cryptor.decrypt(d, base64.b64decode("dGVsYzA5OVBAc3N3b3JkNzg2"))
    #print decrypted_data
    jsondata=json.loads(decrypted_data)
    try:
        storeCacheData(jsondata,fname)
    except:
        print 'unitv file saving error'
        traceback.print_exc(file=sys.stdout)
    return jsondata

def getWTVPage():
    fname='wtvpage.json'
    fname=os.path.join(profile_path, fname)
    try:
        jsondata=getCacheData(fname,1*60*60)
        if not jsondata==None:
            return jsondata
    except:
        print 'file getting error'
        traceback.print_exc(file=sys.stdout)
        
    req = urllib2.Request( base64.b64decode('aHR0cDovL2lwbGlvc2FwcC5kZG5zLm5ldC9QVFYtU3BvcnRzL2Ntcy9YVmVyL0lQTC0yMDE1L2dldENvbnR0VjEtMC5waHA=') )      
    req.add_header(base64.b64decode("VXNlci1BZ2VudA=="),base64.b64decode("SW5kb1Bhay8xLjIgQ0ZOZXR3b3JrLzc1OC4wLjIgRGFyd2luLzE1LjAuMA==")) 
    req.add_header(base64.b64decode("QXV0aG9yaXphdGlvbg=="),base64.b64decode("QmFzaWMgYzNBd2NuUWtRa0J1WnpwVGREUnlVM0F3VW5Ra056ZzI=")) 
    response = urllib2.urlopen(req)
    link=response.read()
    import rc
    cryptor=rc.RNCryptor()
    d=base64.b64decode(link)    
    decrypted_data = cryptor.decrypt(d, base64.b64decode("UEBuZ0FCQXoxUEBzc3dvcmQzMjE="))
    decrypted_data=json.loads(decrypted_data)
    dataUrl=decrypted_data[0]["LiveLink"]

    req = urllib2.Request( dataUrl)      
    req.add_header(base64.b64decode("VXNlci1BZ2VudA=="),base64.b64decode("SW5kb1Bhay8xLjIgQ0ZOZXR3b3JrLzc1OC4wLjIgRGFyd2luLzE1LjAuMA==")) 
    req.add_header(base64.b64decode("QXV0aG9yaXphdGlvbg=="),base64.b64decode("QmFzaWMgYzNBd2NuUWtRa0J1WnpwVGREUnlVM0F3VW5Ra056ZzI=")) 
    response = urllib2.urlopen(req)
    link=response.read()

    d=base64.b64decode(link)    
    decrypted_data = cryptor.decrypt(d, base64.b64decode("UEBuZ0FCQXoxUEBzc3dvcmQzMjE="))
    #print decrypted_data
    jsondata=json.loads(decrypted_data)
    try:
        storeCacheData(jsondata,fname)
    except:
        print 'wtv file saving error'
        traceback.print_exc(file=sys.stdout)
    return jsondata
    
def getGTVPage():
    fname='gtvpage.json'
    fname=os.path.join(profile_path, fname)
    try:
        jsondata=getCacheData(fname,1*60*60)
        if not jsondata==None:
            return jsondata
    except:
        print 'file getting error'
        traceback.print_exc(file=sys.stdout)
        
    req = urllib2.Request( base64.b64decode('aHR0cDovL3d3dy5zb2Z0bWFnbmF0ZS5jb20vQ01TLVNlcnZlci1TcG9ydHMtVFYvWFZlci9nZXRDb250dFYxLTAucGhw') )      
    req.add_header(base64.b64decode("VXNlci1BZ2VudA=="),base64.b64decode("U3BvcnRzVFYvMS4wIENGTmV0d29yay83NTguMC4yIERhcndpbi8xNS4wLjA=")) 
    req.add_header(base64.b64decode("QXV0aG9yaXphdGlvbg=="),base64.b64decode("QmFzaWMgVFRCcU1FdEFhMEU2Y0VGd2NIVkFOamczUUVReFkzUXhiMjVCY25rPQ==")) 
    response = urllib2.urlopen(req)
    link=response.read()
    import rc
    cryptor=rc.RNCryptor()
    d=base64.b64decode(link)    
    decrypted_data = cryptor.decrypt(d, base64.b64decode("dFcxbjNsZUIzbnpANjg3QGQwbGw="))
    decrypted_data=json.loads(decrypted_data)
    dataUrl=decrypted_data[0]["LiveLink"]

    req = urllib2.Request( dataUrl)      
    req.add_header(base64.b64decode("VXNlci1BZ2VudA=="),base64.b64decode("U3BvcnRzVFYvMS4wIENGTmV0d29yay83NTguMC4yIERhcndpbi8xNS4wLjA=")) 
    req.add_header(base64.b64decode("QXV0aG9yaXphdGlvbg=="),base64.b64decode("QmFzaWMgVFRCcU1FdEFhMEU2Y0VGd2NIVkFOamczUUVReFkzUXhiMjVCY25rPQ==")) 
    response = urllib2.urlopen(req)
    link=response.read()

    d=base64.b64decode(link)    
    decrypted_data = cryptor.decrypt(d, base64.b64decode("dFcxbjNsZUIzbnpANjg3QGQwbGw="))
    #print decrypted_data
    jsondata=json.loads(decrypted_data)
    try:
        storeCacheData(jsondata,fname)
    except:
        print 'wtv file saving error'
        traceback.print_exc(file=sys.stdout)
    return jsondata
    
def getPITVPage():
    fname='pitvpage.json'
    fname=os.path.join(profile_path, fname)
    try:
        jsondata=getCacheData(fname,1*60*60)
        if not jsondata==None:
            return jsondata
    except:
        print 'file getting error'
        traceback.print_exc(file=sys.stdout)
        
    req = urllib2.Request( base64.b64decode('aHR0cDovL3NtYXJ0ZXJsb2dpeC5jb20vTmV3QXBwcy9QYWtJbmRpYVNwb3J0c0hEL1YxLTAvbWFpbkNvbnRlbnQucGhw') )      
    req.add_header(base64.b64decode("VXNlci1BZ2VudA=="),base64.b64decode("UGFrJTIwSW5kaWElMjBTcG9ydHMlMjBIRC8xLjAgQ0ZOZXR3b3JrLzc1OC4wLjIgRGFyd2luLzE1LjAuMA==")) 
    req.add_header(base64.b64decode("QXV0aG9yaXphdGlvbg=="),base64.b64decode("QmFzaWMgYWtGM1lURXdjenAwZHpGdWEyd3pRbUZ1UVc1Qk5qZzM=")) 
    response = urllib2.urlopen(req)
    link=response.read()
    import rc
    cryptor=rc.RNCryptor()
    d=base64.b64decode(link)    
    decrypted_data = cryptor.decrypt(d, base64.b64decode("YkFuZ3I0bDF0dGwzNTY3"))
    
    decrypted_data=json.loads(decrypted_data)
    dataUrl=decrypted_data[0]["dataUrl"]

    req = urllib2.Request( dataUrl)      
    req.add_header(base64.b64decode("VXNlci1BZ2VudA=="),base64.b64decode("UGFrJTIwSW5kaWElMjBTcG9ydHMlMjBIRC8xLjAgQ0ZOZXR3b3JrLzc1OC4wLjIgRGFyd2luLzE1LjAuMA==")) 
    req.add_header(base64.b64decode("QXV0aG9yaXphdGlvbg=="),base64.b64decode("QmFzaWMgYWtGM1lURXdjenAwZHpGdWEyd3pRbUZ1UVc1Qk5qZzM=")) 
    response = urllib2.urlopen(req)
    link=response.read()

    d=base64.b64decode(link)    
    decrypted_data = cryptor.decrypt(d, base64.b64decode("YkFuZ3I0bDF0dGwzNTY3"))
    
    jsondata=json.loads(decrypted_data)
    try:
        storeCacheData(jsondata,fname)
    except:
        print 'pitv file saving error'
        traceback.print_exc(file=sys.stdout)
    return jsondata
    
def getPV2Url():
    fname='pv2tvpage.json'
    fname=os.path.join(profile_path, fname)
    try:
        jsondata=getCacheData(fname,4*60*60)
        if not jsondata==None:
            return base64.b64decode(jsondata)
    except:
        print 'file getting error'
        traceback.print_exc(file=sys.stdout)


    import time
    TIME = time.time()
    second= str(TIME).split('.')[0]
    first =int(second)+int(base64.b64decode('NjkyOTY5Mjk='))
    token=base64.b64encode(base64.b64decode('JXNAMm5kMkAlcw==') % (str(first),second))
    #req = urllib2.Request( base64.b64decode('aHR0cHM6Ly9hcHAuZHlubnMuY29tL2FwcF9wYW5lbG5ldy9vdXRwdXQucGhwL3BsYXlsaXN0P3R5cGU9eG1sJmRldmljZVNuPTI0MyZ0b2tlbj0lcw==')  %token)      
    #req = urllib2.Request( base64.b64decode('https://app.dynns.com/app_panelnew/output.php/playlist?type=xml&deviceSn=pakindiahdpaid2.6&token=%s')  %token)      
    req = urllib2.Request( base64.b64decode('aHR0cHM6Ly9hcHAuZHlubnMuY29tL2FwcF9wYW5lbG5ldy9vdXRwdXQucGhwL3BsYXlsaXN0P3R5cGU9eG1sJmRldmljZVNuPTI0NCZ0b2tlbj0lcw==')  %token)      

    req.add_header('Authorization', base64.b64decode('QmFzaWMgWVdSdGFXNDZRV3hzWVdneFFBPT0=')) 
    req.add_header(base64.b64decode("VXNlci1BZ2VudA=="),base64.b64decode("dW1hci8xMjQuMCBDRk5ldHdvcmsvNzU5LjIuOCBEYXJ3aW4vMTUuMTEuMjM=")) 

    response = urllib2.urlopen(req)
    link=response.read()

    try:
        if 'items' in link:
            storeCacheData(base64.b64encode(link),fname)
    except:
        print 'unitv file saving error'
        traceback.print_exc(file=sys.stdout)
    return link

    
def getPV2Auth():
    import base64
    import time
    TIME = time.time()
    second= str(TIME).split('.')[0]
    first =int(second)+int(base64.b64decode('NjkyOTY5Mjk='))
    token=base64.b64encode(base64.b64decode('JXNAMm5kMkAlcw==') % (str(first),second))

    req = urllib2.Request( base64.b64decode('aHR0cHM6Ly9hcHAuZHlubnMuY29tL2tleXMvUGFrLnBocD90b2tlbj0=')+token)
    req.add_header('Authorization', "Basic %s"%base64.b64decode('Wkdsc1pHbHNaR2xzT2xCQWEybHpkRUJ1')) 
    req.add_header(base64.b64decode("VXNlci1BZ2VudA=="),base64.b64decode("dW1hci8xMjQuMCBDRk5ldHdvcmsvNzU5LjIuOCBEYXJ3aW4vMTUuMTEuMjM=")) 
    response = urllib2.urlopen(req)
    link=response.read()
    return link
    
def tryplay(url,listitem):    
    import  CustomPlayer,time

    player = CustomPlayer.MyXBMCPlayer()
    start = time.time() 
    #xbmc.Player().play( liveLink,listitem)
    player.play( url, listitem)
    xbmc.sleep(1000)
    while player.is_active:
        xbmc.sleep(200)
        if player.urlplayed:
            print 'yes played'
            return True
        xbmc.sleep(1000)
    print 'not played',url
    return False
                
def PlayStreamSports(url):

    urlToPlay=base64.b64decode(url)
    import math,random
    print 'urlToPlay',urlToPlay
#    servers=["OTMuMTg5LjU4LjQy","MTg1LjI4LjE5MC4xNTg=","MTc4LjE3NS4xMzIuMjEw","MTc4LjE3LjE2OC45MA=="];
    servers=["MTc4LjE3LjE2OC45MA=="]#works for sl2
    servers=["OTMuMTg5LjU4LjQy"]#works for sl5
    servers=["93.189.58.42","185.28.190.158","178.175.132.210","178.17.168.90","185.56.137.178","94.242.254.72"];
    servers=["178.17.168.90","185.28.190.158"];
    sid=int(math.floor(random.random()*len(servers)) )
    rr=7
    if urlToPlay.startswith('xgame'):
        rr=2
    progress = xbmcgui.DialogProgress()
    progress.create('Progress', 'trying server')
    
    for sr in servers:
        for s in range(1,rr):
            if progress.iscanceled(): return ""
            progress.update( s*10, "", "Server#%d"%s, "" )
            if urlToPlay.startswith('xgame'):
                newurl=base64.b64decode('cnRtcGU6Ly8lcy94bGl2ZSBwbGF5cGF0aD1tcDQ6JXNfNzIwIGNvbm49UzpjbGllbnQgY29ubj1TOjMuMS4wLjQgc3dmVXJsPWh0dHA6Ly92aWRlb3N0cmVhbS5kbi51YS92aWRlb3BhZ2UvaW1hZ2VzL1ZpZGVvUGxheWVyLnN3Zj94IHBhZ2VVcmw9aHR0cDovL3ZpZGVvc3RyZWFtLmRuLnVhL3ZpZGVvcGFnZS92aWRlb1BhZ2UucGhwPyB0aW1lb3V0PTEw')%(base64.b64decode(servers[sid]),urlToPlay)
            else:
                #newurl=base64.b64decode('cnRtcGU6Ly8lcy94bGl2ZSBwbGF5cGF0aD1yYXc6c2wlc18lcyBjb25uPVM6Y2xpZW50IGNvbm49UzozLjEuMC40IHN3ZlVybD1odHRwOi8vdmlkZW9zdHJlYW0uZG4udWEvdmlkZW9wYWdlL2ltYWdlcy9WaWRlb1BsYXllci5zd2Y/eCBwYWdlVXJsPWh0dHA6Ly92aWRlb3N0cmVhbS5kbi51YS92aWRlb3BhZ2UvdmlkZW9QYWdlLnBocD8gdGltZW91dD0xMA==')%(base64.b64decode(servers[sid]),str(s),urlToPlay)        
                newurl=base64.b64decode('cnRtcGU6Ly8lcy94bGl2ZSBwbGF5cGF0aD1yYXc6c2wlc18lcyBjb25uPVM6Y2xpZW50IGNvbm49UzozLjEuMC40IHN3ZlVybD1odHRwOi8vdmlkZW9zdHJlYW0uZG4udWEvdmlkZW9wYWdlL2ltYWdlcy9WaWRlb1BsYXllci5zd2Y/eCBwYWdlVXJsPWh0dHA6Ly92aWRlb3N0cmVhbS5kbi51YS92aWRlb3BhZ2UvdmlkZW9QYWdlLnBocD8gdGltZW91dD0xMA==')%(sr,str(s),urlToPlay)        
            listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
            print "playing stream name: " + str(name) 
            #xbmc.Player(  ).play( urlToPlay, listitem)    
            
            if tryplay(newurl,listitem):
                return
            #print 'tryplay',tt

def getiptvmac():
    import os,binascii,random
  #  binascii.b2a_hex(os.urandom(1))
#    return base64.b64decode("MDA6MUE6Nzg6OTg6NzY6NTQ="),base64.b64decode("aHR0cDovL3BvcnRhbC5pcHR2cHJpdmF0ZXNlcnZlci50dg==")
    macstring=getUrl("http://pastebin.com/raw/KWAJCTQf")
    exec("macs="+macstring)
    maccode= (random.choice(macs))

    return maccode,base64.b64decode("aHR0cDovL213MS5pcHR2NjYudHY=")
#    return maccode,base64.b64decode("aHR0cDovL3BvcnRhbC5pcHR2cHJpdmF0ZXNlcnZlci50dg==")

def playipbox(finalUrl):
    finalUrl='plugin://plugin.video.f4mTester/?name=%s&url=%s&streamtype=TSDOWNLOADER'%(name,urllib.quote_plus(finalUrl))
    
#    finalUrl='plugin://plugin.video.f4mTester/?url=%s&streamtype=HLS'%(urllib.quote_plus(finalUrl))
    xbmc.executebuiltin('XBMC.RunPlugin('+finalUrl+')') 
    
def PlayiptvLink(url):
    progress = xbmcgui.DialogProgress()
    progress.create('Progress', 'Fetching Streaming Info')
    urlToPlay=''
    i=0
    url=base64.b64decode(url)
    while urlToPlay=='' and i<3:
        try:
            i+=1
            progress.update( 20+ (i*20), "", "Finding links.. try#%d"%i, "" )
            
            cj=json.loads(url)
            import iptv
            macid,ipurl=getiptvmac()
            urlToPlay=iptv.retriveUrl(macid,ipurl,None,cj["cmd"] , cj["tmp"])
            print 'urlToPlay in loop',urlToPlay
        except:
            if i<3:
                xbmc.sleep(2000)
            pass
    
    progress.update( 90, "", "Checking if got the result?", "" )
    progress.close()
    if urlToPlay=='':
        time = 5000  #in miliseconds
        line1 = "Failed to get the playable url"
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))        
    else:     
    #    print 'urlToPlay',urlToPlay
        listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
    #    print "playing stream name: " + str(name) 
        xbmc.Player(  ).play( urlToPlay, listitem)  

def playSports365(url):
    #print ('playSports365')
    import live365
    urlToPlay=live365.selectMatch(url)
    if urlToPlay and len(urlToPlay)>0:
        listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
    #    print   "playing stream name: " + str(name) 
        xbmc.Player(  ).play( urlToPlay, listitem)  
    else:
       if RefreshResources([('live365.py','https://raw.githubusercontent.com/Shani-08/ShaniXBMCWork2/master/plugin.video.ZemTV-shani/live365.py')]):
            dialog = xbmcgui.Dialog()
            ok = dialog.ok('XBMC', 'No Links, so updated files dyamically, try again, just in case!')           
            print 'Updated files'
    return
    
def PlayPV2Link(url):

    if not mode==37:
        xmldata=getPV2Url()
        urlToPlay=re.findall(url+'..programTitle.*?programURL\\>(.*?)\\<',xmldata)[0]
    else:
        urlToPlay=base64.b64decode(url)

#    print 'urlToPlay',urlToPlay    
    urlToPlay+=getPV2Auth()
    if '|' not in urlToPlay:
        urlToPlay+='|'
    import random
    urlToPlay+='User-Agent: AppleCoreMedia/1.%s.%s (iPhone; U; CPU OS 9_3_2%s like Mac OS X; en_gb)'%(binascii.b2a_hex(os.urandom(2))[:2],binascii.b2a_hex(os.urandom(2))[:2],binascii.b2a_hex(os.urandom(2))[:3])

    try:
        if 'iptvaus.dynns.com' in urlToPlay:# quickfix
            a=urllib.urlopen('http://iptvaus.dynns.com/')
            if a.getcode()==502: #server not found
                urlToPlay=urlToPlay.replace('iptvaus.dynns.com','130.185.144.63')
    except:
        pass
#    print 'urlToPlay',urlToPlay
    listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
#    print "playing stream name: " + str(name) 
    xbmc.Player(  ).play( urlToPlay, listitem)  
    
def PlayOtherUrl ( url ):
    checkbad.do_block_check(False)
    url=base64.b64decode(url)

    if url.startswith('cid:'): url=base64.b64decode('aHR0cDovL2ZlcnJhcmlsYi5qZW10di5jb20vaW5kZXgucGhwLzJfNS9neG1sL3BsYXkvJXM=')%url.replace('cid:','')
    progress = xbmcgui.DialogProgress()
    progress.create('Progress', 'Fetching Streaming Info')
    progress.update( 10, "", "Finding links..", "" )

    direct=False
    
    
    if "ebound:" in url:
        PlayLiveLink(url.split('ebound:')[1])
        return
    if "ebound2:" in url:
        PlayEboundFromIOS(url.split('ebound2:')[1])
        return
    if "ditto:" in url:
        PlayDittoLive(url.split('ditto:')[1])
        return
    if "Sports365:" in url:
        playSports365(url.split('Sports365:')[1])
        return
    if "CF:" in url:
        PlayCFLive(url.split('CF:')[1])
        return    
    if "uktvnow:" in url:
        PlayUKTVNowChannels(url.split('uktvnow:')[1])
        return
    if "direct:" in url:
        PlayGen(base64.b64encode(url.split('direct:')[1]))
        return    
    if "ipbox:" in url:
        playipbox(url.split('ipbox:')[1])
        return
    if "YP:" in url:
        PlayYP(base64.b64encode(url.split('YP:')[1]))
        return
    if "direct2:" in url:
        PlayGen(base64.b64encode(url.split('direct2:')[1]),True)
        return
    if "ptc:" in url:
        PlayGen(base64.b64encode(url.split('ptc:')[1]+getPTCAuth()))
        return    
    if "pv2:" in url:
        PlayPV2Link(url.split('pv2:')[1])
        return    
    if url in [base64.b64decode('aHR0cDovL2xpdmUuYXJ5bmV3cy50di8='),
            base64.b64decode('aHR0cDovL2xpdmUuYXJ5emluZGFnaS50di8='),
            base64.b64decode('aHR0cDovL2xpdmUuYXJ5cXR2LnR2Lw=='),
            base64.b64decode('aHR0cDovL2xpdmUuYXJ5bXVzaWsudHYv'),
            base64.b64decode('aHR0cDovL2xpdmUuYXJ5ZGlnaXRhbC50di8=')]:
        req = urllib2.Request(url)
        req.add_header('User-Agent', base64.b64decode('TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgNi4xOyBXT1c2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzQ3LjAuMjUyNi4xMTEgU2FmYXJpLzUzNy4zNg==')) 
        response = urllib2.urlopen(req)
        link=response.read()
#        curlpatth='file: "(htt.*?)"' if 'qtv' not in url else 'file: \'(.*?)\''
        curlpatth='file: [\'"](.*?)[\'"]'
        if curlpatth.startswith('rtmp'): curlpatth+=' timeout=20'
        progress.update( 50, "", "Preparing url..", "" )
        dag_url =re.findall(curlpatth,link)[0]
    elif url=='etv':
        req = urllib2.Request(base64.b64decode('aHR0cDovL20ubmV3czE4LmNvbS9saXZlLXR2L2V0di11cmR1'))
        req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
        response = urllib2.urlopen(req)
        link=response.read()
        curlpatth='<source src="(.*?)"'
        progress.update( 50, "", "Preparing url..", "" )
        dag_url =re.findall(curlpatth,link)[0]
    elif 'dag1.asx' not in url and 'hdcast.org' not in url and '?securitytype=2' not in url and 'bernardotv.club' not in url and 'imob.dunyanews.tv' not in url:
        if '/play/' in url:
            code=base64.b64decode('MDAwNkRDODUz')+binascii.b2a_hex(os.urandom(2))[:3]
            url+=base64.b64decode('L1VTLzEv')+code
            getUrl(base64.b64decode('aHR0cDovL2ZlcnJhcmlsYi5qZW10di5jb20vaW5kZXgucGhwL3htbC9pbml0aWFsaXplLzA1LTAyLTEzMDEwNy0yNC1QT1AtNjE4LTAwMC8yLjIuMS40Lw==')+code)
        req = urllib2.Request(url)
        req.add_header('User-Agent', base64.b64decode('VmVyaXNtby1CbGFja1VJXygyLjQuNy41LjguMC4zNCk='))   

        response = urllib2.urlopen(req)
        link=response.read()
        curlpatth='<link>(.*?)<\/link>'
        progress.update( 50, "", "Preparing url..", "" )
        dag_url =re.findall(curlpatth,link)
        if '[CDATA' in dag_url:
            dag_url=dag_url.split('CDATA[')[1].split(']')[0]#
        if not (dag_url and len(dag_url)>0 ):
            curlpatth='\<ENTRY\>\<REF HREF="(.*?)"'
            dag_url =re.findall(curlpatth,link)[0]
        else:
            dag_url=dag_url[0]
    else:
        if 'hdcast.org' in url or 'bernardotv.club' in url:
            direct=True
        dag_url=url
    if '[CDATA' in dag_url:
        dag_url=dag_url.split('CDATA[')[1].split(']')[0]#

#    print 'dag_url',dag_url,name
    
    if '?securitytype=2' in url:
        opener = urllib2.build_opener(NoRedirection)
        response = opener.open(url)
        dag_url = response.info().getheader('Location')
        if '127.0.0.1' not in dag_url: 
            dag_url='rtmp://quinzelivefs.fplive.net/quinzelive-live live=true timeout=15 playpath=%s'%dag_url.split('/')[-1]
#            print 'redir dag_url',dag_url
            direct=True

 

    if 'dag1.asx' in dag_url:    
        req = urllib2.Request(dag_url)
        req.add_header('User-Agent', base64.b64decode('VmVyaXNtby1CbGFja1VJXygyLjQuNy41LjguMC4zNCk='))   
        response = urllib2.urlopen(req)
        link=response.read()
        dat_pattern='href="([^"]+)"[^"]+$'
        dag_url =re.findall(dat_pattern,link)[0]
   
        
#    print 'dag_url2',dag_url
    if direct:
        final_url=dag_url
    else:
        final_url=get_dag_url(dag_url)

    print 'final_url',final_url            
    if 'token=hw_token' in final_url:
        final_url=final_url.split('?')[0]#
        print 'final_url',final_url   
    if 'token=ec_hls_token' in final_url:
        final_url=final_url.split('?')[0]#
        print 'final_url',final_url   
        
        
#    print 'final_urlllllllllllll',final_url

    if base64.b64decode('amFkb29fdG9rZW4=') in final_url or 'elasticbeanstalk' in final_url:
        print 'In Ferari url'
        final_url=get_ferrari_url(final_url,progress)        
    progress.update( 100, "", "Almost done..", "" )
    
    if final_url.startswith('http') and 'User-Agent' not in final_url:
        final_url+='|User-Agent=Verismo-BlackUI_(2.4.7.5.8.0.34)'
        
#    print final_url
    listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
#    print "playing stream name: " + str(name) 
    xbmc.Player(  ).play( final_url, listitem)    

def AddChannelsFromEbound():
    liveURL=base64.b64decode('aHR0cDovL2Vib3VuZHNlcnZpY2VzLmNvbS9pc3RyZWFtX2RlbW8ucGhw')
    req = urllib2.Request(liveURL)
    req.add_header('User-Agent','Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    #	print link
    #	match=re.compile('<param name="URL" value="(.+?)">').findall(link)
    #	match=re.compile('<a href="(.+?)"').findall(link)
    #	match=re.compile('onclick="playChannel\(\'(.*?)\'\);">(.*?)</a>').findall(link)
    #	match =re.findall('onclick="playChannel\(\'(.*?)\'\);">(.*?)</a>', link, re.DOTALL|re.IGNORECASE)
    #	match =re.findall('onclick="playChannel\(\'(.*?)\'\);".?>(.*?)</a>', link, re.DOTALL|re.IGNORECASE)
    #	match =re.findall('<div class=\"post-title\"><a href=\"(.*?)\".*<b>(.*)<\/b><\/a>', link, re.IGNORECASE)
    #	match =re.findall('<img src="(.*?)" alt=".*".+<\/a>\n*.+<div class="post-title"><a href="(.*?)".*<b>(.*)<\/b>', link, re.UNICODE)

    match =re.findall('<a href=".*?stream=(.*?)".*?src="(.*?)" (.)', link,re.M)

    #	print match
    expressExists=False
    expressCName='express'
    arynewsAdded=False

    if not any('Express Tv' == x[0] for x in match):
        match.append(('Express Tv','express','manual'))
    if not any('Ary News' == x[0] for x in match):
        match.append(('Ary News','arynews','manual'))
    if not any('Ary Digital' == x[0] for x in match):
        match.append(('Ary Digital','aryentertainment','manual'))

    match.append(('Channel 92','channel92','manual'))##
    match.append(('mecca','mecca','manual'))##
    match.append(('madina','madina','manual'))##
    match.append(('Peace Tv','peacetv','manual'))##

    match.append(('Tehzeeb','tehzeeb','manual'))

    #added fro #oooee
    match.append(('Style 260','style360','manual'))
    match.append(('Dtv','dtv','manual'))
    match.append(('New Tv','alite','manual'))
    match.append(('Awaz Tv','awaztv','manual'))
    match.append(('Capital Tv','capitaltv','manual'))
    match.append(('Aaj News','aajnews','manual'))
    match.append(('Abb Takk','abbtakk','manual'))
    match.append(('Channel 24','channel24pk','manual'))
    match.append(('Vsh Channels','vsh','manual'))
    match.append(('TV One','tvoneglobal','manual'))
    match.append(('Paigham','paigham','manual'))
    match.append(('Vibe Tv','nvibe','manual'))
    match.append(('Times Tv','times','manual'))
    match.append(('Minhaj Tv','minhaj','manual'))
    match.append(('Jalwa','jalwa','manual'))
    match.append(('Starmax','starmax','manual'))
    match.append(('Hamdard','hamdard','manual'))
    match.append(('Desi Channel','desichannel','manual'))
    match.append(('PBN Music','pbnmusic','manual'))

    if 1==2:
        match.append(('Baby Tv','babytv','manual'))
        match.append(('Star Gold','stargold','manual'))
        match.append(('Ten Sports','tensports','manual'))
        match.append(('Discovery','discovery','manual'))
        match.append(('National Geographic','nationalgeographic','manual'))
        match.append(('Geo Entertainment','geoentertainment','manual'))
        match.append(('Geo News','geonews','manual'))
        match.append(('Geo Super','geosuper','manual'))
        match.append(('Bol News','bol','manual'))
        match.append(('Capital News','capitaltv','manual'))
        match.append(('Dawn News','dawn','manual'))##    

    match.append(('Quran TV Urdu','aHR0cDovL2lzbDEuaXNsYW00cGVhY2UuY29tL1F1cmFuVXJkdVRW','gen'))
    match.append(('Channel 24','cnRtcDovL2RzdHJlYW1vbmUuY29tOjE5MzUvbGl2ZS8gcGxheXBhdGg9Y2l0eTQyIHN3ZlVybD1odHRwOi8vZHN0cmVhbW9uZS5jb20vanAvandwbGF5ZXIuZmxhc2guc3dmIHBhZ2VVcmw9aHR0cDovL2RzdHJlYW1vbmUuY29tL2NpdHk0Mi9pZnJhbWUuaHRtbCB0aW1lb3V0PTIw','gen'))
    match.append(('QTV','cnRtcDovLzkzLjExNS44NS4xNzoxOTM1L0FSWVFUVi9teVN0cmVhbSB0aW1lb3V0PTEw','gen'))
    match.append(('SEE TV','cnRtcDovLzM2Nzc4OTg4Ni5yLm15Y2RuOTIubmV0LzM2Nzc4OTg4Ni9fZGVmaW5zdF8vIHBsYXlwYXRoPXNlZXR2IHN3ZlVybD1odHRwOi8vZHN0cmVhbW9uZS5jb20vanAvandwbGF5ZXIuZmxhc2guc3dmIHBhZ2VVcmw9aHR0cDovL2RzdHJlYW1vbmUuY29tL3NlZXR2L2lmcmFtZS5odG1sIHRpbWVvdXQ9MTA=','gen'))






    match=sorted(match,key=lambda s: s[0].lower()   )

    #name,type,url,img
    ret_match=[]
    #h = HTMLParser.HTMLParser()
    for cname in match:
        if cname[2]=='manual':
            ret_match.append((cname[0].capitalize(),'ebmode:9' ,cname[1] , cname[2]))		#name,url,mode,icon
        elif cname[2]=='gen':
             ret_match.append((cname[0].capitalize(),'ebmode:33' ,cname[1] , cname[2]))		#name,url,mode,icon
        else:
             ret_match.append((cname[0].capitalize(),'ebmode:9' ,cname[0] , cname[1]))		#name,url,mode,icon
    return ret_match
            
            
            
    #h = HTMLParser.HTMLParser()
    for cname in match:
        if cname[2]=='manual':
            addDir(Colored(cname[0].capitalize(),'EB') ,cname[1] ,9,cname[2], False, True,isItFolder=False)		#name,url,mode,icon
        elif cname[2]=='gen':
            addDir(Colored(cname[0].capitalize(),'EB') ,cname[1] ,33,cname[2], False, True,isItFolder=False)		#name,url,mode,icon
        else:
            addDir(Colored(cname[0].capitalize(),'EB') ,cname[0] ,9,cname[1], False, True,isItFolder=False)		#name,url,mode,icon

        if 1==2:
            if cname[0]==expressCName:
                expressExists=True
            if cname[0]=='arynews':
                arynewsAdded=True

    if 1==2:			
        if not expressExists:
            addDir(Colored('Express Tv','EB') ,'express' ,9,'', False, True,isItFolder=False)		#name,url,mode,icon
        if not arynewsAdded:
            addDir(Colored('Ary News','EB') ,'arynews' ,9,'', False, True,isItFolder=False)		#name,url,mode,icon
            addDir(Colored('Ary Digital','EB') ,'aryentertainment' ,9,'', False, True,isItFolder=False)		#name,url,mode,icon
        addDir(Colored('Baby Tv','EB') ,'babytv' ,9,'', False, True,isItFolder=False)		#name,url,mode,icon
        addDir(Colored('Star Gold','EB') ,'stargold' ,9,'', False, True,isItFolder=False)		#name,url,mode,icon
        addDir(Colored('Ten Sports','EB') ,'tensports' ,9,'', False, True,isItFolder=False)		#name,url,mode,icon
    return		

def Colored(text = '', colorid = '', isBold = False):
    if colorid == 'ZM':
        color = 'FF11b500'
    elif colorid == 'EB':
        color = 'FFe37101'
    elif colorid == 'bold':
        return '[B]' + text + '[/B]'
    else:
        color = colorid
        
    if isBold == True:
        text = '[B]' + text + '[/B]'
    return '[COLOR ' + color + ']' + text + '[/COLOR]'	

def convert(s):
    try:
        return s.group(0).encode('latin1').decode('utf8')
    except:
        return s.group(0)
        
def AddProgramsAndShows(Fromurl):
    CookieJar=getZemCookieJar()
    headers=[('User-Agent','Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')]
#    link=getUrl(Fromurl,cookieJar=CookieJar, headers=headers)
    try:
        link=getUrl(Fromurl,cookieJar=CookieJar, headers=headers)
    except:
        import cloudflare
        cloudflare.createCookie(Fromurl,CookieJar,'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
        link=getUrl(Fromurl,cookieJar=CookieJar, headers=headers)

    CookieJar.save (ZEMCOOKIEFILE,ignore_discard=True)
    link=link.split('<select data-placeholder="Choose a Program..."')[1].split('</select>')[0]
#    print link    
    match =re.findall('<optgroup label=\'(.*?)\'', link, re.UNICODE)
    h = HTMLParser.HTMLParser()
    #'<option value="(.*?)">(.*?)<'
    #<optgroup label='(.*?)'
    for cname in match:
        addDir(Colored(cname,'ZM'),cname ,-9,'', True,isItFolder=False)
        subprogs=link.split('<optgroup label=\'%s\''%cname)[1].split('</optgroup>')[0]
        submatch=re.findall('<option value="(.*?)">(.*?)<', subprogs, re.UNICODE)
        for csubname in submatch:
    #		tname=cname[2]#
            addDir('    '+csubname[1],mainurl+ csubname[0] ,43,'', True,isItFolder=True)
    return

    
def AddShows(Fromurl):
    #	print Fromurl
    CookieJar=getZemCookieJar()
    #	req = urllib2.Request(Fromurl)
    #	req.add_header('User-Agent','Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
    #	response = urllib2.urlopen(req)
    #	link=response.read()
    #	response.close()
    headers=[('User-Agent','Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')]
    #	link=getUrl(Fromurl,cookieJar=CookieJar, headers=headers)
    try:
        linkfull=getUrl(Fromurl,cookieJar=CookieJar, headers=headers)
    except:
        import cloudflare
        cloudflare.createCookie(Fromurl,CookieJar,'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
        linkfull=getUrl(Fromurl,cookieJar=CookieJar, headers=headers)


    #	print link
    #cloudflare.createCookie('http://www.movie25.ag/',Cookie_Jar,'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1')
    #	print "addshows"
    #	match=re.compile('<param name="URL" value="(.+?)">').findall(link)
    #	match=re.compile('<a href="(.+?)"').findall(link)
    #	match=re.compile('onclick="playChannel\(\'(.*?)\'\);">(.*?)</a>').findall(link)
    #	match =re.findall('onclick="playChannel\(\'(.*?)\'\);">(.*?)</a>', link, re.DOTALL|re.IGNORECASE)
    #	match =re.findall('onclick="playChannel\(\'(.*?)\'\);".?>(.*?)</a>', link, re.DOTALL|re.IGNORECASE)
    #	match =re.findall('<div class=\"post-title\"><a href=\"(.*?)\".*<b>(.*)<\/b><\/a>', link, re.IGNORECASE)
    #	match =re.findall('<img src="(.*?)" alt=".*".+<\/a>\n*.+<div class="post-title"><a href="(.*?)".*<b>(.*)<\/b>', link, re.UNICODE)
    CookieJar.save (ZEMCOOKIEFILE,ignore_discard=True)

    link=linkfull
    if '<div id="top-articles">' in linkfull:
        link=linkfull.split('<div id="top-articles">')[0]
        
    match =re.findall('<div class="thumbnail">\\s*<a href="(.*?)".*\s*<img class="thumb".*?src="(.*?)" alt="(.*?)"', link, re.UNICODE)
    if len(match)==0:
        match =re.findall('<div class="thumbnail">\s*<a href="(.*?)".*\s*<img.*?.*?src="(.*?)".* alt="(.*?)"', link, re.UNICODE)

    if not '/page/' in Fromurl:
        try:
            pat='\\<a href="(.*?)".*>\\s*<img.*?src="(.*?)".*\\s?.*?\\s*?<h1.*?>(.*?)<'
    #        print linkfull
            matchbanner=re.findall(pat, linkfull, re.UNICODE)
    #        print 'matchbanner',matchbanner,match
            if len(matchbanner)>0:
                match=matchbanner+match
        except: pass

        
    #	print link
    #	print match

    #	print match
    h = HTMLParser.HTMLParser()

    
    for cname in match:
        tname=cname[2]
        tname=re.sub(r'[\x80-\xFF]+', convert,tname )
        #tname=repr(tname)
        addDir(tname,cname[0] ,3,cname[1]+'|Cookie=%s'%getCookiesString(CookieJar)+'&User-Agent=Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10', True,isItFolder=False)
        

    match =re.findall('<a class="nextpostslink" rel="next" href="(.*?)">', link, re.IGNORECASE)

    if len(match)==1:
        addDir('Next Page' ,match[0] ,2,'',isItFolder=True)
    #       print match

    return

def getCookiesString(cookieJar):
    try:
        cookieString=""
        for index, cookie in enumerate(cookieJar):
            cookieString+=cookie.name + "=" + cookie.value +";"
    except: pass
    #print 'cookieString',cookieString
    return cookieString
def AddChannels():
	req = urllib2.Request(liveURL)
	req.add_header('User-Agent','Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
#	print link
#	match=re.compile('<param name="URL" value="(.+?)">').findall(link)
#	match=re.compile('<a href="(.+?)"').findall(link)
#	match=re.compile('onclick="playChannel\(\'(.*?)\'\);">(.*?)</a>').findall(link)
#	match =re.findall('onclick="playChannel\(\'(.*?)\'\);">(.*?)</a>', link, re.DOTALL|re.IGNORECASE)
#	match =re.findall('onclick="playChannel\(\'(.*?)\'\);".?>(.*?)</a>', link, re.DOTALL|re.IGNORECASE)
#	match =re.findall('<div class=\"post-title\"><a href=\"(.*?)\".*<b>(.*)<\/b><\/a>', link, re.IGNORECASE)
#	match =re.findall('<img src="(.*?)" alt=".*".+<\/a>\n*.+<div class="post-title"><a href="(.*?)".*<b>(.*)<\/b>', link, re.UNICODE)

	match =re.findall('<div class="epic-cs">\s*<a href="(.+)" rel=.*<img src="(.+)" alt="(.+)" \/>', link, re.UNICODE)

#	print match
	h = HTMLParser.HTMLParser()
	for cname in match:
		addDir(Colored(h.unescape(cname[2].replace("Watch Now Watch ","").replace("Live, High Quality Streaming","").replace("Live &#8211; High Quality Streaming","").replace("Watch Now ","")) ,'ZM'),cname[0] ,4,cname[1],False,True,isItFolder=False)		
	return	

	
	

def PlayShowLink ( url ): 
    global linkType
    #	url = tabURL.replace('%s',channelName);
#    req = urllib2.Request(url)
#    req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
#    response = urllib2.urlopen(req)
#    link=response.read()
#    response.close()
    headers=[('User-Agent','Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')]
    CookieJar=getZemCookieJar()
    link=getUrl(url,cookieJar=CookieJar, headers=headers)

    #	print url

    line1 = "Playing DM Link"
    time = 5000  #in miliseconds
    defaultLinkType=0 #0 youtube,1 DM,2 tunepk
    defaultLinkType=selfAddon.getSetting( "DefaultVideoType" ) 
    #	print defaultLinkType
    print "LT link is" + linkType
    # if linktype is not provided then use the defaultLinkType

    if linkType.upper()=="SHOWALL" or (linkType.upper()=="" and defaultLinkType=="4"):
        ShowAllSources(url,link)
        return
    if linkType.upper()=="DM" or (linkType=="" and defaultLinkType=="0"):
    #		print "PlayDM"
        line1 = "Playing DM Link"
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1,time  , __icon__))
    #		print link
        playURL= match =re.findall('src="((?:http)?.*?(dailymotion.com).*?)"',link)
        if len(playURL)==0:
            line1 = "Daily motion link not found"
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
            ShowAllSources(url,link)
            return 
        playURL=match[0][0]
        if playURL.startswith('//'):
            playURL='http:'+playURL
        print playURL
        playlist = xbmc.PlayList(1)
        playlist.clear()
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
        listitem.setInfo("Video", {"Title":name})
        listitem.setProperty('mimetype', 'video/x-msvideo')
        listitem.setProperty('IsPlayable', 'true')
        print 'playURL',playURL
        stream_url = urlresolver.HostedMediaFile(playURL).resolve()
        print stream_url
        playlist.add(stream_url,listitem)
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(playlist)
        #xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
        #src="(.*?(dailymotion).*?)"
    elif  linkType.upper()=="EBOUND"  or (linkType=="" and defaultLinkType=="3"):
        line1 = "Playing Ebound Link"
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
    #		print "Eboundlink"
        playURL= match =re.findall(' src=".*?ebound\\.tv.*?site=(.*?)&.*?date=(.*?)\\&', link)
        if len(playURL)>0:
            playURL=match[0]
            dt=playURL[1]
            clip=playURL[0]
            urli=base64.b64decode('aHR0cDovL3d3dy5lYm91bmRzZXJ2aWNlcy5jb20vaWZyYW1lL25ldy92b2RfdWdjLnBocD9zdHJlYW09bXA0OnZvZC8lcy8lcyZ3aWR0aD02MjAmaGVpZ2h0PTM1MCZjbGlwPSVzJmRheT0lcyZtb250aD11bmRlZmluZWQ=')%(dt,clip,clip,dt)
            #req = urllib2.Request(urli)
            #req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
            #response = urllib2.urlopen(req)
            #link=response.read()
            #response.close()
            post = {'username':'hash'}
            post = urllib.urlencode(post)
            req = urllib2.Request(base64.b64decode('aHR0cDovL2Vib3VuZHNlcnZpY2VzLmNvbS9mbGFzaHBsYXllcmhhc2gvaW5kZXgucGhw'))
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36')
            response = urllib2.urlopen(req,post)
            link=response.read()
            response.close()
            strval =link;# match[0]
            stream_url=base64.b64decode('cnRtcDovL2Nkbi5lYm91bmQudHYvdm9kIHBsYXlwYXRoPW1wNDp2b2QvJXMvJXMgYXBwPXZvZD93bXNBdXRoU2lnbj0lcyBzd2Z1cmw9aHR0cDovL3d3dy5lYm91bmRzZXJ2aWNlcy5jb20vbGl2ZS92Ni9wbGF5ZXIuc3dmP2RvbWFpbj13d3cuemVtdHYuY29tJmNoYW5uZWw9JXMmY291bnRyeT1FVSBwYWdlVXJsPSVzIHRjVXJsPXJ0bXA6Ly9jZG4uZWJvdW5kLnR2L3ZvZD93bXNBdXRoU2lnbj0lcyBsaXZlPXRydWUgdGltZW91dD0xNQ==')%(dt,clip,strval,clip,urli,strval)
        else:
            playURL=match=re.findall('src="(.*?(poovee\.net).*?)"', link)
            
            if len(playURL)==0:
                line1 = "EBound/Povee link not found"
                xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
                ShowAllSources(url,link)
                return 
            playURL=match[0][0]
            pat='<source src="(.*?)"'
            link=getUrl(playURL,cookieJar=CookieJar, headers=headers)
            playURL=re.findall(pat, link)
            stream_url=playURL[0]
        playlist = xbmc.PlayList(1)
        playlist.clear()
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
        listitem.setInfo("Video", {"Title":name})
        listitem.setProperty('mimetype', 'video/x-msvideo')
        listitem.setProperty('IsPlayable', 'true')
        playlist.add(stream_url,listitem)
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(playlist)
    elif  linkType.upper()=="VIDRAIL"  or (linkType=="" and defaultLinkType=="5"):
        line1 = "Playing Vidrail Link"
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
        playURL= match =re.findall('src="(.*?(vidrail\.com).*?)"', link)
        if len(playURL)==0:
            line1 = "Vidrail link not found"
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
            ShowAllSources(url,link)
            return 

        playURL=match[0][0]
        pat='<source src="(.*?)"'
        link=getUrl(playURL,cookieJar=CookieJar, headers=headers)
        playURL=re.findall(pat, link)
        if len(playURL)==0:
            line1 = "Vidrail link not found"
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
            ShowAllSources(url,link)
            return 
        stream_url=playURL[0]
        playlist = xbmc.PlayList(1)
        playlist.clear()
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
        listitem.setInfo("Video", {"Title":name})
        listitem.setProperty('mimetype', 'video/x-msvideo')
        listitem.setProperty('IsPlayable', 'true')
#        stream_url = urlresolver.HostedMediaFile(playURL).resolve()' find here
    #		print stream_url
        playlist.add(stream_url,listitem)
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(playlist)
    elif  linkType.upper()=="LINK"  or (linkType=="" and defaultLinkType=="1"):
        line1 = "Playing Tune.pk Link"
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
    #		print "PlayLINK"
        playURL= match =re.findall('src="(.*?(tune\.pk).*?)"', link)
        if len(playURL)==0:
            line1 = "Link.pk link not found"
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
            ShowAllSources(url,link)
            return 

        playURL=match[0][0]
    #		print playURL
        playlist = xbmc.PlayList(1)
        playlist.clear()
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
        listitem.setInfo("Video", {"Title":name})
        listitem.setProperty('mimetype', 'video/x-msvideo')
        listitem.setProperty('IsPlayable', 'true')
        stream_url = urlresolver.HostedMediaFile(playURL).resolve()
    #		print stream_url
        playlist.add(stream_url,listitem)
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(playlist)
    elif  linkType.upper()=="PLAYWIRE"  or (linkType=="" and defaultLinkType=="2"):
        line1 = "Playing Playwire Link"
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
    #		print "Playwire"
        playURL =re.findall('src=".*?(playwire).*?data-publisher-id="(.*?)"\s*data-video-id="(.*?)"', link)
        V=1
        if len(playURL)==0:
            playURL =re.findall('data-config="(.*?config.playwire.com.*?)"', link)
            V=2
        if len(playURL)==0:
            line1 = "Playwire link not found"
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
            ShowAllSources(url,link)
            return 
        if V==1:
            (playWireVar,PubId,videoID)=playURL[0]
            cdnUrl=base64.b64decode("aHR0cDovL2Nkbi5wbGF5d2lyZS5jb20vdjIvJXMvY29uZmlnLyVzLmpzb24=")%(PubId,videoID)
            req = urllib2.Request(cdnUrl)
            req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            playURL =base64.b64decode("aHR0cDovL2Nkbi5wbGF5d2lyZS5jb20vJXMvJXM=")%(PubId,re.findall('src":".*?mp4:(.*?)"', link)[0])
    #			print 'playURL',playURL
        else:
            playURL=playURL[0]
            if playURL.startswith('//'): playURL='http:'+playURL
    #			print playURL            
            reg='media":\{"(.*?)":"(.*?)"'
            req = urllib2.Request(playURL)
            req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
            response = urllib2.urlopen(req)
            link=response.read()
            playURL =re.findall(reg, link)
            if len(playURL)>0:
                playURL=playURL[0]
                ty=playURL[0]
                innerUrl=playURL[1]
    #				print innerUrl
                req = urllib2.Request(innerUrl)
                req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
                response = urllib2.urlopen(req)
                link=response.read()
                reg='baseURL>(.*?)<\/baseURL>\s*?<media url="(.*?)"'
                playURL =re.findall(reg, link)[0]
                playURL=playURL[0]+'/'+playURL[1]
        playlist = xbmc.PlayList(1)
        playlist.clear()
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
        listitem.setInfo("Video", {"Title":name})
        listitem.setProperty('mimetype', 'video/x-msvideo')
        listitem.setProperty('IsPlayable', 'true')
        stream_url = playURL#urlresolver.HostedMediaFile(playURL).resolve()
    #		print 'stream_url',stream_url
        playlist.add(stream_url,listitem)
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(playlist)
        #bmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)#src="(.*?(tune\.pk).*?)"
    else:	#either its default or nothing selected
        line1 = "Playing Youtube Link"
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
        youtubecode= match =re.findall('<strong>Youtube<\/strong>.*?src=\".*?embed\/(.*?)\?.*\".*?<\/iframe>', link,re.DOTALL| re.IGNORECASE)
        if len(youtubecode)==0:
            line1 = "Youtube link not found"
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
            ShowAllSources(url,link)
            return
        youtubecode=youtubecode[0]
        uurl = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % youtubecode
    #	print uurl
        xbmc.executebuiltin("xbmc.PlayMedia("+uurl+")")

    return

def ShowAllSources(url, loadedLink=None):
	global linkType
#	print 'show all sources',url
	link=loadedLink
	if not loadedLink:
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
	available_source=[]
	playURL =re.findall('src=".*?(playwire).*?data-publisher-id="(.*?)"\s*data-video-id="(.*?)"', link)
#	print 'playURL',playURL
	if not len(playURL)==0:
		available_source.append('Playwire Source')

	playURL =re.findall('data-config="(.*?config.playwire.com.*?)"', link)
#	print 'playURL',playURL
	if not len(playURL)==0:
		available_source.append('Playwire Source')

	playURL =re.findall('src="(.*?ebound\\.tv.*?)"', link)
#	print 'playURL',playURL
	if not len(playURL)==0:
		available_source.append('Ebound Source')		
	else:
		playURL =re.findall('src="(.*?poovee\.net.*?)"', link)
		if not len(playURL)==0:
			available_source.append('Ebound Source')		
        
	playURL= match =re.findall('src="(.*?(dailymotion).*?)"',link)
	if not len(playURL)==0:
		available_source.append('Daily Motion Source')

	playURL= match =re.findall('src="(.*?(vidrail\.com).*?)"',link)
	if not len(playURL)==0:
		available_source.append('Vidrail Source')
        
	playURL= match =re.findall('src="(.*?(tune\.pk).*?)"', link)
	if not len(playURL)==0:
		available_source.append('Link Source')

	playURL= match =re.findall('<strong>Youtube<\/strong>.*?src=\".*?embed\/(.*?)\?.*\".*?<\/iframe>', link,re.DOTALL| re.IGNORECASE)
	if not len(playURL)==0:
		available_source.append('Youtube Source')

	if len(available_source)>0:
		dialog = xbmcgui.Dialog()
		index = dialog.select('Choose your stream', available_source)
		if index > -1:
			linkType=available_source[index].replace(' Source','').replace('Daily Motion','DM').upper()
#			print 'linkType',linkType
			PlayShowLink(url);

def PlayDittoLive(url):
    progress = xbmcgui.DialogProgress()
    progress.create('Progress', 'Fetching Streaming Info')
    progress.update( 10, "", "Finding links..", "" )

    req = urllib2.Request(url)
    req.add_header('Referer', base64.b64decode('aHR0cDovL3d3dy5kaXR0b3R2LmNvbS9pbmRleC5waHA/cj1saXZlLXR2L3ZpZXcmaWQ9MTAwMTk='))
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    progress.update( 50, "", "Finding links..", "" )
    try:
        import json
        data=json.loads(link)
        playfile=data["link"]+'|User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36&Referer=http://www.dittotv.com/index.php?r=live-tv/link'#+urllib.unquote(url)
    except:
    
        playlink=re.findall('source type="application/x-mpegurl"  src="(.*?)"',link)[0]
        playfile=playlink+'|User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36&Referer=http://www.dittotv.com/index.php?r=live-tv/link'#+urllib.unquote(url)
#    playfile =url+'?wmsAuthSign='+link+'|User-Agent=AppleCoreMedia/1.0.0.13A452 (iPhone; U; CPU OS 9_0_2 like Mac OS X; en_gb)'
    progress.update( 100, "", "Almost done..", "" )
    listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
    xbmc.Player(  ).play( playfile, listitem)
    return      
def PlayCFLive(url):
    progress = xbmcgui.DialogProgress()
    progress.create('Progress', 'Fetching Streaming Info')
    progress.update( 10, "", "Finding links..", "" )

    req = urllib2.Request(base64.b64decode('aHR0cHM6Ly9jaW5lZnVudHYuY29tL3NtdGFsbmMvY29udGVudC5waHA/Y21kPWRldGFpbHMmQCZkZXZpY2U9aW9zJnZlcnNpb249MCZjb250ZW50aWQ9JXMmc2lkPSZ1PWMzMjgxOTMwQHRyYnZuLmNvbQ==')%url)

    req.add_header('User-Agent', base64.b64decode('Q0ZVTlRWLzMuMSBDRk5ldHdvcmsvNzU4LjAuMiBEYXJ3aW4vMTUuMC4w'))
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    progress.update( 50, "", "Finding links..", "" )
    import json
    data=json.loads(link)
    playfile=""
    
    playfile=data[0]["HLSURL"]
    if playfile=="":
        playfile=data[0]["SamsungURL"]
    if playfile=="":
        playfile=data[0]["PanasonicURL"]
                
    playfile+='|User-Agent=AppleCoreMedia/1.0.0.13A452 (iPhone; U; CPU OS 9_0_2 like Mac OS X; en_gb)'
#    playfile =url+'?wmsAuthSign='+link+'|User-Agent=AppleCoreMedia/1.0.0.13A452 (iPhone; U; CPU OS 9_0_2 like Mac OS X; en_gb)'
    progress.update( 100, "", "Almost done..", "" )
    listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
    xbmc.Player(  ).play( playfile, listitem)
    return  

def PlayEboundFromIOS(url):
    if not url.startswith('http'):
        url='http://cdn.ebound.tv/tv/%s/playlist.m3u8'%url
    progress = xbmcgui.DialogProgress()
    progress.create('Progress', 'Fetching Streaming Info')
    progress.update( 10, "", "Finding links..", "" )

    req = urllib2.Request('http://eboundservices.com/hash/hash_app.php?code=com.maaidpk.PakTvConnectify')
    req.add_header('User-Agent', 'com.maaidpk.PakTvConnectify/4.2 CFNetwork/758.0.2 Darwin/15.0.0')
    req.add_header('Authorization','Digest username="hashapp", realm="Restricted area", nonce="5688ad3bc5566", uri="/hash/hash_app.php?code=com.maaidpk.PakTvConnectify", response="f4964251227b1c4fce0d6ffb5b707b4d", opaque="cdce8a5c95a1427d74df7acbf41c9ce0", cnonce="f4717cdf092fc347336d5cc1c756eb58", nc=00000003, qop="auth"')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    progress.update( 50, "", "Finding links..", "" )

    playfile =url+'?wmsAuthSign='+link+'|User-Agent=AppleCoreMedia/1.0.0.13A452 (iPhone; U; CPU OS 9_0_2 like Mac OS X; en_gb)'
    progress.update( 100, "", "Almost done..", "" )
    listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
    xbmc.Player(  ).play( playfile, listitem)
    return

def PlayLiveLink ( url ):
    PlayEboundFromIOS(url)
    return
    progress = xbmcgui.DialogProgress()
    progress.create('Progress', 'Fetching Streaming Info')
    progress.update( 10, "", "Finding links..", "" )
    if mode==4:
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        #print link
        #print url
        match =re.findall('"http.*(ebound).*?\?site=(.*?)"',link,  re.IGNORECASE)[0]
        cName=match[1]
        progress.update( 20, "", "Finding links..", "" )
    else:
        cName=url
    import math, random, time
    rv=str(int(5000+ math.floor(random.random()*10000)))
    currentTime=str(int(time.time()*1000))
    newURL=base64.b64decode('aHR0cDovL3d3dy5lYm91bmRzZXJ2aWNlcy5jb20vaWZyYW1lL25ldy9tYWluUGFnZS5waHA/c3RyZWFtPQ==')+cName+  '&width=undefined&height=undefined&clip=' + cName+'&rv='+rv+'&_='+currentTime
    req = urllib2.Request(newURL)
    req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    progress.update( 50, "", "Finding links..", "" )

    playfile =re.findall('videoLink =\'(.*?)\'',link)[0]
    
    progress.update( 100, "", "Almost done..", "" )
    listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
    xbmc.Player(  ).play( playfile, listitem)
    return


#print "i am here"
params=get_params()
url=None
name=None
mode=None
linkType=None

try:
	url=urllib.unquote_plus(params["url"])
except:
	pass
try:
	name=urllib.unquote_plus(params["name"])
except:
	pass
try:
	mode=int(params["mode"])
except:
	pass


args = cgi.parse_qs(sys.argv[2][1:])
linkType=''
try:
	linkType=args.get('linkType', '')[0]
except:
	pass


print 	mode,url,linkType
		
try:
	if mode==None or url==None or len(url)<1:
		print "InAddTypes"
		checkbad.do_block_check(False)
		Addtypes()
	elif mode==2 or mode==43:
		print "Ent url is ",name,url        
		AddEnteries(name, url)

	elif mode==3:
		print "Play url is "+url
		PlayShowLink(url)

	elif mode==4 or mode==9:
		print "Play url is "+url
		PlayLiveLink(url)
	elif mode==11:
		print "Play url is "+url
		PlayOtherUrl(url)

	elif mode==6 :
		print "Play url is "+url
		ShowSettings(url)
	elif mode==13 :
		print "Play url is "+url
		AddSports(url)
	elif mode==14 or mode==144:
		print "Play url is "+url
		AddSmartCric(url)
	elif mode==15 :
		print "Play url is "+url
		PlaySmartCric(url)
	elif mode==16 :
		print "Play url is "+url
		AddWatchCric(url)
	elif mode==17 :
		print "Play url is "+url
		PlayWatchCric(url)
	elif mode==19 :
		print "Play url is "+url
		AddWillowCric(url)
	elif mode==20:
		print "Play url is "+url
		AddWillSportsOldSeries(url)
	elif mode==21 or mode==22:
		print "Play url is "+url
		PlayWillowMatch(url)        
	elif mode==23:
		print "Play url is "+url
		AddWillowReplayParts(url)        
	elif mode==24:
		print "Play url is "+url
		AddWillSportsOldSeriesMatches(url)        

	elif mode==26 :
		print "Play url is "+url
		AddCricHD(url)
	elif mode==27 :
		print "Play url is "+url
		PlayCricHD(url)                
	elif mode==31 :
		print "Play url is "+url
		AddFlashtv(url)                
	elif mode==30 :
		print "Play url is "+url
		AddP3gSports(url)                
	elif mode==32 :
		print "Play url is "+url
		PlayFlashTv(url)                
	elif mode==33 :
		print "Play url is "+url
		PlayGen(url)                
	elif mode==34 :
		print "Play url is "+url
		GetSSSEvents(url)                
	elif mode==35 :
		print "Play url is "+url
		PlaySSSEvent(url)                
	elif mode==36 :
		print "Play url is "+url
		AddPv2Sports(url) 
	elif mode==37 :
		print "Play url is "+url
		PlayPV2Link(url) 

	elif mode==39 :
		print "Play url is "+url
		AddStreamSports(url) 
	elif mode==40 :
		print "Play url is "+url
		PlayStreamSports(url)         
	elif mode==41 :
		print "Play url is "+url
		AddCricFree(url) 
	elif mode==42 :
		print "Play url is "+url
		PlayCricFree(url) 
	elif mode==45 :
		print "Play url is "+url
		PlayiptvLink(url) 
	elif mode==46 :
		print "Play url is "+url
		addiptvSports(url) 
	elif mode==51 :
		print "Play url is "+url
		AddPTCSports(url) 
	elif mode==52 :
		print "Play url is "+url
		AddPakTVSports(url) 
	elif mode==53 :
		print "Play url is "+url
		AddUniTVSports(url)       
	elif mode==54 :
		print "Play url is "+url
		clearCache()
	elif mode==55 :
		print "Play url is "+url
		AddIpBoxSources(url)     
	elif mode==61 or mode==67:
		print "Play url is "+url
		AddIpBoxChannels(url)     
	elif mode==56 :
		print "Play url is 56"+url
		AddSports365Channels(url) 
	elif mode==57 :
		print "Play url is 57"+url
		AddUKTVNowChannels(url)     
	elif mode==60 :
		print "Play url is 60"+url
		AddYuppSports(url)     
	elif mode==62 :
		print "Play url is "+url
		AddWTVSports(url)
	elif mode==66 :
		print "Play url is "+url
		ShowAllCategories(url)    
	elif mode==68 :
		print "Play url is "+url
		AddMonaChannels(url)            
	elif mode==70:
		print "Play url is "+url
		AddGTVSports(url)  
	elif mode==71:
		print "Play url is "+url
		AddPITVSports(url)  
except:
	print 'somethingwrong'
	traceback.print_exc(file=sys.stdout)
	

if not ( (mode==3 or mode==4 or mode==9 or mode==11 or mode==15 or mode==21 or mode==22 or mode==27 or mode==33 or mode==35 or mode==37 or mode==40 or mode==42 or mode==45)  )  :
	if mode==144:
		xbmcplugin.endOfDirectory(int(sys.argv[1]),updateListing=True)
	else:
		xbmcplugin.endOfDirectory(int(sys.argv[1]))
