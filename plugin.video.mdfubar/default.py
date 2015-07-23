import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,os
import urlresolver
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net

#F.U.B.A.R - By Mucky Duck (07/2015)

addon_id='plugin.video.mdfubar'
art = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
baseurl = 'dummy'
net = Net()

#http://watch-free-movies-streaming.com/
baseurl101 = 'http://vodlocker.tv'
baseurl102 = 'http://alluc.com'
#http://movies-search-engine.com/
#http://watch-streaming-movies.com/
#http://wawashare.com/


#http://series-cravings.me/
#http://www.tvids.net/
#http://tvstream.ch/
#http://geektv.me/
#http://tvoox.com/
#http://watchtvlinks.ag/


#http://hdfull.tv

baseurl50 = 'http://www.filmovizija.in'
#http://watchmovies-online.ch/hellboy-2004/  1080p
#http://pandamovie.me/
#http://tvoox.com/
baseurl150 = 'http://www.badassmovies4u.com/'
baseurl200 = 'http://www.allcinemamovies.com'


baseurl5001 = 'http://www.hack-sat.com/iptv.php'
#baseurl5001 = 'http://select-pedia.com/tutos/tag/sport/'
#baseurl50002 = 'http://www.iptvlinks.com/2014/12/super-torrent-stream.html'
baseurl5002 = 'http://iptv.filmover.com'
baseurl5010 = 'http://www.iptvsharing.com/2015/07/sport-klub-iptv-links-m3u8.html'
baseurl5020 = 'http://67.159.5.242/ip-1/encoded/Oi8vcGFzdGViaW4uY29tL2hxNlBKWVpS'
def INDEX():
        addDir('Super Search','url',100,'','','')
        addDir('IPTV','url',5000,'','','')
        addDir('www.badassmovies4u.com',baseurl150,150,'','','')
        addDir('www.filmovizija.in',baseurl150,50,'','','')
        addDir('www.allcinemamovies.com','url',200,'','','')

############################################################################################################################

############################################################################################################################

def BASE50(url):
        addDir('NEW',baseurl50,51,'','','')
        addDir('TOP 20',baseurl50,54,'','','')
        addDir('MOVIE GENRE',baseurl50+'/browse-movies-videos-1-date.html',56,'','','')
        addDir('TV SHOWS',baseurl50+'/tvshows.html',58,'','','')
        addDir('DOCUMENTARY',baseurl50+'/browse-Documentary-videos-1-date.html',57,'','','')
        addDir('ANIMATED',baseurl50+'/browse-animated-videos-1-date.html',57,'','','')
        addDir('SEARCH TV','url',60,'','','')
        addDir('SEARCH MOVIES','url',61,'','','')
        

def BASE50MINDEX(url):
        link = OPEN_URL(url)
        match=re.compile('<div class="item"><a href="(.+?)"><img src="(.+?)" alt="(.+?)" .+?</div>(.+?)<.+?>').findall(link)
        for url,icon,name,dis, in match:
                name = name.replace('&amp;','&')
                addDir('[COLOR white]%s[/COLOR]' %name,url,52,icon,'',dis)


def BASE50MHOSTS(url,iconimage):
        link = OPEN_URL(url)
        match=re.compile('<h9>.+?</h9></td>\n<td width="90" style=".+?"><span class="fullm"><a href="(.+?)" title="(.+?)" target="_blank">Watch here</a>').findall(link)
        for url,name in match:
                name = name.replace('&amp;','&').replace('Movie - ','')
                addDir('[COLOR white]%s[/COLOR]' %name,baseurl50+url,53,iconimage,'','')


def BASE50MFINAL(url,iconimage):
        link = OPEN_URL(url)
        match=re.compile('<input type="button" value="Click Here to Play" onclick="location.href=\'(.+?)\'" style="color: #232323;width:220px;height:40px;vertical-align:top;font-size:20px;text-align:center;margin:3px;font-weight:bold;">').findall(link)
        for url in match:
                addDir('[COLOR white]%s[/COLOR]' %name,url,1,iconimage,'','')


