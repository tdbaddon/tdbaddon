#V 2.0.7
import xbmc , xbmcaddon , xbmcgui , xbmcplugin , requests , urllib , urllib2 , json , os , re , sys , datetime , urlresolver , random , liveresolver , base64 , pyxbmct
from resources . lib . common_addon import Addon
from HTMLParser import HTMLParser
from metahandler import metahandlers
import nanscrapers
if 64 - 64: i11iIiiIii
if 65 - 65: Vev / iIii1I11I1II1 % VeeeeeeeVV - i1IIi
eevVVevev = 'plugin.video.Evolve'
ee = Addon ( eevVVevev , sys . argv )
i1iII1IiiIiI1 = xbmcaddon . Addon ( id = eevVVevev )
iIiiiI1IiI1I1 = xbmcaddon . Addon ( ) . getAddonInfo
eevVeVeVVevev = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + eevVVevev , 'fanart.png' ) )
I11i = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + eevVVevev , 'fanart.png' ) )
VevV = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + eevVVevev , 'icon.png' ) )
Ve = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + eevVVevev + '/resources/art' , 'next.png' ) )
I1ii11iIi11i = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + eevVVevev + '/resources' , 'rd.txt' ) )
I1IiI = 'http://evolverepo.net/anewEvolvemenu/EvolveMainMenu.xml'
eevVVV = 'http://evolverepo.net/Evolvemasterlist/'
iIiiiI = i1iII1IiiIiI1 . getSetting ( 'password' )
Iii1ii1II11i = i1iII1IiiIiI1 . getSetting ( 'enable_meta' )
iI111iI = 'http://evolverepo.net/anewEvolvemenu/info.txt'
IiII = xbmc . translatePath ( 'special://home/userdata/addon_data/' + eevVVevev )
iI1Ii11111iIi = xbmc . translatePath ( os . path . join ( 'special://home/userdata/Database' , 'Evolve.db' ) )
i1i1II = open ( iI1Ii11111iIi , 'a' )
i1i1II . close ( )
if 96 - 96: eevVVev - VeeveeVeveeeveV . I1i1iI1i - eeveveeeev / eevev * VeeveVeveee
def eeveVeVeveve ( ) :
 if not os . path . exists ( IiII ) :
  os . mkdir ( IiII )
 i1 ( iI111iI , 'GlobalCompare' )
 eVVeeevevVevV ( '[B][COLOR royalblue]F[/COLOR][COLOR white]avs[/COLOR][/B]' , 'url' , 22 , 'http://i.imgur.com/Fi18HDV.png' , I11i )
 eVVeeevevVevV ( '[B][COLOR red]M[/COLOR][COLOR white]ovies[/COLOR][/B]' , 'http://evolverepo.net/EvolveMenus/Movies/Mainmenu.xml' , 26 , 'http://i.imgur.com/x6BAZUe.png' , I11i )
 eVVeeevevVevV ( '[B][COLOR blue]TV[/COLOR]  [COLOR blue]S[/COLOR][COLOR white]hows[/COLOR][/B]' , 'http://evolverepo.net/EvolveMenus/TvShows/Mainmenu.xml' , 27 , 'http://i.imgur.com/SLdxQL6.png' , I11i )
 i1111 = i11 ( I1IiI )
 I11 = re . compile ( '<item>(.+?)</item>' ) . findall ( i1111 )
 for Veeveeveveveveeveev in I11 :
  eVeeveeeeeveve = re . compile ( '<title>(.+?)</title>.+?folder>(.+?)</folder>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>' ) . findall ( Veeveeveveveveeveev )
  for eVeveeveeveeVeveV , eeeveevVevev , eV , eevVeVeVVevev in eVeeveeeeeveve :
   eVVeeevevVevV ( eVeveeveeveeVeveV , eeeveevVevev , 1 , eV , eevVeVeVVevev )
 eVVeeevevVevV ( '[B][COLOR chartreuse]S[/COLOR][COLOR white]earch[/COLOR][/B] [B][COLOR chartreuse]E[/COLOR][COLOR white]volve[/COLOR][/B]' , 'url' , 5 , 'http://i.imgur.com/oHqT3bb.png' , I11i )
 xbmc . executebuiltin ( 'Container.SetViewMode(500)' )
 if 34 - 34: eVVee * I1IiIiiIII
def iI11 ( name , url , iconimage , fanart ) :
 eVVeeevevVevV ( '[B][COLOR red]MOVIE SEARCH[/COLOR][/B]' , 'http://evolverepo.net/EvolveMenus/Movies/Search/Search.txt' , 5 , 'http://i.imgur.com/Qlc3Efe.png' , I11i )
 eVVeeevevVevV ( '[B][COLOR yellow]UK CINEMA RELEASE DATES[/COLOR][/B]' , 'http://www.empireonline.com/movies/features/upcoming-movies/' , 34 , 'http://i.imgur.com/1ImmOS4.png' , I11i )
 iII111ii = i1iIIi1 ( name )
 i1iII1IiiIiI1 . setSetting ( 'movie' , iII111ii )
 i1111 = i11 ( url )
 I11 = re . compile ( '<item>(.+?)</item>' ) . findall ( i1111 )
 for Veeveeveveveveeveev in I11 :
  eVeeveeeeeveve = re . compile ( '<title>(.+?)</title>.+?folder>(.+?)</folder>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>' ) . findall ( Veeveeveveveveeveev )
  for name , url , iconimage , fanart in eVeeveeeeeveve :
   ii11iIi1I ( name , url , iconimage , fanart , Veeveeveveveveeveev )
   if 6 - 6: I1I11I1I1I * VeeVevVV
def iiiIi ( name , url , iconimage , fanarts ) :
 eVVeeevevVevV ( '[B][COLOR blue]TV SEARCH[/COLOR][/B]' , 'http://evolverepo.net/anewEvolvemenu/search.xml' , 33 , 'http://i.imgur.com/gLWo9QO.png' , fanarts )
 eVVeeevevVevV ( '[B][COLOR yellow]TV SCHEDULE[/COLOR][/B]' , 'http://www.tvwise.co.uk/uk-premiere-dates/' , 32 , 'http://i.imgur.com/Pq53Nxh.png' , fanarts )
 eVVeeevevVevV ( '[B][COLOR blue]Latest[/COLOR] [COLOR white]Episodes[/COLOR][/B]' , 'http://www.watchepisodes4.com' , 28 , 'http://i.imgur.com/PmLtUtH.png' , fanarts )
 eVVeeevevVevV ( '[B][COLOR blue]Popular[/COLOR] [COLOR white]Shows[/COLOR][/B]' , 'http://www.watchepisodes4.com/home/popular-series' , 29 , 'http://i.imgur.com/SHXfj1a.png' , fanarts )
 eVVeeevevVevV ( '[B][COLOR blue]New[/COLOR] [COLOR white]Shows[/COLOR][/B]' , 'http://www.watchepisodes4.com/home/new-series' , 30 , 'http://i.imgur.com/roVYGM8.png' , fanarts )
 iII111ii = i1iIIi1 ( name )
 i1iII1IiiIiI1 . setSetting ( 'tv' , iII111ii )
 i1111 = i11 ( url )
 I11 = re . compile ( '<item>(.+?)</item>' ) . findall ( i1111 )
 for Veeveeveveveveeveev in I11 :
  eVeeveeeeeveve = re . compile ( '<title>(.+?)</title>.+?folder>(.+?)</folder>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>' ) . findall ( Veeveeveveveveeveev )
  for name , url , iconimage , eevVeVeVVevev in eVeeveeeeeveve :
   ii11iIi1I ( name , url , iconimage , eevVeVeVVevev , Veeveeveveveveeveev )
   if 24 - 24: iIiI1I11 % i111I1 % eVeV - iiIiIIi % eeVeeevV
def VeeVev ( name , url , iconimage , fanart ) :
 iII111ii = i1iIIi1 ( name )
 i1iII1IiiIiI1 . setSetting ( 'tv' , iII111ii )
 i1111 = i11 ( url )
 II11iiii1Ii ( i1111 )
 if '<message>' in i1111 :
  iI111iI = re . compile ( '<message>(.+?)</message>' ) . findall ( i1111 ) [ 0 ]
  i1 ( iI111iI , iII111ii )
 if '<intro>' in i1111 :
  VVeve = re . compile ( '<intro>(.+?)</intro>' ) . findall ( i1111 ) [ 0 ]
  Vee ( VVeve )
 if 'XXX>yes</XXX' in i1111 : VeveevVe ( i1111 )
 I11 = re . compile ( '<item>(.+?)</item>' ) . findall ( i1111 )
 for Veeveeveveveveeveev in I11 :
  ii11iIi1I ( name , url , iconimage , fanart , Veeveeveveveveeveev )
  if 78 - 78: iIii1I11I1II1 - iIiI1I11 * eeveveeeev + VeeveVeveee + i111I1 + i111I1
def ii11iIi1I ( name , url , iconimage , fanart , item ) :
 try :
  if '<sportsdevil>' in item : I11I11i1I ( name , url , iconimage , fanart , item )
  elif '<iplayer>' in item : ii11i1iIII ( name , url , iconimage , fanart , item )
  elif '<folder>' in item : Ii1I ( name , url , iconimage , fanart , item )
  elif '<iptv>' in item : Veeveev ( name , url , iconimage , fanart , item )
  elif '<image>' in item : III1ii1iII ( name , url , iconimage , fanart , item )
  elif '<text>' in item : eeeveeeeeVev ( name , url , iconimage , fanart , item )
  elif '<scraper>' in item : i11Iiii ( name , url , iconimage , fanart , item )
  elif '<lbscraper>' in item : iI ( name , url , iconimage , fanart , item )
  elif '<redirect>' in item : I1i1I1II ( name , url , iconimage , fanart , item )
  elif '<oktitle>' in item : i1IiIiiI ( name , url , iconimage , fanart , item )
  elif '<nan>' in item : I1I ( name , url , iconimage , fanart , item )
  else : eVVeveveVV ( name , url , iconimage , fanart , item )
 except : pass
 if 75 - 75: i1IIi / VeeeeeeeVV - Vev / eevev . eevVVev - i1IIi
