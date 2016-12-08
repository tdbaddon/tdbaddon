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
mmKm = 'https://www.googleapis.com/youtube/v3/search?q='
Km = '&regionCode=US&part=snippet&hl=en_US&key=AIzaSyAd-YEOqZz9nXVzGtn3KWzYLbLaajhqIDA&type=video&maxResults=50'
mmkK = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId='
IiiIII111iI = '&maxResults=50&key=AIzaSyAd-YEOqZz9nXVzGtn3KWzYLbLaajhqIDA'
IiII = open ( KmmkK , 'a' )
IiII . close ( )
if 28 - 28: Ii11111i * iiI1i1
def i1I1ii1II1iII ( ) :
 KmkKmkKKmkKmkKmk . setSetting ( 'fav' , 'no' )
 if not os . path . exists ( IiIi11iIIi1Ii ) :
  os . mkdir ( IiIi11iIIi1Ii )
 mmmKmkmmmkmKKKK = KmkmK ( IiI )
 mmkmKmk = re . compile ( '<index>(.+?)</index>' ) . findall ( mmmKmkmmmkmKKKK ) [ 0 ]
 mmmKmkmmmkmKKKK = KmkmK ( mmkmKmk )
 mmmkmk = re . compile ( 'name="(.+?)".+?rl="(.+?)".+?mg="(.+?)"' , re . DOTALL ) . findall ( mmmKmkmmmkmKKKK )
 for mmkmk , KmmkmKmkmmm , mmkmKmKmkmkm in mmmkmk :
  if not 'XXX' in mmkmk :
   i1 ( mmkmk , KmmkmKmkmmm , 1 , mmkmKmKmkmkm , II1 )
  if 'XXX' in mmkmk :
   if I11i11Ii == 'true' :
    if mKmkmkmKm == '' :
     mKKmmmkmkKmkK = xbmcgui . Dialog ( )
     i1111 = mKKmmmkmkKmkK . yesno ( 'Adult Content' , 'You have opted to show adult content' , '' , 'Please set a password to prevent accidental access' , 'Cancel' , 'Lets Go' )
     if i1111 == 1 :
      i11 = xbmc . Keyboard ( '' , 'Set Password' )
      i11 . doModal ( )
      if ( i11 . isConfirmed ( ) ) :
       I11 = i11 . getText ( )
       KmkKmkKKmkKmkKmk . setSetting ( 'password' , I11 )
      i1 ( mmkmk , KmmkmKmkmmm , 1 , mmkmKmKmkmkm , II1 )
   if I11i11Ii == 'true' :
    if mKmkmkmKm <> '' :
     i1 ( mmkmk , KmmkmKmkmmm , 1 , mmkmKmKmkmkm , II1 )
 i1 ( 'Favourites' , KmmkK , 15 , 'http://ukturk.offshorepastebin.com/UKTurk/thumbs/new/Uk%20turk%20thumbnails%20favourites.jpg' , II1 )
 i1 ( 'Search' , 'url' , 5 , 'http://ukturk.offshorepastebin.com/UKTurk/thumbs/new/Uk%20turk%20thumbnails%20search.jpg' , II1 )
 xbmc . executebuiltin ( 'Container.SetViewMode(500)' )
 if 98 - 98: I1111 * mmkmmkKmmkmmmmmk / I1I1i1 * mKmk / IIIi1i1I
def KKmKmmmkmkmm ( url ) :
 KmkKmkKKmkKmkKmk . setSetting ( 'fav' , 'yes' )
 iiI11 = None
 file = open ( KmmkK , 'r' )
 iiI11 = file . read ( )
 mmmkmk = re . compile ( "<item>(.+?)</item>" , re . DOTALL ) . findall ( iiI11 )
 for KKmmK in mmmkmk :
  KKmKmkmkm = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>' , re . DOTALL ) . findall ( KKmmK )
  for mmkmk , url , mmkmKmKmkmkm in KKmKmkmkm :
   if '.txt' in url :
    i1 ( mmkmk , url , 1 , mmkmKmKmkmkm , II1 )
   else :
    II111iiii ( mmkmk , url , 2 , mmkmKmKmkmkm , II1 )
    if 48 - 48: I1Ii . IiIi1Iii1I1 - KmkKmkKmkKmkmkKmmK % Kmmmm % i1iIIIiI1I - KKmKmkmkmkKmkKK
def iiI1IiI ( name , url , iconimage ) :
 url = url . replace ( ' ' , '%20' )
 iconimage = iconimage . replace ( ' ' , '%20' )
 II = '<FAV><item>\n<title>' + name + '</title>\n<link>' + url + '</link>\n' + '<thumbnail>' + iconimage + '</thumbnail>\n</item></FAV>\n'
 IiII = open ( KmmkK , 'a' )
 IiII . write ( II )
 IiII . close ( )
 if 57 - 57: mmKmmmkK
def KmmKmk ( name , url , iconimage ) :
 iiI11 = None
 file = open ( KmmkK , 'r' )
 iiI11 = file . read ( )
 II11iiii1Ii = ''
 mmmkmk = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( iiI11 )
 for KKmKmkmkm in mmmkmk :
  II = '\n<FAV><item>\n' + KKmKmkmkm + '</item>\n'
  if name in KKmKmkmkm :
   II = II . replace ( 'item' , ' ' )
  II11iiii1Ii = II11iiii1Ii + II
 file = open ( KmmkK , 'w' )
 file . truncate ( )
 file . write ( II11iiii1Ii )
 file . close ( )
 xbmc . executebuiltin ( 'Container.Refresh' )
 if 70 - 70: Kmkmk / i1I1i1Ii11 . IIIIII11i1I - mmkmmkKKKmkmmk % mmKKKmmkmmmkKmk
def mmk ( name , url , iconimage , fanart ) :
 I11II1i = IIIII ( name )
 KmkKmkKKmkKmkKmk . setSetting ( 'tv' , I11II1i )
 mmmKmkmmmkmKKKK = KmkmK ( url )
 mmmmmmKmkmm ( mmmKmkmmmkmKKKK )
 if 'Index' in url :
  IIiiiiiiIi1I1 ( url )
 if 'XXX' in name : I1IIIii ( mmmKmkmmmkmKKKK )
 mmmkmk = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( mmmKmkmmmkmKKKK )
 KKKmmk = str ( len ( mmmkmk ) )
 KmkKmkKKmkKmkKmk . setSetting ( 'count' , KKKmmk )
 KmkKmkKKmkKmkKmk . setSetting ( 'fav' , 'no' )
 for KKmmK in mmmkmk :
  try :
   if '<sportsdevil>' in KKmmK : mKmKmmKmmkmmk ( KKmmK , url )
   elif '<iptv>' in KKmmK : KKKK ( KKmmK )
   elif '<Image>' in KKmmK : KKKmkmk ( KKmmK )
   elif '<text>' in KKmmK : iiiiiIIii ( KKmmK )
   elif '<scraper>' in KKmmK : SCRAPER ( KKmmK )
   elif '<redirect>' in KKmmK : REDIRECT ( KKmmK )
   elif '<oktitle>' in KKmmK : KmkmkmkKKmk ( KKmmK )
   else : I11iii1Ii ( KKmmK , url , iconimage )
  except : pass
  if 13 - 13: mmkmmkKKKmkmmk % IiIi1Iii1I1 - i11iIiiIii . mKmk + I1I1i1