def BASE50TOP(url):
        link = OPEN_URL(url)
        match=re.compile('<li class=""><a href="(.+?)">(.+?)</a></li>').findall(link)
        for url,name in match:
                ok = 'topvideos'
                if ok in url:
                        addDir('[COLOR white]%s[/COLOR]' %name,url,55,'','','')


def BASE50TOPL(url):
        link = OPEN_URL(url)
        match=re.compile('.+?</a></div><a href="(.+?)"><img src="(.+?)" alt="(.+?)"  class="tinythumb1" width="53" height="40" align="left" border="1" />').findall(link)
        for url,icon,name in match:
                addDir('[COLOR white]%s[/COLOR]' %name,url,52,icon,'','')


def BASE50GENRE(url):
        link = OPEN_URL(url)
        match=re.compile('<li><a href="(.+?)" title="(.+?)"><div id="tsuper"><span>.+?</span></div><img src=(.+?)></a></li>').findall(link)
        for url,name,icon in match:
                addDir('[COLOR white]%s[/COLOR]' %name,url,57,icon,'','')


def BASE50GENREL(url):
        link = OPEN_URL(url)
        match=re.compile('</td><tr><.+?><a href="(.+?)"><img src="(.+?)" alt=".+?"  class="tinythumb1" width="53" height="40" align="left" border="1" /></a></td><td class="yrr" style="line-height:15px;"><div id="nssl"><a href=".+?">(.+?)</a>').findall(link)
        for url,icon,name in match:
                addDir('[COLOR white]%s[/COLOR]' %name,url,52,icon,'','')
        try:
                match=re.compile('<a href="(.+?)">.+?next &raquo;</a></div>').findall(link)
                for url in match:
                        addDir('[COLOR maroon][B]Next Page>>>[/B][/COLOR]',baseurl50+'/'+url,57,'','','')
        except: pass


def BASE50TV(url):
        link = OPEN_URL(url)
        match=re.compile("<div class='globalblocks'>&bull; <a href='(.+?)'>(.+?)</a></div>").findall(link)
        for url,name in match:
                addDir('[COLOR white]%s[/COLOR]' %name,baseurl50+'/'+url,59,'','','')


def BASE50TVSEA(url):
        link = OPEN_URL(url)
        match=re.compile("<div class='epi'><a href='(.+?)'><span style='.+?'>(.+?)</span><span id='.+?'>(.+?)</span>.+?<span class='airdate'>(.+?)</span>").findall(link)
        for url,name,lin,air in match:
                lin = lin.replace('L',' Links')
                addDir('[COLOR white]%s - %s - Aired %s[/COLOR]' %(name,lin,air),url,52,icon,'','')


def BASE50TVSEARCH():
        try:
                keyb = xbmc.Keyboard('', 'Search TV Shows')
                keyb.doModal()
                if (keyb.isConfirmed()):
                        search = keyb.getText().replace(' ','+')
                        #encode=urllib.quote(search)
                        #print encode
                        url = baseurl50+'/search1.php?keywords='+search+'&btn=Search&ser=528&subs=&lks=&rfrom=0&rto=0&gfrom=0&gto=0&gns='
                        print url
                        link = OPEN_URL(url)
                        match=re.compile('</td><tr><.+?><a href="(.+?)"><img src="(.+?)" alt=".+?"  class="tinythumb1" width="53" height="40" align="left" border="1" /></a></td><td class="yrr" style="line-height:15px;"><div id="nssl"><a href=".+?">(.+?)</a>').findall(link)
                        for url,icon,name in match:
                                addDir('[COLOR white]%s[/COLOR]' %name,url,52,icon,'','')
                        try:
                                match=re.compile('<a href="(.+?)">.+?next &raquo;</a></div>').findall(link)
                                for url in match:
                                        addDir('[COLOR maroon][B]Next Page>>>[/B][/COLOR]',baseurl50+'/'+url,57,'','','')
                        except: pass
        except:
                xbmc.executebuiltin("XBMC.Notification([COLOR gold][B]SORRY NO MATCHES FOUND[/B][/COLOR],,7000,"")")

