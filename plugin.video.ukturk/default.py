import xbmc , xbmcaddon , xbmcgui , xbmcplugin , urllib , urllib2 , os , re , sys , urlresolver , random , glob
from resources . libs . common_addon import Addon
from resources . libs import net
from metahandler import metahandlers
net = net . Net ( )
if 64 - 64: i11iIiiIii
KKmkm = 'plugin.video.ukturk'
KmmkKmm = xbmcaddon . Addon ( id = KKmkm )
KmkKmkKKmkKmkKmk = Addon ( KKmkm , sys . argv )
iiiii = xbmc . translatePath ( 'special://home/addons/' ) + '/*.*'
mmmmkKK = xbmc . translatePath ( 'special://home/addons/' )
II1 = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + KKmkm , 'fanart.jpg' ) )
Kmkmkmmmmmmkmk = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + KKmkm , 'icon.png' ) )
I1IiiI = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + KKmkm , 'search.png' ) )
IIi1IiiiI1Ii = KmmkKmm . getSetting ( 'adult' )
I11i11Ii = KmmkKmm . getSetting ( 'password' )
mKmkmkmKm = KmkKmkKKmkKmkKmk . queries . get ( 'iconimage' , '' )
KKKmmk = KmmkKmm . getSetting ( 'enable_meta' )
Kmmmmkmkmkm = xbmc . translatePath ( os . path . join ( 'special://home/userdata/Database' , 'UKTurk.db' ) )
IiIi11iIIi1Ii = 'https://www.googleapis.com/youtube/v3/search?q='
KmmkK = '&regionCode=US&part=snippet&hl=en_US&key=AIzaSyAd-YEOqZz9nXVzGtn3KWzYLbLaajhqIDA&type=video&maxResults=50'
IiI = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId='
mmKm = '&maxResults=50&key=AIzaSyAd-YEOqZz9nXVzGtn3KWzYLbLaajhqIDA'
Km = 'http://ukturk.offshorepastebin.com/ukturk.jpg'
if 67 - 67: KmkmkmmKK . I1iII1iiII
def iI1Ii11111iIi ( ) :
 i1i1II = xbmc . Keyboard ( '' , 'Search UK Turk' )
 i1i1II . doModal ( )
 if ( i1i1II . isConfirmed ( ) ) :
  KmkmmmkKKmk = i1i1II . getText ( )
  KmkmmmkKKmk = KmkmmmkKKmk . upper ( )
 else : quit ( )
 I1i1iiI1 = iiIIIII1i1iI ( Km )
 mmkmKmk = re . compile ( '<link>(.+?)</link>' ) . findall ( I1i1iiI1 )
 for mmmkmk in mmkmKmk :
  I1i1iiI1 = mmkmk ( mmmkmk )
  KmmkmKmkmmm = re . compile ( 'name="(.+?)".+?url="(.+?)".+?img="(.+?)"' , re . DOTALL ) . findall ( I1i1iiI1 )
  if len ( KmmkmKmkmmm ) > 0 :
   for mmkmKmKmkmkm , i1 , mKKmmmkmkKmkK in KmmkmKmkmmm :
    if 'ImageH' in mKKmmmkmkKmkK : mKKmmmkmkKmkK = I1IiiI
    i1111 = mmkmKmKmkmkm
    mmkmKmKmkmkm = mmkmKmKmkmkm . upper ( )
    if KmkmmmkKKmk in mmkmKmKmkmkm and not 'COLOR' in mmkmKmKmkmkm :
     if 'txt' in i1 :
      i11 ( i1111 , i1 , 3 , mKKmmmkmkKmkK , II1 )
     elif 'youtube.com/playlist?list=' in i1 :
      i11 ( i1111 , i1 , 3 , mKKmmmkmkKmkK , II1 )
     elif 'youtube.com/results?search_query=' in i1 :
      i11 ( i1111 , i1 , 3 , mKKmmmkmkKmkK , II1 )
     else : I11 ( i1111 , i1 , 3 , mKKmmmkmkKmkK , II1 )
  else :
   Kmmkmmkmkmkmkmmkmmk = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?humbnail>(.+?)</thumbnail>' , re . DOTALL ) . findall ( I1i1iiI1 )
   if len ( Kmmkmmkmkmkmkmmkmmk ) > 0 :
    for mmkmKmKmkmkm , i1 , mKKmmmkmkKmkK in Kmmkmmkmkmkmkmmkmmk :
     if 'ImageH' in mKKmmmkmkKmkK : mKKmmmkmkKmkK = I1IiiI
     if not 'http' in i1 : pass
     i1111 = mmkmKmKmkmkm
     mmkmKmKmkmkm = mmkmKmKmkmkm . upper ( )
     if KmkmmmkKKmk in mmkmKmKmkmkm and not 'COLOR' in mmkmKmKmkmkm :
      if 'txt' in i1 :
       i11 ( i1111 , i1 , 3 , mKKmmmkmkKmkK , II1 )
      elif 'youtube.com/playlist?list=' in i1 :
       i11 ( i1111 , i1 , 3 , mKKmmmkmkKmkK , II1 )
      elif 'youtube.com/results?search_query=' in i1 :
       i11 ( i1111 , i1 , 3 , mKKmmmkmkKmkK , II1 )
      else : I11 ( i1111 , i1 , 3 , mKKmmmkmkKmkK , II1 )
      if 86 - 86: iiiii11iII1 % Kmkm
