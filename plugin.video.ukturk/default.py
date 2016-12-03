import xbmc , xbmcaddon , xbmcgui , xbmcplugin , urllib , urllib2 , os , re , sys , datetime , urlresolver , random , liveresolver , base64 , pyxbmct , glob
from resources . lib . common_addon import Addon
from HTMLParser import HTMLParser
from metahandler import metahandlers
if 64 - 64: i11iIiiIii
KKmkm = 'plugin.video.ukturk'
KmmkKmm = Addon ( KKmkm , sys . argv )
KmkKmkKKmkKmkKmk = xbmcaddon . Addon ( id = KKmkm )
iiiii = xbmc . translatePath ( 'special://home/addons/' ) + '/*.*'
mmmmkKK = xbmc . translatePath ( 'special://home/addons/' )
II1 = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + KKmkm , 'fanart.jpg' ) )
Kmkmkmmmmmmkmk = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + KKmkm , 'fanart.jpg' ) )
I1IiiI = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + KKmkm , 'icon.png' ) )
IIi1IiiiI1Ii = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + KKmkm + '/resources/art' , 'next.png' ) )
I11i11Ii = KmkKmkKKmkKmkKmk . getSetting ( 'adult' )
mKmkmkmKm = KmkKmkKKmkKmkKmk . getSetting ( 'password' )
KKKmmk = int ( KmkKmkKKmkKmkKmk . getSetting ( 'count' ) )
Kmmmmkmkmkm = KmkKmkKKmkKmkKmk . getSetting ( 'enable_meta' )
IiIi11iIIi1Ii = xbmc . translatePath ( 'special://home/userdata/addon_data/' + KKmkm )
KmmkK = xbmc . translatePath ( os . path . join ( 'special://home/userdata/Database' , 'UKTurk.db' ) )
IiI = 'http://ukturk.offshorepastebin.com/ukturk2.jpg'
mmKm = open ( KmmkK , 'a' )
mmKm . close ( )
if 91 - 91: Ii1I . KmKK + KmKKmkmmKKmmmkK + mmkmkmkmkmKmKmKmkm * i1I1ii1II1iII % mmmKmkmmmkmKKKK
def KmkmK ( ) :
 KmkKmkKKmkKmkKmk . setSetting ( 'fav' , 'no' )
 if not os . path . exists ( IiIi11iIIi1Ii ) :
  os . mkdir ( IiIi11iIIi1Ii )
 mmkmKmk = mmmkmk ( IiI )
 mmkmk = re . compile ( '<index>(.+?)</index>' ) . findall ( mmkmKmk ) [ 0 ]
 mmkmKmk = mmmkmk ( mmkmk )
 KmmkmKmkmmm = re . compile ( 'name="(.+?)".+?rl="(.+?)".+?mg="(.+?)"' , re . DOTALL ) . findall ( mmkmKmk )
 for mmkmKmKmkmkm , i1 , mKKmmmkmkKmkK in KmmkmKmkmmm :
  if not 'XXX' in mmkmKmKmkmkm :
   i1111 ( mmkmKmKmkmkm , i1 , 1 , mKKmmmkmkKmkK , II1 )
  if 'XXX' in mmkmKmKmkmkm :
   if I11i11Ii == 'true' :
    if mKmkmkmKm == '' :
     i11 = xbmcgui . Dialog ( )
     I11 = i11 . yesno ( 'Adult Content' , 'You have opted to show adult content' , '' , 'Please set a password to prevent accidental access' , 'Cancel' , 'Lets Go' )
     if I11 == 1 :
      Kmmkmmkmkmkmkmmkmmk = xbmc . Keyboard ( '' , 'Set Password' )
      Kmmkmmkmkmkmkmmkmmk . doModal ( )
      if ( Kmmkmmkmkmkmkmmkmmk . isConfirmed ( ) ) :
       mKmmkmmmmmkmkm = Kmmkmmkmkmkmkmmkmmk . getText ( )
       KmkKmkKKmkKmkKmk . setSetting ( 'password' , mKmmkmmmmmkmkm )
      i1111 ( mmkmKmKmkmkm , i1 , 1 , mKKmmmkmkKmkK , II1 )
   if I11i11Ii == 'true' :
    if mKmkmkmKm <> '' :
     i1111 ( mmkmKmKmkmkm , i1 , 1 , mKKmmmkmkKmkK , II1 )
 i1111 ( 'Favourites' , KmmkK , 15 , 'http://ukturk.offshorepastebin.com/UKTurk/thumbs/new/Uk%20turk%20thumbnails%20favourites.jpg' , II1 )
 i1111 ( 'Search' , 'url' , 5 , 'http://ukturk.offshorepastebin.com/UKTurk/thumbs/new/Uk%20turk%20thumbnails%20search.jpg' , II1 )
 xbmc . executebuiltin ( 'Container.SetViewMode(500)' )
 if 65 - 65: Kmkm * i1iIIII * I1
def KmkKmKmmmkmkm ( url ) :
 KmkKmkKKmkKmkKmk . setSetting ( 'fav' , 'yes' )
 iiiI11 = None
 file = open ( KmmkK , 'r' )
 iiiI11 = file . read ( )
 KmmkmKmkmmm = re . compile ( "<item>(.+?)</item>" , re . DOTALL ) . findall ( iiiI11 )
 for KKmmK in KmmkmKmkmmm :
  KKmKmkmkm = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>' , re . DOTALL ) . findall ( KKmmK )
  for mmkmKmKmkmkm , url , mKKmmmkmkKmkK in KKmKmkmkm :
   if '.txt' in url :
    i1111 ( mmkmKmKmkmkm , url , 1 , mKKmmmkmkKmkK , II1 )
   else :
    II111iiii ( mmkmKmKmkmkm , url , 2 , mKKmmmkmkKmkK , II1 )
    if 48 - 48: I1Ii . IiIi1Iii1I1 - KmkKmkKmkKmkmkKmmK % Kmmmm % i1iIIIiI1I - KKmKmkmkmkKmkKK
def iiI1IiI ( name , url , iconimage ) :
 url = url . replace ( ' ' , '%20' )
 iconimage = iconimage . replace ( ' ' , '%20' )
 II = '<FAV><item>\n<title>' + name + '</title>\n<link>' + url + '</link>\n' + '<thumbnail>' + iconimage + '</thumbnail>\n</item></FAV>\n'
 mmKm = open ( KmmkK , 'a' )
 mmKm . write ( II )
 mmKm . close ( )
 if 57 - 57: mmKmmmkK
