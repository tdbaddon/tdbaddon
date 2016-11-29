import xbmc , xbmcaddon , xbmcgui , xbmcplugin , urllib , urllib2 , os , re , sys , datetime , urlresolver , random , liveresolver , base64 , pyxbmct
from resources . lib . common_addon import Addon
from HTMLParser import HTMLParser
from metahandler import metahandlers
from resources . lib . scrape import latesttv
from resources . lib . scrape import latestmovies
if 64 - 64: i11iIiiIii
VVeve = 'plugin.video.Evolve'
VeevVee = Addon ( VVeve , sys . argv )
VevVevVVevVevVev = xbmcaddon . Addon ( id = VVeve )
iiiii = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + VVeve , 'fanart.jpg' ) )
eeeevVV = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + VVeve , 'fanart.jpg' ) )
II1 = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + VVeve , 'icon.png' ) )
Veveveeeeeevev = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + VVeve + '/resources/art' , 'next.png' ) )
I1IiiI = 'http://matsbuilds.uk/Evolvesnewmenu/mainmenu.xml'
IIi1IiiiI1Ii = 'http://matsbuilds.uk/Evolvemasterlist/'
I11i11Ii = VevVevVVevVevVev . getSetting ( 'password' )
eVeveveVe = VevVevVVevVevVev . getSetting ( 'enable_meta' )
VVVeev = 'http://matsbuilds.uk/private/info.txt'
Veeeeveveve = xbmc . translatePath ( 'special://home/userdata/addon_data/' + VVeve )
if 6 - 6: i1 * ii1IiI1i % VVeeVVe / I11i / eevV / IiiIII111iI
def IiII ( ) :
 if not os . path . exists ( Veeeeveveve ) :
  os . mkdir ( Veeeeveveve )
 iI1Ii11111iIi ( VVVeev , 'GlobalCompare' )
 i1i1II = VevVevVVevVevVev . getSetting ( 'layout' )
 if i1i1II == 'Listers' :
  VeveeevVVev = I1i1iiI1 ( I1IiiI )
  iiIIIII1i1iI = re . compile ( '<item>(.+?)</item>' ) . findall ( VeveeevVVev )
  for eeveVev in iiIIIII1i1iI :
   eeevev = re . compile ( '<title>(.+?)</title>.+?folder>(.+?)</folder>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>' ) . findall ( eeveVev )
   for eevev , VeeveVeveee , eeveVeVeveve , iiiii in eeevev :
    i1eVVeeevevVevV ( eevev , VeeveVeveee , 1 , eeveVeVeveve , iiiii )
 else :
  VeveeevVVev = I1i1iiI1 ( IIi1IiiiI1Ii )
  iiIIIII1i1iI = re . compile ( 'alt="\[DIR\]"></td><td><a href="(.+?)">.+?</a>' ) . findall ( VeveeevVVev )
  for i1111 in iiIIIII1i1iI :
   eevev = i1111 . replace ( '/' , '' ) . replace ( '%20' , ' ' ) . split ( '-' ) [ 1 ]
   i11 = 'Evolve ' + eevev
   VeeveVeveee = IIi1IiiiI1Ii + i1111
   eeveVeVeveve = 'http://matsbuilds.uk/pics/evolvecatview/' + eevev . replace ( ' ' , '%20' ) + '.png'
   iiiii = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + VVeve , 'fanart.jpg' ) )
   i1eVVeeevevVevV ( I11 ( i11 ) , VeeveVeveee , 12 , eeveVeVeveve , iiiii )
 i1eVVeeevevVevV ( '[B][COLOR red]S[/COLOR][COLOR white]earch[/COLOR][/B] [B][COLOR red]E[/COLOR][COLOR white]volve[/COLOR][/B]' , 'url' , 5 , 'http://matsbuilds.uk/pics/evolvecatview/Search.png' , eeeevVV )
 if 98 - 98: I1111 * eeveevVeeveeeeev / I1I1i1 * eVev / IIIi1i1I
 xbmc . executebuiltin ( 'Container.SetViewMode(500)' )
 if 72 - 72: iii11iiII % i11IiIiiIIIII / IiiIII111ii / iiIIi1IiIi11 . i1Ii
def I111I11 ( name , url , iconimage , fanart ) :
 fanart = iconimage
 VeveeevVVev = I1i1iiI1 ( url )
 iiIIIII1i1iI = re . compile ( '</td><td><a href="(.+?)">.+?</a>' ) . findall ( VeveeevVVev )
 for VevVevevVee in iiIIIII1i1iI :
  if 'xml' in VevVevevVee :
   name = VevVevevVee . replace ( '.xml' , '' ) . replace ( '%20' , ' ' )
   VVeeeeeV = name . split ( ' ' ) [ 0 ] . lower ( )
   i1iIIIiI1I = url + VevVevevVee
   iconimage = 'http://matsbuilds.uk/pics/newevolveicons/' + VVeeeeeV + '.PNG'
   if VVeeeeeV == 'wraith' : iconimage = 'http://matsbuilds.uk/pics/newevolveicons/' + VVeeeeeV + '.png'
   i1eVVeeevevVevV ( I11 ( name ) , i1iIIIiI1I , 1 , iconimage , fanart )
   if 70 - 70: i111I1 % eVeV - iiIiIIi % ii1IiI1i - i1 + I1111
