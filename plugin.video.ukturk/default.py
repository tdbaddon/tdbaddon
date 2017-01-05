import xbmc , xbmcaddon , xbmcgui , xbmcplugin , urllib , urllib2 , os , re , sys , datetime , urlresolver , random , liveresolver , base64 , pyxbmct , glob
from resources . lib . common_addon import Addon
from HTMLParser import HTMLParser
from metahandler import metahandlers
if 64 - 64: i11iIiiIii
OO0o = 'plugin.video.ukturk'
Oo0Ooo = Addon ( OO0o , sys . argv )
O0O0OO0O0O0 = xbmcaddon . Addon ( id = OO0o )
iiiii = xbmc . translatePath ( 'special://home/addons/' ) + '/*.*'
ooo0OO = xbmc . translatePath ( 'special://home/addons/' )
II1 = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o , 'fanart.jpg' ) )
O00ooooo00 = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o , 'fanart.jpg' ) )
I1IiiI = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o , 'icon.png' ) )
IIi1IiiiI1Ii = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o + '/resources/art' , 'next.png' ) )
I11i11Ii = O0O0OO0O0O0 . getSetting ( 'adult' )
oO00oOo = O0O0OO0O0O0 . getSetting ( 'password' )
OOOo0 = int ( O0O0OO0O0O0 . getSetting ( 'count' ) )
Oooo000o = O0O0OO0O0O0 . getSetting ( 'enable_meta' )
IiIi11iIIi1Ii = xbmc . translatePath ( 'special://home/userdata/addon_data/' + OO0o )
Oo0O = xbmc . translatePath ( os . path . join ( 'special://home/userdata/Database' , 'UKTurk.db' ) )
IiI = 'http://ukturk.offshorepastebin.com/ukturk2.jpg'
ooOo = 'https://www.googleapis.com/youtube/v3/search?q='
Oo = '&regionCode=US&part=snippet&hl=en_US&key=AIzaSyAd-YEOqZz9nXVzGtn3KWzYLbLaajhqIDA&type=video&maxResults=50'
o0O = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId='
IiiIII111iI = '&maxResults=50&key=AIzaSyAd-YEOqZz9nXVzGtn3KWzYLbLaajhqIDA'
IiII = open ( Oo0O , 'a' )
IiII . close ( )
if 28 - 28: Ii11111i * iiI1i1
def i1I1ii1II1iII ( ) :
 O0O0OO0O0O0 . setSetting ( 'fav' , 'no' )
 if not os . path . exists ( IiIi11iIIi1Ii ) :
  os . mkdir ( IiIi11iIIi1Ii )
 oooO0oo0oOOOO = O0oO ( IiI )
 o0oO0 = re . compile ( '<index>(.+?)</index>' ) . findall ( oooO0oo0oOOOO ) [ 0 ]
 oooO0oo0oOOOO = O0oO ( o0oO0 )
 oo00 = re . compile ( 'name="(.+?)".+?rl="(.+?)".+?mg="(.+?)"' , re . DOTALL ) . findall ( oooO0oo0oOOOO )
 for o00 , Oo0oO0ooo , o0oOoO00o in oo00 :
  if not 'XXX' in o00 :
   i1 ( o00 , Oo0oO0ooo , 1 , o0oOoO00o , II1 )
  if 'XXX' in o00 :
   if I11i11Ii == 'true' :
    if oO00oOo == '' :
     oOOoo00O0O = xbmcgui . Dialog ( )
     i1111 = oOOoo00O0O . yesno ( 'Adult Content' , 'You have opted to show adult content' , '' , 'Please set a password to prevent accidental access' , 'Cancel' , 'Lets Go' )
     if i1111 == 1 :
      i11 = xbmc . Keyboard ( '' , 'Set Password' )
      i11 . doModal ( )
      if ( i11 . isConfirmed ( ) ) :
       I11 = i11 . getText ( )
       O0O0OO0O0O0 . setSetting ( 'password' , I11 )
      i1 ( o00 , Oo0oO0ooo , 1 , o0oOoO00o , II1 )
   if I11i11Ii == 'true' :
    if oO00oOo <> '' :
     i1 ( o00 , Oo0oO0ooo , 1 , o0oOoO00o , II1 )
 i1 ( 'Favourites' , Oo0O , 15 , 'http://ukturk.offshorepastebin.com/UKTurk/thumbs/new/Uk%20turk%20thumbnails%20favourites.jpg' , II1 )
 i1 ( 'Search' , 'url' , 5 , 'http://ukturk.offshorepastebin.com/UKTurk/thumbs/new/Uk%20turk%20thumbnails%20search.jpg' , II1 )
 xbmc . executebuiltin ( 'Container.SetViewMode(500)' )
 if 98 - 98: I1111 * o0o0Oo0oooo0 / I1I1i1 * oO0 / IIIi1i1I
def OOoOoo00oo ( url ) :
 O0O0OO0O0O0 . setSetting ( 'fav' , 'yes' )
 iiI11 = None
 file = open ( Oo0O , 'r' )
 iiI11 = file . read ( )
 oo00 = re . compile ( "<item>(.+?)</item>" , re . DOTALL ) . findall ( iiI11 )
 for OOooO in oo00 :
  OOoO00o = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>' , re . DOTALL ) . findall ( OOooO )
  for o00 , url , o0oOoO00o in OOoO00o :
   if '.txt' in url :
    i1 ( o00 , url , 1 , o0oOoO00o , II1 )
   else :
    II111iiii ( o00 , url , 2 , o0oOoO00o , II1 )
    if 48 - 48: I1Ii . IiIi1Iii1I1 - O0O0O0O00OooO % Ooooo % i1iIIIiI1I - OOoO000O0OO
def iiI1IiI ( name , url , iconimage ) :
 url = url . replace ( ' ' , '%20' )
 iconimage = iconimage . replace ( ' ' , '%20' )
 II = '<FAV><item>\n<title>' + name + '</title>\n<link>' + url + '</link>\n' + '<thumbnail>' + iconimage + '</thumbnail>\n</item></FAV>\n'
 IiII = open ( Oo0O , 'a' )
 IiII . write ( II )
 IiII . close ( )
 if 57 - 57: ooOoo0O