def ii11i1iIII ( name , url , iconimage , fanart , item ) :
 url = re . compile ( '<iplayer>(.+?)</iplayer>' ) . findall ( item ) [ 0 ]
 name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
 url = 'plugin://plugin.video.iplayerwww/?url=%s&mode=202&name=%s&iconimage=%s&description=&subtitles_url=&logged_in=False' % ( url , name , iconimage )
 VevevevVVev ( name , url , 16 , iconimage , fanart )
 if 43 - 43: iiIiIIi - Vev % VeeveeVeveeeveV . VeeVevVV
def I1I ( name , url , iconimage , fanart , item ) :
 name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 eevevVeeVeee = re . compile ( '<meta>(.+?)</meta>' ) . findall ( item ) [ 0 ]
 iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
 VeveveveeevV = re . compile ( '<nan>(.+?)</nan>' ) . findall ( item ) [ 0 ]
 VVVV = re . compile ( '<imdb>(.+?)</imdb>' ) . findall ( item ) [ 0 ]
 if VeveveveeevV == 'movie' :
  VVVV = VVVV + '<>movie'
 elif VeveveveeevV == 'tvshow' :
  i11i1 = re . compile ( '<showname>(.+?)</showname>' ) . findall ( item ) [ 0 ]
  IIIii1II1II = re . compile ( '<season>(.+?)</season>' ) . findall ( item ) [ 0 ]
  i1I1iI = re . compile ( '<episode>(.+?)</episode>' ) . findall ( item ) [ 0 ]
  eeevVeeVVeev = re . compile ( '<showyear>(.+?)</showyear>' ) . findall ( item ) [ 0 ]
  eevV = re . compile ( '<episodeyear>(.+?)</episodeyear>' ) . findall ( item ) [ 0 ]
  VVVV = VVVV + '<>' + i11i1 + '<>' + IIIii1II1II + '<>' + i1I1iI + '<>' + eeevVeeVVeev + '<>' + eevV
  VeveveveeevV = "tvep"
 VeveveV ( name , VVVV , 19 , iconimage , 1 , VeveveveeevV , isFolder = True )
 if 39 - 39: eVeV - eevVVev * eeveveeeev % VeeveVeveee * eevVVev % eevVVev
def VeVVVVV ( name , imdb , iconimage , fanart ) :
 I1ii11iIi11i = ''
 iIi1i111II = name
 iII111ii = i1iIIi1 ( name )
 i1iII1IiiIiI1 . setSetting ( 'tv' , iII111ii )
 if 'movie' in imdb :
  imdb = imdb . split ( '<>' ) [ 0 ]
  VeVVevevV = [ ]
  eVVeVevVevVev = [ ]
  Veeveveve = name . partition ( '(' )
  I11IiI1I11i1i = Veeveveve [ 0 ]
  I11IiI1I11i1i = i1iIIi1 ( I11IiI1I11i1i )
  iI1ii1Ii = Veeveveve [ 2 ] . partition ( ')' ) [ 0 ]
  eeeeevevev = nanscrapers . scrape_movie ( I11IiI1I11i1i , iI1ii1Ii , imdb , timeout = 800 )
 else :
  i11i1 = imdb . split ( '<>' ) [ 1 ]
  iIIIi1 = imdb . split ( '<>' ) [ 0 ]
  IIIii1II1II = imdb . split ( '<>' ) [ 2 ]
  i1I1iI = imdb . split ( '<>' ) [ 3 ]
  eeevVeeVVeev = imdb . split ( '<>' ) [ 4 ]
  eevV = imdb . split ( '<>' ) [ 5 ]
  eeeeevevev = nanscrapers . scrape_episode ( i11i1 , eeevVeeVVeev , eevV , IIIii1II1II , i1I1iI , iIIIi1 , None )
 iiII1i1 = 1
 for eeveveVVeve in list ( eeeeevevev ( ) ) :
  for VVVevevV in eeveveVVeve :
   if urlresolver . HostedMediaFile ( VVVevevV [ 'url' ] ) . valid_url ( ) :
    I1ii11iIi11i = VVeVVeveeeveeV ( VVVevevV [ 'url' ] )
    name = "Link " + str ( iiII1i1 ) + ' | ' + VVVevevV [ 'source' ] + I1ii11iIi11i
    iiII1i1 = iiII1i1 + 1
    VeveevVevevVeeveev ( name , VVVevevV [ 'url' ] , 2 , iconimage , fanart , description = i1iII1IiiIiI1 . getSetting ( 'tv' ) )
    if 87 - 87: eeVeeevV * I1i1iI1i % i11iIiiIii % eevev - I1I11I1I1I
def i11Iiii ( name , url , iconimage , fanart , item ) :
 name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 url = re . compile ( '<scraper>(.+?)</scraper>' ) . findall ( item ) [ 0 ]
 fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
 eVVeeevevVevV ( name , url , 18 , iconimage , fanart )
 if 68 - 68: iiIiIIi % i1IIi . eVeV . eVVee
def eev ( name , url , iconimage , fanart ) :
 eeeveVe = url
 if eeeveVe == 'latestmovies' :
  eevevevVeve = 15
  iI1iII1 = MOVIESINDEXER ( )
  eVevVVeeevVV = re . compile ( '<item>(.+?)</item>' ) . findall ( iI1iII1 )
  for Veeveeveveveveeveev in eVevVVeeevVV :
   eVeeveeeeeveve = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>' ) . findall ( Veeveeveveveveeveev )
   Vevii1ii1ii = len ( eVevVVeeevVV )
   for name , url , iconimage , fanart in eVeeveeeeeveve :
    if '<meta>' in Veeveeveveveveeveev :
     eeeeeVeeeveee = re . compile ( '<meta>(.+?)</meta>' ) . findall ( Veeveeveveveveeveev ) [ 0 ]
     VeveveV ( name , url , eevevevVeve , iconimage , Vevii1ii1ii , eeeeeVeeeveee , isFolder = False )
    else : VeveevVevevVeeveev ( name , url , 15 , iconimage , fanart )
    if 6 - 6: VeeVevVV - iIiI1I11 + iIii1I11I1II1 - iiIiIIi - i11iIiiIii
    if 79 - 79: eevev - Vev * eeveveeeev + eevev % Vev * Vev
def eVVeev ( name , url , iconimage , fanarts ) :
 i1111 = eeevevVeveveV ( 'http://www.watchepisodes4.com' )
 iIiIIIi = re . compile ( '<a title=".+?" .+? style="background-image: url(.+?)"></a>.+?<div class="hb-right">.+?<a title=".+?" href="(.+?)" class="episode">(.+?)</a>' , re . DOTALL ) . findall ( i1111 )
 for iconimage , url , name in iIiIIIi :
  iconimage = iconimage . replace ( "('" , "" ) . replace ( "')" , "" )
  name = name . replace ( "&#39;" , "'" ) . replace ( '&amp;' , ' & ' )
  name = name . split ( '  ' ) [ 0 ]
  eVVeeevevVevV ( name , url , 24 , iconimage , iconimage )
  if 93 - 93: i111I1
def i1IIIiiII1 ( name , url , iconimage , fanart ) :
 i1111 = eeevevVeveveV ( url )
 iIiIIIi = re . compile ( '<div class="cb-first">.+?<a href="(.+?)" class="c-image"><img alt=".+?" title="(.+?)" src="(.+?)"></a>' , re . DOTALL ) . findall ( i1111 )
 for url , name , iconimage in iIiIIIi :
  name = name . replace ( "&#39;" , "'" ) . replace ( '&amp;' , ' & ' )
  eVVeeevevVevV ( name , url , 31 , iconimage , iconimage )
  if 87 - 87: I1IiIiiIII * eVVee + I1I11I1I1I / iIii1I11I1II1 / i111I1
def I1111IIi ( name , url , iconimage , fanart ) :
 i1111 = eeevevVeveveV ( url )
 iIiIIIi = re . compile ( '<div class="cb-first">.+?<a href="(.+?)" class="c-image"><img alt=".+?" title="(.+?)" src="(.+?)"></a>' , re . DOTALL ) . findall ( i1111 )
 for url , name , iconimage in iIiIIIi :
  name = name . replace ( "&#39;" , "'" ) . replace ( '&amp;' , ' & ' )
  eVVeeevevVevV ( name , url , 31 , iconimage , iconimage )
  if 93 - 93: VeeeeeeeVV / VeeveeVeveeeveV % i11iIiiIii + eVVee * eeveveeeev
def I1 ( name , url , iconimage , fanart ) :
 i1111 = iI11Ii ( url )
 i1iIIIi1i = re . compile ( '<div class="std-cts">.+?<div class="sdt-content tnContent">.+?<h2>(.+?)</h2>' , re . DOTALL ) . findall ( i1111 ) [ 0 ] . replace ( ' Episodes' , '' ) . replace ( "&#39;" , "'" ) . replace ( '&amp;' , ' & ' )
 I11 = re . compile ( '<a title=".+?" href="(.+?)">.+?<div class="season">(.+?) </div>.+?<div class="episode">(.+?)</div>.+?<div class="e-name">(.+?)</div>' , re . DOTALL ) . findall ( i1111 )
 for url , IIIii1II1II , i1I1iI , iI1iIIiiii in I11 :
  iI1iIIiiii = iI1iIIiiii . replace ( "&#39;" , "'" ) . replace ( '&amp;' , ' & ' )
  if '</div>' in name : name = 'TBA'
  eVVeeevevVevV ( '%s ' % i1iIIIi1i + '(%s ' % IIIii1II1II + '%s)' % i1I1iI , url , 24 , iconimage , iconimage )
  if 26 - 26: VeeVevVV . VeeeeeeeVV
def I11i1ii1 ( name , url , iconimage , fanart ) :
 iIi1i111II = name
 i1111 = iI11Ii ( url )
 VevVeeeevV = re . compile ( '<a target="_blank" href=".+?" data-episodeid=".+?" data-linkid=".+?" data-hostname=".+?" class="watch-button" data-actuallink="(.+?)">Watch Now!</a>' ) . findall ( i1111 )
 iiII1i1 = 1
 VeVVevevV = [ ]
 eVVeVevVevVev = [ ]
 for Veve in VevVeeeevV :
  I1ii11iIi11i = VVeVVeveeeveeV ( Veve )
  if 'http' in Veve : VeVeeV = Veve . split ( '/' ) [ 2 ] . split ( '.' ) [ 0 ]
  else : VeVeeV = Veve
  name = "Link " + str ( iiII1i1 ) + ' | ' + VeVeeV + I1ii11iIi11i
  if VeVeeV != 'www' :
   VeveevVevevVeeveev ( VeVeeV , Veve , 2 , iconimage , fanart , description = '' )
   if 12 - 12: VeeveeVeveeeveV * i111I1 % i1IIi % iIii1I11I1II1
