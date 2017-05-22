import xbmc, xbmcgui, xbmcplugin
import urllib2,urllib,cgi, re


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
#import ssl

overridemode=None    
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

home = xbmc.translatePath(selfAddon.getAddonInfo('path').decode('utf-8'))


WTVCOOKIEFILE='WTVCookieFile.lwp'
WTVCOOKIEFILE=os.path.join(profile_path, WTVCOOKIEFILE)
ZEMCOOKIEFILE='ZemCookieFile.lwp'
ZEMCOOKIEFILE=os.path.join(profile_path, ZEMCOOKIEFILE)
S365COOKIEFILE='s365CookieFile.lwp'
S365COOKIEFILE=os.path.join(profile_path, S365COOKIEFILE)

YPLoginFile='YpCookieFile.lwp'
YPLoginFile=os.path.join(profile_path, YPLoginFile)

HDCASTCookie='HDCastCookieFile.lwp'
HDCASTCookie=os.path.join(profile_path, HDCASTCookie)

TVPCOOKIEFILE='TVPCookieFile.lwp'
TVPCOOKIEFILE=os.path.join(profile_path, TVPCOOKIEFILE)

 
mainurl=base64.b64decode('aHR0cDovL3d3dy56ZW10di5jb20vY2F0ZWdvcnkvcGFraXN0YW5pLw==')
liveURL=base64.b64decode('aHR0cDovL3d3dy56ZW10di5jb20vbGl2ZS1wYWtpc3RhbmktbmV3cy1jaGFubmVscy8=')
viralvideos=base64.b64decode('aHR0cDovL3d3dy56ZW10di5jb20vY2F0ZWdvcnkvdmlyYWwtdmlkZW9zLw==')


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

def ShowStatus(Fromurl):
    dialog = xbmcgui.Dialog()
    ok = dialog.ok('Status',getUrl('http://pastebin.com/raw/f3EBTxM3'))
    
    
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
        cmd0 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "DMASLIVE")
        cmd2 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "LINK")
        cmd3 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "Youtube")
        cmd4 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "PLAYWIRE")
        cmd5 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "EBOUND")
        cmd6 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "PLAYWIRE")
        cmd7 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "VIDRAIL")

        
        liz.addContextMenuItems([('Show All Sources',cmd6),('Play Vidrail video',cmd7),('Play Ebound video',cmd5),('Play Playwire video',cmd4),('Play Youtube video',cmd3),('Play DailyMotion video',cmd1),('Play DailyMotion As Live video',cmd0),('Play Tune.pk video',cmd2)])
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

    #ctx = ssl.create_default_context()
    #ctx.check_hostname = False
    #ctx.verify_mode = ssl.CERT_NONE

    cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
    #opener = urllib2.build_opener(urllib2.HTTPSHandler(context=ctx),cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
    opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
    #opener = urllib2.install_opener(opener)
    header_in_page=None
    if '|' in url:
        url,header_in_page=url.split('|')
    req = urllib2.Request(url)

    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
    req.add_header('Accept-Encoding','gzip')

    if headers:
        for h,hv in headers:
            req.add_header(h,hv)
    if header_in_page:
        header_in_page=header_in_page.split('&')
        
        for h in header_in_page:
            if len(h.split('='))==2:
                n,v=h.split('=')
            else:
                vals=h.split('=')
                n=vals[0]
                v='='.join(vals[1:])
                #n,v=h.split('=')
            #print n,v
            req.add_header(n,v)
            
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

def AddtypesForShows():
    addDir('Latest Shows (ZemTv)' ,'Shows' ,2,os.path.join(home,'icons', 'ShowsfromZemTv.png'))
    addDir('Latest Shows (Siasat.pk)' ,'http://www.siasat.pk/forum/forumdisplay.php?29-Daily-Talk-Shows' ,2,os.path.join(home,'icons','Shows from Siasat.png'))
    addDir('All Programs and Talk Shows' ,'ProgTalkShows' ,2,os.path.join(home,'icons','All Programs and Talk shows.png'))
    addDir('Viral Videos (ZemTv)' ,'viralvideos' ,2,os.path.join(home,'icons', 'ShowsfromZemTv.png'))

def Addtypes():
    addDir('Pakistani Political Shows' ,'PakLive' ,29,os.path.join(home,'icons','Pakistani Political Shows.png'))
    addDir('Indian/Pakistani Shows/Dramas' ,'IndPakLive' ,83,os.path.join(home,'icons','indpakshows.png') )   
    addDir('Pakistani Live Channels' ,'PakLive' ,2,os.path.join(home,'icons','Pakistani Live Channels.png'))
    addDir('Indian Live Channels' ,'IndianLive' ,2,os.path.join(home,'icons','Indian Live Channels.png'))
    addDir('Punjabi Live Channels' ,'PunjabiLive' ,2,os.path.join(home,'icons','Punjabi Live Channels.png'))
    addDir('Movies' ,'pv2',66,os.path.join(home,'icons','Movies.png'))
    addDir('Sports' ,'Live' ,13,os.path.join(home,'icons','Sports.png'))
    try:
        import testarea
        if testarea.testenabled():
            addDir('Test Area' ,'TUFJTg==' ,99,os.path.join(home,'icons','Sports.png'))
    except: traceback.print_exc(file=sys.stdout)
    addDir('Settings' ,'Live' ,6,os.path.join(home,'icons','Settings.png'),isItFolder=False)
    addDir('Clear Cache' ,'Live' ,54,os.path.join(home,'icons','Clear Cache.png'),isItFolder=False)
    addDir(Colored('Status Report', 'red') ,'live',7,os.path.join(home,'icons','status report.png'),isItFolder=False)
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
    
    addDir('IpBox sports Using TSDownloader and HLS' ,'mpegts',55,os.path.join(home,'icons','Ipbox Sports.png'))
    addDir('Football Mania' ,'mpegts',86,os.path.join(home,'icons','football.png'))
    #addDir('IpBox sports Using HLS ' ,'hls',55,'')
    addDir('PTC sports' ,'sss',51,os.path.join(home,'icons','PTC Sports.png'))
    addDir('Paktv sports' ,'sss',52,os.path.join(home,'icons','PakTV sports.png'))
    addDir('UniTV sports' ,'sss',53,os.path.join(home,'icons','UniTV Sports.png'))
    addDir('WTV sports' ,'sss',62,os.path.join(home,'icons','WTV Sports.png'))
    #addDir('GTV sports' ,'sss',70,os.path.join(home,'icons','GTV Sports.png'))
    addDir('Pi sports' ,'sss',71,os.path.join(home,'icons','Pi Sports.png'))
    addDir('Mona' ,'sss',68,os.path.join(home,'icons','Mona.png'))
    addDir('Sport365.live' ,'sss',56,'http://s1.medianetworkinternational.com/images/icons/256x256px.png')
    addDir('SmartCric.com (Live matches only)' ,'Live' ,14,os.path.join(home,'icons','SmartCric.png'))
    addDir('UKTVNow [Limited Channels]','sss' ,57,'http://www.uktvnow.net/images/uktvnow_logo.png')
    
#    addDir('Flashtv.co (Live Channels)' ,'flashtv' ,31,'')
    addDir('Willow.Tv (Subscription required, US Only or use VPN)' ,base64.b64decode('aHR0cDovL3d3dy53aWxsb3cudHYv') ,19,os.path.join(home,'icons','willowtv.png'))
    #addDir(base64.b64decode('U3VwZXIgU3BvcnRz') ,'sss',34,'')
    addDir('My Sports' ,'sss',82,os.path.join(home,'icons','Sports.png'))
    addDir('PV2 Sports' ,'zemsports',36,os.path.join(home,'icons','PV2 Sports.png'))
    addDir('Fast TV' ,'sss',92,os.path.join(home,'icons','Fast TV.png'))
    addDir('NetTV' ,'sss',94,os.path.join(home,'icons','Nettv.png'))
    addDir('Slow TV' ,'sss',96,os.path.join(home,'icons','slowtv.png'))
    addDir('PTV Sports' ,'sss',98,os.path.join(home,'icons','slowtv.png'))

    #addDir('Safe' ,'sss',72,'')
    addDir('TVPlayer [UK Geo Restricted]','sss',74,os.path.join(home,'icons','tvplayer.png'))
    #addDir('StreamHD','sss',75,os.path.join(home,'icons','streamhd.png')) #website bust
    addDir('Mama HD','http://mamahd.com/',79,os.path.join(home,'icons','mamahd.png'))
    #addDir('HDfree','sss',77,os.path.join(home,'icons','HDFree.png'))
    addDir('inFinite Streams','sss',78,os.path.join(home,'icons','Infinite Streams.png'))
    #addDir('Euro Streams','sss',81,os.path.join(home,'icons','Euro Streams.png'))

    #addDir('Yupp Asia Cup','Live' ,60,'')
    #addDir('CricHD.tv (Live Channels)' ,'pope' ,26,'')
    #addDir('cricfree.sx' ,'sss',41,'')
    #addDir('WatchCric.com-Live matches only' ,base64.b64decode('aHR0cDovL3d3dy53YXRjaGNyaWMubmV0Lw==' ),16,'') #blocking as the rtmp requires to be updated to send gaolVanusPobeleVoKosat
   # addDir('c247.tv-P3G.Tv' ,'P3G'  ,30,'')
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
 

def getPV2Cats(movies=False):
    ret=[]
    try:
        xmldata=getPV2Url()
        sources=etree.fromstring(xmldata)
        #print xmldata
        for source in sources.findall('items'):#Cricket#
            if not source.findtext('programCategory') in ret :
                    print source.findtext('programCategory')
                    if movies==False or source.findtext('programCategory').lower().endswith('movies'):
                        ret.append(source.findtext('programCategory'))   
        if len(ret)>0:
            ret=sorted(ret,key=lambda s: s[0].lower()   )
    except:
        traceback.print_exc(file=sys.stdout)
    return ret  

def  AddEmoviesMain(url):
    dummy,url=url.split('emovies:')
    urldata=json.loads(url)
    print urldata
    if urldata["type"]=="decade":
        addEmoviesFromSearch(urldata)
    elif urldata["type"]=="search":
        if 'searchdata' not in urldata:
            userinput=xbmcgui.Dialog().input('Enter Search', type=xbmcgui.INPUT_ALPHANUM)
            if len(userinput)==0: return
            urldata["searchdata"]=userinput        
            searchurl='emovies:'+json.dumps(urldata)
            searchurl = '%s?mode=36&url=%s' % (sys.argv[0], urllib.quote_plus(searchurl))
            xbmc.executebuiltin('Container.Update(%s)' % searchurl)
            return
        addEmoviesFromSearch(urldata)
    elif urldata["type"]=="alpha":
        if 'searchdata' not in urldata:
            dialog = xbmcgui.Dialog()
            import string
            alphas=list(string.ascii_uppercase)
            index = dialog.select('Choose Starts with', alphas)
            userinput=""
            if index > -1:
                userinput=alphas[index]
            if len(userinput)==0: return
            urldata["searchdata"]=userinput
            searchurl='emovies:'+json.dumps(urldata)
            searchurl = '%s?mode=36&url=%s' % (sys.argv[0], urllib.quote_plus(searchurl))
            xbmc.executebuiltin('Container.Update(%s)' % searchurl)
            return
        addEmoviesFromSearch(urldata)
    else:
        addDir ('Search Movie' ,'emovies:{"lang":"%s","type":"search"}'%(urldata["lang"]),36,'', False, True,isItFolder=False)
        addDir ('Alphabetically List' ,'emovies:{"lang":"%s","type":"alpha"}'%(urldata["lang"]),36,'', False, True,isItFolder=False)
        for s in ['2010','2000','1990','1980','1970','1960','1950','1940']:
            addDir ('Movies from %s'%s ,'emovies:{"lang":"%s","type":"decade","decadenum":"%s"}'%(urldata["lang"],s),36,'', False, True,isItFolder=True)


def addEmoviesFromSearch(urldata):
    url=""
    print 'addEmoviesFromSearch',urldata
    page="1"
    lang=urldata["lang"]
    url1=""
    url2=""
    if 'page' in urldata:
        page=urldata["page"]
    urlpage=int(page)*2
    if urldata["type"]=="decade":
        dacadenumer=urldata["decadenum"]
        url1="https://einthusan.tv/movie/results/?decade=%s&find=Decade&lang=%s&page=%s"%(dacadenumer,lang,str(urlpage-1))
        url2="https://einthusan.tv/movie/results/?decade=%s&find=Decade&lang=%s&page=%s"%(dacadenumer,lang,str(urlpage))
    elif urldata["type"]=="search":
        searchdata=urldata["searchdata"]
        url1="https://einthusan.tv/movie/results/?query=%s&lang=%s&page=%s"%(urllib.quote_plus(searchdata),lang,str(urlpage-1))
        url2="https://einthusan.tv/movie/results/?query=%s&lang=%s&page=%s"%(urllib.quote_plus(searchdata),lang,str(urlpage))
    elif urldata["type"]=="alpha":
        searchdata=urldata["searchdata"]
        url1="https://einthusan.tv/movie/results/?alpha=%s&find=Alphabets&lang=%s&page=%s"%(urllib.quote_plus(searchdata),lang,str(urlpage-1))
        url2="https://einthusan.tv/movie/results/?alpha=%s&find=Alphabets&lang=%s&page=%s"%(urllib.quote_plus(searchdata),lang,str(urlpage))
                
    newpage=str(int(page)+1)
    newpagedata=urldata
    newpagedata["page"]=newpage
    moviecode=""
    html1=""
    try:
        html1=getUrl(url1)
        if len(url2)>0:
            html1+=getUrl(url1)
    except: pass
    added=False
    for mov in re.findall( "<div class=\"block1\">.*?href=['\"].*?watch\/(.*?)\/\?lang=(.*?)['\"].*?src=['\"](.*?)['\"].*?<h3>(.*?)<",html1):
        try:
            added=True
            moviecode=mov[0]
            imageurl=mov[2]
            if imageurl.startswith('//'): imageurl='http:'+imageurl
            mname=mov[3]
            addDir (mname,base64.b64encode('emovies:%s,%s'%(moviecode,lang)),11,imageurl, False, True,isItFolder=False)
        except: pass
    if added:
        addDir ('Next Page %s'%newpage ,'emovies:'+json.dumps(newpagedata),36,'', False, True,isItFolder=True)


    
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
            if cname.lower().startswith('high alert'): continue
            #cid=source.findtext('programURL')# change from programURL
            cid=source.findtext('programID')
            cimage=source.findtext('programImage')+'|User-Agent=Pak%20TV/1.4 CFNetwork/808.2.16 Darwin/16.3.0'
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
            addDir(ColoredOpt(url[int(seq)].capitalize(),col),'',37,'', False, True,isItFolder=True)            
        prevseq=seq    
        addDir (ColoredOpt(r[0].capitalize(),col) ,base64.b64encode(r[2]),37,r[3], False, True,isItFolder=False)

def AddMyTVSports(url=None):
        
    for cname,ctype,curl,imgurl in getMyTVChannels():
        cname=cname.encode('ascii', 'ignore').decode('ascii')
        mm=11
        addDir(ColoredOpt(cname.capitalize(),'ZM') ,base64.b64encode(curl) ,mm ,imgurl, False, True,isItFolder=False)		#name,url,mode,icon
    return    
    
def AddPakTVSports(url=None):

    if url=="sss":
        cats=['CTG Stadium','T20 World Cup','Live Cricket','Ptv Sports','PSL','Pak VS NZ','IND VS AUS','ENG VS SA','India Sports','World Sports','Football Clubs','Pak Sports','Cricket','Footbal','Golf','Wrestling & Boxing','T20 Big Bash League']
        isSports=True
        addDir(ColoredOpt('>>Click here for All Categories<<'.capitalize(),'red') ,"paktv",66 ,'', False, True,isItFolder=True)
    else:
        cats=[url]
        isSports=False
        
    for cname,ctype,curl,imgurl in getPakTVChannels(cats,isSports, desi=False):
        cname=cname.encode('ascii', 'ignore').decode('ascii')
        if ctype=='manual2':
            mm=37
        elif ctype=='manual3':
            mm=45
        else:
            mm=11
        addDir(ColoredOpt(cname.capitalize(),'ZM') ,base64.b64encode(curl) ,mm ,imgurl, False, True,isItFolder=False)		#name,url,mode,icon
    return    
                   
def AddPTCSports(url=None):
    if url=="sss":
        isSports=True
        cats=['PSL','IPL','Ptv Sports','Star Sports','Sports','BPL T20','Live Cricket','Live Footbal','Ten Sports','BT Sports','Euro Sports']
        addDir(ColoredOpt('>>Click here for All Categories<<'.capitalize(),'red') ,"ptc",66 ,'', False, True,isItFolder=True)
    else:
        cats=[url]
        isSports=False
    for cname,ctype,curl,imgurl in getptcchannels(cats,isSports, desi=False):
        cname=cname.encode('ascii', 'ignore').decode('ascii')
        if ctype=='manual2':
            mm=37
        elif ctype=='manual3':
            mm=45
        else:
            mm=11
        addDir(ColoredOpt(cname.capitalize(),'ZM') ,base64.b64encode(curl) ,mm ,imgurl, False, True,isItFolder=False)		#name,url,mode,icon
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
    
    
def AddSports365Channels(url=None, recursive=False):
    errored=True
    forced=False
    try:

        addDir(Colored("All times in local timezone.",'blue') ,"" ,0,"", False, True,isItFolder=False)		#name,url,mode,icon
        addDir(Colored("Update parser file.",'blue') ,"sss" ,80,"", False, True,isItFolder=False)		#name,url,mode,icon
        addDir(Colored("Refresh listing",'blue') ,"sss" ,156,"", False, True,isItFolder=True)		#name,url,mode,icon
        addDir(Colored("Stopped playing after 2 minutes??????? CLICK HERE!",'red') ,"sss" ,95,"", False, True,isItFolder=True)		#name,url,mode,icon
        import live365
        forced=not live365.isvalid()        
        videos=live365.getLinks()
        for nm,link,active in videos:
            if active:
               
                addDir(Colored(nm  ,'ZM') ,link,11 ,"",isItFolder=False)
            else:
                addDir("[N/A]"+Colored(nm ,'blue') ,"",0 ,"",isItFolder=False)
            errored=False
    except: traceback.print_exc(file=sys.stdout)
    if errored:
       print 'forced',forced
       import time
       if RefreshResources([('live365.py','http://shani.offshorepastebin.com/live365.py',forced)]):
            dialog = xbmcgui.Dialog()
            ok = dialog.ok('XBMC', 'Updated files dyamically, Try to play again, just in case!')
            #if not recursive:
            #    AddSports365Channels(url=url, recursive=True)            
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
            try:
                if rfile[2]: lastFileTime=None
            except: pass
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
    cc= getUKTVPlayUrl(url)
    print cc
    listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
    played=False
    ##DO YOU WANT ME TO STOP? lol
    try:
        import uktvplayerlimited
        played=uktvplayerlimited.play(listitem,cc)
            
    except: 
        print 'error in PlayUKTVNowChannels'
        traceback.print_exc(file=sys.stdout)
        pass
    #if not played:
    #    if RefreshResources([('uktvplayerlimited.py','https://raw.githubusercontent.com/Shani-08/ShaniXBMCWork2/master/plugin.video.ZemTV-shani/uktvplayerlimited.py')]):
    #        dialog = xbmcgui.Dialog()
    #        ok = dialog.ok('XBMC', 'Updated files dyamically, try again, just in case!')           
    #        print 'Updated files'
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

def getIndianPakShowsCat():
    ret=[]
    try:
        url=base64.b64decode("aHR0cDovL3l0eC5tZS9tanNvbi9nZXRtZW51P2lvc2FwcG5hbWU9YXJ6dQ==")

        headers=[('User-Agent',base64.b64decode('QXJ6dS8yLjAuMiBDRk5ldHdvcmsvNzU4LjAuMiBEYXJ3aW4vMTUuMC4w'))]
        jdata=getUrl(url, headers=headers)
        jsondata=json.loads(jdata)
        for channel in jsondata["menuItems"]:
            cname=channel["title"]
            curl=channel["jsonURL"]
            curl=curl.replace('%@%@',base64.b64decode('eXR4Lm1l'))+'app=%s&c=%s&returnid=%s'%(channel["appName"],channel["category"],channel["id"])
            cimage=''            
            ret.append((cname ,'manual', curl ,cimage))  
    except:
        traceback.print_exc(file=sys.stdout)
    if len(ret)>0:
        ret=sorted(ret,key=lambda s: s[0].lower()   )
    return ret


def getFootballPostData():
    return eval(base64.b64decode("eydhcHBfdGFnJzonZm9vdGJhbGxfaGlnaGxpZ2h0X2hkJywnc3RvcmUnOidpdHVuZXMnLCdhcHBfdmVyc2lvbic6JzInLCAnYXBwX2FwaV9zZWNyZXRfa2V5JzonZm9vdGJhbGxfcHJvZHVjdGlvbl8xMl8zNF9AQCd9"))

def getFastCats():
    fname='FastCats.json'
    fname=os.path.join(profile_path, fname)
    try:
        jsondata=getCacheData(fname,2*60*60)
        if not jsondata==None:
            return json.loads(base64.b64decode(jsondata))
    except:
        print 'file getting error'
        traceback.print_exc(file=sys.stdout)

    fastData=getFastData()
    headers=[('User-Agent',base64.b64decode('RGFsdmlrLzEuNi4wIChMaW51eDsgVTsgQW5kcm9pZCA0LjQuMjsgU00tRzkwMEYgQnVpbGQvS09UNDlIKQ==')),('Authorization','Basic %s'%base64.b64encode(fastData["DATA"][0]["Password"]))]
    link=getUrl(base64.b64decode('aHR0cDovL3N3aWZ0c3RyZWFtei5jb20vU3dpZnRTdHJlYW0vYXBpLnBocA=='),headers=headers)
    
    jsondata=None
    try:
        try:
            jsondata=json.loads(link)
        except:
            jsondata=json.loads(link.split(']}')[0]+']}')
        storeCacheData(base64.b64encode(link),fname)
    except:
        print 'getFastData file saving error'
        traceback.print_exc(file=sys.stdout)
    return jsondata    

def getFastUA(v2=False):
    import random,string
    s=eval(base64.b64decode("Wyc0LjQnLCc0LjQuNCcsJzUuMCcsJzUuMS4xJywnNi4wJywnNi4wLjEnLCc3LjAnLCc3LjEuMSdd"))
    if v2:
        s2=[''.join(random.SystemRandom().choice(string.ascii_letters) for _ in range(4+int(random.random()*15)))]
    else:
        s2=eval(base64.b64decode("WydTb255IEV4cGVyaWEnLCdTb255IEV4cGVyaWEgVGFibGV0JywnS2luZGxlIEZpcmUnLCdGaXJlIEhEJywnVG91Y2hQYWQnXQ=="))
    #s2=eval(base64.b64decode("['Fire HD']"))

    #usagents=base64.b64decode('RGFsdmlrLzEuNi4wIChMaW51eDsgVTsgQW5kcm9pZCAlcy4lcy4lczsgJXMgQnVpbGQvJXMp')%(str(random.choice(range(3,6))),str(random.choice(range(3,6))),str(random.choice(range(3,6))),''.join(random.SystemRandom().choice(string.ascii_uppercase) for _ in range(8)),''.join(random.SystemRandom().choice(string.ascii_uppercase) for _ in range(6)) )
    #keep following me :p
    usagents=base64.b64decode('RGFsdmlrLzEuNi4wIChMaW51eDsgVTsgQW5kcm9pZCAlczsgJXMgQnVpbGQvJXMp')%(random.choice(s),random.choice(s2),''.join(random.SystemRandom().choice(string.ascii_letters) for _ in range(int(random.random()*15))) )
    #usagents=base64.b64decode('Mozilla/5.0 (Linux; U; Android 4.%s.%s; Galaxy Nexus Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30')
    return usagents


def getFastData():
    fname='Fastdata.json'
    fname=os.path.join(profile_path, fname)
    try:
        jsondata=getCacheData(fname,2*60*60)
        if not jsondata==None:
            #print jsondata
            return json.loads(base64.b64decode(jsondata))
    except:
        print 'file getting error'
        traceback.print_exc(file=sys.stdout)

    usagents=getFastUA()
    
    #ua = random.choice(usagents)

    headers=[('User-Agent',usagents),('Authorization',base64.b64decode('QmFzaWMgVTNkcFpuUk9aWGM2UUZOM2FXWjBUbVYzUUE9PQ=='))]
    link=getUrl(base64.b64decode('aHR0cDovL3N3aWZ0c3RyZWFtei5jb20vU3dpZnRTdHJlYW16L3N3aWZ0c3RyZWFtei5waHA='),headers=headers)
    
    jsondata=None
    try:
        print 'link',link
        link=link.replace('\x0a','').replace('\t','')
        jsondata=json.loads(link)
        storeCacheData(base64.b64encode(link),fname)
    except:
        print 'getFastData file saving error'
        traceback.print_exc(file=sys.stdout)
    return jsondata    

def getNetworkTVData2(apptype):
    fname='Networkdata2%s.json'%str(apptype)
    fname=os.path.join(profile_path, fname)
    try:
        jsondata=getCacheData(fname,30*60)
        if not jsondata==None:
            return json.loads(base64.b64decode(jsondata))
    except:
        print 'file getting error'
        traceback.print_exc(file=sys.stdout)

    usagents=getFastUA()
    
    #ua = random.choice(usagents)

    if apptype==1:
        headers=[('User-Agent',usagents),('Authorization',base64.b64decode('QmFzaWMgVTI5c2FXUlRkSEpsWVcxNk9rQWhVMjlzYVdSVGRISmxZVzE2SVVBPQ=='))]
        link=getUrl(base64.b64decode('aHR0cDovL3NvbGlkc3RyZWFtei5jb20vc29saWRkYXRhLnBocA=='),headers=headers, post='')
    else:
        headers=[('User-Agent',usagents),('Authorization',base64.b64decode('QmFzaWMgVUZSV1UxQlBVbFJUT2lFbEpTRlRVRTlTVkZOd2RIWWhKU1Vo'))]
        link=getUrl(base64.b64decode('aHR0cDovL2FwaS5zb2xpZHh0cmVhbS5jb20vcHR2c3BvcnQvcHR2ZGF0YS5waHA='),headers=headers, post='')
        
    jsondata=None
    try:
        print link
        li=link[:2]+link[3:]
        print li
        jsondata=json.loads(base64.b64decode(li).replace("\n",""))
        storeCacheData(li,fname)
    except:
        print 'getNetworkTVData2 dec error'
        traceback.print_exc(file=sys.stdout)
    return jsondata     
    


def getNetworkTVData():
    fname='Networkdata.json'
    fname=os.path.join(profile_path, fname)
    try:
        jsondata=getCacheData(fname,30*60)
        if not jsondata==None:
            return json.loads(base64.b64decode(jsondata))["data"][0]
    except:
        print 'file getting error'
        traceback.print_exc(file=sys.stdout)

    headers=[('application-id',base64.b64decode('QUYxMkY0N0YtMEM5Qy0zQkMxLUZGNkYtNzkzNUUwQzBDQzAw')),('secret-key',base64.b64decode('MTAzQ0JFNkYtNEYyMi0yRTlCLUZGQzEtMjVCRUNEM0QyRjAw')),('application-type','REST')]
    link=getUrl(base64.b64decode('aHR0cHM6Ly9hcGkuYmFja2VuZGxlc3MuY29tL3YxL2RhdGEvQXBwQ29uZmlnQWxwaGE='),headers=headers)
    jsondata=None
    try:
        jsondata=json.loads(link.replace('\x0a',''))
        #print jsondata
        storeCacheData(base64.b64encode(link),fname)
    except:
        print 'getFastData file saving error'
        traceback.print_exc(file=sys.stdout)
    return jsondata["data"][0]

    
    
def getNetworkTVDataGOOGLE():
    fname='Networkdata.json'
    fname=os.path.join(profile_path, fname)
    try:
        jsondata=getCacheData(fname,60*60)
        if not jsondata==None:
            return json.loads(base64.b64decode(jsondata))
    except:
        print 'file getting error'
        traceback.print_exc(file=sys.stdout)

    post='{"returnSecureToken":true}'
   # post = urllib.urlencode(post)


    
    headers=[('X-Android-Package',base64.b64decode('Y29tLmxpdmVuZXQuaXB0dg==')),('X-Android-Cert',base64.b64decode('MEM1RDBDREI3QzU1MTFDNzE4MTY0OTQ1OTc2MDY4MTg5QUU0QzJEMA=='))]
   
    udata=getUrl(base64.b64decode('aHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vaWRlbnRpdHl0b29sa2l0L3YzL3JlbHlpbmdwYXJ0eS9zaWdudXBOZXdVc2VyP2tleT1BSXphU3lEdEFIaXlxa3ZaT09reURNdjNQb1R0dVI5bzVEN1Vxenc='), post=post,jsonpost=True,headers=headers)
    
    print     udata
    udata=json.loads(udata)
    #headers=[('application-id',base64.b64decode('QUYxMkY0N0YtMEM5Qy0zQkMxLUZGNkYtNzkzNUUwQzBDQzAw')),('secret-key',base64.b64decode('MTAzQ0JFNkYtNEYyMi0yRTlCLUZGQzEtMjVCRUNEM0QyRjAw')),('application-type','REST')]
    link=getUrl(base64.b64decode('aHR0cHM6Ly9saXZlbmV0LWlwdHYuZmlyZWJhc2Vpby5jb20vQXBwQ29uZmlnQWxwaGEuanNvbj9wcmludD1wcmV0dHkmYXV0aD0lcw==')%udata["idToken"])
    jsondata=None
    try:
        jsondata=json.loads(link.replace('\x0a',''))
        #print jsondata
        storeCacheData(base64.b64encode(link),fname)
    except:
        print 'getFastData file saving error'
        traceback.print_exc(file=sys.stdout)
    return jsondata    

  
def getFootballData():
    fname='footballdata.json'
    fname=os.path.join(profile_path, fname)
    try:
        jsondata=getCacheData(fname,2*60*60)
        if not jsondata==None:
            return json.loads(base64.b64decode(jsondata))
    except:
        print 'file getting error'
        traceback.print_exc(file=sys.stdout)

        
    post=getFootballPostData()
    post = urllib.urlencode(post)
    headers=[('User-Agent',base64.b64decode('TGl2ZSBGb290YmFsbCBvbiBUViAzLjAuMSAoaVBob25lOyBpUGhvbmUgT1MgOS4wLjI7IGVuX0dCKQ=='))]
    link=getUrl(base64.b64decode('aHR0cDovL2dhbWVzZXJ2aWNlcy5yaW9tb3Rpcy5jb20vYXBpL2NvbmZpZy8='),post=post,headers=headers)
    
    jsondata=None
    try:
        jsondata=json.loads(link)
        storeCacheData(base64.b64encode(link),fname)
    except:
        print 'getFootballData file saving error'
        traceback.print_exc(file=sys.stdout)
    return jsondata    
    
    
def getFootballComp():
    ret=[]
    try:

        jsondata=getFootballData()
        for channel in jsondata["competitions"]:
            cname=channel["name"]
            curl="CM,"+channel["id"]+',0'
            cimage=channel["logo"]    
            seq=channel["popular_point"]
            ret.append((cname ,'manual', curl ,cimage,seq))  
    except:
        traceback.print_exc(file=sys.stdout)
    if len(ret)>0:
        ret=sorted(ret,key=lambda s: int(s[4])   )
    return ret

def AddFootballCats(url=None):
    try:
        addDir('Recent Football Highlights/Live Streams' ,'HL,0,0',87,'', False, True,isItFolder=True)
        addDir('Recent Football Videos [Not All Working]' ,'VD,0,0',88,'', False, True,isItFolder=True)
        channels=getFootballComp()
        if len(channels)>0:
            for cname,ctype,curl,imgurl,seq in channels:
                cname=cname.encode('ascii', 'ignore').decode('ascii') 
                addDir(ColoredOpt (cname,'blue') ,'',0,imgurl, False, True,isItFolder=True)		#name,url,mode,icon
                addDir('   -Highlights/Live Streams' ,curl,87,imgurl, False, True,isItFolder=True)		#name,url,mode,icon
                addDir('   -Videos' ,curl,88,imgurl, False, True,isItFolder=True)		#name,url,mode,icon
    except: 
        traceback.print_exc(file=sys.stdout)