def KmmKmk ( name , url , iconimage ) :
 iiiI11 = None
 file = open ( KmmkK , 'r' )
 iiiI11 = file . read ( )
 II11iiii1Ii = ''
 KmmkmKmkmmm = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( iiiI11 )
 for KKmKmkmkm in KmmkmKmkmmm :
  II = '\n<FAV><item>\n' + KKmKmkmkm + '</item>\n'
  if name in KKmKmkmkm :
   II = II . replace ( 'item' , ' ' )
  II11iiii1Ii = II11iiii1Ii + II
 file = open ( KmmkK , 'w' )
 file . truncate ( )
 file . write ( II11iiii1Ii )
 file . close ( )
 xbmc . executebuiltin ( 'Container.Refresh' )
 if 70 - 70: Kmkmk / i1I1i1Ii11 . IIIIII11i1I - i1iIIIiI1I % i1iIIII
def KmkKKK ( name , url , iconimage , fanart ) :
 mmkmmkmKKKmmkmm = mmkmmmkmmkKmkmkKK ( name )
 KmkKmkKKmkKmkKmk . setSetting ( 'tv' , mmkmmkmKKKmmkmm )
 mmkmKmk = mmmkmk ( url )
 mmkmK ( mmkmKmk )
 if 'Index' in url :
  I1i1iii ( url )
 if 'XXX' in name : i1iiI11I ( mmkmKmk )
 KmmkmKmkmmm = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( mmkmKmk )
 KKKmmk = str ( len ( KmmkmKmkmmm ) )
 KmkKmkKKmkKmkKmk . setSetting ( 'count' , KKKmmk )
 KmkKmkKKmkKmkKmk . setSetting ( 'fav' , 'no' )
 for KKmmK in KmmkmKmkmmm :
  try :
   if '<sportsdevil>' in KKmmK : iiii ( KKmmK , url )
   elif '<iptv>' in KKmmK : mKmkmmkKmkKKKmmmk ( KKmmK )
   elif '<Image>' in KKmmK : IiIiiI ( KKmmK )
   elif '<text>' in KKmmK : I1I ( KKmmK )
   elif '<scraper>' in KKmmK : SCRAPER ( KKmmK )
   elif '<redirect>' in KKmmK : REDIRECT ( KKmmK )
   elif '<oktitle>' in KKmmK : mKKmkmkmKK ( KKmmK )
   else : KmKm ( KKmmK , url , iconimage )
  except : pass
  if 18 - 18: i11iIiiIii
def mKKmkmkmKK ( item ) :
 mmkmKmKmkmkm = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 Ii11I = re . compile ( '<oktitle>(.+?)</oktitle>' ) . findall ( item ) [ 0 ]
 KKKmkKKKmkmkmm = re . compile ( '<line1>(.+?)</line1>' ) . findall ( item ) [ 0 ]
 Iii111II = re . compile ( '<line2>(.+?)</line2>' ) . findall ( item ) [ 0 ]
 iiii11I = re . compile ( '<line3>(.+?)</line3>' ) . findall ( item ) [ 0 ]
 KmmmkKKmkmKK = '##' + Ii11I + '#' + KKKmkKKKmkmkmm + '#' + Iii111II + '#' + iiii11I + '##'
 mKKmmmkmkKmkK = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 ii11i1 ( mmkmKmKmkmkm , KmmmkKKmkmKK , 17 , mKKmmmkmkKmkK , II1 )
 if 29 - 29: IiIi1Iii1I1 % mmmKmkmmmkmKKKK + IIIIII11i1I / I1Ii + Kmmmm * I1Ii
def i1I1iI ( name , url ) :
 mmmkKmmKKmmk = re . compile ( '##(.+?)##' ) . findall ( url ) [ 0 ] . split ( '#' )
 i11 = xbmcgui . Dialog ( )
 i11 . ok ( mmmkKmmKKmmk [ 0 ] , mmmkKmmKKmmk [ 1 ] , mmmkKmmKKmmk [ 2 ] , mmmkKmmKKmmk [ 3 ] )
 if 92 - 92: mmKmmmkK . i1iIIIiI1I + I1Ii
def I1I ( item ) :
 mmkmKmKmkmkm = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 KmmmkKKmkmKK = re . compile ( '<text>(.+?)</text>' ) . findall ( item ) [ 0 ]
 mKKmmmkmkKmkK = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 ii11i1 ( mmkmKmKmkmkm , KmmmkKKmkmKK , 9 , mKKmmmkmkKmkK , II1 )
 if 28 - 28: mmkmkmkmkmKmKmKmkm * Kmkm - I1Ii * Kmkmk * KKmKmkmkmkKmkKK / i1iIIII
def KmmKmkKmKKKK ( name , url ) :
 i1Ii = mmmkmk ( url )
 mmkmkKKmkmkKmK ( name , i1Ii )
 if 60 - 60: i1iIIII * I1 - i1iIIII % KmKKmkmmKKmmmkK - IIIIII11i1I + mmmKmkmmmkmKKKK
def IiIiiI ( item ) :
 KmkmkKmmkmkmkmmKmk = re . compile ( '<Image>(.+?)</Image>' ) . findall ( item )
 if len ( KmkmkKmmkmkmkmmKmk ) == 1 :
  mmkmKmKmkmkm = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  mKKmmmkmkKmkK = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  KmKmkKmkmk = re . compile ( '<Image>(.+?)</Image>' ) . findall ( item ) [ 0 ]
  mKKmmmkmkKmkK = KmKmkKmkmk . replace ( 'http://imgur.com/' , 'http://i.imgur.com/' ) + '.jpg'
  KmKmkKmkmk = KmKmkKmkmk . replace ( 'http://imgur.com/' , 'http://i.imgur.com/' ) + '.jpg'
  ii11i1 ( mmkmKmKmkmkm , KmKmkKmkmk , 7 , mKKmmmkmkKmkK , II1 )
 elif len ( KmkmkKmmkmkmkmmKmk ) > 1 :
  mmkmKmKmkmkm = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  mKKmmmkmkKmkK = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  IIiII = ''
  for KmKmkKmkmk in KmkmkKmmkmkmkmmKmk :
   mKKmmmkmkKmkK = KmKmkKmkmk . replace ( 'http://imgur.com/' , 'http://i.imgur.com/' ) + '.jpg'
   KmKmkKmkmk = KmKmkKmkmk . replace ( 'http://imgur.com/' , 'http://i.imgur.com/' ) + '.jpg'
   IIiII = IIiII + '<Image>' + KmKmkKmkmk + '</Image>'
  mmk = IiIi11iIIi1Ii
  mmkmKmKmkmkm = mmkmmmkmmkKmkmkKK ( mmkmKmKmkmkm )
  mmKmmmmkmkmkmKK = os . path . join ( os . path . join ( mmk , '' ) , mmkmKmKmkmkm + '.txt' )
  if not os . path . exists ( mmKmmmmkmkmkmKK ) : file ( mmKmmmmkmkmkmKK , 'w' ) . close ( )
  KmmkmKKm = open ( mmKmmmmkmkmkmKK , "w" )
  KmmkmKKm . write ( IIiII )
  KmmkmKKm . close ( )
  ii11i1 ( mmkmKmKmkmkm , 'image' , 8 , mKKmmmkmkKmkK , II1 )
  if 58 - 58: i1I1ii1II1iII * Kmmmm * IiIi1Iii1I1 / Kmmmm