def IIi1I11I1II ( name , url , iconimage , fanart ) :
 i1111 = iI11Ii ( url )
 iIiIIIi = re . compile ( '<td height="20">(.+?)</td>.+?<td>(.+?)</td>.+?<td><a href=".+?">(.+?)</a></td>.+?<td><a href=".+?">(.+?)</a></td>.+?</tr>' , re . DOTALL ) . findall ( i1111 )
 for VeeVeeeVe , name , ii11IIII11I , VVeee in iIiIIIi :
  name = name . replace ( "&#8217;" , "'" ) . replace ( '&amp;' , ' & ' )
  eVVeeevevVevV ( '[COLOR yellow]%s[/COLOR] - ' % ii11IIII11I + '[COLOR blue]%s[/COLOR] ' % name + '- [COLOR white]%s[/COLOR]' % VeeVeeeVe , url , 28 , iconimage , fanart )
  if 90 - 90: VeeveVeveee % i1IIi / eeveveeeev
def IIi ( url ) :
 i1Iii1i1I = ''
 VVeVevev = xbmc . Keyboard ( i1Iii1i1I , '[B][COLOR red]S[/COLOR][COLOR white]earch[/COLOR][/B] [B][COLOR red]E[/COLOR][COLOR white]volve[/COLOR][/B]' )
 VVeVevev . doModal ( )
 if VVeVevev . isConfirmed ( ) :
  i1Iii1i1I = VVeVevev . getText ( ) . replace ( ' ' , '+' ) . replace ( '+and+' , '+%26+' )
 if len ( i1Iii1i1I ) > 1 :
  url = 'http://www.watchepisodes4.com/search/ajax_search?q=' + i1Iii1i1I
  i1111 = iI11Ii ( url )
  eVeeveeeeeveve = json . loads ( i1111 )
  eVeeveeeeeveve = eVeeveeeeeveve [ 'series' ]
  for Veeveeveveveveeveev in eVeeveeeeeveve :
   eVeveeveeveeVeveV = Veeveeveveveveeveev [ 'value' ]
   IiI111111IIII = Veeveeveveveveeveev [ 'seo' ]
   url = 'http://www.watchepisodes4.com/' + IiI111111IIII
   eV = 'http://www.watchepisodes4.com/movie_images/' + IiI111111IIII + '.jpg'
   eVVeeevevVevV ( eVeveeveeveeVeveV , url , 31 , eV , eevVeVeVVevev )
  i1Iii1i1I = i1Iii1i1I [ : - 1 ]
  i1111 = i11 ( 'http://evolverepo.net/anewEvolvemenu/search.xml' )
  i1Ii = re . compile ( '<link>(.+?)</link>' ) . findall ( i1111 )
  for url in i1Ii :
   try :
    i1111 = i11 ( url )
    ii111iI1iIi1 = re . compile ( '<item>(.+?)</item>' ) . findall ( i1111 )
    for Veeveeveveveveeveev in ii111iI1iIi1 :
     I11 = re . compile ( '<title>(.+?)</title>' ) . findall ( Veeveeveveveveeveev )
     for iIi1i111II in I11 :
      iIi1i111II = i1iIIi1 ( iIi1i111II . upper ( ) )
      i1Iii1i1I = i1Iii1i1I . upper ( )
      if i1Iii1i1I in iIi1i111II :
       ii11iIi1I ( eVeveeveeveeVeveV , url , eV , eevVeVeVVevev , Veeveeveveveveeveev )
   except : pass
   if 78 - 78: eeveveeeev . I1I11I1I1I + eeveveeeev / VeeVevVV / eeveveeeev
   if 54 - 54: eevev % i111I1
def IIiII111iiI1I ( name , url , iconimage , fanart ) :
 i1111 = iI11Ii ( url )
 iIiIIIi = re . compile ( '<h2 id=".+?">(.+?)</h2>.+?<p><span class="article__image article__image--undefined"><img src="(.+?)" alt=".+?"></span> </p>.+?<p><strong>(.+?)</strong>(.+?)<' , re . DOTALL ) . findall ( i1111 )
 for iIi1i111II , iconimage , Ii1i1iI1iIIi , ii11IIII11I in iIiIIIi :
  name = name . replace ( "&#8217;" , "'" ) . replace ( '&amp;' , ' & ' )
  eVVeeevevVevV ( '[COLOR yellow]%s [/COLOR] ' % iIi1i111II + '[COLOR red]%s[/COLOR]' % Ii1i1iI1iIIi + '[COLOR white]%s[/COLOR]' % ii11IIII11I , url , 35 , iconimage , fanart )
def I1Ii ( name , url , iconimage , fanart ) :
 i1111 = i11 ( 'http://evolverepo.net/EvolveMenus/Movies/EvolveLatest/mainmenu.xml' )
 iIiIIIi = re . compile ( '<item>(.+?)</item>' ) . findall ( i1111 )
 for Veeveeveveveveeveev in iIiIIIi :
  ii11iIi1I ( name , url , iconimage , fanart , Veeveeveveveveeveev )
  if 94 - 94: iIiI1I11 - eevVVev . I1I11I1I1I % VeeVevVV . i11iIiiIii + Vev
  if 26 - 26: VeeVevVV - iIii1I11I1II1 - VeeveeVeveeeveV / eeveveeeev . eevev % iIii1I11I1II1
def iI ( name , url , iconimage , fanart , item ) :
 name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 url = re . compile ( '<lbscraper>(.+?)</lbscraper>' ) . findall ( item ) [ 0 ]
 fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
 eVVeeevevVevV ( name , url , 10 , iconimage , fanart )
 if 91 - 91: VeeveVeveee . iIii1I11I1II1 / I1IiIiiIII + i1IIi
def I1i ( name , url , iconimage , fanart ) :
 eeeeevevev = VVVVVeveeevVevVev ( name , url , iconimage )
 I11 = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( eeeeevevev )
 for Veeveeveveveveeveev in I11 :
  ii11iIi1I ( name , url , iconimage , fanart , Veeveeveveveveeveev )
  if 74 - 74: VeeveVeveee . i111I1
def VVVVVeveeevVevVev ( name , url , iconimage ) :
 eeeveVe = url
 I1I1i1I = ''
 if url == 'mamahd' :
  i1111 = eeevevVeveveV ( "http://mamahd.com" ) . replace ( '\n' , '' ) . replace ( '\t' , '' )
  ii1I = re . compile ( '<a href="(.+?)">.+?<img src="(.+?)"></div>.+?<div class="home cell">.+?<span>(.+?)</span>.+?<span>(.+?)</span>.+?</a>' ) . findall ( i1111 )
  for url , iconimage , VeveVev , eVev in ii1I :
   I1I1i1I = I1I1i1I + '<item>\n<title>%s vs %s</title>\n<sportsdevil>%s</sportsdevil>\n<thumbnail>%s</thumbnail>\n<fanart>fanart</fanart>\n</item>\n\n' % ( VeveVev , eVev , url , iconimage )
  return I1I1i1I
  if 75 - 75: eeVeeevV + eevev + VeeveVeveee * VeeVevVV % I1IiIiiIII . i111I1
 elif url == 'cricfree' :
  i1111 = eeevevVeveveV ( "http://cricfree.sc/football-live-stream" )
  eVI1Ii1I1 = re . compile ( '<td><span class="sport-icon(.+?)</tr>' , re . DOTALL ) . findall ( i1111 )
  for IiII111iI1ii1 in eVI1Ii1I1 :
   iI11I1II = re . compile ( '<td>(.+?)<br(.+?)</td>' ) . findall ( IiII111iI1ii1 )
   for Ii1IIiI1i , ii11IIII11I in iI11I1II :
    Ii1IIiI1i = '[COLOR red]' + Ii1IIiI1i + '[/COLOR]'
    ii11IIII11I = ii11IIII11I . replace ( '>' , '' )
   VVeee = re . compile ( '<td class="matchtime" style="color:#545454;font-weight:bold;font-size: 9px">(.+?)</td>' ) . findall ( IiII111iI1ii1 ) [ 0 ]
   VVeee = '[COLOR white](' + VVeee + ')[/COLOR]'
   eevVeevev = re . compile ( '<a style="text-decoration:none !important;color:#545454;" href="(.+?)" target="_blank">(.+?)</a></td>' ) . findall ( IiII111iI1ii1 )
   for url , iIVevVevVeeeeve in eevVeevev :
    url = url
    iIVevVevVeeeeve = iIVevVevVeeeeve
   I1I1i1I = I1I1i1I + '\n<item>\n<title>%s</title>\n<sportsdevil>%s</sportsdevil>\n' % ( Ii1IIiI1i + ' ' + VVeee + ' - ' + iIVevVevVeeeeve , url )
   I1I1i1I = I1I1i1I + '<thumbnail>iconimage</thumbnail>\n<fanart>fanart</fanart>\n</item>\n'
  return I1I1i1I
  if 56 - 56: eVVee % Vev - VeeveeVeveeeveV
 elif url == 'bigsports' :
  i1111 = eeevevVeveveV ( "http://www.bigsports.me/cat/4/football-live-stream.html" )
  ii1I = re . compile ( '<td>.+?<td>(.+?)\-(.+?)\-(.+?)</td>.+?<td>(.+?)\:(.+?)</td>.+?<td>Football</td>.+?<td><strong>(.+?)</strong></td>.+?<a target=.+? href=(.+?) class=.+?' , re . DOTALL ) . findall ( i1111 )
  for Ii1IIiI1i , VeveveevVVev , IIi1I1iiiii , eeveveVVeeVVeeve , VevVeveeVVV , name , url in ii1I :
   if not '</td>' in Ii1IIiI1i :
    url = url . replace ( '"' , '' )
    ii11IIII11I = Ii1IIiI1i + ' ' + VeveveevVVev + ' ' + IIi1I1iiiii
    VVeee = eeveveVVeeVVeeve + ':' + VevVeveeVVV
    ii11IIII11I = '[COLOR red]' + ii11IIII11I + '[/COLOR]'
    VVeee = '[COLOR white](' + VVeee + ')[/COLOR]'
    I1I1i1I = I1I1i1I + '\n<item>\n<title>%s</title>\n<sportsdevil>%s</sportsdevil>\n' % ( ii11IIII11I + ' ' + VVeee + ' ' + name , url )
    I1I1i1I = I1I1i1I + '<thumbnail>iconimage</thumbnail>\n<fanart>fanart</fanart>\n</item>\n'
  return I1I1i1I
  if 77 - 77: eevev - eevVVev - eeVeeevV