def BASE50MSEARCH():
        try:
                keyb = xbmc.Keyboard('', 'Search Movies')
                keyb.doModal()
                if (keyb.isConfirmed()):
                        search = keyb.getText().replace(' ','+')
                        #encode=urllib.quote(search)
                        #print encode
                        url = baseurl50+'/search1.php?keywords='+search+'&ser=506&subs=&lks=&rfrom=0&rto=0&gfrom=0&gto=0&gns=&btn=Search'
                        print url
                        link = OPEN_URL(url)
                        match=re.compile('</td><tr><.+?><a href="(.+?)"><img src="(.+?)" alt=".+?"  class="tinythumb1" width="53" height="40" align="left" border="1" /></a></td><td class="yrr" style="line-height:15px;"><div id="nssl"><a href=".+?">(.+?)</a>').findall(link)
                        for url,icon,name in match:
                                addDir('[COLOR white]%s[/COLOR]' %name,url,52,icon,'','')
                        try:
                                match=re.compile('<a href="(.+?)">.+?next &raquo;</a></div>').findall(link)
                                for url in match:
                                        addDir('[COLOR maroon][B]Next Page>>>[/B][/COLOR]',baseurl50+'/'+url,57,'','','')
                        except: pass
        except:
                xbmc.executebuiltin("XBMC.Notification([COLOR gold][B]SORRY NO MATCHES FOUND[/B][/COLOR],,7000,"")")

############################################################################################################################

############################################################################################################################
############################################################################################################################

############################################################################################################################

def BADASS(url):
        addDir('All-Sports',baseurl150+'/forumdisplay.php?19-All-Sports',151,'','','')
        addDir('Pay-Per-View-Free',baseurl150+'/forumdisplay.php?6-Pay-Per-View-Free',151,'','','')
        addDir('Horror-Movies-And-More-Section',baseurl150+'/forumdisplay.php?21-Horror-Movies-And-More-Section',151,'','','')
        addDir('Documentaries',baseurl150+'/forumdisplay.php?14-Documentaries',151,'','','')
        addDir('TV-Shows-New-Seasons',baseurl150+'/forumdisplay.php?11-TV-Shows-New-Seasons',151,'','','')
        addDir('Animation',baseurl150+'/forumdisplay.php?15-Animation',151,'','','')
        addDir('2015-2014-Movies',baseurl150+'/forumdisplay.php?3-2015-2014-Movies',151,'','','')
        addDir('2013-2010',baseurl150+'/forumdisplay.php?7-2013-2010',151,'','','')
        addDir('2009-2000',baseurl150+'/forumdisplay.php?8-2009-2000',151,'','','')
        addDir('90s-and-Older',baseurl150+'/forumdisplay.php?9-90s-and-Older',151,'','','')
        addDir('Badass-Movie-Boxsets',baseurl150+'/forumdisplay.php?20-Badass-Movie-Boxsets',151,'','','')
        addDir('Music-and-Concerts',baseurl150+'/forumdisplay.php?10-Music-and-Concerts',151,'','','')
        addDir('Foreign-Movies',baseurl150+'/forumdisplay.php?22-Foreign-Movies',151,'','','')
        
def BADASSINDEX(url):
        try:
                link = OPEN_URL(url)
                match=re.compile('<a class="title" href="(.+?)" id=".+?">(.+?)</a>').findall(link)
                for url,name in match:
                        name = name.replace('&amp;','&')
                        addDir('[COLOR white]%s[/COLOR]' %name,baseurl150+url,152,'','','')
        except:
                xbmc.executebuiltin("XBMC.Notification([COLOR gold][B]SORRY FORUM DOWN[/B][/COLOR],,7000,"")")
        try:
                match=re.compile('<span class="prev_next"><a rel="next" href="(.+?)" title="(.+?)">').findall(link)
                for url,name in match:
                        addDir('[COLOR white]%s[/COLOR]' %name,baseurl150+url,151,'','','')
        except: pass
       	