def mKmkmmkKmkKKKmmmk ( item ) :
 mmkmKmKmkmkm = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 mKKmmmkmkKmkK = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 i1 = re . compile ( '<iptv>(.+?)</iptv>' ) . findall ( item ) [ 0 ]
 i1111 ( mmkmKmKmkmkm , i1 , 6 , mKKmmmkmkKmkK , II1 )
 if 75 - 75: KmkKmkKmkKmkmkKmmK
def I1III ( url , iconimage ) :
 mmkmKmk = mmmkmk ( url )
 KKmkKmkKmKKmk = re . compile ( '^#.+?:-?[0-9]*(.*?),(.*?)\n(.*?)$' , re . I + re . M + re . U + re . S ) . findall ( mmkmKmk )
 iiiI1I11i1 = [ ]
 for IIi1i11111 , mmkmKmKmkmkm , url in KKmkKmkKmKKmk :
  mmKKmkmkKmkmkmm = { "params" : IIi1i11111 , "name" : mmkmKmKmkmkm , "url" : url }
  iiiI1I11i1 . append ( mmKKmkmkKmkmkmm )
 list = [ ]
 for I1ii11iI in iiiI1I11i1 :
  mmKKmkmkKmkmkmm = { "name" : I1ii11iI [ "name" ] , "url" : I1ii11iI [ "url" ] }
  KKmkKmkKmKKmk = re . compile ( ' (.+?)="(.+?)"' , re . I + re . M + re . U + re . S ) . findall ( I1ii11iI [ "params" ] )
  for IIi1i , I1I1iIiII1 in KKmkKmkKmKKmk :
   mmKKmkmkKmkmkmm [ IIi1i . strip ( ) . lower ( ) . replace ( '-' , '_' ) ] = I1I1iIiII1 . strip ( )
  list . append ( mmKKmkmkKmkmkmm )
 for I1ii11iI in list :
  if '.ts' in I1ii11iI [ "url" ] : ii11i1 ( I1ii11iI [ "name" ] , I1ii11iI [ "url" ] , 2 , iconimage , II1 )
  else : II111iiii ( I1ii11iI [ "name" ] , I1ii11iI [ "url" ] , 2 , iconimage , II1 )
  if 4 - 4: IIIIII11i1I + Ii1I * Kmmmm
