import xbmc , xbmcaddon , xbmcgui , xbmcplugin , requests , urllib , urllib2 , os , re , sys , datetime , urlresolver , random , liveresolver , base64 , pyxbmct
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
 eeevev ( '[B][COLOR red]M[/COLOR][COLOR white]ovies[/COLOR][/B]' , 'http://matsbuilds.uk/EvolveMenus/Movies/Mainmenu.xml' , 27 , 'http://i.imgur.com/x6BAZUe.png' , II1 )
 eeevev ( '[B][COLOR blue]TV[/COLOR]  [COLOR blue]S[/COLOR][COLOR white]hows[/COLOR][/B]' , 'http://matsbuilds.uk/EvolveMenus/TvShows/Mainmenu.xml' , 28 , 'http://i.imgur.com/SLdxQL6.png' , II1 )
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
 eeevev ( '[B][COLOR red]MOVIE SEARCH[/COLOR][/B]' , 'http://matsbuilds.uk/EvolveMenus/Movies/Search/Search.txt' , 5 , 'http://i.imgur.com/gLWo9QO.png' , II1 )
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
 eeevev ( '[B][COLOR blue]TV SEARCH[/COLOR][/B]' , 'http://matsbuilds.uk/EvolveMenus/TvShows/Search/Search.txt' , 5 , 'http://i.imgur.com/gLWo9QO.png' , fanarts )
 eeevev ( '[B][COLOR yellow]TV SCHEDULE[/COLOR][/B]' , 'http://www.tvwise.co.uk/uk-premiere-dates/' , 34 , 'http://i.imgur.com/Pq53Nxh.png' , fanarts )
 eeevev ( '[B][COLOR blue]Latest[/COLOR] [COLOR white]Episodes[/COLOR][/B]' , 'http://www.watchepisodes4.com' , 29 , 'http://i.imgur.com/gLWo9QO.png' , fanarts )
 eeevev ( '[B][COLOR blue]Popular[/COLOR] [COLOR white]Shows[/COLOR][/B]' , 'http://www.watchepisodes4.com/home/popular-series' , 31 , 'http://i.imgur.com/SHXfj1a.png' , fanarts )
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
  eeevev ( name , url , 26 , iconimage , iconimage )
  if 71 - 71: i11iIiiIii + Ii1
def eVe ( name , url , iconimage , fanart ) :
 eevev = VevevVVVeVeeevV ( url )
 VevevevVVeevevee = re . compile ( '<div class="cb-first">.+?<a href="(.+?)" class="c-image"><img alt=".+?" title="(.+?)" src="(.+?)"></a>' , re . DOTALL ) . findall ( eevev )
 for url , name , iconimage in VevevevVVeevevee :
  name = name . replace ( "&#39;" , "'" )
  eeevev ( name , url , 32 , iconimage , iconimage )
  if 75 - 75: eeeVeveeeveVVVV + I1111
def VeeeVeveV ( name , url , iconimage , fanart ) :
 eevev = i1iIi ( url )
 VevevevVVeevevee = re . compile ( '<a href="(.+?)" class="c-image"><img alt=".+?" title="(.+?)" src="(.+?)"></a>' , ) . findall ( eevev )
 for url , name , iconimage in VevevevVVeevevee :
  iconimage = iconimage . replace ( "('" , "" ) . replace ( "')" , "" )
  name = name . replace ( "&#39;" , "'" )
  eeevev ( name , url , 33 , iconimage , fanart )
  if 68 - 68: i11iIiiIii % IIIi1i1I + i11iIiiIii
def iii ( name , url , iconimage , fanart ) :
 eevev = VevevVVVeVeeevV ( url )
 eeveVeVeveve = re . compile ( '<a title=".+?" href="(.+?)">.+?<div class="season">(.+?)</div>.+?<div class="episode">(.+?)</div>.+?<div class="e-name">(.+?)</div>' , re . DOTALL ) . findall ( eevev )
 for url , II1III , iI1iI1I1i1I , II1I in eeveVeVeveve :
  II1I = II1I . replace ( "&#39;" , "'" ) . replace ( '&amp;' , ' & ' )
  if '</div>' in II1I : II1I = ''
  eeevev ( '%s ' % II1I + '(%s ' % II1III + '%s)' % iI1iI1I1i1I , url , 24 , iconimage , fanart )
  if 84 - 84: Ii1 . i11iIiiIii . Ii1 * IIIi1i1I - i1Ii
def ii ( name , url , iconimage , fanart ) :
 eevev = VevevVVVeVeeevV ( url )
 eeveVeVeveve = re . compile ( '<a title=".+?" href="(.+?)">.+?<div class="season">(.+?)</div>.+?<div class="episode">(.+?)</div>.+?<div class="e-name">(.+?)</div>' ) . findall ( eevev )
 for url , II1III , iI1iI1I1i1I , II1I in eeveVeVeveve :
  II1I = II1I . replace ( "&#39;" , "'" ) . replace ( '&amp;' , ' & ' )
  if '</div>' in II1I : II1I = ''
  eeevev ( '%s ' % II1I + '(%s ' % II1III + '%s)' % iI1iI1I1i1I , url , 24 , iconimage , fanart )
  if 81 - 81: iIiI1I11 % VevVeeVevVVeee . IIIi1i1I / eVev
def iiiIiI ( name , url , iconimage , fanart ) :
 VevVVVevVVeVevV = name
 eevev = i1iIi ( url )
 eeveveeeVevVe = re . compile ( '<a target="_blank" href=".+?" data-episodeid=".+?" data-linkid=".+?" data-hostname=".+?" class="watch-button" data-actuallink="(.+?)">Watch Now!</a>' ) . findall ( eevev )
 VVVevevV = 1
 VevevVeeveveveeVev = [ ]
 VeVevVevev = [ ]
 for eevVevVVVevVee in eeveveeeVevVe :
  IIi1IiiiI1Ii = VevevVeveVVevevVevev ( eevVevVVVevVee )
  if 'http' in eevVevVVVevVee : iiIiI = eevVevVVVevVee . split ( '/' ) [ 2 ] . split ( '.' ) [ 0 ]
  else : iiIiI = eevVevVVVevVee
  name = "Link " + str ( VVVevevV ) + ' | ' + iiIiI + IIi1IiiiI1Ii
  if iiIiI != 'www' :
   i1Veevev ( iiIiI , eevVevVVVevVee , 2 , iconimage , fanart , description = '' )
   if 6 - 6: Ii1 . I1iiiiI1iII * I1I1i1 - I111I11 - Ii1
def IiIiii1I1 ( name , url , iconiamge , fanart ) :
 eevev = i1iIi ( url )
 VevevevVVeevevee = re . compile ( '<td height="20">(.+?)</td>.+?<td>(.+?)</td>.+?<td><a href=".+?">(.+?)</a></td>.+?<td><a href=".+?">(.+?)</a></td>.+?</tr>' , re . DOTALL ) . findall ( eevev )
 for eVVV , name , iIII1 , eeve in VevevevVVeevevee :
  name = name . replace ( "&#8217;" , "'" ) . replace ( '&amp;' , ' & ' )
  eeevev ( '[COLOR yellow]%s[/COLOR] - ' % iIII1 + '[COLOR blue]%s[/COLOR] ' % name + '- [COLOR white]%s[/COLOR]' % eVVV , url , 5 , I11 , fanart )
  if 73 - 73: Ii1 * IIIi1i1I + eeeVeveeeveVVVV . i111I1
  if 70 - 70: iIiI1I11 - I1111 / I111I11
  if 82 - 82: i1Ii % eVev % eeveevVeeveeeeev - I1111 + VeVVeveeVVeeevV
