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
if 59 - 59: I11i / Ii1I
def IiiIII111iI ( ) :
 KmkKmkKKmkKmkKmk . setSetting ( 'fav' , 'no' )
 if not os . path . exists ( IiIi11iIIi1Ii ) :
  os . mkdir ( IiIi11iIIi1Ii )
 IiII = iI1Ii11111iIi ( IiI )
 i1i1II = re . compile ( '<index>(.+?)</index>' ) . findall ( IiII ) [ 0 ]
 IiII = KmkmmmkKKmk ( i1i1II )
 I1i1iiI1 = re . compile ( 'name="(.+?)".+?rl="(.+?)".+?mg="(.+?)"' , re . DOTALL ) . findall ( IiII )
 for iiIIIII1i1iI , mmkmKmk , mmmkmk in I1i1iiI1 :
  if not 'XXX' in iiIIIII1i1iI :
   mmkmk ( iiIIIII1i1iI , mmkmKmk , 1 , mmmkmk , II1 )
  if 'XXX' in iiIIIII1i1iI :
   if I11i11Ii == 'true' :
    if mKmkmkmKm == '' :
     KmmkmKmkmmm = xbmcgui . Dialog ( )
     mmkmKmKmkmkm = KmmkmKmkmmm . yesno ( 'Adult Content' , 'You have opted to show adult content' , '' , 'Please set a password to prevent accidental access' , 'Cancel' , 'Lets Go' )
     if mmkmKmKmkmkm == 1 :
      i1 = xbmc . Keyboard ( '' , 'Set Password' )
      i1 . doModal ( )
      if ( i1 . isConfirmed ( ) ) :
       mKKmmmkmkKmkK = i1 . getText ( )
       KmkKmkKKmkKmkKmk . setSetting ( 'password' , mKKmmmkmkKmkK )
      mmkmk ( iiIIIII1i1iI , mmkmKmk , 1 , mmmkmk , II1 )
   if I11i11Ii == 'true' :
    if mKmkmkmKm <> '' :
     mmkmk ( iiIIIII1i1iI , mmkmKmk , 1 , mmmkmk , II1 )
     #addDir('Favourites',uktfavs,1,'http://ukturk.offshorepastebin.com/UKTurk/thumbs/new/Uk%20turk%20thumbnails%20favourites.jpg',fanart)
 mmkmk ( 'Search' , 'url' , 5 , 'http://ukturk.offshorepastebin.com/UKTurk/thumbs/new/Uk%20turk%20thumbnails%20search.jpg' , II1 )
 xbmc . executebuiltin ( 'Container.SetViewMode(500)' )
 if 15 - 15: I11iii11IIi
def Kmkmkmmkmmkmkmkmkmmkm ( name , url , iconimage ) :
 url = url . replace ( ' ' , '%20' )
 iconimage = iconimage . replace ( ' ' , '%20' )
 KmkKm = '<FAV><item>\n<title>' + name + '</title>\n<link>' + url + '</link>\n' + '<thumbnail>' + iconimage + '</thumbnail>\n</item></FAV>\n'
 mm = open ( KmmkK , 'a' )
 mm . write ( KmkKm )
 mm . close ( )
 if 33 - 33: I1I1i1 * mKmk / KKmmkmmk / KKmKmmmkmkmm - iI1 + KmKmmKKKK
def i11iiII ( name , url , iconimage ) :
 I1iiiiI1iII = None
 file = open ( KmmkK , 'r' )
 I1iiiiI1iII = file . read ( )
 IiIi11i = ''
 I1i1iiI1 = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( I1iiiiI1iII )
 for iIii1I111I11I in I1i1iiI1 :
  KmkKm = '\n<FAV><item>\n' + iIii1I111I11I + '</item>\n'
  if name in iIii1I111I11I :
   KmkKm = KmkKm . replace ( 'item' , ' ' )
  IiIi11i = IiIi11i + KmkKm
 file = open ( KmmkK , 'w' )
 file . truncate ( )
 file . write ( IiIi11i )
 file . close ( )
 xbmc . executebuiltin ( 'Container.Refresh' )
 if 72 - 72: KKmmKmkKKmm % iii11iII / iI111IiI111I + KmmKmKmkKm
def iiIIiIiIi ( name , url , iconimage , fanart ) :
 i1I11 = iI ( name )
 KmkKmkKKmkKmkKmk . setSetting ( 'tv' , i1I11 )
 if 'UKTurk.db' in url :
  file = open ( KmmkK , 'r' )
  IiII = file . read ( )
 else :
  IiII = KmkmmmkKKmk ( url )
 if '<FAV>' in IiII :
  KmkKmkKKmkKmkKmk . setSetting ( 'fav' , 'yes' )
 else : KmkKmkKKmkKmkKmk . setSetting ( 'fav' , 'no' )
 mmkKmkmkmmmm ( IiII )
 if 'Index' in url :
  Kmkmkm ( url )
 if 'XXX' in name : Kmkmk ( IiII )
 I1i1iiI1 = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( IiII )
 KKKmmk = str ( len ( I1i1iiI1 ) )
 KmkKmkKKmkKmkKmk . setSetting ( 'count' , KKKmmk )
 for i11I1 in I1i1iiI1 :
  try :
   if '<sportsdevil>' in i11I1 : Ii11Ii11I ( i11I1 , url )
   elif '<iptv>' in i11I1 : iI11i1I1 ( i11I1 )
   elif '<Image>' in i11I1 : mmkmmkKKKmkmmk ( i11I1 )
   elif '<text>' in i11I1 : mmKKKmmkmmmkKmk ( i11I1 )
   elif '<scraper>' in i11I1 : SCRAPER ( i11I1 )
   elif '<redirect>' in i11I1 : REDIRECT ( i11I1 )
   elif '<oktitle>' in i11I1 : mmk ( i11I1 )
   else : I11II1i ( i11I1 , url , iconimage )
  except : pass
  if 23 - 23: mKmkmmkmmm / IiiI11Iiiii / I1I1i / IIIii1I1 * iiiIi1i1I
