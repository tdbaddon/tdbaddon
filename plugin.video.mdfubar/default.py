import urllib,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,os
import urlresolver
import requests
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net
from metahandler import metahandlers

#F.U.B.A.R - By Mucky Duck (07/2015)

addon_id='plugin.video.mdfubar'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id, sys.argv)
Addon = xbmcaddon.Addon(addon_id)
art = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
baseurl = 'dummy'
net = Net()
metaset = selfAddon.getSetting('enable_meta')
metaget = metahandlers.MetaData(preparezip=False)
User_Agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'


baseurl1 = 'http://kodimediaportal.ml/smf/index.php?board=2.0'
baseurl2 = 'https://www.youtube.com'

#http://watch-free-movies-streaming.com/
baseurl101 = 'http://vodlocker.tv'
baseurl102 = 'http://www.alluc.com'
#http://movies-search-engine.com/
#http://watch-streaming-movies.com/
#http://wawashare.com/
##http://stagevu.com/
##http://online-tvseries.com/


baseurl350 = 'http://documentaryaddict.com/'
baseurl450 = 'http://concert.ga'


#http://misspremieretv.com/2014/09/
#http://series-cravings.me/
#http://www.tvids.net/
#http://tvstream.ch/
#http://geektv.me/
#http://tvoox.com/
#http://watchtvlinks.ag/
########http://fullepisode.info/
#http://hdfull.tv
##http://movies.documentaryvideosworld.com/
##https://www3.iconcerts.com
##https://www.reddit.com/r/fullconcerts/
##http://music.naij.com/
##https://www.youtube.com/playlist?list=PLD6BF044AE5B386D2
##https://www.itstream.tv/play/NDIyMjc=
##http://www.veoh.com/
##https://www.youtube.com/channel/UCAsanw03kzGRhAG4AvjVA_Q/playlists?sort=dd&view=1
##https://www.youtube.com/playlist?list=PL0vM4tWpymIU4bVBv9XJG26Tbz33KB7Rs
##https://www.youtube.com/playlist?list=PLR8X0-qEtOCf8aeA-6bEBHNNwZv0GqvyZ
##https://www.youtube.com/user/TheRealConcertKing/playlists?view=1&sort=dd real concert king
##https://www.youtube.com/user/GreenDayConcerts/playlists green day
##http://abelgaloismuse.blogspot.co.uk/p/concerts-full.html
baseurl500 = 'http://newsoapcity.blogspot.co.uk'
baseurl510 = 'http://uksoapshare.blogspot.co.uk'
##http://tvlog.link/ benders
##http://tv-show-online.sx/
##http://www.cbc.ca/

##http://luv-movies.com/
##http://primeflicks.me/ looks like vodx
##http://funtastic-vids.com/ hd movies
##http://free-on-line.org/ hd movies
##http://putlocker.tn/
##http://www.movie25.cz/
##http://worldfree4uk.com/
##http://www.vumoo.me/
##http://motionempire.org/  mix of everything
##http://crackmovies.com/
##http://k-films.net/
##http://sceper.ws/2015/06/ted-2-2015-1080p-hdcam-x264-ac3-mrg.html
##http://webmaster-connect.me/2014/08/fast-n-loud-s05e01-chopped-and-dropped-model-a-part1.html
##http://watchseries-online.ch/
##http://watchmovies-online.ch/
#http://watchmovies-online.ch/hellboy-2004/  1080p
#http://tvoox.com/
##http://www.movie25.cz/
##http://rlsbb.com/fast-n-loud-s05e01-720p-hdtv-x264-dhd/  hd bluray 1080 movies
##http://www.newvideoz.com/
##http://board.dailyflix.net/  forum hd links
baseurl50 =  'http://www.filmovizija.club' #'http://www.filmovizija.in'
baseurl150 = 'http://www.badassmovies4u.com/'
baseurl200 = 'http://www.allcinemamovies.com'
baseurl250 = 'http://moviesearth.net'
baseurl300 = 'http://ultra-vid.com'
baseurl400 = 'http://pandamovie.net'

baseurl5001 = 'http://www.hack-sat.com/iptv.php'
#baseurl5001 = 'http://select-pedia.com/tutos/tag/sport/'
#baseurl50002 = 'http://www.iptvlinks.com/2014/12/super-torrent-stream.html'
baseurl5002 = 'http://iptv.filmover.com'
baseurl5010 = 'http://www.iptvsharing.com/2015/07/sport-klub-iptv-links-m3u8.html'
baseurl5020 = 'http://67.159.5.242/ip-1/encoded/Oi8vcGFzdGViaW4uY29tL2hxNlBKWVpS'
baseurl5030 = 'http://free-links-iptv.blogspot.co.uk'
##http://www.iptvsportt.com/
##http://www.ramalin.com/
##http://iptvplaylists.com/category/m3u/
baseurl5040 = 'http://iptvapps.blogspot.co.uk/2015/06/playlist-m3u-662015.html'



def INDEX():
        addDir('[COLOR cyan]ultra-vid.com[/COLOR]',baseurl300,300,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]pandamovie.net[/COLOR]','url',400,art+'panda.png',art+'f1.jpg','')
        addDir('[COLOR cyan]www.badassmovies4u.com[/COLOR]',baseurl150,150,art+'bad.png',art+'f1.jpg','')
        addDir('[COLOR cyan]documentaryaddict.com[/COLOR]',baseurl350,350,art+'da.png',art+'f1.jpg','')
        addDir('[COLOR cyan]newsoapcity.blogspot.co.uk[/COLOR]',baseurl500,500,art+'wls.png',art+'f1.jpg','')
        addDir('[COLOR cyan]uksoapshare.blogspot.co.uk[/COLOR]',baseurl510,510,art+'wls',art+'f1.jpg','')
        #addDir('[COLOR cyan]Concerts[/COLOR]','url',3,art+'concert.png',art+'f1.jpg','')
        #addDir('[COLOR cyan]moviesearth.net[/COLOR]','url',250,'',art+'f1.jpg','')
        addDir('[COLOR cyan]www.filmovizija.in[/COLOR]',baseurl150,50,'',art+'f1.jpg','')
        addDir('[COLOR cyan]www.allcinemamovies.com[/COLOR]','url',200,'',art+'f1.jpg','')
        addDir('[COLOR cyan]kodimediaportal.ml[/COLOR]',baseurl1,4000,'',art+'f1.jpg','')
        addDir('[COLOR cyan]Super Search[/COLOR]','url',100,'',art+'f1.jpg','')
        addDir('[COLOR cyan]IPTV[/COLOR]','url',5000,'',art+'f1.jpg','')
        
        
def CONINDEX():
        #addDir('[COLOR cyan]#Concert[/COLOR]',baseurl450+'/channel/UCAsanw03kzGRhAG4AvjVA_Q/playlists?sort=dd&view=1',451,'',art+'f1.jpg','')
        addDir('[COLOR cyan]concert.ga[/COLOR]','url',450,art+'concert.png',art+'f1.jpg','')
        #addDir('[COLOR cyan]HD Movies[/COLOR]',baseurl400+'/watch-hd-movies-online-free',401,'',art+'f1.jpg','')