def KmkmkmkKKmk ( item ) :
 mmkmk = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 II111ii1II1i = re . compile ( '<oktitle>(.+?)</oktitle>' ) . findall ( item ) [ 0 ]
 KmKmmkmkm = re . compile ( '<line1>(.+?)</line1>' ) . findall ( item ) [ 0 ]
 mmkKKmmmkKKmkKKK = re . compile ( '<line2>(.+?)</line2>' ) . findall ( item ) [ 0 ]
 iI1iI1I1i1I = re . compile ( '<line3>(.+?)</line3>' ) . findall ( item ) [ 0 ]
 iIi11Ii1 = '##' + II111ii1II1i + '#' + KmKmmkmkm + '#' + mmkKKmmmkKKmkKKK + '#' + iI1iI1I1i1I + '##'
 mmkmKmKmkmkm = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 Ii11iII1 ( mmkmk , iIi11Ii1 , 17 , mmkmKmKmkmkm , II1 )
 if 51 - 51: I1I1i1 * I1Ii % KmkKmkKmkKmkmkKmmK * I1I1i1 % Kmmmm / mmKKKmmkmmmkKmk
def iIIIIii1 ( name , url ) :
 mmmkmkmkKKmkmkKm = re . compile ( '##(.+?)##' ) . findall ( url ) [ 0 ] . split ( '#' )
 mKKmmmkmkKmkK = xbmcgui . Dialog ( )
 mKKmmmkmkKmkK . ok ( mmmkmkmkKKmkmkKm [ 0 ] , mmmkmkmkKKmkmkKm [ 1 ] , mmmkmkmkKKmkmkKm [ 2 ] , mmmkmkmkKKmkmkKm [ 3 ] )
 if 51 - 51: IIIIII11i1I * KmkKmkKmkKmkmkKmmK + mmKmmmkK + I1Ii
def iiiiiIIii ( item ) :
 mmkmk = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 iIi11Ii1 = re . compile ( '<text>(.+?)</text>' ) . findall ( item ) [ 0 ]
 mmkmKmKmkmkm = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 Ii11iII1 ( mmkmk , iIi11Ii1 , 9 , mmkmKmKmkmkm , II1 )
 if 66 - 66: IiIi1Iii1I1
def mKmkmkmkKmmkmkmk ( name , url ) :
 i111IiI1I = KmkmK ( url )
 Kmk ( name , i111IiI1I )
 if 30 - 30: KmkKmkKmkKmkmkKmmK . Kmkmk - I1111
def KKKmkmk ( item ) :
 Ii1iIiii1 = re . compile ( '<Image>(.+?)</Image>' ) . findall ( item )
 if len ( Ii1iIiii1 ) == 1 :
  mmkmk = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  mmkmKmKmkmkm = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  KKK = re . compile ( '<Image>(.+?)</Image>' ) . findall ( item ) [ 0 ]
  mmkmKmKmkmkm = KKK . replace ( 'http://imgur.com/' , 'http://i.imgur.com/' ) + '.jpg'
  KKK = KKK . replace ( 'http://imgur.com/' , 'http://i.imgur.com/' ) + '.jpg'
  Ii11iII1 ( mmkmk , KKK , 7 , mmkmKmKmkmkm , II1 )
 elif len ( Ii1iIiii1 ) > 1 :
  mmkmk = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  mmkmKmKmkmkm = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  KmmkmKKm = ''
  for KKK in Ii1iIiii1 :
   mmkmKmKmkmkm = KKK . replace ( 'http://imgur.com/' , 'http://i.imgur.com/' ) + '.jpg'
   KKK = KKK . replace ( 'http://imgur.com/' , 'http://i.imgur.com/' ) + '.jpg'
   KmmkmKKm = KmmkmKKm + '<Image>' + KKK + '</Image>'
  KmmkKmKmkmkmKKmkm = IiIi11iIIi1Ii
  mmkmk = IIIII ( mmkmk )
  KKKmkmkK = os . path . join ( os . path . join ( KmmkKmKmkmkmKKmkm , '' ) , mmkmk + '.txt' )
  if not os . path . exists ( KKKmkmkK ) : file ( KKKmkmkK , 'w' ) . close ( )
  KKmKKmkmmmkmmK = open ( KKKmkmkK , "w" )
  KKmKKmkmmmkmmK . write ( KmmkmKKm )
  KKmKKmkmmmkmmK . close ( )
  Ii11iII1 ( mmkmk , 'image' , 8 , mmkmKmKmkmkm , II1 )
  if 98 - 98: i1I1i1Ii11 * i1I1i1Ii11 / i1I1i1Ii11 + mmKmmmkK
def KKKK ( item ) :
 mmkmk = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 mmkmKmKmkmkm = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 KmmkmKmkmmm = re . compile ( '<iptv>(.+?)</iptv>' ) . findall ( item ) [ 0 ]
 i1 ( mmkmk , KmmkmKmkmmm , 6 , mmkmKmKmkmkm , II1 )
 if 34 - 34: mmKKKmmkmmmkKmk
def I1111I1iII11 ( url , iconimage ) :
 mmmKmkmmmkmKKKK = KmkmK ( url )
 KmmmmkKmkmmmkmkmK = re . compile ( '^#.+?:-?[0-9]*(.*?),(.*?)\n(.*?)$' , re . I + re . M + re . U + re . S ) . findall ( mmmKmkmmmkmKKKK )
 IIi1i = [ ]
 for I1I1iIiII1 , mmkmk , url in KmmmmkKmkmmmkmkmK :
  i11i1I1 = { "params" : I1I1iIiII1 , "name" : mmkmk , "url" : url }
  IIi1i . append ( i11i1I1 )
 list = [ ]
 for ii1I in IIi1i :
  i11i1I1 = { "name" : ii1I [ "name" ] , "url" : ii1I [ "url" ] }
  KmmmmkKmkmmmkmkmK = re . compile ( ' (.+?)="(.+?)"' , re . I + re . M + re . U + re . S ) . findall ( ii1I [ "params" ] )
  for KmmkmmKmmkm , Ii1i1 in KmmmmkKmkmmmkmkmK :
   i11i1I1 [ KmmkmmKmmkm . strip ( ) . lower ( ) . replace ( '-' , '_' ) ] = Ii1i1 . strip ( )
  list . append ( i11i1I1 )
 for ii1I in list :
  if '.ts' in ii1I [ "url" ] : Ii11iII1 ( ii1I [ "name" ] , ii1I [ "url" ] , 2 , iconimage , II1 )
  else : II111iiii ( ii1I [ "name" ] , ii1I [ "url" ] , 2 , iconimage , II1 )
  if 15 - 15: I1I1i1
