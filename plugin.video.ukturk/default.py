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
OO0o = 'plugin.video.ukturk'
Oo0Ooo = Addon ( OO0o , sys . argv )
O0O0OO0O0O0 = xbmcaddon . Addon ( id = OO0o )
iiiii = xbmc . translatePath ( O0O0OO0O0O0 . getAddonInfo ( 'profile' ) )
ooo0OO = xbmc . translatePath ( 'special://home/addons/' ) + '/*.*'
II1 = xbmc . translatePath ( 'special://home/addons/' )
O00ooooo00 = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o , 'fanart.jpg' ) )
I1IiiI = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o , 'fanart.jpg' ) )
IIi1IiiiI1Ii = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o , 'icon.png' ) )
I11i11Ii = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o , 'next.png' ) )
oO00oOo = O0O0OO0O0O0 . getSetting ( 'adult' )
OOOo0 = O0O0OO0O0O0 . getSetting ( 'password' )
Oooo000o = int ( O0O0OO0O0O0 . getSetting ( 'count' ) )
IiIi11iIIi1Ii = O0O0OO0O0O0 . getSetting ( 'enable_meta' )
Oo0O = xbmc . translatePath ( 'special://home/userdata/addon_data/' + OO0o )
IiI = xbmc . translatePath ( os . path . join ( 'special://home/userdata/Database' , 'UKTurk.db' ) )
ooOo = 'http://ukturk.offshorepastebin.com/ukturk2.jpg'
Oo = 'https://www.googleapis.com/youtube/v3/search?q='
o0O = '&regionCode=US&part=snippet&hl=en_US&key=AIzaSyAd-YEOqZz9nXVzGtn3KWzYLbLaajhqIDA&type=video&maxResults=50'
IiiIII111iI = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId='
IiII = '&maxResults=50&key=AIzaSyAd-YEOqZz9nXVzGtn3KWzYLbLaajhqIDA'
iI1Ii11111iIi = open ( IiI , 'a' )
iI1Ii11111iIi . close ( )
net = net . Net ( )
if 41 - 41: I1II1
def Ooo0OO0oOO ( ) :
 O0O0OO0O0O0 . setSetting ( 'fav' , 'no' )
 if not os . path . exists ( Oo0O ) :
  os . mkdir ( Oo0O )
 oooO0oo0oOOOO = O0oO ( ooOo )
 o0oO0 = re . compile ( '<index>(.+?)</index>' ) . findall ( oooO0oo0oOOOO ) [ 0 ]
 oooO0oo0oOOOO = O0oO ( o0oO0 )
 oo00 = re . compile ( 'name="(.+?)".+?rl="(.+?)".+?mg="(.+?)"' , re . DOTALL ) . findall ( oooO0oo0oOOOO )
 for o00 , Oo0oO0ooo , o0oOoO00o in oo00 :
  if not 'XXX' in o00 :
   i1 ( o00 , Oo0oO0ooo , 1 , o0oOoO00o , O00ooooo00 )
  if 'XXX' in o00 :
   if oO00oOo == 'true' :
    if OOOo0 == '' :
     oOOoo00O0O = xbmcgui . Dialog ( )
     i1111 = oOOoo00O0O . yesno ( 'Adult Content' , 'You have opted to show adult content' , '' , 'Please set a password to prevent accidental access' , 'Cancel' , 'Lets Go' )
     if i1111 == 1 :
      i11 = xbmc . Keyboard ( '' , 'Set Password' )
      i11 . doModal ( )
      if ( i11 . isConfirmed ( ) ) :
       I11 = i11 . getText ( )
       O0O0OO0O0O0 . setSetting ( 'password' , I11 )
      i1 ( o00 , Oo0oO0ooo , 1 , o0oOoO00o , O00ooooo00 )
   if oO00oOo == 'true' :
    if OOOo0 <> '' :
     i1 ( o00 , Oo0oO0ooo , 1 , o0oOoO00o , O00ooooo00 )
 i1 ( 'Favourites' , IiI , 15 , 'http://ukturk.offshorepastebin.com/UKTurk/thumbs/new/Uk%20turk%20thumbnails%20favourites.jpg' , O00ooooo00 )
 i1 ( 'Search' , 'url' , 5 , 'http://ukturk.offshorepastebin.com/UKTurk/thumbs/new/Uk%20turk%20thumbnails%20search.jpg' , O00ooooo00 )
 xbmc . executebuiltin ( 'Container.SetViewMode(500)' )
 if 98 - 98: I1111 * o0o0Oo0oooo0 / I1I1i1 * oO0 / IIIi1i1I
def OOoOoo00oo ( url ) :
 O0O0OO0O0O0 . setSetting ( 'fav' , 'yes' )
 iiI11 = None
 file = open ( IiI , 'r' )
 iiI11 = file . read ( )
 oo00 = re . compile ( "<item>(.+?)</item>" , re . DOTALL ) . findall ( iiI11 )
 for OOooO in oo00 :
  OOoO00o = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>' , re . DOTALL ) . findall ( OOooO )
  for o00 , url , o0oOoO00o in OOoO00o :
   if '.txt' in url :
    i1 ( o00 , url , 1 , o0oOoO00o , O00ooooo00 )
   else :
    II111iiii ( o00 , url , 2 , o0oOoO00o , O00ooooo00 )
    if 48 - 48: I1Ii . IiIi1Iii1I1 - O0O0O0O00OooO % Ooooo % i1iIIIiI1I - OOoO000O0OO
def iiI1IiI ( name , url , iconimage ) :
 url = url . replace ( ' ' , '%20' )
 iconimage = iconimage . replace ( ' ' , '%20' )
 II = '<FAV><item>\n<title>' + name + '</title>\n<link>' + url + '</link>\n' + '<thumbnail>' + iconimage + '</thumbnail>\n</item></FAV>\n'
 iI1Ii11111iIi = open ( IiI , 'a' )
 iI1Ii11111iIi . write ( II )
 iI1Ii11111iIi . close ( )
 if 57 - 57: ooOoo0O
def OooO0 ( name , url , iconimage ) :
 iiI11 = None
 file = open ( IiI , 'r' )
 iiI11 = file . read ( )
 II11iiii1Ii = ''
 oo00 = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( iiI11 )
 for OOoO00o in oo00 :
  II = '\n<FAV><item>\n' + OOoO00o + '</item>\n'
  if name in OOoO00o :
   II = II . replace ( 'item' , ' ' )
  II11iiii1Ii = II11iiii1Ii + II
 file = open ( IiI , 'w' )
 file . truncate ( )
 file . write ( II11iiii1Ii )
 file . close ( )
 xbmc . executebuiltin ( 'Container.Refresh' )
 if 70 - 70: O00 / i1I1i1Ii11 . IIIIII11i1I - o0o0OOO0o0 % ooOOOo0oo0O0
def o0 ( name , url , iconimage , fanart ) :
 I11II1i = IIIII ( name )
 O0O0OO0O0O0 . setSetting ( 'tv' , I11II1i )
 oooO0oo0oOOOO = O0oO ( url )
 ooooooO0oo ( oooO0oo0oOOOO )
 if '/UKTurk/TurkishTV.txt' in url : IIiiiiiiIi1I1 ( )
 if '/UKTurk/tv shows/Index.txt' in url : I1IIIii ( )
 if 'Index' in url :
  oOoOooOo0o0 ( url )
 if 'XXX' in name : OOOO ( oooO0oo0oOOOO )
 oo00 = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( oooO0oo0oOOOO )
 Oooo000o = str ( len ( oo00 ) )
 O0O0OO0O0O0 . setSetting ( 'count' , Oooo000o )
 O0O0OO0O0O0 . setSetting ( 'fav' , 'no' )
 for OOooO in oo00 :
  try :
   if '<sportsdevil>' in OOooO : OOO00 ( OOooO , url , iconimage )
   elif '<iptv>' in OOooO : iiiiiIIii ( OOooO )
   elif '<Image>' in OOooO : O000OO0 ( OOooO )
   elif '<text>' in OOooO : I11iii1Ii ( OOooO )
   elif '<scraper>' in OOooO : I1IIiiIiii ( OOooO )
   elif '<redirect>' in OOooO : REDIRECT ( OOooO )
   elif '<oktitle>' in OOooO : O000oo0O ( OOooO )
   elif '<dl>' in OOooO : OOOOi11i1 ( OOooO )
   elif '<scraper>' in OOooO : I1IIiiIiii ( OOooO )
   else : IIIii1II1II ( OOooO , url , iconimage )
  except : pass
  if 42 - 42: OoO0O0o0Ooo + i1iIIIiI1I