def eeeeeVeeeveee ( ) :
 Iiii1i1 = 'movie'
 eevev = i1iIi ( 'http://newmoviesonline.ws/' )
 VV = re . compile ( '<a href="(.+?)" title="Watch (.+?) Online"><img width=".+?" height=".+?" src="(.+?)" class="attachment-post-thumbnail size-post-thumbnail wp-post-image"' ) . findall ( eevev )
 ii1ii1ii = ''
 for i11 , i1111 , I11 in VV :
  i1 = '<item><meta>%s</meta><title>%s</title><link>%s</link><thumbnail>%s</thumbnail><fanart>%s</fanart></item>' % ( Iiii1i1 , i1111 , i11 , I11 , I11 )
  ii1ii1ii = ii1ii1ii + i1
 return ii1ii1ii
 if 77 - 77: I1111
def I1iII1iIi1I ( name , url , iconimage ) :
 VevVVVevVVeVevV = name
 eevev = i1iIi ( url )
 eeveveeeVevVe = re . compile ( '<a href="(.+?)" title=".+?" rel="nofollow" target="blank">.+?</a><br/>' ) . findall ( eevev )
 VVVevevV = 1
 VevevVeeveveveeVev = [ ]
 VeVevVevev = [ ]
 for eevVevVVVevVee in eeveveeeVevVe :
  IIi1IiiiI1Ii = VevevVeveVVevevVevev ( eevVevVVVevVee )
  if 'http' in eevVevVVVevVee : iiIiI = eevVevVVVevVee . split ( '/' ) [ 2 ] . split ( '.' ) [ 0 ]
  else : iiIiI = eevVevVVVevVee
  name = "Link " + str ( VVVevevV ) + ' | ' + iiIiI + IIi1IiiiI1Ii
  if iiIiI != 'www' :
   VeevVevVeveeVevV ( iiIiI , eevVevVVVevVee , 2 , iconimage , 10 , '' , isFolder = False )
   if 54 - 54: I1I1i1 % VevVeeVevVVeee
   if 37 - 37: I1I1i1 * I1111 / i111I1 - VevVeeVevVVeee % i1I1ii1II1iII . I1iiiiI1iII
def i1iiI11I ( name , url , iconimage , fanart , item ) :
 name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 url = re . compile ( '<lbscraper>(.+?)</lbscraper>' ) . findall ( item ) [ 0 ]
 fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
 eeevev ( name , url , 10 , iconimage , fanart )
 if 88 - 88: VevVeeVevVVeee . i1I1ii1II1iII * i1I1ii1II1iII % iIiI1I11
def iiIIiiIi1Ii11 ( name , url , iconimage , fanart ) :
 VeeveVVe = Veev ( name , url , iconimage )
 eeveVeVeveve = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( VeeveVVe )
 for i1 in eeveVeVeveve :
  VVeVeveve ( name , url , iconimage , fanart , i1 )
  if 70 - 70: i1Ii
def Veev ( name , url , iconimage ) :
 eVevVVeeevVV = url
 iiVVeeeeVevVe = ''
 if url == 'mamahd' :
  eevev = VevevVVVeVeeevV ( "http://mamahd.com" ) . replace ( '\n' , '' ) . replace ( '\t' , '' )
  VViIiIIi1 = re . compile ( '<div class="schedule">(.+?)<br><div id="pagination">' ) . findall ( eevev ) [ 0 ]
  I1IIII1i = re . compile ( '<a href="(.+?)">.+?<img src="(.+?)"></div>.+?<div class="home cell">.+?<span>(.+?)</span>.+?<span>(.+?)</span>.+?</a>' ) . findall ( VViIiIIi1 )
  for url , iconimage , I1I11i , Ii1I1I1i1Ii in I1IIII1i :
   iiVVeeeeVevVe = iiVVeeeeVevVe + '<item>\n<title>%s vs %s</title>\n<sportsdevil>%s</sportsdevil>\n<thumbnail>%s</thumbnail>\n<fanart>fanart</fanart>\n</item>\n\n' % ( I1I11i , Ii1I1I1i1Ii , url , iconimage )
  return iiVVeeeeVevVe
  if 5 - 5: iIiI1I11 . eVev
 elif url == 'cricfree' :
  eevev = VevevVVVeVeeevV ( "http://cricfree.sc/football-live-stream" )
  VeveVev = re . compile ( '<td><span class="sport-icon(.+?)</tr>' , re . DOTALL ) . findall ( eevev )
  for eVevVevVVevV in VeveVev :
   VVVeVeV = re . compile ( '<td>(.+?)<br(.+?)</td>' ) . findall ( eVevVevVVevV )
   for Ii1I1i , iIII1 in VVVeVeV :
    Ii1I1i = '[COLOR red]' + Ii1I1i + '[/COLOR]'
    iIII1 = iIII1 . replace ( '>' , '' )
   eeve = re . compile ( '<td class="matchtime" style="color:#545454;font-weight:bold;font-size: 9px">(.+?)</td>' ) . findall ( eVevVevVVevV ) [ 0 ]
   eeve = '[COLOR white](' + eeve + ')[/COLOR]'
   VVI1iI1ii1II = re . compile ( '<a style="text-decoration:none !important;color:#545454;" href="(.+?)" target="_blank">(.+?)</a></td>' ) . findall ( eVevVevVVevV )
   for url , VevVevVVVVee in VVI1iI1ii1II :
    url = url
    VevVevVVVVee = VevVevVVVVee
   iiVVeeeeVevVe = iiVVeeeeVevVe + '\n<item>\n<title>%s</title>\n<sportsdevil>%s</sportsdevil>\n' % ( Ii1I1i + ' ' + eeve + ' - ' + VevVevVVVVee , url )
   iiVVeeeeVevVe = iiVVeeeeVevVe + '<thumbnail>iconimage</thumbnail>\n<fanart>fanart</fanart>\n</item>\n'
  return iiVVeeeeVevVe
  if 74 - 74: IIIi1i1I + i1I1ii1II1iII / eeveevVeeveeeeev
 elif url == 'bigsports' :
  eevev = VevevVVVeVeeevV ( "http://www.bigsports.me/cat/4/football-live-stream.html" )
  I1IIII1i = re . compile ( '<td>.+?<td>(.+?)\-(.+?)\-(.+?)</td>.+?<td>(.+?)\:(.+?)</td>.+?<td>Football</td>.+?<td><strong>(.+?)</strong></td>.+?<a target=.+? href=(.+?) class=.+?' , re . DOTALL ) . findall ( eevev )
  for Ii1I1i , eVeevVevVeeveveV , I111I1Iiii1i , eVVeeevevVeveve , VevVevevVe , name , url in I1IIII1i :
   if not '</td>' in Ii1I1i :
    url = url . replace ( '"' , '' )
    iIII1 = Ii1I1i + ' ' + eVeevVevVeeveveV + ' ' + I111I1Iiii1i
    eeve = eVVeeevevVeveve + ':' + VevVevevVe
    iIII1 = '[COLOR red]' + iIII1 + '[/COLOR]'
    eeve = '[COLOR white](' + eeve + ')[/COLOR]'
    iiVVeeeeVevVe = iiVVeeeeVevVe + '\n<item>\n<title>%s</title>\n<sportsdevil>%s</sportsdevil>\n' % ( iIII1 + ' ' + eeve + ' ' + name , url )
    iiVVeeeeVevVe = iiVVeeeeVevVe + '<thumbnail>iconimage</thumbnail>\n<fanart>fanart</fanart>\n</item>\n'
  return iiVVeeeeVevVe
  if 97 - 97: Ii1I * VeVVeveeVVeeevV . VeVVeveeVVeeevV
def eVeveevVevVVVeeev ( name , url , iconimage , fanart , item ) :
 name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 I111iI = re . compile ( '<oktitle>(.+?)</oktitle>' ) . findall ( item ) [ 0 ]
 eVVeevII1I1iiIII = re . compile ( '<line1>(.+?)</line1>' ) . findall ( item ) [ 0 ]
 eVVeevVeveve = re . compile ( '<line2>(.+?)</line2>' ) . findall ( item ) [ 0 ]
 iIiIi11 = re . compile ( '<line3>(.+?)</line3>' ) . findall ( item ) [ 0 ]
 VVV = '##' + I111iI + '#' + eVVeevII1I1iiIII + '#' + eVVeevVeveve + '#' + iIiIi11 + '##'
 iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
 iii11I111 ( name , VVV , 17 , iconimage , fanart )
 if 32 - 32: eeveveveveVeVeVeve / i1I1ii1II1iII . I1111
