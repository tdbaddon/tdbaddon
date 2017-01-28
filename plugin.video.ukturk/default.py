import xbmc , xbmcaddon , xbmcgui , xbmcplugin , urllib , urllib2 , os , re , sys , datetime , urlresolver , random , liveresolver , base64 , pyxbmct , glob
from resources . lib . common_addon import Addon
from HTMLParser import HTMLParser
from metahandler import metahandlers
from resources . lib import mamahd
from resources . lib import crickfree
from resources . lib import bigsports
if 64 - 64: i11iIiiIii
if 65 - 65: O0 / iIii1I11I1II1 % OoooooooOO - i1IIi
o0OO00 = 'plugin.video.ukturk'
oo = Addon ( o0OO00 , sys . argv )
i1iII1IiiIiI1 = xbmcaddon . Addon ( id = o0OO00 )
iIiiiI1IiI1I1 = xbmc . translatePath ( 'special://home/addons/' ) + '/*.*'
o0OoOoOO00 = xbmc . translatePath ( 'special://home/addons/' )
I11i = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + o0OO00 , 'fanart.jpg' ) )
O0O = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + o0OO00 , 'fanart.jpg' ) )
Oo = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + o0OO00 , 'icon.png' ) )
I1ii11iIi11i = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + o0OO00 + '/resources/art' , 'next.png' ) )
I1IiI = i1iII1IiiIiI1 . getSetting ( 'adult' )
o0OOO = i1iII1IiiIiI1 . getSetting ( 'password' )
iIiiiI = int ( i1iII1IiiIiI1 . getSetting ( 'count' ) )
Iii1ii1II11i = i1iII1IiiIiI1 . getSetting ( 'enable_meta' )
iI111iI = xbmc . translatePath ( 'special://home/userdata/addon_data/' + o0OO00 )
IiII = xbmc . translatePath ( os . path . join ( 'special://home/userdata/Database' , 'UKTurk.db' ) )
iI1Ii11111iIi = 'http://ukturk.offshorepastebin.com/ukturk2.jpg'
i1i1II = 'https://www.googleapis.com/youtube/v3/search?q='
O0oo0OO0 = '&regionCode=US&part=snippet&hl=en_US&key=AIzaSyAd-YEOqZz9nXVzGtn3KWzYLbLaajhqIDA&type=video&maxResults=50'
I1i1iiI1 = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId='
iiIIIII1i1iI = '&maxResults=50&key=AIzaSyAd-YEOqZz9nXVzGtn3KWzYLbLaajhqIDA'
o0oO0 = open ( IiII , 'a' )
o0oO0 . close ( )
if 100 - 100: i11Ii11I1Ii1i
def Ooo ( ) :
 i1iII1IiiIiI1 . setSetting ( 'fav' , 'no' )
 if not os . path . exists ( iI111iI ) :
  os . mkdir ( iI111iI )
 o0oOoO00o = i1 ( iI1Ii11111iIi )
 oOOoo00O0O = re . compile ( '<index>(.+?)</index>' ) . findall ( o0oOoO00o ) [ 0 ]
 o0oOoO00o = i1 ( oOOoo00O0O )
 i1111 = re . compile ( 'name="(.+?)".+?rl="(.+?)".+?mg="(.+?)"' , re . DOTALL ) . findall ( o0oOoO00o )
 for i11 , I11 , Oo0o0000o0o0 in i1111 :
  if not 'XXX' in i11 :
   oOo0oooo00o ( i11 , I11 , 1 , Oo0o0000o0o0 , I11i )
  if 'XXX' in i11 :
   if I1IiI == 'true' :
    if o0OOO == '' :
     oO0o0o0ooO0oO = xbmcgui . Dialog ( )
     oo0o0O00 = oO0o0o0ooO0oO . yesno ( 'Adult Content' , 'You have opted to show adult content' , '' , 'Please set a password to prevent accidental access' , 'Cancel' , 'Lets Go' )
     if oo0o0O00 == 1 :
      oO = xbmc . Keyboard ( '' , 'Set Password' )
      oO . doModal ( )
      if ( oO . isConfirmed ( ) ) :
       i1iiIIiiI111 = oO . getText ( )
       i1iII1IiiIiI1 . setSetting ( 'password' , i1iiIIiiI111 )
      oOo0oooo00o ( i11 , I11 , 1 , Oo0o0000o0o0 , I11i )
   if I1IiI == 'true' :
    if o0OOO <> '' :
     oOo0oooo00o ( i11 , I11 , 1 , Oo0o0000o0o0 , I11i )
 oOo0oooo00o ( 'Favourites' , IiII , 15 , 'http://ukturk.offshorepastebin.com/UKTurk/thumbs/new/Uk%20turk%20thumbnails%20favourites.jpg' , I11i )
 oOo0oooo00o ( 'Search' , 'url' , 5 , 'http://ukturk.offshorepastebin.com/UKTurk/thumbs/new/Uk%20turk%20thumbnails%20search.jpg' , I11i )
 xbmc . executebuiltin ( 'Container.SetViewMode(500)' )
 if 62 - 62: iIIIIiI - OoOO
def I1iiiiI1iII ( url ) :
 i1iII1IiiIiI1 . setSetting ( 'fav' , 'yes' )
 IiIi11i = None
 file = open ( IiII , 'r' )
 IiIi11i = file . read ( )
 i1111 = re . compile ( "<item>(.+?)</item>" , re . DOTALL ) . findall ( IiIi11i )
 for iIii1I111I11I in i1111 :
  OO00OooO0OO = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>' , re . DOTALL ) . findall ( iIii1I111I11I )
  for i11 , url , Oo0o0000o0o0 in OO00OooO0OO :
   if '.txt' in url :
    oOo0oooo00o ( i11 , url , 1 , Oo0o0000o0o0 , I11i )
   else :
    iiiIi ( i11 , url , 2 , Oo0o0000o0o0 , I11i )
    if 24 - 24: iIiI1I11 % i111I1 % oOoO - iiIiIIi % ooOoo0O
def OooO0 ( name , url , iconimage ) :
 url = url . replace ( ' ' , '%20' )
 iconimage = iconimage . replace ( ' ' , '%20' )
 II11iiii1Ii = '<FAV><item>\n<title>' + name + '</title>\n<link>' + url + '</link>\n' + '<thumbnail>' + iconimage + '</thumbnail>\n</item></FAV>\n'
 o0oO0 = open ( IiII , 'a' )
 o0oO0 . write ( II11iiii1Ii )
 o0oO0 . close ( )
 if 70 - 70: O00 / i1I1i1Ii11 . IIIIII11i1I - o0o0OOO0o0 % ooOOOo0oo0O0