def mmk ( item ) :
 iiIIIII1i1iI = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 mKKmkmkmKK = re . compile ( '<oktitle>(.+?)</oktitle>' ) . findall ( item ) [ 0 ]
 KmKm = re . compile ( '<line1>(.+?)</line1>' ) . findall ( item ) [ 0 ]
 iImmkmkK = re . compile ( '<line2>(.+?)</line2>' ) . findall ( item ) [ 0 ]
 KKKmkKKKmkmkmm = re . compile ( '<line3>(.+?)</line3>' ) . findall ( item ) [ 0 ]
 Iii111II = '##' + mKKmkmkmKK + '#' + KmKm + '#' + iImmkmkK + '#' + KKKmkKKKmkmkmm + '##'
 mmmkmk = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 iiii11I ( iiIIIII1i1iI , Iii111II , 17 , mmmkmk , II1 )
 if 96 - 96: iII1iIIIiIi % IIIii1I1 % KmmKmKmkKm / iiiIi1i1I / iii11iII % KmKmmKKKK
def iII1IIIiI1I1i ( name , url ) :
 KmkmmkKmm = re . compile ( '##(.+?)##' ) . findall ( url ) [ 0 ] . split ( '#' )
 KmmkmKmkmmm = xbmcgui . Dialog ( )
 KmmkmKmkmmm . ok ( KmkmmkKmm [ 0 ] , KmkmmkKmm [ 1 ] , KmkmmkKmm [ 2 ] , KmkmmkKmm [ 3 ] )
 if 56 - 56: iII1iIIIiIi . KmKmmKKKK * I1I1i . KmKmmKKKK
def mmKKKmmkmmmkKmk ( item ) :
 iiIIIII1i1iI = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 Iii111II = re . compile ( '<text>(.+?)</text>' ) . findall ( item ) [ 0 ]
 mmmkmk = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 iiii11I ( iiIIIII1i1iI , Iii111II , 9 , mmmkmk , II1 )
 if 72 - 72: I1I1i / I1I1i1 * KKmKmmmkmkmm - iiiIi1i1I
def KmmkKmkKmkmmKmkK ( name , url ) :
 IIIIii = iI1Ii11111iIi ( url )
 Kmkmmk ( name , IIIIii )
 if 71 - 71: KmmKmKmkKm + iII1iIIIiIi % i11iIiiIii + iii11iII - IIIii1I1
def mmkmmkKKKmkmmk ( item ) :
 mKmkKKmKmk = re . compile ( '<Image>(.+?)</Image>' ) . findall ( item )
 if len ( mKmkKKmKmk ) == 1 :
  iiIIIII1i1iI = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  mmmkmk = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  I111Ii111 = re . compile ( '<Image>(.+?)</Image>' ) . findall ( item ) [ 0 ]
  mmmkmk = I111Ii111 . replace ( 'http://imgur.com/' , 'http://i.imgur.com/' ) + '.jpg'
  I111Ii111 = I111Ii111 . replace ( 'http://imgur.com/' , 'http://i.imgur.com/' ) + '.jpg'
  iiii11I ( iiIIIII1i1iI , I111Ii111 , 7 , mmmkmk , II1 )
 elif len ( mKmkKKmKmk ) > 1 :
  iiIIIII1i1iI = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  mmmkmk = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  i111IiI1I = ''
  for I111Ii111 in mKmkKKmKmk :
   mmmkmk = I111Ii111 . replace ( 'http://imgur.com/' , 'http://i.imgur.com/' ) + '.jpg'
   I111Ii111 = I111Ii111 . replace ( 'http://imgur.com/' , 'http://i.imgur.com/' ) + '.jpg'
   i111IiI1I = i111IiI1I + '<Image>' + I111Ii111 + '</Image>'
  Kmk = IiIi11iIIi1Ii
  iiIIIII1i1iI = iI ( iiIIIII1i1iI )
  iII = os . path . join ( os . path . join ( Kmk , '' ) , iiIIIII1i1iI + '.txt' )
  if not os . path . exists ( iII ) : file ( iII , 'w' ) . close ( )
  mmkmmKmmmmkmkmkmKK = open ( iII , "w" )
  mmkmmKmmmmkmkmkmKK . write ( i111IiI1I )
  mmkmmKmmmmkmkmkmKK . close ( )
  iiii11I ( iiIIIII1i1iI , 'image' , 8 , mmmkmk , II1 )
  if 59 - 59: mKmk + I11iii11IIi * KmKmmKKKK + I1I1i1
def iI11i1I1 ( item ) :
 iiIIIII1i1iI = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 mmmkmk = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 mmkmKmk = re . compile ( '<iptv>(.+?)</iptv>' ) . findall ( item ) [ 0 ]
 mmkmk ( iiIIIII1i1iI , mmkmKmk , 6 , mmmkmk , II1 )
 if 58 - 58: mKmk * KmmKmKmkKm * iii11iII / KmmKmKmkKm
def mKmkmmkKKKK ( url , iconimage ) :
 IiII = iI1Ii11111iIi ( url )
 KmkKmkKmKKmk = re . compile ( '^#.+?:-?[0-9]*(.*?),(.*?)\n(.*?)$' , re . I + re . M + re . U + re . S ) . findall ( IiII )
 iiiI1I11i1 = [ ]
 for IIi1i11111 , iiIIIII1i1iI , url in KmkKmkKmKKmk :
  mmKKmkmkKmkmkmm = { "params" : IIi1i11111 , "name" : iiIIIII1i1iI , "url" : url }
  iiiI1I11i1 . append ( mmKKmkmkKmkmkmm )
 list = [ ]
 for I1ii11iI in iiiI1I11i1 :
  mmKKmkmkKmkmkmm = { "name" : I1ii11iI [ "name" ] , "url" : I1ii11iI [ "url" ] }
  KmkKmkKmKKmk = re . compile ( ' (.+?)="(.+?)"' , re . I + re . M + re . U + re . S ) . findall ( I1ii11iI [ "params" ] )
  for IIi1i , I1I1iIiII1 in KmkKmkKmKKmk :
   mmKKmkmkKmkmkmm [ IIi1i . strip ( ) . lower ( ) . replace ( '-' , '_' ) ] = I1I1iIiII1 . strip ( )
  list . append ( mmKKmkmkKmkmkmm )
 for I1ii11iI in list :
  if '.ts' in I1ii11iI [ "url" ] : iiii11I ( I1ii11iI [ "name" ] , I1ii11iI [ "url" ] , 2 , iconimage , II1 )
  else : i11i1I1 ( I1ii11iI [ "name" ] , I1ii11iI [ "url" ] , 2 , iconimage , II1 )
  if 36 - 36: Ii1I / KmKmmKKKK * KmmKmKmkKm