def getFootballVideos(url):
    ret=[]
    moreurl=None
    try:
        fbData=getFootballData()
        post=getFootballPostData()
        vtype,currentval,startindex=url.split(',')
        post['total']=16
        post['from_index']=startindex
        
        moreurl=vtype+','+currentval+","+str(int(startindex)+16)
        if url.startswith("VD,"):        
            urlnew=fbData["API_URLS"][base64.b64decode("R0VUX0xBU1RFU1RfVklERU8=")]
        else:
            urlnew=fbData["API_URLS"][base64.b64decode("R0VUX1ZJREVPX0JZX0NPTVBFVElUSU9OX0lE")]
            post['competition_id']=currentval
            
        post = urllib.urlencode(post)
        headers=[('User-Agent',base64.b64decode('TGl2ZSBGb290YmFsbCBvbiBUViAzLjAuMSAoaVBob25lOyBpUGhvbmUgT1MgOS4wLjI7IGVuX0dCKQ=='))]

        jsondata=json.loads(getUrl(urlnew, post=post,headers=headers))
        import datetime
        
    
        for channel in jsondata["videos"]:
            datenum=channel["date"]/1000
            datenum=datetime.datetime.fromtimestamp(int(datenum) ).strftime('%Y-%m-%d')
            cname=datenum+' '+channel["title"]
            videourl=channel["video_link"][0]["media_url"]
            videotype=channel["video_link"][0]["media_type"]
            curl=videotype+','+base64.b64encode(videourl)
            cimage=channel["thumbnail"]           
            ret.append((cname ,'manual', curl ,cimage))  
    except:
        traceback.print_exc(file=sys.stdout)
    return ret,moreurl

def AddFootballVideos(url):
    try:
        channels,moreurl=getFootballVideos(url)
        if len(channels)>0:
            for cname,ctype,curl,imgurl in channels:
                cname=cname.encode('ascii', 'ignore').decode('ascii') 
                addDir(cname ,curl,91,imgurl, False, True,isItFolder=True)		#name,url,mode,icon
        if moreurl:
            addDir('Next Page' ,moreurl,mode,'', False, True,isItFolder=True)		#name,url,mode,icon
    except: 
        traceback.print_exc(file=sys.stdout)      
        
        
def getFootballMatches(url):
    ret=[]
    moreurl=None
    try:
        fbData=getFootballData()
        post=getFootballPostData()
        vtype,currentval,startindex=url.split(',')
        post['total']=16
        post['from_index']=startindex
        
        moreurl=vtype+','+currentval+","+str(int(startindex)+16)
        if url.startswith("HL,"):        
            urlnew=fbData["API_URLS"][base64.b64decode("R0VUX0xBU1RFU1RfSElHSExJR0hU")]
        else:
            urlnew=fbData["API_URLS"][base64.b64decode("R0VUX0hJR0hMSUdIVF9CWV9DT01QRVRJVElPTl9JRA==")]
            post['competition_id']=currentval
            
        post = urllib.urlencode(post)
        headers=[('User-Agent',base64.b64decode('TGl2ZSBGb290YmFsbCBvbiBUViAzLjAuMSAoaVBob25lOyBpUGhvbmUgT1MgOS4wLjI7IGVuX0dCKQ=='))]

        jsondata=json.loads(getUrl(urlnew, post=post,headers=headers))
        import datetime
        
    
        for channel in jsondata["matchs"]:
            datenum=channel["date"]/1000
            datenum=datetime.datetime.fromtimestamp(int(datenum) ).strftime('%Y-%m-%d')
            namecol="green"
            playtype=""
            curl=base64.b64encode(json.dumps(channel))
            if channel["is_live_streaming"]: 
                namecol="blue"
                playtype="live"
                curl=channel["highlight"][0]["media_url"]
            cname=ColoredOpt( datenum+' '+channel["home_team"]["name"]  + ' ' +str(channel["home_score"]) +'-' +str(channel["guest_score"] ) +' '+channel["guest_team"]["name"],namecol) +'\n' + ColoredOpt(channel["competition"]["name"],'red')
            
            cimage=channel["screenshot"]  
            
            ret.append((cname ,playtype, curl ,cimage))  
    except:
        traceback.print_exc(file=sys.stdout)
    return ret,moreurl

def AddFootballMatches(url):
    try:
        channels,moreurl=getFootballMatches(url)
        if len(channels)>0:
            for cname,ctype,curl,imgurl in channels:
                cname=cname.encode('ascii', 'ignore').decode('ascii') 
                if ctype=="live":
                    addDir(cname ,"LIVE,"+base64.b64encode(curl),91,imgurl, False, True,isItFolder=False)		#name,url,mode,icon
                else:
                    addDir(cname ,curl,89,imgurl, False, True,isItFolder=True)		#name,url,mode,icon
        if moreurl:
            addDir('Next Page' ,moreurl,mode,'', False, True,isItFolder=True)		#name,url,mode,icon
    except: 
        traceback.print_exc(file=sys.stdout)        
        
def AddFootballMatcheHome(url):
    try:
        channel=json.loads(base64.b64decode(url))
        videos=[]
        for c in channel["highlight"]:
            videos.append( (c["media_url"],c["media_type"]))
        for c in channel["fullmatch"]:
            videos.append( (c["media_url"],c["media_type"]))

        #if 'is_live_streaming' in c and c['is_live_streaming']:
        #    addDir(Colored('Play Live Stream NOW[notoworking]','red') ,"LIVE,"+base64.b64encode(videos[0]),91,'', False, True,isItFolder=False)

        seen = set()
        videos=[item for item in videos if item[0] not in seen and not seen.add(item[0])]
        num=0
        if len(videos)>0:
            for curl,ctype in videos:
                num+=1
                addDir('video #'+str(num) + ' [%s]'%ctype,ctype+','+base64.b64encode(curl),91,'', False, True,isItFolder=False)
    except: 
        traceback.print_exc(file=sys.stdout)                
        
def AddIndianPakShowsCat(url=None):
    try:
        channels=getIndianPakShowsCat()
        if len(channels)>0:
            for cname,ctype,curl,imgurl in channels:
                cname=cname.encode('ascii', 'ignore').decode('ascii')
        #        print repr(curl)      
                addDir(cname ,curl,84 ,imgurl, False, True,isItFolder=True)		#name,url,mode,icon
    except: 
        traceback.print_exc(file=sys.stdout)

def getIndianPakShows(url):
    ret=[]
    try:

        headers=[('User-Agent',base64.b64decode('dmlkZW91dC8yLjAgKGlQaG9uZTsgaU9TIDkuMC4yOyBTY2FsZS8yLjAwKQ=='))]
        jdata=getUrl(url, headers=headers)
        appname=url.split('app=')[1].split('&')[0]
        jsondata=json.loads(jdata)
        for channel in jsondata["shows"]:
            cname=channel["title"]
            type=85
            if not 'videoId' in channel:
                showname=channel["title"].lower().replace(' ','_')
                curl=base64.b64decode('aHR0cDovL3l0eC5tZS9tanNvbi9nZXRqc29uP25hbWU9JXMmc3RhcnQ9MCZhcHA9JXMmbWF4PTI1MA==')%(showname,appname)
            else:
                curl=channel["videoId"]  
                type=11
                curl=base64.b64encode('direct:plugin://plugin.video.youtube/?action=play_video&videoid=%s' %curl)                
            cimage=channel["imageurl"] 
            if not cimage.startswith('http'): cimage=base64.b64decode('aHR0cDovL3l0eC5tZS9tanNvbi9jb25mLw==')+cimage            
            ret.append((cname ,type, curl ,cimage))  
    except:
        traceback.print_exc(file=sys.stdout)
    if len(ret)>0:
        ret=sorted(ret,key=lambda s: s[0].lower()   )
    return ret
    
def AddIndianPakShows(url):
    try:
        channels=getIndianPakShows(url)
        if len(channels)>0:
            for cname,ctype,curl,imgurl in channels:
                cname=cname.encode('ascii', 'ignore').decode('ascii')
        #        print repr(curl)      
                if ctype==11:
                    addDir(cname ,curl,ctype ,imgurl, False, True,isItFolder=False)		#name,url,mode,icon
                else:
                    addDir(cname ,curl,ctype ,imgurl, False, True,isItFolder=True)		#name,url,mode,icon
    except: 
        traceback.print_exc(file=sys.stdout)

def getIndianPakShowsEP(url):
    ret=[]
    try:

        headers=[('User-Agent',base64.b64decode('dmlkZW91dC8yLjAgKGlQaG9uZTsgaU9TIDkuMC4yOyBTY2FsZS8yLjAwKQ=='))]
        jdata=getUrl(url, headers=headers)
        appname=url.split('app=')[1].split('&')
        jsondata=json.loads(jdata)
        for channel in jsondata["playlistitems"]:
            cname=channel["title"]
            curl=channel["videoid"]  
            curl=base64.b64encode('direct:plugin://plugin.video.youtube/?action=play_video&videoid=%s' %curl)
            cimage=channel["imageurl"]  
            if not cimage.startswith('http'): cimage=base64.b64decode('aHR0cDovL3l0eC5tZS9tanNvbi9jb25mLw==')+cimage
            ret.append((cname ,'manual', curl ,cimage))  
    except:
        traceback.print_exc(file=sys.stdout)
    #if len(ret)>0:
    #   ret=sorted(ret,key=lambda s: s[0].lower()   )
    return ret
    
def AddIndianPakShowsEP(url):
    try:
        channels=getIndianPakShowsEP(url)
        if len(channels)>0:
            for cname,ctype,curl,imgurl in channels:
                cname=cname.encode('ascii', 'ignore').decode('ascii')
        #        print repr(curl)      
                addDir(cname ,curl,11 ,imgurl, False, True,isItFolder=False)		#name,url,mode,icon
    except: 
        traceback.print_exc(file=sys.stdout)


    
def AddYuppSports(url=None):
    try:

        addDir(ColoredOpt("Live Streams".capitalize(),'ZM') ,"" ,-1,"", False, True,isItFolder=False)		#name,url,mode,icon
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

        addDir(ColoredOpt("Recorded/Highlights".capitalize(),'ZM') ,"" ,-1,"", False, True,isItFolder=False)		#name,url,mode,icon
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
    
def AddTestChannels(url=None):
    import testarea
    for cname,ctype,curl,imgurl,itemtype in testarea.getChannels(url,mode):
        print cname,ctype,curl,imgurl,itemtype
        cname=cname.encode('ascii', 'ignore').decode('ascii')
        isfolder=False
        if itemtype=="folder":
            mm=99
            isfolder=True
        else:
            mm=11
        
        addDir(ColoredOpt(cname.capitalize(),'ZM') ,base64.b64encode(curl) ,mm ,imgurl, False, True,isItFolder=isfolder)		#name,url,mode,icon
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
       
        addDir(ColoredOpt(cname.capitalize(),'ZM') ,base64.b64encode(curl) ,mm ,imgurl, False, True,isItFolder=False)		#name,url,mode,icon
    return   

def AddIpBoxSources(url=None):
    for cname,curl in getIpBoxSources(caller=url):
        try:
            #print cname
            cname=cname#cname.encode('ascii', 'ignore').decode('ascii')
           
            addDir(ColoredOpt(cname.capitalize(),'ZM') ,curl ,61 ,"", False, True,isItFolder=True)		#name,url,mode,icon
        except: traceback.print_exc(file=sys.stdout) 
    return
    
def AddIpBoxChannels(url=None):
    sort=False
    if not mode==67:
        addDir(Colored('>>Click Here for All Channels<<'.capitalize(),'red') ,url ,67 ,"", False, True,isItFolder=True)		#name,url,mode,icon
        sort=True

    for cname,ctype,curl,imgurl in getIpBoxChannels([url],True,sort=sort):
        try:
            #print cname
            cname=cname#cname.encode('ascii', 'ignore').decode('ascii')
            mm=11
    #        print repr(curl)
           
            addDir(ColoredOpt(cname.capitalize(),'ZM') ,base64.b64encode(curl) ,mm ,imgurl, False, True,isItFolder=False)		#name,url,mode,icon
        except: traceback.print_exc(file=sys.stdout) 
    return     
    
def AddWTVSports(url=None):

    if url=="sss":
        cats=['extra time football','tsn','cth stadium','ufc','t20 world cup','horse racing','cricket','footbal','golf','boxing & wrestling','t20 big bash league','nfl live','footbal clubs','sports time','darts','eng vs ind']
        isSports=True
        addDir(Colored('>>Click here for All Categories<<'.capitalize(),'red') ,"wtv",66 ,'', False, True,isItFolder=True)
    else:
        cats=[url]
        isSports=False

    for cname,ctype,curl,imgurl in getWTVChannels(cats,isSports, desi=False):
        cname=cname.encode('ascii', 'ignore').decode('ascii')
        if ctype=='manual2':
            mm=37
        elif ctype=='manual3':
            mm=45
        else:
            mm=11
        addDir(ColoredOpt(cname.capitalize(),'ZM') ,base64.b64encode(curl) ,mm ,imgurl, False, True,isItFolder=False)		#name,url,mode,icon
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
        addDir(ColoredOpt(cname.capitalize(),'ZM') ,base64.b64encode(curl) ,mm ,imgurl, False, True,isItFolder=False)		#name,url,mode,icon
    return      

    
def AddSafeLang(url=None):
    for cname,ctype in [('English','en'),('German','de'),('French','fr'),('Italian','it'),('Dutch','nl'),('Polish','pl')]:        
        addDir(ColoredOpt(cname.capitalize(),'ZM') ,base64.b64encode(cname+','+ctype) ,73 ,'', False, True,isItFolder=True)		#name,url,mode,icon
    return  
    
    
def getTVPlayerChannels(thesechannels=[]):

    headers=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36')]               
    mainhtml=getUrl('https://tvplayer.com/watch/bbcone',headers=headers)
    cdata=re.findall('<li .*? class="online.*?free.*?\s*<a href="(.*?)" title="(.*?)".*?\s*<img.*?src="(.*?)"',mainhtml)
    ret=[]
    for cc in cdata:
        
        mm=11
        col='ZM'
        logo=cc[2]

        cname=cc[1]
        if 'Watch ' in cname:
            cname=cname.replace('Watch ','')
        curl=cc[0]
        if not curl.startswith('http'):
            curl= 'https://tvplayer.com/'+curl
        if len(thesechannels)==0 or cname.lower() in thesechannels:
            ret.append( (cname.capitalize() ,base64.b64encode('tvplayer:'+curl) ,mm ,logo) )		#name,url,mode,icon
    return ret
        
def AddTVPlayerChannels(url, thesechannels=[]):
    addDir('Some channels requires free login, enter in the settings.' ,'' ,'','', False, True,isItFolder=False)
    for ch in sorted(getTVPlayerChannels(thesechannels),key=lambda s: s[0].lower() ) :
        addDir(ch[0] ,ch[1] ,ch[2],ch[3], False, True,isItFolder=False)

def AddStreamHDCats(url):

    cdata=[('Football','http://www.streamhd.eu/football/'),('','')]
    reg='<li>\s*?<a.*?href="(.*?)".*?src="(.*?)".*?>(.*?)<'
    headers=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36')]               
    mainhtml=getUrl('http://www.streamhd.eu/',headers=headers)
    cdata=re.findall(reg,mainhtml)
    cdata=[('http://www.streamhd.eu/tv/','','Live Sports Channels'),('http://www.streamhd.eu/','','All Sports'),
        ('http://www.streamhd.eu/football/','http://www.streamhd.eu/images/icons/football.png','Footbal')
        ]+cdata
    
    for cc in cdata:
        
        mm=76
        logo=cc[1]
        cname=cc[2]
        curl=cc[0]
        if not curl.startswith('http'):
            curl= 'http://www.streamhd.eu'+curl
        addDir(cname.capitalize() ,curl ,mm ,logo, False, True,isItFolder=True)		#name,url,mode,icon
        
def getEuroStreamChannels(url):
    import time
    headers=[('User-Agent','Sports%20TV/2 CFNetwork/758.0.2 Darwin/15.0.0')]               
    mainhtml=getUrl(base64.b64decode('aHR0cDovL3d3dy5ub3RpY2lhc3RlbGVmb25pYS5lcy9zcG9ydHNiaWd0ZWQucGxpc3Q='),headers=headers)
    ret=[]
    try:
        chdata= re.findall( '<string>(.*?)</string>',mainhtml)
        for cc2 in chdata:
            try:
                mm=11            
                          
                logo=''         
                cname,curl=cc2.split(',')                
                ret.append((cname ,base64.b64encode('direct2:'+curl+'|User-Agent=AppleCoreMedia/1.0.0.13A452 (iPhone; U; CPU OS 9_0_2 like Mac OS X; en_gb)') ,mm ,logo))
            except:
                traceback.print_exc(file=sys.stdout)
    except:
        traceback.print_exc(file=sys.stdout)
    return sorted(ret,key=lambda s: s[0].lower()   )
        
def AddEuroStreamChannels(url):

    try:
        for cc2 in getEuroStreamChannels(url):
            try:
                addDir(cc2[0] ,cc2[1] ,cc2[2] ,cc2[3], False, True,isItFolder=False)		#name,url,mode,icon
            except:
                traceback.print_exc(file=sys.stdout)
    except:
        traceback.print_exc(file=sys.stdout)
        
def AddMAMAHDChannels(url):
    import time
    headers=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36')]               
    mainhtml=getUrl(url,headers=headers)
    tv=False
    
    if 1==2 and '/tv/' in url:
        tv=True
        reg='<a href="(.*?)".*?class="re.*?alt="(.*?)".*?'
        cdata=re.findall(reg,mainhtml)
    else:
        #cdata=re.findall('eventsmall">(.*?)<.*?den-xs">(.*?)<.*\s*?<.*?img src="(.*?)".*?>(.*?)<.*\s*.*\s*.*?<span>(.*?)<.*\s*?.*?eventsmall.*?href="(.*?)">(.*?)<',mainhtml)
        cdata= mainhtml.split('<div class="schedule">')[1]
        cdata= re.findall( '(<a.*?<div class="row">.*?)<\/a>',cdata, re.DOTALL)
    try:
        addDir(Colored('Live Channels', 'blue') ,'sss' ,0 ,'', False, True,isItFolder=False)		#name,url,mode,icon
        chdata= mainhtml.split('<div class="standard row channels">')[1].split('</div>')[0]
        chdata= re.findall( '<a href="([^"]+)".*?\s*.*?src="([^"]+)".*?<span>([^<]+)<',chdata)
        for cc2 in chdata:
            try:
                mm=11            
                          
                logo=cc2[1]            
                cname=cc2[2]
                curl=cc2[0]
                

                addDir(cname ,base64.b64encode('mamahd:'+curl) ,mm ,logo, False, True,isItFolder=False)		#name,url,mode,icon
            except:
                traceback.print_exc(file=sys.stdout)
    except:
        traceback.print_exc(file=sys.stdout)

    addDir(Colored('Scheduled Games', 'blue') ,'sss' ,0 ,'', False, True,isItFolder=False)		#name,url,mode,icon        
    for cc in cdata[:30]:
        try:
            mm=11
            
            if tv:
                logo=''
                cname=cc[1]
                curl=cc[0]
                if curl=='#': continue
                
            else:
                cc2=re.findall('<a href="([^"]+)".*?<img src="([^"]+)".*?start="([^"]+)".*?home cell.*?<span>([^<]+)<.*?<span>([^<]+)<',cc, re.DOTALL)[0]
                logo=cc2[1]            
                cname=cc2[3]+' vs '+cc2[4]
                curl=cc2[0]
                timing=cc2[2]
                livetxt=""
                try:
                    if time.time()>int(timing):
                        livetxt="\nLIVE NOW"
                    else:
                        hrs=str(int((int(timing)-time.time())/60/60))
                        if hrs=="0":
                            livetxt="\nLIVE in %s Minutes"% str(int((int(timing)-time.time())/60))
                        else:
                            livetxt="\nLIVE in %s Hrs"% str(int((int(timing)-time.time())/60/60))
                except:
                    traceback.print_exc(file=sys.stdout)
                    pass
                cname+=ColoredOpt(livetxt,'red')

            addDir(cname ,base64.b64encode('mamahd:'+curl) ,mm ,logo, False, True,isItFolder=False)		#name,url,mode,icon
        except:
            traceback.print_exc(file=sys.stdout)
        
def AddStreamHDChannels(url):

    headers=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36')]               
    mainhtml=getUrl(url,headers=headers)
    tv=False
    if '/tv/' in url:
        tv=True
        reg='<a href="(.*?)".*?class="re.*?alt="(.*?)".*?'
        cdata=re.findall(reg,mainhtml)
    else:
        cdata=re.findall('eventsmall">(.*?)<.*?den-xs">(.*?)<.*\s*?<.*?img src="(.*?)".*?>(.*?)<.*\s*.*\s*.*?<span>(.*?)<.*\s*?.*?eventsmall.*?href="(.*?)">(.*?)<',mainhtml)
    for cc in cdata:
        
        
        mm=11
        
        if tv:
            logo=''
            cname=cc[1]
            curl=cc[0]
            if curl=='#': continue
            
        else:
            logo=cc[2]
        
            cname=Colored(cc[0]+cc[1],'green')+': '+Colored(cc[3],'red')+' '+cc[4]+'\n'+cc[6]

            curl=cc[5]
            
        if not curl.startswith('http'):
            curl= 'http://www.streamhd.eu'+curl
        addDir(cname ,base64.b64encode('streamhd:'+curl) ,mm ,logo, False, True,isItFolder=False)		#name,url,mode,icon
        
        
def playInfinite(url):
    try:

        agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'

        mainref=base64.b64decode('aHR0cDovL3d3dy5sYW9sYTEudHYvZW4taW50L2xpdmUtc2NoZWR1bGU=')
        headers=[('Referer',mainref),('User-Agent',agent)]                       
        result = getUrl(url, headers=headers)
        url=re.findall('<iframe frameborde.*\s*.*\s*.*?src="(.*?)"',result)
        if len(url)==0:
            url=re.findall('<iframe.*?src="(.*?player.php.*?)"',result)[0]
        else:
            url=url[0]
        try:
            if not url.startswith('http:'):
                urlnew=base64.b64decode('aHR0cDovL3d3dy5sYW9sYTEudHY=')+url
            print urlnew
            page_data = getUrl(urlnew, headers=headers)
            streamid = re.findall("streamid: \"(.*?)\"", page_data)[0]
        except:
            
            if not url.startswith('http:'):
                url=base64.b64decode('aHR0cDovL3d3dy5laGZ0di5jb20=')+url
            print url
            page_data = getUrl(url, headers=headers)
            streamid = re.findall("streamid: \"(.*?)\"", page_data)[0]
        
        
        partid = re.findall("partnerid: \"(.*?)\"", page_data)[0]
        
        url=base64.b64decode('aHR0cDovL3d3dy5sYW9sYTEudHYvc2VydmVyL2hkX3ZpZGVvLnBocD92PTImcGxheT0lcyZwYXJ0bmVyPSVzJnBvcnRhbD1pbnQmdjVpZGVudD0mbGFuZz1lbg==')%(streamid,partid)
        page_data=getUrl(url, headers=headers)
        
        
        areaid= re.findall(";area=(.*?)<", page_data)[0]
        import string,random
        randomtext=''.join(random.SystemRandom().choice(string.ascii_uppercase) for _ in range(7))

        data=base64.b64decode("MD10diUyRWxhb2xhMSUyRWxhb2xhdHYlMkVwcmVtaXVtY2x1YiYxPXR2JTJFbGFvbGExJTJFbGFvbGF0diUyRXByZW1pdW1jbHViJTVGYWxsJTVGYWNjZXNz")
        pageurl=base64.b64decode("aHR0cHM6Ly9jbHViLmxhb2xhMS50di9zcC9sYW9sYTEvYXBpL3YzL3VzZXIvc2Vzc2lvbi9wcmVtaXVtL3BsYXllci9zdHJlYW0tYWNjZXNzP3ZpZGVvSWQ9JXMmdGFyZ2V0PTE3JmxhYmVsPSZhcmVhPSVz")%(streamid,areaid)

    
        swf=base64.b64decode('aHR0cDovL3d3dy5sYW9sYTEudHYvYXNzZXRzL3N3Zi92aWRlb3BsYXllcl83LjAuMzIzMS5zd2Y=')
        headers=[('Referer',swf),('User-Agent',agent)]                       

        ttext = getUrl(pageurl, headers = headers,post=data)
        import json
        url=json.loads(ttext)["data"]["stream-access"][0]
    
        headers=[('Referer',pageurl),('User-Agent',agent)]                       

        ttext = getUrl(url, headers = headers)
        
        mainurl= re.findall("url=\"(.*?)\"", ttext)[0]
        if mainurl=="restricted":
            ttext = getUrlFromUS(url)
            mainurl= re.findall("url=\"(.*?)\"", ttext)[0]
        
        print mainurl
        auth= re.findall("auth=\"(.*?)\"", ttext)[0]
        final="plugin://plugin.video.f4mTester/?streamtype=HDS&url=%s&swf=%s&name=%s"%(urllib.quote_plus(mainurl+'?hdnea='+auth+'&g='+randomtext+'&hdcore=3.8.0'+'|User-Agent='+urllib.quote_plus(agent)+'&X-Requested-With=ShockwaveFlash/22.0.0.209'),swf,name)
        
        PlayGen(base64.b64encode(final))

    except:
        traceback.print_exc(file=sys.stdout)
        return
        
def playHDCast(url, mainref, altref=None):
    try:
        cookieJar=getHDCASTCookieJar()
        firstframe=url
        pageURl=mainref
        agent='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
        headers=[('Referer',pageURl),('User-Agent',agent)]                       
        result = getUrl(firstframe, headers=headers, cookieJar=cookieJar)

        regid='<script.*?id=[\'"](.*?)[\'"].*?width=[\'"]?(.*?)[\'"]?\;.*?height=[\'"]?(.*?)[\'"]?\;.*?src=[\'"](.*?)[\'"]'
        id,wd,ht, jsurl=re.findall(regid,result)[0]
        finalpageUrl=''
        headers=[('Referer',pageURl),('User-Agent',agent)]                       


        jsresult = getUrl(jsurl, headers=headers, cookieJar=cookieJar)
        broadcast=False
        if not 'bro.adca' in jsresult:
            regjs='src=[\'"](.*?)[\'"]'
            embedUrl=re.findall(regjs,jsresult)[0]
            embedUrl+=id+'&vw='+wd+'&vh='+ht
        else:
            broadcast=True
            regjs="var url = '(.*?)'"
            embedUrl=re.findall(regjs,jsresult)[0]
            embedUrl='http://bro.adca.st'+embedUrl+id+'&width='+wd+'&height='+ht
        headers=[('Referer',altref if not altref==None else mainref),('User-Agent',agent)]                             
        result=getUrl(embedUrl, headers=headers, cookieJar=cookieJar)

        if not broadcast:# in result:
            print 'in not broad', embedUrl,result
            if 'blockscript=' in result or 'name="blockscript"' in result: #ok captcha here
                try:
                    tries=0
                    while ('blockscript=' in result  or 'name="blockscript"' in result) and tries<2:
                        print 'in while'
                        tries+=1
                        xval=re.findall('name="x" value="(.*?)"',result)[0]
                        urlval=re.findall('name="url" value="(.*?)"',result)[0]
                        blocscriptval=re.findall('name="blockscript" value="(.*?)"',result)[0]
                        
                        #imageurl=re.findall('<td nowrap><img src="(.*?)"',result)[0].replace('&amp;','&')        
                        scriptype='sci'
                        try:
                            scriptype=re.findall('script=(.*?)&',result)[0]
                        except: pass
                        
                        imageurl='http://hdcast.org/blockscript/detector.php?blockscript=%s&x=%s'%(scriptype,urllib.quote_plus(xval))
                        
                        if not imageurl.startswith('http'):
                            imageurl='http://hdcast.org'+imageurl
                        headersforimage=[('Referer',embedUrl),('Origin','http://hdcast.org'),('User-Agent',agent)]     
                        captchaval=getHDCastCaptcha(imageurl,cookieJar,headersforimage , tries )
                        if captchaval=="": break
                        post={'blockscript':blocscriptval, 'x':xval, 'url':urlval,'val':captchaval}
                        post = urllib.urlencode(post)
                        
                        result=getUrl(embedUrl,post=post, headers=headersforimage, cookieJar=cookieJar)
                        cookieJar.save (HDCASTCookie,ignore_discard=True)
                        result=getUrl(embedUrl, headers=headers, cookieJar=cookieJar)
                except: 
                    print 'error in catpcha'
                    traceback.print_exc(file=sys.stdout)
            streamurl = re.findall('<div id=[\'"]player.*\s*<iframe.*?src=(.*?)\s',result)
            if len(streamurl)>0:
                headers=[('Referer',embedUrl),('User-Agent',agent)]                             
                html=getUrl(streamurl[0].replace('&amp;','&'),headers=headers, cookieJar=cookieJar)
                streamurl = re.findall('file.?:.?["\'](.*?)["\']',html)
                if len(streamurl)==0:
                    streamurl = re.findall('hls.?:.?["\'](.*?)["\']',html)
                streamurl=streamurl[0]
                cookieJar.save (HDCASTCookie,ignore_discard=True)
                return PlayGen(base64.b64encode(streamurl+'|User-Agent='+agent+'&Referer='+embedUrl))
            if 'rtmp' in result:
                print 'rtmp'
                streamurl= re.findall('"(rtmp.*?)"' , result)[0]
                cookieJar.save (HDCASTCookie,ignore_discard=True)
                return PlayGen(base64.b64encode(streamurl+' timeout=20 live=1')) 
            else:
                Msg="Links not found, try again"
                dialog = xbmcgui.Dialog()
                ok = dialog.ok('Link parsing failed', Msg)
                return False
                
        else:
            headers=[('Referer',embedUrl),('User-Agent',agent),('X-Requested-With','XMLHttpRequest')]                             
            token=getUrl('http://bro.adca.st/getToken.php',headers=headers, cookieJar=cookieJar )
            token=re.findall('"token":"(.*?)"',token)[0]
            streamurl = re.findall('curl = "(.*?)"',result)[0]
            streamurl=base64.b64decode(streamurl)
            cookieJar.save (HDCASTCookie,ignore_discard=True)
            return PlayGen(base64.b64encode(streamurl+token+'|User-Agent='+agent+'&Referer='+embedUrl))

    except:
        traceback.print_exc(file=sys.stdout)
        return False


        
class InputWindow(xbmcgui.WindowDialog):
    def __init__(self, *args, **kwargs):
        self.cptloc = kwargs.get('captcha')
        self.img = xbmcgui.ControlImage(335,30,524,90,self.cptloc)

        self.addControl(self.img)
        self.setProperty('zorder', "99")
        #self.kbd = xbmc.Keyboard()

    def get(self):
        self.show()
        xbmc.sleep(3000)            
        #self.kbd.doModal()
        #if (self.kbd.isConfirmed()):
        #    text = self.kbd.getText()
        #    self.close()
        text=xbmcgui.Dialog().input('Enter Captcha', type=xbmcgui.INPUT_ALPHANUM)
        self.close()
        return text
        return False  
        
    def showme():
        self.setProperty('zorder', "-1")

def tst():
    retcaptcha=""
    if 1==1:
        local_captcha = os.path.join(profile_path, "captchaC.img" )
        #localFile = open(local_captcha, "wb")
        #localFile.write(getUrl(imageurl,cookieJar,headers=[('Referer',logonpaged),('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36')]))
        #localFile.close()
        cap=""#cap=parseCaptcha(local_captcha)
        #if originalcaptcha:
        #    cap=parseCaptcha(local_captcha)
        #print 'parsed cap',cap
        if cap=="":
            solver = InputWindow(captcha=local_captcha)
            retcaptcha = solver.get()
            
def getHDCastCaptcha(imageurl,cookieJar, headers, tries):
    retcaptcha=""
    if 1==1:
        local_captcha = os.path.join(profile_path, "captchaC%s.img"%str(tries) )
        localFile = open(local_captcha, "wb")
        localFile.write(getUrl(imageurl,cookieJar,headers=headers))
        localFile.close()
        cap=""#cap=parseCaptcha(local_captcha)
        #if originalcaptcha:
        #    cap=parseCaptcha(local_captcha)
        #print 'parsed cap',cap
        if cap=="":
            solver = InputWindow(captcha=local_captcha)
            retcaptcha = solver.get()
    return retcaptcha
    