def iI11iiiI1II ( name , url , iconimage , fanart ) :
 VeveeeeevVeevev = Ii11iii11I ( name )
 VevVevVVevVevVev . setSetting ( 'tv' , VeveeeeevVeevev )
 VeveeevVVev = I1i1iiI1 ( url )
 eVeevevVeevevV ( VeveeevVVev )
 if '<message>' in VeveeevVVev :
  VVVeev = re . compile ( '<message>(.+?)</message>' ) . findall ( VeveeevVVev ) [ 0 ]
  iI1Ii11111iIi ( VVVeev , VeveeeeevVeevev )
 if '<intro>' in VeveeevVVev :
  iI11i1I1 = re . compile ( '<intro>(.+?)</intro>' ) . findall ( VeveeevVVev ) [ 0 ]
  eeveevVVVeveev ( iI11i1I1 )
 if 'XXX>yes</XXX' in VeveeevVVev : eeVVVeeveeevVev ( VeveeevVVev )
 iiIIIII1i1iI = re . compile ( '<item>(.+?)</item>' ) . findall ( VeveeevVVev )
 eev = len ( iiIIIII1i1iI )
 for eeveVev in iiIIIII1i1iI :
  try :
   if '<sportsdevil>' in eeveVev : I11II1i ( eeveVev , url )
   elif '<folder>' in eeveVev : IIIII ( eeveVev )
   elif '<iptv>' in eeveVev : eeeeeeVevee ( eeveVev )
   elif '<image>' in eeveVev : IIiiiiiiIi1I1 ( eeveVev )
   elif '<text>' in eeveVev : I1IIIii ( eeveVev )
   elif '<scraper>' in eeveVev : eVeVeeVeeveev ( eeveVev )
   elif '<redirect>' in eeveVev : VVVV ( eeveVev )
   elif '<oktitle>' in eeveVev : VVVevev ( eeveVev )
   else : iiiiiIIii ( eeveVev , url )
  except : pass
  if 71 - 71: i11IiIiiIIIII + iiIIi1IiIi11 * i11IiIiiIIIII - eeveevVeeveeeeev * eVev
def VVVevev ( item ) :
 eevev = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 VeeeevVeeevevev = re . compile ( '<oktitle>(.+?)</oktitle>' ) . findall ( item ) [ 0 ]
 ee = re . compile ( '<line1>(.+?)</line1>' ) . findall ( item ) [ 0 ]
 ii11I = re . compile ( '<line2>(.+?)</line2>' ) . findall ( item ) [ 0 ]
 VeeevVVeveVV = re . compile ( '<line3>(.+?)</line3>' ) . findall ( item ) [ 0 ]
 ii11i1 = '##' + VeeeevVeeevevev + '#' + ee + '#' + ii11I + '#' + VeeevVVeveVV + '##'
 eeveVeVeveve = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 iiiii = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
 IIIii1II1II ( eevev , ii11i1 , 17 , eeveVeVeveve , iiiii )
 if 42 - 42: iiIIi1IiIi11 + iii11iiII
def eevVeveevVe ( name , url ) :
 Ii11Ii1I = re . compile ( '##(.+?)##' ) . findall ( url ) [ 0 ] . split ( '#' )
 VeveveV = xbmcgui . Dialog ( )
 VeveveV . ok ( Ii11Ii1I [ 0 ] , Ii11Ii1I [ 1 ] , Ii11Ii1I [ 2 ] , Ii11Ii1I [ 3 ] )
 if 39 - 39: i111I1 - eevV * eeveevVeeveeeeev % eVev * eevV % eevV
def VVVV ( item ) :
 VeeveVeveee = re . compile ( '<redirect>(.+?)</redirect>' ) . findall ( item ) [ 0 ]
 iI11iiiI1II ( 'name' , VeeveVeveee , 'iconimage' , 'fanart' )
 if 59 - 59: ii1IiI1i + IiiIII111iI - eVev - IiiIII111iI + i11IiIiiIIIII / IIIi1i1I
def eVeVeeVeeveev ( item ) :
 eevev = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 eeveVeVeveve = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 VeeveVeveee = re . compile ( '<scraper>(.+?)</scraper>' ) . findall ( item ) [ 0 ]
 iiiii = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
 i1eVVeeevevVevV ( eevev , VeeveVeveee , 10 , eeveVeVeveve , iiiii )
 if 24 - 24: IiiIII111ii . i1Ii % i11IiIiiIIIII + iiIiIIi % I1I1i1
def I11III1II ( name , url ) :
 iI1I111Ii111i = url
 if 7 - 7: iiIiIIi * eeveevVeeveeeeev % iii11iiII . i111I1
 if 45 - 45: i11iIiiIii * eevV % ii1IiI1i + IIIi1i1I - iiIIi1IiIi11
 if iI1I111Ii111i == 'latesttv' :
  iIi1iIiii111 = 14
  iIIIi1 = latesttv . INDEXER ( )
 elif iI1I111Ii111i == 'latestmovies' :
  iIi1iIiii111 = 15
  iIIIi1 = latestmovies . INDEXER ( )
  if 20 - 20: I11i + IIIi1i1I - iiIiIIi
  if 30 - 30: eevV - i11IiIiiIIIII - i11iIiiIii % I1I1i1 - eevV * iiIIi1IiIi11
 eVevevVevVevV = re . compile ( '<item>(.+?)</item>' ) . findall ( iIIIi1 )
 for eeveVev in eVevevVevVevV :
  eeevev = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>' ) . findall ( eeveVev )
  eev = len ( eVevevVevVevV )
  for name , url , eeveVeVeveve , iiiii in eeevev :
   if '<meta>' in eeveVev :
    i1ii1iiI = re . compile ( '<meta>(.+?)</meta>' ) . findall ( eeveVev ) [ 0 ]
    VeveevVevevVeeveev ( name , url , iIi1iIiii111 , eeveVeVeveve , eev , i1ii1iiI , isFolder = False )
   else : VevevVeveVVevevVevev ( name , url , iIi1iIiii111 , eeveVeVeveve , iiiii )
   if 11 - 11: i111I1 . IIIi1i1I
   if 92 - 92: i1Ii . eVeV
def i1i ( name , url , iconimage ) :
 iIIIi1 = latesttv . HOSTS ( name , url , iconimage )
 iiI111I1iIiI ( name , iIIIi1 )
 if 41 - 41: I1111 . iiIiIIi + i1 * eVev % I1111 * I1111
def iIIIIi1iiIi1 ( name , url , iconimage ) :
 iIIIi1 = latestmovies . HOSTS ( name , url , iconimage )
 iiI111I1iIiI ( name , iIIIi1 )
 if 21 - 21: IiiIII111iI * ii1IiI1i
 if 91 - 91: i111I1
def iiI111I1iIiI ( title , itemlist ) :
 iiIii = 1
 eeeevV = [ ]
 eVeVeveevevVVev = [ ]
 for i1I1ii in itemlist :
  eVVeev = i1I1ii . split ( '/' ) [ 2 ] . split ( '.' ) [ 0 ]
  eevev = "Link " + str ( iiIii ) + ' | ' + eVVeev
  if eVVeev != 'www' :
   iiIii = iiIii + 1
   eeeevV . append ( i1I1ii )
   eVeVeveevevVVev . append ( eevev )
 title = '[COLOR red]' + title + '[/COLOR]'
 VeveveV = xbmcgui . Dialog ( )
 eeevevVeveveV = VeveveV . select ( title , eVeVeveevevVVev )
 if eeevevVeveveV < 0 : quit ( )
 else :
  VeeveVeveee = eeeevV [ eeevevVeveveV ]
  iIiIIIi ( eevev , VeeveVeveee , eeveVeVeveve )
  if 93 - 93: i1Ii
