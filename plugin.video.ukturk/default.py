# -*- coding: utf-8 -*-
import xbmc , xbmcaddon , xbmcgui , xbmcplugin , urllib , urllib2 , os , re , sys , datetime , urlresolver , random , liveresolver , base64 , pyxbmct , glob , net
from resources . lib . common_addon import Addon
from HTMLParser import HTMLParser
from metahandler import metahandlers
from resources . lib import mamahd
from resources . lib import crickfree
from resources . lib import bigsports
from resources . lib import hergundizi
if 64 - 64: i11iIiiIii
if 65 - 65: O0 / iIii1I11I1II1 % OoooooooOO - i1IIi
o0OO00 = 'plugin.video.ukturk'
oo = Addon ( o0OO00 , sys . argv )
i1iII1IiiIiI1 = xbmcaddon . Addon ( id = o0OO00 )
iIiiiI1IiI1I1 = xbmc . translatePath ( i1iII1IiiIiI1 . getAddonInfo ( 'profile' ) )
o0OoOoOO00 = xbmc . translatePath ( 'special://home/addons/' ) + '/*.*'
I11i = xbmc . translatePath ( 'special://home/addons/' )
O0O = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + o0OO00 , 'fanart.jpg' ) )
Oo = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + o0OO00 , 'fanart.jpg' ) )
I1ii11iIi11i = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + o0OO00 , 'icon.png' ) )
I1IiI = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + o0OO00 , 'next.png' ) )
o0OOO = i1iII1IiiIiI1 . getSetting ( 'adult' )
iIiiiI = i1iII1IiiIiI1 . getSetting ( 'password' )
Iii1ii1II11i = int ( i1iII1IiiIiI1 . getSetting ( 'count' ) )
iI111iI = i1iII1IiiIiI1 . getSetting ( 'enable_meta' )
IiII = xbmc . translatePath ( 'special://home/userdata/addon_data/' + o0OO00 )
iI1Ii11111iIi = xbmc . translatePath ( os . path . join ( 'special://home/userdata/Database' , 'UKTurk.db' ) )
i1i1II = 'http://ukturk.offshorepastebin.com/ukturk2.jpg'
O0oo0OO0 = 'https://www.googleapis.com/youtube/v3/search?q='
I1i1iiI1 = '&regionCode=US&part=snippet&hl=en_US&key=AIzaSyAd-YEOqZz9nXVzGtn3KWzYLbLaajhqIDA&type=video&maxResults=50'
iiIIIII1i1iI = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId='
o0oO0 = '&maxResults=50&key=AIzaSyAd-YEOqZz9nXVzGtn3KWzYLbLaajhqIDA'
oo00 = open ( iI1Ii11111iIi , 'a' )
oo00 . close ( )
net = net . Net ( )
if 88 - 88: O0Oo0oO0o . II1iI . i1iIii1Ii1II
def i1I1Iiii1111 ( ) :
 i1iII1IiiIiI1 . setSetting ( 'fav' , 'no' )
 if not os . path . exists ( IiII ) :
  os . mkdir ( IiII )
 i11 = I11 ( i1i1II )
 Oo0o0000o0o0 = re . compile ( '<index>(.+?)</index>' ) . findall ( i11 ) [ 0 ]
 i11 = I11 ( Oo0o0000o0o0 )
 oOo0oooo00o = re . compile ( 'name="(.+?)".+?rl="(.+?)".+?mg="(.+?)"' , re . DOTALL ) . findall ( i11 )
 for oO0o0o0ooO0oO , oo0o0O00 , oO in oOo0oooo00o :
  if not 'XXX' in oO0o0o0ooO0oO :
   i1iiIIiiI111 ( oO0o0o0ooO0oO , oo0o0O00 , 1 , oO , O0O )
  if 'XXX' in oO0o0o0ooO0oO :
   if o0OOO == 'true' :
    if iIiiiI == '' :
     oooOOOOO = xbmcgui . Dialog ( )
     i1iiIII111ii = oooOOOOO . yesno ( 'Adult Content' , 'You have opted to show adult content' , '' , 'Please set a password to prevent accidental access' , 'Cancel' , 'Lets Go' )
     if i1iiIII111ii == 1 :
      i1iIIi1 = xbmc . Keyboard ( '' , 'Set Password' )
      i1iIIi1 . doModal ( )
      if ( i1iIIi1 . isConfirmed ( ) ) :
       ii11iIi1I = i1iIIi1 . getText ( )
       i1iII1IiiIiI1 . setSetting ( 'password' , ii11iIi1I )
      i1iiIIiiI111 ( oO0o0o0ooO0oO , oo0o0O00 , 1 , oO , O0O )
   if o0OOO == 'true' :
    if iIiiiI <> '' :
     i1iiIIiiI111 ( oO0o0o0ooO0oO , oo0o0O00 , 1 , oO , O0O )
 i1iiIIiiI111 ( 'Favourites' , iI1Ii11111iIi , 15 , 'http://ukturk.offshorepastebin.com/UKTurk/thumbs/new/Uk%20turk%20thumbnails%20favourites.jpg' , O0O )
 i1iiIIiiI111 ( 'Search' , 'url' , 5 , 'http://ukturk.offshorepastebin.com/UKTurk/thumbs/new/Uk%20turk%20thumbnails%20search.jpg' , O0O )
 xbmc . executebuiltin ( 'Container.SetViewMode(500)' )
 if 6 - 6: I1I11I1I1I * OooO0OO
def iiiIi ( url ) :
 i1iII1IiiIiI1 . setSetting ( 'fav' , 'yes' )
 IiIIIiI1I1 = None
 file = open ( iI1Ii11111iIi , 'r' )
 IiIIIiI1I1 = file . read ( )
 oOo0oooo00o = re . compile ( "<item>(.+?)</item>" , re . DOTALL ) . findall ( IiIIIiI1I1 )
 for OoO000 in oOo0oooo00o :
  IIiiIiI1 = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>' , re . DOTALL ) . findall ( OoO000 )
  for oO0o0o0ooO0oO , url , oO in IIiiIiI1 :
   if '.txt' in url :
    i1iiIIiiI111 ( oO0o0o0ooO0oO , url , 1 , oO , O0O )
   else :
    iiIiIIi ( oO0o0o0ooO0oO , url , 2 , oO , O0O )
    if 65 - 65: iii1I1
def ooOO0O00 ( name , url , iconimage ) :
 url = url . replace ( ' ' , '%20' )
 iconimage = iconimage . replace ( ' ' , '%20' )
 ii1 = '<FAV><item>\n<title>' + name + '</title>\n<link>' + url + '</link>\n' + '<thumbnail>' + iconimage + '</thumbnail>\n</item></FAV>\n'
 oo00 = open ( iI1Ii11111iIi , 'a' )
 oo00 . write ( ii1 )
 oo00 . close ( )
 if 57 - 57: o0o00ooo0 % oo0Oo00Oo0
def oOOO00o ( name , url , iconimage ) :
 IiIIIiI1I1 = None
 file = open ( iI1Ii11111iIi , 'r' )
 IiIIIiI1I1 = file . read ( )
 O0O00o0OOO0 = ''
 oOo0oooo00o = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( IiIIIiI1I1 )
 for IIiiIiI1 in oOo0oooo00o :
  ii1 = '\n<FAV><item>\n' + IIiiIiI1 + '</item>\n'
  if name in IIiiIiI1 :
   ii1 = ii1 . replace ( 'item' , ' ' )
  O0O00o0OOO0 = O0O00o0OOO0 + ii1
 file = open ( iI1Ii11111iIi , 'w' )
 file . truncate ( )
 file . write ( O0O00o0OOO0 )
 file . close ( )
 xbmc . executebuiltin ( 'Container.Refresh' )
 if 27 - 27: IIII % o0O0 . ii1I11II1ii1i % I1i1iii - IiiI11Iiiii / ii1I1i1I