def playHDFree(url):
    try:

        #url='http://hdfree.tv/watch/2/sky-sports-1-hd-live-stream.html'
        pageURl = url
        mainref='http://hdfree.tv/tvlogos.html'
        headers=[('Referer',mainref),('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36')]                       
        result = getUrl(url, headers=headers)
        #print result
        firstframe=re.findall( '<iframe frameborder="0.*?src="(.*?)"', result)
        if len(firstframe)==0:
            firstframe=re.findall( '<iframe.*?src="(.*?)"', result)
            
        firstframe=firstframe[0]
        
        headers=[('Referer',pageURl),('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36')]                       
        result = getUrl(firstframe, headers=headers)
        #print result
        regid='<script.*?id=[\'"](.*?)[\'"].*?width=(.*?)\;.*?height=(.*?)\;.*?src=[\'"](.*?)[\'"]'
        id,wd,ht, jsurl=re.findall(regid,result)[0]
        finalpageUrl=''
        headers=[('Referer',firstframe),('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36')]                       
        jsresult = getUrl(jsurl, headers=headers)
        regjs='src=[\'"](.*?)[\'"]'
        embedUrl=re.findall(regjs,jsresult)[0]
        embedUrl+=id+'&vw='+wd+'&vh='+ht
        headers=[('Referer',firstframe),('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36')]                             
        print embedUrl
        result=getUrl(embedUrl, headers=headers)
        
        result= result.replace('","','').replace('["','').replace('"]','').replace('.join("")',' ').replace(r'\/','/')

        vars = re.findall('var (.+?)\s*=\s*(.+?);',result)
        inners = re.findall('id=(.+?)>([^<]+)<',result)
        inners = dict(inners)

        js = re.findall('srcs*=s*(?:\'|\")(.+?player\.js(?:.+?|))(?:\'|\")',result)
        if len(js)==0 and 'cast4u.tv' in result:
            reg='file: ["\'](http.*?)["\']'
            r=re.findall(reg,result)
            if len(r)==0:
                reg='file: ["\'](http.*?)["\']'
                r=re.findall(reg,result)
            r=r[0]
            PlayGen(base64.b64encode(r))
        else:
            
            js=js[0]
            js = getUrl(js, headers=headers)
            token = re.findall('securetoken: ([^\n]+)',result)[0]
            token = re.findall('var\s+%s\s*=\s*(?:\'|\")(.+?)(?:\'|\")' % token, js)[-1]

            for i in range (100):
                for v in vars:
                    result = result.replace('  + %s'%v[0],v[1])
            for x in inners.keys():
                result = result.replace('  + document.getElementById("%s").innerHTML'%x,inners[x])

            
            fs = re.findall('function (.+?)\(\)\s*\{\s*return\(([^\n]+)',result)
            url = re.findall('file:(.+?)\s*\}',result)[0]
            for f in fs:
                    url = url.replace('%s()'%f[0],f[1])
            url = url.replace(');','').split(" + '/' + ")
            streamer, file = url[0].replace('rtmpe','rtmp').strip(), url[1]
            url=streamer + '/ playpath=' + file + ' swfUrl=http://www.hdcast.info/myplayer/jwplayer.flash.swf flashver=' + "WIN\2021,0,0,242" + ' live=1 timeout=20 token=' + token + ' pageUrl=' + embedUrl
            
            print url
            PlayGen(base64.b64encode(url))

    except:
        traceback.print_exc(file=sys.stdout)
        return

def AddInfiniteChannels(url):

    headers=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36')]               
    addDir(Colored("All times in UTC, Blue ones are LIVE now","red") ,"" ,0 ,'', False, True,isItFolder=False)		#name,url,mode,icon
    mainhtml=getUrl(base64.b64decode('aHR0cDovL3d3dy5sYW9sYTEudHYvZW4taW50L2xpdmUtc2NoZWR1bGU='),headers=headers)
    elements=mainhtml.split('<li class="item list-sport')# re.findall('<time.*?>(.*?)<.*\s*.*\s*.*\s*<span.*?>(.*?)<.*\s*.*\s*.*\s*.*?src="(.*?)".*\s*.*\s*.*\s*.*?href="(.*?)".*\s.*?h3>(.*?)<.*\s*.*?h2>(.*?)<',mainhtml)
    print 'starting'
    for el in elements[1:40]:
        
        cc=re.findall('<time.*?>(.*?)<.*?displaymo.*?>(.*?)<.*?img.*?src="([^"]+)".*?h3>([^<]+)<.*?h2>([^<]+)<.*?href="([^"]+)".*?data-sstatus="([^"]+)"',el,re.DOTALL)[0]
        res=re.findall('<dt class="full">Available in.*?<dd>(.*?)<\/dd>',el,re.DOTALL)
        restext=""
        try:
            if len(res)>0:
                res=res[0]
                if "Worldwide" in res:
                    restext="Worldwide"
                if "except" in res:
                    restext+=" Except "
                    restext+=res.split('except')[1].split('>')[1].split('<')[0]
                if len(restext)==0:
                    restext="Only in "
                    restext+=res.split('>')[1].split('<')[0]
        except: pass
            
        mm=11
        col='ZM'
        #print 'xxxxxxxxxxx'
        #print 'name' in cc
        name='%s %s %s\n%s'%(Colored(cc[0], 'red'),Colored(cc[1],col),cc[4],Colored(cc[4],('blue' if cc[6]=="4" else "white")  ))
        if len(restext)>0:
            name+= Colored(' [%s]'%restext, 'red')
        
        
        
        url=cc[5]
        logo=cc[2]
        #print name, logo
        if not logo.startswith('http'):
            logo= 'http:'+logo
        if not url.startswith('http'):
            url= base64.b64decode('aHR0cDovL3d3dy5sYW9sYTEudHY=')+url
            
        addDir(name ,base64.b64encode('infi:'+url) ,mm ,logo, False, True,isItFolder=True)		#name,url,mode,icon
    
    
    
def AddHDFreeChannels(url):

    headers=[('Referer',"http://customer.safersurf.com/onlinetv.html"),('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'),('X-Requested-With','XMLHttpRequest')]               
    headers=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36')]               
    
    mainhtml=getUrl('http://hdfree.tv/tvlogos.html',headers=headers)
    #if 'quiv="refresh' in mainhtml:
    #    mainhtml=getUrl(re.findall('url=(.*?)"',mainhtml)[0])
    #print jsondata
    elements=re.findall('<a href=[\'"](.*?)[\'"].*?img.*?src=[\'"](.*?)[\'"]',mainhtml)
    #print elements
    #print jsondata
    #jsondata=json.loads(jsondata)
    for cc in elements:

        mm=11
        col='ZM'
        #print 'xxxxxxxxxxx'
        #print 'name' in cc
        name=cc[0]
        name=name.split('/')[-1]
        
        if '-live-stream' in name:
            name=name.split('-live-stream')[0]
        url=cc[0]
        logo=cc[1]
        #print name, logo
        if not logo.startswith('http'):
            logo= 'http://hdfree.tv'+logo
        addDir(ColoredOpt(name.capitalize(),col) ,base64.b64encode('hdfree:'+url) ,mm ,logo, False, True,isItFolder=True)		#name,url,mode,icon
    

        
def AddSafeChannels(url):
    import safelinks
    print url
    cname,curlmedia=url.decode("base64").split(',')
    addDir(Colored('Channel Language [%s] .\nPlease Click again if fails first time'.capitalize()%cname,'red') ,'' ,0 ,'', False, True,isItFolder=False)
    for cc in safelinks.getSafeChannels(url):
        addDir(cc[0] ,cc[1] ,cc[2] ,cc[3], False, True,isItFolder=False)
    
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
        addDir(ColoredOpt(cname.capitalize(),'ZM') ,base64.b64encode(curl) ,mm ,imgurl, False, True,isItFolder=False)		#name,url,mode,icon
    return  


#YXBwPTEgc2xvd3R2IGFrYSBzb2xpZGlwdHYgZnJvbSBwbGF5c3RvcmUgYW5kIGFwcD0yIGlzIHB0diBzcG9ydHMgZnJvbSBwbGF5c3RvcmU=
def AddNetworkTVSports2(url=None,apptype=None):  

    if url=="sss":
        cats=[NetworkTVCatIDByName2("Sports",apptype=apptype, findin=True)]
        try:
            cats.append(NetworkTVCatIDByName2("cricket",apptype=apptype, findin=True))
        except: pass
        isSports=True
        addDir(Colored('>>Click here for All Categories<<'.capitalize(),'red') ,"networktv2" if apptype==1 else "networktv3",66 ,'', False, True,isItFolder=True)
    else:
        cats=[url]
        isSports=False
    for cname,ctype,curl,imgurl in getNetworkTVChannels2(cats,sports=True,apptype=apptype):
        cname=cname.encode('ascii', 'ignore').decode('ascii')
        if ctype=='manual2':
            mm=37
        elif ctype=='manual3':
            mm=45
        else:
            mm=11
        addDir(ColoredOpt(cname.capitalize(),'ZM') ,base64.b64encode(curl) ,mm ,imgurl, False, True,isItFolder=False)		#name,url,mode,icon
    return       
    
def AddNetworkTVSports(url=None):  

    if url=="sss":
        cats=[NetworkTVCatIDByName("Sports")]
        isSports=True
        addDir(Colored('>>Click here for All Categories<<'.capitalize(),'red') ,"networktv",66 ,'', False, True,isItFolder=True)
    else:
        cats=[url]
        isSports=False
    for cname,ctype,curl,imgurl in getNetworkTVChannels(cats,sports=True):
        cname=cname.encode('ascii', 'ignore').decode('ascii')
        if ctype=='manual2':
            mm=37
        elif ctype=='manual3':
            mm=45
        else:
            mm=11
        addDir(ColoredOpt(cname.capitalize(),'ZM') ,base64.b64encode(curl) ,mm ,imgurl, False, True,isItFolder=False)		#name,url,mode,icon
    return        
    
def AddFastSport(url=None):   
    clist=[]
    if url=="sss":
        cats=fastCatIDByName('SPORTS TV')
        isSports=True
        addDir(Colored('>>Click here for All Categories<<'.capitalize(),'red') ,"fasttv",66 ,'', False, True,isItFolder=True)
    else:
        cats=url
        isSports=False
    for cname,ctype,curl,imgurl in getFastTVChannels(cats,sports=True):
        cname=cname.encode('ascii', 'ignore').decode('ascii')
        if ctype=='manual2':
            mm=37
        elif ctype=='manual3':
            mm=45
        else:
            mm=11
        addDir(ColoredOpt(cname.capitalize(),'ZM') ,base64.b64encode(curl) ,mm ,imgurl, False, True,isItFolder=False)		#name,url,mode,icon
    return        
def AddUniTVSports(url=None):   

    if url=="sss":
        cats=['Extra Time','TSN','Cth Stadium','UFC','T20 World Cup','Horse Racing','Cricket','Footbal','Sports','Golf','Boxing & Wrestling','T20 Big Bash League','NFL Live','Footbal Clubs','Sports Time']
        isSports=True
        addDir(Colored('>>Click here for All Categories<<'.capitalize(),'red') ,"unitv",66 ,'', False, True,isItFolder=True)
    else:
        cats=[url]
        isSports=False
    for cname,ctype,curl,imgurl in getUniTVChannels(cats,isSports, desi=False):
        cname=cname.encode('ascii', 'ignore').decode('ascii')
        if ctype=='manual2':
            mm=37
        elif ctype=='manual3':
            mm=45
        else:
            mm=11
        addDir(ColoredOpt(cname.capitalize(),'ZM') ,base64.b64encode(curl) ,mm ,imgurl, False, True,isItFolder=False)		#name,url,mode,icon
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
        if name.lower()=="movies":
            cats.append(('emovies:{"lang":"hindi","type":"main"}','Hindi - Einthusan Movies'))
            cats.append(('emovies:{"lang":"hindi","type":"main"}','Punjabi - Einthusan Movies'))
        cats+=getPV2Cats(True if name.lower()=="movies" else False)

        
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
    elif url=="networktv":
        cats=getNetworkTVCats()
        cmode=94
    elif url=="networktv2":
        cats=getNetworkTVCats2(apptype=1)
        cmode=96
    elif url=="networktv3":
        cats=getNetworkTVCats2(apptype=2)
        cmode=98
    elif url=="fasttv":
        cats=[]
        for p in getFastCats()["LIVETV"]:
            cats.append((p["cid"],p["category_name"]))
        cmode=92               
    for cname in cats:
        print cname
        if type(cname).__name__ == 'tuple':
            cid,cname=cname
            cname=cname.encode("utf-8")
        else:
            cid=cname
        addDir(ColoredOpt(cname.capitalize(),'red') ,cid,cmode,'', False, True,isItFolder=True)
        

    
def AddStreamSports(url=None):
    jsondata=getUrl('http://videostream.dn.ua/list/GetLeftMenuShort?lng=en')
    sources= json.loads(jsondata)
    ret=[]
    addDir('Refresh' ,'Live' ,39,'')
    for source in sources["Value"]:
        cname=ColoredOpt(source["Sport"] ,'EB')
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
        res=res.split('Handle_WLSeriesDetailsObj(')[1][:-1]
        print 'res',res
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
        res=res.split('Handle_WLSeriesDetailsObj(')[1][:-1]
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
    
def getHDCASTCookieJar(updatedUName=False):
    cookieJar=None
    try:
        cookieJar = cookielib.LWPCookieJar()
        if not updatedUName:
            cookieJar.load(HDCASTCookie,ignore_discard=True)
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
            loginurl=base64.b64decode('aHR0cHM6Ly93aWxsb3cudHYvbG9naW4=')
            loginpage = getUrl(loginurl,cookieJar=cookieJar)
            token=re.findall('name="csrf_token".*?value=["\'](.*?)["\']',loginpage)[0]
            
            headers=[('Referer',loginurl),('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'),('Origin','https://www.willow.tv')]                      
            post = {'login':willow_username,'password':willow_pwd,'submit':'Sign In','csrf_token':token}
            post = urllib.urlencode(post)
            mainpage = getUrl(loginurl,cookieJar=cookieJar,post=post,headers=headers )
            cookieJar.save (WTVCOOKIEFILE,ignore_discard=True)
            selfAddon.setSetting( id="lastSuccessLogin" ,value=willow_username)
            mainpage = getUrl(url,cookieJar=cookieJar)
        
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
            priority=''
            if mode==21:
                WLlive=True
#                print 'matchid',matchid
                matchid,source_sectionid=matchid.split(':')
                st='LiveMatch'
                url=base64.b64decode('aHR0cDovL3d3dy53aWxsb3cudHYvRXZlbnRNZ210LyVzVVJMLmFzcD9taWQ9JXM=')%(st,matchid)
                pat='secureurl":"(.*?)".*?priority":%s,'%source_sectionid    
                priority=source_sectionid
                calltype='Live'                
            else:
                if ':' in matchid:
                    matchid,source_sectionid=matchid.split(':')
                    st='Replay'
                    url=base64.b64decode('aHR0cHM6Ly93d3cud2lsbG93LnR2L0V2ZW50TWdtdC9SZXBsYXlVUkwuYXNwP21pZD0lcyZ1c2VySWQ9JXM=')%(matchid,userid)
                    pat='secureurl":"(.*?)".*?priority":%s,'%source_sectionid    
                    priority=source_sectionid
                    calltype='RecordOne'     
                else:
                    returnParts=True
                    st='Replay'
                    url=base64.b64decode('aHR0cHM6Ly93d3cud2lsbG93LnR2L0V2ZW50TWdtdC9SZXBsYXlVUkwuYXNwP21pZD0lcyZ1c2VySWQ9JXM=')%(matchid,userid)
                    pat='"priority":(.+?),"title":"(.*?)",'
                    priority=""
                    calltype='RecordAll' 
            
            videoPage = getUrl(url,cookieJar=cookieJar)    

            final_url=''
        
#            print 'calltype',calltype,mode
#            print videoPage
#            print pat
            if calltype=='Live' or calltype=='RecordOne':
                #videoPage='},\n{'.join(videoPage.split("},{"))
                print videoPage
                jdata=json.loads(videoPage)
                
                if calltype=='Live':
                    for d in jdata["roku"]["URL"]:
                        if int(d["priority"])==int(priority):
                            final_url=d["secureurl"]
                            break;
                
                else:
                
                    for dd in jdata["replay"]:
                        for d in dd:
                            if int(d["priority"])==int(priority):
                                final_url=d["secureurl"]
                                break;
                print pat,videoPage
                #final_url=re.findall(pat,videoPage)[0]
            else:
                #final_url=re.findall(pat,videoPage)
                final_url2=''
                #for u in final_url:
                jdata=json.loads(videoPage)
                print jdata
                for dd in jdata["replay"]:
                    for d in dd:
                        print d
                        final_url2+='#'+str(d["priority"]) +' ' +d["title"].replace(',','')+'='+str(d["priority"])+','
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
        loginworked,cookieJar= performWillowLogin();
        for m in matchdata["result"]:
            if "BGUrl" in m and  (not m["BGUrl"]=="") and (base64.b64decode('d3p2b2Q6') in m["BGUrl"] or base64.b64decode('Ymd2b2Q=') in m["BGUrl"]  or base64.b64decode("d2x2b2Q=") in m["BGUrl"] ):
                rurl=m["BGUrl"]
                print 'rurl',rurl
                if base64.b64decode('d3p2b2Q6') in rurl:
                    rurl=rurl.replace(base64.b64decode('d3p2b2Q6Ly8='),base64.b64decode('aHR0cDovLzM4Ljk5LjY4LjE2MjoxOTM1L3dsbHd2b2QvX2RlZmluc3RfL3dsdm9kL3NtaWw6'));
                    rurl=rurl.replace('.mp4',base64.b64decode('X3dlYi5zbWlsL3BsYXlsaXN0Lm0zdTg='));
                elif base64.b64decode("d2x2b2Q=")  in m["BGUrl"]:
                    rurl=base64.b64decode("aHR0cHM6Ly93d3cud2lsbG93LnR2L0V2ZW50TWdtdC93ZWJzZXJ2aWNlcy9nZXRIaWdobGlnaHRVUkwuYXNwP3ZvZHVybD0=")+urllib.quote_plus(rurl)
                    rurl=getUrl(rurl, cookieJar=cookieJar)
                    rurl=json.loads(rurl)["url"]
                else:
                    rurl=rurl.replace('bgvod:/','')
                    data={"bgvodurl":rurl}
                    rurl=getUrl(base64.b64decode('aHR0cHM6Ly93d3cud2lsbG93LnR2L0V2ZW50TWdtdC93ZWJzZXJ2aWNlcy9nZXRCR0hnbHRVcmwuYXNw?')+urllib.urlencode(data))
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
        liveadded=False
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
                            addDir(ColoredOpt('Source %s %s '%(str(video["priority"]), video["player"]),'ZM',True) +entry_name ,match_id+':'+str(video["priority"]),21,'', False, True,isItFolder=False)		#name,url,mode,icon
                            liveadded=True
        if not liveadded:
            addDir(Colored('     ----No Live Games----','red',True) ,'' ,-1,'', False, True,isItFolder=False)		#name,url,mode,icon
                
                
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
    import scdec
    channeladded=False
    try:
        for source in scdec.getlinks():
            if 1==1:#ctype=='liveWMV' or ctype=='manual':
    #                print source
                addDir (source[0],source[1],source[2],'', False, True,isItFolder=False)		#name,url,mode,icon
                channeladded=True
        if not channeladded:
            cname='No streams available'
            curl=''
            addDir('    -'+cname ,curl ,-1,'', False, True,isItFolder=False)		#name,url,mode,icon 
    except:  traceback.print_exc(file=sys.stdout)
    addDir('Refresh Listing' ,'Live' ,144,'')

    addDir('Refresh Fetch Code' ,'Live' ,97,'')

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
    print 'link',link
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
    elif 'p3g.tv/resources' in link or '247bay.tv'  in link :
        c=''
        ccommand=''
        swfUrl=base64.b64decode('aHR0cDovL3d3dy4yNDdiYXkudHYvc3RhdGljL3NjcmlwdHMvZXBsYXllci5zd2Y=')
        sitename='www.247bay.tv'
        pat_e='channel.*?g=\'(.*?)\''
        loadbalanacername='www.publish247.xyz'
        app='stream'
        pat_js='channel=\'(.*?)\''
    elif 'janjuaplayer.com/resources' in link:
        c='zenataStoGoPuknalaGavolot'
        ccommand=''
        swfUrl=base64.b64decode('aHR0cDovL3d3dy5qYW5qdWFwbGF5ZXIuY29tL3Jlc291cmNlcy9zY3JpcHRzL2VwbGF5ZXIuc3dm')
        sitename='www.janjuaplayer.com'
        pat_e='channel.*?g=\'(.*?)\''
        loadbalanacername='www.janjuapublisher.com'
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
    print 'match_flash',match_flash
    matchid=match_flash.split('id=')[1].split('&')[0]
    if 'pk=' in match_flash:
        matchid+="&pk="+match_flash.split('pk=')[1].split('\'')[0].split('\"')[0]
    
    lb_url='http://%s:1935/loadbalancer?%s'%(loadbalanacername,matchid.split('&')[0])
        
    req = urllib2.Request(lb_url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')
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
    
    url='rtmp://%s/%s playpath=%s?id=%s pageUrl=%s swfUrl=%s Conn=S:OK %s flashVer=WIN\\2022,0,0,209 live=true timeout=20'%(ip,app,sid,matchid,match_urljs,swfUrl,ccommand)
    print url
    
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
    
        sess= getYPSession()
        print 'sess',sess
        pageurl='http://www.yupptv.com/Account/OctoNewFrame.aspx?ChanId=%s'%videoid 
        print pageurl
        emhtm=getUrl(pageurl,headers=[('Cookie',sess),('Referer','http://www.yupptv.com/Livetv/'),('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')])
        print 'after em'
        rr='file:\'(http.*?)\''    
        finalUrl=re.findall(rr,emhtm)
        print 'finalUrl',finalUrl
        #if len(finalUrl)==0:
        #    
        #    pageurl='http://stream.yupptv.com/PreviewPaidChannel.aspx?cid=%s'%videoid  
        #    #emhtm=getUrl(pageurl)
        #    emhtm=getUrlFromUS(pageurl)
        #    rr='file:\'(http.*?)\''    
        #    finalUrl=re.findall(rr,emhtm)
        ret=finalUrl[0]
        
    except: 
        traceback.print_exc(file=sys.stdout)
    return ret
    
def playMYTV(url):
    url = base64.b64decode(url)
    #print 'gen is '+url
    headers=[('User-Agent','sport%20TV%20Live/2.7 CFNetwork/758.0.2 Darwin/15.0.0')]
    jsondata=getUrl(base64.b64decode('aHR0cDovL21lZGlhb25zcG9ydC5kZS90di9zcG9ydGlvcy9hcGkucGhwP2NoYW5uZWxfaWQ9JXM=')%url,headers=headers)
    jsondata=json.loads(jsondata)
    
    PlayGen(base64.b64encode( jsondata["LIVETV"][0]["channel_url"]+'|User-Agent=NSPlayer/7.10.0.3059'))
        

        
def PlayYP(url):
    url = base64.b64decode(url)
    #print 'gen is '+url

    finalUrl=getYPUrl(url)
    if '.f4m' in finalUrl:
        finalUrl=urllib.quote_plus(finalUrl+'&g=FLONTKRDWKGI&hdcore=3.2.0&amp;plugin=jwplayer-3.2.0.1|Referer=http://stream.yupptv.com/PreviewPaidChannel.aspx?cid=195')
        finalUrl='plugin://plugin.video.f4mTester/?url='+finalUrl
            
            
        xbmc.executebuiltin("xbmc.PlayMedia("+finalUrl+")")
    else:
        PlayGen(base64.b64encode( finalUrl+'|User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36'))

def getFootVideoUrl(ftype,url ):
    if ftype in ["facebook","vidme","espn", "streamable"]:  
        headers=[('User-Agent',base64.b64decode('TGl2ZSBGb290YmFsbCBvbiBUViAzLjAuMSAoaVBob25lOyBpUGhvbmUgT1MgOS4wLjI7IGVuX0dCKQ=='))]
        htmlcontents=url
        print 'ftype',ftype
        if ftype not in ["espn"]:
            htmlcontents=getUrl(url,headers=headers)
        fbData=getFootballData()
        post=getFootballPostData()
        urlnew=fbData["API_URLS"]["PARSE_TOOL"]
        post['content_html']=htmlcontents
        post['video_type']=ftype
        post = urllib.urlencode(post)
        url=json.loads(getUrl(urlnew, post=post,headers=headers))["video_url"]
    elif  ftype =="LIVE":
        print 'do live'
        
    return url
    
 
def PlayFootballVideo(url):
    ftype,url = url.split(',')
    url=base64.b64decode(url)

    url=getFootVideoUrl(ftype,url)
    if 'youtube.com' in url:
        youtubecode=url.split('?v=')[1].split('&')[0]
        uurl = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % youtubecode
        xbmc.executebuiltin("xbmc.PlayMedia("+uurl+")")
    else:
        url+='|User-Agent=AppleCoreMedia/1.0.0.13A452 (iPhone; U; CPU OS 9_0_2 like Mac OS X; en_gb)'

        playlist = xbmc.PlayList(1)
        playlist.clear()
        listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
        playlist.add(url,listitem)
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(playlist)         


def PlayGen(url,checkUrl=False, followredirect=False):
    url = base64.b64decode(url)
    print 'gen is '+url

    if url.startswith('plugin://'):
        xbmc.executebuiltin("xbmc.PlayMedia("+url+")")
        return
    
    if checkUrl and url.startswith('http') and '.m3u' in url:
        headers=[('User-Agent','AppleCoreMedia/1.0.0.13A452 (iPhone; U; CPU OS 9_0_2 like Mac OS X; en_gb)')]
        urldata=getUrl(url.split('|')[0],timeout=5,headers=headers).strip()
        if followredirect:
            if not urldata.startswith('#EXTM3U'):
                url=urldata+'|'+url.split('|')[1]
            if 'jio.com' in url and 'EXT-X-STREAM-INF' in urldata:
                print 'settingup'
                import urlparse
                url=urlparse.urljoin(url.split('|')[0],re.findall('#EXT-X-STREAM-INF.*\s(.*)',urldata)[-1])+'|'+url.split('|')[1]
                

            
    playlist = xbmc.PlayList(1)
    playlist.clear()
    listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )

    try:
        if '.m3u8' in url :
            listitem.setMimeType("flv-application/octet-stream");
            listitem.setContentLookup(False)
        elif '.ts' in url:
            listitem.setMimeType("video/mp2t");
            listitem.setContentLookup(False)
    except: print 'error while setting setMimeType, so ignoring it '
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
    elif type=='viralvideos':
        AddShows(viralvideos)    
    elif '(Siasat.pk)' in name:
        AddShowsFromSiasat(url)
    elif type=='ProgTalkShows':
        AddProgramsAndShows('http://www.zemtv.com/')
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
                
                ret_match=getChannelsFromEbound();#AddChannels()
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
            
def getMyTVChannels():
    ret=[]
    try:
        xmldata=getMYTVPage()
        for ss in xmldata["LIVETV"]:
            
            cname=ss["channel_title"]
            curl='mytv:'+ss["id"]#+'|User-Agent=AppleCoreMedia/1.0.0.13A452 (iPhone; U; CPU OS 9_0_2 like Mac OS X; en_gb)'
            cimage='http://mediaonsport.de/tv/sportios/images/'+ss["channel_thumbnail"]
            
            
            if len([i for i, x in enumerate(ret) if x[2] ==curl ])==0:                    
                ret.append((cname ,'manual', curl ,cimage))   
        if len(ret)>0:
            ret=sorted(ret,key=lambda s: s[0].lower()   )
    except:
        traceback.print_exc(file=sys.stdout)
    return ret

def fastCatIDByName(catname, findin=False):
    retId=''
    for p in getFastCats()["LIVETV"]:
        if p["category_name"].lower()== catname.lower() or (findin and catname.lower() in p["category_name"].lower()):
            return p["cid"]
    return retId

def getNetworkTVCats():
    retval=[]
    for c in getNetworkTVPage()["cats"]:
        retval.append((c["cat_id"],c["cat_name"]))
    return retval#
    
def getNetworkTVCats2(apptype):
    retval=[]
    for c in getNetworkTVPage2(apptype)["categories"]["live"]:
        retval.append((c["category_id"],c["category_name"]))
    return retval#

def NetworkTVCatIDByName2(catname, findin=False,apptype=1):
    retId=''
    for p in getNetworkTVPage2(apptype)["categories"]["live"]:
        print 'p is',p
        if p["category_name"].lower()== catname.lower() or (findin and catname.lower() in p["category_name"].lower()):
            return p["category_id"]
    return retId
    
def NetworkTVCatIDByName(catname, findin=False):
    retId=''
    for p in getNetworkTVPage()["cats"]:
        if p["cat_name"].lower()== catname.lower() or (findin and catname.lower() in p["cat_name"].lower()):
            return p["cat_id"]
    return retId

def getNetworkTVChannels2(cat=None,sports=False, liveflag="1", streamtype="live", removeprefix=None,apptype=1):
    ret=[]
    try:
        xmldata=getNetworkTVPage2(apptype)
   
            
        #print 'got getNetworkTVPage2',cat,xmldata
        for source in xmldata["available_channels"]:
            #print 'ss',source
            source=xmldata["available_channels"][source]
            #print 'ss',source
            if (cat==None or source["category_id"] in cat):# and (country ==None or  source["country_name"] in country):#source["categoryName"] in categories or (forSports):# and ('sport' in source["categoryName"].lower() or 'BarclaysPremierLeague' in source["categoryName"] )    ) :
                if source["live"]==liveflag and streamtype==source["stream_type"]:
                    ss=source
                    cname=ss["name"]
                    #print cname
                    if 1==2:# 'ebound.tv' in ss["streamurl"]:
                        #print ss["channelLink"]
                        curl='ebound2:'+ss["streamurl"].replace(':1935','')
                    else:
                        #curl='networktv:'+ss["streamurl"]
                        curl='networktv2:%s:%s'%(str(apptype),str(ss["stream_id"]))
                    cimage=ss["stream_icon"]
                    
                    if removeprefix and removeprefix in cname:
                        cname=':'.join(cname.split(removeprefix)[1:]).strip()
                    cname=cname.capitalize()
                    #print cname
                    cname=cname + (' SlowTV' if not sports else '') 
                    if 1==1:#len([i for i, x in enumerate(ret) if x[0] ==cname + (' SlowTV' if not sports else '') ])==0:                    
                        ret.append((cname,'manual', curl ,cimage))
        
        if len(ret)>0:
            ret=sorted(ret,key=lambda s: s[0].lower()   )
    except:
        traceback.print_exc(file=sys.stdout)
    #print ret
    return ret
    
def getNetworkTVChannels(cat=None,sports=False, country=None):
    ret=[]
    try:
        xmldata=getNetworkTVPage()
   
            
        print 'got getNetworkTVPage',cat,xmldata
        for source in xmldata["channels"]:
            print source["cat_id"] 
            if (cat==None or source["cat_id"] in cat) and (country ==None or  source["country_name"] in country):#source["categoryName"] in categories or (forSports):# and ('sport' in source["categoryName"].lower() or 'BarclaysPremierLeague' in source["categoryName"] )    ) :
                
                ss=source
                cname=ss["chname"]
                if 'ebound.tv' in ss["streamurl"]:
                    #print ss["channelLink"]
                    curl='ebound2:'+ss["streamurl"].replace(':1935','')
                else:
                    #curl='networktv:'+ss["streamurl"]
                    curl='networktv:'+str(ss["streamid"])
                cimage=ss["logo"]
                
                if len([i for i, x in enumerate(ret) if x[2] ==curl ])==0:                    
                    ret.append((cname + (' NetTV' if not sports else ''),'manual', curl ,cimage))   
        
        if len(ret)>0:
            ret=sorted(ret,key=lambda s: s[0].lower()   )
    except:
        traceback.print_exc(file=sys.stdout)
    print ret
    return ret
    
