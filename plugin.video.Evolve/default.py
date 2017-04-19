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
 eeevev ( '[B][COLOR chartreuse]S[/COLOR][COLOR white]earch[/COLOR][/B] [B][COLOR chartreuse]E[/COLOR][COLOR white]volve[/COLOR][/B]' , 'http://matsbuilds.uk/anewEvolvemenu/search.xml' , 5 , 'http://i.imgur.com/oHqT3bb.png' , II1 )
 xbmc . executebuiltin ( 'Container.SetViewMode(500)' )
 if 98 - 98: I1111 * eeveevVeeveeeeev / I1I1i1 * eVev / IIIi1i1I
def VVeVeeevevee ( name , url , iconimage , fanart ) :
 if not os . path . exists ( VeevV ) :
  os . mkdir ( VeevV )
 eeevev ( '[B][COLOR tersomet]MOVIE SEARCH[/COLOR][/B]' , 'http://matsbuilds.uk/EvolveMenus/Movies/Search/Search.txt' , 5 , 'http://i.imgur.com/oHqT3bb.png' , II1 )
 iiI11 = VVeeV ( name )
 VevVevVVevVevVev . setSetting ( 'movie' , iiI11 )
 eevev = VeeveVeveee ( url )
 eeveVeVeveve = re . compile ( '<item>(.+?)</item>' ) . findall ( eevev )
 for i1 in eeveVeVeveve :
  eVVeeevevVevV = re . compile ( '<title>(.+?)</title>.+?folder>(.+?)</folder>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>' ) . findall ( i1 )
  for name , url , iconimage , fanart in eVVeeevevVevV :
   VVeVeveve ( name , url , iconimage , fanart , i1 )
   if 9 - 9: I1iiiiI1iII - eVeev / i1Ii % I111I11
   if 62 - 62: VevVeeVevVVeee - Ii1 / iIiI1I11 % i111I1 % eVev
def eVeV ( name , url , iconimage , fanarts ) :
 if not os . path . exists ( VeevV ) :
  os . mkdir ( VeevV )
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
   if 68 - 68: I1I1i1 . I1iiiiI1iII . i11iIiiIii
def II ( name , url , iconimage , fanart ) :
 iiI11 = VVeeV ( name )
 VevVevVVevVevVev . setSetting ( 'tv' , iiI11 )
 eevev = VeeveVeveee ( url )
 iI ( eevev )
 if '<message>' in eevev :
  IiIi11iIIi1Ii = re . compile ( '<message>(.+?)</message>' ) . findall ( eevev ) [ 0 ]
  eeveVev ( IiIi11iIIi1Ii , iiI11 )
 if '<intro>' in eevev :
  iI11iiiI1II = re . compile ( '<intro>(.+?)</intro>' ) . findall ( eevev ) [ 0 ]
  VeveeeeevVeevev ( iI11iiiI1II )
 if 'XXX>yes</XXX' in eevev : Ii11iii11I ( eevev )
 eeveVeVeveve = re . compile ( '<item>(.+?)</item>' ) . findall ( eevev )
 for i1 in eeveVeVeveve :
  VVeVeveve ( name , url , iconimage , fanart , i1 )
  if 72 - 72: eVeev
def VVeVeveve ( name , url , iconimage , fanart , item ) :
 if 63 - 63: I111I11
 if '<sportsdevil>' in item : Vevev ( name , url , iconimage , fanart , item )
 elif '<iplayer>' in item : iII11i ( name , url , iconimage , fanart , item )
 elif '<folder>' in item : VevVeveveevVVVev ( name , url , iconimage , fanart , item )
 elif '<iptv>' in item : Ii1iIIIi1ii ( name , url , iconimage , fanart , item )
 elif '<image>' in item : eeveeeveevVevevVV ( name , url , iconimage , fanart , item )
 elif '<text>' in item : eeveV ( name , url , iconimage , fanart , item )
 elif '<scraper>' in item : I1i1iii ( name , url , iconimage , fanart , item )
 elif '<lbscraper>' in item : i1iiI11I ( name , url , iconimage , fanart , item )
 elif '<redirect>' in item : iiii ( name , url , iconimage , fanart , item )
 elif '<oktitle>' in item : eVeveevVevVVVeeev ( name , url , iconimage , fanart , item )
 elif '<nan>' in item : IiIiiI ( name , url , iconimage , fanart , item )
 else : I1I ( name , url , iconimage , fanart , item )
 if 80 - 80: I1I1i1 - eeveevVeeveeeeev
 if 87 - 87: I1iiiiI1iII / i1Ii - eeveveveveVeVeVeve * eVeev / VeVVeveeVVeeevV . Ii1I
def iII11i ( name , url , iconimage , fanart , item ) :
 url = re . compile ( '<iplayer>(.+?)</iplayer>' ) . findall ( item ) [ 0 ]
 name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
 url = 'plugin://plugin.video.iplayerwww/?url=%s&mode=202&name=%s&iconimage=%s&description=&subtitles_url=&logged_in=False' % ( url , name , iconimage )
 iii11I111 ( name , url , 16 , iconimage , fanart )
 if 63 - 63: eeveevVeeveeeeev * I1iiiiI1iII - VevVeeVevVVeee * Ii1I
def IiIiiI ( name , url , iconimage , fanart , item ) :
 name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 iIii111IIi = re . compile ( '<meta>(.+?)</meta>' ) . findall ( item ) [ 0 ]
 iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
 iii11 = re . compile ( '<nan>(.+?)</nan>' ) . findall ( item ) [ 0 ]
 VeveeevVVeveVVVe = re . compile ( '<imdb>(.+?)</imdb>' ) . findall ( item ) [ 0 ]
 if iii11 == 'movie' :
  VeveeevVVeveVVVe = VeveeevVVeveVVVe + '<>movie'
 elif iii11 == 'tvshow' :
  i1i1i11IIi = re . compile ( '<showname>(.+?)</showname>' ) . findall ( item ) [ 0 ]
  II1III = re . compile ( '<season>(.+?)</season>' ) . findall ( item ) [ 0 ]
  iI1iI1I1i1I = re . compile ( '<episode>(.+?)</episode>' ) . findall ( item ) [ 0 ]
  iIi11Ii1 = re . compile ( '<showyear>(.+?)</showyear>' ) . findall ( item ) [ 0 ]
  Ii11iII1 = re . compile ( '<episodeyear>(.+?)</episodeyear>' ) . findall ( item ) [ 0 ]
  VeveeevVVeveVVVe = VeveeevVVeveVVVe + '<>' + i1i1i11IIi + '<>' + II1III + '<>' + iI1iI1I1i1I + '<>' + iIi11Ii1 + '<>' + Ii11iII1
  iii11 = "tvep"
 VeevVevVeveeVevV ( name , VeveeevVVeveVVVe , 19 , iconimage , 1 , iii11 , isFolder = True )
 if 15 - 15: IIIi1i1I + I1I1i1 - VeVVeveeVVeeevV / eVeev
def eeevevevVVevevVe ( name , imdb , iconimage , fanart ) :
 IIi1IiiiI1Ii = ''
 VevVVVevVVeVevV = name
 iiI11 = VVeeV ( name )
 VevVevVVevVevVev . setSetting ( 'tv' , iiI11 )
 if 'movie' in imdb :
  imdb = imdb . split ( '<>' ) [ 0 ]
  VevevVeeveveveeVev = [ ]
  VeVevVevev = [ ]
  IIiII = name . partition ( '(' )
  eev = IIiII [ 0 ]
  eev = VVeeV ( eev )
  eeVeeeeveveveVV = IIiII [ 2 ] . partition ( ')' ) [ 0 ]
  VeeveVVe = nanscrapers . scrape_movie ( eev , eeVeeeeveveveVV , imdb , timeout = 800 )
 else :
  i1i1i11IIi = imdb . split ( '<>' ) [ 1 ]
  VeevVeVeveveVVeve = imdb . split ( '<>' ) [ 0 ]
  II1III = imdb . split ( '<>' ) [ 2 ]
  iI1iI1I1i1I = imdb . split ( '<>' ) [ 3 ]
  iIi11Ii1 = imdb . split ( '<>' ) [ 4 ]
  Ii11iII1 = imdb . split ( '<>' ) [ 5 ]
  VeeveVVe = nanscrapers . scrape_episode ( i1i1i11IIi , iIi11Ii1 , Ii11iII1 , II1III , iI1iI1I1i1I , VeevVeVeveveVVeve , None )
 VVVevevV = 1
 for VVeVVeveeeveeV in list ( VeeveVVe ( ) ) :
  for VeveevVevevVeeveev in VVeVVeveeeveeV :
   if urlresolver . HostedMediaFile ( VeveevVevevVeeveev [ 'url' ] ) . valid_url ( ) :
    IIi1IiiiI1Ii = VevevVeveVVevevVevev ( VeveevVevevVeeveev [ 'url' ] )
    name = "Link " + str ( VVVevevV ) + ' | ' + VeveevVevevVeeveev [ 'source' ] + IIi1IiiiI1Ii
    VVVevevV = VVVevevV + 1
    i1Veevev ( name , VeveevVevevVeeveev [ 'url' ] , 2 , iconimage , fanart , description = VevVevVVevVevVev . getSetting ( 'tv' ) )
    if 31 - 31: iIiI1I11 . I1I1i1 / Ii1I