def I11iii1Ii ( item , url , iconimage ) :
 Ii = iconimage
 mmmmkK = url
 mKmKmkmmkmkKKmk = re . compile ( '<link>(.+?)</link>' ) . findall ( item )
 KKmKmkmkm = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>' , re . DOTALL ) . findall ( item )
 for mmkmk , i1I1ii , iconimage in KKmKmkmkm :
  if 'youtube.com/playlist?' in i1I1ii :
   mKKmmk = i1I1ii . split ( 'list=' ) [ 1 ]
   i1 ( mmkmk , i1I1ii , mmmkmkKmkmkmK , iconimage , II1 , description = mKKmmk )
 if len ( mKmKmkmmkmkKKmk ) == 1 :
  mmkmk = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  url = re . compile ( '<link>(.+?)</link>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  if iconimage == 'ImageHere' : iconimage = Ii
  if '.ts' in url : Ii11iII1 ( mmkmk , url , 16 , iconimage , II1 , description = '' )
  elif 'movies' in mmmmkK :
   iIiIIIi ( mmkmk , url , 2 , iconimage , int ( KKKmmk ) , isFolder = False )
  else : II111iiii ( mmkmk , url , 2 , iconimage , II1 )
 elif len ( mKmKmkmmkmkKKmk ) > 1 :
  mmkmk = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  if iconimage == 'ImageHere' : iconimage = Ii
  print iconimage
  if '.ts' in url : Ii11iII1 ( mmkmk , url , 16 , iconimage , II1 , description = '' )
  elif 'movies' in mmmmkK :
   iIiIIIi ( mmkmk , url , 3 , iconimage , int ( KKKmmk ) , isFolder = False )
  else : II111iiii ( mmkmk , url , 3 , iconimage , II1 )
  if 93 - 93: i1I1i1Ii11
def IIiiiiiiIi1I1 ( url ) :
 mmmKmkmmmkmKKKK = KmkmK ( url )
 mmmkmk = re . compile ( 'name="(.+?)".+?rl="(.+?)".+?mg="(.+?)"' , re . DOTALL ) . findall ( mmmKmkmmmkmKKKK )
 for mmkmk , url , I1IiiI in mmmkmk :
  if 'youtube.com/playlist?list=' in url :
   i1 ( mmkmk , url , 18 , I1IiiI , II1 )
  elif 'youtube.com/results?search_query=' in url :
   i1 ( mmkmk , url , 18 , I1IiiI , II1 )
  else :
   i1 ( mmkmk , url , 1 , I1IiiI , II1 )
   if 10 - 10: mmKmmmkK
def KKmmKKmkmkmk ( name , url , iconimage ) :
 if 'youtube.com/results?search_query=' in url :
  mKKmmk = url . split ( 'search_query=' ) [ 1 ]
  KKmKmm = mmKm + mKKmmk + Km
  mKmkmkmkmkKKmmkmk = urllib2 . Request ( KKmKmm )
  mKmkmkmkmkKKmmkmk . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' )
  iiIi1IIiIi = urllib2 . urlopen ( mKmkmkmkmkKKmmkmk )
  mmmKmkmmmkmKKKK = iiIi1IIiIi . read ( )
  iiIi1IIiIi . close ( )
  mmmKmkmmmkmKKKK = mmmKmkmmmkmKKKK . replace ( '\r' , '' ) . replace ( '\n' , '' ) . replace ( '  ' , '' )
  mmmkmk = re . compile ( '"videoId": "(.+?)".+?"title": "(.+?)"' , re . DOTALL ) . findall ( mmmKmkmmmkmKKKK )
  for mKKmkmkKm , name in mmmkmk :
   url = 'https://www.youtube.com/watch?v=' + mKKmkmkKm
   iconimage = 'https://i.ytimg.com/vi/%s/hqdefault.jpg' % mKKmkmkKm
   II111iiii ( name , url , 2 , iconimage , II1 )
 elif 'youtube.com/playlist?list=' in url :
  mKKmmk = url . split ( 'playlist?list=' ) [ 1 ]
  KKmKmm = mmkK + mKKmmk + IiiIII111iI
  mKmkmkmkmkKKmmkmk = urllib2 . Request ( KKmKmm )
  mKmkmkmkmkKKmmkmk . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' )
  iiIi1IIiIi = urllib2 . urlopen ( mKmkmkmkmkKKmmkmk )
  mmmKmkmmmkmKKKK = iiIi1IIiIi . read ( )
  iiIi1IIiIi . close ( )
  mmmKmkmmmkmKKKK = mmmKmkmmmkmKKKK . replace ( '\r' , '' ) . replace ( '\n' , '' ) . replace ( '  ' , '' )
  mmmkmk = re . compile ( '"title": "(.+?)".+?"videoId": "(.+?)"' , re . DOTALL ) . findall ( mmmKmkmmmkmKKKK )
  for name , mKKmkmkKm in mmmkmk :
   url = 'https://www.youtube.com/watch?v=' + mKKmkmkKm
   iconimage = 'https://i.ytimg.com/vi/%s/hqdefault.jpg' % mKKmkmkKm
   II111iiii ( name , url , 2 , iconimage , II1 )
   if 6 - 6: i1iIIIiI1I
def mKKmmkmKmmk ( item ) :
 item = item . replace ( '\r' , '' ) . replace ( '\t' , '' ) . replace ( '&nbsp;' , '' ) . replace ( '\'' , '' ) . replace ( '\n' , '' )
 KKmKmkmkm = re . compile ( 'name="(.+?)".+?rl="(.+?)".+?mg="(.+?)"' , re . DOTALL ) . findall ( item )
 for mmkmk , KmmkmKmkmmm , mmkmKmKmkmkm in KKmKmkmkm :
  if 'youtube.com/channel/' in KmmkmKmkmmm :
   mKKmmk = KmmkmKmkmmm . split ( 'channel/' ) [ 1 ]
   i1 ( mmkmk , KmmkmKmkmmm , mmmkmkKmkmkmK , mmkmKmKmkmkm , II1 , description = mKKmmk )
  elif 'youtube.com/user/' in KmmkmKmkmmm :
   mKKmmk = KmmkmKmkmmm . split ( 'user/' ) [ 1 ]
   i1 ( mmkmk , KmmkmKmkmmm , mmmkmkKmkmkmK , mmkmKmKmkmkm , II1 , description = mKKmmk )
  elif 'youtube.com/playlist?' in KmmkmKmkmmm :
   mKKmmk = KmmkmKmkmmm . split ( 'list=' ) [ 1 ]
   i1 ( mmkmk , KmmkmKmkmmm , mmmkmkKmkmkmK , mmkmKmKmkmkm , II1 , description = mKKmmk )
  elif 'plugin://' in KmmkmKmkmmm :
   IImmmmm = HTMLParser ( )
   KmmkmKmkmmm = IImmmmm . unescape ( KmmkmKmkmmm )
   i1 ( mmkmk , KmmkmKmkmmm , mmmkmkKmkmkmK , mmkmKmKmkmkm , II1 )
  else :
   i1 ( mmkmk , KmmkmKmkmmm , 1 , mmkmKmKmkmkm , II1 )
   if 1 - 1: IIIi1i1I / KmkKmkKmkKmkmkKmmK % i1I1i1Ii11 * IIIIII11i1I . i11iIiiIii
def mKmKmmKmmkmmk ( item , url ) :
 mKmKmkmmkmkKKmk = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( item )
 III1Iiii1I11 = re . compile ( '<link>(.+?)</link>' ) . findall ( item )
 if len ( mKmKmkmmkmkKKmk ) + len ( III1Iiii1I11 ) == 1 :
  mmkmk = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  mmkmKmKmkmkm = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  url = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( item ) [ 0 ]
  mmmKmkmmmkmKKKK = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' + url
  Ii11iII1 ( mmkmk , url , 16 , mmkmKmKmkmkm , II1 )
 elif len ( mKmKmkmmkmkKKmk ) + len ( III1Iiii1I11 ) > 1 :
  mmkmk = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  mmkmKmKmkmkm = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  Ii11iII1 ( mmkmk , url , 3 , mmkmKmKmkmkm , II1 )
  if 9 - 9: Kmmmm / IIIi1i1I - mKmk / I1111 / iiI1i1 - KmkKmkKmkKmkmkKmmK
def I1IIIii ( link ) :
 if mKmkmkmKm == '' :
  mKKmmmkmkKmkK = xbmcgui . Dialog ( )
  i1111 = mKKmmmkmkKmkK . yesno ( 'Adult Content' , 'You have opted to show adult content' , '' , 'Please set a password to prevent accidental access' , 'Cancel' , 'OK' )
  if i1111 == 1 :
   i11 = xbmc . Keyboard ( '' , 'Set Password' )
   i11 . doModal ( )
   if ( i11 . isConfirmed ( ) ) :
    I11 = i11 . getText ( )
    KmkKmkKKmkKmkKmk . setSetting ( 'password' , I11 )
  else : quit ( )
 elif mKmkmkmKm <> '' :
  mKKmmmkmkKmkK = xbmcgui . Dialog ( )
  i1111 = mKKmmmkmkKmkK . yesno ( 'Adult Content' , 'Please enter the password you set' , 'to continue' , '' , 'Cancel' , 'OK' )
  if i1111 == 1 :
   i11 = xbmc . Keyboard ( '' , 'Enter Password' )
   i11 . doModal ( )
   if ( i11 . isConfirmed ( ) ) :
    I11 = i11 . getText ( )
   if I11 <> mKmkmkmKm :
    quit ( )
  else : quit ( )
  if 91 - 91: i1I1i1Ii11 % mmkmmkKmmkmmmmmk % iiI1i1
def IIi1I11I1II ( ) :
 i11 = xbmc . Keyboard ( '' , 'Search' )
 i11 . doModal ( )
 if ( i11 . isConfirmed ( ) ) :
  mKKmmk = i11 . getText ( )
  mKKmmk = mKKmmk . upper ( )
 else : quit ( )
 mmmKmkmmmkmKKKK = KmkmK ( IiI )
 KmmKmmmKm = re . compile ( '<link>(.+?)</link>' ) . findall ( mmmKmkmmmkmKKKK )
 for KmmkmKmkmmm in KmmKmmmKm :
  try :
   mmmKmkmmmkmKKKK = KmkmK ( KmmkmKmkmmm )
   ii11IIII11I = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( mmmKmkmmmkmKKKK )
   for KKmmK in ii11IIII11I :
    mmmkmk = re . compile ( '<title>(.+?)</title>' ) . findall ( KKmmK )
    for KKmmm in mmmkmk :
     KKmmm = KKmmm . upper ( )
     if mKKmmk in KKmmm :
      try :
       if 'Index' in KmmkmKmkmmm : IIiiiiiiIi1I1 ( KmmkmKmkmmm )
       elif '<sportsdevil>' in KKmmK : mKmKmmKmmkmmk ( KKmmK , KmmkmKmkmmm )
       elif '<iptv>' in KKmmK : KKKK ( KKmmK )
       elif '<Image>' in KKmmK : KKKmkmk ( KKmmK )
       elif '<text>' in KKmmK : iiiiiIIii ( KKmmK )
       elif '<scraper>' in KKmmK : SCRAPER ( KKmmK )
       elif '<redirect>' in KKmmK : REDIRECT ( KKmmK )
       elif '<oktitle>' in KKmmK : KmkmkmkKKmk ( KKmmK )
       else : I11iii1Ii ( KKmmK , KmmkmKmkmmm , mmkmKmKmkmkm )
      except : pass
  except : pass
  if 90 - 90: KmkKmkKmkKmkmkKmmK % mmkmmkKmmkmmmmmk / I1Ii
def IIi ( name , url , iconimage ) :
 Ii = iconimage
 i1Iii1i1I = [ ]
 KKmKmkmk = [ ]
 IiI111111IIII = [ ]
 mmmKmkmmmkmKKKK = KmkmK ( url )
 i1Ii = re . compile ( '<title>' + re . escape ( name ) + '</title>(.+?)</item>' , re . DOTALL ) . findall ( mmmKmkmmmkmKKKK ) [ 0 ]
 mKmKmkmmkmkKKmk = [ ]
 if '<link>' in i1Ii :
  ii111iI1iIi1 = re . compile ( '<link>(.+?)</link>' ) . findall ( i1Ii )
  for KKKmmmkKKmmk in ii111iI1iIi1 :
   mKmKmkmmkmkKKmk . append ( KKKmmmkKKmmk )
 if '<sportsdevil>' in i1Ii :
  I11IiI = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( i1Ii )
  for KmkmmKmkKmmkmkm in I11IiI :
   KmkmmKmkKmmkmkm = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' + KmkmmKmkKmmkmkm
   mKmKmkmmkmkKKmk . append ( KmkmmKmkKmmkmkm )
 mmKmkmKKmmKmmk = 1
 for i1I1ii11i1Iii in mKmKmkmmkmkKKmk :
  I1IiiiiI = i1I1ii11i1Iii
  if '(' in i1I1ii11i1Iii :
   i1I1ii11i1Iii = i1I1ii11i1Iii . split ( '(' ) [ 0 ]
   mmkKIiII = str ( I1IiiiiI . split ( '(' ) [ 1 ] . replace ( ')' , '' ) )
   i1Iii1i1I . append ( i1I1ii11i1Iii )
   KKmKmkmk . append ( mmkKIiII )
  else :
   ii1iII1II = i1I1ii11i1Iii . split ( '/' ) [ 2 ] . replace ( 'www.' , '' )
   i1Iii1i1I . append ( i1I1ii11i1Iii )
   KKmKmkmk . append ( 'Link ' + str ( mmKmkmKKmmKmmk ) )
  mmKmkmKKmmKmmk = mmKmkmKKmmKmmk + 1
 mKKmmmkmkKmkK = xbmcgui . Dialog ( )
 Iii1I1I11iiI1 = mKKmmmkmkKmkK . select ( 'Choose a link..' , KKmKmkmk )
 if Iii1I1I11iiI1 < 0 : quit ( )
 else :
  url = i1Iii1i1I [ Iii1I1I11iiI1 ]
  I1I1i1I ( name , url , iconimage )
  if 30 - 30: I1111
def I1Ii1iI1 ( url ) :
 II = "ShowPicture(%s)" % url
 xbmc . executebuiltin ( II )
 if 87 - 87: IIIi1i1I . IIIIII11i1I
def I1I1i1I ( name , url , iconimage ) :
 try :
  if 'plugin://plugin.video.SportsDevil/' in url :
   KmkKKmkK ( name , url , iconimage )
  elif '.ts' in url :
   url = 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;name=' + name + '&amp;url=' + url
   KmkKKmkK ( name , url , iconimage )
  elif urlresolver . HostedMediaFile ( url ) . valid_url ( ) :
   url = urlresolver . HostedMediaFile ( url ) . resolve ( )
   KK ( name , url , iconimage )
  elif liveresolver . isValid ( url ) == True :
   url = liveresolver . resolve ( url )
   KK ( name , url , iconimage )
  else : KK ( name , url , iconimage )
 except :
  KmKmK ( 'UKTurk' , 'Stream Unavailable' , '3000' , I1IiiI )
  if 43 - 43: i11iIiiIii + IIIi1i1I * I1I1i1 * mmkmmkKKKmkmmk * Ii11111i
def mmkmkmKmkmmmkKK ( url ) :
 if urlresolver . HostedMediaFile ( url ) . valid_url ( ) :
  url = urlresolver . HostedMediaFile ( url ) . resolve ( )
 xbmc . Player ( ) . play ( url )
 if 57 - 57: mmkmmkKKKmkmmk % Kmkmk + KmkKmkKmkKmkmkKmmK - IIIi1i1I
def KK ( name , url , iconimage ) :
 mmkKIiI1i = True
 mmkKmmkmk = xbmcgui . ListItem ( name , iconImage = iconimage , thumbnailImage = iconimage ) ; mmkKmmkmk . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
 mmkKIiI1i = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = url , listitem = mmkKmmkmk )
 mmkKmmkmk . setPath ( url )
 xbmcplugin . setResolvedUrl ( int ( sys . argv [ 1 ] ) , True , mmkKmmkmk )
 if 32 - 32: KmkKmkKmkKmkmkKmmK . IIIIII11i1I * mmKmmmkK