def o0 ( name , url , iconimage ) :
 IiIi11i = None
 file = open ( IiII , 'r' )
 IiIi11i = file . read ( )
 I11II1i = ''
 i1111 = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( IiIi11i )
 for OO00OooO0OO in i1111 :
  II11iiii1Ii = '\n<FAV><item>\n' + OO00OooO0OO + '</item>\n'
  if name in OO00OooO0OO :
   II11iiii1Ii = II11iiii1Ii . replace ( 'item' , ' ' )
  I11II1i = I11II1i + II11iiii1Ii
 file = open ( IiII , 'w' )
 file . truncate ( )
 file . write ( I11II1i )
 file . close ( )
 xbmc . executebuiltin ( 'Container.Refresh' )
 if 23 - 23: oO0o0ooo / IiiI11Iiiii / i11iIiiIii / i11Ii11I1Ii1i - IiiI11Iiiii
def O0OOOoo0O0 ( name , url , iconimage , fanart ) :
 iiiIi1i1I = oOO00oOO ( name )
 i1iII1IiiIiI1 . setSetting ( 'tv' , iiiIi1i1I )
 o0oOoO00o = i1 ( url )
 OoOo ( o0oOoO00o )
 if 'Index' in url :
  iI ( url )
 if 'XXX' in name : o00O ( o0oOoO00o )
 i1111 = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( o0oOoO00o )
 iIiiiI = str ( len ( i1111 ) )
 i1iII1IiiIiI1 . setSetting ( 'count' , iIiiiI )
 i1iII1IiiIiI1 . setSetting ( 'fav' , 'no' )
 for iIii1I111I11I in i1111 :
  try :
   if '<sportsdevil>' in iIii1I111I11I : OOO0OOO00oo ( iIii1I111I11I , url , iconimage )
   elif '<iptv>' in iIii1I111I11I : Iii111II ( iIii1I111I11I )
   elif '<Image>' in iIii1I111I11I : iiii11I ( iIii1I111I11I )
   elif '<text>' in iIii1I111I11I : Ooo0OO0oOO ( iIii1I111I11I )
   elif '<scraper>' in iIii1I111I11I : ii11i1 ( iIii1I111I11I )
   elif '<redirect>' in iIii1I111I11I : REDIRECT ( iIii1I111I11I )
   elif '<oktitle>' in iIii1I111I11I : IIIii1II1II ( iIii1I111I11I )
   elif '<dl>' in iIii1I111I11I : i1I1iI ( iIii1I111I11I )
   elif '<scraper>' in iIii1I111I11I : ii11i1 ( iIii1I111I11I )
   else : oo0OooOOo0 ( iIii1I111I11I , url , iconimage )
  except : pass
  if 92 - 92: o0o0OOO0o0 . i1I1i1Ii11 + oOoO
def ii11i1 ( item ) :
 i11 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 Oo0o0000o0o0 = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 I11 = re . compile ( '<scraper>(.+?)</scraper>' ) . findall ( item ) [ 0 ]
 oOo0oooo00o ( i11 , I11 , 20 , Oo0o0000o0o0 , I11i )
 if 28 - 28: i1IIi * OoOO - oOoO * ooOOOo0oo0O0 * IIIIII11i1I / iIiI1I11
def OooO0OoOOOO ( url , iconimage ) :
 II11iiii1Ii = url + '.scrape()'
 o0oOoO00o = eval ( II11iiii1Ii )
 i1111 = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( o0oOoO00o )
 iIiiiI = str ( len ( i1111 ) )
 i1iII1IiiIiI1 . setSetting ( 'count' , iIiiiI )
 i1iII1IiiIiI1 . setSetting ( 'fav' , 'no' )
 for iIii1I111I11I in i1111 :
  try :
   if '<sportsdevil>' in iIii1I111I11I : OOO0OOO00oo ( iIii1I111I11I , url , iconimage )
   elif '<iptv>' in iIii1I111I11I : Iii111II ( iIii1I111I11I )
   elif '<Image>' in iIii1I111I11I : iiii11I ( iIii1I111I11I )
   elif '<text>' in iIii1I111I11I : Ooo0OO0oOO ( iIii1I111I11I )
   elif '<scraper>' in iIii1I111I11I : ii11i1 ( iIii1I111I11I )
   elif '<redirect>' in iIii1I111I11I : REDIRECT ( iIii1I111I11I )
   elif '<oktitle>' in iIii1I111I11I : IIIii1II1II ( iIii1I111I11I )
   elif '<dl>' in iIii1I111I11I : i1I1iI ( iIii1I111I11I )
   elif '<scraper>' in iIii1I111I11I : ii11i1 ( iIii1I111I11I , iconimage )
   else : oo0OooOOo0 ( iIii1I111I11I , url , iconimage )
  except : pass
  if 46 - 46: O00 / iiIiIIi
def i1I1iI ( item ) :
 i11 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 I11 = re . compile ( '<dl>(.+?)</dl>' ) . findall ( item ) [ 0 ]
 Oo0o0000o0o0 = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 I1 ( i11 , I11 , 19 , Oo0o0000o0o0 , I11i )
 if 71 - 71: O00 + IiiI11Iiiii % i11iIiiIii + iiIiIIi - ooOOOo0oo0O0
def oO0OOoO0 ( name , url ) :
 I111Ii111 = url . split ( '/' ) [ - 1 ]
 if I111Ii111 == 'latest' : I111Ii111 = 'AceStreamEngine.apk'
 import downloader
 oO0o0o0ooO0oO = xbmcgui . Dialog ( )
 i111IiI1I = xbmcgui . DialogProgress ( )
 O0iII = oO0o0o0ooO0oO . browse ( 0 , 'Select folder to download to' , 'myprograms' )
 o0ooOooo000oOO = os . path . join ( O0iII , I111Ii111 )
 i111IiI1I . create ( 'Downloading' , '' , '' , 'Please Wait' )
 downloader . download ( url , o0ooOooo000oOO , i111IiI1I )
 i111IiI1I . close ( )
 oO0o0o0ooO0oO = xbmcgui . Dialog ( )
 oO0o0o0ooO0oO . ok ( 'Download complete' , 'Please install from..' , O0iII )
 if 59 - 59: i11Ii11I1Ii1i + OoooooooOO * i111I1 + i1IIi
def IIIii1II1II ( item ) :
 i11 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 Oo0OoO00oOO0o = re . compile ( '<oktitle>(.+?)</oktitle>' ) . findall ( item ) [ 0 ]
 OOO00O = re . compile ( '<line1>(.+?)</line1>' ) . findall ( item ) [ 0 ]
 OOoOO0oo0ooO = re . compile ( '<line2>(.+?)</line2>' ) . findall ( item ) [ 0 ]
 O0o0O00Oo0o0 = re . compile ( '<line3>(.+?)</line3>' ) . findall ( item ) [ 0 ]
 O00O0oOO00O00 = '##' + Oo0OoO00oOO0o + '#' + OOO00O + '#' + OOoOO0oo0ooO + '#' + O0o0O00Oo0o0 + '##'
 Oo0o0000o0o0 = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 I1 ( i11 , O00O0oOO00O00 , 17 , Oo0o0000o0o0 , I11i )
 if 11 - 11: ooOOOo0oo0O0 . iiIiIIi
