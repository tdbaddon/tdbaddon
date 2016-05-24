import urllib,urllib2,re,sys,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os,xbmcvfs,string
from t0mm0.common.net import Net as net
from t0mm0.common.addon import Addon
import settings
import json
import datetime
import time


PLUGIN='plugin.video.MikeysKaraoke'

net=net()
begurl='http://www.sunflykaraoke.com/search/genre/'
          
endurl='?sort_Karaoke Tracks=popularity-desc'
youtubeaddon = xbmcaddon.Addon(id='plugin.video.youtube')
downloads= youtubeaddon.getSetting('download_path')

local = xbmcaddon.Addon(id=PLUGIN)

ADDON = settings.addon()
home = ADDON.getAddonInfo('path')
sfdownloads= ADDON.getSetting('sfdownloads')
datapath = xbmc.translatePath(ADDON.getAddonInfo('profile'))
font=ADDON.getSetting('font').lower()
cookie_path = os.path.join(datapath, 'cookies')
cookie_jar = os.path.join(cookie_path, "karaokantalive")

if os.path.exists(datapath)==False:
    os.mkdir(datapath) 
if ADDON.getSetting('sfenable') == True:
    os.makedirs(sfdownloads)
if ADDON.getSetting('visitor_ga')=='':
    from random import randint
    ADDON.setSetting('visitor_ga',str(randint(0, 0x7fffffff)))
    
K_db='http://xtyrepo.me/xunitytalk/addons/plugin.video.MikeysKaraoke/Karaoke.db'
updatetxt='http://xtyrepo.me/xunitytalk/addons/plugin.video.MikeysKaraoke/update.txt'


addon = Addon('plugin.video.MikeysKaraoke',sys.argv)
art= "%s/KaraokeArt/"%local.getAddonInfo("path")
from sqlite3 import dbapi2 as database
db_dir = os.path.join(xbmc.translatePath("special://database"), 'Karaoke.db')


def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link


def Update():
    import downloader
    dp = xbmcgui.DialogProgress()
    dp.create("Mikeys Karaoke","",'Building Database Please Wait', ' ')
    downloader.download(K_db, db_dir,dp)
    
if os.path.exists(db_dir)==False:
    link=OPEN_URL(updatetxt)
    match=re.compile('id=<(.+?)>').findall (link)
    dp = xbmcgui.Dialog()
    dp.ok("Mikeys Karaoke","",'There is a New Database Update', 'Please Wait')
    Update()
    ADDON.setSetting('id',match[0])     
       
        
db = database.connect(db_dir)
db.execute('CREATE TABLE IF NOT EXISTS tracklist (sunfly_name, number, artist, track, iconimage, url)')
db.execute('CREATE TABLE IF NOT EXISTS favourites (track_name, artist, track, iconimage, url)')
db.commit()
db.close()

def GRABBER(type,mode,item):
    db = database.connect( db_dir );cur = db.cursor()
    if type == 1:#EXACT MATCH ALL
        item = '%'+item+'%'
        cached = cur.fetchall()
        try: cur.execute('SELECT * FROM tracklist WHERE %s = "%s"' %(mode,item))
        except:pass
    elif type == 2: #EXACT MATCH ONE
        item = '%'+item+'%'
        try: cur.execute('SELECT * FROM tracklist WHERE %s = "%s"' %(mode,item))
        except:pass
        cached = cur.fetchone()
    elif type == 3:#NEAREST MATCH ONE
        item = '%'+item+'%'
        try: cur.execute('SELECT * FROM tracklist WHERE %s LIKE "%s"' %(mode,item))
        except:pass
        cached = cur.fetchone()
    elif type == 4:# NEAREST MATCH ALL
        item = '%'+item+'%'
        try: cur.execute('SELECT * FROM tracklist WHERE %s LIKE "%s"' %(mode,item))
        except:pass
        cached = cur.fetchall()
    elif type == 5:# NEAREST MATCH ALL BY FIRST LETTER
        item = item+'%'
        try: cur.execute('SELECT * FROM tracklist WHERE %s LIKE "%s"' %(mode,item))
        except:pass
        cached = cur.fetchall()
    if cached:
        db.close()
        return cached

def STRIP(name):
  return re.sub(r'\[.*?\]|\(.*?\)|\W -', ' ', name).strip()

  
def download_DB():
    import downloader
    dp = xbmcgui.DialogProgress()
    dp.create("Mikeys Karaoke","",'Building Database Please Wait', ' ')
    downloader.download(K_db, db_dir,dp)
  
  
