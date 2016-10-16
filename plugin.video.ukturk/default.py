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
 elif 'XXX' not in url :
  I1I = url
  I1i1iiI1 = mmkmk ( url )
  I1i1iiI1 = I1i1iiI1 . replace ( 'Image' , 'image' )
  mKKmkmkmKK = ''
  if '<FAV>' in I1i1iiI1 : mKKmkmkmKK = 'yes'
  if 'SportsList' in url : mKKmkmkmKK = mKKmkmkmKK + 'BL'
  if 'Live%20TV' in url : mKKmkmkmKK = mKKmkmkmKK + 'BL'
  KmmkmKmkmmm = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( I1i1iiI1 )
  for mmmkmk in KmmkmKmkmmm :
   if '<image>' in mmmkmk :
    KmKm = re . compile ( '<title>(.+?)</title>.+?image>(.+?)</image>.+?humbnail>(.+?)</thumbnail>' , re . DOTALL ) . findall ( mmmkmk )
    for name , url , Kmkmkmmmmmmkmk in KmKm :
     url = url . replace ( 'http://imgur.com/' , 'http://i.imgur.com/' ) + '.jpg'
     Kmkmkmmmmmmkmk = Kmkmkmmmmmmkmk . replace ( 'http://imgur.com/' , 'http://i.imgur.com/' ) + '.jpg'
     if 'ImageH' in Kmkmkmmmmmmkmk :
      iI ( name , url , 9 , iconimage , II1 , mKKmkmkmKK )
     else :
      iI ( name , url , '9' , Kmkmkmmmmmmkmk , II1 , mKKmkmkmKK )
   else :
    mmkmkK = re . compile ( '<link>(.+?)</link>' ) . findall ( mmmkmk )
    if len ( mmkmkK ) == 1 :
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
def KKKmkKKKmkmkmm ( url ) :
 IIIi1i1I = "ShowPicture(%s)" % url
 xbmc . executebuiltin ( IIIi1i1I )
 if 31 - 31: i11IIiiIii - KmkmkmkmmmkK . mKKmKmmkmkm - i11IiIiiIIIII % KmkmkmkmmmkK
def KmmmkKKmk ( name , url , iconimage ) :
 KmKmkKmk = [ ]
 II1i1IiiIIi11 = [ ]
 iI1Ii11iII1 = [ ]
 I1i1iiI1 = mmkmk ( url )
 I1i1iiI1 = re . sub ( r'\(.*\)' , '' , I1i1iiI1 )
 name = re . sub ( r'\(.*\)' , '' , name )
 KmmkKmkKmkmmKmkK = re . compile ( '<item>.+?<title>' + name + '</title>(.+?)</item>' , re . DOTALL ) . findall ( I1i1iiI1 ) [ 0 ]
 iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( KmmkKmkKmkmmKmkK ) [ 0 ]
 mmkmkK = re . compile ( '<link>(.+?)</link>' ) . findall ( KmmkKmkKmkmmKmkK )
 IIIIii = 1
 for Kmkmmk in mmkmkK :
  KmKmkKmk . append ( Kmkmmk )
  II1i1IiiIIi11 . append ( 'Link ' + str ( IIIIii ) )
  i11I1 = xbmcgui . Dialog ( )
  IIIIii = IIIIii + 1
 KKmkmkKm = i11I1 . select ( name , II1i1IiiIIi11 )
 if KKmkmkKm == - 1 :
  quit ( )
 else :
  url = KmKmkKmk [ KKmkmkKm ]
  KmkKKKmkKKmKmkK = True
  KmkmkKmmkmkmkmmKmk = xbmcgui . ListItem ( name , iconImage = iconimage , thumbnailImage = iconimage ) ; KmkmkKmmkmkmkmmKmk . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
  KmkKKKmkKKmKmkK = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = url , listitem = KmkmkKmmkmkmkmmKmk )
  KmkmkKmmkmkmkmmKmk . setPath ( url )
  xbmcplugin . setResolvedUrl ( int ( sys . argv [ 1 ] ) , True , KmkmkKmmkmkmkmmKmk )
  if 100 - 100: KmkmkmmKK + i11IIiiIii - Kmmm + i11iIiiIii * mmk
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
   if 30 - 30: mKm . mmk - iiiii11iII1
