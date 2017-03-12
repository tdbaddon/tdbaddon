# -*- coding: utf-8 -*-
import xbmc , xbmcaddon , xbmcgui , xbmcplugin , urllib , urllib2 , os , re , sys , datetime , urlresolver , random , liveresolver , base64 , pyxbmct , glob , net
from resources . lib . common_addon import Addon
from HTMLParser import HTMLParser
from metahandler import metahandlers
from resources . lib import mamahd
from resources . lib import crickfree
from resources . lib import bigsports
from resources . lib import hergundizi
from resources . lib import tv
if 64 - 64: i11iIiiIii
if 65 - 65: O0 / iIii1I11I1II1 % OoooooooOO - i1IIi
if 73 - 73: II111iiii
IiII1IiiIiI1 = 'plugin.video.ukturk'
iIiiiI1IiI1I1 = Addon ( IiII1IiiIiI1 , sys . argv )
o0OoOoOO00 = xbmcaddon . Addon ( id = IiII1IiiIiI1 )
I11i = xbmc . translatePath ( o0OoOoOO00 . getAddonInfo ( 'profile' ) )
O0O = xbmc . translatePath ( 'special://home/addons/' ) + '/*.*'
Oo = xbmc . translatePath ( 'special://home/addons/' )
I1ii11iIi11i = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + IiII1IiiIiI1 , 'fanart.jpg' ) )
I1IiI = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + IiII1IiiIiI1 , 'fanart.jpg' ) )
o0OOO = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + IiII1IiiIiI1 , 'icon.png' ) )
iIiiiI = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + IiII1IiiIiI1 , 'next.png' ) )
Iii1ii1II11i = o0OoOoOO00 . getSetting ( 'adult' )
iI111iI = o0OoOoOO00 . getSetting ( 'password' )
IiII = int ( o0OoOoOO00 . getSetting ( 'count' ) )
iI1Ii11111iIi = o0OoOoOO00 . getSetting ( 'enable_meta' )
i1i1II = xbmc . translatePath ( 'special://home/userdata/addon_data/' + IiII1IiiIiI1 )
O0oo0OO0 = xbmc . translatePath ( os . path . join ( 'special://home/userdata/Database' , 'UKTurk.db' ) )
I1i1iiI1 = 'http://ukturk.offshorepastebin.com/ukturk2.jpg'
iiIIIII1i1iI = 'https://www.googleapis.com/youtube/v3/search?q='
o0oO0 = '&regionCode=US&part=snippet&hl=en_US&key=AIzaSyAd-YEOqZz9nXVzGtn3KWzYLbLaajhqIDA&type=video&maxResults=50'
oo00 = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId='
o00 = '&maxResults=50&key=AIzaSyAd-YEOqZz9nXVzGtn3KWzYLbLaajhqIDA'
Oo0oO0ooo = open ( O0oo0OO0 , 'a' )
Oo0oO0ooo . close ( )
net = net . Net ( )
if 56 - 56: ooO00oOoo - O0OOo
def II1Iiii1111i ( ) :
 o0OoOoOO00 . setSetting ( 'fav' , 'no' )
 if not os . path . exists ( i1i1II ) :
  os . mkdir ( i1i1II )
 i1IIi11111i = o000o0o00o0Oo ( I1i1iiI1 )
 oo = re . compile ( '<index>(.+?)</index>' ) . findall ( i1IIi11111i ) [ 0 ]
 i1IIi11111i = o000o0o00o0Oo ( oo )
 IiII1I1i1i1ii = re . compile ( 'name="(.+?)".+?rl="(.+?)".+?mg="(.+?)"' , re . DOTALL ) . findall ( i1IIi11111i )
 for IIIII , I1 , O0OoOoo00o in IiII1I1i1i1ii :
  if not 'XXX' in IIIII :
   iiiI11 ( IIIII , I1 , 1 , O0OoOoo00o , I1ii11iIi11i )
  if 'XXX' in IIIII :
   if Iii1ii1II11i == 'true' :
    if iI111iI == '' :
     OOooO = xbmcgui . Dialog ( )
     OOoO00o = OOooO . yesno ( 'Adult Content' , 'You have opted to show adult content' , '' , 'Please set a password to prevent accidental access' , 'Cancel' , 'Lets Go' )
     if OOoO00o == 1 :
      II111iiiiII = xbmc . Keyboard ( '' , 'Set Password' )
      II111iiiiII . doModal ( )
      if ( II111iiiiII . isConfirmed ( ) ) :
       oOoOo00oOo = II111iiiiII . getText ( )
       o0OoOoOO00 . setSetting ( 'password' , oOoOo00oOo )
      iiiI11 ( IIIII , I1 , 1 , O0OoOoo00o , I1ii11iIi11i )
   if Iii1ii1II11i == 'true' :
    if iI111iI <> '' :
     iiiI11 ( IIIII , I1 , 1 , O0OoOoo00o , I1ii11iIi11i )
 iiiI11 ( 'Favourites' , O0oo0OO0 , 15 , 'http://ukturk.offshorepastebin.com/UKTurk/thumbs/new/Uk%20turk%20thumbnails%20favourites.jpg' , I1ii11iIi11i )
 iiiI11 ( 'Search' , 'url' , 5 , 'http://ukturk.offshorepastebin.com/UKTurk/thumbs/new/Uk%20turk%20thumbnails%20search.jpg' , I1ii11iIi11i )
 xbmc . executebuiltin ( 'Container.SetViewMode(500)' )
 if 96 - 96: I111I11 . OO00OooO0OO - iiIii / OO
def oO0O ( url ) :
 o0OoOoOO00 . setSetting ( 'fav' , 'yes' )
 OOoO000O0OO = None
 file = open ( O0oo0OO0 , 'r' )
 OOoO000O0OO = file . read ( )
 IiII1I1i1i1ii = re . compile ( "<item>(.+?)</item>" , re . DOTALL ) . findall ( OOoO000O0OO )
 for iiI1IiI in IiII1I1i1i1ii :
  II = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>' , re . DOTALL ) . findall ( iiI1IiI )
  for IIIII , url , O0OoOoo00o in II :
   if '.txt' in url :
    iiiI11 ( IIIII , url , 1 , O0OoOoo00o , I1ii11iIi11i )
   else :
    ooOoOoo0O ( IIIII , url , 2 , O0OoOoo00o , I1ii11iIi11i )
    if 76 - 76: i1II1I11 / i1I / OO0o / ooO0o0Oo % Oo00OOOOO
def O0OO00o0OO ( name , url , iconimage ) :
 url = url . replace ( ' ' , '%20' )
 iconimage = iconimage . replace ( ' ' , '%20' )
 I11i1 = '<FAV><item>\n<title>' + name + '</title>\n<link>' + url + '</link>\n' + '<thumbnail>' + iconimage + '</thumbnail>\n</item></FAV>\n'
 Oo0oO0ooo = open ( O0oo0OO0 , 'a' )
 Oo0oO0ooo . write ( I11i1 )
 Oo0oO0ooo . close ( )
 if 25 - 25: iii1I11ii1i1 - OO0oo0oOO + oo0oooooO0
def i11Iiii ( name , url , iconimage ) :
 OOoO000O0OO = None
 file = open ( O0oo0OO0 , 'r' )
 OOoO000O0OO = file . read ( )
 iI = ''
 IiII1I1i1i1ii = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( OOoO000O0OO )
 for II in IiII1I1i1i1ii :
  I11i1 = '\n<FAV><item>\n' + II + '</item>\n'
  if name in II :
   I11i1 = I11i1 . replace ( 'item' , ' ' )
  iI = iI + I11i1
 file = open ( O0oo0OO0 , 'w' )
 file . truncate ( )
 file . write ( iI )
 file . close ( )
 xbmc . executebuiltin ( 'Container.Refresh' )
 if 28 - 28: i1I - iii1I11ii1i1 . iii1I11ii1i1 + OO00OooO0OO - OoooooooOO + O0