def CATEGORIES():
        link=OPEN_URL(updatetxt)
        match=re.compile('id=<(.+?)>').findall (link)
        if int(match[0]) > int(ADDON.getSetting('id')):
            dp = xbmcgui.Dialog()
            dp.ok("Mikeys Karaoke","",'There is a New Database Update', 'Please Wait')
            Update()
            ADDON.setSetting('id',match[0])        
        addDir('[COLOR '+font+']'+'Youtube[/COLOR] Karaoke','url',19,art+'Main/youtube.png','none',1)
        addDir('[COLOR '+font+']'+'Sunfly[/COLOR] Karaoke','url',20,art+'Main/SUNFLY.png','none',1)
        if ADDON.getSetting('karaokantalive') =='true':
            addDir('[COLOR '+font+']'+'Karaokanta[/COLOR] Karaoke','url',201,art+'Main/karaokantalive.png','none',1)
        addDir('[COLOR '+font+']'+'Favourites[/COLOR]','url',2,art+'Main/SUNFLY.png','none',1)
        setView('movies', 'MAIN')

def karaokantaliveCATEGORIES():      
        addDir('[COLOR '+font+']'+'Ultimas Novedades[/COLOR] Karaoke','http://www.karaokantalive.com/busqueda.php?n=1',202,'','none',1)
        addDir('[COLOR '+font+']'+'Temas Exclusivos K-Live[/COLOR] Karaoke','http://www.karaokantalive.com/busqueda.php?n=2',202,'','none',1)
        addDir('[COLOR '+font+']'+'Lo Mas Nuevo[/COLOR] Karaoke','http://www.karaokantalive.com/busqueda.php?n=3',202,'','none',1)
        addDir('[COLOR '+font+']'+'Mis Favoritos[/COLOR] Karaoke','http://www.karaokantalive.com/favoritos.php',202,'','none',1)


def karaokanta_GET(name,url):      
        karaokanta_LOGIN()
        net.set_cookies(cookie_jar)
        html = net.http_GET(url).content
        match=re.compile('vID=(.+?)\.flv.+?><img src=.+?/>(.+?)<').findall(html)
        for URL ,name in match:
            name=name.replace('&nbsp;',' ')
            NAME=name.encode('utf-8')
            addDir(NAME,URL,203,'','none',1)
            
            
def karaokanta_PLAY(name,url):
    STREAM='rtmp://fss29.streamhoster.com/sfuente/videos/%s app=sfuente/ swfUrl=http://www.karaokantalive.com/jwplayer/player2.swf playPath=videos/%s' %(url,url)
    liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
    liz.setInfo(type='Video', infoLabels={'Title':name})
    liz.setProperty("IsPlayable","true")
    liz.setPath(STREAM)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
        
            
def mikeyyoutube(url):
        addDir('[COLOR '+font+']'+'Search[/COLOR]-[COLOR '+font+']'+'Y[/COLOR]outube Karaoke','url',3,art+'Main/Search.png','none',1)
        if ADDON.getSetting('downloads') == 'true':
            addDir('[COLOR '+font+']'+'D[/COLOR]ownloads','url',15,art+'Main/favorites.png','',1)
        addDir('[COLOR '+font+']'+'Most[/COLOR] Popular','http://www.sunflykaraoke.com/tracks?dir=asc&limit=200&order=popular',7,art+'AtoZ/P.png','none',1)
        addDir('[COLOR '+font+']'+'L[/COLOR]atest','http://www.sunflykaraoke.com/tracks?dir=asc&limit=200&order=latestalbums',7,art+'AtoZ/L.png','none',1)
        addDir('[COLOR '+font+']'+'Browse[/COLOR] Artist','http://www.lyricsmania.com/lyrics/%s.html',1,art+'Main/Artist.png','none',4)
        addDir('[COLOR '+font+']'+'Browse[/COLOR] Tracks','http://www.sunflykaraoke.com/tracks/search/byletter/letter/%s/',1,art+'Main/Title.png','none',7)
        addDir('[COLOR '+font+']'+'G[/COLOR]enre','http://www.sunflykaraoke.com/',8,art+'Main/Genre.png','none',1)
        setView('movies', 'MAIN')
        