def i1IiIiiI ( name , url , iconimage , fanart , item ) :
 name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 IiiiIIiIi1 = re . compile ( '<oktitle>(.+?)</oktitle>' ) . findall ( item ) [ 0 ]
 VeVVeVeeeeVVe = re . compile ( '<line1>(.+?)</line1>' ) . findall ( item ) [ 0 ]
 eVeevV = re . compile ( '<line2>(.+?)</line2>' ) . findall ( item ) [ 0 ]
 eeevVev = re . compile ( '<line3>(.+?)</line3>' ) . findall ( item ) [ 0 ]
 iIVVevVevevev = '##' + IiiiIIiIi1 + '#' + VeVVeVeeeeVVe + '#' + eVeevV + '#' + eeevVev + '##'
 iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
 VevevevVVev ( name , iIVVevVevevev , 17 , iconimage , fanart )
 if 37 - 37: VeeeeeeeVV - Vev - VeeveVeveee
def eeveevVevVeveveVVe ( name , url ) :
 iIIIiIi = re . compile ( '##(.+?)##' ) . findall ( url ) [ 0 ] . split ( '#' )
 VVevVev = xbmcgui . Dialog ( )
 VVevVev . ok ( iIIIiIi [ 0 ] , iIIIiIi [ 1 ] , iIIIiIi [ 2 ] , iIIIiIi [ 3 ] )
 if 30 - 30: I1I11I1I1I + eVVee * VeeVevVV % i11iIiiIii % eevev
def I1i1I1II ( name , url , iconimage , fanart , item ) :
 url = re . compile ( '<redirect>(.+?)</redirect>' ) . findall ( item ) [ 0 ]
 VeeVev ( 'name' , url , 'iconimage' , 'fanart' )
 if 97 - 97: eVVee % eVVee % I1IiIiiIII / i111I1 - iIii1I11I1II1
def eeeveeeeeVev ( name , url , iconimage , fanart , item ) :
 name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 iIVVevVevevev = re . compile ( '<text>(.+?)</text>' ) . findall ( item ) [ 0 ]
 iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
 VevevevVVev ( name , iIVVevVevevev , 9 , iconimage , fanart )
 if 69 - 69: iiIiIIi
def ii1I1 ( name , url ) :
 VeeeeVVeeev = iI11Ii ( url )
 i1I1IiiIi1i ( name , VeeeeVVeeev )
 if 29 - 29: VeeveeVeveeeveV % VeeveeVeveeeveV
def III1ii1iII ( name , url , iconimage , fanart , item ) :
 VeevVev = re . compile ( '<image>(.+?)</image>' ) . findall ( item )
 if len ( VeevVev ) == 1 :
  name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  VeeevVVeVeVev = re . compile ( '<image>(.+?)</image>' ) . findall ( item ) [ 0 ]
  fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
  VevevevVVev ( name , VeeevVVeVeVev , 7 , iconimage , fanart )
 elif len ( VeevVev ) > 1 :
  name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
  eVeevVVeVev = ''
  for VeeevVVeVeVev in VeevVev : eVeevVVeVev = eVeevVVeVev + '<image>' + VeeevVVeVeVev + '</image>'
  II = IiII
  name = i1iIIi1 ( name )
  eevVeeveVeveVVevev = os . path . join ( os . path . join ( II , '' ) , name + '.txt' )
  if not os . path . exists ( eevVeeveVeveVVevev ) : file ( eevVeeveVeveVVevev , 'w' ) . close ( )
  eeevevVVeveveveveV = open ( eevVeeveVeveVVevev , "w" )
  eeevevVVeveveveveV . write ( eVeevVVeVev )
  eeevevVVeveveveveV . close ( )
  VevevevVVev ( name , 'image' , 8 , iconimage , fanart )
  if 11 - 11: eeVeeevV / eevev - eVeV * VeeeeeeeVV + VeeeeeeeVV . eevev
def Veeveev ( name , url , iconimage , fanart , item ) :
 name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 url = re . compile ( '<iptv>(.+?)</iptv>' ) . findall ( item ) [ 0 ]
 fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
 eVVeeevevVevV ( name , url , 6 , iconimage , fanart )
 if 26 - 26: iIiI1I11 % eVVee
def eevevVeeveeeeee ( url , iconimage ) :
 i1111 = iI11Ii ( url )
 VeveVeviII11 = re . compile ( '^#.+?:-?[0-9]*(.*?),(.*?)\n(.*?)$' , re . I + re . M + re . U + re . S ) . findall ( i1111 )
 iiIiii1IIIII = [ ]
 for eeveve , eVeveeveeveeVeveV , url in VeveVeviII11 :
  IIIIiiIiiI = { "params" : eeveve , "name" : eVeveeveeveeVeveV , "url" : url }
  iiIiii1IIIII . append ( IIIIiiIiiI )
 list = [ ]
 for VeeVeeeVe in iiIiii1IIIII :
  IIIIiiIiiI = { "name" : VeeVeeeVe [ "name" ] , "url" : VeeVeeeVe [ "url" ] }
  VeveVeviII11 = re . compile ( ' (.+?)="(.+?)"' , re . I + re . M + re . U + re . S ) . findall ( VeeVeeeVe [ "params" ] )
  for IIIIiI11I11 , eeeveveev in VeveVeviII11 :
   IIIIiiIiiI [ IIIIiI11I11 . strip ( ) . lower ( ) . replace ( '-' , '_' ) ] = eeeveveev . strip ( )
  list . append ( IIIIiiIiiI )
 for VeeVeeeVe in list :
  if '.ts' in VeeVeeeVe [ "url" ] : VevevevVVev ( VeeVeeeVe [ "name" ] , VeeVeeeVe [ "url" ] , 2 , iconimage , eevVeVeVVevev )
  else : VeveevVevevVeeveev ( VeeVeeeVe [ "name" ] , VeeVeeeVe [ "url" ] , 2 , iconimage , eevVeVeVVevev )
  if 4 - 4: iIiI1I11 % I1IiIiiIII * eeveveeeev
def eVVeveveVV ( name , url , iconimage , fanart , item ) :
 I1ii11iIi11i = ''
 eevVevVVVVeVVev = re . compile ( '<link>(.+?)</link>' ) . findall ( item )
 eVeeveeeeeveve = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>' ) . findall ( item )
 for name , ii , iconimage , fanart in eVeeveeeeeveve :
  if 'youtube.com/playlist?' in ii :
   i1Iii1i1I = ii . split ( 'list=' ) [ 1 ]
   eVVeeevevVevV ( name , ii , VeveVeeveve , iconimage , fanart , description = i1Iii1i1I )
 if len ( eevVevVVVVeVVev ) == 1 :
  eVeeveeeeeveve = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>' ) . findall ( item )
  for name , url , iconimage , fanart in eVeeveeeeeveve :
   try :
    I1ii11iIi11i = VVeVVeveeeveeV ( url )
    eeveeeeVeveevV = url . split ( '/' ) [ 2 ] . replace ( 'www.' , '' )
    if 'SportsDevil' in url : eeveeeeVeveevV = ''
   except : pass
   if '.ts' in url : VeveevVevevVeeveev ( name , url , 16 , iconimage , fanart , description = '' )
   if '<meta>' in item :
    eeeeeVeeeveee = re . compile ( '<meta>(.+?)</meta>' ) . findall ( item ) [ 0 ]
    VeveveV ( name + I1ii11iIi11i , url , 2 , iconimage , 10 , eeeeeVeeeveee , isFolder = False )
   else :
    VeveevVevevVeeveev ( name + I1ii11iIi11i , url , 2 , iconimage , fanart )
 elif len ( eevVevVVVVeVVev ) > 1 :
  name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
  if '.ts' in url : VeveevVevevVeeveev ( name , url , 16 , iconimage , fanart , description = '' )
  if '<meta>' in item :
   eeeeeVeeeveee = re . compile ( '<meta>(.+?)</meta>' ) . findall ( item ) [ 0 ]
   VeveveV ( name , url , 3 , iconimage , len ( eevVevVVVVeVVev ) , eeeeeVeeeveee , isFolder = True )
  else :
   eVVeeevevVevV ( name , url , 3 , iconimage , fanart )
   if 24 - 24: Vev * VeeveVeveee
   if 29 - 29: VeeveeVeveeeveV % I1I11I1I1I - VeeveeVeveeeveV / I1I11I1I1I . i1IIi
def I11I11i1I ( name , url , iconimage , fanart , item ) :
 eevVevVVVVeVVev = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( item )
 i11III1111iIi = re . compile ( '<link>(.+?)</link>' ) . findall ( item )
 if len ( eevVevVVVVeVVev ) + len ( i11III1111iIi ) == 1 :
  name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  url = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( item ) [ 0 ]
  url = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' + url
  VevevevVVev ( name , url , 16 , iconimage , fanart )
 elif len ( eevVevVVVVeVVev ) + len ( i11III1111iIi ) > 1 :
  name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  eVVeeevevVevV ( name , url , 3 , iconimage , fanart )
  if 38 - 38: i111I1 + VeeVevVV / iiIiIIi % eeVeeevV - eVVee