def I1i1iii ( name , url , iconimage , fanart , item ) :
 name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 url = re . compile ( '<scraper>(.+?)</scraper>' ) . findall ( item ) [ 0 ]
 fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
 eeevev ( name , url , 18 , iconimage , fanart )
 if 89 - 89: I1I1i1
def VVeveVeVVeveVVev ( name , url , iconimage , fanart ) :
 eVevVVeeevVV = url
 if eVevVVeeevVV == 'latestmovies' :
  Vev = 15
  ii1ii1ii = eeeeeVeeeveee ( )
  I1I1IiI1 = re . compile ( '<item>(.+?)</item>' ) . findall ( ii1ii1ii )
  for i1 in I1I1IiI1 :
   eVVeeevevVevV = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>' ) . findall ( i1 )
   III1iII1I1ii = len ( I1I1IiI1 )
   for name , url , iconimage , fanart in eVVeeevevVevV :
    if '<meta>' in i1 :
     eVVeev = re . compile ( '<meta>(.+?)</meta>' ) . findall ( i1 ) [ 0 ]
     VeevVevVeveeVevV ( name , url , Vev , iconimage , III1iII1I1ii , eVVeev , isFolder = False )
    else : i1Veevev ( name , url , 15 , iconimage , fanart )
    if 54 - 54: Ii1I - Ii1 % eVeev
    if 77 - 77: I1I1i1 / eeeVeveeeveVVVV / eeveevVeeveeeeev + eeveevVeeveeeeev . eVeev
def ii1ii11IIIiiI ( name , url , iconimage , fanarts ) :
 eevev = VevevVVVeVeeevV ( url )
 VevevevVVeevevee = re . compile ( '<a title=".+?" .+? style="background-image: url(.+?)"></a>.+?<div class="hb-right">.+?<a title=".+?" href="(.+?)" class="episode">(.+?)</a>' , re . DOTALL ) . findall ( eevev )
 for iconimage , url , name in VevevevVVeevevee :
  iconimage = iconimage . replace ( "('" , "" ) . replace ( "')" , "" )
  name = name . replace ( "&#39;" , "'" )
  name = name . split ( '  ' ) [ 0 ]
  eeevev ( name , url , 24 , iconimage , iconimage )
  if 71 - 71: i11iIiiIii + Ii1
def eVe ( name , url , iconimage , fanart ) :
 eevev = VevevVVVeVeeevV ( url )
 VevevevVVeevevee = re . compile ( '<div class="cb-first">.+?<a href="(.+?)" class="c-image"><img alt=".+?" title="(.+?)" src="(.+?)"></a>' , re . DOTALL ) . findall ( eevev )
 for url , name , iconimage in VevevevVVeevevee :
  name = name . replace ( "&#39;" , "'" )
  eeevev ( name , url , 31 , iconimage , iconimage )
  if 75 - 75: eeeVeveeeveVVVV + I1111
def VeeeVeveV ( name , url , iconimage , fanart ) :
 eevev = i1iIi ( url )
 VevevevVVeevevee = re . compile ( '<a href="(.+?)" class="c-image"><img alt=".+?" title="(.+?)" src="(.+?)"></a>' , ) . findall ( eevev )
 for url , name , iconimage in VevevevVVeevevee :
  iconimage = iconimage . replace ( "('" , "" ) . replace ( "')" , "" )
  name = name . replace ( "&#39;" , "'" )
  eeevev ( name , url , 31 , iconimage , iconimage )
  if 68 - 68: i11iIiiIii % IIIi1i1I + i11iIiiIii
def iii ( name , url , iconimage , fanart ) :
 eevev = i1iIi ( url )
 II1I = re . compile ( '<div class="std-cts">.+?<div class="sdt-content tnContent">.+?<h2>(.+?)</h2>' , re . DOTALL ) . findall ( eevev ) [ 0 ] . replace ( ' Episodes' , '' )
 eeveVeVeveve = re . compile ( '<a title=".+?" href="(.+?)">.+?<div class="season">(.+?) </div>.+?<div class="episode">(.+?)</div>.+?<div class="e-name">(.+?)</div>' , re . DOTALL ) . findall ( eevev )
 for url , II1III , iI1iI1I1i1I , Vevi1II1Iiii1I11 in eeveVeVeveve :
  Vevi1II1Iiii1I11 = Vevi1II1Iiii1I11 . replace ( "&#39;" , "'" ) . replace ( '&amp;' , ' & ' )
  if '</div>' in name : name = 'TBA'
  eeevev ( '%s ' % II1I + '(%s ' % II1III + '%s)' % iI1iI1I1i1I , url , 24 , iconimage , iconimage )
  if 9 - 9: IIIi1i1I / I1111 - eeeVeveeeveVVVV / VeVVeveeVVeeevV / VeVV - eVev
def eeveveeeVevVe ( name , url , iconimage , fanart ) :
 VevVVVevVVeVevV = name
 eevev = i1iIi ( url )
 eevVevVVVevVee = re . compile ( '<a target="_blank" href=".+?" data-episodeid=".+?" data-linkid=".+?" data-hostname=".+?" class="watch-button" data-actuallink="(.+?)">Watch Now!</a>' ) . findall ( eevev )
 VVVevevV = 1
 VevevVeeveveveeVev = [ ]
 VeVevVevev = [ ]
 for iiIiI in eevVevVVVevVee :
  IIi1IiiiI1Ii = VevevVeveVVevevVevev ( iiIiI )
  if 'http' in iiIiI : I1 = iiIiI . split ( '/' ) [ 2 ] . split ( '.' ) [ 0 ]
  else : I1 = iiIiI
  name = "Link " + str ( VVVevevV ) + ' | ' + I1 + IIi1IiiiI1Ii
  if I1 != 'www' :
   i1Veevev ( I1 , iiIiI , 2 , iconimage , fanart , description = '' )
   if 86 - 86: I1I1i1 - I111I11 - eeveevVeeveeeeev * VevVeeVevVVeee
def eeeeevVev ( name , url , iconiamge , fanart ) :
 eevev = i1iIi ( url )
 VevevevVVeevevee = re . compile ( '<td height="20">(.+?)</td>.+?<td>(.+?)</td>.+?<td><a href=".+?">(.+?)</a></td>.+?<td><a href=".+?">(.+?)</a></td>.+?</tr>' , re . DOTALL ) . findall ( eevev )
 for eVVV , name , iIII1 , eeve in VevevevVVeevevee :
  name = name . replace ( "&#8217;" , "'" ) . replace ( '&amp;' , ' & ' )
  eeevev ( '[COLOR yellow]%s[/COLOR] - ' % iIII1 + '[COLOR blue]%s[/COLOR] ' % name + '- [COLOR white]%s[/COLOR]' % eVVV , url , 5 , I11 , fanart )
  if 73 - 73: Ii1 * IIIi1i1I + eeeVeveeeveVVVV . i111I1
def eeveVevevevevev ( url ) :
 VVVVeeevVe = ''
 ii111iI1iIi1 = xbmc . Keyboard ( VVVVeeevVe , '[B][COLOR red]S[/COLOR][COLOR white]earch[/COLOR][/B] [B][COLOR red]E[/COLOR][COLOR white]volve[/COLOR][/B]' )
 ii111iI1iIi1 . doModal ( )
 if ii111iI1iIi1 . isConfirmed ( ) :
  VVVVeeevVe = ii111iI1iIi1 . getText ( ) . replace ( ' ' , '+' ) . replace ( '+and+' , '+%26+' )
 if len ( VVVVeeevVe ) > 1 :
  url = 'http://www.watchepisodes4.com/search/ajax_search?q=' + VVVVeeevVe
  eevev = i1iIi ( url )
  eVVeeevevVevV = json . loads ( eevev )
  eVVeeevevVevV = eVVeeevevVevV [ 'series' ]
  for i1 in eVVeeevevVevV :
   i1111 = i1 [ 'value' ]
   VVV = i1 [ 'seo' ]
   url = 'http://www.watchepisodes4.com/' + VVV
   I11 = 'http://www.watchepisodes4.com/movie_images/' + VVV + '.jpg'
   eeevev ( i1111 , url , 31 , I11 , eeeevVV )
 else :
  eevev = VeeveVeveee ( url )
  eeevVVeev = re . compile ( '<link>(.+?)</link>' ) . findall ( eevev )
  for url in eeevVVeev :
   try :
    eevev = VeeveVeveee ( url )
    I11IiI = re . compile ( '<item>(.+?)</item>' ) . findall ( eevev )
    for i1 in I11IiI :
     eeveVeVeveve = re . compile ( '<title>(.+?)</title>' ) . findall ( i1 )
     for VevVVVevVVeVevV in eeveVeVeveve :
      VevVVVevVVeVevV = VevVVVevVVeVevV . upper ( )
      if search_entered in VevVVVevVVeVevV :
       VVeVeveve ( i1111 , url , I11 , eeeevVV , i1 )
   except :
    pass
    if 53 - 53: VevVeeVevVVeee % i1I1ii1II1iII . Ii1 - VeVV - Ii1 * i1I1ii1II1iII
    if 77 - 77: VeVV * eeveevVeeveeeeev
    if 95 - 95: eeeVeveeeveVVVV + i11iIiiIii
