import xbmc , xbmcaddon , xbmcgui , xbmcplugin , urllib , urllib2 , os , re , sys , datetime , urlresolver , random , liveresolver , base64 , pyxbmct , net
from resources . lib . common_addon import Addon
from HTMLParser import HTMLParser
from metahandler import metahandlers
from resources . lib . scrape import latesttv
from resources . lib . scrape import latestmovies
if 64 - 64: i11iIiiIii
OO0o = 'plugin.video.Evolve'
Oo0Ooo = Addon ( OO0o , sys . argv )
O0O0OO0O0O0 = xbmcaddon . Addon ( id = OO0o )
iiiii = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o , 'fanart.jpg' ) )
ooo0OO = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o , 'fanart.jpg' ) )
II1 = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o , 'icon.png' ) )
O00ooooo00 = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o + '/resources/art' , 'next.png' ) )
I1IiiI = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o + '/resources/art' , 'close2.png' ) ) ; I1IiiI = open ( I1IiiI , 'r' ) ; I1IiiI = I1IiiI . read ( )
IIi1IiiiI1Ii = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o + '/resources/art' , 'search2.png' ) ) ; IIi1IiiiI1Ii = open ( IIi1IiiiI1Ii , 'r' ) ; IIi1IiiiI1Ii = IIi1IiiiI1Ii . read ( )
I11i11Ii = O0O0OO0O0O0 . getSetting ( 'password' )
oO00oOo = O0O0OO0O0O0 . getSetting ( 'enable_meta' )
OOOo0 = 'http://matsbuilds.uk/private/info.txt'
Oooo000o = xbmc . translatePath ( 'special://home/userdata/addon_data/' + OO0o )
IiIi11iIIi1Ii = os . path . join ( os . path . join ( Oooo000o , '' ) , 'cookie.lwp' )
net = net . Net ( )
if 54 - 54: IIIiiIIii / o0oo0oo0OO00 . iI111iI / oOOo + I1Ii111
def OOo ( ) :
 if not os . path . exists ( Oooo000o ) :
  os . mkdir ( Oooo000o )
 i1i1II ( OOOo0 , 'GlobalCompare' )
 O0oo0OO0 = O0O0OO0O0O0 . getSetting ( 'layout' )
 I1i1iiI1 = re . compile ( '<item>(.+?)</item>' ) . findall ( I1IiiI ) [ 0 ]
 iiIIIII1i1iI = re . compile ( '<title>(.+?)</title>' ) . findall ( I1IiiI ) [ 0 ]
 if O0oo0OO0 == 'Listers' :
  o0oO0 = oo00 ( I1i1iiI1 )
  o00 = re . compile ( '<item>(.+?)</item>' ) . findall ( o0oO0 )
  for Oo0oO0ooo in o00 :
   o0oOoO00o = re . compile ( '<title>(.+?)</title>.+?folder>(.+?)</folder>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>' ) . findall ( Oo0oO0ooo )
   for i1 , oOOoo00O0O , i1111 , iiiii in o0oOoO00o :
    i11 ( i1 , oOOoo00O0O , 1 , i1111 , iiiii )
 else :
  o0oO0 = oo00 ( iiIIIII1i1iI )
  o00 = re . compile ( '&nbsp;</td><td><a href="(.+?)">' ) . findall ( o0oO0 ) [ 1 : ] [ : - 1 ]
  for I11 in o00 :
   i1 = I11 . replace ( '/' , '' ) . replace ( '%20' , ' ' ) . split ( '-' ) [ 1 ]
   Oo0o0000o0o0 = 'Evolve ' + i1
   oOOoo00O0O = baseurl2 + I11
   i1111 = 'http://matsbuilds.uk/pics/evolvecatview/' + i1 . replace ( ' ' , '%20' ) + '.png'
   iiiii = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o , 'fanart.jpg' ) )
   i11 ( oOo0oooo00o ( Oo0o0000o0o0 ) , oOOoo00O0O , 12 , i1111 , iiiii )
 i11 ( '[B][COLOR red]S[/COLOR][COLOR white]earch[/COLOR][/B] [B][COLOR red]E[/COLOR][COLOR white]volve[/COLOR][/B]' , 'url' , 5 , 'http://matsbuilds.uk/pics/evolvecatview/Search.png' , ooo0OO )
 if 65 - 65: O0o * i1iIIII * I1
 xbmc . executebuiltin ( 'Container.SetViewMode(500)' )
 if 54 - 54: oO % IiiIIiiI11 / oooOOOOO * IiiIII111ii / i1iIIi1
def ii11iIi1I ( name , url , iconimage , fanart ) :
 fanart = iconimage
 o0oO0 = oo00 ( url )
 o00 = re . compile ( '&nbsp;</td><td><a href="(.+?)">' ) . findall ( o0oO0 )
 for iI111I11I1I1 in o00 :
  if 'xml' in iI111I11I1I1 :
   name = iI111I11I1I1 . replace ( '.xml' , '' ) . replace ( '%20' , ' ' )
   OOooO0OOoo = name . split ( ' ' ) [ 0 ] . lower ( )
   iIii1 = url + iI111I11I1I1
   iconimage = 'http://matsbuilds.uk/pics/newevolveicons/' + OOooO0OOoo + '.PNG'
   if OOooO0OOoo == 'wraith' : iconimage = 'http://matsbuilds.uk/pics/newevolveicons/' + OOooO0OOoo + '.png'
   i11 ( oOo0oooo00o ( name ) , iIii1 , 1 , iconimage , fanart )
   if 71 - 71: IiI1I1