def OooO0 ( name , url , iconimage ) :
 iiI11 = None
 file = open ( Oo0O , 'r' )
 iiI11 = file . read ( )
 II11iiii1Ii = ''
 oo00 = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( iiI11 )
 for OOoO00o in oo00 :
  II = '\n<FAV><item>\n' + OOoO00o + '</item>\n'
  if name in OOoO00o :
   II = II . replace ( 'item' , ' ' )
  II11iiii1Ii = II11iiii1Ii + II
 file = open ( Oo0O , 'w' )
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
 if 'Index' in url :
  IIiiiiiiIi1I1 ( url )
 if 'XXX' in name : I1IIIii ( oooO0oo0oOOOO )
 oo00 = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( oooO0oo0oOOOO )
 OOOo0 = str ( len ( oo00 ) )
 O0O0OO0O0O0 . setSetting ( 'count' , OOOo0 )
 O0O0OO0O0O0 . setSetting ( 'fav' , 'no' )
 for OOooO in oo00 :
  try :
   if '<sportsdevil>' in OOooO : oOoOooOo0o0 ( OOooO , url )
   elif '<iptv>' in OOooO : OOOO ( OOooO )
   elif '<Image>' in OOooO : OOO00 ( OOooO )
   elif '<text>' in OOooO : iiiiiIIii ( OOooO )
   elif '<scraper>' in OOooO : SCRAPER ( OOooO )
   elif '<redirect>' in OOooO : REDIRECT ( OOooO )
   elif '<oktitle>' in OOooO : O000OO0 ( OOooO )
   elif '<dl>' in OOooO : I11iii1Ii ( OOooO )
   else : I1IIiiIiii ( OOooO , url , iconimage )
  except : pass
  if 97 - 97: ooOOOo0oo0O0 - OOoO000O0OO * i11iIiiIii / IiIi1Iii1I1 % o0o0OOO0o0 - I1111
def I11iii1Ii ( item ) :
 o00 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 Oo0oO0ooo = re . compile ( '<dl>(.+?)</dl>' ) . findall ( item ) [ 0 ]
 o0oOoO00o = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 OoOo00o ( o00 , Oo0oO0ooo , 19 , o0oOoO00o , II1 )
 if 70 - 70: i1I1i1Ii11 * Ooooo
def i1II1 ( name , url ) :
 OoO0O0 = url . split ( '/' ) [ - 1 ]
 if OoO0O0 == 'latest' : OoO0O0 = 'AceStreamEngine.apk'
 import downloader
 oOOoo00O0O = xbmcgui . Dialog ( )
 II1i1IiiIIi11 = xbmcgui . DialogProgress ( )
 iI1Ii11iII1 = oOOoo00O0O . browse ( 0 , 'Select folder to download to' , 'myprograms' )
 Oo0O0O0ooO0O = os . path . join ( iI1Ii11iII1 , OoO0O0 )
 II1i1IiiIIi11 . create ( 'Downloading' , '' , '' , 'Please Wait' )
 downloader . download ( url , Oo0O0O0ooO0O , II1i1IiiIIi11 )
 II1i1IiiIIi11 . close ( )
 oOOoo00O0O = xbmcgui . Dialog ( )
 oOOoo00O0O . ok ( 'Download complete' , 'Please install from..' , iI1Ii11iII1 )
 if 15 - 15: Ooooo + IiIi1Iii1I1 - I1111 / OOoO000O0OO
def O000OO0 ( item ) :
 o00 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 oo000OO00Oo = re . compile ( '<oktitle>(.+?)</oktitle>' ) . findall ( item ) [ 0 ]
 O0OOO0OOoO0O = re . compile ( '<line1>(.+?)</line1>' ) . findall ( item ) [ 0 ]
 O00Oo000ooO0 = re . compile ( '<line2>(.+?)</line2>' ) . findall ( item ) [ 0 ]
 OoO0O00 = re . compile ( '<line3>(.+?)</line3>' ) . findall ( item ) [ 0 ]
 IIiII = '##' + oo000OO00Oo + '#' + O0OOO0OOoO0O + '#' + O00Oo000ooO0 + '#' + OoO0O00 + '##'
 o0oOoO00o = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 OoOo00o ( o00 , IIiII , 17 , o0oOoO00o , II1 )
 if 80 - 80: IIIIII11i1I . i1iIIIiI1I
def IIi ( name , url ) :
 i11iIIIIIi1 = re . compile ( '##(.+?)##' ) . findall ( url ) [ 0 ] . split ( '#' )
 oOOoo00O0O = xbmcgui . Dialog ( )
 oOOoo00O0O . ok ( i11iIIIIIi1 [ 0 ] , i11iIIIIIi1 [ 1 ] , i11iIIIIIi1 [ 2 ] , i11iIIIIIi1 [ 3 ] )
 if 20 - 20: o0o0Oo0oooo0 + Ooooo - ooOOOo0oo0O0
def iiiiiIIii ( item ) :
 o00 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 IIiII = re . compile ( '<text>(.+?)</text>' ) . findall ( item ) [ 0 ]
 o0oOoO00o = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 OoOo00o ( o00 , IIiII , 9 , o0oOoO00o , II1 )
 if 30 - 30: I1I1i1 - OOoO000O0OO - i11iIiiIii % IiIi1Iii1I1 - I1I1i1 * O00
def oO00O0O0O ( name , url ) :
 i1ii1iiI = O0oO ( url )
 O0o0O00Oo0o0 ( name , i1ii1iiI )
 if 87 - 87: ooOOOo0oo0O0 * IIIi1i1I % i11iIiiIii % IiIi1Iii1I1 - OOoO000O0OO
def OOO00 ( item ) :
 O0ooo0O0oo0 = re . compile ( '<Image>(.+?)</Image>' ) . findall ( item )
 if len ( O0ooo0O0oo0 ) == 1 :
  o00 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  o0oOoO00o = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  oo0oOo = re . compile ( '<Image>(.+?)</Image>' ) . findall ( item ) [ 0 ]
  o0oOoO00o = oo0oOo . replace ( 'http://imgur.com/' , 'http://i.imgur.com/' ) + '.jpg'
  oo0oOo = oo0oOo . replace ( 'http://imgur.com/' , 'http://i.imgur.com/' ) + '.jpg'
  OoOo00o ( o00 , oo0oOo , 7 , o0oOoO00o , II1 )
 elif len ( O0ooo0O0oo0 ) > 1 :
  o00 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  o0oOoO00o = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  o000O0o = ''
  for oo0oOo in O0ooo0O0oo0 :
   o0oOoO00o = oo0oOo . replace ( 'http://imgur.com/' , 'http://i.imgur.com/' ) + '.jpg'
   oo0oOo = oo0oOo . replace ( 'http://imgur.com/' , 'http://i.imgur.com/' ) + '.jpg'
   o000O0o = o000O0o + '<Image>' + oo0oOo + '</Image>'
  iI1iII1 = IiIi11iIIi1Ii
  o00 = IIIII ( o00 )
  oO0OOoo0OO = os . path . join ( os . path . join ( iI1iII1 , '' ) , o00 + '.txt' )
  if not os . path . exists ( oO0OOoo0OO ) : file ( oO0OOoo0OO , 'w' ) . close ( )
  O0 = open ( oO0OOoo0OO , "w" )
  O0 . write ( o000O0o )
  O0 . close ( )
  OoOo00o ( o00 , 'image' , 8 , o0oOoO00o , II1 )
  if 25 - 25: Ooooo