def KmKm ( item , url , iconimage ) :
 KKmmmkK = iconimage
 KmmkmmKmmkm = url
 Ii1i1 = re . compile ( '<link>(.+?)</link>' ) . findall ( item )
 KKmKmkmkm = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>' , re . DOTALL ) . findall ( item )
 for mmkmKmKmkmkm , iiIii , iconimage in KKmKmkmkm :
  if 'youtube.com/playlist?' in iiIii :
   mmmmkK = iiIii . split ( 'list=' ) [ 1 ]
   i1111 ( mmkmKmKmkmkm , iiIii , mKmKmkmmkmkKKmk , iconimage , II1 , description = mmmmkK )
 if len ( Ii1i1 ) == 1 :
  mmkmKmKmkmkm = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  url = re . compile ( '<link>(.+?)</link>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  if iconimage == 'ImageHere' : iconimage = KKmmmkK
  if '.ts' in url : ii11i1 ( mmkmKmKmkmkm , url , 16 , iconimage , II1 , description = '' )
  elif 'movies' in KmmkmmKmmkm :
   i1I1ii ( mmkmKmKmkmkm , url , 2 , iconimage , int ( KKKmmk ) , isFolder = False )
  else : II111iiii ( mmkmKmKmkmkm , url , 2 , iconimage , II1 )
 elif len ( Ii1i1 ) > 1 :
  mmkmKmKmkmkm = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  if '.ts' in url : ii11i1 ( mmkmKmKmkmkm , url , 16 , iconimage , II1 , description = '' )
  elif 'movies' in KmmkmmKmmkm :
   i1I1ii ( mmkmKmKmkmkm , url , 2 , iconimage , int ( KKKmmk ) , isFolder = False )
  else : II111iiii ( mmkmKmKmkmkm , url , 3 , iconimage , II1 )
  if 61 - 61: i1I1ii1II1iII
def I1i1iii ( url ) :
 mmkmKmk = mmmkmk ( url )
 KmmkmKmkmmm = re . compile ( 'name="(.+?)".+?rl="(.+?)".+?mg="(.+?)"' , re . DOTALL ) . findall ( mmkmKmk )
 for mmkmKmKmkmkm , url , I1IiiI in KmmkmKmkmmm :
  if 'youtube.com/playlist?list=' in url :
   i1111 ( mmkmKmKmkmkm , url , 3 , I1IiiI , II1 )
  elif 'youtube.com/results?search_query=' in url :
   i1111 ( mmkmKmKmkmkm , url , 3 , I1IiiI , II1 )
  else :
   i1111 ( mmkmKmKmkmkm , url , 1 , I1IiiI , II1 )
   if 64 - 64: IIIIII11i1I / I1 - Ii1I - i1iIIIiI1I
def KmkmKmKKKmKK ( item ) :
 item = item . replace ( '\r' , '' ) . replace ( '\t' , '' ) . replace ( '&nbsp;' , '' ) . replace ( '\'' , '' ) . replace ( '\n' , '' )
 KKmKmkmkm = re . compile ( 'name="(.+?)".+?rl="(.+?)".+?mg="(.+?)"' , re . DOTALL ) . findall ( item )
 for mmkmKmKmkmkm , i1 , mKKmmmkmkKmkK in KKmKmkmkm :
  if 'youtube.com/channel/' in i1 :
   mmmmkK = i1 . split ( 'channel/' ) [ 1 ]
   i1111 ( mmkmKmKmkmkm , i1 , mKmKmkmmkmkKKmk , mKKmmmkmkKmkK , II1 , description = mmmmkK )
  elif 'youtube.com/user/' in i1 :
   mmmmkK = i1 . split ( 'user/' ) [ 1 ]
   i1111 ( mmkmKmKmkmkm , i1 , mKmKmkmmkmkKKmk , mKKmmmkmkKmkK , II1 , description = mmmmkK )
  elif 'youtube.com/playlist?' in i1 :
   mmmmkK = i1 . split ( 'list=' ) [ 1 ]
   i1111 ( mmkmKmKmkmkm , i1 , mKmKmkmmkmkKKmk , mKKmmmkmkKmkK , II1 , description = mmmmkK )
  elif 'plugin://' in i1 :
   ii1ii11IIIiiI = HTMLParser ( )
   i1 = ii1ii11IIIiiI . unescape ( i1 )
   i1111 ( mmkmKmKmkmkm , i1 , mKmKmkmmkmkKKmk , mKKmmmkmkKmkK , II1 )
  else :
   i1111 ( mmkmKmKmkmkm , i1 , 1 , mKKmmmkmkKmkK , II1 )
   if 67 - 67: i1iIIIiI1I * KmkKmkKmkKmkmkKmmK * IiIi1Iii1I1 + Kmmmm / mmkmkmkmkmKmKmKmkm
def iiii ( item , url ) :
 Ii1i1 = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( item )
 I1I111 = re . compile ( '<link>(.+?)</link>' ) . findall ( item )
 if len ( Ii1i1 ) + len ( I1I111 ) == 1 :
  mmkmKmKmkmkm = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  mKKmmmkmkKmkK = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  url = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( item ) [ 0 ]
  mmkmKmk = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' + url
  ii11i1 ( mmkmKmKmkmkm , url , 16 , mKKmmmkmkKmkK , II1 )
 elif len ( Ii1i1 ) + len ( I1I111 ) > 1 :
  mmkmKmKmkmkm = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  mKKmmmkmkKmkK = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  ii11i1 ( mmkmKmKmkmkm , url , 3 , mKKmmmkmkKmkK , II1 )
  if 82 - 82: i11iIiiIii - mmKmmmkK * KmKKmkmmKKmmmkK / i1iIIIiI1I
def i1iiI11I ( link ) :
 if mKmkmkmKm == '' :
  i11 = xbmcgui . Dialog ( )
  I11 = i11 . yesno ( 'Adult Content' , 'You have opted to show adult content' , '' , 'Please set a password to prevent accidental access' , 'Cancel' , 'OK' )
  if I11 == 1 :
   Kmmkmmkmkmkmkmmkmmk = xbmc . Keyboard ( '' , 'Set Password' )
   Kmmkmmkmkmkmkmmkmmk . doModal ( )
   if ( Kmmkmmkmkmkmkmmkmmk . isConfirmed ( ) ) :
    mKmmkmmmmmkmkm = Kmmkmmkmkmkmkmmkmmk . getText ( )
    KmkKmkKKmkKmkKmk . setSetting ( 'password' , mKmmkmmmmmkmkm )
  else : quit ( )
 elif mKmkmkmKm <> '' :
  i11 = xbmcgui . Dialog ( )
  I11 = i11 . yesno ( 'Adult Content' , 'Please enter the password you set' , 'to continue' , '' , 'Cancel' , 'OK' )
  if I11 == 1 :
   Kmmkmmkmkmkmkmmkmmk = xbmc . Keyboard ( '' , 'Enter Password' )
   Kmmkmmkmkmkmkmmkmmk . doModal ( )
   if ( Kmmkmmkmkmkmkmmkmmk . isConfirmed ( ) ) :
    mKmmkmmmmmkmkm = Kmmkmmkmkmkmkmmkmmk . getText ( )
   if mKmmkmmmmmkmkm <> mKmkmkmKm :
    quit ( )
  else : quit ( )
  if 31 - 31: Kmkmk . i1iIIII - KmKK
def mmKKKmkmkKmm ( ) :
 Kmmkmmkmkmkmkmmkmmk = xbmc . Keyboard ( '' , 'Search' )
 Kmmkmmkmkmkmkmmkmmk . doModal ( )
 if ( Kmmkmmkmkmkmkmmkmmk . isConfirmed ( ) ) :
  mmmmkK = Kmmkmmkmkmkmkmmkmmk . getText ( )
  mmmmkK = mmmmkK . upper ( )
 else : quit ( )
 mmkmKmk = mmmkmk ( IiI )
 IiIIIi1iIi = re . compile ( '<link>(.+?)</link>' ) . findall ( mmkmKmk )
 for i1 in IiIIIi1iIi :
  try :
   mmkmKmk = mmmkmk ( i1 )
   mmKKmmmmmm = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( mmkmKmk )
   for KKmmK in mmKKmmmmmm :
    KmmkmKmkmmm = re . compile ( '<title>(.+?)</title>' ) . findall ( KKmmK )
    for II1I in KmmkmKmkmmm :
     II1I = II1I . upper ( )
     if mmmmkK in II1I :
      try :
       if 'Index' in i1 : I1i1iii ( i1 )
       elif '<sportsdevil>' in KKmmK : iiii ( KKmmK , i1 )
       elif '<iptv>' in KKmmK : mKmkmmkKmkKKKmmmk ( KKmmK )
       elif '<Image>' in KKmmK : IiIiiI ( KKmmK )
       elif '<text>' in KKmmK : I1I ( KKmmK )
       elif '<scraper>' in KKmmK : SCRAPER ( KKmmK )
       elif '<redirect>' in KKmmK : REDIRECT ( KKmmK )
       elif '<oktitle>' in KKmmK : mKKmkmkmKK ( KKmmK )
       else : KmKm ( KKmmK , i1 , mKKmmmkmkKmkK )
      except : pass
  except : pass
  if 84 - 84: Kmkmk . i11iIiiIii . Kmkmk * IiIi1Iii1I1 - i1iIIIiI1I
def ii ( name , url , iconimage ) :
 KmkmmkmKKKmKm = [ ]
 II1I1iiiI1Ii1I = [ ]
 KmkKKKmkK = [ ]
 mmkmKmk = mmmkmk ( url )
 iiiiIiI = re . compile ( '<title>' + re . escape ( name ) + '</title>(.+?)</item>' , re . DOTALL ) . findall ( mmkmKmk ) [ 0 ]
 iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( iiiiIiI ) [ 0 ]
 Ii1i1 = [ ]
 if '<link>' in iiiiIiI :
  I1KKKmkmkKmkK = re . compile ( '<link>(.+?)</link>' ) . findall ( iiiiIiI )
  for iii in I1KKKmkmkKmkK :
   Ii1i1 . append ( iii )
 if '<sportsdevil>' in iiiiIiI :
  mKmmKKKmKm = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( iiiiIiI )
  for i1Iii1i1I in mKmmKKKmKm :
   i1Iii1i1I = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' + i1Iii1i1I
   Ii1i1 . append ( i1Iii1i1I )
 KKmKmkmk = 1
 for IiI111111IIII in Ii1i1 :
  i1Iiii111iI1iIi1 = IiI111111IIII
  if '(' in IiI111111IIII :
   IiI111111IIII = IiI111111IIII . split ( '(' ) [ 0 ]
   KKK = str ( i1Iiii111iI1iIi1 . split ( '(' ) [ 1 ] . replace ( ')' , '' ) )
   KmkmmkmKKKmKm . append ( IiI111111IIII )
   II1I1iiiI1Ii1I . append ( KKK )
  else :
   mmmkKKmmk = IiI111111IIII . split ( '/' ) [ 2 ] . replace ( 'www.' , '' )
   KmkmmkmKKKmKm . append ( IiI111111IIII )
   II1I1iiiI1Ii1I . append ( 'Link ' + str ( KKmKmkmk ) )
  KKmKmkmk = KKmKmkmk + 1
 i11 = xbmcgui . Dialog ( )
 I11IiI = i11 . select ( 'Choose a link..' , II1I1iiiI1Ii1I )
 if I11IiI < 0 : quit ( )
 else :
  url = KmkmmkmKKKmKm [ I11IiI ]
  KmkmmKmkKmmkmkm ( name , url , iconimage )
  if 77 - 77: KmKK * i1iIIII
def mKmmKmmk ( url ) :
 II = "ShowPicture(%s)" % url
 xbmc . executebuiltin ( II )
 if 38 - 38: i1I1i1Ii11
def KmkmmKmkKmmkmkm ( name , url , iconimage ) :
 try :
  if 'plugin://plugin.video.SportsDevil/' in url :
   KmmmkmkmmkKmmm ( name , url , iconimage )
  elif '.ts' in url :
   url = 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;name=' + name + '&amp;url=' + url
   KmmmkmkmmkKmmm ( name , url , iconimage )
  elif urlresolver . HostedMediaFile ( url ) . valid_url ( ) :
   url = urlresolver . HostedMediaFile ( url ) . resolve ( )
   KKmmmmKmkKm ( name , url , iconimage )
  elif liveresolver . isValid ( url ) == True :
   url = liveresolver . resolve ( url )
   KKmmmmKmkKm ( name , url , iconimage )
  else : KKmmmmKmkKm ( name , url , iconimage )
 except :
  KK ( 'UKTurk' , 'Stream Unavailable' , '3000' , I1IiiI )
  if 25 - 25: i1iIIII
def mKmmkmK ( url ) :
 if urlresolver . HostedMediaFile ( url ) . valid_url ( ) :
  url = urlresolver . HostedMediaFile ( url ) . resolve ( )
 xbmc . Player ( ) . play ( url )
 if 51 - 51: Kmkm - KmkKmkKmkKmkmkKmmK + i1I1ii1II1iII * KKmKmkmkmkKmkKK . i1iIIIiI1I + KmkKmkKmkKmkmkKmmK
def KKmmmmKmkKm ( name , url , iconimage ) :
 KmKmkm = True
 mKmkmmkKmmmm = xbmcgui . ListItem ( name , iconImage = iconimage , thumbnailImage = iconimage ) ; mKmkmmkKmmmm . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
 KmKmkm = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = url , listitem = mKmkmmkKmmmm )
 mKmkmmkKmmmm . setPath ( url )
 xbmcplugin . setResolvedUrl ( int ( sys . argv [ 1 ] ) , True , mKmkmmkKmmmm )
 if 94 - 94: I1Ii * KKmKmkmkmkKmkKK / Kmkm / KKmKmkmkmkKmkKK
