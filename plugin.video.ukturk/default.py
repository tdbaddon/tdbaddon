import xbmc , xbmcaddon , xbmcgui , xbmcplugin , urllib , urllib2 , os , re , sys , urlresolver , random
from resources . libs . common_addon import Addon
from metahandler import metahandlers
mmmkmkmk = 'plugin.video.ukturk'
ii = xbmcaddon . Addon ( id = mmmkmkmk )
mKKm = Addon ( mmmkmkmk , sys . argv )
Kmk = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + mmmkmkmk , 'fanart.jpg' ) )
mmkK = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + mmmkmkmk , 'icon.png' ) )
iI11I1II1I1I = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + mmmkmkmk , 'search.png' ) )
mmmm = ii . getSetting ( 'adult' )
iIIii1IIi = ii . getSetting ( 'password' )
mmkKKmkmk = mKKm . queries . get ( 'iconimage' , '' )
mm = ii . getSetting ( 'enable_meta' )
i1iII1IiiIiI1 = xbmc . translatePath ( os . path . join ( 'special://home/userdata/Database' , 'UKTurk.db' ) )
iIiiiI1IiI1I1 = 'https://www.googleapis.com/youtube/v3/search?q='
mmkKmKmKKmkmk = '&regionCode=US&part=snippet&hl=en_US&key=AIzaSyAd-YEOqZz9nXVzGtn3KWzYLbLaajhqIDA&type=video&maxResults=50'
I11i = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId='
KmkK = '&maxResults=50&key=AIzaSyAd-YEOqZz9nXVzGtn3KWzYLbLaajhqIDA'
Km = 'http://metalkettle.co/ukturk.jpg'
if 2 - 2: mmk * i1 * ii1IiI1i % KKmmKKm / I11iIi1I / IiiIII111iI
def IiII ( ) :
 iI1Ii11111iIi = xbmc . Keyboard ( '' , 'Search UK Turk' )
 iI1Ii11111iIi . doModal ( )
 if ( iI1Ii11111iIi . isConfirmed ( ) ) :
  i1i1II = iI1Ii11111iIi . getText ( )
  i1i1II = i1i1II . upper ( )
 else : quit ( )
 KmkmmmkKKmk = I1i1iiI1 ( Km )
 iiIIIII1i1iI = re . compile ( '<link>(.+?)</link>' ) . findall ( KmkmmmkKKmk )
 for mmkmKmk in iiIIIII1i1iI :
  KmkmmmkKKmk = I1i1iiI1 ( mmkmKmk )
  if '[{' in KmkmmmkKKmk :
   KmkmmmkKKmk = mmmkmk ( KmkmmmkKKmk )
  mmkmk = re . compile ( 'name="(.+?)".+?url="(.+?)".+?img="(.+?)"' , re . DOTALL ) . findall ( KmkmmmkKKmk )
  if len ( mmkmk ) > 0 :
   for KmmkmKmkmmm , mmkmKmKmkmkm , i1mKKmmmkmkKmkK in mmkmk :
    if 'ImageH' in i1mKKmmmkmkKmkK : i1mKKmmmkmkKmkK = iI11I1II1I1I
    i1111 = KmmkmKmkmmm
    KmmkmKmkmmm = KmmkmKmkmmm . upper ( )
    if i1i1II in KmmkmKmkmmm and not 'COLOR' in KmmkmKmkmmm :
     if 'txt' in mmkmKmKmkmkm :
      i11 ( i1111 , mmkmKmKmkmkm , 3 , i1mKKmmmkmkKmkK , Kmk )
     elif 'youtube.com/playlist?list=' in mmkmKmKmkmkm :
      i11 ( i1111 , mmkmKmKmkmkm , 3 , i1mKKmmmkmkKmkK , Kmk )
     elif 'youtube.com/results?search_query=' in mmkmKmKmkmkm :
      i11 ( i1111 , mmkmKmKmkmkm , 3 , i1mKKmmmkmkKmkK , Kmk )
     else : I11 ( i1111 , mmkmKmKmkmkm , 3 , i1mKKmmmkmkKmkK , Kmk )
  else :
   Kmmkmmkmkmkmkmmkmmk = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?humbnail>(.+?)</thumbnail>' , re . DOTALL ) . findall ( KmkmmmkKKmk )
   if len ( Kmmkmmkmkmkmkmmkmmk ) > 0 :
    for KmmkmKmkmmm , mmkmKmKmkmkm , i1mKKmmmkmkKmkK in Kmmkmmkmkmkmkmmkmmk :
     if 'ImageH' in i1mKKmmmkmkKmkK : i1mKKmmmkmkKmkK = iI11I1II1I1I
     if not 'http' in mmkmKmKmkmkm : pass
     i1111 = KmmkmKmkmmm
     KmmkmKmkmmm = KmmkmKmkmmm . upper ( )
     if i1i1II in KmmkmKmkmmm and not 'COLOR' in KmmkmKmkmmm :
      if 'txt' in mmkmKmKmkmkm :
       i11 ( i1111 , mmkmKmKmkmkm , 3 , i1mKKmmmkmkKmkK , Kmk )
      elif 'youtube.com/playlist?list=' in mmkmKmKmkmkm :
       i11 ( i1111 , mmkmKmKmkmkm , 3 , i1mKKmmmkmkKmkK , Kmk )
      elif 'youtube.com/results?search_query=' in mmkmKmKmkmkm :
       i11 ( i1111 , mmkmKmKmkmkm , 3 , i1mKKmmmkmkKmkK , Kmk )
      else : I11 ( i1111 , mmkmKmKmkmkm , 3 , i1mKKmmmkmkKmkK , Kmk )
      if 86 - 86: iiiii11iII1 % Kmkm
      if 97 - 97: IIIII . I1