def mikeysunfly(url):
        addDir('[COLOR '+font+']'+'Search[/COLOR]-[COLOR '+font+']'+'X[/COLOR]unity Karaoke','url',16,art+'Main/Search.png','none',1)
        if ADDON.getSetting('sfenable') == 'true':
            addDir('[COLOR '+font+']'+'D[/COLOR]ownloads','url',31,art+'Main/favorites.png','',1)
        addDir('[COLOR '+font+']'+'Search[/COLOR] By Number','url',25,art+'Main/Search.png','none',1)
        addDir('[COLOR '+font+']'+'Browse[/COLOR] Artist','http://www.sunflykaraoke.com/',1,art+'Main/Artist.png','none',23)
        addDir('[COLOR '+font+']'+'Browse[/COLOR] Tracks','http://www.sunflykaraoke.com/',1,art+'Main/Title.png','none',24)
        addDir('[COLOR '+font+']'+'G[/COLOR]enre','http://www.sunflykaraoke.com/',32,art+'Main/Genre.png','none',1)
        addDir('[COLOR '+font+']'+'D[/COLOR]ownload Database','http://www.sunflykaraoke.com/',103,'','none',1)
        setView('movies', 'MAIN')

def AtoZ(url,number,fanart):

    if '%s' in url:
        addDir('0-9',url%'0-9',number,"%s/KaraokeArt/AtoZ/%s.png"%(local.getAddonInfo("path"),'0-9'),fanart,1)
        for i in string.ascii_uppercase:
            addDir(i,url%i,number,"%s/KaraokeArt/AtoZ/%s.png"%(local.getAddonInfo("path"),i),fanart,1)
            setView('movies', 'A-Z')
    else:
        for i in string.ascii_uppercase:
            addDir(i,url,number,"%s/KaraokeArt/AtoZ/%s.png"%(local.getAddonInfo("path"),i),fanart,1)

def FAVOURITES(switch,name,iconimage,url):
    IMAGE = os.path.join(ADDON.getAddonInfo('path'), 'icon.jpg')
   
    db = database.connect( db_dir );cur = db.cursor()
    if switch == 'add':
        sql = "INSERT OR REPLACE INTO favourites (track_name,iconimage,url) VALUES(?,?,?)"
        cur.execute(sql, (name,iconimage.replace(' ','%20'),url.replace(' ','%20')))
        db.commit(); db.close()
        xbmc.executebuiltin('XBMC.Notification('+name+',Added to Favorites,2000,'+IMAGE+')')
    if switch == 'delete':
        cur.execute("DELETE FROM favourites WHERE track_name='%s'"%name)
        db.commit(); db.close()
        xbmc.executebuiltin('XBMC.Notification('+name.replace('  ',' ')+',Deleted from Favorites,2000,'+IMAGE+')')
        xbmc.executebuiltin("XBMC.Container.Refresh")
    if switch == 'display':
        cur.execute("SELECT * FROM favourites")
        cached = cur.fetchall()
        if cached:
            for name,artist,track,iconimage,url in cached:
                addLinkSF(name,url,url.replace('.avi','.jpg'))
        
def GENRE(url):
        link=net.http_GET('http://www.sunflykaraoke.com/genre').content.encode('ascii','ignore')
        match=re.compile('class="thumb_img">.+?<img src="(.+?)".+?href="(.+?)">(.+?)</a>',re.DOTALL).findall(link)
        for iconimage,url , name in match:
            addDir(name,url+'?dir=asc&limit=200&order=latestalbums',10,iconimage,art+'Main/Fanart_G.jpg',1) 
        
        setView('movies', 'GENRE')
        
def GENRESF(url):
        link=net.http_GET('http://www.sunflykaraoke.com/genre').content.encode('ascii','ignore')
        match=re.compile('class="thumb_img">.+?<img src="(.+?)".+?href="(.+?)">(.+?)</a>',re.DOTALL).findall(link)
        for iconimage,url , name in match:
            addDir(name,url+'?dir=asc&limit=200&order=latestalbums',33,iconimage,art+'Main/Fanart_G.jpg',1) 
        
        setView('movies', 'GENRE')
            
def Next_Page(link):
    link = link.split('class="paging-bar-pages">')[1]
    link=link.split('<a href=')
    for l in link:
        match=re.compile('"(.+?)#.+?" class="arrow">&gt;</a>').findall(l)        
        if match:
            return match
    return None 


    
    
