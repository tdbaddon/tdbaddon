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
Km = 'http://ukturk.offshorepastebin.com/ukturk2.jpg'
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
   if 31 - 31: KmKKKmkmkmKKmk . iiiiiIIii * mmkmkKKmkKKKmk % KmkmkmmKK % IiiIII111ii . mKKKmkmmkmkmmkm
 elif 'XXX' not in url :
  mmkmkKmmKmmm = url
  I1i1iiI1 = mmkmk ( url )
  I1i1iiI1 = I1i1iiI1 . replace ( 'Image' , 'image' )
  KmkmkmkmmmkK = ''
  if '<FAV>' in I1i1iiI1 : KmkmkmkmmmkK = 'yes'
  if 'SportsList' in url : KmkmkmkmmmkK = KmkmkmkmmmkK + 'BL'
  if 'Live%20TV' in url : KmkmkmkmmmkK = KmkmkmkmmmkK + 'BL'
  KmmkmKmkmmm = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( I1i1iiI1 )
  for mmmkmk in KmmkmKmkmmm :
   if '<image>' in mmmkmk :
    KKKK = re . compile ( '<title>(.+?)</title>.+?image>(.+?)</image>.+?humbnail>(.+?)</thumbnail>' , re . DOTALL ) . findall ( mmmkmk )
    for name , url , Kmkmkmmmmmmkmk in KKKK :
     url = url . replace ( 'http://imgur.com/' , 'http://i.imgur.com/' ) + '.jpg'
     Kmkmkmmmmmmkmk = Kmkmkmmmmmmkmk . replace ( 'http://imgur.com/' , 'http://i.imgur.com/' ) + '.jpg'
     if 'ImageH' in Kmkmkmmmmmmkmk :
      i11i1 ( name , url , 9 , iconimage , II1 , KmkmkmkmmmkK )
     else :
      i11i1 ( name , url , '9' , Kmkmkmmmmmmkmk , II1 , KmkmkmkmmmkK )
   else :
    IIIii1II1II = re . compile ( '<link>(.+?)</link>' ) . findall ( mmmkmk )
    if len ( IIIii1II1II ) == 1 :
     i1iiI11I = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?humbnail>(.+?)</thumbnail>' , re . DOTALL ) . findall ( mmmkmk )
     for name , url , Kmkmkmmmmmmkmk in i1iiI11I :
      if 'youtube.com/results?search_query=' in url :
       i11 ( name , url , 3 , Kmkmkmmmmmmkmk , II1 , KmkmkmkmmmkK )
      elif 'youtube.com/playlist?list=' in url :
       i11 ( name , url , 3 , Kmkmkmmmmmmkmk , II1 , KmkmkmkmmmkK )
      else :
       if 'txt' in url :
        i11 ( name , url , 3 , Kmkmkmmmmmmkmk , II1 , KmkmkmkmmmkK )
       else :
        if 'ImageH' in Kmkmkmmmmmmkmk :
         I11 ( name , url , 3 , iconimage , II1 , KmkmkmkmmmkK )
        else : I11 ( name , url , 3 , Kmkmkmmmmmmkmk , II1 , KmkmkmkmmmkK )
    else :
     name = re . compile ( '<title>(.+?)</title>' ) . findall ( mmmkmk ) [ 0 ]
     iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( mmmkmk ) [ 0 ]
     I11 ( name , mmkmkKmmKmmm , 5 , iconimage , II1 , KmkmkmkmmmkK )
  if 'SportsList' in mmkmkKmmKmmm :
   try :
    KmmkmKmkmmm = i1I1iI ( )
    mmmkKmmKKmmk = 'http://ukturk.offshorepastebin.com/UKTurk/thumbs/new/Uk%20turk%20thumbnails%20sports.jpg'
    for name , url , mKKmmmkmkKmkK in KmmkmKmkmmm :
     if 'zona' in url :
      I11 ( name + '.' , url , 10 , mmmkKmmKKmmk , II1 , KmkmkmkmmmkK )
    xbmcplugin . addSortMethod ( int ( sys . argv [ 1 ] ) , 1 )
   except : pass
   if 92 - 92: iI11ii1i1I1 . mKKKmkmmkmkmmkm + mKm