def KmkKmKmmmkmkm ( name , url , iconimage ) :
 url = url . replace ( ' ' , '%20' )
 iconimage = iconimage . replace ( ' ' , '%20' )
 iiiI11 = '<FAV><item>\n<title>' + name + '</title>\n<link>' + url + '</link>\n' + '<Thumbnail>' + iconimage + '</thumbnail>\n</item></FAV>\n'
 KKmmK = open ( i1iII1IiiIiI1 , 'a' )
 KKmmK . write ( iiiI11 )
 KKmmK . close ( )
 if 58 - 58: i11iiII + KmmmmKmkmKK + mKmmk / mmmkKmmmk
def I1I11I1I1I ( name , url , iconimage ) :
 KmmKmkKK = None
 file = open ( i1iII1IiiIiI1 , 'r' )
 KmmKmkKK = file . read ( )
 iiiIi = ''
 mmkmk = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( KmmKmkKK )
 for IiIIIiI1I1 in mmkmk :
  iiiI11 = '\n<FAV><item>\n' + IiIIIiI1I1 + '</item>\n'
  if name in IiIIIiI1I1 :
   iiiI11 = iiiI11 . replace ( 'item' , ' ' )
  iiiIi = iiiIi + iiiI11
 file = open ( i1iII1IiiIiI1 , 'w' )
 file . truncate ( )
 file . write ( iiiIi )
 file . close ( )
 xbmc . executebuiltin ( 'Container.Refresh' )
 if 86 - 86: i11I1IIiiIi + mKm + iiIiIiIi - mmkmmmKmkKKmkK / Kmmm
def mmmkmk ( string ) :
 string = string . replace ( '}' , '' ) . replace ( '{' , '' ) . replace ( ',' , '' ) . replace ( ']' , '' ) . replace ( '[' , '' )
 string = string + '=='
 string = string . decode ( 'base64' )
 return string
 if 67 - 67: KKmkm / KKmkm % mmk . iiiii11iII1