def OoO000 ( name , url , iconimage , fanart ) :
 IIiiIiI1 = iiIiIIi ( name )
 O0O0OO0O0O0 . setSetting ( 'tv' , IIiiIiI1 )
 o0oO0 = oo00 ( url )
 ooOoo0O ( o0oO0 )
 if '<message>' in o0oO0 :
  OOOo0 = re . compile ( '<message>(.+?)</message>' ) . findall ( o0oO0 ) [ 0 ]
  i1i1II ( OOOo0 , IIiiIiI1 )
 if '<intro>' in o0oO0 :
  OooO0 = re . compile ( '<intro>(.+?)</intro>' ) . findall ( o0oO0 ) [ 0 ]
  II11iiii1Ii ( OooO0 )
 if 'XXX>yes</XXX' in o0oO0 : OO0oOoo ( o0oO0 )
 o00 = re . compile ( '<item>(.+?)</item>' ) . findall ( o0oO0 )
 O0o0Oo = len ( o00 )
 for Oo0oO0ooo in o00 :
  try :
   if '<sportsdevil>' in Oo0oO0ooo : Oo00OOOOO ( Oo0oO0ooo , url )
   elif '<folder>' in Oo0oO0ooo : O0O ( Oo0oO0ooo )
   elif '<iptv>' in Oo0oO0ooo : O00o0OO ( Oo0oO0ooo )
   elif '<image>' in Oo0oO0ooo : I11i1 ( Oo0oO0ooo )
   elif '<text>' in Oo0oO0ooo : iIi1ii1I1 ( Oo0oO0ooo )
   elif '<scraper>' in Oo0oO0ooo : o0 ( Oo0oO0ooo )
   elif '<redirect>' in Oo0oO0ooo : I11II1i ( Oo0oO0ooo )
   elif '<oktitle>' in Oo0oO0ooo : IIIII ( Oo0oO0ooo )
   else : ooooooO0oo ( Oo0oO0ooo , url )
  except : pass
  if 49 - 49: ooo * I1I1i / IIIii1I1 * Ii + oo0O0oOOO00oO
def IIIII ( item ) :
 i1 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 OooOooooOOoo0 = re . compile ( '<oktitle>(.+?)</oktitle>' ) . findall ( item ) [ 0 ]
 o00OO0OOO0 = re . compile ( '<line1>(.+?)</line1>' ) . findall ( item ) [ 0 ]
 oo0 = re . compile ( '<line2>(.+?)</line2>' ) . findall ( item ) [ 0 ]
 o00OooOooo = re . compile ( '<line3>(.+?)</line3>' ) . findall ( item ) [ 0 ]
 O000oo0O = '##' + OooOooooOOoo0 + '#' + o00OO0OOO0 + '#' + oo0 + '#' + o00OooOooo + '##'
 i1111 = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 iiiii = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
 OOOO ( i1 , O000oo0O , 17 , i1111 , iiiii )
 if 10 - 10: i1iIIi1 / O0o * i1iIIi1
def IIIii1II1II ( name , url ) :
 i1I1iI = re . compile ( '##(.+?)##' ) . findall ( url ) [ 0 ] . split ( '#' )
 oo0OooOOo0 = xbmcgui . Dialog ( )
 oo0OooOOo0 . ok ( i1I1iI [ 0 ] , i1I1iI [ 1 ] , i1I1iI [ 2 ] , i1I1iI [ 3 ] )
 if 92 - 92: I1I1i . IiI1I1 + IiiIIiiI11
def I11II1i ( item ) :
 oOOoo00O0O = re . compile ( '<redirect>(.+?)</redirect>' ) . findall ( item ) [ 0 ]
 OoO000 ( 'name' , oOOoo00O0O , 'iconimage' , 'fanart' )
 if 28 - 28: oOOo * i1iIIII - IiiIIiiI11 * IIIii1I1 * ooo / I1
def o0 ( item ) :
 i1 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 i1111 = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 oOOoo00O0O = re . compile ( '<scraper>(.+?)</scraper>' ) . findall ( item ) [ 0 ]
 iiiii = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
 i11 ( i1 , oOOoo00O0O , 10 , i1111 , iiiii )
 if 94 - 94: I1Ii111 % oooOOOOO / oO * o0oo0oo0OO00
def oOOoo0Oo ( name , url ) :
 o00OO00OoO = url
 if 60 - 60: I1 * oO - I1 % iI111iI - oo0O0oOOO00oO + O0o
 if 70 - 70: IIIii1I1 * i1iIIII * IiI1I1 / ooo
 if o00OO00OoO == 'latesttv' :
  oOOOoO0O00o0 = 14
  iII = latesttv . INDEXER ( )
 elif o00OO00OoO == 'latestmovies' :
  oOOOoO0O00o0 = 15
  iII = latestmovies . INDEXER ( )
  if 80 - 80: IIIii1I1 . IiiIII111ii
  if 25 - 25: oO . I1Ii111 / I1I1i . i1iIIi1 * I1 . O0o
 Oo0oOOo = re . compile ( '<item>(.+?)</item>' ) . findall ( iII )
 for Oo0oO0ooo in Oo0oOOo :
  o0oOoO00o = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>' ) . findall ( Oo0oO0ooo )
  O0o0Oo = len ( Oo0oOOo )
  for name , url , i1111 , iiiii in o0oOoO00o :
   if '<meta>' in Oo0oO0ooo :
    Oo0OoO00oOO0o = re . compile ( '<meta>(.+?)</meta>' ) . findall ( Oo0oO0ooo ) [ 0 ]
    OOO00O ( name , url , oOOOoO0O00o0 , i1111 , O0o0Oo , Oo0OoO00oOO0o , isFolder = False )
   else : OOoOO0oo0ooO ( name , url , oOOOoO0O00o0 , i1111 , iiiii )
   if 98 - 98: I1I1i * I1I1i / I1I1i + IiI1I1
   if 34 - 34: oo0O0oOOO00oO
def I1111I1iII11 ( name , url , iconimage ) :
 iII = latesttv . HOSTS ( name , url , iconimage )
 Oooo0O0oo00oO ( name , iII )
 if 14 - 14: oO / IIIii1I1 . oO . IiI1I1 % I1 * IiI1I1
def iIIoO00o0 ( name , url , iconimage ) :
 iII = latestmovies . HOSTS ( name , url , iconimage )
 Oooo0O0oo00oO ( name , iII )
 if 55 - 55: i1iIIII + o0oo0oo0OO00 / oO * IiiIII111ii - i11iIiiIii - ooo
 if 25 - 25: oooOOOOO
def Oooo0O0oo00oO ( title , itemlist ) :
 Ii1i = 1
 I1iiIii = [ ]
 ooo0O = [ ]
 for oOoO0o00OO0 in itemlist :
  i1I1ii = oOoO0o00OO0 . split ( '/' ) [ 2 ] . split ( '.' ) [ 0 ]
  i1 = "Link " + str ( Ii1i ) + ' | ' + i1I1ii
  if i1I1ii != 'www' :
   Ii1i = Ii1i + 1
   I1iiIii . append ( oOoO0o00OO0 )
   ooo0O . append ( i1 )
 title = '[COLOR red]' + title + '[/COLOR]'
 oo0OooOOo0 = xbmcgui . Dialog ( )
 oOOo0 = oo0OooOOo0 . select ( title , ooo0O )
 if oOOo0 < 0 : quit ( )
 else :
  oOOoo00O0O = I1iiIii [ oOOo0 ]
  oo00O00oO ( i1 , oOOoo00O0O , i1111 )
  if 23 - 23: I1 + I1 . i1iIIi1