def KmkKKmkK ( name , url , iconimage ) :
 mmkKIiI1i = True
 mmkKmmkmk = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage ) ; mmkKmmkmk . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
 mmkKIiI1i = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = url , listitem = mmkKmmkmk )
 mKKmmmkmkKmkK = xbmcgui . Dialog ( )
 xbmc . Player ( ) . play ( url , mmkKmmkmk , False )
 if 93 - 93: KmkKmkKmkKmkmkKmmK % mmkmmkKmmkmmmmmk . Kmkmk . i11iIiiIii
def mKKmmmkmkKmkmkm ( url ) :
 xbmc . executebuiltin ( "PlayMedia(%s)" % url )
 if 98 - 98: KKmKmkmkmkKmkKK + IIIIII11i1I + i1iIIIiI1I % I1111
def mmmmmmmkKmkmkmkm ( url ) :
 KmK = KmkKmkKKmkKmkKmk . getSetting ( 'layout' )
 if KmK == 'Listers' : KmkKmkKKmkKmkKmk . setSetting ( 'layout' , 'Category' )
 else : KmkKmkKKmkKmkKmk . setSetting ( 'layout' , 'Listers' )
 xbmc . executebuiltin ( 'Container.Refresh' )
 if 51 - 51: I1111 * KKmKmkmkmkKmkKK