def getFastTVChannels(cat,sports=False, catname=None):
    ret=[]
    try:
        if catname:
            cat=fastCatIDByName(catname)
        xmldata=getFastTVPage(cat)
        #print 'got getFastTVChannels',xmldata
        for source in xmldata["LIVETV"]:
            if 1==1:#source["categoryName"] in categories or (forSports):# and ('sport' in source["categoryName"].lower() or 'BarclaysPremierLeague' in source["categoryName"] )    ) :
                ss=source
                cname=ss["channel_title"]
                if 'ebound.tv' in ss["channel_url"]:
                    #print ss["channelLink"]
                    curl='ebound2:'+ss["channel_url"].replace(':1935','')
                else:
                    #curl='fast:'+ss["channel_url"]
                    curl='fast:'+str(cat)+'='+str(ss["id"])
                cimage=ss["channel_thumbnail"]
                
                if not cimage.startswith('http'):
                    cimage=base64.b64decode('aHR0cDovL3N3aWZ0c3RyZWFtei5jb20vU3dpZnRTdHJlYW0vaW1hZ2VzL3RodW1icy8=')+cimage
                
                if len([i for i, x in enumerate(ret) if x[2] ==curl ])==0:                    
                    ret.append((cname + (' fast' if not sports else ''),'manual', curl ,cimage))   
        
        if len(ret)>0:
            ret=sorted(ret,key=lambda s: s[0].lower()   )
    except:
        traceback.print_exc(file=sys.stdout)
    return ret
    
def getPakTVChannels(categories, forSports=False, desi=True):
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
                    ret.append((cname +(' v7' if desi else '') ,'manual', curl ,cimage))   
        
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
            if 1==2 and 'HLSURL' in ss and len(ss["HLSURL"])>0 :
                curl="direct:"+ss["HLSURL"]
            elif 1==2 and 'SamsungURL' in ss  and len(ss["SamsungURL"])>0 :
                curl="direct:"+ss["SamsungURL"]
            else:
                curl="CF:"+ss["ContentId"]
                    
            ret.append((cname +' CF' ,'manual', curl ,cimage))   
        if len(ret)>0:
            ret=sorted(ret,key=lambda s: s[0].lower()   )
    except:
        traceback.print_exc(file=sys.stdout)
    return ret  
    
def getZengaChannels(url,progress):
    ret=[]
    try:
        
        jsondata=getZengaPage(url,progress)
        print 'jsondata',jsondata
        for js in jsondata:

            cname=js["title"]
            cimage=base64.b64decode('aHR0cDovL2Qzam5rcDNscnMyaGQ1LmNsb3VkZnJvbnQubmV0L2ltYWdlcy8zMjB4MTgwLyVzLmpwZw==')%js["uid"]
            curl="zenga:"+js["dvrid"]     
            print curl            
            ret.append((cname +' Zenga' ,'manual', curl ,cimage))   
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
                cname=ss[1]#ss["name"]
                curl=ss[0]#base64.b64decode("ZGl0dG86aHR0cDovL29yaWdpbi5kaXR0b3R2LmNvbS9saXZldHYvJXM=")%urllib.quote_plus(cname)
                if not curl.startswith("http"): curl='http://origin.dittotv.com'+curl
                curl='ditto:'+curl
                try:
                    cname+=" "+ss["manual"]
                except: pass
                
                cimage=ss[2]#ss["poster"].replace('\\/','/')
                
                
                if len([i for i, x in enumerate(ret) if x[2] ==curl ])==0:                    
                    ret.append((cname +' ditto' ,'manual', curl ,cimage))   
        if len(ret)>0:
            ret=sorted(ret,key=lambda s: s[0].lower()   )
    except:
        traceback.print_exc(file=sys.stdout)
    return ret    

def getIpBoxSourcesAllOtherSource(caller):
    ret=[]
    print 'getIpBoxSourcesAllOtherSource'
    if not caller=="hls":
        try:


            htmls=getUrl("http://www.oneplaylist.eu.pn/")

            servers=re.findall( '>(http:\/\/(.*?)\/.*?get.php.*?)<', htmls)
            print servers
            import time

            for ln in servers[0:25]:
                try:
                    surl,servername=ln
                    servername=servername.split('/')[0].split(':')[0]
                    ret.append((servername, surl.replace('&amp;','&')  ))   
                except: traceback.print_exc(file=sys.stdout)

        except:
            traceback.print_exc(file=sys.stdout)

    return ret
    
def getIpBoxSources(frompakindia=False , caller=None):
    ret=[]
    try:

        if caller=="mpegts" or caller==None:
            servers=getUrl("http://pastebin.com/raw/GrYKMHrF")
        #else:
        #    servers=getUrl("http://pastebin.com/raw/SQfcddBn")
        servers=servers.splitlines()

        import time
        for ln in servers:
            if not ln.startswith("##") and len(ln)>0:
                try:
                    ##serial:mac:time:text
                    print 'ln',ln
                    servername,surl=ln.split('$')
                    
                    ret.append((servername, surl ))   
                except: traceback.print_exc(file=sys.stdout)
    except:
        traceback.print_exc(file=sys.stdout)
    
    if frompakindia:
        return ret
    else:
        return ret+getIpBoxSourcesAllOtherSource(caller)

    
def getIpBoxChannels(url,forSports=False, sort=True):
    ret=[]
    try:
        for u in url:
            try:
                fileheaders,playheaders=None,None
                if '|' in u:
                    u,fileheaders,playheaders=u.split('|')
                    u=u+'|'+fileheaders
                    if '[gettext]' in u:
                        print 'in gettext',u
                        u=getUrl(u.replace('[gettext]',''))
                        if ' ' in u or '>' in u:
                            u=u.replace(' ','%20')
                            u=u.replace('>','%3E')
                            u=u.replace('<','%3C')
                        
                    header_in_page=playheaders.split('&')
                    headers=[]
                    for h in header_in_page:
                        if len(h.split('='))==2:
                            n,v=h.split('=')
                        else:
                            vals=h.split('=')
                            n=vals[0]
                            v='='.join(vals[1:])
                            #n,v=h.split('=')
                        print n,v
                        if n=="User-Agent" and v.startswith('http'):
                            v=getUrl(v)
                            print v
                        headers.append((n,v))
                    playheaders=urllib.urlencode(headers)
                #print 'playheaders',playheaders 
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
                        if 1==1:
                            #curl='direct:'+ss[2].replace('.ts','.ts').replace('\r','')
                            #curl='direct:'+ss[2].replace('.ts','.m3u8').replace('\r','')
                            #curl='ipbox:'+ss[2].replace('\r','').replace('.ts','.ts')#+'|Mozilla/5.0 (Windows NT 6.1 WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36'
                            urlmedia=ss[2]
                            if ' ' in urlmedia or '>' in urlmedia:
                                urlmedia=urlmedia.replace(' ','%20')
                                urlmedia=urlmedia.replace('>','%3E')
                                urlmedia=urlmedia.replace('<','%3C')
                            if playheaders:
                                curl='ipbox:'+urlmedia.replace('\r','')+'|'+playheaders
                            else:
                                curl='ipbox:'+urlmedia.replace('\r','')+'|User-Agent=VLC/2.3.1 LibVLC/2.2.17&Icy-MetaData=1'
                            ##curl='ipbox:'+ss[2].replace('\r','').replace('.ts','.m3u8')+'|User-Agent=VLC/2.2.1 LibVLC/2.2.17&Icy-MetaData=1'
                            #print 'iptv',curl
                            ret.append((cname +' Ipbox' ,'manual', curl ,''))   
                    except: pass
            except: pass
            if len(ret)>0 and sort:
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

    
def getWTVChannels(categories, forSports=False, desi=True):
    ret=[]
    try:
        xmldata=getWTVPage()
        #print xmldata
        #print categories
        for source in xmldata:#Cricket#
            print source["categoryName"] in categories
            if source["categoryName"].strip().lower() in categories or source["categoryName"].strip() in categories or (forSports and ('sport' in source["categoryName"].lower() or 'barclayspremierleague' in source["categoryName"].lower() )    ) :
                print source
                ss=source
                cname=ss["channelName"]
                if cname.lower().startswith('ant man'): continue
                #print cname
                if 'ebound.tv' in ss["channelLink"]:
                    curl='ebound2:'+ss["channelLink"].replace(':1935','')
                else:
                    curl='direct2:'+ss["channelLink"]
                    if ss["channelLink"].startswith('http'): curl+='|User-Agent=AppleCoreMedia/1.0.0.13A452 (iPhone; U; CPU OS 9_0_2 like Mac OS X; en_gb)' 

                #cimage=ss["categoryImageLink"]
                cimage='http://shani.offshorepastebin.com/ZemLogos/%s.png'%cname.lower().replace(' ','')
                
                if len([i for i, x in enumerate(ret) if x[2] ==curl ])==0:                    
                    #print cname
                    ret.append((cname +(' v9' if desi else '')  ,'manual', curl ,cimage))   
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
                
                if 'ebound.tv' in ss["channelLink"]:
                    curl='ebound2:'+ss["channelLink"].replace(':1935','')
                else:
                    curl='direct2:'+ss["channelLink"]
                    if ss["channelLink"].startswith('http'): curl+='|User-Agent=AppleCoreMedia/1.0.0.13A452 (iPhone; U; CPU OS 9_0_2 like Mac OS X; en_gb)' 

                #cimage=ss["categoryLogo"]
                cimage='http://shani.offshorepastebin.com/ZemLogos/%s.png'%cname.lower().replace(' ','')
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

                #cimage=ss["categoryImageLink"]
                cimage='http://shani.offshorepastebin.com/ZemLogos/%s.png'%cname.lower().replace(' ','')
                
                
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
        
def getUniTVChannels(categories, forSports=False, desi=True):
    ret=[]
  
    try:
        xmldata=getUniTVPage()
        #print xmldata
        for source in xmldata:#Cricket#
            if source["categoryName"].strip() in categories or source["categoryName"] in categories or (forSports and ('sport' in source["categoryName"].lower() or 'BarclaysPremierLeague' in source["categoryName"] )    ) :

                ss=source
                cname=ss["channelName"]
                #print ss
                if 'ebound.tv' in ss["channelLink"]:
                    curl='ebound2:'+ss["channelLink"].replace(':1935','')
                    #print curl
                else:
                    curl='direct2:'+ss["channelLink"]
                    if ss["channelLink"].startswith('http'): curl+='|User-Agent=AppleCoreMedia/1.0.0.13A452 (iPhone; U; CPU OS 9_0_2 like Mac OS X; en_gb)' 
                #cimage=ss["categoryImageLink"]
                cimage='http://shani.offshorepastebin.com/ZemLogos/%s.png'%cname.lower().replace(' ','')
                
                if len([i for i, x in enumerate(ret) if x[2] ==curl ])==0:                    
                    #print cname
                    ret.append((cname +(' v8' if desi else '') ,'manual', curl ,cimage))   
        if len(ret)>0:
            ret=sorted(ret,key=lambda s: s[0].lower()   )
    except:
        traceback.print_exc(file=sys.stdout)
    return ret  
    
def getUKTVUserAgent():
    try:
        username = "-1"#random.choice(usernames)
        post = {'version':'5.7'}
        post = urllib.urlencode(post)
      
        headers=[('User-Agent','USER-AGENT-UKTVNOW-APP-V2'),('app-token',getAPIToken(base64.b64decode("aHR0cDovL3VrdHZub3cubmV0L2FwcDIvdjMvZ2V0X3VzZXJfYWdlbnQ="),username))]
        jsondata=getUrl(base64.b64decode("aHR0cDovL3VrdHZub3cubmV0L2FwcDMvdjMvZ2V0X3VzZXJfYWdlbnQ="),post=post,headers=headers)
        jsondata=json.loads(jsondata)    
        import pyaes
        try:
            if 'useragent' in jsondata["msg"]:
                return jsondata["msg"]["useragent"]
        except: 
            pass
        key="MDk0NTg3MjEyNDJhZmZkZQ==".decode("base64")
        iv="ZWVkY2ZhMDQ4OTE3NDM5Mg==".decode("base64")
        decryptor = pyaes.new(key, pyaes.MODE_CBC, IV=iv)
        print 'user agent trying'
        ua= decryptor.decrypt(jsondata["msg"]["54b23f9b3596397b2acf70a81b2da31d"].decode("hex")).split('\0')[0]
        print ua
        return ua
    except: 
        print 'err in user agent'
        traceback.print_exc(file=sys.stdout)
        return 'USER-AGENT-UKTVNOW-APP-V2'
#    print jsondata

def local_time(zone='Asia/Karachi'):
    from datetime import datetime
    from pytz import timezone
    other_zone = timezone(zone)
    other_zone_time = datetime.now(other_zone)
    return other_zone_time.strftime('%B-%d-%Y')

def getUKTVPlayUrl(channelID ):

    url=base64.b64decode("aHR0cDovL3VrdHZub3cubmV0L2FwcDMvdjMvZ2V0X3ZhbGlkX2xpbms=")
    username="-1"
    usernameC=username+channelID
    s = base64.b64decode("dWt0dm5vdy10b2tlbi0tX3xfLSVzLXVrdHZub3dfdG9rZW5fZ2VuZXJhdGlvbi0lcy1ffF8tMTIzNDU2X3VrdHZub3dfNjU0MzIxLV98Xy11a3R2bm93X2xpbmtfdG9rZW4=")%(url,username)
    import hashlib
    token= hashlib.md5(s).hexdigest()
    
    post = {'username':username,'channel_id':channelID,'useragent':getUKTVUserAgent(),'version':'5.7'}
    post = urllib.urlencode(post)
  
    headers=[('User-Agent','USER-AGENT-UKTVNOW-APP-V2'),('app-token',token)]
    jsondata=getUrl(url,post=post+'&',headers=headers)
    return json.loads(jsondata)
    
    
def getAPIToken( url,  username):
    #print url,username
    #from pytz import timezone
    #dt=local_time()
    s = base64.b64decode("dWt0dm5vdy10b2tlbi0tX3xfLSVzLXVrdHZub3dfdG9rZW5fZ2VuZXJhdGlvbi0lcy1ffF8tMTIzNDU2X3VrdHZub3dfNjU0MzIx")%(url,  username)
    import hashlib
    return hashlib.md5(s).hexdigest()
#aHR0cHM6Ly93d3cuZmFjZWJvb2suY29tL1pvbmEuTGl2ZS5UVi8=
def getMonaKey():
    s=getUrl(base64.b64decode("aHR0cDovL3pvbmEtbGl2ZS10di5jb20vem8yMzIvYXBpLnBocD9hcGlfa2V5"),headers=[('User-Agent','Dalvik/1.6.0 (Linux; U; Android 4.4.2; SM-G900F Build/KOT49H)')])
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
        url=base64.b64decode('aHR0cDovL3pvbmEtbGl2ZS10di5jb20vem8yMzIvYXBpLnBocD9rZXk9JXMmYWRtb2JfaWQ9Y2EtYXBwLXB1Yi0xNjI0MjgwNzMxMjE3NzE0LzYyNjMwNTUxODU=')%(getMonaKey())
    else:
        url=base64.b64decode('aHR0cDovL3pvbmEtbGl2ZS10di5jb20vem8yMzIvYXBpLnBocD9jYXRfaWQ9JXMma2V5PSVzJmFkbW9iX2lkPWNhLWFwcC1wdWItMTYyNDI4MDczMTIxNzcxNC82MjYzMDU1MTg1')%(cat,getMonaKey())
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
    username = "-1"#random.choice(usernames)
    post = {'username':username}
    post = urllib.urlencode(post)
  
    #headers=eval(base64.b64decode("WygnVXNlci1BZ2VudCcsJ1VTRVItQUdFTlQtVUtUVk5PVy1BUFAtVjEnKSwoJ2FwcC10b2tlbicsJ2FmZjE2MTRiNTJhNTM3YmQ3YmEyZDMyODE0ODU1NmFmJyld"))
    headers=[('User-Agent','USER-AGENT-UKTVNOW-APP-V2'),('app-token',getAPIToken(base64.b64decode("aHR0cHM6Ly9hcHAudWt0dm5vdy5uZXQvdjMvZ2V0X2FsbF9jaGFubmVscw=="),username))]
    jsondata=getUrl(base64.b64decode("aHR0cDovL3VrdHZub3cubmV0L2FwcDMvdjMvZ2V0X2FsbF9jaGFubmVscw=="),post=post,headers=headers)
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
            curl='direct3:'+curl
            #print curl
            if 'wiseplay' in cname.lower():
                ua='Lavf/57.25.100'
            if  curl.startswith("direct3:http"):
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
                    cimage=channel["img"].replace(' ','%20')
                    print cimage
                    if not cimage.startswith("http"):
                        cimage='https://app.uktvnow.net/'+cimage
                    print cimage
                    if cname==None: cname=curl
                    if len([i for i, x in enumerate(ret) if x[2] ==curl  ])==0:                    
                        ret.append((cname ,'manual', curl ,cimage))  
        if len(ret)>0:
            ret=sorted(ret,key=lambda s: s[0].lower() )                        
    except:
        traceback.print_exc(file=sys.stdout)
    return ret

def getptcchannels(categories, forSports=False,desi=True):
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
                    #cimage=ss["imgurl"]
                    cimage='http://shani.offshorepastebin.com/ZemLogos/%s.png'%cname.lower().replace(' ','')
                    
                    if len([i for i, x in enumerate(ret) if x[2] ==curl and x[0].lower()==cname.lower() +(' v6' if desi else '')  ])==0:                    
                        ret.append((cname +(' v6' if desi else '') ,'manual', curl ,cimage))  
        if len(ret)>0:
            ret=sorted(ret,key=lambda s: s[0].lower() )                        
    except:
        traceback.print_exc(file=sys.stdout)

    return ret

    
def getiptvchannels(gen, desi=True):
    
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
                ret.append((cname +(' v5' if desi else '') ,'manual3', curl ,cimage))        
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
    isIpBoxff="true"#turn off
    isYPgenOff= selfAddon.getSetting( "isYPOff" )
    isYPgenOff="true"
    isUKTVOff=selfAddon.getSetting( "isUKTVOff" )
    
    isZengaOff=selfAddon.getSetting( "isZengaOff" )
    
    isFastOff=selfAddon.getSetting( "isFastOff" )
    isNetworkTVOff=selfAddon.getSetting( "isNetworkTVOff" )
    isSlowTVOff=selfAddon.getSetting( "isSlowTVOff" )
    
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
            match.append(('Ary News (website)','manual',base64.b64decode('aHR0cDovL2xpdmUuYXJ5bmV3cy50di8='),'http://arynews.tv/en/wp-content/uploads/2016/10/arynewsfb-1.jpg'))
            match.append(('Ary Music (website)','manual',base64.b64decode('aHR0cDovL2xpdmUuYXJ5bXVzaWsudHYv'),base64.b64decode('aHR0cDovL2FyeW11c2lrLnR2L3dwLWNvbnRlbnQvdXBsb2Fkcy8yMDE0LzA4L2FyeW11c2lrLWxvZ28xLnBuZw==')))
            match.append(('Ary Digital (website)','manual',base64.b64decode('aHR0cDovL2xpdmUuYXJ5ZGlnaXRhbC50di8='),base64.b64decode('aHR0cDovL3d3dy5hcnlkaWdpdGFsLnR2L3dwLWNvbnRlbnQvdXBsb2Fkcy8yMDE0LzEyL2RpZ2l0YWwtbG9nby5naWY=')))
            match.append(('QTV (website)','manual',base64.b64decode('aHR0cDovL2xpdmUuYXJ5cXR2LnR2Lw=='),base64.b64decode('aHR0cDovL2FyeXF0di50di93cC1jb250ZW50L3VwbG9hZHMvMjAxNC8xMi9hcnktcXR2LTEtY29weS5qcGc=')))
            
            match.append((base64.b64decode('RHVueWEgKHdlYnNpdGUp'),'manual',base64.b64decode('aHR0cDovL2ltb2IuZHVueWFuZXdzLnR2OjE5MzUvbGl2ZS9zbWlsOnN0cmVhbS5zbWlsL3BsYXlsaXN0Lm0zdTg='),'http://shani.offshorepastebin.com/ZemLogos/dunyanews.png'))
            match.append((base64.b64decode('TmV3cyBvbmUgKHdlYnNpdGUp'),'manual','direct:'+base64.b64decode('aHR0cDovL2Nkbi5lYm91bmQudHYvdHYvbmV3c29uZS9wbGF5bGlzdC5tM3U4'),'http://shani.offshorepastebin.com/ZemLogos/newsone.png'))

            match.append((base64.b64decode('V2FzZWViICh3ZWJzaXRlKQ=='),'manual','direct:'+base64.b64decode('aHR0cDovL2Nkbi5lYm91bmQudHYvdHYvd2FzZWIvcGxheWxpc3QubTN1OA=='),'http://shani.offshorepastebin.com/ZemLogos/waseb.png'))

           
            
            
            match.append((base64.b64decode('Q2FwaXRhbCAod2Vic2l0ZSk='),'manual',base64.b64decode('ZWJvdW5kOmNhcGl0YWx0dg=='),'http://shani.offshorepastebin.com/ZemLogos/capitalnews.png'))
            match.append((base64.b64decode('RGF3biBuZXdzICh3ZWJzaXRlKQ=='),'manual',base64.b64decode('ZWJvdW5kOmRhd24='),'http://shani.offshorepastebin.com/ZemLogos/dunyanews.png'))
            match.append((base64.b64decode('Qm9sIHYy'),'manual',base64.b64decode('cHYyOkJvbCBOZXdz'),'http://shani.offshorepastebin.com/ZemLogos/bol.png'))
            match.append((base64.b64decode('R2VvIE5ld3MgdjI='),'manual',base64.b64decode('cHYyOkdlbyBOZXdz'),'http://shani.offshorepastebin.com/ZemLogos/geonews.png'))
            match.append((base64.b64decode('R2VvIEVudGVydGFpbm1lbnQgdjI='),'manual',base64.b64decode('cHYyOkdlbyBFbnRlcnRhaW5tZW50'),'http://shani.offshorepastebin.com/ZemLogos/geoentertainment.png'))
                        
            match.append((base64.b64decode('R2VvIEthaGFuaSB2Mg=='),'manual',base64.b64decode('cHYyOkdlbyBrYWhhbmk='),'http://shani.offshorepastebin.com/ZemLogos/geokahani.png'))
            match.append((base64.b64decode('R2VvIFRleiB2Mg=='),'manual',base64.b64decode('cHYyOkdlbyB0ZXp6'),'http://shani.offshorepastebin.com/ZemLogos/geotez.png'))
            match.append((base64.b64decode('S1ROIHYy'),'manual',base64.b64decode('cHYyOktUTg=='),'http://shani.offshorepastebin.com/ZemLogos/ktn.png'))
            match.append((base64.b64decode('S1ROIE5FV1MgdjI='),'manual',base64.b64decode('cHYyOktUTiBORVdT'),'http://shani.offshorepastebin.com/ZemLogos/ktnnews.png'))
            
            match.append((base64.b64decode('S1ROIEVudC4gKHdlYnNpdGUp'),'manual','direct:'+"rtmp://103.24.96.74/ktn/ playpath=ktn swfUrl=http://ktntv.tv/wp-content/player/jwplayer.flash.swf pageUrl=http://www.ktntv.tv/ live=1",'http://shani.offshorepastebin.com/ZemLogos/ktn.png'))
            match.append((base64.b64decode('S1ROIE5FV1MgKHdlYnNpdGUp'),'manual','direct:'+"rtmp://103.24.96.74/ktn/ playpath=ktnnews swfUrl=http://ktntv.tv/wp-content/player/jwplayer.flash.swf pageUrl=http://www.ktnnews.tv/ live=1",'http://shani.offshorepastebin.com/ZemLogos/ktnnews.png'))
            match.append(('Makkah (youtube)','manual','direct:plugin://plugin.video.youtube/?action=play_video&videoid=%s' %'0b1IMR2H_7s','makkah.png'))
            match.append(('Makkah (youtube)','manual','direct:plugin://plugin.video.youtube/?action=play_video&videoid=%s' %'wfQcy7vp55Q','makkah.png'))
            match.append(('Makkah (youtube)','manual','direct:plugin://plugin.video.youtube/?action=play_video&videoid=%s' %'Nxzeb_5LjtU','makkah.png'))
            match.append(('Madina (youtube)','manual','direct:plugin://plugin.video.youtube/?action=play_video&videoid=%s' %'-WYI832cx5Q','madina.png'))
  


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
    tvplayerChannels=None
    Zengagen=None
    fastgen=None
    nettvgen=None
    slowtvgen=None
    if cctype==1:
        pg='pakistan'
        iptvgen="pakistani"
        ptcgen=['News','Entertainment','Islamic','Cooking']
        paktvgen=['News','Islamic','Cooking']
        unitvgen=['News','Religious','Cooking','PAK&IND']
        wtvgen=['News','Religious','Cooking','Asian News','Entertainment','Pak&ind']
        CFgen="32"
        YPgen=base64.b64decode("aHR0cDovL3d3dy55dXBwdHYuY29tL3VyZHUtdHYuaHRtbA==")
        UKTVGenCat,UKTVGenCH=['religious','news','food'], ['masala tv', 'ary digital', 'ary zindagi','hum tv','drama','express ent.']
        fastgen=['PAKISTANI TV','ISLAMIC TV']
        nettvgen=["Pakistani"]
        slowtvgen=["Pakistani"]
        slowtvprefix="PK:"
    elif cctype==2:
        pg='indian'
        iptvgen="indian"
        ptcgen=['Indian']
        dittogen="ind"
        CFgen="33"
        ipBoxGen=1
        YPgen=base64.b64decode("aHR0cDovL3d3dy55dXBwdHYuY29tL2hpbmRpLXR2Lmh0bWw=")
        UKTVGenCat,UKTVGenCH=['movies'],['zee tv','colors','sony tv hd', 'star plus hd', 'zee tv']
        tvplayerChannels=['sony sab','zing']
        Zengagen='ch'
        fastgen=['INDIAN TV','SOUTH INDIAN']
        nettvgen=["Indian"]
        slowtvgen=["Hindi"]
        slowtvprefix="IN:"
    else:
        pg='punjabi'
        CFgen="1314"
        fastgen=['PUNJABI']
        YPgen=base64.b64decode("aHR0cDovL3d3dy55dXBwdHYuY29tL3B1bmphYmktdHYuaHRtbA==")
        slowtvgen=["Punjabi Live"]
        slowtvprefix="PB:"
    
    if isv3Off=='true': pg=None
    if isv5Off=='true': iptvgen=None
    if isv6Off=='true': ptcgen=None
    if isv7Off=='true': paktvgen=None
    if isv8Off=='true': unitvgen=None
    if isv9Off=='true': wtvgen=None
    if isFastOff=='true': fastgen=None
    if isNetworkTVOff=='true': nettvgen=None
    if isSlowTVOff=='true': slowtvgen=None
    
    
    
    if isdittoOff=='true': dittogen=None
    if isCFOff=='true': CFgen=None    
    if isIpBoxff=='true': ipBoxGen=None
    if isYPgenOff=='true': YPgen=None
    if isUKTVOff=='true': 
        UKTVGenCat=[]
        UKTVGenCH=[]
    if isZengaOff=='true': 
        Zengagen=None

        
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
                    
                    if cname.lower().startswith('high alert'): continue
                    #cid=source.findtext('programURL')# change from programURL
                    cid=source.findtext('programID')
                    cimage=source.findtext('programImage')+'|User-Agent=Pak%20TV/1.4 CFNetwork/808.2.16 Darwin/16.3.0'
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
    
    if Zengagen:
        try:
            
            progress.update( 90, "", "Loading Zenga Channels", "" )
            
            rematch=getZengaChannels(base64.b64decode('aHR0cDovL3plbmdhdHZnZXRhcGktZW52LmVsYXN0aWNiZWFuc3RhbGsuY29tL2dldHRyZW5kc2J5Y29udGVudHR5cGU/Y29udGVudHR5cGU9NmZmNDM3OGEtMDdkZC0xMWUyLTg1NWItNzA3MWJjY2M4NWFjJmNvdW50cnljb2RlPUlOJmZyb209MCZpczE4cGx1cz0wJnBsYXRmb3JtPWJmYzY4NWYxLTNkMzQtNDNmOS1hODliLTkzMDUxYzI4OGJjZSZzaXplPTIwMCZzdGF0ZT0yYmViMzJmZS0zM2RiLTQ3YWItYjJlNy1kMmRlOTVmZWM4NTI='),progress)
            progress.update( 92, "", "Loading Zenga Channels loaded", "" )
            if len(rematch)>0:
                match+=rematch
        except:
            traceback.print_exc(file=sys.stdout)    
            
            
    if ipBoxGen:
        try:
            
            progress.update( 90, "", "Loading IpBox Channels", "" )
            for nm,url in getIpBoxSources(True):
                rematch=getIpBoxChannels([url])
                if len(rematch)>0:
                    match+=rematch
        except:
            traceback.print_exc(file=sys.stdout)
            
    if fastgen:
        try:
            
            progress.update( 80, "", "Loading Fast Channels", "" )
            for cat in fastgen:
                rematch=getFastTVChannels(cat='',catname=cat)
                if len(rematch)>0:
                    match+=rematch
        except:
            traceback.print_exc(file=sys.stdout)  
            
    if nettvgen:
        try:
            progress.update( 83, "", "Loading Network TV Channels", "" )
            rematch=getNetworkTVChannels(cat=None,sports=False,country=nettvgen)
            if len(rematch)>0:
                match+=rematch
        except:
            traceback.print_exc(file=sys.stdout)   
    print 'ssssssssssssssssssssssslow',slowtvgen        
    if slowtvgen:
        try:
            progress.update( 87, "", "Loading SlowTV Channels", "" )
            print 'ssssssssssssssssssssssslossssssssssssssw',slowtvgen
            rematch=getNetworkTVChannels2(cat=[NetworkTVCatIDByName2(slowtvgen[0], findin=True)],sports=False,removeprefix=slowtvprefix)
            print 'rematch',rematch
           
            if len(rematch)>0:
                match+=rematch
        except:
            traceback.print_exc(file=sys.stdout)    
                        



    if tvplayerChannels:
        try:
            
            progress.update( 95, "", "Loading TVPlayer Channels", "" )

            for ch in getTVPlayerChannels(tvplayerChannels):
                match.append((ch[0] +' UK Only' ,'manual', base64.b64decode(ch[1])  ,ch[3]))
        except:
            traceback.print_exc(file=sys.stdout)
            

#    match=sorted(match,key=itemgetter(0)   )
    if len(eboundMatches)>0:
        match+=eboundMatches
    try:
        match=sorted(match,key=lambda s: s[0].lower()   )
    except: traceback.print_exc(file=sys.stdout)
    for cname,ctype,curl,imgurl in match:
        try:#ctype=='liveWMV' or ctype=='manual':
#            print curl
            #if ctype<>'': cname+= '[' + ctype+']'
            if isv3Off and curl.startswith('pv2:'):
                continue
            cname=cname.encode('ascii', 'ignore').decode('ascii')
            if ctype.startswith('ebmode:'):
                ctype=ctype.split(':')[1]
                addDir(ColoredOpt(cname.capitalize(),'EB') ,curl ,ctype,imgurl, False, True,isItFolder=False)
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
                    cc='fffc00cc'
                elif cname.lower().endswith(' cf'):
                    cc='blue'                
                elif cname.lower().endswith(' yp'):
                    cc='ffdc00cc'                
                elif cname.lower().endswith(' uktv'):
                    cc='ffdc1111'
                elif cname.lower().endswith(' zenga'):
                    cc='ffcc1111'
                elif cname.lower().endswith(' fast'):
                    cc='ffbb1111'
                elif cname.lower().endswith(' nettv'):
                    cc='ff991111'
                addDir(ColoredOpt(cname.capitalize(),cc) ,base64.b64encode(curl) ,mm ,imgurl, False, True,isItFolder=False)		#name,url,mode,icon
        except: traceback.print_exc(file=sys.stdout)
    return    
    
