import xbmc , xbmcaddon , xbmcgui , xbmcplugin , requests , urllib , urllib2 , json , os , re , sys , datetime , urlresolver , random , liveresolver , base64 , pyxbmct
from resources . lib . common_addon import Addon
from HTMLParser import HTMLParser
from metahandler import metahandlers
import nanscrapers
if 64 - 64: i11iIiiIii
VVeve = 'plugin.video.Evolve'
VeevVee = Addon ( VVeve , sys . argv )
VevVevVVevVevVev = xbmcaddon . Addon ( id = VVeve )
iiiii = xbmcaddon . Addon ( ) . getAddonInfo
eeeevVV = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + VVeve , 'fanart.png' ) )
II1 = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + VVeve , 'fanart.png' ) )
Veveveeeeeevev = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + VVeve , 'icon.png' ) )
I1IiiI = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + VVeve + '/resources/art' , 'next.png' ) )
IIi1IiiiI1Ii = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + VVeve + '/resources' , 'rd.txt' ) )
I11i11Ii = 'http://matsbuilds.uk/anewEvolvemenu/EvolveMainMenu.xml'
eVeveveVe = 'http://matsbuilds.uk/Evolvemasterlist/'
VVVeev = VevVevVVevVevVev . getSetting ( 'password' )
Veeeeveveve = VevVevVVevVevVev . getSetting ( 'enable_meta' )
IiIi11iIIi1Ii = 'http://matsbuilds.uk/anewEvolvemenu/info.txt'
VeevV = xbmc . translatePath ( 'special://home/userdata/addon_data/' + VVeve )
IiI = xbmc . translatePath ( os . path . join ( 'special://home/userdata/Database' , 'Evolve.db' ) )
eeVe = open ( IiI , 'a' )
eeVe . close ( )
if 91 - 91: Ii1I . VeVV + VeVVeveeVVeeevV + eeveveveveVeVeVeve * i1I1ii1II1iII % eeeVeveeeveVVVV
def VeveV ( ) :
 if not os . path . exists ( VeevV ) :
  os . mkdir ( VeevV )
 eeveVev ( IiIi11iIIi1Ii , 'GlobalCompare' )
 eeevev ( '[B][COLOR royalblue]F[/COLOR][COLOR white]avs[/COLOR][/B]' , 'url' , 22 , 'http://i.imgur.com/Fi18HDV.png' , II1 )
 eeevev ( '[B][COLOR red]M[/COLOR][COLOR white]ovies[/COLOR][/B]' , 'http://matsbuilds.uk/EvolveMenus/Movies/Mainmenu.xml' , 26 , 'http://i.imgur.com/x6BAZUe.png' , II1 )
 eeevev ( '[B][COLOR blue]TV[/COLOR]  [COLOR blue]S[/COLOR][COLOR white]hows[/COLOR][/B]' , 'http://matsbuilds.uk/EvolveMenus/TvShows/Mainmenu.xml' , 27 , 'http://i.imgur.com/SLdxQL6.png' , II1 )
 eevev = VeeveVeveee ( I11i11Ii )
 eeveVeVeveve = re . compile ( '<item>(.+?)</item>' ) . findall ( eevev )
 for i1 in eeveVeVeveve :
  eVVeeevevVevV = re . compile ( '<title>(.+?)</title>.+?folder>(.+?)</folder>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>' ) . findall ( i1 )
  for i1111 , i11 , I11 , eeeevVV in eVVeeevevVevV :
   eeevev ( i1111 , i11 , 1 , I11 , eeeevVV )
 eeevev ( '[B][COLOR chartreuse]S[/COLOR][COLOR white]earch[/COLOR][/B] [B][COLOR chartreuse]E[/COLOR][COLOR white]volve[/COLOR][/B]' , 'url' , 5 , 'http://i.imgur.com/oHqT3bb.png' , II1 )
 xbmc . executebuiltin ( 'Container.SetViewMode(500)' )
 if 98 - 98: I1111 * eeveevVeeveeeeev / I1I1i1 * eVev / IIIi1i1I
def VVeVeeevevee ( name , url , iconimage , fanart ) :
 eeevev ( '[B][COLOR red]MOVIE SEARCH[/COLOR][/B]' , 'http://matsbuilds.uk/EvolveMenus/Movies/Search/Search.txt' , 5 , 'http://i.imgur.com/Qlc3Efe.png' , II1 )
 eeevev ( '[B][COLOR yellow]UK CINEMA RELEASE DATES[/COLOR][/B]' , 'http://www.empireonline.com/movies/features/upcoming-movies/' , 34 , 'http://i.imgur.com/1ImmOS4.png' , II1 )
 iiI11 = VVeeV ( name )
 VevVevVVevVevVev . setSetting ( 'movie' , iiI11 )
 eevev = VeeveVeveee ( url )
 eeveVeVeveve = re . compile ( '<item>(.+?)</item>' ) . findall ( eevev )
 for i1 in eeveVeVeveve :
  eVVeeevevVevV = re . compile ( '<title>(.+?)</title>.+?folder>(.+?)</folder>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>' ) . findall ( i1 )
  for name , url , iconimage , fanart in eVVeeevevVevV :
   VVeVeveve ( name , url , iconimage , fanart , i1 )
   if 9 - 9: I1iiiiI1iII - eVeev / i1Ii % I111I11
def VevVevevVee ( name , url , iconimage , fanarts ) :
 eeevev ( '[B][COLOR blue]TV SEARCH[/COLOR][/B]' , 'http://matsbuilds.uk/EvolveMenus/TvShows/Search/Search.txt' , 33 , 'http://i.imgur.com/gLWo9QO.png' , fanarts )
 eeevev ( '[B][COLOR yellow]TV SCHEDULE[/COLOR][/B]' , 'http://www.tvwise.co.uk/uk-premiere-dates/' , 32 , 'http://i.imgur.com/Pq53Nxh.png' , fanarts )
 eeevev ( '[B][COLOR blue]Latest[/COLOR] [COLOR white]Episodes[/COLOR][/B]' , 'http://www.watchepisodes4.com' , 28 , 'http://i.imgur.com/gLWo9QO.png' , fanarts )
 eeevev ( '[B][COLOR blue]Popular[/COLOR] [COLOR white]Shows[/COLOR][/B]' , 'http://www.watchepisodes4.com/home/popular-series' , 29 , 'http://i.imgur.com/SHXfj1a.png' , fanarts )
 eeevev ( '[B][COLOR blue]New[/COLOR] [COLOR white]Shows[/COLOR][/B]' , 'http://www.watchepisodes4.com/home/new-series' , 30 , 'http://i.imgur.com/roVYGM8.png' , fanarts )
 iiI11 = VVeeV ( name )
 VevVevVVevVevVev . setSetting ( 'tv' , iiI11 )
 eevev = VeeveVeveee ( url )
 eeveVeVeveve = re . compile ( '<item>(.+?)</item>' ) . findall ( eevev )
 for i1 in eeveVeVeveve :
  eVVeeevevVevV = re . compile ( '<title>(.+?)</title>.+?folder>(.+?)</folder>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>' ) . findall ( i1 )
  for name , url , iconimage , eeeevVV in eVVeeevevVevV :
   VVeVeveve ( name , url , iconimage , eeeevVV , i1 )
   if 64 - 64: ee - Ii1 / iIiI1I11 % i111I1 % eVev
def eVeV ( name , url , iconimage , fanart ) :
 iiI11 = VVeeV ( name )
 VevVevVVevVevVev . setSetting ( 'tv' , iiI11 )
 eevev = VeeveVeveee ( url )
 eVe ( eevev )
 if '<message>' in eevev :
  IiIi11iIIi1Ii = re . compile ( '<message>(.+?)</message>' ) . findall ( eevev ) [ 0 ]
  eeveVev ( IiIi11iIIi1Ii , iiI11 )
 if '<intro>' in eevev :
  eVeVeV = re . compile ( '<intro>(.+?)</intro>' ) . findall ( eevev ) [ 0 ]
  ii1I ( eVeVeV )
 if 'XXX>yes</XXX' in eevev : VeeVev ( eevev )
 eeveVeVeveve = re . compile ( '<item>(.+?)</item>' ) . findall ( eevev )
 for i1 in eeveVeVeveve :
  VVeVeveve ( name , url , iconimage , fanart , i1 )
  if 35 - 35: eVeev % iIiI1I11 % i11iIiiIii / VeVVeveeVVeeevV
def VVeVeveve ( name , url , iconimage , fanart , item ) :
 try :
  if '<sportsdevil>' in item : Ii11iI1i ( name , url , iconimage , fanart , item )
  elif '<iplayer>' in item : Vee ( name , url , iconimage , fanart , item )
  elif '<folder>' in item : VeveevVe ( name , url , iconimage , fanart , item )
  elif '<iptv>' in item : VeevevVVVVV ( name , url , iconimage , fanart , item )
  elif '<image>' in item : VevV ( name , url , iconimage , fanart , item )
  elif '<text>' in item : VeveveevVV ( name , url , iconimage , fanart , item )
  elif '<scraper>' in item : I11i1 ( name , url , iconimage , fanart , item )
  elif '<lbscraper>' in item : iIi1ii1I1 ( name , url , iconimage , fanart , item )
  elif '<redirect>' in item : eev ( name , url , iconimage , fanart , item )
  elif '<oktitle>' in item : I11II1i ( name , url , iconimage , fanart , item )
  elif '<nan>' in item : IIIII ( name , url , iconimage , fanart , item )
  else : eeeeeeVevee ( name , url , iconimage , fanart , item )
 except : pass
 if 49 - 49: eVev * VeVV / eeveveveveVeVeVeve / i11iIiiIii / eVev