def I1IIIii ( ) :
 O0O0OO0O0O0 . setSetting ( 'fav' , 'no' )
 Oo0oO0ooo = 'https://watchseries-online.pl/last-350-episodes'
 i1 ( 'New Episodes of TV Shows' , Oo0oO0ooo , 23 , 'http://ukturk.offshorepastebin.com/UKTurk/tv%20shows/Uk turk thumbnails new episodes tv shows1.jpg' , O00ooooo00 , description = '' )
 if 56 - 56: OoO0O0o0Ooo
def o0OO00oO ( url ) :
 O0O0OO0O0O0 . setSetting ( 'fav' , 'no' )
 I11i1I1I = tv . TVShows ( url )
 oo00 = re . compile ( '<start>(.+?)<sep>(.+?)<end>' ) . findall ( str ( I11i1I1I ) )
 for o00 , url in oo00 :
  II111iiii ( o00 , url , 24 , o0oOoO00o , O00ooooo00 , description = '' )
 xbmc . executebuiltin ( 'Container.SetViewMode(50)' )
 if 83 - 83: i1iIIIiI1I / OoO0O0o0Ooo
def iIIIIii1 ( name , url , iconimage ) :
 O0O0OO0O0O0 . setSetting ( 'fav' , 'no' )
 oo000OO00Oo = [ 'vidto.me' , 'gorillavid.in' , 'vidzi.tv' , 'rapidvideo.ws' ]
 Oooo000o = [ ]
 O0OOO0OOoO0O = [ ]
 O00Oo000ooO0 = tv . Stream ( url )
 OoO0O00 = 1
 for oooO0oo0oOOOO in O00Oo000ooO0 :
  if urlresolver . HostedMediaFile ( oooO0oo0oOOOO ) . valid_url ( ) :
   for IIiII in oo000OO00Oo :
    if IIiII in oooO0oo0oOOOO :
     Oooo000o . append ( 'Link ' + str ( OoO0O00 ) )
     O0OOO0OOoO0O . append ( oooO0oo0oOOOO )
     OoO0O00 = OoO0O00 + 1
 oOOoo00O0O = xbmcgui . Dialog ( )
 o0ooOooo000oOO = oOOoo00O0O . select ( 'Choose a link..' , Oooo000o )
 if o0ooOooo000oOO < 0 : quit ( )
 url = O0OOO0OOoO0O [ o0ooOooo000oOO ]
 Oo0oOOo ( name , url , iconimage )
 if 58 - 58: oO0 * ooOoo0O * i1iIIIiI1I / ooOoo0O
def IIiiiiiiIi1I1 ( ) :
 Oo0oO0ooo = 'http://www.hergundizi.net'
 i1 ( '[COLOR gold]**** Yerli Yeni Eklenenler Diziler ****[/COLOR]' , Oo0oO0ooo , 21 , o0oOoO00o , O00ooooo00 , description = '' )
 if 75 - 75: OOoO000O0OO
def I1III ( url ) :
 I11i1I1I = hergundizi . TVShows ( url )
 oo00 = re . compile ( '<start>(.+?)<sep>(.+?)<sep>(.+?)<end>' ) . findall ( str ( I11i1I1I ) )
 for o00 , url , o0oOoO00o in oo00 :
  if not 'dızlar' in o00 :
   II111iiii ( o00 , url , 22 , o0oOoO00o , O00ooooo00 , description = '' )
 try :
  OO0O0OoOO0 = re . compile ( '<np>(.+?)<np>' ) . findall ( str ( I11i1I1I ) ) [ 0 ]
  i1 ( 'Next Page>>' , OO0O0OoOO0 , 21 , I11i11Ii , O00ooooo00 , description = '' )
 except : pass
 xbmc . executebuiltin ( 'Container.SetViewMode(50)' )
 if 10 - 10: o0o0Oo0oooo0 % I1111
def O00o0O00 ( name , url , iconimage ) :
 ii111111I1iII = hergundizi . Parts ( url )
 O00ooo0O0 = len ( ii111111I1iII )
 if O00ooo0O0 > 1 :
  Oooo000o = [ ]
  OoO0O00 = 1
  for i1iIi1iIi1i in ii111111I1iII :
   Oooo000o . append ( 'Part ' + str ( OoO0O00 ) )
   OoO0O00 = OoO0O00 + 1
   oOOoo00O0O = xbmcgui . Dialog ( )
  o0ooOooo000oOO = oOOoo00O0O . select ( 'Choose a Part..' , Oooo000o )
  if o0ooOooo000oOO < 0 : quit ( )
  url = ii111111I1iII [ o0ooOooo000oOO ]
 I1I1iIiII1 = hergundizi . Stream ( url )
 Oo0oOOo ( name , I1I1iIiII1 , iconimage )
 if 4 - 4: OoO0O0o0Ooo + I1II1 * ooOoo0O
def I1IIiiIiii ( item ) :
 o00 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 o0oOoO00o = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 Oo0oO0ooo = re . compile ( '<scraper>(.+?)</scraper>' ) . findall ( item ) [ 0 ]
 i1 ( o00 , Oo0oO0ooo , 20 , o0oOoO00o , O00ooooo00 )
 if 55 - 55: I1Ii + I1111 / O0O0O0O00OooO * OOoO000O0OO - i11iIiiIii - i1I1i1Ii11
def ii1ii1ii ( url , iconimage ) :
 II = url + '.scrape()'
 oooO0oo0oOOOO = eval ( II )
 oo00 = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( oooO0oo0oOOOO )
 Oooo000o = str ( len ( oo00 ) )
 O0O0OO0O0O0 . setSetting ( 'count' , Oooo000o )
 O0O0OO0O0O0 . setSetting ( 'fav' , 'no' )
 for OOooO in oo00 :
  try :
   if '<sportsdevil>' in OOooO : OOO00 ( OOooO , url , iconimage )
   elif '<iptv>' in OOooO : iiiiiIIii ( OOooO )
   elif '<Image>' in OOooO : O000OO0 ( OOooO )
   elif '<text>' in OOooO : I11iii1Ii ( OOooO )
   elif '<scraper>' in OOooO : I1IIiiIiii ( OOooO )
   elif '<redirect>' in OOooO : REDIRECT ( OOooO )
   elif '<oktitle>' in OOooO : O000oo0O ( OOooO )
   elif '<dl>' in OOooO : OOOOi11i1 ( OOooO )
   elif '<scraper>' in OOooO : I1IIiiIiii ( OOooO , iconimage )
   else : IIIii1II1II ( OOooO , url , iconimage )
  except : pass
  if 91 - 91: o0o0OOO0o0
def OOOOi11i1 ( item ) :
 o00 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 Oo0oO0ooo = re . compile ( '<dl>(.+?)</dl>' ) . findall ( item ) [ 0 ]
 o0oOoO00o = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 iiIii ( o00 , Oo0oO0ooo , 19 , o0oOoO00o , O00ooooo00 )
 if 79 - 79: o0o0Oo0oooo0 / I1II1