def addiptvSports(url):

    match=getiptvchannels('sports', desi=False)
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
    req = urllib2.Request( base64.b64decode("aHR0cHM6Ly9pb3MudmlzaW9zb2Z0bHRkLmNvbS9pYXBwL29hdXRoLnBocA=="))
    req.add_header('Authorization', "Basic %s"%base64.b64decode('WVhWMGFIVnpaWEk2ZW1OVFpUSjNaWEk9')) 
    req.add_header(base64.b64decode("VXNlci1BZ2VudA=="),base64.b64decode("UGFrJTIwVFYlMjBDb25uZWN0aWZ5LzQuNCBDRk5ldHdvcmsvODA4LjIuMTYgRGFyd2luLzE2LjMuMA==")) 
    response = urllib2.urlopen(req,data="")
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

    req = urllib2.Request( base64.b64decode('aHR0cDovL2NsdW9kYmFja2VuZGFwaS5hcHBzcG90LmNvbS9pb3MvcGFrdHYvcGFrdHY0LjQuanNvbg==') )      
    req.add_header(base64.b64decode("VXNlci1BZ2VudA=="),base64.b64decode("UGFrJTIwVFYlMjBDb25uZWN0aWZ5LzQuNCBDRk5ldHdvcmsvODA4LjIuMTYgRGFyd2luLzE2LjMuMA==")) 
    response = urllib2.urlopen(req)
    link=response.read()
    maindata=json.loads(link)
    #print maindata
    decodeddata=maindata["Secret"]
    #decodeddata='JCQkJIklu'.join(decodeddata.split('JCQkJIklu')[:-1])+'JCQkJIklu'
    #print decodeddata
    #data=base64.b64decode(decodeddata)
    #decodeddata=decodeddata.replace('nbUioPLk6nbviOP0kjgfreWEur','')
    #print len(decodeddata)
    if (len(decodeddata) % 4)>0:
        #decodeddata+=('='*(4-(len(decodeddata) % 4)))
        decodeddata=decodeddata[:-int(len(decodeddata) % 4)]
    #print len(decodeddata)
    #print decodeddata
    data=base64.b64decode(decodeddata)
    #print data
    #data=''
    try:
        #data=base64.b64decode(decodeddata)
        jsondata= json.loads(data)
    except:
        #print 'in except'   ,data
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
    
    #print jsondata
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
    
    fname='footballdata.json'
    fname=os.path.join(profile_path, fname)
    files+=[fname] 
    
    
    fname='zenga.json'
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
    
    fname='mytvpage.json'
    fname=os.path.join(profile_path, fname)
    files+=[fname]  
    
    
    fname='wtvpage.json'
    fname=os.path.join(profile_path, fname)
    files+=[fname]       
    fname='dreampage.json'
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
    
    fname='povee.json'
    fname=os.path.join(profile_path, fname)
    files+=[fname]     
    
    fname='network_page.json'
    fname=os.path.join(profile_path, fname)
    files+=[fname]     

    fname='network_page21.json'
    fname=os.path.join(profile_path, fname)
    files+=[fname]     

    fname='network_page22.json'
    fname=os.path.join(profile_path, fname)
    files+=[fname]     

    
    fname='Networkdata.json'
    fname=os.path.join(profile_path, fname)
    files+=[fname]

    fname='Networkdata21.json'
    fname=os.path.join(profile_path, fname)
    files+=[fname]
    fname='Networkdata22.json'
    fname=os.path.join(profile_path, fname)
    files+=[fname]    

 
    fname='pitvpage.json'
    fname=os.path.join(profile_path, fname)
    files+=[fname]  
    for p in ['u','p','h']:
        fname='yptvpage_%s.json'%p
        fname=os.path.join(profile_path, fname)
        files+=[fname]  

    
        
    try:
        for p in getFastCats()["LIVETV"]:
            fname='fast_%s_page.json'%p["cid"]
            fname=os.path.join(profile_path, fname)
            files+=[fname] 
    except: pass
        
    fname='Fastdata.json'
    fname=os.path.join(profile_path, fname)
    files+=[fname]     
    fname='FastCats.json'
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
        html= getUrl(base64.b64decode('aHR0cDovL29yaWdpbi5kaXR0b3R2LmNvbS9saXZldHYvYWxsLzA='))
        r=re.findall('<div class="subpattern.*?\s*<a href="(.*?)" title="(.*?)".*?\s*<img src="(.*?)"',html)
        #r+=eval(links)
        
    except:
        pass
    #r+=eval(base64.b64decode('W3sibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDE5MiIsIm5hbWUiOidaZWUgVFYgSEQnLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDE5Mi5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDE4OSIsIm5hbWUiOicmVFYgSEQnLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDE4OS5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDE5MSIsIm5hbWUiOidaZWUgQ2luZW1hIEhEJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAxOTEuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAxOTAiLCJuYW1lIjonJlBpY3R1cmVzIEhEJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAxOTAuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAwMDMiLCJuYW1lIjonWmVlIENsYXNzaWMnLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDAwMy5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDAxMyIsIm5hbWUiOidMaXZpbmcgRm9vZHonLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDAxMy5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDE4NyIsIm5hbWUiOidabGl2aW5nJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAxODcuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAwMDUiLCJuYW1lIjonWmVlIEJ1c2luZXNzJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAwMDUuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAwMTAiLCJuYW1lIjonWmVlIE1hcmF0aGknLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDAxMC5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDE2NiIsIm5hbWUiOidaZWUgVGVsdWd1JywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAxNjYuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAxODUiLCJuYW1lIjonTWFzdGlpJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAxODUuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAxNTIiLCJuYW1lIjonRVRDJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAxNTIuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAwMDciLCJuYW1lIjonUmFqIFRWJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAwMDcuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAxNTciLCJuYW1lIjonUmFqIERpZ2l0YWwgUGx1cycsInBvc3RlciI6Imh0dHA6XC9cLzg5LjM1LjE1OC4zNFwvaW1hZ2VzX2RpdHRvXC9uZXdfaW1hZ2VzXC9saXZldHZcLzEwMTU3LmpwZyJ9LAogICAgeyJtYW51YWwiOiJtYW51YWwiLCJpZCI6IjEwMTk5IiwibmFtZSI6J0FsIEphemVlcmEnLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDE5OS5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDE5MyIsIm5hbWUiOidNYWtrYWwgVFYnLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDE5My5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDAxNCIsIm5hbWUiOidaZWUgQmFuZ2xhJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAwMTQuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAyMDMiLCJuYW1lIjonWmluZycsInBvc3RlciI6Imh0dHA6XC9cLzg5LjM1LjE1OC4zNFwvaW1hZ2VzX2RpdHRvXC9uZXdfaW1hZ2VzXC9saXZldHZcLzEwMjAzLmpwZyJ9XQ=='))
    #r+=eval(base64.b64decode('W3sibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDE4MyIsIm5hbWUiOicmIFBpY3R1cmVzJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAxODMuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAxOTAiLCJuYW1lIjonJlBpY3R1cmVzIEhEJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAxOTAuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAwMDQiLCJuYW1lIjonJlRWJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAwMDQuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAxODkiLCJuYW1lIjonJlRWIEhEJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAxODkuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAwMTkiLCJuYW1lIjonMjQgR2hhbnRhJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAwMTkuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAxNTkiLCJuYW1lIjonQ1RWTiBBS0QgUGx1cycsInBvc3RlciI6Imh0dHA6XC9cLzg5LjM1LjE1OC4zNFwvaW1hZ2VzX2RpdHRvXC9uZXdfaW1hZ2VzXC9saXZldHZcLzEwMTU5LmpwZyJ9LAogICAgeyJtYW51YWwiOiJtYW51YWwiLCJpZCI6IjEwMTcxIiwibmFtZSI6J0RpdnlhIFRWJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAxNzEuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAxNTIiLCJuYW1lIjonRVRDJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAxNTIuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAwMjIiLCJuYW1lIjonSW5kaWEgMjR4NycsInBvc3RlciI6Imh0dHA6XC9cLzg5LjM1LjE1OC4zNFwvaW1hZ2VzX2RpdHRvXC9uZXdfaW1hZ2VzXC9saXZldHZcLzEwMDIyLmpwZyJ9LAogICAgeyJtYW51YWwiOiJtYW51YWwiLCJpZCI6IjEwMTYwIiwibmFtZSI6J0tvbGthdGEgVFYnLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDE2MC5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDAxMyIsIm5hbWUiOidMaXZpbmcgRm9vZHonLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDAxMy5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDE5MyIsIm5hbWUiOidNYWtrYWwgVFYnLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDE5My5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDE4NSIsIm5hbWUiOidNYXN0aWknLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDE4NS5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDE2MSIsIm5hbWUiOidSIFBsdXMnLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDE2MS5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDE1NyIsIm5hbWUiOidSYWogRGlnaXRhbCBQbHVzJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAxNTcuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAwMjUiLCJuYW1lIjonUmFqIE11c2ljJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAwMjUuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAwMTciLCJuYW1lIjonUmFqIE11c2l4JywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAwMTcuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAwMDkiLCJuYW1lIjonUmFqIE11c2l4IFRlbHVndScsInBvc3RlciI6Imh0dHA6XC9cLzg5LjM1LjE1OC4zNFwvaW1hZ2VzX2RpdHRvXC9uZXdfaW1hZ2VzXC9saXZldHZcLzEwMDA5LmpwZyJ9LAogICAgeyJtYW51YWwiOiJtYW51YWwiLCJpZCI6IjEwMDE2IiwibmFtZSI6J2FqIE5ld3MgMjR4NycsInBvc3RlciI6Imh0dHA6XC9cLzg5LjM1LjE1OC4zNFwvaW1hZ2VzX2RpdHRvXC9uZXdfaW1hZ2VzXC9saXZldHZcLzEwMDE2LmpwZyJ9LAogICAgeyJtYW51YWwiOiJtYW51YWwiLCJpZCI6IjEwMDI2IiwibmFtZSI6J1JhaiBOZXdzIEthbm5hZGEnLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDAyNi5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDAxOCIsIm5hbWUiOidSYWogTmV3cyBNYWxheWFsYW0nLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDAxOC5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDAwOCIsIm5hbWUiOidSYWogTmV3cyBUZWx1Z3UnLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDAwOC5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDAwNyIsIm5hbWUiOidSYWogVFYnLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDAwNy5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDE2MiIsIm5hbWUiOidUYWF6YSBUViAnLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDE2Mi5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDE2MyIsIm5hbWUiOidVdHRhciBCYW5nbGEgQUtEJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAxNjMuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAxNjciLCJuYW1lIjonVmlzc2EgVFYnLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDE2Ny5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDE1NCIsIm5hbWUiOidaRUUgMjQgVGFhcycsInBvc3RlciI6Imh0dHA6XC9cLzg5LjM1LjE1OC4zNFwvaW1hZ2VzX2RpdHRvXC9uZXdfaW1hZ2VzXC9saXZldHZcLzEwMTU0LmpwZyJ9LAogICAgeyJtYW51YWwiOiJtYW51YWwiLCJpZCI6IjEwMTY5IiwibmFtZSI6J1plZSBBZmxhbScsInBvc3RlciI6Imh0dHA6XC9cLzg5LjM1LjE1OC4zNFwvaW1hZ2VzX2RpdHRvXC9uZXdfaW1hZ2VzXC9saXZldHZcLzEwMTY5LmpwZyJ9LAogICAgeyJtYW51YWwiOiJtYW51YWwiLCJpZCI6IjEwMTcwIiwibmFtZSI6J1plZSBBbHdhbicsInBvc3RlciI6Imh0dHA6XC9cLzg5LjM1LjE1OC4zNFwvaW1hZ2VzX2RpdHRvXC9uZXdfaW1hZ2VzXC9saXZldHZcLzEwMTcwLmpwZyJ9LAogICAgeyJtYW51YWwiOiJtYW51YWwiLCJpZCI6IjEwMDE0IiwibmFtZSI6J1plZSBCYW5nbGEnLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDAxNC5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDE4OCIsIm5hbWUiOidaZWUgQmFuZ2xhIENpbmVtYScsInBvc3RlciI6Imh0dHA6XC9cLzg5LjM1LjE1OC4zNFwvaW1hZ2VzX2RpdHRvXC9uZXdfaW1hZ2VzXC9saXZldHZcLzEwMTg4LmpwZyJ9LAogICAgeyJtYW51YWwiOiJtYW51YWwiLCJpZCI6IjEwMDA1IiwibmFtZSI6J1plZSBCdXNpbmVzcycsInBvc3RlciI6Imh0dHA6XC9cLzg5LjM1LjE1OC4zNFwvaW1hZ2VzX2RpdHRvXC9uZXdfaW1hZ2VzXC9saXZldHZcLzEwMDA1LmpwZyJ9LAogICAgeyJtYW51YWwiOiJtYW51YWwiLCJpZCI6IjEwMTkxIiwibmFtZSI6J1plZSBDaW5lbWEgSEQnLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDE5MS5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDAwMyIsIm5hbWUiOidaZWUgQ2xhc3NpYycsInBvc3RlciI6Imh0dHA6XC9cLzg5LjM1LjE1OC4zNFwvaW1hZ2VzX2RpdHRvXC9uZXdfaW1hZ2VzXC9saXZldHZcLzEwMDAzLmpwZyJ9LAogICAgeyJtYW51YWwiOiJtYW51YWwiLCJpZCI6IjEwMTU1IiwibmFtZSI6J1plZSBLYWxpbmdhIE5ld3MnLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDE1NS5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDAzMSIsIm5hbWUiOidaZWUgS2FubmFkYScsInBvc3RlciI6Imh0dHA6XC9cLzg5LjM1LjE1OC4zNFwvaW1hZ2VzX2RpdHRvXC9uZXdfaW1hZ2VzXC9saXZldHZcLzEwMDMxLmpwZyJ9LAogICAgeyJtYW51YWwiOiJtYW51YWwiLCJpZCI6IjEwMDEwIiwibmFtZSI6J1plZSBNYXJhdGhpJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAwMTAuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAwMjAiLCJuYW1lIjonWmVlIE1QQ0cnLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDAyMC5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDAwNiIsIm5hbWUiOidaZWUgTmV3cycsInBvc3RlciI6Imh0dHA6XC9cLzg5LjM1LjE1OC4zNFwvaW1hZ2VzX2RpdHRvXC9uZXdfaW1hZ2VzXC9saXZldHZcLzEwMDA2LmpwZyJ9LAogICAgeyJtYW51YWwiOiJtYW51YWwiLCJpZCI6IjEwMTU2IiwibmFtZSI6J1plZSBQdW5qYWIgSGFyeWFuYSBIaW1hY2hhbCBQcmFkZXNoJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAxNTYuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAwMjMiLCJuYW1lIjonWmVlIFB1cnZhaXlhJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAwMjMuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAxOTQiLCJuYW1lIjonWmVlIFNhbGFhbScsInBvc3RlciI6Imh0dHA6XC9cLzg5LjM1LjE1OC4zNFwvaW1hZ2VzX2RpdHRvXC9uZXdfaW1hZ2VzXC9saXZldHZcLzEwMTk0LmpwZyJ9LAogICAgeyJtYW51YWwiOiJtYW51YWwiLCJpZCI6IjEwMDExIiwibmFtZSI6J1plZSBUYWxraWVzJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAwMTEuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAwMTUiLCJuYW1lIjonWmVlIFRhbWlsJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAwMTUuanBnIn0sCiAgICB7Im1hbnVhbCI6Im1hbnVhbCIsImlkIjoiMTAxNjYiLCJuYW1lIjonWmVlIFRlbHVndScsInBvc3RlciI6Imh0dHA6XC9cLzg5LjM1LjE1OC4zNFwvaW1hZ2VzX2RpdHRvXC9uZXdfaW1hZ2VzXC9saXZldHZcLzEwMTY2LmpwZyJ9LAogICAgeyJtYW51YWwiOiJtYW51YWwiLCJpZCI6IjEwMTkyIiwibmFtZSI6J1plZSBUViBIRCcsInBvc3RlciI6Imh0dHA6XC9cLzg5LjM1LjE1OC4zNFwvaW1hZ2VzX2RpdHRvXC9uZXdfaW1hZ2VzXC9saXZldHZcLzEwMTkyLmpwZyJ9LAogICAgeyJtYW51YWwiOiJtYW51YWwiLCJpZCI6IjEwMDEyIiwibmFtZSI6J1ppbmcgSW5kaWEnLCJwb3N0ZXIiOiJodHRwOlwvXC84OS4zNS4xNTguMzRcL2ltYWdlc19kaXR0b1wvbmV3X2ltYWdlc1wvbGl2ZXR2XC8xMDAxMi5qcGcifSwKICAgIHsibWFudWFsIjoibWFudWFsIiwiaWQiOiIxMDE4NyIsIm5hbWUiOidabGl2aW5nJywicG9zdGVyIjoiaHR0cDpcL1wvODkuMzUuMTU4LjM0XC9pbWFnZXNfZGl0dG9cL25ld19pbWFnZXNcL2xpdmV0dlwvMTAxODcuanBnIn1d'))

    return r
    
def getZengaPage(url,progress):
 
    print 'url',url
    fname='zenga.json'
    fname=os.path.join(profile_path, fname)
    jj=None
    try:
        jsondata=getCacheData(fname,60*60*2)
        if not jsondata==None:
            return json.loads(jsondata)
    except:
        print 'file getting error'
        traceback.print_exc(file=sys.stdout)
        
    headers=[('User-Agent','Mozilla/5.0 (iPhone; CPU iPhone OS 9_0_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13A452 (5215161440)'), ('Origin','file://')]

    try:
        print 'url',url
        jj= json.loads(getUrl(url,headers=headers,post=""))
        storeCacheData(json.dumps(jj),fname)
    except:
        print 'zenga file saving error'
        traceback.print_exc(file=sys.stdout)
    return jj
    
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
        if 1==1:# not getYPUrl(l[0])==None:
            ret+=[l]
    links=ret
    jj=json.dumps(links)
    try:
        storeCacheData(jj,fname)
    except:
        print 'yp file saving error'
        traceback.print_exc(file=sys.stdout)
    return links
    
def getYpCookieJar(updatedUName=False):
    cookieJar=None
    try:
        cookieJar = cookielib.LWPCookieJar()
        if not updatedUName:
            cookieJar.load(YPLoginFile,ignore_discard=True)
    except: 
        cookieJar=None

    if not cookieJar:
        cookieJar = cookielib.LWPCookieJar()
    return cookieJar 
    
#def getYPSession():
#    cookieJar=getYpCookieJar()
#    try:
#        headers=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')]
#        mainpage=getUrl('http://www.yupptv.com/Default.aspx',headers=headers,cookieJar=cookieJar )
#        if 'Login / Register' in mainpage:
#            headers=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'),
#            ('Origin','http://www.yupptv.com') ,
#              ('Referer','http://www.yupptv.com/Default.aspx') ,
#                ('X-Requested-With','XMLHttpRequest')             ]
#            
#            post="ctl00%24header1%24sm1=ctl00%24header1%24upLocation%7Cctl00%24header1%24btnSubmit&__LASTFOCUS=&__EVENTTARGET=&__EVENTARGUMENT=&ctl00%24header1%24txtSearch1280=&ctl00%24header1%24txtSearch1600=&ctl00%24header1%24txtLogin=cdn54447%40zasod.com&ctl00%24header1%24txtpassword=NOPWD&ctl00%24header1%24txtName=&ctl00%24header1%24txtEmail=&ctl00%24header1%24txtPwd=&ctl00%24header1%24txtretypwd=&ctl00%24header1%24ddlLangugae=0&ctl00%24header1%24TxtBoxCountry=0&ctl00%24header1%24txtCountryCode=&ctl00%24header1%24txtphoneno=&ctl00%24header1%24chkRterm=option3&ctl00%24header1%24txtFLogin=&ctl00%24header1%24lblCountryName=&ctl00%24header1%24lblCountryValue=&ctl00%24header1%24lblCountryNameindia=&ctl00%24header1%24lblCountryValueindia=&ctl00%24header1%24txtOtp=&ctl00%24header1%24dpdotplogin=0&ctl00%24header1%24txtlogincountrycode=&ctl00%24header1%24txtloginphone=&ctl00%24header1%24txtloginotp=&ctl00%24ContentPlaceHolder1%24header3%24txtActDiv=divHindi&__ASYNCPOST=true&ctl00%24header1%24btnSubmit=Login"
#            mainpage=getUrl('http://www.yupptv.com/Default.aspx',post=post,cookieJar=cookieJar,headers=headers)
#        cookieJar.save (YPLoginFile,ignore_discard=True)
#    except: pass
#    return cookieJar
def getYPSession():
    cookieJar=getYpCookieJar()
    try:
        import time
        headers=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')]
        mainpage=getUrl('http://shani.offshorepastebin.com/yppsession.php?i'+str(time.time()),headers=headers )
        sess=re.findall('ASP.NET_SessionId\s(.*)',mainpage)[0]
        return "ASP.NET_SessionId="+sess+";"
    except: pass
    return ""
    
def getCFPage(catId):
    headers=[('User-Agent',base64.b64decode('CFUNTV/3.1 CFNetwork/758.0.2 Darwin/15.0.0'))]
#    html= getUrl(base64.b64decode('aHR0cHM6Ly9jaW5lZnVudHYuY29tL3NtdGFsbmMvY29udGVudC5waHA/Y21kPWNvbnRlbnQmY2F0ZWdvcnlpZD0lcyZkZXZpY2U9aW9zJnZlcnNpb249MCZrZXk9Q1l4UElWRTlhZQ==')%catId,headers=headers)
    html= getUrl(base64.b64decode('aHR0cHM6Ly9jaW5lZnVudHYuY29tL3NtdGFsbmMvY29udGVudC5waHA/Y21kPWNvbnRlbnQmY2F0ZWdvcnlpZD0lcyZkZXZpY2U9aW9zJnZlcnNpb249MCZrZXk9Q1l4UElWRTlhZSZ1PWt3cDMwNjcwQHJjYXNkLmNvbSZhcHB0eXBlPWlvcw==')%catId,headers=headers)
    return json.loads(html)

def getMYTVPage():

    fname='mytvpage.json'
    fname=os.path.join(profile_path, fname)
    try:
        jsondata=getCacheData(fname,3*60*60)
        if not jsondata==None:
            return jsondata
    except:
        print 'file getting error'
        traceback.print_exc(file=sys.stdout)
    
    headers=[('User-Agent',base64.b64decode('c3BvcnQlMjBUViUyMExpdmUvMi43IENGTmV0d29yay83NTguMC4yIERhcndpbi8xNS4wLjA='))]
    jsondata=getUrl(base64.b64decode('aHR0cDovL21lZGlhb25zcG9ydC5kZS90di9zcG9ydGlvcy9hcGkucGhwP2xhdGVzdD0zNTA='), headers=headers)
    print 'decrypted paktvpage'
    #print decrypted_data
    jsondata=json.loads(jsondata)
    try:
        storeCacheData(jsondata,fname)
    except:
        print 'paktv file saving error'
        traceback.print_exc(file=sys.stdout)
    return jsondata

#aHR0cDovL3NvbGlkc3RyZWFtei5jb20vc29saWRzdHJlYW16MS4wLmFwaw==    
def getNetworkTVPage2(apptype):
    fname='network_page2%s.json'%str(apptype)
    fname=os.path.join(profile_path, fname)
    try:
        jsondata=getCacheData(fname,30*60)
        if not jsondata==None:
            return json.loads(jsondata)
    except:
        print 'file getting error'
        traceback.print_exc(file=sys.stdout)
    
    netData=getNetworkTVData2(apptype)["DATA"][0]
    
    url=netData["MainURL"]+ "/panel_api.php?mode=live&username=" + netData["Username"] + "&password=" + netData["Password"]
    ua=netData["UserAgent"]
    
    try:
        if apptype==1:
            headers=[('User-Agent',getFastUA()),('Authorization','Basic %s'%base64.b64decode("bWZwMjU1NzNAZHNpYXkuY29tX2dlbzE0OlN1cGVyMTIz"))]
        else:
            headers=[('User-Agent',getFastUA())]

        jsondata=json.loads(getUrl(url,headers=headers))
        storeCacheData(json.dumps(jsondata),fname)
    except:
        print 'getNetworkTVPage2 file saving error'
        traceback.print_exc(file=sys.stdout)
    return jsondata

    

#aHR0cDovL2xpdmVuZXR0di54eXov    
def getNetworkTVPage():
    fname='network_page.json'
    fname=os.path.join(profile_path, fname)
    try:
        jsondata=getCacheData(fname,2*60*60)
        if not jsondata==None:
            return json.loads(jsondata)
    except:
        print 'file getting error'
        traceback.print_exc(file=sys.stdout)
    
    ##netData=getNetworkTVData()["data"][0]
    #netData=getNetworkTVData()
    #print 'netData',netData
    #baseurl=netData["YmFzZXVybG5ld3gw"]
    #baseurl=baseurl[1:].decode("base64")+"bGl2ZTMubmV0dHYv".decode("base64")
    #import random,math
    #uid=int(math.floor(random.random()*50000) )
    #auth = netData["amFnX3Ryb3JfYXR0X2Vu"][1:].decode("base64") 
    #ref = netData["SXNpc2VrZWxvX3Nlc2lzdGltdV95ZXppbm9tYm9sbzAw"][1:].decode("base64")
                
    #headers=[('User-Agent',getFastUA(v2=True)),('Authorization',auth),('Referer',ref)]
    headers=[('User-Agent','zemtvaddons')]
    #post={'check':'1','user_id':str(uid),'version':'26'}
    #post = urllib.urlencode(post)
    #jsondata=getUrl(baseurl,post=post,headers=headers)
    import time
    jsondata=getUrl(base64.b64decode("aHR0cDovL3NoYW5pLm9mZnNob3JlcGFzdGViaW4uY29tL25ldC5qc29u")+"?dt="+str(int(time.time())),headers=headers)
    #print jsondata
    jsondata=json.loads(jsondata)

    chlist="eY2hhbm5lbHNfbGlzdA=="
    cid="rY19pZA=="
    cname="ZY19uYW1l"
    steamlist="Qc3RyZWFtX2xpc3Q="
    streamid="cc3RyZWFtX2lk"
    streamurl="Bc3RyZWFtX3VybA=="
    token= "AdG9rZW4="
    logo="abG9nb191cmw="
    channels={"channels":[],"cats":[]}
    tokentype={}
    channels["cats"]=jsondata["categories_list"]
    for chmain in jsondata[chlist]:
        v=0
        single=False
        #print chmain
        if len(chmain[steamlist])<=1:
            single=True
        for chlist in chmain[steamlist]:
            v+=1
            
            tt=chlist[token][:-1].decode("base64")
            #print chmain[cname ][:-1].decode("base64"),tt,chlist
            if tt in tokentype:
                tokentype[tt]+=1
            else:
                tokentype[tt]=1
            
            #["24","25","28","29","30","31","32"]==29
            #if tt not in ['5','33','18','0',"24","25","28","29","30","31","32","38","26"]: continue
            #if tt not in ["35","34"]: continue
            #if tt not in ["38"]: continue
            channels["channels"].append( {
            'cid': chmain[cid][:-1].decode("base64") ,
            'chname': chmain[cname ][:-1].decode("base64"), #+ ("" if single else " "+str(v)),
            'streamid': chlist[streamid ][:-1].decode("base64") ,
            'streamurl': chlist[streamurl ][1:].decode("base64") ,
            'token': chlist[token][:-1].decode("base64"),
            'logo': chmain[logo][1:].decode("base64"),
            'quality':chlist['quality'],
            'referer':chlist['referer'],
            'user_agent':chlist['user_agent'],
            'player_user_agent':chlist['player_user_agent'],
            'player_referer':chlist['player_referer']  ,  
            'cat_id':chmain['cat_id']  ,
            'country_id':chmain['country_id']  ,
            'status':chmain['status']  ,
            'cat_name':chmain['cat_name']  ,
            'country_name':chmain['country_name']  
            }   )
            
    print tokentype
    import operator
    print sorted(tokentype.items(), key=operator.itemgetter(1))
    #[('36', 2), ('11', 3), ('20', 3), ('14', 9), ('4', 19), ('6', 19), ('30', 24), ('9', 38), ('34', 42), ('19', 44), ('5', 58), ('29', 99), ('0', 108), ('18', 115), ('33', 390)]
    try:
        storeCacheData(json.dumps(channels),fname)
    except:
        print 'networktv file saving error'
        traceback.print_exc(file=sys.stdout)
    return channels
    
    
def getFastTVPage(cat):
    fname='fast_%s_page.json'%cat
    fname=os.path.join(profile_path, fname)
    try:
        jsondata=getCacheData(fname,3*60*60)
        if not jsondata==None:
            return json.loads(jsondata)
    except:
        print 'file getting error'
        traceback.print_exc(file=sys.stdout)
    
    fastData=getFastData()   
    headers=[('User-Agent',getFastUA()),('Authorization','Basic %s'%base64.b64encode(fastData["DATA"][0]["Password"]))]
    jsondata=getUrl(base64.b64decode('aHR0cDovL3N3aWZ0c3RyZWFtei5jb20vU3dpZnRTdHJlYW0vYXBpLnBocD9jYXRfaWQ9JXM=')%cat,headers=headers)
    try:
        jsondataobj=json.loads(jsondata)
    except: 
        jsondataobj=json.loads(jsondata.split(']}')[0]+']}')
    try:
        storeCacheData(jsondata,fname)
    except:
        print 'paktv file saving error'
        traceback.print_exc(file=sys.stdout)
    return jsondataobj
        
        
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



    try:
        req = urllib2.Request( base64.b64decode('aHR0cDovL25ld2NtczZocHBhay5keW5kbnMudHYvQ01TOC9jbXMvWFZlci9nZXRDb250dFYxLTAucGhw') )      
        req.add_header(base64.b64decode("VXNlci1BZ2VudA=="),base64.b64decode("VW5pdmVyc2FsJTIwU3BvcnRzJTIwSEQlMjBUVi8xLjEgQ0ZOZXR3b3JrLzc1OC4wLjIgRGFyd2luLzE1LjAuMA==")) 
        req.add_header(base64.b64decode("QXV0aG9yaXphdGlvbg=="),base64.b64decode("QmFzaWMgUTIxek9GVnpKSEk2UTIxek9GVnpKSEpBY0VGQVFIZHZja1E9")) 
        response = urllib2.urlopen(req)
        link=response.read()
        import rc
        cryptor=rc.RNCryptor()
        d=base64.b64decode(link)    
        decrypted_data = cryptor.decrypt(d, base64.b64decode("Q21TODhQQEBAc1N3MHJkNzg2"))
        decrypted_data=json.loads(decrypted_data)
        dataUrl=decrypted_data[0]["LiveLink"]

        req = urllib2.Request( dataUrl)      
        req.add_header(base64.b64decode("VXNlci1BZ2VudA=="),base64.b64decode("VW5pdmVyc2FsJTIwU3BvcnRzJTIwSEQlMjBUVi8xLjEgQ0ZOZXR3b3JrLzc1OC4wLjIgRGFyd2luLzE1LjAuMA==")) 
        req.add_header(base64.b64decode("QXV0aG9yaXphdGlvbg=="),base64.b64decode("QmFzaWMgUTIxek9GVnpKSEk2UTIxek9GVnpKSEpBY0VGQVFIZHZja1E9")) 
        response = urllib2.urlopen(req)
        link=response.read()

        d=base64.b64decode(link)    
        decrypted_data = cryptor.decrypt(d, base64.b64decode("Q21TODhQQEBAc1N3MHJkNzg2"))
        print decrypted_data
        jsondata=json.loads(decrypted_data)
    except:
        traceback.print_exc(file=sys.stdout)
        print 'trying different server'
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
        print decrypted_data
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
        
    req = urllib2.Request( base64.b64decode('aHR0cDovL2NtczEzLmlwdHZzYWxlLmNvbS9DTVMxMy9jbXMvQ3ZBWlpYL2dldENvbnR0VjEtMC5waHA=') )      
                                             
    req.add_header(base64.b64decode("VXNlci1BZ2VudA=="),base64.b64decode("V29ybGQlMjBUViUyMFBsdXMlMjBIRC8xLjEgQ0ZOZXR3b3JrLzc1OC4wLjIgRGFyd2luLzE1LjAuMA==")) 
    req.add_header(base64.b64decode("QXV0aG9yaXphdGlvbg=="),base64.b64decode("QmFzaWMgWkdsc1FHUnBiRHBoUVhOeVVDUXNaR1pUYlgwPQ==")) 
    response = urllib2.urlopen(req)
    link=response.read()
    import rc
    cryptor=rc.RNCryptor()
    d=base64.b64decode(link)    
    decrypted_data = cryptor.decrypt(d, base64.b64decode("VW1hcmJoYWlDTXNQMHMjcy53MHJk"))
    decrypted_data=json.loads(decrypted_data)
    dataUrl=decrypted_data[0]["LiveLink"]

    req = urllib2.Request( dataUrl)      
    req.add_header(base64.b64decode("VXNlci1BZ2VudA=="),base64.b64decode("V29ybGQlMjBUViUyMFBsdXMlMjBIRC8xLjEgQ0ZOZXR3b3JrLzc1OC4wLjIgRGFyd2luLzE1LjAuMA==")) 
    req.add_header(base64.b64decode("QXV0aG9yaXphdGlvbg=="),base64.b64decode("QmFzaWMgWkdsc1FHUnBiRHBoUVhOeVVDUXNaR1pUYlgwPQ==")) 
    response = urllib2.urlopen(req)
    link=response.read()

    d=base64.b64decode(link)    
    decrypted_data = cryptor.decrypt(d, base64.b64decode("VW1hcmJoYWlDTXNQMHMjcy53MHJk"))
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
        
    req = urllib2.Request( base64.b64decode('aHR0cDovL3d3dy5zb2Z0bWFnbmF0ZS5jb20vQ01TLVNlcnZlci1TcG9ydHMtVFYvWFZlci9QVFYtU3BvcnRzLVRWL2dldENvbnR0VjEtMC5waHA=') )      
    req.add_header(base64.b64decode("VXNlci1BZ2VudA=="),base64.b64decode("UFRWU3BvcnRzLzEuMCBDRk5ldHdvcmsvNzU4LjAuMiBEYXJ3aW4vMTUuMC4w")) 
    req.add_header(base64.b64decode("QXV0aG9yaXphdGlvbg=="),base64.b64decode("QmFzaWMgVFRCcU1FdEFhMEU2Y0VGd2NIVkFOamczUUVReFkzUXhiMjVCY25rPQ==")) 
    response = urllib2.urlopen(req)
    link=response.read()
    import rc
    cryptor=rc.RNCryptor()
    d=base64.b64decode(link)    
    decrypted_data = cryptor.decrypt(d, base64.b64decode("dFcxbjNsZUIzbnpANDc1QGQwMzM="))#first
    decrypted_data=json.loads(decrypted_data)
    dataUrl=decrypted_data[0]["LiveLink"]

    req = urllib2.Request( dataUrl)      
    req.add_header(base64.b64decode("VXNlci1BZ2VudA=="),base64.b64decode("UFRWU3BvcnRzLzEuMCBDRk5ldHdvcmsvNzU4LjAuMiBEYXJ3aW4vMTUuMC4w")) 
    req.add_header(base64.b64decode("QXV0aG9yaXphdGlvbg=="),base64.b64decode("QmFzaWMgVFRCcU1FdEFhMEU2Y0VGd2NIVkFOamczUUVReFkzUXhiMjVCY25rPQ==")) 
    response = urllib2.urlopen(req)
    link=response.read()

    d=base64.b64decode(link)    
    decrypted_data = cryptor.decrypt(d, base64.b64decode("dFcxbjNsZUIzbnpANDc1QGQwMzM="))#second
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