def Vee ( name , url , iconimage , fanart , item ) :
 url = re . compile ( '<iplayer>(.+?)</iplayer>' ) . findall ( item ) [ 0 ]
 name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
 url = 'plugin://plugin.video.iplayerwww/?url=%s&mode=202&name=%s&iconimage=%s&description=&subtitles_url=&logged_in=False' % ( url , name , iconimage )
 I1i1I1II ( name , url , 16 , iconimage , fanart )
 if 45 - 45: iIiI1I11 . I1I1i1
def IIIII ( name , url , iconimage , fanart , item ) :
 name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 eV = re . compile ( '<meta>(.+?)</meta>' ) . findall ( item ) [ 0 ]
 iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
 ii1i1I1i = re . compile ( '<nan>(.+?)</nan>' ) . findall ( item ) [ 0 ]
 eeveveVVev = re . compile ( '<imdb>(.+?)</imdb>' ) . findall ( item ) [ 0 ]
 if ii1i1I1i == 'movie' :
  eeveveVVev = eeveveVVev + '<>movie'
 elif ii1i1I1i == 'tvshow' :
  eVee = re . compile ( '<showname>(.+?)</showname>' ) . findall ( item ) [ 0 ]
  iIii11I = re . compile ( '<season>(.+?)</season>' ) . findall ( item ) [ 0 ]
  VVVevVVVevevee = re . compile ( '<episode>(.+?)</episode>' ) . findall ( item ) [ 0 ]
  Iii111II = re . compile ( '<showyear>(.+?)</showyear>' ) . findall ( item ) [ 0 ]
  iiii11I = re . compile ( '<episodeyear>(.+?)</episodeyear>' ) . findall ( item ) [ 0 ]
  eeveveVVev = eeveveVVev + '<>' + eVee + '<>' + iIii11I + '<>' + VVVevVVVevevee + '<>' + Iii111II + '<>' + iiii11I
  ii1i1I1i = "tvep"
 VeeevVVeveVV ( name , eeveveVVev , 19 , iconimage , 1 , ii1i1I1i , isFolder = True )
 if 50 - 50: eeeVeveeeveVVVV
def Ii1i11IIii1I ( name , imdb , iconimage , fanart ) :
 IIi1IiiiI1Ii = ''
 VVVeVevVeve = name
 iiI11 = VVeeV ( name )
 VevVevVVevVevVev . setSetting ( 'tv' , iiI11 )
 if 'movie' in imdb :
  imdb = imdb . split ( '<>' ) [ 0 ]
  VeveevVee = [ ]
  Vevev = [ ]
  iI1Ii11iII1 = name . partition ( '(' )
  VeevVevVeveeVevV = iI1Ii11iII1 [ 0 ]
  VeevVevVeveeVevV = VVeeV ( VeevVevVeveeVevV )
  IIIIii = iI1Ii11iII1 [ 2 ] . partition ( ')' ) [ 0 ]
  Veveev = nanscrapers . scrape_movie ( VeevVevVeveeVevV , IIIIii , imdb , timeout = 800 )
 else :
  eVee = imdb . split ( '<>' ) [ 1 ]
  VVevevVe = imdb . split ( '<>' ) [ 0 ]
  iIii11I = imdb . split ( '<>' ) [ 2 ]
  VVVevVVVevevee = imdb . split ( '<>' ) [ 3 ]
  Iii111II = imdb . split ( '<>' ) [ 4 ]
  iiii11I = imdb . split ( '<>' ) [ 5 ]
  Veveev = nanscrapers . scrape_episode ( eVee , Iii111II , iiii11I , iIii11I , VVVevVVVevevee , VVevevVe , None )
 VevVVVevVVeVevV = 1
 for VevevVeeveveveeVev in list ( Veveev ( ) ) :
  for VeVevVevev in VevevVeeveveveeVev :
   if urlresolver . HostedMediaFile ( VeVevVevev [ 'url' ] ) . valid_url ( ) :
    IIi1IiiiI1Ii = IIiII ( VeVevVevev [ 'url' ] )
    name = "Link " + str ( VevVVVevVVeVevV ) + ' | ' + VeVevVevev [ 'source' ] + IIi1IiiiI1Ii
    VevVVVevVVeVevV = VevVVVevVVeVevV + 1
    eeveeVeeeeveveveVV ( name , VeVevVevev [ 'url' ] , 2 , iconimage , fanart , description = VevVevVVevVevVev . getSetting ( 'tv' ) )
    if 59 - 59: i1I1ii1II1iII + VeVVeveeVVeeevV * I1I1i1 + eeveveveveVeVeVeve
def I11i1 ( name , url , iconimage , fanart , item ) :
 name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 url = re . compile ( '<scraper>(.+?)</scraper>' ) . findall ( item ) [ 0 ]
 fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
 eeevev ( name , url , 18 , iconimage , fanart )
 if 58 - 58: i1I1ii1II1iII * eVeev * IIIi1i1I / eVeev
def eVeveevVVVV ( name , url , iconimage , fanart ) :
 VevVevVeVVev = url
 if VevVevVeVVev == 'latestmovies' :
  iiiI1I11i1 = 15
  IIi1i11111 = MOVIESINDEXER ( )
  eeVVevevVevevee = re . compile ( '<item>(.+?)</item>' ) . findall ( IIi1i11111 )
  for i1 in eeVVevevVevevee :
   eVVeeevevVevV = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>' ) . findall ( i1 )
   I1ii11iI = len ( eeVVevevVevevee )
   for name , url , iconimage , fanart in eVVeeevevVevV :
    if '<meta>' in i1 :
     IIi1i = re . compile ( '<meta>(.+?)</meta>' ) . findall ( i1 ) [ 0 ]
     VeeevVVeveVV ( name , url , iiiI1I11i1 , iconimage , I1ii11iI , IIi1i , isFolder = False )
    else : eeveeVeeeeveveveVV ( name , url , 15 , iconimage , fanart )
    if 46 - 46: iIiI1I11 % i1Ii + eeveevVeeveeeeev . I1I1i1 . eeveevVeeveeeeev
    if 96 - 96: I1111
def Ii1I1IIii1II ( name , url , iconimage , fanarts ) :
 eevev = Vev ( 'http://www.watchepisodes4.com' )
 ii1ii1ii = re . compile ( '<a title=".+?" .+? style="background-image: url(.+?)"></a>.+?<div class="hb-right">.+?<a title=".+?" href="(.+?)" class="episode">(.+?)</a>' , re . DOTALL ) . findall ( eevev )
 for iconimage , url , name in ii1ii1ii :
  iconimage = iconimage . replace ( "('" , "" ) . replace ( "')" , "" )
  name = name . replace ( "&#39;" , "'" )
  name = name . split ( '  ' ) [ 0 ]
  eeevev ( name , url , 24 , iconimage , iconimage )
  if 91 - 91: Ii1
def iiIii ( name , url , iconimage , fanart ) :
 eevev = Vev ( url )
 ii1ii1ii = re . compile ( '<div class="cb-first">.+?<a href="(.+?)" class="c-image"><img alt=".+?" title="(.+?)" src="(.+?)"></a>' , re . DOTALL ) . findall ( eevev )
 for url , name , iconimage in ii1ii1ii :
  name = name . replace ( "&#39;" , "'" )
  eeevev ( name , url , 31 , iconimage , iconimage )
  if 79 - 79: VeVVeveeVVeeevV / Ii1I
def VVevVeVeveevev ( name , url , iconimage , fanart ) :
 eevev = Vev ( url )
 ii1ii1ii = re . compile ( '<div class="cb-first">.+?<a href="(.+?)" class="c-image"><img alt=".+?" title="(.+?)" src="(.+?)"></a>' , re . DOTALL ) . findall ( eevev )
 for url , name , iconimage in ii1ii1ii :
  name = name . replace ( "&#39;" , "'" )
  eeevev ( name , url , 31 , iconimage , iconimage )
  if 53 - 53: Ii1I * eeveevVeeveeeeev + eVeev
def Ii ( name , url , iconimage , fanart ) :
 eevev = eVVeev ( url )
 eeevevVeveveV = re . compile ( '<div class="std-cts">.+?<div class="sdt-content tnContent">.+?<h2>(.+?)</h2>' , re . DOTALL ) . findall ( eevev ) [ 0 ] . replace ( ' Episodes' , '' )
 eeveVeVeveve = re . compile ( '<a title=".+?" href="(.+?)">.+?<div class="season">(.+?) </div>.+?<div class="episode">(.+?)</div>.+?<div class="e-name">(.+?)</div>' , re . DOTALL ) . findall ( eevev )
 for url , iIii11I , VVVevVVVevevee , iIiIIIi in eeveVeVeveve :
  iIiIIIi = iIiIIIi . replace ( "&#39;" , "'" ) . replace ( '&amp;' , ' & ' )
  if '</div>' in name : name = 'TBA'
  eeevev ( '%s ' % eeevevVeveveV + '(%s ' % iIii11I + '%s)' % VVVevVVVevevee , url , 24 , iconimage , iconimage )
  if 93 - 93: ee
def i1IIIiiII1 ( name , url , iconimage , fanart ) :
 VVVeVevVeve = name
 eevev = eVVeev ( url )
 VVVVeVeeevVevVev = re . compile ( '<a target="_blank" href=".+?" data-episodeid=".+?" data-linkid=".+?" data-hostname=".+?" class="watch-button" data-actuallink="(.+?)">Watch Now!</a>' ) . findall ( eevev )
 VevVVVevVVeVevV = 1
 VeveevVee = [ ]
 Vevev = [ ]
 for VVVeeveveeeveV in VVVVeVeeevVevVev :
  IIi1IiiiI1Ii = IIiII ( VVVeeveveeeveV )
  if 'http' in VVVeeveveeeveV : IIiIi1iI = VVVeeveveeeveV . split ( '/' ) [ 2 ] . split ( '.' ) [ 0 ]
  else : IIiIi1iI = VVVeeveveeeveV
  name = "Link " + str ( VevVVVevVVeVevV ) + ' | ' + IIiIi1iI + IIi1IiiiI1Ii
  if IIiIi1iI != 'www' :
   eeveeVeeeeveveveVV ( IIiIi1iI , VVVeeveveeeveV , 2 , iconimage , fanart , description = '' )
   if 35 - 35: I111I11 % Ii1I - Ii1I