def iiii ( url ) :
 I1i1iiI1 = mmkmk ( url )
 list = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?humbnail>(.+?)</thumbnail>' , re . DOTALL ) . findall ( I1i1iiI1 )
 return list
 if 8 - 8: Kmkm - I1iII1iiII * i11IiIiiIIIII + i11iIiiIii / KmkmkmkmmmkK % Kmmm
def iIIIi1 ( url , name , iconimage ) :
 try :
  if 'search' in iconimage : iconimage = Kmkmkmmmmmmkmk
 except : pass
 if 'txt' in url :
  KmkmmmkmK ( name , url , iconimage )
 else :
  if 'youtube.com/results?search_query=' in url :
   KmkmmmkKKmk = url . split ( 'search_query=' ) [ 1 ]
   iiII1i1 = IiIi11iIIi1Ii + KmkmmmkKKmk + KmmkK
   mmkmkmKKmkm = urllib2 . Request ( iiII1i1 )
   mmkmkmKKmkm . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' )
   KKKmkmkK = urllib2 . urlopen ( mmkmkmKKmkm )
   I1i1iiI1 = KKKmkmkK . read ( )
   KKKmkmkK . close ( )
   I1i1iiI1 = I1i1iiI1 . replace ( '\r' , '' ) . replace ( '\n' , '' ) . replace ( '  ' , '' )
   KmmkmKmkmmm = re . compile ( '"videoId": "(.+?)".+?"title": "(.+?)"' , re . DOTALL ) . findall ( I1i1iiI1 )
   for KKmKKmkmmmkmmK , name in KmmkmKmkmmm :
    url = 'https://www.youtube.com/watch?v=' + KKmKKmkmmmkmmK
    I11 ( name , url , 3 , iconimage , II1 )
  elif 'youtube.com/playlist?list=' in url :
   KmkmmmkKKmk = url . split ( 'playlist?list=' ) [ 1 ]
   iiII1i1 = IiI + KmkmmmkKKmk + mmKm
   mmkmkmKKmkm = urllib2 . Request ( iiII1i1 )
   mmkmkmKKmkm . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' )
   KKKmkmkK = urllib2 . urlopen ( mmkmkmKKmkm )
   I1i1iiI1 = KKKmkmkK . read ( )
   KKKmkmkK . close ( )
   I1i1iiI1 = I1i1iiI1 . replace ( '\r' , '' ) . replace ( '\n' , '' ) . replace ( '  ' , '' )
   KmmkmKmkmmm = re . compile ( '"title": "(.+?)".+?"videoId": "(.+?)"' , re . DOTALL ) . findall ( I1i1iiI1 )
   for name , KKmKKmkmmmkmmK in KmmkmKmkmmm :
    url = 'https://www.youtube.com/watch?v=' + KKmKKmkmmmkmmK
    I11 ( name , url , 3 , iconimage , II1 )
  else :
   if urlresolver . HostedMediaFile ( url ) . valid_url ( ) :
    KmKmkKmk = urlresolver . HostedMediaFile ( url ) . resolve ( )
   else : KmKmkKmk = url
   KmkmkKmmkmkmkmmKmk = xbmcgui . ListItem ( name , iconImage = iconimage , thumbnailImage = iconimage )
   KmkmkKmmkmkmkmmKmk . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
   KmkmkKmmkmkmkmmKmk . setPath ( KmKmkKmk )
   xbmcplugin . setResolvedUrl ( int ( sys . argv [ 1 ] ) , True , KmkmkKmmkmkmkmmKmk )
   if 98 - 98: iI11ii1i1I1 * iI11ii1i1I1 / iI11ii1i1I1 + mKKKmkmmkmkmmkm
   #################################################################################	   