def OOoo0O0 ( name , url , iconimage , fanart ) :
 iiiIi1i1I = oOO00oOO ( name )
 i1iII1IiiIiI1 . setSetting ( 'tv' , iiiIi1i1I )
 i11 = I11 ( url )
 OoOo ( i11 )
 if 18 - 18: iii11I111
 if 'Index' in url :
  OOOO00ooo0Ooo ( url )
 if 'XXX' in name : OOOooOooo00O0 ( i11 )
 if '/UKTurk/TurkishTV.txt' in url : Oo0OO ( )
 if 92 - 92: oo0Oo00Oo0 - OooO0OO
 oOo0oooo00o = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( i11 )
 Iii1ii1II11i = str ( len ( oOo0oooo00o ) )
 i1iII1IiiIiI1 . setSetting ( 'count' , Iii1ii1II11i )
 i1iII1IiiIiI1 . setSetting ( 'fav' , 'no' )
 for OoO000 in oOo0oooo00o :
  try :
   if '<sportsdevil>' in OoO000 : i11i1 ( OoO000 , url , iconimage )
   elif '<iptv>' in OoO000 : IIIii1II1II ( OoO000 )
   elif '<Image>' in OoO000 : i1I1iI ( OoO000 )
   elif '<text>' in OoO000 : oo0OooOOo0 ( OoO000 )
   elif '<scraper>' in OoO000 : o0O ( OoO000 )
   elif '<redirect>' in OoO000 : REDIRECT ( OoO000 )
   elif '<oktitle>' in OoO000 : O00oO ( OoO000 )
   elif '<dl>' in OoO000 : I11i1I1I ( OoO000 )
   elif '<scraper>' in OoO000 : o0O ( OoO000 )
   else : oO0Oo ( OoO000 , url , iconimage )
  except : pass
  if 54 - 54: iii1I1 - II1iI + OoooooooOO
def Oo0OO ( ) :
 oo0o0O00 = 'http://www.hergundizi.net'
 i1iiIIiiI111 ( 'Yerli Yeni Eklenenler Diziler' , oo0o0O00 , 21 , oO , O0O , description = '' )
 if 70 - 70: ii1I11II1ii1i / o0O0 . I1i1iii % i1iIii1Ii1II
def OOoOO00OOO0OO ( url ) :
 iI1I111Ii111i = hergundizi . TVShows ( url )
 oOo0oooo00o = re . compile ( '<start>(.+?)<sep>(.+?)<sep>(.+?)<end>' ) . findall ( str ( iI1I111Ii111i ) )
 for oO0o0o0ooO0oO , url , oO in oOo0oooo00o :
  if not 'dızlar' in oO0o0o0ooO0oO :
   iiIiIIi ( oO0o0o0ooO0oO , url , 22 , oO , O0O , description = '' )
 try :
  I11IiI1I11i1i = re . compile ( '<np>(.+?)<np>' ) . findall ( str ( iI1I111Ii111i ) ) [ 0 ]
  i1iiIIiiI111 ( 'Next Page>>' , I11IiI1I11i1i , 21 , I1IiI , O0O , description = '' )
 except : pass
 xbmc . executebuiltin ( 'Container.SetViewMode(50)' )
 if 38 - 38: iii1I1
def Oo0O ( name , url , iconimage ) :
 IIi = hergundizi . Parts ( url )
 i11iIIIIIi1 = len ( IIi )
 if i11iIIIIIi1 > 1 :
  Iii1ii1II11i = [ ]
  iiII1i1 = 1
  for o00oOO0o in IIi :
   Iii1ii1II11i . append ( 'Part ' + str ( iiII1i1 ) )
   iiII1i1 = iiII1i1 + 1
   oooOOOOO = xbmcgui . Dialog ( )
  OOO00O = oooOOOOO . select ( 'Choose a Part..' , Iii1ii1II11i )
  if OOO00O < 0 : quit ( )
  url = IIi [ OOO00O ]
 OOoOO0oo0ooO = hergundizi . Stream ( url )
 O0o0O00Oo0o0 ( name , OOoOO0oo0ooO , iconimage )
 if 87 - 87: iii11I111 * i1iIii1Ii1II % i11iIiiIii % OooO0OO - IIII
def o0O ( item ) :
 oO0o0o0ooO0oO = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 oO = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 oo0o0O00 = re . compile ( '<scraper>(.+?)</scraper>' ) . findall ( item ) [ 0 ]
 i1iiIIiiI111 ( oO0o0o0ooO0oO , oo0o0O00 , 20 , oO , O0O )
 if 68 - 68: ii1I1i1I % i1IIi . IiiI11Iiiii . o0o00ooo0
def o0 ( url , iconimage ) :
 ii1 = url + '.scrape()'
 i11 = eval ( ii1 )
 oOo0oooo00o = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( i11 )
 Iii1ii1II11i = str ( len ( oOo0oooo00o ) )
 i1iII1IiiIiI1 . setSetting ( 'count' , Iii1ii1II11i )
 i1iII1IiiIiI1 . setSetting ( 'fav' , 'no' )
 for OoO000 in oOo0oooo00o :
  try :
   if '<sportsdevil>' in OoO000 : i11i1 ( OoO000 , url , iconimage )
   elif '<iptv>' in OoO000 : IIIii1II1II ( OoO000 )
   elif '<Image>' in OoO000 : i1I1iI ( OoO000 )
   elif '<text>' in OoO000 : oo0OooOOo0 ( OoO000 )
   elif '<scraper>' in OoO000 : o0O ( OoO000 )
   elif '<redirect>' in OoO000 : REDIRECT ( OoO000 )
   elif '<oktitle>' in OoO000 : O00oO ( OoO000 )
   elif '<dl>' in OoO000 : I11i1I1I ( OoO000 )
   elif '<scraper>' in OoO000 : o0O ( OoO000 , iconimage )
   else : oO0Oo ( OoO000 , url , iconimage )
  except : pass
  if 91 - 91: iIii1I11I1II1 + ii1I1i1I
def I11i1I1I ( item ) :
 oO0o0o0ooO0oO = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 oo0o0O00 = re . compile ( '<dl>(.+?)</dl>' ) . findall ( item ) [ 0 ]
 oO = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 i1i ( oO0o0o0ooO0oO , oo0o0O00 , 19 , oO , O0O )
 if 46 - 46: ii1I1i1I % o0O0 + I1I11I1I1I . OooO0OO . I1I11I1I1I
def oO00o0 ( name , url ) :
 OOoo0O = url . split ( '/' ) [ - 1 ]
 if OOoo0O == 'latest' : OOoo0O = 'AceStreamEngine.apk'
 import downloader
 oooOOOOO = xbmcgui . Dialog ( )
 Oo0ooOo0o = xbmcgui . DialogProgress ( )
 Ii1i1 = oooOOOOO . browse ( 0 , 'Select folder to download to' , 'myprograms' )
 iiIii = os . path . join ( Ii1i1 , OOoo0O )
 Oo0ooOo0o . create ( 'Downloading' , '' , '' , 'Please Wait' )
 downloader . download ( url , iiIii , Oo0ooOo0o )
 Oo0ooOo0o . close ( )
 oooOOOOO = xbmcgui . Dialog ( )
 oooOOOOO . ok ( 'Download complete' , 'Please install from..' , Ii1i1 )
 if 79 - 79: OoooooooOO / O0