def o0oo0oOo ( name , url ) :
 o000O0o = re . compile ( '##(.+?)##' ) . findall ( url ) [ 0 ] . split ( '#' )
 oO0o0o0ooO0oO = xbmcgui . Dialog ( )
 oO0o0o0ooO0oO . ok ( o000O0o [ 0 ] , o000O0o [ 1 ] , o000O0o [ 2 ] , o000O0o [ 3 ] )
 if 42 - 42: i111I1
def Ooo0OO0oOO ( item ) :
 i11 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 O00O0oOO00O00 = re . compile ( '<text>(.+?)</text>' ) . findall ( item ) [ 0 ]
 Oo0o0000o0o0 = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 I1 ( i11 , O00O0oOO00O00 , 9 , Oo0o0000o0o0 , I11i )
 if 41 - 41: OoOO . IiiI11Iiiii + O0 * oOoO % OoOO * OoOO
def iIIIIi1iiIi1 ( name , url ) :
 iii1i1iiiiIi = i1 ( url )
 Iiii ( name , iii1i1iiiiIi )
 if 75 - 75: i111I1 % oOoO % oOoO . oO0o0ooo
def iiii11I ( item ) :
 III1iII1I1ii = re . compile ( '<Image>(.+?)</Image>' ) . findall ( item )
 if len ( III1iII1I1ii ) == 1 :
  i11 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  Oo0o0000o0o0 = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  oOOo0 = re . compile ( '<Image>(.+?)</Image>' ) . findall ( item ) [ 0 ]
  Oo0o0000o0o0 = oOOo0 . replace ( 'http://imgur.com/' , 'http://i.imgur.com/' ) + '.jpg'
  oOOo0 = oOOo0 . replace ( 'http://imgur.com/' , 'http://i.imgur.com/' ) + '.jpg'
  I1 ( i11 , oOOo0 , 7 , Oo0o0000o0o0 , I11i )
 elif len ( III1iII1I1ii ) > 1 :
  i11 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  Oo0o0000o0o0 = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  oo00O00oO = ''
  for oOOo0 in III1iII1I1ii :
   Oo0o0000o0o0 = oOOo0 . replace ( 'http://imgur.com/' , 'http://i.imgur.com/' ) + '.jpg'
   oOOo0 = oOOo0 . replace ( 'http://imgur.com/' , 'http://i.imgur.com/' ) + '.jpg'
   oo00O00oO = oo00O00oO + '<Image>' + oOOo0 + '</Image>'
  iIiIIIi = iI111iI
  i11 = oOO00oOO ( i11 )
  ooo00OOOooO = os . path . join ( os . path . join ( iIiIIIi , '' ) , i11 + '.txt' )
  if not os . path . exists ( ooo00OOOooO ) : file ( ooo00OOOooO , 'w' ) . close ( )
  O00OOOoOoo0O = open ( ooo00OOOooO , "w" )
  O00OOOoOoo0O . write ( oo00O00oO )
  O00OOOoOoo0O . close ( )
  I1 ( i11 , 'image' , 8 , Oo0o0000o0o0 , I11i )
  if 77 - 77: o0o0OOO0o0 % o0o0OOO0o0 * ooOoo0O - i11iIiiIii
def Iii111II ( item ) :
 i11 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 Oo0o0000o0o0 = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 I11 = re . compile ( '<iptv>(.+?)</iptv>' ) . findall ( item ) [ 0 ]
 oOo0oooo00o ( i11 , I11 , 6 , Oo0o0000o0o0 , I11i )
 if 93 - 93: OoooooooOO / iIIIIiI % i11iIiiIii + iiIiIIi * iIiI1I11
def I1iI11Ii ( url , iconimage ) :
 o0oOoO00o = i1 ( url )
 i1iIIIi1i = re . compile ( '^#.+?:-?[0-9]*(.*?),(.*?)\n(.*?)$' , re . I + re . M + re . U + re . S ) . findall ( o0oOoO00o )
 iI1iIIiiii = [ ]
 for i1iI11i1ii11 , i11 , url in i1iIIIi1i :
  OOooo0O00o = { "params" : i1iI11i1ii11 , "name" : i11 , "url" : url }
  iI1iIIiiii . append ( OOooo0O00o )
 list = [ ]
 for oOOoOooOo in iI1iIIiiii :
  OOooo0O00o = { "name" : oOOoOooOo [ "name" ] , "url" : oOOoOooOo [ "url" ] }
  i1iIIIi1i = re . compile ( ' (.+?)="(.+?)"' , re . I + re . M + re . U + re . S ) . findall ( oOOoOooOo [ "params" ] )
  for O000oo , IIi1I11I1II in i1iIIIi1i :
   OOooo0O00o [ O000oo . strip ( ) . lower ( ) . replace ( '-' , '_' ) ] = IIi1I11I1II . strip ( )
  list . append ( OOooo0O00o )
 for oOOoOooOo in list :
  if '.ts' in oOOoOooOo [ "url" ] : I1 ( oOOoOooOo [ "name" ] , oOOoOooOo [ "url" ] , 2 , iconimage , I11i )
  else : iiiIi ( oOOoOooOo [ "name" ] , oOOoOooOo [ "url" ] , 2 , iconimage , I11i )
  if 63 - 63: OoooooooOO - iIiI1I11 . i11Ii11I1Ii1i / oOoO . i111I1 / O0
