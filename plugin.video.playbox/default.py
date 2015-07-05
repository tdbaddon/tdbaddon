import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os

import json


ADDON = xbmcaddon.Addon(id='plugin.video.playbox')
art= "%s/art/"%ADDON.getAddonInfo("path")


API='http://playboxhd.com/api/box?'


if ADDON.getSetting('kidmode')=='true':
    KID ='1'
else:
    KID ='0'

    
def GetStream(url):
    from lib import pyaes as pyaes
    import base64

    decrypter = pyaes.Decrypter(pyaes.AESModeOfOperationCBC(base64.urlsafe_b64decode('cXdlcnR5dWlvcGFzZGZnaGprbHp4YzEyMzQ1Njc4OTA='), '\0' * 16))
    url = base64.decodestring(url)
    url = decrypter.feed(url) + decrypter.feed()
    return url


def CATEGORIES():
    addDir('Search','movie',8,art+'search.png','')            
    addDir('Movies','movie',1,'','')
    addDir('Tv Shows','show',1,'','')
    addDir('Cartoons','cartoon',1,'','')
    addDir('Genre','listcat',7,'','')
    addDir('Todays Lists','list',5,'','')
    setView('movies', 'default')       
       
                                                                      
def GetContent(url):
    PAGE= 1
    print url
    if not 'list' in url:
        if not 'catid' in url:
            name=['popular','new']
            GRRR=['Popular','New']
            action= name[xbmcgui.Dialog().select('Please Choose Preference', GRRR)]
                 #type=popular&t=movie&catid=0&page=1&os=Android&v=1.0&k=0&al=key
            new_url = API+'type=%s&t=%s&catid=0&os=Android&v=1.0&k=%s&al=key' % (action,url,KID)+'&page='
        else:new_url=url   
    else:new_url=url
    try:link = json.loads(OPEN_URL(new_url+str(PAGE)))
    except:return PlayBoxFucker()


    data=link['data']
    for field in data['films']:
        name=field['title'].encode('utf8')
        url=str(field['id'])
        iconimage=field['poster']
        addDir(name,url,3,iconimage,'')
        
    addDir('[COLOR blue][B]Next Page >>[/B][/COLOR]',new_url,2,art+'nextpage.png','1')
    setView('movies', 'movies')


def Genre(url):
    new_url = API+'type=%s&catid=0&os=Android&v=1.0&k=%s&al=key' % (url,KID)
    
    try:link = json.loads(OPEN_URL(new_url))
    except:return PlayBoxFucker()


    data=link['data']
    for field in data:
        name=field['name'].encode('utf8')
        url=str(field['id'])
        URL='http://playboxhd.com/api/box?type=popular&t=movie&catid=%s&page=1&os=Android&v=1.0&page=' % url
        addDir(name,URL,1,'','')
        

    setView('movies', 'default')    

def SEARCHPLAYBOX(url):
    search_entered = ''
    keyboard = xbmc.Keyboard(search_entered, 'Search PlayBox')
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_entered = keyboard.getText() .replace(' ','+')    
    new_url = API+'type=search&os=Android&v=2.0.1&k=0&keyword=%s' % search_entered

    
    try:link = json.loads(OPEN_URL(new_url))
    except:return PlayBoxFucker()


    data=link['data']
    for field in data['films']:
        name=field['title'].encode('utf8')
        url=str(field['id'])
        iconimage=field['poster']
        addDir(name,url,3,iconimage,'')

    setView('movies', 'movies')


def TodayList(url):
    
    new_url = 'http://playboxhd.com/api/box?t=box&type=list&os=Android&v=1.0&k=%s&al=key' % KID
    try:link = json.loads(OPEN_URL(new_url))
    except:return PlayBoxFucker()


    data=link['data']
    for field in data:
        name=field['title'].encode('utf8')
        url=str(field['id'])
        iconimage=field['image']
        addDir(name,url,6,iconimage,'')
    setView('movies', 'movies')


def TodayListGetContent(url):
    PAGE= 1
    new_url = 'http://playboxhd.com/api/box?type=detail&t=box&id=%s&os=Android&v=1.0&k=%s&al=key' % (url,KID)+'&page='

    try:link = json.loads(OPEN_URL(new_url+str(PAGE)))
    except:return PlayBoxFucker()


    data=link['data']
    for field in data['films']:
        name=field['title'].encode('utf8')
        url=str(field['id'])
        iconimage=field['poster']
        addDir(name,url,3,iconimage,'')
        
    addDir('[COLOR blue][B]Next Page >>[/B][/COLOR]',new_url,2,art+'nextpage.png','1')
    setView('movies', 'movies')    
    

def GetNextPageContent(url,iconimage,page):
   
    PAGE=int(page)+1
    new_url = url+str(PAGE)

    try:link = json.loads(OPEN_URL(new_url))
    except:return PlayBoxFucker()

    data=link['data']

    for field in data['films']:
        name=field['title'].encode('utf8')

        url=str(field['id'])
        iconimage=field['poster']
        addDir(name,url,3,iconimage,'')
        
    addDir('[COLOR blue][B]Next Page >>[/B][/COLOR]',new_url,2,art+'nextpage.png',str(PAGE))     
    setView('movies', 'movies')
    
def PlayBoxFucker():
    d = xbmcgui.Dialog()
    d.ok('Playbox HD', 'No Response From Playbox Server')

    
 