def OOOO ( item ) :
 o00 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 o0oOoO00o = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 Oo0oO0ooo = re . compile ( '<iptv>(.+?)</iptv>' ) . findall ( item ) [ 0 ]
 i1 ( o00 , Oo0oO0ooo , 6 , o0oOoO00o , II1 )
 if 7 - 7: o0o0Oo0oooo0 / oO0 * o0o0OOO0o0 . IIIIII11i1I . iiI1i1
def iIii ( url , iconimage ) :
 oooO0oo0oOOOO = O0oO ( url )
 ooo0O = re . compile ( '^#.+?:-?[0-9]*(.*?),(.*?)\n(.*?)$' , re . I + re . M + re . U + re . S ) . findall ( oooO0oo0oOOOO )
 oOoO0o00OO0 = [ ]
 for i1I1ii , o00 , url in ooo0O :
  oOOo0 = { "params" : i1I1ii , "name" : o00 , "url" : url }
  oOoO0o00OO0 . append ( oOOo0 )
 list = [ ]
 for oo00O00oO in oOoO0o00OO0 :
  oOOo0 = { "name" : oo00O00oO [ "name" ] , "url" : oo00O00oO [ "url" ] }
  ooo0O = re . compile ( ' (.+?)="(.+?)"' , re . I + re . M + re . U + re . S ) . findall ( oo00O00oO [ "params" ] )
  for iIiIIIi , ooo00OOOooO in ooo0O :
   oOOo0 [ iIiIIIi . strip ( ) . lower ( ) . replace ( '-' , '_' ) ] = ooo00OOOooO . strip ( )
  list . append ( oOOo0 )
 for oo00O00oO in list :
  if '.ts' in oo00O00oO [ "url" ] : OoOo00o ( oo00O00oO [ "name" ] , oo00O00oO [ "url" ] , 2 , iconimage , II1 )
  else : II111iiii ( oo00O00oO [ "name" ] , oo00O00oO [ "url" ] , 2 , iconimage , II1 )
  if 67 - 67: ooOoo0O * i1iIIIiI1I * Ooooo + OOoO000O0OO / o0o0Oo0oooo0