def iIi1ii1I1 ( item ) :
 i1 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 O000oo0O = re . compile ( '<text>(.+?)</text>' ) . findall ( item ) [ 0 ]
 i1111 = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 iiiii = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
 OOOO ( i1 , O000oo0O , 9 , i1111 , iiiii )
 if 38 - 38: Ii
def Ii1 ( name , url ) :
 OOooOO000 = OOoOoo ( url )
 oO0000OOo00 ( name , OOooOO000 )
 if 27 - 27: O0o % O0o
def I11i1 ( item ) :
 IIiIi1iI = re . compile ( '<image>(.+?)</image>' ) . findall ( item )
 if len ( IIiIi1iI ) == 1 :
  i1 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  i1111 = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  i1IiiiI1iI = re . compile ( '<image>(.+?)</image>' ) . findall ( item ) [ 0 ]
  iiiii = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
  OOOO ( i1 , i1IiiiI1iI , 7 , i1111 , iiiii )
 elif len ( IIiIi1iI ) > 1 :
  i1 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  i1111 = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  iiiii = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
  i1iIi = ''
  for i1IiiiI1iI in IIiIi1iI : i1iIi = i1iIi + '<image>' + i1IiiiI1iI + '</image>'
  ooOOoooooo = Oooo000o
  i1 = iiIiIIi ( i1 )
  II1I = os . path . join ( os . path . join ( ooOOoooooo , '' ) , i1 + '.txt' )
  if not os . path . exists ( II1I ) : file ( II1I , 'w' ) . close ( )
  O0 = open ( II1I , "w" )
  O0 . write ( i1iIi )
  O0 . close ( )
  OOOO ( i1 , 'image' , 8 , i1111 , iiiii )
  if 5 - 5: Ii
def O00o0OO ( item ) :
 i1 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 i1111 = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 oOOoo00O0O = re . compile ( '<iptv>(.+?)</iptv>' ) . findall ( item ) [ 0 ]
 iiiii = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
 i11 ( i1 , oOOoo00O0O , 6 , i1111 , iiiii )
 if 87 - 87: IiI1I1 - o0oo0oo0OO00 + O0o . I1I1i
def Oo0oOOOoOooOo ( url , iconimage ) :
 o0oO0 = OOoOoo ( url )
 O000oo = re . compile ( '^#.+?:-?[0-9]*(.*?),(.*?)\n(.*?)$' , re . I + re . M + re . U + re . S ) . findall ( o0oO0 )
 IIi1I11I1II = [ ]
 for OooOoooOo , i1 , url in O000oo :
  i1 = i1 . replace ( '\n' , '' ) . replace ( '\r' , '' )
  url = url . replace ( '\n' , '' ) . replace ( '\r' , '' )
  ii11IIII11I = { "params" : OooOoooOo , "name" : i1 , "url" : url }
  IIi1I11I1II . append ( ii11IIII11I )
 list = [ ]
 for OOooo in IIi1I11I1II :
  ii11IIII11I = { "name" : OOooo [ "name" ] , "url" : OOooo [ "url" ] }
  O000oo = re . compile ( ' (.+?)="(.+?)"' , re . I + re . M + re . U + re . S ) . findall ( OOooo [ "params" ] )
  for oOooOOOoOo , i1Iii1i1I in O000oo :
   ii11IIII11I [ oOooOOOoOo . strip ( ) . lower ( ) . replace ( '-' , '_' ) ] = i1Iii1i1I . strip ( )
  list . append ( ii11IIII11I )
 for OOooo in list :
  if '.ts' in OOooo [ "url" ] : OOOO ( OOooo [ "name" ] , OOooo [ "url" ] , 2 , iconimage , iiiii )
  else : OOoOO0oo0ooO ( OOooo [ "name" ] , OOooo [ "url" ] , 2 , iconimage , iiiii )
  if 91 - 91: oooOOOOO + O0o . i1iIIi1 * oooOOOOO + O0o * i1iIIII
def ooooooO0oo ( item , url ) :
 O000OOOOOo = re . compile ( '<link>(.+?)</link>' ) . findall ( item )
 o0oOoO00o = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>' ) . findall ( item )
 for i1 , Iiii1i1 , i1111 , iiiii in o0oOoO00o :
  if 'youtube.com/playlist?' in Iiii1i1 :
   OO = Iiii1i1 . split ( 'list=' ) [ 1 ]
   i11 ( i1 , Iiii1i1 , oo000o , i1111 , iiiii , description = OO )
 if len ( O000OOOOOo ) == 1 :
  o0oOoO00o = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>' ) . findall ( item )
  for i1 , url , i1111 , iiiii in o0oOoO00o :
   if '.ts' in url : OOOO ( i1 , url , 16 , i1111 , iiiii , description = '' )
   elif '<meta>' in item :
    Oo0OoO00oOO0o = re . compile ( '<meta>(.+?)</meta>' ) . findall ( item ) [ 0 ]
    OOO00O ( i1 , url , 2 , i1111 , 10 , Oo0OoO00oOO0o , isFolder = False )
   else : OOoOO0oo0ooO ( i1 , url , 2 , i1111 , iiiii )
 elif len ( O000OOOOOo ) > 1 :
  i1 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  i1111 = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  iiiii = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
  if '.ts' in item : OOOO ( i1 , url , 16 , i1111 , iiiii , description = '' )
  elif '<meta>' in item :
   Oo0OoO00oOO0o = re . compile ( '<meta>(.+?)</meta>' ) . findall ( item ) [ 0 ]
   OOO00O ( i1 , url , 3 , i1111 , 80 , Oo0OoO00oOO0o , isFolder = False )
  else : OOoOO0oo0ooO ( i1 , url , 3 , i1111 , iiiii )
  if 44 - 44: oOOo % I1Ii111 + IiI1I1