def OO0OoO0o00 ( name , url ) :
 ooOO0O0ooOooO = url . split ( '/' ) [ - 1 ]
 if ooOO0O0ooOooO == 'latest' : ooOO0O0ooOooO = 'AceStreamEngine.apk'
 import downloader
 oOOoo00O0O = xbmcgui . Dialog ( )
 oOOOo00O00oOo = xbmcgui . DialogProgress ( )
 iiIIIi = oOOoo00O0O . browse ( 0 , 'Select folder to download to' , 'myprograms' )
 ooo00OOOooO = os . path . join ( iiIIIi , ooOO0O0ooOooO )
 oOOOo00O00oOo . create ( 'Downloading' , '' , '' , 'Please Wait' )
 downloader . download ( url , ooo00OOOooO , oOOOo00O00oOo )
 oOOOo00O00oOo . close ( )
 oOOoo00O0O = xbmcgui . Dialog ( )
 oOOoo00O0O . ok ( 'Download complete' , 'Please install from..' , iiIIIi )
 if 67 - 67: O00 * OOoO000O0OO * i1iIIIiI1I + ooOoo0O / I1I1i1
def O000oo0O ( item ) :
 o00 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 I1I111 = re . compile ( '<oktitle>(.+?)</oktitle>' ) . findall ( item ) [ 0 ]
 Oo00oo0oO = re . compile ( '<line1>(.+?)</line1>' ) . findall ( item ) [ 0 ]
 IIiIi1iI = re . compile ( '<line2>(.+?)</line2>' ) . findall ( item ) [ 0 ]
 i1IiiiI1iI = re . compile ( '<line3>(.+?)</line3>' ) . findall ( item ) [ 0 ]
 i1iIi = '##' + I1I111 + '#' + Oo00oo0oO + '#' + IIiIi1iI + '#' + i1IiiiI1iI + '##'
 o0oOoO00o = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 iiIii ( o00 , i1iIi , 17 , o0oOoO00o , O00ooooo00 )
 if 68 - 68: i11iIiiIii % i1iIIIiI1I + i11iIiiIii
def iii ( name , url ) :
 II1I = re . compile ( '##(.+?)##' ) . findall ( url ) [ 0 ] . split ( '#' )
 oOOoo00O0O = xbmcgui . Dialog ( )
 oOOoo00O0O . ok ( II1I [ 0 ] , II1I [ 1 ] , II1I [ 2 ] , II1I [ 3 ] )
 if 84 - 84: o0o0OOO0o0 . i11iIiiIii . o0o0OOO0o0 * i1iIIIiI1I - O00
def I11iii1Ii ( item ) :
 o00 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 i1iIi = re . compile ( '<text>(.+?)</text>' ) . findall ( item ) [ 0 ]
 o0oOoO00o = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 iiIii ( o00 , i1iIi , 9 , o0oOoO00o , O00ooooo00 )
 if 42 - 42: i11iIiiIii
def I11i1iIII ( name , url ) :
 iiIiI = O0oO ( url )
 o00oooO0Oo ( name , iiIiI )
 if 78 - 78: i1I1i1Ii11 % ooOOOo0oo0O0 + i1iIIIiI1I
def O000OO0 ( item ) :
 OOooOoooOoOo = re . compile ( '<Image>(.+?)</Image>' ) . findall ( item )
 if len ( OOooOoooOoOo ) == 1 :
  o00 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  o0oOoO00o = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  o0OOOO00O0Oo = re . compile ( '<Image>(.+?)</Image>' ) . findall ( item ) [ 0 ]
  o0oOoO00o = o0OOOO00O0Oo . replace ( 'http://imgur.com/' , 'http://i.imgur.com/' ) + '.jpg'
  o0OOOO00O0Oo = o0OOOO00O0Oo . replace ( 'http://imgur.com/' , 'http://i.imgur.com/' ) + '.jpg'
  iiIii ( o00 , o0OOOO00O0Oo , 7 , o0oOoO00o , O00ooooo00 )
 elif len ( OOooOoooOoOo ) > 1 :
  o00 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  o0oOoO00o = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  ii = ''
  for o0OOOO00O0Oo in OOooOoooOoOo :
   o0oOoO00o = o0OOOO00O0Oo . replace ( 'http://imgur.com/' , 'http://i.imgur.com/' ) + '.jpg'
   o0OOOO00O0Oo = o0OOOO00O0Oo . replace ( 'http://imgur.com/' , 'http://i.imgur.com/' ) + '.jpg'
   ii = ii + '<Image>' + o0OOOO00O0Oo + '</Image>'
  oOooOOOoOo = Oo0O
  o00 = IIIII ( o00 )
  i1Iii1i1I = os . path . join ( os . path . join ( oOooOOOoOo , '' ) , o00 + '.txt' )
  if not os . path . exists ( i1Iii1i1I ) : file ( i1Iii1i1I , 'w' ) . close ( )
  OOoO00 = open ( i1Iii1i1I , "w" )
  OOoO00 . write ( ii )
  OOoO00 . close ( )
  iiIii ( o00 , 'image' , 8 , o0oOoO00o , O00ooooo00 )
  if 40 - 40: IIIi1i1I * i1I1i1Ii11 + ooOoo0O % IIIIII11i1I
def iiiiiIIii ( item ) :
 o00 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 o0oOoO00o = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 Oo0oO0ooo = re . compile ( '<iptv>(.+?)</iptv>' ) . findall ( item ) [ 0 ]
 i1 ( o00 , Oo0oO0ooo , 6 , o0oOoO00o , O00ooooo00 )
 if 74 - 74: OOoO000O0OO - I1Ii + o0o0Oo0oooo0 + ooOOOo0oo0O0 / O0O0O0O00OooO
def i1I1iI1iIi111i ( url , iconimage ) :
 oooO0oo0oOOOO = O0oO ( url )
 iiIi1IIi1I = re . compile ( '^#.+?:-?[0-9]*(.*?),(.*?)\n(.*?)$' , re . I + re . M + re . U + re . S ) . findall ( oooO0oo0oOOOO )
 o0OoOO000ooO0 = [ ]
 for o0o0o0oO0oOO , o00 , url in iiIi1IIi1I :
  ii1Ii11I = { "params" : o0o0o0oO0oOO , "name" : o00 , "url" : url }
  o0OoOO000ooO0 . append ( ii1Ii11I )
 list = [ ]
 for o00o0 in o0OoOO000ooO0 :
  ii1Ii11I = { "name" : o00o0 [ "name" ] , "url" : o00o0 [ "url" ] }
  iiIi1IIi1I = re . compile ( ' (.+?)="(.+?)"' , re . I + re . M + re . U + re . S ) . findall ( o00o0 [ "params" ] )
  for iiOOooooO0Oo , OO in iiIi1IIi1I :
   ii1Ii11I [ iiOOooooO0Oo . strip ( ) . lower ( ) . replace ( '-' , '_' ) ] = OO . strip ( )
  list . append ( ii1Ii11I )
 for o00o0 in list :
  if '.ts' in o00o0 [ "url" ] : iiIii ( o00o0 [ "name" ] , o00o0 [ "url" ] , 2 , iconimage , O00ooooo00 )
  else : II111iiii ( o00o0 [ "name" ] , o00o0 [ "url" ] , 2 , iconimage , O00ooooo00 )
  if 25 - 25: IiIi1Iii1I1