def KmkmmkKm ( ) :
 KmkmmmkKKmk = I1i1iiI1 ( Km )
 KmmkmkKKKKK = re . compile ( '<index>(.+?)</index>' ) . findall ( KmkmmmkKKmk ) [ 0 ]
 KmkmmmkKKmk = I1i1iiI1 ( KmmkmkKKKKK )
 KmkmmmkKKmk = mmmkmk ( KmkmmmkKKmk )
 mmkmk = re . compile ( 'name="(.+?)".+?url="(.+?)".+?img="(.+?)"' , re . DOTALL ) . findall ( KmkmmmkKKmk )
 for KmmkmKmkmmm , mmkmKmKmkmkm , mmkKKmkmk in mmkmk :
  if not 'XXX' in KmmkmKmkmmm :
   i11 ( KmmkmKmkmmm , mmkmKmKmkmkm , 1 , mmkKKmkmk , Kmk )
  if 'XXX' in KmmkmKmkmmm :
   if mmmm == 'true' :
    if iIIii1IIi == '' :
     KmkKKmkmkmmkKK = xbmcgui . Dialog ( )
     I11i1 = KmkKKmkmkmmkKK . yesno ( 'Adult Content' , 'You have opted to show adult content' , '' , 'Please set a password to prevent accidental access' , 'Cancel' , 'Lets Go' )
     if I11i1 == 1 :
      iI1Ii11111iIi = xbmc . Keyboard ( '' , 'Set Password' )
      iI1Ii11111iIi . doModal ( )
      if ( iI1Ii11111iIi . isConfirmed ( ) ) :
       iIi1ii1I1 = iI1Ii11111iIi . getText ( )
       ii . setSetting ( 'password' , iIi1ii1I1 )
      i11 ( KmmkmKmkmmm , mmkmKmKmkmkm , 1 , mmkKKmkmk , Kmk )
   if mmmm == 'true' :
    if iIIii1IIi <> '' :
     i11 ( KmmkmKmkmmm , mmkmKmKmkmkm , 1 , mmkKKmkmk , Kmk )
 i11 ( 'Favourites' , i1iII1IiiIiI1 , 1 , 'http://metalkettle.co/UKTurk18022016/thumbs/new/Uk%20turk%20thumbnails%20favourites.jpg' , Kmk )
 i11 ( 'Search' , 'url' , 4 , 'http://metalkettle.co/UKTurk18022016/thumbs/new/Uk%20turk%20thumbnails%20search.jpg' , Kmk )
 if 71 - 71: Kmmm . i1
def mmkKKmkmmmkmKK ( name , url , iconimage ) :
 if 'Index' in url :
  mmmkmmmmmKmk ( url )
 if 'XXX' in url :
  if iIIii1IIi <> '' :
   KmkKKmkmkmmkKK = xbmcgui . Dialog ( )
   I11i1 = KmkKKmkmkmmkKK . yesno ( 'Adult Content' , 'Please enter the password you set' , 'to continue' , '' , 'Cancel' , 'Show me the money' )
   if I11i1 == 1 :
    try :
     iI1Ii11111iIi = xbmc . Keyboard ( '' , 'Set Password' )
     iI1Ii11111iIi . doModal ( )
     if ( iI1Ii11111iIi . isConfirmed ( ) ) :
      iIi1ii1I1 = iI1Ii11111iIi . getText ( )
     if iIi1ii1I1 == iIIii1IIi :
      i11Iiii = iI ( url )
     for name , url , mmkK in i11Iiii :
      I11 ( name , url , 3 , iconimage , Kmk )
    except : pass
 if 'movies' in url :
  i11Iiii = iI ( url )
  I1i1I1II = len ( i11Iiii )
  for name , url , mmkK in i11Iiii :
   i1IiIiiI ( name , url , 3 , iconimage , I1i1I1II , isFolder = False )
  if 'Index' in url :
   xbmc . executebuiltin ( 'Container.SetViewMode(50)' )
 elif 'XXX' not in url :
  I1I = url
  KmkmmmkKKmk = I1i1iiI1 ( url )
  if not 'UKTurk.db' in url :
   KmkmmmkKKmk = mmmkmk ( KmkmmmkKKmk )
  mKKmkmkmKK = ''
  if '<FAV>' in KmkmmmkKKmk : mKKmkmkmKK = 'yes'
  if 'SportsList' in url : mKKmkmkmKK = mKKmkmkmKK + 'BL'
  if 'Live%20TV' in url : mKKmkmkmKK = mKKmkmkmKK + 'BL'
  mmkmk = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( KmkmmmkKKmk )
  for mmkmKmk in mmkmk :
   KmKm = re . compile ( '<link>(.+?)</link>' ) . findall ( mmkmKmk )
   if len ( KmKm ) == 1 :
    i11Iiii = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?humbnail>(.+?)</thumbnail>' , re . DOTALL ) . findall ( mmkmKmk )
    for name , url , mmkK in i11Iiii :
     if 'youtube.com/results?search_query=' in url :
      i11 ( name , url , 3 , mmkK , Kmk , mKKmkmkmKK )
     elif 'youtube.com/playlist?list=' in url :
      i11 ( name , url , 3 , mmkK , Kmk , mKKmkmkmKK )
     else :
      if 'txt' in url :
       i11 ( name , url , 3 , mmkK , Kmk , mKKmkmkmKK )
      else :
       if 'ImageH' in mmkK :
        I11 ( name , url , 3 , iconimage , Kmk , mKKmkmkmKK )
       else : I11 ( name , url , 3 , mmkK , Kmk , mKKmkmkmKK )
   else :
    name = re . compile ( '<title>(.+?)</title>' ) . findall ( mmkmKmk ) [ 0 ]
    iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( mmkmKmk ) [ 0 ]
    I11 ( name , I1I , 5 , iconimage , Kmk , mKKmkmkmKK )
    if 18 - 18: mmk