def I1IIiiIiii ( item , url , iconimage ) :
 I1I111 = iconimage
 Oo00oo0oO = url
 IIiIi1iI = re . compile ( '<link>(.+?)</link>' ) . findall ( item )
 OOoO00o = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>' , re . DOTALL ) . findall ( item )
 for o00 , i1IiiiI1iI , iconimage in OOoO00o :
  if 'youtube.com/playlist?' in i1IiiiI1iI :
   i1iIi = i1IiiiI1iI . split ( 'list=' ) [ 1 ]
   i1 ( o00 , i1IiiiI1iI , ooOOoooooo , iconimage , II1 , description = i1iIi )
 if len ( IIiIi1iI ) == 1 :
  o00 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  url = re . compile ( '<link>(.+?)</link>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  if iconimage == 'ImageHere' : iconimage = I1I111
  if '.ts' in url : OoOo00o ( o00 , url , 16 , iconimage , II1 , description = '' )
  elif 'movies' in Oo00oo0oO :
   II1I ( o00 , url , 2 , iconimage , int ( OOOo0 ) , isFolder = False )
  else : II111iiii ( o00 , url , 2 , iconimage , II1 )
 elif len ( IIiIi1iI ) > 1 :
  o00 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  if iconimage == 'ImageHere' : iconimage = I1I111
  print iconimage
  if '.ts' in url : OoOo00o ( o00 , url , 16 , iconimage , II1 , description = '' )
  elif 'movies' in Oo00oo0oO :
   II1I ( o00 , url , 3 , iconimage , int ( OOOo0 ) , isFolder = False )
  else : II111iiii ( o00 , url , 3 , iconimage , II1 )
  if 84 - 84: IIIIII11i1I . i11iIiiIii . IIIIII11i1I * Ooooo - ooOoo0O
def IIiiiiiiIi1I1 ( url ) :
 oooO0oo0oOOOO = O0oO ( url )
 oo00 = re . compile ( 'name="(.+?)".+?rl="(.+?)".+?mg="(.+?)"' , re . DOTALL ) . findall ( oooO0oo0oOOOO )
 for o00 , url , I1IiiI in oo00 :
  if 'youtube.com/playlist?list=' in url :
   i1 ( o00 , url , 18 , I1IiiI , II1 )
  elif 'youtube.com/results?search_query=' in url :
   i1 ( o00 , url , 18 , I1IiiI , II1 )
  else :
   i1 ( o00 , url , 1 , I1IiiI , II1 )
   if 42 - 42: i11iIiiIii
def I11i1iIII ( name , url , iconimage ) :
 if 'youtube.com/results?search_query=' in url :
  i1iIi = url . split ( 'search_query=' ) [ 1 ]
  iiIiI = ooOo + i1iIi + Oo
  o00oooO0Oo = urllib2 . Request ( iiIiI )
  o00oooO0Oo . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' )
  o0O0OOO0Ooo = urllib2 . urlopen ( o00oooO0Oo )
  oooO0oo0oOOOO = o0O0OOO0Ooo . read ( )
  o0O0OOO0Ooo . close ( )
  oooO0oo0oOOOO = oooO0oo0oOOOO . replace ( '\r' , '' ) . replace ( '\n' , '' ) . replace ( '  ' , '' )
  oo00 = re . compile ( '"videoId": "(.+?)".+?"title": "(.+?)"' , re . DOTALL ) . findall ( oooO0oo0oOOOO )
  for iiIiII1 , name in oo00 :
   url = 'https://www.youtube.com/watch?v=' + iiIiII1
   iconimage = 'https://i.ytimg.com/vi/%s/hqdefault.jpg' % iiIiII1
   II111iiii ( name , url , 2 , iconimage , II1 )
 elif 'youtube.com/playlist?list=' in url :
  i1iIi = url . split ( 'playlist?list=' ) [ 1 ]
  iiIiI = o0O + i1iIi + IiiIII111iI
  o00oooO0Oo = urllib2 . Request ( iiIiI )
  o00oooO0Oo . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' )
  o0O0OOO0Ooo = urllib2 . urlopen ( o00oooO0Oo )
  oooO0oo0oOOOO = o0O0OOO0Ooo . read ( )
  o0O0OOO0Ooo . close ( )
  oooO0oo0oOOOO = oooO0oo0oOOOO . replace ( '\r' , '' ) . replace ( '\n' , '' ) . replace ( '  ' , '' )
  oo00 = re . compile ( '"title": "(.+?)".+?"videoId": "(.+?)"' , re . DOTALL ) . findall ( oooO0oo0oOOOO )
  for name , iiIiII1 in oo00 :
   url = 'https://www.youtube.com/watch?v=' + iiIiII1
   iconimage = 'https://i.ytimg.com/vi/%s/hqdefault.jpg' % iiIiII1
   II111iiii ( name , url , 2 , iconimage , II1 )
   if 86 - 86: IiIi1Iii1I1 - O00 - I1Ii * i1I1i1Ii11
def oooo0O0 ( item ) :
 item = item . replace ( '\r' , '' ) . replace ( '\t' , '' ) . replace ( '&nbsp;' , '' ) . replace ( '\'' , '' ) . replace ( '\n' , '' )
 OOoO00o = re . compile ( 'name="(.+?)".+?rl="(.+?)".+?mg="(.+?)"' , re . DOTALL ) . findall ( item )
 for o00 , Oo0oO0ooo , o0oOoO00o in OOoO00o :
  if 'youtube.com/channel/' in Oo0oO0ooo :
   i1iIi = Oo0oO0ooo . split ( 'channel/' ) [ 1 ]
   i1 ( o00 , Oo0oO0ooo , ooOOoooooo , o0oOoO00o , II1 , description = i1iIi )
  elif 'youtube.com/user/' in Oo0oO0ooo :
   i1iIi = Oo0oO0ooo . split ( 'user/' ) [ 1 ]
   i1 ( o00 , Oo0oO0ooo , ooOOoooooo , o0oOoO00o , II1 , description = i1iIi )
  elif 'youtube.com/playlist?' in Oo0oO0ooo :
   i1iIi = Oo0oO0ooo . split ( 'list=' ) [ 1 ]
   i1 ( o00 , Oo0oO0ooo , ooOOoooooo , o0oOoO00o , II1 , description = i1iIi )
  elif 'plugin://' in Oo0oO0ooo :
   oOOO = HTMLParser ( )
   Oo0oO0ooo = oOOO . unescape ( Oo0oO0ooo )
   i1 ( o00 , Oo0oO0ooo , ooOOoooooo , o0oOoO00o , II1 )
  else :
   i1 ( o00 , Oo0oO0ooo , 1 , o0oOoO00o , II1 )
   if 16 - 16: I1Ii / Ooooo + O00
def oOoOooOo0o0 ( item , url ) :
 IIiIi1iI = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( item )
 o0o = re . compile ( '<link>(.+?)</link>' ) . findall ( item )
 if len ( IIiIi1iI ) + len ( o0o ) == 1 :
  o00 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  o0oOoO00o = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  url = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( item ) [ 0 ]
  oooO0oo0oOOOO = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' + url
  OoOo00o ( o00 , url , 16 , o0oOoO00o , II1 )
 elif len ( IIiIi1iI ) + len ( o0o ) > 1 :
  o00 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  o0oOoO00o = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  OoOo00o ( o00 , url , 3 , o0oOoO00o , II1 )
  if 73 - 73: IIIIII11i1I * Ooooo + oO0 . ooOOOo0oo0O0
def I1IIIii ( link ) :
 if oO00oOo == '' :
  oOOoo00O0O = xbmcgui . Dialog ( )
  i1111 = oOOoo00O0O . yesno ( 'Adult Content' , 'You have opted to show adult content' , '' , 'Please set a password to prevent accidental access' , 'Cancel' , 'OK' )
  if i1111 == 1 :
   i11 = xbmc . Keyboard ( '' , 'Set Password' )
   i11 . doModal ( )
   if ( i11 . isConfirmed ( ) ) :
    I11 = i11 . getText ( )
    O0O0OO0O0O0 . setSetting ( 'password' , I11 )
  else : quit ( )
 elif oO00oOo <> '' :
  oOOoo00O0O = xbmcgui . Dialog ( )
  i1111 = oOOoo00O0O . yesno ( 'Adult Content' , 'Please enter the password you set' , 'to continue' , '' , 'Cancel' , 'OK' )
  if i1111 == 1 :
   i11 = xbmc . Keyboard ( '' , 'Enter Password' )
   i11 . doModal ( )
   if ( i11 . isConfirmed ( ) ) :
    I11 = i11 . getText ( )
   if I11 <> oO00oOo :
    quit ( )
  else : quit ( )
  if 70 - 70: o0o0OOO0o0 - IIIi1i1I / O00
def O00OOOOOoo0 ( ) :
 i11 = xbmc . Keyboard ( '' , 'Search' )
 i11 . doModal ( )
 if ( i11 . isConfirmed ( ) ) :
  i1iIi = i11 . getText ( )
  i1iIi = i1iIi . upper ( )
 else : quit ( )
 oooO0oo0oOOOO = O0oO ( IiI )
 ii1 = re . compile ( '<link>(.+?)</link>' ) . findall ( oooO0oo0oOOOO )
 for Oo0oO0ooo in ii1 :
  try :
   oooO0oo0oOOOO = O0oO ( Oo0oO0ooo )
   I1iI1iIi111i = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( oooO0oo0oOOOO )
   for OOooO in I1iI1iIi111i :
    oo00 = re . compile ( '<title>(.+?)</title>' ) . findall ( OOooO )
    for iiIi1IIi1I in oo00 :
     iiIi1IIi1I = iiIi1IIi1I . upper ( )
     if i1iIi in iiIi1IIi1I :
      try :
       if 'Index' in Oo0oO0ooo : IIiiiiiiIi1I1 ( Oo0oO0ooo )
       elif '<sportsdevil>' in OOooO : oOoOooOo0o0 ( OOooO , Oo0oO0ooo )
       elif '<iptv>' in OOooO : OOOO ( OOooO )
       elif '<Image>' in OOooO : OOO00 ( OOooO )
       elif '<text>' in OOooO : iiiiiIIii ( OOooO )
       elif '<scraper>' in OOooO : SCRAPER ( OOooO )
       elif '<redirect>' in OOooO : REDIRECT ( OOooO )
       elif '<oktitle>' in OOooO : O000OO0 ( OOooO )
       else : I1IIiiIiii ( OOooO , Oo0oO0ooo , o0oOoO00o )
      except : pass
  except : pass
  if 84 - 84: ooOOOo0oo0O0 * I1I1i1 + IIIi1i1I
def O0ooO0Oo00o ( name , url , iconimage ) :
 I1I111 = iconimage
 ooO0oOOooOo0 = [ ]
 i1I1ii11i1Iii = [ ]
 I1IiiiiI = [ ]
 oooO0oo0oOOOO = O0oO ( url )
 o0OIiII = re . compile ( '<title>' + re . escape ( name ) + '</title>(.+?)</item>' , re . DOTALL ) . findall ( oooO0oo0oOOOO ) [ 0 ]
 IIiIi1iI = [ ]
 if '<link>' in o0OIiII :
  ii1iII1II = re . compile ( '<link>(.+?)</link>' ) . findall ( o0OIiII )
  for Iii1I1I11iiI1 in ii1iII1II :
   IIiIi1iI . append ( Iii1I1I11iiI1 )
 if '<sportsdevil>' in o0OIiII :
  I1I1i1I = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( o0OIiII )
  for ii1I in I1I1i1I :
   ii1I = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' + ii1I
   IIiIi1iI . append ( ii1I )
 O0oO0 = 1
 for oO0O0OO0O in IIiIi1iI :
  OO = oO0O0OO0O
  if 'acestream://' in oO0O0OO0O or '.acelive' in oO0O0OO0O or 'sop://' in oO0O0OO0O : OoOoO = ' (Acestreams)'
  else : OoOoO = ''
  if '(' in oO0O0OO0O :
   oO0O0OO0O = oO0O0OO0O . split ( '(' ) [ 0 ]
   Ii1I1i = str ( OO . split ( '(' ) [ 1 ] . replace ( ')' , '' ) + OoOoO )
   ooO0oOOooOo0 . append ( oO0O0OO0O )
   i1I1ii11i1Iii . append ( Ii1I1i )
  else :
   OOI1iI1ii1II = oO0O0OO0O . split ( '/' ) [ 2 ] . replace ( 'www.' , '' )
   ooO0oOOooOo0 . append ( oO0O0OO0O )
   i1I1ii11i1Iii . append ( 'Link ' + str ( O0oO0 ) + OoOoO )
  O0oO0 = O0oO0 + 1
 oOOoo00O0O = xbmcgui . Dialog ( )
 O0O0OOOOoo = oOOoo00O0O . select ( 'Choose a link..' , i1I1ii11i1Iii )
 if O0O0OOOOoo < 0 : quit ( )
 else :
  url = ooO0oOOooOo0 [ O0O0OOOOoo ]
  oOooO0 ( name , url , iconimage )
  if 29 - 29: iiI1i1 + IiIi1Iii1I1 * I1Ii * OOoO000O0OO . oO0 * oO0
def I111I1Iiii1i ( url ) :
 II = "ShowPicture(%s)" % url
 xbmc . executebuiltin ( II )
 if 56 - 56: Ooooo % Ii11111i - oO0
def oOooO0 ( name , url , iconimage ) :
 try :
  if 'sop://' in url :
   url = urllib . quote ( url )
   url = 'plugin://program.plexus/?mode=2&url=%s&name=%s' % ( url , name . replace ( ' ' , '+' ) )
   O00o0OO0 ( name , url , iconimage )
  elif 'acestream://' in url or '.acelive' in url :
   url = urllib . quote ( url )
   url = 'plugin://program.plexus/?mode=1&url=%s&name=%s' % ( url , name . replace ( ' ' , '+' ) )
   O00o0OO0 ( name , url , iconimage )
  elif 'plugin://plugin.video.SportsDevil/' in url :
   O00o0OO0 ( name , url , iconimage )
  elif '.ts' in url :
   url = 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;name=' + name + '&amp;url=' + url
   O00o0OO0 ( name , url , iconimage )
  elif urlresolver . HostedMediaFile ( url ) . valid_url ( ) :
   url = urlresolver . HostedMediaFile ( url ) . resolve ( )
   IIi1I1iiiii ( name , url , iconimage )
  elif liveresolver . isValid ( url ) == True :
   url = liveresolver . resolve ( url )
   IIi1I1iiiii ( name , url , iconimage )
  else : IIi1I1iiiii ( name , url , iconimage )
 except :
  o00oOOooOOo0o ( 'UKTurk' , 'Stream Unavailable' , '3000' , I1IiiI )
  if 66 - 66: i1I1i1Ii11 - i1I1i1Ii11 - i11iIiiIii . Ooooo - OOoO000O0OO
def oOOo0O00o ( url ) :
 if urlresolver . HostedMediaFile ( url ) . valid_url ( ) :
  url = urlresolver . HostedMediaFile ( url ) . resolve ( )
 xbmc . Player ( ) . play ( url )
 if 8 - 8: I1Ii
def IIi1I1iiiii ( name , url , iconimage ) :
 ii1111iII = True
 iiiiI = xbmcgui . ListItem ( name , iconImage = iconimage , thumbnailImage = iconimage ) ; iiiiI . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
 ii1111iII = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = url , listitem = iiiiI )
 iiiiI . setPath ( url )
 xbmcplugin . setResolvedUrl ( int ( sys . argv [ 1 ] ) , True , iiiiI )
 if 62 - 62: I1111 * oO0