def IIIii1II1II ( item , url , iconimage ) :
 oOo0oO = iconimage
 OOOO0oo0 = url
 O0OOO0OOoO0O = re . compile ( '<link>(.+?)</link>' ) . findall ( item )
 OOoO00o = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>' , re . DOTALL ) . findall ( item )
 for o00 , I11iiI1i1 , iconimage in OOoO00o :
  if 'youtube.com/playlist?' in I11iiI1i1 :
   I1i1Iiiii = I11iiI1i1 . split ( 'list=' ) [ 1 ]
   i1 ( o00 , I11iiI1i1 , OOo0oO00ooO00 , iconimage , O00ooooo00 , description = I1i1Iiiii )
 if len ( O0OOO0OOoO0O ) == 1 :
  o00 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  url = re . compile ( '<link>(.+?)</link>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  if iconimage == 'ImageHere' : iconimage = oOo0oO
  if '.ts' in url : iiIii ( o00 , url , 16 , iconimage , O00ooooo00 , description = '' )
  elif 'movies' in OOOO0oo0 :
   oOO0O00oO0Ooo ( o00 , url , 2 , iconimage , int ( Oooo000o ) , isFolder = False )
  else : II111iiii ( o00 , url , 2 , iconimage , O00ooooo00 )
 elif len ( O0OOO0OOoO0O ) > 1 :
  o00 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  if iconimage == 'ImageHere' : iconimage = oOo0oO
  if '.ts' in url : iiIii ( o00 , url , 16 , iconimage , O00ooooo00 , description = '' )
  elif 'movies' in OOOO0oo0 :
   oOO0O00oO0Ooo ( o00 , url , 3 , iconimage , int ( Oooo000o ) , isFolder = False )
  else : II111iiii ( o00 , url , 3 , iconimage , O00ooooo00 )
  if 67 - 67: IiIi1Iii1I1 - ooOoo0O
def oOoOooOo0o0 ( url ) :
 oooO0oo0oOOOO = O0oO ( url )
 oo00 = re . compile ( 'name="(.+?)".+?rl="(.+?)".+?mg="(.+?)"' , re . DOTALL ) . findall ( oooO0oo0oOOOO )
 for o00 , url , IIi1IiiiI1Ii in oo00 :
  if 'youtube.com/playlist?list=' in url :
   i1 ( o00 , url , 18 , IIi1IiiiI1Ii , O00ooooo00 )
  elif 'youtube.com/results?search_query=' in url :
   i1 ( o00 , url , 18 , IIi1IiiiI1Ii , O00ooooo00 )
  else :
   i1 ( o00 , url , 1 , IIi1IiiiI1Ii , O00ooooo00 )
   if 36 - 36: o0o0OOO0o0
def I11iI ( name , url , iconimage ) :
 if 'youtube.com/results?search_query=' in url :
  I1i1Iiiii = url . split ( 'search_query=' ) [ 1 ]
  I1iI1ii1II = Oo + I1i1Iiiii + o0O
  O0O0OOOOoo = urllib2 . Request ( I1iI1ii1II )
  O0O0OOOOoo . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' )
  oOooO0 = urllib2 . urlopen ( O0O0OOOOoo )
  oooO0oo0oOOOO = oOooO0 . read ( )
  oOooO0 . close ( )
  oooO0oo0oOOOO = oooO0oo0oOOOO . replace ( '\r' , '' ) . replace ( '\n' , '' ) . replace ( '  ' , '' )
  oo00 = re . compile ( '"videoId": "(.+?)".+?"title": "(.+?)"' , re . DOTALL ) . findall ( oooO0oo0oOOOO )
  for Ii1I1Ii , name in oo00 :
   url = 'https://www.youtube.com/watch?v=' + Ii1I1Ii
   iconimage = 'https://i.ytimg.com/vi/%s/hqdefault.jpg' % Ii1I1Ii
   II111iiii ( name , url , 2 , iconimage , O00ooooo00 )
 elif 'youtube.com/playlist?list=' in url :
  I1i1Iiiii = url . split ( 'playlist?list=' ) [ 1 ]
  I1iI1ii1II = IiiIII111iI + I1i1Iiiii + IiII
  O0O0OOOOoo = urllib2 . Request ( I1iI1ii1II )
  O0O0OOOOoo . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' )
  oOooO0 = urllib2 . urlopen ( O0O0OOOOoo )
  oooO0oo0oOOOO = oOooO0 . read ( )
  oOooO0 . close ( )
  oooO0oo0oOOOO = oooO0oo0oOOOO . replace ( '\r' , '' ) . replace ( '\n' , '' ) . replace ( '  ' , '' )
  oo00 = re . compile ( '"title": "(.+?)".+?"videoId": "(.+?)"' , re . DOTALL ) . findall ( oooO0oo0oOOOO )
  for name , Ii1I1Ii in oo00 :
   url = 'https://www.youtube.com/watch?v=' + Ii1I1Ii
   iconimage = 'https://i.ytimg.com/vi/%s/hqdefault.jpg' % Ii1I1Ii
   II111iiii ( name , url , 2 , iconimage , O00ooooo00 )
   if 69 - 69: IIIi1i1I / Ooooo . o0o0OOO0o0 * ooOOOo0oo0O0 % i1I1i1Ii11 - Ooooo
def i1i ( item ) :
 item = item . replace ( '\r' , '' ) . replace ( '\t' , '' ) . replace ( '&nbsp;' , '' ) . replace ( '\'' , '' ) . replace ( '\n' , '' )
 OOoO00o = re . compile ( 'name="(.+?)".+?rl="(.+?)".+?mg="(.+?)"' , re . DOTALL ) . findall ( item )
 for o00 , Oo0oO0ooo , o0oOoO00o in OOoO00o :
  if 'youtube.com/channel/' in Oo0oO0ooo :
   I1i1Iiiii = Oo0oO0ooo . split ( 'channel/' ) [ 1 ]
   i1 ( o00 , Oo0oO0ooo , OOo0oO00ooO00 , o0oOoO00o , O00ooooo00 , description = I1i1Iiiii )
  elif 'youtube.com/user/' in Oo0oO0ooo :
   I1i1Iiiii = Oo0oO0ooo . split ( 'user/' ) [ 1 ]
   i1 ( o00 , Oo0oO0ooo , OOo0oO00ooO00 , o0oOoO00o , O00ooooo00 , description = I1i1Iiiii )
  elif 'youtube.com/playlist?' in Oo0oO0ooo :
   I1i1Iiiii = Oo0oO0ooo . split ( 'list=' ) [ 1 ]
   i1 ( o00 , Oo0oO0ooo , OOo0oO00ooO00 , o0oOoO00o , O00ooooo00 , description = I1i1Iiiii )
  elif 'plugin://' in Oo0oO0ooo :
   oOOoo00O00o = HTMLParser ( )
   Oo0oO0ooo = oOOoo00O00o . unescape ( Oo0oO0ooo )
   i1 ( o00 , Oo0oO0ooo , OOo0oO00ooO00 , o0oOoO00o , O00ooooo00 )
  else :
   i1 ( o00 , Oo0oO0ooo , 1 , o0oOoO00o , O00ooooo00 )
   if 98 - 98: ooOoo0O + o0o0OOO0o0 + OOoO000O0OO % o0o0Oo0oooo0
def OOO00 ( item , url , iconimage ) :
 oOo0oO = iconimage
 O0OOO0OOoO0O = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( item )
 oooooo0O000o = re . compile ( '<link>(.+?)</link>' ) . findall ( item )
 if len ( O0OOO0OOoO0O ) + len ( oooooo0O000o ) == 1 :
  o00 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  url = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( item ) [ 0 ]
  url = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' + url
  if iconimage == 'ImageHere' : iconimage = oOo0oO
  iiIii ( o00 , url , 16 , iconimage , O00ooooo00 )
 elif len ( O0OOO0OOoO0O ) + len ( oooooo0O000o ) > 1 :
  o00 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  if iconimage == 'ImageHere' : iconimage = oOo0oO
  iiIii ( o00 , url , 3 , iconimage , O00ooooo00 )
  if 64 - 64: IIIi1i1I . Ooooo - ooOOOo0oo0O0 / o0o0Oo0oooo0
def OOOO ( link ) :
 if OOOo0 == '' :
  oOOoo00O0O = xbmcgui . Dialog ( )
  i1111 = oOOoo00O0O . yesno ( 'Adult Content' , 'You have opted to show adult content' , '' , 'Please set a password to prevent accidental access' , 'Cancel' , 'OK' )
  if i1111 == 1 :
   i11 = xbmc . Keyboard ( '' , 'Set Password' )
   i11 . doModal ( )
   if ( i11 . isConfirmed ( ) ) :
    I11 = i11 . getText ( )
    O0O0OO0O0O0 . setSetting ( 'password' , I11 )
  else : quit ( )
 elif OOOo0 <> '' :
  oOOoo00O0O = xbmcgui . Dialog ( )
  i1111 = oOOoo00O0O . yesno ( 'Adult Content' , 'Please enter the password you set' , 'to continue' , '' , 'Cancel' , 'OK' )
  if i1111 == 1 :
   i11 = xbmc . Keyboard ( '' , 'Enter Password' )
   i11 . doModal ( )
   if ( i11 . isConfirmed ( ) ) :
    I11 = i11 . getText ( )
   if I11 <> OOOo0 :
    quit ( )
  else : quit ( )
  if 66 - 66: IIIIII11i1I - IIIIII11i1I - i11iIiiIii . i1iIIIiI1I - ooOoo0O
def oOOo0O00o ( ) :
 i11 = xbmc . Keyboard ( '' , 'Search' )
 i11 . doModal ( )
 if ( i11 . isConfirmed ( ) ) :
  I1i1Iiiii = i11 . getText ( )
  I1i1Iiiii = I1i1Iiiii . upper ( )
 else : quit ( )
 oooO0oo0oOOOO = O0oO ( ooOo )
 iIiIi11 = re . compile ( '<link>(.+?)</link>' ) . findall ( oooO0oo0oOOOO )
 for Oo0oO0ooo in iIiIi11 :
  try :
   oooO0oo0oOOOO = O0oO ( Oo0oO0ooo )
   OOO = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( oooO0oo0oOOOO )
   for OOooO in OOO :
    oo00 = re . compile ( '<title>(.+?)</title>' ) . findall ( OOooO )
    for iiiiI in oo00 :
     iiiiI = iiiiI . upper ( )
     if I1i1Iiiii in iiiiI :
      try :
       if '<sportsdevil>' in OOooO : OOO00 ( OOooO , Oo0oO0ooo , o0oOoO00o )
       elif '<iptv>' in OOooO : iiiiiIIii ( OOooO )
       elif '<Image>' in OOooO : O000OO0 ( OOooO )
       elif '<text>' in OOooO : I11iii1Ii ( OOooO )
       elif '<scraper>' in OOooO : I1IIiiIiii ( OOooO )
       elif '<redirect>' in OOooO : REDIRECT ( OOooO )
       elif '<oktitle>' in OOooO : O000oo0O ( OOooO )
       elif '<dl>' in OOooO : OOOOi11i1 ( OOooO )
       elif '<scraper>' in OOooO : I1IIiiIiii ( OOooO , o0oOoO00o )
       else : IIIii1II1II ( OOooO , Oo0oO0ooo , o0oOoO00o )
      except : pass
  except : pass
  if 62 - 62: o0o0Oo0oooo0 * IIIi1i1I
def oOOOoo0O0oO ( name , url , iconimage ) :
 oOo0oO = iconimage
 iIII1I111III = [ ]
 IIo0o0O0O00oOOo = [ ]
 iIIIiIi = [ ]
 oooO0oo0oOOOO = O0oO ( url )
 OO0O0 = re . compile ( '<title>' + re . escape ( name ) + '</title>(.+?)</item>' , re . DOTALL ) . findall ( oooO0oo0oOOOO ) [ 0 ]
 O0OOO0OOoO0O = [ ]
 if '<link>' in OO0O0 :
  I11I11 = re . compile ( '<link>(.+?)</link>' ) . findall ( OO0O0 )
  for o000O0O in I11I11 :
   O0OOO0OOoO0O . append ( o000O0O )
 if '<sportsdevil>' in OO0O0 :
  I1i1i1iii = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( OO0O0 )
  for I1111i in I1i1i1iii :
   I1111i = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' + I1111i
   O0OOO0OOoO0O . append ( I1111i )
 OoO0O00 = 1
 for iIIii in O0OOO0OOoO0O :
  o00O0O = iIIii
  if 'acestream://' in iIIii or '.acelive' in iIIii or 'sop://' in iIIii : ii1iii1i = ' (Acestreams)'
  else : ii1iii1i = ''
  if '(' in iIIii :
   iIIii = iIIii . split ( '(' ) [ 0 ]
   Iii1I1111ii = str ( o00O0O . split ( '(' ) [ 1 ] . replace ( ')' , '' ) + ii1iii1i )
   iIII1I111III . append ( iIIii )
   IIo0o0O0O00oOOo . append ( Iii1I1111ii )
  else :
   ooOoO00 = iIIii . split ( '/' ) [ 2 ] . replace ( 'www.' , '' )
   iIII1I111III . append ( iIIii )
   IIo0o0O0O00oOOo . append ( 'Link ' + str ( OoO0O00 ) + ii1iii1i )
  OoO0O00 = OoO0O00 + 1
 oOOoo00O0O = xbmcgui . Dialog ( )
 o0ooOooo000oOO = oOOoo00O0O . select ( 'Choose a link..' , IIo0o0O0O00oOOo )
 if o0ooOooo000oOO < 0 : quit ( )
 else :
  url = iIII1I111III [ o0ooOooo000oOO ]
  Oo0oOOo ( name , url , iconimage )
  if 14 - 14: I1I1i1 - Ooooo % I1II1 - IiIi1Iii1I1
def ooO0O00Oo0o ( url ) :
 II = "ShowPicture(%s)" % url
 xbmc . executebuiltin ( II )
 if 65 - 65: i1iIIIiI1I . O00 - ooOOOo0oo0O0 * o0o0OOO0o0 / ooOOOo0oo0O0 / OoO0O0o0Ooo
def Oo0oOOo ( name , url , iconimage ) :
 try :
  if 'sop://' in url :
   url = urllib . quote ( url )
   url = 'plugin://program.plexus/?mode=2&url=%s&name=%s' % ( url , name . replace ( ' ' , '+' ) )
   i111iIi1i1II1 ( name , url , iconimage )
  elif 'acestream://' in url or '.acelive' in url :
   url = urllib . quote ( url )
   url = 'plugin://program.plexus/?mode=1&url=%s&name=%s' % ( url , name . replace ( ' ' , '+' ) )
   i111iIi1i1II1 ( name , url , iconimage )
  elif 'plugin://plugin.video.SportsDevil/' in url :
   i111iIi1i1II1 ( name , url , iconimage )
  elif '.ts' in url :
   url = 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;name=' + name + '&amp;url=' + url
   i111iIi1i1II1 ( name , url , iconimage )
  elif urlresolver . HostedMediaFile ( url ) . valid_url ( ) :
   url = urlresolver . HostedMediaFile ( url ) . resolve ( )
   oooO ( name , url , iconimage )
  elif liveresolver . isValid ( url ) == True :
   url = liveresolver . resolve ( url )
   oooO ( name , url , iconimage )
  else : i111iIi1i1II1 ( name , url , iconimage )
 except :
  i1I1i111Ii ( 'UKTurk' , 'Stream Unavailable' , '3000' , IIi1IiiiI1Ii )
  if 67 - 67: IIIi1i1I . I1I1i1
def i1i1iI1iiiI ( url ) :
 if urlresolver . HostedMediaFile ( url ) . valid_url ( ) :
  url = urlresolver . HostedMediaFile ( url ) . resolve ( )
 xbmc . Player ( ) . play ( url )
 if 51 - 51: IIIi1i1I % ooOOOo0oo0O0 . OOoO000O0OO / I1111 / O00 . OOoO000O0OO
def oooO ( name , url , iconimage ) :
 IIIii11 = True
 iiIiIIIiiI = xbmcgui . ListItem ( name , iconImage = iconimage , thumbnailImage = iconimage ) ; iiIiIIIiiI . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
 IIIii11 = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = url , listitem = iiIiIIIiiI )
 iiIiIIIiiI . setPath ( url )
 xbmcplugin . setResolvedUrl ( int ( sys . argv [ 1 ] ) , True , iiIiIIIiiI )
 if 12 - 12: I1II1 - Ooooo