def oo0OooOOo0 ( item , url , iconimage ) :
 o0OOOO00O0Oo = iconimage
 ii = url
 oOooOOOoOo = re . compile ( '<link>(.+?)</link>' ) . findall ( item )
 OO00OooO0OO = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>' , re . DOTALL ) . findall ( item )
 for i11 , i1Iii1i1I , iconimage in OO00OooO0OO :
  if 'youtube.com/playlist?' in i1Iii1i1I :
   OOoO00 = i1Iii1i1I . split ( 'list=' ) [ 1 ]
   oOo0oooo00o ( i11 , i1Iii1i1I , IiI111111IIII , iconimage , I11i , description = OOoO00 )
 if len ( oOooOOOoOo ) == 1 :
  i11 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  url = re . compile ( '<link>(.+?)</link>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  if iconimage == 'ImageHere' : iconimage = o0OOOO00O0Oo
  if '.ts' in url : I1 ( i11 , url , 16 , iconimage , I11i , description = '' )
  elif 'movies' in ii :
   i1Ii ( i11 , url , 2 , iconimage , int ( iIiiiI ) , isFolder = False )
  else : iiiIi ( i11 , url , 2 , iconimage , I11i )
 elif len ( oOooOOOoOo ) > 1 :
  i11 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  if iconimage == 'ImageHere' : iconimage = o0OOOO00O0Oo
  print iconimage
  if '.ts' in url : I1 ( i11 , url , 16 , iconimage , I11i , description = '' )
  elif 'movies' in ii :
   i1Ii ( i11 , url , 3 , iconimage , int ( iIiiiI ) , isFolder = False )
  else : iiiIi ( i11 , url , 3 , iconimage , I11i )
  if 14 - 14: o0o0OOO0o0
def iI ( url ) :
 o0oOoO00o = i1 ( url )
 i1111 = re . compile ( 'name="(.+?)".+?rl="(.+?)".+?mg="(.+?)"' , re . DOTALL ) . findall ( o0oOoO00o )
 for i11 , url , Oo in i1111 :
  if 'youtube.com/playlist?list=' in url :
   oOo0oooo00o ( i11 , url , 18 , Oo , I11i )
  elif 'youtube.com/results?search_query=' in url :
   oOo0oooo00o ( i11 , url , 18 , Oo , I11i )
  else :
   oOo0oooo00o ( i11 , url , 1 , Oo , I11i )
   if 11 - 11: ooOOOo0oo0O0 * iIIIIiI . iIii1I11I1II1 % OoooooooOO + o0o0OOO0o0
def OOO ( name , url , iconimage ) :
 if 'youtube.com/results?search_query=' in url :
  OOoO00 = url . split ( 'search_query=' ) [ 1 ]
  oo0OOo0 = i1i1II + OOoO00 + O0oo0OO0
  I11IiI = urllib2 . Request ( oo0OOo0 )
  I11IiI . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' )
  O0ooO0Oo00o = urllib2 . urlopen ( I11IiI )
  o0oOoO00o = O0ooO0Oo00o . read ( )
  O0ooO0Oo00o . close ( )
  o0oOoO00o = o0oOoO00o . replace ( '\r' , '' ) . replace ( '\n' , '' ) . replace ( '  ' , '' )
  i1111 = re . compile ( '"videoId": "(.+?)".+?"title": "(.+?)"' , re . DOTALL ) . findall ( o0oOoO00o )
  for ooO0oOOooOo0 , name in i1111 :
   url = 'https://www.youtube.com/watch?v=' + ooO0oOOooOo0
   iconimage = 'https://i.ytimg.com/vi/%s/hqdefault.jpg' % ooO0oOOooOo0
   iiiIi ( name , url , 2 , iconimage , I11i )
 elif 'youtube.com/playlist?list=' in url :
  OOoO00 = url . split ( 'playlist?list=' ) [ 1 ]
  oo0OOo0 = I1i1iiI1 + OOoO00 + iiIIIII1i1iI
  I11IiI = urllib2 . Request ( oo0OOo0 )
  I11IiI . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' )
  O0ooO0Oo00o = urllib2 . urlopen ( I11IiI )
  o0oOoO00o = O0ooO0Oo00o . read ( )
  O0ooO0Oo00o . close ( )
  o0oOoO00o = o0oOoO00o . replace ( '\r' , '' ) . replace ( '\n' , '' ) . replace ( '  ' , '' )
  i1111 = re . compile ( '"title": "(.+?)".+?"videoId": "(.+?)"' , re . DOTALL ) . findall ( o0oOoO00o )
  for name , ooO0oOOooOo0 in i1111 :
   url = 'https://www.youtube.com/watch?v=' + ooO0oOOooOo0
   iconimage = 'https://i.ytimg.com/vi/%s/hqdefault.jpg' % ooO0oOOooOo0
   iiiIi ( name , url , 2 , iconimage , I11i )
   if 38 - 38: oO0o0ooo
def Ooo00o0Oooo ( item ) :
 item = item . replace ( '\r' , '' ) . replace ( '\t' , '' ) . replace ( '&nbsp;' , '' ) . replace ( '\'' , '' ) . replace ( '\n' , '' )
 OO00OooO0OO = re . compile ( 'name="(.+?)".+?rl="(.+?)".+?mg="(.+?)"' , re . DOTALL ) . findall ( item )
 for i11 , I11 , Oo0o0000o0o0 in OO00OooO0OO :
  if 'youtube.com/channel/' in I11 :
   OOoO00 = I11 . split ( 'channel/' ) [ 1 ]
   oOo0oooo00o ( i11 , I11 , IiI111111IIII , Oo0o0000o0o0 , I11i , description = OOoO00 )
  elif 'youtube.com/user/' in I11 :
   OOoO00 = I11 . split ( 'user/' ) [ 1 ]
   oOo0oooo00o ( i11 , I11 , IiI111111IIII , Oo0o0000o0o0 , I11i , description = OOoO00 )
  elif 'youtube.com/playlist?' in I11 :
   OOoO00 = I11 . split ( 'list=' ) [ 1 ]
   oOo0oooo00o ( i11 , I11 , IiI111111IIII , Oo0o0000o0o0 , I11i , description = OOoO00 )
  elif 'plugin://' in I11 :
   OOooooO0Oo = HTMLParser ( )
   I11 = OOooooO0Oo . unescape ( I11 )
   oOo0oooo00o ( i11 , I11 , IiI111111IIII , Oo0o0000o0o0 , I11i )
  else :
   oOo0oooo00o ( i11 , I11 , 1 , Oo0o0000o0o0 , I11i )
   if 91 - 91: oOoO . iIii1I11I1II1 / ooOoo0O + i1IIi
def OOO0OOO00oo ( item , url , iconimage ) :
 o0OOOO00O0Oo = iconimage
 oOooOOOoOo = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( item )
 I1i = re . compile ( '<link>(.+?)</link>' ) . findall ( item )
 if len ( oOooOOOoOo ) + len ( I1i ) == 1 :
  i11 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  url = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( item ) [ 0 ]
  url = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' + url
  if iconimage == 'ImageHere' : iconimage = o0OOOO00O0Oo
  I1 ( i11 , url , 16 , iconimage , I11i )
 elif len ( oOooOOOoOo ) + len ( I1i ) > 1 :
  i11 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  if iconimage == 'ImageHere' : iconimage = o0OOOO00O0Oo
  I1 ( i11 , url , 3 , iconimage , I11i )
  if 53 - 53: iiIiIIi * i111I1 + IiiI11Iiiii - i11Ii11I1Ii1i
def o00O ( link ) :
 if o0OOO == '' :
  oO0o0o0ooO0oO = xbmcgui . Dialog ( )
  oo0o0O00 = oO0o0o0ooO0oO . yesno ( 'Adult Content' , 'You have opted to show adult content' , '' , 'Please set a password to prevent accidental access' , 'Cancel' , 'OK' )
  if oo0o0O00 == 1 :
   oO = xbmc . Keyboard ( '' , 'Set Password' )
   oO . doModal ( )
   if ( oO . isConfirmed ( ) ) :
    i1iiIIiiI111 = oO . getText ( )
    i1iII1IiiIiI1 . setSetting ( 'password' , i1iiIIiiI111 )
  else : quit ( )
 elif o0OOO <> '' :
  oO0o0o0ooO0oO = xbmcgui . Dialog ( )
  oo0o0O00 = oO0o0o0ooO0oO . yesno ( 'Adult Content' , 'Please enter the password you set' , 'to continue' , '' , 'Cancel' , 'OK' )
  if oo0o0O00 == 1 :
   oO = xbmc . Keyboard ( '' , 'Enter Password' )
   oO . doModal ( )
   if ( oO . isConfirmed ( ) ) :
    i1iiIIiiI111 = oO . getText ( )
   if i1iiIIiiI111 <> o0OOO :
    quit ( )
  else : quit ( )
  if 2 - 2: i1I1i1Ii11 + IIIIII11i1I - iIIIIiI % oOoO . o0o0OOO0o0
def I1I1i1I ( ) :
 oO = xbmc . Keyboard ( '' , 'Search' )
 oO . doModal ( )
 if ( oO . isConfirmed ( ) ) :
  OOoO00 = oO . getText ( )
  OOoO00 = OOoO00 . upper ( )
 else : quit ( )
 o0oOoO00o = i1 ( iI1Ii11111iIi )
 ii1I = re . compile ( '<link>(.+?)</link>' ) . findall ( o0oOoO00o )
 for I11 in ii1I :
  try :
   o0oOoO00o = i1 ( I11 )
   O0oO0 = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( o0oOoO00o )
   for iIii1I111I11I in O0oO0 :
    i1111 = re . compile ( '<title>(.+?)</title>' ) . findall ( iIii1I111I11I )
    for oO0 in i1111 :
     oO0 = oO0 . upper ( )
     if OOoO00 in oO0 :
      try :
       if '<sportsdevil>' in iIii1I111I11I : OOO0OOO00oo ( iIii1I111I11I , I11 , Oo0o0000o0o0 )
       elif '<iptv>' in iIii1I111I11I : Iii111II ( iIii1I111I11I )
       elif '<Image>' in iIii1I111I11I : iiii11I ( iIii1I111I11I )
       elif '<text>' in iIii1I111I11I : Ooo0OO0oOO ( iIii1I111I11I )
       elif '<scraper>' in iIii1I111I11I : ii11i1 ( iIii1I111I11I )
       elif '<redirect>' in iIii1I111I11I : REDIRECT ( iIii1I111I11I )
       elif '<oktitle>' in iIii1I111I11I : IIIii1II1II ( iIii1I111I11I )
       elif '<dl>' in iIii1I111I11I : i1I1iI ( iIii1I111I11I )
       elif '<scraper>' in iIii1I111I11I : ii11i1 ( iIii1I111I11I , Oo0o0000o0o0 )
       else : oo0OooOOo0 ( iIii1I111I11I , I11 , Oo0o0000o0o0 )
      except : pass
  except : pass
  if 75 - 75: IiiI11Iiiii + i111I1 + oOoO * i1I1i1Ii11 % ooOoo0O . o0o0OOO0o0
def oOI1Ii1I1 ( name , url , iconimage ) :
 o0OOOO00O0Oo = iconimage
 IiII111iI1ii1 = [ ]
 iI11I1II = [ ]
 Ii1I = [ ]
 o0oOoO00o = i1 ( url )
 IiI1i = re . compile ( '<title>' + re . escape ( name ) + '</title>(.+?)</item>' , re . DOTALL ) . findall ( o0oOoO00o ) [ 0 ]
 oOooOOOoOo = [ ]
 if '<link>' in IiI1i :
  o0O = re . compile ( '<link>(.+?)</link>' ) . findall ( IiI1i )
  for o00 in o0O :
   oOooOOOoOo . append ( o00 )
 if '<sportsdevil>' in IiI1i :
  iIO0O0Oooo0o = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( IiI1i )
  for oOOoo00O00o in iIO0O0Oooo0o :
   oOOoo00O00o = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' + oOOoo00O00o
   oOooOOOoOo . append ( oOOoo00O00o )
 O0O00Oo = 1
 for oooooo0O000o in oOooOOOoOo :
  OoO = oooooo0O000o
  if 'acestream://' in oooooo0O000o or '.acelive' in oooooo0O000o or 'sop://' in oooooo0O000o : ooO0O0O0ooOOO = ' (Acestreams)'
  else : ooO0O0O0ooOOO = ''
  if '(' in oooooo0O000o :
   oooooo0O000o = oooooo0O000o . split ( '(' ) [ 0 ]
   oOOo0O00o = str ( OoO . split ( '(' ) [ 1 ] . replace ( ')' , '' ) + ooO0O0O0ooOOO )
   IiII111iI1ii1 . append ( oooooo0O000o )
   iI11I1II . append ( oOOo0O00o )
  else :
   iIiIi11 = oooooo0O000o . split ( '/' ) [ 2 ] . replace ( 'www.' , '' )
   IiII111iI1ii1 . append ( oooooo0O000o )
   iI11I1II . append ( 'Link ' + str ( O0O00Oo ) + ooO0O0O0ooOOO )
  O0O00Oo = O0O00Oo + 1
 oO0o0o0ooO0oO = xbmcgui . Dialog ( )
 OOOiiiiI = oO0o0o0ooO0oO . select ( 'Choose a link..' , iI11I1II )
 if OOOiiiiI < 0 : quit ( )
 else :
  url = IiII111iI1ii1 [ OOOiiiiI ]
  oooOo0OOOoo0 ( name , url , iconimage )
  if 51 - 51: OoOO / i111I1 . O00 * oOoO + iIiI1I11 * ooOOOo0oo0O0
def OOOoOo ( url ) :
 II11iiii1Ii = "ShowPicture(%s)" % url
 xbmc . executebuiltin ( II11iiii1Ii )
 if 51 - 51: IiiI11Iiiii / iIii1I11I1II1 % OoOO * iIIIIiI % oO0o0ooo
def oooOo0OOOoo0 ( name , url , iconimage ) :
 try :
  if 'sop://' in url :
   url = urllib . quote ( url )
   url = 'plugin://program.plexus/?mode=2&url=%s&name=%s' % ( url , name . replace ( ' ' , '+' ) )
   oOoooOOO ( name , url , iconimage )
  elif 'acestream://' in url or '.acelive' in url :
   url = urllib . quote ( url )
   url = 'plugin://program.plexus/?mode=1&url=%s&name=%s' % ( url , name . replace ( ' ' , '+' ) )
   oOoooOOO ( name , url , iconimage )
  elif 'plugin://plugin.video.SportsDevil/' in url :
   oOoooOOO ( name , url , iconimage )
  elif '.ts' in url :
   url = 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;name=' + name + '&amp;url=' + url
   oOoooOOO ( name , url , iconimage )
  elif urlresolver . HostedMediaFile ( url ) . valid_url ( ) :
   url = urlresolver . HostedMediaFile ( url ) . resolve ( )
   oo00oO0O0 ( name , url , iconimage )
  elif liveresolver . isValid ( url ) == True :
   url = liveresolver . resolve ( url )
   oo00oO0O0 ( name , url , iconimage )
  else : oo00oO0O0 ( name , url , iconimage )
 except :
  I11I11 ( 'UKTurk' , 'Stream Unavailable' , '3000' , Oo )
  if 69 - 69: i111I1
def OO0OoOO0o0o ( url ) :
 if urlresolver . HostedMediaFile ( url ) . valid_url ( ) :
  url = urlresolver . HostedMediaFile ( url ) . resolve ( )
 xbmc . Player ( ) . play ( url )
 if 95 - 95: i11iIiiIii
def oo00oO0O0 ( name , url , iconimage ) :
 iI1111iiii = True
 Oo0OO = xbmcgui . ListItem ( name , iconImage = iconimage , thumbnailImage = iconimage ) ; Oo0OO . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
 iI1111iiii = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = url , listitem = Oo0OO )
 Oo0OO . setPath ( url )
 xbmcplugin . setResolvedUrl ( int ( sys . argv [ 1 ] ) , True , Oo0OO )
 if 78 - 78: O00 - OoooooooOO - iiIiIIi / IiiI11Iiiii / i11Ii11I1Ii1i