def O00oO ( item ) :
 oO0o0o0ooO0oO = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 OO0OoO0o00 = re . compile ( '<oktitle>(.+?)</oktitle>' ) . findall ( item ) [ 0 ]
 ooOO0O0ooOooO = re . compile ( '<line1>(.+?)</line1>' ) . findall ( item ) [ 0 ]
 oOOOo00O00oOo = re . compile ( '<line2>(.+?)</line2>' ) . findall ( item ) [ 0 ]
 iiIIIi = re . compile ( '<line3>(.+?)</line3>' ) . findall ( item ) [ 0 ]
 ooo00OOOooO = '##' + OO0OoO0o00 + '#' + ooOO0O0ooOooO + '#' + oOOOo00O00oOo + '#' + iiIIIi + '##'
 oO = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 i1i ( oO0o0o0ooO0oO , ooo00OOOooO , 17 , oO , O0O )
 if 67 - 67: o0O0 * oo0Oo00Oo0 * o0o00ooo0 + IIII / i1IIi
def I1I111 ( name , url ) :
 Oo00oo0oO = re . compile ( '##(.+?)##' ) . findall ( url ) [ 0 ] . split ( '#' )
 oooOOOOO = xbmcgui . Dialog ( )
 oooOOOOO . ok ( Oo00oo0oO [ 0 ] , Oo00oo0oO [ 1 ] , Oo00oo0oO [ 2 ] , Oo00oo0oO [ 3 ] )
 if 1 - 1: I1I11I1I1I - oo0Oo00Oo0 . o0O0 . I1I11I1I1I / i1iIii1Ii1II + o0O0
def oo0OooOOo0 ( item ) :
 oO0o0o0ooO0oO = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 ooo00OOOooO = re . compile ( '<text>(.+?)</text>' ) . findall ( item ) [ 0 ]
 oO = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 i1i ( oO0o0o0ooO0oO , ooo00OOOooO , 9 , oO , O0O )
 if 78 - 78: O0 . oo0Oo00Oo0 . O0Oo0oO0o % IIII
def i1iIi ( name , url ) :
 ooOOoooooo = I11 ( url )
 II1I ( name , ooOOoooooo )
 if 84 - 84: IiiI11Iiiii . i11iIiiIii . IiiI11Iiiii * o0o00ooo0 - o0O0
def i1I1iI ( item ) :
 ii = re . compile ( '<Image>(.+?)</Image>' ) . findall ( item )
 if len ( ii ) == 1 :
  oO0o0o0ooO0oO = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  oO = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  O0o0oOOOoOo = re . compile ( '<Image>(.+?)</Image>' ) . findall ( item ) [ 0 ]
  oO = O0o0oOOOoOo . replace ( 'http://imgur.com/' , 'http://i.imgur.com/' ) + '.jpg'
  O0o0oOOOoOo = O0o0oOOOoOo . replace ( 'http://imgur.com/' , 'http://i.imgur.com/' ) + '.jpg'
  i1i ( oO0o0o0ooO0oO , O0o0oOOOoOo , 7 , oO , O0O )
 elif len ( ii ) > 1 :
  oO0o0o0ooO0oO = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  oO = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  II1 = ''
  for O0o0oOOOoOo in ii :
   oO = O0o0oOOOoOo . replace ( 'http://imgur.com/' , 'http://i.imgur.com/' ) + '.jpg'
   O0o0oOOOoOo = O0o0oOOOoOo . replace ( 'http://imgur.com/' , 'http://i.imgur.com/' ) + '.jpg'
   II1 = II1 + '<Image>' + O0o0oOOOoOo + '</Image>'
  I1iiiI1Ii1I = IiII
  oO0o0o0ooO0oO = oOO00oOO ( oO0o0o0ooO0oO )
  O0OOO0O = os . path . join ( os . path . join ( I1iiiI1Ii1I , '' ) , oO0o0o0ooO0oO + '.txt' )
  if not os . path . exists ( O0OOO0O ) : file ( O0OOO0O , 'w' ) . close ( )
  iiiiIiI = open ( O0OOO0O , "w" )
  iiiiIiI . write ( II1 )
  iiiiIiI . close ( )
  i1i ( oO0o0o0ooO0oO , 'image' , 8 , oO , O0O )
  if 6 - 6: IiiI11Iiiii . oo0Oo00Oo0 * OooO0OO - ii1I11II1ii1i - IiiI11Iiiii
def IIIii1II1II ( item ) :
 oO0o0o0ooO0oO = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 oO = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 oo0o0O00 = re . compile ( '<iptv>(.+?)</iptv>' ) . findall ( item ) [ 0 ]
 i1iiIIiiI111 ( oO0o0o0ooO0oO , oo0o0O00 , 6 , oO , O0O )
 if 45 - 45: II1iI - OoooooooOO + iIii1I11I1II1 . II1iI * o0O0
def oOOO ( url , iconimage ) :
 i11 = I11 ( url )
 iIII1 = re . compile ( '^#.+?:-?[0-9]*(.*?),(.*?)\n(.*?)$' , re . I + re . M + re . U + re . S ) . findall ( i11 )
 o0o = [ ]
 for O0OOoO00OO0o , oO0o0o0ooO0oO , url in iIII1 :
  I1111IIIIIi = { "params" : O0OOoO00OO0o , "name" : oO0o0o0ooO0oO , "url" : url }
  o0o . append ( I1111IIIIIi )
 list = [ ]
 for Iiii1i1 in o0o :
  I1111IIIIIi = { "name" : Iiii1i1 [ "name" ] , "url" : Iiii1i1 [ "url" ] }
  iIII1 = re . compile ( ' (.+?)="(.+?)"' , re . I + re . M + re . U + re . S ) . findall ( Iiii1i1 [ "params" ] )
  for OO , oo000o in iIII1 :
   I1111IIIIIi [ OO . strip ( ) . lower ( ) . replace ( '-' , '_' ) ] = oo000o . strip ( )
  list . append ( I1111IIIIIi )
 for Iiii1i1 in list :
  if '.ts' in Iiii1i1 [ "url" ] : i1i ( Iiii1i1 [ "name" ] , Iiii1i1 [ "url" ] , 2 , iconimage , O0O )
  else : iiIiIIi ( Iiii1i1 [ "name" ] , Iiii1i1 [ "url" ] , 2 , iconimage , O0O )
  if 44 - 44: i1IIi % O0Oo0oO0o + o0O0