def SEARCH(url):
        PAGE=1
        keyboard = xbmc.Keyboard('', 'Search')
        keyboard.doModal()
        if keyboard.isConfirmed() and len(keyboard.getText())>0:
           TXT='https://www.youtube.com/results?search_query=%s+karaoke&hl=en-GB&page='  % (keyboard.getText().replace(' ','+'))
           html=OPEN_URL(TXT+str(PAGE))
        else: return
        
        link=html.split('yt-lockup-title')
        
        for p in link:
            #print p
            try:
                url=p.split('watch?v=')[1]
                name= p.split('title="')[1]
                name=name.split('"')[0]  
                name = str(name).replace("&#39;","'") .replace("&amp;","and") .replace("&#252;","u") .replace("&quot;","").replace("[","").replace("]","").replace("-"," ")
                iconimage = 'http://i.ytimg.com/vi/%s/0.jpg' % url.split('"')[0]
                if not 'video_id' in name:
                    if not '_title_' in name:
                        addLink(name,url.split('"')[0] ,iconimage,'')
            except:pass
   
        addDir('[COLOR blue][B]Next Page >>[/B][/COLOR]',TXT,11,art+'nextpage.png','',PAGE)
        setView('movies', 'VIDEO')
        
                                                                                
def ARTIST_INDEX(url, iconimage):
        link=net.http_GET(url).content.encode('ascii','ignore')
        match = re.compile('<a href="(.+?)" title="(.+?)"').findall(link)
        for url, name in match:
            url = 'http://www.lyricsmania.com'+url   
            name = str(name).replace("lyrics","")
            addDir(name,url,5,iconimage,art+'Main/Fanart_A.jpg',1)
            setView('movies', 'DEFAULT')


def ARTIST_SONG_INDEX(url,name):
        link=net.http_GET(url).content
        match = re.compile('http://www.musictory.com/(.+?)"').findall(link)
        url1 = 'http://www.musictory.com/'+match[0]+'/Songs'
        link1=net.http_GET(url1).content
        url = re.compile('<h1 itemprop="name">(.+?) Songs<').findall(link1)[0]
        match1 = re.compile('<span itemprop="name">(.+?)</span>').findall(link1)
        fanart = art+'Main/Fanart_A.jpg'
        for name in match1:
            name=name.encode('ascii','ignore')
            name = str(name).replace("&Agrave;","A").replace('&eacute;','e').replace('&ecirc;','e').replace('&egrave;','e').replace("&agrave;","A")
            addDir(name,'url',6,iconimage,fanart,1)
            setView('tvshow', 'DEFAULT')
            

    
def TRACK_INDEX(url, iconimage):
        link=OPEN_URL(url.replace(' ','%20'))
        #link=str(link1).replace('&___c=___c#listingTrack0_link','')
        match = re.compile('<li><span>.+?href=.+?title="(.+?)">.+?> - <.+?>(.+?)</a>').findall(link)
        #nextpageurl=Next_Page(link)[0]       
        uniques = []        
        for name, url, in match:

                name = str(name).replace("&#39;","'") .replace("&amp;","and") .replace("&#252;","u") .replace("&quot;","")  
                url = str(url).replace("&#39;","'") .replace("&amp;","and") .replace("&#252;","u") .replace("&quot;","") 
                name = name+ '   ('+ url+')'
                if not '</a>' in name:
                    if name not in uniques:
                        uniques.append(name)      
                        addDir(name,url,9,iconimage,art+'Main/Fanart_T.jpg',1)
                setView('movies', 'DEFAULT')
        #try:
                #url='http://www.sunflykaraoke.com'+str(nextpageurl)
                #name= '[COLOR '+font+']'+'[B]Next Page >>[/B][/COLOR]'
                #addDir(name,url,7,art+'next.png','none',1)    
                #setView('movies', 'DEFAULT') 
        #except:
                #pass
                
def GENRE_INDEX(name,url, iconimage):
        link=OPEN_URL(url.replace(' ','%20'))
        match = re.compile('<div class="track_det" style="width:80%">.+?<p><a href=".+?s">(.+?)<.+?<p class="trkname">.+?href=".+?">(.+?)<',re.DOTALL).findall(link)
        #nextpageurl=Next_Page(link)[0]
        uniques=[]
        for name, url, in match:
            name = str(name).replace("&#39;","'") .replace("&amp;","and") .replace("&#252;","u") .replace("&quot;","")  
            url = str(url).replace("&#39;","'") .replace("&amp;","and") .replace("&#252;","u") .replace("&quot;","") 
            name = name+ '   ('+ url+')'
            if not '</a>' in name:
                if name not in uniques:
                    uniques.append(name)      
    
                    addDir(name,url,9,iconimage,art+'Main/Fanart_G.jpg',1)
            setView('movies', 'DEFAULT')
        #try:
                #url='http://www.sunflykaraoke.com'+str(nextpageurl)
                #name= '[COLOR '+font+']'+'[B]Next Page >>[/B][/COLOR]'
                #addDir(name,url,7,art+'next.png','none',1)    
                #setView('movies', 'DEFAULT') 
        #except:
                #pass
            
            