def oOoOooOo0o0 ( name , url , iconimage , fanart ) :
 OOOO = OOO00 ( name )
 o0OoOoOO00 . setSetting ( 'tv' , OOOO )
 i1IIi11111i = o000o0o00o0Oo ( url )
 iiiiiIIii ( i1IIi11111i )
 if '/UKTurk/TurkishTV.txt' in url : O000OO0 ( )
 if '/UKTurk/tv shows/Index.txt' in url : I11iii1Ii ( )
 if 'Index' in url :
  I1IIiiIiii ( url )
 if 'XXX' in name : O000oo0O ( i1IIi11111i )
 IiII1I1i1i1ii = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( i1IIi11111i )
 IiII = str ( len ( IiII1I1i1i1ii ) )
 o0OoOoOO00 . setSetting ( 'count' , IiII )
 o0OoOoOO00 . setSetting ( 'fav' , 'no' )
 for iiI1IiI in IiII1I1i1i1ii :
  try :
   if '<sportsdevil>' in iiI1IiI : OOOOi11i1 ( iiI1IiI , url , iconimage )
   elif '<iptv>' in iiI1IiI : IIIii1II1II ( iiI1IiI )
   elif '<Image>' in iiI1IiI : i1I1iI ( iiI1IiI )
   elif '<text>' in iiI1IiI : oo0OooOOo0 ( iiI1IiI )
   elif '<scraper>' in iiI1IiI : o0O ( iiI1IiI )
   elif '<redirect>' in iiI1IiI : REDIRECT ( iiI1IiI )
   elif '<oktitle>' in iiI1IiI : O00oO ( iiI1IiI )
   elif '<dl>' in iiI1IiI : I11i1I1I ( iiI1IiI )
   elif '<scraper>' in iiI1IiI : o0O ( iiI1IiI )
   else : oO0Oo ( iiI1IiI , url , iconimage )
  except : pass
  if 54 - 54: iiIii - ooO00oOoo + OoooooooOO
def I11iii1Ii ( ) :
 I1 = 'https://watchseries-online.pl/last-350-episodes'
 iiiI11 ( 'New Episodes of TV Shows' , I1 , 23 , 'http://ukturk.offshorepastebin.com/UKTurk/tv%20shows/Uk turk thumbnails new episodes tv shows1.jpg' , I1ii11iIi11i , description = '' )
 if 70 - 70: ooO0o0Oo / OO0o . Oo00OOOOO % O0OOo
def O000OO0 ( ) :
 I1 = 'http://www.hergundizi.net'
 iiiI11 ( '[COLOR gold]**** Yerli Yeni Eklenenler Diziler ****[/COLOR]' , I1 , 21 , O0OoOoo00o , I1ii11iIi11i , description = '' )
 if 67 - 67: OO00OooO0OO * iiIii . iii1I11ii1i1 - I111I11 * iiIii
def IIiI1I ( url ) :
 O00Oo000ooO0 = tv . TVShows ( url )
 IiII1I1i1i1ii = re . compile ( '<start>(.+?)<sep>(.+?)<end>' ) . findall ( str ( O00Oo000ooO0 ) )
 for IIIII , url in IiII1I1i1i1ii :
  ooOoOoo0O ( IIIII , url , 24 , O0OoOoo00o , I1ii11iIi11i , description = '' )
 xbmc . executebuiltin ( 'Container.SetViewMode(50)' )
 if 100 - 100: O0 + iii1I11ii1i1 - i1I + i11iIiiIii * ooO0o0Oo
def iII ( name , url , iconimage ) :
 o0 = [ 'vidto.me' , 'gorillavid.in' , 'vidzi.tv' , 'rapidvideo.ws' ]
 IiII = [ ]
 ooOooo000oOO = [ ]
 Oo0oOOo = tv . Stream ( url )
 Oo0OoO00oOO0o = 1
 for i1IIi11111i in Oo0oOOo :
  if urlresolver . HostedMediaFile ( i1IIi11111i ) . valid_url ( ) :
   for OOO00O in o0 :
    if OOO00O in i1IIi11111i :
     IiII . append ( 'Link ' + str ( Oo0OoO00oOO0o ) )
     ooOooo000oOO . append ( i1IIi11111i )
     Oo0OoO00oOO0o = Oo0OoO00oOO0o + 1
 OOooO = xbmcgui . Dialog ( )
 OOoOO0oo0ooO = OOooO . select ( 'Choose a link..' , IiII )
 if OOoOO0oo0ooO < 0 : quit ( )
 url = ooOooo000oOO [ OOoOO0oo0ooO ]
 O0o0O00Oo0o0 ( name , url , iconimage )
 if 87 - 87: oo0oooooO0 * O0OOo % i11iIiiIii % OO00OooO0OO - i1I
def O0ooo0O0oo0 ( url ) :
 O00Oo000ooO0 = hergundizi . TVShows ( url )
 IiII1I1i1i1ii = re . compile ( '<start>(.+?)<sep>(.+?)<sep>(.+?)<end>' ) . findall ( str ( O00Oo000ooO0 ) )
 for IIIII , url , O0OoOoo00o in IiII1I1i1i1ii :
  if not 'dızlar' in IIIII :
   ooOoOoo0O ( IIIII , url , 22 , O0OoOoo00o , I1ii11iIi11i , description = '' )
 try :
  oo0oOo = re . compile ( '<np>(.+?)<np>' ) . findall ( str ( O00Oo000ooO0 ) ) [ 0 ]
  iiiI11 ( 'Next Page>>' , oo0oOo , 21 , iIiiiI , I1ii11iIi11i , description = '' )
 except : pass
 xbmc . executebuiltin ( 'Container.SetViewMode(50)' )
 if 89 - 89: OO00OooO0OO
def OO0oOoOO0oOO0 ( name , url , iconimage ) :
 oO0OOoo0OO = hergundizi . Parts ( url )
 O0ii1ii1ii = len ( oO0OOoo0OO )
 if O0ii1ii1ii > 1 :
  IiII = [ ]
  Oo0OoO00oOO0o = 1
  for oooooOoo0ooo in oO0OOoo0OO :
   IiII . append ( 'Part ' + str ( Oo0OoO00oOO0o ) )
   Oo0OoO00oOO0o = Oo0OoO00oOO0o + 1
   OOooO = xbmcgui . Dialog ( )
  OOoOO0oo0ooO = OOooO . select ( 'Choose a Part..' , IiII )
  if OOoOO0oo0ooO < 0 : quit ( )
  url = oO0OOoo0OO [ OOoOO0oo0ooO ]
 I1I1IiI1 = hergundizi . Stream ( url )
 O0o0O00Oo0o0 ( name , I1I1IiI1 , iconimage )
 if 5 - 5: iiIii * oo0oooooO0 + OO00OooO0OO . i1I + OO00OooO0OO
def o0O ( item ) :
 IIIII = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 O0OoOoo00o = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 I1 = re . compile ( '<scraper>(.+?)</scraper>' ) . findall ( item ) [ 0 ]
 iiiI11 ( IIIII , I1 , 20 , O0OoOoo00o , I1ii11iIi11i )
 if 91 - 91: O0