def ii111111I1iII ( ) :
 KmkmkmmmmkKmk = ''
 i1iIi1iIi1i = 'https://script.google.com/macros/s/AKfycbyBcUa5TlEQudk6Y_0o0ZubnmhGL_-b7Up8kQt11xgVwz3ErTo/exec?588677963413065728'
 mmkmkmKKmkm = urllib2 . Request ( i1iIi1iIi1i )
 mmkmkmKKmkm . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' )
 KKKmkmkK = urllib2 . urlopen ( mmkmkmKKmkm )
 I1i1iiI1 = KKKmkmkK . read ( )
 KKKmkmkK . close ( )
 I1i1iiI1 = I1i1iiI1 . replace ( '/n' , '' )
 I1i1iiI1 = I1i1iiI1 . decode ( 'utf-8' ) . encode ( 'utf-8' ) . replace ( '&#39;' , '\'' ) . replace ( '&#10;' , ' - ' ) . replace ( '&#x2026;' , '' )
 KmmkmKmkmmm = re . compile ( "<title>(.+?)</title>.+?<pubDate>(.+?)</pubDate>" , re . DOTALL ) . findall ( I1i1iiI1 ) [ 1 : ]
 for I1I1iIiII1 , i11i1I1 in KmmkmKmkmmm :
  try :
   I1I1iIiII1 = I1I1iIiII1 . decode ( 'ascii' , 'ignore' )
  except :
   I1I1iIiII1 = I1I1iIiII1 . decode ( 'utf-8' , 'ignore' )
  i11i1I1 = i11i1I1 [ : - 15 ]
  I1I1iIiII1 = I1I1iIiII1 . replace ( '&amp;' , '' )
  i11i1I1 = '[COLOR blue][B]' + i11i1I1 + '[/B][/COLOR]'
  KmkmkmmmmkKmk = KmkmkmmmmkKmk + i11i1I1 + '\n' + I1I1iIiII1 + '\n' + '\n'
 ii1I ( '[COLOR blue][B]@uk_turk[/B][/COLOR]' , KmkmkmmmmkKmk )
 if 67 - 67: i11iIiiIii - Kmkm % iiIiIiIi . KmkmkmmKK
def ii1I ( heading , text ) :
 id = 10147
 xbmc . executebuiltin ( 'ActivateWindow(%d)' % id )
 xbmc . sleep ( 100 )
 mmkmm = xbmcgui . Window ( id )
 mmmmmKmmmkmmm = 50
 while ( mmmmmKmmmkmmm > 0 ) :
  try :
   xbmc . sleep ( 10 )
   mmmmmKmmmkmmm -= 1
   mmkmm . getControl ( 1 ) . setLabel ( heading )
   mmkmm . getControl ( 5 ) . setText ( text )
   return
  except :
   pass
   if 6 - 6: mKKKmkmmkmkmmkm - mmk + I1iII1iiII - KmkmkmkmmmkK - i11iIiiIii
def mmkmk ( url ) :
 if 'UKTurk.db' in url :
  KKmKmmmkmkmm = open ( Kmmmmkmkmkm , 'r' )
  I1i1iiI1 = KKmKmmmkmkmm . read ( )
 else :
  url = url . replace ( ' ' , '%20' )
  I1i1iiI1 = net . http_GET ( url ) . content . replace ( '\r' , '' ) . replace ( '\t' , '' ) . replace ( '&nbsp;' , '' ) . replace ( '\'' , '' ) . replace ( '\n' , '' )
  I1i1iiI1 = KKmkmKKmkK ( I1i1iiI1 )
 return I1i1iiI1
 if 91 - 91: KmkmkmmKK