def eeeVeevVVVeeev ( name , url ) :
 VVeV = re . compile ( '##(.+?)##' ) . findall ( url ) [ 0 ] . split ( '#' )
 VVevVevevev = xbmcgui . Dialog ( )
 VVevVevevev . ok ( VVeV [ 0 ] , VVeV [ 1 ] , VVeV [ 2 ] , VVeV [ 3 ] )
 if 37 - 37: VeVVeveeVVeeevV - Ii1I - eVev
def iiii ( name , url , iconimage , fanart , item ) :
 url = re . compile ( '<redirect>(.+?)</redirect>' ) . findall ( item ) [ 0 ]
 II ( 'name' , url , 'iconimage' , 'fanart' )
 if 77 - 77: eVeev * VeVV
def eeveV ( name , url , iconimage , fanart , item ) :
 name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 VVV = re . compile ( '<text>(.+?)</text>' ) . findall ( item ) [ 0 ]
 iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
 iii11I111 ( name , VVV , 9 , iconimage , fanart )
 if 98 - 98: eeeVeveeeveVVVV % I111I11 * VeVVeveeVVeeevV
def Ve ( name , url ) :
 iIIiIi1 = i1iIi ( url )
 eevVeveev ( name , iIIiIi1 )
 if 37 - 37: IIIi1i1I * i1Ii % i11iIiiIii % i111I1 + I111I11
def eeveeeveevVevevVV ( name , url , iconimage , fanart , item ) :
 VVeVVeveeveev = re . compile ( '<image>(.+?)</image>' ) . findall ( item )
 if len ( VVeVVeveeveev ) == 1 :
  name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  ii1I1 = re . compile ( '<image>(.+?)</image>' ) . findall ( item ) [ 0 ]
  fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
  iii11I111 ( name , ii1I1 , 7 , iconimage , fanart )
 elif len ( VVeVVeveeveev ) > 1 :
  name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
  VeeeeVVeeev = ''
  for ii1I1 in VVeVVeveeveev : VeeeeVVeeev = VeeeeVVeeev + '<image>' + ii1I1 + '</image>'
  i1I1IiiIi1i = VeevV
  name = VVeeV ( name )
  iiI11ii1I1 = os . path . join ( os . path . join ( i1I1IiiIi1i , '' ) , name + '.txt' )
  if not os . path . exists ( iiI11ii1I1 ) : file ( iiI11ii1I1 , 'w' ) . close ( )
  VeeevVVeVeVev = open ( iiI11ii1I1 , "w" )
  VeeevVVeVeVev . write ( VeeeeVVeeev )
  VeeevVVeVeVev . close ( )
  iii11I111 ( name , 'image' , 8 , iconimage , fanart )
  if 70 - 70: I1iiiiI1iII
def Ii1iIIIi1ii ( name , url , iconimage , fanart , item ) :
 name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 url = re . compile ( '<iptv>(.+?)</iptv>' ) . findall ( item ) [ 0 ]
 fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
 eeevev ( name , url , 6 , iconimage , fanart )
 if 59 - 59: eVev % I1iiiiI1iII
def ii1iI1I11I ( url , iconimage ) :
 eevev = i1iIi ( url )
 II1iI = re . compile ( '^#.+?:-?[0-9]*(.*?),(.*?)\n(.*?)$' , re . I + re . M + re . U + re . S ) . findall ( eevev )
 VeveeveevevVVevevevev = [ ]
 for I1i , i1111 , url in II1iI :
  VevevVeee = { "params" : I1i , "name" : i1111 , "url" : url }
  VeveeveevevVVevevevev . append ( VevevVeee )
 list = [ ]
 for eVVV in VeveeveevevVVevevevev :
  VevevVeee = { "name" : eVVV [ "name" ] , "url" : eVVV [ "url" ] }
  II1iI = re . compile ( ' (.+?)="(.+?)"' , re . I + re . M + re . U + re . S ) . findall ( eVVV [ "params" ] )
  for i11I , eevevVeeveeeeee in II1iI :
   VevevVeee [ i11I . strip ( ) . lower ( ) . replace ( '-' , '_' ) ] = eevevVeeveeeeee . strip ( )
  list . append ( VevevVeee )
 for eVVV in list :
  if '.ts' in eVVV [ "url" ] : iii11I111 ( eVVV [ "name" ] , eVVV [ "url" ] , 2 , iconimage , eeeevVV )
  else : i1Veevev ( eVVV [ "name" ] , eVVV [ "url" ] , 2 , iconimage , eeeevVV )
  if 76 - 76: i1Ii / eVeev . Ii1I % eeeVeveeeveVVVV . eVev + Ii1
def I1I ( name , url , iconimage , fanart , item ) :
 IIi1IiiiI1Ii = ''
 eeveeeev = re . compile ( '<link>(.+?)</link>' ) . findall ( item )
 eVVeeevevVevV = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>' ) . findall ( item )
 for name , eVVVeeevev , iconimage , fanart in eVVeeevevVevV :
  if 'youtube.com/playlist?' in eVVVeeevev :
   iiIiIIIiiI = eVVVeeevev . split ( 'list=' ) [ 1 ]
   eeevev ( name , eVVVeeevev , iiI1IIIi , iconimage , fanart , description = iiIiIIIiiI )
 if len ( eeveeeev ) == 1 :
  eVVeeevevVevV = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>' ) . findall ( item )
  for name , url , iconimage , fanart in eVVeeevevVevV :
   try :
    IIi1IiiiI1Ii = VevevVeveVVevevVevev ( url )
    II11IiIi11 = url . split ( '/' ) [ 2 ] . replace ( 'www.' , '' )
    if 'SportsDevil' in url : II11IiIi11 = ''
   except : pass
   if '.ts' in url : iii11I111 ( name , url , 16 , iconimage , fanart , description = '' )
   if '<meta>' in item :
    eVVeev = re . compile ( '<meta>(.+?)</meta>' ) . findall ( item ) [ 0 ]
    VeevVevVeveeVevV ( name + IIi1IiiiI1Ii , url , 2 , iconimage , 10 , eVVeev , isFolder = False )
   else :
    i1Veevev ( name + IIi1IiiiI1Ii , url , 2 , iconimage , fanart )
 elif len ( eeveeeev ) > 1 :
  name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
  if '.ts' in url : iii11I111 ( name , url , 16 , iconimage , fanart , description = '' )
  if '<meta>' in item :
   eVVeev = re . compile ( '<meta>(.+?)</meta>' ) . findall ( item ) [ 0 ]
   VeevVevVeveeVevV ( name , url , 3 , iconimage , len ( eeveeeev ) , eVVeev , isFolder = True )
  else :
   eeevev ( name , url , 3 , iconimage , fanart )
   if 7 - 7: eeveevVeeveeeeev . I111I11 % I1iiiiI1iII * i111I1 + Ii1 + iIiI1I11
   if 38 - 38: eVev - eeeVeveeeveVVVV - eVev / i1Ii - eeveveveveVeVeVeve
def Vevev ( name , url , iconimage , fanart , item ) :
 eeveeeev = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( item )
 i1II1 = re . compile ( '<link>(.+?)</link>' ) . findall ( item )
 if len ( eeveeeev ) + len ( i1II1 ) == 1 :
  name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  url = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( item ) [ 0 ]
  url = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' + url
  iii11I111 ( name , url , 16 , iconimage , fanart )
 elif len ( eeveeeev ) + len ( i1II1 ) > 1 :
  name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  eeevev ( name , url , 3 , iconimage , fanart )
  if 25 - 25: iIiI1I11 / VeVV % VevVeeVevVVeee