def mKmk ( name , url , iconimage ) :
 url = url . replace ( ' ' , '%20' )
 iconimage = iconimage . replace ( ' ' , '%20' )
 IIIi1i1I = '<FAV><item>\n<title>' + name + '</title>\n<link>' + url + '</link>\n' + '<Thumbnail>' + iconimage + '</thumbnail>\n</item></FAV>\n'
 KKmKmmmkmkmm = open ( Kmmmmkmkmkm , 'a' )
 KKmKmmmkmkmm . write ( IIIi1i1I )
 KKmKmmmkmkmm . close ( )
 if 41 - 41: i11IiIiiIIIII / IiiIII111ii / i1iIIi1
def ii11iIi1I ( name , url , iconimage ) :
 iI111I11I1I1 = None
 file = open ( Kmmmmkmkmkm , 'r' )
 iI111I11I1I1 = file . read ( )
 KKmmKmkKKmm = ''
 KmmkmKmkmmm = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( iI111I11I1I1 )
 for iIii1 in KmmkmKmkmmm :
  IIIi1i1I = '\n<FAV><item>\n' + iIii1 + '</item>\n'
  if name in iIii1 :
   IIIi1i1I = IIIi1i1I . replace ( 'item' , ' ' )
  KKmmKmkKKmm = KKmmKmkKKmm + IIIi1i1I
 file = open ( Kmmmmkmkmkm , 'w' )
 file . truncate ( )
 file . write ( KKmmKmkKKmm )
 file . close ( )
 xbmc . executebuiltin ( 'Container.Refresh' )
 if 71 - 71: IiI1I1
 if 86 - 86: i11I1IIiiIi + mKm + iiIiIiIi - mmkmmmKmkKKmkK / Kmmm