def IiIIIi1iIi ( name , url , iconimage , fanart ) :
 eevev = eVVeev ( url )
 ii1ii1ii = re . compile ( '<td height="20">(.+?)</td>.+?<td>(.+?)</td>.+?<td><a href=".+?">(.+?)</a></td>.+?<td><a href=".+?">(.+?)</a></td>.+?</tr>' , re . DOTALL ) . findall ( eevev )
 for eeVVeeeeee , name , II1I , Vevi1II1Iiii1I11 in ii1ii1ii :
  name = name . replace ( "&#8217;" , "'" ) . replace ( '&amp;' , ' & ' )
  eeevev ( '[COLOR yellow]%s[/COLOR] - ' % II1I + '[COLOR blue]%s[/COLOR] ' % name + '- [COLOR white]%s[/COLOR]' % eeVVeeeeee , url , 28 , iconimage , fanart )
  if 9 - 9: IIIi1i1I / I1111 - eeeVeveeeveVVVV / VeVVeveeVVeeevV / VeVV - eVev
def eeveveeeVevVe ( url ) :
 eevVevVVVevVee = ''
 iiIiI = xbmc . Keyboard ( eevVevVVVevVee , '[B][COLOR red]S[/COLOR][COLOR white]earch[/COLOR][/B] [B][COLOR red]E[/COLOR][COLOR white]volve[/COLOR][/B]' )
 iiIiI . doModal ( )
 if iiIiI . isConfirmed ( ) :
  eevVevVVVevVee = iiIiI . getText ( ) . replace ( ' ' , '+' ) . replace ( '+and+' , '+%26+' )
 if len ( eevVevVVVevVee ) > 1 :
  url = 'http://www.watchepisodes4.com/search/ajax_search?q=' + eevVevVVVevVee
  eevev = eVVeev ( url )
  eVVeeevevVevV = json . loads ( eevev )
  eVVeeevevVevV = eVVeeevevVevV [ 'series' ]
  for i1 in eVVeeevevVevV :
   i1111 = i1 [ 'value' ]
   I1 = i1 [ 'seo' ]
   url = 'http://www.watchepisodes4.com/' + I1
   I11 = 'http://www.watchepisodes4.com/movie_images/' + I1 + '.jpg'
   eeevev ( i1111 , url , 31 , I11 , eeeevVV )
  eevVevVVVevVee = eevVevVVVevVee [ : - 1 ]
  eevev = VeeveVeveee ( 'http://matsbuilds.uk/EvolveMenus/TvShows/Search/Search.txt' )
  VVVevevVevV = re . compile ( '<link>(.+?)</link>' ) . findall ( eevev )
  for url in VVVevevVevV :
   try :
    eevev = VeeveVeveee ( url )
    iii = re . compile ( '<item>(.+?)</item>' ) . findall ( eevev )
    for i1 in iii :
     eeveVeVeveve = re . compile ( '<title>(.+?)</title>' ) . findall ( i1 )
     for VVVeVevVeve in eeveVeVeveve :
      VVVeVevVeve = VVeeV ( VVVeVevVeve . upper ( ) )
      eevVevVVVevVee = eevVevVVVevVee . upper ( )
      if eevVevVVVevVee in VVVeVevVeve :
       VVeVeveve ( i1111 , url , I11 , eeeevVV , i1 )
   except : pass
   if 90 - 90: eVev % eeveveveveVeVeVeve / eeveevVeeveeeeev
   if 44 - 44: I1111 . eeveevVeeveeeeev / IIIi1i1I + I111I11
def eeve ( name , url , iconimage , fanart ) :
 eevev = eVVeev ( url )
 ii1ii1ii = re . compile ( '<h2 id=".+?">(.+?)</h2>.+?<p><span class="article__image article__image--undefined"><img src="(.+?)" alt=".+?"></span> </p>.+?<p><strong>(.+?)</strong>(.+?)<' , re . DOTALL ) . findall ( eevev )
 for VVVeVevVeve , iconimage , VevVVeVevevVVeve , II1I in ii1ii1ii :
  name = name . replace ( "&#8217;" , "'" ) . replace ( '&amp;' , ' & ' )
  eeevev ( '[COLOR yellow]%s [/COLOR] ' % VVVeVevVeve + '[COLOR red]%s[/COLOR]' % VevVVeVevevVVeve + '[COLOR white]%s[/COLOR]' % II1I , url , 35 , iconimage , fanart )
def I1111IIIIIi ( name , url , iconimage , fanart ) :
 eevev = VeeveVeveee ( 'http://matsbuilds.uk/EvolveMenus/Movies/EvolveLatest/mainmenu.xml' )
 ii1ii1ii = re . compile ( '<item>(.+?)</item>' ) . findall ( eevev )
 for i1 in ii1ii1ii :
  VVeVeveve ( name , url , iconimage , fanart , i1 )
  if 22 - 22: eeveveveveVeVeVeve + Ii1I . VeVV * ee % i11iIiiIii * eeeVeveeeveVVVV
  if 77 - 77: I1111
def iIi1ii1I1 ( name , url , iconimage , fanart , item ) :
 name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 url = re . compile ( '<lbscraper>(.+?)</lbscraper>' ) . findall ( item ) [ 0 ]
 fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
 eeevev ( name , url , 10 , iconimage , fanart )
 if 17 - 17: ee % eeveevVeeveeeeev . eVeev + eeveevVeeveeeeev / i1I1ii1II1iII
def eeevVevVevev ( name , url , iconimage , fanart ) :
 Veveev = iI111i ( name , url , iconimage )
 eeveVeVeveve = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( Veveev )
 for i1 in eeveVeVeveve :
  VVeVeveve ( name , url , iconimage , fanart , i1 )
  if 26 - 26: IIIi1i1I * ee . i1I1ii1II1iII * I111I11
def iI111i ( name , url , iconimage ) :
 VevVevVeVVev = url
 II1iiiIi1 = ''
 if url == 'mamahd' :
  eevev = Vev ( "http://mamahd.com" ) . replace ( '\n' , '' ) . replace ( '\t' , '' )
  i1I1ii11i1Iii = re . compile ( '<a href="(.+?)">.+?<img src="(.+?)"></div>.+?<div class="home cell">.+?<span>(.+?)</span>.+?<span>(.+?)</span>.+?</a>' ) . findall ( eevev )
  for url , iconimage , I1IiiiiI , eevV in i1I1ii11i1Iii :
   II1iiiIi1 = II1iiiIi1 + '<item>\n<title>%s vs %s</title>\n<sportsdevil>%s</sportsdevil>\n<thumbnail>%s</thumbnail>\n<fanart>fanart</fanart>\n</item>\n\n' % ( I1IiiiiI , eevV , url , iconimage )
  return II1iiiIi1
  if 2 - 2: VeVV / I1iiiiI1iII + eeveevVeeveeeeev / eVeev
 elif url == 'cricfree' :
  eevev = Vev ( "http://cricfree.sc/football-live-stream" )
  II = re . compile ( '<td><span class="sport-icon(.+?)</tr>' , re . DOTALL ) . findall ( eevev )
  for VVVVeveeev in II :
   I11iiI1i1 = re . compile ( '<td>(.+?)<br(.+?)</td>' ) . findall ( VVVVeveeev )
   for I1i1Iiiii , II1I in I11iiI1i1 :
    I1i1Iiiii = '[COLOR red]' + I1i1Iiiii + '[/COLOR]'
    II1I = II1I . replace ( '>' , '' )
   Vevi1II1Iiii1I11 = re . compile ( '<td class="matchtime" style="color:#545454;font-weight:bold;font-size: 9px">(.+?)</td>' ) . findall ( VVVVeveeev ) [ 0 ]
   Vevi1II1Iiii1I11 = '[COLOR white](' + Vevi1II1Iiii1I11 + ')[/COLOR]'
   VVeeveVeveveeVevev = re . compile ( '<a style="text-decoration:none !important;color:#545454;" href="(.+?)" target="_blank">(.+?)</a></td>' ) . findall ( VVVVeveeev )
   for url , eVVevVeveveVevVee in VVeeveVeveveeVevev :
    url = url
    eVVevVeveveVevVee = eVVevVeveveVevVee
   II1iiiIi1 = II1iiiIi1 + '\n<item>\n<title>%s</title>\n<sportsdevil>%s</sportsdevil>\n' % ( I1i1Iiiii + ' ' + Vevi1II1Iiii1I11 + ' - ' + eVVevVeveveVevVee , url )
   II1iiiIi1 = II1iiiIi1 + '<thumbnail>iconimage</thumbnail>\n<fanart>fanart</fanart>\n</item>\n'
  return II1iiiIi1
  if 67 - 67: eeveevVeeveeeeev - eVeev
 elif url == 'bigsports' :
  eevev = Vev ( "http://www.bigsports.me/cat/4/football-live-stream.html" )
  i1I1ii11i1Iii = re . compile ( '<td>.+?<td>(.+?)\-(.+?)\-(.+?)</td>.+?<td>(.+?)\:(.+?)</td>.+?<td>Football</td>.+?<td><strong>(.+?)</strong></td>.+?<a target=.+? href=(.+?) class=.+?' , re . DOTALL ) . findall ( eevev )
  for I1i1Iiiii , iI1i11iII111 , Iii1IIII11I , VVVeeevVV , eVeveev , name , url in i1I1ii11i1Iii :
   if not '</td>' in I1i1Iiiii :
    url = url . replace ( '"' , '' )
    II1I = I1i1Iiiii + ' ' + iI1i11iII111 + ' ' + Iii1IIII11I
    Vevi1II1Iiii1I11 = VVVeeevVV + ':' + eVeveev
    II1I = '[COLOR red]' + II1I + '[/COLOR]'
    Vevi1II1Iiii1I11 = '[COLOR white](' + Vevi1II1Iiii1I11 + ')[/COLOR]'
    II1iiiIi1 = II1iiiIi1 + '\n<item>\n<title>%s</title>\n<sportsdevil>%s</sportsdevil>\n' % ( II1I + ' ' + Vevi1II1Iiii1I11 + ' ' + name , url )
    II1iiiIi1 = II1iiiIi1 + '<thumbnail>iconimage</thumbnail>\n<fanart>fanart</fanart>\n</item>\n'
  return II1iiiIi1
  if 50 - 50: Ii1