def O00o0OO0 ( name , url , iconimage ) :
 ii1111iII = True
 iiiiI = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage ) ; iiiiI . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
 ii1111iII = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = url , listitem = iiiiI )
 oOOoo00O0O = xbmcgui . Dialog ( )
 xbmc . Player ( ) . play ( url , iiiiI , False )
 if 58 - 58: IiIi1Iii1I1 % O0O0O0O00OooO
def i1OOoO ( url ) :
 xbmc . executebuiltin ( "PlayMedia(%s)" % url )
 if 89 - 89: O0O0O0O00OooO + I1Ii * ooOoo0O * O00
def iiIiI1i1 ( url ) :
 oO0O00oOOoooO = O0O0OO0O0O0 . getSetting ( 'layout' )
 if oO0O00oOOoooO == 'Listers' : O0O0OO0O0O0 . setSetting ( 'layout' , 'Category' )
 else : O0O0OO0O0O0 . setSetting ( 'layout' , 'Listers' )
 xbmc . executebuiltin ( 'Container.Refresh' )
 if 46 - 46: oO0 - I1111 - ooOoo0O * I1I1i1
def O0oO ( url ) :
 o00oooO0Oo = urllib2 . Request ( url )
 o00oooO0Oo . add_header ( 'User-Agent' , 'mat' )
 o0O0OOO0Ooo = urllib2 . urlopen ( o00oooO0Oo )
 oooO0oo0oOOOO = o0O0OOO0Ooo . read ( )
 o0O0OOO0Ooo . close ( )
 oooO0oo0oOOOO = oooO0oo0oOOOO . replace ( '</fanart>' , '<fanart>x</fanart>' ) . replace ( '<thumbnail></thumbnail>' , '<thumbnail>x</thumbnail>' ) . replace ( '<utube>' , '<link>https://www.youtube.com/watch?v=' ) . replace ( '</utube>' , '</link>' )
 if '{' in oooO0oo0oOOOO : oooO0oo0oOOOO = I1i1I11I ( oooO0oo0oOOOO )
 return oooO0oo0oOOOO
 if 80 - 80: i11iIiiIii % ooOOOo0oo0O0 + O00 % ooOoo0O - Ooooo