def i1I1iI ( ) :
 IiII1I11i1I1I = { 'User-Agent' : 'Mozilla/5.0 (Linux; Android 6.0.1; en-GB; SM-G935F Build/MMB29K.G935FXXU1APGG) MXPlayer/1.8.3' ,
 'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8' ,
 'Accept-Encoding' : 'gzip' ,
 'Connection' : 'Keep-Alive' }
 mKmkKm = net . http_GET ( 'http://zona-live-tv.com/zonaapp/api.php?api_key' , IiII1I11i1I1I ) . content
 i1 = 'http://zona-live-tv.com/zonaapp/api.php?cat_id=14&key=' + re . compile ( '"key":"(.+?)"' ) . findall ( mKmkKm ) [ 0 ]
 mKKmmmkKm = net . http_GET ( i1 , IiII1I11i1I1I ) . content
 KmmkmKmkmmm = re . compile ( '"channel_title":"(.+?)","channel_url":"(.+?)","channel_thumbnail":"(.+?)"' ) . findall ( mKKmmmkKm )
 return KmmkmKmkmmm
 if 78 - 78: mKKKmkmmkmkmmkm
 if 71 - 71: Kmmm + mmkmkKKmkKKKmk % i11iIiiIii + iiIiIiIi - KmKKKmkmkmKKmk
def mKmkKKmKmk ( url ) :
 IIIi1i1I = "ShowPicture(%s)" % url
 xbmc . executebuiltin ( IIIi1i1I )
 if 34 - 34: KmKKKmkmkmKKmk - KmKKKmkmkmKKmk * IiiIII111ii + mmk % KmKKKmkmkmKKmk
def i111IiI1I ( name , url , iconimage ) :
 Kmk = [ ]
 iII = [ ]
 mmkmmKmmmmkmkmkmKK = [ ]
 I1i1iiI1 = mmkmk ( url )
 I1i1iiI1 = re . sub ( r'\(.*\)' , '' , I1i1iiI1 )
 name = re . sub ( r'\(.*\)' , '' , name )
 KmmkmKKm = re . compile ( '<item>.+?<title>' + name + '</title>(.+?)</item>' , re . DOTALL ) . findall ( I1i1iiI1 ) [ 0 ]
 iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( KmmkmKKm ) [ 0 ]
 IIIii1II1II = re . compile ( '<link>(.+?)</link>' ) . findall ( KmmkmKKm )
 KmmkKmKmkmkmKKmkm = 1
 for KKKmkmkK in IIIii1II1II :
  Kmk . append ( KKKmkmkK )
  iII . append ( 'Link ' + str ( KmmkKmKmkmkmKKmkm ) )
  i11I1 = xbmcgui . Dialog ( )
  KmmkKmKmkmkmKKmkm = KmmkKmKmkmkmKKmkm + 1
 KKmKKmkmmmkmmK = i11I1 . select ( name , iII )
 if KKmKKmkmmmkmmK == - 1 :
  quit ( )
 else :
  url = Kmk [ KKmKKmkmmmkmmK ]
  if '.ts' in url : url = 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;name=' + name + '&amp;url=' + url
  KmkmmkKmkmkKmmkmmk = True
  KmkmkKmkmKKmkmkKmkmk = xbmcgui . ListItem ( name , iconImage = iconimage , thumbnailImage = iconimage ) ; KmkmkKmkmKKmkmkKmkmk . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
  KmkmmkKmkmkKmmkmmk = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = url , listitem = KmkmkKmkmKKmkmkKmkmk )
  xbmc . Player ( ) . play ( url , KmkmkKmkmKKmkmkKmkmk , False )
  return KmkmmkKmkmkKmmkmmk
  if 11 - 11: KmKKKmkmkmKKmk . iiIiIiIi
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
   if 92 - 92: iI11ii1i1I1 . iiiiiIIii
def iiii ( url ) :
 I1i1iiI1 = mmkmk ( url )
 list = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?humbnail>(.+?)</thumbnail>' , re . DOTALL ) . findall ( I1i1iiI1 )
 return list
 if 31 - 31: iiiiiIIii . i11I1IIiiIi / KmkmkmmKK