def eeeeeVeeeveee ( ) :
 I1Ii = 'movie'
 eevev = i1iIi ( 'http://newmoviesonline.ws/' )
 VeveeeveveevV = re . compile ( '<a href="(.+?)" title="Watch (.+?) Online"><img width=".+?" height=".+?" src="(.+?)" class="attachment-post-thumbnail size-post-thumbnail wp-post-image"' ) . findall ( eevev )
 ii1ii1ii = ''
 for i11 , i1111 , I11 in VeveeeveveevV :
  i1 = '<item><meta>%s</meta><title>%s</title><link>%s</link><thumbnail>%s</thumbnail><fanart>%s</fanart></item>' % ( I1Ii , i1111 , i11 , I11 , I11 )
  ii1ii1ii = ii1ii1ii + i1
 return ii1ii1ii
 if 1 - 1: i1I1ii1II1iII
def VVeeeeVevVe ( name , url , iconimage ) :
 VevVVVevVVeVevV = name
 eevev = i1iIi ( url )
 eevVevVVVevVee = re . compile ( '<a href="(.+?)" title=".+?" rel="nofollow" target="blank">.+?</a><br/>' ) . findall ( eevev )
 VVVevevV = 1
 VevevVeeveveveeVev = [ ]
 VeVevVevev = [ ]
 for iiIiI in eevVevVVVevVee :
  IIi1IiiiI1Ii = VevevVeveVVevevVevev ( iiIiI )
  if 'http' in iiIiI : I1 = iiIiI . split ( '/' ) [ 2 ] . split ( '.' ) [ 0 ]
  else : I1 = iiIiI
  name = "Link " + str ( VVVevevV ) + ' | ' + I1 + IIi1IiiiI1Ii
  if I1 != 'www' :
   VeevVevVeveeVevV ( I1 , iiIiI , 2 , iconimage , 10 , '' , isFolder = False )
   if 91 - 91: eVev . VeVV / I1iiiiI1iII + eeveveveveVeVeVeve
   if 42 - 42: i111I1 . eVev . i111I1 - IIIi1i1I
def i1iiI11I ( name , url , iconimage , fanart , item ) :
 name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 url = re . compile ( '<lbscraper>(.+?)</lbscraper>' ) . findall ( item ) [ 0 ]
 fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
 eeevev ( name , url , 10 , iconimage , fanart )
 if 40 - 40: i111I1 - i11iIiiIii / I111I11
def I11iiI1i1 ( name , url , iconimage , fanart ) :
 VeeveVVe = I1i1Iiiii ( name , url , iconimage )
 eeveVeVeveve = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( VeeveVVe )
 for i1 in eeveVeVeveve :
  VVeVeveve ( name , url , iconimage , fanart , i1 )
  if 94 - 94: eVev * I111I11 / I1111 / I111I11
def I1i1Iiiii ( name , url , iconimage ) :
 eVevVVeeevVV = url
 eVevVevVVevV = ''
 if url == 'mamahd' :
  eevev = VevevVVVeVeeevV ( "http://mamahd.com" ) . replace ( '\n' , '' ) . replace ( '\t' , '' )
  VV = re . compile ( '<div class="schedule">(.+?)<br><div id="pagination">' ) . findall ( eevev ) [ 0 ]
  VeVeV = re . compile ( '<a href="(.+?)">.+?<img src="(.+?)"></div>.+?<div class="home cell">.+?<span>(.+?)</span>.+?<span>(.+?)</span>.+?</a>' ) . findall ( VV )
  for url , iconimage , Ii1I1i , VVI1iI1ii1II in VeVeV :
   eVevVevVVevV = eVevVevVVevV + '<item>\n<title>%s vs %s</title>\n<sportsdevil>%s</sportsdevil>\n<thumbnail>%s</thumbnail>\n<fanart>fanart</fanart>\n</item>\n\n' % ( Ii1I1i , VVI1iI1ii1II , url , iconimage )
  return eVevVevVVevV
  if 57 - 57: iIiI1I11 % I111I11 + eVev - I1111
 elif url == 'cricfree' :
  eevev = VevevVVVeVeeevV ( "http://cricfree.sc/football-live-stream" )
  eevV = re . compile ( '<td><span class="sport-icon(.+?)</tr>' , re . DOTALL ) . findall ( eevev )
  for IiI1i in eevV :
   eevVeevev = re . compile ( '<td>(.+?)<br(.+?)</td>' ) . findall ( IiI1i )
   for iIVevVevVeeeeve , iIII1 in eevVeevev :
    iIVevVevVeeeeve = '[COLOR red]' + iIVevVevVeeeeve + '[/COLOR]'
    iIII1 = iIII1 . replace ( '>' , '' )
   eeve = re . compile ( '<td class="matchtime" style="color:#545454;font-weight:bold;font-size: 9px">(.+?)</td>' ) . findall ( IiI1i ) [ 0 ]
   eeve = '[COLOR white](' + eeve + ')[/COLOR]'
   eVVeeevevVeveve = re . compile ( '<a style="text-decoration:none !important;color:#545454;" href="(.+?)" target="_blank">(.+?)</a></td>' ) . findall ( IiI1i )
   for url , VevVevevVe in eVVeeevevVeveve :
    url = url
    VevVevevVe = VevVevevVe
   eVevVevVVevV = eVevVevVVevV + '\n<item>\n<title>%s</title>\n<sportsdevil>%s</sportsdevil>\n' % ( iIVevVevVeeeeve + ' ' + eeve + ' - ' + VevVevevVe , url )
   eVevVevVVevV = eVevVevVVevV + '<thumbnail>iconimage</thumbnail>\n<fanart>fanart</fanart>\n</item>\n'
  return eVevVevVVevV
  if 97 - 97: Ii1I * VeVVeveeVVeeevV . VeVVeveeVVeeevV
 elif url == 'bigsports' :
  eevev = VevevVVVeVeeevV ( "http://www.bigsports.me/cat/4/football-live-stream.html" )
  VeVeV = re . compile ( '<td>.+?<td>(.+?)\-(.+?)\-(.+?)</td>.+?<td>(.+?)\:(.+?)</td>.+?<td>Football</td>.+?<td><strong>(.+?)</strong></td>.+?<a target=.+? href=(.+?) class=.+?' , re . DOTALL ) . findall ( eevev )
  for iIVevVevVeeeeve , I111iI , eVVeevII1I1iiIII , eVVeevVeveve , iIiIi11 , name , url in VeVeV :
   if not '</td>' in iIVevVevVeeeeve :
    url = url . replace ( '"' , '' )
    iIII1 = iIVevVevVeeeeve + ' ' + I111iI + ' ' + eVVeevII1I1iiIII
    eeve = eVVeevVeveve + ':' + iIiIi11
    iIII1 = '[COLOR red]' + iIII1 + '[/COLOR]'
    eeve = '[COLOR white](' + eeve + ')[/COLOR]'
    eVevVevVVevV = eVevVevVVevV + '\n<item>\n<title>%s</title>\n<sportsdevil>%s</sportsdevil>\n' % ( iIII1 + ' ' + eeve + ' ' + name , url )
    eVevVevVVevV = eVevVevVVevV + '<thumbnail>iconimage</thumbnail>\n<fanart>fanart</fanart>\n</item>\n'
  return eVevVevVVevV
  if 87 - 87: I1111 . eeeVeveeeveVVVV - i1I1ii1II1iII + Ii1I / I1111 / I1iiiiI1iII
def eVeveevVevVVVeeev ( name , url , iconimage , fanart , item ) :
 name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 IiIIIIii1I = re . compile ( '<oktitle>(.+?)</oktitle>' ) . findall ( item ) [ 0 ]
 eeVevVV = re . compile ( '<line1>(.+?)</line1>' ) . findall ( item ) [ 0 ]
 VevevevVVV = re . compile ( '<line2>(.+?)</line2>' ) . findall ( item ) [ 0 ]
 IIeeveevVevVeveveVVe = re . compile ( '<line3>(.+?)</line3>' ) . findall ( item ) [ 0 ]
 iIIIiIi = '##' + IiIIIIii1I + '#' + eeVevVV + '#' + VevevevVVV + '#' + IIeeveevVevVeveveVVe + '##'
 iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
 iii11I111 ( name , iIIIiIi , 17 , iconimage , fanart )
 if 100 - 100: eeeVeveeeveVVVV / eVev % i1I1ii1II1iII % I1111 % eVeev
def VeveveVevevevVevV ( name , url ) :
 I1i1i1iii = re . compile ( '##(.+?)##' ) . findall ( url ) [ 0 ] . split ( '#' )
 I1111i = xbmcgui . Dialog ( )
 I1111i . ok ( I1i1i1iii [ 0 ] , I1i1i1iii [ 1 ] , I1i1i1iii [ 2 ] , I1i1i1iii [ 3 ] )
 if 14 - 14: eVeev / eVev
