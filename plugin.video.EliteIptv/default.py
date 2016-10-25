import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os
import datetime
import time
import net

from threading import Timer
import json



PLUGIN='plugin.video.EliteIptv'
ADDON = xbmcaddon.Addon(id=PLUGIN)
SETTINGS = xbmc.translatePath(os.path.join(ADDON.getAddonInfo('profile'),'settings.xml'))
image='http://offsidestreams.com/'

auth=ADDON.getSetting('authtoken')

USER='[COLOR yellow]'+ADDON.getSetting('user')+'[/COLOR]'
THESITE='offsidestreams.com'

UA='XBMC'

net=net.Net()


                

def OPEN_URL(url):
    req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
    con = urllib2.urlopen( req )
    link= con.read()
    return link

def EXIT():
        xbmc.executebuiltin("XBMC.Container.Update(path,replace)")
        xbmc.executebuiltin("XBMC.ActivateWindow(Home)")
    
    
if ADDON.getSetting('user')=='':
    dialog = xbmcgui.Dialog()
    if dialog.yesno(THESITE.upper(), "If You Dont Have An Account", "Please Sign Up At",THESITE.upper(),"Exit","Carry On"):
        
        dialog.ok(THESITE.upper(), "You Now Need To Input", "Your [COLOR yellow]Username[/COLOR]")
        search_entered = ''
        keyboard = xbmc.Keyboard(search_entered, THESITE.upper())
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_entered = keyboard.getText() 
        ADDON.setSetting('user',search_entered)
        
        dialog.ok(THESITE.upper(), "You Now Need To Input", "Your [COLOR yellow]Password[/COLOR]")
        search_entered = ''
        keyboard = xbmc.Keyboard(search_entered, THESITE.upper())
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_entered = keyboard.getText() 
        ADDON.setSetting('pass',search_entered)
        ADDON.setSetting('login_time','2000-01-01 00:00:00')
    else:
        EXIT()
    
site='http://'+THESITE+'/live-tv/'


datapath = xbmc.translatePath(ADDON.getAddonInfo('profile'))
cookie_path = os.path.join(datapath, 'cookies')
cookie_jar = os.path.join(cookie_path, THESITE+".lwp")
channeljs=os.path.join(cookie_path, "channels.js")
world=os.path.join(datapath, "world")


   
def KICKOUT():
        dialog = xbmcgui.Dialog()
        dialog.ok("Please Check Your Details & Try Again", "Username : "+ADDON.getSetting('user'), "Password : "+ ADDON.getSetting('pass'), "[COLOR red]is Wrong Please Sign up @ "+THESITE.upper()+"[/COLOR]")
        ADDON.setSetting('user','')
        ADDON.setSetting('pass','')
        os.remove(SETTINGS)
        try:
            os.remove(cookie_jar)
        except:
            pass
        EXIT()

def LOGOUT():
    net.set_cookies(cookie_jar)
    html = net.http_GET(site).content
    match=re.compile(' href="(.+?)">Log Out</a>').findall(html)[0]
    net.set_cookies(cookie_jar)
    logout = net.http_GET(match.replace('#038;','')).content
    if 'You are now logged out' in logout:
        print '===============LOGGED OUT !!==============='
        dialog = xbmcgui.Dialog()
        dialog.ok(THESITE.upper(),'', "You Are Now Logged Out", "")
        EXIT()
        
    
    

def Login():
    print '###############    LOGIN   #####################'
    loginurl = 'http://'+ THESITE +'/login/login/'
    username = ADDON.getSetting('user')
    password = ADDON.getSetting('pass')

    data     = {'password': password,
                                            'email': username,
                                            'action': 'go','return':'/channels/'}
    headers  = {'Host':THESITE,
                                            'Origin':'http://'+THESITE,
                                            'Referer':'http://'+THESITE+'/channels/',
                                            'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36',
                                            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                                            'Accept-Encoding':'gzip, deflate',
                                            'Accept-Language':'en-US,en;q=0.8',
                                            'Cache-Control':'max-age=0',
                                            'Connection':'keep-alive',
                                                    'Content-Type':'application/x-www-form-urlencoded'}
    html = net.http_POST(loginurl, data, headers).content
    if 'Lost your password</a>' in html:
        KICKOUT()
    else:
        if os.path.exists(cookie_path) == False:
                os.makedirs(cookie_path)
        net.save_cookies(cookie_jar)

        net.set_cookies(cookie_jar)
        a=net.http_GET('http://'+THESITE+'/api/matrix/channels',headers={'User-Agent' :UA}).content
        f = open(channeljs, mode='w')
        f.write(a)
        f.close()