def I1i1i1iii ( ) :
 I1111i = [ ]
 iIIii = sys . argv [ 2 ]
 if len ( iIIii ) >= 2 :
  i1I1ii = sys . argv [ 2 ]
  o00O0O = i1I1ii . replace ( '?' , '' )
  if ( i1I1ii [ len ( i1I1ii ) - 1 ] == '/' ) :
   i1I1ii = i1I1ii [ 0 : len ( i1I1ii ) - 2 ]
  ii1iii1i = o00O0O . split ( '&' )
  I1111i = { }
  for O0oO0 in range ( len ( ii1iii1i ) ) :
   Iii1I1111ii = { }
   Iii1I1111ii = ii1iii1i [ O0oO0 ] . split ( '=' )
   if ( len ( Iii1I1111ii ) ) == 2 :
    I1111i [ Iii1I1111ii [ 0 ] ] = Iii1I1111ii [ 1 ]
 return I1111i
 if 72 - 72: I1I1i1 + o0o0Oo0oooo0 + O0O0O0O00OooO
def o00oOOooOOo0o ( title , message , ms , nart ) :
 xbmc . executebuiltin ( "XBMC.notification(" + title + "," + message + "," + ms + "," + nart + ")" )
 if 94 - 94: i1iIIIiI1I . o0o0Oo0oooo0 - O0O0O0O00OooO % Ii11111i - I1Ii
def IIIII ( string ) :
 ooO0O00Oo0o = re . compile ( '\[(.+?)\]' ) . findall ( string )
 for OOO in ooO0O00Oo0o : string = string . replace ( OOO , '' ) . replace ( '[/]' , '' ) . replace ( '[]' , '' )
 return string
 if 73 - 73: I1111 * I1111 * ooOOOo0oo0O0 * IiIi1Iii1I1 + ooOOOo0oo0O0 * o0o0OOO0o0
def oo0o0OO0 ( string ) :
 string = string . split ( ' ' )
 oooO = ''
 for i1I1i111Ii in string :
  ooo = '[B][COLOR red]' + i1I1i111Ii [ 0 ] . upper ( ) + '[/COLOR][COLOR white]' + i1I1i111Ii [ 1 : ] + '[/COLOR][/B] '
  oooO = oooO + ooo
 return oooO
 if 27 - 27: ooOOOo0oo0O0 % oO0
def II1I ( name , url , mode , iconimage , itemcount , isFolder = False ) :
 if Oooo000o == 'true' :
  if not 'COLOR' in name :
   o0oooOO00 = name . partition ( '(' )
   iiIiii1IIIII = ""
   o00o = ""
   if len ( o0oooOO00 ) > 0 :
    iiIiii1IIIII = o0oooOO00 [ 0 ]
    o00o = o0oooOO00 [ 2 ] . partition ( ')' )
   if len ( o00o ) > 0 :
    o00o = o00o [ 0 ]
   IIIIiiIiiI = eval ( base64 . b64decode ( 'bWV0YWhhbmRsZXJzLk1ldGFEYXRhKHRtZGJfYXBpX2tleT0iZDk1NWQ4ZjAyYTNmMjQ4MGE1MTg4MWZlNGM5NmYxMGUiKQ==' ) )
   IIIIiI11I11 = IIIIiiIiiI . get_meta ( 'movie' , name = iiIiii1IIIII , year = o00o )
   oo00o0 = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&site=" + str ( i11II1I11I1 ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name )
   ii1111iII = True
   iiiiI = xbmcgui . ListItem ( name , iconImage = IIIIiI11I11 [ 'cover_url' ] , thumbnailImage = IIIIiI11I11 [ 'cover_url' ] )
   iiiiI . setInfo ( type = "Video" , infoLabels = IIIIiI11I11 )
   iiiiI . setProperty ( "IsPlayable" , "true" )
   OOoOO0ooo = [ ]
   if O0O0OO0O0O0 . getSetting ( 'fav' ) == 'yes' : OOoOO0ooo . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
   if O0O0OO0O0O0 . getSetting ( 'fav' ) == 'no' : OOoOO0ooo . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
   iiiiI . addContextMenuItems ( OOoOO0ooo , replaceItems = False )
   if not IIIIiI11I11 [ 'backdrop_url' ] == '' : iiiiI . setProperty ( 'fanart_image' , IIIIiI11I11 [ 'backdrop_url' ] )
   else : iiiiI . setProperty ( 'fanart_image' , II1 )
   ii1111iII = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = oo00o0 , listitem = iiiiI , isFolder = isFolder , totalItems = itemcount )
   return ii1111iII
 else :
  oo00o0 = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&site=" + str ( i11II1I11I1 ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name )
  ii1111iII = True
  iiiiI = xbmcgui . ListItem ( name , iconImage = iconimage , thumbnailImage = iconimage )
  iiiiI . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
  iiiiI . setProperty ( 'fanart_image' , II1 )
  iiiiI . setProperty ( "IsPlayable" , "true" )
  OOoOO0ooo = [ ]
  if O0O0OO0O0O0 . getSetting ( 'fav' ) == 'yes' : OOoOO0ooo . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
  if O0O0OO0O0O0 . getSetting ( 'fav' ) == 'no' : OOoOO0ooo . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
  iiiiI . addContextMenuItems ( OOoOO0ooo , replaceItems = False )
  ii1111iII = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = oo00o0 , listitem = iiiiI , isFolder = isFolder )
  return ii1111iII
  if 30 - 30: O0O0O0O00OooO - o0o0Oo0oooo0 % I1I1i1 + ooOoo0O * iiI1i1