def KmkmK ( url ) :
 mKmkmkmkmkKKmmkmk = urllib2 . Request ( url )
 mKmkmkmkmkKKmmkmk . add_header ( 'User-Agent' , 'mat' )
 iiIi1IIiIi = urllib2 . urlopen ( mKmkmkmkmkKKmmkmk )
 mmmKmkmmmkmKKKK = iiIi1IIiIi . read ( )
 iiIi1IIiIi . close ( )
 mmmKmkmmmkmKKKK = mmmKmkmmmkmKKKK . replace ( '</fanart>' , '<fanart>x</fanart>' ) . replace ( '<thumbnail></thumbnail>' , '<thumbnail>x</thumbnail>' ) . replace ( '<utube>' , '<link>https://www.youtube.com/watch?v=' ) . replace ( '</utube>' , '</link>' )
 if '{' in mmmKmkmmmkmKKKK : mmmKmkmmmkmKKKK = KKmkmmKKKmkKKK ( mmmKmkmmmkmKKKK )
 return mmmKmkmmmkmKKKK
 if 63 - 63: IiIi1Iii1I1 * i1I1i1Ii11
def mm ( ) :
 iIi1 = [ ]
 KmKKmKmmmmKKm = sys . argv [ 2 ]
 if len ( KmKKmKmmmmKKm ) >= 2 :
  I1I1iIiII1 = sys . argv [ 2 ]
  mKmmkK = I1I1iIiII1 . replace ( '?' , '' )
  if ( I1I1iIiII1 [ len ( I1I1iIiII1 ) - 1 ] == '/' ) :
   I1I1iIiII1 = I1I1iIiII1 [ 0 : len ( I1I1iIiII1 ) - 2 ]
  mmmkKmk = mKmmkK . split ( '&' )
  iIi1 = { }
  for mmKmkmKKmmKmmk in range ( len ( mmmkKmk ) ) :
   iI = { }
   iI = mmmkKmk [ mmKmkmKKmmKmmk ] . split ( '=' )
   if ( len ( iI ) ) == 2 :
    iIi1 [ iI [ 0 ] ] = iI [ 1 ]
 return iIi1
 if 89 - 89: KmkKmkKmkKmkmkKmmK + I1Ii * mmKmmmkK * Kmkmk