def mmkmkmkKmkm ( url , name , iconimage ) :
 mmmkKmmKKmmk = 'http://ukturk.offshorepastebin.com/UKTurk/thumbs/new/Uk%20turk%20thumbnails%20sports.jpg'
 mKKmmmkKm = net . http_GET ( url ) . content
 url = mKKmmmkKm + '|User-Agent=Mozilla/5.0 (Linux; Android 6.0.1; en-GB; SM-G935F Build/MMB29K.G935FXXU1APGG) MXPlayer/1.8.3'
 KmkmkKmkmKKmkmkKmkmk = xbmcgui . ListItem ( name , iconImage = mmmkKmmKKmmk , thumbnailImage = mmmkKmmKKmmk )
 KmkmkKmkmKKmkmkKmkmk . setPath ( url )
 xbmcplugin . setResolvedUrl ( int ( sys . argv [ 1 ] ) , True , KmkmkKmkmKKmkmkKmkmk )
 if 42 - 42: i11I1IIiiIi
def II ( url , name , iconimage ) :
 try :
  if 'search' in iconimage : iconimage = Kmkmkmmmmmmkmk
 except : pass
 if 'txt' in url :
  KmkmmmkmK ( name , url , iconimage )
 else :
  if 'youtube.com/results?search_query=' in url :
   KmkmmmkKKmk = url . split ( 'search_query=' ) [ 1 ]
   Ii1I1IIii1II = IiIi11iIIi1Ii + KmkmmmkKKmk + KmmkK
   Kmkii1ii1ii = urllib2 . Request ( Ii1I1IIii1II )
   Kmkii1ii1ii . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' )
   mmmmmKmmmkmmm = urllib2 . urlopen ( Kmkii1ii1ii )
   I1i1iiI1 = mmmmmKmmmkmmm . read ( )
   mmmmmKmmmkmmm . close ( )
   I1i1iiI1 = I1i1iiI1 . replace ( '\r' , '' ) . replace ( '\n' , '' ) . replace ( '  ' , '' )
   KmmkmKmkmmm = re . compile ( '"videoId": "(.+?)".+?"title": "(.+?)"' , re . DOTALL ) . findall ( I1i1iiI1 )
   for I1I1IiI1 , name in KmmkmKmkmmm :
    url = 'https://www.youtube.com/watch?v=' + I1I1IiI1
    I11 ( name , url , 3 , iconimage , II1 )
  elif 'youtube.com/playlist?list=' in url :
   KmkmmmkKKmk = url . split ( 'playlist?list=' ) [ 1 ]
   Ii1I1IIii1II = IiI + KmkmmmkKKmk + mmKm
   Kmkii1ii1ii = urllib2 . Request ( Ii1I1IIii1II )
   Kmkii1ii1ii . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' )
   mmmmmKmmmkmmm = urllib2 . urlopen ( Kmkii1ii1ii )
   I1i1iiI1 = mmmmmKmmmkmmm . read ( )
   mmmmmKmmmkmmm . close ( )
   I1i1iiI1 = I1i1iiI1 . replace ( '\r' , '' ) . replace ( '\n' , '' ) . replace ( '  ' , '' )
   KmmkmKmkmmm = re . compile ( '"title": "(.+?)".+?"videoId": "(.+?)"' , re . DOTALL ) . findall ( I1i1iiI1 )
   for name , I1I1IiI1 in KmmkmKmkmmm :
    url = 'https://www.youtube.com/watch?v=' + I1I1IiI1
    I11 ( name , url , 3 , iconimage , II1 )
  else :
   if urlresolver . HostedMediaFile ( url ) . valid_url ( ) :
    Kmk = urlresolver . HostedMediaFile ( url ) . resolve ( )
   elif '.ts' in url :
    url = 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;name=' + name + '&amp;url=' + url
    KmkmmkKmkmkKmmkmmk = True
    KmkmkKmkmKKmkmkKmkmk = xbmcgui . ListItem ( name , iconImage = iconimage , thumbnailImage = iconimage ) ; KmkmkKmkmKKmkmkKmkmk . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
    KmkmmkKmkmkKmmkmmk = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = url , listitem = KmkmkKmkmKKmkmkKmkmk )
    xbmc . Player ( ) . play ( url , KmkmkKmkmKKmkmkKmkmk , False )
    return KmkmmkKmkmkKmmkmmk
   else :
    Kmk = url
    KmkmkKmkmKKmkmkKmkmk = xbmcgui . ListItem ( name , iconImage = iconimage , thumbnailImage = iconimage )
    KmkmkKmkmKKmkmkKmkmk . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
    KmkmkKmkmKKmkmkKmkmk . setPath ( Kmk )
    xbmcplugin . setResolvedUrl ( int ( sys . argv [ 1 ] ) , True , KmkmkKmkmKKmkmkKmkmk )
    if 5 - 5: mKm * mmkmkKKmkKKKmk + i11I1IIiiIi . Kmmm + i11I1IIiiIi
    #################################################################################	   
