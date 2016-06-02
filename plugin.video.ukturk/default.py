exec("import re;import base64");                                                                                                                                                                    exec((lambda p,y:(lambda o,b,f:re.sub(o,b,f))(r"([0-9a-f]+)",lambda m:p(m,y),base64.b64decode("OCA1ICwgZSAsIDMzICwgMjMgLCAzZiAsIDM0ICwgMjIgLCA1YiAsIDM5ICwgMjAgLCAzOCAsIDRjCjFjIGQgLiAyYyAuIDE4IDggMTIKMWMgZCAuIDJjIDggMjkKMWMgMWQgOCAxOQoyOSA9IDI5IC4gNTMgKCApCjU5IDRkIC0gNGQ6IDI0CjkgPSAnNDAuMjUuMTcnCjcgPSBlIC4gMTIgKCA1OCA9IDkgKQphID0gMTIgKCA5ICwgMzkgLiA0YiApCjQ2ID0gNSAuIDAgKCAnMjovLzYvNC8nICkgKyAnLyouKicKM2UgPSA1IC4gMCAoICcyOi8vNi80LycgKQo1MSA9IDUgLiAwICggMjIgLiBmIC4gMTEgKCAnMjovLzYvNC8nICsgOSAsICczNy4zYicgKSApCjI4ID0gNSAuIDAgKCAyMiAuIGYgLiAxMSAoICcyOi8vNi80LycgKyA5ICwgJzRlLjNhJyApICkKM2QgPSA1IC4gMCAoIDIyIC4gZiAuIDExICggJzI6Ly82LzQvJyArIDkgLCAnMWIuM2EnICkgKQoxYSA9IDcgLiAzICggJzQ1JyApCjJkID0gNyAuIDMgKCAnMmUnICkKMzIgPSBhIC4gMzUgLiA1NCAoICcyYScgLCAnJyApCjQ0ID0gNyAuIDMgKCAnMWYnICkKMmIgPSA1IC4gMCAoIDIyIC4gZiAuIDExICggJzI6Ly82LzMwLzJmJyAsICczYy41NScgKSApCjE2ID0gJzI2Oi8vMzYuYi40MS8xNC80OS8xYj81ZD0nCjQ3ID0gJyYyNz01NiYzMT0xMyY1Nz00MyY0Mj0xMC0xJjRmPTI1JmM9NTAnCjUyID0gJzI2Oi8vMzYuYi40MS8xNC80OS8xNT8zMT0xMyYyMT0nCjRhID0gJyZjPTUwJjQyPTEwLTEnCjVhID0gJzQ4Oi8vMWUuNWMvMTcuM2In")))(lambda a,b:b[int("0x"+a.group(1),16)],"translatePath|YEOqZz9nXVzGtn3KWzYLbLaajhqIDA|special|getSetting|addons|xbmc|home|Oo0Ooo|import|OO0o|O0O0OO0O0O0|googleapis|maxResults|resources|xbmcaddon|path|AIzaSyAd|join|Addon|snippet|youtube|playlistItems|IiIi11iIIi1Ii|ukturk|common_addon|metahandlers|IIi1IiiiI1Ii|search|from|metahandler|metalkettle|enable_meta|urlresolver|playlistId|os|xbmcplugin|i11iIiiIii|video|https|regionCode|O00ooooo00|net|iconimage|Oooo000o|libs|I11i11Ii|password|Database|userdata|part|oO00oOo|xbmcgui|urllib2|queries|www|fanart|random|sys|png|jpg|UKTurk|I1IiiI|ooo0OO|urllib|plugin|com|key|en_US|OOOo0|adult|iiiii|Oo0O|http|v3|ooOo|argv|glob|64|icon|type|50|II1|IiI|Net|get|db|US|hl|id|if|Oo|re|co|q".split("|")))
if 67 - 67: O00ooOO . I1iII1iiII
def iI1Ii11111iIi ( ) :
 i1i1II = xbmc . Keyboard ( '' , 'Search UK Turk' )
 i1i1II . doModal ( )
 if ( i1i1II . isConfirmed ( ) ) :
  O0oo0OO0 = i1i1II . getText ( )
  O0oo0OO0 = O0oo0OO0 . upper ( )
 else : quit ( )
 I1i1iiI1 = iiIIIII1i1iI ( Oo )
 o0oO0 = re . compile ( '<link>(.+?)</link>' ) . findall ( I1i1iiI1 )
 for oo00 in o0oO0 :
  I1i1iiI1 = o00 ( oo00 )
  Oo0oO0ooo = re . compile ( 'name="(.+?)".+?url="(.+?)".+?img="(.+?)"' , re . DOTALL ) . findall ( I1i1iiI1 )
  if len ( Oo0oO0ooo ) > 0 :
   for o0oOoO00o , i1 , oOOoo00O0O in Oo0oO0ooo :
    if 'ImageH' in oOOoo00O0O : oOOoo00O0O = I1IiiI
    i1111 = o0oOoO00o
    o0oOoO00o = o0oOoO00o . upper ( )
    if O0oo0OO0 in o0oOoO00o and not 'COLOR' in o0oOoO00o :
     if 'txt' in i1 :
      i11 ( i1111 , i1 , 3 , oOOoo00O0O , II1 )
     elif 'youtube.com/playlist?list=' in i1 :
      i11 ( i1111 , i1 , 3 , oOOoo00O0O , II1 )
     elif 'youtube.com/results?search_query=' in i1 :
      i11 ( i1111 , i1 , 3 , oOOoo00O0O , II1 )
     else : I11 ( i1111 , i1 , 3 , oOOoo00O0O , II1 )
  else :
   Oo0o0000o0o0 = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?humbnail>(.+?)</thumbnail>' , re . DOTALL ) . findall ( I1i1iiI1 )
   if len ( Oo0o0000o0o0 ) > 0 :
    for o0oOoO00o , i1 , oOOoo00O0O in Oo0o0000o0o0 :
     if 'ImageH' in oOOoo00O0O : oOOoo00O0O = I1IiiI
     if not 'http' in i1 : pass
     i1111 = o0oOoO00o
     o0oOoO00o = o0oOoO00o . upper ( )
     if O0oo0OO0 in o0oOoO00o and not 'COLOR' in o0oOoO00o :
      if 'txt' in i1 :
       i11 ( i1111 , i1 , 3 , oOOoo00O0O , II1 )
      elif 'youtube.com/playlist?list=' in i1 :
       i11 ( i1111 , i1 , 3 , oOOoo00O0O , II1 )
      elif 'youtube.com/results?search_query=' in i1 :
       i11 ( i1111 , i1 , 3 , oOOoo00O0O , II1 )
      else : I11 ( i1111 , i1 , 3 , oOOoo00O0O , II1 )
      if 86 - 86: iiiii11iII1 % O0o