def i111iIi1i1II1 ( name , url , iconimage ) :
 IIIii11 = True
 iiIiIIIiiI = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage ) ; iiIiIIIiiI . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
 IIIii11 = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = url , listitem = iiIiIIIiiI )
 oOOoo00O0O = xbmcgui . Dialog ( )
 xbmc . Player ( ) . play ( url , iiIiIIIiiI , False )
 if 81 - 81: O0O0O0O00OooO - O0O0O0O00OooO . IIIIII11i1I
def o0OoOo00o0o ( url ) :
 xbmc . executebuiltin ( "PlayMedia(%s)" % url )
 if 41 - 41: OoO0O0o0Ooo % IiIi1Iii1I1 - I1Ii * ooOOOo0oo0O0 * I1Ii
def OOOoOO0o ( url ) :
 i1II1 = O0O0OO0O0O0 . getSetting ( 'layout' )
 if i1II1 == 'Listers' : O0O0OO0O0O0 . setSetting ( 'layout' , 'Category' )
 else : O0O0OO0O0O0 . setSetting ( 'layout' , 'Listers' )
 xbmc . executebuiltin ( 'Container.Refresh' )
 if 25 - 25: ooOOOo0oo0O0 / I1111 % IIIIII11i1I
def O0oO ( url ) :
 O0O0OOOOoo = urllib2 . Request ( url )
 O0O0OOOOoo . add_header ( 'User-Agent' , 'mat' )
 oOooO0 = urllib2 . urlopen ( O0O0OOOOoo )
 oooO0oo0oOOOO = oOooO0 . read ( )
 oOooO0 . close ( )
 oooO0oo0oOOOO = oooO0oo0oOOOO . replace ( '</fanart>' , '<fanart>x</fanart>' ) . replace ( '<thumbnail></thumbnail>' , '<thumbnail>x</thumbnail>' ) . replace ( '<utube>' , '<link>https://www.youtube.com/watch?v=' ) . replace ( '</utube>' , '</link>' )
 if '{' in oooO0oo0oOOOO : oooO0oo0oOOOO = IiiiiI1i1Iii ( oooO0oo0oOOOO )
 return oooO0oo0oOOOO
 if 87 - 87: Ooooo