def mK ( ) :
 iIi1IIIi1 = ''
 KmkmKmKKKmKK = 'https://script.google.com/macros/s/AKfycbyBcUa5TlEQudk6Y_0o0ZubnmhGL_-b7Up8kQt11xgVwz3ErTo/exec?588677963413065728'
 Kmkii1ii1ii = urllib2 . Request ( KmkmKmKKKmKK )
 Kmkii1ii1ii . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' )
 mmmmmKmmmkmmm = urllib2 . urlopen ( Kmkii1ii1ii )
 I1i1iiI1 = mmmmmKmmmkmmm . read ( )
 mmmmmKmmmkmmm . close ( )
 I1i1iiI1 = I1i1iiI1 . replace ( '/n' , '' )
 I1i1iiI1 = I1i1iiI1 . decode ( 'utf-8' ) . encode ( 'utf-8' ) . replace ( '&#39;' , '\'' ) . replace ( '&#10;' , ' - ' ) . replace ( '&#x2026;' , '' )
 KmmkmKmkmmm = re . compile ( "<title>(.+?)</title>.+?<pubDate>(.+?)</pubDate>" , re . DOTALL ) . findall ( I1i1iiI1 ) [ 1 : ]
 for ii1ii11IIIiiI , KmkmkKKKmKmmmkK in KmmkmKmkmmm :
  try :
   ii1ii11IIIiiI = ii1ii11IIIiiI . decode ( 'ascii' , 'ignore' )
  except :
   ii1ii11IIIiiI = ii1ii11IIIiiI . decode ( 'utf-8' , 'ignore' )
  KmkmkKKKmKmmmkK = KmkmkKKKmKmmmkK [ : - 15 ]
  ii1ii11IIIiiI = ii1ii11IIIiiI . replace ( '&amp;' , '' )
  KmkmkKKKmKmmmkK = '[COLOR blue][B]' + KmkmkKKKmKmmmkK + '[/B][/COLOR]'
  iIi1IIIi1 = iIi1IIIi1 + KmkmkKKKmKmmmkK + '\n' + ii1ii11IIIiiI + '\n' + '\n'
 KmkmkmkKKmmkmkmm ( '[COLOR blue][B]@uk_turk[/B][/COLOR]' , iIi1IIIi1 )
 if 71 - 71: i11iIiiIii + KmKKKmkmkmKKmk
def KmkmkmkKKmmkmkmm ( heading , text ) :
 id = 10147
 xbmc . executebuiltin ( 'ActivateWindow(%d)' % id )
 xbmc . sleep ( 100 )
 mKmmKKmkmkKm = xbmcgui . Window ( id )
 i1iIIIi1i = 50
 while ( i1iIIIi1i > 0 ) :
  try :
   xbmc . sleep ( 10 )
   i1iIIIi1i -= 1
   mKmmKKmkmkKm . getControl ( 1 ) . setLabel ( heading )
   mKmmKKmkmkKm . getControl ( 5 ) . setText ( text )
   return
  except :
   pass
   if 43 - 43: i11I1IIiiIi % Kmmm