def parse_date(dateString):
    import time
    return datetime.datetime.fromtimestamp(time.mktime(time.strptime(dateString.encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S")))


def sessionExpired():
    try:
        a=open(cookie_jar).read()
        expiry=re.compile('expires="(.+?)"').findall(a)[0]
        expiry=expiry [0:len(expiry)-1]
    except:
        expiry='2000-01-01 00:00:00'


    now        = datetime.datetime.today()
 
    
    prev = parse_date(expiry)


    return (now > prev)



def server():
    try:
        a = open(channeljs).read()
        print 'LOCAL READ'
    except:
        net.set_cookies(cookie_jar)
        a = net.http_GET('http://'+THESITE+'/MatrixUp/site/api/matrix/channels',headers={'User-Agent' :UA}).content
    return a

def cleanHex(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == "&#x": return unichr(int(text[3:-1], 16)).encode('utf-8')
        else: return unichr(int(text[2:-1])).encode('utf-8')
    return re.sub("(?i)&#\w+;", fixup, text.decode('ISO-8859-1').encode('utf-8'))

def CATEGORIES():
    if sessionExpired():
        Login()
    if os.path.exists(cookie_jar) == True:
        try:
            import random
            text=''
            twit = 'http://twitrss.me/twitter_user_to_rss/?user=@offsidesupport'
            link = OPEN_URL(twit)
            
            match=re.compile("<description><!\[CDATA\[(.+?)\]\]></description>",re.DOTALL).findall(link)
            status = cleanHex(match[0])
            addDir('[COLOR blue]***[/COLOR] [COLOR yellow]'+THESITE.upper()+' STATUS[/COLOR] [COLOR blue]***[/COLOR] - [COLOR orange]'+status.strip()+'[/COLOR]','url','','','','','')
        except:pass            
    net.set_cookies(cookie_jar)
    try:
        link = json.loads(server())
    except:
        os.remove(cookie_jar)
        Login()
        link = json.loads(server())
    if ADDON.getSetting('genre')=='true':
        uniques=[]
        uniquesurl=[]
        data=link['categories']
        ret = ''
        for j in data:
            url = j
            name = data[j].encode("utf-8")       
            if name not in uniques:
                uniques.append(name)
                uniquesurl.append(url)
                addDir(name,url,4,'','','','')
  
    else:
        data=link['channels']
        for field in data:
            id= str(field['id'])
            name= field['title'].encode("utf-8")            
            iconimage=image+name.replace(' ','').replace('-Free','').replace('HD','').replace('i/H','i-H').replace('-[US]','').replace('-[EU]','').replace('[COLOR yellow]','').replace('[/COLOR]','').replace(' (G)','').lower()+'.png'
            addDir(name,id,2,iconimage,'False','','')
                
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)
    
    
def GENRES(name,url):

    link = json.loads(server())
    data=link['channels']
    for field in data:
        id= field['id']
        title= field['title'].encode("utf-8")
        genre= field['cat_id']
        iconimage=image+title.replace(' ','').replace('HD','').replace('i/H','i-H').lower()+'.png'        
        if url == genre:
            addDir(title,id,2,iconimage,'False','','')
                
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)                     

 
def Show_Dialog():
    dialog = xbmcgui.Dialog()
    dialog.ok(THESITE.upper(), '',"All Done Try Now", "")
 
    
def OPEN_MAGIC(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent' , "Magic Browser")
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
        
        
        
def timeout():
    quality = ADDON.getSetting('timeout')
    if quality == '0':
        return ' timeout=5 '
    elif quality == '1':
        return ' timeout=10'
    elif quality == '2':
        return ' timeout=15'
    elif quality == '3':
        return ' timeout=20'
    elif quality == '4':
        return ' timeout=25'
    elif quality == '5':
        return ' timeout=30'
    elif quality == '6':
        return ' timeout=35'
    elif quality == '7':
        return ' timeout=40'
    elif quality == '8':
        return ' timeout=45'
    elif quality == '9':
        return ' timeout=50'
        


def Show_Down():
    dialog = xbmcgui.Dialog()
    dialog.ok(THESITE.upper(), 'Sorry Channel is Down',"Will Be Back Up Soon", "Try Another Channel")  
    
def Show_Cover():
    dialog = xbmcgui.Dialog()
    dialog.ok(THESITE.upper(), '',"Sorry We Dont Cover This Channel", "")    
   
        
def PLAY_STREAM(name, url, iconimage, play, description):

    
    if play =='GET_EVENT':
        url=PLAY_FROM_EVENTS(name, url, iconimage, play, description)
        if not url:
            return Show_Cover()
    if sessionExpired():
        Login()
    net.set_cookies(cookie_jar)
    stream_url= net.http_GET('http://'+THESITE+'/api/matrix/channel/%s'%url,headers={'User-Agent' :UA}).content
    if stream_url=='':
        return Show_Down()
    liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
    liz.setInfo(type='Video', infoLabels={'Title':description})
    liz.setProperty("IsPlayable","true")
    liz.setPath(stream_url+timeout())
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz) 



def PLAY_FROM_EVENTS(name, url, iconimage, play, description):
    name=name.split('[COLOR green]')[1].replace('[/COLOR]','')
    nameFINAL=[]
    urlFINAL=[]
    
    if ',' in name:
        nameSelect=[]
        urlSelect=[]
        name=name.split(',')
        for p in name:
            urlSelect.append(p.strip().lower())
            nameSelect.append(p.strip())
        TITLE = urlSelect[xbmcgui.Dialog().select('Please Select Channel', nameSelect)]      
        TITLE=TITLE.replace(' ','').lower().strip()
        link = server().split('{')
        for YOYO in link:
            if TITLE in YOYO.replace(' ','').lower():
                print YOYO
                id = re.compile('"id":"(.+?)"').findall(YOYO)[0]
                NAME = re.compile('"title":"(.+?)"').findall(YOYO)[0]
                #GENRE = re.compile('"mediaid":"(.+?)"').findall(YOYO)[0]
                urlFINAL.append(id)
                nameFINAL.append('[COLOR red]%s[/COLOR]'%(NAME))
        if urlFINAL:
            return urlFINAL[xbmcgui.Dialog().select('Multiple Channels Found', nameFINAL)] 
        else:
            return False

                       
    else:
    
        NAME=name.replace(' ','').lower().strip()
        link = server().split('{')
        for YOYO in link:
                match = re.compile('"id":"(.+?)".+?"title":"(.+?)"').findall(YOYO)
                for id,NAME_ in match :
                    print NAME
                    print NAME_.replace(' ','').lower().strip()
                    if NAME in NAME_.replace(' ','').lower().strip():
                        urlFINAL.append(id)
                        nameFINAL.append('[COLOR red]%s[/COLOR]'%(NAME_))
        if urlFINAL:
            return urlFINAL[xbmcgui.Dialog().select('Multiple Channels Found', nameFINAL)] 
        else:
            return False
            
            
    
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

def addDir(name,url,mode,iconimage,play,date,description,page=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&play="+urllib.quote_plus(play)+"&date="+urllib.quote_plus(date)+"&description="+urllib.quote_plus(description)+"&page="+str(page)
        #print name.replace('-[US]','').replace('-[EU]','').replace('[COLOR yellow]','').replace('[/COLOR]','').replace(' (G)','')+'='+u
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name,"Premiered":date,"Plot":description} )
        menu=[]
        menu.append(('[COLOR green]Refresh Channel List[/COLOR]','XBMC.RunPlugin(%s?mode=202&url=None)'% (sys.argv[0])))
        menu.append(('[COLOR red]Delete Cookie[/COLOR]','XBMC.RunPlugin(%s?mode=203&url=None&description=%s&name=%s&play=False&iconimage=%s)'% (sys.argv[0],description,name,iconimage)))
        menu.append(('[COLOR cyan]Log Out[/COLOR]','XBMC.RunPlugin(%s?mode=205&url=None&description=%s&name=%s&play=False&iconimage=%s)'% (sys.argv[0],description,name,iconimage)))
        liz.addContextMenuItems(items=menu, replaceItems=False)
        if mode == 2 or mode==7  or mode==2004:
            if not mode == 2000:
            
                liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
          
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok


def addLink(name,url,iconimage, fanart):
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty("IsPlayable","true")
        liz.setProperty("Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)

        
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
date=None
description=None
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
        play=urllib.unquote_plus(params["play"])
except:
        pass
try:
        date=urllib.unquote_plus(params["date"])
except:
        pass
try:
        description=urllib.unquote_plus(params["description"])
except:
        pass
try:        
        page=int(params["page"])
except:
        pass
   
        
#these are the modes which tells the plugin where to go
if mode==None or url==None or len(url)<1:
        CATEGORIES()
               
elif mode==2:
        PLAY_STREAM(name,url,iconimage,play,description)
        
elif mode==3:
        REPLAY()
        
elif mode==4:
        GENRES(name,url)
        
elif mode==202:
        Login()
        Show_Dialog()
        
elif mode==203:
        os.remove(cookie_jar)
        Show_Dialog()  
        
elif mode==205:
        LOGOUT()     
        
elif mode==2001:
        ADDON.openSettings()   
        
else:
        #just in case mode is invalid 
        CATEGORIES()

               
xbmcplugin.endOfDirectory(int(sys.argv[1]))