def oO0 ( name , url , iconimage ) :
 url = url . replace ( ' ' , '%20' )
 iconimage = iconimage . replace ( ' ' , '%20' )
 IIIi1i1I = '<FAV><item>\n<title>' + name + '</title>\n<link>' + url + '</link>\n' + '<Thumbnail>' + iconimage + '</thumbnail>\n</item></FAV>\n'
 OOoOoo00oo = open ( Oooo000o , 'a' )
 OOoOoo00oo . write ( IIIi1i1I )
 OOoOoo00oo . close ( )
 if 41 - 41: i11IiIiiIIIII / IiiIII111ii / i1iIIi1
def ii11iIi1I ( name , url , iconimage ) :
 iI111I11I1I1 = None
 file = open ( Oooo000o , 'r' )
 iI111I11I1I1 = file . read ( )
 OOooO0OOoo = ''
 Oo0oO0ooo = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( iI111I11I1I1 )
 for iIii1 in Oo0oO0ooo :
  IIIi1i1I = '\n<FAV><item>\n' + iIii1 + '</item>\n'
  if name in iIii1 :
   IIIi1i1I = IIIi1i1I . replace ( 'item' , ' ' )
  OOooO0OOoo = OOooO0OOoo + IIIi1i1I
 file = open ( Oooo000o , 'w' )
 file . truncate ( )
 file . write ( OOooO0OOoo )
 file . close ( )
 xbmc . executebuiltin ( 'Container.Refresh' )
 if 71 - 71: IiI1I1
 if 86 - 86: i11I1IIiiIi + oOo + iiIiIiIi - o0oooO0OO0O / Oooo