############################################################################################################################

############################################################################################################################

def BASE50(url):
        addDir('[COLOR cyan]NEW[/COLOR]',baseurl50,51,'',art+'f1.jpg','')
        addDir('[COLOR cyan]TOP 20[/COLOR]',baseurl50,54,'',art+'f1.jpg','')
        addDir('[COLOR cyan]MOVIE GENRE[/COLOR]',baseurl50+'/browse-movies-videos-1-date.html',56,'',art+'f1.jpg','')
        addDir('[COLOR cyan]TV SHOWS[/COLOR]',baseurl50+'/tvshows.html',58,'',art+'f1.jpg','')
        addDir('[COLOR cyan]DOCUMENTARY[/COLOR]',baseurl50+'/browse-Documentary-videos-1-date.html',57,'',art+'f1.jpg','')
        addDir('[COLOR cyan]ANIMATED[/COLOR]',baseurl50+'/browse-animated-videos-1-date.html',57,'',art+'f1.jpg','')
        addDir('[COLOR cyan]SEARCH TV[/COLOR]','url',60,'',art+'f1.jpg','')
        addDir('[COLOR cyan]SEARCH MOVIES[/COLOR]','url',61,'',art+'f1.jpg','')
        

def BASE50MINDEX(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore')
        match=re.compile('<a href="(.*?)"><img src="(.*?)" alt="(.*?)" .*?</div>(.*?)<div id="titcategs">').findall(link)
        for url,icon,name,dis, in match:
                name = name.replace('&amp;','&')
                addDir('[COLOR white]%s[/COLOR]' %name,url,52,icon,art+'f1.jpg',dis)


def BASE50MHOSTS(url,iconimage):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore')
        match=re.compile('<h9>.+?</h9></td>\n<td width="90" style=".+?"><span class="fullm"><a href="(.+?)" title="(.+?)" target="_blank">Watch here</a>').findall(link)
        for url,name in match:
                name = name.replace('&amp;','&').replace('Movie - ','')
                addDir('[COLOR white]%s[/COLOR]' %name,baseurl50+url,53,iconimage,art+'f1.jpg','')


def BASE50MFINAL(url,iconimage):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore')
        match=re.compile('<input type="button" value="Click Here to Play" onclick="location.href=\'(.+?)\'" style="color: #232323;width:220px;height:40px;vertical-align:top;font-size:20px;text-align:center;margin:3px;font-weight:bold;">').findall(link)
        for url in match:
                addDir('[COLOR white]%s[/COLOR]' %name,url,1,iconimage,art+'f1.jpg','')


def BASE50TOP(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore')
        match=re.compile('<li class=""><a href="(.+?)">(.+?)</a></li>').findall(link)
        for url,name in match:
                ok = 'topvideos'
                if ok in url:
                        addDir('[COLOR white]%s[/COLOR]' %name,url,55,'',art+'f1.jpg','')


def BASE50TOPL(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore')
        match=re.compile('.+?</a></div><a href="(.+?)"><img src="(.+?)" alt="(.+?)"  class="tinythumb1" width="53" height="40" align="left" border="1" />').findall(link)
        for url,icon,name in match:
                addDir('[COLOR white]%s[/COLOR]' %name,url,52,icon,art+'f1.jpg','')


def BASE50GENRE(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore')
        match=re.compile('<li><a href="(.+?)" title="(.+?)"><div id="tsuper"><span>.+?</span></div><img src=(.+?)></a></li>').findall(link)
        for url,name,icon in match:
                addDir('[COLOR white]%s[/COLOR]' %name,url,57,icon,art+'f1.jpg','')


def BASE50GENREL(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore')
        match=re.compile('</td><tr><.+?><a href="(.+?)"><img src="(.+?)" alt=".+?"  class="tinythumb1" width="53" height="40" align="left" border="1" /></a></td><td class="yrr" style="line-height:15px;"><div id="nssl"><a href=".+?">(.+?)</a>').findall(link)
        for url,icon,name in match:
                addDir('[COLOR white]%s[/COLOR]' %name,url,52,icon,art+'f1.jpg','')
        try:
                match=re.compile('<a href="(.+?)">.+?next &raquo;</a></div>').findall(link)
                for url in match:
                        addDir('[COLOR maroon][B]Next Page>>>[/B][/COLOR]',baseurl50+'/'+url,57,'',art+'f1.jpg','')
        except: pass


def BASE50TV(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore')
        match=re.compile("<div class='globalblocks'>&bull; <a href='(.+?)'>(.+?)</a></div>").findall(link)
        for url,name in match:
                addDir('[COLOR white]%s[/COLOR]' %name,baseurl50+'/'+url,59,'',art+'f1.jpg','')


def BASE50TVSEA(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore')
        match=re.compile("<div class='epi'><a href='(.+?)'><span style='.+?'>(.+?)</span><span id='.+?'>(.+?)</span>.+?<span class='airdate'>(.+?)</span>").findall(link)
        for url,name,lin,air in match:
                lin = lin.replace('L',' Links')
                addDir('[COLOR white]%s - %s - Aired %s[/COLOR]' %(name,lin,air),url,52,icon,art+'f1.jpg','')


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
                        link = link.encode('ascii', 'ignore')
                        match=re.compile('</td><tr><.+?><a href="(.+?)"><img src="(.+?)" alt=".+?"  class="tinythumb1" width="53" height="40" align="left" border="1" /></a></td><td class="yrr" style="line-height:15px;"><div id="nssl"><a href=".+?">(.+?)</a>').findall(link)
                        for url,icon,name in match:
                                addDir('[COLOR white]%s[/COLOR]' %name,url,52,icon,art+'f1.jpg','')
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
                        link = link.encode('ascii', 'ignore')
                        match=re.compile('</td><tr><.+?><a href="(.+?)"><img src="(.+?)" alt=".+?"  class="tinythumb1" width="53" height="40" align="left" border="1" /></a></td><td class="yrr" style="line-height:15px;"><div id="nssl"><a href=".+?">(.+?)</a>').findall(link)
                        for url,icon,name in match:
                                addDir('[COLOR white]%s[/COLOR]' %name,url,52,icon,art+'f1.jpg','')
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
        addDir('[COLOR cyan]All-Sports[/COLOR]',baseurl150+'/forumdisplay.php?19-All-Sports',151,art+'bad.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Pay-Per-View-Free[/COLOR]',baseurl150+'/forumdisplay.php?6-Pay-Per-View-Free',151,art+'bad.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Horror-Movies-And-More-Section[/COLOR]',baseurl150+'/forumdisplay.php?21-Horror-Movies-And-More-Section',151,art+'bad.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Documentaries[/COLOR]',baseurl150+'/forumdisplay.php?14-Documentaries',151,art+'bad.png',art+'f1.jpg','')
        #addDir('TV-Shows-New-Seasons',baseurl150+'/forumdisplay.php?11-TV-Shows-New-Seasons',151,art+'badi.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Animation[/COLOR]',baseurl150+'/forumdisplay.php?15-Animation',151,art+'bad.png',art+'f1.jpg','')
        addDir('[COLOR cyan]2015-2014-Movies[/COLOR]',baseurl150+'/forumdisplay.php?3-2015-2014-Movies',151,art+'bad.png',art+'f1.jpg','')
        addDir('[COLOR cyan]2013-2010[/COLOR]',baseurl150+'/forumdisplay.php?7-2013-2010',151,art+'bad.png',art+'f1.jpg','')
        addDir('[COLOR cyan]2009-2000[/COLOR]',baseurl150+'/forumdisplay.php?8-2009-2000',151,art+'bad.png',art+'f1.jpg','')
        addDir('[COLOR cyan]90s-and-Older[/COLOR]',baseurl150+'/forumdisplay.php?9-90s-and-Older',151,art+'bad.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Badass-Movie-Boxsets[/COLOR]',baseurl150+'/forumdisplay.php?20-Badass-Movie-Boxsets',151,art+'bad.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Music-and-Concerts[/COLOR]',baseurl150+'/forumdisplay.php?10-Music-and-Concerts',151,art+'bad.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Foreign-Movies[/COLOR]',baseurl150+'/forumdisplay.php?22-Foreign-Movies',151,art+'bad.png',art+'f1.jpg','')
        
def BADASSINDEX(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore').decode('ascii')
        match=re.compile('class="title" href="(.*?)" id=".*?">(.*?)</a>').findall(link)
        items = len(match)
        for url,name in match:
                if 'How To Watch' not in name:
                        if 'There is No Mal' not in name:
                                name = name.replace('Help Badassmovies Facebook Page Like Us Please!!!!!','[COLOR cyan]Help Badassmovies Facebook Page Like Us Please!!!!![/COLOR]')
                                name = name.replace('&amp;','&')
                                addDir2(name,baseurl150+url,152,'',items)
        try:
                url=re.compile('<span class="prev_next"><a rel="next" href="(.+?)" title=".+?">').findall(link)
                url = url[0]
                name=re.compile('<span class="prev_next"><a rel="next" href=".+?" title="(.+?)">').findall(link)
                name = name[0]
                addDir('[COLOR cyan]%s[/COLOR]' %name,baseurl150+url,151,art+'bad.png',art+'f1.jpg','')
        except: pass
       	

def BADASSLINKS(url,name):
        link = OPEN_URL(url)
        match = re.compile('<a href="(.+?)" target="_blank">.+?</a><br />').findall(link)
        match1 = re.compile('<IFRAME SRC="(.+?)" .+?></IFRAME>').findall(link)
        match2 = re.compile('<iframe src="(.+?)" .+?></iframe>').findall(link)
        try:
                for url in match1:
                        if 'youtube' not in url:
                                addDir2(name,url,1,'',len(match))
        except: pass
        try:
                for url in match2:
                        if 'youtube' not in url:
                                addDir2(name,url,1,'',len(match))
        except: pass
        for url in match:
                nono = 'www.imdb.com'
                nono2 = 'http://www.badassmovies4u.com/'
                if nono not in url:
                        print url
                        if nono2 not in url:
                                addDir2(name,url,1,'',len(match))


############################################################################################################################

############################################################################################################################
############################################################################################################################

############################################################################################################################        

def BASE200():
        addDir('[COLOR cyan]Newest Movies[/COLOR]',baseurl200+'/movies',201,'',art+'f1.jpg','')
        addDir('[COLOR cyan]Popular Movies[/COLOR]',baseurl200+'/movies/popular',201,'',art+'f1.jpg','')
        addDir('[COLOR cyan]Movies By IMDB Rating[/COLOR]',baseurl200+'/movies/imdb_rating',201,'',art+'f1.jpg','')
        addDir('[COLOR cyan]Movies Genre[/COLOR]',baseurl200,204,'',art+'f1.jpg','')
        addDir('[COLOR cyan]Movies ABC[/COLOR]',baseurl200+'/movies/abc',201,'',art+'f1.jpg','')
        addDir('[COLOR cyan]Newest TV Shows[/COLOR]',baseurl200+'/tv-shows',201,'',art+'f1.jpg','')
        addDir('[COLOR cyan]TV Shows By IMDB Rating[/COLOR]',baseurl200+'/tv-shows/imdb_rating',201,'',art+'f1.jpg','')
        addDir('[COLOR cyan]TV Shows Genre[/COLOR]',baseurl200,205,'',art+'f1.jpg','')
        addDir('[COLOR cyan]TV Shows ABC[/COLOR]',baseurl200+'/tv-shows/abc',201,'',art+'f1.jpg','')
        addDir('[COLOR cyan]Search Movies[/COLOR]','url',209,'',art+'f1.jpg','')
        addDir('[COLOR cyan]Search TV[/COLOR]','url',210,'',art+'f1.jpg','')
        
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
                url=re.compile('<li><a href="(.+?)".+?>&raquo;</a></li>').findall(link)[-1]
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

def BASE250():
        addDir('Genre',baseurl250,251,'','','')


def BASE250GENRE(url):
        link = OPEN_URL(url)
        match=re.compile('<li id=".+?" class=".+?"><a href="(.+?)">(.+?)</a></li>').findall(link)
        for url,name in match:
                name = name.replace('&amp;','&').replace("&#8217;","'").replace('&#8211;','-')
                cat = '/category/'
                if cat in url:
                        addDir('[COLOR white]%s[/COLOR]' %name,url,252,'','','')



def BASE250INDEX(url):
        try:
                link = OPEN_URL(url)
                match=re.compile('<a href="(.+?)" title="(.+?)">').findall(link)
                items = len(match)
                for url,name in match:
                        name = name.replace('&amp;','&').replace("&#8217;","'").replace('&#8211;','-')
                        addDir2(name,url,253,'',items)
                        print url
        except:
                xbmc.executebuiltin("XBMC.Notification([COLOR gold][B]SORRY SITE DOWN[/B][/COLOR],,7000,"")")

        try:
                match=re.compile("<a rel='.+?' class='.+?' href='(.+?)'>(.+?)</a>").findall(link)
                for url,name in match:
                        addDir('[COLOR maroon]Page %s >>>[/COLOR]' %name,url,252,'','','')
        except: pass



def BASE250L(url):
        link = OPEN_URL(url)
        match=re.compile('<iframe src="(.+?)".+?></iframe>').findall(link)
        for url in match:
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                streamlink = urlresolver.resolve(urllib2.urlopen(req).url)
                print streamlink
                url = streamlink
                ok=True
                liz=xbmcgui.ListItem(name, iconImage=icon,thumbnailImage=icon); liz.setInfo( type="Video", infoLabels={ "Title": name } )
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=str(url),listitem=liz)
                xbmc.Player().play(streamlink,liz,False)



############################################################################################################################

############################################################################################################################



def BASE300():
        addDir('[COLOR cyan]New Movies[/COLOR]',baseurl300+'/category/new-release/',301,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]New on BluRay[/COLOR]',baseurl300+'/category/new-on-bluray/',301,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Search[/COLOR]','url',303,art+'ultra.png',art+'f1.jpg','')
        #addDir('In Theaters',baseurl300+'/in-theaters/',301,'','','')
        addDir('[COLOR cyan]Action[/COLOR]',baseurl300+'/category/movies/action/',301,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Adventure[/COLOR]',baseurl300+'/category/adventure/',301,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Animation[/COLOR]',baseurl300+'/category/movies/animation/',301,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Bollywood[/COLOR]',baseurl300+'/category/movies/hindi/',301,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Chick Flicks[/COLOR]',baseurl300+'/category/movies/rom-com/',301,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Comedy[/COLOR]',baseurl300+'/category/movies/comedy/',301,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Crime[/COLOR]',baseurl300+'/category/movies/crime/',301,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Documentaries[/COLOR]',baseurl300+'/category/movies/documentary/',301,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Drama[/COLOR]',baseurl300+'/category/movies/drama/',301,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Family[/COLOR]',baseurl300+'/category/movies/family/',301,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Fantasy[/COLOR]',baseurl300+'/category/movies/fantasy/',301,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Foreign[/COLOR]',baseurl300+'/category/foreign/',301,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Horror[/COLOR]',baseurl300+'/category/movies/horror/',301,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Romance[/COLOR]',baseurl300+'/category/movies/romance-movies/',301,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Sci-Fi[/COLOR]',baseurl300+'/category/movies/sci-fi/',301,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Super Hero[/COLOR]',baseurl300+'/category/superhero/',301,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Thriller[/COLOR]',baseurl300+'/category/movies/thriller/',301,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]War[/COLOR]',baseurl300+'/category/movies/action/war/',301,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Western[/COLOR]',baseurl300+'/category/movies/action/western-action/',301,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]WWE / UFC[/COLOR]',baseurl300+'/category/ufc/',301,art+'ultra.png',art+'f1.jpg','')


        
        

def BASE300INDEX(url):
        try:
                link = OPEN_URL(url)
                link = link.encode('ascii', 'ignore')
                match=re.compile('<span class="itemdets"> <a href="(.+?)" title="(.+?)"> </span>').findall(link)
                items = len(match)
                for url,name in match:
                        name = name.replace('&#038;','&').replace("&#8217;","'").replace('&#8211;','-').replace('( BluRay ) ','').replace('( BluRay added ) ','').replace('NEW> ','').replace('( ENGLISH ) ','').replace('( HDTS ) ','').replace('( BLURAY added) ','')
                        addDir2(name,url,302,'',items)

        except:
                xbmc.executebuiltin("XBMC.Notification([COLOR gold][B]SORRY SITE DOWN[/B][/COLOR],,7000,"")")
        try:
                match=re.compile('<a class="next page-numbers" href="(.+?)">(.+?)</a>').findall(link)
                name = name.replace(' \xc2\xbb','')
                for url, name in match:
                        addDir('[COLOR cyan]%s[/COLOR]' %name,url,301,art+'ultra.png',art+'f1.jpg','')
        except: pass


def BASE300L(url,name):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore')
        match=re.compile('<p style="text-align: center;"><a href="(.+?)" target="_blank" rel="nofollow">').findall(link)
        qual=re.compile('<strong>(.+?)</strong>').findall(link)[-1]
        qual = qual.replace('<em>','').replace('</em>','')
        items = len(match)
        addLink('[B][COLOR cyan]%s[/COLOR][/B]' %qual,'url','','','','')                
        for url in match:
                addDir2(name,url,1,'',items)
        try:
                match=re.compile('<iframe.+?="(.+?)".+?></iframe>').findall(link)   
                items = len(match)
                for url in match:
                        addDir2(name,url,1,'',items)
        except: pass
        try:
                match=re.compile('<IFRAME.+?="(.+?)".+?></IFRAME>').findall(link)   
                items = len(match)
                for url in match:
                        addDir2(name,url,1,'',items)
        except: pass
        try:
                match=re.compile('<p><a href="(.+?)".+?>.+?</a></p>').findall(link)   
                items = len(match)
                for url in match:
                        addDir2(name,url,1,'',items)
        except: pass



def BASE300SEARCH():
        try:
                keyb = xbmc.Keyboard('', 'Ultra-Vid')
                keyb.doModal()
                if (keyb.isConfirmed()):
                        search = keyb.getText().replace(' ','+')
                        #encode=urllib.quote(search)
                        #print encode
                        url = baseurl300+'/?s='+search
                        print url
                        try:
                                link = OPEN_URL(url)
                                link = link.encode('ascii', 'ignore')
                                match=re.compile('<span class="itemdets"> <a href="(.+?)" title="(.+?)"> </span>').findall(link)
                                items = len(match)
                                for url,name in match:
                                        name = name.replace('&#038;','&').replace("&#8217;","'").replace('&#8211;','-').replace('( BluRay ) ','').replace('( BluRay added ) ','').replace('NEW> ','').replace('( ENGLISH ) ','')
                                        addDir2(name,url,302,'',items)

                        except:
                                xbmc.executebuiltin("XBMC.Notification([COLOR gold][B]SORRY SITE DOWN[/B][/COLOR],,7000,"")")
                        try:
                                match=re.compile('<a class="next page-numbers" href="(.+?)">(.+?)</a>').findall(link)
                                name = name.replace(' \xc2\xbb','')
                                for url, name in match:
                                        addDir('[COLOR cyan]%s[/COLOR]' %name,url,301,art+'ultra.png',art+'f1.jpg','')
                        except: pass
        except:
                xbmc.executebuiltin("XBMC.Notification([COLOR gold][B]SORRY NO MATCHES FOUND[/B][/COLOR],,7000,"")")
        


############################################################################################################################
############################################################################################################################




def BASE350(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore').decode('ascii')
        try:
                dis=re.compile('<p class="lead margin-none">(.+?)</p>').findall(link)[0]
                dis = dis.replace('<em>','').replace('</em>','').replace('Now part of ','').replace('<span style="color:#a8a8a8">','').replace('</span>','').replace('<strong>','').replace('</strong>','').replace('<a href="#top100highestrated" onclick="_gaq.push([\'_trackEvent\', \'Best Docos\', \'Clicked Highest Rated Link\', \'Went to Highest Rated\']);">','').replace('</a>','').replace('<h3><i class="icon-uniF12C"></i> Here\'s the 100 Most Viewed</h3>','')
                addLink('[COLOR cyan]%s[/COLOR]' %dis,'url','',art+'da.png',art+'f2.jpg','')
        except: pass
        addDir('[COLOR white]Top[/COLOR]',baseurl350+'best',351,art+'da.png',art+'f2.jpg','')
        addDir('[COLOR white]List All[/COLOR]',baseurl350+'list-all-documentaries',351,art+'da.png',art+'f2.jpg','')
        addDir('[COLOR white]Random[/COLOR]',baseurl350+'random-docos',351,art+'da.png',art+'f2.jpg','')
        all_videos = regex_get_all(link, '<li class="">', '</a>')
        for a in all_videos:
                name = regex_from_to(a, '<span itemprop="genre">', '</span>')
                url = regex_from_to(a, 'href="', '"').replace("&amp;","&")
                nono = ['best','best#top100highestrated']
                if name not in url:
                        addDir('[COLOR white]%s[/COLOR]' %name,baseurl350+url,351,art+'da.png',art+'f2.jpg','')




def BASE350INDEX(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore').decode('ascii')
        all_videos = regex_get_all(link, '<div class="col-md-3" style="margin-top: 12px;">', '</div> </div>')
        try:
                dis=re.compile('<div class="widget-body"> <p class="margin-none">(.+?)</p> </div>').findall(link)[0]
                dis = dis.replace('<em>','').replace('</em>','').replace('<span style="color:#a8a8a8">','').replace('</span>','').replace('<strong>','').replace('</strong>','').replace('<a href="#top100highestrated" onclick="_gaq.push([\'_trackEvent\', \'Best Docos\', \'Clicked Highest Rated Link\', \'Went to Highest Rated\']);">','').replace('</a>','').replace('<h3><i class="icon-uniF12C"></i> Here\'s the 100 Most Viewed</h3>','')
                addLink('[COLOR cyan]%s[/COLOR]' %dis,'url','',art+'da.png',art+'f2.jpg','')
        except: pass
        for a in all_videos:
                name = regex_from_to(a, 'title="', '"').replace("&amp;","&")
                url = regex_from_to(a, 'href="', '"').replace("&amp;","&")
                icon = regex_from_to(a, 'data-src ="', '"').replace("&amp;","&")
                description = regex_from_to(a, '<p>', '</p>')
                name = name.replace('&#39;',"'")
                name = name.replace('&quot;','"')
                url = url.replace('../','').replace('./','').replace("&amp;","&")
                addDir('[COLOR white]%s[/COLOR]' %name,baseurl350+url,352,icon,icon,description)
        try:
                url=re.compile(" <a href='(.+?)'.+?> .+? </a>").findall(link)[-1]
                url = url.replace('./','').replace('../','')
                url = url.replace("&amp;","&")
                addDir('[COLOR cyan]Next Page[/COLOR]',baseurl350+url,351,art+'da.png',art+'f2.jpg','')
        except: pass
        setView('movies', 'movie-view')




def BASE350L(name,url,iconimage):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore')
        match=re.compile("<meta content='(.+?)' itemprop='embedUrl'>").findall(link)
        for url in match:
                url = url.replace('http://www.youtube.com/v/','plugin://plugin.video.youtube/play/?video_id=').replace('http://vimeo.com/moogaloop.swf?clip_id=','plugin://plugin.video.vimeo/play/?video_id=')
                url = url.replace('../','').replace("&amp;","&")
                addDir(name,url,1,iconimage,'','')




############################################################################################################################
############################################################################################################################




def BASE400():
        addDir('[COLOR cyan]List Movies[/COLOR]',baseurl400+'/list-movies',401,art+'panda.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Featured Movies[/COLOR]',baseurl400+'/watch-featured-movies-online-free',401,art+'panda.png',art+'f1.jpg','')
        addDir('[COLOR cyan]HD Movies[/COLOR]',baseurl400+'/watch-hd-movies-online-free',401,art+'panda.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Popular Movies Of All Time[/COLOR]',baseurl400+'/popular-movies',401,art+'panda.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Movies popular in the last 24 hours[/COLOR]',baseurl400+'/popular-movies-in-last-24-hours',401,art+'panda.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Movies popular in the last 7 days[/COLOR]',baseurl400+'/popular-movies-last-7-days',401,art+'panda.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Movies popular in the last 30 days[/COLOR]',baseurl400+'/popular-movies-in-last-30-days',401,art+'panda.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Movies By Genre[/COLOR]',baseurl400,403,art+'panda.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Movies By Year[/COLOR]',baseurl400,404,art+'panda.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Search Movies[/COLOR]',baseurl400,405,art+'panda.png',art+'f1.jpg','')




def BASE400INDEX(url):
        link = OPEN_URL(url)
        all_videos = regex_get_all(link, '<div class="data">', '</div>')
        try:
                pageno=re.compile('<div id="content_home_tv"><.+?>(.+?)<.+?></div><div class="qgitborder"></div>').findall(link)[0]
                addLink('[COLOR cyan]%s[/COLOR]' %pageno,'url','',art+'panda.png',art+'f1.jpg','')
        except: pass
        try:
                pageno=re.compile('<div class=\'wp-pagenavi\'>\n<span class=\'pages\'>(.*?)</span>').findall(link)[0]
                addLink('[COLOR cyan]%s[/COLOR]' %pageno,'url','',art+'panda.png',art+'f1.jpg','')
        except: pass
        for a in all_videos:
                #qual = regex_from_to(a, '<span class="', '"').replace('long_min_source_','')
                name = regex_from_to(a, 'title="', '"').replace("&#038;","&").replace('&#8217;',"'").replace('&#8211;',"-").replace('&#8216;',"`")
                url = regex_from_to(a, 'href="', '"')
                items = len(all_videos)
                addDir2(name,url,402,'',items)
        try:
                pageno=re.compile('<div class=\'wp-pagenavi\'>\n<span class=\'pages\'>(.*?)</span>').findall(link)[0]
                addLink('[COLOR cyan]%s[/COLOR]' %pageno,'url','',art+'panda.png',art+'f1.jpg','')
        except: pass
        try:
                url=re.compile('<a class="nextpostslink" rel="next" href="(.+?)">&raquo;</a>').findall(link)[0]
                addDir('[COLOR cyan]Next Page>>>[/COLOR]',url,401,art+'panda.png',art+'f1.jpg','')
        except: pass
        setView('movies', 'movie-view')



def BASE400L(name,url,iconimage):
        link = OPEN_URL(url)
        #url=re.compile('<span class=".+?"><a title=".+?" href="(.+?)".+?>.+?</a></li>').findall(link)[0]
        #items = len(name)
        #addDir2(name,url,1,'',items)
        all_videos = regex_get_all(link, '<span class=".+?">', '</a></li>')
        for a in all_videos:
                #name = regex_from_to(a, 'title="', '"').replace("&#038;","&").replace('&#8217;',"'")
                url = regex_from_to(a, 'href="', '"')
                #name2 = regex_from_to(a, '<a title=".*? - on ', '"')
                items = len(all_videos)
                nono = 'http://pandamovie.net/'
                nono2 = 'https://openload.co/'
                if nono not in url:
                        if nono2 not in url:
                                addDir2(name,url,1,'',items)



def BASE400GENRE(url):
        link = OPEN_URL(url)
        match=re.compile('<li><a title="(.+?)" href="(.+?)">.+?</a></li>').findall(link)
        for name,url in match:
                ok = '-movies-online-free'
                if ok in url:
                        addDir('[COLOR cyan]%s[/COLOR]' %name,url,401,art+'panda.png',art+'f1.jpg','')



def BASE400YEAR(url):
        link = OPEN_URL(url)
        match=re.compile('<li><a title="(.+?)" href="(.+?)">.+?</a></li>').findall(link)
        for name,url in match:
                ok = 'watch-movies-of-'
                if ok in url:
                        addDir('[COLOR cyan]%s[/COLOR]' %name,url,401,art+'panda.png',art+'f1.jpg','')



def BASE400SEARCH(url):
        try:
                keyb = xbmc.Keyboard('', 'Search PandaMovies')
                keyb.doModal()
                if (keyb.isConfirmed()):
                        search = keyb.getText().replace(' ','+')
                        #encode=urllib.quote(search)
                        #print encode
                        url = baseurl400+'/?s='+search
                        print url
                        all_videos = regex_get_all(link, '<div class="data">', '</a></h3>')
                        try:
                                pageno=re.compile('<div id="content_home_tv"><.+?>(.+?)<.+?></div><div class="qgitborder"></div>').findall(link)[0]
                                addLink('[COLOR cyan]%s[/COLOR]' %pageno,'url','',art+'panda.png',art+'f1.jpg','')
                        except: pass
                        try:
                                pageno=re.compile('<div class=\'wp-pagenavi\'>\n<span class=\'pages\'>(.*?)</span>').findall(link)[0]
                                addLink('[COLOR cyan]%s[/COLOR]' %pageno,'url','',art+'panda.png',art+'f1.jpg','')
                        except: pass
                        for a in all_videos:
                                #qual = regex_from_to(a, '<span class="', '"').replace('long_min_source_','')
                                name = regex_from_to(a, 'title="', '"').replace("&#038;","&").replace('&#8217;',"'").replace('&#8211;',"-").replace('&#8216;',"`")
                                url = regex_from_to(a, 'href="', '"')
                                items = len(all_videos)
                                addDir2(name,url,402,'',items)
                        try:
                                pageno=re.compile('<div class=\'wp-pagenavi\'>\n<span class=\'pages\'>(.*?)</span>').findall(link)[0]
                                addLink('[COLOR cyan]%s[/COLOR]' %pageno,'url','',art+'panda.png',art+'f1.jpg','')
                        except: pass
                        try:
                                url=re.compile('<a class="nextpostslink" rel="next" href="(.+?)">&raquo;</a>').findall(link)[0]
                                addDir('[COLOR cyan]Next Page>>>[/COLOR]',url,401,art+'panda.png',art+'f1.jpg','')
                        except: pass
                        setView('movies', 'movie-view')
        except:
                xbmc.executebuiltin("XBMC.Notification([COLOR gold][B]SORRY NO MATCHES FOUND[/B][/COLOR],,7000,"")")





############################################################################################################################
############################################################################################################################




def BASE450():
        addDir('[COLOR cyan]Recently Added[/COLOR]',baseurl450+'?so=rav',451,art+'concert.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Most Viewed[/COLOR]',baseurl450+'?so=mvv',451,art+'concert.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Top Rated[/COLOR]',baseurl450+'?so=trv',451,art+'concert.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Search[/COLOR]',baseurl450+'?so=trv',451,art+'concert.png',art+'f1.jpg','')




def BASE450INDEX(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore').decode('ascii')
        all_videos = regex_get_all(link, '<div class="video">', '<div class="stats">')
        try:
                dis=re.compile('<h1 id="page_title">\n(.+?)</h1>').findall(link)[0]
                addLink('[COLOR cyan]%s[/COLOR]' %dis,'url','',art+'concert.png',art+'f4.jpg','')
        except: pass
        for a in all_videos:
                name = regex_from_to(a, 'title="', '"').replace("&amp;","&").replace('&#39;',"'").replace('&quot;','"').replace('&#8230;','...')
                name = name.replace('&#8211;','-').replace('&#8212;','--').replace("&#8217;","'").replace('&#8220;','"').replace('&#8221;','"')
                url = regex_from_to(a, 'href="', '"').replace("&amp;","&")
                icon = regex_from_to(a, '<img src="', '"').replace("&amp;","&")
                description = regex_from_to(a, '<p>', '</p>').replace("&amp;","&").replace('&#39;',"'").replace('&quot;','"').replace('&#8230;','...')
                description = description.replace('&#8211;','-').replace('&#8212;','--').replace("&#8217;","'").replace('&#8220;','"').replace('&#8221;','"')
                addDir('[COLOR white]%s[/COLOR]' %name,url,452,icon,icon,description)
        try:
                current=re.compile('<div class="pagination"><span>(.+?)</span>').findall(link)[0]
                addLink('[COLOR cyan]%s[/COLOR]' %current,'url','',art+'concert.png',art+'f4.jpg','')
        except: pass
        try:
                nextp=re.compile('<a class="next page-numbers" href="(.+?)">').findall(link)[0]
                addDir('[COLOR cyan]Next Page>>>[/COLOR]',nextp,451,art+'concert.png',art+'f4.jpg','')
                match=re.compile("<a class='page-numbers' href='(.+?)'>(.+?)</a>").findall(link)
                for url, name in match:
                      addDir('[COLOR cyan]Page %s[/COLOR]' %name,url,451,art+'concert.png',art+'f4.jpg','')  
        except: pass
        setView('movies', 'movie-view')



def BASE450L(name,url,description):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore').decode('ascii')
        url=re.compile('<iframe .+?src="(.+?)".+?>').findall(link)[0]
        url = url.replace('http://www.youtube.com/embed/','plugin://plugin.video.youtube/play/?video_id=')
        if 'youtube' in url:
                url = url.replace('http://www.youtube.com/embed/','plugin://plugin.video.youtube/play/?video_id=')
                addDir(name,url,1,'','','')
                print url
        else:
                url = urlresolver.resolve(url)
                ok=True
                liz=xbmcgui.ListItem(name, iconImage=icon,thumbnailImage=icon); liz.setInfo( type="Video", infoLabels={ "Title": name } )
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=str(url),listitem=liz)
                xbmc.Player().play(str(url),liz,False)




############################################################################################################################
############################################################################################################################




def BASE500(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore').decode('ascii')
        match=re.compile("<a dir='ltr' href='(.+?)'>(.+?)</a>").findall(link)
        for url, name in match:
                if 'Days' not in name:
                        icon = art+name+'.jpg'
                        addDir('[COLOR cyan]%s[/COLOR]' %name,url,501,icon,art+'f1.jpg','')
        xbmc.executebuiltin("Container.SetViewMode(500)")



def BASE500INDEX(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore').decode('ascii')
        all_videos = regex_get_all(link, '<div style="text-align: left;">', '</h2>')
        for a in all_videos:
                name = regex_from_to(a, "<a href='.+?'>", "</a>").replace("&amp;","&").replace('&#39;',"'").replace('&quot;','"').replace('&#8230;','...')
                name = name.replace('&#8211;','-').replace('&#8212;','--').replace("&#8217;","'").replace('&#8220;','"').replace('&#8221;','"')
                name = name.replace('Watch Online','').replace('HD','')
                url = regex_from_to(a, '<iframe .+?src="', '"></iframe>').replace("&amp;","&")
                icon = regex_from_to(a, '<img .+?src="', '"').replace("&amp;","&")
                addDir('[COLOR white]%s[/COLOR]' %name,url,1,icon,fanart,'')
        try:
                nextp=re.compile("<a class='blog-pager-older-link' href='(.+?)'").findall(link)[0]
                addDir('[COLOR cyan]Next Page>>>[/COLOR]',nextp,501,art+'wls.png',art+'f1.jpg','')
        except: pass
        xbmc.executebuiltin("Container.SetViewMode(500)")




def BASE510(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore').decode('ascii')
        match=re.compile("<a dir='ltr' href='(.+?)'>(.+?)</a>").findall(link)
        for url, name in match:
                try:
                        link = OPEN_URL(url)
                        icon = re.compile("<meta content=\'(.+?)\' itemprop=\'image_url\'/>\n<meta content=\'.+?\' itemprop=\'blogId\'/>").findall(link)[0] 
                        addDir('[COLOR cyan]%s[/COLOR]' %name,url,511,icon,art+'f1.jpg','')
                except: pass




def BASE510L(url,iconimage):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore').decode('ascii')
        match=re.compile('<a href="(.+?)" target=_blank>(.+?)</a><br />').findall(link)
        for url, name in match:
                if 'cloudy' in url:
                        name = name.replace('.x264','').replace('-SS.mp4','')
                        addDir('[COLOR white]%s[/COLOR]' %name,url,1,iconimage,art+'f1.jpg','')
        try:
                nextp=re.compile("<a class='blog-pager-older-link' href='(.+?)'").findall(link)[0]
                addDir('[COLOR cyan]Next Page>>>[/COLOR]',nextp,511,art+'wls.png',art+'f1.jpg','')
        except: pass




############################################################################################################################
############################################################################################################################




def KMPINDEX(url):
        link = OPEN_URL(url)
        match=re.compile('<span id=".+?"><a href="(.+?)">(.+?)</a></span>').findall(link)
        for url,name in match:
                name = name.replace('&amp;','&')
                addDir('[COLOR cyan]%s[/COLOR]' %name,url,4001,'',art+'f1.jpg','')


def KMPL(url):
        link = OPEN_URL(url)
        try:
                match=re.compile('&lt;item&gt;<br />&lt;title&gt;(.+?)&lt;/title&gt;<br />&lt;link&gt;(.+?)&lt;/link&gt;<br />&lt;thumbnail&gt;(.+?)&lt;/thumbnail&gt;<br />&lt;/item&gt;</div>').findall(link)
                for name,url,thumb in match:
                        name = name.replace('&amp;','&')
                        addDir('[COLOR cyan]%s[/COLOR]' %name,url,1,thumb,'','')
        except: pass

        try:
                match=re.compile('&lt;item&gt;<br />&lt;title&gt;(.+?)&lt;/title&gt;<br />&lt;link&gt;<a href="(.+?)" class="bbc_link" target="_blank">.+?</a>&lt;/link&gt;<br />&lt;thumbnail&gt;<a href="(.+?)" class="bbc_link" target="_blank">.+?</a>&lt;/thumbnail&gt;<br />&lt;/item&gt;').findall(link)
                for name,url,thumb in match:
                        name = name.replace('&amp;','&')
                        addDir('[COLOR cyan]%s[/COLOR]' %name,url,1,thumb,'','')
        except: pass

############################################################################################################################

############################################################################################################################

def SS():
        #addDir('Alluc Super Search',baseurl102,102,'','','')
        addDir('[COLOR cyan]Ultra-Vid Search[/COLOR]','url',303,'',art+'f1.jpg','')
        addDir('[COLOR cyan]PandaMovie Search[/COLOR]',baseurl400,405,art+'panda.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Filmovizija Search[/COLOR]','url',105,'',art+'f1.jpg','')
        addDir('[COLOR cyan]Vodlocker Search[/COLOR]',baseurl101,101,'',art+'f1.jpg','')
        addDir('[COLOR cyan]Allcinemamovies Search[/COLOR]','url',106,'',art+'f1.jpg','')
        
        
        
def FILMOVSEARCH():
        addDir('[COLOR cyan]Filmovizija TV Search[/COLOR]','url',60,'',art+'f1.jpg','')
        addDir('[COLOR cyan]Filmovizija Movie Movie Search[/COLOR]','url',61,'',art+'f1.jpg','')


def ALLCINSEARCH():
        addDir('[COLOR cyan]Allcinemamovies TV Search[/COLOR]','url',210,'',art+'f1.jpg','')
        addDir('[COLOR cyan]Allcinemamovies Search[/COLOR]','url',209,'',art+'f1.jpg','')


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
                        addDir('[B[COLOR cyan]%s[/COLOR][/B]' %name,url,1,'',art+'f1.jpg','')
                        


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
                        addDir('[B][COLOR yellow]%s[/COLOR][/B]' %name,baseurl102+url,104,'',art+'f1.jpg','')
                        print url
        try:
                match=re.compile('<li><a href="(.+?)" rel=.+?>(.+?)</a></li>').findall(link)
                
                for url,name in match:
                        addDir('[B][COLOR yellow]%s Page[/COLOR][/B]' %name,baseurl102+url,103,'',art+'f1.jpg','')
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
        addDir('[COLOR cyan]www.hack-sat.com[/COLOR]',baseurl5001,5001,'',art+'f1.jpg','')
        addDir('[COLOR cyan]iptvapps.blogspot.co.uk[/COLOR]',baseurl5040,5040,'',art+'f1.jpg','')
        addDir('[COLOR cyan]iptv.filmover.com[/COLOR]',baseurl5002,5002,'',art+'f1.jpg','')
        #addDir('www.iptvsharing.com/2015/07/sport-klub-iptv-links-m3u8.html',baseurl5010,5003,'','','')
        #addDir('www.iptvsharing.com/2015/07/sport-klub-iptv-links-m3u8.html',baseurl5020,5003,'','','')
        addDir('[COLOR cyan]free-links-iptv.blogspot.co.uk[/COLOR]',baseurl5030,5030,'',art+'f1.jpg','')
        

def BASE5001(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore')
        match=re.compile('#EXTINF.+?,(.+?)\n(.+?)\n').findall(link)
        for name,url in match:
                url = url.replace('#extinf:0,','')
                addDir('[COLOR cyan]%s[/COLOR]' %name,url,1,'',art+'f1.jpg','')

def BASE5002(url):
        link = OPEN_URL(url)
        match=re.compile('<li class=".+?"><a href="(.+?)" >(.+?)</a>.+?\n</li>').findall(link)
        for url,name in match:
                ok = 'xbmc'
                if ok in url:
                        addDir('[COLOR cyan]%s[/COLOR]' %name,url,5003,'',art+'f1.jpg','')

def BASE5002L(url):
        link = OPEN_URL(url)
        match=re.compile('#EXTINF:.+?,(.+?) http://(.+?) ').findall(link)
        match1=re.compile('#EXTINF:.+?,(.+?) rtmp://(.+?) ').findall(link)
        try:
                for name,url in match:
                        addDir('[COLOR cyan]%s[/COLOR]' %name,'http://'+url,1,'',art+'f1.jpg','')
        except: pass

        try:
                for name,url in match1:
                        addDir('[COLOR cyan]%s[/COLOR]' %name,'rtmp://'+url,1,'',art+'f1.jpg','')
        except: pass


def BASE5030(url):
        link = OPEN_URL(url)
        match=re.compile("<a href='(.+?)' title='(.+?)'>Read more &#187;</a>").findall(link)
        match1=re.compile("<a dir='ltr' href='(.+?)'>(.+?)</a>").findall(link)
        try:
                for url,name in match:
                        name = name.replace('&amp;','&')
                        addDir('[COLOR cyan]%s[/COLOR]' %name,url,5031,'',art+'f1.jpg','')
        except: pass

        try:
                for url,name in match1:
                        name = name.replace('&amp;','&')
                        addDir('[COLOR cyan]%s[/COLOR]' %name,url,5030,'',art+'f1.jpg','')
        except: pass

def BASE5030L(url):
        link = OPEN_URL(url)
        match=re.compile("\nEXTINF:.+?,(.+?)<br />\n<br />\n<a name=\'more\'></a>(.+?)<br />").findall(link)
        match1=re.compile("#EXTINF:.+?,(.+?)<br />(.+?)<br />").findall(link)
        match2=re.compile("(.+?),<br />(.+?)<br />").findall(link)
        try:
                for name,url in match:
                        name = name.replace('&amp;','&').replace('&nbsp;','')
                        addDir('[COLOR cyan]%s[/COLOR]' %name,url,1,'',art+'f1.jpg','')
        except: pass
        
        try:
                for name,url in match1:
                        name = name.replace('&amp;','&').replace('&nbsp;','')
                        addDir('[COLOR cyan]%s[/COLOR]' %name,url,1,'',art+'f1.jpg','')
        except: pass

        try:
                for name,url in match2:
                        name = name.replace('&amp;','&').replace('&nbsp;','')
                        addDir('[COLOR cyan]%s[/COLOR]' %name,url,1,'',art+'f1.jpg','')
        except: pass




def BASE5040(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore').decode('ascii')
        match=re.compile('<span style="color: #38761d;"><b>(.*?)</b></span><b><span style="color: #38761d;">(.*?)</span></b><span style="color: #38761d;"><b>(.*?)</b></span><b><span style="color: #38761d;">(.*?)</span></b><b><span style="color: #38761d;">(.*?)</span></b><br />\n(.*?)<br />').findall(link)
        for n1,n2,n3,n4,n5,url in match:
                n1 = n1.replace('<span style="background-color: #666666;"> </span>','')
                n1 = n1.replace('<span style="font-size: large;"> </span>','')
                n1 = n1.replace('<span style="color: red;">','').replace('</span>','').replace('<span style="color: blue;">','')
                url = url.replace('<b>','').replace('</b>','')
                addDir('[COLOR cyan]%s %s %s %s %s[/COLOR]' %(n1,n2,n3,n4,n5),url,5041,'',art+'f1.jpg','')




def BASE5040L(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore').decode('ascii')
        match=re.compile('#EXTINF:.*?,(.*?)\r\n(.*?)\r').findall(link)
        for name,url in match:
                url = url.replace('rtmp://$OPT:rtmp-raw=','')
                name = name.replace('&#65533;','')
                addDir('[COLOR cyan]%s[/COLOR]' %name,url,1,'',art+'f1.jpg','')





############################################################################################################################

############################################################################################################################
############################################################################################################################

############################################################################################################################




def regex_from_to(text, from_string, to_string, excluding=True):
        if excluding:
                try: r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
                except: r = ''
        else:
                try: r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
                except: r = ''
        return r




def regex_get_all(text, start_with, end_with):
        r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
        return r



def PLAYTUBE(url):
        try:
                url = "PlayMedia(plugin://plugin.video.youtube/play/?video_id="+url+")"
                xbmc.executebuiltin(url)
        except:
                xbmc.executebuiltin("XBMC.Notification([COLOR gold][B]SORRY LINK DOWN[/B][/COLOR],,7000,"")")

            


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



def addDir2(name,url,mode,iconimage,itemcount):
        if metaset=='true':
                splitName=name.partition('(')
                simplename=""
                simpleyear=""
                if len(splitName)>0:
                        simplename=splitName[0]
                        simpleyear=splitName[2].partition(')')
                if len(simpleyear)>0:
                        simpleyear=simpleyear[0]
                meta = metaget.get_meta('movie', simplename ,simpleyear)
                u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&site="+str(site)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
                ok=True
                liz=xbmcgui.ListItem(name, iconImage=meta['cover_url'], thumbnailImage=meta['cover_url'])
                liz.setInfo( type="Video", infoLabels= meta )
                contextMenuItems = []
                contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
                liz.addContextMenuItems(contextMenuItems, replaceItems=False)
                if not meta['backdrop_url'] == '': liz.setProperty('fanart_image', meta['backdrop_url'])
                else: liz.setProperty('fanart_image', fanart)
                if mode==1:
                        liz.setProperty("IsPlayable","true")
                        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False,totalItems=itemcount)
                else:
                        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True,totalItems=itemcount)
                return ok
        else:
                u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&site="+str(site)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
                ok=True
                liz=xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
                liz.setInfo( type="Video", infoLabels={ "Title": name } )
                liz.setProperty('fanart_image', fanart)
                if mode==1:
                        liz.setProperty("IsPlayable","true")
                        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False,totalItems=itemcount)
                else:
                        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True,totalItems=itemcount)
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
    headers = {}
    name = ''
    headers['User-Agent'] = User_Agent
    link = requests.get(url, headers=headers).text
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
site=None

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

elif mode==2:
        PLAYTUBE(url)

elif mode==3:
        CONINDEX()

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

elif mode==250:
        BASE250()

elif mode==251:
        BASE250GENRE(url)

elif mode==252:
        BASE250INDEX(url)

elif mode==253:
        BASE250L(url)

elif mode==300:
        BASE300()

elif mode==301:
        BASE300INDEX(url)

elif mode==302:
        BASE300L(url,name)

elif mode==303:
        BASE300SEARCH()

elif mode==350:
        BASE350(url)

elif mode==351:
        BASE350INDEX(url)

elif mode==352:
        BASE350L(name,url,iconimage)

elif mode==400:
        BASE400()

elif mode==401:
        BASE400INDEX(url)

elif mode==402:
        BASE400L(name,url,iconimage)

elif mode==403:
        BASE400GENRE(url)

elif mode==404:
        BASE400YEAR(url)

elif mode==405:
        BASE400SEARCH(url)

elif mode==450:
        BASE450()

elif mode==451:
        BASE450INDEX(url)

elif mode==452:
        BASE450L(name,url,description)

elif mode==500:
        BASE500(url)

elif mode==501:
        BASE500INDEX(url)

elif mode==510:
        BASE510(url)

elif mode==511:
        BASE510L(url,iconimage)

elif mode==4000:
        KMPINDEX(url)

elif mode==4001:
        KMPL(url)

elif mode==5000:
        IPTV()

elif mode==5001:
        BASE5001(url)

elif mode==5002:
        BASE5002(url)

elif mode==5003:
        BASE5002L(url)

elif mode==5030:
        BASE5030(url)

elif mode==5031:
        BASE5030L(url)

elif mode==5040:
        BASE5040(url)

elif mode==5041:
        BASE5040L(url)
        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