def I1IIIii ( item ) :
 eevev = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 ii11i1 = re . compile ( '<text>(.+?)</text>' ) . findall ( item ) [ 0 ]
 eeveVeVeveve = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 iiiii = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
 IIIii1II1II ( eevev , ii11i1 , 9 , eeveVeVeveve , iiiii )
 if 10 - 10: IiiIII111ii
def VVeeVVevevev ( name , url ) :
 VVeVee = eVevevevevVVeevev ( url )
 iiIi1IIiIi ( name , VVeVee )
 if 75 - 75: IiiIII111iI + I1111
def IIiiiiiiIi1I1 ( item ) :
 VeeeVeveV = re . compile ( '<image>(.+?)</image>' ) . findall ( item )
 if len ( VeeeVeveV ) == 1 :
  eevev = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  eeveVeVeveve = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  i1iIi = re . compile ( '<image>(.+?)</image>' ) . findall ( item ) [ 0 ]
  iiiii = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
  IIIii1II1II ( eevev , i1iIi , 7 , eeveVeVeveve , iiiii )
 elif len ( VeeeVeveV ) > 1 :
  eevev = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  eeveVeVeveve = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  iiiii = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
  eeVVeeeeee = ''
  for i1iIi in VeeeVeveV : eeVVeeeeee = eeVVeeeeee + '<image>' + i1iIi + '</image>'
  II1I = Veeeeveveve
  eevev = Ii11iii11I ( eevev )
  Vev = os . path . join ( os . path . join ( II1I , '' ) , eevev + '.txt' )
  if not os . path . exists ( Vev ) : file ( Vev , 'w' ) . close ( )
  i1II1Iiii1I11 = open ( Vev , "w" )
  i1II1Iiii1I11 . write ( eeVVeeeeee )
  i1II1Iiii1I11 . close ( )
  IIIii1II1II ( eevev , 'image' , 8 , eeveVeVeveve , iiiii )
  if 9 - 9: IIIi1i1I / I1111 - IiiIII111iI / VVeeVVe / ii1IiI1i - eVev
def eeeeeeVevee ( item ) :
 eevev = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 eeveVeVeveve = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 VeeveVeveee = re . compile ( '<iptv>(.+?)</iptv>' ) . findall ( item ) [ 0 ]
 iiiii = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
 i1eVVeeevevVevV ( eevev , VeeveVeveee , 6 , eeveVeVeveve , iiiii )
 if 91 - 91: i1Ii % I11i % ii1IiI1i
def IIi1I11I1II ( url , iconimage ) :
 VeveeevVVev = eVevevevevVVeevev ( url )
 VeeVeeeVe = re . compile ( '^#.+?:-?[0-9]*(.*?),(.*?)\n(.*?)$' , re . I + re . M + re . U + re . S ) . findall ( VeveeevVVev )
 ii11IIII11I = [ ]
 for VVeee , eevev , url in VeeVeeeVe :
  eVeeVVVeVe = { "params" : VVeee , "name" : eevev , "url" : url }
  ii11IIII11I . append ( eVeeVVVeVe )
 list = [ ]
 for i1Iii1i1I in ii11IIII11I :
  eVeeVVVeVe = { "name" : i1Iii1i1I [ "name" ] , "url" : i1Iii1i1I [ "url" ] }
  VeeVeeeVe = re . compile ( ' (.+?)="(.+?)"' , re . I + re . M + re . U + re . S ) . findall ( i1Iii1i1I [ "params" ] )
  for VVeVevev , IiI111111IIII in VeeVeeeVe :
   eVeeVVVeVe [ VVeVevev . strip ( ) . lower ( ) . replace ( '-' , '_' ) ] = IiI111111IIII . strip ( )
  list . append ( eVeeVVVeVe )
 for i1Iii1i1I in list :
  if '.ts' in i1Iii1i1I [ "url" ] : IIIii1II1II ( i1Iii1i1I [ "name" ] , i1Iii1i1I [ "url" ] , 2 , iconimage , iiiii )
  else : VevevVeveVVevevVevev ( i1Iii1i1I [ "name" ] , i1Iii1i1I [ "url" ] , 2 , iconimage , iiiii )
  if 37 - 37: eVeV / I1I1i1
def iiiiiIIii ( item , url ) :
 i1I1iI1iIi111i = re . compile ( '<link>(.+?)</link>' ) . findall ( item )
 eeevev = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>' ) . findall ( item )
 for eevev , iiIi1IIi1I , eeveVeVeveve , iiiii in eeevev :
  if 'youtube.com/playlist?' in iiIi1IIi1I :
   eevVeVVeveveveeVev = iiIi1IIi1I . split ( 'list=' ) [ 1 ]
   i1eVVeeevevVevV ( eevev , iiIi1IIi1I , eeveeveeveVeveVV , eeveVeVeveve , iiiii , description = eevVeVVeveveveeVev )
 if len ( i1I1iI1iIi111i ) == 1 :
  eeevev = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>' ) . findall ( item )
  for eevev , url , eeveVeVeveve , iiiii in eeevev :
   if '.ts' in url : IIIii1II1II ( eevev , url , 16 , eeveVeVeveve , iiiii , description = '' )
   elif '<meta>' in item :
    i1ii1iiI = re . compile ( '<meta>(.+?)</meta>' ) . findall ( item ) [ 0 ]
    VeveevVevevVeeveev ( eevev , url , 2 , eeveVeVeveve , 10 , i1ii1iiI , isFolder = False )
   else : VevevVeveVVevevVevev ( eevev , url , 2 , eeveVeVeveve , iiiii )
 elif len ( i1I1iI1iIi111i ) > 1 :
  eevev = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  eeveVeVeveve = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  iiiii = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
  if '.ts' in url : IIIii1II1II ( eevev , url , 16 , eeveVeVeveve , iiiii , description = '' )
  elif '<meta>' in item :
   i1ii1iiI = re . compile ( '<meta>(.+?)</meta>' ) . findall ( item ) [ 0 ]
   VeveevVevevVeeveev ( eevev , url , 3 , eeveVeVeveve , 80 , i1ii1iiI , isFolder = False )
  else : VevevVeveVVevevVevev ( eevev , url , 3 , eeveVeVeveve , iiiii )
  if 3 - 3: eVev