def GENRE_INDEXSF(name,url, iconimage):
        link=OPEN_URL(url.replace(' ','%20'))
        match = re.compile('<div class="track_det" style="width:80%">.+?<p><a href=".+?">(.+?)<.+?<p class="trkname">.+?href=".+?">(.+?)<',re.DOTALL).findall(link)
        #nextpageurl=Next_Page(link)[0]
        uniques=[]
        for name, url, in match:
            passto = re.sub('[\(\)\{\}<>]', '', name.replace("&#39;","'") .replace("&amp;","and") .replace("&#252;","u") .replace("&quot;","").replace("&quot;",""))
            name = re.sub('[\(\)\{\}<>]', '', name.replace("&#39;","'") .replace("&amp;","and") .replace("&#252;","u") .replace("&quot;","").replace("&quot;","").replace("'",""))
            url = str(url).replace("&#39;","'") .replace("&amp;","and") .replace("&#252;","u") .replace("&quot;","") 
            name = name+ '   ('+ url+')'
            if not '</a>' in name:
                if name not in uniques:
                    uniques.append(name)      

                    addDir('[COLOR '+font+']'+'%s[/COLOR] - %s'%(passto,url),name,34,iconimage,art+'Main/Fanart_G.jpg',1)
            setView('movies', 'DEFAULT')
        #try:
                #url='http://www.sunflykaraoke.com'+str(nextpageurl)
                #name= '[COLOR '+font+']'+'[B]Next Page >>[/B][/COLOR]'
                #addDir(name,url,33,art+'next.png','none',1)    
                #setView('movies', 'DEFAULT') 
        #except:
                #pass
          
        
def SEARCH_GENRE(url,name):

    url=url.split('(')[0].strip()
    #url=url.slpit('[')[0]
    
    db=GRABBER(4,'track',re.sub('\A(a|A|the|THE|The)\s','',url))
    if not db: addLinkSF('[COLOR red]TRACK NOT AVAILABLE.[/COLOR]',url,'');return
    for sf,number,artist,track,icon,burl in db:
        if artist in name.split('-')[1].strip():
            addLinkSF('[COLOR '+font+']'+'%s ~ [/COLOR]%s'%(artist,track),burl,icon,split=1)
        
def YOUTUBE_SONG_INDEX(name, url, iconimage, fanart):
        PAGE=1
        url = str(url).replace(' ','+').replace('_','+')  
        name = str(name).replace(' ','+') 
        url = 'https://www.youtube.com/results?search_query=%s+%s+karaoke&hl=en-GB&page=' % (name, url) 
        html=OPEN_URL(url)
        link=html.split('yt-lockup-title')
        for p in link:
            try:
                url=p.split('watch?v=')[1]
                name= p.split('title="')[1]
                name=name.split('"')[0]  
                name = str(name).replace("&#39;","'") .replace("&amp;","and") .replace("&#252;","u") .replace("&quot;","").replace("[","").replace("]","").replace("-"," ")
                iconimage = 'http://i.ytimg.com/vi/%s/0.jpg' % url.split('"')[0]
                if not 'video_id' in name:
                    if not '_title_' in name:
                        addLink(name,url.split('"')[0] ,iconimage,'')
            except:pass
   
        addDir('[COLOR blue][B]Next Page >>[/B][/COLOR]',url,11,art+'nextpage.png','',PAGE)
        setView('movies', 'VIDEO')
            
def TITLE_ORDERS_YOUTUBE(name, url,fanart):
        PAGE=1
        name = str(name).replace('   (','+') .replace(' ','+') .replace(')','')
        url = 'https://www.youtube.com/results?search_query=%s+karaoke&hl=en-GB&page=' % (name) 
        #print url
        html=OPEN_URL(url)
        link=html.split('yt-lockup-title')
        for p in link:
            try:
                url=p.split('watch?v=')[1]
                name= p.split('title="')[1]
                name=name.split('"')[0]  
                name = str(name).replace("&#39;","'") .replace("&amp;","and") .replace("&#252;","u") .replace("&quot;","").replace("[","").replace("]","").replace("-"," ")
                iconimage = 'http://i.ytimg.com/vi/%s/0.jpg' % url.split('"')[0]
                if not 'video_id' in name:
                    if not '_title_' in name:
                        addLink(name,url.split('"')[0] ,iconimage,'')
            except:pass
   
        addDir('[COLOR blue][B]Next Page >>[/B][/COLOR]',url,11,art+'nextpage.png','',PAGE)
        setView('movies', 'VIDEO')
        
        