def O0O ( item ) :
 o0oOoO00o = re . compile ( '<title>(.+?)</title>.+?folder>(.+?)</folder>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>' ) . findall ( item )
 for i1 , oOOoo00O0O , i1111 , iiiii in o0oOoO00o :
  if 'youtube.com/channel/' in oOOoo00O0O :
   OO = oOOoo00O0O . split ( 'channel/' ) [ 1 ]
   i11 ( i1 , oOOoo00O0O , oo000o , i1111 , iiiii , description = OO )
  elif 'youtube.com/user/' in oOOoo00O0O :
   OO = oOOoo00O0O . split ( 'user/' ) [ 1 ]
   i11 ( i1 , oOOoo00O0O , oo000o , i1111 , iiiii , description = OO )
  elif 'youtube.com/playlist?' in oOOoo00O0O :
   OO = oOOoo00O0O . split ( 'list=' ) [ 1 ]
   i11 ( i1 , oOOoo00O0O , oo000o , i1111 , iiiii , description = OO )
  elif 'plugin://' in oOOoo00O0O :
   I1I1I = HTMLParser ( )
   oOOoo00O0O = I1I1I . unescape ( oOOoo00O0O )
   i11 ( i1 , oOOoo00O0O , oo000o , i1111 , iiiii )
  else :
   i11 ( i1 , oOOoo00O0O , 1 , i1111 , iiiii )
   if 95 - 95: I1Ii111 + IiiIIiiI11 + I1I1i * o0oo0oo0OO00 % IiiIII111ii / IIIii1I1
def Oo00OOOOO ( item , url ) :
 O000OOOOOo = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( item )
 o0o0o0oO0oOO = re . compile ( '<link>(.+?)</link>' ) . findall ( item )
 if len ( O000OOOOOo ) + len ( o0o0o0oO0oOO ) == 1 :
  i1 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  i1111 = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  url = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( item ) [ 0 ]
  iiiii = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
  ii1Ii11I = re . compile ( '<referer>(.+?)</referer>' ) . findall ( item ) [ 0 ]
  o0oO0 = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' + urllib . quote ( url )
  url = o0oO0 + '%26referer=' + ii1Ii11I
  OOOO ( i1 , url , 16 , i1111 , iiiii )
 elif len ( O000OOOOOo ) + len ( o0o0o0oO0oOO ) > 1 :
  i1 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  i1111 = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  iiiii = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
  OOOO ( i1 , url , 3 , i1111 , iiiii )
  if 80 - 80: I1Ii111
def OO0oOoo ( link ) :
 if I11i11Ii == '' :
  oo0OooOOo0 = xbmcgui . Dialog ( )
  O0Oi1I1I = oo0OooOOo0 . yesno ( 'Adult Content' , 'You have opted to show adult content' , '' , 'Please set a password to prevent accidental access' , 'Cancel' , 'OK' )
  if O0Oi1I1I == 1 :
   iiI1I = xbmc . Keyboard ( '' , 'Set Password' )
   iiI1I . doModal ( )
   if ( iiI1I . isConfirmed ( ) ) :
    IiIiiIIiI = iiI1I . getText ( )
    O0O0OO0O0O0 . setSetting ( 'password' , IiIiiIIiI )
  else : quit ( )
 elif I11i11Ii <> '' :
  oo0OooOOo0 = xbmcgui . Dialog ( )
  O0Oi1I1I = oo0OooOOo0 . yesno ( 'Adult Content' , 'Please enter the password you set' , 'to continue' , '' , 'Cancel' , 'OK' )
  if O0Oi1I1I == 1 :
   iiI1I = xbmc . Keyboard ( '' , 'Enter Password' )
   iiI1I . doModal ( )
   if ( iiI1I . isConfirmed ( ) ) :
    IiIiiIIiI = iiI1I . getText ( )
   if IiIiiIIiI <> I11i11Ii :
    quit ( )
  else : quit ( )
  if 67 - 67: oo0O0oOOO00oO
def I1IIII1i ( ) :
 iiI1I = xbmc . Keyboard ( '' , '[COLOR red]S[/COLOR][COLOR white]earch[/COLOR] [COLOR red]E[/COLOR][COLOR white]volve[/COLOR]' )
 iiI1I . doModal ( )
 if ( iiI1I . isConfirmed ( ) ) :
  OO = iiI1I . getText ( )
  OO = OO . upper ( )
 else : quit ( )
 o0oO0 = oo00 ( 'http://matsbuilds.uk/search/search.xml' )
 I1I11i = re . compile ( '<link>(.+?)</link>' ) . findall ( o0oO0 )
 for oOOoo00O0O in I1I11i :
  try :
   o0oO0 = oo00 ( oOOoo00O0O )
   Ii1I1I1i1Ii = re . compile ( '<item>(.+?)</item>' ) . findall ( o0oO0 )
   for Oo0oO0ooo in Ii1I1I1i1Ii :
    o00 = re . compile ( '<title>(.+?)</title>' ) . findall ( Oo0oO0ooo )
    for i1Oo0oO00o in o00 :
     i1Oo0oO00o = i1Oo0oO00o . upper ( )
     if OO in i1Oo0oO00o :
      try :
       if '<sportsdevil>' in Oo0oO0ooo : Oo00OOOOO ( Oo0oO0ooo , oOOoo00O0O )
       elif '<folder>' in Oo0oO0ooo : O0O ( Oo0oO0ooo )
       elif '<iptv>' in Oo0oO0ooo : O00o0OO ( Oo0oO0ooo )
       elif '<image>' in Oo0oO0ooo : I11i1 ( Oo0oO0ooo )
       elif '<text>' in Oo0oO0ooo : iIi1ii1I1 ( Oo0oO0ooo )
       else : ooooooO0oo ( Oo0oO0ooo , oOOoo00O0O )
      except : pass
  except : pass
  if 13 - 13: IiI1I1 * i1iIIII * oo0O0oOOO00oO