def oOoooOOO ( name , url , iconimage ) :
 iI1111iiii = True
 Oo0OO = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage ) ; Oo0OO . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
 iI1111iiii = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = url , listitem = Oo0OO )
 oO0o0o0ooO0oO = xbmcgui . Dialog ( )
 xbmc . Player ( ) . play ( url , Oo0OO , False )
 if 29 - 29: iIIIIiI % iIIIIiI
def Oo0O0 ( url ) :
 xbmc . executebuiltin ( "PlayMedia(%s)" % url )
 if 82 - 82: i11Ii11I1Ii1i % i1I1i1Ii11 / iIiI1I11 + i111I1 / oOoO / oO0o0ooo
def oOo0OOoO0 ( url ) :
 II = i1iII1IiiIiI1 . getSetting ( 'layout' )
 if II == 'Listers' : i1iII1IiiIiI1 . setSetting ( 'layout' , 'Category' )
 else : i1iII1IiiIiI1 . setSetting ( 'layout' , 'Listers' )
 xbmc . executebuiltin ( 'Container.Refresh' )
 if 93 - 93: ooOOOo0oo0O0 * OoooooooOO + IiiI11Iiiii
def i1 ( url ) :
 I11IiI = urllib2 . Request ( url )
 I11IiI . add_header ( 'User-Agent' , 'mat' )
 O0ooO0Oo00o = urllib2 . urlopen ( I11IiI )
 o0oOoO00o = O0ooO0Oo00o . read ( )
 O0ooO0Oo00o . close ( )
 o0oOoO00o = o0oOoO00o . replace ( '</fanart>' , '<fanart>x</fanart>' ) . replace ( '<thumbnail></thumbnail>' , '<thumbnail>x</thumbnail>' ) . replace ( '<utube>' , '<link>https://www.youtube.com/watch?v=' ) . replace ( '</utube>' , '</link>' )
 if '{' in o0oOoO00o : o0oOoO00o = IiII111i1i11 ( o0oOoO00o )
 return o0oOoO00o
 if 40 - 40: IiiI11Iiiii * ooOOOo0oo0O0 * i11iIiiIii