def VeveevVe ( link ) :
 if iIiiiI == '' :
  VVevVev = xbmcgui . Dialog ( )
  iI11Ii1I = VVevVev . yesno ( 'Adult Content' , 'You have found the goodies ;)' , '' , 'Please set a password to prevent accidental access' , 'Cancel' , 'OK' )
  if iI11Ii1I == 1 :
   eevVVeveeveeveve = xbmc . Keyboard ( '' , 'Set Password' )
   eevVVeveeveeveve . doModal ( )
   if ( eevVVeveeveeveve . isConfirmed ( ) ) :
    eVeev = eevVVeveeveeveve . getText ( )
    i1iII1IiiIiI1 . setSetting ( 'password' , eVeev )
  else : quit ( )
 elif iIiiiI <> '' :
  VVevVev = xbmcgui . Dialog ( )
  iI11Ii1I = VVevVev . yesno ( 'Adult Content' , 'Please enter the password you set!' , 'to continue' , 'dirty git' , 'Cancel' , 'OK' )
  if iI11Ii1I == 1 :
   eevVVeveeveeveve = xbmc . Keyboard ( '' , 'Enter Password' )
   eevVVeveeveeveve . doModal ( )
   if ( eevVVeveeveeveve . isConfirmed ( ) ) :
    eVeev = eevVVeveeveeveve . getText ( )
   if eVeev <> iIiiiI :
    quit ( )
  else : quit ( )
  if 56 - 56: VeeveVeveee + eevVVev + eevev - eeVeeevV . eevev
def VVVeee ( name , url , iconimage ) :
 VeeVevVVeevVVeeveevVevV = ''
 iII111ii = i1iIIi1 ( name )
 i1iII1IiiIiI1 . setSetting ( 'tv' , iII111ii )
 i1111 = i11 ( url )
 eevVVeveeveVVVevV = re . compile ( '<title>.*?' + re . escape ( name ) + '.*?</title>(.+?)</item>' , re . DOTALL ) . findall ( i1111 ) [ 0 ]
 iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( eevVVeveeveVVVevV ) [ 0 ]
 eevVevVVVVeVVev = [ ]
 if '<link>' in eevVVeveeveVVVevV :
  iII1i11 = re . compile ( '<link>(.+?)</link>' ) . findall ( eevVVeveeveVVVevV )
  for VeeIiIIII1i11I in iII1i11 :
   eevVevVVVVeVVev . append ( VeeIiIIII1i11I )
 if '<sportsdevil>' in eevVVeveeveVVVevV :
  VVV = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( eevVVeveeveVVVevV )
  for iII1 in VVV :
   iII1 = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' + iII1
   eevVevVVVVeVVev . append ( iII1 )
 iiII1i1 = 1
 for i1111 in eevVevVVVVeVVev :
  if '(' in i1111 :
   i1111 = i1111 . split ( '(' )
   VeeVevVVeevVVeeveevVevV = i1111 [ 1 ] . replace ( ')' , '' )
   i1111 = i1111 [ 0 ]
  I1ii11iIi11i = VVeVVeveeeveeV ( i1111 )
  eeveeeeVeveevV = i1111 . split ( '/' ) [ 2 ] . replace ( 'www.' , '' )
  if VeeVevVVeevVVeeveevVevV <> '' : name = "Link " + str ( iiII1i1 ) + ' | ' + VeeVevVVeevVVeeveevVevV + I1ii11iIi11i
  else : name = "Link " + str ( iiII1i1 ) + ' | ' + eeveeeeVeveevV + I1ii11iIi11i
  iiII1i1 = iiII1i1 + 1
  VeveveV ( name , i1111 , 2 , iconimage , 10 , '' , isFolder = False , description = i1iII1IiiIiI1 . getSetting ( 'tv' ) )
  if 57 - 57: VeeveVeveee . i1IIi . eVeV * i11iIiiIii + iiIiIIi . eVeV
def Ii1I ( name , url , iconimage , fanart , item ) :
 eVeeveeeeeveve = re . compile ( '<title>(.+?)</title>.+?folder>(.+?)</folder>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>' ) . findall ( item )
 for name , url , iconimage , fanart in eVeeveeeeeveve :
  if 'youtube.com/channel/' in url :
   i1Iii1i1I = url . split ( 'channel/' ) [ 1 ]
   eVVeeevevVevV ( name , url , VeveVeeveve , iconimage , fanart , description = i1Iii1i1I )
  elif 'youtube.com/user/' in url :
   i1Iii1i1I = url . split ( 'user/' ) [ 1 ]
   eVVeeevevVevV ( name , url , VeveVeeveve , iconimage , fanart , description = i1Iii1i1I )
  elif 'youtube.com/playlist?' in url :
   i1Iii1i1I = url . split ( 'list=' ) [ 1 ]
   eVVeeevevVevV ( name , url , VeveVeeveve , iconimage , fanart , description = i1Iii1i1I )
  elif 'plugin://' in url :
   eeevVevevVeeeevVev = HTMLParser ( )
   url = eeevVevevVeeeevVev . unescape ( url )
   eVVeeevevVevV ( name , url , VeveVeeveve , iconimage , fanart )
  else :
   eVVeeevevVevV ( name , url , 1 , iconimage , fanart )
   if 34 - 34: eeVeeevV . VeeveVeveee % Vev * i111I1 + VeeveeVeveeeveV
def VeveeevV ( ) :
 eevVVeveeveeveve = xbmc . Keyboard ( '' , '[B][COLOR red]S[/COLOR][COLOR white]earch[/COLOR][/B] [B][COLOR red]E[/COLOR][COLOR white]volve[/COLOR][/B]' )
 eevVVeveeveeveve . doModal ( )
 if ( eevVVeveeveeveve . isConfirmed ( ) ) :
  i1Iii1i1I = eevVVeveeveeveve . getText ( )
  i1Iii1i1I = i1Iii1i1I . upper ( )
 else : quit ( )
 i1111 = i11 ( 'http://evolverepo.net/anewEvolvemenu/search.xml' )
 i1Ii = re . compile ( '<link>(.+?)</link>' ) . findall ( i1111 )
 for eeeveevVevev in i1Ii :
  try :
   i1111 = i11 ( eeeveevVevev )
   ii111iI1iIi1 = re . compile ( '<item>(.+?)</item>' ) . findall ( i1111 )
   for Veeveeveveveveeveev in ii111iI1iIi1 :
    I11 = re . compile ( '<title>(.+?)</title>' ) . findall ( Veeveeveveveveeveev )
    for iIi1i111II in I11 :
     iIi1i111II = iIi1i111II . upper ( )
     if i1Iii1i1I in iIi1i111II :
      ii11iIi1I ( eVeveeveeveeVeveV , eeeveevVevev , eV , eevVeVeVVevev , Veeveeveveveveeveev )
  except : pass
  if 36 - 36: I1I11I1I1I + Vev - iIiI1I11 - Vev % VeeVevVV . I1IiIiiIII
def eee ( url ) :
 I1I1i1I = "ShowPicture(%s)" % url
 xbmc . executebuiltin ( I1I1i1I )
 if 36 - 36: VeeeeeeeVV . eeveveeeev
def eVIIiIi ( name , url , iconimage , description ) :
 if description : name = description
 try :
  if 'plugin://plugin.video.SportsDevil/' in url :
   VVeVeeVeVVVee ( name , url , iconimage )
  elif '.ts' in url :
   url = 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;name=' + name + '&amp;url=' + url
   url = url . replace ( '|' , '' )
   VVeVeeVeVVVee ( name , url , iconimage )
  elif urlresolver . HostedMediaFile ( url ) . valid_url ( ) :
   url = urlresolver . HostedMediaFile ( url ) . resolve ( )
   Iiii1iI1i ( name , url , iconimage )
  elif liveresolver . isValid ( url ) == True :
   url = liveresolver . resolve ( url )
   Iiii1iI1i ( name , url , iconimage )
  else : Iiii1iI1i ( name , url , iconimage )
 except :
  I1ii1ii11i1I ( eevVeVV ( 'Evolve' ) , 'Stream Unavailable' , '3000' , VevV )
  if 55 - 55: eeVeeevV - VeeVevVV + eevVVev + i111I1 % iIiI1I11
def Vee ( url ) :
 if urlresolver . HostedMediaFile ( url ) . valid_url ( ) :
  url = urlresolver . HostedMediaFile ( url ) . resolve ( )
 xbmc . Player ( ) . play ( url )
 if 41 - 41: i1IIi - VeeVevVV - iIiI1I11
def Iiii1iI1i ( name , url , iconimage ) :
 III11I1 = True
 IIi1IIIi = xbmcgui . ListItem ( name , iconImage = iconimage , thumbnailImage = iconimage ) ; IIi1IIIi . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
 III11I1 = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = url , listitem = IIi1IIIi )
 IIi1IIIi . setPath ( url )
 xbmcplugin . setResolvedUrl ( int ( sys . argv [ 1 ] ) , True , IIi1IIIi )
 if 99 - 99: iIiI1I11 + eeveveeeev * eevVVev . VeeveVeveee - eVVee
def VVeVeeVeVVVee ( name , url , iconimage ) :
 xbmc . executebuiltin ( 'Dialog.Close(all,True)' )
 III11I1 = True
 IIi1IIIi = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage ) ; IIi1IIIi . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
 III11I1 = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = url , listitem = IIi1IIIi )
 xbmc . Player ( ) . play ( url , IIi1IIIi , False )
 if 58 - 58: iIiI1I11 + VeeveVeveee - VeeveeVeveeeveV
def i1i1ii ( url ) :
 xbmc . executebuiltin ( "PlayMedia(%s)" % url )
 if 46 - 46: eevev + eeveveeeev
def i11 ( url ) :
 eeveevV = urllib2 . Request ( url )
 eeveevV . add_header ( 'User-Agent' , 'mat' )
 eeeeVeveVeVVeV = urllib2 . urlopen ( eeveevV )
 i1111 = eeeeVeveVeVVeV . read ( )
 eeeeVeveVeVVeV . close ( )
 i1111 = i1111 . replace ( '<fanart></fanart>' , '<fanart>x</fanart>' ) . replace ( '<thumbnail></thumbnail>' , '<thumbnail>x</thumbnail>' ) . replace ( '<utube>' , '<link>https://www.youtube.com/watch?v=' ) . replace ( '</utube>' , '</link>' )
 if '{' in i1111 :
  I1I1i1I = i1111 [ : : - 1 ]
  I1I1i1I = I1I1i1I . replace ( '}' , '' ) . replace ( '{' , '' ) . replace ( ',' , '' ) . replace ( ']' , '' ) . replace ( '[' , '' )
  I1I1i1I = I1I1i1I + '=='
  i1111 = I1I1i1I . decode ( 'base64' )
 if url <> iI111iI : i1111 = i1111 . replace ( '\n' , '' ) . replace ( '\r' , '' )
 print i1111
 return i1111
 if 20 - 20: VeeVevVV + iIiI1I11 / Vev % iIii1I11I1II1