def iI11iI1IiiIiI ( name , url , iconimage ) :
 I1iiIii = [ ]
 ooo0O = [ ]
 Ii1I1i = [ ]
 o0oO0 = oo00 ( url )
 OOI1iI1ii1II = re . compile ( '<title>' + re . escape ( name ) + '</title>(.+?)</item>' , re . DOTALL ) . findall ( o0oO0 ) [ 0 ]
 iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( OOI1iI1ii1II ) [ 0 ]
 O000OOOOOo = [ ]
 if '<link>' in OOI1iI1ii1II :
  O0O0OOOOoo = re . compile ( '<link>(.+?)</link>' ) . findall ( OOI1iI1ii1II )
  for oOooO0 in O0O0OOOOoo :
   O000OOOOOo . append ( oOooO0 )
 if '<sportsdevil>' in OOI1iI1ii1II :
  Ii1I1Ii = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( OOI1iI1ii1II )
  for OOoO0 in Ii1I1Ii :
   OOoO0 = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' + urllib . quote ( OOoO0 )
   O000OOOOOo . append ( OOoO0 )
 Ii1i = 1
 for OO0Oooo0oOO0O in O000OOOOOo :
  o00O0 = OO0Oooo0oOO0O
  if '(' in OO0Oooo0oOO0O :
   OO0Oooo0oOO0O = OO0Oooo0oOO0O . split ( '(' ) [ 0 ]
   oOO0O00Oo0O0o = str ( o00O0 . split ( '(' ) [ 1 ] . replace ( ')' , '' ) )
   I1iiIii . append ( OO0Oooo0oOO0O )
   ooo0O . append ( oOO0O00Oo0O0o )
  else :
   ii1 = OO0Oooo0oOO0O . split ( '/' ) [ 2 ] . replace ( 'www.' , '' )
   I1iiIii . append ( OO0Oooo0oOO0O )
   ooo0O . append ( 'Link ' + str ( Ii1i ) + ' | ' + ii1 )
  Ii1i = Ii1i + 1
 oo0OooOOo0 = xbmcgui . Dialog ( )
 oOOo0 = oo0OooOOo0 . select ( name , ooo0O )
 if oOOo0 < 0 : quit ( )
 else :
  url = I1iiIii [ oOOo0 ]
  oo00O00oO ( name , url , iconimage )
  if 35 - 35: I1I1i * IiiIII111ii / o0oo0oo0OO00 - IiiIIiiI11 / iI111iI - Ii
def II1I1iiIII ( url ) :
 oOOo0O00o = "ShowPicture(%s)" % url
 xbmc . executebuiltin ( oOOo0O00o )
 if 8 - 8: I1
def oo00O00oO ( name , url , iconimage ) :
 try :
  if 'plugin://plugin.video.SportsDevil/' in url :
   ii1111iII ( name , url , iconimage )
  elif '.ts' in url :
   url = 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;name=' + urllib . quote ( name ) + '&amp;url=' + urllib . quote ( url )
   ii1111iII ( name , url , iconimage )
  elif urlresolver . HostedMediaFile ( url ) . valid_url ( ) :
   url = urlresolver . HostedMediaFile ( url ) . resolve ( )
   iiiiI ( name , url , iconimage )
  elif liveresolver . isValid ( url ) == True :
   url = liveresolver . resolve ( url )
   iiiiI ( name , url , iconimage )
  else : iiiiI ( name , url , iconimage )
 except :
  oooOo0OOOoo0 ( oOo0oooo00o ( 'Evolve' ) , 'Stream Unavailable' , '3000' , II1 )
  if 51 - 51: i1iIIII / oO . i1iIIi1 * IiiIIiiI11 + I1 * IIIii1I1
def II11iiii1Ii ( url ) :
 if urlresolver . HostedMediaFile ( url ) . valid_url ( ) :
  url = urlresolver . HostedMediaFile ( url ) . resolve ( )
 xbmc . Player ( ) . play ( url )
 if 73 - 73: I1 + iI111iI - IIIiiIIii - ooo - I1Ii111
def iiiiI ( name , url , iconimage ) :
 O0Oo0oOOoooOOOOo = True
 o0oO0O0o0O00O = xbmcgui . ListItem ( name , iconImage = iconimage , thumbnailImage = iconimage ) ; o0oO0O0o0O00O . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
 O0Oo0oOOoooOOOOo = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = url , listitem = o0oO0O0o0O00O )
 o0oO0O0o0O00O . setPath ( url )
 xbmcplugin . setResolvedUrl ( int ( sys . argv [ 1 ] ) , True , o0oO0O0o0O00O )
 if 80 - 80: i11iIiiIii % oo0O0oOOO00oO + ooo % IiI1I1 - oooOOOOO
def ii1111iII ( name , url , iconimage ) :
 O0Oo0oOOoooOOOOo = True
 o0oO0O0o0O00O = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage ) ; o0oO0O0o0O00O . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
 O0Oo0oOOoooOOOOo = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = url , listitem = o0oO0O0o0O00O )
 xbmc . Player ( ) . play ( url , o0oO0O0o0O00O , False )
 if 18 - 18: I1I1i - i1iIIi1 . Ii . o0oo0oo0OO00
def i1I ( url ) :
 xbmc . executebuiltin ( "PlayMedia(%s)" % url )
 if 78 - 78: IiI1I1 * o0oo0oo0OO00 . O0o / IiiIIiiI11 - iI111iI / Ii
def i1I1IiiIi1i ( url ) :
 O0oo0OO0 = O0O0OO0O0O0 . getSetting ( 'layout' )
 if O0oo0OO0 == 'Listers' : O0O0OO0O0O0 . setSetting ( 'layout' , 'Category' )
 else : O0O0OO0O0O0 . setSetting ( 'layout' , 'Listers' )
 xbmc . executebuiltin ( 'Container.Refresh' )
 if 29 - 29: O0o % O0o
def oo00 ( url ) :
 Oo0O0 = urllib2 . Request ( url )
 Oo0O0 . add_header ( 'User-Agent' , 'mat' )
 Ooo0OOoOoO0 = urllib2 . urlopen ( Oo0O0 )
 o0oO0 = Ooo0OOoOoO0 . read ( )
 Ooo0OOoOoO0 . close ( )
 if '{' in o0oO0 : o0oO0 = o0oO0 [ : : - 1 ] ; o0oO0 = o0oO0 . replace ( '}' , '' ) . replace ( '{' , '' ) . replace ( ',' , '' ) . replace ( ']' , '' ) . replace ( '[' , '' ) ; o0oO0 = o0oO0 + '==' ; o0oO0 = o0oO0 . decode ( 'base64' )
 o0oO0 = o0oO0 . replace ( '<fanart></fanart>' , '<fanart>x</fanart>' ) . replace ( '<thumbnail></thumbnail>' , '<thumbnail>x</thumbnail>' ) . replace ( '<utube>' , '<link>https://www.youtube.com/watch?v=' ) . replace ( '</utube>' , '</link>' )
 if url <> OOOo0 : o0oO0 = o0oO0 . replace ( '\n' , '' ) . replace ( '\r' , '' )
 return o0oO0
 if 70 - 70: IiiIII111ii