def getPv2Code(newcode=False):
    currentcode=selfAddon.getSetting( id="pv2DeviceID")
    if currentcode=="" or newcode:
        import os,binascii
        currentcode=binascii.b2a_hex(os.urandom(16)).upper()
        print 'code is ',currentcode
        selfAddon.setSetting( id="pv2DeviceID" ,value=currentcode)
    return currentcode
    
def getPV2UserAgent(option):
    if option==1:
        #headers=[('User-Agent',base64.b64decode('UGFrJTIwVFYvMS4wIENGTmV0d29yay83NTguMi44IERhcndpbi8xNS4wLjA=')),('Authorization',base64.b64decode('QmFzaWMgWVcxMU9rQmtia0J1T0RRNQ=='))]
        headers=[('User-Agent',getPv2Code()),('Authorization',base64.b64decode('QmFzaWMgWVcxMU9rQmtia0J1T0RRNQ=='))]
        return getUrl(base64.b64decode('aHR0cHM6Ly9hcHAuZHlubnMuY29tL2tleXMvcGFraW5kaWFoZHYyZmYucGhw'),headers=headers)
    else:
        return getPv2Code();

def getpv2stkey():
    headers=[('User-Agent',base64.b64decode('cDl4VE1nV2hFclpxZGlFWU1iV045bFVvd0xGMFdWM3I=')),('Authorization',base64.b64decode('QmFzaWMgWVcxMVpHbHNZbUZ5YW1GdWFUcHFZVzUxWjJWeWJXRnVhbUZ1YVE9PQ=='))]
    return getUrl(base64.b64decode('aHR0cHM6Ly93d3cuYm94dHZoZC5jb20vdG9wL3Bha2luZGlhdjIzcC5waHA='),headers=headers)
    
def getPV2Device(option):
    useragent=getpv2stkey()
    #if option==1 or 1==1:
    #    #headers=[('User-Agent',base64.b64decode('UGFrJTIwVFYvMS4wIENGTmV0d29yay83NTguMi44IERhcndpbi8xNS4wLjA=')),('Authorization',base64.b64decode('QmFzaWMgWVcxMU9rQmtia0J1T0RRNQ=='))]
    #    headers=[('User-Agent',base64.b64decode('UGFrJTIwVFYvMS4wIENGTmV0d29yay83NTguMi44IERhcndpbi8xNS4wLjA=')),('Authorization',base64.b64decode('QmFzaWMgWVcxMU9rQmtia0J1T0RRNQ=='))]
    #    useragent=getUrl(base64.b64decode('aHR0cHM6Ly9hcHAuZHlubnMuY29tL2tleXMvYXJhYmljdHZoZHYxcHAucGhw'),headers=headers)
    #else:
    #    headers=[('User-Agent',getPv2Code()),('Authorization',base64.b64decode('QmFzaWMgWVcxMU9rQmtia0J1T0RRNQ=='))]
    #    useragent=getUrl(base64.b64decode('aHR0cHM6Ly9hcHAuZHlubnMuY29tL2tleXMvYXJhYmljdHZoZHYxZmYucGhw'),headers=headers)
    return useragent.split('.')[-1]
    

    
def getPV2Url():
    fname='pv2tvpage.json'
    fname=os.path.join(profile_path, fname)
    try:
        jsondata=getCacheData(fname,2*60*60)
        if not jsondata==None:
            return base64.b64decode(jsondata)
    except:
        print 'file getting error'
        traceback.print_exc(file=sys.stdout)

    link=''
    for pvopt in [(1,2),(2,2)]:#[(0,1),(1,1),(1,2)]:
        pvitr,pv2option=pvopt  ##pv2option==2=soapxml with, =1 with 
        try:
            selfAddon.setSetting( id="pv2PlayOption" ,value=str(pv2option))
            mainurl=''
            nm=getPv2Code(True)
            deviceid=''
            if pv2option==1:#not in use
                
                if pvitr==0:
                    mainurl='aHR0cHM6Ly9hcHAuZHlubnMuY29tL2FwcF9wYW5lbG5ldy9vdXRwdXQucGhwL3BsYXlsaXN0P3R5cGU9eG1sJmRldmljZVNuPTEyMyZ0b2tlbj0lcw=='
                else:                    
                    mainurl='aHR0cHM6Ly9hcHAuZHlubnMuY29tL2FwcF9wYW5lbG5ldy9vdXRwdXQucGhwL3BsYXlsaXN0P3R5cGU9eG1sJmRldmljZVNuPXBha2luZGlhaGRwYWlkMi42JnRva2VuPSVz'
            else: #soap xml
                headers=[('User-Agent',base64.b64decode('dW1hci8xLjEgQ0ZOZXR3b3JrLzc1OC4wLjIgRGFyd2luLzE1LjAuMA=='))]
                #iphtml=getUrl(base64.b64decode('aHR0cHM6Ly9hcHAuZHluZG5zLnR2L2tleXMvaXBfY2hlY2sucGhw'),headers=headers)
                #   ipaddrs=re.findall('Address: (.*)',iphtml)[0]
                
                #headers=[('User-Agent',nm),('SOAPAction',base64.b64decode('aHR0cDovL2FwcC5keW5ucy5jb20vc2F2ZURldmljZUlkU2VydmljZS90bnM6ZGIuc2F2ZUlk')),('Content-Type','text/xml; charset=ISO-8859-1')]
                
                #xmldata=base64.b64decode("PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iSVNPLTg4NTktMSI/Pgo8U09BUC1FTlY6RW52ZWxvcGUgU09BUC1FTlY6ZW5jb2RpbmdTdHlsZT0iaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvc29hcC9lbmNvZGluZy8iIHhtbG5zOlNPQVAtRU5WPSJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy9zb2FwL2VudmVsb3BlLyIgeG1sbnM6eHNkPSJodHRwOi8vd3d3LnczLm9yZy8yMDAxL1hNTFNjaGVtYSIgeG1sbnM6eHNpPSJodHRwOi8vd3d3LnczLm9yZy8yMDAxL1hNTFNjaGVtYS1pbnN0YW5jZSIgeG1sbnM6U09BUC1FTkM9Imh0dHA6Ly9zY2hlbWFzLnhtbHNvYXAub3JnL3NvYXAvZW5jb2RpbmcvIiB4bWxuczp0bnM9Imh0dHA6Ly9zY3JpcHRiYWtlci5jb20vc2F2ZURldmljZUlkU2VydmljZSI+CjxTT0FQLUVOVjpCb2R5Pgo8dG5zOmRiLnNhdmVJZCB4bWxuczp0bnM9Imh0dHA6Ly9hcHAuZHlubnMuY29tL3NhdmVEZXZpY2VJZFNlcnZpY2UiPgo8aWQgeHNpOnR5cGU9InhzZDpzdHJpbmciPiVzIEBkbkBuMDMzMTwvaWQ+CjxuYW1lIHhzaTp0eXBlPSJ4c2Q6c3RyaW5nIj4lczwvbmFtZT4KPC90bnM6ZGIuc2F2ZUlkPgo8L1NPQVAtRU5WOkJvZHk+CjwvU09BUC1FTlY6RW52ZWxvcGU+")%(ipaddrs,nm)
                
                #try:
                #    getUrl(base64.b64decode('aHR0cHM6Ly9hcHAuZHlubnMuY29tL2FwaXNvYXAvaW5kZXgucGhw'),post=xmldata,headers=headers)
                #except: pass
                
                deviceid=getPV2Device(pvitr)
                #if pvitr==1: deviceid="331"
                if pvitr==3:                    
                    link=getUrl(base64.b64decode('aHR0cDovL3NoYW5pLm9mZnNob3JlcGFzdGViaW4uY29tL3B2Mkxhc3RXb3JraW5nLnhtbA==')).decode("base64")
                else:
                    mainurl=base64.b64encode(base64.b64decode('aHR0cHM6Ly9hcHMuZHlubnMuY29tL2FwcHMvb3V0cHV0LnBocC9wbGF5bGlzdD90eXBlPXhtbCZkZXZpY2VTbj0lcw==')%deviceid)
                                                               

                #else:
                #    mainurl='aHR0cHM6Ly9hcHAuZHlubnMuY29tL2FwcF9wYW5lbG5ldy9vdXRwdXQucGhwL3BsYXlsaXN0P3R5cGU9eG1sJmRldmljZVNuPTEyMyZ0b2tlbj0lcw=='    
                #mainurl='aHR0cHM6Ly9hcHAuZHlubnMuY29tL2FwcF9wYW5lbG5ldy9vdXRwdXQucGhwL3BsYXlsaXN0P3R5cGU9eG1sJmRldmljZVNuPXBha2luZGlhaGRwYWlkMi42JnRva2VuPSVz'
                    import time
                    TIME = time.time()
                    second= str(TIME).split('.')[0]
                    first =int(second)+int(base64.b64decode('NjkyOTY5Mjk='))
                    token=base64.b64encode(base64.b64decode('JXNAMm5kMkAlcw==') % (str(first),second))
                    #req = urllib2.Request( base64.b64decode('aHR0cHM6Ly9hcHAuZHlubnMuY29tL2FwcF9wYW5lbG5ldy9vdXRwdXQucGhwL3BsYXlsaXN0P3R5cGU9eG1sJmRldmljZVNuPXBha2luZGlhaGRwYWlkMi42JnRva2VuPSVz')  %token)      
                    #req = urllib2.Request( base64.b64decode('aHR0cHM6Ly9hcHAuZHlubnMuY29tL2FwcF9wYW5lbG5ldy9vdXRwdXQucGhwL3BsYXlsaXN0P3R5cGU9eG1sJmRldmljZVNuPTI0NCZ0b2tlbj0lcw==')  %token)    
                    
                    req = urllib2.Request( base64.b64decode(mainurl))#  %(token))    
                    #req.add_header('Authorization', base64.b64decode('QmFzaWMgWVdSdGFXNUFZWE5rWmpwaGMyUm1jWGRsY25SNQ==')) 
                    req.add_header(base64.b64decode("VXNlci1BZ2VudA=="),getPV2UserAgent(pv2option)) 
                    #req.add_header(base64.b64decode("VXNlci1BZ2VudA=="),base64.b64decode("QkVCNDNDOENDNUU5NDVFOTk4QjI3MjM4MDFFQjk0RkY=")) 
                    response = urllib2.urlopen(req)
                    link=response.read()
                if 'items' in link.lower():
                    break;
                #if 'sky sports' in link.lower():
                #    break
        except:
            traceback.print_exc(file=sys.stdout)
            pass
        #    req = urllib2.Request( base64.b64decode('aHR0cHM6Ly9hcHAuZHlubnMuY29tL2FwcF9wYW5lbG5ldy9vdXRwdXQucGhwL3BsYXlsaXN0P3R5cGU9eG1sJmRldmljZVNuPXBha2luZGlhaGRwYWlkMi42JnRva2VuPSVz')  %token)    
        #    req.add_header('Authorization', base64.b64decode('QmFzaWMgWVdSdGFXNDZRV3hzWVdneFFBPT0=')) 
        #    req.add_header(base64.b64decode("VXNlci1BZ2VudA=="),base64.b64decode("dW1hci8xMjQuMCBDRk5ldHdvcmsvNzU5LjIuOCBEYXJ3aW4vMTUuMTEuMjM=")) 
        #    response = urllib2.urlopen(req)
        #    link=response.read()
    if not 'sky sports' in link.lower():
        try:
            dummyxml=getUrl(base64.b64decode('aHR0cDovL3NoYW5pLm9mZnNob3JlcGFzdGViaW4uY29tL3B2MnNwb3J0cy54bWw=')).decode("base64")
            link='<channel>'+dummyxml+link.split('<channel>')[1]
            
        except: pass
    try:
        if 'items' in link:
            storeCacheData(base64.b64encode(link),fname)
    except:
        print 'unitv file saving error'
        traceback.print_exc(file=sys.stdout)
    return link

def getPV2Option():
    return int(selfAddon.getSetting( "pv2PlayOption" ) )
    
def getPV2PlayAuth():
    import base64
    import time
    
    url=base64.b64decode('aHR0cHM6Ly9hcHMuZHlubnMuY29tL3RvcC8lcy5waHA/d21zQXV0aFNpZ249')

    lastplay=getpv2stkey()
    filename=lastplay[:4]
    import datetime  ,hashlib
    timesegment = datetime.datetime.utcnow().strftime("%m/%d/%Y %H:%M:%S")
    validtime=lastplay[4]
    headers=[('User-Agent',base64.b64decode('UGFrJTIwVFYvMS4wIENGTmV0d29yay84MDguMi4xNiBEYXJ3aW4vMTYuMy4w'))]
    
    ipstring=getUrl(base64.b64decode("aHR0cHM6Ly9hcHMuZHlubnMuY29tL3RvcC9pcF9jaGVjay5waHA="),headers=headers)
    ipadd=ipstring.split('Address: ')[1]
    s="%s%s%s%s"%(ipadd,base64.b64decode("dHVtYmluamlhamF5bmFqYW5h")+lastplay[:10],timesegment ,validtime)
    dd=base64.b64decode("c2VydmVyX3RpbWU9JXMmaGFzaF92YWx1ZT0lcyZ2YWxpZG1pbnV0ZXM9JXM=")%(timesegment,base64.b64encode(hashlib.md5(s).hexdigest().lower()),validtime )
##    print dd
    url=(url%filename)+base64.b64encode(dd)
    headers=[('User-Agent',getPv2Code()),('Authorization',base64.b64decode('QmFzaWMgWW05emMyZGliM056T21kdmIyUm5aMjl2WkE9PQ=='))]
##    print repr(url)
    res=getUrl(url,headers=headers)

    s=list(res)
    for i in range( (len(s)-59)/12):
            ind=len(s)-59 + (12*(i))
            if ind<len(s):
                print ind
                s[ind]=''
    return ''.join(s)
    
def tryplay(url,listitem, keepactive=False, aliveobject=None , pdialogue=None, timetowait=None):    
    import  CustomPlayer,time

    try:
        if '.m3u8' in url :
            listitem.setMimeType("flv-application/octet-stream");
            listitem.setContentLookup(False)
    except: print 'error while setting setMimeType, so ignoring it '
    localobject=aliveobject
    player = CustomPlayer.MyXBMCPlayer()
    player.pdialogue=pdialogue
    start = time.time() 
    #xbmc.Player().play( liveLink,listitem)
    player.play( url, listitem)
    xbmc.sleep(1000)
    while player.is_active:
        xbmc.sleep(200)
        if player.urlplayed and not keepactive:
            print 'yes played'
            return True
        if timetowait and (time.time() -start)>timetowait: return False
        xbmc.sleep(1000)
    
    try:
        if localobject: localobject.close()
    except: pass
    print 'not played',url
    return False
              
def tryplaywithping(url,listitem,pingurl,cookiejar, timeout):    
    import  CustomPlayer,time

    player = CustomPlayer.MyXBMCPlayer()
    start = time.time() 
    #xbmc.Player().play( liveLink,listitem)
    player.play( url, listitem)
    xbmc.sleep(1000)
    useragent='Mozilla/5.0 (iPhone; CPU iPhone OS 9_0_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13A452 Safari/601.1'

    headers=[('User-Agent',useragent)]
    getUrl(pingurl, cookieJar = cookiejar,headers=headers)
    import time
    lastpingdone=time.time()
    while player.is_active:
        xbmc.sleep(3000)
        if time.time()-lastpingdone>timeout:
            getUrl(pingurl, cookieJar = cookiejar,headers=headers)
            lastpingdone=time.time()
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
    print 'finalUrl',finalUrl
    if '.ts' in finalUrl or '.mpegts' in finalUrl:
        finalUrl='plugin://plugin.video.f4mTester/?name=%s&url=%s&streamtype=TSDOWNLOADER'%(urllib.quote_plus(name),urllib.quote_plus(finalUrl))
    elif '.m3u8' in finalUrl:
        finalUrl='plugin://plugin.video.f4mTester/?name=%s&url=%s&streamtype=HLSRETRY'%(urllib.quote_plus(name),urllib.quote_plus(finalUrl))
        
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
        xbmcgui.Dialog().notification(__addonname__,line1, __icon__ , time, False)
    else:     
    #    print 'urlToPlay',urlToPlay
        listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
    #    print "playing stream name: " + str(name) 
        xbmc.Player(  ).play( urlToPlay, listitem)  
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
    
def playSports365(url,progress):
    #print ('playSports365')
    played=False
    forced=False
    try:
        import live365
        forced=not live365.isvalid()
        urlToPlay=live365.selectMatch(url)

        if urlToPlay and urlToPlay=="-1":
            dialog = xbmcgui.Dialog()
            ok = dialog.ok('XBMC', 'Couldn\'t play, Please visit their website and try again!')        
            urlToPlay=None
        if urlToPlay and len(urlToPlay)>0:
            
            listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
            if 'f4mtester' in urlToPlay:
                xbmc.executebuiltin('XBMC.RunPlugin('+urlToPlay+')') 
            else:        
        #    print   "playing stream name: " + str(name) 
                #xbmc.Player().play( urlToPlay, listitem)  
                progress.close()
                #xbmc.Player().play( urlToPlay, listitem)  
                played=tryplay(urlToPlay,listitem) 
    except:
        pass
    import time
    if not played  and RefreshResources([('live365.py','http://shani.offshorepastebin.com/live365.py',forced)]):
        
        dialog = xbmcgui.Dialog()
        ok = dialog.ok('XBMC', 'Updated files dyamically, Try to play again, just in case!')          
        print 'Updated files'
    return


def getFastAuth(url):
    print 'url',url
    postUrl=None
    stripping=True
    fastData=getFastData()   
    if fastData["DATA"][0]["HelloUrl"] in url or  fastData["DATA"][0]["HelloUrl1"]  in url:
        postUrl=fastData["DATA"][0]["HelloLogin"]
        auth='Basic %s'%base64.b64encode(fastData["DATA"][0]["PasswordHello"]) 
        stripping=False
    elif fastData["DATA"][0]["LiveTvUrl"] in url:
        postUrl=fastData["DATA"][0]["LiveTvLogin"]
        auth='Basic %s'%base64.b64encode(fastData["DATA"][0]["PasswordLiveTv"])
    elif fastData["DATA"][0]["nexgtvUrl"] in url:
        print 'processnextgtv'
        postUrl=fastData["DATA"][0]["nexgtvToken"]
        auth='Basic %s'%base64.b64encode(fastData["DATA"][0]["nexgtvPass"]) 
        stripping=False
    elif '.m3u8' not in url:
        print 'skip auth'
    else:
        postUrl=fastData["DATA"][0]["loginUrl"]
        auth='Basic %s'%base64.b64encode(fastData["DATA"][0]["Password"])   
    
    if postUrl:
        headers=[('User-Agent',getFastUA()),('Authorization',auth)]
        res=getUrl(postUrl,headers=headers)
        s=list(res)
        if stripping:
            for i in range( (len(s)-59)/12):
                    ind=len(s)-59 + (12*(i))
                    if ind<len(s):
                        print ind
                        s[ind]=''
        ret= ''.join(s)
        return url+'?'+ret.split('?')[1]
    return url
    
    
def getFastPlayUA():

    fastData=getFastData()   
    return fastData["DATA"][0]["Agent"]

def getNetworkTVStringExtra3(response):
        response = response.strip();
        builder  = list(response);
        ilen = len(builder) -1
        del builder[ilen - 10];
        del builder[ilen - 22];
        del builder[ilen - 34];
        del builder[ilen - 46];
        del builder[ilen - 58];
        return "".join(builder)
        
def getNetworkTVStringExtra(response):
        response = response.strip();
        builder  = list(response);
        ilen = len(builder) -1
        del builder[ilen - 33+1];
        del builder[ilen - 42+2];
        del builder[ilen - 51+3];
        del builder[ilen - 58+4];
        return "".join(builder)

def getNetworkTVStringExtra2(response):
    try:
        response = response.strip();
        builder  = list(response);
        ilen = len(builder) -1
        del builder[ilen - 35+1];
        del builder[ilen - 46+2];
        del builder[ilen - 57+3];
        del builder[ilen - 66+4];
        return "".join(builder)
    except : return ""

def getNetworkTVHash (value):
    import time
    k=str( value^ int(time.time()))
    rval=""
    for i in range(len(k)):
        rval+=str(k[i])+str(i)
    return rval

   
def PlayNetworkTVLink2(url,progress=None):
    if 1==2:#not mode==37:
        print url
        ##cat,url=url.split('=')
        #xmldata=getNetworkTVPage2()
        ##print 'got getFastTVChannels',xmldata
        #for ss in xmldata["channels"]:
        #    if ss["streamid"]==url:
        #        url=ss
        #        break
    print 'xxxxxxxxxxxxxxxxxxxxx',url
    
    apptype,url=url.split(":")
    apptype=int(apptype)
    pagedata=getNetworkTVPage2(apptype)
    username=pagedata["user_info"]["username"]
    pwd=pagedata["user_info"]["password"]
    server=pagedata["server_info"]["url"]
    port=pagedata["server_info"]["port"]
    finalurl= "http://" + server + ":" + port + "/live/" + username + "/" + pwd + "/" + url + ".ts"
    
    netData=getNetworkTVData2(apptype)["DATA"][0]
    ua=netData["UserAgent"]
    
    urlnew=finalurl+"|User-Agent="+ua
    return playipbox(urlnew)
    
    print urlnew
    listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
    PlayGen(base64.b64encode(urlnew))
    #tryplay( urlnew , listitem,keepactive=True, aliveobject =ws , pdialogue= progress)

def PlayNetworkTVLink(url,progress=None):
    if 1==1:#not mode==37:
        print url
        #cat,url=url.split('=')
        xmldata=getNetworkTVPage()
        #print 'got getFastTVChannels',xmldata
        for ss in xmldata["channels"]:
            if ss["streamid"]==url:
                url=ss
                break
    print url
    token=url["token"]
    finalurl=""
    anduseragent=getFastUA(v2=True)
    #['33','18','0','29']         
    if token=="0":
        finalurl=url["streamurl"]
    elif token=="33":
        netData=getNetworkTVData()
        posturl=netData["ZmFtYW50YXJhbmFfdGF0aTAw"][1:].decode("base64")
        auth=netData["dGVydHRleWFj"][1:].decode("base64")
        ref=url["referer"]
        authua=url["user_agent"]

            
        headers=[('Authorization',auth)]
        if ref and len(ref)>0:
            headers.append(('Referer',ref))
        if authua and len(authua)>0:
            headers.append(('User-Agent',authua))     
        else:
            headers.append(('User-Agent',anduseragent))
            
        
        authdata2=getUrl(posturl,headers=headers)
        authdata=getNetworkTVStringExtra(authdata2)
        
        defplayua=anduseragent
        playua=url["player_user_agent"]
        if playua and len(playua)>0:
            defplayua=playua
        finalurl=url["streamurl"]+authdata+"|User-Agent="+defplayua
        finalurl2=url["streamurl"]+authdata2+"|User-Agent="+defplayua
        listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
        listitem.setMimeType("flv-application/octet-stream");
        listitem.setContentLookup(False)
        if not tryplay( finalurl , listitem,pdialogue= progress, timetowait=12):
            tryplay( finalurl2 , listitem,pdialogue= progress, timetowait=12)
        return
    elif token=="18":
        netData=getNetworkTVData()    
        posturl=url["streamurl"]
        ref=url["referer"]
        authua=url["user_agent"]
        
        headers=[]
        if ref and len(ref)>0:
            headers.append(('Referer',ref))
        if authua and len(authua)>0:
            headers.append(('User-Agent',authua))     
        else:
            headers.append(('User-Agent',anduseragent))
            
        rethtml=getUrl(posturl,headers=headers)
        playurl=re.findall( "((http|https):[^\" ]+m3u8[^\" ]*)", rethtml)[-1]
        
        #if len(playurl)==0:
        #    playurl=re.findall( "http.*?m3u8.*)", rethtml)
        print playurl
        defplayua=anduseragent
        playua=url["player_user_agent"]
        print playua
        if playua and len(playua)>0:
            defplayua=playua
        finalurl=playurl[0].split('\'')[0]+"|User-Agent="+defplayua
    elif token in ["38", "26"]:
        #netData=getNetworkTVData()    
        #posturl=netData["YmVsZ2lfMzgw"][1:].decode("base64")
        #auth=netData["Z2Vsb29mc2JyaWVm"][1:].decode("base64")
        ref=url["referer"]
        #authua=url["user_agent"]

            
        headers=[('User-Agent','ZemTv')]
        #if ref and len(ref)>0:
        #    headers.append(('Referer',ref))
        #if authua and len(authua)>0:
        #    headers.append(('User-Agent',authua))     
        #else:
        #    headers.append(('User-Agent',anduseragent))
        import time     
        #authdata2=getUrl(posturl,headers=headers)
        authdata2=getUrl(base64.b64decode("aHR0cDovL3NoYW5pLm9mZnNob3JlcGFzdGViaW4uY29tL2dldG5ldHR2dG9rZW4ucGhw")+"?dt="+str(int(time.time())),headers=headers)
        authdata=getNetworkTVStringExtra2(authdata2)
        
        defplayua=anduseragent
        playua=url["player_user_agent"]
        if playua and len(playua)>0:
            defplayua=playua
        finalurl=url["streamurl"]+authdata+"|User-Agent="+defplayua
        #finalurl2=url["streamurl"]+authdata2+"|User-Agent="+defplayua
        
        #listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
        #listitem.setMimeType("flv-application/octet-stream");
        #listitem.setContentLookup(False)
        #if not tryplay( finalurl , listitem,pdialogue= progress, timetowait=12):
         #   tryplay( finalurl2 , listitem,pdialogue= progress, timetowait=12)
        #return
        
    elif token in ["24","25","28","29","30","31","32"]:
        mapping={"24":   ["YW1pX2NoYmlz","TWVuX2Nob2Jpc18w","",0],
                "25":["aXRob2toZW5pX3BhaHMw","QmVuX3BhaGlz","",0],
                "28":["Y29udGFkb3JfYWhpczAw","YXRhaXNfaW5p","Ym9ldHNhX3Nla2VuZ19yYXN0YV9hdGFpczAw","dWt1cWFxd2FfY2hhYmlfYXRhaGlz"],
                "29": ["YmVsaXJ0ZWNfb250aXMw","c2F5YV9kb25v","Y2hlaWxlYWRoIF9DZWFuZ2FsX29udGlz","cGFyb2xfaGFsX2NoYWJpX29uYXRpczAw"],
                "30": ["cG9udHNvX3Rlc3Mw","bXdlbnRlcnR5","Y2hlaWxlYWRoX29yX3RlZXMw","c2lmcmVfY296bWVfQW5haHRhcmlfdGVz"],
                "31": ["bmFic2FuYV9pa2l0czAw","dGVydDFfaW5p","bmdhZGVrcmlwX3Jhc3RhX2lrYXRpczAw","ZGVzenlmcm93YW5pZV9rbHVjel9pa2F0aXMw"],
                "32": ["bWFya2llcmlzX2J0aXMw","dGVydHR3X2Ji","dWt1c3VzYV91a3ViaGFsYV9iYXRlczAw","dHNoaXJvbG9sb19rZV9iYXRpczAw"]
                }
        tokenLinkKey,tokenCredsKey,decryptorLinkKey,decryptorKeyKey=mapping[token]

        netData=getNetworkTVData()
        
        tokenLink=netData[tokenLinkKey][1:].decode("base64")
        tokenCreds=netData[tokenCredsKey][1:].decode("base64")
        decryptorLink=netData[decryptorLinkKey][1:].decode("base64")
        print netData[decryptorKeyKey]
        decryptorKey=0
        if not decryptorKeyKey==0:
            decryptorKey=int(netData[decryptorKeyKey][1:].decode("base64"))
        print 'decryptorKey',decryptorKey
        bp=netData["YnVueWFkaV9wYXRhX25hdnVh"][1:].decode("base64")
        print 'bp',bp
        posturl=url["streamurl"]
        ref=url["referer"]
        authua=url["user_agent"]
        
        headers=[]
        if ref and len(ref)>0:
            headers.append(('Referer',ref))
        if authua and len(authua)>0:
            headers.append(('User-Agent',authua))     
        else:
            headers.append(('User-Agent',anduseragent))
        if tokenCreds and len(tokenCreds)>0:
            headers.append(('Authorization',tokenCreds))
        print 'tokenLink',tokenLink
        authhtml=getUrl(tokenLink,headers=headers)
        headers=[]
        print netData["TW9vbl9oaWsx"]
        x1auth=int(netData["TW9vbl9oaWsx"][1:].decode("base64"))
        c1auth=netData["amFnX3Ryb3JfYXR0X2Vu"][1:].decode("base64")
        headers.append(('Authorization',c1auth))
        hashval=getNetworkTVHash(x1auth if decryptorKey == 0 else decryptorKey)
        headers.append(('Modified',hashval))
        if not (decryptorLink and len(decryptorLink)>0):
            decryptorLink=bp+ "decrypt.nettv/"
        jsondata={'stream_url':url["streamurl"],'token':int(token),'response_body':authhtml}
        post={'data':json.dumps(jsondata)}
        post = urllib.urlencode(post)
        if authua and len(authua)>0:
            headers.append(('User-Agent',authua))     
        else:
            headers.append(('User-Agent',anduseragent))
            
        htmldata=getUrl(decryptorLink,headers=headers,post=post)
        
        playurl=json.loads(htmldata)["stream_url"]
        
        #if len(playurl)==0:
        #    playurl=re.findall( "http.*?m3u8.*)", rethtml)
        print playurl
        defplayua=anduseragent
        playua=url["player_user_agent"]
        print playua
        if playua and len(playua)>0:
            defplayua=playua
        finalurl=playurl.split('\'')[0]+"|User-Agent="+defplayua
        
        
    elif token in ["26"]:
        settingslinkkey="cGFrX2l5YWhvb18x"
        settingsecuritykey="UGFrX3VrdWJ1bmdhemEx"
        

        netData=getNetworkTVData()
        settingslink=netData[settingslinkkey][1:].decode("base64")
        settingsecurity=netData[settingsecuritykey][1:].decode("base64")
        print settingslink,settingsecurity
        
        
        streamurl=url["streamurl"]
        ref=url["referer"]
        authua=url["user_agent"]
        
        
        headers=[]
        if ref and len(ref)>0:
            headers.append(('Referer',ref))
        if authua and len(authua)>0:
            headers.append(('User-Agent',authua))     
        else:
            headers.append(('User-Agent',anduseragent))
        if settingsecurity and len(settingsecurity)>0:
            headers.append(('Authorization',settingsecurity))

        settingjson=json.loads(getUrl(settingslink,headers=headers))
        print settingjson
        jsonurl=settingjson["DATA"][0]["URL"]
        jsonpassword=settingjson["DATA"][0]["Password"]
        jsonvalue=settingjson["DATA"][0]["Value"]
        headers=[]
        hashval=getNetworkTVHash(jsonvalue)
        headers.append(('Modified',hashval))
        headers.append(('User-Agent',anduseragent))
            
        htmldata=getUrl(jsonurl,headers=headers)
        print htmldata
        
        finalurl=streamurl+getNetworkTVStringExtra3(htmldata)
        defplayua=anduseragent
        playua=jsonpassword
        if playua and len(playua)>0:
            defplayua=playua
        finalurl=finalurl+"|User-Agent="+defplayua
    else:
        finalurl=""
    print "finalurl",finalurl
    urlnew=finalurl
    listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
    PlayGen(base64.b64encode(urlnew))
    #tryplay( urlnew , listitem,keepactive=True, aliveobject =ws , pdialogue= progress)
    