def Ii11iii11I ( link ) :
 if VVVeev == '' :
  VVevVevevev = xbmcgui . Dialog ( )
  IiiiiI1i1Iii = VVevVevevev . yesno ( 'Adult Content' , 'You have found the goodies ;)' , '' , 'Please set a password to prevent accidental access' , 'Cancel' , 'OK' )
  if IiiiiI1i1Iii == 1 :
   eeeveveVeve = xbmc . Keyboard ( '' , 'Set Password' )
   eeeveveVeve . doModal ( )
   if ( eeeveveVeve . isConfirmed ( ) ) :
    iiii111II = eeeveveVeve . getText ( )
    VevVevVVevVevVev . setSetting ( 'password' , iiii111II )
  else : quit ( )
 elif VVVeev <> '' :
  VVevVevevev = xbmcgui . Dialog ( )
  IiiiiI1i1Iii = VVevVevevev . yesno ( 'Adult Content' , 'Please enter the password you set! dirty git' , 'to continue' , '' , 'Cancel' , 'OK' )
  if IiiiiI1i1Iii == 1 :
   eeeveveVeve = xbmc . Keyboard ( '' , 'Enter Password' )
   eeeveveVeve . doModal ( )
   if ( eeeveveVeve . isConfirmed ( ) ) :
    iiii111II = eeeveveVeve . getText ( )
   if iiii111II <> VVVeev :
    quit ( )
  else : quit ( )
  if 50 - 50: eVeev * eeeVeveeeveVVVV % VeVV + I111I11 + VevVeeVevVVeee + eeeVeveeeveVVVV
def VVevVeeeVeveveev ( name , url , iconimage ) :
 iI1i11II1i = ''
 iiI11 = VVeeV ( name )
 VevVevVVevVevVev . setSetting ( 'tv' , iiI11 )
 eevev = VeeveVeveee ( url )
 eeveevVeVeevVevVV = re . compile ( '<title>.*?' + re . escape ( name ) + '.*?</title>(.+?)</item>' , re . DOTALL ) . findall ( eevev ) [ 0 ]
 iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( eeveevVeVeevVevVV ) [ 0 ]
 eeveeeev = [ ]
 if '<link>' in eeveevVeVeevVevVV :
  iIi1I11I = re . compile ( '<link>(.+?)</link>' ) . findall ( eeveevVeVeevVevVV )
  for Iii1 in iIi1I11I :
   eeveeeev . append ( Iii1 )
 if '<sportsdevil>' in eeveevVeVeevVevVV :
  eeV = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( eeveevVeVeevVevVV )
  for eeveevevVVeev in eeV :
   eeveevevVVeev = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' + eeveevevVVeev
   eeveeeev . append ( eeveevevVVeev )
 VVVevevV = 1
 for eevev in eeveeeev :
  if '(' in eevev :
   eevev = eevev . split ( '(' )
   iI1i11II1i = eevev [ 1 ] . replace ( ')' , '' )
   eevev = eevev [ 0 ]
  IIi1IiiiI1Ii = VevevVeveVVevevVevev ( eevev )
  II11IiIi11 = eevev . split ( '/' ) [ 2 ] . replace ( 'www.' , '' )
  if iI1i11II1i <> '' : name = "Link " + str ( VVVevevV ) + ' | ' + iI1i11II1i + IIi1IiiiI1Ii
  else : name = "Link " + str ( VVVevevV ) + ' | ' + II11IiIi11 + IIi1IiiiI1Ii
  VVVevevV = VVVevevV + 1
  VeevVevVeveeVevV ( name , eevev , 2 , iconimage , 10 , '' , isFolder = False , description = VevVevVVevVevVev . getSetting ( 'tv' ) )
  if 17 - 17: iIiI1I11 + I1iiiiI1iII - i11iIiiIii . iIiI1I11 * eVeev
def VevVeveveevVVVev ( name , url , iconimage , fanart , item ) :
 eVVeeevevVevV = re . compile ( '<title>(.+?)</title>.+?folder>(.+?)</folder>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>' ) . findall ( item )
 for name , url , iconimage , fanart in eVVeeevevVevV :
  if 'youtube.com/channel/' in url :
   iiIiIIIiiI = url . split ( 'channel/' ) [ 1 ]
   eeevev ( name , url , iiI1IIIi , iconimage , fanart , description = iiIiIIIiiI )
  elif 'youtube.com/user/' in url :
   iiIiIIIiiI = url . split ( 'user/' ) [ 1 ]
   eeevev ( name , url , iiI1IIIi , iconimage , fanart , description = iiIiIIIiiI )
  elif 'youtube.com/playlist?' in url :
   iiIiIIIiiI = url . split ( 'list=' ) [ 1 ]
   eeevev ( name , url , iiI1IIIi , iconimage , fanart , description = iiIiIIIiiI )
  elif 'plugin://' in url :
   eeeveVVVevVVVe = HTMLParser ( )
   url = eeeveVVVevVVVe . unescape ( url )
   eeevev ( name , url , iiI1IIIi , iconimage , fanart )
  else :
   eeevev ( name , url , 1 , iconimage , fanart )
   if 56 - 56: eVev
def I1 ( url ) :
 eeeveveVeve = xbmc . Keyboard ( '' , '[B][COLOR red]S[/COLOR][COLOR white]earch[/COLOR][/B] [B][COLOR red]E[/COLOR][COLOR white]volve[/COLOR][/B]' )
 eeeveveVeve . doModal ( )
 if ( eeeveveVeve . isConfirmed ( ) ) :
  iiIiIIIiiI = eeeveveVeve . getText ( )
  iiIiIIIiiI = iiIiIIIiiI . upper ( )
 else : quit ( )
 eevev = VeeveVeveee ( url )
 VeeeeVeveVVVV = re . compile ( '<link>(.+?)</link>' ) . findall ( eevev )
 for url in VeeeeVeveVVVV :
  try :
   eevev = VeeveVeveee ( url )
   eevVeveveVVee = re . compile ( '<item>(.+?)</item>' ) . findall ( eevev )
   for i1 in eevVeveveVVee :
    eeveVeVeveve = re . compile ( '<title>(.+?)</title>' ) . findall ( i1 )
    for VevVVVevVVeVevV in eeveVeVeveve :
     VevVVVevVVeVevV = VevVVVevVVeVevV . upper ( )
     if iiIiIIIiiI in VevVVVevVVeVevV :
      VVeVeveve ( i1111 , url , I11 , eeeevVV , i1 )
  except : pass
  if 18 - 18: I111I11 + Ii1 - Ii1I
def eevevV ( url ) :
 iiVVeeeeVevVe = "ShowPicture(%s)" % url
 xbmc . executebuiltin ( iiVVeeeeVevVe )
 if 5 - 5: iIiI1I11
def VevI11Iiii1I ( name , url , iconimage , description ) :
 if description : name = description
 try :
  if 'plugin://plugin.video.SportsDevil/' in url :
   eeevevVeveVevVev ( name , url , iconimage )
  elif '.ts' in url :
   url = 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;name=' + name + '&amp;url=' + url
   eeevevVeveVevVev ( name , url , iconimage )
  elif urlresolver . HostedMediaFile ( url ) . valid_url ( ) :
   url = urlresolver . HostedMediaFile ( url ) . resolve ( )
   eeeevVVevVevVe ( name , url , iconimage )
  elif liveresolver . isValid ( url ) == True :
   url = liveresolver . resolve ( url )
   eeeevVVevVevVe ( name , url , iconimage )
  else : eeeevVVevVevVe ( name , url , iconimage )
 except :
  VeeevVeveeee ( iiI ( 'Evolve' ) , 'Stream Unavailable' , '3000' , Veveveeeeeevev )
  if 56 - 56: I1111 . IIIi1i1I . eeeVeveeeveVVVV