def Ii11I ( name , url , iconimage ) :
 KKKmkKKKmkmkmm = [ ]
 Iii111II = [ ]
 iiii11I = [ ]
 KmkmmmkKKmk = I1i1iiI1 ( url )
 KmkmmmkKKmk = mmmkmk ( KmkmmmkKKmk )
 KmkmmmkKKmk = re . sub ( r'\(.*\)' , '' , KmkmmmkKKmk )
 name = re . sub ( r'\(.*\)' , '' , name )
 KmmmkKKmkmKK = re . compile ( '<item>.+?<title>' + name + '</title>(.+?)</item>' , re . DOTALL ) . findall ( KmkmmmkKKmk ) [ 0 ]
 iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( KmmmkKKmkmKK ) [ 0 ]
 KmKm = re . compile ( '<link>(.+?)</link>' ) . findall ( KmmmkKKmkmKK )
 ii11i1 = 1
 for IIIii1II1II in KmKm :
  KKKmkKKKmkmkmm . append ( IIIii1II1II )
  Iii111II . append ( 'Link ' + str ( ii11i1 ) )
  KmkKKmkmkmmkKK = xbmcgui . Dialog ( )
  ii11i1 = ii11i1 + 1
 i1I1iI = KmkKKmkmkmmkKK . select ( name , Iii111II )
 if i1I1iI == - 1 :
  quit ( )
 else :
  url = KKKmkKKKmkmkmm [ i1I1iI ]
  mmmkKmmKKmmk = True
  mmkKKmkmkmK = xbmcgui . ListItem ( name , iconImage = iconimage , thumbnailImage = iconimage ) ; mmkKKmkmkmK . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
  mmmkKmmKKmmk = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = url , listitem = mmkKKmkmkmK )
  mmkKKmkmkmK . setPath ( url )
  xbmcplugin . setResolvedUrl ( int ( sys . argv [ 1 ] ) , True , mmkKKmkmkmK )
  if 39 - 39: mmkmmmKmkKKmkK - IiiIII111iI * IIIII % i11iiII * IiiIII111iI % IiiIII111iI
def mmmkmmmmmKmk ( url ) :
 KmkmmmkKKmk = I1i1iiI1 ( url )
 mmkmk = re . compile ( 'name="(.+?)".+?url="(.+?)".+?img="(.+?)"' , re . DOTALL ) . findall ( KmkmmmkKKmk )
 for KmmkmKmkmmm , url , mmkK in mmkmk :
  if 'youtube.com/playlist?list=' in url :
   i11 ( KmmkmKmkmmm , url , 3 , mmkK , Kmk )
  elif 'youtube.com/results?search_query=' in url :
   i11 ( KmmkmKmkmmm , url , 3 , mmkK , Kmk )
  else :
   i11 ( KmmkmKmkmmm , url , 1 , mmkK , Kmk )
   if 59 - 59: ii1IiI1i + iiiii11iII1 - i11iiII - iiiii11iII1 + mmmkKmmmk / KmmmmKmkmKK
def iI ( url ) :
 KmkmmmkKKmk = I1i1iiI1 ( url )
 if not 'UKTurk.db' in url :
  KmkmmmkKKmk = mmmkmk ( KmkmmmkKKmk )
 list = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?humbnail>(.+?)</thumbnail>' , re . DOTALL ) . findall ( KmkmmmkKKmk )
 return list
 if 24 - 24: i11I1IIiiIi . iiIiIiIi % mmmkKmmmk + KKmkm % I1