def I11II1i ( item , url , iconimage ) :
 Kmkii1ii1ii = iconimage
 mmmmmKmmmkmmm = url
 I1I1IiI1 = re . compile ( '<link>(.+?)</link>' ) . findall ( item )
 iIii1I111I11I = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>' , re . DOTALL ) . findall ( item )
 for iiIIIII1i1iI , III1iII1I1ii , iconimage in iIii1I111I11I :
  if 'youtube.com/playlist?' in III1iII1I1ii :
   mKKmmk = III1iII1I1ii . split ( 'list=' ) [ 1 ]
   mmkmk ( iiIIIII1i1iI , III1iII1I1ii , mmmkmkKmkmkmK , iconimage , II1 , description = mKKmmk )
 if len ( I1I1IiI1 ) == 1 :
  iiIIIII1i1iI = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  url = re . compile ( '<link>(.+?)</link>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  if iconimage == 'ImageHere' : iconimage = Kmkii1ii1ii
  if '.ts' in url : iiii11I ( iiIIIII1i1iI , url , 16 , iconimage , II1 , description = '' )
  elif 'movies' in mmmmmKmmmkmmm :
   iIiIIIi ( iiIIIII1i1iI , url , 2 , iconimage , int ( KKKmmk ) , isFolder = False )
  else : i11i1I1 ( iiIIIII1i1iI , url , 2 , iconimage , II1 )
 elif len ( I1I1IiI1 ) > 1 :
  iiIIIII1i1iI = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  if '.ts' in url : iiii11I ( iiIIIII1i1iI , url , 16 , iconimage , II1 , description = '' )
  elif 'movies' in mmmmmKmmmkmmm :
   iIiIIIi ( iiIIIII1i1iI , url , 2 , iconimage , int ( KKKmmk ) , isFolder = False )
  else : i11i1I1 ( iiIIIII1i1iI , url , 3 , iconimage , II1 )
  if 93 - 93: I1I1i
def Kmkmkm ( url ) :
 IiII = iI1Ii11111iIi ( url )
 I1i1iiI1 = re . compile ( 'name="(.+?)".+?rl="(.+?)".+?mg="(.+?)"' , re . DOTALL ) . findall ( IiII )
 for iiIIIII1i1iI , url , I1IiiI in I1i1iiI1 :
  if 'youtube.com/playlist?list=' in url :
   mmkmk ( iiIIIII1i1iI , url , 3 , I1IiiI , II1 )
  elif 'youtube.com/results?search_query=' in url :
   mmkmk ( iiIIIII1i1iI , url , 3 , I1IiiI , II1 )
  else :
   mmkmk ( iiIIIII1i1iI , url , 1 , I1IiiI , II1 )
   if 10 - 10: mKmkmmkmmm
def KKmmKKmkmkmk ( item ) :
 item = item . replace ( '\r' , '' ) . replace ( '\t' , '' ) . replace ( '&nbsp;' , '' ) . replace ( '\'' , '' ) . replace ( '\n' , '' )
 iIii1I111I11I = re . compile ( 'name="(.+?)".+?rl="(.+?)".+?mg="(.+?)"' , re . DOTALL ) . findall ( item )
 for iiIIIII1i1iI , mmkmKmk , mmmkmk in iIii1I111I11I :
  if 'youtube.com/channel/' in mmkmKmk :
   mKKmmk = mmkmKmk . split ( 'channel/' ) [ 1 ]
   mmkmk ( iiIIIII1i1iI , mmkmKmk , mmmkmkKmkmkmK , mmmkmk , II1 , description = mKKmmk )
  elif 'youtube.com/user/' in mmkmKmk :
   mKKmmk = mmkmKmk . split ( 'user/' ) [ 1 ]
   mmkmk ( iiIIIII1i1iI , mmkmKmk , mmmkmkKmkmkmK , mmmkmk , II1 , description = mKKmmk )
  elif 'youtube.com/playlist?' in mmkmKmk :
   mKKmmk = mmkmKmk . split ( 'list=' ) [ 1 ]
   mmkmk ( iiIIIII1i1iI , mmkmKmk , mmmkmkKmkmkmK , mmmkmk , II1 , description = mKKmmk )
  elif 'plugin://' in mmkmKmk :
   KKmKmm = HTMLParser ( )
   mmkmKmk = KKmKmm . unescape ( mmkmKmk )
   mmkmk ( iiIIIII1i1iI , mmkmKmk , mmmkmkKmkmkmK , mmmkmk , II1 )
  else :
   mmkmk ( iiIIIII1i1iI , mmkmKmk , 1 , mmmkmk , II1 )
   if 85 - 85: iii11iII % I1I1i % iII1iIIIiIi
def Ii11Ii11I ( item , url ) :
 I1I1IiI1 = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( item )
 KmmkmkmmmkmK = re . compile ( '<link>(.+?)</link>' ) . findall ( item )
 if len ( I1I1IiI1 ) + len ( KmmkmkmmmkmK ) == 1 :
  iiIIIII1i1iI = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  mmmkmk = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  url = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( item ) [ 0 ]
  IiII = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' + url
  iiii11I ( iiIIIII1i1iI , url , 16 , mmmkmk , II1 )
 elif len ( I1I1IiI1 ) + len ( KmmkmkmmmkmK ) > 1 :
  iiIIIII1i1iI = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  mmmkmk = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  iiii11I ( iiIIIII1i1iI , url , 3 , mmmkmk , II1 )
  if 1 - 1: iI1 - iI111IiI111I . mKmkmmkmmm . iI1 / KKmKmmmkmkmm + mKmkmmkmmm
def Kmkmk ( link ) :
 if mKmkmkmKm == '' :
  KmmkmKmkmmm = xbmcgui . Dialog ( )
  mmkmKmKmkmkm = KmmkmKmkmmm . yesno ( 'Adult Content' , 'You have opted to show adult content' , '' , 'Please set a password to prevent accidental access' , 'Cancel' , 'OK' )
  if mmkmKmKmkmkm == 1 :
   i1 = xbmc . Keyboard ( '' , 'Set Password' )
   i1 . doModal ( )
   if ( i1 . isConfirmed ( ) ) :
    mKKmmmkmkKmkK = i1 . getText ( )
    KmkKmkKKmkKmkKmk . setSetting ( 'password' , mKKmmmkmkKmkK )
  else : quit ( )
 elif mKmkmkmKm <> '' :
  KmmkmKmkmmm = xbmcgui . Dialog ( )
  mmkmKmKmkmkm = KmmkmKmkmmm . yesno ( 'Adult Content' , 'Please enter the password you set' , 'to continue' , '' , 'Cancel' , 'OK' )
  if mmkmKmKmkmkm == 1 :
   i1 = xbmc . Keyboard ( '' , 'Enter Password' )
   i1 . doModal ( )
   if ( i1 . isConfirmed ( ) ) :
    mKKmmmkmkKmkK = i1 . getText ( )
   if mKKmmmkmkKmkK <> mKmkmkmKm :
    quit ( )
  else : quit ( )
  if 78 - 78: I11i . iI111IiI111I . mKmk % KmmKmKmkKm
def i1iIi ( ) :
 i1 = xbmc . Keyboard ( '' , 'Search' )
 i1 . doModal ( )
 if ( i1 . isConfirmed ( ) ) :
  mKKmmk = i1 . getText ( )
  mKKmmk = mKKmmk . upper ( )
 else : quit ( )
 IiII = KmkmmmkKKmk ( IiI )
 mmKKmmmmmm = re . compile ( '<link>(.+?)</link>' ) . findall ( IiII )
 for mmkmKmk in mmKKmmmmmm :
  try :
   IiII = KmkmmmkKKmk ( mmkmKmk )
   II1I = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( IiII )
   for i11I1 in II1I :
    I1i1iiI1 = re . compile ( '<title>(.+?)</title>' ) . findall ( i11I1 )
    for Kmki1II1Iiii1I11 in I1i1iiI1 :
     Kmki1II1Iiii1I11 = Kmki1II1Iiii1I11 . upper ( )
     if mKKmmk in Kmki1II1Iiii1I11 :
      try :
       if 'Index' in mmkmKmk : Kmkmkm ( mmkmKmk )
       elif '<sportsdevil>' in i11I1 : Ii11Ii11I ( i11I1 , mmkmKmk )
       elif '<iptv>' in i11I1 : iI11i1I1 ( i11I1 )
       elif '<Image>' in i11I1 : mmkmmkKKKmkmmk ( i11I1 )
       elif '<text>' in i11I1 : mmKKKmmkmmmkKmk ( i11I1 )
       elif '<scraper>' in i11I1 : SCRAPER ( i11I1 )
       elif '<redirect>' in i11I1 : REDIRECT ( i11I1 )
       elif '<oktitle>' in i11I1 : mmk ( i11I1 )
       else : I11II1i ( i11I1 , mmkmKmk , mmmkmk )
      except : pass
  except : pass
  if 9 - 9: iii11iII / KKmKmmmkmkmm - KKmmkmmk / I11iii11IIi / Ii1I - KKmmKmkKKmm
def mmkmkmmmKmkKm ( name , url , iconimage ) :
 mmkKmkKKKmkKmm = [ ]
 iiIiI = [ ]
 I1 = [ ]
 IiII = KmkmmmkKKmk ( url )
 KKKmkmkKmkK = re . compile ( '<title>' + re . escape ( name ) + '</title>(.+?)</item>' , re . DOTALL ) . findall ( IiII ) [ 0 ]
 iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( KKKmkmkKmkK ) [ 0 ]
 I1I1IiI1 = [ ]
 if '<link>' in KKKmkmkKmkK :
  iii = re . compile ( '<link>(.+?)</link>' ) . findall ( KKKmkmkKmkK )
  for mKmmKKKmKm in iii :
   I1I1IiI1 . append ( mKmmKKKmKm )
 if '<sportsdevil>' in KKKmkmkKmkK :
  i1Iii1i1I = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( KKKmkmkKmkK )
  for KKmKmkmk in i1Iii1i1I :
   KKmKmkmk = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' + KKmKmkmk
   I1I1IiI1 . append ( KKmKmkmk )
 IiI111111IIII = 1
 for i1Ii in I1I1IiI1 :
  ii111iI1iIi1 = i1Ii
  if '(' in i1Ii :
   i1Ii = i1Ii . split ( '(' ) [ 0 ]
   KKK = str ( ii111iI1iIi1 . split ( '(' ) [ 1 ] . replace ( ')' , '' ) )
   mmkKmkKKKmkKmm . append ( i1Ii )
   iiIiI . append ( KKK )
  else :
   mmmkKKmmk = i1Ii . split ( '/' ) [ 2 ] . replace ( 'www.' , '' )
   mmkKmkKKKmkKmm . append ( i1Ii )
   iiIiI . append ( 'Link ' + str ( IiI111111IIII ) )
  IiI111111IIII = IiI111111IIII + 1
 KmmkmKmkmmm = xbmcgui . Dialog ( )
 I11IiI = KmmkmKmkmmm . select ( name , iiIiI )
 if I11IiI < 0 : quit ( )
 else :
  url = mmkKmkKKKmkKmm [ I11IiI ]
  KmkmmKmkKmmkmkm ( name , url , iconimage )
  if 77 - 77: Ii1I * iI1
def mKmmKmmk ( url ) :
 KmkKm = "ShowPicture(%s)" % url
 xbmc . executebuiltin ( KmkKm )
 if 38 - 38: iiiIi1i1I
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
  KK ( iIiIIi1 ( 'UKTurk' ) , 'Stream Unavailable' , '3000' , I1IiiI )
  if 7 - 7: iII1iIIIiIi - KKmKmmmkmkmm - iI111IiI111I + iII1iIIIiIi
def iI1I11iiI1i ( url ) :
 if urlresolver . HostedMediaFile ( url ) . valid_url ( ) :
  url = urlresolver . HostedMediaFile ( url ) . resolve ( )
 xbmc . Player ( ) . play ( url )
 if 78 - 78: iI111IiI111I % I11i % IiiI11Iiiii
def KKmmmmKmkKm ( name , url , iconimage ) :
 ii = True
 I1Ii1iI1 = xbmcgui . ListItem ( name , iconImage = iconimage , thumbnailImage = iconimage ) ; I1Ii1iI1 . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
 ii = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = url , listitem = I1Ii1iI1 )
 I1Ii1iI1 . setPath ( url )
 xbmcplugin . setResolvedUrl ( int ( sys . argv [ 1 ] ) , True , I1Ii1iI1 )
 if 87 - 87: KKmKmmmkmkmm . IIIii1I1