def KmmmkmkmmkKmmm ( name , url , iconimage ) :
 KmKmkm = True
 mKmkmmkKmmmm = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage ) ; mKmkmmkKmmmm . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
 KmKmkm = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = url , listitem = mKmkmmkKmmmm )
 i11 = xbmcgui . Dialog ( )
 xbmc . Player ( ) . play ( url , mKmkmmkKmmmm , False )
 if 87 - 87: Kmkm . Kmkmk
def KmkKKmkK ( url ) :
 xbmc . executebuiltin ( "PlayMedia(%s)" % url )
 if 81 - 81: KmkKmkKmkKmkmkKmmK . I1Ii % Ii1I / mmmKmkmmmkmKKKK - KmkKmkKmkKmkmkKmmK
def Ii1I1i ( url ) :
 KKI1iI1ii1II = KmkKmkKKmkKmkKmk . getSetting ( 'layout' )
 if KKI1iI1ii1II == 'Listers' : KmkKmkKKmkKmkKmk . setSetting ( 'layout' , 'Category' )
 else : KmkKmkKKmkKmkKmk . setSetting ( 'layout' , 'Listers' )
 xbmc . executebuiltin ( 'Container.Refresh' )
 if 57 - 57: i1I1i1Ii11 % KKmKmkmkmkKmkKK + I1Ii - Kmkm
def mmmkmk ( url ) :
 mmkK = urllib2 . Request ( url )
 mmkK . add_header ( 'User-Agent' , 'mat' )
 IiI1i = urllib2 . urlopen ( mmkK )
 mmkmKmk = IiI1i . read ( )
 IiI1i . close ( )
 mmkmKmk = mmkmKmk . replace ( '</fanart>' , '<fanart>x</fanart>' ) . replace ( '<thumbnail></thumbnail>' , '<thumbnail>x</thumbnail>' ) . replace ( '<utube>' , '<link>https://www.youtube.com/watch?v=' ) . replace ( '</utube>' , '</link>' )
 if '{' in mmkmKmk : mmkmKmk = mmkKmmkmk ( mmkmKmk )
 return mmkmKmk
 if 32 - 32: I1Ii . Kmkmk * i1iIIIiI1I
def KKmmmmkmKKmkK ( ) :
 mmkmkKmk = [ ]
 mKKmkKmkmkKmmkKmkm = sys . argv [ 2 ]
 if len ( mKKmkKmkmkKmmkKmkm ) >= 2 :
  IIi1i11111 = sys . argv [ 2 ]
  ii1 = IIi1i11111 . replace ( '?' , '' )
  if ( IIi1i11111 [ len ( IIi1i11111 ) - 1 ] == '/' ) :
   IIi1i11111 = IIi1i11111 [ 0 : len ( IIi1i11111 ) - 2 ]
  I1iIIiiIIi1i = ii1 . split ( '&' )
  mmkmkKmk = { }
  for KKmKmkmk in range ( len ( I1iIIiiIIi1i ) ) :
   KmkKmkmmKKK = { }
   KmkKmkmmKKK = I1iIIiiIIi1i [ KKmKmkmk ] . split ( '=' )
   if ( len ( KmkKmkmmKKK ) ) == 2 :
    mmkmkKmk [ KmkKmkmmKKK [ 0 ] ] = KmkKmkmmKKK [ 1 ]
 return mmkmkKmk
 if 77 - 77: I1 - i1I1ii1II1iII - IIIIII11i1I