def I11III1II ( url , name , iconimage ) :
 try :
  if 'search' in iconimage : iconimage = mmkK
 except : pass
 if 'txt' in url :
  mmkKKmkmmmkmKK ( name , url , iconimage )
 else :
  if 'youtube.com/results?search_query=' in url :
   i1i1II = url . split ( 'search_query=' ) [ 1 ]
   iI1I111Ii111i = iIiiiI1IiI1I1 + i1i1II + mmkKmKmKKmkmk
   I11IiI1I11i1i = urllib2 . Request ( iI1I111Ii111i )
   I11IiI1I11i1i . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' )
   iI1ii1Ii = urllib2 . urlopen ( I11IiI1I11i1i )
   KmkmmmkKKmk = iI1ii1Ii . read ( )
   iI1ii1Ii . close ( )
   KmkmmmkKKmk = KmkmmmkKKmk . replace ( '\r' , '' ) . replace ( '\n' , '' ) . replace ( '  ' , '' )
   mmkmk = re . compile ( '"videoId": "(.+?)".+?"title": "(.+?)"' , re . DOTALL ) . findall ( KmkmmmkKKmk )
   for mmmmmkmkmk , name in mmkmk :
    url = 'https://www.youtube.com/watch?v=' + mmmmmkmkmk
    I11 ( name , url , 3 , iconimage , Kmk )
  elif 'youtube.com/playlist?list=' in url :
   i1i1II = url . split ( 'playlist?list=' ) [ 1 ]
   iI1I111Ii111i = I11i + i1i1II + KmkK
   I11IiI1I11i1i = urllib2 . Request ( iI1I111Ii111i )
   I11IiI1I11i1i . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' )
   iI1ii1Ii = urllib2 . urlopen ( I11IiI1I11i1i )
   KmkmmmkKKmk = iI1ii1Ii . read ( )
   iI1ii1Ii . close ( )
   KmkmmmkKKmk = KmkmmmkKKmk . replace ( '\r' , '' ) . replace ( '\n' , '' ) . replace ( '  ' , '' )
   mmkmk = re . compile ( '"title": "(.+?)".+?"videoId": "(.+?)"' , re . DOTALL ) . findall ( KmkmmmkKKmk )
   for name , mmmmmkmkmk in mmkmk :
    if not 'Deleted v' in name :
     url = 'https://www.youtube.com/watch?v=' + mmmmmkmkmk
     I11 ( name , url , 3 , iconimage , Kmk )
  else :
   if urlresolver . HostedMediaFile ( url ) . valid_url ( ) :
    KKKmkKKKmkmkmm = urlresolver . HostedMediaFile ( url ) . resolve ( )
   else : KKKmkKKKmkmkmm = url
   mmkKKmkmkmK = xbmcgui . ListItem ( name , iconImage = iconimage , thumbnailImage = iconimage )
   mmkKKmkmkmK . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
   mmkKKmkmkmK . setPath ( KKKmkKKKmkmkmm )
   xbmcplugin . setResolvedUrl ( int ( sys . argv [ 1 ] ) , True , mmkKKmkmkmK )
   if 16 - 16: KmmmmKmkmKK + IIIII - IiiIII111iI
   if 85 - 85: I1 + I11iIi1I
def I1i1iiI1 ( url ) :
 if 'UKTurk.db' in url :
  KKmmK = open ( i1iII1IiiIiI1 , 'r' )
  KmkmmmkKKmk = KKmmK . read ( )
 else :
  url = url . replace ( ' ' , '%20' )
  url += '?%d=%d' % ( random . randint ( 1 , 10000 ) , random . randint ( 1 , 10000 ) )
  I11IiI1I11i1i = urllib2 . Request ( url )
  I11IiI1I11i1i . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' )
  iI1ii1Ii = urllib2 . urlopen ( I11IiI1I11i1i )
  KmkmmmkKKmk = iI1ii1Ii . read ( )
  KmkmmmkKKmk = KmkmmmkKKmk . replace ( '\r' , '' ) . replace ( '\t' , '' ) . replace ( '&nbsp;' , '' ) . replace ( '\'' , '' )
  iI1ii1Ii . close ( )
 return KmkmmmkKKmk
 if 58 - 58: IiiIII111iI * mmmkKmmmk * KmmmmKmkmKK / mmmkKmmmk