def KmKmK ( title , message , ms , nart ) :
 xbmc . executebuiltin ( "XBMC.notification(" + title + "," + message + "," + ms + "," + nart + ")" )
 if 37 - 37: I1111 - Ii11111i - KmkKmkKmkKmkmkKmmK
def IIIII ( string ) :
 mmkmmkKmkKmkmkmKKm = re . compile ( '\[(.+?)\]' ) . findall ( string )
 for iIIIiIi in mmkmmkKmkKmkmkmKKm : string = string . replace ( iIIIiIi , '' ) . replace ( '[/]' , '' ) . replace ( '[]' , '' )
 return string
 if 100 - 100: mKmk / KmkKmkKmkKmkmkKmmK % I1I1i1 % IIIi1i1I % KKmKmkmkmkKmkKK
def KmkmkmKmkmkmkKmkK ( string ) :
 string = string . split ( ' ' )
 I1i1i1iii = ''
 for I1111i in string :
  iIIii = '[B][COLOR red]' + I1111i [ 0 ] . upper ( ) + '[/COLOR][COLOR white]' + I1111i [ 1 : ] + '[/COLOR][/B] '
  I1i1i1iii = I1i1i1iii + iIIii
 return I1i1i1iii
 if 92 - 92: Kmkmk + i1iIIIiI1I % KKmKmkmkmkKmkKK
def iIiIIIi ( name , url , mode , iconimage , itemcount , isFolder = False ) :
 if Kmmmmkmkmkm == 'true' :
  if not 'COLOR' in name :
   mKmmk = name . partition ( '(' )
   i1iI = ""
   KmmkKmk = ""
   if len ( mKmmk ) > 0 :
    i1iI = mKmmk [ 0 ]
    KmmkKmk = mKmmk [ 2 ] . partition ( ')' )
   if len ( KmmkKmk ) > 0 :
    KmmkKmk = KmmkKmk [ 0 ]
   KmmmkKKmKmKmk = eval ( base64 . b64decode ( 'bWV0YWhhbmRsZXJzLk1ldGFEYXRhKHRtZGJfYXBpX2tleT0iZDk1NWQ4ZjAyYTNmMjQ4MGE1MTg4MWZlNGM5NmYxMGUiKQ==' ) )
   mKmmkKKmKmk = KmmmkKKmKmKmk . get_meta ( 'movie' , name = i1iI , year = KmmkKmk )
   IImmkKmmkmKmkmKKmkmk = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&site=" + str ( mmmkmkKKmkmkmkmkmK ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name )
   mmkKIiI1i = True
   mmkKmmkmk = xbmcgui . ListItem ( name , iconImage = mKmmkKKmKmk [ 'cover_url' ] , thumbnailImage = mKmmkKKmKmk [ 'cover_url' ] )
   mmkKmmkmk . setInfo ( type = "Video" , infoLabels = mKmmkKKmKmk )
   mmkKmmkmk . setProperty ( "IsPlayable" , "true" )
   I1II1 = [ ]
   if KmkKmkKKmkKmkKmk . getSetting ( 'fav' ) == 'yes' : I1II1 . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
   if KmkKmkKKmkKmkKmk . getSetting ( 'fav' ) == 'no' : I1II1 . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
   mmkKmmkmk . addContextMenuItems ( I1II1 , replaceItems = False )
   if not mKmmkKKmKmk [ 'backdrop_url' ] == '' : mmkKmmkmk . setProperty ( 'fanart_image' , mKmmkKKmKmk [ 'backdrop_url' ] )
   else : mmkKmmkmk . setProperty ( 'fanart_image' , II1 )
   mmkKIiI1i = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = IImmkKmmkmKmkmKKmkmk , listitem = mmkKmmkmk , isFolder = isFolder , totalItems = itemcount )
   return mmkKIiI1i
 else :
  IImmkKmmkmKmkmKKmkmk = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&site=" + str ( mmmkmkKKmkmkmkmkmK ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name )
  mmkKIiI1i = True
  mmkKmmkmk = xbmcgui . ListItem ( name , iconImage = iconimage , thumbnailImage = iconimage )
  mmkKmmkmk . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
  mmkKmmkmk . setProperty ( 'fanart_image' , II1 )
  mmkKmmkmk . setProperty ( "IsPlayable" , "true" )
  I1II1 = [ ]
  if KmkKmkKKmkKmkKmk . getSetting ( 'fav' ) == 'yes' : I1II1 . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
  if KmkKmkKKmkKmkKmk . getSetting ( 'fav' ) == 'no' : I1II1 . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
  mmkKmmkmk . addContextMenuItems ( I1II1 , replaceItems = False )
  mmkKIiI1i = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = IImmkKmmkmKmkmKKmkmk , listitem = mmkKmmkmk , isFolder = isFolder )
  return mmkKIiI1i
  if 86 - 86: iiI1i1 / IiIi1Iii1I1 . I1I1i1
def i1 ( name , url , mode , iconimage , fanart , description = '' ) :
 IImmkKmmkmKmkmKKmkmk = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&fanart=" + urllib . quote_plus ( fanart ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 mmkKIiI1i = True
 mmkKmmkmk = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 mmkKmmkmk . setInfo ( type = "Video" , infoLabels = { "Title" : name , 'plot' : description } )
 mmkKmmkmk . setProperty ( 'fanart_image' , fanart )
 I1II1 = [ ]
 if KmkKmkKKmkKmkKmk . getSetting ( 'fav' ) == 'yes' : I1II1 . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 if KmkKmkKKmkKmkKmk . getSetting ( 'fav' ) == 'no' : I1II1 . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 mmkKmmkmk . addContextMenuItems ( I1II1 , replaceItems = False )
 if 'youtube.com/channel/' in url :
  IImmkKmmkmKmkmKKmkmk = 'plugin://plugin.video.youtube/channel/' + description + '/'
 if 'youtube.com/user/' in url :
  IImmkKmmkmKmkmKKmkmk = 'plugin://plugin.video.youtube/user/' + description + '/'
 if 'youtube.com/playlist?' in url :
  IImmkKmmkmKmkmKKmkmk = 'plugin://plugin.video.youtube/playlist/' + description + '/'
 if 'plugin://' in url :
  IImmkKmmkmKmkmKKmkmk = url
 mmkKIiI1i = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = IImmkKmmkmKmkmKKmkmk , listitem = mmkKmmkmk , isFolder = True )
 return mmkKIiI1i
 if 19 - 19: Kmmmm % I1111 % IIIIII11i1I * KmkKmkKmkKmkmkKmmK % Ii11111i