def I11II1i ( name , url , iconimage , fanart , item ) :
 name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 Ii11iIi = re . compile ( '<oktitle>(.+?)</oktitle>' ) . findall ( item ) [ 0 ]
 VevevVevVeeeeveV = re . compile ( '<line1>(.+?)</line1>' ) . findall ( item ) [ 0 ]
 IIii11I1 = re . compile ( '<line2>(.+?)</line2>' ) . findall ( item ) [ 0 ]
 eVVevVevevVeevVeve = re . compile ( '<line3>(.+?)</line3>' ) . findall ( item ) [ 0 ]
 ii1 = '##' + Ii11iIi + '#' + VevevVevVeeeeveV + '#' + IIii11I1 + '#' + eVVevVevevVeevVeve + '##'
 iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
 I1i1I1II ( name , ii1 , 17 , iconimage , fanart )
 if 35 - 35: ee * I1iiiiI1iII / VeVV - eVev / VeVVeveeVVeeevV - iIiI1I11
def II1I1iiIII ( name , url ) :
 eVVeevVeveve = re . compile ( '##(.+?)##' ) . findall ( url ) [ 0 ] . split ( '#' )
 iIiIi11 = xbmcgui . Dialog ( )
 iIiIi11 . ok ( eVVeevVeveve [ 0 ] , eVVeevVeveve [ 1 ] , eVVeevVeveve [ 2 ] , eVVeevVeveve [ 3 ] )
 if 87 - 87: I1111 . eeeVeveeeveVVVV - i1I1ii1II1iII + Ii1I / I1111 / I1iiiiI1iII
def eev ( name , url , iconimage , fanart , item ) :
 url = re . compile ( '<redirect>(.+?)</redirect>' ) . findall ( item ) [ 0 ]
 eVeV ( 'name' , url , 'iconimage' , 'fanart' )
 if 25 - 25: eeeVeveeeveVVVV . eeeVeveeeveVVVV - I1I1i1 % I1I1i1 - i11iIiiIii / iIiI1I11
def VeveveevVV ( name , url , iconimage , fanart , item ) :
 name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 ii1 = re . compile ( '<text>(.+?)</text>' ) . findall ( item ) [ 0 ]
 iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
 I1i1I1II ( name , ii1 , 9 , iconimage , fanart )
 if 51 - 51: I1111 / I1I1i1 . eVeev * eVev + eeveevVeeveeeeev * Ii1
def VVVeVe ( name , url ) :
 Veveveev = eVVeev ( url )
 I11iII ( name , Veveveev )
 if 5 - 5: eeeVeveeeveVVVV
def VevV ( name , url , iconimage , fanart , item ) :
 iIiIi11iI = re . compile ( '<image>(.+?)</image>' ) . findall ( item )
 if len ( iIiIi11iI ) == 1 :
  name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  VeevVevevVevevev = re . compile ( '<image>(.+?)</image>' ) . findall ( item ) [ 0 ]
  fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
  I1i1I1II ( name , VeevVevevVevevev , 7 , iconimage , fanart )
 elif len ( iIiIi11iI ) > 1 :
  name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
  i11I1IiII1i1i = ''
  for VeevVevevVevevev in iIiIi11iI : i11I1IiII1i1i = i11I1IiII1i1i + '<image>' + VeevVevevVevevev + '</image>'
  eeI1111i = VeevV
  name = VVeeV ( name )
  iIIii = os . path . join ( os . path . join ( eeI1111i , '' ) , name + '.txt' )
  if not os . path . exists ( iIIii ) : file ( iIIii , 'w' ) . close ( )
  eevevVevV = open ( iIIii , "w" )
  eevevVevV . write ( i11I1IiII1i1i )
  eevevVevV . close ( )
  I1i1I1II ( name , 'image' , 8 , iconimage , fanart )
  if 20 - 20: eeveveveveVeVeVeve - i111I1
def VeevevVVVVV ( name , url , iconimage , fanart , item ) :
 name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 url = re . compile ( '<iptv>(.+?)</iptv>' ) . findall ( item ) [ 0 ]
 fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
 eeevev ( name , url , 6 , iconimage , fanart )
 if 30 - 30: i1Ii / eeeVeveeeveVVVV
def Iii1I1111ii ( url , iconimage ) :
 eevev = eVVeev ( url )
 eeVeVevev = re . compile ( '^#.+?:-?[0-9]*(.*?),(.*?)\n(.*?)$' , re . I + re . M + re . U + re . S ) . findall ( eevev )
 Ii1IIiI1i = [ ]
 for eevVevevVeev , i1111 , url in eeVeVevev :
  IiII111i1i11 = { "params" : eevVevevVeev , "name" : i1111 , "url" : url }
  Ii1IIiI1i . append ( IiII111i1i11 )
 list = [ ]
 for eeVVeeeeee in Ii1IIiI1i :
  IiII111i1i11 = { "name" : eeVVeeeeee [ "name" ] , "url" : eeVVeeeeee [ "url" ] }
  eeVeVevev = re . compile ( ' (.+?)="(.+?)"' , re . I + re . M + re . U + re . S ) . findall ( eeVVeeeeee [ "params" ] )
  for i111iIi1i1II1 , eeeV in eeVeVevev :
   IiII111i1i11 [ i111iIi1i1II1 . strip ( ) . lower ( ) . replace ( '-' , '_' ) ] = eeeV . strip ( )
  list . append ( IiII111i1i11 )
 for eeVVeeeeee in list :
  if '.ts' in eeVVeeeeee [ "url" ] : I1i1I1II ( eeVVeeeeee [ "name" ] , eeVVeeeeee [ "url" ] , 2 , iconimage , eeeevVV )
  else : eeveeVeeeeveveveVV ( eeVVeeeeee [ "name" ] , eeVVeeeeee [ "url" ] , 2 , iconimage , eeeevVV )
  if 26 - 26: I111I11 % IIIi1i1I
def eeeeeeVevee ( name , url , iconimage , fanart , item ) :
 IIi1IiiiI1Ii = ''
 eevevVeeveeeeee = re . compile ( '<link>(.+?)</link>' ) . findall ( item )
 eVVeeevevVevV = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>' ) . findall ( item )
 for name , VeveVev , iconimage , fanart in eVVeeevevVevV :
  if 'youtube.com/playlist?' in VeveVev :
   eevVevVVVevVee = VeveVev . split ( 'list=' ) [ 1 ]
   eeevev ( name , VeveVev , iII11 , iconimage , fanart , description = eevVevVVVevVee )
 if len ( eevevVeeveeeeee ) == 1 :
  eVVeeevevVevV = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>' ) . findall ( item )
  for name , url , iconimage , fanart in eVVeeevevVevV :
   try :
    IIi1IiiiI1Ii = IIiII ( url )
    iiIiii1IIIII = url . split ( '/' ) [ 2 ] . replace ( 'www.' , '' )
    if 'SportsDevil' in url : iiIiii1IIIII = ''
   except : pass
   if '.ts' in url : eeveeVeeeeveveveVV ( name , url , 16 , iconimage , fanart , description = '' )
   if '<meta>' in item :
    IIi1i = re . compile ( '<meta>(.+?)</meta>' ) . findall ( item ) [ 0 ]
    VeeevVVeveVV ( name + IIi1IiiiI1Ii , url , 2 , iconimage , 10 , IIi1i , isFolder = False )
   else :
    eeveeVeeeeveveveVV ( name + IIi1IiiiI1Ii , url , 2 , iconimage , fanart )
 elif len ( eevevVeeveeeeee ) > 1 :
  name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
  if '.ts' in url : eeveeVeeeeveveveVV ( name , url , 16 , iconimage , fanart , description = '' )
  if '<meta>' in item :
   IIi1i = re . compile ( '<meta>(.+?)</meta>' ) . findall ( item ) [ 0 ]
   VeeevVVeveVV ( name , url , 3 , iconimage , len ( eevevVeeveeeeee ) , IIi1i , isFolder = True )
  else :
   eeevev ( name , url , 3 , iconimage , fanart )
   if 67 - 67: I111I11 / Ii1
   if 9 - 9: Ii1I % Ii1I - eVev
def Ii11iI1i ( name , url , iconimage , fanart , item ) :
 eevevVeeveeeeee = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( item )
 VeV = re . compile ( '<link>(.+?)</link>' ) . findall ( item )
 if len ( eevevVeeveeeeee ) + len ( VeV ) == 1 :
  name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  url = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( item ) [ 0 ]
  url = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' + url
  I1i1I1II ( name , url , 16 , iconimage , fanart )
 elif len ( eevevVeeveeeeee ) + len ( VeV ) > 1 :
  name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  eeevev ( name , url , 3 , iconimage , fanart )
  if 12 - 12: Ii1I - eVev