def IIIII ( item ) :
 eeevev = re . compile ( '<title>(.+?)</title>.+?folder>(.+?)</folder>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>' ) . findall ( item )
 for eevev , VeeveVeveee , eeveVeVeveve , iiiii in eeevev :
  if 'youtube.com/channel/' in VeeveVeveee :
   eevVeVVeveveveeVev = VeeveVeveee . split ( 'channel/' ) [ 1 ]
   i1eVVeeevevVevV ( eevev , VeeveVeveee , eeveeveeveVeveVV , eeveVeVeveve , iiiii , description = eevVeVVeveveveeVev )
  elif 'youtube.com/user/' in VeeveVeveee :
   eevVeVVeveveveeVev = VeeveVeveee . split ( 'user/' ) [ 1 ]
   i1eVVeeevevVevV ( eevev , VeeveVeveee , eeveeveeveVeveVV , eeveVeVeveve , iiiii , description = eevVeVVeveveveeVev )
  elif 'youtube.com/playlist?' in VeeveVeveee :
   eevVeVVeveveveeVev = VeeveVeveee . split ( 'list=' ) [ 1 ]
   i1eVVeeevevVevV ( eevev , VeeveVeveee , eeveeveeveVeveVV , eeveVeVeveve , iiiii , description = eevVeVVeveveveeVev )
  elif 'plugin://' in VeeveVeveee :
   Ii11I1 = HTMLParser ( )
   VeeveVeveee = Ii11I1 . unescape ( VeeveVeveee )
   i1eVVeeevevVevV ( eevev , VeeveVeveee , eeveeveeveVeveVV , eeveVeVeveve , iiiii )
  else :
   i1eVVeeevevVevV ( eevev , VeeveVeveee , 1 , eeveVeVeveve , iiiii )
   if 14 - 14: i11IiIiiIIIII % ii1IiI1i
def I11II1i ( item , url ) :
 i1I1iI1iIi111i = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( item )
 eeI1IiiiiI = re . compile ( '<link>(.+?)</link>' ) . findall ( item )
 if len ( i1I1iI1iIi111i ) + len ( eeI1IiiiiI ) == 1 :
  eevev = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  eeveVeVeveve = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  url = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( item ) [ 0 ]
  iiiii = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
  eevVIiII = re . compile ( '<referer>(.+?)</referer>' ) . findall ( item ) [ 0 ]
  VeveeevVVev = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' + url
  url = VeveeevVVev + '%26referer=' + eevVIiII
  IIIii1II1II ( eevev , url , 16 , eeveVeVeveve , iiiii )
 elif len ( i1I1iI1iIi111i ) + len ( eeI1IiiiiI ) > 1 :
  eevev = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  eeveVeVeveve = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  iiiii = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
  IIIii1II1II ( eevev , url , 3 , eeveVeVeveve , iiiii )
  if 25 - 25: i1 - i1 * eVev
def eeVVVeeveeevVev ( link ) :
 if I11i11Ii == '' :
  VeveveV = xbmcgui . Dialog ( )
  VVVVeveeev = VeveveV . yesno ( 'Adult Content' , 'You have opted to show adult content' , '' , 'Please set a password to prevent accidental access' , 'Cancel' , 'OK' )
  if VVVVeveeev == 1 :
   I11iiI1i1 = xbmc . Keyboard ( '' , 'Set Password' )
   I11iiI1i1 . doModal ( )
   if ( I11iiI1i1 . isConfirmed ( ) ) :
    I1i1Iiiii = I11iiI1i1 . getText ( )
    VevVevVVevVevVev . setSetting ( 'password' , I1i1Iiiii )
  else : quit ( )
 elif I11i11Ii <> '' :
  VeveveV = xbmcgui . Dialog ( )
  VVVVeveeev = VeveveV . yesno ( 'Adult Content' , 'Please enter the password you set' , 'to continue' , '' , 'Cancel' , 'OK' )
  if VVVVeveeev == 1 :
   I11iiI1i1 = xbmc . Keyboard ( '' , 'Enter Password' )
   I11iiI1i1 . doModal ( )
   if ( I11iiI1i1 . isConfirmed ( ) ) :
    I1i1Iiiii = I11iiI1i1 . getText ( )
   if I1i1Iiiii <> I11i11Ii :
    quit ( )
  else : quit ( )
  if 94 - 94: eVev * iiIIi1IiIi11 / I1111 / iiIIi1IiIi11
def eVevVevVVevV ( ) :
 I11iiI1i1 = xbmc . Keyboard ( '' , '[COLOR red]S[/COLOR][COLOR white]earch[/COLOR] [COLOR red]E[/COLOR][COLOR white]volve[/COLOR]' )
 I11iiI1i1 . doModal ( )
 if ( I11iiI1i1 . isConfirmed ( ) ) :
  eevVeVVeveveveeVev = I11iiI1i1 . getText ( )
  eevVeVVeveveveeVev = eevVeVVeveveveeVev . upper ( )
 else : quit ( )
 VeveeevVVev = I1i1iiI1 ( 'http://matsbuilds.uk/search/search.xml' )
 VV = re . compile ( '<link>(.+?)</link>' ) . findall ( VeveeevVVev )
 for VeeveVeveee in VV :
  try :
   VeveeevVVev = I1i1iiI1 ( VeeveVeveee )
   VeVeV = re . compile ( '<item>(.+?)</item>' ) . findall ( VeveeevVVev )
   for eeveVev in VeVeV :
    iiIIIII1i1iI = re . compile ( '<title>(.+?)</title>' ) . findall ( eeveVev )
    for Ii1I1i in iiIIIII1i1iI :
     Ii1I1i = Ii1I1i . upper ( )
     if eevVeVVeveveveeVev in Ii1I1i :
      try :
       if '<sportsdevil>' in eeveVev : I11II1i ( eeveVev , VeeveVeveee )
       elif '<folder>' in eeveVev : IIIII ( eeveVev )
       elif '<iptv>' in eeveVev : eeeeeeVevee ( eeveVev )
       elif '<image>' in eeveVev : IIiiiiiiIi1I1 ( eeveVev )
       elif '<text>' in eeveVev : I1IIIii ( eeveVev )
       else : iiiiiIIii ( eeveVev , VeeveVeveee )
      except : pass
  except : pass
  if 99 - 99: iii11iiII . i1Ii + iiIiIIi % iii11iiII . i11iIiiIii % i1