def Ii11iII1 ( name , url , mode , iconimage , fanart , description = '' ) :
 IImmkKmmkmKmkmKKmkmk = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 mmkKIiI1i = True
 mmkKmmkmk = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 mmkKmmkmk . setProperty ( 'fanart_image' , fanart )
 I1II1 = [ ]
 if KmkKmkKKmkKmkKmk . getSetting ( 'fav' ) == 'yes' : I1II1 . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 if KmkKmkKKmkKmkKmk . getSetting ( 'fav' ) == 'no' : I1II1 . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 mmkKmmkmk . addContextMenuItems ( I1II1 , replaceItems = False )
 mmkKIiI1i = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = IImmkKmmkmKmkmKKmkmk , listitem = mmkKmmkmk , isFolder = False )
 return mmkKIiI1i
 if 67 - 67: mKmk . mmkmmkKmmkmmmmmk
def II111iiii ( name , url , mode , iconimage , fanart , description = '' ) :
 IImmkKmmkmKmkmKKmkmk = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 mmkKIiI1i = True
 mmkKmmkmk = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 mmkKmmkmk . setProperty ( 'fanart_image' , fanart )
 mmkKmmkmk . setProperty ( "IsPlayable" , "true" )
 I1II1 = [ ]
 if KmkKmkKKmkKmkKmk . getSetting ( 'fav' ) == 'yes' : I1II1 . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 if KmkKmkKKmkKmkKmk . getSetting ( 'fav' ) == 'no' : I1II1 . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 mmkKmmkmk . addContextMenuItems ( I1II1 , replaceItems = False )
 mmkKIiI1i = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = IImmkKmmkmKmkmKKmkmk , listitem = mmkKmmkmk , isFolder = False )
 return mmkKIiI1i
 if 27 - 27: mmKKKmmkmmmkKmk % mKmk
def mmkmmmKKmkmk ( url , name ) :
 iiIiii1IIIII = KmkmK ( url )
 if len ( iiIiii1IIIII ) > 1 :
  KmmkKmKmkmkmKKmkm = IiIi11iIIi1Ii
  KKKmkmkK = os . path . join ( os . path . join ( KmmkKmKmkmkmKKmkm , '' ) , name + '.txt' )
  if not os . path . exists ( KKKmkmkK ) :
   file ( KKKmkmkK , 'w' ) . close ( )
  mmkmkm = open ( KKKmkmkK )
  IIIIiiIiiI = mmkmkm . read ( )
  if IIIIiiIiiI == iiIiii1IIIII : pass
  else :
   Kmk ( 'UKTurk' , iiIiii1IIIII )
   KKmKKmkmmmkmmK = open ( KKKmkmkK , "w" )
   KKmKKmkmmmkmmK . write ( iiIiii1IIIII )
   KKmKKmkmmmkmmK . close ( )
   if 10 - 10: IiIi1Iii1I1 % IiIi1Iii1I1 - IiIi1Iii1I1 . i1I1i1Ii11
def Kmk ( heading , text ) :
 id = 10147
 xbmc . executebuiltin ( 'ActivateWindow(%d)' % id )
 xbmc . sleep ( 500 )
 mmkKmKmmkmkmmkm = xbmcgui . Window ( id )
 I1II1I11I1I = 50
 while ( I1II1I11I1I > 0 ) :
  try :
   xbmc . sleep ( 10 )
   I1II1I11I1I -= 1
   mmkKmKmmkmkmmkm . getControl ( 1 ) . setLabel ( heading )
   mmkKmKmmkmkmmkm . getControl ( 5 ) . setText ( text )
   return
  except :
   pass
   if 54 - 54: I1111 + KmkKmkKmkKmkmkKmmK - mmkmmkKmmkmmmmmk % i11iIiiIii
def iII1iIi11i ( name ) :
 global Icon
 global Next
 global Previous
 global window
 global Quit
 global images
 KKKmkmkK = os . path . join ( os . path . join ( IiIi11iIIi1Ii , '' ) , name + '.txt' )
 mmkmkm = open ( KKKmkmkK )
 IIIIiiIiiI = mmkmkm . read ( )
 images = re . compile ( '<image>(.+?)</image>' ) . findall ( IIIIiiIiiI )
 KmkKmkKKmkKmkKmk . setSetting ( 'pos' , '0' )
 window = pyxbmct . AddonDialogWindow ( '' )
 mmkmmmmKmkmmkK = '/resources/art'
 iiIi11iI1iii = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + KKmkm + mmkmmmmKmkmmkK , 'next_focus.png' ) )
 mmmkmkmk = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + KKmkm + mmkmmmmKmkmmkK , 'next1.png' ) )
 mmkmkmkmkmK = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + KKmkm + mmkmmmmKmkmmkK , 'previous_focus.png' ) )
 iI1i111I1Ii = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + KKmkm + mmkmmmmKmkmmkK , 'previous.png' ) )
 i11i1ii1I = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + KKmkm + mmkmmmmKmkmmkK , 'close_focus.png' ) )
 mmkKKmkmmkmmkmkm = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + KKmkm + mmkmmmmKmkmmkK , 'close.png' ) )
 mKmmkKKKmKK = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + KKmkm + mmkmmmmKmkmmkK , 'main-bg1.png' ) )
 window . setGeometry ( 1300 , 720 , 100 , 50 )
 I11IIIi = pyxbmct . Image ( mKmmkKKKmKK )
 window . placeControl ( I11IIIi , - 10 , - 10 , 130 , 70 )
 iIi11Ii1 = '0xFF000000'
 Previous = pyxbmct . Button ( '' , focusTexture = mmkmkmkmkmK , noFocusTexture = iI1i111I1Ii , textColor = iIi11Ii1 , focusedColor = iIi11Ii1 )
 Next = pyxbmct . Button ( '' , focusTexture = iiIi11iI1iii , noFocusTexture = mmmkmkmk , textColor = iIi11Ii1 , focusedColor = iIi11Ii1 )
 Quit = pyxbmct . Button ( '' , focusTexture = i11i1ii1I , noFocusTexture = mmkKKmkmmkmmkmkm , textColor = iIi11Ii1 , focusedColor = iIi11Ii1 )
 Icon = pyxbmct . Image ( images [ 0 ] , aspectRatio = 1 )
 window . placeControl ( Previous , 102 , 1 , 10 , 10 )
 window . placeControl ( Next , 102 , 40 , 10 , 10 )
 window . placeControl ( Quit , 102 , 21 , 10 , 10 )
 window . placeControl ( Icon , 0 , 0 , 100 , 50 )
 Previous . controlRight ( Next )
 Previous . controlUp ( Quit )
 window . connect ( Previous , iIIiiI1II1i11 )
 window . connect ( Next , mmkmmk )
 Previous . setVisible ( False )
 window . setFocus ( Quit )
 Previous . controlRight ( Quit )
 Quit . controlLeft ( Previous )
 Quit . controlRight ( Next )
 Next . controlLeft ( Quit )
 window . connect ( Quit , window . close )
 window . doModal ( )
 del window
 if 49 - 49: i1iIIIiI1I - i11iIiiIii . mmkmmkKKKmkmmk * Kmkmk % i1I1i1Ii11 + mmkmmkKmmkmmmmmk