def KK ( title , message , ms , nart ) :
 xbmc . executebuiltin ( "XBMC.notification(" + title + "," + message + "," + ms + "," + nart + ")" )
 if 49 - 49: i1I1ii1II1iII % Ii1I . I1 + KmkKmkKmkKmkmkKmmK / mmmKmkmmmkmKKKK
def mmkmmmkmmkKmkmkKK ( string ) :
 KmkmKKmKmmmmK = re . compile ( '\[(.+?)\]' ) . findall ( string )
 for mmmKmmkKKKmmmk in KmkmKKmKmmmmK : string = string . replace ( mmmKmmkKKKmmmk , '' ) . replace ( '[/]' , '' ) . replace ( '[]' , '' )
 return string
 if 51 - 51: Kmkm / I1 . Kmmmm * I1Ii + i1iIIII * Kmkmk
def KKKmKm ( string ) :
 string = string . split ( ' ' )
 Kmkmkmmk = ''
 for I11iII in string :
  iIIII = '[B][COLOR red]' + I11iII [ 0 ] . upper ( ) + '[/COLOR][COLOR white]' + I11iII [ 1 : ] + '[/COLOR][/B] '
  Kmkmkmmk = Kmkmkmmk + iIIII
 return Kmkmkmmk
 if 33 - 33: IIIIII11i1I . i1I1ii1II1iII % mmKmmmkK + I1Ii
def i1I1ii ( name , url , mode , iconimage , itemcount , isFolder = False ) :
 if Kmmmmkmkmkm == 'true' :
  if not 'COLOR' in name :
   mKmkmkKmkmkmkmKmk = name . partition ( '(' )
   KmkKmKKmkm = ""
   mmmmmmkKmkmkmkmkmm = ""
   if len ( mKmkmkKmkmkmkmKmk ) > 0 :
    KmkKmKKmkm = mKmkmkKmkmkmkmKmk [ 0 ]
    mmmmmmkKmkmkmkmkmm = mKmkmkKmkmkmkmKmk [ 2 ] . partition ( ')' )
   if len ( mmmmmmkKmkmkmkmkmm ) > 0 :
    mmmmmmkKmkmkmkmkmm = mmmmmmkKmkmkmkmkmm [ 0 ]
   iIii1II11 = eval ( base64 . b64decode ( 'bWV0YWhhbmRsZXJzLk1ldGFEYXRhKHRtZGJfYXBpX2tleT0iZDk1NWQ4ZjAyYTNmMjQ4MGE1MTg4MWZlNGM5NmYxMGUiKQ==' ) )
   KmmKmmkmmm = iIii1II11 . get_meta ( 'movie' , name = KmkKmKKmkm , year = mmmmmmkKmkmkmkmkmm )
   mmkmkmmmk = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&site=" + str ( I11ii1IIiIi ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name )
   KmKmkm = True
   mKmkmmkKmmmm = xbmcgui . ListItem ( name , iconImage = KmmKmmkmmm [ 'cover_url' ] , thumbnailImage = KmmKmmkmmm [ 'cover_url' ] )
   mKmkmmkKmmmm . setInfo ( type = "Video" , infoLabels = KmmKmmkmmm )
   mKmkmmkKmmmm . setProperty ( "IsPlayable" , "true" )
   KmKKmmkKKmK = [ ]
   if KmkKmkKKmkKmkKmk . getSetting ( 'fav' ) == 'yes' : KmKKmmkKKmK . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
   if KmkKmkKKmkKmkKmk . getSetting ( 'fav' ) == 'no' : KmKKmmkKKmK . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
   mKmkmmkKmmmm . addContextMenuItems ( KmKKmmkKKmK , replaceItems = False )
   if not KmmKmmkmmm [ 'backdrop_url' ] == '' : mKmkmmkKmmmm . setProperty ( 'fanart_image' , KmmKmmkmmm [ 'backdrop_url' ] )
   else : mKmkmmkKmmmm . setProperty ( 'fanart_image' , II1 )
   KmKmkm = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = mmkmkmmmk , listitem = mKmkmmkKmmmm , isFolder = isFolder , totalItems = itemcount )
   return KmKmkm
 else :
  mmkmkmmmk = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&site=" + str ( I11ii1IIiIi ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name )
  KmKmkm = True
  mKmkmmkKmmmm = xbmcgui . ListItem ( name , iconImage = iconimage , thumbnailImage = iconimage )
  mKmkmmkKmmmm . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
  mKmkmmkKmmmm . setProperty ( 'fanart_image' , II1 )
  mKmkmmkKmmmm . setProperty ( "IsPlayable" , "true" )
  KmKKmmkKKmK = [ ]
  if KmkKmkKKmkKmkKmk . getSetting ( 'fav' ) == 'yes' : KmKKmmkKKmK . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
  if KmkKmkKKmkKmkKmk . getSetting ( 'fav' ) == 'no' : KmKKmmkKKmK . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
  mKmkmmkKmmmm . addContextMenuItems ( KmKKmmkKKmK , replaceItems = False )
  KmKmkm = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = mmkmkmmmk , listitem = mKmkmmkKmmmm , isFolder = isFolder )
  return KmKmkm
  if 72 - 72: KKmKmkmkmkKmkKK
def i1111 ( name , url , mode , iconimage , fanart , description = '' ) :
 mmkmkmmmk = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&fanart=" + urllib . quote_plus ( fanart ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 KmKmkm = True
 mKmkmmkKmmmm = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 mKmkmmkKmmmm . setInfo ( type = "Video" , infoLabels = { "Title" : name , 'plot' : description } )
 mKmkmmkKmmmm . setProperty ( 'fanart_image' , fanart )
 KmKKmmkKKmK = [ ]
 if KmkKmkKKmkKmkKmk . getSetting ( 'fav' ) == 'yes' : KmKKmmkKKmK . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 if KmkKmkKKmkKmkKmk . getSetting ( 'fav' ) == 'no' : KmKKmmkKKmK . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 mKmkmmkKmmmm . addContextMenuItems ( KmKKmmkKKmK , replaceItems = False )
 if 'youtube.com/channel/' in url :
  mmkmkmmmk = 'plugin://plugin.video.youtube/channel/' + description + '/'
 if 'youtube.com/user/' in url :
  mmkmkmmmk = 'plugin://plugin.video.youtube/user/' + description + '/'
 if 'youtube.com/playlist?' in url :
  mmkmkmmmk = 'plugin://plugin.video.youtube/playlist/' + description + '/'
 if 'plugin://' in url :
  mmkmkmmmk = url
 KmKmkm = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = mmkmkmmmk , listitem = mKmkmmkKmmmm , isFolder = True )
 return KmKmkm
 if 1 - 1: i1iIIII * Kmkmk * KmKKmkmmKKmmmkK + IIIIII11i1I