def eVVevevV ( name , url , iconimage ) :
 eeeevV = [ ]
 eVeVeveevevVVev = [ ]
 VVVeeevVV = [ ]
 VeveeevVVev = I1i1iiI1 ( url )
 eVeveev = re . compile ( '<title>' + re . escape ( name ) + '</title>(.+?)</item>' , re . DOTALL ) . findall ( VeveeevVVev ) [ 0 ]
 iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( eVeveev ) [ 0 ]
 i1I1iI1iIi111i = [ ]
 if '<link>' in eVeveev :
  iI1Ii11iIiI1 = re . compile ( '<link>(.+?)</link>' ) . findall ( eVeveev )
  for VVevVeeeeveVVevV in iI1Ii11iIiI1 :
   i1I1iI1iIi111i . append ( VVevVeeeeveVVevV )
 if '<sportsdevil>' in eVeveev :
  eevevVev = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( eVeveev )
  for eVVevVevevVeevVeve in eevevVev :
   eVVevVevevVeevVeve = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' + eVVevVevevVeevVeve
   i1I1iI1iIi111i . append ( eVVevVevevVeevVeve )
 iiIii = 1
 for ii1 in i1I1iI1iIi111i :
  I1iIIiiIIi1i = ii1
  if '(' in ii1 :
   ii1 = ii1 . split ( '(' ) [ 0 ]
   VevVeveeVVV = str ( I1iIIiiIIi1i . split ( '(' ) [ 1 ] . replace ( ')' , '' ) )
   eeeevV . append ( ii1 )
   eVeVeveevevVVev . append ( VevVeveeVVV )
  else :
   eVVeevVeveve = ii1 . split ( '/' ) [ 2 ] . replace ( 'www.' , '' )
   eeeevV . append ( ii1 )
   eVeVeveevevVVev . append ( 'Link ' + str ( iiIii ) + ' | ' + eVVeevVeveve )
  iiIii = iiIii + 1
 VeveveV = xbmcgui . Dialog ( )
 eeevevVeveveV = VeveveV . select ( name , eVeVeveevevVVev )
 if eeevevVeveveV < 0 : quit ( )
 else :
  url = eeeevV [ eeevevVeveveV ]
  iIiIIIi ( name , url , iconimage )
  if 8 - 8: eeveevVeeveeeeev
def ii1111iII ( url ) :
 iiiiI = "ShowPicture(%s)" % url
 xbmc . executebuiltin ( iiiiI )
 if 62 - 62: VVeeVVe * IiiIII111iI
def iIiIIIi ( name , url , iconimage ) :
 try :
  if 'plugin://plugin.video.SportsDevil/' in url :
   eVVVeeevVeveV ( name , url , iconimage )
  elif '.ts' in url :
   url = 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;name=' + name + '&amp;url=' + url
   eVVVeeevVeveV ( name , url , iconimage )
  elif urlresolver . HostedMediaFile ( url ) . valid_url ( ) :
   url = urlresolver . HostedMediaFile ( url ) . resolve ( )
   iIII1I111III ( name , url , iconimage )
  elif liveresolver . isValid ( url ) == True :
   url = liveresolver . resolve ( url )
   iIII1I111III ( name , url , iconimage )
  else : iIII1I111III ( name , url , iconimage )
 except :
  II ( I11 ( 'Evolve' ) , 'Stream Unavailable' , '3000' , II1 )
  if 77 - 77: i11IiIiiIIIII * ii1IiI1i
def eeveevVVVeveev ( url ) :
 if urlresolver . HostedMediaFile ( url ) . valid_url ( ) :
  url = urlresolver . HostedMediaFile ( url ) . resolve ( )
 xbmc . Player ( ) . play ( url )
 if 98 - 98: IiiIII111iI % iiIIi1IiIi11 * VVeeVVe
def iIII1I111III ( name , url , iconimage ) :
 Ve = True
 iIIiIi1 = xbmcgui . ListItem ( name , iconImage = iconimage , thumbnailImage = iconimage ) ; iIIiIi1 . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
 Ve = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = url , listitem = iIIiIi1 )
 iIIiIi1 . setPath ( url )
 xbmcplugin . setResolvedUrl ( int ( sys . argv [ 1 ] ) , True , iIIiIi1 )
 if 74 - 74: i1Ii + eVev
def eVVVeeevVeveV ( name , url , iconimage ) :
 Ve = True
 iIIiIi1 = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage ) ; iIIiIi1 . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
 Ve = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = url , listitem = iIIiIi1 )
 xbmc . Player ( ) . play ( url , iIIiIi1 , False )
 if 71 - 71: I1111 % i11IiIiiIIIII
def VeveveVevevevVevV ( url ) :
 xbmc . executebuiltin ( "PlayMedia(%s)" % url )
 if 18 - 18: i1Ii - i11IiIiiIIIII . eVeV . ii1IiI1i
def i1I ( url ) :
 i1i1II = VevVevVVevVevVev . getSetting ( 'layout' )
 if i1i1II == 'Listers' : VevVevVVevVevVev . setSetting ( 'layout' , 'Category' )
 else : VevVevVVevVevVev . setSetting ( 'layout' , 'Listers' )
 xbmc . executebuiltin ( 'Container.Refresh' )
 if 78 - 78: IiiIII111ii * ii1IiI1i . IiiIII111iI / eVev - VVeeVVe / eVeV
def I1i1iiI1 ( url ) :
 i1I1IiiIi1i = urllib2 . Request ( url )
 i1I1IiiIi1i . add_header ( 'User-Agent' , 'mat' )
 iiI11ii1I1 = urllib2 . urlopen ( i1I1IiiIi1i )
 VeveeevVVev = iiI11ii1I1 . read ( )
 iiI11ii1I1 . close ( )
 VeveeevVVev = VeveeevVVev . replace ( '<fanart></fanart>' , '<fanart>x</fanart>' ) . replace ( '<thumbnail></thumbnail>' , '<thumbnail>x</thumbnail>' ) . replace ( '<utube>' , '<link>https://www.youtube.com/watch?v=' ) . replace ( '</utube>' , '</link>' )
 if url <> VVVeev : VeveeevVVev = VeveeevVVev . replace ( '\n' , '' ) . replace ( '\r' , '' )
 return VeveeevVVev
 if 82 - 82: eevV % IiiIII111ii / eeveevVeeveeeeev + I1I1i1 / eVev / eVeV