def KmmmkmkmmkKmmm ( name , url , iconimage ) :
 ii = True
 I1Ii1iI1 = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage ) ; I1Ii1iI1 . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
 ii = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = url , listitem = I1Ii1iI1 )
 xbmc . Player ( ) . play ( url , I1Ii1iI1 , False )
 if 75 - 75: iII1iIIIiIi + KmKmmKKKK + KKmmKmkKKmm * mKmkmmkmmm % iI111IiI111I . I1I1i
def mK ( url ) :
 xbmc . executebuiltin ( "PlayMedia(%s)" % url )
 if 31 - 31: KmmKmKmkKm + i11iIiiIii + KKmKmmmkmkmm * iII1iIIIiIi
def IiII111iI1ii1 ( url ) :
 iI11I1II = KmkKmkKKmkKmkKmk . getSetting ( 'layout' )
 if iI11I1II == 'Listers' : KmkKmkKKmkKmkKmk . setSetting ( 'layout' , 'Category' )
 else : KmkKmkKKmkKmkKmk . setSetting ( 'layout' , 'Listers' )
 xbmc . executebuiltin ( 'Container.Refresh' )
 if 40 - 40: Ii1I / KmKmmKKKK % iii11iII + mKmk
def KmkmmmkKKmk ( url ) :
 ii1Ii1I1Ii11i = urllib2 . Request ( url )
 ii1Ii1I1Ii11i . add_header ( 'User-Agent' , 'mat' )
 i1111I1I = urllib2 . urlopen ( ii1Ii1I1Ii11i )
 IiII = i1111I1I . read ( )
 i1111I1I . close ( )
 IiII = IiII . replace ( '</fanart>' , '<fanart>x</fanart>' ) . replace ( '<thumbnail></thumbnail>' , '<thumbnail>x</thumbnail>' ) . replace ( '<utube>' , '<link>https://www.youtube.com/watch?v=' ) . replace ( '</utube>' , '</link>' )
 if '{' in IiII : IiII = i1i ( IiII )
 return IiII
 if 56 - 56: iii11iII % I11i - KKmmkmmk