def ii11i1 ( name , url , mode , iconimage , fanart , description = '' ) :
 mmkmkmmmk = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 KmKmkm = True
 mKmkmmkKmmmm = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 mKmkmmkKmmmm . setProperty ( 'fanart_image' , fanart )
 KmKKmmkKKmK = [ ]
 if KmkKmkKKmkKmkKmk . getSetting ( 'fav' ) == 'yes' : KmKKmmkKKmK . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 if KmkKmkKKmkKmkKmk . getSetting ( 'fav' ) == 'no' : KmKKmmkKKmK . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 mKmkmmkKmmmm . addContextMenuItems ( KmKKmmkKKmK , replaceItems = False )
 KmKmkm = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = mmkmkmmmk , listitem = mKmkmmkKmmmm , isFolder = False )
 return KmKmkm
 if 33 - 33: Ii1I * I1Ii - i1I1i1Ii11 % i1I1i1Ii11
def II111iiii ( name , url , mode , iconimage , fanart , description = '' ) :
 mmkmkmmmk = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 KmKmkm = True
 mKmkmmkKmmmm = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 mKmkmmkKmmmm . setProperty ( 'fanart_image' , fanart )
 mKmkmmkKmmmm . setProperty ( "IsPlayable" , "true" )
 KmKKmmkKKmK = [ ]
 if KmkKmkKKmkKmkKmk . getSetting ( 'fav' ) == 'yes' : KmKKmmkKKmK . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 if KmkKmkKKmkKmkKmk . getSetting ( 'fav' ) == 'no' : KmKKmmkKKmK . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 mKmkmmkKmmmm . addContextMenuItems ( KmKKmmkKKmK , replaceItems = False )
 KmKmkm = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = mmkmkmmmk , listitem = mKmkmmkKmmmm , isFolder = False )
 return KmKmkm
 if 18 - 18: i1I1i1Ii11 / Kmkm * i1I1i1Ii11 + i1I1i1Ii11 * i11iIiiIii * IiIi1Iii1I1
def I1II1 ( url , name ) :
 mmmK = mmmkmk ( url )
 if len ( mmmK ) > 1 :
  mmk = IiIi11iIIi1Ii
  mmKmmmmkmkmkmKK = os . path . join ( os . path . join ( mmk , '' ) , name + '.txt' )
  if not os . path . exists ( mmKmmmmkmkmkmKK ) :
   file ( mmKmmmmkmkmkmKK , 'w' ) . close ( )
  i1I1i111Ii = open ( mmKmmmmkmkmkmKK )
  mmm = i1I1i111Ii . read ( )
  if mmm == mmmK : pass
  else :
   mmkmkKKmkmkKmK ( 'UKTurk' , mmmK )
   KmmkmKKm = open ( mmKmmmmkmkmkmKK , "w" )
   KmmkmKKm . write ( mmmK )
   KmmkmKKm . close ( )
   if 27 - 27: IIIIII11i1I % mmmKmkmmmkmKKKK
def mmkmkKKmkmkKmK ( heading , text ) :
 id = 10147
 xbmc . executebuiltin ( 'ActivateWindow(%d)' % id )
 xbmc . sleep ( 500 )
 mmkmmmKKmkmk = xbmcgui . Window ( id )
 iiIiii1IIIII = 50
 while ( iiIiii1IIIII > 0 ) :
  try :
   xbmc . sleep ( 10 )
   iiIiii1IIIII -= 1
   mmkmmmKKmkmk . getControl ( 1 ) . setLabel ( heading )
   mmkmmmKKmkmk . getControl ( 5 ) . setText ( text )
   return
  except :
   pass
   if 67 - 67: KKmKmkmkmkKmkKK / Kmkmk
def iiIiIIIiiI ( name ) :
 global Icon
 global Next
 global Previous
 global window
 global Quit
 global images
 mmKmmmmkmkmkmKK = os . path . join ( os . path . join ( IiIi11iIIi1Ii , '' ) , name + '.txt' )
 i1I1i111Ii = open ( mmKmmmmkmkmkmKK )
 mmm = i1I1i111Ii . read ( )
 images = re . compile ( '<image>(.+?)</image>' ) . findall ( mmm )
 KmkKmkKKmkKmkKmk . setSetting ( 'pos' , '0' )
 window = pyxbmct . AddonDialogWindow ( '' )
 iiI1IIIi = '/resources/art'
 II11IiIi11 = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + KKmkm + iiI1IIIi , 'next_focus.png' ) )
 IIKKKmkKmkmkKmkKKKK = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + KKmkm + iiI1IIIi , 'next1.png' ) )
 I1iiii1I = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + KKmkm + iiI1IIIi , 'previous_focus.png' ) )
 KKmmk = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + KKmkm + iiI1IIIi , 'previous.png' ) )
 mKmkmkmmmmKmkm = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + KKmkm + iiI1IIIi , 'close_focus.png' ) )
 mmmkm = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + KKmkm + iiI1IIIi , 'close.png' ) )
 mmkmKmkmmmKmm = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + KKmkm + iiI1IIIi , 'main-bg1.png' ) )
 window . setGeometry ( 1300 , 720 , 100 , 50 )
 I1III1111iIi = pyxbmct . Image ( mmkmKmkmmmKmm )
 window . placeControl ( I1III1111iIi , - 10 , - 10 , 130 , 70 )
 KmmmkKKmkmKK = '0xFF000000'
 Previous = pyxbmct . Button ( '' , focusTexture = I1iiii1I , noFocusTexture = KKmmk , textColor = KmmmkKKmkmKK , focusedColor = KmmmkKKmkmKK )
 Next = pyxbmct . Button ( '' , focusTexture = II11IiIi11 , noFocusTexture = IIKKKmkKmkmkKmkKKKK , textColor = KmmmkKKmkmKK , focusedColor = KmmmkKKmkmKK )
 Quit = pyxbmct . Button ( '' , focusTexture = mKmkmkmmmmKmkm , noFocusTexture = mmmkm , textColor = KmmmkKKmkmKK , focusedColor = KmmmkKKmkmKK )
 Icon = pyxbmct . Image ( images [ 0 ] , aspectRatio = 1 )
 window . placeControl ( Previous , 102 , 1 , 10 , 10 )
 window . placeControl ( Next , 102 , 40 , 10 , 10 )
 window . placeControl ( Quit , 102 , 21 , 10 , 10 )
 window . placeControl ( Icon , 0 , 0 , 100 , 50 )
 Previous . controlRight ( Next )
 Previous . controlUp ( Quit )
 window . connect ( Previous , I1i111I )
 window . connect ( Next , Kmm )
 Previous . setVisible ( False )
 window . setFocus ( Quit )
 Previous . controlRight ( Quit )
 Quit . controlLeft ( Previous )
 Quit . controlRight ( Next )
 Next . controlLeft ( Quit )
 window . connect ( Quit , window . close )
 window . doModal ( )
 del window
 if 65 - 65: Ii1I * KmKKmkmmKKmmmkK % Kmmmm / Kmkmk - KKmKmkmkmkKmkKK / i1iIIIiI1I