def OPEN_URL(url):
    import utils
    return utils.GetHTML(url)


def GetDetail(name,url,iconimage):
    
    NAME=name
    ID=url
    
    new_url = 'http://playboxhd.com/api/box?type=detail&id=%s&os=Android&v=1.0&k=%s&al=key' % (url,KID)

    try:link = json.loads(OPEN_URL(new_url))
    except:return PlayBoxFucker()

    data=link['data']['chapters']
    if len(data)>1: 
        for field in data:
            name=field['title'].encode('utf8')
            url=str(field['id'])
            addDir(name.replace('E0','E'),url,4,iconimage,NAME + ' '+name.replace('E0','E'))
    else:
        for field in data:
            ID=str(field['id'])
            continue
        new_url = 'http://playboxhd.com/api/box?type=stream&id=%s&os=Android' % ID

        try:link = json.loads(OPEN_URL(new_url))
        except:return PlayBoxFucker()

        data=link['data']
      
        for field in data:
            name=field['server'].encode('utf8').upper()+' '+field['quality']
            url=str(field['stream'])
            
            name=name.replace('GGVIDEO','GOOGLEVIDEO')
            if ('720p' in name) or ('1080' in name):
                name=name.replace('720p','[COLOR green]720P[/COLOR]').replace('1080p','[COLOR green]1080P[/COLOR]')         
            addDir(name,url,200,iconimage,str(NAME))

   
def GetStreamLinks(url,iconimage,name,page):
    NAME=page
    new_url = 'http://playboxhd.com/api/box?type=stream&id=%s&os=Android' % url

    try:link = json.loads(OPEN_URL(new_url))
    except:return PlayBoxFucker()

    data=link['data']
  
    for field in data:
        name=field['server'].encode('utf8').upper()+' '+field['quality']
        url=str(field['stream'])
        name=name.replace('GGVIDEO','GOOGLEVIDEO')
        if ('720p' in name) or ('1080' in name):
            name=name.replace('720p','[COLOR green]720P[/COLOR]').replace('1080p','[COLOR green]1080P[/COLOR]')
        addDir(name,url,200,iconimage,NAME)

        
    
def OPEN_URLS(url):
    req = urllib2.Request(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36'})
    con = urllib2.urlopen( req )
    link= con.read()
    return link


def nowvideo(url):
    link=OPEN_URLS(url)
    match=re.compile('<source src="(.+?)"').findall(link)[0]
    return match


def anime(url):
    link=OPEN_URLS(url.replace('at/t','at/nw'))
    match=re.compile('_url = "(.+?)"').findall(link)[0]
    return urllib.unquote(match)


def thevideos(url):
    link=OPEN_URLS(url)
    match=re.compile('file:"(.+?)"').findall(link)
    last=len(match)-1
    return match[last]
    
def PLAY_STREAM(name,url,iconimage,page):
    STREAM=GetStream(url)
    print STREAM
    if 'google' in STREAM:
        STREAM_URL=STREAM

    elif 'ANIME' in name:
        STREAM_URL=anime(STREAM)
        
    else:
        import urlresolver
        #STREAM=STREAM.replace('/mobile','').replace('?id=','?v=').replace('video.php','embed.php')
        
        if '<IFRAME SRC=' in STREAM:
            STREAM=re.compile('<IFRAME SRC="(.+?)"').findall(STREAM)[0]
        if 'nowvideo' in STREAM:
            STREAM_URL=  nowvideo(STREAM)
        elif 'thevideos.tv' in STREAM:
            STREAM_URL=  thevideos(STREAM)            
        else:    
            STREAM_URL=urlresolver.resolve(STREAM)
      
    liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
    liz.setInfo(type='Video', infoLabels={'Title':page})
    liz.setProperty("IsPlayable","true")
    liz.setPath(STREAM_URL)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)


    
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

def addDir(name,url,mode,iconimage,page):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&page="+urllib.quote_plus(page)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name} )
        menu = []
        if mode ==200:
            liz.setProperty("IsPlayable","true")
            
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            menu.append(('Play All Videos','XBMC.RunPlugin(%s?name=%s&mode=2001&iconimage=None&url=%s)'% (sys.argv[0],name,url)))
            liz.addContextMenuItems(items=menu, replaceItems=False)
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
        
 
        
def setView(content, viewType):
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
        if ADDON.getSetting('auto-view') == 'true':#<<<----see here if auto-view is enabled(true) 
                xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )#<<<-----then get the view type
                      
               
params=get_params()
url=None
name=None
mode=None
iconimage=None
page=None


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
        page=urllib.unquote_plus(params["page"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)
   
        
#these are the modes which tells the plugin where to go
if mode==None or url==None or len(url)<1:
        
        CATEGORIES()
       
elif mode==1:
        
        GetContent(url)

elif mode==2:
        
        GetNextPageContent(url,iconimage,page)

elif mode==3:
        
        GetDetail(name,url,iconimage)

elif mode==4:
      
        GetStreamLinks(url,iconimage,name,page)

elif mode==5:
       
        TodayList(url)


elif mode==6:
        
        TodayListGetContent(url)

elif mode==7:
        
        Genre(url)

elif mode==8:
        
        SEARCHPLAYBOX(url)         
        
elif mode==200:

        PLAY_STREAM(name,url,iconimage,page)

elif mode==2001:

        playall(name,url)        
       
xbmcplugin.endOfDirectory(int(sys.argv[1]))