def iiii ( name , url , iconimage , fanart , item ) :
 url = re . compile ( '<redirect>(.+?)</redirect>' ) . findall ( item ) [ 0 ]
 II ( 'name' , url , 'iconimage' , 'fanart' )
 if 32 - 32: eeeVeveeeveVVVV * I1111
def eeveV ( name , url , iconimage , fanart , item ) :
 name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 iIIIiIi = re . compile ( '<text>(.+?)</text>' ) . findall ( item ) [ 0 ]
 iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
 iii11I111 ( name , iIIIiIi , 9 , iconimage , fanart )
 if 78 - 78: eVeev - VeVVeveeVVeeevV - IIIi1i1I / i111I1 / i1I1ii1II1iII
def iiI11ii1I1 ( name , url ) :
 VeeevVVeVeVev = i1iIi ( url )
 eVeevVVeVev ( name , VeeevVVeVeVev )
 if 11 - 11: IIIi1i1I . eeveevVeeveeeeev * Ii1 * VeVVeveeVVeeevV + i111I1
def eeveeeveevVevevVV ( name , url , iconimage , fanart , item ) :
 IiII111i1i11 = re . compile ( '<image>(.+?)</image>' ) . findall ( item )
 if len ( IiII111i1i11 ) == 1 :
  name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  i111iIi1i1II1 = re . compile ( '<image>(.+?)</image>' ) . findall ( item ) [ 0 ]
  fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
  iii11I111 ( name , i111iIi1i1II1 , 7 , iconimage , fanart )
 elif len ( IiII111i1i11 ) > 1 :
  name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
  eeeV = ''
  for i111iIi1i1II1 in IiII111i1i11 : eeeV = eeeV + '<image>' + i111iIi1i1II1 + '</image>'
  i1I1i111Ii = VeevV
  name = VVeeV ( name )
  eee = os . path . join ( os . path . join ( i1I1i111Ii , '' ) , name + '.txt' )
  if not os . path . exists ( eee ) : file ( eee , 'w' ) . close ( )
  i1i1iI1iiiI = open ( eee , "w" )
  i1i1iI1iiiI . write ( eeeV )
  i1i1iI1iiiI . close ( )
  iii11I111 ( name , 'image' , 8 , iconimage , fanart )
  if 51 - 51: eeeVeveeeveVVVV % iIiI1I11 . I1iiiiI1iII / VeVV / i1Ii . I1iiiiI1iII
def Ii1iIIIi1ii ( name , url , iconimage , fanart , item ) :
 name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 url = re . compile ( '<iptv>(.+?)</iptv>' ) . findall ( item ) [ 0 ]
 fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
 eeevev ( name , url , 6 , iconimage , fanart )
 if 42 - 42: eVev + eeveveveveVeVeVeve - I111I11 / Ii1
def iiIiIIIiiI ( url , iconimage ) :
 eevev = i1iIi ( url )
 iiI1IIIi = re . compile ( '^#.+?:-?[0-9]*(.*?),(.*?)\n(.*?)$' , re . I + re . M + re . U + re . S ) . findall ( eevev )
 II11IiIi11 = [ ]
 for IIVVVevVevevVevVVVV , i1111 , url in iiI1IIIi :
  I1iiii1I = { "params" : IIVVVevVevevVevVVVV , "name" : i1111 , "url" : url }
  II11IiIi11 . append ( I1iiii1I )
 list = [ ]
 for eVVV in II11IiIi11 :
  I1iiii1I = { "name" : eVVV [ "name" ] , "url" : eVVV [ "url" ] }
  iiI1IIIi = re . compile ( ' (.+?)="(.+?)"' , re . I + re . M + re . U + re . S ) . findall ( eVVV [ "params" ] )
  for VVeev , eVeveveeeeVeve in iiI1IIIi :
   I1iiii1I [ VVeev . strip ( ) . lower ( ) . replace ( '-' , '_' ) ] = eVeveveeeeVeve . strip ( )
  list . append ( I1iiii1I )
 for eVVV in list :
  if '.ts' in eVVV [ "url" ] : iii11I111 ( eVVV [ "name" ] , eVVV [ "url" ] , 2 , iconimage , eeeevVV )
  else : i1Veevev ( eVVV [ "name" ] , eVVV [ "url" ] , 2 , iconimage , eeeevVV )
  if 75 - 75: eeveveveveVeVeVeve / Ii1I * eVev
def I1I ( name , url , iconimage , fanart , item ) :
 IIi1IiiiI1Ii = ''
 IiI1iiiIii = re . compile ( '<link>(.+?)</link>' ) . findall ( item )
 eVVeeevevVevV = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>' ) . findall ( item )
 for name , I1III1111iIi , iconimage , fanart in eVVeeevevVevV :
  if 'youtube.com/playlist?' in I1III1111iIi :
   VVVVeeevVe = I1III1111iIi . split ( 'list=' ) [ 1 ]
   eeevev ( name , I1III1111iIi , I1i111I , iconimage , fanart , description = VVVVeeevVe )
 if len ( IiI1iiiIii ) == 1 :
  eVVeeevevVevV = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>' ) . findall ( item )
  for name , url , iconimage , fanart in eVVeeevevVevV :
   try :
    IIi1IiiiI1Ii = VevevVeveVVevevVevev ( url )
    Vee = url . split ( '/' ) [ 2 ] . replace ( 'www.' , '' )
    if 'SportsDevil' in url : Vee = ''
   except : pass
   if '.ts' in url : i1Veevev ( name , url , 16 , iconimage , fanart , description = '' )
   if '<meta>' in item :
    eVVeev = re . compile ( '<meta>(.+?)</meta>' ) . findall ( item ) [ 0 ]
    VeevVevVeveeVevV ( name + IIi1IiiiI1Ii , url , 2 , iconimage , 10 , eVVeev , isFolder = False )
   else :
    i1Veevev ( name + IIi1IiiiI1Ii , url , 2 , iconimage , fanart )
 elif len ( IiI1iiiIii ) > 1 :
  name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
  if '.ts' in url : i1Veevev ( name , url , 16 , iconimage , fanart , description = '' )
  if '<meta>' in item :
   eVVeev = re . compile ( '<meta>(.+?)</meta>' ) . findall ( item ) [ 0 ]
   VeevVevVeveeVevV ( name , url , 3 , iconimage , len ( IiI1iiiIii ) , eVVeev , isFolder = True )
  else :
   eeevev ( name , url , 3 , iconimage , fanart )
   if 65 - 65: Ii1I * VeVVeveeVVeeevV % eVeev / Ii1 - I111I11 / i1Ii
   if 56 - 56: eeeVeveeeveVVVV * i11iIiiIii * iIiI1I11
def Vevev ( name , url , iconimage , fanart , item ) :
 IiI1iiiIii = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( item )
 eVeVeevVevVVVeV = re . compile ( '<link>(.+?)</link>' ) . findall ( item )
 if len ( IiI1iiiIii ) + len ( eVeVeevVevVVVeV ) == 1 :
  name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  url = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( item ) [ 0 ]
  url = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' + url
  iii11I111 ( name , url , 16 , iconimage , fanart )
 elif len ( IiI1iiiIii ) + len ( eVeVeevVevVVVeV ) > 1 :
  name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  eeevev ( name , url , 3 , iconimage , fanart )
  if 50 - 50: i111I1
def Ii11iii11I ( link ) :
 if VVVeev == '' :
  I1111i = xbmcgui . Dialog ( )
  IIIIiii1IIii = I1111i . yesno ( 'Adult Content' , 'You have found the goodies ;)' , '' , 'Please set a password to prevent accidental access' , 'Cancel' , 'OK' )
  if IIIIiii1IIii == 1 :
   II1i11I = xbmc . Keyboard ( '' , 'Set Password' )
   II1i11I . doModal ( )
   if ( II1i11I . isConfirmed ( ) ) :
    ii1I1IIii11 = II1i11I . getText ( )
    VevVevVVevVevVev . setSetting ( 'password' , ii1I1IIii11 )
  else : quit ( )
 elif VVVeev <> '' :
  I1111i = xbmcgui . Dialog ( )
  IIIIiii1IIii = I1111i . yesno ( 'Adult Content' , 'Please enter the password you set!' , 'to continue' , 'dirty git!!' , 'Cancel' , 'OK' )
  if IIIIiii1IIii == 1 :
   II1i11I = xbmc . Keyboard ( '' , 'Enter Password' )
   II1i11I . doModal ( )
   if ( II1i11I . isConfirmed ( ) ) :
    ii1I1IIii11 = II1i11I . getText ( )
   if ii1I1IIii11 <> VVVeev :
    quit ( )
  else : quit ( )
  if 67 - 67: VevVeeVevVVeee + i1Ii / eVev . I1iiiiI1iII + eVeev