def SF_Download(name,url,iconimage,split):
    import downloader
    name=name.replace(' [/color]','').split('~')[split]
    dp = xbmcgui.DialogProgress()
    dp.create("Mikeys Karaoke","",'Downloading', name)
    path = xbmc.translatePath(os.path.join(sfdownloads,''))
    name=name.upper()
    lib=os.path.join(path, name+'.avi')
    downloader.download(iconimage.replace('.jpg','.avi'),lib,dp)
    lib=os.path.join(path, name+'.jpg')
    downloader.download(iconimage,lib,dp)
    
    
def DOWNLOADS(downloads):
     import glob
     path = downloads
     for infile in glob.glob(os.path.join(path, '*.*')):
         addFile(infile)
    
    
def SFDOWNLOADS(sfdownloads):
     import glob
     path = sfdownloads
     for infile in glob.glob(os.path.join(path, '*.avi')):
         addFileSF(infile)
        
            
def nextpage(url,number):
        URL=url
        PAGE=int(number)+1
        html=OPEN_URL(url+str(PAGE))
        link=html.split('yt-lockup-title')
        for p in link:
            try:
                url=p.split('watch?v=')[1]
                name= p.split('title="')[1]
                name=name.split('"')[0]  
                name = str(name).replace("&#39;","'") .replace("&amp;","and") .replace("&#252;","u") .replace("&quot;","").replace("[","").replace("]","").replace("-"," ")
                iconimage = 'http://i.ytimg.com/vi/%s/0.jpg' % url.split('"')[0]
                if not 'video_id' in name:
                    if not '_title_' in name:
                        addLink(name,url.split('"')[0] ,iconimage,'')
            except:pass
   
        addDir('[COLOR blue][B]Next Page >>[/B][/COLOR]',URL,11,art+'nextpage.png','',PAGE)
        setView('movies', 'VIDEO')
            
def addFile(file):
        name = file.replace(downloads,'').replace('.mp4','')
        name = name.split('-[')[-2]
        thumb = icon(file)[0]
        iconimage = 'http://i.ytimg.com/vi/%s/0.jpg' % thumb
        url=file
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name})
        liz.setProperty("IsPlayable","true")
        liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        contextMenu = []
        contextMenu.append(('Delete', 'XBMC.RunPlugin(%s?mode=102&url=%s&iconimage=%s)'% (sys.argv[0], file,iconimage)))
        liz.addContextMenuItems(contextMenu,replaceItems=True)
        xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url=url,listitem = liz, isFolder = False)
        setView('movies', 'VIDEO')
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)    

def addFileSF(file):
        iconimage = file.replace('.avi','.jpg').replace('.mp4','.jpg')
        name = file.replace(sfdownloads,'').replace('.avi','').replace('.mp4','')
        url=file
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name})
        liz.setProperty("IsPlayable","true")
        liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        contextMenu = []
        contextMenu.append(('Delete', 'XBMC.RunPlugin(%s?mode=102&url=%s&iconimage=%s)'% (sys.argv[0], file,iconimage)))
        liz.addContextMenuItems(contextMenu,replaceItems=True)
        xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url=url,listitem = liz, isFolder = False)
        setView('movies', 'VIDEO')
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)   
        
                
def deleteFileSF(file,iconimage):
    tries    = 0
    maxTries = 10
    while os.path.exists(file) and tries < maxTries:
        try:
            os.remove(file)
            break
        except:
            xbmc.sleep(500)
            tries = tries + 1
    while os.path.exists(iconimage) and tries < maxTries:
        try:
            os.remove(iconimage)
            break
        except:
            xbmc.sleep(500)
            tries = tries + 1
            
            
    if os.path.exists(file):
        d = xbmcgui.Dialog()
        d.ok('Mikeys Karaoke', 'Failed to delete file')         
                           
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
        

def Sunflysearch(url):
    keyboard = xbmc.Keyboard('', '[COLOR grey3]Search by[/COLOR] [COLOR '+font+']'+'Artist[/COLOR] [COLOR grey3]or[/COLOR] [COLOR '+font+']'+'Track[/COLOR]')
    keyboard.doModal()
    if keyboard.isConfirmed():
        db=GRABBER(4,'artist',keyboard.getText())
        if not db: db=GRABBER(4,'artist',re.sub('\A(a|A|the|THE|The)\s','',keyboard.getText()))
        if not db: db=GRABBER(4,'track',keyboard.getText())
        if not db: db=GRABBER(4,'track',re.sub('\A(a|A|the|THE|The)\s','',keyboard.getText()))
        if not db: addLinkSF('[COLOR red]TRACK NOT AVAILABLE.[/COLOR]',url,'');return
        for sf,number,artist,track,icon,burl in db:
            addLinkSF('[COLOR '+font+']'+'%s ~ [/COLOR]%s'%(artist,track),burl,icon)
    
                
             