def mmkmk ( url ) :
 if 'UKTurk.db' in url :
  KKmKmmmkmkmm = open ( Kmmmmkmkmkm , 'r' )
  I1i1iiI1 = KKmKmmmkmkmm . read ( )
 else :
  url = url . replace ( ' ' , '%20' )
  I1i1iiI1 = net . http_GET ( url ) . content . replace ( '\r' , '' ) . replace ( '\t' , '' ) . replace ( '&nbsp;' , '' ) . replace ( '\'' , '' ) . replace ( '\n' , '' )
  I1i1iiI1 = iiiiiiii1 ( I1i1iiI1 )
 return I1i1iiI1
 if 18 - 18: mKm % iI11ii1i1I1 * KmkmkmmKK
def iiIIIII1i1iI ( url ) :
 url = url . replace ( ' ' , '%20' )
 I1i1iiI1 = net . http_GET ( url ) . content . replace ( '\r' , '' ) . replace ( '\t' , '' ) . replace ( '&nbsp;' , '' ) . replace ( '\'' , '' ) . replace ( '\n' , '' )
 return I1i1iiI1
 if 87 - 87: i11iIiiIii
def iiiiiiii1 ( gobble ) :
 gobble = gobble . replace ( '}' , '' ) . replace ( '{' , '' ) . replace ( ',' , '' ) . replace ( ']' , '' ) . replace ( '[' , '' )
 gobble = gobble + '=='
 gobble = gobble . decode ( 'base64' )
 return gobble
 if 93 - 93: iiIiIiIi - IiI1I1 % i11iIiiIii . iI11ii1i1I1 / iI11ii1i1I1 - iiiiiIIii
def IIII ( ) :
 iiIiI = [ ]
 mmkmkmmmKmkKm = sys . argv [ 2 ]
 if len ( mmkmkmmmKmkKm ) >= 2 :
  mmkKmkKKKmkKmm = sys . argv [ 2 ]
  iiIiII1 = mmkKmkKKKmkKmm . replace ( '?' , '' )
  if ( mmkKmkKKKmkKmm [ len ( mmkKmkKKKmkKmm ) - 1 ] == '/' ) :
   mmkKmkKKKmkKmm = mmkKmkKKKmkKmm [ 0 : len ( mmkKmkKKKmkKmm ) - 2 ]
  KKKmkmkKmkK = iiIiII1 . split ( '&' )
  iiIiI = { }
  for KmmkKmKmkmkmKKmkm in range ( len ( KKKmkmkKmkK ) ) :
   iii = { }
   iii = KKKmkmkKmkK [ KmmkKmKmkmkmKKmkm ] . split ( '=' )
   if ( len ( iii ) ) == 2 :
    iiIiI [ iii [ 0 ] ] = iii [ 1 ]
 return iiIiI
 if 90 - 90: mKm % Kmkm / IiI1I1
def i11 ( name , url , mode , iconimage , fanart , description = '' ) :
 IIi = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&iconimage=" + urllib . quote_plus ( iconimage ) + "&description=" + urllib . quote_plus ( description )
 KmkmmkKmkmkKmmkmmk = True
 KmkmkKmkmKKmkmkKmkmk = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 KmkmkKmkmKKmkmkKmkmk . setInfo ( type = "Video" , infoLabels = { "Title" : name , 'plot' : description } )
 KmkmkKmkmKKmkmkKmkmk . setProperty ( 'fanart_image' , fanart )
 i1Iii1i1I = [ ]
 i1Iii1i1I . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=6&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 if description == 'yes' :
  i1Iii1i1I . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=8&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 KmkmkKmkmKKmkmkKmkmk . addContextMenuItems ( items = i1Iii1i1I , replaceItems = True )
 KmkmmkKmkmkKmmkmmk = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = IIi , listitem = KmkmkKmkmKKmkmkKmkmk , isFolder = True )
 return KmkmmkKmkmkKmmkmmk
 if 91 - 91: iiIiIiIi + IiiIII111ii . Kmmm * iiIiIiIi + IiiIII111ii * i1iIIi1