def OOoOoo ( url ) :
 Oo0O0 = urllib2 . Request ( url )
 Oo0O0 . add_header ( 'User-Agent' , 'mat' )
 Ooo0OOoOoO0 = urllib2 . urlopen ( Oo0O0 )
 o0oO0 = Ooo0OOoOoO0 . read ( )
 Ooo0OOoOoO0 . close ( )
 return o0oO0
 if 59 - 59: IiiIIiiI11 % IiiIII111ii
 if 6 - 6: o0oo0oo0OO00 % i11iIiiIii % oooOOOOO
def o0Oo0oO0oOO00 ( ) :
 oo00OO0000oO = [ ]
 I1II1 = sys . argv [ 2 ]
 if len ( I1II1 ) >= 2 :
  OooOoooOo = sys . argv [ 2 ]
  oooO = OooOoooOo . replace ( '?' , '' )
  if ( OooOoooOo [ len ( OooOoooOo ) - 1 ] == '/' ) :
   OooOoooOo = OooOoooOo [ 0 : len ( OooOoooOo ) - 2 ]
  i1I1i111Ii = oooO . split ( '&' )
  oo00OO0000oO = { }
  for Ii1i in range ( len ( i1I1i111Ii ) ) :
   oooi1i1iI1iiiI = { }
   oooi1i1iI1iiiI = i1I1i111Ii [ Ii1i ] . split ( '=' )
   if ( len ( oooi1i1iI1iiiI ) ) == 2 :
    oo00OO0000oO [ oooi1i1iI1iiiI [ 0 ] ] = oooi1i1iI1iiiI [ 1 ]
 return oo00OO0000oO
 if 51 - 51: O0o % Ii . IiiIII111ii / o0oo0oo0OO00 / IiI1I1 . IiiIII111ii
def oooOo0OOOoo0 ( title , message , ms , nart ) :
 xbmc . executebuiltin ( "XBMC.notification(" + title + "," + message + "," + ms + "," + nart + ")" )
 if 42 - 42: IiiIIiiI11 + oOOo - ooo / IIIii1I1
def iiIiIIi ( string ) :
 iiIiIIIiiI = re . compile ( '\[(.+?)\]' ) . findall ( string )
 for iiI1IIIi in iiIiIIIiiI : string = string . replace ( iiI1IIIi , '' ) . replace ( '[/]' , '' ) . replace ( '[]' , '' )
 return string
 if 47 - 47: i1iIIII % IiI1I1 % i11iIiiIii - IIIiiIIii + oo0O0oOOO00oO
def oOo0oooo00o ( string ) :
 string = string . split ( ' ' )
 ooO000OO0O00O = ''
 for OOOoOO0o in string :
  i1II1 = '[B][COLOR red]' + OOOoOO0o [ 0 ] . upper ( ) + '[/COLOR][COLOR white]' + OOOoOO0o [ 1 : ] + '[/COLOR][/B] '
  ooO000OO0O00O = ooO000OO0O00O + i1II1
 return ooO000OO0O00O
 if 25 - 25: Ii / o0oo0oo0OO00 % I1I1i
def OOO00O ( name , url , mode , iconimage , itemcount , metatype , isFolder = False ) :
 if oO00oOo == 'true' :
  name = iiIiIIi ( name )
  IiiiiI1i1Iii = ""
  oo00oO0o = ""
  iiii111II = [ ]
  I11iIiI1I1i11 = eval ( base64 . b64decode ( 'bWV0YWhhbmRsZXJzLk1ldGFEYXRhKHRtZGJfYXBpX2tleT0iZDk1NWQ4ZjAyYTNmMjQ4MGE1MTg4MWZlNGM5NmYxMGUiKQ==' ) )
  if metatype == 'movie' :
   OOoooO00o0oo0 = name . partition ( '(' )
   if len ( OOoooO00o0oo0 ) > 0 :
    IiiiiI1i1Iii = OOoooO00o0oo0 [ 0 ]
    oo00oO0o = OOoooO00o0oo0 [ 2 ] . partition ( ')' )
   if len ( oo00oO0o ) > 0 :
    oo00oO0o = oo00oO0o [ 0 ]
   O00O = I11iIiI1I1i11 . get_meta ( 'movie' , name = IiiiiI1i1Iii , year = oo00oO0o )
   if not O00O [ 'trailer' ] == '' : iiii111II . append ( ( oOo0oooo00o ( 'Play Trailer' ) , 'XBMC.RunPlugin(%s)' % Oo0Ooo . build_plugin_url ( { 'mode' : 11 , 'url' : O00O [ 'trailer' ] } ) ) )
  elif metatype == 'tvshow' :
   IiiiiI1i1Iii = name . split ( 'Season' ) [ 0 ]
   O00O = I11iIiI1I1i11 . get_meta ( 'tvshow' , name = IiiiiI1i1Iii )
  elif metatype == 'tvep' :
   I1i11 = re . compile ( 'Season (.+?) Episode (.+?)\)' ) . findall ( name )
   i1Oo0oO00o = O0O0OO0O0O0 . getSetting ( 'tv' )
   for IiIi1I1 , IiIIi1 in I1i11 :
    O00O = I11iIiI1I1i11 . get_episode_meta ( i1Oo0oO00o , imdb_id = '' , season = IiIi1I1 , episode = IiIIi1 , air_date = '' , episode_title = '' , overlay = '' )
  IIIIiii1IIii = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&iconimage=" + urllib . quote_plus ( iconimage )
  O0Oo0oOOoooOOOOo = True
  o0oO0O0o0O00O = xbmcgui . ListItem ( name , iconImage = O00O [ 'cover_url' ] , thumbnailImage = O00O [ 'cover_url' ] )
  o0oO0O0o0O00O . setInfo ( type = "Video" , infoLabels = O00O )
  o0oO0O0o0O00O . setProperty ( "IsPlayable" , "true" )
  iiii111II . append ( ( oOo0oooo00o ( 'Stream Information' ) , 'XBMC.Action(Info)' ) )
  o0oO0O0o0O00O . addContextMenuItems ( iiii111II , replaceItems = False )
  if not O00O [ 'backdrop_url' ] == '' : o0oO0O0o0O00O . setProperty ( 'fanart_image' , O00O [ 'backdrop_url' ] )
  else : o0oO0O0o0O00O . setProperty ( 'fanart_image' , iiiii )
  O0Oo0oOOoooOOOOo = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = IIIIiii1IIii , listitem = o0oO0O0o0O00O , isFolder = isFolder , totalItems = itemcount )
  return O0Oo0oOOoooOOOOo
 else : OOoOO0oo0ooO ( name , url , mode , iconimage , iiiii , description = '' )
 if 38 - 38: i1iIIi1 + I1Ii111 % oo0O0oOOO00oO % oO - ooo / iI111iI