def mmkmmk ( ) :
 mKKmkKKKm = int ( KmkKmkKKmkKmkKmk . getSetting ( 'pos' ) )
 mmmkmmkmkmkmk = int ( mKKmkKKKm ) + 1
 KmkKmkKKmkKmkKmk . setSetting ( 'pos' , str ( mmmkmmkmkmkmk ) )
 iiI = len ( images )
 Icon . setImage ( images [ int ( mmmkmmkmkmkmk ) ] )
 Previous . setVisible ( True )
 if int ( mmmkmmkmkmkmk ) == int ( iiI ) - 1 :
  Next . setVisible ( False )
  if 82 - 82: IIIi1i1I + I1Ii
def iIIiiI1II1i11 ( ) :
 mKKmkKKKm = int ( KmkKmkKKmkKmkKmk . getSetting ( 'pos' ) )
 KmkmkK = int ( mKKmkKKKm ) - 1
 KmkKmkKKmkKmkKmk . setSetting ( 'pos' , str ( KmkmkK ) )
 Icon . setImage ( images [ int ( KmkmkK ) ] )
 Next . setVisible ( True )
 if int ( KmkmkK ) == 0 :
  Previous . setVisible ( False )
  if 86 - 86: IIIi1i1I . Ii11111i - I1111 . I1Ii + Kmkmk
def KKmkmmKKKmkKKK ( gobble ) :
 gobble = gobble . replace ( '}' , '' ) . replace ( '{' , '' ) . replace ( ',' , '' ) . replace ( ']' , '' ) . replace ( '[' , '' )
 gobble = gobble + '=='
 gobble = gobble . decode ( 'base64' )
 return gobble
 if 57 - 57: KmkKmkKmkKmkmkKmmK . mmkmmkKmmkmmmmmk . IIIIII11i1I * i11iIiiIii + mmkmmkKKKmkmmk . IIIIII11i1I
def mmmmmmKmkmm ( link ) :
 try :
  mmmkKmkmkKmmmmkKmk = re . compile ( '<layouttype>(.+?)</layouttype>' ) . findall ( link ) [ 0 ]
  if mmmkKmkmkKmmmmkKmk == 'thumbnail' : xbmc . executebuiltin ( 'Container.SetViewMode(500)' )
  else : xbmc . executebuiltin ( 'Container.SetViewMode(50)' )
 except : pass
 if 34 - 34: mmKKKmmkmmmkKmk . KmkKmkKmkKmkmkKmmK % Ii11111i * i1I1i1Ii11 + mKmk
I1I1iIiII1 = mm ( ) ; KmmkmKmkmmm = None ; mmkmk = None ; mmmkmkKmkmkmK = None ; mmmkmkKKmkmkmkmkmK = None ; mmkmKmKmkmkm = None
try : mmmkmkKKmkmkmkmkmK = urllib . unquote_plus ( I1I1iIiII1 [ "site" ] )
except : pass
try : KmmkmKmkmmm = urllib . unquote_plus ( I1I1iIiII1 [ "url" ] )
except : pass
try : mmkmk = urllib . unquote_plus ( I1I1iIiII1 [ "name" ] )
except : pass
try : mmmkmkKmkmkmK = int ( I1I1iIiII1 [ "mode" ] )
except : pass
try : mmkmKmKmkmkm = urllib . unquote_plus ( I1I1iIiII1 [ "iconimage" ] )
except : pass
try : II1 = urllib . unquote_plus ( I1I1iIiII1 [ "fanart" ] )
except : pass
if 77 - 77: Kmkmk + I1I1i1 . IiIi1Iii1I1 * mmkmmkKKKmkmmk + KKmKmkmkmkKmkKK + KKmKmkmkmkKmkKK
try : I1ii1I1iiii = urllib . unquote_plus ( [ "description" ] )
except : pass
if 36 - 36: I1111 . I1Ii
if mmmkmkKmkmkmK == None or KmmkmKmkmmm == None or len ( KmmkmKmkmmm ) < 1 : i1I1ii1II1iII ( )
elif mmmkmkKmkmkmK == 1 : mmk ( mmkmk , KmmkmKmkmmm , mmkmKmKmkmkm , II1 )
elif mmmkmkKmkmkmK == 2 : I1I1i1I ( mmkmk , KmmkmKmkmmm , mmkmKmKmkmkm )
elif mmmkmkKmkmkmK == 3 : IIi ( mmkmk , KmmkmKmkmmm , mmkmKmKmkmkm )
elif mmmkmkKmkmkmK == 4 : KK ( mmkmk , KmmkmKmkmmm , mmkmKmKmkmkm )
elif mmmkmkKmkmkmK == 5 : IIi1I11I1II ( )
elif mmmkmkKmkmkmK == 6 : I1111I1iII11 ( KmmkmKmkmmm , mmkmKmKmkmkm )
elif mmmkmkKmkmkmK == 7 : I1Ii1iI1 ( KmmkmKmkmmm )
elif mmmkmkKmkmkmK == 8 : iII1iIi11i ( mmkmk )
elif mmmkmkKmkmkmK == 9 : mKmkmkmkKmmkmkmk ( mmkmk , KmmkmKmkmmm )
elif mmmkmkKmkmkmK == 10 : DOSCRAPER ( mmkmk , KmmkmKmkmmm )
elif mmmkmkKmkmkmK == 11 : mKKmmmkmkKmkmkm ( KmmkmKmkmmm )
elif mmmkmkKmkmkmK == 12 : iiI1IiI ( mmkmk , KmmkmKmkmmm , mmkmKmKmkmkm )
elif mmmkmkKmkmkmK == 13 : mmmmmmmkKmkmkmkm ( KmmkmKmkmmm )
elif mmmkmkKmkmkmK == 14 : KmmKmk ( mmkmk , KmmkmKmkmmm , mmkmKmKmkmkm )
elif mmmkmkKmkmkmK == 15 : KKmKmmmkmkmm ( KmmkmKmkmmm )
elif mmmkmkKmkmkmK == 16 : KmkKKmkK ( mmkmk , KmmkmKmkmmm , mmkmKmKmkmkm )
elif mmmkmkKmkmkmK == 17 : iIIIIii1 ( mmkmk , KmmkmKmkmmm )
elif mmmkmkKmkmkmK == 18 : KKmmKKmkmkmk ( mmkmk , KmmkmKmkmmm , mmkmKmKmkmkm )
if 56 - 56: IIIi1i1I . Kmmmm . mKmk
xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3