def eeVeVeev ( name , url , iconimage ) :
 I11iiiiI1i = ''
 iiI11 = VVeeV ( name )
 VevVevVVevVevVev . setSetting ( 'tv' , iiI11 )
 eevev = VeeveVeveee ( url )
 iI1i11 = re . compile ( '<title>.*?' + re . escape ( name ) + '.*?</title>(.+?)</item>' , re . DOTALL ) . findall ( eevev ) [ 0 ]
 iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( iI1i11 ) [ 0 ]
 IiI1iiiIii = [ ]
 if '<link>' in iI1i11 :
  VeVVeeeVVevV = re . compile ( '<link>(.+?)</link>' ) . findall ( iI1i11 )
  for eeeevevVee in VeVVeeeVVevV :
   IiI1iiiIii . append ( eeeevevVee )
 if '<sportsdevil>' in iI1i11 :
  VeeveevVevev = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( iI1i11 )
  for ii1 in VeeveevVevev :
   ii1 = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' + ii1
   IiI1iiiIii . append ( ii1 )
 VVVevevV = 1
 for eevev in IiI1iiiIii :
  if '(' in eevev :
   eevev = eevev . split ( '(' )
   I11iiiiI1i = eevev [ 1 ] . replace ( ')' , '' )
   eevev = eevev [ 0 ]
  IIi1IiiiI1Ii = VevevVeveVVevevVevev ( eevev )
  Vee = eevev . split ( '/' ) [ 2 ] . replace ( 'www.' , '' )
  if I11iiiiI1i <> '' : name = "Link " + str ( VVVevevV ) + ' | ' + I11iiiiI1i + IIi1IiiiI1Ii
  else : name = "Link " + str ( VVVevevV ) + ' | ' + Vee + IIi1IiiiI1Ii
  VVVevevV = VVVevevV + 1
  VeevVevVeveeVevV ( name , eevev , 2 , iconimage , 10 , '' , isFolder = False , description = VevVevVVevVevVev . getSetting ( 'tv' ) )
  if 39 - 39: I111I11 / i111I1 . eVev % Ii1I * VevVeeVevVVeee + eeeVeveeeveVVVV
def VevVeveveevVVVev ( name , url , iconimage , fanart , item ) :
 eVVeeevevVevV = re . compile ( '<title>(.+?)</title>.+?folder>(.+?)</folder>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>' ) . findall ( item )
 for name , url , iconimage , fanart in eVVeeevevVevV :
  if 'youtube.com/channel/' in url :
   VVVVeeevVe = url . split ( 'channel/' ) [ 1 ]
   eeevev ( name , url , I1i111I , iconimage , fanart , description = VVVVeeevVe )
  elif 'youtube.com/user/' in url :
   VVVVeeevVe = url . split ( 'user/' ) [ 1 ]
   eeevev ( name , url , I1i111I , iconimage , fanart , description = VVVVeeevVe )
  elif 'youtube.com/playlist?' in url :
   VVVVeeevVe = url . split ( 'list=' ) [ 1 ]
   eeevev ( name , url , I1i111I , iconimage , fanart , description = VVVVeeevVe )
  elif 'plugin://' in url :
   VeveeevV = HTMLParser ( )
   url = VeveeevV . unescape ( url )
   eeevev ( name , url , I1i111I , iconimage , fanart )
  else :
   eeevev ( name , url , 1 , iconimage , fanart )
   if 36 - 36: eVeev + Ii1I - I111I11 - Ii1I % i1Ii . I1iiiiI1iII
def eeeiiI ( url ) :
 II1i11I = xbmc . Keyboard ( '' , '[B][COLOR red]S[/COLOR][COLOR white]earch[/COLOR][/B] [B][COLOR red]E[/COLOR][COLOR white]volve[/COLOR][/B]' )
 II1i11I . doModal ( )
 if ( II1i11I . isConfirmed ( ) ) :
  VVVVeeevVe = II1i11I . getText ( )
  VVVVeeevVe = VVVVeeevVe . upper ( )
 else : quit ( )
 eevev = VeeveVeveee ( url )
 eeevVVeev = re . compile ( '<link>(.+?)</link>' ) . findall ( eevev )
 for url in eeevVVeev :
  try :
   eevev = VeeveVeveee ( url )
   I11IiI = re . compile ( '<item>(.+?)</item>' ) . findall ( eevev )
   for i1 in I11IiI :
    eeveVeVeveve = re . compile ( '<title>(.+?)</title>' ) . findall ( i1 )
    for VevVVVevVVeVevV in eeveVeVeveve :
     VevVVVevVVeVevV = VevVVVevVVeVevV . upper ( )
     if VVVVeeevVe in VevVVVevVVeVevV :
      VVeVeveve ( i1111 , url , I11 , eeeevVV , i1 )
  except : pass
  if 56 - 56: I1111 . IIIi1i1I . eeeVeveeeveVVVV
def ii111I ( url ) :
 eVevVevVVevV = "ShowPicture(%s)" % url
 xbmc . executebuiltin ( eVevVevVVevV )
 if 17 - 17: eeeVeveeeveVVVV . Ii1I + eeveevVeeveeeeev
def ii ( name , url , iconimage , description ) :
 if description : name = description
 try :
  if 'plugin://plugin.video.SportsDevil/' in url :
   Iiii1iI1i ( name , url , iconimage )
  elif '.ts' in url :
   url = 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;name=' + name + '&amp;url=' + url
   url = url . replace ( '|' , '' )
   Iiii1iI1i ( name , url , iconimage )
  elif urlresolver . HostedMediaFile ( url ) . valid_url ( ) :
   url = urlresolver . HostedMediaFile ( url ) . resolve ( )
   I1ii1ii11i1I ( name , url , iconimage )
  elif liveresolver . isValid ( url ) == True :
   url = liveresolver . resolve ( url )
   I1ii1ii11i1I ( name , url , iconimage )
  else : I1ii1ii11i1I ( name , url , iconimage )
 except :
  eevVeVV ( VevVevVeevev ( 'Evolve' ) , 'Stream Unavailable' , '3000' , Veveveeeeeevev )
  if 80 - 80: I1iiiiI1iII + eVeev / i1Ii
def VeveeeeevVeevev ( url ) :
 if urlresolver . HostedMediaFile ( url ) . valid_url ( ) :
  url = urlresolver . HostedMediaFile ( url ) . resolve ( )
 xbmc . Player ( ) . play ( url )
 if 79 - 79: i111I1
def I1ii1ii11i1I ( name , url , iconimage ) :
 i11I1I1I = True
 eVVVeevevVevevV = xbmcgui . ListItem ( name , iconImage = iconimage , thumbnailImage = iconimage ) ; eVVVeevevVevevV . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
 i11I1I1I = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = url , listitem = eVVVeevevVevevV )
 eVVVeevevVevevV . setPath ( url )
 xbmcplugin . setResolvedUrl ( int ( sys . argv [ 1 ] ) , True , eVVVeevevVevevV )
 if 2 - 2: eVev - IIIi1i1I
def Iiii1iI1i ( name , url , iconimage ) :
 xbmc . executebuiltin ( 'Dialog.Close(all,True)' )
 i11I1I1I = True
 eVVVeevevVevevV = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage ) ; eVVVeevevVevevV . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
 i11I1I1I = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = url , listitem = eVVVeevevVevevV )
 xbmc . Player ( ) . play ( url , eVVVeevevVevevV , False )
 if 58 - 58: I111I11 + eVev - eeeVeveeeveVVVV
def i1i1ii ( url ) :
 xbmc . executebuiltin ( "PlayMedia(%s)" % url )
 if 46 - 46: I1I1i1 + eeveevVeeveeeeev
def VeeveVeveee ( url ) :
 eeveevV = urllib2 . Request ( url )
 eeveevV . add_header ( 'User-Agent' , 'mat' )
 eeeeVeveVeVVeV = urllib2 . urlopen ( eeveevV )
 eevev = eeeeVeveVeVVeV . read ( )
 eeeeVeveVeVVeV . close ( )
 eevev = eevev . replace ( '<fanart></fanart>' , '<fanart>x</fanart>' ) . replace ( '<thumbnail></thumbnail>' , '<thumbnail>x</thumbnail>' ) . replace ( '<utube>' , '<link>https://www.youtube.com/watch?v=' ) . replace ( '</utube>' , '</link>' )
 if '{' in eevev :
  eVevVevVVevV = eevev [ : : - 1 ]
  eVevVevVVevV = eVevVevVVevV . replace ( '}' , '' ) . replace ( '{' , '' ) . replace ( ',' , '' ) . replace ( ']' , '' ) . replace ( '[' , '' )
  eVevVevVVevV = eVevVevVVevV + '=='
  eevev = eVevVevVVevV . decode ( 'base64' )
 if url <> IiIi11iIIi1Ii : eevev = eevev . replace ( '\n' , '' ) . replace ( '\r' , '' )
 print eevev
 return eevev
 if 20 - 20: i1Ii + I111I11 / Ii1I % VeVV
def i1iIi ( url ) :
 eeveevV = urllib2 . Request ( url )
 eeveevV . add_header ( 'User-Agent' , 'mat' )
 eeeeVeveVeVVeV = urllib2 . urlopen ( eeveevV )
 eevev = eeeeVeveVeVVeV . read ( )
 eeeeVeveVeVVeV . close ( )
 return eevev
 if 88 - 88: I1I1i1 / i1I1ii1II1iII