def VeeVev ( link ) :
 if VVVeev == '' :
  iIiIi11 = xbmcgui . Dialog ( )
  eVeVevevVev = iIiIi11 . yesno ( 'Adult Content' , 'You have found the goodies ;)' , '' , 'Please set a password to prevent accidental access' , 'Cancel' , 'OK' )
  if eVeVevevVev == 1 :
   VV = xbmc . Keyboard ( '' , 'Set Password' )
   VV . doModal ( )
   if ( VV . isConfirmed ( ) ) :
    Ii1iI111II1I1 = VV . getText ( )
    VevVevVVevVevVev . setSetting ( 'password' , Ii1iI111II1I1 )
  else : quit ( )
 elif VVVeev <> '' :
  iIiIi11 = xbmcgui . Dialog ( )
  eVeVevevVev = iIiIi11 . yesno ( 'Adult Content' , 'Please enter the password you set' , 'to continue' , 'You dirty git!' , 'Cancel' , 'OK' )
  if eVeVevevVev == 1 :
   VV = xbmc . Keyboard ( '' , 'Enter Password' )
   VV . doModal ( )
   if ( VV . isConfirmed ( ) ) :
    Ii1iI111II1I1 = VV . getText ( )
   if Ii1iI111II1I1 <> VVVeev :
    quit ( )
  else : quit ( )
  if 91 - 91: eVeev % eVeev - eeeVeveeeveVVVV
def I1iiii1I ( name , url , iconimage ) :
 VVeev = ''
 iiI11 = VVeeV ( name )
 VevVevVVevVevVev . setSetting ( 'tv' , iiI11 )
 eevev = VeeveVeveee ( url )
 eVeveveeeeVeve = re . compile ( '<title>.*?' + re . escape ( name ) + '.*?</title>(.+?)</item>' , re . DOTALL ) . findall ( eevev ) [ 0 ]
 iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( eVeveveeeeVeve ) [ 0 ]
 eevevVeeveeeeee = [ ]
 if '<link>' in eVeveveeeeVeve :
  eeeve = re . compile ( '<link>(.+?)</link>' ) . findall ( eVeveveeeeVeve )
  for eeveVeveeeVee in eeeve :
   eevevVeeveeeeee . append ( eeveVeveeeVee )
 if '<sportsdevil>' in eVeveveeeeVeve :
  I1III1111iIi = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( eVeveveeeeVeve )
  for I1i111I in I1III1111iIi :
   I1i111I = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' + I1i111I
   eevevVeeveeeeee . append ( I1i111I )
 VevVVVevVVeVevV = 1
 for eevev in eevevVeeveeeeee :
  if '(' in eevev :
   eevev = eevev . split ( '(' )
   VVeev = eevev [ 1 ] . replace ( ')' , '' )
   eevev = eevev [ 0 ]
  IIi1IiiiI1Ii = IIiII ( eevev )
  iiIiii1IIIII = eevev . split ( '/' ) [ 2 ] . replace ( 'www.' , '' )
  if VVeev <> '' : name = "Link " + str ( VevVVVevVVeVevV ) + ' | ' + VVeev + IIi1IiiiI1Ii
  else : name = "Link " + str ( VevVVVevVVeVevV ) + ' | ' + iiIiii1IIIII + IIi1IiiiI1Ii
  VevVVVevVVeVevV = VevVVVevVVeVevV + 1
  VeeevVVeveVV ( name , eevev , 2 , iconimage , 10 , '' , isFolder = False , description = VevVevVVevVevVev . getSetting ( 'tv' ) )
  if 97 - 97: eeveveveveVeVeVeve . I1iiiiI1iII / ee * Ii1I
def VeveevVe ( name , url , iconimage , fanart , item ) :
 eVVeeevevVevV = re . compile ( '<title>(.+?)</title>.+?folder>(.+?)</folder>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>' ) . findall ( item )
 for name , url , iconimage , fanart in eVVeeevevVevV :
  if 'youtube.com/channel/' in url :
   eevVevVVVevVee = url . split ( 'channel/' ) [ 1 ]
   eeevev ( name , url , iII11 , iconimage , fanart , description = eevVevVVVevVee )
  elif 'youtube.com/user/' in url :
   eevVevVVVevVee = url . split ( 'user/' ) [ 1 ]
   eeevev ( name , url , iII11 , iconimage , fanart , description = eevVevVVVevVee )
  elif 'youtube.com/playlist?' in url :
   eevVevVVVevVee = url . split ( 'list=' ) [ 1 ]
   eeevev ( name , url , iII11 , iconimage , fanart , description = eevVevVVVevVee )
  elif 'plugin://' in url :
   eevVeve = HTMLParser ( )
   url = eevVeve . unescape ( url )
   eeevev ( name , url , iII11 , iconimage , fanart )
  else :
   eeevev ( name , url , 1 , iconimage , fanart )
   if 77 - 77: I1I1i1 - eeeVeveeeveVVVV * i11iIiiIii * i111I1 * VeVV
def eVeevVVVeVV ( ) :
 VV = xbmc . Keyboard ( '' , '[B][COLOR red]S[/COLOR][COLOR white]earch[/COLOR][/B] [B][COLOR red]E[/COLOR][COLOR white]volve[/COLOR][/B]' )
 VV . doModal ( )
 if ( VV . isConfirmed ( ) ) :
  eevVevVVVevVee = VV . getText ( )
  eevVevVVVevVee = eevVevVVVevVee . upper ( )
 else : quit ( )
 eevev = VeeveVeveee ( 'http://matsbuilds.uk/anewEvolvemenu/search.xml' )
 VVVevevVevV = re . compile ( '<link>(.+?)</link>' ) . findall ( eevev )
 for i11 in VVVevevVevV :
  try :
   eevev = VeeveVeveee ( i11 )
   iii = re . compile ( '<item>(.+?)</item>' ) . findall ( eevev )
   for i1 in iii :
    eeveVeVeveve = re . compile ( '<title>(.+?)</title>' ) . findall ( i1 )
    for VVVeVevVeve in eeveVeVeveve :
     VVVeVevVeve = VVVeVevVeve . upper ( )
     if eevVevVVVevVee in VVVeVevVeve :
      VVeVeveve ( i1111 , i11 , I11 , eeeevVV , i1 )
  except : pass
  if 10 - 10: ee + I1111 * IIIi1i1I + VeVV / iIiI1I11 / IIIi1i1I
def iI1II ( url ) :
 II1iiiIi1 = "ShowPicture(%s)" % url
 xbmc . executebuiltin ( II1iiiIi1 )
 if 69 - 69: i111I1 % I1iiiiI1iII
def ii1I1IIii11 ( name , url , iconimage , description ) :
 if description : name = description
 try :
  if 'plugin://plugin.video.SportsDevil/' in url :
   VeveeveV ( name , url , iconimage )
  elif '.ts' in url :
   url = 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;name=' + name + '&amp;url=' + url
   url = url . replace ( '|' , '' )
   VeveeveV ( name , url , iconimage )
  elif urlresolver . HostedMediaFile ( url ) . valid_url ( ) :
   url = urlresolver . HostedMediaFile ( url ) . resolve ( )
   IIIIiIiIi1 ( name , url , iconimage )
  elif liveresolver . isValid ( url ) == True :
   url = liveresolver . resolve ( url )
   IIIIiIiIi1 ( name , url , iconimage )
  else : IIIIiIiIi1 ( name , url , iconimage )
 except :
  I11iiiiI1i ( iI1i11 ( 'Evolve' ) , 'Stream Unavailable' , '3000' , Veveveeeeeevev )
  if 66 - 66: Ii1I % IIIi1i1I + i11iIiiIii . I1I1i1 / I111I11 + IIIi1i1I
def ii1I ( url ) :
 if urlresolver . HostedMediaFile ( url ) . valid_url ( ) :
  url = urlresolver . HostedMediaFile ( url ) . resolve ( )
 xbmc . Player ( ) . play ( url )
 if 86 - 86: eVev
def IIIIiIiIi1 ( name , url , iconimage ) :
 i1Iii11Ii1i1 = True
 VVeeeevVeveev = xbmcgui . ListItem ( name , iconImage = iconimage , thumbnailImage = iconimage ) ; VVeeeevVeveev . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
 i1Iii11Ii1i1 = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = url , listitem = VVeeeevVeveev )
 VVeeeevVeveev . setPath ( url )
 xbmcplugin . setResolvedUrl ( int ( sys . argv [ 1 ] ) , True , VVeeeevVeveev )
 if 14 - 14: eVev % Ii1I * ee + I111I11 + I1111 * I111I11
def VeveeveV ( name , url , iconimage ) :
 xbmc . executebuiltin ( 'Dialog.Close(all,True)' )
 i1Iii11Ii1i1 = True
 VVeeeevVeveev = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage ) ; VVeeeevVeveev . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
 i1Iii11Ii1i1 = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = url , listitem = VVeeeevVeveev )
 xbmc . Player ( ) . play ( url , VVeeeevVeveev , False )
 if 3 - 3: I1I1i1 * I1111
def eVeVeveveeevV ( url ) :
 xbmc . executebuiltin ( "PlayMedia(%s)" % url )
 if 74 - 74: i11iIiiIii . eeeVeveeeveVVVV