def mKmkmmkKKKK ( ) :
 KmkKmkKmKKmk = [ ]
 iiiI1I11i1 = sys . argv [ 2 ]
 if len ( iiiI1I11i1 ) >= 2 :
  IIi1i11111 = sys . argv [ 2 ]
  mmKKmkmkKmkmkmm = IIi1i11111 . replace ( '?' , '' )
  if ( IIi1i11111 [ len ( IIi1i11111 ) - 1 ] == '/' ) :
   IIi1i11111 = IIi1i11111 [ 0 : len ( IIi1i11111 ) - 2 ]
  I1ii11iI = mmKKmkmkKmkmkmm . split ( '&' )
  KmkKmkKmKKmk = { }
  for ii11i1 in range ( len ( I1ii11iI ) ) :
   IIi1i = { }
   IIi1i = I1ii11iI [ ii11i1 ] . split ( '=' )
   if ( len ( IIi1i ) ) == 2 :
    KmkKmkKmKKmk [ IIi1i [ 0 ] ] = IIi1i [ 1 ]
 return KmkKmkKmKKmk
 if 46 - 46: Kmmm % i11I1IIiiIi + IIIII . I1 . IIIII
def i11 ( name , url , mode , iconimage , fanart , description = '' ) :
 mKmkmkmmk = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&iconimage=" + urllib . quote_plus ( iconimage ) + "&description=" + urllib . quote_plus ( description )
 mmmkKmmKKmmk = True
 mmkKKmkmkmK = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 mmkKKmkmkmK . setInfo ( type = "Video" , infoLabels = { "Title" : name , 'plot' : description } )
 mmkKKmkmkmK . setProperty ( 'fanart_image' , fanart )
 KKmmmkK = [ ]
 KKmmmkK . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=6&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 if description == 'yes' :
  KKmmmkK . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=8&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 mmkKKmkmkmK . addContextMenuItems ( items = KKmmmkK , replaceItems = True )
 mmmkKmmKKmmk = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = mKmkmkmmk , listitem = mmkKKmkmkmK , isFolder = True )
 return mmmkKmmKKmmk
 if 67 - 67: mmk - I11iIi1I % KmmmmKmkmKK . i1
def I11 ( name , url , mode , iconimage , fanart , description = '' ) :
 mKmkmkmmk = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&iconimage=" + urllib . quote_plus ( iconimage ) + "&description=" + urllib . quote_plus ( description )
 mmmkKmmKKmmk = True
 mmkKKmkmkmK = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 mmkKKmkmkmK . setProperty ( 'fanart_image' , fanart )
 if not mode == 2 :
  mmkKKmkmkmK . setInfo ( type = "Video" , infoLabels = { "Title" : name , 'plot' : description } )
  mmkKKmkmkmK . setProperty ( "IsPlayable" , "true" )
  KKmmmkK = [ ]
  if not 'BL' in description :
   KKmmmkK . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=6&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
  if 'yes' in description :
   KKmmmkK . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=8&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
  mmkKKmkmkmK . addContextMenuItems ( items = KKmmmkK , replaceItems = True )
 mmmkKmmKKmmk = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = mKmkmkmmk , listitem = mmkKKmkmkmK , isFolder = False )
 return mmmkKmmKKmmk
 if 77 - 77: mmkmmmKmkKKmkK / iiiii11iII1