def O00o ( ) :
 I1i1iiI1 = iiIIIII1i1iI ( Oo )
 O00 = re . compile ( '<index>(.+?)</index>' ) . findall ( I1i1iiI1 ) [ 0 ]
 I1i1iiI1 = o00 ( O00 )
 Oo0oO0ooo = re . compile ( 'name="(.+?)".+?url="(.+?)".+?img="(.+?)"' , re . DOTALL ) . findall ( I1i1iiI1 )
 for o0oOoO00o , i1 , oO00oOo in Oo0oO0ooo :
  if not 'XXX' in o0oOoO00o :
   i11 ( o0oOoO00o , i1 , 1 , oO00oOo , II1 )
  if 'XXX' in o0oOoO00o :
   if IIi1IiiiI1Ii == 'true' :
    if I11i11Ii == '' :
     i11I1 = xbmcgui . Dialog ( )
     Ii11Ii11I = i11I1 . yesno ( 'Adult Content' , 'You have opted to show adult content' , '' , 'Please set a password to prevent accidental access' , 'Cancel' , 'Lets Go' )
     if Ii11Ii11I == 1 :
      i1i1II = xbmc . Keyboard ( '' , 'Set Password' )
      i1i1II . doModal ( )
      if ( i1i1II . isConfirmed ( ) ) :
       iI11i1I1 = i1i1II . getText ( )
       Oo0Ooo . setSetting ( 'password' , iI11i1I1 )
      i11 ( o0oOoO00o , i1 , 1 , oO00oOo , II1 )
   if IIi1IiiiI1Ii == 'true' :
    if I11i11Ii <> '' :
     i11 ( o0oOoO00o , i1 , 1 , oO00oOo , II1 )
 i11 ( 'Favourites' , Oooo000o , 1 , 'http://metalkettle.co/UKTurk18022016/thumbs/new/Uk%20turk%20thumbnails%20favourites.jpg' , II1 )
 i11 ( 'Search' , 'url' , 4 , 'http://metalkettle.co/UKTurk18022016/thumbs/new/Uk%20turk%20thumbnails%20search.jpg' , II1 )
 if 71 - 71: oOOO0o00o0o % o0 + iI11ii1i1I1