def oo0OO00OoooOo ( ) :
 II1i111Ii1i = [ ]
 iii1 = sys . argv [ 2 ]
 if len ( iii1 ) >= 2 :
  i1iI11i1ii11 = sys . argv [ 2 ]
  ooO0oooOO0 = i1iI11i1ii11 . replace ( '?' , '' )
  if ( i1iI11i1ii11 [ len ( i1iI11i1ii11 ) - 1 ] == '/' ) :
   i1iI11i1ii11 = i1iI11i1ii11 [ 0 : len ( i1iI11i1ii11 ) - 2 ]
  o0o = ooO0oooOO0 . split ( '&' )
  II1i111Ii1i = { }
  for O0O00Oo in range ( len ( o0o ) ) :
   oo0 = { }
   oo0 = o0o [ O0O00Oo ] . split ( '=' )
   if ( len ( oo0 ) ) == 2 :
    II1i111Ii1i [ oo0 [ 0 ] ] = oo0 [ 1 ]
 return II1i111Ii1i
 if 61 - 61: i111I1 - O00 - i1IIi
def I11I11 ( title , message , ms , nart ) :
 xbmc . executebuiltin ( "XBMC.notification(" + title + "," + message + "," + ms + "," + nart + ")" )
 if 25 - 25: O0 * i1I1i1Ii11 + iiIiIIi . oOoO . oOoO
def oOO00oOO ( string ) :
 oOooO = re . compile ( '\[(.+?)\]' ) . findall ( string )
 for IIIIiI11I11 in oOooO : string = string . replace ( IIIIiI11I11 , '' ) . replace ( '[/]' , '' ) . replace ( '[]' , '' )
 return string
 if 58 - 58: iIIIIiI
def Ii1iI111II1I1 ( string ) :
 string = string . split ( ' ' )
 oOOOOoOO0o = ''
 for i1II1 in string :
  i11i1 = '[B][COLOR red]' + i1II1 [ 0 ] . upper ( ) + '[/COLOR][COLOR white]' + i1II1 [ 1 : ] + '[/COLOR][/B] '
  oOOOOoOO0o = oOOOOoOO0o + i11i1
 return oOOOOoOO0o
 if 42 - 42: i11iIiiIii * iIii1I11I1II1 / iiIiIIi . i11iIiiIii % i1I1i1Ii11
def i1Ii ( name , url , mode , iconimage , itemcount , isFolder = False ) :
 if Iii1ii1II11i == 'true' :
  if not 'COLOR' in name :
   i1iI = name . partition ( '(' )
   IiI1iiiIii = ""
   I1III1111iIi = ""
   if len ( i1iI ) > 0 :
    IiI1iiiIii = i1iI [ 0 ]
    I1III1111iIi = i1iI [ 2 ] . partition ( ')' )
   if len ( I1III1111iIi ) > 0 :
    I1III1111iIi = I1III1111iIi [ 0 ]
   I1i111I = eval ( base64 . b64decode ( 'bWV0YWhhbmRsZXJzLk1ldGFEYXRhKHRtZGJfYXBpX2tleT0iZDk1NWQ4ZjAyYTNmMjQ4MGE1MTg4MWZlNGM5NmYxMGUiKQ==' ) )
   OooOo0oo0O0o00O = I1i111I . get_meta ( 'movie' , name = IiI1iiiIii , year = I1III1111iIi )
   I1i11 = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&site=" + str ( IiIi1I1 ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name )
   iI1111iiii = True
   Oo0OO = xbmcgui . ListItem ( name , iconImage = OooOo0oo0O0o00O [ 'cover_url' ] , thumbnailImage = OooOo0oo0O0o00O [ 'cover_url' ] )
   Oo0OO . setInfo ( type = "Video" , infoLabels = OooOo0oo0O0o00O )
   Oo0OO . setProperty ( "IsPlayable" , "true" )
   IiIIi1 = [ ]
   if i1iII1IiiIiI1 . getSetting ( 'fav' ) == 'yes' : IiIIi1 . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
   if i1iII1IiiIiI1 . getSetting ( 'fav' ) == 'no' : IiIIi1 . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
   Oo0OO . addContextMenuItems ( IiIIi1 , replaceItems = False )
   if not OooOo0oo0O0o00O [ 'backdrop_url' ] == '' : Oo0OO . setProperty ( 'fanart_image' , OooOo0oo0O0o00O [ 'backdrop_url' ] )
   else : Oo0OO . setProperty ( 'fanart_image' , I11i )
   iI1111iiii = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = I1i11 , listitem = Oo0OO , isFolder = isFolder , totalItems = itemcount )
   return iI1111iiii
 else :
  I1i11 = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&site=" + str ( IiIi1I1 ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name )
  iI1111iiii = True
  Oo0OO = xbmcgui . ListItem ( name , iconImage = iconimage , thumbnailImage = iconimage )
  Oo0OO . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
  Oo0OO . setProperty ( 'fanart_image' , I11i )
  Oo0OO . setProperty ( "IsPlayable" , "true" )
  IiIIi1 = [ ]
  if i1iII1IiiIiI1 . getSetting ( 'fav' ) == 'yes' : IiIIi1 . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
  if i1iII1IiiIiI1 . getSetting ( 'fav' ) == 'no' : IiIIi1 . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
  Oo0OO . addContextMenuItems ( IiIIi1 , replaceItems = False )
  iI1111iiii = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = I1i11 , listitem = Oo0OO , isFolder = isFolder )
  return iI1111iiii
  if 47 - 47: OoOO * iiIiIIi + iIii1I11I1II1 / oO0o0ooo / iIiI1I11 - OoooooooOO