def oOOo0 ( url , iconimage ) :
 I11i1 = url + '.scrape()'
 i1IIi11111i = eval ( I11i1 )
 IiII1I1i1i1ii = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( i1IIi11111i )
 IiII = str ( len ( IiII1I1i1i1ii ) )
 o0OoOoOO00 . setSetting ( 'count' , IiII )
 o0OoOoOO00 . setSetting ( 'fav' , 'no' )
 for iiI1IiI in IiII1I1i1i1ii :
  try :
   if '<sportsdevil>' in iiI1IiI : OOOOi11i1 ( iiI1IiI , url , iconimage )
   elif '<iptv>' in iiI1IiI : IIIii1II1II ( iiI1IiI )
   elif '<Image>' in iiI1IiI : i1I1iI ( iiI1IiI )
   elif '<text>' in iiI1IiI : oo0OooOOo0 ( iiI1IiI )
   elif '<scraper>' in iiI1IiI : o0O ( iiI1IiI )
   elif '<redirect>' in iiI1IiI : REDIRECT ( iiI1IiI )
   elif '<oktitle>' in iiI1IiI : O00oO ( iiI1IiI )
   elif '<dl>' in iiI1IiI : I11i1I1I ( iiI1IiI )
   elif '<scraper>' in iiI1IiI : o0O ( iiI1IiI , iconimage )
   else : oO0Oo ( iiI1IiI , url , iconimage )
  except : pass
  if 54 - 54: O0 - iii1I11ii1i1 % i1I
def I11i1I1I ( item ) :
 IIIII = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 I1 = re . compile ( '<dl>(.+?)</dl>' ) . findall ( item ) [ 0 ]
 O0OoOoo00o = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 OOoO ( IIIII , I1 , 19 , O0OoOoo00o , I1ii11iIi11i )
 if 46 - 46: I111I11 . O0OOo - OoooooooOO
def ooo00OOOooO ( name , url ) :
 O00OOOoOoo0O = url . split ( '/' ) [ - 1 ]
 if O00OOOoOoo0O == 'latest' : O00OOOoOoo0O = 'AceStreamEngine.apk'
 import downloader
 OOooO = xbmcgui . Dialog ( )
 O000OOo00oo = xbmcgui . DialogProgress ( )
 oo0OOo = OOooO . browse ( 0 , 'Select folder to download to' , 'myprograms' )
 ooOOO00Ooo = os . path . join ( oo0OOo , O00OOOoOoo0O )
 O000OOo00oo . create ( 'Downloading' , '' , '' , 'Please Wait' )
 downloader . download ( url , ooOOO00Ooo , O000OOo00oo )
 O000OOo00oo . close ( )
 OOooO = xbmcgui . Dialog ( )
 OOooO . ok ( 'Download complete' , 'Please install from..' , oo0OOo )
 if 16 - 16: II111iiii % OO00OooO0OO - II111iiii + ooO0o0Oo
def O00oO ( item ) :
 IIIII = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 i1I1i = re . compile ( '<oktitle>(.+?)</oktitle>' ) . findall ( item ) [ 0 ]
 Ii = re . compile ( '<line1>(.+?)</line1>' ) . findall ( item ) [ 0 ]
 iii1i = re . compile ( '<line2>(.+?)</line2>' ) . findall ( item ) [ 0 ]
 I11i1ii1 = re . compile ( '<line3>(.+?)</line3>' ) . findall ( item ) [ 0 ]
 O0Oooo0O = '##' + i1I1i + '#' + Ii + '#' + iii1i + '#' + I11i1ii1 + '##'
 O0OoOoo00o = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 OOoO ( IIIII , O0Oooo0O , 17 , O0OoOoo00o , I1ii11iIi11i )
 if 84 - 84: Oo00OOOOO . OO / O0OOo - ooO00oOoo / OoooooooOO / iiIii
def II111iiiI1Ii ( name , url ) :
 o0O0OOO0Ooo = re . compile ( '##(.+?)##' ) . findall ( url ) [ 0 ] . split ( '#' )
 OOooO = xbmcgui . Dialog ( )
 OOooO . ok ( o0O0OOO0Ooo [ 0 ] , o0O0OOO0Ooo [ 1 ] , o0O0OOO0Ooo [ 2 ] , o0O0OOO0Ooo [ 3 ] )
 if 45 - 45: O0 / iiIii
def oo0OooOOo0 ( item ) :
 IIIII = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 O0Oooo0O = re . compile ( '<text>(.+?)</text>' ) . findall ( item ) [ 0 ]
 O0OoOoo00o = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 OOoO ( IIIII , O0Oooo0O , 9 , O0OoOoo00o , I1ii11iIi11i )
 if 32 - 32: Oo00OOOOO . iii1I11ii1i1 . iii1I11ii1i1
def OO00O0O ( name , url ) :
 iii = o000o0o00o0Oo ( url )
 oOooOOOoOo ( name , iii )
 if 41 - 41: ooO0o0Oo - O0 - O0
def i1I1iI ( item ) :
 oO00OOoO00 = re . compile ( '<Image>(.+?)</Image>' ) . findall ( item )
 if len ( oO00OOoO00 ) == 1 :
  IIIII = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  O0OoOoo00o = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  IiI111111IIII = re . compile ( '<Image>(.+?)</Image>' ) . findall ( item ) [ 0 ]
  O0OoOoo00o = IiI111111IIII . replace ( 'http://imgur.com/' , 'http://i.imgur.com/' ) + '.jpg'
  IiI111111IIII = IiI111111IIII . replace ( 'http://imgur.com/' , 'http://i.imgur.com/' ) + '.jpg'
  OOoO ( IIIII , IiI111111IIII , 7 , O0OoOoo00o , I1ii11iIi11i )
 elif len ( oO00OOoO00 ) > 1 :
  IIIII = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  O0OoOoo00o = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  i1Ii = ''
  for IiI111111IIII in oO00OOoO00 :
   O0OoOoo00o = IiI111111IIII . replace ( 'http://imgur.com/' , 'http://i.imgur.com/' ) + '.jpg'
   IiI111111IIII = IiI111111IIII . replace ( 'http://imgur.com/' , 'http://i.imgur.com/' ) + '.jpg'
   i1Ii = i1Ii + '<Image>' + IiI111111IIII + '</Image>'
  ii111iI1iIi1 = i1i1II
  IIIII = OOO00 ( IIIII )
  OOO = os . path . join ( os . path . join ( ii111iI1iIi1 , '' ) , IIIII + '.txt' )
  if not os . path . exists ( OOO ) : file ( OOO , 'w' ) . close ( )
  oo0OOo0 = open ( OOO , "w" )
  oo0OOo0 . write ( i1Ii )
  oo0OOo0 . close ( )
  OOoO ( IIIII , 'image' , 8 , O0OoOoo00o , I1ii11iIi11i )
  if 47 - 47: OO0oo0oOO + OO00OooO0OO * O0OOo / oo0oooooO0 - Oo00OOOOO % iIii1I11I1II1
def IIIii1II1II ( item ) :
 IIIII = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 O0OoOoo00o = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 I1 = re . compile ( '<iptv>(.+?)</iptv>' ) . findall ( item ) [ 0 ]
 iiiI11 ( IIIII , I1 , 6 , O0OoOoo00o , I1ii11iIi11i )
 if 26 - 26: OO * Oo00OOOOO . II111iiii * ooO0o0Oo