def VeeveVeveee ( url ) :
 iiI = urllib2 . Request ( url )
 iiI . add_header ( 'User-Agent' , 'mat' )
 eVIIiIi = urllib2 . urlopen ( iiI )
 eevev = eVIIiIi . read ( )
 eVIIiIi . close ( )
 eevev = eevev . replace ( '<fanart></fanart>' , '<fanart>x</fanart>' ) . replace ( '<thumbnail></thumbnail>' , '<thumbnail>x</thumbnail>' ) . replace ( '<utube>' , '<link>https://www.youtube.com/watch?v=' ) . replace ( '</utube>' , '</link>' )
 if '{' in eevev :
  II1iiiIi1 = eevev [ : : - 1 ]
  II1iiiIi1 = II1iiiIi1 . replace ( '}' , '' ) . replace ( '{' , '' ) . replace ( ',' , '' ) . replace ( ']' , '' ) . replace ( '[' , '' )
  II1iiiIi1 = II1iiiIi1 + '=='
  eevev = II1iiiIi1 . decode ( 'base64' )
 if url <> IiIi11iIIi1Ii : eevev = eevev . replace ( '\n' , '' ) . replace ( '\r' , '' )
 print eevev
 return eevev
 if 91 - 91: IIIi1i1I * I1111 / eeeVeveeeveVVVV . Ii1I + eeveevVeeveeeeev + I1I1i1
def eVVeev ( url ) :
 iiI = urllib2 . Request ( url )
 iiI . add_header ( 'User-Agent' , 'mat' )
 eVIIiIi = urllib2 . urlopen ( iiI )
 eevev = eVIIiIi . read ( )
 eVIIiIi . close ( )
 return eevev
 if 8 - 8: I1iiiiI1iII / IIIi1i1I
def Vev ( url ) :
 iiI = urllib2 . Request ( url )
 iiI . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' )
 eVIIiIi = urllib2 . urlopen ( iiI )
 eevev = eVIIiIi . read ( )
 eVIIiIi . close ( )
 eevev = eevev . replace ( '\n' , '' ) . replace ( '\r' , '' )
 return eevev
 if 20 - 20: eeeVeveeeveVVVV
 if 95 - 95: ee - eeeVeveeeveVVVV
def I1ii1ii11i1I ( ) :
 eevVeVV = [ ]
 VevVevVeevev = sys . argv [ 2 ]
 if len ( VevVevVeevev ) >= 2 :
  eevVevevVeev = sys . argv [ 2 ]
  eVeVeveve = eevVevevVeev . replace ( '?' , '' )
  if ( eevVevevVeev [ len ( eevVevevVeev ) - 1 ] == '/' ) :
   eevVevevVeev = eevVevevVeev [ 0 : len ( eevVevevVeev ) - 2 ]
  eVevevVev = eVeVeveve . split ( '&' )
  eevVeVV = { }
  for VevVVVevVVeVevV in range ( len ( eVevevVev ) ) :
   IIi1IIIi = { }
   IIi1IIIi = eVevevVev [ VevVVVevVVeVevV ] . split ( '=' )
   if ( len ( IIi1IIIi ) ) == 2 :
    eevVeVV [ IIi1IIIi [ 0 ] ] = IIi1IIIi [ 1 ]
 return eevVeVV
 if 99 - 99: I111I11 + eeveevVeeveeeeev * i1I1ii1II1iII . eVev - IIIi1i1I
def I11iiiiI1i ( title , message , ms , nart ) :
 xbmc . executebuiltin ( "XBMC.notification(" + title + "," + message + "," + ms + "," + nart + ")" )
 if 58 - 58: I111I11 + eVev - eeeVeveeeveVVVV
def VVeeV ( string ) :
 i1i1ii = re . compile ( '(\[.+?\])' ) . findall ( string )
 for iII1ii1 in i1i1ii : string = string . replace ( iII1ii1 , '' )
 return string
 if 12 - 12: eVeev - i111I1 . VeVVeveeVVeeevV / IIIi1i1I . eeveveveveVeVeVeve * eeveevVeeveeeeev
def iI1i11 ( string ) :
 string = string . split ( ' ' )
 IiIiII1 = ''
 for Iii1iiIi1II in string :
  VVevVeveveVe = '[B][COLOR red]' + Iii1iiIi1II [ 0 ] . upper ( ) + '[/COLOR][COLOR white]' + Iii1iiIi1II [ 1 : ] + '[/COLOR][/B] '
  IiIiII1 = IiIiII1 + VVevVeveveVe
 return IiIiII1
 if 14 - 14: eeeVeveeeveVVVV