def i11 ( name , url , mode , iconimage , fanart , description = '' ) :
 IIIIiii1IIii = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&fanart=" + urllib . quote_plus ( fanart ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 O0Oo0oOOoooOOOOo = True
 o0oO0O0o0O00O = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 o0oO0O0o0O00O . setInfo ( type = "Video" , infoLabels = { "Title" : name , 'plot' : description } )
 o0oO0O0o0O00O . setProperty ( 'fanart_image' , fanart )
 if mode == 12 or mode == 1 :
  iiii111II = [ ]
  iiii111II . append ( ( oOo0oooo00o ( 'Switch Evolve View' ) , 'XBMC.RunPlugin(%s)' % Oo0Ooo . build_plugin_url ( { 'mode' : 13 , 'url' : 'url' } ) ) )
  o0oO0O0o0O00O . addContextMenuItems ( iiii111II , replaceItems = False )
 if 'youtube.com/channel/' in url :
  IIIIiii1IIii = 'plugin://plugin.video.youtube/channel/' + description + '/'
 if 'youtube.com/user/' in url :
  IIIIiii1IIii = 'plugin://plugin.video.youtube/user/' + description + '/'
 if 'youtube.com/playlist?' in url :
  IIIIiii1IIii = 'plugin://plugin.video.youtube/playlist/' + description + '/'
 if 'plugin://' in url :
  IIIIiii1IIii = url
 O0Oo0oOOoooOOOOo = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = IIIIiii1IIii , listitem = o0oO0O0o0O00O , isFolder = True )
 return O0Oo0oOOoooOOOOo
 if 73 - 73: IiiIIiiI11 * IIIiiIIii - i11iIiiIii
def OOOO ( name , url , mode , iconimage , fanart , description = '' ) :
 IIIIiii1IIii = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 O0Oo0oOOoooOOOOo = True
 o0oO0O0o0O00O = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 o0oO0O0o0O00O . setProperty ( 'fanart_image' , fanart )
 O0Oo0oOOoooOOOOo = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = IIIIiii1IIii , listitem = o0oO0O0o0O00O , isFolder = False )
 return O0Oo0oOOoooOOOOo
 if 85 - 85: ooo % I1I1i + IiI1I1 / IiiIIiiI11 . IiiIII111ii + i1iIIi1
def OOoOO0oo0ooO ( name , url , mode , iconimage , fanart , description = '' ) :
 IIIIiii1IIii = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 O0Oo0oOOoooOOOOo = True
 o0oO0O0o0O00O = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 o0oO0O0o0O00O . setProperty ( 'fanart_image' , fanart )
 o0oO0O0o0O00O . setProperty ( "IsPlayable" , "true" )
 O0Oo0oOOoooOOOOo = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = IIIIiii1IIii , listitem = o0oO0O0o0O00O , isFolder = False )
 return O0Oo0oOOoooOOOOo
 if 62 - 62: i11iIiiIii + i11iIiiIii - IiiIIiiI11
def i1i1II ( url , name ) :
 I1OooooO0oOOOO = OOoOoo ( url )
 if len ( I1OooooO0oOOOO ) > 1 :
  ooOOoooooo = Oooo000o
  II1I = os . path . join ( os . path . join ( ooOOoooooo , '' ) , name + '.txt' )
  if not os . path . exists ( II1I ) :
   file ( II1I , 'w' ) . close ( )
  o0O00oOOoo = open ( II1I )
  i1I1iIi = o0O00oOOoo . read ( )
  if i1I1iIi == I1OooooO0oOOOO : pass
  else :
   oO0000OOo00 ( '[B][COLOR red]E[/COLOR][COLOR white]volve[/COLOR][/B] [B][COLOR red]I[/COLOR][COLOR white]nformation[/COLOR][/B]' , I1OooooO0oOOOO )
   O0 = open ( II1I , "w" )
   O0 . write ( I1OooooO0oOOOO )
   O0 . close ( )
   if 22 - 22: oO * IIIiiIIii . IIIii1I1 * i11iIiiIii - O0o * oo0O0oOOO00oO
def oO0000OOo00 ( heading , text ) :
 id = 10147
 xbmc . executebuiltin ( 'ActivateWindow(%d)' % id )
 xbmc . sleep ( 500 )
 OOooo0O0o0 = xbmcgui . Window ( id )
 II1iI1I11I = 50
 while ( II1iI1I11I > 0 ) :
  try :
   xbmc . sleep ( 10 )
   II1iI1I11I -= 1
   OOooo0O0o0 . getControl ( 1 ) . setLabel ( heading )
   OOooo0O0o0 . getControl ( 5 ) . setText ( text )
   return
  except :
   pass
   if 78 - 78: I1Ii111