def iI1Ii11111iIi ( url ) :
 ii1Ii1I1Ii11i = urllib2 . Request ( url )
 ii1Ii1I1Ii11i . add_header ( 'User-Agent' , 'mat' )
 i1111I1I = urllib2 . urlopen ( ii1Ii1I1Ii11i )
 IiII = i1111I1I . read ( )
 i1111I1I . close ( )
 return IiII
 if 100 - 100: IiiI11Iiiii - I11i % iI111IiI111I * KmmKmKmkKm + KKmmkmmk
 if 88 - 88: I11iii11IIi - iI1 * I11i * I11iii11IIi . I11iii11IIi
def I111iI ( ) :
 mKKmmkII1I1iiIII = [ ]
 mKKmmkKmkmkm = sys . argv [ 2 ]
 if len ( mKKmmkKmkmkm ) >= 2 :
  IIi1i11111 = sys . argv [ 2 ]
  iIiIi11 = IIi1i11111 . replace ( '?' , '' )
  if ( IIi1i11111 [ len ( IIi1i11111 ) - 1 ] == '/' ) :
   IIi1i11111 = IIi1i11111 [ 0 : len ( IIi1i11111 ) - 2 ]
  KKKiiiiI = iIiIi11 . split ( '&' )
  mKKmmkII1I1iiIII = { }
  for IiI111111IIII in range ( len ( KKKiiiiI ) ) :
   mmmKmmkKKKmmmk = { }
   mmmKmmkKKKmmmk = KKKiiiiI [ IiI111111IIII ] . split ( '=' )
   if ( len ( mmmKmmkKKKmmmk ) ) == 2 :
    mKKmmkII1I1iiIII [ mmmKmmkKKKmmmk [ 0 ] ] = mmmKmmkKKKmmmk [ 1 ]
 return mKKmmkII1I1iiIII
 if 51 - 51: KKmKmmmkmkmm / KmKmmKKKK . KmmKmKmkKm * KKmmKmkKKmm + iI1 * IIIii1I1
def KK ( title , message , ms , nart ) :
 xbmc . executebuiltin ( "XBMC.notification(" + title + "," + message + "," + ms + "," + nart + ")" )
 if 73 - 73: iI1 + I11iii11IIi - I11i - IiiI11Iiiii - mKmk
def iI ( string ) :
 KmkK = re . compile ( '\[(.+?)\]' ) . findall ( string )
 for mmkmKKmmmKKKKm in KmkK : string = string . replace ( mmkmKKmmmKKKKm , '' ) . replace ( '[/]' , '' ) . replace ( '[]' , '' )
 return string
 if 62 - 62: iII1iIIIiIi