def oO0Oo ( item , url , iconimage ) :
 I1I1I = iconimage
 OoOO000 = url
 i1Ii11i1i = re . compile ( '<link>(.+?)</link>' ) . findall ( item )
 IIiiIiI1 = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>' , re . DOTALL ) . findall ( item )
 for oO0o0o0ooO0oO , o0oOOoo , iconimage in IIiiIiI1 :
  if 'youtube.com/playlist?' in o0oOOoo :
   oOo00O0oo00o0 = o0oOOoo . split ( 'list=' ) [ 1 ]
   i1iiIIiiI111 ( oO0o0o0ooO0oO , o0oOOoo , iiOOooooO0Oo , iconimage , O0O , description = oOo00O0oo00o0 )
 if len ( i1Ii11i1i ) == 1 :
  oO0o0o0ooO0oO = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  url = re . compile ( '<link>(.+?)</link>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  if iconimage == 'ImageHere' : iconimage = I1I1I
  if '.ts' in url : i1i ( oO0o0o0ooO0oO , url , 16 , iconimage , O0O , description = '' )
  elif 'movies' in OoOO000 :
   OOiIiIIi1 ( oO0o0o0ooO0oO , url , 2 , iconimage , int ( Iii1ii1II11i ) , isFolder = False )
  else : iiIiIIi ( oO0o0o0ooO0oO , url , 2 , iconimage , O0O )
 elif len ( i1Ii11i1i ) > 1 :
  oO0o0o0ooO0oO = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  if iconimage == 'ImageHere' : iconimage = I1I1I
  if '.ts' in url : i1i ( oO0o0o0ooO0oO , url , 16 , iconimage , O0O , description = '' )
  elif 'movies' in OoOO000 :
   OOiIiIIi1 ( oO0o0o0ooO0oO , url , 3 , iconimage , int ( Iii1ii1II11i ) , isFolder = False )
  else : iiIiIIi ( oO0o0o0ooO0oO , url , 3 , iconimage , O0O )
  if 7 - 7: iii11I111 - i1iIii1Ii1II - oo0Oo00Oo0 + iii11I111
def OOOO00ooo0Ooo ( url ) :
 i11 = I11 ( url )
 oOo0oooo00o = re . compile ( 'name="(.+?)".+?rl="(.+?)".+?mg="(.+?)"' , re . DOTALL ) . findall ( i11 )
 for oO0o0o0ooO0oO , url , I1ii11iIi11i in oOo0oooo00o :
  if 'youtube.com/playlist?list=' in url :
   i1iiIIiiI111 ( oO0o0o0ooO0oO , url , 18 , I1ii11iIi11i , O0O )
  elif 'youtube.com/results?search_query=' in url :
   i1iiIIiiI111 ( oO0o0o0ooO0oO , url , 18 , I1ii11iIi11i , O0O )
  else :
   i1iiIIiiI111 ( oO0o0o0ooO0oO , url , 1 , I1ii11iIi11i , O0O )
   if 26 - 26: ii1I11II1ii1i
def I11iiI1i1 ( name , url , iconimage ) :
 if 'youtube.com/results?search_query=' in url :
  oOo00O0oo00o0 = url . split ( 'search_query=' ) [ 1 ]
  I1i1Iiiii = O0oo0OO0 + oOo00O0oo00o0 + I1i1iiI1
  OOo0oO00ooO00 = urllib2 . Request ( I1i1Iiiii )
  OOo0oO00ooO00 . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' )
  oOO0O00oO0Ooo = urllib2 . urlopen ( OOo0oO00ooO00 )
  i11 = oOO0O00oO0Ooo . read ( )
  oOO0O00oO0Ooo . close ( )
  i11 = i11 . replace ( '\r' , '' ) . replace ( '\n' , '' ) . replace ( '  ' , '' )
  oOo0oooo00o = re . compile ( '"videoId": "(.+?)".+?"title": "(.+?)"' , re . DOTALL ) . findall ( i11 )
  for oO0Oo0O0o , name in oOo0oooo00o :
   url = 'https://www.youtube.com/watch?v=' + oO0Oo0O0o
   iconimage = 'https://i.ytimg.com/vi/%s/hqdefault.jpg' % oO0Oo0O0o
   iiIiIIi ( name , url , 2 , iconimage , O0O )
 elif 'youtube.com/playlist?list=' in url :
  oOo00O0oo00o0 = url . split ( 'playlist?list=' ) [ 1 ]
  I1i1Iiiii = iiIIIII1i1iI + oOo00O0oo00o0 + o0oO0
  OOo0oO00ooO00 = urllib2 . Request ( I1i1Iiiii )
  OOo0oO00ooO00 . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' )
  oOO0O00oO0Ooo = urllib2 . urlopen ( OOo0oO00ooO00 )
  i11 = oOO0O00oO0Ooo . read ( )
  oOO0O00oO0Ooo . close ( )
  i11 = i11 . replace ( '\r' , '' ) . replace ( '\n' , '' ) . replace ( '  ' , '' )
  oOo0oooo00o = re . compile ( '"title": "(.+?)".+?"videoId": "(.+?)"' , re . DOTALL ) . findall ( i11 )
  for name , oO0Oo0O0o in oOo0oooo00o :
   url = 'https://www.youtube.com/watch?v=' + oO0Oo0O0o
   iconimage = 'https://i.ytimg.com/vi/%s/hqdefault.jpg' % oO0Oo0O0o
   iiIiIIi ( name , url , 2 , iconimage , O0O )
   if 99 - 99: oo0Oo00Oo0 . I1i1iii + iii11I111 % oo0Oo00Oo0 . i11iIiiIii % O0
def oOO00O ( item ) :
 item = item . replace ( '\r' , '' ) . replace ( '\t' , '' ) . replace ( '&nbsp;' , '' ) . replace ( '\'' , '' ) . replace ( '\n' , '' )
 IIiiIiI1 = re . compile ( 'name="(.+?)".+?rl="(.+?)".+?mg="(.+?)"' , re . DOTALL ) . findall ( item )
 for oO0o0o0ooO0oO , oo0o0O00 , oO in IIiiIiI1 :
  if 'youtube.com/channel/' in oo0o0O00 :
   oOo00O0oo00o0 = oo0o0O00 . split ( 'channel/' ) [ 1 ]
   i1iiIIiiI111 ( oO0o0o0ooO0oO , oo0o0O00 , iiOOooooO0Oo , oO , O0O , description = oOo00O0oo00o0 )
  elif 'youtube.com/user/' in oo0o0O00 :
   oOo00O0oo00o0 = oo0o0O00 . split ( 'user/' ) [ 1 ]
   i1iiIIiiI111 ( oO0o0o0ooO0oO , oo0o0O00 , iiOOooooO0Oo , oO , O0O , description = oOo00O0oo00o0 )
  elif 'youtube.com/playlist?' in oo0o0O00 :
   oOo00O0oo00o0 = oo0o0O00 . split ( 'list=' ) [ 1 ]
   i1iiIIiiI111 ( oO0o0o0ooO0oO , oo0o0O00 , iiOOooooO0Oo , oO , O0O , description = oOo00O0oo00o0 )
  elif 'plugin://' in oo0o0O00 :
   OOOoo0OO = HTMLParser ( )
   oo0o0O00 = OOOoo0OO . unescape ( oo0o0O00 )
   i1iiIIiiI111 ( oO0o0o0ooO0oO , oo0o0O00 , iiOOooooO0Oo , oO , O0O )
  else :
   i1iiIIiiI111 ( oO0o0o0ooO0oO , oo0o0O00 , 1 , oO , O0O )
   if 57 - 57: I1I11I1I1I / iii11I111
def i11i1 ( item , url , iconimage ) :
 I1I1I = iconimage
 i1Ii11i1i = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( item )
 Ii1I1Ii = re . compile ( '<link>(.+?)</link>' ) . findall ( item )
 if len ( i1Ii11i1i ) + len ( Ii1I1Ii ) == 1 :
  oO0o0o0ooO0oO = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  url = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( item ) [ 0 ]
  url = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' + url
  if iconimage == 'ImageHere' : iconimage = I1I1I
  i1i ( oO0o0o0ooO0oO , url , 16 , iconimage , O0O )
 elif len ( i1Ii11i1i ) + len ( Ii1I1Ii ) > 1 :
  oO0o0o0ooO0oO = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  if iconimage == 'ImageHere' : iconimage = I1I1I
  i1i ( oO0o0o0ooO0oO , url , 3 , iconimage , O0O )
  if 69 - 69: II1iI / iii1I1 . IiiI11Iiiii * ii1I1i1I % ii1I11II1ii1i - iii1I1
def OOOooOooo00O0 ( link ) :
 if iIiiiI == '' :
  oooOOOOO = xbmcgui . Dialog ( )
  i1iiIII111ii = oooOOOOO . yesno ( 'Adult Content' , 'You have opted to show adult content' , '' , 'Please set a password to prevent accidental access' , 'Cancel' , 'OK' )
  if i1iiIII111ii == 1 :
   i1iIIi1 = xbmc . Keyboard ( '' , 'Set Password' )
   i1iIIi1 . doModal ( )
   if ( i1iIIi1 . isConfirmed ( ) ) :
    ii11iIi1I = i1iIIi1 . getText ( )
    i1iII1IiiIiI1 . setSetting ( 'password' , ii11iIi1I )
  else : quit ( )
 elif iIiiiI <> '' :
  oooOOOOO = xbmcgui . Dialog ( )
  i1iiIII111ii = oooOOOOO . yesno ( 'Adult Content' , 'Please enter the password you set' , 'to continue' , '' , 'Cancel' , 'OK' )
  if i1iiIII111ii == 1 :
   i1iIIi1 = xbmc . Keyboard ( '' , 'Enter Password' )
   i1iIIi1 . doModal ( )
   if ( i1iIIi1 . isConfirmed ( ) ) :
    ii11iIi1I = i1iIIi1 . getText ( )
   if ii11iIi1I <> iIiiiI :
    quit ( )
  else : quit ( )
  if 13 - 13: ii1I11II1ii1i . i11iIiiIii
def oOOoo00O00o ( ) :
 i1iIIi1 = xbmc . Keyboard ( '' , 'Search' )
 i1iIIi1 . doModal ( )
 if ( i1iIIi1 . isConfirmed ( ) ) :
  oOo00O0oo00o0 = i1iIIi1 . getText ( )
  oOo00O0oo00o0 = oOo00O0oo00o0 . upper ( )
 else : quit ( )
 i11 = I11 ( i1i1II )
 O0O00Oo = re . compile ( '<link>(.+?)</link>' ) . findall ( i11 )
 for oo0o0O00 in O0O00Oo :
  try :
   i11 = I11 ( oo0o0O00 )
   oooooo0O000o = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( i11 )
   for OoO000 in oooooo0O000o :
    oOo0oooo00o = re . compile ( '<title>(.+?)</title>' ) . findall ( OoO000 )
    for OoO in oOo0oooo00o :
     OoO = OoO . upper ( )
     if oOo00O0oo00o0 in OoO :
      try :
       if '<sportsdevil>' in OoO000 : i11i1 ( OoO000 , oo0o0O00 , oO )
       elif '<iptv>' in OoO000 : IIIii1II1II ( OoO000 )
       elif '<Image>' in OoO000 : i1I1iI ( OoO000 )
       elif '<text>' in OoO000 : oo0OooOOo0 ( OoO000 )
       elif '<scraper>' in OoO000 : o0O ( OoO000 )
       elif '<redirect>' in OoO000 : REDIRECT ( OoO000 )
       elif '<oktitle>' in OoO000 : O00oO ( OoO000 )
       elif '<dl>' in OoO000 : I11i1I1I ( OoO000 )
       elif '<scraper>' in OoO000 : o0O ( OoO000 , oO )
       else : oO0Oo ( OoO000 , oo0o0O00 , oO )
      except : pass
  except : pass
  if 51 - 51: OoooooooOO * IIII
def OO0ooOOO0OOO ( name , url , iconimage ) :
 I1I1I = iconimage
 oO00oooOOoOo0 = [ ]
 OoOOoOooooOOo = [ ]
 oOo0O = [ ]
 i11 = I11 ( url )
 oo0O0 = re . compile ( '<title>' + re . escape ( name ) + '</title>(.+?)</item>' , re . DOTALL ) . findall ( i11 ) [ 0 ]
 i1Ii11i1i = [ ]
 if '<link>' in oo0O0 :
  iI = re . compile ( '<link>(.+?)</link>' ) . findall ( oo0O0 )
  for OO0O000 in iI :
   i1Ii11i1i . append ( OO0O000 )
 if '<sportsdevil>' in oo0O0 :
  iiIiI1i1 = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( oo0O0 )
  for oO0O00oOOoooO in iiIiI1i1 :
   oO0O00oOOoooO = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' + oO0O00oOOoooO
   i1Ii11i1i . append ( oO0O00oOOoooO )
 iiII1i1 = 1
 for IiIi11iI in i1Ii11i1i :
  Oo0O00O000 = IiIi11iI
  if 'acestream://' in IiIi11iI or '.acelive' in IiIi11iI or 'sop://' in IiIi11iI : i11I1IiII1i1i = ' (Acestreams)'
  else : i11I1IiII1i1i = ''
  if '(' in IiIi11iI :
   IiIi11iI = IiIi11iI . split ( '(' ) [ 0 ]
   ooI1111i = str ( Oo0O00O000 . split ( '(' ) [ 1 ] . replace ( ')' , '' ) + i11I1IiII1i1i )
   oO00oooOOoOo0 . append ( IiIi11iI )
   OoOOoOooooOOo . append ( ooI1111i )
  else :
   iIIii = IiIi11iI . split ( '/' ) [ 2 ] . replace ( 'www.' , '' )
   oO00oooOOoOo0 . append ( IiIi11iI )
   OoOOoOooooOOo . append ( 'Link ' + str ( iiII1i1 ) + i11I1IiII1i1i )
  iiII1i1 = iiII1i1 + 1
 oooOOOOO = xbmcgui . Dialog ( )
 OOO00O = oooOOOOO . select ( 'Choose a link..' , OoOOoOooooOOo )
 if OOO00O < 0 : quit ( )
 else :
  url = oO00oooOOoOo0 [ OOO00O ]
  O0o0O00Oo0o0 ( name , url , iconimage )
  if 92 - 92: ii1I11II1ii1i + oo0Oo00Oo0 % IIII
def oOo0 ( url ) :
 ii1 = "ShowPicture(%s)" % url
 xbmc . executebuiltin ( ii1 )
 if 30 - 30: o0O0 / II1iI
def O0o0O00Oo0o0 ( name , url , iconimage ) :
 try :
  if 'sop://' in url :
   url = urllib . quote ( url )
   url = 'plugin://program.plexus/?mode=2&url=%s&name=%s' % ( url , name . replace ( ' ' , '+' ) )
   Iii1I1111ii ( name , url , iconimage )
  elif 'acestream://' in url or '.acelive' in url :
   url = urllib . quote ( url )
   url = 'plugin://program.plexus/?mode=1&url=%s&name=%s' % ( url , name . replace ( ' ' , '+' ) )
   Iii1I1111ii ( name , url , iconimage )
  elif 'plugin://plugin.video.SportsDevil/' in url :
   Iii1I1111ii ( name , url , iconimage )
  elif '.ts' in url :
   url = 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;name=' + name + '&amp;url=' + url
   Iii1I1111ii ( name , url , iconimage )
  elif urlresolver . HostedMediaFile ( url ) . valid_url ( ) :
   url = urlresolver . HostedMediaFile ( url ) . resolve ( )
   ooOoO00 ( name , url , iconimage )
  elif liveresolver . isValid ( url ) == True :
   url = liveresolver . resolve ( url )
   ooOoO00 ( name , url , iconimage )
  else : ooOoO00 ( name , url , iconimage )
 except :
  Ii1IIiI1i ( 'UKTurk' , 'Stream Unavailable' , '3000' , I1ii11iIi11i )
  if 78 - 78: o0o00ooo0
def o0Oo0oO0oOO00 ( url ) :
 if urlresolver . HostedMediaFile ( url ) . valid_url ( ) :
  url = urlresolver . HostedMediaFile ( url ) . resolve ( )
 xbmc . Player ( ) . play ( url )
 if 92 - 92: OoooooooOO * ii1I1i1I
def ooOoO00 ( name , url , iconimage ) :
 o0000oO = True
 I1II1 = xbmcgui . ListItem ( name , iconImage = iconimage , thumbnailImage = iconimage ) ; I1II1 . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
 o0000oO = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = url , listitem = I1II1 )
 I1II1 . setPath ( url )
 xbmcplugin . setResolvedUrl ( int ( sys . argv [ 1 ] ) , True , I1II1 )
 if 86 - 86: iIii1I11I1II1 / OooO0OO . O0Oo0oO0o