def Kmm ( ) :
 mmmkmmkmkmmkKmKm = int ( KmkKmkKKmkKmkKmk . getSetting ( 'pos' ) )
 KKKKmKKmmkKmk = int ( mmmkmmkmkmmkKmKm ) + 1
 KmkKmkKKmkKmkKmk . setSetting ( 'pos' , str ( KKKKmKKmmkKmk ) )
 mKmmmmk = len ( images )
 Icon . setImage ( images [ int ( KKKKmKKmmkKmk ) ] )
 Previous . setVisible ( True )
 if int ( KKKKmKKmmkKmk ) == int ( mKmmmmk ) - 1 :
  Next . setVisible ( False )
  if 58 - 58: mmmKmkmmmkmKKKK . mmKmmmkK + I1
def I1i111I ( ) :
 mmmkmmkmkmmkKmKm = int ( KmkKmkKKmkKmkKmk . getSetting ( 'pos' ) )
 KmkmkKK = int ( mmmkmmkmkmmkKmKm ) - 1
 KmkKmkKKmkKmkKmk . setSetting ( 'pos' , str ( KmkmkKK ) )
 Icon . setImage ( images [ int ( KmkmkKK ) ] )
 Next . setVisible ( True )
 if int ( KmkmkKK ) == 0 :
  Previous . setVisible ( False )
  if 17 - 17: i1iIIIiI1I / i1I1i1Ii11 + KmkKmkKmkKmkmkKmmK - i11iIiiIii . mmKmmmkK
def mmkKmmkmk ( gobble ) :
 gobble = gobble . replace ( '}' , '' ) . replace ( '{' , '' ) . replace ( ',' , '' ) . replace ( ']' , '' ) . replace ( '[' , '' )
 gobble = gobble + '=='
 gobble = gobble . decode ( 'base64' )
 return gobble
 if 95 - 95: i1iIIII % mmkmkmkmkmKmKmKmkm * i11iIiiIii % Kmkm - KmkKmkKmkKmkmkKmmK
def mmkmK ( link ) :
 try :
  KKmKmKm = re . compile ( '<layouttype>(.+?)</layouttype>' ) . findall ( link ) [ 0 ]
  if KKmKmKm == 'thumbnail' : xbmc . executebuiltin ( 'Container.SetViewMode(500)' )
  else : xbmc . executebuiltin ( 'Container.SetViewMode(50)' )
 except : pass
 if 98 - 98: mmKmmmkK
IIi1i11111 = KKmmmmkmKKmkK ( ) ; i1 = None ; mmkmKmKmkmkm = None ; mKmKmkmmkmkKKmk = None ; I11ii1IIiIi = None ; mKKmmmkmkKmkK = None
try : I11ii1IIiIi = urllib . unquote_plus ( IIi1i11111 [ "site" ] )
except : pass
try : i1 = urllib . unquote_plus ( IIi1i11111 [ "url" ] )
except : pass
try : mmkmKmKmkmkm = urllib . unquote_plus ( IIi1i11111 [ "name" ] )
except : pass
try : mKmKmkmmkmkKKmk = int ( IIi1i11111 [ "mode" ] )
except : pass
try : mKKmmmkmkKmkK = urllib . unquote_plus ( IIi1i11111 [ "iconimage" ] )
except : pass
try : II1 = urllib . unquote_plus ( IIi1i11111 [ "fanart" ] )
except : pass
if 68 - 68: KmKK * KmKK . I1Ii / i1I1ii1II1iII % Kmkm
try : i1i11I11 = urllib . unquote_plus ( [ "description" ] )
except : pass
if 10 - 10: Ii1I - KmKKmkmmKKmmmkK . I1
if mKmKmkmmkmkKKmk == None or i1 == None or len ( i1 ) < 1 : KmkmK ( )
elif mKmKmkmmkmkKKmk == 1 : KmkKKK ( mmkmKmKmkmkm , i1 , mKKmmmkmkKmkK , II1 )
elif mKmKmkmmkmkKKmk == 2 : KmkmmKmkKmmkmkm ( mmkmKmKmkmkm , i1 , mKKmmmkmkKmkK )
elif mKmKmkmmkmkKKmk == 3 : ii ( mmkmKmKmkmkm , i1 , mKKmmmkmkKmkK )
elif mKmKmkmmkmkKKmk == 4 : KKmmmmKmkKm ( mmkmKmKmkmkm , i1 , mKKmmmkmkKmkK )
elif mKmKmkmmkmkKKmk == 5 : mmKKKmkmkKmm ( )
elif mKmKmkmmkmkKKmk == 6 : I1III ( i1 , mKKmmmkmkKmkK )
elif mKmKmkmmkmkKKmk == 7 : mKmmKmmk ( i1 )
elif mKmKmkmmkmkKKmk == 8 : iiIiIIIiiI ( mmkmKmKmkmkm )
elif mKmKmkmmkmkKKmk == 9 : KmmKmkKmKKKK ( mmkmKmKmkmkm , i1 )
elif mKmKmkmmkmkKKmk == 10 : DOSCRAPER ( mmkmKmKmkmkm , i1 )
elif mKmKmkmmkmkKKmk == 11 : KmkKKmkK ( i1 )
elif mKmKmkmmkmkKKmk == 12 : iiI1IiI ( mmkmKmKmkmkm , i1 , mKKmmmkmkKmkK )
elif mKmKmkmmkmkKKmk == 13 : Ii1I1i ( i1 )
elif mKmKmkmmkmkKKmk == 14 : KmmKmk ( mmkmKmKmkmkm , i1 , mKKmmmkmkKmkK )
elif mKmKmkmmkmkKKmk == 15 : KmkKmKmmmkmkm ( i1 )
elif mKmKmkmmkmkKKmk == 16 : KmmmkmkmmkKmmm ( mmkmKmKmkmkm , i1 , mKKmmmkmkKmkK )
elif mKmKmkmmkmkKKmk == 17 : i1I1iI ( mmkmKmKmkmkm , i1 )
if 44 - 44: Kmkmk - I1Ii . mmkmkmkmkmKmKmKmkm . Kmkmk * I1
xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3