def iI11Ii ( url ) :
 eeveevV = urllib2 . Request ( url )
 eeveevV . add_header ( 'User-Agent' , 'mat' )
 eeeeVeveVeVVeV = urllib2 . urlopen ( eeveevV )
 i1111 = eeeeVeveVeVVeV . read ( )
 eeeeVeveVeVVeV . close ( )
 return i1111
 if 88 - 88: eevev / eevVVev
def eeevevVeveveV ( url ) :
 eeveevV = urllib2 . Request ( url )
 eeveevV . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' )
 eeeeVeveVeVVeV = urllib2 . urlopen ( eeveevV )
 i1111 = eeeeVeveVeVVeV . read ( )
 eeeeVeveVeVVeV . close ( )
 i1111 = i1111 . replace ( '\n' , '' ) . replace ( '\r' , '' )
 return i1111
 if 87 - 87: eVVee - eVVee - i111I1 + I1IiIiiIII
 if 82 - 82: I1IiIiiIII / iIii1I11I1II1 . VeeveeVeveeeveV . I1I11I1I1I / VeeveVeveee
def iiI1I1 ( ) :
 eeV = [ ]
 iiVVevVevVee = sys . argv [ 2 ]
 if len ( iiVVevVevVee ) >= 2 :
  eeveve = sys . argv [ 2 ]
  eVeVev = eeveve . replace ( '?' , '' )
  if ( eeveve [ len ( eeveve ) - 1 ] == '/' ) :
   eeveve = eeveve [ 0 : len ( eeveve ) - 2 ]
  Veev = eVeVev . split ( '&' )
  eeV = { }
  for iiII1i1 in range ( len ( Veev ) ) :
   eeevVeveeveveevV = { }
   eeevVeveeveveevV = Veev [ iiII1i1 ] . split ( '=' )
   if ( len ( eeevVeveeveveevV ) ) == 2 :
    eeV [ eeevVeveeveveevV [ 0 ] ] = eeevVeveeveveevV [ 1 ]
 return eeV
 if 35 - 35: eeVeeevV + i1IIi % eVVee % VeeVevVV + I1IiIiiIII
def I1ii1ii11i1I ( title , message , ms , nart ) :
 xbmc . executebuiltin ( "XBMC.notification(" + title + "," + message + "," + ms + "," + nart + ")" )
 if 17 - 17: i1IIi
def i1iIIi1 ( string ) :
 iiIi1i = re . compile ( '(\[.+?\])' ) . findall ( string )
 for I1i11111i1i11 in iiIi1i : string = string . replace ( I1i11111i1i11 , '' )
 return string
 if 77 - 77: eVVee + eeveveeeev / I1IiIiiIII + Vev * VeeveVeveee
def eevVeVV ( string ) :
 string = string . split ( ' ' )
 I1ii11 = ''
 for eVeVeVeeev in string :
  III1ii1I = '[B][COLOR red]' + eVeVeVeeev [ 0 ] . upper ( ) + '[/COLOR][COLOR white]' + eVeVeVeeev [ 1 : ] + '[/COLOR][/B] '
  I1ii11 = I1ii11 + III1ii1I
 return I1ii11
 if 13 - 13: i11iIiiIii + i1IIi * iIii1I11I1II1 % VeeeeeeeVV - eevVVev * I1I11I1I1I