def decodeEInth(lnk):
    t=10
    #var t=10,r=e.slice(0,t)+e.slice(e.length-1)+e.slice(t+2,e.length-1)
    r=lnk[0:t]+lnk[-1]+lnk[t+2:-1]
    return r
def encodeEInth(lnk):
    t=10
    #var t=10,r=e.slice(0,t)+e.slice(e.length-1)+e.slice(t+2,e.length-1)
    r=lnk[0:t]+lnk[-1]+lnk[t+2:-1]
    return r
    
def PlayEinthusamLink(url,progress=None):
    url,lang=url.split(',')
    cookieJar = cookielib.LWPCookieJar()
    headers=[('Origin','https://einthusan.tv'),('Referer','https://einthusan.tv/movie/browse/?lang=hindi'),('User-Agent',base64.b64decode('TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgNi4xOyBXT1c2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzU1LjAuMjg4My44NyBTYWZhcmkvNTM3LjM2'))]
    mainurl='https://einthusan.tv/movie/watch/%s/?lang=%s'%(url,lang)
    mainurlajax='https://einthusan.tv/ajax/movie/watch/%s/?lang=%s'%(url,lang)
    
    #htm=getUrl(mainurl,headers=headers,cookieJar=cookieJar)
    htm=getUrl(mainurl,headers=headers,cookieJar=cookieJar)
    lnk=re.findall('data-ejpingables=["\'](.*?)["\']',htm)[0]#.replace('&amp;','&')

    r=decodeEInth(lnk)
    #for s in json.loads(r.decode("base64")):
    #    getUrl(s,headers=headers,cookieJar=cookieJar)
    jdata='{"EJOutcomes":"%s","NativeHLS":false}'%lnk
    
    h = HTMLParser.HTMLParser()
    gid=re.findall('data-pageid=["\'](.*?)["\']',htm)[0]
    gid=h.unescape(gid).encode("utf-8")
    #gid="mDLAIYbcj9HmxLt7F+2j8p1cOpLlUmNfbcGXxmG0yPBMJzVUCwih/D02umaXkrhNP3Vh3ZUayTVmNy4DLatp4w=="
    #for s in ["goadx_primary_lr1","goadx_primary_lb1","goadx_primary_lb2","goadx_primary_lb3"]:
    #    postdata={'xEvent':'GetAd','xJson':'{"AdID":"%s"}'%s,'arcVersion':'3','appVersion':'59','tabID':gid+'652','gorilla.csrf.Token':gid}
    #    postdata = urllib.urlencode(postdata)
    #    rdata=getUrl('https://einthusan.tv/ajax/movie/watch/4jWb/?lang=hindi',headers=headers,post=postdata,cookieJar=cookieJar)
        
    
    postdata={'xEvent':'UIVideoPlayer.PingOutcome','xJson':jdata,'arcVersion':'3','appVersion':'59','gorilla.csrf.Token':gid}
    postdata = urllib.urlencode(postdata)
    rdata=getUrl(mainurlajax,headers=headers,post=postdata,cookieJar=cookieJar)
    r=json.loads(rdata)["Data"]["EJLinks"]
    print r
    lnk=json.loads(decodeEInth(r).decode("base64"))["HLSLink"]
    
    
      
    urlnew=lnk+('|https://einthusan.tv&Referer=%s&User-Agent=%s'%(mainurl,'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'))
    listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
    PlayGen(base64.b64encode(urlnew))
    #tryplay( urlnew , listitem,keepactive=True, aliveobject =ws , pdialogue= progress)
        
    
    
def PlayFastLink(url,progress=None):
    if 1==1:#not mode==37:
        print url
        cat,url=url.split('=')
        xmldata=getFastTVPage(cat)
        #print 'got getFastTVChannels',xmldata
        for ss in xmldata["LIVETV"]:
            if ss["id"]==url:
                url=ss["channel_url"]
                break
        
    print 'url is',url 
    if len(url.split('http:'))>2:
        url='http:'+url.split('http:')[-1]
    urlnew=getFastAuth(url)+'|User-Agent='+getFastPlayUA()
    listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
    PlayGen(base64.b64encode(urlnew))
    #tryplay( urlnew , listitem,keepactive=True, aliveobject =ws , pdialogue= progress)
    
    
def PlaySafeLink(url, recursive=False, usecode=None, progress=None):


    import safelinks
    listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
    urlnew, ws=safelinks.getSafeLink(url, progress=progress, name=name)
    PlayGen(base64.b64encode(urlnew))
    #tryplay( urlnew , listitem,keepactive=True, aliveobject =ws , pdialogue= progress)
    

def safeFinishedTest(dur):
    import math
    res = "";
    kbMulti = 1
    if (dur > 5): #// 43 kb/s
        res = "GPRS"; 
    elif (dur > 2):# // 47 kb/s | onlinedemo : ~2.3s
        res = "2G"; 
        kbMulti = 2.6;
    elif (dur > 1.3):# // 89 kb/s | onlinedemo : ~1.3s
        res = "2G"; 
        kbMulti = 2.8;
    elif (dur > 0.7):# // 153 kb/s | onlinedemo : ~0.8s
        res = "3G"; 
        kbMulti = 3;
    elif (dur > 0.4):# // 358 kb/s | onlinedemo : ~0.45s
        res = "3G";
        kbMulti = 3;
    elif (dur > 0.3):# // 358 kb/s | onlinedemo : ~0.35s
        res = "DSL";
        kbMulti = 3.3;
    else:
        res = "4G"; 
        kbMulti = 4;
    kbps = (210 / dur) * 1.024 * kbMulti
    kbps = round(kbps * 100) / 100
    kbRes = "";
    if (kbps > 1500.0):
        kbRes = "4G";
    elif (kbps > 600.0):
        kbRes = "DSL";
    elif (kbps > 300.0):
        kbRes = "3G";
    elif (kbps > 100.0):
        kbRes = "2G";
    else:
        kbRes = "GPRS";
    
                
    return "210",kbps, kbRes, res
     
def PlayPV2Link(url):

    if 1==1:#not mode==37:
        xmldata=getPV2Url()
        url=base64.b64decode(url)

        urlToPlay=re.findall('>'+url+'</programID>.*?programURL\\>(.*?)\\<',xmldata)[0]
    else:
        urlToPlay=base64.b64decode(url)

#    print 'urlToPlay',urlToPlay    
    urlToPlay+=getPV2PlayAuth()
    if '|' not in urlToPlay:
        urlToPlay+='|'
    import random
    useragent='User-Agent=AppleCoreMedia/1.0.0.%s (%s; U; CPU OS %s like Mac OS X; en_gb)'%(random.choice(['13G35','13G36','14A403','14A456','14B72','14B150']),random.choice(['iPhone','iPad','iPod']),random.choice(['9.3.4','9.3.5','10.0.2','10.1','10.1.1']))
    urlToPlay+=useragent



    listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )


    if not tryplay(urlToPlay, listitem):
        if '130.185.144.112' not in urlToPlay:
            urlToPlay2='http://130.185.144.112:8081/'+'/'.join(urlToPlay.split('/')[3:])          
            print urlToPlay2
            if not tryplay(urlToPlay2, listitem):
                return False
    
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
        playSports365(url.split('Sports365:')[1],progress)
        return
    if "CF:" in url:
        PlayCFLive(url.split('CF:')[1])
        return    
    if "uktvnow:" in url:
        PlayUKTVNowChannels(url.split('uktvnow:')[1])
        return
    if "testpage:" in url:
        import testarea
        testarea.play(name,url.split('testpage:')[1],mode)
        return
    if "direct:" in url:
        PlayGen(base64.b64encode(url.split('direct:')[1]))
        return    
    if "mytv:" in url:
        playMYTV(base64.b64encode(url.split('mytv:')[1]))
        return  
        
    if "direct3:" in url:
        PlayGen(base64.b64encode(url.split('direct3:')[1]),True,followredirect=True)
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
        PlayGen(base64.b64encode(url.split('ptc:')[1]+getPTCAuth()+'|User-Agent=AppleCoreMedia/1.0.0.13A452 (iPhone; U; CPU OS 9_0_2 like Mac OS X; en_gb)'))
        return    
    if "pv2:" in url:
        PlayPV2Link(url.split('pv2:')[1])
        return 
    if "fast:" in url:
        PlayFastLink(url.split('fast:')[1],progress=progress)
        return 
    if "emovies:" in url:
        PlayEinthusamLink(url.split('emovies:')[1],progress=progress)
        return 
    if "networktv:" in url:
        PlayNetworkTVLink(url.split('networktv:')[1],progress=progress)
        return    
    if "networktv2:" in url:
        PlayNetworkTVLink2(url.split('networktv2:')[1],progress=progress)
        return    

        
    if "safe:" in url:
        PlaySafeLink(url.split('safe:')[1],progress=progress)
        return        
    if "tvplayer:" in url:
        playtvplayer(url.split('tvplayer:')[1])
        return  
    if "streamhd:" in url:
        playstreamhd(url.split('streamhd:')[1])
        return
    if "mamahd:" in url:
        playmamahd(url.split('mamahd:')[1])
        return
        
    if "hdfree:" in url:
        playHDFree(url.split('hdfree:')[1])
        return                       
    if "infi:" in url:
        playInfinite(url.split('infi:')[1])
        return                       
    if "zenga:" in url:
        playzenga(url.split('zenga:')[1],progress)
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
        print link
        paa='(content.jwplatform.com.players.*?.js)'
        ln=re.findall(paa,link)
        if len(ln)>0:
            print ln, 'ln val'
            link=getUrl('http://'+ln[0])
        
#        curlpatth='file: "(htt.*?)"' if 'qtv' not in url else 'file: \'(.*?)\''
        curlpatth='file[\'"]?: [\'"](.*?)[\'"]'
        
        progress.update( 50, "", "Preparing url..", "" )
        dag_url =re.findall(curlpatth,link)[-1]
        if dag_url.startswith('rtmp'): dag_url+=' timeout=20'
        direct=True
    elif url=='etv':
        req = urllib2.Request(base64.b64decode('aHR0cDovL2VuZ2xpc2gucHJhZGVzaDE4LmNvbS9hamF4LXN0cmVhbWluZy5waHA/ZGV2aWNlPXdlYiZjaGFubmVsPWV0di11cmR1Jnc9MTAwJTI1Jmg9NTAw'))
        req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
        response = urllib2.urlopen(req)
        link=response.read()
        curlpatth='<backup.*?(http.*?)\]?\]?>'
        encdataurl=re.findall(curlpatth,link)[0]
        encdata=getUrl(encdataurl)
        
        #from mixed swf
        paragraph= base64.b64decode("UGFjayBteSBib3ggd2l0aCAjMTI1IGxpcXVvciBqdWdzLiBCTE9XWlkgTklHSFQtRlJVTVBTIFZFWCdEIEpBQ0sgUS4gSmFja2Rhd3MgbG92ZSBteSAzOCBiaWcgc3BoaW54IG9mICJxdWFydHoiLiAyKzI9NCwgQSBRVUlDSy1tb3ZlbWVudCBvZiB0aGUgZW5lbXkgd2lsbCBqZW9wYXJkaXplICM2OSBndW5ib2F0czsgZm9yc2FraW5nIG1vbmFzdGljIHRyYWRpdGlvbjogNDclIGpvdmlhbCBmcmlhcnMgZ2F2ZSB1cCB0aGVpciAqdm9jYXRpb24qIGZvciBhIHF1ZXN0aW9uYWJsZSBleGlzdGVuY2Ugb24gdGhlIChmbHlpbmcpIHRyYXBlemUgZWFybmluZyAkMC1yZXR1cm5zISBXRSBxdWlja2x5IFNFSVpFRCBUSEUgW0JMQUNLXSBBWExFICYgSlVTVCBTQVZFRCBJVCBGUk9NIEdPSU5HIFBBU1QgSElNLiBJcyAzPjU/IG9yIGlzIDU8Mz8gIGNvbnRhY3RAbmV0d29yazE4dGVjaC5jb21+L18=")
        finalurl=''
        for i in encdata.split(','):
            finalurl+=paragraph[int(i)]
        
        progress.update( 50, "", "Preparing url..", "" )
        dag_url =finalurl
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

def getChannelsFromEbound():
    fname='povee.json'
    fname=os.path.join(profile_path, fname)
    try:
        jsondata=getCacheData(fname,2*60*60)#2 hours
        if not jsondata==None:
            return eval(base64.b64decode(jsondata))
    except:
        print 'file getting error'
        traceback.print_exc(file=sys.stdout)
        
    data=getChannelsFromEboundInternal()
    try:
        if data and len(data)>0:
            storeCacheData(base64.b64encode(str(data)),fname)
    except:
        print 'povee file saving error'
        traceback.print_exc(file=sys.stdout)
    return data
    