def Kmkmkm ( ) :
 I1i1iiI1 = iiIIIII1i1iI ( Km )
 Kmkmk = re . compile ( '<index>(.+?)</index>' ) . findall ( I1i1iiI1 ) [ 0 ]
 I1i1iiI1 = mmkmk ( Kmkmk )
 KmmkmKmkmmm = re . compile ( 'name="(.+?)".+?rl="(.+?)".+?mg="(.+?)"' , re . DOTALL ) . findall ( I1i1iiI1 )
 for mmkmKmKmkmkm , i1 , mKmkmkmKm in KmmkmKmkmmm :
  if not 'XXX' in mmkmKmKmkmkm :
   i11 ( mmkmKmKmkmkm , i1 , 1 , mKmkmkmKm , II1 )
  if 'XXX' in mmkmKmKmkmkm :
   if IIi1IiiiI1Ii == 'true' :
    if I11i11Ii == '' :
     i11I1 = xbmcgui . Dialog ( )
     Ii11Ii11I = i11I1 . yesno ( 'Adult Content' , 'You have opted to show adult content' , '' , 'Please set a password to prevent accidental access' , 'Cancel' , 'Lets Go' )
     if Ii11Ii11I == 1 :
      i1i1II = xbmc . Keyboard ( '' , 'Set Password' )
      i1i1II . doModal ( )
      if ( i1i1II . isConfirmed ( ) ) :
       iI11i1I1 = i1i1II . getText ( )
       KmmkKmm . setSetting ( 'password' , iI11i1I1 )
      i11 ( mmkmKmKmkmkm , i1 , 1 , mKmkmkmKm , II1 )
   if IIi1IiiiI1Ii == 'true' :
    if I11i11Ii <> '' :
     i11 ( mmkmKmKmkmkm , i1 , 1 , mKmkmkmKm , II1 )
 i11 ( 'Favourites' , Kmmmmkmkmkm , 1 , 'http://ukturk.offshorepastebin.com/UKTurk/thumbs/new/Uk%20turk%20thumbnails%20favourites.jpg' , II1 )
 i11 ( 'Search' , 'url' , 4 , 'http://ukturk.offshorepastebin.com/UKTurk/thumbs/new/Uk%20turk%20thumbnails%20search.jpg' , II1 )
 if 71 - 71: mKKKmkmmkmkmmkm % mmk + iI11ii1i1I1
def KmkmmmkmK ( name , url , iconimage ) :
 if 'Index' in url :
  I1i1iii ( url )
 if 'XXX' in url :
  if I11i11Ii <> '' :
   i11I1 = xbmcgui . Dialog ( )
   Ii11Ii11I = i11I1 . yesno ( 'Adult Content' , 'Please enter the password you set' , 'to continue' , '' , 'Cancel' , 'Show me the money' )
   if Ii11Ii11I == 1 :
    try :
     i1i1II = xbmc . Keyboard ( '' , 'Set Password' )
     i1i1II . doModal ( )
     if ( i1i1II . isConfirmed ( ) ) :
      iI11i1I1 = i1i1II . getText ( )
     if iI11i1I1 == I11i11Ii :
      i1iiI11I = iiii ( url )
     for name , url , Kmkmkmmmmmmkmk in i1iiI11I :
      I11 ( name , url , 3 , iconimage , II1 )
    except : pass
 if 'movies' in url :
  i1iiI11I = iiii ( url )
  mKmkmmkKmkKKKmmmk = len ( i1iiI11I )
  for name , url , Kmkmkmmmmmmkmk in i1iiI11I :
   IiIiiI ( name , url , 3 , iconimage , mKmkmmkKmkKKKmmmk , isFolder = False )
  if 'Index' in url :
   xbmc . executebuiltin ( 'Container.SetViewMode(50)' )
 elif 'XXX' not in url :
  I1I = url
  I1i1iiI1 = mmkmk ( url )
  mKKmkmkmKK = ''
  if '<FAV>' in I1i1iiI1 : mKKmkmkmKK = 'yes'
  if 'SportsList' in url : mKKmkmkmKK = mKKmkmkmKK + 'BL'
  if 'Live%20TV' in url : mKKmkmkmKK = mKKmkmkmKK + 'BL'
  KmmkmKmkmmm = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( I1i1iiI1 )
  for mmmkmk in KmmkmKmkmmm :
   KmKm = re . compile ( '<link>(.+?)</link>' ) . findall ( mmmkmk )
   if len ( KmKm ) == 1 :
    i1iiI11I = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?humbnail>(.+?)</thumbnail>' , re . DOTALL ) . findall ( mmmkmk )
    for name , url , Kmkmkmmmmmmkmk in i1iiI11I :
     if 'youtube.com/results?search_query=' in url :
      i11 ( name , url , 3 , Kmkmkmmmmmmkmk , II1 , mKKmkmkmKK )
     elif 'youtube.com/playlist?list=' in url :
      i11 ( name , url , 3 , Kmkmkmmmmmmkmk , II1 , mKKmkmkmKK )
     else :
      if 'txt' in url :
       i11 ( name , url , 3 , Kmkmkmmmmmmkmk , II1 , mKKmkmkmKK )
      else :
       if 'ImageH' in Kmkmkmmmmmmkmk :
        I11 ( name , url , 3 , iconimage , II1 , mKKmkmkmKK )
       else : I11 ( name , url , 3 , Kmkmkmmmmmmkmk , II1 , mKKmkmkmKK )
   else :
    name = re . compile ( '<title>(.+?)</title>' ) . findall ( mmmkmk ) [ 0 ]
    iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( mmmkmk ) [ 0 ]
    I11 ( name , I1I , 5 , iconimage , II1 , mKKmkmkmKK )
    if 18 - 18: iii11I111