def eVevevevevVVeevev ( url ) :
 i1I1IiiIi1i = urllib2 . Request ( url )
 i1I1IiiIi1i . add_header ( 'User-Agent' , 'mat' )
 iiI11ii1I1 = urllib2 . urlopen ( i1I1IiiIi1i )
 VeveeevVVev = iiI11ii1I1 . read ( )
 iiI11ii1I1 . close ( )
 return VeveeevVVev
 if 70 - 70: iii11iiII
 if 59 - 59: eVev % iii11iiII
def ii1iI1I11I ( ) :
 II1iI = [ ]
 VeveeveevevVVevevevev = sys . argv [ 2 ]
 if len ( VeveeveevevVVevevevev ) >= 2 :
  VVeee = sys . argv [ 2 ]
  I1i = VVeee . replace ( '?' , '' )
  if ( VVeee [ len ( VVeee ) - 1 ] == '/' ) :
   VVeee = VVeee [ 0 : len ( VVeee ) - 2 ]
  VevevVeee = I1i . split ( '&' )
  II1iI = { }
  for iiIii in range ( len ( VevevVeee ) ) :
   i11I = { }
   i11I = VevevVeee [ iiIii ] . split ( '=' )
   if ( len ( i11I ) ) == 2 :
    II1iI [ i11I [ 0 ] ] = i11I [ 1 ]
 return II1iI
 if 76 - 76: i111I1 * i1Ii
def II ( title , message , ms , nart ) :
 xbmc . executebuiltin ( "XBMC.notification(" + title + "," + message + "," + ms + "," + nart + ")" )
 if 52 - 52: i11IiIiiIIIII
def Ii11iii11I ( string ) :
 iiii1 = re . compile ( '\[(.+?)\]' ) . findall ( string )
 for eeVeveeeVVev in iiii1 : string = string . replace ( eeVeveeeVVev , '' ) . replace ( '[/]' , '' ) . replace ( '[]' , '' )
 return string
 if 71 - 71: eVeV . eevV
def I11 ( string ) :
 string = string . split ( ' ' )
 eeev = ''
 for eVVVeeevev in string :
  iiIiIIIiiI = '[B][COLOR red]' + eVVVeeevev [ 0 ] . upper ( ) + '[/COLOR][COLOR white]' + eVVVeeevev [ 1 : ] + '[/COLOR][/B] '
  eeev = eeev + iiIiIIIiiI
 return eeev
 if 12 - 12: i1 - eVev
def VeveevVevevVeeveev ( name , url , mode , iconimage , itemcount , metatype , isFolder = False ) :
 if eVeveveVe == 'true' :
  name = Ii11iii11I ( name )
  eVeVevevVev = ""
  VVIi1iI111II1I1 = ""
  eVVVVeVVeve = [ ]
  i1II1 = eval ( base64 . b64decode ( 'bWV0YWhhbmRsZXJzLk1ldGFEYXRhKHRtZGJfYXBpX2tleT0iZDk1NWQ4ZjAyYTNmMjQ4MGE1MTg4MWZlNGM5NmYxMGUiKQ==' ) )
  if metatype == 'movie' :
   i11i1 = name . partition ( '(' )
   if len ( i11i1 ) > 0 :
    eVeVevevVev = i11i1 [ 0 ]
    VVIi1iI111II1I1 = i11i1 [ 2 ] . partition ( ')' )
   if len ( VVIi1iI111II1I1 ) > 0 :
    VVIi1iI111II1I1 = VVIi1iI111II1I1 [ 0 ]
   IiiiiI1i1Iii = i1II1 . get_meta ( 'movie' , name = eVeVevevVev , year = VVIi1iI111II1I1 )
   if not IiiiiI1i1Iii [ 'trailer' ] == '' : eVVVVeVVeve . append ( ( I11 ( 'Play Trailer' ) , 'XBMC.RunPlugin(%s)' % VeevVee . build_plugin_url ( { 'mode' : 11 , 'url' : IiiiiI1i1Iii [ 'trailer' ] } ) ) )
  elif metatype == 'tvshow' :
   eVeVevevVev = name . split ( 'Season' ) [ 0 ]
   IiiiiI1i1Iii = i1II1 . get_meta ( 'tvshow' , name = eVeVevevVev )
  elif metatype == 'tvep' :
   eeeveveVeve = re . compile ( 'Season (.+?) Episode (.+?)\)' ) . findall ( name )
   Ii1I1i = VevVevVVevVevVev . getSetting ( 'tv' )
   for iiii111II , I11iIiI1I1i11 in eeeveveVeve :
    IiiiiI1i1Iii = i1II1 . get_episode_meta ( Ii1I1i , imdb_id = '' , season = iiii111II , episode = I11iIiI1I1i11 , air_date = '' , episode_title = '' , overlay = '' )
  VVeeeVeveveeveeev = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&iconimage=" + urllib . quote_plus ( iconimage )
  Ve = True
  iIIiIi1 = xbmcgui . ListItem ( name , iconImage = IiiiiI1i1Iii [ 'cover_url' ] , thumbnailImage = IiiiiI1i1Iii [ 'cover_url' ] )
  iIIiIi1 . setInfo ( type = "Video" , infoLabels = IiiiiI1i1Iii )
  iIIiIi1 . setProperty ( "IsPlayable" , "true" )
  eVVVVeVVeve . append ( ( I11 ( 'Stream Information' ) , 'XBMC.Action(Info)' ) )
  iIIiIi1 . addContextMenuItems ( eVVVVeVVeve , replaceItems = False )
  if not IiiiiI1i1Iii [ 'backdrop_url' ] == '' : iIIiIi1 . setProperty ( 'fanart_image' , IiiiiI1i1Iii [ 'backdrop_url' ] )
  else : iIIiIi1 . setProperty ( 'fanart_image' , iiiii )
  Ve = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = VVeeeVeveveeveeev , listitem = iIIiIi1 , isFolder = isFolder , totalItems = itemcount )
  return Ve
 else : VevevVeveVVevevVevev ( name , url , mode , iconimage , iiiii , description = '' )
 if 61 - 61: iiIIi1IiIi11 / IIIi1i1I % i111I1 + iiIiIIi / eVeV . iiIiIIi