def Iii1I1111ii ( name , url , iconimage ) :
 o0000oO = True
 I1II1 = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage ) ; I1II1 . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
 o0000oO = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = url , listitem = I1II1 )
 oooOOOOO = xbmcgui . Dialog ( )
 xbmc . Player ( ) . play ( url , I1II1 , False )
 if 19 - 19: o0o00ooo0 % OoooooooOO % IiiI11Iiiii * iii1I1 % O0
def ooo ( url ) :
 xbmc . executebuiltin ( "PlayMedia(%s)" % url )
 if 27 - 27: iii11I111 % II1iI
def o0oooOO00 ( url ) :
 iiIiii1IIIII = i1iII1IiiIiI1 . getSetting ( 'layout' )
 if iiIiii1IIIII == 'Listers' : i1iII1IiiIiI1 . setSetting ( 'layout' , 'Category' )
 else : i1iII1IiiIiI1 . setSetting ( 'layout' , 'Listers' )
 xbmc . executebuiltin ( 'Container.Refresh' )
 if 67 - 67: ii1I11II1ii1i / IiiI11Iiiii
def I11 ( url ) :
 OOo0oO00ooO00 = urllib2 . Request ( url )
 OOo0oO00ooO00 . add_header ( 'User-Agent' , 'mat' )
 oOO0O00oO0Ooo = urllib2 . urlopen ( OOo0oO00ooO00 )
 i11 = oOO0O00oO0Ooo . read ( )
 oOO0O00oO0Ooo . close ( )
 i11 = i11 . replace ( '</fanart>' , '<fanart>x</fanart>' ) . replace ( '<thumbnail></thumbnail>' , '<thumbnail>x</thumbnail>' ) . replace ( '<utube>' , '<link>https://www.youtube.com/watch?v=' ) . replace ( '</utube>' , '</link>' )
 if '{' in i11 : i11 = iiIiIIIiiI ( i11 )
 return i11
 if 12 - 12: O0 - iii1I1