def VeeevVVeveVV ( name , url , mode , iconimage , itemcount , metatype , isFolder = False , description = '' ) :
 if isFolder == True : VevVevVVevVevVev . setSetting ( 'favtype' , 'folder' )
 else : VevVevVVevVevVev . setSetting ( 'favtype' , 'link' )
 if Veeeeveveve == 'true' :
  IIiIiI1I = name
  name = VVeeV ( name )
  VeeVeVe = ""
  III1I1Iii1iiI = ""
  i1Iii11I1i = [ ]
  VeeveveevVVevVeveve = eval ( base64 . b64decode ( 'bWV0YWhhbmRsZXJzLk1ldGFEYXRhKHRtZGJfYXBpX2tleT0iZDk1NWQ4ZjAyYTNmMjQ4MGE1MTg4MWZlNGM5NmYxMGUiKQ==' ) )
  eV = { }
  if metatype == 'movie' :
   iI1Ii11iII1 = name . partition ( '(' )
   if len ( iI1Ii11iII1 ) > 0 :
    VeeVeVe = iI1Ii11iII1 [ 0 ]
    III1I1Iii1iiI = iI1Ii11iII1 [ 2 ] . partition ( ')' )
   if len ( III1I1Iii1iiI ) > 0 :
    III1I1Iii1iiI = III1I1Iii1iiI [ 0 ]
   eV = VeeveveevVVevVeveve . get_meta ( 'movie' , name = VeeVeVe , year = III1I1Iii1iiI )
   if not eV [ 'trailer' ] == '' : i1Iii11I1i . append ( ( iI1i11 ( 'Play Trailer' ) , 'XBMC.RunPlugin(%s)' % VeevVee . build_plugin_url ( { 'mode' : 11 , 'url' : eV [ 'trailer' ] } ) ) )
  elif metatype == 'tvep' :
   VVVeVevVeve = VevVevVVevVevVev . getSetting ( 'tv' )
   if '<>' in url :
    print url
    VVevevVe = url . split ( '<>' ) [ 0 ]
    eVee = url . split ( '<>' ) [ 1 ]
    iIii11I = url . split ( '<>' ) [ 2 ]
    VVVevVVVevevee = url . split ( '<>' ) [ 3 ]
    Iii111II = url . split ( '<>' ) [ 4 ]
    iiii11I = url . split ( '<>' ) [ 5 ]
    eV = VeeveveevVVevVeveve . get_episode_meta ( eVee , imdb_id = VVevevVe , season = iIii11I , episode = VVVevVVVevevee , air_date = '' , episode_title = '' , overlay = '' )
   else :
    VevVeee = re . compile ( 'Season (.+?) Episode (.+?)\)' ) . findall ( name )
    for iiIi1i , I1i11111i1i11 in VevVeee :
     eV = VeeveveevVVevVeveve . get_episode_meta ( VVVeVevVeve , imdb_id = '' , season = iiIi1i , episode = I1i11111i1i11 , air_date = '' , episode_title = '' , overlay = '' )
  try :
   if eV [ 'cover_url' ] == '' : iconimage = iconimage
   else : iconimage = eV [ 'cover_url' ]
  except : pass
  VVeVVVev = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&fanart=" + urllib . quote_plus ( eeeevVV ) + "&iconimage=" + urllib . quote_plus ( iconimage )
  i1Iii11Ii1i1 = True
  VVeeeevVeveev = xbmcgui . ListItem ( IIiIiI1I , iconImage = iconimage , thumbnailImage = iconimage )
  VVeeeevVeveev . setInfo ( type = "Video" , infoLabels = eV )
  VVeeeevVeveev . setProperty ( "IsPlayable" , "true" )
  VVeeeevVeveev . addContextMenuItems ( i1Iii11I1i , replaceItems = False )
  if not eV . get ( 'backdrop_url' , '' ) == '' : VVeeeevVeveev . setProperty ( 'fanart_image' , eV [ 'backdrop_url' ] )
  else : VVeeeevVeveev . setProperty ( 'fanart_image' , eeeevVV )
  I1I1i = VevVevVVevVevVev . getSetting ( 'favlist' )
  I1IIIiIiIi = [ ]
  I1IIIiIiIi . append ( ( iI1i11 ( 'Stream Information' ) , 'XBMC.Action(Info)' ) )
  if I1I1i == 'yes' : I1IIIiIiIi . append ( ( '[COLOR white]Remove from Evolve Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=21&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
  else : I1IIIiIiIi . append ( ( '[COLOR white]Add to Evolve Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=20&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
  VVeeeevVeveev . addContextMenuItems ( I1IIIiIiIi , replaceItems = False )
  i1Iii11Ii1i1 = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = VVeVVVev , listitem = VVeeeevVeveev , isFolder = isFolder , totalItems = itemcount )
  return i1Iii11Ii1i1
 else :
  if isFolder :
   eeevev ( name , url , mode , iconimage , eeeevVV , description = '' )
  else :
   eeveeVeeeeveveveVV ( name , url , mode , iconimage , eeeevVV , description = '' )
   if 27 - 27: IIIi1i1I + I1I1i1 - eVeev + Ii1I . I111I11
def eeevev ( name , url , mode , iconimage , fanart , description = '' ) :
 VevVevVVevVevVev . setSetting ( 'favtype' , 'folder' )
 VVeVVVev = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&fanart=" + urllib . quote_plus ( fanart ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 i1Iii11Ii1i1 = True
 VVeeeevVeveev = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 VVeeeevVeveev . setInfo ( type = "Video" , infoLabels = { "Title" : name , 'plot' : description } )
 VVeeeevVeveev . setProperty ( 'fanart_image' , fanart )
 if 'youtube.com/channel/' in url :
  VVeVVVev = 'plugin://plugin.video.youtube/channel/' + description + '/'
 if 'youtube.com/user/' in url :
  VVeVVVev = 'plugin://plugin.video.youtube/user/' + description + '/'
 if 'youtube.com/playlist?' in url :
  VVeVVVev = 'plugin://plugin.video.youtube/playlist/' + description + '/'
 if 'plugin://' in url :
  VVeVVVev = url
 I1IIIiIiIi = [ ]
 I1I1i = VevVevVVevVevVev . getSetting ( 'favlist' )
 if I1I1i == 'yes' : I1IIIiIiIi . append ( ( '[COLOR white]Remove from Evolve Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=21&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 else : I1IIIiIiIi . append ( ( '[COLOR white]Add to Evolve Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=20&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 VVeeeevVeveev . addContextMenuItems ( I1IIIiIiIi , replaceItems = False )
 i1Iii11Ii1i1 = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = VVeVVVev , listitem = VVeeeevVeveev , isFolder = True )
 return i1Iii11Ii1i1
 if 46 - 46: Ii1
def I1i1I1II ( name , url , mode , iconimage , fanart , description = '' ) :
 VevVevVVevVevVev . setSetting ( 'favtype' , 'link' )
 VVeVVVev = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&fanart=" + urllib . quote_plus ( fanart ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 i1Iii11Ii1i1 = True
 VVeeeevVeveev = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 VVeeeevVeveev . setProperty ( 'fanart_image' , fanart )
 I1IIIiIiIi = [ ]
 I1I1i = VevVevVVevVevVev . getSetting ( 'favlist' )
 if I1I1i == 'yes' : I1IIIiIiIi . append ( ( '[COLOR white]Remove from Evolve Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=21&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 else : I1IIIiIiIi . append ( ( '[COLOR white]Add to Evolve Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=20&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 VVeeeevVeveev . addContextMenuItems ( I1IIIiIiIi , replaceItems = False )
 i1Iii11Ii1i1 = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = VVeVVVev , listitem = VVeeeevVeveev , isFolder = False )
 return i1Iii11Ii1i1
 if 45 - 45: i111I1
def eeveeVeeeeveveveVV ( name , url , mode , iconimage , fanart , description = '' ) :
 VevVevVVevVevVev . setSetting ( 'favtype' , 'link' )
 VVeVVVev = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&fanart=" + urllib . quote_plus ( fanart ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 i1Iii11Ii1i1 = True
 VVeeeevVeveev = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 VVeeeevVeveev . setProperty ( 'fanart_image' , fanart )
 VVeeeevVeveev . setProperty ( "IsPlayable" , "true" )
 I1IIIiIiIi = [ ]
 I1I1i = VevVevVVevVevVev . getSetting ( 'favlist' )
 if I1I1i == 'yes' : I1IIIiIiIi . append ( ( '[COLOR white]Remove from Evolve Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=21&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 else : I1IIIiIiIi . append ( ( '[COLOR white]Add to Evolve Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=20&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 VVeeeevVeveev . addContextMenuItems ( I1IIIiIiIi , replaceItems = False )
 i1Iii11Ii1i1 = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = VVeVVVev , listitem = VVeeeevVeveev , isFolder = False )
 return i1Iii11Ii1i1
 if 21 - 21: I1iiiiI1iII . iIiI1I11 . eVeev / I1111 / iIiI1I11
def eeveVev ( url , name ) :
 i1iI1 = eVVeev ( url )
 if len ( i1iI1 ) > 1 :
  eeI1111i = VeevV
  iIIii = os . path . join ( os . path . join ( eeI1111i , '' ) , name + '.txt' )
  if not os . path . exists ( iIIii ) :
   file ( iIIii , 'w' ) . close ( )
  ii1I1IiiI1ii1i = open ( iIIii )
  Veve = ii1I1IiiI1ii1i . read ( )
  if Veve == i1iI1 : pass
  else :
   I11iII ( '[B][COLOR red]E[/COLOR][COLOR white]volve[/COLOR][/B] [B][COLOR red]I[/COLOR][COLOR white]nformation[/COLOR][/B]' , i1iI1 )
   eevevVevV = open ( iIIii , "w" )
   eevevVevV . write ( i1iI1 )
   eevevVevV . close ( )
   if 54 - 54: eVeev
def I11iII ( heading , text ) :
 id = 10147
 xbmc . executebuiltin ( 'ActivateWindow(%d)' % id )
 xbmc . sleep ( 500 )
 IiI11ii1I = xbmcgui . Window ( id )
 IiiiI = 50
 while ( IiiiI > 0 ) :
  try :
   xbmc . sleep ( 10 )
   IiiiI -= 1
   IiI11ii1I . getControl ( 1 ) . setLabel ( heading )
   IiI11ii1I . getControl ( 5 ) . setText ( text )
   return
  except :
   pass
   if 61 - 61: eVeev % eVeev * eVev / eVev
def eeveVV ( name ) :
 global Icon
 global Next
 global Previous
 global window
 global Quit
 global images
 iIIii = os . path . join ( os . path . join ( VeevV , '' ) , name + '.txt' )
 ii1I1IiiI1ii1i = open ( iIIii )
 Veve = ii1I1IiiI1ii1i . read ( )
 images = re . compile ( '<image>(.+?)</image>' ) . findall ( Veve )
 VevVevVVevVevVev . setSetting ( 'pos' , '0' )
 window = pyxbmct . AddonDialogWindow ( '' )
 VeveevVVeveveveveee = '/resources/art'
 iIIII1iIIii = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + VVeve + VeveevVVeveveveveee , 'next_focus.png' ) )
 eVVVeveveeveveve = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + VVeve + VeveevVVeveveveveee , 'next1.png' ) )
 iIi11i1 = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + VVeve + VeveevVVeveveveveee , 'previous_focus.png' ) )
 eVeveveeeveeveveeve = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + VVeve + VeveevVVeveveveveee , 'previous.png' ) )
 IiIIIIIi = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + VVeve + VeveevVVeveveveveee , 'close_focus.png' ) )
 IiIi1iIIi1 = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + VVeve + VeveevVVeveveveveee , 'close.png' ) )
 VevVeVeveeVVeve = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + VVeve + VeveevVVeveveveveee , 'main-bg1.png' ) )
 window . setGeometry ( 1300 , 720 , 100 , 50 )
 VeVeeveVeeVeVV = pyxbmct . Image ( VevVeVeveeVVeve )
 window . placeControl ( VeVeeveVeeVeVV , - 10 , - 10 , 130 , 70 )
 ii1 = '0xFF000000'
 Previous = pyxbmct . Button ( '' , focusTexture = iIi11i1 , noFocusTexture = eVeveveeeveeveveeve , textColor = ii1 , focusedColor = ii1 )
 Next = pyxbmct . Button ( '' , focusTexture = iIIII1iIIii , noFocusTexture = eVVVeveveeveveve , textColor = ii1 , focusedColor = ii1 )
 Quit = pyxbmct . Button ( '' , focusTexture = IiIIIIIi , noFocusTexture = IiIi1iIIi1 , textColor = ii1 , focusedColor = ii1 )
 Icon = pyxbmct . Image ( images [ 0 ] , aspectRatio = 2 )
 window . placeControl ( Previous , 102 , 1 , 10 , 10 )
 window . placeControl ( Next , 102 , 40 , 10 , 10 )
 window . placeControl ( Quit , 102 , 21 , 10 , 10 )
 window . placeControl ( Icon , 0 , 0 , 100 , 50 )
 Previous . controlRight ( Next )
 Previous . controlUp ( Quit )
 window . connect ( Previous , eeeveveeVeVevev )
 window . connect ( Next , eeveveVeVeev )
 Previous . setVisible ( False )
 window . setFocus ( Quit )
 Previous . controlRight ( Quit )
 Quit . controlLeft ( Previous )
 Quit . controlRight ( Next )
 Next . controlLeft ( Quit )
 window . connect ( Quit , window . close )
 window . doModal ( )
 del window
 if 72 - 72: iIiI1I11
def eeveveVeVeev ( ) :
 VVeveeeeveVV = int ( VevVevVVevVevVev . getSetting ( 'pos' ) )
 eeevevev = int ( VVeveeeeveVV ) + 1
 VevVevVVevVevVev . setSetting ( 'pos' , str ( eeevevev ) )
 ii = len ( images )
 Icon . setImage ( images [ int ( eeevevev ) ] )
 Previous . setVisible ( True )
 if int ( eeevevev ) == int ( ii ) - 1 :
  Next . setVisible ( False )
  if 78 - 78: VeVVeveeVVeeevV . eeveevVeeveeeeev + i111I1 - eeveveveveVeVeVeve
def eeeveveeVeVevev ( ) :
 VVeveeeeveVV = int ( VevVevVVevVevVev . getSetting ( 'pos' ) )
 ii1Vev = int ( VVeveeeeveVV ) - 1
 VevVevVVevVevVev . setSetting ( 'pos' , str ( ii1Vev ) )
 Icon . setImage ( images [ int ( ii1Vev ) ] )
 Next . setVisible ( True )
 if int ( ii1Vev ) == 0 :
  Previous . setVisible ( False )
  if 33 - 33: eeveveveveVeVeVeve
def Ii1iII1iI1 ( url , fanart ) :
 VevVevVVevVevVev . setSetting ( 'favlist' , 'yes' )
 i1i1IIIIi1i = None
 file = open ( IiI , 'r' )
 i1i1IIIIi1i = file . read ( ) . replace ( '\n' , '' ) . replace ( '\r' , '' )
 eeveVeVeveve = re . compile ( "<item>(.+?)</item>" , re . DOTALL ) . findall ( i1i1IIIIi1i )
 for i1 in eeveVeVeveve :
  VVeVeveve ( i1111 , url , Veveveeeeeevev , fanart , i1 )
 VevVevVVevVevVev . setSetting ( 'favlist' , 'no' )
 if 7 - 7: VeVV + ee * i11iIiiIii / VeVVeveeVVeeevV + ee - I1111