def VevevVVVeVeeevV ( url ) :
 eeveevV = urllib2 . Request ( url )
 eeveevV . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' )
 eeeeVeveVeVVeV = urllib2 . urlopen ( eeveevV )
 eevev = eeeeVeveVeVVeV . read ( )
 eeeeVeveVeVVeV . close ( )
 eevev = eevev . replace ( '\n' , '' ) . replace ( '\r' , '' )
 return eevev
 if 87 - 87: IIIi1i1I - IIIi1i1I - VevVeeVevVVeee + I1iiiiI1iII
 if 82 - 82: I1iiiiI1iII / VeVV . eeeVeveeeveVVVV . eVeev / eVev
def iiI1I1 ( ) :
 eeV = [ ]
 iiVVevVevVee = sys . argv [ 2 ]
 if len ( iiVVevVevVee ) >= 2 :
  IIVVVevVevevVevVVVV = sys . argv [ 2 ]
  eVeVev = IIVVVevVevevVevVVVV . replace ( '?' , '' )
  if ( IIVVVevVevevVevVVVV [ len ( IIVVVevVevevVevVVVV ) - 1 ] == '/' ) :
   IIVVVevVevevVevVVVV = IIVVVevVevevVevVVVV [ 0 : len ( IIVVVevVevevVevVVVV ) - 2 ]
  Veev = eVeVev . split ( '&' )
  eeV = { }
  for VVVevevV in range ( len ( Veev ) ) :
   eeevVeveeveveevV = { }
   eeevVeveeveveevV = Veev [ VVVevevV ] . split ( '=' )
   if ( len ( eeevVeveeveveevV ) ) == 2 :
    eeV [ eeevVeveeveveevV [ 0 ] ] = eeevVeveeveveevV [ 1 ]
 return eeV
 if 35 - 35: i111I1 + eeveveveveVeVeVeve % IIIi1i1I % i1Ii + I1iiiiI1iII
def eevVeVV ( title , message , ms , nart ) :
 xbmc . executebuiltin ( "XBMC.notification(" + title + "," + message + "," + ms + "," + nart + ")" )
 if 17 - 17: eeveveveveVeVeVeve
def VVeeV ( string ) :
 iiIi1i = re . compile ( '(\[.+?\])' ) . findall ( string )
 for I1i11111i1i11 in iiIi1i : string = string . replace ( I1i11111i1i11 , '' )
 return string
 if 77 - 77: IIIi1i1I + eeveevVeeveeeeev / I1iiiiI1iII + Ii1I * eVev
def VevVevVeevev ( string ) :
 string = string . split ( ' ' )
 I1ii11 = ''
 for eVeVeVeeev in string :
  III1ii1I = '[B][COLOR red]' + eVeVeVeeev [ 0 ] . upper ( ) + '[/COLOR][COLOR white]' + eVeVeVeeev [ 1 : ] + '[/COLOR][/B] '
  I1ii11 = I1ii11 + III1ii1I
 return I1ii11
 if 13 - 13: i11iIiiIii + eeveveveveVeVeVeve * VeVV % VeVVeveeVVeeevV - i1I1ii1II1iII * eVeev