def AZ_ARTIST_SEARCH(name):
    db=GRABBER(5,'artist',name)
    if not db: addLinkSF('[COLOR red]ARTIST NOT AVAILABLE.[/COLOR]',url,'');return
    for sf,number,artist,track,icon,burl in db:
            addLinkSF('[COLOR '+font+']'+'%s ~ [/COLOR]%s'%(artist,track),burl,icon,split=1)
    
def SF_SEARCH(url):
    sunfly = 'SF'
    keyboard = xbmc.Keyboard(sunfly, 'Enter Sunfly Disc Number:-')
    keyboard.doModal()
    if keyboard.isConfirmed():
        db=GRABBER(4,'sunfly_name',keyboard.getText())
        if not db: addLinkSF('[COLOR red]DISC NOT AVAILABLE.[/COLOR]',url,'');return
        for sf,number,artist,track,icon,burl in db:
            addLinkSF('[COLOR '+font+']'+'%s:-%s ~ [/COLOR]%s'%(sf,number,track),burl,icon,split=1)
        
        
def AZ_TRACK_SEARCH(name):
    db=GRABBER(5,'track',re.sub('\A(a|A|the|THE|The)\s','',name))
    if not db: addLinkSF('[COLOR red]TRACK NOT AVAILABLE.[/COLOR]',url,'');return
    for sf,number,artist,track,icon,burl in db:
            addLinkSF('[COLOR '+font+']'+'%s ~ [/COLOR]%s'%(track,artist),burl,icon,split=0)    


def karaokanta_LOGIN():
    
    loginurl = 'http://www.karaokantalive.com/login.php?action=process'
    username = ADDON.getSetting('karaokantaliveuser')
    password = ADDON.getSetting('karaokantalivepass')

    html = net.http_GET('http://www.karaokantalive.com').content
    formid=re.compile('name="formid" value="(.+?)"').findall (html)[0]
    data     = {'formid':formid,'password': password,
                                            'email_address': username,
                                            'submit.x':'0','submit.y':'0'}
    headers  = {'Host':'www.karaokantalive.com',
                                            'Origin':'http://www.karaokantalive.com',
                                            'Referer':'http://www.karaokantalive.com'}
    
    html = net.http_POST(loginurl, data, headers).content
  
    if os.path.exists(cookie_path) == False:
            os.makedirs(cookie_path)
    net.save_cookies(cookie_jar)


        
def addDir(name,url,mode,iconimage,fanart,number):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&number="+str(number)
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setProperty( "Fanart_Image", fanart )
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        if (mode == 2000)or mode==103 or mode==203:
            if mode ==203:
                liz.setProperty("IsPlayable","true")
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz, isFolder=False)
        else:
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz, isFolder=True)
        if not mode==1 and mode==20 and mode==19:
            xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
            
        
def addLink(name,url,iconimage, fanart,showcontext=True):
    #name=name.encode('ascii', 'ignore')
    #url=url.encode('ascii', 'ignore')
    cmd = 'plugin://plugin.video.youtube/?path=root/video&action=download&videoid=%s' % url
    youtube = 'plugin://plugin.video.youtube/?path=root/video&action=play_video&videoid=%s' % url
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    liz.setProperty("IsPlayable","true")
    liz.setProperty("Fanart_Image", fanart )
    menu = []
    if showcontext:
        try:
            if name in FAV:
                menu.append(('Remove YouTube Favorites','XBMC.RunPlugin(%s?name=%s&mode=14&iconimage=None&fanart=None&url=None)' %(sys.argv[0],name)))
            else:
                menu.append(('Add to YouTube Favorites','XBMC.RunPlugin((%s?fanart=%s&mode=13&iconimage=%s&url=%s&name=%s)' %(sys.argv[0],fanart,iconimage,url,name)))
        except:
            menu.append(('Add to YouTube Favorites','XBMC.RunPlugin(%s?fanart=%s&mode=13&iconimage=%s&url=%s&name=%s)' %(sys.argv[0],fanart,iconimage,url,name)))
    if ADDON.getSetting('downloads') == 'true':
        menu.append(('Download', 'XBMC.RunPlugin(%s)' % cmd))   
    liz.addContextMenuItems(items=menu, replaceItems=True)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=youtube,listitem=liz,isFolder=False)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)