def oOoO00O0 ( ) :
 OOIi1iI111II1I1 = [ ]
 oOOOOoOO0o = sys . argv [ 2 ]
 if len ( oOOOOoOO0o ) >= 2 :
  O0OOoO00OO0o = sys . argv [ 2 ]
  i1II1 = O0OOoO00OO0o . replace ( '?' , '' )
  if ( O0OOoO00OO0o [ len ( O0OOoO00OO0o ) - 1 ] == '/' ) :
   O0OOoO00OO0o = O0OOoO00OO0o [ 0 : len ( O0OOoO00OO0o ) - 2 ]
  i11i1IiiiiI1i1Iii = i1II1 . split ( '&' )
  OOIi1iI111II1I1 = { }
  for iiII1i1 in range ( len ( i11i1IiiiiI1i1Iii ) ) :
   oo00oO0o = { }
   oo00oO0o = i11i1IiiiiI1i1Iii [ iiII1i1 ] . split ( '=' )
   if ( len ( oo00oO0o ) ) == 2 :
    OOIi1iI111II1I1 [ oo00oO0o [ 0 ] ] = oo00oO0o [ 1 ]
 return OOIi1iI111II1I1
 if 31 - 31: IIII
def Ii1IIiI1i ( title , message , ms , nart ) :
 xbmc . executebuiltin ( "XBMC.notification(" + title + "," + message + "," + ms + "," + nart + ")" )
 if 23 - 23: ii1I1i1I . IiiI11Iiiii
def oOO00oOO ( string ) :
 OO0000o = re . compile ( '\[(.+?)\]' ) . findall ( string )
 for i1I1i1 in OO0000o : string = string . replace ( i1I1i1 , '' ) . replace ( '[/]' , '' ) . replace ( '[]' , '' )
 return string
 if 81 - 81: iii11I111 - iIii1I11I1II1 - i1IIi / ii1I1i1I - O0 * o0O0
def iI1i11II1i ( string ) :
 string = string . split ( ' ' )
 o0o0OoOo0O0OO = ''
 for iIi1I11I in string :
  Iii1 = '[B][COLOR red]' + iIi1I11I [ 0 ] . upper ( ) + '[/COLOR][COLOR white]' + iIi1I11I [ 1 : ] + '[/COLOR][/B] '
  o0o0OoOo0O0OO = o0o0OoOo0O0OO + Iii1
 return o0o0OoOo0O0OO
 if 58 - 58: II1iI . I1i1iii + OooO0OO
def OOiIiIIi1 ( name , url , mode , iconimage , itemcount , isFolder = False ) :
 if iI111iI == 'true' :
  if not 'COLOR' in name :
   O00OO = name . partition ( '(' )
   I1I1 = ""
   OoO0O0o0oOOO = ""
   if len ( O00OO ) > 0 :
    I1I1 = O00OO [ 0 ]
    OoO0O0o0oOOO = O00OO [ 2 ] . partition ( ')' )
   if len ( OoO0O0o0oOOO ) > 0 :
    OoO0O0o0oOOO = OoO0O0o0oOOO [ 0 ]
   OOoOoOo = eval ( base64 . b64decode ( 'bWV0YWhhbmRsZXJzLk1ldGFEYXRhKHRtZGJfYXBpX2tleT0iZDk1NWQ4ZjAyYTNmMjQ4MGE1MTg4MWZlNGM5NmYxMGUiKQ==' ) )
   o000ooooO0o = OOoOoOo . get_meta ( 'movie' , name = I1I1 , year = OoO0O0o0oOOO )
   iI1i11 = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&site=" + str ( OoOOoooOO0O ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name )
   o0000oO = True
   I1II1 = xbmcgui . ListItem ( name , iconImage = o000ooooO0o [ 'cover_url' ] , thumbnailImage = o000ooooO0o [ 'cover_url' ] )
   I1II1 . setInfo ( type = "Video" , infoLabels = o000ooooO0o )
   I1II1 . setProperty ( "IsPlayable" , "true" )
   ooo00Ooo = [ ]
   if i1iII1IiiIiI1 . getSetting ( 'fav' ) == 'yes' : ooo00Ooo . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
   if i1iII1IiiIiI1 . getSetting ( 'fav' ) == 'no' : ooo00Ooo . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
   I1II1 . addContextMenuItems ( ooo00Ooo , replaceItems = False )
   if not o000ooooO0o [ 'backdrop_url' ] == '' : I1II1 . setProperty ( 'fanart_image' , o000ooooO0o [ 'backdrop_url' ] )
   else : I1II1 . setProperty ( 'fanart_image' , O0O )
   o0000oO = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = iI1i11 , listitem = I1II1 , isFolder = isFolder , totalItems = itemcount )
   return o0000oO
 else :
  iI1i11 = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&site=" + str ( OoOOoooOO0O ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name )
  o0000oO = True
  I1II1 = xbmcgui . ListItem ( name , iconImage = iconimage , thumbnailImage = iconimage )
  I1II1 . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
  I1II1 . setProperty ( 'fanart_image' , O0O )
  I1II1 . setProperty ( "IsPlayable" , "true" )
  ooo00Ooo = [ ]
  if i1iII1IiiIiI1 . getSetting ( 'fav' ) == 'yes' : ooo00Ooo . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
  if i1iII1IiiIiI1 . getSetting ( 'fav' ) == 'no' : ooo00Ooo . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
  I1II1 . addContextMenuItems ( ooo00Ooo , replaceItems = False )
  o0000oO = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = iI1i11 , listitem = I1II1 , isFolder = isFolder )
  return o0000oO
  if 93 - 93: i11iIiiIii - II1iI * o0o00ooo0 * o0O0 % O0 + OoooooooOO
