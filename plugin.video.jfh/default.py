if 64 - 64: i11iIiiIii
if 65 - 65: O0 / iIii1I11I1II1 % OoooooooOO - i1IIi
if 73 - 73: II111iiii
if 22 - 22: I1IiiI * Oo0Ooo / OoO0O00 . OoOoOO00 . o0oOOo0O0Ooo / I1ii11iIi11i
if 48 - 48: oO0o / OOooOOo / I11i / Ii1I
if 48 - 48: iII111i % IiII + I1Ii111 / ooOoO0o * Ii1I
if 46 - 46: ooOoO0o * I11i - OoooooooOO
if 30 - 30: o0oOOo0O0Ooo - O0 % o0oOOo0O0Ooo - OoooooooOO * O0 * OoooooooOO
if 60 - 60: iIii1I11I1II1 / i1IIi * oO0o - I1ii11iIi11i + o0oOOo0O0Ooo
if 94 - 94: i1IIi % Oo0Ooo
import sys , os , xbmc , xbmcgui , xbmcplugin , xbmcaddon , urllib , urllib2 , cookielib , re
if 68 - 68: Ii1I / O0
Iiii111Ii11I1 = xbmcaddon . Addon ( id = 'plugin.video.jfh' )
ooO0oooOoO0 = cookielib . LWPCookieJar ( )
II11i = urllib2 . HTTPCookieProcessor ( ooO0oooOoO0 )
i1 = urllib2 . build_opener ( II11i )
oOOoo00O0O = 'plugin.video.jfh'
i1111 = xbmcaddon . Addon ( id = oOOoo00O0O )
i11 = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + oOOoo00O0O , 'icon.png' ) )
if 41 - 41: I1Ii111 . ooOoO0o * IiII % i11iIiiIii
def o000o0o00o0Oo ( ) :
 oo = IiII1I1i1i1ii ( 'http://www.perfectgirls.net/' )
 IIIII = re . compile ( '<a href="/category/([0-9][0-9])/(.*)">(.*)</a>' ) . findall ( oo )
 I1 ( '[COLOR red]Latest[/COLOR]' , 'http://www.perfectgirls.net/' , 1 , i11 , 1 )
 I1 ( '---' , '' , 1 , '' , 1 )
 for O0OoOoo00o , iiiI11 , OOooO in IIIII :
  I1 ( OOooO ,
 ( 'http://www.perfectgirls.net/category/' + O0OoOoo00o + '/' + iiiI11 ) ,
 1 , i11 , 1 )
 xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
 if 58 - 58: OoO0O00 + OoOoOO00 / Ii1I * OoooooooOO
def II111iiiiII ( url ) :
 oo = IiII1I1i1i1ii ( url )
 IIIII = re . compile ( '-->\n<a href="/([0-9]+)/(.*)" title="(.*)">' ) . findall ( oo )
 for oOoOo00oOo , Oo , OOooO , in IIIII :
  o00O00O0O0O ( OOooO , 'http://www.perfectgirls.net/' + oOoOo00oOo + '/' + Oo , 2 , i11 )
 xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
 if 90 - 90: II111iiii + oO0o / o0oOOo0O0Ooo % II111iiii - O0
 if 29 - 29: o0oOOo0O0Ooo / iIii1I11I1II1
def IiIIIiI1I1 ( url ) :
 oo = IiII1I1i1i1ii ( url )
 IIIII = re . compile ( 'get\("(.*)", function' ) . findall ( oo )
 for OoO000 in IIIII :
  oo = IiII1I1i1i1ii ( 'http://www.perfectgirls.net/' + OoO000 )
  IIiiIiI1 = re . compile ( 'http://(.*)' ) . findall ( oo )
  iiIiIIi = [ 'http://' + str ( IIiiIiI1 [ 0 ] ) ]
  if IIiiIiI1 :
   xbmc . Player ( ) . play ( iiIiIIi [ - 1 ] )
   if 65 - 65: OoOoOO00
   if 6 - 6: I1IiiI / Oo0Ooo % Ii1I