def VeevVevVeveeVevV ( name , url , mode , iconimage , itemcount , metatype , isFolder = False , description = '' ) :
 if isFolder == True : VevVevVVevVevVev . setSetting ( 'favtype' , 'folder' )
 else : VevVevVVevVevVev . setSetting ( 'favtype' , 'link' )
 if Veeeeveveve == 'true' :
  iiIi1iI1iIii = name
  name = VVeeV ( name )
  eevevVeeVevee = ""
  eeveeveVeVVevV = ""
  i1ii1II1ii = [ ]
  iII111Ii = eval ( base64 . b64decode ( 'bWV0YWhhbmRsZXJzLk1ldGFEYXRhKHRtZGJfYXBpX2tleT0iZDk1NWQ4ZjAyYTNmMjQ4MGE1MTg4MWZlNGM5NmYxMGUiKQ==' ) )
  iIii111IIi = { }
  if metatype == 'movie' :
   IIiII = name . partition ( '(' )
   if len ( IIiII ) > 0 :
    eevevVeeVevee = IIiII [ 0 ]
    eeveeveVeVVevV = IIiII [ 2 ] . partition ( ')' )
   if len ( eeveeveVeVVevV ) > 0 :
    eeveeveVeVVevV = eeveeveVeVVevV [ 0 ]
   iIii111IIi = iII111Ii . get_meta ( 'movie' , name = eevevVeeVevee , year = eeveeveVeVVevV )
   if not iIii111IIi [ 'trailer' ] == '' : i1ii1II1ii . append ( ( VevVevVeevev ( 'Play Trailer' ) , 'XBMC.RunPlugin(%s)' % VeevVee . build_plugin_url ( { 'mode' : 11 , 'url' : iIii111IIi [ 'trailer' ] } ) ) )
  elif metatype == 'tvep' :
   VevVVVevVVeVevV = VevVevVVevVevVev . getSetting ( 'tv' )
   if '<>' in url :
    print url
    VeevVeVeveveVVeve = url . split ( '<>' ) [ 0 ]
    i1i1i11IIi = url . split ( '<>' ) [ 1 ]
    II1III = url . split ( '<>' ) [ 2 ]
    iI1iI1I1i1I = url . split ( '<>' ) [ 3 ]
    iIi11Ii1 = url . split ( '<>' ) [ 4 ]
    Ii11iII1 = url . split ( '<>' ) [ 5 ]
    iIii111IIi = iII111Ii . get_episode_meta ( i1i1i11IIi , imdb_id = VeevVeVeveveVVeve , season = II1III , episode = iI1iI1I1i1I , air_date = '' , episode_title = '' , overlay = '' )
    print iIii111IIi
   else :
    VeeevevVeVVV = re . compile ( 'Season (.+?) Episode (.+?)\)' ) . findall ( name )
    for VeevVVeveveveveeee , IIII1iII in VeeevevVeVVV :
     iIii111IIi = iII111Ii . get_episode_meta ( VevVVVevVVeVevV , imdb_id = '' , season = VeevVVeveveveveeee , episode = IIII1iII , air_date = '' , episode_title = '' , overlay = '' )
  ii1III11 = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&fanart=" + urllib . quote_plus ( eeeevVV ) + "&iconimage=" + urllib . quote_plus ( iconimage )
  i11I1I1I = True
  eVVVeevevVevevV = xbmcgui . ListItem ( iiIi1iI1iIii , iconImage = iconimage , thumbnailImage = iconimage )
  eVVVeevevVevevV . setInfo ( type = "Video" , infoLabels = iIii111IIi )
  eVVVeevevVevevV . setProperty ( "IsPlayable" , "true" )
  eVVVeevevVevevV . addContextMenuItems ( i1ii1II1ii , replaceItems = False )
  if not iIii111IIi . get ( 'backdrop_url' , '' ) == '' : eVVVeevevVevevV . setProperty ( 'fanart_image' , iIii111IIi [ 'backdrop_url' ] )
  else : eVVVeevevVevevV . setProperty ( 'fanart_image' , eeeevVV )
  eVVVeevevVevevV . setProperty ( iIii111IIi . get ( 'cover_url' , iconimage ) , iconimage )
  I1iiIIIi11 = VevVevVVevVevVev . getSetting ( 'favlist' )
  Ii1I11ii1i = [ ]
  Ii1I11ii1i . append ( ( VevVevVeevev ( 'Stream Information' ) , 'XBMC.Action(Info)' ) )
  if I1iiIIIi11 == 'yes' : Ii1I11ii1i . append ( ( '[COLOR white]Remove from Evolve Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=21&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
  else : Ii1I11ii1i . append ( ( '[COLOR white]Add to Evolve Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=20&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
  eVVVeevevVevevV . addContextMenuItems ( Ii1I11ii1i , replaceItems = False )
  i11I1I1I = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = ii1III11 , listitem = eVVVeevevVevevV , isFolder = isFolder , totalItems = itemcount )
  return i11I1I1I
 else :
  if isFolder :
   eeevev ( name , url , mode , iconimage , eeeevVV , description = '' )
  else :
   i1Veevev ( name , url , mode , iconimage , eeeevVV , description = '' )
   if 89 - 89: VevVeeVevVVeee . Ii1I / IIIi1i1I % I1I1i1 . I1111
def eeevev ( name , url , mode , iconimage , fanart , description = '' ) :
 VevVevVVevVevVev . setSetting ( 'favtype' , 'folder' )
 ii1III11 = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&fanart=" + urllib . quote_plus ( fanart ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 i11I1I1I = True
 eVVVeevevVevevV = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 eVVVeevevVevevV . setInfo ( type = "Video" , infoLabels = { "Title" : name , 'plot' : description } )
 eVVVeevevVevevV . setProperty ( 'fanart_image' , fanart )
 if 'youtube.com/channel/' in url :
  ii1III11 = 'plugin://plugin.video.youtube/channel/' + description + '/'
 if 'youtube.com/user/' in url :
  ii1III11 = 'plugin://plugin.video.youtube/user/' + description + '/'
 if 'youtube.com/playlist?' in url :
  ii1III11 = 'plugin://plugin.video.youtube/playlist/' + description + '/'
 if 'plugin://' in url :
  ii1III11 = url
 Ii1I11ii1i = [ ]
 I1iiIIIi11 = VevVevVVevVevVev . getSetting ( 'favlist' )
 if I1iiIIIi11 == 'yes' : Ii1I11ii1i . append ( ( '[COLOR white]Remove from Evolve Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=21&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 else : Ii1I11ii1i . append ( ( '[COLOR white]Add to Evolve Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=20&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 eVVVeevevVevevV . addContextMenuItems ( Ii1I11ii1i , replaceItems = False )
 i11I1I1I = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = ii1III11 , listitem = eVVVeevevVevevV , isFolder = True )
 return i11I1I1I
 if 50 - 50: i1I1ii1II1iII + IIIi1i1I . eeveveveveVeVeVeve % eVev
def iii11I111 ( name , url , mode , iconimage , fanart , description = '' ) :
 VevVevVVevVevVev . setSetting ( 'favtype' , 'link' )
 ii1III11 = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&fanart=" + urllib . quote_plus ( fanart ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 i11I1I1I = True
 eVVVeevevVevevV = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 eVVVeevevVevevV . setProperty ( 'fanart_image' , fanart )
 Ii1I11ii1i = [ ]
 I1iiIIIi11 = VevVevVVevVevVev . getSetting ( 'favlist' )
 if I1iiIIIi11 == 'yes' : Ii1I11ii1i . append ( ( '[COLOR white]Remove from Evolve Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=21&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 else : Ii1I11ii1i . append ( ( '[COLOR white]Add to Evolve Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=20&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 eVVVeevevVevevV . addContextMenuItems ( Ii1I11ii1i , replaceItems = False )
 i11I1I1I = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = ii1III11 , listitem = eVVVeevevVevevV , isFolder = False )
 return i11I1I1I
 if 5 - 5: I1I1i1 / VeVVeveeVVeeevV + Ii1 * iIiI1I11 - eeveevVeeveeeeev % eeeVeveeeveVVVV
def i1Veevev ( name , url , mode , iconimage , fanart , description = '' ) :
 VevVevVVevVevVev . setSetting ( 'favtype' , 'link' )
 ii1III11 = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&fanart=" + urllib . quote_plus ( fanart ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 i11I1I1I = True
 eVVVeevevVevevV = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 eVVVeevevVevevV . setProperty ( 'fanart_image' , fanart )
 eVVVeevevVevevV . setProperty ( "IsPlayable" , "true" )
 Ii1I11ii1i = [ ]
 I1iiIIIi11 = VevVevVVevVevVev . getSetting ( 'favlist' )
 if I1iiIIIi11 == 'yes' : Ii1I11ii1i . append ( ( '[COLOR white]Remove from Evolve Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=21&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 else : Ii1I11ii1i . append ( ( '[COLOR white]Add to Evolve Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=20&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 eVVVeevevVevevV . addContextMenuItems ( Ii1I11ii1i , replaceItems = False )
 i11I1I1I = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = ii1III11 , listitem = eVVVeevevVevevV , isFolder = False )
 return i11I1I1I
 if 42 - 42: Ii1I / eVev + VeVVeveeVVeeevV * i111I1 % i111I1
def eeveVev ( url , name ) :
 i1iIiIIIII = i1iIi ( url )
 if len ( i1iIiIIIII ) > 1 :
  i1I1i111Ii = VeevV
  eee = os . path . join ( os . path . join ( i1I1i111Ii , '' ) , name + '.txt' )
  if not os . path . exists ( eee ) :
   file ( eee , 'w' ) . close ( )
  eeveeVeVeveveveV = open ( eee )
  VVe = eeveeVeVeveveveV . read ( )
  if VVe == i1iIiIIIII : pass
  else :
   eVeevVVeVev ( '[B][COLOR red]E[/COLOR][COLOR white]volve[/COLOR][/B] [B][COLOR red]I[/COLOR][COLOR white]nformation[/COLOR][/B]' , i1iIiIIIII )
   i1i1iI1iiiI = open ( eee , "w" )
   i1i1iI1iiiI . write ( i1iIiIIIII )
   i1i1iI1iiiI . close ( )
   if 50 - 50: i111I1
def eVeevVVeVev ( heading , text ) :
 id = 10147
 xbmc . executebuiltin ( 'ActivateWindow(%d)' % id )
 xbmc . sleep ( 500 )
 eevVevVeveeeeveVV = xbmcgui . Window ( id )
 eeevevev = 50
 while ( eeevevev > 0 ) :
  try :
   xbmc . sleep ( 10 )
   eeevevev -= 1
   eevVevVeveeeeveVV . getControl ( 1 ) . setLabel ( heading )
   eevVevVeveeeeveVV . getControl ( 5 ) . setText ( text )
   return
  except :
   pass
   if 32 - 32: eeveveveveVeVeVeve . I111I11
def eVV ( name ) :
 global Icon
 global Next
 global Previous
 global window
 global Quit
 global images
 eee = os . path . join ( os . path . join ( VeevV , '' ) , name + '.txt' )
 eeveeVeVeveveveV = open ( eee )
 VVe = eeveeVeVeveveveV . read ( )
 images = re . compile ( '<image>(.+?)</image>' ) . findall ( VVe )
 VevVevVVevVevVev . setSetting ( 'pos' , '0' )
 window = pyxbmct . AddonDialogWindow ( '' )
 Veee = '/resources/art'
 I1i1iiiII1i = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + VVeve + Veee , 'next_focus.png' ) )
 eVeveVev = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + VVeve + Veee , 'next1.png' ) )
 i1i1IIIIi1i = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + VVeve + Veee , 'previous_focus.png' ) )
 Ii11iiI = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + VVeve + Veee , 'previous.png' ) )
 IIi1iiii1iI = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + VVeve + Veee , 'close_focus.png' ) )
 iIiiii = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + VVeve + Veee , 'close.png' ) )
 VevevevevVVVev = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + VVeve + Veee , 'main-bg1.png' ) )
 window . setGeometry ( 1300 , 720 , 100 , 50 )
 eeeev = pyxbmct . Image ( VevevevevVVVev )
 window . placeControl ( eeeev , - 10 , - 10 , 130 , 70 )
 iIIIiIi = '0xFF000000'
 Previous = pyxbmct . Button ( '' , focusTexture = i1i1IIIIi1i , noFocusTexture = Ii11iiI , textColor = iIIIiIi , focusedColor = iIIIiIi )
 Next = pyxbmct . Button ( '' , focusTexture = I1i1iiiII1i , noFocusTexture = eVeveVev , textColor = iIIIiIi , focusedColor = iIIIiIi )
 Quit = pyxbmct . Button ( '' , focusTexture = IIi1iiii1iI , noFocusTexture = iIiiii , textColor = iIIIiIi , focusedColor = iIIIiIi )
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
 if 70 - 70: i1Ii . IIIi1i1I * VeVVeveeVVeeevV - Ii1 * eeeVeveeeveVVVV + I1I1i1
def VeveveVev ( ) :
 iIi1 = int ( VevVevVVevVevVev . getSetting ( 'pos' ) )
 i11iiI1111 = int ( iIi1 ) + 1
 VevVevVVevVevVev . setSetting ( 'pos' , str ( i11iiI1111 ) )
 eVeeeeevevevVeevev = len ( images )
 Icon . setImage ( images [ int ( i11iiI1111 ) ] )
 Previous . setVisible ( True )
 if int ( i11iiI1111 ) == int ( eVeeeeevevevVeevev ) - 1 :
  Next . setVisible ( False )
  if 93 - 93: IIIi1i1I / eeeVeveeeveVVVV / VeVV % iIiI1I11 % iIiI1I11
def eVeveveveVeeveveeve ( ) :
 iIi1 = int ( VevVevVVevVevVev . getSetting ( 'pos' ) )
 IiI11iI1i1i1i = int ( iIi1 ) - 1
 VevVevVVevVevVev . setSetting ( 'pos' , str ( IiI11iI1i1i1i ) )
 Icon . setImage ( images [ int ( IiI11iI1i1i1i ) ] )
 Next . setVisible ( True )
 if int ( IiI11iI1i1i1i ) == 0 :
  Previous . setVisible ( False )
  if 89 - 89: i1Ii
def Veeeeee ( url , fanart ) :
 VevVevVVevVevVev . setSetting ( 'favlist' , 'yes' )
 I1IIIiI1I1ii1 = None
 file = open ( IiI , 'r' )
 I1IIIiI1I1ii1 = file . read ( ) . replace ( '\n' , '' ) . replace ( '\r' , '' )
 eeveVeVeveve = re . compile ( "<item>(.+?)</item>" , re . DOTALL ) . findall ( I1IIIiI1I1ii1 )
 for i1 in eeveVeVeveve :
  VVeVeveve ( i1111 , url , Veveveeeeeevev , fanart , i1 )
 VevVevVVevVevVev . setSetting ( 'favlist' , 'no' )
 if 30 - 30: Ii1I * VeVVeveeVVeeevV