def BADASSLINKS(url,name):
        print url
        link = OPEN_URL(url)
        #iconimage = re.compile('<div style="text-align: center;"><img src="(.+?)" border="0" alt="" />').findall(link)
        match = re.compile('<a href="(.+?)" target="_blank">(.+?)</a><br />').findall(link)
        match1 = re.compile('<IFRAME SRC="(.+?)" .+?></IFRAME>').findall(link)
        match2 = re.compile('<iframe src="(.+?)" .+?></iframe>').findall(link)
        try:
                for url in match1:
                        addDir('[COLOR white]%s[/COLOR]' %name,url,1,'','','')
        except: pass
        try:
                for url in match2:
                        addDir('[COLOR white]%s[/COLOR]' %name,url,1,'','','')
        except: pass
        for name,url in match:
                nono = 'www.imdb.com'
                if nono not in url:
                        addDir('[COLOR white]%s[/COLOR]' %name,url,1,'','','')


############################################################################################################################

############################################################################################################################
############################################################################################################################

############################################################################################################################        

def BASE200():
        addDir('Newest Movies',baseurl200+'/movies',201,'','','')
        addDir('Popular Movies',baseurl200+'/movies/popular',201,'','','')
        addDir('Movies By IMDB Rating',baseurl200+'/movies/imdb_rating',201,'','','')
        addDir('Movies Genre',baseurl200,204,'','','')
        addDir('Movies ABC',baseurl200+'/movies/abc',201,'','','')
        addDir('Newest TV Shows',baseurl200+'/tv-shows',201,'','','')
        addDir('TV Shows By IMDB Rating',baseurl200+'/tv-shows/imdb_rating',201,'','','')
        addDir('TV Shows Genre',baseurl200,205,'','','')
        addDir('TV Shows ABC',baseurl200+'/tv-shows/abc',201,'','','')
        addDir('Search Movies','url',209,'','','')
        addDir('Search TV','url',210,'','','')
        
def BASE200INDEX(url):
        try:
                link = OPEN_URL(url)
                match=re.compile('<a href="(.+?)" class="spec-border-ie" title="">\n\t\t\t\t\t\t\t\t\t\t\t\t\t<img class=".+?"  src="(.+?)" alt="Watch (.+?) Online".+?>').findall(link)
                for url,icon,name in match:
                        tv = 'http://www.allcinemamovies.com/show/'
                        name = name.replace('&amp;','&')
                        if tv in url:
                                addDir('[COLOR white]%s[/COLOR]' %name,url,206,icon,'','')
                        else:
                                addDir('[COLOR white]%s[/COLOR]' %name,url,202,icon,'','')
        except:
                xbmc.executebuiltin("XBMC.Notification([COLOR gold][B]SORRY SITE DOWN[/B][/COLOR],,7000,"")")

        try:
                match=re.compile('<li><a href="(.+?)".+?>&raquo;</a></li>').findall(link)
                for url in match:
                        addDir('[COLOR maroon]Next Page>>>[/COLOR]',url,201,'','','')
        except: pass


def BASE200MHOSTS(url,iconimage):
        link = OPEN_URL(url)
        match=re.compile('<span>(.+?)</span></a>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</h5>\n\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t<ul class="filter" style="width:200px;float:right;margin-top: 0px;">\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<li class="current right" style="float:right"><a href="(.+?)" target="_blank">').findall(link)
        for name,url in match:
                name = name.replace('&amp;','&')
                addDir('[COLOR white]%s[/COLOR]' %name,url,203,iconimage,'','')


def BASE200L(url,iconimage):
        link = OPEN_URL(url)
        match=re.compile('<IFRAME.+?"(.+?)".+?></IFRAME>').findall(link)
        match1=re.compile('<iframe.+?src="(.+?)".+?></iframe>').findall(link)
        match2=re.compile("<a href='(.+?)' target='_blank' style='.+?'>Click here to play this video</a>").findall(link)
        try:
                for url in match:
                        addDir('[COLOR white]%s[/COLOR]' %name,url,1,iconimage,'','')
        except: pass

        try:
                for url in match1:
                        addDir('[COLOR white]%s[/COLOR]' %name,url,1,iconimage,'','')
        except: pass

        try:
                for url in match2:
                        addDir('[COLOR white]%s[/COLOR]' %name,url,1,iconimage,'','')
        except: pass