def i1 ( name , url , mode , iconimage , fanart , description = '' ) :
 oo00o0 = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&fanart=" + urllib . quote_plus ( fanart ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 ii1111iII = True
 iiiiI = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 iiiiI . setInfo ( type = "Video" , infoLabels = { "Title" : name , 'plot' : description } )
 iiiiI . setProperty ( 'fanart_image' , fanart )
 OOoOO0ooo = [ ]
 if O0O0OO0O0O0 . getSetting ( 'fav' ) == 'yes' : OOoOO0ooo . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 if O0O0OO0O0O0 . getSetting ( 'fav' ) == 'no' : OOoOO0ooo . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 iiiiI . addContextMenuItems ( OOoOO0ooo , replaceItems = False )
 if 'plugin://' in url :
  oo00o0 = url
 ii1111iII = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = oo00o0 , listitem = iiiiI , isFolder = True )
 return ii1111iII
 if 81 - 81: IIIIII11i1I % o0o0Oo0oooo0 . iiI1i1
def OoOo00o ( name , url , mode , iconimage , fanart , description = '' ) :
 oo00o0 = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 ii1111iII = True
 iiiiI = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 iiiiI . setProperty ( 'fanart_image' , fanart )
 OOoOO0ooo = [ ]
 if O0O0OO0O0O0 . getSetting ( 'fav' ) == 'yes' : OOoOO0ooo . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 if O0O0OO0O0O0 . getSetting ( 'fav' ) == 'no' : OOoOO0ooo . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 iiiiI . addContextMenuItems ( OOoOO0ooo , replaceItems = False )
 ii1111iII = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = oo00o0 , listitem = iiiiI , isFolder = False )
 return ii1111iII
 if 4 - 4: i11iIiiIii % I1Ii % o0o0Oo0oooo0 / IIIIII11i1I
def II111iiii ( name , url , mode , iconimage , fanart , description = '' ) :
 oo00o0 = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 ii1111iII = True
 iiiiI = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 iiiiI . setProperty ( 'fanart_image' , fanart )
 iiiiI . setProperty ( "IsPlayable" , "true" )
 OOoOO0ooo = [ ]
 if O0O0OO0O0O0 . getSetting ( 'fav' ) == 'yes' : OOoOO0ooo . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 if O0O0OO0O0O0 . getSetting ( 'fav' ) == 'no' : OOoOO0ooo . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 iiiiI . addContextMenuItems ( OOoOO0ooo , replaceItems = False )
 ii1111iII = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = oo00o0 , listitem = iiiiI , isFolder = False )
 return ii1111iII
 if 6 - 6: i1I1i1Ii11 / oO0 % OOoO000O0OO - oO0
def iiii111II ( url , name ) :
 I11iIiI1I1i11 = O0oO ( url )
 if len ( I11iIiI1I1i11 ) > 1 :
  iI1iII1 = IiIi11iIIi1Ii
  oO0OOoo0OO = os . path . join ( os . path . join ( iI1iII1 , '' ) , name + '.txt' )
  if not os . path . exists ( oO0OOoo0OO ) :
   file ( oO0OOoo0OO , 'w' ) . close ( )
  OOoooO00o0oo0 = open ( oO0OOoo0OO )
  O00O = OOoooO00o0oo0 . read ( )
  if O00O == I11iIiI1I1i11 : pass
  else :
   O0o0O00Oo0o0 ( 'UKTurk' , I11iIiI1I1i11 )
   O0 = open ( oO0OOoo0OO , "w" )
   O0 . write ( I11iIiI1I1i11 )
   O0 . close ( )
   if 48 - 48: ooOOOo0oo0O0 / o0o0OOO0o0 . iiI1i1 * IiIi1Iii1I1 * i1iIIIiI1I / o0o0Oo0oooo0
def O0o0O00Oo0o0 ( heading , text ) :
 id = 10147
 xbmc . executebuiltin ( 'ActivateWindow(%d)' % id )
 xbmc . sleep ( 500 )
 OOOOoOOo0O0 = xbmcgui . Window ( id )
 oOooo0 = 50
 while ( oOooo0 > 0 ) :
  try :
   xbmc . sleep ( 10 )
   oOooo0 -= 1
   OOOOoOOo0O0 . getControl ( 1 ) . setLabel ( heading )
   OOOOoOOo0O0 . getControl ( 5 ) . setText ( text )
   return
  except :
   pass
   if 58 - 58: oO0 . i1I1i1Ii11 + IiIi1Iii1I1
def O00OO ( name ) :
 global Icon
 global Next
 global Previous
 global window
 global Quit
 global images
 oO0OOoo0OO = os . path . join ( os . path . join ( IiIi11iIIi1Ii , '' ) , name + '.txt' )
 OOoooO00o0oo0 = open ( oO0OOoo0OO )
 O00O = OOoooO00o0oo0 . read ( )
 images = re . compile ( '<image>(.+?)</image>' ) . findall ( O00O )
 O0O0OO0O0O0 . setSetting ( 'pos' , '0' )
 window = pyxbmct . AddonDialogWindow ( '' )
 I1I1 = '/resources/art'
 OoO0O0o0oOOO = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o + I1I1 , 'next_focus.png' ) )
 OOoOoOo = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o + I1I1 , 'next1.png' ) )
 o000ooooO0o = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o + I1I1 , 'previous_focus.png' ) )
 iI1i11 = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o + I1I1 , 'previous.png' ) )
 OoOOoooOO0O = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o + I1I1 , 'close_focus.png' ) )
 ooo00Ooo = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o + I1I1 , 'close.png' ) )
 Oo0o0O00 = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o + I1I1 , 'main-bg1.png' ) )
 window . setGeometry ( 1300 , 720 , 100 , 50 )
 ii1I1i11 = pyxbmct . Image ( Oo0o0O00 )
 window . placeControl ( ii1I1i11 , - 10 , - 10 , 130 , 70 )
 IIiII = '0xFF000000'
 Previous = pyxbmct . Button ( '' , focusTexture = o000ooooO0o , noFocusTexture = iI1i11 , textColor = IIiII , focusedColor = IIiII )
 Next = pyxbmct . Button ( '' , focusTexture = OoO0O0o0oOOO , noFocusTexture = OOoOoOo , textColor = IIiII , focusedColor = IIiII )
 Quit = pyxbmct . Button ( '' , focusTexture = OoOOoooOO0O , noFocusTexture = ooo00Ooo , textColor = IIiII , focusedColor = IIiII )
 Icon = pyxbmct . Image ( images [ 0 ] , aspectRatio = 1 )
 window . placeControl ( Previous , 102 , 1 , 10 , 10 )
 window . placeControl ( Next , 102 , 40 , 10 , 10 )
 window . placeControl ( Quit , 102 , 21 , 10 , 10 )
 window . placeControl ( Icon , 0 , 0 , 100 , 50 )
 Previous . controlRight ( Next )
 Previous . controlUp ( Quit )
 window . connect ( Previous , OOo0O0oo0OO0O )
 window . connect ( Next , OO0 )
 Previous . setVisible ( False )
 window . setFocus ( Quit )
 Previous . controlRight ( Quit )
 Quit . controlLeft ( Previous )
 Quit . controlRight ( Next )
 Next . controlLeft ( Quit )
 window . connect ( Quit , window . close )
 window . doModal ( )
 del window
 if 72 - 72: I1111