def i1iiIIiiI111 ( name , url , mode , iconimage , fanart , description = '' ) :
 iI1i11 = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&fanart=" + urllib . quote_plus ( fanart ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 o0000oO = True
 I1II1 = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 I1II1 . setInfo ( type = "Video" , infoLabels = { "Title" : name , 'plot' : description } )
 I1II1 . setProperty ( 'fanart_image' , fanart )
 ooo00Ooo = [ ]
 if i1iII1IiiIiI1 . getSetting ( 'fav' ) == 'yes' : ooo00Ooo . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 if i1iII1IiiIiI1 . getSetting ( 'fav' ) == 'no' : ooo00Ooo . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 I1II1 . addContextMenuItems ( ooo00Ooo , replaceItems = False )
 if 'plugin://' in url :
  iI1i11 = url
 o0000oO = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = iI1i11 , listitem = I1II1 , isFolder = True )
 return o0000oO
 if 25 - 25: IiiI11Iiiii + ii1I11II1ii1i / iii11I111 . iii1I1 % O0 * I1I11I1I1I
def i1i ( name , url , mode , iconimage , fanart , description = '' ) :
 iI1i11 = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 o0000oO = True
 I1II1 = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 I1II1 . setProperty ( 'fanart_image' , fanart )
 ooo00Ooo = [ ]
 if i1iII1IiiIiI1 . getSetting ( 'fav' ) == 'yes' : ooo00Ooo . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 if i1iII1IiiIiI1 . getSetting ( 'fav' ) == 'no' : ooo00Ooo . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 I1II1 . addContextMenuItems ( ooo00Ooo , replaceItems = False )
 o0000oO = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = iI1i11 , listitem = I1II1 , isFolder = False )
 return o0000oO
 if 84 - 84: iii11I111 % ii1I11II1ii1i + i11iIiiIii
def iiIiIIi ( name , url , mode , iconimage , fanart , description = '' ) :
 iI1i11 = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 o0000oO = True
 I1II1 = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 I1II1 . setProperty ( 'fanart_image' , fanart )
 I1II1 . setProperty ( "IsPlayable" , "true" )
 ooo00Ooo = [ ]
 if i1iII1IiiIiI1 . getSetting ( 'fav' ) == 'yes' : ooo00Ooo . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 if i1iII1IiiIiI1 . getSetting ( 'fav' ) == 'no' : ooo00Ooo . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 I1II1 . addContextMenuItems ( ooo00Ooo , replaceItems = False )
 o0000oO = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = iI1i11 , listitem = I1II1 , isFolder = False )
 return o0000oO
 if 28 - 28: i1iIii1Ii1II + I1I11I1I1I * IIII % oo0Oo00Oo0 . o0O0 % O0
def I1iiiiIii ( url , name ) :
 iIiIiIiI = I11 ( url )
 if len ( iIiIiIiI ) > 1 :
  I1iiiI1Ii1I = IiII
  O0OOO0O = os . path . join ( os . path . join ( I1iiiI1Ii1I , '' ) , name + '.txt' )
  if not os . path . exists ( O0OOO0O ) :
   file ( O0OOO0O , 'w' ) . close ( )
  i11OOoo = open ( O0OOO0O )
  iIIiiiI = i11OOoo . read ( )
  if iIIiiiI == iIiIiIiI : pass
  else :
   II1I ( 'UKTurk' , iIiIiIiI )
   iiiiIiI = open ( O0OOO0O , "w" )
   iiiiIiI . write ( iIiIiIiI )
   iiiiIiI . close ( )
   if 60 - 60: II1iI . ii1I1i1I
def II1I ( heading , text ) :
 id = 10147
 xbmc . executebuiltin ( 'ActivateWindow(%d)' % id )
 xbmc . sleep ( 500 )
 IiI111ii1ii = xbmcgui . Window ( id )
 O0OOo = 50
 while ( O0OOo > 0 ) :
  try :
   xbmc . sleep ( 10 )
   O0OOo -= 1
   IiI111ii1ii . getControl ( 1 ) . setLabel ( heading )
   IiI111ii1ii . getControl ( 5 ) . setText ( text )
   return
  except :
   pass
   if 38 - 38: iIii1I11I1II1 + o0o00ooo0 - IIII - iii11I111 - OooO0OO
def o000O ( name ) :
 global Icon
 global Next
 global Previous
 global window
 global Quit
 global images
 O0OOO0O = os . path . join ( os . path . join ( IiII , '' ) , name + '.txt' )
 i11OOoo = open ( O0OOO0O )
 iIIiiiI = i11OOoo . read ( )
 images = re . compile ( '<image>(.+?)</image>' ) . findall ( iIIiiiI )
 i1iII1IiiIiI1 . setSetting ( 'pos' , '0' )
 window = pyxbmct . AddonDialogWindow ( '' )
 II11 = '/resources/art'
 III11I1 = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + o0OO00 + II11 , 'next_focus.png' ) )
 IIi1IIIi = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + o0OO00 + II11 , 'next1.png' ) )
 O00Ooo = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + o0OO00 + II11 , 'previous_focus.png' ) )
 OOOO0OOO = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + o0OO00 + II11 , 'previous.png' ) )
 i1i1ii = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + o0OO00 + II11 , 'close_focus.png' ) )
 iII1ii1 = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + o0OO00 + II11 , 'close.png' ) )
 I1i1iiiI1 = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + o0OO00 + II11 , 'main-bg1.png' ) )
 window . setGeometry ( 1300 , 720 , 100 , 50 )
 iIIi = pyxbmct . Image ( I1i1iiiI1 )
 window . placeControl ( iIIi , - 10 , - 10 , 130 , 70 )
 ooo00OOOooO = '0xFF000000'
 Previous = pyxbmct . Button ( '' , focusTexture = O00Ooo , noFocusTexture = OOOO0OOO , textColor = ooo00OOOooO , focusedColor = ooo00OOOooO )
 Next = pyxbmct . Button ( '' , focusTexture = III11I1 , noFocusTexture = IIi1IIIi , textColor = ooo00OOOooO , focusedColor = ooo00OOOooO )
 Quit = pyxbmct . Button ( '' , focusTexture = i1i1ii , noFocusTexture = iII1ii1 , textColor = ooo00OOOooO , focusedColor = ooo00OOOooO )
 Icon = pyxbmct . Image ( images [ 0 ] , aspectRatio = 1 )
 window . placeControl ( Previous , 102 , 1 , 10 , 10 )
 window . placeControl ( Next , 102 , 40 , 10 , 10 )
 window . placeControl ( Quit , 102 , 21 , 10 , 10 )
 window . placeControl ( Icon , 0 , 0 , 100 , 50 )
 Previous . controlRight ( Next )
 Previous . controlUp ( Quit )
 window . connect ( Previous , oO0o00oo0 )
 window . connect ( Next , ii1IIII )
 Previous . setVisible ( False )
 window . setFocus ( Quit )
 Previous . controlRight ( Quit )
 Quit . controlLeft ( Previous )
 Quit . controlRight ( Next )
 Next . controlLeft ( Quit )
 window . connect ( Quit , window . close )
 window . doModal ( )
 del window
 if 59 - 59: oo0Oo00Oo0 * o0O0 % O0Oo0oO0o