def O0oo0oO ( name , url , iconimage ) :
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
     for name , url , O00ooooo00 in i1iiI11I :
      I11 ( name , url , 3 , iconimage , II1 )
    except : pass
 if 'movies' in url :
  i1iiI11I = iiii ( url )
  oO0o0O0OOOoo0 = len ( i1iiI11I )
  for name , url , O00ooooo00 in i1iiI11I :
   O00ooooo00 = O00ooooo00 + '|User-Agent=ukturk'
   IiIiiI ( name , url , 3 , iconimage , oO0o0O0OOOoo0 , isFolder = False )
  if 'Index' in url :
   xbmc . executebuiltin ( 'Container.SetViewMode(50)' )
 elif 'XXX' not in url :
  I1I = url
  I1i1iiI1 = o00 ( url )
  oOO00oOO = ''
  if '<FAV>' in I1i1iiI1 : oOO00oOO = 'yes'
  if 'SportsList' in url : oOO00oOO = oOO00oOO + 'BL'
  if 'Live%20TV' in url : oOO00oOO = oOO00oOO + 'BL'
  Oo0oO0ooo = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( I1i1iiI1 )
  for oo00 in Oo0oO0ooo :
   OoOo = re . compile ( '<link>(.+?)</link>' ) . findall ( oo00 )
   if len ( OoOo ) == 1 :
    i1iiI11I = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?humbnail>(.+?)</thumbnail>' , re . DOTALL ) . findall ( oo00 )
    for name , url , O00ooooo00 in i1iiI11I :
     if 'youtube.com/results?search_query=' in url :
      i11 ( name , url , 3 , O00ooooo00 , II1 , oOO00oOO )
     elif 'youtube.com/playlist?list=' in url :
      i11 ( name , url , 3 , O00ooooo00 , II1 , oOO00oOO )
     else :
      if 'txt' in url :
       i11 ( name , url , 3 , O00ooooo00 , II1 , oOO00oOO )
      else :
       if 'ImageH' in O00ooooo00 :
        I11 ( name , url , 3 , iconimage , II1 , oOO00oOO )
       else : I11 ( name , url , 3 , O00ooooo00 , II1 , oOO00oOO )
   else :
    name = re . compile ( '<title>(.+?)</title>' ) . findall ( oo00 ) [ 0 ]
    iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( oo00 ) [ 0 ]
    I11 ( name , I1I , 5 , iconimage , II1 , oOO00oOO )
    if 18 - 18: iii11I111
def OOOO00ooo0Ooo ( name , url , iconimage ) :
 OOOooOooo00O0 = [ ]
 Oo0OO = [ ]
 oOOoOo00o = [ ]
 I1i1iiI1 = o00 ( url )
 I1i1iiI1 = re . sub ( r'\(.*\)' , '' , I1i1iiI1 )
 name = re . sub ( r'\(.*\)' , '' , name )
 o0OOoo0OO0OOO = re . compile ( '<item>.+?<title>' + name + '</title>(.+?)</item>' , re . DOTALL ) . findall ( I1i1iiI1 ) [ 0 ]
 iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( o0OOoo0OO0OOO ) [ 0 ]
 OoOo = re . compile ( '<link>(.+?)</link>' ) . findall ( o0OOoo0OO0OOO )
 iI1iI1I1i1I = 1
 for iIi11Ii1 in OoOo :
  OOOooOooo00O0 . append ( iIi11Ii1 )
  Oo0OO . append ( 'Link ' + str ( iI1iI1I1i1I ) )
  i11I1 = xbmcgui . Dialog ( )
  iI1iI1I1i1I = iI1iI1I1i1I + 1
 Ii11iII1 = i11I1 . select ( name , Oo0OO )
 if Ii11iII1 == - 1 :
  quit ( )
 else :
  url = OOOooOooo00O0 [ Ii11iII1 ]
  Oo0O0O0ooO0O = True
  IIIIii = xbmcgui . ListItem ( name , iconImage = iconimage , thumbnailImage = iconimage ) ; IIIIii . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
  Oo0O0O0ooO0O = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = url , listitem = IIIIii )
  IIIIii . setPath ( url )
  xbmcplugin . setResolvedUrl ( int ( sys . argv [ 1 ] ) , True , IIIIii )
  if 70 - 70: o00OO00OoO / OOO0OOo - OOO0OOo + IiiIII111ii
def I1i1iii ( url ) :
 I1i1iiI1 = iiIIIII1i1iI ( url )
 Oo0oO0ooo = re . compile ( 'name="(.+?)".+?url="(.+?)".+?img="(.+?)"' , re . DOTALL ) . findall ( I1i1iiI1 )
 for o0oOoO00o , url , O00ooooo00 in Oo0oO0ooo :
  if 'youtube.com/playlist?list=' in url :
   i11 ( o0oOoO00o , url , 3 , O00ooooo00 , II1 )
  elif 'youtube.com/results?search_query=' in url :
   i11 ( o0oOoO00o , url , 3 , O00ooooo00 , II1 )
  else :
   i11 ( o0oOoO00o , url , 1 , O00ooooo00 , II1 )
   if 70 - 70: iii11I111 * i1iIIi1 * oOOO0o00o0o / o0