def BASE200MGENRE(url):
        link = OPEN_URL(url)
        match=re.compile('<li><a href="(.+?)">(.+?)</a></li>').findall(link)
        for url,name in match:
                name = name.replace('&amp;','&')
                mov = 'http://www.allcinemamovies.com/movie-tags/'
                if mov in url:
                        addDir('[COLOR white]%s[/COLOR]' %name,url,201,'','','')


def BASE200TGENRE(url):
        link = OPEN_URL(url)
        match=re.compile('<li><a href="(.+?)">(.+?)</a></li>').findall(link)
        for url,name in match:
                name = name.replace('&amp;','&')
                tv = 'http://www.allcinemamovies.com/tv-tags/'
                if tv in url:
                        addDir('[COLOR white]%s[/COLOR]' %name,url,201,'','','')


def BASE200TSEA(url,iconimage):
        link = OPEN_URL(url)
        match=re.compile("<li ><a href='(.+?)'>(.+?)</a></li>").findall(link)
        for url,name in match:
                name = name.replace('&amp;','&')
                addDir('[COLOR white]%s[/COLOR]' %name,url,207,iconimage,'','')


def BASE200TEP(url,iconimage):
        link = OPEN_URL(url)
        match=re.compile('<a class="link" href="(.+?)" title="(.+?)"><span class="tv_episode_name">(.+?)</span>').findall(link)
        for url,description,name in match:
                name = name.replace('&amp;','&')
                addDir('[COLOR white]%s[/COLOR]' %name,url,208,iconimage,'',description)


def BASE200THOSTS(url,iconimage):
        link = OPEN_URL(url)
        match=re.compile('<span>(.+?)</span></a>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</h5>\n\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\t<ul id="filter" style="width:200px;float:right;margin-top: 0px;">\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<li class="current" style="float:right"><a href="(.+?)" target="_blank">Watch Now</a>').findall(link)
        for name,url in match:
                name = name.replace('&amp;','&')
                addDir('[COLOR white]%s[/COLOR]' %name,url,203,iconimage,'','')

def BASE200MSEARCH():
        try:
                keyb = xbmc.Keyboard('', 'Movie Search')
                keyb.doModal()
                if (keyb.isConfirmed()):
                        search = keyb.getText().replace(' ','-')
                        #encode=urllib.quote(search)
                        #print encode
                        url = baseurl200+'/movie/'+search
                        print url
                        link = OPEN_URL(url)
                        BASE200MHOSTS(url,name)
        except:
                xbmc.executebuiltin("XBMC.Notification([COLOR gold][B]SORRY NO MATCHES FOUND[/B][/COLOR],,7000,"")")


def BASE200TSEARCH():
        try:
                keyb = xbmc.Keyboard('', 'Movie Search')
                keyb.doModal()
                if (keyb.isConfirmed()):
                        search = keyb.getText().replace(' ','-')
                        #encode=urllib.quote(search)
                        #print encode
                        url = baseurl200+'/show/'+search
                        print url
                        link = OPEN_URL(url)
                        BASE200TSEA(url,name)
        except:
                xbmc.executebuiltin("XBMC.Notification([COLOR gold][B]SORRY NO MATCHES FOUND[/B][/COLOR],,7000,"")")
        
       
############################################################################################################################

############################################################################################################################
############################################################################################################################

############################################################################################################################

def SS():
        addDir('Alluc Super Search',baseurl102,102,'','','')
        addDir('Filmovizija Search','url',105,'','','')
        addDir('Vodlocker Search',baseurl101,101,'','','')
        addDir('Allcinemamovies Search','url',106,'','','')
        
        