def KKKKmkmkmmmmkKmm ( name , url , iconimage ) :
 KKKmmKmmmmkmkKmk = [ ]
 KmmkKK = [ ]
 mKKmKmmkmkm = [ ]
 I1i1iiI1 = mmkmk ( url )
 I1i1iiI1 = re . sub ( r'\(.*\)' , '' , I1i1iiI1 )
 name = re . sub ( r'\(.*\)' , '' , name )
 mmkKKmmmkKKmkKKK = re . compile ( '<item>.+?<title>' + name + '</title>(.+?)</item>' , re . DOTALL ) . findall ( I1i1iiI1 ) [ 0 ]
 iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( mmkKKmmmkKKmkKKK ) [ 0 ]
 KmKm = re . compile ( '<link>(.+?)</link>' ) . findall ( mmkKKmmmkKKmkKKK )
 iI1iI1I1i1I = 1
 for iIi11Ii1 in KmKm :
  KKKmmKmmmmkmkKmk . append ( iIi11Ii1 )
  KmmkKK . append ( 'Link ' + str ( iI1iI1I1i1I ) )
  i11I1 = xbmcgui . Dialog ( )
  iI1iI1I1i1I = iI1iI1I1i1I + 1
 Ii11iII1 = i11I1 . select ( name , KmmkKK )
 if Ii11iII1 == - 1 :
  quit ( )
 else :
  url = KKKmmKmmmmkmkKmk [ Ii11iII1 ]
  KmmkKmkKmkmmKmkK = True
  IIIIii = xbmcgui . ListItem ( name , iconImage = iconimage , thumbnailImage = iconimage ) ; IIIIii . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
  KmmkKmkKmkmmKmkK = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = url , listitem = IIIIii )
  IIIIii . setPath ( url )
  xbmcplugin . setResolvedUrl ( int ( sys . argv [ 1 ] ) , True , IIIIii )
  if 70 - 70: mmkmkKKmkmkKmK / KKKmkKKm - KKKmkKKm + IiiIII111ii
def I1i1iii ( url ) :
 I1i1iiI1 = iiIIIII1i1iI ( url )
 KmmkmKmkmmm = re . compile ( 'name="(.+?)".+?rl="(.+?)".+?mg="(.+?)"' , re . DOTALL ) . findall ( I1i1iiI1 )
 for mmkmKmKmkmkm , url , Kmkmkmmmmmmkmk in KmmkmKmkmmm :
  if 'youtube.com/playlist?list=' in url :
   i11 ( mmkmKmKmkmkm , url , 3 , Kmkmkmmmmmmkmk , II1 )
  elif 'youtube.com/results?search_query=' in url :
   i11 ( mmkmKmKmkmkm , url , 3 , Kmkmkmmmmmmkmk , II1 )
  else :
   i11 ( mmkmKmKmkmkm , url , 1 , Kmkmkmmmmmmkmk , II1 )
   if 70 - 70: iii11I111 * i1iIIi1 * mKKKmkmmkmkmmkm / mmk
def iiii ( url ) :
 I1i1iiI1 = mmkmk ( url )
 list = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?humbnail>(.+?)</thumbnail>' , re . DOTALL ) . findall ( I1i1iiI1 )
 return list
 if 88 - 88: KmkmkmmKK