def II1 ( url , iconimage ) :
 i1IIi11111i = o000o0o00o0Oo ( url )
 iiiIi1 = re . compile ( '^#.+?:-?[0-9]*(.*?),(.*?)\n(.*?)$' , re . I + re . M + re . U + re . S ) . findall ( i1IIi11111i )
 i1I1ii11i1Iii = [ ]
 for I1IiiiiI , IIIII , url in iiiIi1 :
  o0OIiII = { "params" : I1IiiiiI , "name" : IIIII , "url" : url }
  i1I1ii11i1Iii . append ( o0OIiII )
 list = [ ]
 for ii1iII1II in i1I1ii11i1Iii :
  o0OIiII = { "name" : ii1iII1II [ "name" ] , "url" : ii1iII1II [ "url" ] }
  iiiIi1 = re . compile ( ' (.+?)="(.+?)"' , re . I + re . M + re . U + re . S ) . findall ( ii1iII1II [ "params" ] )
  for Iii1I1I11iiI1 , I1I1i1I in iiiIi1 :
   o0OIiII [ Iii1I1I11iiI1 . strip ( ) . lower ( ) . replace ( '-' , '_' ) ] = I1I1i1I . strip ( )
  list . append ( o0OIiII )
 for ii1iII1II in list :
  if '.ts' in ii1iII1II [ "url" ] : OOoO ( ii1iII1II [ "name" ] , ii1iII1II [ "url" ] , 2 , iconimage , I1ii11iIi11i )
  else : ooOoOoo0O ( ii1iII1II [ "name" ] , ii1iII1II [ "url" ] , 2 , iconimage , I1ii11iIi11i )
  if 30 - 30: OoooooooOO