def I1iIIIi1 ( name , url , iconimage , fanart ) :
 Iii = VevVevVVevVevVev . getSetting ( 'favtype' )
 url = url . replace ( ' ' , '%20' )
 iconimage = iconimage . replace ( ' ' , '%20' )
 if '<>' in url :
  VeevVeVeveveVVeve = url . split ( '<>' ) [ 0 ]
  II1III = url . split ( '<>' ) [ 1 ]
  iI1iI1I1i1I = url . split ( '<>' ) [ 2 ]
  iIi11Ii1 = url . split ( '<>' ) [ 3 ]
  Ii11iII1 = url . split ( '<>' ) [ 4 ]
  eVevVevVVevV = '<FAV><item>\n<title>' + name + '</title>\n<meta>tvep</meta>\n<nan>tvshow</nan>\n<showyear>' + iIi11Ii1 + '</showyear>\n<imdb>' + VeevVeVeveveVVeve + '</imdb>\n<season>' + II1III + '</season>\n<episode>' + iI1iI1I1i1I + '</episode>\n<episodeyear>' + Ii11iII1 + '</episodeyear>\n<thumbnail>' + iconimage + '</thumbnail>\n<fanart>' + fanart + '</fanart></item></FAV>\n'
 elif len ( url ) == 9 :
  eVevVevVVevV = '<FAV><item>\n<title>' + name + '</title>\n<meta>movie</meta>\n<nan>movie</nan>\n<imdb>' + url + '</imdb>\n' + '<thumbnail>' + iconimage + '</thumbnail>\n<fanart>' + fanart + '</fanart></item></FAV>\n'
 else :
  eVevVevVVevV = '<FAV><item>\n<title>' + name + '</title>\n<' + Iii + '>' + url + '</' + Iii + '>\n' + '<thumbnail>' + iconimage + '</thumbnail>\n<fanart>' + fanart + '</fanart></item></FAV>\n'
 eeVe = open ( IiI , 'a' )
 eeVe . write ( eVevVevVVevV )
 eeVe . close ( )
 if 19 - 19: i1Ii % i1I1ii1II1iII / i11iIiiIii / VevVeeVevVVeee - VeVVeveeVVeeevV
def iIIii ( name , url , iconimage ) :
 print name
 I1IIIiI1I1ii1 = None
 file = open ( IiI , 'r' )
 I1IIIiI1I1ii1 = file . read ( )
 i1iIiIi1I = ''
 eeveVeVeveve = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( I1IIIiI1I1ii1 )
 for eVVeeevevVevV in eeveVeVeveve :
  eVevVevVVevV = '\n<FAV><item>\n' + eVVeeevevVevV + '</item>\n'
  if name in eVVeeevevVevV :
   print 'xxxxxxxxxxxxxxxxx'
   eVevVevVVevV = eVevVevVVevV . replace ( 'item' , ' ' )
  i1iIiIi1I = i1iIiIi1I + eVevVevVVevV
 file = open ( IiI , 'w' )
 file . truncate ( )
 file . write ( i1iIiIi1I )
 file . close ( )
 xbmc . executebuiltin ( 'Container.Refresh' )
 if 45 - 45: eeveveveveVeVeVeve + i1I1ii1II1iII
def VevevVeveVVevevVevev ( url ) :
 try :
  Vee = url . split ( '/' ) [ 2 ] . replace ( 'www.' , '' )
  file = open ( IIi1IiiiI1Ii , 'r' )
  IiII1II11I = file . read ( )
  if Vee in IiII1II11I : return '[COLOR springgreen] (RD)[/COLOR]'
  else : return ''
 except : return ''
 if 54 - 54: Ii1 + Ii1I + i1Ii * iIiI1I11 - eVeev % I1iiiiI1iII
def I111 ( ) :
 import xbmcaddon
 xbmcaddon . Addon ( 'script.module.nanscrapers' ) . openSettings ( )
 if 13 - 13: eeveevVeeveeeeev * I1iiiiI1iII * VevVeeVevVVeee
def iI ( link ) :
 try :
  IiIIiiI11III = re . compile ( '<layouttype>(.+?)</layouttype>' ) . findall ( link ) [ 0 ]
  if IiIIiiI11III == 'thumbnail' : xbmc . executebuiltin ( 'Container.SetViewMode(500)' )
  else : xbmc . executebuiltin ( 'Container.SetViewMode(50)' )
 except : pass
 if 42 - 42: IIIi1i1I
 if 76 - 76: IIIi1i1I * i1I1ii1II1iII . eeeVeveeeveVVVV - I1111 + I1iiiiI1iII + i11iIiiIii
IIVVVevVevevVevVVVV = iiI1I1 ( ) ; i11 = None ; i1111 = None ; I1i111I = None ; i1i1ii111 = None ; I11 = None ; IiI1ieVeveVVeeevevevevev = None
try : i1i1ii111 = urllib . unquote_plus ( IIVVVevVevevVevVVVV [ "site" ] )
except : pass
try : i11 = urllib . unquote_plus ( IIVVVevVevevVevVVVV [ "url" ] )
except : pass
try : i1111 = urllib . unquote_plus ( IIVVVevVevevVevVVVV [ "name" ] )
except : pass
try : I1i111I = int ( IIVVVevVevevVevVVVV [ "mode" ] )
except : pass
try : I11 = urllib . unquote_plus ( IIVVVevVevevVevVVVV [ "iconimage" ] )
except : pass
try : eeeevVV = urllib . unquote_plus ( IIVVVevVevevVevVVVV [ "fanart" ] )
except : pass
try : IiI1ieVeveVVeeevevevevev = str ( IIVVVevVevevVevVVVV [ "description" ] )
except : pass
if 52 - 52: eeeVeveeeveVVVV
if I1i111I == None or i11 == None or len ( i11 ) < 1 : VeveV ( )
elif I1i111I == 1 : II ( i1111 , i11 , I11 , eeeevVV )
elif I1i111I == 2 : ii ( i1111 , i11 , I11 , IiI1ieVeveVVeeevevevevev )
elif I1i111I == 3 : eeVeVeev ( i1111 , i11 , I11 )
elif I1i111I == 4 : I1ii1ii11i1I ( i1111 , i11 , I11 )
elif I1i111I == 5 : eeeiiI ( i11 )
elif I1i111I == 6 : iiIiIIIiiI ( i11 , I11 )
elif I1i111I == 7 : ii111I ( i11 )
elif I1i111I == 8 : eVV ( i1111 )
elif I1i111I == 9 : iiI11ii1I1 ( i1111 , i11 )
elif I1i111I == 10 : I11iiI1i1 ( i1111 , i11 , I11 , eeeevVV )
elif I1i111I == 11 : i1i1ii ( i11 )
elif I1i111I == 15 : VVeeeeVevVe ( i1111 , i11 , I11 )
elif I1i111I == 16 : Iiii1iI1i ( i1111 , i11 , I11 )
elif I1i111I == 17 : VeveveVevevevVevV ( i1111 , i11 )
elif I1i111I == 18 : VVeveVeVVeveVVev ( i1111 , i11 , I11 , eeeevVV )
elif I1i111I == 19 : eeevevevVVevevVe ( i1111 , i11 , I11 , eeeevVV )
if 51 - 51: Ii1
elif I1i111I == 20 : I1iIIIi1 ( i1111 , i11 , I11 , eeeevVV )
elif I1i111I == 21 : iIIii ( i1111 , i11 , I11 )
elif I1i111I == 22 : Veeeeee ( i11 , eeeevVV )
elif I1i111I == 23 : DOIPLAYER ( i1111 , i11 , I11 , eeeevVV )
elif I1i111I == 24 : eeveveeeVevVe ( i1111 , i11 , I11 , eeeevVV )
elif I1i111I == 25 : I111 ( )
if 88 - 88: VeVVeveeVVeeevV
elif I1i111I == 26 : VVeVeeevevee ( i1111 , i11 , I11 , eeeevVV )
elif I1i111I == 27 : eVeV ( i1111 , i11 , I11 , eeeevVV )
elif I1i111I == 28 : ii1ii11IIIiiI ( i1111 , i11 , I11 , eeeevVV )
elif I1i111I == 29 : VeeeVeveV ( i1111 , i11 , I11 , eeeevVV )
elif I1i111I == 30 : eVe ( i1111 , i11 , I11 , eeeevVV )
elif I1i111I == 31 : iii ( i1111 , i11 , I11 , eeeevVV )
elif I1i111I == 32 : eeeeevVev ( i1111 , i11 , I11 , eeeevVV )
elif I1i111I == 33 : eeveVevevevevev ( i11 )
if 84 - 84: I1I1i1 / i1Ii * VevVeeVevVVeee / I1iiiiI1iII - i11iIiiIii . I1111
if 60 - 60: IIIi1i1I * eeeVeveeeveVVVV
if 17 - 17: eVeev % I1111 / IIIi1i1I . Ii1 * eVeev - i1I1ii1II1iII
if 41 - 41: I111I11
if 77 - 77: iIiI1I11
if 65 - 65: i1I1ii1II1iII . eeeVeveeeveVVVV % I1iiiiI1iII * eeveevVeeveeeeev
if 38 - 38: I1I1i1 / VevVeeVevVVeee % I1111
xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3