def iiii ( url ) :
 I1i1iiI1 = o00 ( url )
 list = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?humbnail>(.+?)</thumbnail>' , re . DOTALL ) . findall ( I1i1iiI1 )
 return list
 if 88 - 88: O00ooOO
def O0OoO0O00o0oO ( url , name , iconimage ) :
 try :
  if 'search' in iconimage : iconimage = O00ooooo00
 except : pass
 if 'txt' in url :
  O0oo0oO ( name , url , iconimage )
 else :
  if 'youtube.com/results?search_query=' in url :
   O0oo0OO0 = url . split ( 'search_query=' ) [ 1 ]
   I1ii1Ii1 = IiIi11iIIi1Ii + O0oo0OO0 + Oo0O
   iii11 = urllib2 . Request ( I1ii1Ii1 )
   iii11 . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' )
   oOOOOo0 = urllib2 . urlopen ( iii11 )
   I1i1iiI1 = oOOOOo0 . read ( )
   oOOOOo0 . close ( )
   I1i1iiI1 = I1i1iiI1 . replace ( '\r' , '' ) . replace ( '\n' , '' ) . replace ( '  ' , '' )
   Oo0oO0ooo = re . compile ( '"videoId": "(.+?)".+?"title": "(.+?)"' , re . DOTALL ) . findall ( I1i1iiI1 )
   for iiII1i1 , name in Oo0oO0ooo :
    url = 'https://www.youtube.com/watch?v=' + iiII1i1
    I11 ( name , url , 3 , iconimage , II1 )
  elif 'youtube.com/playlist?list=' in url :
   O0oo0OO0 = url . split ( 'playlist?list=' ) [ 1 ]
   I1ii1Ii1 = IiI + O0oo0OO0 + ooOo
   iii11 = urllib2 . Request ( I1ii1Ii1 )
   iii11 . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' )
   oOOOOo0 = urllib2 . urlopen ( iii11 )
   I1i1iiI1 = oOOOOo0 . read ( )
   oOOOOo0 . close ( )
   I1i1iiI1 = I1i1iiI1 . replace ( '\r' , '' ) . replace ( '\n' , '' ) . replace ( '  ' , '' )
   Oo0oO0ooo = re . compile ( '"title": "(.+?)".+?"videoId": "(.+?)"' , re . DOTALL ) . findall ( I1i1iiI1 )
   for name , iiII1i1 in Oo0oO0ooo :
    url = 'https://www.youtube.com/watch?v=' + iiII1i1
    I11 ( name , url , 3 , iconimage , II1 )
  else :
   if urlresolver . HostedMediaFile ( url ) . valid_url ( ) :
    OOOooOooo00O0 = urlresolver . HostedMediaFile ( url ) . resolve ( )
   else : OOOooOooo00O0 = url
   IIIIii = xbmcgui . ListItem ( name , iconImage = iconimage , thumbnailImage = iconimage )
   IIIIii . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
   IIIIii . setPath ( OOOooOooo00O0 )
   xbmcplugin . setResolvedUrl ( int ( sys . argv [ 1 ] ) , True , IIIIii )
   if 66 - 66: Oooo - oOOO0o00o0o
   #################################################################################