def oO0Oo ( item , url , iconimage ) :
 I1Ii1iI1 = iconimage
 oO0 = url
 ooOooo000oOO = re . compile ( '<link>(.+?)</link>' ) . findall ( item )
 II = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>' , re . DOTALL ) . findall ( item )
 for IIIII , O0OO0O , iconimage in II :
  if 'youtube.com/playlist?' in O0OO0O :
   OOOoOoO = O0OO0O . split ( 'list=' ) [ 1 ]
   iiiI11 ( IIIII , O0OO0O , Ii1I1i , iconimage , I1ii11iIi11i , description = OOOoOoO )
 if len ( ooOooo000oOO ) == 1 :
  IIIII = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  url = re . compile ( '<link>(.+?)</link>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  if iconimage == 'ImageHere' : iconimage = I1Ii1iI1
  if '.ts' in url : OOoO ( IIIII , url , 16 , iconimage , I1ii11iIi11i , description = '' )
  elif 'movies' in oO0 :
   OOI1iI1ii1II ( IIIII , url , 2 , iconimage , int ( IiII ) , isFolder = False )
  else : ooOoOoo0O ( IIIII , url , 2 , iconimage , I1ii11iIi11i )
 elif len ( ooOooo000oOO ) > 1 :
  IIIII = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  if iconimage == 'ImageHere' : iconimage = I1Ii1iI1
  if '.ts' in url : OOoO ( IIIII , url , 16 , iconimage , I1ii11iIi11i , description = '' )
  elif 'movies' in oO0 :
   OOI1iI1ii1II ( IIIII , url , 3 , iconimage , int ( IiII ) , isFolder = False )
  else : OOoO ( IIIII , url , 3 , iconimage , I1ii11iIi11i )
  if 57 - 57: OO0oo0oOO % ooO0o0Oo + iiIii - O0OOo
def I1IIiiIiii ( url ) :
 i1IIi11111i = o000o0o00o0Oo ( url )
 IiII1I1i1i1ii = re . compile ( 'name="(.+?)".+?rl="(.+?)".+?mg="(.+?)"' , re . DOTALL ) . findall ( i1IIi11111i )
 for IIIII , url , o0OOO in IiII1I1i1i1ii :
  if 'youtube.com/playlist?list=' in url :
   iiiI11 ( IIIII , url , 18 , o0OOO , I1ii11iIi11i )
  elif 'youtube.com/results?search_query=' in url :
   iiiI11 ( IIIII , url , 18 , o0OOO , I1ii11iIi11i )
  else :
   iiiI11 ( IIIII , url , 1 , o0OOO , I1ii11iIi11i )
   if 65 - 65: OO0o . OO00OooO0OO
def IiI1i ( name , url , iconimage ) :
 if 'youtube.com/results?search_query=' in url :
  OOOoOoO = url . split ( 'search_query=' ) [ 1 ]
  o0Oo00 = iiIIIII1i1iI + OOOoOoO + o0oO0
  iIO0O0Oooo0o = urllib2 . Request ( o0Oo00 )
  iIO0O0Oooo0o . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' )
  oOOoo00O00o = urllib2 . urlopen ( iIO0O0Oooo0o )
  i1IIi11111i = oOOoo00O00o . read ( )
  oOOoo00O00o . close ( )
  i1IIi11111i = i1IIi11111i . replace ( '\r' , '' ) . replace ( '\n' , '' ) . replace ( '  ' , '' )
  IiII1I1i1i1ii = re . compile ( '"videoId": "(.+?)".+?"title": "(.+?)"' , re . DOTALL ) . findall ( i1IIi11111i )
  for O0O00Oo , name in IiII1I1i1i1ii :
   url = 'https://www.youtube.com/watch?v=' + O0O00Oo
   iconimage = 'https://i.ytimg.com/vi/%s/hqdefault.jpg' % O0O00Oo
   ooOoOoo0O ( name , url , 2 , iconimage , I1ii11iIi11i )
 elif 'youtube.com/playlist?list=' in url :
  OOOoOoO = url . split ( 'playlist?list=' ) [ 1 ]
  o0Oo00 = oo00 + OOOoOoO + o00
  iIO0O0Oooo0o = urllib2 . Request ( o0Oo00 )
  iIO0O0Oooo0o . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' )
  oOOoo00O00o = urllib2 . urlopen ( iIO0O0Oooo0o )
  i1IIi11111i = oOOoo00O00o . read ( )
  oOOoo00O00o . close ( )
  i1IIi11111i = i1IIi11111i . replace ( '\r' , '' ) . replace ( '\n' , '' ) . replace ( '  ' , '' )
  IiII1I1i1i1ii = re . compile ( '"title": "(.+?)".+?"videoId": "(.+?)"' , re . DOTALL ) . findall ( i1IIi11111i )
  for name , O0O00Oo in IiII1I1i1i1ii :
   url = 'https://www.youtube.com/watch?v=' + O0O00Oo
   iconimage = 'https://i.ytimg.com/vi/%s/hqdefault.jpg' % O0O00Oo
   ooOoOoo0O ( name , url , 2 , iconimage , I1ii11iIi11i )
   if 97 - 97: O0 * OoooooooOO . OoooooooOO
def I111iI ( item ) :
 item = item . replace ( '\r' , '' ) . replace ( '\t' , '' ) . replace ( '&nbsp;' , '' ) . replace ( '\'' , '' ) . replace ( '\n' , '' )
 II = re . compile ( 'name="(.+?)".+?rl="(.+?)".+?mg="(.+?)"' , re . DOTALL ) . findall ( item )
 for IIIII , I1 , O0OoOoo00o in II :
  if 'youtube.com/channel/' in I1 :
   OOOoOoO = I1 . split ( 'channel/' ) [ 1 ]
   iiiI11 ( IIIII , I1 , Ii1I1i , O0OoOoo00o , I1ii11iIi11i , description = OOOoOoO )
  elif 'youtube.com/user/' in I1 :
   OOOoOoO = I1 . split ( 'user/' ) [ 1 ]
   iiiI11 ( IIIII , I1 , Ii1I1i , O0OoOoo00o , I1ii11iIi11i , description = OOOoOoO )
  elif 'youtube.com/playlist?' in I1 :
   OOOoOoO = I1 . split ( 'list=' ) [ 1 ]
   iiiI11 ( IIIII , I1 , Ii1I1i , O0OoOoo00o , I1ii11iIi11i , description = OOOoOoO )
  elif 'plugin://' in I1 :
   oOOo0II1I1iiIII = HTMLParser ( )
   I1 = oOOo0II1I1iiIII . unescape ( I1 )
   iiiI11 ( IIIII , I1 , Ii1I1i , O0OoOoo00o , I1ii11iIi11i )
  else :
   iiiI11 ( IIIII , I1 , 1 , O0OoOoo00o , I1ii11iIi11i )
   if 77 - 77: OO00OooO0OO - II111iiii - oo0oooooO0
def OOOOi11i1 ( item , url , iconimage ) :
 I1Ii1iI1 = iconimage
 ooOooo000oOO = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( item )
 IiiiIIiIi1 = re . compile ( '<link>(.+?)</link>' ) . findall ( item )
 if len ( ooOooo000oOO ) + len ( IiiiIIiIi1 ) == 1 :
  IIIII = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  url = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( item ) [ 0 ]
  url = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' + url
  if iconimage == 'ImageHere' : iconimage = I1Ii1iI1
  OOoO ( IIIII , url , 16 , iconimage , I1ii11iIi11i )
 elif len ( ooOooo000oOO ) + len ( IiiiIIiIi1 ) > 1 :
  IIIII = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  if iconimage == 'ImageHere' : iconimage = I1Ii1iI1
  OOoO ( IIIII , url , 3 , iconimage , I1ii11iIi11i )
  if 74 - 74: iIii1I11I1II1 * OO + OO00OooO0OO / i1IIi / II111iiii . O0OOo
def O000oo0O ( link ) :
 if iI111iI == '' :
  OOooO = xbmcgui . Dialog ( )
  OOoO00o = OOooO . yesno ( 'Adult Content' , 'You have opted to show adult content' , '' , 'Please set a password to prevent accidental access' , 'Cancel' , 'OK' )
  if OOoO00o == 1 :
   II111iiiiII = xbmc . Keyboard ( '' , 'Set Password' )
   II111iiiiII . doModal ( )
   if ( II111iiiiII . isConfirmed ( ) ) :
    oOoOo00oOo = II111iiiiII . getText ( )
    o0OoOoOO00 . setSetting ( 'password' , oOoOo00oOo )
  else : quit ( )
 elif iI111iI <> '' :
  OOooO = xbmcgui . Dialog ( )
  OOoO00o = OOooO . yesno ( 'Adult Content' , 'Please enter the password you set' , 'to continue' , '' , 'Cancel' , 'OK' )
  if OOoO00o == 1 :
   II111iiiiII = xbmc . Keyboard ( '' , 'Enter Password' )
   II111iiiiII . doModal ( )
   if ( II111iiiiII . isConfirmed ( ) ) :
    oOoOo00oOo = II111iiiiII . getText ( )
   if oOoOo00oOo <> iI111iI :
    quit ( )
  else : quit ( )
  if 62 - 62: OoooooooOO * ooO00oOoo
def oOOOoo0O0oO ( ) :
 II111iiiiII = xbmc . Keyboard ( '' , 'Search' )
 II111iiiiII . doModal ( )
 if ( II111iiiiII . isConfirmed ( ) ) :
  OOOoOoO = II111iiiiII . getText ( )
  OOOoOoO = OOOoOoO . upper ( )
 else : quit ( )
 i1IIi11111i = o000o0o00o0Oo ( I1i1iiI1 )
 iIII1I111III = re . compile ( '<link>(.+?)</link>' ) . findall ( i1IIi11111i )
 for I1 in iIII1I111III :
  try :
   i1IIi11111i = o000o0o00o0Oo ( I1 )
   IIo0o0O0O00oOOo = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( i1IIi11111i )
   for iiI1IiI in IIo0o0O0O00oOOo :
    IiII1I1i1i1ii = re . compile ( '<title>(.+?)</title>' ) . findall ( iiI1IiI )
    for iIIIiIi in IiII1I1i1i1ii :
     iIIIiIi = iIIIiIi . upper ( )
     if OOOoOoO in iIIIiIi :
      try :
       if '<sportsdevil>' in iiI1IiI : OOOOi11i1 ( iiI1IiI , I1 , O0OoOoo00o )
       elif '<iptv>' in iiI1IiI : IIIii1II1II ( iiI1IiI )
       elif '<Image>' in iiI1IiI : i1I1iI ( iiI1IiI )
       elif '<text>' in iiI1IiI : oo0OooOOo0 ( iiI1IiI )
       elif '<scraper>' in iiI1IiI : o0O ( iiI1IiI )
       elif '<redirect>' in iiI1IiI : REDIRECT ( iiI1IiI )
       elif '<oktitle>' in iiI1IiI : O00oO ( iiI1IiI )
       elif '<dl>' in iiI1IiI : I11i1I1I ( iiI1IiI )
       elif '<scraper>' in iiI1IiI : o0O ( iiI1IiI , O0OoOoo00o )
       else : oO0Oo ( iiI1IiI , I1 , O0OoOoo00o )
      except : pass
  except : pass
  if 100 - 100: ooO00oOoo / iiIii % II111iiii % O0OOo % i1I
def O00oO000O0O ( name , url , iconimage ) :
 I1Ii1iI1 = iconimage
 I1i1i1iii = [ ]
 I1111i = [ ]
 iIIii = [ ]
 i1IIi11111i = o000o0o00o0Oo ( url )
 o00O0O = re . compile ( '<title>' + re . escape ( name ) + '</title>(.+?)</item>' , re . DOTALL ) . findall ( i1IIi11111i ) [ 0 ]
 ooOooo000oOO = [ ]
 if '<link>' in o00O0O :
  ii1iii1i = re . compile ( '<link>(.+?)</link>' ) . findall ( o00O0O )
  for Iii1I1111ii in ii1iii1i :
   ooOooo000oOO . append ( Iii1I1111ii )
 if '<sportsdevil>' in o00O0O :
  ooOoO00 = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( o00O0O )
  for Ii1IIiI1i in ooOoO00 :
   Ii1IIiI1i = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' + Ii1IIiI1i
   ooOooo000oOO . append ( Ii1IIiI1i )
 Oo0OoO00oOO0o = 1
 for o0O00Oo0 in ooOooo000oOO :
  IiII111i1i11 = o0O00Oo0
  if 'acestream://' in o0O00Oo0 or '.acelive' in o0O00Oo0 or 'sop://' in o0O00Oo0 : i111iIi1i1II1 = ' (Acestreams)'
  else : i111iIi1i1II1 = ''
  if '(' in o0O00Oo0 :
   o0O00Oo0 = o0O00Oo0 . split ( '(' ) [ 0 ]
   oooO = str ( IiII111i1i11 . split ( '(' ) [ 1 ] . replace ( ')' , '' ) + i111iIi1i1II1 )
   I1i1i1iii . append ( o0O00Oo0 )
   I1111i . append ( oooO )
  else :
   i1I1i111Ii = o0O00Oo0 . split ( '/' ) [ 2 ] . replace ( 'www.' , '' )
   I1i1i1iii . append ( o0O00Oo0 )
   I1111i . append ( 'Link ' + str ( Oo0OoO00oOO0o ) + i111iIi1i1II1 )
  Oo0OoO00oOO0o = Oo0OoO00oOO0o + 1
 OOooO = xbmcgui . Dialog ( )
 OOoOO0oo0ooO = OOooO . select ( 'Choose a link..' , I1111i )
 if OOoOO0oo0ooO < 0 : quit ( )
 else :
  url = I1i1i1iii [ OOoOO0oo0ooO ]
  O0o0O00Oo0o0 ( name , url , iconimage )
  if 67 - 67: ooO00oOoo . i1IIi
def i1i1iI1iiiI ( url ) :
 I11i1 = "ShowPicture(%s)" % url
 xbmc . executebuiltin ( I11i1 )
 if 51 - 51: ooO00oOoo % OO0oo0oOO . i1II1I11 / iIii1I11I1II1 / OO0o . i1II1I11
def O0o0O00Oo0o0 ( name , url , iconimage ) :
 try :
  if 'sop://' in url :
   url = urllib . quote ( url )
   url = 'plugin://program.plexus/?mode=2&url=%s&name=%s' % ( url , name . replace ( ' ' , '+' ) )
   IIIii11 ( name , url , iconimage )
  elif 'acestream://' in url or '.acelive' in url :
   url = urllib . quote ( url )
   url = 'plugin://program.plexus/?mode=1&url=%s&name=%s' % ( url , name . replace ( ' ' , '+' ) )
   IIIii11 ( name , url , iconimage )
  elif 'plugin://plugin.video.SportsDevil/' in url :
   IIIii11 ( name , url , iconimage )
  elif '.ts' in url :
   url = 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;name=' + name + '&amp;url=' + url
   IIIii11 ( name , url , iconimage )
  elif urlresolver . HostedMediaFile ( url ) . valid_url ( ) :
   url = urlresolver . HostedMediaFile ( url ) . resolve ( )
   iiIiIIIiiI ( name , url , iconimage )
  elif liveresolver . isValid ( url ) == True :
   url = liveresolver . resolve ( url )
   iiIiIIIiiI ( name , url , iconimage )
  else : IIIii11 ( name , url , iconimage )
 except :
  iiI1IIIi ( 'UKTurk' , 'Stream Unavailable' , '3000' , o0OOO )
  if 47 - 47: O0OOo % OO0o % i11iIiiIii - O0 + oo0oooooO0
def ooO000OO0O00O ( url ) :
 if urlresolver . HostedMediaFile ( url ) . valid_url ( ) :
  url = urlresolver . HostedMediaFile ( url ) . resolve ( )
 xbmc . Player ( ) . play ( url )
 if 69 - 69: i1I - OoooooooOO + iiIii - OO0o
def iiIiIIIiiI ( name , url , iconimage ) :
 ii = True
 O0oOo00o = xbmcgui . ListItem ( name , iconImage = iconimage , thumbnailImage = iconimage ) ; O0oOo00o . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
 ii = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = url , listitem = O0oOo00o )
 O0oOo00o . setPath ( url )
 xbmcplugin . setResolvedUrl ( int ( sys . argv [ 1 ] ) , True , O0oOo00o )
 if 81 - 81: iii1I11ii1i1 % i1IIi . iIii1I11I1II1