def iiIIIII1i1iI ( url ) :
 url = url . replace ( ' ' , '%20' )
 I1i1iiI1 = net . http_GET ( url ) . content . replace ( '\r' , '' ) . replace ( '\t' , '' ) . replace ( '&nbsp;' , '' ) . replace ( '\'' , '' ) . replace ( '\n' , '' )
 return I1i1iiI1
 if 61 - 61: i11IiIiiIIIII
def KKmkmKKmkK ( gobble ) :
 gobble = gobble . replace ( '}' , '' ) . replace ( '{' , '' ) . replace ( ',' , '' ) . replace ( ']' , '' ) . replace ( '[' , '' )
 gobble = gobble + '=='
 gobble = gobble . decode ( 'base64' )
 return gobble
 if 64 - 64: mKKmKmmkmkm / i11I1IIiiIi - KmkmkmmKK - mKKKmkmmkmkmmkm
def KmkmKmKKKmKK ( ) :
 ii1ii11IIIiiI = [ ]
 KmkmkKKKmKmmmkK = sys . argv [ 2 ]
 if len ( KmkmkKKKmKmmmkK ) >= 2 :
  KmkmkmkKKmmkmkmm = sys . argv [ 2 ]
  mmmkKKm = KmkmkmkKKmmkmkmm . replace ( '?' , '' )
  if ( KmkmkmkKKmmkmkmm [ len ( KmkmkmkKKmmkmkmm ) - 1 ] == '/' ) :
   KmkmkmkKKmmkmkmm = KmkmkmkKKmmkmkmm [ 0 : len ( KmkmkmkKKmmkmkmm ) - 2 ]
  mmKKKmkmkKmm = mmmkKKm . split ( '&' )
  ii1ii11IIIiiI = { }
  for IIIIii in range ( len ( mmKKKmkmkKmm ) ) :
   IiIIIi1iIi = { }
   IiIIIi1iIi = mmKKKmkmkKmm [ IIIIii ] . split ( '=' )
   if ( len ( IiIIIi1iIi ) ) == 2 :
    ii1ii11IIIiiI [ IiIIIi1iIi [ 0 ] ] = IiIIIi1iIi [ 1 ]
 return ii1ii11IIIiiI
 if 68 - 68: i11iIiiIii % iiIiIiIi + i11iIiiIii
def i11 ( name , url , mode , iconimage , fanart , description = '' ) :
 iii = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&iconimage=" + urllib . quote_plus ( iconimage ) + "&description=" + urllib . quote_plus ( description )
 KmkKKKmkKKmKmkK = True
 KmkmkKmmkmkmkmmKmk = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 KmkmkKmmkmkmkmmKmk . setInfo ( type = "Video" , infoLabels = { "Title" : name , 'plot' : description } )
 KmkmkKmmkmkmkmmKmk . setProperty ( 'fanart_image' , fanart )
 II1I = [ ]
 II1I . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=6&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 if description == 'yes' :
  II1I . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=8&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 KmkmkKmmkmkmkmmKmk . addContextMenuItems ( items = II1I , replaceItems = True )
 KmkKKKmkKKmKmkK = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = iii , listitem = KmkmkKmmkmkmkmmKmk , isFolder = True )
 return KmkKKKmkKKmKmkK
 if 84 - 84: i11IIiiIii . i11iIiiIii . i11IIiiIii * iiIiIiIi - mKKKmkmmkmkmmkm
def I11 ( name , url , mode , iconimage , fanart , description = '' ) :
 iii = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&iconimage=" + urllib . quote_plus ( iconimage ) + "&description=" + urllib . quote_plus ( description )
 KmkKKKmkKKmKmkK = True
 KmkmkKmmkmkmkmmKmk = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 KmkmkKmmkmkmkmmKmk . setProperty ( 'fanart_image' , fanart )
 if not mode == 2 :
  KmkmkKmmkmkmkmmKmk . setInfo ( type = "Video" , infoLabels = { "Title" : name , 'plot' : description } )
  KmkmkKmmkmkmkmmKmk . setProperty ( "IsPlayable" , "true" )
  II1I = [ ]
  if not 'BL' in description :
   II1I . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=6&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
  if 'yes' in description :
   II1I . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=8&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
  KmkmkKmmkmkmkmmKmk . addContextMenuItems ( items = II1I , replaceItems = True )
 KmkKKKmkKKmKmkK = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = iii , listitem = KmkmkKmmkmkmkmmKmk , isFolder = False )
 return KmkKKKmkKKmKmkK
 if 42 - 42: i11iIiiIii