def PlayYouTube(name,url,iconimage):
    import yt
    youtube=yt.PlayVideo(url)    
    liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
    liz.setInfo(type='Video', infoLabels={'Title':name})
    liz.setProperty("IsPlayable","true")
    liz.setPath(str(youtube))
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
                                
def addLinkSF(name,url,iconimage,showcontext=True,split=None):
        if '.mp4' in url:
            iconimage=url.replace('.mp4','.jpg')
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name})
        liz.setProperty("IsPlayable","true")
        liz.setProperty('mimetype', 'video/x-msvideo')
            
        menu = []
        if showcontext:
            menu.append(('[COLOR green]Add[/COLOR] to Xunity Karaoke Favorites','XBMC.RunPlugin(%s?mode=2&iconimage=%s&url=%s&name=%s&switch=%s)' %(sys.argv[0],iconimage,url,name,'add')))
            menu.append(('[COLOR red]Remove[/COLOR] Xunity Karaoke from Favourites','XBMC.RunPlugin(%s?mode=2&iconimage=%s&url=%s&name=%s&switch=%s)' %(sys.argv[0],iconimage,url,name,'delete')))
        if ADDON.getSetting('sfenable') == 'true':
            menu.append(('Download', 'XBMC.Container.Update(%s?&mode=30&url=%s&name=%s&iconimage=%s&split=%s)' %(sys.argv[0],url,name,iconimage,split)))  
        liz.addContextMenuItems(items=menu, replaceItems=True)
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)

      

params=get_params()
url=None
name=None
mode=None
iconimage=None
fanart=None

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
        switch=urllib.unquote_plus(params["switch"])
except:
        switch='display'
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        number=int(params["number"])
except:
        pass
try:        
        split=int(params["split"])
except:
        pass
                
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)
print "FanartImage: "+str(fanart)
try:print "number: "+str(number)
except:pass

def setView(content, viewType):
    # set content type so library shows more views and info
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if ADDON.getSetting('auto-view') == 'true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )
        
        
if mode==None or url==None or len(url)<1:
        CATEGORIES()
       
elif mode==1:
    AtoZ(url,number,fanart)

elif mode==2:
    FAVOURITES(switch,name,iconimage,url)
        
elif mode==3:
        print ""+url
        SEARCH(url)
        
elif mode==4:
        ARTIST_INDEX(url, iconimage) 
        
elif mode==5:
        ARTIST_SONG_INDEX(url,name)
        
elif mode==6:
        YOUTUBE_SONG_INDEX(name, url, iconimage, fanart)
                                                             
elif mode==7:
        TRACK_INDEX(url, iconimage)
        
elif mode==8:
        GENRE(url)   
        
elif mode==9:
        TITLE_ORDERS_YOUTUBE(name, url, fanart)   
        
elif mode==10:
        GENRE_INDEX(name,url, iconimage)
                      
elif mode==11:
        nextpage(url,number)  
        
elif mode==12:
    pass
elif mode==13:
    addFavorite(name,url,iconimage,fanart)

elif mode==14:
    rmFavorite(name)
        
elif mode==15:
    DOWNLOADS(downloads)
    
elif mode==16:
    Sunflysearch(url)
    
elif mode==17:
    Sunflyurl(name)
    
elif mode==19:
    mikeyyoutube(url)

elif mode==20:
    mikeysunfly(url)

elif mode==23:
    AZ_ARTIST_SEARCH(name)
    
elif mode==24:
    AZ_TRACK_SEARCH(name)
    
elif mode==25:
    SF_SEARCH(name) 
    
elif mode==26:
    print ""
    LATEST_LIST(url)    
    
elif mode==27:
    addSF_Favorite(name,url,iconimage)

elif mode==28:
    rmSF_Favorite(name)
    
elif mode==29:
    getSF_Favorites()
    
elif mode==30:
    SF_Download(name,url,iconimage,split)
    
elif mode==31:
    SFDOWNLOADS(sfdownloads)
    
elif mode==32:
        GENRESF(url)   
elif mode==33:
        GENRE_INDEXSF(name,url, iconimage)
        
elif mode==34:
        SEARCH_GENRE(url,name)
       
elif mode==102:
    deleteFileSF(url,iconimage)
    xbmc.executebuiltin("Container.Refresh")
    
elif mode==103:
    download_DB()

    
elif mode==201:
    karaokantaliveCATEGORIES()

elif mode==202:
    karaokanta_GET(name,url)

elif mode==203:
    karaokanta_PLAY(name,url)    
    
elif mode==3000:
    test()

elif mode==3001:
    PlayYouTube (name,url,iconimage)
    
xbmcplugin.endOfDirectory(int(sys.argv[1]))