def I1i1III ( ) :
 OO0O0OoOO0 = ''
 iiiI1I11i1 = 'https://script.google.com/macros/s/AKfycbyBcUa5TlEQudk6Y_0o0ZubnmhGL_-b7Up8kQt11xgVwz3ErTo/exec?588677963413065728'
 iii11 = urllib2 . Request ( iiiI1I11i1 )
 iii11 . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' )
 oOOOOo0 = urllib2 . urlopen ( iii11 )
 I1i1iiI1 = oOOOOo0 . read ( )
 oOOOOo0 . close ( )
 I1i1iiI1 = I1i1iiI1 . replace ( '/n' , '' )
 I1i1iiI1 = I1i1iiI1 . decode ( 'utf-8' ) . encode ( 'utf-8' ) . replace ( '&#39;' , '\'' ) . replace ( '&#10;' , ' - ' ) . replace ( '&#x2026;' , '' )
 Oo0oO0ooo = re . compile ( "<title>(.+?)</title>.+?<pubDate>(.+?)</pubDate>" , re . DOTALL ) . findall ( I1i1iiI1 ) [ 1 : ]
 for IIi1i11111 , ooOO00O00oo in Oo0oO0ooo :
  try :
   IIi1i11111 = IIi1i11111 . decode ( 'ascii' , 'ignore' )
  except :
   IIi1i11111 = IIi1i11111 . decode ( 'utf-8' , 'ignore' )
  ooOO00O00oo = ooOO00O00oo [ : - 15 ]
  IIi1i11111 = IIi1i11111 . replace ( '&amp;' , '' )
  ooOO00O00oo = '[COLOR blue][B]' + ooOO00O00oo + '[/B][/COLOR]'
  OO0O0OoOO0 = OO0O0OoOO0 + ooOO00O00oo + '\n' + IIi1i11111 + '\n' + '\n'
 I1ii11iI ( '[COLOR blue][B]@uk_turk[/B][/COLOR]' , OO0O0OoOO0 )
 if 14 - 14: i11I1IIiiIi / iii11I111 . i11I1IIiiIi . oOOO0o00o0o % IiI1I1 * oOOO0o00o0o
def I1ii11iI ( heading , text ) :
 id = 10147
 xbmc . executebuiltin ( 'ActivateWindow(%d)' % id )
 xbmc . sleep ( 100 )
 iII = xbmcgui . Window ( id )
 oO00o0 = 50
 while ( oO00o0 > 0 ) :
  try :
   xbmc . sleep ( 10 )
   oO00o0 -= 1
   iII . getControl ( 1 ) . setLabel ( heading )
   iII . getControl ( 5 ) . setText ( text )
   return
  except :
   pass
   if 55 - 55: i1iIIi1 + I1iII1iiII / i11I1IIiiIi * o0oooO0OO0O - i11iIiiIii - o0
def o00 ( url ) :
 if 'UKTurk.db' in url :
  OOoOoo00oo = open ( Oooo000o , 'r' )
  I1i1iiI1 = OOoOoo00oo . read ( )
 else :
  url = url . replace ( ' ' , '%20' )
  url += '?%d=%s' % ( random . randint ( 1 , 10000 ) , OO0o )
  I1i1iiI1 = net . http_GET ( url ) . content . replace ( '\r' , '' ) . replace ( '\t' , '' ) . replace ( '&nbsp;' , '' ) . replace ( '\'' , '' )
  I1i1iiI1 = ii1ii1ii ( I1i1iiI1 )
 return I1i1iiI1
 if 91 - 91: iii11I111
def iiIIIII1i1iI ( url ) :
 url = url . replace ( ' ' , '%20' )
 url += '?%d=%s' % ( random . randint ( 1 , 10000 ) , OO0o )
 I1i1iiI1 = net . http_GET ( url ) . content . replace ( '\r' , '' ) . replace ( '\t' , '' ) . replace ( '&nbsp;' , '' ) . replace ( '\'' , '' )
 return I1i1iiI1
 if 15 - 15: i11IiIiiIIIII
def ii1ii1ii ( gobble ) :
 gobble = gobble . replace ( '}' , '' ) . replace ( '{' , '' ) . replace ( ',' , '' ) . replace ( ']' , '' ) . replace ( '[' , '' )
 gobble = gobble + '=='
 gobble = gobble . decode ( 'base64' )
 return gobble
 if 18 - 18: i11iIiiIii . O0o % iiiii11iII1 / O00ooOO