def FILMOVSEARCH():
        addDir('Filmovizija TV Search','url',60,'','','')
        addDir('Filmovizija Movie Movie Search','url',61,'','','')


def ALLCINSEARCH():
        addDir('Allcinemamovies TV Search','url',210,'','','')
        addDir('Allcinemamovies Search','url',209,'','','')


def VODLOCKERSEARCH(url):
        keyb = xbmc.Keyboard('', 'Search Vodlocker')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText().replace('%20','+')
                #encode=urllib.quote(search)
                #print encode
                url = baseurl101+'/stream/'+search
                match=re.compile('<a href=".+?">(.+?)</a> <br>  <span style="font-size: 13px">.+?</span> \n  <br>\n<span style="font-size: 13px;color:grey;">(.+?)</span>').findall(net.http_GET(url).content) 
                for name,url in match:
                        url = url.replace('   ','')
                        addDir('[B][COLOR yellow]%s[/COLOR][/B]' %name,url,1,'','','')
                        


def ALLUCSEARCH(url):
        try:
                keyb = xbmc.Keyboard('', 'Super Search')
                keyb.doModal()
                if (keyb.isConfirmed()):
                        search = keyb.getText().replace(' ','+')
                        #encode=urllib.quote(search)
                        #print encode
                        url = baseurl102+'/stream/'+search
                        print url
                        link = OPEN_URL(url)
                        ALLUCRESULTS(url,name)
        except:
                xbmc.executebuiltin("XBMC.Notification([COLOR gold][B]SORRY NO MATCHES FOUND[/B][/COLOR],,7000,"")")
               


def ALLUCRESULTS(url,name):
        link = OPEN_URL(url)
        match=re.compile('<a href="(.+?)" target=_blank>(.+?)</a>').findall(net.http_GET(url).content) 
        for url,name in match:
                nono = 'Video On Demand'
                if nono not in name:
                        addDir('[B][COLOR yellow]%s[/COLOR][/B]' %name,baseurl102+url,104,'','','')
                        print url
        try:
                match=re.compile('<li><a href="(.+?)" rel=.+?>(.+?)</a></li>').findall(link)
                
                for url,name in match:
                        addDir('[B][COLOR yellow]%s Page[/COLOR][/B]' %name,baseurl102+url,103,'','','')
        except: pass


def ALLUCLINK(url):
        link = OPEN_URL(url)
        match=re.compile('<textarea onClick=".+?">(.+?)\n</textarea>').findall(net.http_GET(url).content)
        for url in match:
                addDir('[COLOR yellow]%s[/COLOR]' %name,url,1,'','','')

############################################################################################################################

############################################################################################################################
############################################################################################################################

############################################################################################################################

def IPTV():
        addDir('www.hack-sat.com',baseurl5001,5001,'','','')
        addDir('iptv.filmover.com',baseurl5002,5002,'','','')
        #addDir('www.iptvsharing.com/2015/07/sport-klub-iptv-links-m3u8.html',baseurl5010,5003,'','','')
        #addDir('www.iptvsharing.com/2015/07/sport-klub-iptv-links-m3u8.html',baseurl5020,5003,'','','')
        

def BASE5001(url):
        link = OPEN_URL(url)
        match=re.compile('#EXTINF.+?,(.+?)\n(.+?)\n').findall(link)
        for name,url in match:
                addDir('[COLOR white]%s[/COLOR]' %name,url,1,'','','')

def BASE5002(url):
        link = OPEN_URL(url)
        match=re.compile('<li class=".+?"><a href="(.+?)" >(.+?)</a>.+?\n</li>').findall(link)
        for url,name in match:
                ok = 'xbmc'
                if ok in url:
                        addDir('[COLOR white]%s[/COLOR]' %name,url,5003,'','','')

def BASE5002L(url):
        link = OPEN_URL(url)
        match=re.compile('#EXTINF:.+?,(.+?) http://(.+?) ').findall(link)
        match1=re.compile('#EXTINF:.+?,(.+?) rtmp://(.+?) ').findall(link)
        try:
                for name,url in match:
                        addDir('[COLOR white]%s[/COLOR]' %name,'http://'+url,1,'','','')
        except: pass

        try:
                for name,url in match1:
                        addDir('[COLOR white]%s[/COLOR]' %name,'rtmp://'+url,1,'','','')
        except: pass