def ii1IIII ( ) :
 oooIIiIiI1I = int ( i1iII1IiiIiI1 . getSetting ( 'pos' ) )
 OooOoOo = int ( oooIIiIiI1I ) + 1
 i1iII1IiiIiI1 . setSetting ( 'pos' , str ( OooOoOo ) )
 III1I1Iii1iiI = len ( images )
 Icon . setImage ( images [ int ( OooOoOo ) ] )
 Previous . setVisible ( True )
 if int ( OooOoOo ) == int ( III1I1Iii1iiI ) - 1 :
  Next . setVisible ( False )
  if 17 - 17: ii1I11II1ii1i % iIii1I11I1II1 - iIii1I11I1II1
def oO0o00oo0 ( ) :
 oooIIiIiI1I = int ( i1iII1IiiIiI1 . getSetting ( 'pos' ) )
 O0o0O0 = int ( oooIIiIiI1I ) - 1
 i1iII1IiiIiI1 . setSetting ( 'pos' , str ( O0o0O0 ) )
 Icon . setImage ( images [ int ( O0o0O0 ) ] )
 Next . setVisible ( True )
 if int ( O0o0O0 ) == 0 :
  Previous . setVisible ( False )
  if 11 - 11: O0Oo0oO0o % I1I11I1I1I * I1i1iii + iii11I111 + ii1I11II1ii1i
def iiIiIIIiiI ( gobble ) :
 gobble = gobble . replace ( '}' , '' ) . replace ( '{' , '' ) . replace ( ',' , '' ) . replace ( ']' , '' ) . replace ( '[' , '' )
 gobble = gobble + '=='
 gobble = gobble . decode ( 'base64' )
 return gobble
 if 24 - 24: i1iIii1Ii1II - oo0Oo00Oo0 % iIii1I11I1II1 . i1IIi / O0
def ii1ii111 ( text ) :
 def I111i1i1111 ( m ) :
  ooo00OOOooO = m . group ( 0 )
  if ooo00OOOooO [ : 3 ] == "&#x" : return unichr ( int ( ooo00OOOooO [ 3 : - 1 ] , 16 ) ) . encode ( 'utf-8' )
  else : return unichr ( int ( ooo00OOOooO [ 2 : - 1 ] ) ) . encode ( 'utf-8' )
 try : return re . sub ( "(?i)&#\w+;" , I111i1i1111 , text . decode ( 'ISO-8859-1' ) . encode ( 'utf-8' ) )
 except : return re . sub ( "(?i)&#\w+;" , I111i1i1111 , text . encode ( "ascii" , "ignore" ) . encode ( 'utf-8' ) )
 if 49 - 49: I1I11I1I1I / oo0Oo00Oo0 + O0 * iii1I1
def OoOo ( link ) :
 try :
  I1ii11 = re . compile ( '<layouttype>(.+?)</layouttype>' ) . findall ( link ) [ 0 ]
  if I1ii11 == 'thumbnail' : xbmc . executebuiltin ( 'Container.SetViewMode(500)' )
  else : xbmc . executebuiltin ( 'Container.SetViewMode(50)' )
 except : pass
 if 74 - 74: i1iIii1Ii1II - iii1I1 . i1IIi
O0OOoO00OO0o = oOoO00O0 ( ) ; oo0o0O00 = None ; oO0o0o0ooO0oO = None ; iiOOooooO0Oo = None ; OoOOoooOO0O = None ; oO = None
try : OoOOoooOO0O = urllib . unquote_plus ( O0OOoO00OO0o [ "site" ] )
except : pass
try : oo0o0O00 = urllib . unquote_plus ( O0OOoO00OO0o [ "url" ] )
except : pass
try : oO0o0o0ooO0oO = urllib . unquote_plus ( O0OOoO00OO0o [ "name" ] )
except : pass
try : iiOOooooO0Oo = int ( O0OOoO00OO0o [ "mode" ] )
except : pass
try : oO = urllib . unquote_plus ( O0OOoO00OO0o [ "iconimage" ] )
except : pass
try : O0O = urllib . unquote_plus ( O0OOoO00OO0o [ "fanart" ] )
except : pass
try : i1III = urllib . unquote_plus ( [ "description" ] )
except : pass
if 49 - 49: i11iIiiIii % ii1I11II1ii1i . OooO0OO
if iiOOooooO0Oo == None or oo0o0O00 == None or len ( oo0o0O00 ) < 1 : i1I1Iiii1111 ( )
elif iiOOooooO0Oo == 1 : OOoo0O0 ( oO0o0o0ooO0oO , oo0o0O00 , oO , O0O )
elif iiOOooooO0Oo == 2 : O0o0O00Oo0o0 ( oO0o0o0ooO0oO , oo0o0O00 , oO )
elif iiOOooooO0Oo == 3 : OO0ooOOO0OOO ( oO0o0o0ooO0oO , oo0o0O00 , oO )
elif iiOOooooO0Oo == 4 : ooOoO00 ( oO0o0o0ooO0oO , oo0o0O00 , oO )
elif iiOOooooO0Oo == 5 : oOOoo00O00o ( )
elif iiOOooooO0Oo == 6 : oOOO ( oo0o0O00 , oO )
elif iiOOooooO0Oo == 7 : oOo0 ( oo0o0O00 )
elif iiOOooooO0Oo == 8 : o000O ( oO0o0o0ooO0oO )
elif iiOOooooO0Oo == 9 : i1iIi ( oO0o0o0ooO0oO , oo0o0O00 )
elif iiOOooooO0Oo == 10 : DOSCRAPER ( oO0o0o0ooO0oO , oo0o0O00 )
elif iiOOooooO0Oo == 11 : ooo ( oo0o0O00 )
elif iiOOooooO0Oo == 12 : ooOO0O00 ( oO0o0o0ooO0oO , oo0o0O00 , oO )
elif iiOOooooO0Oo == 13 : o0oooOO00 ( oo0o0O00 )
elif iiOOooooO0Oo == 14 : oOOO00o ( oO0o0o0ooO0oO , oo0o0O00 , oO )
elif iiOOooooO0Oo == 15 : iiiIi ( oo0o0O00 )
elif iiOOooooO0Oo == 16 : Iii1I1111ii ( oO0o0o0ooO0oO , oo0o0O00 , oO )
elif iiOOooooO0Oo == 17 : I1I111 ( oO0o0o0ooO0oO , oo0o0O00 )
elif iiOOooooO0Oo == 18 : I11iiI1i1 ( oO0o0o0ooO0oO , oo0o0O00 , oO )
elif iiOOooooO0Oo == 19 : oO00o0 ( oO0o0o0ooO0oO , oo0o0O00 )
elif iiOOooooO0Oo == 20 : o0 ( oo0o0O00 , oO )
elif iiOOooooO0Oo == 21 : OOoOO00OOO0OO ( oo0o0O00 )
elif iiOOooooO0Oo == 22 : Oo0O ( oO0o0o0ooO0oO , oo0o0O00 , oO )
if 13 - 13: i11iIiiIii + i1IIi * iIii1I11I1II1 % OoooooooOO - O0Oo0oO0o * IIII
xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3