def VeveveV ( name , url , mode , iconimage , itemcount , metatype , isFolder = False , description = '' ) :
 if isFolder == True : i1iII1IiiIiI1 . setSetting ( 'favtype' , 'folder' )
 else : i1iII1IiiIiI1 . setSetting ( 'favtype' , 'link' )
 if Iii1ii1II11i == 'true' :
  iiIi1iI1iIii = name
  name = i1iIIi1 ( name )
  eevevVeeVevee = ""
  eeveeveVeVVevV = ""
  i1ii1II1ii = [ ]
  iII111Ii = eval ( base64 . b64decode ( 'bWV0YWhhbmRsZXJzLk1ldGFEYXRhKHRtZGJfYXBpX2tleT0iZDk1NWQ4ZjAyYTNmMjQ4MGE1MTg4MWZlNGM5NmYxMGUiKQ==' ) )
  eevevVeeVeee = { }
  if metatype == 'movie' :
   Veeveveve = name . partition ( '(' )
   if len ( Veeveveve ) > 0 :
    eevevVeeVevee = Veeveveve [ 0 ]
    eeveeveVeVVevV = Veeveveve [ 2 ] . partition ( ')' )
   if len ( eeveeveVeVVevV ) > 0 :
    eeveeveVeVVevV = eeveeveVeVVevV [ 0 ]
   eevevVeeVeee = iII111Ii . get_meta ( 'movie' , name = eevevVeeVevee , year = eeveeveVeVVevV )
   if not eevevVeeVeee [ 'trailer' ] == '' : i1ii1II1ii . append ( ( eevVeVV ( 'Play Trailer' ) , 'XBMC.RunPlugin(%s)' % ee . build_plugin_url ( { 'mode' : 11 , 'url' : eevevVeeVeee [ 'trailer' ] } ) ) )
  elif metatype == 'tvep' :
   iIi1i111II = i1iII1IiiIiI1 . getSetting ( 'tv' )
   if '<>' in url :
    print url
    iIIIi1 = url . split ( '<>' ) [ 0 ]
    i11i1 = url . split ( '<>' ) [ 1 ]
    IIIii1II1II = url . split ( '<>' ) [ 2 ]
    i1I1iI = url . split ( '<>' ) [ 3 ]
    eeevVeeVVeev = url . split ( '<>' ) [ 4 ]
    eevV = url . split ( '<>' ) [ 5 ]
    eevevVeeVeee = iII111Ii . get_episode_meta ( i11i1 , imdb_id = iIIIi1 , season = IIIii1II1II , episode = i1I1iI , air_date = '' , episode_title = '' , overlay = '' )
   else :
    VeeevevVeVVV = re . compile ( 'Season (.+?) Episode (.+?)\)' ) . findall ( name )
    for VeevVVeveveveveeee , IIII1iII in VeeevevVeVVV :
     eevevVeeVeee = iII111Ii . get_episode_meta ( iIi1i111II , imdb_id = '' , season = VeevVVeveveveveeee , episode = IIII1iII , air_date = '' , episode_title = '' , overlay = '' )
  try :
   if eevevVeeVeee [ 'cover_url' ] == '' : iconimage = iconimage
   else : iconimage = eevevVeeVeee [ 'cover_url' ]
  except : pass
  ii1III11 = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&fanart=" + urllib . quote_plus ( eevVeVeVVevev ) + "&iconimage=" + urllib . quote_plus ( iconimage )
  III11I1 = True
  IIi1IIIi = xbmcgui . ListItem ( iiIi1iI1iIii , iconImage = iconimage , thumbnailImage = iconimage )
  IIi1IIIi . setInfo ( type = "Video" , infoLabels = eevevVeeVeee )
  IIi1IIIi . setProperty ( "IsPlayable" , "true" )
  IIi1IIIi . addContextMenuItems ( i1ii1II1ii , replaceItems = False )
  if not eevevVeeVeee . get ( 'backdrop_url' , '' ) == '' : IIi1IIIi . setProperty ( 'fanart_image' , eevevVeeVeee [ 'backdrop_url' ] )
  else : IIi1IIIi . setProperty ( 'fanart_image' , eevVeVeVVevev )
  I1iiIIIi11 = i1iII1IiiIiI1 . getSetting ( 'favlist' )
  Ii1I11ii1i = [ ]
  Ii1I11ii1i . append ( ( eevVeVV ( 'Stream Information' ) , 'XBMC.Action(Info)' ) )
  if I1iiIIIi11 == 'yes' : Ii1I11ii1i . append ( ( '[COLOR white]Remove from Evolve Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=21&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
  else : Ii1I11ii1i . append ( ( '[COLOR white]Add to Evolve Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=20&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
  IIi1IIIi . addContextMenuItems ( Ii1I11ii1i , replaceItems = False )
  III11I1 = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = ii1III11 , listitem = IIi1IIIi , isFolder = isFolder , totalItems = itemcount )
  return III11I1
 else :
  if isFolder :
   eVVeeevevVevV ( name , url , mode , iconimage , eevVeVeVVevev , description = '' )
  else :
   VeveevVevevVeeveev ( name , url , mode , iconimage , eevVeVeVVevev , description = '' )
   if 89 - 89: i111I1 . Vev / eVVee % eevev . I1i1iI1i
def eVVeeevevVevV ( name , url , mode , iconimage , fanart , description = '' ) :
 i1iII1IiiIiI1 . setSetting ( 'favtype' , 'folder' )
 ii1III11 = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&fanart=" + urllib . quote_plus ( fanart ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 III11I1 = True
 IIi1IIIi = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 IIi1IIIi . setInfo ( type = "Video" , infoLabels = { "Title" : name , 'plot' : description } )
 IIi1IIIi . setProperty ( 'fanart_image' , fanart )
 if 'youtube.com/channel/' in url :
  ii1III11 = 'plugin://plugin.video.youtube/channel/' + description + '/'
 if 'youtube.com/user/' in url :
  ii1III11 = 'plugin://plugin.video.youtube/user/' + description + '/'
 if 'youtube.com/playlist?' in url :
  ii1III11 = 'plugin://plugin.video.youtube/playlist/' + description + '/'
 if 'plugin://' in url :
  ii1III11 = url
 Ii1I11ii1i = [ ]
 I1iiIIIi11 = i1iII1IiiIiI1 . getSetting ( 'favlist' )
 if I1iiIIIi11 == 'yes' : Ii1I11ii1i . append ( ( '[COLOR white]Remove from Evolve Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=21&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 else : Ii1I11ii1i . append ( ( '[COLOR white]Add to Evolve Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=20&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 IIi1IIIi . addContextMenuItems ( Ii1I11ii1i , replaceItems = False )
 III11I1 = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = ii1III11 , listitem = IIi1IIIi , isFolder = True )
 return III11I1
 if 50 - 50: eevVVev + eVVee . i1IIi % VeeveVeveee
def VevevevVVev ( name , url , mode , iconimage , fanart , description = '' ) :
 i1iII1IiiIiI1 . setSetting ( 'favtype' , 'link' )
 ii1III11 = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&fanart=" + urllib . quote_plus ( fanart ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 III11I1 = True
 IIi1IIIi = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 IIi1IIIi . setProperty ( 'fanart_image' , fanart )
 Ii1I11ii1i = [ ]
 I1iiIIIi11 = i1iII1IiiIiI1 . getSetting ( 'favlist' )
 if I1iiIIIi11 == 'yes' : Ii1I11ii1i . append ( ( '[COLOR white]Remove from Evolve Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=21&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 else : Ii1I11ii1i . append ( ( '[COLOR white]Add to Evolve Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=20&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 IIi1IIIi . addContextMenuItems ( Ii1I11ii1i , replaceItems = False )
 III11I1 = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = ii1III11 , listitem = IIi1IIIi , isFolder = False )
 return III11I1
 if 5 - 5: eevev / VeeeeeeeVV + eVeV * iiIiIIi - eeveveeeev % VeeveeVeveeeveV
def VeveevVevevVeeveev ( name , url , mode , iconimage , fanart , description = '' ) :
 i1iII1IiiIiI1 . setSetting ( 'favtype' , 'link' )
 ii1III11 = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&fanart=" + urllib . quote_plus ( fanart ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 III11I1 = True
 IIi1IIIi = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 IIi1IIIi . setProperty ( 'fanart_image' , fanart )
 IIi1IIIi . setProperty ( "IsPlayable" , "true" )
 Ii1I11ii1i = [ ]
 I1iiIIIi11 = i1iII1IiiIiI1 . getSetting ( 'favlist' )
 if I1iiIIIi11 == 'yes' : Ii1I11ii1i . append ( ( '[COLOR white]Remove from Evolve Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=21&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 else : Ii1I11ii1i . append ( ( '[COLOR white]Add to Evolve Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=20&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 IIi1IIIi . addContextMenuItems ( Ii1I11ii1i , replaceItems = False )
 III11I1 = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = ii1III11 , listitem = IIi1IIIi , isFolder = False )
 return III11I1
 if 42 - 42: Vev / VeeveVeveee + VeeeeeeeVV * eeVeeevV % eeVeeevV
def i1 ( url , name ) :
 i1iIi = iI11Ii ( url )
 if len ( i1iIi ) > 1 :
  II = IiII
  eevVeeveVeveVVevev = os . path . join ( os . path . join ( II , '' ) , name + '.txt' )
  if not os . path . exists ( eevVeeveVeveVVevev ) :
   file ( eevVeeveVeveVVevev , 'w' ) . close ( )
  IIIII = open ( eevVeeveVeveVVevev )
  eeveeVeVeveveveV = IIIII . read ( )
  if eeveeVeVeveveveV == i1iIi : pass
  else :
   i1I1IiiIi1i ( '[B][COLOR red]E[/COLOR][COLOR white]volve[/COLOR][/B] [B][COLOR red]I[/COLOR][COLOR white]nformation[/COLOR][/B]' , i1iIi )
   eeevevVVeveveveveV = open ( eevVeeveVeveVVevev , "w" )
   eeevevVVeveveveveV . write ( i1iIi )
   eeevevVVeveveveveV . close ( )
   if 85 - 85: VeeveVeveee . eevev / eeVeeevV . Vev % iiIiIIi
def i1I1IiiIi1i ( heading , text ) :
 id = 10147
 xbmc . executebuiltin ( 'ActivateWindow(%d)' % id )
 xbmc . sleep ( 500 )
 VVeveeeeveVV = xbmcgui . Window ( id )
 eeevevev = 50
 while ( eeevevev > 0 ) :
  try :
   xbmc . sleep ( 10 )
   eeevevev -= 1
   VVeveeeeveVV . getControl ( 1 ) . setLabel ( heading )
   VVeveeeeveVV . getControl ( 5 ) . setText ( text )
   return
  except :
   pass
   if 32 - 32: i1IIi . iIiI1I11
def eVV ( name ) :
 global Icon
 global Next
 global Previous
 global window
 global Quit
 global images
 eevVeeveVeveVVevev = os . path . join ( os . path . join ( IiII , '' ) , name + '.txt' )
 IIIII = open ( eevVeeveVeveVVevev )
 eeveeVeVeveveveV = IIIII . read ( )
 images = re . compile ( '<image>(.+?)</image>' ) . findall ( eeveeVeVeveveveV )
 i1iII1IiiIiI1 . setSetting ( 'pos' , '0' )
 window = pyxbmct . AddonDialogWindow ( '' )
 Veee = '/resources/art'
 I1i1iiiII1i = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + eevVVevev + Veee , 'next_focus.png' ) )
 eVeveVev = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + eevVVevev + Veee , 'next1.png' ) )
 i1i1IIIIi1i = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + eevVVevev + Veee , 'previous_focus.png' ) )
 Ii11iiI = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + eevVVevev + Veee , 'previous.png' ) )
 IIi1iiii1iI = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + eevVVevev + Veee , 'close_focus.png' ) )
 iIiiii = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + eevVVevev + Veee , 'close.png' ) )
 VevevevevVVVev = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + eevVVevev + Veee , 'main-bg1.png' ) )
 window . setGeometry ( 1300 , 720 , 100 , 50 )
 eeeev = pyxbmct . Image ( VevevevevVVVev )
 window . placeControl ( eeeev , - 10 , - 10 , 130 , 70 )
 iIVVevVevevev = '0xFF000000'
 Previous = pyxbmct . Button ( '' , focusTexture = i1i1IIIIi1i , noFocusTexture = Ii11iiI , textColor = iIVVevVevevev , focusedColor = iIVVevVevevev )
 Next = pyxbmct . Button ( '' , focusTexture = I1i1iiiII1i , noFocusTexture = eVeveVev , textColor = iIVVevVevevev , focusedColor = iIVVevVevevev )
 Quit = pyxbmct . Button ( '' , focusTexture = IIi1iiii1iI , noFocusTexture = iIiiii , textColor = iIVVevVevevev , focusedColor = iIVVevVevevev )
 Icon = pyxbmct . Image ( images [ 0 ] , aspectRatio = 2 )
 window . placeControl ( Previous , 102 , 1 , 10 , 10 )
 window . placeControl ( Next , 102 , 40 , 10 , 10 )
 window . placeControl ( Quit , 102 , 21 , 10 , 10 )
 window . placeControl ( Icon , 0 , 0 , 100 , 50 )
 Previous . controlRight ( Next )
 Previous . controlUp ( Quit )
 window . connect ( Previous , eVeveveveVeeveveeve )
 window . connect ( Next , VeveveVev )
 Previous . setVisible ( False )
 window . setFocus ( Quit )
 Previous . controlRight ( Quit )
 Quit . controlLeft ( Previous )
 Quit . controlRight ( Next )
 Next . controlLeft ( Quit )
 window . connect ( Quit , window . close )
 window . doModal ( )
 del window
 if 70 - 70: VeeVevVV . eVVee * VeeeeeeeVV - eVeV * VeeveeVeveeeveV + eevev
def VeveveVev ( ) :
 iIi1 = int ( i1iII1IiiIiI1 . getSetting ( 'pos' ) )
 i11iiI1111 = int ( iIi1 ) + 1
 i1iII1IiiIiI1 . setSetting ( 'pos' , str ( i11iiI1111 ) )
 eVeeeeevevevVeevev = len ( images )
 Icon . setImage ( images [ int ( i11iiI1111 ) ] )
 Previous . setVisible ( True )
 if int ( i11iiI1111 ) == int ( eVeeeeevevevVeevev ) - 1 :
  Next . setVisible ( False )
  if 93 - 93: eVVee / VeeveeVeveeeveV / iIii1I11I1II1 % iiIiIIi % iiIiIIi
def eVeveveveVeeveveeve ( ) :
 iIi1 = int ( i1iII1IiiIiI1 . getSetting ( 'pos' ) )
 IiI11iI1i1i1i = int ( iIi1 ) - 1
 i1iII1IiiIiI1 . setSetting ( 'pos' , str ( IiI11iI1i1i1i ) )
 Icon . setImage ( images [ int ( IiI11iI1i1i1i ) ] )
 Next . setVisible ( True )
 if int ( IiI11iI1i1i1i ) == 0 :
  Previous . setVisible ( False )
  if 89 - 89: VeeVevVV
def Veeeeee ( url , fanart ) :
 i1iII1IiiIiI1 . setSetting ( 'favlist' , 'yes' )
 I1IIIiI1I1ii1 = None
 file = open ( iI1Ii11111iIi , 'r' )
 I1IIIiI1I1ii1 = file . read ( ) . replace ( '\n' , '' ) . replace ( '\r' , '' )
 I11 = re . compile ( "<item>(.+?)</item>" , re . DOTALL ) . findall ( I1IIIiI1I1ii1 )
 for Veeveeveveveveeveev in I11 :
  ii11iIi1I ( eVeveeveeveeVeveV , url , VevV , fanart , Veeveeveveveveeveev )
 i1iII1IiiIiI1 . setSetting ( 'favlist' , 'no' )
 if 30 - 30: Vev * VeeeeeeeVV