def I11 ( name , url , mode , iconimage , fanart , description = '' ) :
 IIi = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&iconimage=" + urllib . quote_plus ( iconimage ) + "&description=" + urllib . quote_plus ( description )
 KmkmmkKmkmkKmmkmmk = True
 KmkmkKmkmKKmkmkKmkmk = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 KmkmkKmkmKKmkmkKmkmk . setProperty ( 'fanart_image' , fanart )
 if not mode == 2 :
  KmkmkKmkmKKmkmkKmkmk . setInfo ( type = "Video" , infoLabels = { "Title" : name , 'plot' : description } )
  KmkmkKmkmKKmkmkKmkmk . setProperty ( "IsPlayable" , "true" )
  i1Iii1i1I = [ ]
  if not 'BL' in description :
   i1Iii1i1I . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=6&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
  if 'yes' in description :
   i1Iii1i1I . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=8&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
  KmkmkKmkmKKmkmkKmkmk . addContextMenuItems ( items = i1Iii1i1I , replaceItems = True )
 KmkmmkKmkmkKmmkmmk = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = IIi , listitem = KmkmkKmkmKKmkmkKmkmk , isFolder = False )
 return KmkmmkKmkmkKmmkmmk
 if 80 - 80: iI11ii1i1I1 % Kmmm % mmkmmmKmkKKmkK - i1iIIi1 + i1iIIi1
def i11i1 ( name , url , mode , iconimage , fanart , description = '' ) :
 IIi = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&iconimage=" + urllib . quote_plus ( iconimage ) + "&description=" + urllib . quote_plus ( description )
 KmkmmkKmkmkKmmkmmk = True
 KmkmkKmkmKKmkmkKmkmk = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 KmkmkKmkmKKmkmkKmkmk . setProperty ( 'fanart_image' , fanart )
 KmkmmkKmkmkKmmkmmk = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = IIi , listitem = KmkmkKmkmKKmkmkKmkmk , isFolder = False )
 return KmkmmkKmkmkKmmkmmk
 if 19 - 19: i11I1IIiiIi * Kmkm
def IiIiiI ( name , url , mode , iconimage , itemcount , isFolder = False ) :
 if KKKmmk == 'true' :
  if not 'COLOR' in name :
   ii111iI1iIi1 = name . partition ( '(' )
   KKK = ""
   mmmkKKmmk = ""
   if len ( ii111iI1iIi1 ) > 0 :
    KKK = ii111iI1iIi1 [ 0 ]
    mmmkKKmmk = ii111iI1iIi1 [ 2 ] . partition ( ')' )
   if len ( mmmkKKmmk ) > 0 :
    mmmkKKmmk = mmmkKKmmk [ 0 ]
   I11IiI = metahandlers . MetaData ( )
   KmkmmKmkKmmkmkm = I11IiI . get_meta ( 'movie' , name = KKK , year = mmmkKKmmk )
   IIi = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&site=" + str ( mmKmkmKKmmKmmk ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name )
   KmkmmkKmkmkKmmkmmk = True
   KmkmkKmkmKKmkmkKmkmk = xbmcgui . ListItem ( name , iconImage = KmkmmKmkKmmkmkm [ 'cover_url' ] , thumbnailImage = KmkmmKmkKmmkmkm [ 'cover_url' ] )
   KmkmkKmkmKKmkmkKmkmk . setInfo ( type = "Video" , infoLabels = KmkmmKmkKmmkmkm )
   KmkmkKmkmKKmkmkKmkmk . setProperty ( "IsPlayable" , "true" )
   i1I1ii11i1Iii = [ ]
   i1I1ii11i1Iii . append ( ( 'Movie Information' , 'XBMC.Action(Info)' ) )
   i1I1ii11i1Iii . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=6&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , KmkmmKmkKmmkmkm [ 'cover_url' ] ) ) )
   KmkmkKmkmKKmkmkKmkmk . addContextMenuItems ( i1I1ii11i1Iii , replaceItems = True )
   if not KmkmmKmkKmmkmkm [ 'backdrop_url' ] == '' : KmkmkKmkmKKmkmkKmkmk . setProperty ( 'fanart_image' , KmkmmKmkKmmkmkm [ 'backdrop_url' ] )
   else : KmkmkKmkmKKmkmkKmkmk . setProperty ( 'fanart_image' , II1 )
   KmkmmkKmkmkKmmkmmk = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = IIi , listitem = KmkmkKmkmKKmkmkKmkmk , isFolder = isFolder , totalItems = itemcount )
   return KmkmmkKmkmkKmmkmmk
 else :
  IIi = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&site=" + str ( mmKmkmKKmmKmmk ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name )
  KmkmmkKmkmkKmmkmmk = True
  KmkmkKmkmKKmkmkKmkmk = xbmcgui . ListItem ( name , iconImage = iconimage , thumbnailImage = iconimage )
  KmkmkKmkmKKmkmkKmkmk . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
  KmkmkKmkmKKmkmkKmkmk . setProperty ( 'fanart_image' , II1 )
  KmkmkKmkmKKmkmkKmkmk . setProperty ( "IsPlayable" , "true" )
  i1Iii1i1I = [ ]
  i1Iii1i1I . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=6&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
  KmkmkKmkmKKmkmkKmkmk . addContextMenuItems ( items = i1Iii1i1I , replaceItems = True )
  KmkmmkKmkmkKmmkmmk = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = IIi , listitem = KmkmkKmkmKKmkmkKmkmk , isFolder = isFolder )
  return KmkmmkKmkmkKmmkmmk
  if 26 - 26: mKKKmkmmkmkmmkm - I1iII1iiII - IiiIII111ii / IiI1I1 . i11I1IIiiIi % I1iII1iiII