############################################################################################################################

############################################################################################################################
############################################################################################################################

############################################################################################################################

def RESOLVE(name,url):
    url1 = urlresolver.resolve(url)
    if url1:
        try:
            liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
            liz.setInfo(type='Video', infoLabels={'Title':description})
            liz.setProperty("IsPlayable","true")
            liz.setPath(url1)
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
        except: pass
    else:
        liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
        liz.setInfo(type='Video', infoLabels={'Title':description})
        liz.setProperty("IsPlayable","true")
        liz.setPath(url)
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



def addDir(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name,"Plot":description} )
        liz.setProperty('fanart_image', fanart)
        if mode==1 or mode==8:
            liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok



def addLink(name,url,mode,iconimage,fanart,description=''):
        #u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        return ok


def OPEN_URL(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent' , "Magic Browser")
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link

def setView(content, viewType):
        ''' Why recode whats allready written and works well,
        Thanks go to Eldrado for it '''

        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
        #if addon.get_setting('auto-view') == 'true':

        #    print addon.get_setting(viewType)
        #    if addon.get_setting(viewType) == 'Info':
        #        VT = '515'
        #    elif addon.get_setting(viewType) == 'Wall':
        #        VT = '501'
        #    elif viewType == 'default-view':
        #        VT = addon.get_setting(viewType)

        #    print viewType
        #    print VT
        
        #    xbmc.executebuiltin("Container.SetViewMode(%s)" % ( int(VT) ) )

        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING )
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_PROGRAM_COUNT )
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RUNTIME )
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_GENRE )
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_MPAA_RATING )

           
params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None


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
   
        
if mode==None or url==None or len(url)<1:
        INDEX()

elif mode==1:
        RESOLVE(name,url)

elif mode==50:
        BASE50(url)

elif mode==51:
        BASE50MINDEX(url)

elif mode==52:
        BASE50MHOSTS(url,iconimage)

elif mode==53:
        BASE50MFINAL(url,iconimage)

elif mode==54:
        BASE50TOP(url)

elif mode==55:
        BASE50TOPL(url)

elif mode==56:
        BASE50GENRE(url)

elif mode==57:
        BASE50GENREL(url)

elif mode==58:
        BASE50TV(url)

elif mode==59:
        BASE50TVSEA(url)

elif mode==60:
        BASE50TVSEARCH()

elif mode==61:
        BASE50MSEARCH()

elif mode==100:
        SS()

elif mode==101:
        VODLOCKERSEARCH(url)

elif mode==102:
        ALLUCSEARCH(url)

elif mode==103:
        ALLUCRESULTS(url,name)

elif mode==104:
        ALLUCLINK(url)

elif mode==105:
        FILMOVSEARCH()

elif mode==106:
        ALLCINSEARCH()

elif mode==150:
        BADASS(url)

elif mode==151:
        BADASSINDEX(url)

elif mode==152:
        BADASSLINKS(url,name)

elif mode==200:
        BASE200()

elif mode==201:
        BASE200INDEX(url)

elif mode==202:
        BASE200MHOSTS(url,iconimage)

elif mode==203:
        BASE200L(url,iconimage)

elif mode==204:
        BASE200MGENRE(url)

elif mode==205:
        BASE200TGENRE(url)

elif mode==206:
        BASE200TSEA(url,iconimage)

elif mode==207:
        BASE200TEP(url,iconimage)

elif mode==208:
        BASE200THOSTS(url,iconimage)

elif mode==209:
        BASE200MSEARCH()

elif mode==210:
        BASE200TSEARCH()

elif mode==5000:
        IPTV()

elif mode==5001:
        BASE5001(url)

elif mode==5002:
        BASE5002(url)

elif mode==5003:
        BASE5002L(url)
        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