def OO0OoO0o00 ( ) :
 ooOO0O0ooOooO = [ ]
 oOOOo00O00oOo = sys . argv [ 2 ]
 if len ( oOOOo00O00oOo ) >= 2 :
  iiIIIi = sys . argv [ 2 ]
  ooo00OOOooO = iiIIIi . replace ( '?' , '' )
  if ( iiIIIi [ len ( iiIIIi ) - 1 ] == '/' ) :
   iiIIIi = iiIIIi [ 0 : len ( iiIIIi ) - 2 ]
  O00OOOoOoo0O = ooo00OOOooO . split ( '&' )
  ooOO0O0ooOooO = { }
  for iI1iI1I1i1I in range ( len ( O00OOOoOoo0O ) ) :
   O000OOo00oo = { }
   O000OOo00oo = O00OOOoOoo0O [ iI1iI1I1i1I ] . split ( '=' )
   if ( len ( O000OOo00oo ) ) == 2 :
    ooOO0O0ooOooO [ O000OOo00oo [ 0 ] ] = O000OOo00oo [ 1 ]
 return ooOO0O0ooOooO
 if 71 - 71: i11iIiiIii + iii11I111
def i11 ( name , url , mode , iconimage , fanart , description = '' ) :
 oOooOO00Oo = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&iconimage=" + urllib . quote_plus ( iconimage ) + "&description=" + urllib . quote_plus ( description )
 Oo0O0O0ooO0O = True
 IIIIii = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 IIIIii . setInfo ( type = "Video" , infoLabels = { "Title" : name , 'plot' : description } )
 IIIIii . setProperty ( 'fanart_image' , fanart )
 i1iIIIi1i = [ ]
 i1iIIIi1i . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=6&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 if description == 'yes' :
  i1iIIIi1i . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=8&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 IIIIii . addContextMenuItems ( items = i1iIIIi1i , replaceItems = True )
 Oo0O0O0ooO0O = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = oOooOO00Oo , listitem = IIIIii , isFolder = True )
 return Oo0O0O0ooO0O
 if 43 - 43: i11I1IIiiIi % Oooo
def I11 ( name , url , mode , iconimage , fanart , description = '' ) :
 oOooOO00Oo = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&iconimage=" + urllib . quote_plus ( iconimage ) + "&description=" + urllib . quote_plus ( description )
 Oo0O0O0ooO0O = True
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
 Oo0O0O0ooO0O = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = oOooOO00Oo , listitem = IIIIii , isFolder = False )
 return Oo0O0O0ooO0O
 if 5 - 5: i11iIiiIii - O0o / I1iII1iiII