def I1iIIIi1 ( name , url , iconimage , fanart ) :
 Iii = i1iII1IiiIiI1 . getSetting ( 'favtype' )
 url = url . replace ( ' ' , '%20' )
 iconimage = iconimage . replace ( ' ' , '%20' )
 if '<>' in url :
  iIIIi1 = url . split ( '<>' ) [ 0 ]
  IIIii1II1II = url . split ( '<>' ) [ 1 ]
  i1I1iI = url . split ( '<>' ) [ 2 ]
  eeevVeeVVeev = url . split ( '<>' ) [ 3 ]
  eevV = url . split ( '<>' ) [ 4 ]
  I1I1i1I = '<FAV><item>\n<title>' + name + '</title>\n<meta>tvep</meta>\n<nan>tvshow</nan>\n<showyear>' + eeevVeeVVeev + '</showyear>\n<imdb>' + iIIIi1 + '</imdb>\n<season>' + IIIii1II1II + '</season>\n<episode>' + i1I1iI + '</episode>\n<episodeyear>' + eevV + '</episodeyear>\n<thumbnail>' + iconimage + '</thumbnail>\n<fanart>' + fanart + '</fanart></item></FAV>\n'
 elif len ( url ) == 9 :
  I1I1i1I = '<FAV><item>\n<title>' + name + '</title>\n<meta>movie</meta>\n<nan>movie</nan>\n<imdb>' + url + '</imdb>\n' + '<thumbnail>' + iconimage + '</thumbnail>\n<fanart>' + fanart + '</fanart></item></FAV>\n'
 else :
  I1I1i1I = '<FAV><item>\n<title>' + name + '</title>\n<' + Iii + '>' + url + '</' + Iii + '>\n' + '<thumbnail>' + iconimage + '</thumbnail>\n<fanart>' + fanart + '</fanart></item></FAV>\n'
 i1i1II = open ( iI1Ii11111iIi , 'a' )
 i1i1II . write ( I1I1i1I )
 i1i1II . close ( )
 if 19 - 19: VeeVevVV % eevVVev / i11iIiiIii / i111I1 - VeeeeeeeVV
def iIIii ( name , url , iconimage ) :
 print name
 I1IIIiI1I1ii1 = None
 file = open ( iI1Ii11111iIi , 'r' )
 I1IIIiI1I1ii1 = file . read ( )
 i1iIiIi1I = ''
 I11 = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( I1IIIiI1I1ii1 )
 for eVeeveeeeeveve in I11 :
  I1I1i1I = '\n<FAV><item>\n' + eVeeveeeeeveve + '</item>\n'
  if name in eVeeveeeeeveve :
   print 'xxxxxxxxxxxxxxxxx'
   I1I1i1I = I1I1i1I . replace ( 'item' , ' ' )
  i1iIiIi1I = i1iIiIi1I + I1I1i1I
 file = open ( iI1Ii11111iIi , 'w' )
 file . truncate ( )
 file . write ( i1iIiIi1I )
 file . close ( )
 xbmc . executebuiltin ( 'Container.Refresh' )
 if 45 - 45: i1IIi + eevVVev
def VVeVVeveeeveeV ( url ) :
 try :
  eeveeeeVeveevV = url . split ( '/' ) [ 2 ] . replace ( 'www.' , '' )
  file = open ( I1ii11iIi11i , 'r' )
  IiII1II11I = file . read ( )
  if eeveeeeVeveevV in IiII1II11I : return '[COLOR springgreen] (RD)[/COLOR]'
  else : return ''
 except : return ''
 if 54 - 54: eVeV + Vev + VeeVevVV * iiIiIIi - I1I11I1I1I % I1IiIiiIII
def I111 ( ) :
 xbmcaddon . Addon ( 'script.module.nanscrapers' ) . openSettings ( )
 if 13 - 13: eeveveeeev * I1IiIiiIII * i111I1
def IiIIiiI11III ( ) :
 xbmcaddon . Addon ( 'script.module.urlresolver' ) . openSettings ( )
 if 42 - 42: eVVee
def VVeeVVVVVVeee ( ) :
 xbmcaddon . Addon ( 'script.module.metahandler' ) . openSettings ( )
 if 61 - 61: eVeV . i1IIi / iiIiIIi % i11iIiiIii * i111I1
def II11iiii1Ii ( link ) :
 try :
  i1i1i1I = re . compile ( '<layouttype>(.+?)</layouttype>' ) . findall ( link ) [ 0 ]
  if i1i1i1I == 'thumbnail' : xbmc . executebuiltin ( 'Container.SetViewMode(500)' )
  else : xbmc . executebuiltin ( 'Container.SetViewMode(50)' )
 except : pass
 if 83 - 83: I1IiIiiIII + VeeeeeeeVV
 if 22 - 22: iIiI1I11 % i111I1 * VeeeeeeeVV - VeeveVeveee / iIii1I11I1II1
eeveve = iiI1I1 ( ) ; eeeveevVevev = None ; eVeveeveeveeVeveV = None ; VeveVeeveve = None ; VeVVevev = None ; eV = None ; IIiiIIi1 = None
try : VeVVevev = urllib . unquote_plus ( eeveve [ "site" ] )
except : pass
try : eeeveevVevev = urllib . unquote_plus ( eeveve [ "url" ] )
except : pass
try : eVeveeveeveeVeveV = urllib . unquote_plus ( eeveve [ "name" ] )
except : pass
try : VeveVeeveve = int ( eeveve [ "mode" ] )
except : pass
try : eV = urllib . unquote_plus ( eeveve [ "iconimage" ] )
except : pass
try : eevVeVeVVevev = urllib . unquote_plus ( eeveve [ "fanart" ] )
except : pass
try : IIiiIIi1 = str ( eeveve [ "description" ] )
except : pass
if 59 - 59: eVeV . I1I11I1I1I % eevVVev
if VeveVeeveve == None or eeeveevVevev == None or len ( eeeveevVevev ) < 1 : eeveVeVeveve ( )
elif VeveVeeveve == 1 : VeeVev ( eVeveeveeveeVeveV , eeeveevVevev , eV , eevVeVeVVevev )
elif VeveVeeveve == 2 : eVIIiIi ( eVeveeveeveeVeveV , eeeveevVevev , eV , IIiiIIi1 )
elif VeveVeeveve == 3 : VVVeee ( eVeveeveeveeVeveV , eeeveevVevev , eV )
elif VeveVeeveve == 4 : Iiii1iI1i ( eVeveeveeveeVeveV , eeeveevVevev , eV )
elif VeveVeeveve == 5 : VeveeevV ( )
elif VeveVeeveve == 6 : eevevVeeveeeeee ( eeeveevVevev , eV )
elif VeveVeeveve == 7 : eee ( eeeveevVevev )
elif VeveVeeveve == 8 : eVV ( eVeveeveeveeVeveV )
elif VeveVeeveve == 9 : ii1I1 ( eVeveeveeveeVeveV , eeeveevVevev )
elif VeveVeeveve == 10 : I1i ( eVeveeveeveeVeveV , eeeveevVevev , eV , eevVeVeVVevev )
elif VeveVeeveve == 11 : i1i1ii ( eeeveevVevev )
elif VeveVeeveve == 12 : IiIIiiI11III ( )
elif VeveVeeveve == 13 : VVeeVVVVVVeee ( )
elif VeveVeeveve == 15 : SCRAPEMOVIE ( eVeveeveeveeVeveV , eeeveevVevev , eV )
elif VeveVeeveve == 16 : VVeVeeVeVVVee ( eVeveeveeveeVeveV , eeeveevVevev , eV )
elif VeveVeeveve == 17 : eeveevVevVeveveVVe ( eVeveeveeveeVeveV , eeeveevVevev )
elif VeveVeeveve == 18 : eev ( eVeveeveeveeVeveV , eeeveevVevev , eV , eevVeVeVVevev )
elif VeveVeeveve == 19 : VeVVVVV ( eVeveeveeveeVeveV , eeeveevVevev , eV , eevVeVeVVevev )
if 39 - 39: eVVee
elif VeveVeeveve == 20 : I1iIIIi1 ( eVeveeveeveeVeveV , eeeveevVevev , eV , eevVeVeVVevev )
elif VeveVeeveve == 21 : iIIii ( eVeveeveeveeVeveV , eeeveevVevev , eV )
elif VeveVeeveve == 22 : Veeeeee ( eeeveevVevev , eevVeVeVVevev )
elif VeveVeeveve == 23 : DOIPLAYER ( eVeveeveeveeVeveV , eeeveevVevev , eV , eevVeVeVVevev )
elif VeveVeeveve == 24 : I11i1ii1 ( eVeveeveeveeVeveV , eeeveevVevev , eV , eevVeVeVVevev )
elif VeveVeeveve == 25 : I111 ( )
if 97 - 97: I1I11I1I1I - eeveveeeev / iIiI1I11 . i11iIiiIii % I1IiIiiIII * I1IiIiiIII
elif VeveVeeveve == 26 : iI11 ( eVeveeveeveeVeveV , eeeveevVevev , eV , eevVeVeVVevev )
elif VeveVeeveve == 27 : iiiIi ( eVeveeveeveeVeveV , eeeveevVevev , eV , eevVeVeVVevev )
elif VeveVeeveve == 28 : eVVeev ( eVeveeveeveeVeveV , eeeveevVevev , eV , eevVeVeVVevev )
elif VeveVeeveve == 29 : I1111IIi ( eVeveeveeveeVeveV , eeeveevVevev , eV , eevVeVeVVevev )
elif VeveVeeveve == 30 : i1IIIiiII1 ( eVeveeveeveeVeveV , eeeveevVevev , eV , eevVeVeVVevev )
elif VeveVeeveve == 31 : I1 ( eVeveeveeveeVeveV , eeeveevVevev , eV , eevVeVeVVevev )
elif VeveVeeveve == 32 : IIi1I11I1II ( eVeveeveeveeVeveV , eeeveevVevev , eV , eevVeVeVVevev )
elif VeveVeeveve == 33 : IIi ( eeeveevVevev )
elif VeveVeeveve == 34 : IIiII111iiI1I ( eVeveeveeveeVeveV , eeeveevVevev , eV , eevVeVeVVevev )
elif VeveVeeveve == 35 : I1Ii ( eVeveeveeveeVeveV , eeeveevVevev , eV , eevVeVeVVevev )
if 1 - 1: VeeveeVeveeeveV % eeVeeevV
if 65 - 65: VeeveeVeveeeveV + eevev / I1I11I1I1I
if 83 - 83: VeeveVeveee . i111I1 - I1i1iI1i
if 65 - 65: iIii1I11I1II1 / eeVeeevV . eVeV - eevVVev
if 72 - 72: iIii1I11I1II1 / eVeV % i111I1 % I1I11I1I1I - VeeVevVV % I1I11I1I1I
if 100 - 100: I1i1iI1i + i11iIiiIii
if 71 - 71: VeeVevVV / VeeveVeveee / iiIiIIi % I1I11I1I1I
xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3