def IIIii11 ( name , url , iconimage ) :
 ii = True
 O0oOo00o = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage ) ; O0oOo00o . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
 ii = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = url , listitem = O0oOo00o )
 OOooO = xbmcgui . Dialog ( )
 xbmc . Player ( ) . play ( url , O0oOo00o , False )
 if 4 - 4: i11iIiiIii % I111I11 % i1IIi / iii1I11ii1i1
def I11iI ( url ) :
 xbmc . executebuiltin ( "PlayMedia(%s)" % url )
 if 68 - 68: iIii1I11I1II1 / i1I
def i1 ( url ) :
 OOO0000oO = o0OoOoOO00 . getSetting ( 'layout' )
 if OOO0000oO == 'Listers' : o0OoOoOO00 . setSetting ( 'layout' , 'Category' )
 else : o0OoOoOO00 . setSetting ( 'layout' , 'Listers' )
 xbmc . executebuiltin ( 'Container.Refresh' )
 if 15 - 15: OO00OooO0OO % ooO00oOoo * OO0o
def o000o0o00o0Oo ( url ) :
 iIO0O0Oooo0o = urllib2 . Request ( url )
 iIO0O0Oooo0o . add_header ( 'User-Agent' , 'mat' )
 oOOoo00O00o = urllib2 . urlopen ( iIO0O0Oooo0o )
 i1IIi11111i = oOOoo00O00o . read ( )
 oOOoo00O00o . close ( )
 i1IIi11111i = i1IIi11111i . replace ( '</fanart>' , '<fanart>x</fanart>' ) . replace ( '<thumbnail></thumbnail>' , '<thumbnail>x</thumbnail>' ) . replace ( '<utube>' , '<link>https://www.youtube.com/watch?v=' ) . replace ( '</utube>' , '</link>' )
 if '{' in i1IIi11111i : i1IIi11111i = O0OoooO0 ( i1IIi11111i )
 return i1IIi11111i
 if 85 - 85: OO0o
def iI1i11II1i ( ) :
 o0o0OoOo0O0OO = [ ]
 iIi1I11I = sys . argv [ 2 ]
 if len ( iIi1I11I ) >= 2 :
  I1IiiiiI = sys . argv [ 2 ]
  Iii1 = I1IiiiiI . replace ( '?' , '' )
  if ( I1IiiiiI [ len ( I1IiiiiI ) - 1 ] == '/' ) :
   I1IiiiiI = I1IiiiiI [ 0 : len ( I1IiiiiI ) - 2 ]
  ooO = Iii1 . split ( '&' )
  o0o0OoOo0O0OO = { }
  for Oo0OoO00oOO0o in range ( len ( ooO ) ) :
   o0o00OOo0 = { }
   o0o00OOo0 = ooO [ Oo0OoO00oOO0o ] . split ( '=' )
   if ( len ( o0o00OOo0 ) ) == 2 :
    o0o0OoOo0O0OO [ o0o00OOo0 [ 0 ] ] = o0o00OOo0 [ 1 ]
 return o0o0OoOo0O0OO
 if 17 - 17: OO0oo0oOO + i1II1I11 - i11iIiiIii . OO0oo0oOO * i1I
def iiI1IIIi ( title , message , ms , nart ) :
 xbmc . executebuiltin ( "XBMC.notification(" + title + "," + message + "," + ms + "," + nart + ")" )
 if 77 - 77: i1IIi * i11iIiiIii % iiIii
def OOO00 ( string ) :
 IIIIiIiIi1 = re . compile ( '\[(.+?)\]' ) . findall ( string )
 for I11iiiiI1i in IIIIiIiIi1 : string = string . replace ( I11iiiiI1i , '' ) . replace ( '[/]' , '' ) . replace ( '[]' , '' )
 return string
 if 40 - 40: OO + i1IIi * i1I
def O0oOOoooOO0O ( string ) :
 string = string . split ( ' ' )
 ooo00Ooo = ''
 for Oo0o0O00 in string :
  ii1 = '[B][COLOR red]' + Oo0o0O00 [ 0 ] . upper ( ) + '[/COLOR][COLOR white]' + Oo0o0O00 [ 1 : ] + '[/COLOR][/B] '
  ooo00Ooo = ooo00Ooo + ii1
 return ooo00Ooo
 if 39 - 39: ooO0o0Oo / oo0oooooO0 . iiIii % O0 * Oo00OOOOO + ooO00oOoo