def oOo0oooo00o ( name , url , mode , iconimage , fanart , description = '' ) :
 I1i11 = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&fanart=" + urllib . quote_plus ( fanart ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 iI1111iiii = True
 Oo0OO = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 Oo0OO . setInfo ( type = "Video" , infoLabels = { "Title" : name , 'plot' : description } )
 Oo0OO . setProperty ( 'fanart_image' , fanart )
 IiIIi1 = [ ]
 if i1iII1IiiIiI1 . getSetting ( 'fav' ) == 'yes' : IiIIi1 . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 if i1iII1IiiIiI1 . getSetting ( 'fav' ) == 'no' : IiIIi1 . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 Oo0OO . addContextMenuItems ( IiIIi1 , replaceItems = False )
 if 'plugin://' in url :
  I1i11 = url
 iI1111iiii = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = I1i11 , listitem = Oo0OO , isFolder = True )
 return iI1111iiii
 if 33 - 33: i111I1 * O00 - i11Ii11I1Ii1i
def I1 ( name , url , mode , iconimage , fanart , description = '' ) :
 I1i11 = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 iI1111iiii = True
 Oo0OO = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 Oo0OO . setProperty ( 'fanart_image' , fanart )
 IiIIi1 = [ ]
 if i1iII1IiiIiI1 . getSetting ( 'fav' ) == 'yes' : IiIIi1 . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 if i1iII1IiiIiI1 . getSetting ( 'fav' ) == 'no' : IiIIi1 . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 Oo0OO . addContextMenuItems ( IiIIi1 , replaceItems = False )
 iI1111iiii = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = I1i11 , listitem = Oo0OO , isFolder = False )
 return iI1111iiii
 if 83 - 83: i111I1 - IIIIII11i1I / i1I1i1Ii11 / oO0o0ooo + ooOoo0O - O0
def iiiIi ( name , url , mode , iconimage , fanart , description = '' ) :
 I1i11 = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 iI1111iiii = True
 Oo0OO = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 Oo0OO . setProperty ( 'fanart_image' , fanart )
 Oo0OO . setProperty ( "IsPlayable" , "true" )
 IiIIi1 = [ ]
 if i1iII1IiiIiI1 . getSetting ( 'fav' ) == 'yes' : IiIIi1 . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 if i1iII1IiiIiI1 . getSetting ( 'fav' ) == 'no' : IiIIi1 . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 Oo0OO . addContextMenuItems ( IiIIi1 , replaceItems = False )
 iI1111iiii = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = I1i11 , listitem = Oo0OO , isFolder = False )
 return iI1111iiii
 if 4 - 4: O00 * iIiI1I11 % i1IIi * i11iIiiIii % OoOO - ooOoo0O
def OOoOoOo ( url , name ) :
 o000ooooO0o = i1 ( url )
 if len ( o000ooooO0o ) > 1 :
  iIiIIIi = iI111iI
  ooo00OOOooO = os . path . join ( os . path . join ( iIiIIIi , '' ) , name + '.txt' )
  if not os . path . exists ( ooo00OOOooO ) :
   file ( ooo00OOOooO , 'w' ) . close ( )
  iI1i11 = open ( ooo00OOOooO )
  OoOOoooOO0O = iI1i11 . read ( )
  if OoOOoooOO0O == o000ooooO0o : pass
  else :
   Iiii ( 'UKTurk' , o000ooooO0o )
   O00OOOoOoo0O = open ( ooo00OOOooO , "w" )
   O00OOOoOoo0O . write ( o000ooooO0o )
   O00OOOoOoo0O . close ( )
   if 86 - 86: oOoO
def Iiii ( heading , text ) :
 id = 10147
 xbmc . executebuiltin ( 'ActivateWindow(%d)' % id )
 xbmc . sleep ( 500 )
 i1Iii11Ii1i1 = xbmcgui . Window ( id )
 OOooo0O0o0 = 50
 while ( OOooo0O0o0 > 0 ) :
  try :
   xbmc . sleep ( 10 )
   OOooo0O0o0 -= 1
   i1Iii11Ii1i1 . getControl ( 1 ) . setLabel ( heading )
   i1Iii11Ii1i1 . getControl ( 5 ) . setText ( text )
   return
  except :
   pass
   if 14 - 14: oOoO % O0 * o0o0OOO0o0 + IIIIII11i1I + OoOO * IIIIII11i1I