def iIiIIi1 ( string ) :
 string = string . split ( ' ' )
 mmkKmkmmk = ''
 for II111iI111I1I in string :
  I1i1i1iii = '[B][COLOR red]' + II111iI111I1I [ 0 ] . upper ( ) + '[/COLOR][COLOR white]' + II111iI111I1I [ 1 : ] + '[/COLOR][/B] '
  mmkKmkmmk = mmkKmkmmk + I1i1i1iii
 return mmkKmkmmk
 if 16 - 16: IiiI11Iiiii + IIIii1I1 * I11i % I1I1i1 . KKmmkmmk
def iIiIIIi ( name , url , mode , iconimage , itemcount , isFolder = False ) :
 if Kmmmmkmkmkm == 'true' :
  if not 'COLOR' in name :
   KmmkKK = name . partition ( '(' )
   KmkKmmKmmkm = ""
   iiI11ii1I1 = ""
   if len ( KmmkKK ) > 0 :
    KmkKmmKmmkm = KmmkKK [ 0 ]
    iiI11ii1I1 = KmmkKK [ 2 ] . partition ( ')' )
   if len ( iiI11ii1I1 ) > 0 :
    iiI11ii1I1 = iiI11ii1I1 [ 0 ]
   KmmmkKKmKmKmk = eval ( base64 . b64decode ( 'bWV0YWhhbmRsZXJzLk1ldGFEYXRhKHRtZGJfYXBpX2tleT0iZDk1NWQ4ZjAyYTNmMjQ4MGE1MTg4MWZlNGM5NmYxMGUiKQ==' ) )
   mKmmkKKmKmk = KmmmkKKmKmKmk . get_meta ( 'movie' , name = KmkKmmKmmkm , year = iiI11ii1I1 )
   II = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&site=" + str ( mmkKmmkmKmkmKKmkmk ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name )
   ii = True
   I1Ii1iI1 = xbmcgui . ListItem ( name , iconImage = mKmmkKKmKmk [ 'cover_url' ] , thumbnailImage = mKmmkKKmKmk [ 'cover_url' ] )
   I1Ii1iI1 . setInfo ( type = "Video" , infoLabels = mKmmkKKmKmk )
   I1Ii1iI1 . setProperty ( "IsPlayable" , "true" )
   mmmkmkKKmkmkmkmkmK = [ ]
   if KmkKmkKKmkKmkKmk . getSetting ( 'fav' ) == 'yes' : mmmkmkKKmkmkmkmkmK . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
   if KmkKmkKKmkKmkKmk . getSetting ( 'fav' ) == 'no' : mmmkmkKKmkmkmkmkmK . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
   I1Ii1iI1 . addContextMenuItems ( mmmkmkKKmkmkmkmkmK , replaceItems = False )
   if not mKmmkKKmKmk [ 'backdrop_url' ] == '' : I1Ii1iI1 . setProperty ( 'fanart_image' , mKmmkKKmKmk [ 'backdrop_url' ] )
   else : I1Ii1iI1 . setProperty ( 'fanart_image' , II1 )
   ii = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = II , listitem = I1Ii1iI1 , isFolder = isFolder , totalItems = itemcount )
   return ii
 else :
  II = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&site=" + str ( mmkKmmkmKmkmKKmkmk ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name )
  ii = True
  I1Ii1iI1 = xbmcgui . ListItem ( name , iconImage = iconimage , thumbnailImage = iconimage )
  I1Ii1iI1 . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
  I1Ii1iI1 . setProperty ( 'fanart_image' , II1 )
  I1Ii1iI1 . setProperty ( "IsPlayable" , "true" )
  mmmkmkKKmkmkmkmkmK = [ ]
  if KmkKmkKKmkKmkKmk . getSetting ( 'fav' ) == 'yes' : mmmkmkKKmkmkmkmkmK . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
  if KmkKmkKKmkKmkKmk . getSetting ( 'fav' ) == 'no' : mmmkmkKKmkmkmkmkmK . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
  I1Ii1iI1 . addContextMenuItems ( mmmkmkKKmkmkmkmkmK , replaceItems = False )
  ii = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = II , listitem = I1Ii1iI1 , isFolder = isFolder )
  return ii
  if 11 - 11: iII1iIIIiIi / KmKmmKKKK - IIIii1I1 * I11iii11IIi + I11iii11IIi . KmKmmKKKK
def mmkmk ( name , url , mode , iconimage , fanart , description = '' ) :
 II = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&fanart=" + urllib . quote_plus ( fanart ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 ii = True
 I1Ii1iI1 = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 I1Ii1iI1 . setInfo ( type = "Video" , infoLabels = { "Title" : name , 'plot' : description } )
 I1Ii1iI1 . setProperty ( 'fanart_image' , fanart )
 mmmkmkKKmkmkmkmkmK = [ ]
 if KmkKmkKKmkKmkKmk . getSetting ( 'fav' ) == 'yes' : mmmkmkKKmkmkmkmkmK . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 if KmkKmkKKmkKmkKmk . getSetting ( 'fav' ) == 'no' : mmmkmkKKmkmkmkmkmK . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 I1Ii1iI1 . addContextMenuItems ( mmmkmkKKmkmkmkmkmK , replaceItems = False )
 if 'youtube.com/channel/' in url :
  II = 'plugin://plugin.video.youtube/channel/' + description + '/'
 if 'youtube.com/user/' in url :
  II = 'plugin://plugin.video.youtube/user/' + description + '/'
 if 'youtube.com/playlist?' in url :
  II = 'plugin://plugin.video.youtube/playlist/' + description + '/'
 if 'plugin://' in url :
  II = url
 ii = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = II , listitem = I1Ii1iI1 , isFolder = True )
 return ii
 if 26 - 26: IiiI11Iiiii % iii11iII