def Iiii ( name , url , iconimage , fanart ) :
 eeeVVeeee = VevVevVVevVevVev . getSetting ( 'favtype' )
 url = url . replace ( ' ' , '%20' )
 iconimage = iconimage . replace ( ' ' , '%20' )
 if '<>' in url :
  VVevevVe = url . split ( '<>' ) [ 0 ]
  iIii11I = url . split ( '<>' ) [ 1 ]
  VVVevVVVevevee = url . split ( '<>' ) [ 2 ]
  Iii111II = url . split ( '<>' ) [ 3 ]
  iiii11I = url . split ( '<>' ) [ 4 ]
  II1iiiIi1 = '<FAV><item>\n<title>' + name + '</title>\n<meta>tvep</meta>\n<nan>tvshow</nan>\n<showyear>' + Iii111II + '</showyear>\n<imdb>' + VVevevVe + '</imdb>\n<season>' + iIii11I + '</season>\n<episode>' + VVVevVVVevevee + '</episode>\n<episodeyear>' + iiii11I + '</episodeyear>\n<thumbnail>' + iconimage + '</thumbnail>\n<fanart>' + fanart + '</fanart></item></FAV>\n'
 elif len ( url ) == 9 :
  II1iiiIi1 = '<FAV><item>\n<title>' + name + '</title>\n<meta>movie</meta>\n<nan>movie</nan>\n<imdb>' + url + '</imdb>\n' + '<thumbnail>' + iconimage + '</thumbnail>\n<fanart>' + fanart + '</fanart></item></FAV>\n'
 else :
  II1iiiIi1 = '<FAV><item>\n<title>' + name + '</title>\n<' + eeeVVeeee + '>' + url + '</' + eeeVVeeee + '>\n' + '<thumbnail>' + iconimage + '</thumbnail>\n<fanart>' + fanart + '</fanart></item></FAV>\n'
 eeVe = open ( IiI , 'a' )
 eeVe . write ( II1iiiIi1 )
 eeVe . close ( )
 if 89 - 89: ee - i111I1 % I1111 % eVev
def IIiii11i ( name , url , iconimage ) :
 print name
 i1i1IIIIi1i = None
 file = open ( IiI , 'r' )
 i1i1IIIIi1i = file . read ( )
 VeveveVeeveveeve = ''
 eeveVeVeveve = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( i1i1IIIIi1i )
 for eVVeeevevVevV in eeveVeVeveve :
  II1iiiIi1 = '\n<FAV><item>\n' + eVVeeevevVevV + '</item>\n'
  if name in eVVeeevevVevV :
   print 'xxxxxxxxxxxxxxxxx'
   II1iiiIi1 = II1iiiIi1 . replace ( 'item' , ' ' )
  VeveveVeeveveeve = VeveveVeeveveeve + II1iiiIi1
 file = open ( IiI , 'w' )
 file . truncate ( )
 file . write ( VeveveVeeveveeve )
 file . close ( )
 xbmc . executebuiltin ( 'Container.Refresh' )
 if 85 - 85: ee + VeVVeveeVVeeevV * ee - iIiI1I11 % i11iIiiIii
def IIiII ( url ) :
 try :
  iiIiii1IIIII = url . split ( '/' ) [ 2 ] . replace ( 'www.' , '' )
  file = open ( IIi1IiiiI1Ii , 'r' )
  VVeevevVeV = file . read ( )
  if iiIiii1IIIII in VVeevevVeV : return '[COLOR springgreen] (RD)[/COLOR]'
  else : return ''
 except : return ''
 if 10 - 10: eVev / i11iIiiIii
def eeveveV ( ) :
 xbmcaddon . Addon ( 'script.module.nanscrapers' ) . openSettings ( )
 if 92 - 92: Ii1 * I1111 * I1111 * eeeVeveeeveVVVV . VeVV
def I1Ii1111iIi ( ) :
 xbmcaddon . Addon ( 'script.module.urlresolver' ) . openSettings ( )
 if 31 - 31: i1Ii . iIiI1I11 * i111I1 + i11iIiiIii * I1iiiiI1iII
def VVeveeeeveevVevVeeeee ( ) :
 xbmcaddon . Addon ( 'script.module.metahandler' ) . openSettings ( )
 if 1 - 1: i111I1 % I1I1i1 * I1111
def eVe ( link ) :
 try :
  eevVeveeev = re . compile ( '<layouttype>(.+?)</layouttype>' ) . findall ( link ) [ 0 ]
  if eevVeveeev == 'thumbnail' : xbmc . executebuiltin ( 'Container.SetViewMode(500)' )
  else : xbmc . executebuiltin ( 'Container.SetViewMode(50)' )
 except : pass
 if 30 - 30: Ii1I * VeVVeveeVVeeevV
 if 38 - 38: Ii1 - IIIi1i1I . I1I1i1 - iIiI1I11 . VeVVeveeVVeeevV
eevVevevVeev = I1ii1ii11i1I ( ) ; i11 = None ; i1111 = None ; iII11 = None ; eee = None ; I11 = None ; VeeeeVeveVV = None
try : eee = urllib . unquote_plus ( eevVevevVeev [ "site" ] )
except : pass
try : i11 = urllib . unquote_plus ( eevVevevVeev [ "url" ] )
except : pass
try : i1111 = urllib . unquote_plus ( eevVevevVeev [ "name" ] )
except : pass
try : iII11 = int ( eevVevevVeev [ "mode" ] )
except : pass
try : I11 = urllib . unquote_plus ( eevVevevVeev [ "iconimage" ] )
except : pass
try : eeeevVV = urllib . unquote_plus ( eevVevevVeev [ "fanart" ] )
except : pass
try : VeeeeVeveVV = str ( eevVevevVeev [ "description" ] )
except : pass
if 30 - 30: VeVVeveeVVeeevV - VeVVeveeVVeeevV . Ii1I / ee
if iII11 == None or i11 == None or len ( i11 ) < 1 : VeveV ( )
elif iII11 == 1 : eVeV ( i1111 , i11 , I11 , eeeevVV )
elif iII11 == 2 : ii1I1IIii11 ( i1111 , i11 , I11 , VeeeeVeveVV )
elif iII11 == 3 : I1iiii1I ( i1111 , i11 , I11 )
elif iII11 == 4 : IIIIiIiIi1 ( i1111 , i11 , I11 )
elif iII11 == 5 : eVeevVVVeVV ( )
elif iII11 == 6 : Iii1I1111ii ( i11 , I11 )
elif iII11 == 7 : iI1II ( i11 )
elif iII11 == 8 : eeveVV ( i1111 )
elif iII11 == 9 : VVVeVe ( i1111 , i11 )
elif iII11 == 10 : eeevVevVevev ( i1111 , i11 , I11 , eeeevVV )
elif iII11 == 11 : eVeVeveveeevV ( i11 )
elif iII11 == 12 : I1Ii1111iIi ( )
elif iII11 == 13 : VVeveeeeveevVevVeeeee ( )
elif iII11 == 15 : SCRAPEMOVIE ( i1111 , i11 , I11 )
elif iII11 == 16 : VeveeveV ( i1111 , i11 , I11 )
elif iII11 == 17 : II1I1iiIII ( i1111 , i11 )
elif iII11 == 18 : eVeveevVVVV ( i1111 , i11 , I11 , eeeevVV )
elif iII11 == 19 : Ii1i11IIii1I ( i1111 , i11 , I11 , eeeevVV )
if 31 - 31: eVeev + eVev . VeVVeveeVVeeevV
elif iII11 == 20 : Iiii ( i1111 , i11 , I11 , eeeevVV )
elif iII11 == 21 : IIiii11i ( i1111 , i11 , I11 )
elif iII11 == 22 : Ii1iII1iI1 ( i11 , eeeevVV )
elif iII11 == 23 : DOIPLAYER ( i1111 , i11 , I11 , eeeevVV )
elif iII11 == 24 : i1IIIiiII1 ( i1111 , i11 , I11 , eeeevVV )
elif iII11 == 25 : eeveveV ( )
if 89 - 89: i1I1ii1II1iII + eeveveveveVeVeVeve + i1I1ii1II1iII
elif iII11 == 26 : VVeVeeevevee ( i1111 , i11 , I11 , eeeevVV )
elif iII11 == 27 : VevVevevVee ( i1111 , i11 , I11 , eeeevVV )
elif iII11 == 28 : Ii1I1IIii1II ( i1111 , i11 , I11 , eeeevVV )
elif iII11 == 29 : VVevVeVeveevev ( i1111 , i11 , I11 , eeeevVV )
elif iII11 == 30 : iiIii ( i1111 , i11 , I11 , eeeevVV )
elif iII11 == 31 : Ii ( i1111 , i11 , I11 , eeeevVV )
elif iII11 == 32 : IiIIIi1iIi ( i1111 , i11 , I11 , eeeevVV )
elif iII11 == 33 : eeveveeeVevVe ( i11 )
elif iII11 == 34 : eeve ( i1111 , i11 , I11 , eeeevVV )
elif iII11 == 35 : I1111IIIIIi ( i1111 , i11 , I11 , eeeevVV )
if 7 - 7: Ii1I % eVev + IIIi1i1I * ee - ee
if 42 - 42: I1I1i1 * I1I1i1 * iIiI1I11 . i1Ii
if 51 - 51: eVeev % VeVV - VeVVeveeVVeeevV % i111I1 * VeVV % eeveevVeeveeeeev
if 99 - 99: I1iiiiI1iII * i1I1ii1II1iII * iIiI1I11
if 92 - 92: I1111
if 40 - 40: I1I1i1 / Ii1
if 79 - 79: eeveevVeeveeeeev - VeVV + I111I11 - iIiI1I11
xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3