def iII1I1IiI11ii ( name ) :
 global Icon
 global Next
 global Previous
 global window
 global Quit
 global images
 ooo00OOOooO = os . path . join ( os . path . join ( iI111iI , '' ) , name + '.txt' )
 iI1i11 = open ( ooo00OOOooO )
 OoOOoooOO0O = iI1i11 . read ( )
 images = re . compile ( '<image>(.+?)</image>' ) . findall ( OoOOoooOO0O )
 i1iII1IiiIiI1 . setSetting ( 'pos' , '0' )
 window = pyxbmct . AddonDialogWindow ( '' )
 OooooOoooO = '/resources/art'
 oOIIiIi = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + o0OO00 + OooooOoooO , 'next_focus.png' ) )
 OOoOooOoOOOoo = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + o0OO00 + OooooOoooO , 'next1.png' ) )
 Iiii1iI1i = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + o0OO00 + OooooOoooO , 'previous_focus.png' ) )
 I1ii1ii11i1I = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + o0OO00 + OooooOoooO , 'previous.png' ) )
 o0OoOO = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + o0OO00 + OooooOoooO , 'close_focus.png' ) )
 O0O0Oo00 = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + o0OO00 + OooooOoooO , 'close.png' ) )
 oOoO00o = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + o0OO00 + OooooOoooO , 'main-bg1.png' ) )
 window . setGeometry ( 1300 , 720 , 100 , 50 )
 oO00O0 = pyxbmct . Image ( oOoO00o )
 window . placeControl ( oO00O0 , - 10 , - 10 , 130 , 70 )
 O00O0oOO00O00 = '0xFF000000'
 Previous = pyxbmct . Button ( '' , focusTexture = Iiii1iI1i , noFocusTexture = I1ii1ii11i1I , textColor = O00O0oOO00O00 , focusedColor = O00O0oOO00O00 )
 Next = pyxbmct . Button ( '' , focusTexture = oOIIiIi , noFocusTexture = OOoOooOoOOOoo , textColor = O00O0oOO00O00 , focusedColor = O00O0oOO00O00 )
 Quit = pyxbmct . Button ( '' , focusTexture = o0OoOO , noFocusTexture = O0O0Oo00 , textColor = O00O0oOO00O00 , focusedColor = O00O0oOO00O00 )
 Icon = pyxbmct . Image ( images [ 0 ] , aspectRatio = 1 )
 window . placeControl ( Previous , 102 , 1 , 10 , 10 )
 window . placeControl ( Next , 102 , 40 , 10 , 10 )
 window . placeControl ( Quit , 102 , 21 , 10 , 10 )
 window . placeControl ( Icon , 0 , 0 , 100 , 50 )
 Previous . controlRight ( Next )
 Previous . controlUp ( Quit )
 window . connect ( Previous , IIi1IIIi )
 window . connect ( Next , O00Ooo )
 Previous . setVisible ( False )
 window . setFocus ( Quit )
 Previous . controlRight ( Quit )
 Quit . controlLeft ( Previous )
 Quit . controlRight ( Next )
 Next . controlLeft ( Quit )
 window . connect ( Quit , window . close )
 window . doModal ( )
 del window
 if 52 - 52: iiIiIIi - OoOO + iiIiIIi % oOoO
def O00Ooo ( ) :
 iI1 = int ( i1iII1IiiIiI1 . getSetting ( 'pos' ) )
 IiI = int ( iI1 ) + 1
 i1iII1IiiIiI1 . setSetting ( 'pos' , str ( IiI ) )
 iI1ii1i = len ( images )
 Icon . setImage ( images [ int ( IiI ) ] )
 Previous . setVisible ( True )
 if int ( IiI ) == int ( iI1ii1i ) - 1 :
  Next . setVisible ( False )
  if 85 - 85: OoooooooOO % i1IIi * OoooooooOO / iiIiIIi
def IIi1IIIi ( ) :
 iI1 = int ( i1iII1IiiIiI1 . getSetting ( 'pos' ) )
 ooOOoO = int ( iI1 ) - 1
 i1iII1IiiIiI1 . setSetting ( 'pos' , str ( ooOOoO ) )
 Icon . setImage ( images [ int ( ooOOoO ) ] )
 Next . setVisible ( True )
 if int ( ooOOoO ) == 0 :
  Previous . setVisible ( False )
  if 20 - 20: i1I1i1Ii11 + IIIIII11i1I / O0 % iIii1I11I1II1
def IiII111i1i11 ( gobble ) :
 gobble = gobble . replace ( '}' , '' ) . replace ( '{' , '' ) . replace ( ',' , '' ) . replace ( ']' , '' ) . replace ( '[' , '' )
 gobble = gobble + '=='
 gobble = gobble . decode ( 'base64' )
 return gobble
 if 88 - 88: i111I1 / i11Ii11I1Ii1i
def OoOo ( link ) :
 try :
  OOOOO0O00 = re . compile ( '<layouttype>(.+?)</layouttype>' ) . findall ( link ) [ 0 ]
  if OOOOO0O00 == 'thumbnail' : xbmc . executebuiltin ( 'Container.SetViewMode(500)' )
  else : xbmc . executebuiltin ( 'Container.SetViewMode(50)' )
 except : pass
 if 30 - 30: iIii1I11I1II1 . iIIIIiI . O00 / oOoO
i1iI11i1ii11 = oo0OO00OoooOo ( ) ; I11 = None ; i11 = None ; IiI111111IIII = None ; IiIi1I1 = None ; Oo0o0000o0o0 = None
try : IiIi1I1 = urllib . unquote_plus ( i1iI11i1ii11 [ "site" ] )
except : pass
try : I11 = urllib . unquote_plus ( i1iI11i1ii11 [ "url" ] )
except : pass
try : i11 = urllib . unquote_plus ( i1iI11i1ii11 [ "name" ] )
except : pass
try : IiI111111IIII = int ( i1iI11i1ii11 [ "mode" ] )
except : pass
try : Oo0o0000o0o0 = urllib . unquote_plus ( i1iI11i1ii11 [ "iconimage" ] )
except : pass
try : I11i = urllib . unquote_plus ( i1iI11i1ii11 [ "fanart" ] )
except : pass
if 42 - 42: OoOO
try : II1IIiiIiI = urllib . unquote_plus ( [ "description" ] )
except : pass
if 1 - 1: o0o0OOO0o0
if IiI111111IIII == None or I11 == None or len ( I11 ) < 1 : Ooo ( )
elif IiI111111IIII == 1 : O0OOOoo0O0 ( i11 , I11 , Oo0o0000o0o0 , I11i )
elif IiI111111IIII == 2 : oooOo0OOOoo0 ( i11 , I11 , Oo0o0000o0o0 )
elif IiI111111IIII == 3 : oOI1Ii1I1 ( i11 , I11 , Oo0o0000o0o0 )
elif IiI111111IIII == 4 : oo00oO0O0 ( i11 , I11 , Oo0o0000o0o0 )
elif IiI111111IIII == 5 : I1I1i1I ( )
elif IiI111111IIII == 6 : I1iI11Ii ( I11 , Oo0o0000o0o0 )
elif IiI111111IIII == 7 : OOOoOo ( I11 )
elif IiI111111IIII == 8 : iII1I1IiI11ii ( i11 )
elif IiI111111IIII == 9 : iIIIIi1iiIi1 ( i11 , I11 )
elif IiI111111IIII == 10 : DOSCRAPER ( i11 , I11 )
elif IiI111111IIII == 11 : Oo0O0 ( I11 )
elif IiI111111IIII == 12 : OooO0 ( i11 , I11 , Oo0o0000o0o0 )
elif IiI111111IIII == 13 : oOo0OOoO0 ( I11 )
elif IiI111111IIII == 14 : o0 ( i11 , I11 , Oo0o0000o0o0 )
elif IiI111111IIII == 15 : I1iiiiI1iII ( I11 )
elif IiI111111IIII == 16 : oOoooOOO ( i11 , I11 , Oo0o0000o0o0 )
elif IiI111111IIII == 17 : o0oo0oOo ( i11 , I11 )
elif IiI111111IIII == 18 : OOO ( i11 , I11 , Oo0o0000o0o0 )
elif IiI111111IIII == 19 : oO0OOoO0 ( i11 , I11 )
elif IiI111111IIII == 20 : OooO0OoOOOO ( I11 , Oo0o0000o0o0 )
if 97 - 97: O00 + o0o0OOO0o0 + O0 + i11iIiiIii
xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3