def IiI1iiiIii ( ) :
 I1III1111iIi = [ ]
 I1i111I = sys . argv [ 2 ]
 if len ( I1i111I ) >= 2 :
  o0o0o0oO0oOO = sys . argv [ 2 ]
  Ooo = o0o0o0oO0oOO . replace ( '?' , '' )
  if ( o0o0o0oO0oOO [ len ( o0o0o0oO0oOO ) - 1 ] == '/' ) :
   o0o0o0oO0oOO = o0o0o0oO0oOO [ 0 : len ( o0o0o0oO0oOO ) - 2 ]
  Oo0oo0O0o00O = Ooo . split ( '&' )
  I1III1111iIi = { }
  for OoO0O00 in range ( len ( Oo0oo0O0o00O ) ) :
   I1i11 = { }
   I1i11 = Oo0oo0O0o00O [ OoO0O00 ] . split ( '=' )
   if ( len ( I1i11 ) ) == 2 :
    I1III1111iIi [ I1i11 [ 0 ] ] = I1i11 [ 1 ]
 return I1III1111iIi
 if 12 - 12: I1I1i1 + I1I1i1 - i1iIIIiI1I * I1Ii % I1Ii - oO0
def i1I1i111Ii ( title , message , ms , nart ) :
 xbmc . executebuiltin ( "XBMC.notification(" + title + "," + message + "," + ms + "," + nart + ")" )
 if 52 - 52: OoO0O0o0Ooo . IIIIII11i1I + ooOOOo0oo0O0
def IIIII ( string ) :
 iiii1IIi = re . compile ( '\[(.+?)\]' ) . findall ( string )
 for iII1i11IIi1i in iiii1IIi : string = string . replace ( iII1i11IIi1i , '' ) . replace ( '[/]' , '' ) . replace ( '[]' , '' )
 return string
 if 73 - 73: Ooooo * I1II1 - i11iIiiIii
def O0O0o0oOOO ( string ) :
 string = string . split ( ' ' )
 OOoOoOo = ''
 for o000ooooO0o in string :
  iI1i11 = '[B][COLOR red]' + o000ooooO0o [ 0 ] . upper ( ) + '[/COLOR][COLOR white]' + o000ooooO0o [ 1 : ] + '[/COLOR][/B] '
  OOoOoOo = OOoOoOo + iI1i11
 return OOoOoOo
 if 66 - 66: I1II1 % i1iIIIiI1I + i11iIiiIii . O0O0O0O00OooO / i1I1i1Ii11 + i1iIIIiI1I
def oOO0O00oO0Ooo ( name , url , mode , iconimage , itemcount , isFolder = False ) :
 if IiIi11iIIi1Ii == 'true' :
  if not 'COLOR' in name :
   ooo00Ooo = name . partition ( '(' )
   Oo0o0O00 = ""
   ii1 = ""
   if len ( ooo00Ooo ) > 0 :
    Oo0o0O00 = ooo00Ooo [ 0 ]
    ii1 = ooo00Ooo [ 2 ] . partition ( ')' )
   if len ( ii1 ) > 0 :
    ii1 = ii1 [ 0 ]
   I1i11OO = eval ( base64 . b64decode ( 'bWV0YWhhbmRsZXJzLk1ldGFEYXRhKHRtZGJfYXBpX2tleT0iZDk1NWQ4ZjAyYTNmMjQ4MGE1MTg4MWZlNGM5NmYxMGUiKQ==' ) )
   o0O0oo0OO0O = I1i11OO . get_meta ( 'movie' , name = Oo0o0O00 , year = ii1 )
   OO0 = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&site=" + str ( o0Oooo ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name )
   IIIii11 = True
   iiIiIIIiiI = xbmcgui . ListItem ( name , iconImage = o0O0oo0OO0O [ 'cover_url' ] , thumbnailImage = o0O0oo0OO0O [ 'cover_url' ] )
   iiIiIIIiiI . setInfo ( type = "Video" , infoLabels = o0O0oo0OO0O )
   iiIiIIIiiI . setProperty ( "IsPlayable" , "true" )
   iiI = [ ]
   if O0O0OO0O0O0 . getSetting ( 'fav' ) == 'yes' : iiI . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
   if O0O0OO0O0O0 . getSetting ( 'fav' ) == 'no' : iiI . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
   iiIiIIIiiI . addContextMenuItems ( iiI , replaceItems = False )
   if not o0O0oo0OO0O [ 'backdrop_url' ] == '' : iiIiIIIiiI . setProperty ( 'fanart_image' , o0O0oo0OO0O [ 'backdrop_url' ] )
   else : iiIiIIIiiI . setProperty ( 'fanart_image' , O00ooooo00 )
   IIIii11 = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = OO0 , listitem = iiIiIIIiiI , isFolder = isFolder , totalItems = itemcount )
   return IIIii11
 else :
  OO0 = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&site=" + str ( o0Oooo ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name )
  IIIii11 = True
  iiIiIIIiiI = xbmcgui . ListItem ( name , iconImage = iconimage , thumbnailImage = iconimage )
  iiIiIIIiiI . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
  iiIiIIIiiI . setProperty ( 'fanart_image' , O00ooooo00 )
  iiIiIIIiiI . setProperty ( "IsPlayable" , "true" )
  iiI = [ ]
  if O0O0OO0O0O0 . getSetting ( 'fav' ) == 'yes' : iiI . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
  if O0O0OO0O0O0 . getSetting ( 'fav' ) == 'no' : iiI . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
  iiIiIIIiiI . addContextMenuItems ( iiI , replaceItems = False )
  IIIii11 = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = OO0 , listitem = iiIiIIIiiI , isFolder = isFolder )
  return IIIii11
  if 56 - 56: I1Ii . i1iIIIiI1I . IIIi1i1I