def KmkKmKmkKmkmkmmkmK ( url , name , iconimage ) :
 try :
  if 'search' in iconimage : iconimage = Kmkmkmmmmmmkmk
 except : pass
 if 'txt' in url :
  KmkmmmkmK ( name , url , iconimage )
 else :
  if 'youtube.com/results?search_query=' in url :
   KmkmmmkKKmk = url . split ( 'search_query=' ) [ 1 ]
   I1ii1Ii1 = IiIi11iIIi1Ii + KmkmmmkKKmk + KmmkK
   iii11 = urllib2 . Request ( I1ii1Ii1 )
   iii11 . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' )
   mKKKKmmk = urllib2 . urlopen ( iii11 )
   I1i1iiI1 = mKKKKmmk . read ( )
   mKKKKmmk . close ( )
   I1i1iiI1 = I1i1iiI1 . replace ( '\r' , '' ) . replace ( '\n' , '' ) . replace ( '  ' , '' )
   KmmkmKmkmmm = re . compile ( '"videoId": "(.+?)".+?"title": "(.+?)"' , re . DOTALL ) . findall ( I1i1iiI1 )
   for iiII1i1 , name in KmmkmKmkmmm :
    url = 'https://www.youtube.com/watch?v=' + iiII1i1
    I11 ( name , url , 3 , iconimage , II1 )
  elif 'youtube.com/playlist?list=' in url :
   KmkmmmkKKmk = url . split ( 'playlist?list=' ) [ 1 ]
   I1ii1Ii1 = IiI + KmkmmmkKKmk + mmKm
   iii11 = urllib2 . Request ( I1ii1Ii1 )
   iii11 . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' )
   mKKKKmmk = urllib2 . urlopen ( iii11 )
   I1i1iiI1 = mKKKKmmk . read ( )
   mKKKKmmk . close ( )
   I1i1iiI1 = I1i1iiI1 . replace ( '\r' , '' ) . replace ( '\n' , '' ) . replace ( '  ' , '' )
   KmmkmKmkmmm = re . compile ( '"title": "(.+?)".+?"videoId": "(.+?)"' , re . DOTALL ) . findall ( I1i1iiI1 )
   for name , iiII1i1 in KmmkmKmkmmm :
    url = 'https://www.youtube.com/watch?v=' + iiII1i1
    I11 ( name , url , 3 , iconimage , II1 )
  else :
   if urlresolver . HostedMediaFile ( url ) . valid_url ( ) :
    KKKmmKmmmmkmkKmk = urlresolver . HostedMediaFile ( url ) . resolve ( )
   else : KKKmmKmmmmkmkKmk = url
   IIIIii = xbmcgui . ListItem ( name , iconImage = iconimage , thumbnailImage = iconimage )
   IIIIii . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
   IIIIii . setPath ( KKKmmKmmmmkmkKmk )
   xbmcplugin . setResolvedUrl ( int ( sys . argv [ 1 ] ) , True , IIIIii )
   if 66 - 66: Kmmm - mKKKmkmmkmkmmkm
   #################################################################################	   
def I1i1III ( ) :
 KKmkKmkKmKKmk = ''
 iiiI1I11i1 = 'https://script.google.com/macros/s/AKfycbyBcUa5TlEQudk6Y_0o0ZubnmhGL_-b7Up8kQt11xgVwz3ErTo/exec?588677963413065728'
 iii11 = urllib2 . Request ( iiiI1I11i1 )
 iii11 . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' )
 mKKKKmmk = urllib2 . urlopen ( iii11 )
 I1i1iiI1 = mKKKKmmk . read ( )
 mKKKKmmk . close ( )
 I1i1iiI1 = I1i1iiI1 . replace ( '/n' , '' )
 I1i1iiI1 = I1i1iiI1 . decode ( 'utf-8' ) . encode ( 'utf-8' ) . replace ( '&#39;' , '\'' ) . replace ( '&#10;' , ' - ' ) . replace ( '&#x2026;' , '' )
 KmmkmKmkmmm = re . compile ( "<title>(.+?)</title>.+?<pubDate>(.+?)</pubDate>" , re . DOTALL ) . findall ( I1i1iiI1 ) [ 1 : ]
 for IIi1i11111 , mmKKmkmkKmkmkmm in KmmkmKmkmmm :
  try :
   IIi1i11111 = IIi1i11111 . decode ( 'ascii' , 'ignore' )
  except :
   IIi1i11111 = IIi1i11111 . decode ( 'utf-8' , 'ignore' )
  mmKKmkmkKmkmkmm = mmKKmkmkKmkmkmm [ : - 15 ]
  IIi1i11111 = IIi1i11111 . replace ( '&amp;' , '' )
  mmKKmkmkKmkmkmm = '[COLOR blue][B]' + mmKKmkmkKmkmkmm + '[/B][/COLOR]'
  KKmkKmkKmKKmk = KKmkKmkKmKKmk + mmKKmkmkKmkmkmm + '\n' + IIi1i11111 + '\n' + '\n'
 I1ii11iI ( '[COLOR blue][B]@uk_turk[/B][/COLOR]' , KKmkKmkKmKKmk )
 if 14 - 14: i11I1IIiiIi / iii11I111 . i11I1IIiiIi . mKKKmkmmkmkmmkm % IiI1I1 * mKKKmkmmkmkmmkm