def iiii11I ( name , url , mode , iconimage , fanart , description = '' ) :
 II = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 ii = True
 I1Ii1iI1 = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 I1Ii1iI1 . setProperty ( 'fanart_image' , fanart )
 mmmkmkKKmkmkmkmkmK = [ ]
 if KmkKmkKKmkKmkKmk . getSetting ( 'fav' ) == 'yes' : mmmkmkKKmkmkmkmkmK . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 if KmkKmkKKmkKmkKmk . getSetting ( 'fav' ) == 'no' : mmmkmkKKmkmkmkmkmK . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 I1Ii1iI1 . addContextMenuItems ( mmmkmkKKmkmkmkmkmK , replaceItems = False )
 ii = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = II , listitem = I1Ii1iI1 , isFolder = False )
 return ii
 if 76 - 76: IIIii1I1 * I1I1i
def i11i1I1 ( name , url , mode , iconimage , fanart , description = '' ) :
 II = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 ii = True
 I1Ii1iI1 = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 I1Ii1iI1 . setProperty ( 'fanart_image' , fanart )
 I1Ii1iI1 . setProperty ( "IsPlayable" , "true" )
 mmmkmkKKmkmkmkmkmK = [ ]
 if KmkKmkKKmkKmkKmk . getSetting ( 'fav' ) == 'yes' : mmmkmkKKmkmkmkmkmK . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 if KmkKmkKKmkKmkKmk . getSetting ( 'fav' ) == 'no' : mmmkmkKKmkmkmkmkmK . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 I1Ii1iI1 . addContextMenuItems ( mmmkmkKKmkmkmkmkmK , replaceItems = False )
 ii = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = II , listitem = I1Ii1iI1 , isFolder = False )
 return ii
 if 52 - 52: KmmKmKmkKm
def iiii1 ( url , name ) :
 mmKmkmmmKKmk = iI1Ii11111iIi ( url )
 if len ( mmKmkmmmKKmk ) > 1 :
  Kmk = IiIi11iIIi1Ii
  iII = os . path . join ( os . path . join ( Kmk , '' ) , name + '.txt' )
  if not os . path . exists ( iII ) :
   file ( iII , 'w' ) . close ( )
  mmkm = open ( iII )
  mmmk = mmkm . read ( )
  if mmmk == mmKmkmmmKKmk : pass
  else :
   Kmkmmk ( 'UKTurk' , mmKmkmmmKKmk )
   mmkmmKmmmmkmkmkmKK = open ( iII , "w" )
   mmkmmKmmmmkmkmkmKK . write ( mmKmkmmmKKmk )
   mmkmmKmmmmkmkmkmKK . close ( )
   if 61 - 61: KmKmmKKKK - KmmKmKmkKm - I1I1i1
def Kmkmmk ( heading , text ) :
 id = 10147
 xbmc . executebuiltin ( 'ActivateWindow(%d)' % id )
 xbmc . sleep ( 500 )
 IiI1iIiIIIii = xbmcgui . Window ( id )
 mKmK = 50
 while ( mKmK > 0 ) :
  try :
   xbmc . sleep ( 10 )
   mKmK -= 1
   IiI1iIiIIIii . getControl ( 1 ) . setLabel ( heading )
   IiI1iIiIIIii . getControl ( 5 ) . setText ( text )
   return
  except :
   pass
   if 81 - 81: KmKmmKKKK - KmKmmKKKK . I1I1i
def mmkKmKmmkmkmmkm ( name ) :
 global Icon
 global Next
 global Previous
 global window
 global Quit
 global images
 iII = os . path . join ( os . path . join ( IiIi11iIIi1Ii , '' ) , name + '.txt' )
 mmkm = open ( iII )
 mmmk = mmkm . read ( )
 images = re . compile ( '<image>(.+?)</image>' ) . findall ( mmmk )
 KmkKmkKKmkKmkKmk . setSetting ( 'pos' , '0' )
 window = pyxbmct . AddonDialogWindow ( '' )
 I1II1I11I1I = '/resources/art'
 KmKKmkm = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + KKmkm + I1II1I11I1I , 'next_focus.png' ) )
 i1II1 = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + KKmkm + I1II1I11I1I , 'next1.png' ) )
 i11i1 = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + KKmkm + I1II1I11I1I , 'previous_focus.png' ) )
 IiiiiI1i1Iii = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + KKmkm + I1II1I11I1I , 'previous.png' ) )
 mmmkmkmKmkm = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + KKmkm + I1II1I11I1I , 'close_focus.png' ) )
 iiii111II = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + KKmkm + I1II1I11I1I , 'close.png' ) )
 I11iIiI1I1i11 = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + KKmkm + I1II1I11I1I , 'main-bg1.png' ) )
 window . setGeometry ( 1300 , 720 , 100 , 50 )
 KKmmmKmkmkmmkmmmk = pyxbmct . Image ( I11iIiI1I1i11 )
 window . placeControl ( KKmmmKmkmkmmkmmmk , - 10 , - 10 , 130 , 70 )
 Iii111II = '0xFF000000'
 Previous = pyxbmct . Button ( '' , focusTexture = i11i1 , noFocusTexture = IiiiiI1i1Iii , textColor = Iii111II , focusedColor = Iii111II )
 Next = pyxbmct . Button ( '' , focusTexture = KmKKmkm , noFocusTexture = i1II1 , textColor = Iii111II , focusedColor = Iii111II )
 Quit = pyxbmct . Button ( '' , focusTexture = mmmkmkmKmkm , noFocusTexture = iiii111II , textColor = Iii111II , focusedColor = Iii111II )
 Icon = pyxbmct . Image ( images [ 0 ] , aspectRatio = 1 )
 window . placeControl ( Previous , 102 , 1 , 10 , 10 )
 window . placeControl ( Next , 102 , 40 , 10 , 10 )
 window . placeControl ( Quit , 102 , 21 , 10 , 10 )
 window . placeControl ( Icon , 0 , 0 , 100 , 50 )
 Previous . controlRight ( Next )
 Previous . controlUp ( Quit )
 window . connect ( Previous , KmkmkK )
 window . connect ( Next , I1i11 )
 Previous . setVisible ( False )
 window . setFocus ( Quit )
 Previous . controlRight ( Quit )
 Quit . controlLeft ( Previous )
 Quit . controlRight ( Next )
 Next . controlLeft ( Quit )
 window . connect ( Quit , window . close )
 window . doModal ( )
 del window
 if 12 - 12: I1I1i1 + I1I1i1 - iii11iII * KKmKmmmkmkmm % KKmKmmmkmkmm - mKmk