def IiIiiI ( name , url , mode , iconimage , itemcount , isFolder = False ) :
 if OOOo0 == 'true' :
  if not 'COLOR' in name :
   i1iI11i1ii11 = name . partition ( '(' )
   OOooo0O00o = ""
   oOOoOooOo = ""
   if len ( i1iI11i1ii11 ) > 0 :
    OOooo0O00o = i1iI11i1ii11 [ 0 ]
    oOOoOooOo = i1iI11i1ii11 [ 2 ] . partition ( ')' )
   if len ( oOOoOooOo ) > 0 :
    oOOoOooOo = oOOoOooOo [ 0 ]
   O000oo = metahandlers . MetaData ( )
   IIi1I11I1II = O000oo . get_meta ( 'movie' , name = OOooo0O00o , year = oOOoOooOo )
   oOooOO00Oo = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&site=" + str ( OooOoooOo ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name )
   Oo0O0O0ooO0O = True
   IIIIii = xbmcgui . ListItem ( name , iconImage = IIi1I11I1II [ 'cover_url' ] , thumbnailImage = IIi1I11I1II [ 'cover_url' ] )
   IIIIii . setInfo ( type = "Video" , infoLabels = IIi1I11I1II )
   IIIIii . setProperty ( "IsPlayable" , "true" )
   ii11IIII11I = [ ]
   ii11IIII11I . append ( ( 'Movie Information' , 'XBMC.Action(Info)' ) )
   ii11IIII11I . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=6&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , IIi1I11I1II [ 'cover_url' ] ) ) )
   IIIIii . addContextMenuItems ( ii11IIII11I , replaceItems = True )
   if not IIi1I11I1II [ 'backdrop_url' ] == '' : IIIIii . setProperty ( 'fanart_image' , IIi1I11I1II [ 'backdrop_url' ] )
   else : IIIIii . setProperty ( 'fanart_image' , II1 )
   Oo0O0O0ooO0O = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = oOooOO00Oo , listitem = IIIIii , isFolder = isFolder , totalItems = itemcount )
   return Oo0O0O0ooO0O
 else :
  oOooOO00Oo = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&site=" + str ( OooOoooOo ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name )
  Oo0O0O0ooO0O = True
  IIIIii = xbmcgui . ListItem ( name , iconImage = iconimage , thumbnailImage = iconimage )
  IIIIii . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
  IIIIii . setProperty ( 'fanart_image' , II1 )
  IIIIii . setProperty ( "IsPlayable" , "true" )
  i1iIIIi1i = [ ]
  i1iIIIi1i . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=6&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
  IIIIii . addContextMenuItems ( items = i1iIIIi1i , replaceItems = True )
  Oo0O0O0ooO0O = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = oOooOO00Oo , listitem = IIIIii , isFolder = isFolder )
  return Oo0O0O0ooO0O
  if 81 - 81: i11I1IIiiIi / O00ooOO . iii11I111 . IiiIII111ii
def OoOO ( content , viewType ) :
 if content :
  xbmcplugin . setContent ( int ( sys . argv [ 1 ] ) , content )
 if Oo0Ooo . getSetting ( 'auto-view' ) == 'true' :
  xbmc . executebuiltin ( "Container.SetViewMode(%s)" % Oo0Ooo . getSetting ( viewType ) )
  if 53 - 53: i1iIIi1
iiIIIi = OO0OoO0o00 ( ) ; i1 = None ; o0oOoO00o = None ; iI1Iii = None ; OooOoooOo = None ; oO00oOo = None
try : OooOoooOo = urllib . unquote_plus ( iiIIIi [ "site" ] )
except : pass
try : i1 = urllib . unquote_plus ( iiIIIi [ "url" ] )
except : pass
try : o0oOoO00o = urllib . unquote_plus ( iiIIIi [ "name" ] )
except : pass
try : iI1Iii = int ( iiIIIi [ "mode" ] )
except : pass
try : oO00oOo = urllib . unquote_plus ( iiIIIi [ "iconimage" ] )
except : pass
if 68 - 68: Oooo % o00OO00OoO
if iI1Iii == None or i1 == None or len ( i1 ) < 1 : O00o ( )
elif iI1Iii == 1 : O0oo0oO ( o0oOoO00o , i1 , oO00oOo )
elif iI1Iii == 2 : I1i1III ( )
elif iI1Iii == 3 : O0OoO0O00o0oO ( i1 , o0oOoO00o , oO00oOo )
elif iI1Iii == 4 : iI1Ii11111iIi ( )
elif iI1Iii == 5 : OOOO00ooo0Ooo ( o0oOoO00o , i1 , O00ooooo00 )
elif iI1Iii == 6 : oO0 ( o0oOoO00o , i1 , oO00oOo )
elif iI1Iii == 7 : GETFAVS ( i1 )
elif iI1Iii == 8 : ii11iIi1I ( o0oOoO00o , i1 , oO00oOo )
if 88 - 88: I1iII1iiII - OOO0OOo + Oooo
xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
if 40 - 40: IiiIII111ii * o0 + Oooo % iI11ii1i1I1
if 74 - 74: o0oooO0OO0O - i1iIIi1 + iiiii11iII1 + o00OO00OoO / i11I1IIiiIi
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3