def I1ii11iI ( heading , text ) :
 id = 10147
 xbmc . executebuiltin ( 'ActivateWindow(%d)' % id )
 xbmc . sleep ( 100 )
 iII = xbmcgui . Window ( id )
 mKmkmkmmk = 50
 while ( mKmkmkmmk > 0 ) :
  try :
   xbmc . sleep ( 10 )
   mKmkmkmmk -= 1
   iII . getControl ( 1 ) . setLabel ( heading )
   iII . getControl ( 5 ) . setText ( text )
   return
  except :
   pass
   if 55 - 55: i1iIIi1 + I1iII1iiII / i11I1IIiiIi * mmkmmmKmkKKmkK - i11iIiiIii - mmk
def mmkmk ( url ) :
 if 'UKTurk.db' in url :
  KKmKmmmkmkmm = open ( Kmmmmkmkmkm , 'r' )
  I1i1iiI1 = KKmKmmmkmkmm . read ( )
 else :
  url = url . replace ( ' ' , '%20' )
  I1i1iiI1 = net . http_GET ( url ) . content . replace ( '\r' , '' ) . replace ( '\t' , '' ) . replace ( '&nbsp;' , '' ) . replace ( '\'' , '' ) . replace ( '\n' , '' )
  I1i1iiI1 = ii1ii1ii ( I1i1iiI1 )
 return I1i1iiI1
 if 91 - 91: iii11I111
def iiIIIII1i1iI ( url ) :
 url = url . replace ( ' ' , '%20' )
 I1i1iiI1 = net . http_GET ( url ) . content . replace ( '\r' , '' ) . replace ( '\t' , '' ) . replace ( '&nbsp;' , '' ) . replace ( '\'' , '' ) . replace ( '\n' , '' )
 return I1i1iiI1
 if 15 - 15: i11IiIiiIIIII
def ii1ii1ii ( gobble ) :
 gobble = gobble . replace ( '}' , '' ) . replace ( '{' , '' ) . replace ( ',' , '' ) . replace ( ']' , '' ) . replace ( '[' , '' )
 gobble = gobble + '=='
 gobble = gobble . decode ( 'base64' )
 return gobble
 if 18 - 18: i11iIiiIii . Kmkm % iiiii11iII1 / KmkmkmmKK
def KKmkKmKmkmmkmk ( ) :
 mmKKmkKmkmmKmmK = [ ]
 mKKKmmkmkKmkmkmKm = sys . argv [ 2 ]
 if len ( mKKKmmkmkKmkmkmKm ) >= 2 :
  iiIIIi = sys . argv [ 2 ]
  mmmmkmkKKKmmK = iiIIIi . replace ( '?' , '' )
  if ( iiIIIi [ len ( iiIIIi ) - 1 ] == '/' ) :
   iiIIIi = iiIIIi [ 0 : len ( iiIIIi ) - 2 ]
  KmkmkKKKmKmmmkK = mmmmkmkKKKmmK . split ( '&' )
  mmKKmkKmkmmKmmK = { }
  for iI1iI1I1i1I in range ( len ( KmkmkKKKmKmmmkK ) ) :
   KmkmkmkKKmmkmkmm = { }
   KmkmkmkKKmmkmkmm = KmkmkKKKmKmmmkK [ iI1iI1I1i1I ] . split ( '=' )
   if ( len ( KmkmkmkKKmmkmkmm ) ) == 2 :
    mmKKmkKmkmmKmmK [ KmkmkmkKKmmkmkmm [ 0 ] ] = KmkmkmkKKmmkmkmm [ 1 ]
 return mmKKmkKmkmmKmmK
 if 71 - 71: i11iIiiIii + iii11I111