def i1eVVeeevevVevV ( name , url , mode , iconimage , fanart , description = '' ) :
 VVeeeVeveveeveeev = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&fanart=" + urllib . quote_plus ( fanart ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 Ve = True
 iIIiIi1 = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 iIIiIi1 . setInfo ( type = "Video" , infoLabels = { "Title" : name , 'plot' : description } )
 iIIiIi1 . setProperty ( 'fanart_image' , fanart )
 if mode == 12 or mode == 1 :
  eVVVVeVVeve = [ ]
  eVVVVeVVeve . append ( ( I11 ( 'Switch Evolve View' ) , 'XBMC.RunPlugin(%s)' % VeevVee . build_plugin_url ( { 'mode' : 13 , 'url' : 'url' } ) ) )
  iIIiIi1 . addContextMenuItems ( eVVVVeVVeve , replaceItems = False )
 if 'youtube.com/channel/' in url :
  VVeeeVeveveeveeev = 'plugin://plugin.video.youtube/channel/' + description + '/'
 if 'youtube.com/user/' in url :
  VVeeeVeveveeveeev = 'plugin://plugin.video.youtube/user/' + description + '/'
 if 'youtube.com/playlist?' in url :
  VVeeeVeveveeveeev = 'plugin://plugin.video.youtube/playlist/' + description + '/'
 if 'plugin://' in url :
  VVeeeVeveveeveeev = url
 Ve = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = VVeeeVeveveeveeev , listitem = iIIiIi1 , isFolder = True )
 return Ve
 if 12 - 12: I11i + I11i - IIIi1i1I * I1111 % I1111 - eevV
def IIIii1II1II ( name , url , mode , iconimage , fanart , description = '' ) :
 VVeeeVeveveeveeev = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 Ve = True
 iIIiIi1 = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 iIIiIi1 . setProperty ( 'fanart_image' , fanart )
 Ve = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = VVeeeVeveveeveeev , listitem = iIIiIi1 , isFolder = False )
 return Ve
 if 52 - 52: iiIiIIi . i1Ii + eVeV
def VevevVeveVVevevVevev ( name , url , mode , iconimage , fanart , description = '' ) :
 VVeeeVeveveeveeev = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 Ve = True
 iIIiIi1 = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 iIIiIi1 . setProperty ( 'fanart_image' , fanart )
 iIIiIi1 . setProperty ( "IsPlayable" , "true" )
 Ve = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = VVeeeVeveveeveeev , listitem = iIIiIi1 , isFolder = False )
 return Ve
 if 38 - 38: I11i - eevV . eVeV
def iI1Ii11111iIi ( url , name ) :
 eeV = eVevevevevVVeevev ( url )
 if len ( eeV ) > 1 :
  II1I = Veeeeveveve
  Vev = os . path . join ( os . path . join ( II1I , '' ) , name + '.txt' )
  if not os . path . exists ( Vev ) :
   file ( Vev , 'w' ) . close ( )
  eeveevevVVeev = open ( Vev )
  I1IIii1 = eeveevevVVeev . read ( )
  if I1IIii1 == eeV : pass
  else :
   iiIi1IIiIi ( '[B][COLOR red]E[/COLOR][COLOR white]volve[/COLOR][/B] [B][COLOR red]I[/COLOR][COLOR white]nformation[/COLOR][/B]' , eeV )
   i1II1Iiii1I11 = open ( Vev , "w" )
   i1II1Iiii1I11 . write ( eeV )
   i1II1Iiii1I11 . close ( )
   if 95 - 95: eeveevVeeveeeeev % I11i * i11iIiiIii % I1111 - iii11iiII
def iiIi1IIiIi ( heading , text ) :
 id = 10147
 xbmc . executebuiltin ( 'ActivateWindow(%d)' % id )
 xbmc . sleep ( 500 )
 VVeVeVe = xbmcgui . Window ( id )
 eeveveveeeeVeve = 50
 while ( eeveveveeeeVeve > 0 ) :
  try :
   xbmc . sleep ( 10 )
   eeveveveeeeVeve -= 1
   VVeVeVe . getControl ( 1 ) . setLabel ( heading )
   VVeVeVe . getControl ( 5 ) . setText ( text )
   return
  except :
   pass
   if 40 - 40: IIIi1i1I + I11i * i11IiIiiIIIII
def VeveVVeeeVVevV ( name ) :
 global Icon
 global Next
 global Previous
 global window
 global Quit
 global images
 Vev = os . path . join ( os . path . join ( Veeeeveveve , '' ) , name + '.txt' )
 eeveevevVVeev = open ( Vev )
 I1IIii1 = eeveevevVVeev . read ( )
 images = re . compile ( '<image>(.+?)</image>' ) . findall ( I1IIii1 )
 VevVevVVevVevVev . setSetting ( 'pos' , '0' )
 window = pyxbmct . AddonDialogWindow ( '' )
 eeeevevVee = '/resources/art'
 VeeveevVevev = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + VVeve + eeeevevVee , 'next_focus.png' ) )
 ii1I1i11 = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + VVeve + eeeevevVee , 'next1.png' ) )
 VVeevVeveeevVVevV = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + VVeve + eeeevevVee , 'previous_focus.png' ) )
 VVev = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + VVeve + eeeevevVee , 'previous.png' ) )
 eevVeee = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + VVeve + eeeevevVee , 'close_focus.png' ) )
 iiI = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + VVeve + eeeevevVee , 'close.png' ) )
 eV = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + VVeve + eeeevevVee , 'main-bg1.png' ) )
 window . setGeometry ( 1300 , 720 , 100 , 50 )
 IIiIi = pyxbmct . Image ( eV )
 window . placeControl ( IIiIi , - 10 , - 10 , 130 , 70 )
 ii11i1 = '0xFF000000'
 Previous = pyxbmct . Button ( '' , focusTexture = VVeevVeveeevVVevV , noFocusTexture = VVev , textColor = ii11i1 , focusedColor = ii11i1 )
 Next = pyxbmct . Button ( '' , focusTexture = VeeveevVevev , noFocusTexture = ii1I1i11 , textColor = ii11i1 , focusedColor = ii11i1 )
 Quit = pyxbmct . Button ( '' , focusTexture = eevVeee , noFocusTexture = iiI , textColor = ii11i1 , focusedColor = ii11i1 )
 Icon = pyxbmct . Image ( images [ 0 ] , aspectRatio = 1 )
 window . placeControl ( Previous , 102 , 1 , 10 , 10 )
 window . placeControl ( Next , 102 , 40 , 10 , 10 )
 window . placeControl ( Quit , 102 , 21 , 10 , 10 )
 window . placeControl ( Icon , 0 , 0 , 100 , 50 )
 Previous . controlRight ( Next )
 Previous . controlUp ( Quit )
 window . connect ( Previous , VVeVeeVeVVVee )
 window . connect ( Next , Iiii1iI1i )
 Previous . setVisible ( False )
 window . setFocus ( Quit )
 Previous . controlRight ( Quit )
 Quit . controlLeft ( Previous )
 Quit . controlRight ( Next )
 Next . controlLeft ( Quit )
 window . connect ( Quit , window . close )
 window . doModal ( )
 del window
 if 34 - 34: iiIiIIi * IiiIII111iI . I11i * iiIiIIi / iiIiIIi