def o0O0Oo ( name ) :
 global Icon
 global Next
 global Previous
 global window
 global Quit
 global images
 II1I = os . path . join ( os . path . join ( Oooo000o , '' ) , name + '.txt' )
 o0O00oOOoo = open ( II1I )
 i1I1iIi = o0O00oOOoo . read ( )
 images = re . compile ( '<image>(.+?)</image>' ) . findall ( i1I1iIi )
 O0O0OO0O0O0 . setSetting ( 'pos' , '0' )
 window = pyxbmct . AddonDialogWindow ( '' )
 Ooo0O0oooo = '/resources/art'
 iiI = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o + Ooo0O0oooo , 'next_focus.png' ) )
 oOIIiIi = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o + Ooo0O0oooo , 'next1.png' ) )
 OOoOooOoOOOoo = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o + Ooo0O0oooo , 'previous_focus.png' ) )
 Iiii1iI1i = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o + Ooo0O0oooo , 'previous.png' ) )
 I1ii1ii11i1I = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o + Ooo0O0oooo , 'close_focus.png' ) )
 o0OoOO = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o + Ooo0O0oooo , 'close.png' ) )
 O0O0Oo00 = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o + Ooo0O0oooo , 'main-bg1.png' ) )
 window . setGeometry ( 1300 , 720 , 100 , 50 )
 oOoO00o = pyxbmct . Image ( O0O0Oo00 )
 window . placeControl ( oOoO00o , - 10 , - 10 , 130 , 70 )
 O000oo0O = '0xFF000000'
 Previous = pyxbmct . Button ( '' , focusTexture = OOoOooOoOOOoo , noFocusTexture = Iiii1iI1i , textColor = O000oo0O , focusedColor = O000oo0O )
 Next = pyxbmct . Button ( '' , focusTexture = iiI , noFocusTexture = oOIIiIi , textColor = O000oo0O , focusedColor = O000oo0O )
 Quit = pyxbmct . Button ( '' , focusTexture = I1ii1ii11i1I , noFocusTexture = o0OoOO , textColor = O000oo0O , focusedColor = O000oo0O )
 Icon = pyxbmct . Image ( images [ 0 ] , aspectRatio = 1 )
 window . placeControl ( Previous , 102 , 1 , 10 , 10 )
 window . placeControl ( Next , 102 , 40 , 10 , 10 )
 window . placeControl ( Quit , 102 , 21 , 10 , 10 )
 window . placeControl ( Icon , 0 , 0 , 100 , 50 )
 Previous . controlRight ( Next )
 Previous . controlUp ( Quit )
 window . connect ( Previous , oO00O0 )
 window . connect ( Next , IIi1IIIi )
 Previous . setVisible ( False )
 window . setFocus ( Quit )
 Previous . controlRight ( Quit )
 Quit . controlLeft ( Previous )
 Quit . controlRight ( Next )
 Next . controlLeft ( Quit )
 window . connect ( Quit , window . close )
 window . doModal ( )
 del window
 if 99 - 99: ooo + I1 * I1Ii111 . IiiIIiiI11 - oooOOOOO
def IIi1IIIi ( ) :
 o0OOOo = int ( O0O0OO0O0O0 . getSetting ( 'pos' ) )
 ii1iiIiIII1ii = int ( o0OOOo ) + 1
 O0O0OO0O0O0 . setSetting ( 'pos' , str ( ii1iiIiIII1ii ) )
 oO0o0oooO0oO = len ( images )
 Icon . setImage ( images [ int ( ii1iiIiIII1ii ) ] )
 Previous . setVisible ( True )
 if int ( ii1iiIiIII1ii ) == int ( oO0o0oooO0oO ) - 1 :
  Next . setVisible ( False )
  if 19 - 19: i11iIiiIii + iI111iI - i1iIIII - IiI1I1
def oO00O0 ( ) :
 o0OOOo = int ( O0O0OO0O0O0 . getSetting ( 'pos' ) )
 Iii1iiIi1II = int ( o0OOOo ) - 1
 O0O0OO0O0O0 . setSetting ( 'pos' , str ( Iii1iiIi1II ) )
 Icon . setImage ( images [ int ( Iii1iiIi1II ) ] )
 Next . setVisible ( True )
 if int ( Iii1iiIi1II ) == 0 :
  Previous . setVisible ( False )
  if 60 - 60: O0o - IiiIII111ii * IiI1I1 % I1Ii111
def ooOoo0O ( link ) :
 try :
  oooIIiIiI1I = re . compile ( '<layouttype>(.+?)</layouttype>' ) . findall ( link ) [ 0 ]
  if oooIIiIiI1I == 'thumbnail' : xbmc . executebuiltin ( 'Container.SetViewMode(500)' )
  else : xbmc . executebuiltin ( 'Container.SetViewMode(50)' )
 except : pass
 if 100 - 100: o0oo0oo0OO00 + oO / i1iIIII . i11iIiiIii
OooOoooOo = o0Oo0oO0oOO00 ( ) ; oOOoo00O0O = None ; i1 = None ; oo000o = None ; III1I1Iii1iiI = None ; i1111 = None
try : III1I1Iii1iiI = urllib . unquote_plus ( OooOoooOo [ "site" ] )
except : pass
try : oOOoo00O0O = urllib . unquote_plus ( OooOoooOo [ "url" ] )
except : pass
try : i1 = urllib . unquote_plus ( OooOoooOo [ "name" ] )
except : pass
try : oo000o = int ( OooOoooOo [ "mode" ] )
except : pass
try : i1111 = urllib . unquote_plus ( OooOoooOo [ "iconimage" ] )
except : pass
try : iiiii = urllib . unquote_plus ( OooOoooOo [ "fanart" ] )
except : pass
if 17 - 17: ooo % o0oo0oo0OO00 - o0oo0oo0OO00
try : O0o0O0 = urllib . unquote_plus ( [ "description" ] )
except : pass
if 11 - 11: I1Ii111 % I1 * I1I1i + oo0O0oOOO00oO + ooo
if oo000o == None or oOOoo00O0O == None or len ( oOOoo00O0O ) < 1 : OOo ( )
elif oo000o == 1 : OoO000 ( i1 , oOOoo00O0O , i1111 , iiiii )
elif oo000o == 2 : oo00O00oO ( i1 , oOOoo00O0O , i1111 )
elif oo000o == 3 : iI11iI1IiiIiI ( i1 , oOOoo00O0O , i1111 )
elif oo000o == 4 : iiiiI ( i1 , oOOoo00O0O , i1111 )
elif oo000o == 5 : I1IIII1i ( )
elif oo000o == 6 : Oo0oOOOoOooOo ( oOOoo00O0O , i1111 )
elif oo000o == 7 : II1I1iiIII ( oOOoo00O0O )
elif oo000o == 8 : o0O0Oo ( i1 )
elif oo000o == 9 : Ii1 ( i1 , oOOoo00O0O )
elif oo000o == 10 : oOOoo0Oo ( i1 , oOOoo00O0O )
elif oo000o == 11 : i1I ( oOOoo00O0O )
elif oo000o == 12 : ii11iIi1I ( i1 , oOOoo00O0O , i1111 , iiiii )
elif oo000o == 13 : i1I1IiiIi1i ( oOOoo00O0O )
elif oo000o == 14 : I1111I1iII11 ( i1 , oOOoo00O0O , i1111 )
elif oo000o == 15 : iIIoO00o0 ( i1 , oOOoo00O0O , i1111 )
elif oo000o == 16 : ii1111iII ( i1 , oOOoo00O0O , i1111 )
elif oo000o == 17 : IIIii1II1II ( i1 , oOOoo00O0O )
if 24 - 24: i1iIIII - IiiIII111ii % o0oo0oo0OO00 . oOOo / IIIiiIIii
xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3