def i11 ( name , url , mode , iconimage , fanart , description = '' ) :
 mKmmKKmkmkKm = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&iconimage=" + urllib . quote_plus ( iconimage ) + "&description=" + urllib . quote_plus ( description )
 KmmkKmkKmkmmKmkK = True
 IIIIii = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 IIIIii . setInfo ( type = "Video" , infoLabels = { "Title" : name , 'plot' : description } )
 IIIIii . setProperty ( 'fanart_image' , fanart )
 i1iIIIi1i = [ ]
 i1iIIIi1i . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=6&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 if description == 'yes' :
  i1iIIIi1i . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=8&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 IIIIii . addContextMenuItems ( items = i1iIIIi1i , replaceItems = True )
 KmmkKmkKmkmmKmkK = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = mKmmKKmkmkKm , listitem = IIIIii , isFolder = True )
 return KmmkKmkKmkmmKmkK
 if 43 - 43: i11I1IIiiIi % Kmmm
def I11 ( name , url , mode , iconimage , fanart , description = '' ) :
 mKmmKKmkmkKm = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&iconimage=" + urllib . quote_plus ( iconimage ) + "&description=" + urllib . quote_plus ( description )
 KmmkKmkKmkmmKmkK = True
 IIIIii = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 IIIIii . setProperty ( 'fanart_image' , fanart )
 if not mode == 2 :
  IIIIii . setInfo ( type = "Video" , infoLabels = { "Title" : name , 'plot' : description } )
  IIIIii . setProperty ( "IsPlayable" , "true" )
  i1iIIIi1i = [ ]
  if not 'BL' in description :
   i1iIIIi1i . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=6&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
  if 'yes' in description :
   i1iIIIi1i . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=8&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
  IIIIii . addContextMenuItems ( items = i1iIIIi1i , replaceItems = True )
 KmmkKmkKmkmmKmkK = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = mKmmKKmkmkKm , listitem = IIIIii , isFolder = False )
 return KmmkKmkKmkmmKmkK
 if 5 - 5: i11iIiiIii - Kmkm / I1iII1iiII