def I1i11 ( ) :
 mmkK = int ( KmkKmkKKmkKmkKmk . getSetting ( 'pos' ) )
 KKKmmm = int ( mmkK ) + 1
 KmkKmkKKmkKmkKmk . setSetting ( 'pos' , str ( KKKmmm ) )
 KmmKmkKK = len ( images )
 Icon . setImage ( images [ int ( KKKmmm ) ] )
 Previous . setVisible ( True )
 if int ( KKKmmm ) == int ( KmmKmkKK ) - 1 :
  Next . setVisible ( False )
  if 69 - 69: iII1iIIIiIi % iI111IiI111I
def KmkmkK ( ) :
 mmkK = int ( KmkKmkKKmkKmkKmk . getSetting ( 'pos' ) )
 ii1I1IIii11 = int ( mmkK ) - 1
 KmkKmkKKmkKmkKmk . setSetting ( 'pos' , str ( ii1I1IIii11 ) )
 Icon . setImage ( images [ int ( ii1I1IIii11 ) ] )
 Next . setVisible ( True )
 if int ( ii1I1IIii11 ) == 0 :
  Previous . setVisible ( False )
  if 67 - 67: I1I1i + mKmkmmkmmm / KKmmKmkKKmm . iI111IiI111I + KmmKmKmkKm
def i1i ( gobble ) :
 gobble = gobble . replace ( '}' , '' ) . replace ( '{' , '' ) . replace ( ',' , '' ) . replace ( ']' , '' ) . replace ( '[' , '' )
 gobble = gobble + '=='
 gobble = gobble . decode ( 'base64' )
 return gobble
 if 62 - 62: i11iIiiIii + i11iIiiIii - KKmmKmkKKmm
def mmkKmkmkmmmm ( link ) :
 try :
  I1KmmmmKmkmKKKK = re . compile ( '<layouttype>(.+?)</layouttype>' ) . findall ( link ) [ 0 ]
  if I1KmmmmKmkmKKKK == 'thumbnail' : xbmc . executebuiltin ( 'Container.SetViewMode(500)' )
  else : xbmc . executebuiltin ( 'Container.SetViewMode(50)' )
 except : pass
 if 100 - 100: I1I1i % KmmKmKmkKm
IIi1i11111 = I111iI ( ) ; mmkmKmk = None ; iiIIIII1i1iI = None ; mmmkmkKmkmkmK = None ; mmkKmmkmKmkmKKmkmk = None ; mmmkmk = None
try : mmkKmmkmKmkmKKmkmk = urllib . unquote_plus ( IIi1i11111 [ "site" ] )
except : pass
try : mmkmKmk = urllib . unquote_plus ( IIi1i11111 [ "url" ] )
except : pass
try : iiIIIII1i1iI = urllib . unquote_plus ( IIi1i11111 [ "name" ] )
except : pass
try : mmmkmkKmkmkmK = int ( IIi1i11111 [ "mode" ] )
except : pass
try : mmmkmk = urllib . unquote_plus ( IIi1i11111 [ "iconimage" ] )
except : pass
try : II1 = urllib . unquote_plus ( IIi1i11111 [ "fanart" ] )
except : pass
if 86 - 86: KKmKmmmkmkmm . I11i - I11iii11IIi . iI1 + IiiI11Iiiii
try : KKm = urllib . unquote_plus ( [ "description" ] )
except : pass
if 22 - 22: KmKmmKKKK * I11i . IIIii1I1 * i11iIiiIii - KKmmkmmk * iII1iIIIiIi
if mmmkmkKmkmkmK == None or mmkmKmk == None or len ( mmkmKmk ) < 1 : IiiIII111iI ( )
elif mmmkmkKmkmkmK == 1 : iiIIiIiIi ( iiIIIII1i1iI , mmkmKmk , mmmkmk , II1 )
elif mmmkmkKmkmkmK == 2 : KmkmmKmkKmmkmkm ( iiIIIII1i1iI , mmkmKmk , mmmkmk )
elif mmmkmkKmkmkmK == 3 : mmkmkmmmKmkKm ( iiIIIII1i1iI , mmkmKmk , mmmkmk )
elif mmmkmkKmkmkmK == 4 : KKmmmmKmkKm ( iiIIIII1i1iI , mmkmKmk , mmmkmk )
elif mmmkmkKmkmkmK == 5 : i1iIi ( )
elif mmmkmkKmkmkmK == 6 : mKmkmmkKKKK ( mmkmKmk , mmmkmk )
elif mmmkmkKmkmkmK == 7 : mKmmKmmk ( mmkmKmk )
elif mmmkmkKmkmkmK == 8 : mmkKmKmmkmkmmkm ( iiIIIII1i1iI )
elif mmmkmkKmkmkmK == 9 : KmmkKmkKmkmmKmkK ( iiIIIII1i1iI , mmkmKmk )
elif mmmkmkKmkmkmK == 10 : DOSCRAPER ( iiIIIII1i1iI , mmkmKmk )
elif mmmkmkKmkmkmK == 11 : mK ( mmkmKmk )
elif mmmkmkKmkmkmK == 12 : Kmkmkmmkmmkmkmkmkmmkm ( iiIIIII1i1iI , mmkmKmk , mmmkmk )
elif mmmkmkKmkmkmK == 13 : IiII111iI1ii1 ( mmkmKmk )
elif mmmkmkKmkmkmK == 14 : i11iiII ( iiIIIII1i1iI , mmkmKmk , mmmkmk )
elif mmmkmkKmkmkmK == 16 : KmmmkmkmmkKmmm ( iiIIIII1i1iI , mmkmKmk , mmmkmk )
elif mmmkmkKmkmkmK == 17 : iII1IIIiI1I1i ( iiIIIII1i1iI , mmkmKmk )
if 59 - 59: KKmKmmmkmkmm % I11iii11IIi . I1I1i / IIIii1I1 + KKmmkmmk
xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3