def getChannelsFromEboundInternal():

    match=[]
    pvhtml=getUrl('http://poovee.net/profile/poovee/1/')
    reg='<div class=\"video-data\">\s*.*?href=\".*?\/video\/([0-9]*?)\/.*?title=\"(.*?)\"'
    links=re.findall(reg,pvhtml)
    for s in links:
        if not (s[1].lower().startswith('office') or s[1].lower() in ['poovee','ary zindagai','qtv','see tv','samaa tv','mashriq tv','madani','jaag tv','hadi','dunya','dawn low','daily jeejal','channel 24']):
            nm=s[1]
            if 'Baharia' in nm: nm=nm.replace('Baharia','Bahria')
            if 'Bahari' in nm: nm=nm.replace('Bahari','Bahria')
            
            
            match.append((nm,s[0],'povee','http://shani.offshorepastebin.com/ZemLogos/%s.png'%nm.lower().replace(' ','')))        

    #print 'main',str(match)     
    if 1==2:# just to generate the static povee links
        pvhtml=getUrl('http://shani.offshorepastebin.com/ZemLogos/eb.xml')
        reg='<title>(.*?)<\/title>\s.*?doreg.*?\s.*\s.*\s.*\s.*?\/embed\/([0-9]*)\/.*\s.*\s<thumbnail>(.*?)<'
        links=re.findall(reg,pvhtml)
        match2=[]
        for s in links:
            if s[0].replace(' ','').lower() not in (i[0].replace(' ','').lower() for i in match):
                match2.append((s[0],s[1],'povee',s[2])) 
        print 'reg',str(match2)   
    match+=[('HEALTH TV', '349', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/htv.png'), ('ZAIQA TFC', '101576', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/zaiqatfc.png'), ('A PLUS', '297', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/aplus.png'), ('A TV', '399', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/atv.png'), ('ARY DIGITAL', '220186', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/arydigital.png'), ('ARY ZINDAGI', '220241', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/aryzindagi.png'), ('DM DIGITAL', '373', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/dmdigital.png'), ('DTV PLUS', '313', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/dtvplus.png'), ('FILMASIA', '2324', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/filmasia.png'), ('HUM TV ASIA', '307', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/humtv.png'), ('ON TV', '13681', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/ontv.png'), ('PLAY ENTERTAINMENT', '379', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/playentertainment.png'), ('SEE TV HD', '187', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/seetvhd.png'), ('STAR MAX', '2322', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/starmax.png'), ('TIMES', '397', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/times.png'), ('TV ONE', '363', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/tvone.png'), ('VIBE', '383', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/vibetv.png'), ('8XM HD', '51308', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/8xmhd.png'), ('ANDAZ TV', '52166', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/andaztv.png'), ('JALWA', '393', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/jalwa.png'), ('92 NEWS HD', '239', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/92newshd.png'), ('AAJ NEWS', '343', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/aajnews.png'), ('ABB TAKK', '15410', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/abbtakk.png'), ('ADALAT NEWS', '29416', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/adalatnews.png'), ('CAPITAL TV', '335', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/capitaltv.png'), ('CHANNEL 5', '337', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/channel5.png'), ('DAWN NEWS', '323', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/dawnnews.png'), ('DIN NEWS', '351', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/dinnews.png'), ('DUNYA NEWS', '220156', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/dunyanews.png'), ('JAAG', '208646', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/jaag.png'), ('METRO 1 NEWS', '391', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/metro1news.png'), ('NEO NEWS', '331', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/neonews.png'), ('NEWS ONE', '385', 'povee', 'http://www.newsone.tv/wp-content/uploads/2016/01/cropped-logo-newsone.png'), ('RASSAI', '29904', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/rassai.png'), ('ROYAL NEWS 24/7', '377', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/royalnews247.png'), ('ROZE NEWS', '301', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/rozenews.png'), ('SAMAA', '220149', 'povee', 'http://vignette2.wikia.nocookie.net/logopedia/images/1/12/Samaa_TV.png'), ('SUCH TV', '365', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/suchtv.png'), ('WAQT NEWS', '353', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/waqtnews.png'), ('MOVIES 24/7', '40774', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/movies247.png'), ('APNA CHANNEL', '345', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/apnachannel.png'), ('ARUJ', '104227', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/aruj.png'), ('AVT KHYBER', '289', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/avtkhyber.png'), ('AWAZ', '333', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/awaz.png'), ('INDEPENDENT', '305', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/independent.png'), ('K 21', '38158', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/k21.png'), ('KAY 2', '291', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/kay2.png'), ('KHYBER NEWS', '287', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/khybernews.png'), ('MASHRIQ', '140409', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/mashriq.png'), ('MEHRAN TV', '401', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/mehrantv.png'), ('PASHTO 1', '293', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/pashto1.png'), ('SHAMSHAD', '375', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/shamshad.png'), ('SHARQ RADIO TV', '11892', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/sharqradiotv.png'), ('SINDH TV', '163810', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/sindhtv.png'), ('SINDH TV NEWS', '369', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/sindhtvnews.png'), ('VSH NEWS', '361', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/vshnews.png'), ('WASEB', '371', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/waseb.png'), ('ZHWANDOON', '357', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/zhwandoon.png'), ('ARY QTV', '220248', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/aryqtv.png'), ('HADI TV 1', '49338', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/haditv1.png'), ('MADANI CHANNEL', '387', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/madanichannel.png'), ('QURAN TV MADINA', '27768', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/qurantv.png'), ('QURAN TV MECCA', '303', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/qurantv.png'), ('PAIGHAM', '381', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/paigham.png'), ('PEACE TV URDU', '220131', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/peacetvurdu.png'), ('RAAH TV', '395', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/raahtv.png'), ('TEHZEEB TV', '231', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/tehzeebtv.png'), ('ZINDAGI TV', '327', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/zindagitv.png'), ('TEN SPORTS OFFICIAL', '32360', 'povee', 'http://shani.offshorepastebin.com/ZemLogos/tensports.png')]   
             
    if 1==2:# just to generate the static static links
        pvhtml=getUrl('http://shani.offshorepastebin.com/ZemLogos/eb.xml')
        reg='<title>(.*?)<\/title>\s<link>(http.*?eboundservice.*?)<.*\s<thumbnail>(.*?)<'
        links=re.findall(reg,pvhtml)
        match2=[]
        for s in links:
            if s[0].replace(' ','').lower() not in (i[0].replace(' ','').lower() for i in match):
                match2.append((s[0],base64.b64encode(s[1]),'gen',s[2])) 
        print 'static',str(match2)            

    match+=[('HUM MASALA', 'aHR0cDovL3N0cmVhbWVyMjcuZWJvdW5kc2VydmljZXMuY29tL3RlaGFtaW1la3lsMDAvbWFzYWxhdHYvcGxheWxpc3QubTN1OA==', 'gen', 'http://shani.offshorepastebin.com/ZemLogos/hummasala.png'), ('AAJ ENTERTAINMENT', 'aHR0cDovL3N0cmVhbWVyMjcuZWJvdW5kc2VydmljZXMuY29tL3RlaGFtaW1la3lsMDAvYWFqZW50ZXJ0YWlubWVudC9wbGF5bGlzdC5tM3U4', 'gen', 'http://shani.offshorepastebin.com/ZemLogos/aajentertainment.png'), ('COLORS', 'aHR0cDovL3N0cmVhbWVyMjcuZWJvdW5kc2VydmljZXMuY29tL3RlaGFtaW1la3lsMDAvY29sb3JzL3BsYXlsaXN0Lm0zdTg=', 'gen', 'http://shani.offshorepastebin.com/ZemLogos/colors.png'), ('EXPRESS ENTERTAINMENT', 'aHR0cDovL3N0cmVhbWVyNjEuZWJvdW5kc2VydmljZXMuY29tL21vYmlsZS9leHByZXNzZW50ZXJ0YWlubWVudC9wbGF5bGlzdC5tM3U4', 'gen', 'http://shani.offshorepastebin.com/ZemLogos/expressentertainment.png'), ('G1 TV', 'aHR0cDovL3N0cmVhbWVyMjcuZWJvdW5kc2VydmljZXMuY29tL3RlaGFtaW1la3lsMDAvZzF0di9wbGF5bGlzdC5tM3U4', 'gen', 'http://shani.offshorepastebin.com/ZemLogos/g1tv.png'), ('GEO KAHANI', 'aHR0cDovL3N0cmVhbWVyMjcuZWJvdW5kc2VydmljZXMuY29tL3RlaGFtaW1la3lsMDAvZ2Vva2FoYW5pL3BsYXlsaXN0Lm0zdTg=', 'gen', 'http://shani.offshorepastebin.com/ZemLogos/geokahani.png'), ('GEO TV', 'aHR0cDovL3N0cmVhbWVyMjcuZWJvdW5kc2VydmljZXMuY29tL3RlaGFtaW1la3lsMDAvZ2VvZW50ZXJ0YWlubWVudC9wbGF5bGlzdC5tM3U4', 'gen', 'http://shani.offshorepastebin.com/ZemLogos/geoentertainment.png'), ('HBO', 'aHR0cDovL3N0cmVhbWVyMjcuZWJvdW5kc2VydmljZXMuY29tL3RlaGFtaW1la3lsMDAvaGJvL3BsYXlsaXN0Lm0zdTg=', 'gen', 'http://shani.offshorepastebin.com/ZemLogos/hbo.png'), ('HUM SITARAY WORLD', 'aHR0cDovL3N0cmVhbWVyNjEuZWJvdW5kc2VydmljZXMuY29tL21vYmlsZS9odW0yL3BsYXlsaXN0Lm0zdTg=', 'gen', 'http://shani.offshorepastebin.com/ZemLogos/humsitaray.png'), ('PTV GLOBAL', 'aHR0cDovL3N0cmVhbWVyMjcuZWJvdW5kc2VydmljZXMuY29tL3RlaGFtaW1la3lsMDAvcHR2Z2xvYmFsL3BsYXlsaXN0Lm0zdTg=', 'gen', 'http://shani.offshorepastebin.com/ZemLogos/ptvglobal.png'), ('STYLE 360', 'aHR0cDovL3N0cmVhbWVyNjEuZWJvdW5kc2VydmljZXMuY29tL21vYmlsZS9zdHlsZTM2MC9wbGF5bGlzdC5tM3U4', 'gen', 'http://shani.offshorepastebin.com/ZemLogos/style360.png'), ('ARY MUSIK', 'aHR0cDovL3N0cmVhbWVyMjcuZWJvdW5kc2VydmljZXMuY29tL3RlaGFtaW1la3lsMDAvYXJ5bXVzaWsvcGxheWxpc3QubTN1OA==', 'gen', 'http://shani.offshorepastebin.com/ZemLogos/arymusik.png'), ('24 NEWS HD', 'aHR0cDovL3N0cmVhbWVyMjcuZWJvdW5kc2VydmljZXMuY29tL3RlaGFtaW1la3lsMDAvY2hhbm5lbDI0cGsvcGxheWxpc3QubTN1OA==', 'gen', 'http://shani.offshorepastebin.com/ZemLogos/24newshd.png'), ('24 NEWS HD (2)', 'aHR0cDovL3N0cmVhbWVyMjcuZWJvdW5kc2VydmljZXMuY29tL3RlaGFtaW1la3lsMDAvY2hhbm5lbDI0L3BsYXlsaXN0Lm0zdTg=', 'gen', 'http://shani.offshorepastebin.com/ZemLogos/24newshd.png'), ('CITY 42', 'aHR0cDovL3N0cmVhbWVyMjcuZWJvdW5kc2VydmljZXMuY29tL3RlaGFtaW1la3lsMDAvY2l0eTQyL3BsYXlsaXN0Lm0zdTg=', 'gen', 'http://shani.offshorepastebin.com/ZemLogos/city42.png'), ('EXPRESS NEWS', 'aHR0cDovL3N0cmVhbWVyMjcuZWJvdW5kc2VydmljZXMuY29tL3RlaGFtaW1la3lsMDAvZXhwcmVzcy9wbGF5bGlzdC5tM3U4', 'gen', 'http://shani.offshorepastebin.com/ZemLogos/expressnews.png'), ('GEO NEWS', 'aHR0cDovL3N0cmVhbWVyMjcuZWJvdW5kc2VydmljZXMuY29tL3RlaGFtaW1la3lsMDAvZ2VvbmV3cy9wbGF5bGlzdC5tM3U4', 'gen', 'http://shani.offshorepastebin.com/ZemLogos/geonews.png'), ('GEO TEZ', 'aHR0cDovL3N0cmVhbWVyMjcuZWJvdW5kc2VydmljZXMuY29tL3RlaGFtaW1la3lsMDAvZ2VvdGV6ei9wbGF5bGlzdC5tM3U4', 'gen', 'http://shani.offshorepastebin.com/ZemLogos/geotez.png'), ('MOVIES 24/7-iKID', 'aHR0cDovL3N0cmVhbWVyMjcuZWJvdW5kc2VydmljZXMuY29tL3RlaGFtaW1la3lsMDAvaWtpZC9wbGF5bGlzdC5tM3U4', 'gen', 'http://shani.offshorepastebin.com/ZemLogos/movies247.png'), ('MOVIES 24/7-iMOVIE', 'aHR0cDovL3N0cmVhbWVyMjcuZWJvdW5kc2VydmljZXMuY29tL3RlaGFtaW1la3lsMDAvbW92aWUvcGxheWxpc3QubTN1OA==', 'gen', 'http://shani.offshorepastebin.com/ZemLogos/movies247.png'), ('APNA NEWS', 'aHR0cDovL3N0cmVhbWVyNjEuZWJvdW5kc2VydmljZXMuY29tL21vYmlsZS9hcG5hbmV3cy9wbGF5bGlzdC5tM3U4', 'gen', 'http://shani.offshorepastebin.com/ZemLogos/apnanews.png'), ('GEO SUPER', 'aHR0cDovL3N0cmVhbWVyMjcuZWJvdW5kc2VydmljZXMuY29tL3RlaGFtaW1la3lsMDAvZ2Vvc3VwZXIvcGxheWxpc3QubTN1OA==', 'gen', 'http://shani.offshorepastebin.com/ZemLogos/geosuper.png'), ('SPORTS', 'aHR0cDovL3N0cmVhbWVyMjcuZWJvdW5kc2VydmljZXMuY29tL3RlaGFtaW1la3lsMDAvc3BvcnRzL3BsYXlsaXN0Lm0zdTg=', 'gen', 'http://shani.offshorepastebin.com/ZemLogos/sports.png'),('Ten Sports', 'aHR0cDovL3N0cmVhbWVyMjcuZWJvdW5kc2VydmljZXMuY29tL3RlaGFtaW1la3lsMDAvdGVuc3BvcnRzL3BsYXlsaXN0Lm0zdTg=', 'gen', 'http://shani.offshorepastebin.com/ZemLogos/tensports.png')]  

    match.append(('Quran TV Urdu','aHR0cDovL2lzbDEuaXNsYW00cGVhY2UuY29tL1F1cmFuVXJkdVRW','gen',''))
    match.append(('Channel 24','cnRtcDovL2RzdHJlYW1vbmUuY29tOjE5MzUvbGl2ZS8gcGxheXBhdGg9Y2l0eTQyIHN3ZlVybD1odHRwOi8vZHN0cmVhbW9uZS5jb20vanAvandwbGF5ZXIuZmxhc2guc3dmIHBhZ2VVcmw9aHR0cDovL2RzdHJlYW1vbmUuY29tL2NpdHk0Mi9pZnJhbWUuaHRtbCB0aW1lb3V0PTIw','gen',''))
    match.append(('QTV','aHR0cDovLzE1OC42OS4yMjkuMzA6MTkzNS9BUllRVFYvbXlTdHJlYW0vcGxheWxpc3QubTN1OA==','gen',''))
    match.append(('SEE TV','cnRtcDovLzM2Nzc4OTg4Ni5yLm15Y2RuOTIubmV0LzM2Nzc4OTg4Ni9fZGVmaW5zdF8vIHBsYXlwYXRoPXNlZXR2IHN3ZlVybD1odHRwOi8vZHN0cmVhbW9uZS5jb20vanAvandwbGF5ZXIuZmxhc2guc3dmIHBhZ2VVcmw9aHR0cDovL2RzdHJlYW1vbmUuY29tL3NlZXR2L2lmcmFtZS5odG1sIHRpbWVvdXQ9MTA=','gen',''))
 
    match=sorted(match,key=lambda s: s[0].lower()   )

    #name,type,url,img
    ret_match=[]
    #h = HTMLParser.HTMLParser()
    for cname in match:
        #if cname[2]=='manual':
        #    ret_match.append((cname[0].capitalize(),'ebmode:9' ,cname[1] , cname[2]))		#name,url,mode,icon
        if cname[2]=='povee':
            ret_match.append((cname[0].capitalize(),'ebmode:93' ,cname[1] , cname[3]))		#name,url,mode,icon
        elif cname[2]=='gen':
             ret_match.append((cname[0].capitalize(),'ebmode:33' ,cname[1] , cname[3]))		#name,url,mode,icon
        #else:
        #     ret_match.append((cname[0].capitalize(),'ebmode:9' ,cname[0] , cname[1]))		#name,url,mode,icon
    return ret_match
            
   
def ColoredOpt(text = '', colorid = '', isBold = False):
    if not selfAddon.getSetting( "enablecolor")=='true': 
        return text
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
    link=link.split('<div class="title mb10">Programs')[1].split('</select>')[0]
    print link    
    match =re.findall('<optgroup label="(.*?)"', link, re.UNICODE)
    print match
    h = HTMLParser.HTMLParser()
    #'<option value="(.*?)">(.*?)<'
    #<optgroup label='(.*?)'
    for cname in match:
        addDir(ColoredOpt(cname,'ZM'),cname ,-9,'', True,isItFolder=False)
        subprogs=link.split('<optgroup label="%s"'%cname)[1].split('</optgroup>')[0]
        submatch=re.findall('<option value="(.*?)">(.*?)<', subprogs, re.UNICODE)
        for csubname in submatch:
    #		tname=cname[2]#
            addDir('    '+csubname[1],'http://www.zemtv.com'+ csubname[0] ,43,'', True,isItFolder=True)
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
    pageNumber=1
    catid=''
    if not 'loopHandler' in Fromurl:
        catid=re.findall("currentcat = (.*?);",linkfull)[0]
        Fromurl='http://www.zemtv.com/wp-content/themes/zemresponsive/loopHandler.php?pageNumber=%s&catNumber=%s'%(str(pageNumber),catid)
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

    

    match =re.findall('<div class=\"(?:teal)?.?card\">.*?<img src=\"(.*?)\".*?<a href=\"(.*?)\".*?>(.*?)<', linkfull, re.UNICODE|re.DOTALL)
    print match
    #if len(match)==0:
    #    match =re.findall('<div class="thumbnail">\s*<a href="(.*?)".*\s*<img.*?.*?src="(.*?)".* alt="(.*?)"', link, re.UNICODE)
    h = HTMLParser.HTMLParser()

    
    for cname in match:
        tname=cname[2]
        try:
            tname=h.unescape(tname).encode("utf-8")
        except:
            tname=re.sub(r'[\x80-\xFF]+', convert,tname )
        #tname=repr(tname)
        addDir(tname,cname[1] ,3,cname[0]+'|Cookie=%s'%getCookiesString(CookieJar)+'&User-Agent=Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10', True,isItFolder=False)
        
    
    pageNumber=re.findall("pageNumber=(.*?)&",Fromurl)[0]
    catid=re.findall("catNumber=(.*)",Fromurl)[0]
    
    pageNumber=int(pageNumber)+1
    Fromurl='http://www.zemtv.com/wp-content/themes/zemresponsive/loopHandler.php?pageNumber=%s&catNumber=%s'%(str(pageNumber),catid)
    addDir('Next Page' ,Fromurl ,2,'',isItFolder=True)
    #       print match

    return
    
def AddShowsFromSiasat(Fromurl):

    headers=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')]       
    link=getUrl(Fromurl, headers=headers)
    match =re.findall('<div class="threadinfo".*?<img src="(.*?)".*?href="(.*?)" id="thread_title.*?>(.*?)<', link, re.DOTALL)
    #if len(match)==0:
    #    match =re.findall('<div class="thumbnail">\s*<a href="(.*?)".*\s*<img.*?.*?src="(.*?)".* alt="(.*?)"', link, re.UNICODE)

        
    #	print link
    #	print match

    #	print match
    h = HTMLParser.HTMLParser()

    print match
    
    for cname in match:
        tname=cname[2]
        url=cname[1]
        imageurl=cname[0].replace('&amp;','&')
        try:
            tname=h.unescape(tname).encode("utf-8")
        except:
            tname=re.sub(r'[\x80-\xFF]+', convert,tname )
            
        if not url.startswith('http'):
            url='http://www.siasat.pk/forum/'+url

        if not imageurl.startswith('http'):
            url='http://www.siasat.pk/forum/'+url
            
        #tname=repr(tname)
        addDir(tname,url,3,imageurl, True,isItFolder=False)
        

    match =re.findall('title="Results.*?<a href="(.*?)" title', link, re.IGNORECASE)

    if len(match)>0:
        pageurl=match[0]
        pg=''
        try:
            if '/page' in pageurl:
                pg=pageurl.split('/page')[1].split('&')[0].split('/')[0]
        except: pass
        addDir('Next Page %s (Siasat.pk)' %pg,'http://www.siasat.pk/forum/'+pageurl ,2,'',isItFolder=True)
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
        addDir(ColoredOpt(h.unescape(cname[2].replace("Watch Now Watch ","").replace("Live, High Quality Streaming","").replace("Live &#8211; High Quality Streaming","").replace("Watch Now ","")) ,'ZM'),cname[0] ,4,cname[1],False,True,isItFolder=False)		
    return	

def PlayShowLink ( url, redirect=True ): 
    global linkType
    #	url = tabURL.replace('%s',channelName);
#    req = urllib2.Request(url)
#    req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
#    response = urllib2.urlopen(req)
#    link=response.read()
#    response.close()
    
    headers=[('User-Agent','Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')]
    iszem=True
    if 'zemtv.' in url:
        CookieJar=getZemCookieJar()
        link=getUrl(url,cookieJar=CookieJar, headers=headers)
    else:
        iszem=False
        headers=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')]
        link=getUrl(url, headers=headers)

    #	print url

    line1 = "Playing DM Link"
    time = 5000  #in miliseconds
    defaultLinkType=0 #0 youtube,1 DM,2 tunepk
    defaultLinkType=selfAddon.getSetting( "DefaultVideoType" ) 
    #	print defaultLinkType
    print "LT link is" ,linkType,defaultLinkType,redirect
    if defaultLinkType=="": defaultLinkType="0"
    # if linktype is not provided then use the defaultLinkType

    if linkType.upper()=="SHOWALL" or (linkType.upper()=="" and defaultLinkType=="4"):
        if redirect: ShowAllSources(url,link)
        return
    if linkType.upper() in ["DM","DMASLIVE"] or (linkType=="" and defaultLinkType=="0"):
    #		print "PlayDM"
        line1 = "Playing DM Link"
        xbmcgui.Dialog().notification(__addonname__,line1, __icon__ , time, False)
        #showNotification(__addonname__,line1,time  , __icon__)
    #		print link
        playURL= match =re.findall('src=["\']((?:http)?.*?(dailymotion.com).*?)["\']',link)
        if len(playURL)==0:
            line1 = "Daily motion link not found"
            xbmcgui.Dialog().notification(__addonname__,line1, __icon__ , time, False)
            if redirect: ShowAllSources(url,link)
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
        #try: 
        #    import urlresolver  
        #except: 
        #    print 'urlresolver err'
        #    traceback.print_exc(file=sys.stdout)
        #stream_url = urlresolver.HostedMediaFile(playURL).resolve()
        headers=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36')]
        html=getUrl(playURL,headers=headers)
        html = html.replace('\\', '')##

        auto = re.findall('"auto"\s*:\s*.+?"url"\s*:\s*"(.+?)"', html)
        qualities = re.findall('"(\d+?)"\s*:\s*.+?"url"\s*:\s*"(.+?)"', html)

        if auto and not qualities:
            newurl= auto[0]
        else:
            qualities = [(int(i[0]), i[1]) for i in qualities]
            qualities = sorted(qualities, key=lambda x: x[0])[::-1]##

            videoUrl = [i[1] for i in qualities]
            newurl=videoUrl[0]

        html=getUrl(newurl,headers=headers)
        stream_url= re.findall( '(http.*)',html)[-1].split('#')[0]
        stream_url=stream_url+'|Origin=http://www.dailymotion.com&Referer=http://www.dailymotion.com/embed/video/&User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'
        if linkType.upper() in ["DMASLIVE"]:
            return playipbox(stream_url)#you stingy mf
        print stream_url
        playlist.add(stream_url,listitem)
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(playlist)
        #xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
        #src="(.*?(dailymotion).*?)"
    elif  linkType.upper()=="EBOUND"  or (linkType=="" and defaultLinkType=="3"):
        line1 = "Playing Ebound Link"
        xbmcgui.Dialog().notification(__addonname__,line1, __icon__ , time, False)
    #		print "Eboundlink"
        playURL= match =re.findall(' src=["\'].*?ebound\\.tv.*?site=(.*?)&.*?date=(.*?)\\&', link)
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
            playURL=match=re.findall('src=["\'](.*?(poovee\.net).*?)["\']', link)
            
            if len(playURL)==0:
                line1 = "EBound/Povee link not found"
                xbmcgui.Dialog().notification(__addonname__,line1, __icon__ , time, False)
                
                if redirect: ShowAllSources(url,link)
                return 
            playURL=match[0][0]
            pat='<source src="(.*?)"'
            #print 'source is',playURL
            if playURL.startswith('//'): playURL='http:'+playURL
            #print playURL
            link=getUrl(playURL,cookieJar=CookieJar, headers=headers)
            #print link
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
        xbmcgui.Dialog().notification(__addonname__,line1, __icon__ , time, False)
        playURL= match =re.findall('src=["\'](.*?(vidrail\.com).*?)["\']', link)
        if len(playURL)==0:
            line1 = "Vidrail link not found"
            xbmcgui.Dialog().notification(__addonname__,line1, __icon__ , time, False)
            if redirect: ShowAllSources(url,link)
            return 

        playURL=match[0][0]
        pat='<source src="(.*?)"'
        link=getUrl(playURL,cookieJar=CookieJar, headers=headers)
        playURL=re.findall(pat, link)
        if len(playURL)==0:
            line1 = "Vidrail link not found"
            xbmcgui.Dialog().notification(__addonname__,line1, __icon__ , time, False)
            if redirect: ShowAllSources(url,link)
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
        xbmcgui.Dialog().notification(__addonname__,line1, __icon__ , time, False)
    #		print "PlayLINK"
        playURL= match =re.findall('src=[\'"](.*?(tune\.pk).*?)[\'"]', link)
        if len(playURL)==0:
            line1 = "Link.pk link not found"
            xbmcgui.Dialog().notification(__addonname__,line1, __icon__ , time, False)
            if redirect: ShowAllSources(url,link)
            return 

        playURL=match[0][0]
    #		print playURL
        playlist = xbmc.PlayList(1)
        playlist.clear()
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
        listitem.setInfo("Video", {"Title":name})
        listitem.setProperty('mimetype', 'video/x-msvideo')
        listitem.setProperty('IsPlayable', 'true')
        try: 
            import urlresolver  
        except: 
            print 'urlresolver err'
            traceback.print_exc(file=sys.stdout)
        stream_url = urlresolver.HostedMediaFile(playURL).resolve()
        stream_url=stream_url+'|Referer=%s&User-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'%playURL

    #		print stream_url
        playlist.add(stream_url,listitem)
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(playlist)
    elif  linkType.upper()=="PLAYWIRE"  or (linkType=="" and defaultLinkType=="2"):
        line1 = "Playing Playwire Link"
        xbmcgui.Dialog().notification(__addonname__,line1, __icon__ , time, False)
    #		print "Playwire"
        playURL =re.findall('src=["\'].*?(playwire).*?data-publisher-id="(.*?)"\s*data-video-id="(.*?)["\']', link)
        V=1
        if len(playURL)==0:
            playURL =re.findall('data-config="(.*?config.playwire.com.*?)"', link)
            V=2
        if len(playURL)==0:
            line1 = "Playwire link not found"
            xbmcgui.Dialog().notification(__addonname__,line1, __icon__ , time, False)
            if redirect: ShowAllSources(url,link)
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
        xbmcgui.Dialog().notification(__addonname__,line1, __icon__ , time, False)
        youtubecode= match =re.findall('<iframe.*?src=\".*?youtube.*?embed\/(.*?)\"', link,re.DOTALL| re.IGNORECASE)
        if len(youtubecode)==0:
            line1 = "Youtube link not found"
            xbmcgui.Dialog().notification(__addonname__,line1, __icon__ , time, False)
            if redirect: ShowAllSources(url,link)
            return
        youtubecode=youtubecode[0]
        uurl = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % youtubecode
    #	print uurl
        xbmc.executebuiltin("xbmc.PlayMedia("+uurl+")")

    return
    
def get_treabaAia():
    val=""
    import math
    for d in [5.6
            ,12.1
            ,7.5
            ,3.3
            ,11.8
            ,7
            ,11.6
            ,9
            ,10.7
            ,6.6
            ,3.5
            ,10.1
            ,11.8
            ,7.1
            ,11.5]:
        val +=  chr(int(math.floor(d * 10)));
    return val

#print 

def generateKey(tokenexpiry):
    import hashlib
    return hashlib.md5(tokenexpiry+get_treabaAia()).hexdigest()


def playstreamhd(url):
    import re,urllib,json
    headers=[('Referer','http://streamhdeu.com/'),('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')]

    watchHtml=getUrl(url,headers=headers)
    videframe=re.findall('"videoiframe" src="(.*?)"' ,watchHtml)[0]
    
    videoframedata=getUrl(videframe,headers=headers)
    iframe=re.findall('iframe src="(.*?)"' ,videoframedata)
    if len(iframe)>0:
        
        iframdata=getUrl(iframe[0],headers=headers)
        iframe=iframe[0]
    else:
        if 'hdcast' in videoframedata or 'static.bro' in videoframedata:
            return playHDCast(videframe, "http://streamhdeu.com/","http://streamhd.eu/")
        iframdata=videoframedata
    m3ufile=re.findall('file: "(.*?)"' ,iframdata)[0]

    PlayGen(base64.b64encode(m3ufile+'|User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'))
    return 
    
def playmamahd(url):
    import re,urllib,json
    headers=[('Referer','http://mamahd.com/index.html'),('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')]

    watchHtml=getUrl(url,headers=headers)
    videframe=re.findall('<iframe wid.*?src="(.*?)"' ,watchHtml)[0]
    watchHtml=getUrl(videframe,headers=headers)
    if 'hdcast' in watchHtml or 'static.bro' in watchHtml:
        return playHDCast(videframe, "http://mamahd.com/")
    return 
    
def playzenga(url,progress):
    import re,urllib,json
    listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )

    playurl=''
    try:
        progress.update( 30, "", "getting links", "" )
        headers=[('Referer','http://www.zengatv.com/'),('User-Agent','Mozilla/5.0 (iPhone; CPU iPhone OS 9_0_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13A452 (5215161440)')]
        
        jsfile=getUrl(base64.b64decode('aHR0cDovL2FkYS56ZW5nYXR2LmNvbS9jb250cm9sbGVycy9MaXZlUGxheWVyQ29udHJvbGxlci5qcw=='),headers=headers)
        reg= "var dvrid.*?\s.*?\"(http.*)\"\s"
        
        churl=re.findall(reg,jsfile)[0]
        churl=churl.replace('" + dvrid + "',url)
        headers=[('Referer','http://www.zengatv.com/'),('Origin','www.zengatv.com/'),('User-Agent','Mozilla/5.0 (iPhone; CPU iPhone OS 9_0_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13A452 (5215161440)')]
        xmlfile=getUrl(churl,headers=headers)
        reg= "(http.*?)\]?\]?>"
        m3uurl=re.findall(reg,xmlfile)[0]
        
        playurl=m3uurl+'|User-Agent=Mozilla/5.0 (iPhone; CPU iPhone OS 9_0_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13A452 (5215161440)&Referer=http://www.zengatv.com/'
        try:
            import urlparse
            m3u8res=getUrl(playurl)
            m38uurl=re.findall('#EXT-X-STREAM-INF.*\n(.*)',m3u8res)[-1]
            suburl=urlparse.urljoin(m3uurl,m38uurl)
            progress.update( 40, "", "skipping Ads", "" )
            subdata=getUrl(suburl+'|User-Agent=Mozilla/5.0 (iPhone; CPU iPhone OS 9_0_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13A452 (5215161440)&Referer=http://www.zengatv.com/')
            playurl=suburl+'|User-Agent=Mozilla/5.0 (iPhone; CPU iPhone OS 9_0_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13A452 (5215161440)&Referer=http://www.zengatv.com/'
            print subdata
            lnum=0
            if 1==2:
                for tsurl in re.findall('#EXTINF.*\n(.*)',subdata):
                    subtsurl=urlparse.urljoin(suburl,tsurl)
                    lnum+=1
                    progress.update( 40+(10*lnum), "", "skipping Ads", "" )
                    getUrl(subtsurl+'|User-Agent=Mozilla/5.0 (iPhone; CPU iPhone OS 9_0_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13A452 (5215161440)&Referer=http://www.zengatv.com/')
            progress.update( 95, "", "alomost finished", "" )    
        except:
            print 'error avoiding ad'
            print traceback.print_exc(file=sys.stdout)
        #downloadm3u8(playurl)
    except: 
        traceback.print_exc(file=sys.stdout)
        playurl=''
    progress.close()
    xbmc.Player().play( playurl, listitem)
        


def getTVPCookieJar(updatedUName=False):
    cookieJar=None
    print 'updatedUName',updatedUName
    try:
        cookieJar = cookielib.LWPCookieJar()
        if not updatedUName:
            cookieJar.load(TVPCOOKIEFILE,ignore_discard=True)
    except: 
        cookieJar=None

    if not cookieJar:
        cookieJar = cookielib.LWPCookieJar()
    return cookieJar
    
def performTVPLogin():
    cookieJar = cookielib.LWPCookieJar()
    try:
        
        url="https://tvplayer.com/account"
        username=selfAddon.getSetting( "tvpusername" ) 
        if username=="": return False,cookieJar
        pwd=selfAddon.getSetting( "tvppwd" ) 
        lasstusername=selfAddon.getSetting( "lasttvpusername" )
        lasstpwd=selfAddon.getSetting( "lasttvppwd" )         
        cookieJar=getTVPCookieJar(lasstusername!=username or lasstpwd!= pwd)
        mainpage = getUrl(url,cookieJar=cookieJar)
        

        if 'Login to TVPlayer' in mainpage:
            token   = urllib.unquote(re.findall('name="token" value="(.*?)"' ,mainpage)[0])
            print 'LOGIN NOW'
            url="https://tvplayer.com/account/login"
            headers=[('Referer',"https://tvplayer.com/account/login"),('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'),('Origin','https://tvplayer.com')]           
            post = {'email':username,'password':pwd,'token':token}
            post = urllib.urlencode(post)
            mainpage = getUrl(url,cookieJar=cookieJar,post=post,headers=headers )
            cookieJar.save (TVPCOOKIEFILE,ignore_discard=True)
            selfAddon.setSetting( id="lasttvpusername" ,value=username)
            selfAddon.setSetting( id="lasttvppwd" ,value=pwd)
        
        return not '>Login</a>' in mainpage,cookieJar
    except: 
            traceback.print_exc(file=sys.stdout)
    return False,cookieJar
    
def playtvplayer(url):
    import re,urllib,json
    listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )

    playurl=''
    try:
        loginstatus,cj=performTVPLogin()
        watchHtml=getUrl(url, cookieJar=cj)
        channelid=re.findall('data-resource="(.*?)"' ,watchHtml)[0]
        #token=re.findall('var validate = "(.*?)"' ,watchHtml)[0]
        token='null'
        try:
            token=re.findall('data-token="(.*?)"' ,watchHtml)[0]
        except: pass
        
        contextjs=getUrl("https://tvplayer.com/watch/context?resource=%s&nonce=%s"%(channelid,token), cookieJar=cj)   
        contextjs=json.loads(contextjs)
        validate=contextjs["validate"]
        #cj = cookielib.LWPCookieJar()
        data = urllib.urlencode({'service':'1','platform':'chrome','validate':validate ,'id' : channelid})
        headers=[('Referer','https://tvplayer.com/watch/'),('Origin','http://tvplayer.com'),('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')]
        retjson=getUrl("http://api.tvplayer.com/api/v2/stream/live",post=data, headers=headers,cookieJar=cj);
        jsondata=json.loads(retjson)
    #    print cj
        #cj = cookielib.LWPCookieJar()
        playurl1=jsondata["tvplayer"]["response"]["stream"]
        m3utext=getUrl(playurl1, headers=headers,cookieJar=cj);
        #playurl1=re.findall('(http.*)',m3utext)[-1]
        playurl=playurl1+'|Cookie=%s&User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36&X-Requested-With=ShockwaveFlash/22.0.0.209&Referer=https://tvplayer.com/watch/'%getCookiesString(cj)
        
    except: 
        traceback.print_exc(file=sys.stdout)
        playurl=''
    if playurl=='' or not tryplay(playurl+'|Cookie=%s&User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36&X-Requested-With=ShockwaveFlash/22.0.0.209&Referer=https://tvplayer.com/watch/'%getCookiesString(cj),listitem):
        playtvplayerfallback(url)
    return 
    
def playtvplayerfallback(url):
    import re,urllib,json
    watchHtml=getUrl(url.replace('/watch/','/watch/fallback/'))
    channelid=re.findall('var initialChannelId = "(.*?)"' ,watchHtml)[0]
    hashval=urllib.unquote(re.findall('hash = "(.*?)"' ,watchHtml)[0])
    expval=re.findall('exp = "(.*?)"' ,watchHtml)[0]
    keyval=generateKey(expval)
    cj = cookielib.LWPCookieJar()
    data = urllib.urlencode({'id' : channelid})
    headers=[('Token-Expiry',expval) ,('Hash',hashval),('Key',keyval),('Referer','http://assets.tvplayer.com/web/flash/tvplayer/TVPlayer-DFP-3.swf'),('X-Requested-With','ShockwaveFlash/22.0.0.209')]
    retjson=getUrl("http://live.tvplayer.com/stream-web-encrypted.php",post=data, headers=headers,cookieJar=cj);
    jsondata=json.loads(retjson)
#    print cj
    playurl=jsondata["tvplayer"]["response"]["stream"]
    listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )

    return tryplay(playurl+'|Cookie=%s&User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36&X-Requested-With=ShockwaveFlash/22.0.0.209&Referer=https://tvplayer.com/watch/'%getCookiesString(cj),listitem)
    
    
def ShowAllSources(url, loadedLink=None):
    global linkType
    #print 'show all sources',url
    link=loadedLink
    if not loadedLink:
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
    available_source=[]
    playURL =re.findall('src=".*?(playwire).*?data-publisher-id="(.*?)"\s*data-video-id="(.*?)"', link)
    
    if not len(playURL)==0:
        available_source.append('Playwire Source')

    playURL =re.findall('data-config="(.*?config.playwire.com.*?)"', link)
    #	print 'playURL',playURL
    if not len(playURL)==0:
        available_source.append('Playwire Source')

    playURL =re.findall('src=["\'](.*?ebound\\.tv.*?)["\']', link)
    #	print 'playURL',playURL
    if not len(playURL)==0:
        available_source.append('Ebound Source')		
    else:
        playURL =re.findall('src=["\'](.*?poovee\.net.*?)["\']', link)
        if not len(playURL)==0:
            available_source.append('Ebound Source')		
        
    playURL= match =re.findall('src=["\'](.*?(dailymotion).*?)["\']',link)
    if not len(playURL)==0:
        available_source.append('Daily Motion Source')

    playURL= match =re.findall('src=["\'](.*?(vidrail\.com).*?)["\']',link)
    if not len(playURL)==0:
        available_source.append('Vidrail Source')
        
    playURL= match =re.findall('src=[\'"](.*?(tune\.pk).*?)[\'"]', link)
    if not len(playURL)==0:
        available_source.append('Link Source')

    
    playURL= match =re.findall('<iframe.*?src=\".*?youtube.*?embed\/(.*?)\"', link,re.DOTALL| re.IGNORECASE)
    #print 'playURL uyoutube',playURL
    if not len(playURL)==0:
        available_source.append('Youtube Source')

    if len(available_source)>0:
        if len(available_source)==1:
            linkType=available_source[0].replace(' Source','').replace('Daily Motion','DM').upper()
            PlayShowLink(url, redirect=False);
        else:    
            dialog = xbmcgui.Dialog()
            index = dialog.select('Choose your stream', available_source)
            if index > -1:
                linkType=available_source[index].replace(' Source','').replace('Daily Motion','DM').upper()

                PlayShowLink(url);
def findInDic(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return dic
    return None
def PlayDittoLive(url):
    progress = xbmcgui.DialogProgress()
    progress.create('Progress', 'Fetching Streaming Info')
    progress.update( 10, "", "Finding links..", "" )

    req = urllib2.Request(url)
    req.add_header('Referer', base64.b64decode('aHR0cDovL29yaWdpbi5kaXR0b3R2LmNvbS8='))
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    #pro_reg='class="live-program-id" value="(.*?)"'
    pl_reg='window.pl_data = (\{.*?"key":.*?\}\})'
    #videoid=re.findall(pro_reg, link)[0]
    videoid=url.split('/')[-1]
    playdata=re.findall(pl_reg, link)[0]

    
    progress.update( 50, "", "Finding links..", "" )
    try:
        #print videoid
        #print 'string data',playdata
        playdata=playdata.replace('null','None')
        playdata=playdata.replace('false','False')
        playdata=playdata.replace('true','True')
        playdata=eval(playdata)

        vobject=findInDic(playdata["live"]["channel_list"], 'videoid',videoid)
        #print vobject
        url=vobject["file"]
        if not (url.startswith('http') or url.startswith('rtmp')):
            import pyaes
            url=url.decode("base64")
            key=playdata["live"]["key"].decode("base64")
    
            de = pyaes.new(key, pyaes.MODE_CBC, IV='\0'*16)
            url =de.decrypt(url).replace('\x00', '').split('\0')[0]
            url=re.sub('[^\s!-~]', '', url)
            print url
            playfile=url+'|User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36&Referer=http://origin.dittotv.com/livetv/zee-tv-uk'
        #import json
        #data=json.loads(link)
        #playfile=data["link"]+'|User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36&Referer=http://www.dittotv.com/index.php?r=live-tv/link'#+urllib.unquote(url)
    except:
        traceback.print_exc(file=sys.stdout)
        #playlink=re.findall('source type="application/x-mpegurl"  src="(.*?)"',link)[0]
        #playfile=playlink+'|User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36&Referer=http://www.dittotv.com/index.php?r=live-tv/link'#+urllib.unquote(url)
#    playfile =url+'?wmsAuthSign='+link+'|User-Agent=AppleCoreMedia/1.0.0.13A452 (iPhone; U; CPU OS 9_0_2 like Mac OS X; en_gb)'
    progress.update( 100, "", "Almost done..", "" )
    listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
    xbmc.Player(  ).play( playfile, listitem)
    return      
def PlayCFLive(url):
    progress = xbmcgui.DialogProgress()
    progress.create('Progress', 'Fetching Streaming Info')
    progress.update( 10, "", "Finding links..", "" )

    try:
        #headers=[('User-Agent','Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')]
        opener = urllib2.build_opener(NoRedirection)
        opener.addheaders = [('User-agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')]
        response = opener.open('https://cinefuntv.com/watchnow.php?content='+url)
        html= response.read();#getUrl('https://cinefuntv.com/watchnow.php?content='+url,headers=headers)
        #print html
        playfile=re.findall('var cms_url = [\'"](.*?)[\'"]', html)[0]+'|User-Agent=Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10'
    except: 
        traceback.print_exc(file=sys.stdout)
        playfile=''
        
    if playfile=='':
        req = urllib2.Request(base64.b64decode('aHR0cHM6Ly9jaW5lZnVudHYuY29tL3NtdGFsbmMvY29udGVudC5waHA/Y21kPWRldGFpbHMmQCZkZXZpY2U9aW9zJnZlcnNpb249MCZjb250ZW50aWQ9JXMmc2lkPSZ1PWt3cDMwNjcwQHJjYXNkLmNvbQ==')%url)
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
    
def PlayPoveeLink(url):

    progress = xbmcgui.DialogProgress()
    progress.create('Progress', 'Fetching Streaming Info')
    progress.update( 10, "", "Finding links..", "" )
    link=getUrl('http://poovee.net/embed/%s/?autoplay=0'%url)
    progress.update( 50, "", "Finding links..", "" )
    url=re.findall('videosrc :"(.*?)"' ,link)[0]
    playfile =url+'|User-Agent=iPhone'
    progress.update( 100, "", "Almost done..", "" )
    progress.close()
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

    playfile =url+'?wmsAuthSign='+link+'|User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
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

print params
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
    elif mode==29:
        print "Ent url is ",name,url        
        AddtypesForShows()
        
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
    elif mode==7 :
        print "Play url is "+url
        ShowStatus(url)        
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
    elif mode in [36] :
        print "Play url is "+url
        if not 'emovies:' in url:
            AddPv2Sports(url) 
        else:
            AddEmoviesMain(url)
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
    elif mode in [56,156]  :
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
    elif mode==72:
        print "Play url is "+url
        AddSafeLang(url)  
    elif mode==73:
        print "Play url is "+url
        AddSafeChannels(url)  
    elif mode==74:
        print "Play url is "+url
        AddTVPlayerChannels(url)        
    elif mode==75:
        print "Play url is "+url
        #tst()
        AddStreamHDCats(url)  
    elif mode==76:
        print "Play url is "+url
        AddStreamHDChannels(url)
    elif mode==77:
        print "Play url is "+url
        AddHDFreeChannels(url)    
    elif mode==78:
        print "Play url is "+url
        AddInfiniteChannels(url)               
    elif mode==79:
        print "Play url is "+url
        AddMAMAHDChannels(url)               
    elif mode==80:
        print "Play url is "+url
        import time        
        try:
            if RefreshResources([('live365.py','http://shani.offshorepastebin.com/live365.py?t=%s'%str(int(time.time())),True)]):
                dialog = xbmcgui.Dialog()
                ok = dialog.ok('XBMC', 'Updated files! Try click Refresh Listing to see if it works')   
            else:
                dialog = xbmcgui.Dialog()
                ok = dialog.ok('XBMC', 'Not updated, perhaps no change?')  
                print 'Updated files'
        except: traceback.print_exc(file=sys.stdout)
    elif mode==81:
        print "Play url is "+url
        AddEuroStreamChannels(url)      
    elif mode==82:
        print "Play url is "+url
        AddMyTVSports(url)            
    elif mode==83:
        print "Play url is "+url
        AddIndianPakShowsCat(url)
    elif mode==84:
        print "Play url is "+url
        AddIndianPakShows(url)  
    elif mode==85:
        print "Play url is "+url
        AddIndianPakShowsEP(url)  
    elif mode==86:
        print "Play url is "+url
        AddFootballCats(url)        
    elif mode==87:
        print "Play url is "+url
        AddFootballMatches(url)       
    elif mode==88:
        print "Play url is "+url        
        AddFootballVideos(url)
    elif mode==89:
        print "Play url is "+url
        AddFootballMatcheHome(url)         
    elif mode==91:
        print "Play url is "+url
        PlayFootballVideo(url)            
    elif mode==92:
        print "Play url is "+url
        AddFastSport(url)  
    elif mode==93:
        print "Play url is "+url
        PlayPoveeLink(url)           
    elif mode==94:
        print "Play url is "+url
        AddNetworkTVSports(url)  
    elif mode==95:
        print "Play url is "+url
        dialog = xbmcgui.Dialog()
        ok = dialog.ok('PLEASE SAVE ME!!!!', 'If it stops playing after 2 minutes please oh please remember that you must visit their site and play a video/click on live links.\nYou can use any devices/mobile to visit their site http;//sport365.live, just make sure you are connected to the same network.')          
    elif mode==96:
        print "Play url is "+url
        AddNetworkTVSports2(url,apptype=1)  
    elif mode==98:
        print "Play url is "+url
        AddNetworkTVSports2(url,apptype=2)  
    elif mode==97:
        print "Play url is "+url
        import time        
        try:
            if RefreshResources([('scdec.py','https://offshoregit.com/Shani-08/main/plugin.video.ZemTV-shani/scdec.py?t=%s'%str(int(time.time())),True)]):
                dialog = xbmcgui.Dialog()
                ok = dialog.ok('XBMC', 'Updated files! Try click Refresh Listing to see if it works')   
            else:
                dialog = xbmcgui.Dialog()
                ok = dialog.ok('XBMC', 'Not updated, perhaps no change?')  
                print 'Updated files'
        except: traceback.print_exc(file=sys.stdout)
    elif mode==99 :
        print "Play url is 57"+url
        AddTestChannels(url)           
        
        
except:

    print 'somethingwrong'
    traceback.print_exc(file=sys.stdout)
VIEW_MODES = {
    'thumbnail': {
        'skin.confluence': 500,
        'skin.aeon.nox': 551,
        'skin.confluence-vertical': 500,
        'skin.jx720': 52,
        'skin.pm3-hd': 53,
        'skin.rapier': 50,
        'skin.simplicity': 500,
        'skin.slik': 53,
        'skin.touched': 500,
        'skin.transparency': 53,
        'skin.xeebo': 55,
    },
}

def get_view_mode_id( view_mode):
    default_view_mode=selfAddon.getSetting( "usethisviewmode" )
    if default_view_mode=="":
        view_mode_ids = VIEW_MODES.get(view_mode.lower())
        if view_mode_ids:
            return view_mode_ids.get(xbmc.getSkinDir())
    else:
        return int(default_view_mode)
    return None

playmode=[3,4,9,11,15,21,22,27,33,35,37,40,42,45,91,93,95]
nonthumbview=[55,61,67,56,14,57,19,20,21,22,23,24,79,75,76,78,81,2,51,52,53,62,70,71,81,66,94]
try:
    if (not mode==None) and mode>1 and mode not in nonthumbview and mode not in playmode:
        view_mode_id = get_view_mode_id('thumbnail')
        if overridemode: view_mode_id=overridemode
        if view_mode_id is not None:
            print 'view_mode_id',view_mode_id
            xbmc.executebuiltin('Container.SetViewMode(%d)' % view_mode_id)
except: traceback.print_exc(file=sys.stdout)

if not  (mode in  playmode ):
    if mode in [144,156]:
        xbmcplugin.endOfDirectory(int(sys.argv[1]),updateListing=True)
    else:
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

        
        