def IiIiiI ( name , url , mode , iconimage , itemcount , isFolder = False ) :
 if KKKmmk == 'true' :
  if not 'COLOR' in name :
   i1iI11i1ii11 = name . partition ( '(' )
   KKmmmmkKmkmkm = ""
   mKKmKmmKm = ""
   if len ( i1iI11i1ii11 ) > 0 :
    KKmmmmkKmkmkm = i1iI11i1ii11 [ 0 ]
    mKKmKmmKm = i1iI11i1ii11 [ 2 ] . partition ( ')' )
   if len ( mKKmKmmKm ) > 0 :
    mKKmKmmKm = mKKmKmmKm [ 0 ]
   Kmkmkmkmm = metahandlers . MetaData ( )
   IIi1I11I1II = Kmkmkmkmm . get_meta ( 'movie' , name = KKmmmmkKmkmkm , year = mKKmKmmKm )
   mKmmKKmkmkKm = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&site=" + str ( KmmKmmmKm ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name )
   KmmkKmkKmkmmKmkK = True
   IIIIii = xbmcgui . ListItem ( name , iconImage = IIi1I11I1II [ 'cover_url' ] , thumbnailImage = IIi1I11I1II [ 'cover_url' ] )
   IIIIii . setInfo ( type = "Video" , infoLabels = IIi1I11I1II )
   IIIIii . setProperty ( "IsPlayable" , "true" )
   ii11IIII11I = [ ]
   ii11IIII11I . append ( ( 'Movie Information' , 'XBMC.Action(Info)' ) )
   ii11IIII11I . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=6&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , IIi1I11I1II [ 'cover_url' ] ) ) )
   IIIIii . addContextMenuItems ( ii11IIII11I , replaceItems = True )
   if not IIi1I11I1II [ 'backdrop_url' ] == '' : IIIIii . setProperty ( 'fanart_image' , IIi1I11I1II [ 'backdrop_url' ] )
   else : IIIIii . setProperty ( 'fanart_image' , II1 )
   KmmkKmkKmkmmKmkK = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = mKmmKKmkmkKm , listitem = IIIIii , isFolder = isFolder , totalItems = itemcount )
   return KmmkKmkKmkmmKmkK
 else :
  mKmmKKmkmkKm = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&site=" + str ( KmmKmmmKm ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name )
  KmmkKmkKmkmmKmkK = True
  IIIIii = xbmcgui . ListItem ( name , iconImage = iconimage , thumbnailImage = iconimage )
  IIIIii . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
  IIIIii . setProperty ( 'fanart_image' , II1 )
  IIIIii . setProperty ( "IsPlayable" , "true" )
  i1iIIIi1i = [ ]
  i1iIIIi1i . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=6&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
  IIIIii . addContextMenuItems ( items = i1iIIIi1i , replaceItems = True )
  KmmkKmkKmkmmKmkK = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = mKmmKKmkmkKm , listitem = IIIIii , isFolder = isFolder )
  return KmmkKmkKmkmmKmkK
  if 81 - 81: i11I1IIiiIi / KmkmkmmKK . iii11I111 . IiiIII111ii
def KmKK ( content , viewType ) :
 if content :
  xbmcplugin . setContent ( int ( sys . argv [ 1 ] ) , content )
 if KmmkKmm . getSetting ( 'auto-view' ) == 'true' :
  xbmc . executebuiltin ( "Container.SetViewMode(%s)" % KmmkKmm . getSetting ( viewType ) )
  if 53 - 53: i1iIIi1
iiIIIi = KKmkKmKmkmmkmk ( ) ; i1 = None ; mmkmKmKmkmkm = None ; iI1Iii = None ; KmmKmmmKm = None ; mKmkmkmKm = None
try : KmmKmmmKm = urllib . unquote_plus ( iiIIIi [ "site" ] )
except : pass
try : i1 = urllib . unquote_plus ( iiIIIi [ "url" ] )
except : pass
try : mmkmKmKmkmkm = urllib . unquote_plus ( iiIIIi [ "name" ] )
except : pass
try : iI1Iii = int ( iiIIIi [ "mode" ] )
except : pass
try : mKmkmkmKm = urllib . unquote_plus ( iiIIIi [ "iconimage" ] )
except : pass
if 68 - 68: Kmmm % mmkmkKKmkmkKmK
if iI1Iii == None or i1 == None or len ( i1 ) < 1 : Kmkmkm ( )
elif iI1Iii == 1 : KmkmmmkmK ( mmkmKmKmkmkm , i1 , mKmkmkmKm )
elif iI1Iii == 2 : I1i1III ( )
elif iI1Iii == 3 : KmkKmKmkKmkmkmmkmK ( i1 , mmkmKmKmkmkm , mKmkmkmKm )
elif iI1Iii == 4 : iI1Ii11111iIi ( )
elif iI1Iii == 5 : KKKKmkmkmmmmkKmm ( mmkmKmKmkmkm , i1 , Kmkmkmmmmmmkmk )
elif iI1Iii == 6 : mKmk ( mmkmKmKmkmkm , i1 , mKmkmkmKm )
elif iI1Iii == 7 : GETFAVS ( i1 )
elif iI1Iii == 8 : ii11iIi1I ( mmkmKmKmkmkm , i1 , mKmkmkmKm )
if 88 - 88: I1iII1iiII - KKKmkKKm + Kmmm
xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
if 40 - 40: IiiIII111ii * mmk + Kmmm % iI11ii1i1I1
if 74 - 74: mmkmmmKmkKKmkK - i1iIIi1 + iiiii11iII1 + mmkmkKKmkmkKmK / i11I1IIiiIi
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3