def i1 ( name , url , mode , iconimage , fanart , description = '' ) :
 OO0 = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&fanart=" + urllib . quote_plus ( fanart ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 IIIii11 = True
 iiIiIIIiiI = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 iiIiIIIiiI . setInfo ( type = "Video" , infoLabels = { "Title" : name , 'plot' : description } )
 iiIiIIIiiI . setProperty ( 'fanart_image' , fanart )
 iiI = [ ]
 if O0O0OO0O0O0 . getSetting ( 'fav' ) == 'yes' : iiI . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 if O0O0OO0O0O0 . getSetting ( 'fav' ) == 'no' : iiI . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 iiIiIIIiiI . addContextMenuItems ( iiI , replaceItems = False )
 if 'plugin://' in url :
  OO0 = url
 IIIii11 = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = OO0 , listitem = iiIiIIIiiI , isFolder = True )
 return IIIii11
 if 39 - 39: I1II1 + ooOOOo0oo0O0
def iiIii ( name , url , mode , iconimage , fanart , description = '' ) :
 OO0 = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 IIIii11 = True
 iiIiIIIiiI = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 iiIiIIIiiI . setProperty ( 'fanart_image' , fanart )
 iiI = [ ]
 if O0O0OO0O0O0 . getSetting ( 'fav' ) == 'yes' : iiI . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 if O0O0OO0O0O0 . getSetting ( 'fav' ) == 'no' : iiI . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 iiIiIIIiiI . addContextMenuItems ( iiI , replaceItems = False )
 IIIii11 = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = OO0 , listitem = iiIiIIIiiI , isFolder = False )
 return IIIii11
 if 91 - 91: o0o0Oo0oooo0 - I1111 + O0O0O0O00OooO / IiIi1Iii1I1 . O0O0O0O00OooO + I1II1
def II111iiii ( name , url , mode , iconimage , fanart , description = '' ) :
 OO0 = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 IIIii11 = True
 iiIiIIIiiI = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 iiIiIIIiiI . setProperty ( 'fanart_image' , fanart )
 iiIiIIIiiI . setProperty ( "IsPlayable" , "true" )
 iiI = [ ]
 if O0O0OO0O0O0 . getSetting ( 'fav' ) == 'yes' : iiI . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 if O0O0OO0O0O0 . getSetting ( 'fav' ) == 'no' : iiI . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 iiIiIIIiiI . addContextMenuItems ( iiI , replaceItems = False )
 IIIii11 = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = OO0 , listitem = iiIiIIIiiI , isFolder = False )
 return IIIii11
 if 26 - 26: i1iIIIiI1I - o0o0Oo0oooo0
def iiI1iI111ii1i ( url , name ) :
 Ii1IIiI1IiIII = O0oO ( url )
 if len ( Ii1IIiI1IiIII ) > 1 :
  oOooOOOoOo = Oo0O
  i1Iii1i1I = os . path . join ( os . path . join ( oOooOOOoOo , '' ) , name + '.txt' )
  if not os . path . exists ( i1Iii1i1I ) :
   file ( i1Iii1i1I , 'w' ) . close ( )
  OO0Oo000OOOoO = open ( i1Iii1i1I )
  O0 = OO0Oo000OOOoO . read ( )
  if O0 == Ii1IIiI1IiIII : pass
  else :
   o00oooO0Oo ( 'UKTurk' , Ii1IIiI1IiIII )
   OOoO00 = open ( i1Iii1i1I , "w" )
   OOoO00 . write ( Ii1IIiI1IiIII )
   OOoO00 . close ( )
   if 48 - 48: ooOOOo0oo0O0 - Ooooo % i1I1i1Ii11
def o00oooO0Oo ( heading , text ) :
 id = 10147
 xbmc . executebuiltin ( 'ActivateWindow(%d)' % id )
 xbmc . sleep ( 500 )
 IIi1IIIi = xbmcgui . Window ( id )
 O00Ooo = 50
 while ( O00Ooo > 0 ) :
  try :
   xbmc . sleep ( 10 )
   O00Ooo -= 1
   IIi1IIIi . getControl ( 1 ) . setLabel ( heading )
   IIi1IIIi . getControl ( 5 ) . setText ( text )
   return
  except :
   pass
   if 52 - 52: i1iIIIiI1I - I1Ii + i1iIIIiI1I % Ooooo
def iI1 ( name ) :
 global Icon
 global Next
 global Previous
 global window
 global Quit
 global images
 i1Iii1i1I = os . path . join ( os . path . join ( Oo0O , '' ) , name + '.txt' )
 OO0Oo000OOOoO = open ( i1Iii1i1I )
 O0 = OO0Oo000OOOoO . read ( )
 images = re . compile ( '<image>(.+?)</image>' ) . findall ( O0 )
 O0O0OO0O0O0 . setSetting ( 'pos' , '0' )
 window = pyxbmct . AddonDialogWindow ( '' )
 IiIiI1ii1i = '/resources/art'
 Oo0oooO0oO = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o + IiIiI1ii1i , 'next_focus.png' ) )
 IiIiII1 = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o + IiIiI1ii1i , 'next1.png' ) )
 Iii1iiIi1II = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o + IiIiI1ii1i , 'previous_focus.png' ) )
 OO0O00oOo = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o + IiIiI1ii1i , 'previous.png' ) )
 ii1II = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o + IiIiI1ii1i , 'close_focus.png' ) )
 iI1I = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o + IiIiI1ii1i , 'close.png' ) )
 OooOoOo = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o + IiIiI1ii1i , 'main-bg1.png' ) )
 window . setGeometry ( 1300 , 720 , 100 , 50 )
 III1I1Iii1iiI = pyxbmct . Image ( OooOoOo )
 window . placeControl ( III1I1Iii1iiI , - 10 , - 10 , 130 , 70 )
 i1iIi = '0xFF000000'
 Previous = pyxbmct . Button ( '' , focusTexture = Iii1iiIi1II , noFocusTexture = OO0O00oOo , textColor = i1iIi , focusedColor = i1iIi )
 Next = pyxbmct . Button ( '' , focusTexture = Oo0oooO0oO , noFocusTexture = IiIiII1 , textColor = i1iIi , focusedColor = i1iIi )
 Quit = pyxbmct . Button ( '' , focusTexture = ii1II , noFocusTexture = iI1I , textColor = i1iIi , focusedColor = i1iIi )
 Icon = pyxbmct . Image ( images [ 0 ] , aspectRatio = 1 )
 window . placeControl ( Previous , 102 , 1 , 10 , 10 )
 window . placeControl ( Next , 102 , 40 , 10 , 10 )
 window . placeControl ( Quit , 102 , 21 , 10 , 10 )
 window . placeControl ( Icon , 0 , 0 , 100 , 50 )
 Previous . controlRight ( Next )
 Previous . controlUp ( Quit )
 window . connect ( Previous , i1Iii11I1i )
 window . connect ( Next , Oo00o0OO0O00o )
 Previous . setVisible ( False )
 window . setFocus ( Quit )
 Previous . controlRight ( Quit )
 Quit . controlLeft ( Previous )
 Quit . controlRight ( Next )
 Next . controlLeft ( Quit )
 window . connect ( Quit , window . close )
 window . doModal ( )
 del window
 if 82 - 82: O00 + o0o0Oo0oooo0 - I1I1i1 . I1I1i1