def OOI1iI1ii1II ( name , url , mode , iconimage , itemcount , isFolder = False ) :
 if iI1Ii11111iIi == 'true' :
  if not 'COLOR' in name :
   O0oo0O = name . partition ( '(' )
   I1IiI11 = ""
   iI1iiiiIii = ""
   if len ( O0oo0O ) > 0 :
    I1IiI11 = O0oo0O [ 0 ]
    iI1iiiiIii = O0oo0O [ 2 ] . partition ( ')' )
   if len ( iI1iiiiIii ) > 0 :
    iI1iiiiIii = iI1iiiiIii [ 0 ]
   iIiIiIiI = eval ( base64 . b64decode ( 'bWV0YWhhbmRsZXJzLk1ldGFEYXRhKHRtZGJfYXBpX2tleT0iZDk1NWQ4ZjAyYTNmMjQ4MGE1MTg4MWZlNGM5NmYxMGUiKQ==' ) )
   i11 = iIiIiIiI . get_meta ( 'movie' , name = I1IiI11 , year = iI1iiiiIii )
   OOoo = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&site=" + str ( iIIiiiI ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name )
   ii = True
   O0oOo00o = xbmcgui . ListItem ( name , iconImage = i11 [ 'cover_url' ] , thumbnailImage = i11 [ 'cover_url' ] )
   O0oOo00o . setInfo ( type = "Video" , infoLabels = i11 )
   O0oOo00o . setProperty ( "IsPlayable" , "true" )
   oo0 = [ ]
   if o0OoOoOO00 . getSetting ( 'fav' ) == 'yes' : oo0 . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
   if o0OoOoOO00 . getSetting ( 'fav' ) == 'no' : oo0 . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
   O0oOo00o . addContextMenuItems ( oo0 , replaceItems = False )
   if not i11 [ 'backdrop_url' ] == '' : O0oOo00o . setProperty ( 'fanart_image' , i11 [ 'backdrop_url' ] )
   else : O0oOo00o . setProperty ( 'fanart_image' , I1ii11iIi11i )
   ii = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = OOoo , listitem = O0oOo00o , isFolder = isFolder , totalItems = itemcount )
   return ii
 else :
  OOoo = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&site=" + str ( iIIiiiI ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name )
  ii = True
  O0oOo00o = xbmcgui . ListItem ( name , iconImage = iconimage , thumbnailImage = iconimage )
  O0oOo00o . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
  O0oOo00o . setProperty ( 'fanart_image' , I1ii11iIi11i )
  O0oOo00o . setProperty ( "IsPlayable" , "true" )
  oo0 = [ ]
  if o0OoOoOO00 . getSetting ( 'fav' ) == 'yes' : oo0 . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
  if o0OoOoOO00 . getSetting ( 'fav' ) == 'no' : oo0 . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
  O0oOo00o . addContextMenuItems ( oo0 , replaceItems = False )
  ii = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = OOoo , listitem = O0oOo00o , isFolder = isFolder )
  return ii
  if 34 - 34: ooO00oOoo % Oo00OOOOO + oo0oooooO0 * iIii1I11I1II1
def iiiI11 ( name , url , mode , iconimage , fanart , description = '' ) :
 OOoo = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&fanart=" + urllib . quote_plus ( fanart ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 ii = True
 O0oOo00o = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 O0oOo00o . setInfo ( type = "Video" , infoLabels = { "Title" : name , 'plot' : description } )
 O0oOo00o . setProperty ( 'fanart_image' , fanart )
 oo0 = [ ]
 if o0OoOoOO00 . getSetting ( 'fav' ) == 'yes' : oo0 . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 if o0OoOoOO00 . getSetting ( 'fav' ) == 'no' : oo0 . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 O0oOo00o . addContextMenuItems ( oo0 , replaceItems = False )
 if 'plugin://' in url :
  OOoo = url
 ii = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = OOoo , listitem = O0oOo00o , isFolder = True )
 return ii
 if 33 - 33: ooO00oOoo / oo0oooooO0 * i1I / OO + O0OOo / Oo00OOOOO
def OOoO ( name , url , mode , iconimage , fanart , description = '' ) :
 OOoo = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 ii = True
 O0oOo00o = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 O0oOo00o . setProperty ( 'fanart_image' , fanart )
 oo0 = [ ]
 if o0OoOoOO00 . getSetting ( 'fav' ) == 'yes' : oo0 . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 if o0OoOoOO00 . getSetting ( 'fav' ) == 'no' : oo0 . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 O0oOo00o . addContextMenuItems ( oo0 , replaceItems = False )
 ii = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = OOoo , listitem = O0oOo00o , isFolder = False )
 return ii
 if 40 - 40: OO
def ooOoOoo0O ( name , url , mode , iconimage , fanart , description = '' ) :
 OOoo = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 ii = True
 O0oOo00o = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 O0oOo00o . setProperty ( 'fanart_image' , fanart )
 O0oOo00o . setProperty ( "IsPlayable" , "true" )
 oo0 = [ ]
 if o0OoOoOO00 . getSetting ( 'fav' ) == 'yes' : oo0 . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 if o0OoOoOO00 . getSetting ( 'fav' ) == 'no' : oo0 . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 O0oOo00o . addContextMenuItems ( oo0 , replaceItems = False )
 ii = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = OOoo , listitem = O0oOo00o , isFolder = False )
 return ii
 if 60 - 60: OO % OO00OooO0OO * I111I11 % II111iiii
def OOOOoO00o0O ( url , name ) :
 I1I1I1IIi1III = o000o0o00o0Oo ( url )
 if len ( I1I1I1IIi1III ) > 1 :
  ii111iI1iIi1 = i1i1II
  OOO = os . path . join ( os . path . join ( ii111iI1iIi1 , '' ) , name + '.txt' )
  if not os . path . exists ( OOO ) :
   file ( OOO , 'w' ) . close ( )
  II11IiiIII = open ( OOO )
  o0OOOo = II11IiiIII . read ( )
  if o0OOOo == I1I1I1IIi1III : pass
  else :
   oOooOOOoOo ( 'UKTurk' , I1I1I1IIi1III )
   oo0OOo0 = open ( OOO , "w" )
   oo0OOo0 . write ( I1I1I1IIi1III )
   oo0OOo0 . close ( )
   if 11 - 11: iIii1I11I1II1 * iIii1I11I1II1 * ooO00oOoo
def oOooOOOoOo ( heading , text ) :
 id = 10147
 xbmc . executebuiltin ( 'ActivateWindow(%d)' % id )
 xbmc . sleep ( 500 )
 iII1ii1 = xbmcgui . Window ( id )
 I1i1iiiI1 = 50
 while ( I1i1iiiI1 > 0 ) :
  try :
   xbmc . sleep ( 10 )
   I1i1iiiI1 -= 1
   iII1ii1 . getControl ( 1 ) . setLabel ( heading )
   iII1ii1 . getControl ( 5 ) . setText ( text )
   return
  except :
   pass
   if 24 - 24: i1II1I11 / i11iIiiIii + i1II1I11
def I1i11i ( name ) :
 global Icon
 global Next
 global Previous
 global window
 global Quit
 global images
 OOO = os . path . join ( os . path . join ( i1i1II , '' ) , name + '.txt' )
 II11IiiIII = open ( OOO )
 o0OOOo = II11IiiIII . read ( )
 images = re . compile ( '<image>(.+?)</image>' ) . findall ( o0OOOo )
 o0OoOoOO00 . setSetting ( 'pos' , '0' )
 window = pyxbmct . AddonDialogWindow ( '' )
 IiIi = '/resources/art'
 OOOOO0O00 = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + IiII1IiiIiI1 + IiIi , 'next_focus.png' ) )
 Iii = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + IiII1IiiIiI1 + IiIi , 'next1.png' ) )
 iIIiIiI1I1 = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + IiII1IiiIiI1 + IiIi , 'previous_focus.png' ) )
 ooOii = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + IiII1IiiIiI1 + IiIi , 'previous.png' ) )
 OO0O0Ooo = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + IiII1IiiIiI1 + IiIi , 'close_focus.png' ) )
 oOoO0 = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + IiII1IiiIiI1 + IiIi , 'close.png' ) )
 Oo0 = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + IiII1IiiIiI1 + IiIi , 'main-bg1.png' ) )
 window . setGeometry ( 1300 , 720 , 100 , 50 )
 oo0O0o00o0O = pyxbmct . Image ( Oo0 )
 window . placeControl ( oo0O0o00o0O , - 10 , - 10 , 130 , 70 )
 O0Oooo0O = '0xFF000000'
 Previous = pyxbmct . Button ( '' , focusTexture = iIIiIiI1I1 , noFocusTexture = ooOii , textColor = O0Oooo0O , focusedColor = O0Oooo0O )
 Next = pyxbmct . Button ( '' , focusTexture = OOOOO0O00 , noFocusTexture = Iii , textColor = O0Oooo0O , focusedColor = O0Oooo0O )
 Quit = pyxbmct . Button ( '' , focusTexture = OO0O0Ooo , noFocusTexture = oOoO0 , textColor = O0Oooo0O , focusedColor = O0Oooo0O )
 Icon = pyxbmct . Image ( images [ 0 ] , aspectRatio = 1 )
 window . placeControl ( Previous , 102 , 1 , 10 , 10 )
 window . placeControl ( Next , 102 , 40 , 10 , 10 )
 window . placeControl ( Quit , 102 , 21 , 10 , 10 )
 window . placeControl ( Icon , 0 , 0 , 100 , 50 )
 Previous . controlRight ( Next )
 Previous . controlUp ( Quit )
 window . connect ( Previous , I11i1II )
 window . connect ( Next , Ooo )
 Previous . setVisible ( False )
 window . setFocus ( Quit )
 Previous . controlRight ( Quit )
 Quit . controlLeft ( Previous )
 Quit . controlRight ( Next )
 Next . controlLeft ( Quit )
 window . connect ( Quit , window . close )
 window . doModal ( )
 del window
 if 21 - 21: O0OOo