def i1IiIiiI ( name , url , mode , iconimage , itemcount , isFolder = False ) :
 if mm == 'true' :
  if not 'COLOR' in name :
   I1iiIii = name . partition ( '(' )
   mmmmkK = ""
   mKmKmkmmkmkKKmk = ""
   if len ( I1iiIii ) > 0 :
    mmmmkK = I1iiIii [ 0 ]
    mKmKmkmmkmkKKmk = I1iiIii [ 2 ] . partition ( ')' )
   if len ( mKmKmkmmkmkKKmk ) > 0 :
    mKmKmkmmkmkKKmk = mKmKmkmmkmkKKmk [ 0 ]
   i1I1ii = metahandlers . MetaData ( )
   mKKmmk = i1I1ii . get_meta ( 'movie' , name = mmmmkK , year = mKmKmkmmkmkKKmk )
   mKmkmkmmk = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&site=" + str ( mmmkmkKmkmkmK ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name )
   mmmkKmmKKmmk = True
   mmkKKmkmkmK = xbmcgui . ListItem ( name , iconImage = mKKmmk [ 'cover_url' ] , thumbnailImage = mKKmmk [ 'cover_url' ] )
   mmkKKmkmkmK . setInfo ( type = "Video" , infoLabels = mKKmmk )
   mmkKKmkmkmK . setProperty ( "IsPlayable" , "true" )
   iIiIIIi = [ ]
   iIiIIIi . append ( ( 'Movie Information' , 'XBMC.Action(Info)' ) )
   iIiIIIi . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=6&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , mKKmmk [ 'cover_url' ] ) ) )
   mmkKKmkmkmK . addContextMenuItems ( iIiIIIi , replaceItems = True )
   if not mKKmmk [ 'backdrop_url' ] == '' : mmkKKmkmkmK . setProperty ( 'fanart_image' , mKKmmk [ 'backdrop_url' ] )
   else : mmkKKmkmkmK . setProperty ( 'fanart_image' , Kmk )
   mmmkKmmKKmmk = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = mKmkmkmmk , listitem = mmkKKmkmkmK , isFolder = isFolder , totalItems = itemcount )
   return mmmkKmmKKmmk
 else :
  mKmkmkmmk = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&site=" + str ( mmmkmkKmkmkmK ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name )
  mmmkKmmKKmmk = True
  mmkKKmkmkmK = xbmcgui . ListItem ( name , iconImage = iconimage , thumbnailImage = iconimage )
  mmkKKmkmkmK . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
  mmkKKmkmkmK . setProperty ( 'fanart_image' , Kmk )
  mmkKKmkmkmK . setProperty ( "IsPlayable" , "true" )
  KKmmmkK = [ ]
  KKmmmkK . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=6&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
  mmkKKmkmkmK . addContextMenuItems ( items = KKmmmkK , replaceItems = True )
  mmmkKmmKKmmk = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = mKmkmkmmk , listitem = mmkKKmkmkmK , isFolder = isFolder )
  return mmmkKmmKKmmk
  if 93 - 93: iiIiIiIi
def i1IIIiiII1 ( content , viewType ) :
 if content :
  xbmcplugin . setContent ( int ( sys . argv [ 1 ] ) , content )
 if ii . getSetting ( 'auto-view' ) == 'true' :
  xbmc . executebuiltin ( "Container.SetViewMode(%s)" % ii . getSetting ( viewType ) )
  if 87 - 87: mKmmk * KmmmmKmkmKK + mmmkKmmmk / ii1IiI1i / iiIiIiIi
IIi1i11111 = mKmkmmkKKKK ( ) ; mmkmKmKmkmkm = None ; KmmkmKmkmmm = None ; I1111IIi = None ; mmmkmkKmkmkmK = None ; mmkKKmkmk = None
try : mmmkmkKmkmkmK = urllib . unquote_plus ( IIi1i11111 [ "site" ] )
except : pass
try : mmkmKmKmkmkm = urllib . unquote_plus ( IIi1i11111 [ "url" ] )
except : pass
try : KmmkmKmkmmm = urllib . unquote_plus ( IIi1i11111 [ "name" ] )
except : pass
try : I1111IIi = int ( IIi1i11111 [ "mode" ] )
except : pass
try : mmkKKmkmk = urllib . unquote_plus ( IIi1i11111 [ "iconimage" ] )
except : pass
if 93 - 93: KKmmKKm / iiiii11iII1 % mmk + KmmmmKmkmKK * IIIII
if I1111IIi == None or mmkmKmKmkmkm == None or len ( mmkmKmKmkmkm ) < 1 : KmkmmkKm ( )
elif I1111IIi == 1 : mmkKKmkmmmkmKK ( KmmkmKmkmmm , mmkmKmKmkmkm , mmkKKmkmk )
elif I1111IIi == 2 : TWITTER ( )
elif I1111IIi == 3 : I11III1II ( mmkmKmKmkmkm , KmmkmKmkmmm , mmkKKmkmk )
elif I1111IIi == 4 : IiII ( )
elif I1111IIi == 5 : Ii11I ( KmmkmKmkmmm , mmkmKmKmkmkm , mmkK )
elif I1111IIi == 6 : KmkKmKmmmkmkm ( KmmkmKmkmmm , mmkmKmKmkmkm , mmkKKmkmk )
elif I1111IIi == 7 : GETFAVS ( mmkmKmKmkmkm )
elif I1111IIi == 8 : I1I11I1I1I ( KmmkmKmkmmm , mmkmKmKmkmkm , mmkKKmkmk )
if 15 - 15: i11I1IIiiIi . IIIII / Kmkm + i11I1IIiiIi
xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