def VeveeeeevVeevev ( url ) :
 if urlresolver . HostedMediaFile ( url ) . valid_url ( ) :
  url = urlresolver . HostedMediaFile ( url ) . resolve ( )
 xbmc . Player ( ) . play ( url )
 if 39 - 39: Ii1I + iIiI1I11
def eeeevVVevVevVe ( name , url , iconimage ) :
 VeVeeVeV = True
 iiIiii1iI1i = xbmcgui . ListItem ( name , iconImage = iconimage , thumbnailImage = iconimage ) ; iiIiii1iI1i . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
 VeVeeVeV = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = url , listitem = iiIiii1iI1i )
 iiIiii1iI1i . setPath ( url )
 xbmcplugin . setResolvedUrl ( int ( sys . argv [ 1 ] ) , True , iiIiii1iI1i )
 if 34 - 34: i111I1 * eeeVeveeeveVVVV . eeveveveveVeVeVeve * i111I1 / i111I1
def eeevevVeveVevVev ( name , url , iconimage ) :
 VeVeeVeV = True
 iiIiii1iI1i = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage ) ; iiIiii1iI1i . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
 VeVeeVeV = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = url , listitem = iiIiii1iI1i )
 xbmc . Player ( ) . play ( url , iiIiii1iI1i , False )
 if 30 - 30: IIIi1i1I + I1111 / I1111 % IIIi1i1I . IIIi1i1I
def VevVevVeevev ( url ) :
 xbmc . executebuiltin ( "PlayMedia(%s)" % url )
 if 80 - 80: I1iiiiI1iII + eVeev / i1Ii
def VeeveVeveee ( url ) :
 eVVVevevVevVevVVe = urllib2 . Request ( url )
 eVVVevevVevVevVVe . add_header ( 'User-Agent' , 'mat' )
 VVeevevV = urllib2 . urlopen ( eVVVevevVevVevVVe )
 eevev = VVeevevV . read ( )
 VVeevevV . close ( )
 eevev = eevev . replace ( '<fanart></fanart>' , '<fanart>x</fanart>' ) . replace ( '<thumbnail></thumbnail>' , '<thumbnail>x</thumbnail>' ) . replace ( '<utube>' , '<link>https://www.youtube.com/watch?v=' ) . replace ( '</utube>' , '</link>' )
 if '{' in eevev :
  iiVVeeeeVevVe = eevev [ : : - 1 ]
  iiVVeeeeVevVe = iiVVeeeeVevVe . replace ( '}' , '' ) . replace ( '{' , '' ) . replace ( ',' , '' ) . replace ( ']' , '' ) . replace ( '[' , '' )
  iiVVeeeeVevVe = iiVVeeeeVevVe + '=='
  eevev = iiVVeeeeVevVe . decode ( 'base64' )
 if url <> IiIi11iIIi1Ii : eevev = eevev . replace ( '\n' , '' ) . replace ( '\r' , '' )
 print eevev
 return eevev
 if 76 - 76: i11iIiiIii + eVev / IIIi1i1I - eeveevVeeveeeeev - I111I11 + IIIi1i1I
def i1iIi ( url ) :
 eVVVevevVevVevVVe = urllib2 . Request ( url )
 eVVVevevVevVevVVe . add_header ( 'User-Agent' , 'mat' )
 VVeevevV = urllib2 . urlopen ( eVVVevevVevVevVVe )
 eevev = VVeevevV . read ( )
 VVeevevV . close ( )
 return eevev
 if 51 - 51: VeVV . i111I1 + VeVV
def VevevVVVeVeeevV ( url ) :
 eVVVevevVevVevVVe = urllib2 . Request ( url )
 eVVVevevVevVevVVe . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' )
 VVeevevV = urllib2 . urlopen ( eVVVevevVevVevVVe )
 eevev = VVeevevV . read ( )
 VVeevevV . close ( )
 eevev = eevev . replace ( '\n' , '' ) . replace ( '\r' , '' )
 return eevev
 if 95 - 95: eeeVeveeeveVVVV
 if 46 - 46: I1I1i1 + eeveevVeeveeeeev
def eeveevV ( ) :
 eeeeVeveVeVVeV = [ ]
 I1i11i = sys . argv [ 2 ]
 if len ( I1i11i ) >= 2 :
  I1i = sys . argv [ 2 ]
  IiIi = I1i . replace ( '?' , '' )
  if ( I1i [ len ( I1i ) - 1 ] == '/' ) :
   I1i = I1i [ 0 : len ( I1i ) - 2 ]
  VVVVVevVevev = IiIi . split ( '&' )
  eeeeVeveVeVVeV = { }
  for VVVevevV in range ( len ( VVVVVevVevev ) ) :
   Iii = { }
   Iii = VVVVVevVevev [ VVVevevV ] . split ( '=' )
   if ( len ( Iii ) ) == 2 :
    eeeeVeveVeVVeV [ Iii [ 0 ] ] = Iii [ 1 ]
 return eeeeVeveVeVVeV
 if 31 - 31: eVev % eeveevVeeveeeeev
def VeeevVeveeee ( title , message , ms , nart ) :
 xbmc . executebuiltin ( "XBMC.notification(" + title + "," + message + "," + ms + "," + nart + ")" )
 if 14 - 14: I1iiiiI1iII / I1iiiiI1iII % i111I1
def VVeeV ( string ) :
 eeVii = re . compile ( '\[(.+?)\]' ) . findall ( string )
 for VVevVevVee in eeVii : string = string . replace ( VVevVevVee , '' ) . replace ( '[/]' , '' ) . replace ( '[]' , '' )
 return string
 if 77 - 77: eVev / VeVVeveeVVeeevV
def iiI ( string ) :
 string = string . split ( ' ' )
 IIii11I1i1I = ''
 for eeveevVVevVeveve in string :
  VevVeee = '[B][COLOR red]' + eeveevVVevVeveve [ 0 ] . upper ( ) + '[/COLOR][COLOR white]' + eeveevVVevVeveve [ 1 : ] + '[/COLOR][/B] '
  IIii11I1i1I = IIii11I1i1I + VevVeee
 return IIii11I1i1I
 if 21 - 21: I1111