def ooOO0O00 ( ) :
 ii1 = [ ]
 o0oO0o00oo = sys . argv [ 2 ]
 if len ( o0oO0o00oo ) >= 2 :
  II1i1Ii11Ii11 = sys . argv [ 2 ]
  iII11i = II1i1Ii11Ii11 . replace ( '?' , '' )
  if ( II1i1Ii11Ii11 [ len ( II1i1Ii11Ii11 ) - 1 ] == '/' ) :
   II1i1Ii11Ii11 = II1i1Ii11Ii11 [ 0 : len ( II1i1Ii11Ii11 ) - 2 ]
  O0O00o0OOO0 = iII11i . split ( '&' )
  ii1 = { }
  for Ii1iIIIi1ii in range ( len ( O0O00o0OOO0 ) ) :
   o0oo0o0O00OO = { }
   o0oo0o0O00OO = O0O00o0OOO0 [ Ii1iIIIi1ii ] . split ( '=' )
   if ( len ( o0oo0o0O00OO ) ) == 2 :
    ii1 [ o0oo0o0O00OO [ 0 ] ] = o0oo0o0O00OO [ 1 ]
 return ii1
 if 80 - 80: i1IIi
 if 70 - 70: OoOoOO00 - o0oOOo0O0Ooo
def o00O00O0O0O ( name , url , mode , iconimage ) :
 I1iii = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name )
 if 20 - 20: o0oOOo0O0Ooo
 oO00 = True
 ooo = xbmcgui . ListItem ( name , iconImage = "icon.png" ,
 thumbnailImage = iconimage )
 oO00 = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = I1iii ,
 listitem = ooo , isFolder = False )
 return oO00
 if 18 - 18: o0oOOo0O0Ooo
 if 28 - 28: OOooOOo - IiII . IiII + OoOoOO00 - OoooooooOO + O0
def I1 ( name , url , mode , iconimage , page ) :
 I1iii = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&page=" + str ( page )
 if 95 - 95: OoO0O00 % oO0o . O0
 oO00 = True
 ooo = xbmcgui . ListItem ( name , iconImage = "icon.png" ,
 thumbnailImage = iconimage )
 oO00 = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = I1iii ,
 listitem = ooo , isFolder = True )
 return oO00
 if 15 - 15: ooOoO0o / Ii1I . Ii1I - i1IIi
 if 53 - 53: IiII + I1IiiI * oO0o
def IiII1I1i1i1ii ( url ) :
 OooOooooOOoo0 = urllib2 . Request ( url )
 OooOooooOOoo0 . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' )
 o00OO0OOO0 = urllib2 . urlopen ( OooOooooOOoo0 )
 oo = o00OO0OOO0 . read ( )
 o00OO0OOO0 . close ( )
 return oo
 if 83 - 83: OoooooooOO
 if 31 - 31: II111iiii - OOooOOo . I1Ii111 % OoOoOO00 - O0
def iii11 ( ) :
 II1i1Ii11Ii11 = ooOO0O00 ( )
 O0oo0OO0oOOOo = None
 OOooO = None
 i1i1i11IIi = None
 II1III = 1
 if 19 - 19: oO0o % i1IIi % o0oOOo0O0Ooo
 try :
  O0oo0OO0oOOOo = urllib . unquote_plus ( II1i1Ii11Ii11 [ "url" ] )
 except :
  pass
 try :
  OOooO = urllib . unquote_plus ( II1i1Ii11Ii11 [ "name" ] )
 except :
  pass
 try :
  i1i1i11IIi = int ( II1i1Ii11Ii11 [ "mode" ] )
 except :
  pass
 try :
  II1III = int ( II1i1Ii11Ii11 [ "page" ] )
 except :
  pass
  if 93 - 93: iIii1I11I1II1 % oO0o * i1IIi
 if i1i1i11IIi == None or O0oo0OO0oOOOo == None or len ( O0oo0OO0oOOOo ) < 1 :
  o000o0o00o0Oo ( )
  if 16 - 16: O0 - I1Ii111 * iIii1I11I1II1 + iII111i
 elif i1i1i11IIi == 1 :
  xbmc . log ( "VIDEOLIST " + O0oo0OO0oOOOo )
  xbmc . log ( "VIDEOLIST " + str ( II1III ) )
  II111iiiiII ( O0oo0OO0oOOOo )
  if 50 - 50: II111iiii - ooOoO0o * I1ii11iIi11i / I1Ii111 + o0oOOo0O0Ooo
 elif i1i1i11IIi == 2 :
  xbmc . log ( "PLAYVIDEO " + O0oo0OO0oOOOo )
  IiIIIiI1I1 ( O0oo0OO0oOOOo )
  if 88 - 88: Ii1I / I1Ii111 + iII111i - II111iiii / ooOoO0o - OoOoOO00
  if 15 - 15: I1ii11iIi11i + OoOoOO00 - OoooooooOO / OOooOOo
if __name__ == "__main__" :
 iii11 ( )
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3