def OO0 ( ) :
 OooooOoooO = int ( O0O0OO0O0O0 . getSetting ( 'pos' ) )
 oO = int ( OooooOoooO ) + 1
 O0O0OO0O0O0 . setSetting ( 'pos' , str ( oO ) )
 IIiIi = len ( images )
 Icon . setImage ( images [ int ( oO ) ] )
 Previous . setVisible ( True )
 if int ( oO ) == int ( IIiIi ) - 1 :
  Next . setVisible ( False )
  if 91 - 91: Ooooo * IIIi1i1I / oO0 . Ii11111i + I1Ii + IiIi1Iii1I1
def OOo0O0oo0OO0O ( ) :
 OooooOoooO = int ( O0O0OO0O0O0 . getSetting ( 'pos' ) )
 iIIi = int ( OooooOoooO ) - 1
 O0O0OO0O0O0 . setSetting ( 'pos' , str ( iIIi ) )
 Icon . setImage ( images [ int ( iIIi ) ] )
 Next . setVisible ( True )
 if int ( iIIi ) == 0 :
  Previous . setVisible ( False )
  if 11 - 11: oO0 * i1iIIIiI1I
def I1i1I11I ( gobble ) :
 gobble = gobble . replace ( '}' , '' ) . replace ( '{' , '' ) . replace ( ',' , '' ) . replace ( ']' , '' ) . replace ( '[' , '' )
 gobble = gobble + '=='
 gobble = gobble . decode ( 'base64' )
 return gobble
 if 81 - 81: i1I1i1Ii11 + IIIIII11i1I
def ooooooO0oo ( link ) :
 try :
  o0oo0 = re . compile ( '<layouttype>(.+?)</layouttype>' ) . findall ( link ) [ 0 ]
  if o0oo0 == 'thumbnail' : xbmc . executebuiltin ( 'Container.SetViewMode(500)' )
  else : xbmc . executebuiltin ( 'Container.SetViewMode(50)' )
 except : pass
 if 97 - 97: IiIi1Iii1I1 % Ooooo
i1I1ii = I1i1i1iii ( ) ; Oo0oO0ooo = None ; o00 = None ; ooOOoooooo = None ; i11II1I11I1 = None ; o0oOoO00o = None
try : i11II1I11I1 = urllib . unquote_plus ( i1I1ii [ "site" ] )
except : pass
try : Oo0oO0ooo = urllib . unquote_plus ( i1I1ii [ "url" ] )
except : pass
try : o00 = urllib . unquote_plus ( i1I1ii [ "name" ] )
except : pass
try : ooOOoooooo = int ( i1I1ii [ "mode" ] )
except : pass
try : o0oOoO00o = urllib . unquote_plus ( i1I1ii [ "iconimage" ] )
except : pass
try : II1 = urllib . unquote_plus ( i1I1ii [ "fanart" ] )
except : pass
if 25 - 25: IIIi1i1I % Ooooo . Ooooo
try : O0O0Oo00 = urllib . unquote_plus ( [ "description" ] )
except : pass
if 80 - 80: i1iIIIiI1I + OOoO000O0OO / ooOoo0O
if ooOOoooooo == None or Oo0oO0ooo == None or len ( Oo0oO0ooo ) < 1 : i1I1ii1II1iII ( )
elif ooOOoooooo == 1 : o0 ( o00 , Oo0oO0ooo , o0oOoO00o , II1 )
elif ooOOoooooo == 2 : oOooO0 ( o00 , Oo0oO0ooo , o0oOoO00o )
elif ooOOoooooo == 3 : O0ooO0Oo00o ( o00 , Oo0oO0ooo , o0oOoO00o )
elif ooOOoooooo == 4 : IIi1I1iiiii ( o00 , Oo0oO0ooo , o0oOoO00o )
elif ooOOoooooo == 5 : O00OOOOOoo0 ( )
elif ooOOoooooo == 6 : iIii ( Oo0oO0ooo , o0oOoO00o )
elif ooOOoooooo == 7 : I111I1Iiii1i ( Oo0oO0ooo )
elif ooOOoooooo == 8 : O00OO ( o00 )
elif ooOOoooooo == 9 : oO00O0O0O ( o00 , Oo0oO0ooo )
elif ooOOoooooo == 10 : DOSCRAPER ( o00 , Oo0oO0ooo )
elif ooOOoooooo == 11 : i1OOoO ( Oo0oO0ooo )
elif ooOOoooooo == 12 : iiI1IiI ( o00 , Oo0oO0ooo , o0oOoO00o )
elif ooOOoooooo == 13 : iiIiI1i1 ( Oo0oO0ooo )
elif ooOOoooooo == 14 : OooO0 ( o00 , Oo0oO0ooo , o0oOoO00o )
elif ooOOoooooo == 15 : OOoOoo00oo ( Oo0oO0ooo )
elif ooOOoooooo == 16 : O00o0OO0 ( o00 , Oo0oO0ooo , o0oOoO00o )
elif ooOOoooooo == 17 : IIi ( o00 , Oo0oO0ooo )
elif ooOOoooooo == 18 : I11i1iIII ( o00 , Oo0oO0ooo , o0oOoO00o )
elif ooOOoooooo == 19 : i1II1 ( o00 , Oo0oO0ooo )
if 79 - 79: ooOOOo0oo0O0
xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3