def VeevVevVeveeVevV ( name , url , mode , iconimage , itemcount , metatype , isFolder = False , description = '' ) :
 if isFolder == True : VevVevVVevVevVev . setSetting ( 'favtype' , 'folder' )
 else : VevVevVVevVevVev . setSetting ( 'favtype' , 'link' )
 if Veeeeveveve == 'true' :
  I1ii1 = name
  name = VVeeV ( name )
  VevevVeeveevevevevVVeV = ""
  IiIi1I1ii111 = ""
  IiIiIi = [ ]
  IIIII1 = eval ( base64 . b64decode ( 'bWV0YWhhbmRsZXJzLk1ldGFEYXRhKHRtZGJfYXBpX2tleT0iZDk1NWQ4ZjAyYTNmMjQ4MGE1MTg4MWZlNGM5NmYxMGUiKQ==' ) )
  iIii111IIi = { }
  if metatype == 'movie' :
   IIiII = name . partition ( '(' )
   if len ( IIiII ) > 0 :
    VevevVeeveevevevevVVeV = IIiII [ 0 ]
    IiIi1I1ii111 = IIiII [ 2 ] . partition ( ')' )
   if len ( IiIi1I1ii111 ) > 0 :
    IiIi1I1ii111 = IiIi1I1ii111 [ 0 ]
   iIii111IIi = IIIII1 . get_meta ( 'movie' , name = VevevVeeveevevevevVVeV , year = IiIi1I1ii111 )
   if not iIii111IIi [ 'trailer' ] == '' : IiIiIi . append ( ( iiI ( 'Play Trailer' ) , 'XBMC.RunPlugin(%s)' % VeevVee . build_plugin_url ( { 'mode' : 11 , 'url' : iIii111IIi [ 'trailer' ] } ) ) )
  elif metatype == 'tvep' :
   VevVVVevVVeVevV = VevVevVVevVevVev . getSetting ( 'tv' )
   if '<>' in url :
    VeevVeVeveveVVeve = url . split ( '<>' ) [ 0 ]
    i1i1i11IIi = url . split ( '<>' ) [ 1 ]
    II1III = url . split ( '<>' ) [ 2 ]
    iI1iI1I1i1I = url . split ( '<>' ) [ 3 ]
    iIi11Ii1 = url . split ( '<>' ) [ 4 ]
    Ii11iII1 = url . split ( '<>' ) [ 5 ]
    iIii111IIi = IIIII1 . get_episode_meta ( i1i1i11IIi , imdb_id = VeevVeVeveveVVeve , season = II1III , episode = iI1iI1I1i1I , air_date = '' , episode_title = '' , overlay = '' )
    print iIii111IIi
   else :
    iIi1Ii1i1iI = re . compile ( 'Season (.+?) Episode (.+?)\)' ) . findall ( name )
    for IIiI1 , i1iI1 in iIi1Ii1i1iI :
     iIii111IIi = IIIII1 . get_episode_meta ( VevVVVevVVeVevV , imdb_id = '' , season = IIiI1 , episode = i1iI1 , air_date = '' , episode_title = '' , overlay = '' )
  ii1 = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&fanart=" + urllib . quote_plus ( eeeevVV ) + "&iconimage=" + urllib . quote_plus ( iconimage )
  VeVeeVeV = True
  iiIiii1iI1i = xbmcgui . ListItem ( I1ii1 , iconImage = iconimage , thumbnailImage = iconimage )
  iiIiii1iI1i . setInfo ( type = "Video" , infoLabels = iIii111IIi )
  iiIiii1iI1i . setProperty ( "IsPlayable" , "true" )
  iiIiii1iI1i . addContextMenuItems ( IiIiIi , replaceItems = False )
  if not iIii111IIi . get ( 'backdrop_url' , '' ) == '' : iiIiii1iI1i . setProperty ( 'fanart_image' , iIii111IIi [ 'backdrop_url' ] )
  else : iiIiii1iI1i . setProperty ( 'fanart_image' , eeeevVV )
  iiIiii1iI1i . setProperty ( iIii111IIi . get ( 'cover_url' , iconimage ) , iconimage )
  I1IiiI1ii1i = VevVevVVevVevVev . getSetting ( 'favlist' )
  Veve = [ ]
  Veve . append ( ( iiI ( 'Stream Information' ) , 'XBMC.Action(Info)' ) )
  if I1IiiI1ii1i == 'yes' : Veve . append ( ( '[COLOR white]Remove from Evolve Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=21&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
  else : Veve . append ( ( '[COLOR white]Add to Evolve Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=20&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
  iiIiii1iI1i . addContextMenuItems ( Veve , replaceItems = False )
  VeVeeVeV = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = ii1 , listitem = iiIiii1iI1i , isFolder = isFolder , totalItems = itemcount )
  return VeVeeVeV
 else :
  if isFolder :
   eeevev ( name , url , mode , iconimage , eeeevVV , description = '' )
  else :
   i1Veevev ( name , url , mode , iconimage , eeeevVV , description = '' )
   if 54 - 54: eVeev
def eeevev ( name , url , mode , iconimage , fanart , description = '' ) :
 VevVevVVevVevVev . setSetting ( 'favtype' , 'folder' )
 ii1 = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&fanart=" + urllib . quote_plus ( fanart ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 VeVeeVeV = True
 iiIiii1iI1i = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 iiIiii1iI1i . setInfo ( type = "Video" , infoLabels = { "Title" : name , 'plot' : description } )
 iiIiii1iI1i . setProperty ( 'fanart_image' , fanart )
 if 'youtube.com/channel/' in url :
  ii1 = 'plugin://plugin.video.youtube/channel/' + description + '/'
 if 'youtube.com/user/' in url :
  ii1 = 'plugin://plugin.video.youtube/user/' + description + '/'
 if 'youtube.com/playlist?' in url :
  ii1 = 'plugin://plugin.video.youtube/playlist/' + description + '/'
 if 'plugin://' in url :
  ii1 = url
 Veve = [ ]
 I1IiiI1ii1i = VevVevVVevVevVev . getSetting ( 'favlist' )
 if I1IiiI1ii1i == 'yes' : Veve . append ( ( '[COLOR white]Remove from Evolve Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=21&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 else : Veve . append ( ( '[COLOR white]Add to Evolve Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=20&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 iiIiii1iI1i . addContextMenuItems ( Veve , replaceItems = False )
 VeVeeVeV = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = ii1 , listitem = iiIiii1iI1i , isFolder = True )
 return VeVeeVeV
 if 45 - 45: VeVVeveeVVeeevV - eVeev + Ii1I * I111I11 . IIIi1i1I
def iii11I111 ( name , url , mode , iconimage , fanart , description = '' ) :
 VevVevVVevVevVev . setSetting ( 'favtype' , 'link' )
 ii1 = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&fanart=" + urllib . quote_plus ( fanart ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 VeVeeVeV = True
 iiIiii1iI1i = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 iiIiii1iI1i . setProperty ( 'fanart_image' , fanart )
 Veve = [ ]
 I1IiiI1ii1i = VevVevVVevVevVev . getSetting ( 'favlist' )
 if I1IiiI1ii1i == 'yes' : Veve . append ( ( '[COLOR white]Remove from Evolve Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=21&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 else : Veve . append ( ( '[COLOR white]Add to Evolve Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=20&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 iiIiii1iI1i . addContextMenuItems ( Veve , replaceItems = False )
 VeVeeVeV = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = ii1 , listitem = iiIiii1iI1i , isFolder = False )
 return VeVeeVeV
 if 39 - 39: VeVV / Ii1I / I1iiiiI1iII - I111I11 - VevVeeVevVVeee % eVeev
def i1Veevev ( name , url , mode , iconimage , fanart , description = '' ) :
 VevVevVVevVevVev . setSetting ( 'favtype' , 'link' )
 ii1 = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&fanart=" + urllib . quote_plus ( fanart ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 VeVeeVeV = True
 iiIiii1iI1i = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 iiIiii1iI1i . setProperty ( 'fanart_image' , fanart )
 iiIiii1iI1i . setProperty ( "IsPlayable" , "true" )
 Veve = [ ]
 I1IiiI1ii1i = VevVevVVevVevVev . getSetting ( 'favlist' )
 if I1IiiI1ii1i == 'yes' : Veve . append ( ( '[COLOR white]Remove from Evolve Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=21&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 else : Veve . append ( ( '[COLOR white]Add to Evolve Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=20&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 iiIiii1iI1i . addContextMenuItems ( Veve , replaceItems = False )
 VeVeeVeV = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = ii1 , listitem = iiIiii1iI1i , isFolder = False )
 return VeVeeVeV
 if 31 - 31: i1Ii - Ii1I / i111I1 * I1I1i1
def eeveVev ( url , name ) :
 iI111i1II = i1iIi ( url )
 if len ( iI111i1II ) > 1 :
  i1I1IiiIi1i = VeevV
  iiI11ii1I1 = os . path . join ( os . path . join ( i1I1IiiIi1i , '' ) , name + '.txt' )
  if not os . path . exists ( iiI11ii1I1 ) :
   file ( iiI11ii1I1 , 'w' ) . close ( )
  VeveeeeeevVVVVev = open ( iiI11ii1I1 )
  IiiIi1III = VeveeeeeevVVVVev . read ( )
  if IiiIi1III == iI111i1II : pass
  else :
   eevVeveev ( '[B][COLOR red]E[/COLOR][COLOR white]volve[/COLOR][/B] [B][COLOR red]I[/COLOR][COLOR white]nformation[/COLOR][/B]' , iI111i1II )
   VeeevVVeVeVev = open ( iiI11ii1I1 , "w" )
   VeeevVVeVeVev . write ( iI111i1II )
   VeeevVVeVeVev . close ( )
   if 84 - 84: eVeev . VevVeeVevVVeee % Ii1I . I1I1i1 + I1iiiiI1iII
def eevVeveev ( heading , text ) :
 id = 10147
 xbmc . executebuiltin ( 'ActivateWindow(%d)' % id )
 xbmc . sleep ( 500 )
 Ii11i1I11i = xbmcgui . Window ( id )
 I11i1 = 50
 while ( I11i1 > 0 ) :
  try :
   xbmc . sleep ( 10 )
   I11i1 -= 1
   Ii11i1I11i . getControl ( 1 ) . setLabel ( heading )
   Ii11i1I11i . getControl ( 5 ) . setText ( text )
   return
  except :
   pass
   if 28 - 28: i1Ii
def eVVVVee ( name ) :
 global Icon
 global Next
 global Previous
 global window
 global Quit
 global images
 iiI11ii1I1 = os . path . join ( os . path . join ( VeevV , '' ) , name + '.txt' )
 VeveeeeeevVVVVev = open ( iiI11ii1I1 )
 IiiIi1III = VeveeeeeevVVVVev . read ( )
 images = re . compile ( '<image>(.+?)</image>' ) . findall ( IiiIi1III )
 VevVevVVevVevVev . setSetting ( 'pos' , '0' )
 window = pyxbmct . AddonDialogWindow ( '' )
 VVeev = '/resources/art'
 ii11I1 = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + VVeve + VVeev , 'next_focus.png' ) )
 eVevee = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + VVeve + VVeev , 'next1.png' ) )
 Ii111iIi1iIi = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + VVeve + VVeev , 'previous_focus.png' ) )
 IIIII = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + VVeve + VVeev , 'previous.png' ) )
 eeveeVeVeveveveV = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + VVeve + VVeev , 'close_focus.png' ) )
 VVe = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + VVeve + VVeev , 'close.png' ) )
 i1i11I1I1iii1 = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + VVeve + VVeev , 'main-bg1.png' ) )
 window . setGeometry ( 1300 , 720 , 100 , 50 )
 I1iii11 = pyxbmct . Image ( i1i11I1I1iii1 )
 window . placeControl ( I1iii11 , - 10 , - 10 , 130 , 70 )
 VVV = '0xFF000000'
 Previous = pyxbmct . Button ( '' , focusTexture = Ii111iIi1iIi , noFocusTexture = IIIII , textColor = VVV , focusedColor = VVV )
 Next = pyxbmct . Button ( '' , focusTexture = ii11I1 , noFocusTexture = eVevee , textColor = VVV , focusedColor = VVV )
 Quit = pyxbmct . Button ( '' , focusTexture = eeveeVeVeveveveV , noFocusTexture = VVe , textColor = VVV , focusedColor = VVV )
 Icon = pyxbmct . Image ( images [ 0 ] , aspectRatio = 2 )
 window . placeControl ( Previous , 102 , 1 , 10 , 10 )
 window . placeControl ( Next , 102 , 40 , 10 , 10 )
 window . placeControl ( Quit , 102 , 21 , 10 , 10 )
 window . placeControl ( Icon , 0 , 0 , 100 , 50 )
 Previous . controlRight ( Next )
 Previous . controlUp ( Quit )
 window . connect ( Previous , eeeevV )
 window . connect ( Next , iII1iii )
 Previous . setVisible ( False )
 window . setFocus ( Quit )
 Previous . controlRight ( Quit )
 Quit . controlLeft ( Previous )
 Quit . controlRight ( Next )
 Next . controlLeft ( Quit )
 window . connect ( Quit , window . close )
 window . doModal ( )
 del window
 if 12 - 12: eVeev