def iI ( name , url , mode , iconimage , fanart , description = '' ) :
 iii = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&iconimage=" + urllib . quote_plus ( iconimage ) + "&description=" + urllib . quote_plus ( description )
 KmkKKKmkKKmKmkK = True
 KmkmkKmmkmkmkmmKmk = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 KmkmkKmmkmkmkmmKmk . setProperty ( 'fanart_image' , fanart )
 KmkKKKmkKKmKmkK = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = iii , listitem = KmkmkKmmkmkmkmmKmk , isFolder = False )
 return KmkKKKmkKKmKmkK
 if 33 - 33: iI11ii1i1I1 - KmkmkmmKK * Kmkm * mKm - i1iIIi1
def IiIiiI ( name , url , mode , iconimage , itemcount , isFolder = False ) :
 if KKKmmk == 'true' :
  if not 'COLOR' in name :
   iiIiI = name . partition ( '(' )
   mmkmkmmmKmkKm = ""
   mmkKmkKKKmkKmm = ""
   if len ( iiIiI ) > 0 :
    mmkmkmmmKmkKm = iiIiI [ 0 ]
    mmkKmkKKKmkKmm = iiIiI [ 2 ] . partition ( ')' )
   if len ( mmkKmkKKKmkKmm ) > 0 :
    mmkKmkKKKmkKmm = mmkKmkKKKmkKmm [ 0 ]
   iiIiII1 = metahandlers . MetaData ( )
   KKKmkmkKmkK = iiIiII1 . get_meta ( 'movie' , name = mmkmkmmmKmkKm , year = mmkKmkKKKmkKmm )
   iii = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&site=" + str ( iiimKmmKKKmKm ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name )
   KmkKKKmkKKmKmkK = True
   KmkmkKmmkmkmkmmKmk = xbmcgui . ListItem ( name , iconImage = KKKmkmkKmkK [ 'cover_url' ] , thumbnailImage = KKKmkmkKmkK [ 'cover_url' ] )
   KmkmkKmmkmkmkmmKmk . setInfo ( type = "Video" , infoLabels = KKKmkmkKmkK )
   KmkmkKmmkmkmkmmKmk . setProperty ( "IsPlayable" , "true" )
   i1Iii1i1I = [ ]
   i1Iii1i1I . append ( ( 'Movie Information' , 'XBMC.Action(Info)' ) )
   i1Iii1i1I . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=6&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , KKKmkmkKmkK [ 'cover_url' ] ) ) )
   KmkmkKmmkmkmkmmKmk . addContextMenuItems ( i1Iii1i1I , replaceItems = True )
   if not KKKmkmkKmkK [ 'backdrop_url' ] == '' : KmkmkKmmkmkmkmmKmk . setProperty ( 'fanart_image' , KKKmkmkKmkK [ 'backdrop_url' ] )
   else : KmkmkKmmkmkmkmmKmk . setProperty ( 'fanart_image' , II1 )
   KmkKKKmkKKmKmkK = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = iii , listitem = KmkmkKmmkmkmkmmKmk , isFolder = isFolder , totalItems = itemcount )
   return KmkKKKmkKKmKmkK
 else :
  iii = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&site=" + str ( iiimKmmKKKmKm ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name )
  KmkKKKmkKKmKmkK = True
  KmkmkKmmkmkmkmmKmk = xbmcgui . ListItem ( name , iconImage = iconimage , thumbnailImage = iconimage )
  KmkmkKmmkmkmkmmKmk . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
  KmkmkKmmkmkmkmmKmk . setProperty ( 'fanart_image' , II1 )
  KmkmkKmmkmkmkmmKmk . setProperty ( "IsPlayable" , "true" )
  II1I = [ ]
  II1I . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=6&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
  KmkmkKmmkmkmkmmKmk . addContextMenuItems ( items = II1I , replaceItems = True )
  KmkKKKmkKKmKmkK = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = iii , listitem = KmkmkKmmkmkmkmmKmk , isFolder = isFolder )
  return KmkKKKmkKKmKmkK
  if 91 - 91: iiIiIiIi + IiiIII111ii . Kmmm * iiIiIiIi + IiiIII111ii * i1iIIi1