def Iiii1iI1i ( ) :
 IIiI1Ii = int ( VevVevVVevVevVev . getSetting ( 'pos' ) )
 VevVevVevVe = int ( IIiI1Ii ) + 1
 VevVevVVevVevVev . setSetting ( 'pos' , str ( VevVevVevVe ) )
 VVVVeVeveveevV = len ( images )
 Icon . setImage ( images [ int ( VevVevVevVe ) ] )
 Previous . setVisible ( True )
 if int ( VevVevVevVe ) == int ( VVVVeVeveveevV ) - 1 :
  Next . setVisible ( False )
  if 41 - 41: i11IiIiiIIIII * iiIIi1IiIi11 - i111I1 + eVev
def VVeVeeVeVVVee ( ) :
 IIiI1Ii = int ( VevVevVVevVevVev . getSetting ( 'pos' ) )
 eVVVeevevVevevV = int ( IIiI1Ii ) - 1
 VevVevVVevVevVev . setSetting ( 'pos' , str ( eVVVeevevVevevV ) )
 Icon . setImage ( images [ int ( eVVVeevevVevevV ) ] )
 Next . setVisible ( True )
 if int ( eVVVeevevVevevV ) == 0 :
  Previous . setVisible ( False )
  if 2 - 2: eVev - IIIi1i1I
def eVeevevVeevevV ( link ) :
 try :
  eevVVVe = re . compile ( '<layouttype>(.+?)</layouttype>' ) . findall ( link ) [ 0 ]
  if eevVVVe == 'thumbnail' : xbmc . executebuiltin ( 'Container.SetViewMode(500)' )
  else : xbmc . executebuiltin ( 'Container.SetViewMode(50)' )
 except : pass
 if 11 - 11: ii1IiI1i * ii1IiI1i * IiiIII111iI
VVeee = ii1iI1I11I ( ) ; VeeveVeveee = None ; eevev = None ; eeveeveeveVeveVV = None ; iII1ii1 = None ; eeveVeVeveve = None
try : iII1ii1 = urllib . unquote_plus ( VVeee [ "site" ] )
except : pass
try : VeeveVeveee = urllib . unquote_plus ( VVeee [ "url" ] )
except : pass
try : eevev = urllib . unquote_plus ( VVeee [ "name" ] )
except : pass
try : eeveeveeveVeveVV = int ( VVeee [ "mode" ] )
except : pass
try : eeveVeVeveve = urllib . unquote_plus ( VVeee [ "iconimage" ] )
except : pass
try : iiiii = urllib . unquote_plus ( VVeee [ "fanart" ] )
except : pass
if 12 - 12: i11IiIiiIIIII - iiIiIIi . VVeeVVe / IIIi1i1I . I11i * eeveevVeeveeeeev
try : IiIiII1 = urllib . unquote_plus ( [ "description" ] )
except : pass
if 21 - 21: i1 % i111I1 . IiiIII111iI / eevV + i111I1
if eeveeveeveVeveVV == None or VeeveVeveee == None or len ( VeeveVeveee ) < 1 : IiII ( )
elif eeveeveeveVeveVV == 1 : iI11iiiI1II ( eevev , VeeveVeveee , eeveVeVeveve , iiiii )
elif eeveeveeveVeveVV == 2 : iIiIIIi ( eevev , VeeveVeveee , eeveVeVeveve )
elif eeveeveeveVeveVV == 3 : eVVevevV ( eevev , VeeveVeveee , eeveVeVeveve )
elif eeveeveeveVeveVV == 4 : iIII1I111III ( eevev , VeeveVeveee , eeveVeVeveve )
elif eeveeveeveVeveVV == 5 : eVevVevVVevV ( )
elif eeveeveeveVeveVV == 6 : IIi1I11I1II ( VeeveVeveee , eeveVeVeveve )
elif eeveeveeveVeveVV == 7 : ii1111iII ( VeeveVeveee )
elif eeveeveeveVeveVV == 8 : VeveVVeeeVVevV ( eevev )
elif eeveeveeveVeveVV == 9 : VVeeVVevevev ( eevev , VeeveVeveee )
elif eeveeveeveVeveVV == 10 : I11III1II ( eevev , VeeveVeveee )
elif eeveeveeveVeveVV == 11 : VeveveVevevevVevV ( VeeveVeveee )
elif eeveeveeveVeveVV == 12 : I111I11 ( eevev , VeeveVeveee , eeveVeVeveve , iiiii )
elif eeveeveeveVeveVV == 13 : i1I ( VeeveVeveee )
elif eeveeveeveVeveVV == 14 : i1i ( eevev , VeeveVeveee , eeveVeVeveve )
elif eeveeveeveVeveVV == 15 : iIIIIi1iiIi1 ( eevev , VeeveVeveee , eeveVeVeveve )
elif eeveeveeveVeveVV == 16 : eVVVeeevVeveV ( eevev , VeeveVeveee , eeveVeVeveve )
elif eeveeveeveVeveVV == 17 : eevVeveevVe ( eevev , VeeveVeveee )
if 53 - 53: iii11iiII - IiiIII111iI - iii11iiII * i1Ii
xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3