def Ooo ( ) :
 I1ii1 = int ( o0OoOoOO00 . getSetting ( 'pos' ) )
 O00 = int ( I1ii1 ) + 1
 o0OoOoOO00 . setSetting ( 'pos' , str ( O00 ) )
 Oo0o0000OOoO = len ( images )
 Icon . setImage ( images [ int ( O00 ) ] )
 Previous . setVisible ( True )
 if int ( O00 ) == int ( Oo0o0000OOoO ) - 1 :
  Next . setVisible ( False )
  if 46 - 46: O0 * II111iiii - O0OOo * oo0oooooO0
def I11i1II ( ) :
 I1ii1 = int ( o0OoOoOO00 . getSetting ( 'pos' ) )
 i11IIIiIiIi = int ( I1ii1 ) - 1
 o0OoOoOO00 . setSetting ( 'pos' , str ( i11IIIiIiIi ) )
 Icon . setImage ( images [ int ( i11IIIiIiIi ) ] )
 Next . setVisible ( True )
 if int ( i11IIIiIiIi ) == 0 :
  Previous . setVisible ( False )
  if 27 - 27: OO + OO00OooO0OO - i1I + O0 . ooO0o0Oo
def O0OoooO0 ( gobble ) :
 gobble = gobble . replace ( '}' , '' ) . replace ( '{' , '' ) . replace ( ',' , '' ) . replace ( ']' , '' ) . replace ( '[' , '' )
 gobble = gobble + '=='
 gobble = gobble . decode ( 'base64' )
 return gobble
 if 46 - 46: iii1I11ii1i1
def ii1iIi1iIiI1i ( text ) :
 def iiI1iIii1i ( m ) :
  O0Oooo0O = m . group ( 0 )
  if O0Oooo0O [ : 3 ] == "&#x" : return unichr ( int ( O0Oooo0O [ 3 : - 1 ] , 16 ) ) . encode ( 'utf-8' )
  else : return unichr ( int ( O0Oooo0O [ 2 : - 1 ] ) ) . encode ( 'utf-8' )
 try : return re . sub ( "(?i)&#\w+;" , iiI1iIii1i , text . decode ( 'ISO-8859-1' ) . encode ( 'utf-8' ) )
 except : return re . sub ( "(?i)&#\w+;" , iiI1iIii1i , text . encode ( "ascii" , "ignore" ) . encode ( 'utf-8' ) )
 if 70 - 70: I111I11 * O0 . OO0o + ooO00oOoo . iii1I11ii1i1
def iiiiiIIii ( link ) :
 try :
  Ii1iIiII1Ii = re . compile ( '<layouttype>(.+?)</layouttype>' ) . findall ( link ) [ 0 ]
  if Ii1iIiII1Ii == 'thumbnail' : xbmc . executebuiltin ( 'Container.SetViewMode(500)' )
  else : xbmc . executebuiltin ( 'Container.SetViewMode(50)' )
 except : pass
 if 42 - 42: O0 * ooO0o0Oo . O0OOo - ooO00oOoo * iIii1I11I1II1
I1IiiiiI = iI1i11II1i ( ) ; I1 = None ; IIIII = None ; Ii1I1i = None ; iIIiiiI = None ; O0OoOoo00o = None
try : iIIiiiI = urllib . unquote_plus ( I1IiiiiI [ "site" ] )
except : pass
try : I1 = urllib . unquote_plus ( I1IiiiiI [ "url" ] )
except : pass
try : IIIII = urllib . unquote_plus ( I1IiiiiI [ "name" ] )
except : pass
try : Ii1I1i = int ( I1IiiiiI [ "mode" ] )
except : pass
try : O0OoOoo00o = urllib . unquote_plus ( I1IiiiiI [ "iconimage" ] )
except : pass
try : I1ii11iIi11i = urllib . unquote_plus ( I1IiiiiI [ "fanart" ] )
except : pass
try : iII111Ii = urllib . unquote_plus ( [ "description" ] )
except : pass
if 52 - 52: II111iiii % iii1I11ii1i1 . OO00OooO0OO * iIii1I11I1II1
if Ii1I1i == None or I1 == None or len ( I1 ) < 1 : II1Iiii1111i ( )
elif Ii1I1i == 1 : oOoOooOo0o0 ( IIIII , I1 , O0OoOoo00o , I1ii11iIi11i )
elif Ii1I1i == 2 : O0o0O00Oo0o0 ( IIIII , I1 , O0OoOoo00o )
elif Ii1I1i == 3 : O00oO000O0O ( IIIII , I1 , O0OoOoo00o )
elif Ii1I1i == 4 : iiIiIIIiiI ( IIIII , I1 , O0OoOoo00o )
elif Ii1I1i == 5 : oOOOoo0O0oO ( )
elif Ii1I1i == 6 : II1 ( I1 , O0OoOoo00o )
elif Ii1I1i == 7 : i1i1iI1iiiI ( I1 )
elif Ii1I1i == 8 : I1i11i ( IIIII )
elif Ii1I1i == 9 : OO00O0O ( IIIII , I1 )
elif Ii1I1i == 10 : DOSCRAPER ( IIIII , I1 )
elif Ii1I1i == 11 : I11iI ( I1 )
elif Ii1I1i == 12 : O0OO00o0OO ( IIIII , I1 , O0OoOoo00o )
elif Ii1I1i == 13 : i1 ( I1 )
elif Ii1I1i == 14 : i11Iiii ( IIIII , I1 , O0OoOoo00o )
elif Ii1I1i == 15 : oO0O ( I1 )
elif Ii1I1i == 16 : IIIii11 ( IIIII , I1 , O0OoOoo00o )
elif Ii1I1i == 17 : II111iiiI1Ii ( IIIII , I1 )
elif Ii1I1i == 18 : IiI1i ( IIIII , I1 , O0OoOoo00o )
elif Ii1I1i == 19 : ooo00OOOooO ( IIIII , I1 )
elif Ii1I1i == 20 : oOOo0 ( I1 , O0OoOoo00o )
elif Ii1I1i == 21 : O0ooo0O0oo0 ( I1 )
elif Ii1I1i == 22 : OO0oOoOO0oOO0 ( IIIII , I1 , O0OoOoo00o )
elif Ii1I1i == 23 : IIiI1I ( I1 )
elif Ii1I1i == 24 : iII ( IIIII , I1 , O0OoOoo00o )
if 50 - 50: oo0oooooO0 - OO0oo0oOO * iii1I11ii1i1 . OO
xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3