def iII1iii ( ) :
 VeviII1 = int ( VevVevVVevVevVev . getSetting ( 'pos' ) )
 IIII1i = int ( VeviII1 ) + 1
 VevVevVVevVevVev . setSetting ( 'pos' , str ( IIII1i ) )
 Ii1IIIIi1ii1I = len ( images )
 Icon . setImage ( images [ int ( IIII1i ) ] )
 Previous . setVisible ( True )
 if int ( IIII1i ) == int ( Ii1IIIIi1ii1I ) - 1 :
  Next . setVisible ( False )
  if 13 - 13: eeeVeveeeveVVVV % I1I1i1 . IIIi1i1I / I1111 % eVeev . VeVVeveeVVeeevV
def eeeevV ( ) :
 VeviII1 = int ( VevVevVVevVevVev . getSetting ( 'pos' ) )
 i1iIiiiiii1II = int ( VeviII1 ) - 1
 VevVevVVevVevVev . setSetting ( 'pos' , str ( i1iIiiiiii1II ) )
 Icon . setImage ( images [ int ( i1iIiiiiii1II ) ] )
 Next . setVisible ( True )
 if int ( i1iIiiiiii1II ) == 0 :
  Previous . setVisible ( False )
  if 81 - 81: I111I11 * eVev + iIiI1I11 + I1111 - VeVVeveeVVeeevV
def i1i1I111iIi1 ( url , fanart ) :
 VevVevVVevVevVev . setSetting ( 'favlist' , 'yes' )
 eeevevVeveveVeveveve = None
 file = open ( IiI , 'r' )
 eeevevVeveveVeveveve = file . read ( ) . replace ( '\n' , '' ) . replace ( '\r' , '' )
 eeveVeVeveve = re . compile ( "<item>(.+?)</item>" , re . DOTALL ) . findall ( eeevevVeveveVeveveve )
 for i1 in eeveVeVeveve :
  VVeVeveve ( i1111 , url , Veveveeeeeevev , fanart , i1 )
 VevVevVVevVevVev . setSetting ( 'favlist' , 'no' )
 if 71 - 71: IIIi1i1I - i111I1 / I1I1i1 * I1I1i1 / eeveveveveVeVeVeve . eeveveveveVeVeVeve
def eeeeveveveeVevevevev ( name , url , iconimage , fanart ) :
 eVeeeeevevevVeevev = VevVevVVevVevVev . getSetting ( 'favtype' )
 url = url . replace ( ' ' , '%20' )
 iconimage = iconimage . replace ( ' ' , '%20' )
 if '<>' in url :
  VeevVeVeveveVVeve = url . split ( '<>' ) [ 0 ]
  II1III = url . split ( '<>' ) [ 1 ]
  iI1iI1I1i1I = url . split ( '<>' ) [ 2 ]
  iIi11Ii1 = url . split ( '<>' ) [ 3 ]
  Ii11iII1 = url . split ( '<>' ) [ 4 ]
  iiVVeeeeVevVe = '<FAV><item>\n<title>' + name + '</title>\n<meta>tvep</meta>\n<nan>tvshow</nan>\n<showyear>' + iIi11Ii1 + '</showyear>\n<imdb>' + VeevVeVeveveVVeve + '</imdb>\n<season>' + II1III + '</season>\n<episode>' + iI1iI1I1i1I + '</episode>\n<episodeyear>' + Ii11iII1 + '</episodeyear>\n<thumbnail>' + iconimage + '</thumbnail>\n<fanart>' + fanart + '</fanart></item></FAV>\n'
 elif len ( url ) == 9 :
  iiVVeeeeVevVe = '<FAV><item>\n<title>' + name + '</title>\n<meta>movie</meta>\n<nan>movie</nan>\n<imdb>' + url + '</imdb>\n' + '<thumbnail>' + iconimage + '</thumbnail>\n<fanart>' + fanart + '</fanart></item></FAV>\n'
 else :
  iiVVeeeeVevVe = '<FAV><item>\n<title>' + name + '</title>\n<' + eVeeeeevevevVeevev + '>' + url + '</' + eVeeeeevevevVeevev + '>\n' + '<thumbnail>' + iconimage + '</thumbnail>\n<fanart>' + fanart + '</fanart></item></FAV>\n'
 eeVe = open ( IiI , 'a' )
 eeVe . write ( iiVVeeeeVevVe )
 eeVe . close ( )
 if 93 - 93: IIIi1i1I / eeeVeveeeveVVVV / VeVV % iIiI1I11 % iIiI1I11