def Oo00o0OO0O00o ( ) :
 iIi1i = int ( O0O0OO0O0O0 . getSetting ( 'pos' ) )
 I1i11111i1i11 = int ( iIi1i ) + 1
 O0O0OO0O0O0 . setSetting ( 'pos' , str ( I1i11111i1i11 ) )
 OOoOOO0 = len ( images )
 Icon . setImage ( images [ int ( I1i11111i1i11 ) ] )
 Previous . setVisible ( True )
 if int ( I1i11111i1i11 ) == int ( OOoOOO0 ) - 1 :
  Next . setVisible ( False )
  if 10 - 10: ooOOOo0oo0O0 / OoO0O0o0Ooo + i11iIiiIii / i1I1i1Ii11
def i1Iii11I1i ( ) :
 iIi1i = int ( O0O0OO0O0O0 . getSetting ( 'pos' ) )
 OOOoOoO = int ( iIi1i ) - 1
 O0O0OO0O0O0 . setSetting ( 'pos' , str ( OOOoOoO ) )
 Icon . setImage ( images [ int ( OOOoOoO ) ] )
 Next . setVisible ( True )
 if int ( OOOoOoO ) == 0 :
  Previous . setVisible ( False )
  if 22 - 22: IIIi1i1I % i1iIIIiI1I
def IiiiiI1i1Iii ( gobble ) :
 gobble = gobble . replace ( '}' , '' ) . replace ( '{' , '' ) . replace ( ',' , '' ) . replace ( ']' , '' ) . replace ( '[' , '' )
 gobble = gobble + '=='
 gobble = gobble . decode ( 'base64' )
 return gobble
 if 57 - 57: ooOoo0O + I1II1 . i1I1i1Ii11
def iIi1i1iIi1iI ( text ) :
 def iiIi1iI1iIii ( m ) :
  i1iIi = m . group ( 0 )
  if i1iIi [ : 3 ] == "&#x" : return unichr ( int ( i1iIi [ 3 : - 1 ] , 16 ) ) . encode ( 'utf-8' )
  else : return unichr ( int ( i1iIi [ 2 : - 1 ] ) ) . encode ( 'utf-8' )
 try : return re . sub ( "(?i)&#\w+;" , iiIi1iI1iIii , text . decode ( 'ISO-8859-1' ) . encode ( 'utf-8' ) )
 except : return re . sub ( "(?i)&#\w+;" , iiIi1iI1iIii , text . encode ( "ascii" , "ignore" ) . encode ( 'utf-8' ) )
 if 68 - 68: ooOoo0O
def ooooooO0oo ( link ) :
 try :
  OooO0oo = re . compile ( '<layouttype>(.+?)</layouttype>' ) . findall ( link ) [ 0 ]
  if OooO0oo == 'thumbnail' : xbmc . executebuiltin ( 'Container.SetViewMode(500)' )
  else : xbmc . executebuiltin ( 'Container.SetViewMode(50)' )
 except : pass
 if 89 - 89: i1I1i1Ii11
o0o0o0oO0oOO = IiI1iiiIii ( ) ; Oo0oO0ooo = None ; o00 = None ; OOo0oO00ooO00 = None ; o0Oooo = None ; o0oOoO00o = None
try : o0Oooo = urllib . unquote_plus ( o0o0o0oO0oOO [ "site" ] )
except : pass
try : Oo0oO0ooo = urllib . unquote_plus ( o0o0o0oO0oOO [ "url" ] )
except : pass
try : o00 = urllib . unquote_plus ( o0o0o0oO0oOO [ "name" ] )
except : pass
try : OOo0oO00ooO00 = int ( o0o0o0oO0oOO [ "mode" ] )
except : pass
try : o0oOoO00o = urllib . unquote_plus ( o0o0o0oO0oOO [ "iconimage" ] )
except : pass
try : O00ooooo00 = urllib . unquote_plus ( o0o0o0oO0oOO [ "fanart" ] )
except : pass
try : ooOoOO0OoO00o = urllib . unquote_plus ( [ "description" ] )
except : pass
if 11 - 11: I1Ii - IIIi1i1I * oO0 . i1iIIIiI1I . OOoO000O0OO
if OOo0oO00ooO00 == None or Oo0oO0ooo == None or len ( Oo0oO0ooo ) < 1 : Ooo0OO0oOO ( )
elif OOo0oO00ooO00 == 1 : o0 ( o00 , Oo0oO0ooo , o0oOoO00o , O00ooooo00 )
elif OOo0oO00ooO00 == 2 : Oo0oOOo ( o00 , Oo0oO0ooo , o0oOoO00o )
elif OOo0oO00ooO00 == 3 : oOOOoo0O0oO ( o00 , Oo0oO0ooo , o0oOoO00o )
elif OOo0oO00ooO00 == 4 : oooO ( o00 , Oo0oO0ooo , o0oOoO00o )
elif OOo0oO00ooO00 == 5 : oOOo0O00o ( )
elif OOo0oO00ooO00 == 6 : i1I1iI1iIi111i ( Oo0oO0ooo , o0oOoO00o )
elif OOo0oO00ooO00 == 7 : ooO0O00Oo0o ( Oo0oO0ooo )
elif OOo0oO00ooO00 == 8 : iI1 ( o00 )
elif OOo0oO00ooO00 == 9 : I11i1iIII ( o00 , Oo0oO0ooo )
elif OOo0oO00ooO00 == 10 : DOSCRAPER ( o00 , Oo0oO0ooo )
elif OOo0oO00ooO00 == 11 : o0OoOo00o0o ( Oo0oO0ooo )
elif OOo0oO00ooO00 == 12 : iiI1IiI ( o00 , Oo0oO0ooo , o0oOoO00o )
elif OOo0oO00ooO00 == 13 : OOOoOO0o ( Oo0oO0ooo )
elif OOo0oO00ooO00 == 14 : OooO0 ( o00 , Oo0oO0ooo , o0oOoO00o )
elif OOo0oO00ooO00 == 15 : OOoOoo00oo ( Oo0oO0ooo )
elif OOo0oO00ooO00 == 16 : i111iIi1i1II1 ( o00 , Oo0oO0ooo , o0oOoO00o )
elif OOo0oO00ooO00 == 17 : iii ( o00 , Oo0oO0ooo )
elif OOo0oO00ooO00 == 18 : I11iI ( o00 , Oo0oO0ooo , o0oOoO00o )
elif OOo0oO00ooO00 == 19 : OO0OoO0o00 ( o00 , Oo0oO0ooo )
elif OOo0oO00ooO00 == 20 : ii1ii1ii ( Oo0oO0ooo , o0oOoO00o )
elif OOo0oO00ooO00 == 21 : I1III ( Oo0oO0ooo )
elif OOo0oO00ooO00 == 22 : O00o0O00 ( o00 , Oo0oO0ooo , o0oOoO00o )
elif OOo0oO00ooO00 == 23 : o0OO00oO ( Oo0oO0ooo )
elif OOo0oO00ooO00 == 24 : iIIIIii1 ( o00 , Oo0oO0ooo , o0oOoO00o )
if 61 - 61: IIIIII11i1I % IIIi1i1I - Ooooo - oO0 % I1II1
xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3