def KK ( content , viewType ) :
 if content :
  xbmcplugin . setContent ( int ( sys . argv [ 1 ] ) , content )
 if KmmkKmm . getSetting ( 'auto-view' ) == 'true' :
  xbmc . executebuiltin ( "Container.SetViewMode(%s)" % KmmkKmm . getSetting ( viewType ) )
  if 25 - 25: IiI1I1
mmkKmkKKKmkKmm = IIII ( ) ; i1 = None ; mmkmKmKmkmkm = None ; mKmmkmK = None ; mmKmkmKKmmKmmk = None ; mKmkmkmKm = None
try : mmKmkmKKmmKmmk = urllib . unquote_plus ( mmkKmkKKKmkKmm [ "site" ] )
except : pass
try : i1 = urllib . unquote_plus ( mmkKmkKKKmkKmm [ "url" ] )
except : pass
try : mmkmKmKmkmkm = urllib . unquote_plus ( mmkKmkKKKmkKmm [ "name" ] )
except : pass
try : mKmmkmK = int ( mmkKmkKKKmkKmm [ "mode" ] )
except : pass
try : mKmkmkmKm = urllib . unquote_plus ( mmkKmkKKKmkKmm [ "iconimage" ] )
except : pass
if 51 - 51: i1iIIi1 - mmkmmmKmkKKmkK + i11IiIiiIIIII * mmk . mKKKmkmmkmkmmkm + mmkmmmKmkKKmkK
if mKmmkmK == None or i1 == None or len ( i1 ) < 1 : Kmkmkm ( )
elif mKmmkmK == 1 : KmkmmmkmK ( mmkmKmKmkmkm , i1 , mKmkmkmKm )
elif mKmmkmK == 2 : mK ( )
elif mKmmkmK == 3 : II ( i1 , mmkmKmKmkmkm , mKmkmkmKm )
elif mKmmkmK == 4 : iI1Ii11111iIi ( )
elif mKmmkmK == 5 : i111IiI1I ( mmkmKmKmkmkm , i1 , Kmkmkmmmmmmkmk )
elif mKmmkmK == 6 : mKmk ( mmkmKmKmkmkm , i1 , mKmkmkmKm )
elif mKmmkmK == 7 : GETFAVS ( i1 )
elif mKmmkmK == 8 : ii11iIi1I ( mmkmKmKmkmkm , i1 , mKmkmkmKm )
elif mKmmkmK == 9 : mKmkKKmKmk ( i1 )
elif mKmmkmK == 10 : mmkmkmkKmkm ( i1 , mmkmKmKmkmkm , mKmkmkmKm )
if 78 - 78: i11iIiiIii / iI11ii1i1I1 - mmk / Kmmm + mmkmmmKmkKKmkK
if 82 - 82: mmk
xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
if 46 - 46: iiiii11iII1 . i11iIiiIii
if 94 - 94: mKm * mmk / i1iIIi1 / mmk
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3