def IiI11iI1i1i1i ( name , url , iconimage ) :
 print name
 eeevevVeveveVeveveve = None
 file = open ( IiI , 'r' )
 eeevevVeveveVeveveve = file . read ( )
 eVevVeeeeee = ''
 eeveVeVeveve = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( eeevevVeveveVeveveve )
 for eVVeeevevVevV in eeveVeVeveve :
  iiVVeeeeVevVe = '\n<FAV><item>\n' + eVVeeevevVevV + '</item>\n'
  if name in eVVeeevevVevV :
   print 'xxxxxxxxxxxxxxxxx'
   iiVVeeeeVevVe = iiVVeeeeVevVe . replace ( 'item' , ' ' )
  eVevVeeeeee = eVevVeeeeee + iiVVeeeeVevVe
 file = open ( IiI , 'w' )
 file . truncate ( )
 file . write ( eVevVeeeeee )
 file . close ( )
 xbmc . executebuiltin ( 'Container.Refresh' )
 if 39 - 39: Ii1 * I1111 + VeVV - Ii1 + eVeev
def VevevVeveVVevevVevev ( url ) :
 try :
  II11IiIi11 = url . split ( '/' ) [ 2 ] . replace ( 'www.' , '' )
  file = open ( IIi1IiiiI1Ii , 'r' )
  eeviiiI1I1iIIIi1 = file . read ( )
  if II11IiIi11 in eeviiiI1I1iIIIi1 : return '[COLOR springgreen] (RD)[/COLOR]'
  else : return ''
 except : return ''
 if 17 - 17: VeVV . VeVVeveeVVeeevV / i1Ii % i1I1ii1II1iII % eeveveveveVeVeVeve / i11iIiiIii
def VVVIiiiii1iI ( ) :
 import xbmcaddon
 xbmcaddon . Addon ( 'script.module.nanscrapers' ) . openSettings ( )
 if 49 - 49: eVev . Ii1 / eeveevVeeveeeeev + i1I1ii1II1iII
def iI ( link ) :
 try :
  ii11i = re . compile ( '<layouttype>(.+?)</layouttype>' ) . findall ( link ) [ 0 ]
  if ii11i == 'thumbnail' : xbmc . executebuiltin ( 'Container.SetViewMode(500)' )
  else : xbmc . executebuiltin ( 'Container.SetViewMode(50)' )
 except : pass
 if 35 - 35: IIIi1i1I * VevVeeVevVVeee - eeveevVeeveeeeev % eVev
 if 87 - 87: I1I1i1 * iIiI1I11 . i1Ii
I1i = eeveevV ( ) ; i11 = None ; i1111 = None ; iiI1IIIi = None ; VevVeeveeveveveV = None ; I11 = None ; eVeveeveveVVeeVev = None
try : VevVeeveeveveveV = urllib . unquote_plus ( I1i [ "site" ] )
except : pass
try : i11 = urllib . unquote_plus ( I1i [ "url" ] )
except : pass
try : i1111 = urllib . unquote_plus ( I1i [ "name" ] )
except : pass
try : iiI1IIIi = int ( I1i [ "mode" ] )
except : pass
try : I11 = urllib . unquote_plus ( I1i [ "iconimage" ] )
except : pass
try : eeeevVV = urllib . unquote_plus ( I1i [ "fanart" ] )
except : pass
try : eVeveeveveVVeeVev = str ( I1i [ "description" ] )
except : pass
if 79 - 79: eeveevVeeveeeeev - VeVV + I111I11 - iIiI1I11
if iiI1IIIi == None or i11 == None or len ( i11 ) < 1 : VeveV ( )
elif iiI1IIIi == 1 : II ( i1111 , i11 , I11 , eeeevVV )
elif iiI1IIIi == 2 : VevI11Iiii1I ( i1111 , i11 , I11 , eVeveeveveVVeeVev )
elif iiI1IIIi == 3 : VVevVeeeVeveveev ( i1111 , i11 , I11 )
elif iiI1IIIi == 4 : eeeevVVevVevVe ( i1111 , i11 , I11 )
elif iiI1IIIi == 5 : I1 ( i11 )
elif iiI1IIIi == 6 : ii1iI1I11I ( i11 , I11 )
elif iiI1IIIi == 7 : eevevV ( i11 )
elif iiI1IIIi == 8 : eVVVVee ( i1111 )
elif iiI1IIIi == 9 : Ve ( i1111 , i11 )
elif iiI1IIIi == 10 : iiIIiiIi1Ii11 ( i1111 , i11 , I11 , eeeevVV )
elif iiI1IIIi == 11 : VevVevVeevev ( i11 )
elif iiI1IIIi == 15 : I1iII1iIi1I ( i1111 , i11 , I11 )
elif iiI1IIIi == 16 : eeevevVeveVevVev ( i1111 , i11 , I11 )
elif iiI1IIIi == 17 : eeeVeevVVVeeev ( i1111 , i11 )
elif iiI1IIIi == 18 : VVeveVeVVeveVVev ( i1111 , i11 , I11 , eeeevVV )
elif iiI1IIIi == 19 : eeevevevVVevevVe ( i1111 , i11 , I11 , eeeevVV )
if 93 - 93: i1I1ii1II1iII . eeeVeveeeveVVVV - I1111 + I1I1i1
elif iiI1IIIi == 20 : eeeeveveveeVevevevev ( i1111 , i11 , I11 , eeeevVV )
elif iiI1IIIi == 21 : IiI11iI1i1i1i ( i1111 , i11 , I11 )
elif iiI1IIIi == 22 : i1i1I111iIi1 ( i11 , eeeevVV )
elif iiI1IIIi == 23 : DOIPLAYER ( i1111 , i11 , I11 , eeeevVV )
elif iiI1IIIi == 24 : iiiIiI ( i1111 , i11 , I11 , eeeevVV )
elif iiI1IIIi == 25 : VVVIiiiii1iI ( )
if 61 - 61: i1I1ii1II1iII
elif iiI1IIIi == 26 : iiiIiI ( i1111 , i11 , I11 , eeeevVV )
elif iiI1IIIi == 27 : VVeVeeevevee ( i1111 , i11 , I11 , eeeevVV )
elif iiI1IIIi == 28 : eVeV ( i1111 , i11 , I11 , eeeevVV )
elif iiI1IIIi == 29 : ii1ii11IIIiiI ( i1111 , i11 , I11 , eeeevVV )
elif iiI1IIIi == 30 : eVe ( i1111 , i11 , I11 , eeeevVV )
elif iiI1IIIi == 31 : VeeeVeveV ( i1111 , i11 , I11 , eeeevVV )
elif iiI1IIIi == 32 : iii ( i1111 , i11 , I11 , eeeevVV )
elif iiI1IIIi == 33 : ii ( i1111 , i11 , I11 , eeeevVV )
elif iiI1IIIi == 34 : IiIiii1I1 ( i1111 , i11 , I11 , eeeevVV )
if 15 - 15: i11iIiiIii % eeeVeveeeveVVVV * i1Ii / iIiI1I11
if 90 - 90: VevVeeVevVVeee
if 31 - 31: eVeev + Ii1I
if 87 - 87: i111I1
if 45 - 45: eeveevVeeveeeeev / VeVVeveeVVeeevV - VevVeeVevVVeee / I111I11 % Ii1
if 83 - 83: eeeVeveeeveVVVV . VeVV - Ii1 * i11iIiiIii
if 20 - 20: eeveveveveVeVeVeve * iIiI1I11 + i1I1ii1II1iII % eVev % I1iiiiI1iII
xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3