def KmkmkmkKKKKKm ( content , viewType ) :
 if content :
  xbmcplugin . setContent ( int ( sys . argv [ 1 ] ) , content )
 if KmmkKmm . getSetting ( 'auto-view' ) == 'true' :
  xbmc . executebuiltin ( "Container.SetViewMode(%s)" % KmmkKmm . getSetting ( viewType ) )
  if 22 - 22: Kmkm + KmkmkmmKK . I1iII1iiII * iI11ii1i1I1 % i11iIiiIii * IiiIII111ii
KmkmkmkKKmmkmkmm = KmkmKmKKKmKK ( ) ; i1 = None ; mmkmKmKmkmkm = None ; mmmkmkmkm = None ; iiimKmmKKKmKm = None ; mKmkmkmKm = None
try : iiimKmmKKKmKm = urllib . unquote_plus ( KmkmkmkKKmmkmkmm [ "site" ] )
except : pass
try : i1 = urllib . unquote_plus ( KmkmkmkKKmmkmkmm [ "url" ] )
except : pass
try : mmkmKmKmkmkm = urllib . unquote_plus ( KmkmkmkKKmmkmkmm [ "name" ] )
except : pass
try : mmmkmkmkm = int ( KmkmkmkKKmmkmkmm [ "mode" ] )
except : pass
try : mKmkmkmKm = urllib . unquote_plus ( KmkmkmkKKmmkmkmm [ "iconimage" ] )
except : pass
if 44 - 44: Kmkm % i11IiIiiIIIII + mKKKmkmmkmkmmkm
if mmmkmkmkm == None or i1 == None or len ( i1 ) < 1 : Kmkmkm ( )
elif mmmkmkmkm == 1 : KmkmmmkmK ( mmkmKmKmkmkm , i1 , mKmkmkmKm )
elif mmmkmkmkm == 2 : ii111111I1iII ( )
elif mmmkmkmkm == 3 : iIIIi1 ( i1 , mmkmKmKmkmkm , mKmkmkmKm )
elif mmmkmkmkm == 4 : iI1Ii11111iIi ( )
elif mmmkmkmkm == 5 : KmmmkKKmk ( mmkmKmKmkmkm , i1 , Kmkmkmmmmmmkmk )
elif mmmkmkmkm == 6 : mKmk ( mmkmKmKmkmkm , i1 , mKmkmkmKm )
elif mmmkmkmkm == 7 : GETFAVS ( i1 )
elif mmmkmkmkm == 8 : ii11iIi1I ( mmkmKmKmkmkm , i1 , mKmkmkmKm )
elif mmmkmkmkm == 9 : KKKmkKKKmkmkmm ( i1 )
if 45 - 45: iI11ii1i1I1 / iI11ii1i1I1 + KmkmkmkmmmkK + mKKmKmmkmkm
if 47 - 47: mKm + mKKmKmmkmkm
xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
if 82 - 82: i11IiIiiIIIII . i11IIiiIii - I1iII1iiII - i11IIiiIii * i11IiIiiIIIII
if 77 - 77: I1iII1iiII * IiI1I1
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3
