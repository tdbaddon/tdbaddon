import xbmc , xbmcaddon , xbmcgui , xbmcplugin , urllib , urllib2 , os , re , sys , datetime , shutil , urlresolver , random , liveresolver
from resources . libs . common_addon import Addon
import base64
from metahandler import metahandlers
if 64 - 64: i11iIiiIii
from pyDes import *
import base64
import os
if 65 - 65: O0 / iIii1I11I1II1 % OoooooooOO - i1IIi
if 73 - 73: II111iiii
# decoded = DecodeAES(cipher, data_to_be_decrypted)
if 22 - 22: I1IiiI * Oo0Ooo / OoO0O00 . OoOoOO00 . o0oOOo0O0Ooo / I1ii11iIi11i
I1IiI = 'plugin.video.streamarmy'
o0OOO = Addon ( I1IiI , sys . argv )
iIiiiI = xbmcaddon . Addon ( id = I1IiI )
Iii1ii1II11i = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + I1IiI , 'fanart.jpg' ) )
iI111iI = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + I1IiI , 'fanart.jpg' ) )
IiII = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + I1IiI , 'icon.png' ) )
iI1Ii11111iIi = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + I1IiI , 'search.jpg' ) )
i1i1II = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + I1IiI , 'next.png' ) )
O0oo0OO0 = xbmc . translatePath ( os . path . join ( 'special://home/addons/' , 'plugin.video.sportsdevil' ) )
I1i1iiI1 = base64 . b64decode ( b'aHR0cDovL3d3dy5zdHJlYW1hcm15LnVrL01haW4vTWVudS54bWw=' )
iiIIIII1i1iI = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId='
o0oO0 = '&maxResults=50&key=AIzaSyCebQaY3SIk6VlFNzDlYy4nqNva9c9N4CI'
oo00 = 'https://www.googleapis.com/youtube/v3/playlistItems?pageToken='
o00 = '&part=snippet&playlistId='
Oo0oO0ooo = '&maxResults=50&key=AIzaSyCebQaY3SIk6VlFNzDlYy4nqNva9c9N4CI'
o0oOoO00o = iIiiiI . getSetting ( 'password' )
i1 = iIiiiI . getSetting ( 'Conspiracy Password' )
oOOoo00O0O = iIiiiI . getSetting ( 'enable_meta' )
i1111 = 'http://streamarmy.uk/Main/update.txt'
i11 = base64 . b64decode ( b'aHR0cDovL2dldGFmbGl4LnVzL2FkZG9uL3lvdXR1YmUucGhw' )
I11 = 'http://streamarmy.uk/Main/searchtext.xml'
Oo0o0000o0o0 = 'http://www.streamarmy.uk/Main/Exceptions/Exceptions.xml'
if 86 - 86: iiiii11iII1 % O0o
if 97 - 97: IIIII . I1
O0OoOoo00o = base64 . b64decode ( b"MzkyNjk5bGl2ZXJwb29sNQ==" )
if 31 - 31: i111IiI + iIIIiI11 . iII111ii
if 3 - 3: oOo0Oo + O0o
IiIi1Iii1I1 = 16
if 67 - 67: oOo0Oo - iiiii11iII1 * o0oOOo0O0Ooo % o0oOOo0O0Ooo % IIIII * OoOoOO00
if 26 - 26: I1 - o0oOOo0O0Ooo
if 63 - 63: II111iiii . II111iiii
if 32 - 32: i1IIi . IIIII % OoO0O00 . o0oOOo0O0Ooo
i1I111I = '{'
if 1 - 1: iIIIiI11 % OoO0O00 * IIIII
if 55 - 55: i1IIi / i11iIiiIii + O0o + OoO0O00
iIi = lambda II : II + ( IiIi1Iii1I1 - len ( II ) % IiIi1Iii1I1 ) * i1I111I
if 14 - 14: Oo0Ooo . I1IiiI / I1
if 38 - 38: II111iiii % i11iIiiIii . oOo0Oo - O0o + I1
if 66 - 66: OoooooooOO * OoooooooOO . O0o . i1IIi - O0o
o0o00ooo0 = lambda oo0Oo00Oo0 , II : base64 . b64encode ( oo0Oo00Oo0 . encrypt ( iIi ( II ) ) )
oOOO00o = lambda oo0Oo00Oo0 , O0O00o0OOO0 : oo0Oo00Oo0 . decrypt ( base64 . b64decode ( O0O00o0OOO0 ) ) . rstrip ( i1I111I )
Ii1iIIIi1ii = triple_des ( O0OoOoo00o , CBC )
if 80 - 80: IIIII * i11iIiiIii / iII111ii
if 9 - 9: I1 + iiiii11iII1 % I1 + i1IIi . O0o
def III1i1i ( link , splitting = '\n' ) :
 iiI1 = urllib2 . Request ( link )
 try :
  i11Iiii = urllib2 . urlopen ( iiI1 )
 except IOError :
  return [ ]
  if 23 - 23: o0oOOo0O0Ooo . II111iiii
 else :
  Oo0O0OOOoo = i11Iiii . read ( )
  return Oo0O0OOOoo . split ( splitting )
  if 95 - 95: OoO0O00 % iiiii11iII1 . O0
I1i1I = III1i1i ( Oo0o0000o0o0 )
if 80 - 80: OoOoOO00 - OoO0O00
if 87 - 87: iiiii11iII1 / IIIII - i1IIi * O0o / OoooooooOO . O0
def iii11I111 ( ) :
 OOOO00ooo0Ooo ( )
 xbmc . executebuiltin ( 'Container.SetViewMode(500)' )
 OOOooOooo00O0 = I1i1iiI1
 Oo0OO ( '[B][COLOR lime]S[/COLOR][COLOR white]earch[/COLOR][/B] [B][COLOR lime]S[/COLOR][COLOR white]tream[/COLOR][/B] [B][COLOR lime]A[/COLOR][COLOR white]rmy[/COLOR][/B]' , OOOooOooo00O0 , 5 , iI1Ii11111iIi , iI111iI )
 oOOoOo00o = o0OOoo0OO0OOO ( I1i1iiI1 )
 iI1iI1I1i1I = re . compile ( '<item>(.+?)</item>' ) . findall ( oOOoOo00o )
 for iIi11Ii1 in iI1iI1I1i1I :
  try :
   if '<channel>' in iIi11Ii1 :
    Ii11iII1 = re . compile ( '<title>(.+?)</title>' ) . findall ( iIi11Ii1 ) [ 0 ]
    Oo0O0O0ooO0O = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( iIi11Ii1 ) [ 0 ]
    Iii1ii1II11i = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( iIi11Ii1 ) [ 0 ]
    OOOooOooo00O0 = re . compile ( '<channel>(.+?)</channel>' ) . findall ( iIi11Ii1 ) [ 0 ]
    Oo0OO ( Ii11iII1 , OOOooOooo00O0 , 6 , Oo0O0O0ooO0O , Iii1ii1II11i )
   if '<sportsdevil>' in iIi11Ii1 :
    IIIIii = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( iIi11Ii1 )
    if len ( IIIIii ) == 1 :
     Ii11iII1 = re . compile ( '<title>(.+?)</title>' ) . findall ( iIi11Ii1 ) [ 0 ]
     Oo0O0O0ooO0O = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( iIi11Ii1 ) [ 0 ]
     OOOooOooo00O0 = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( iIi11Ii1 ) [ 0 ]
     O0o0 = re . compile ( '<referer>(.+?)</referer>' ) . findall ( iIi11Ii1 ) [ 0 ]
     OO00Oo = O0o0
     O0OOO0OOoO0O = "/"
     if not OO00Oo . endswith ( O0OOO0OOoO0O ) :
      O00Oo000ooO0 = OO00Oo + "/"
     else :
      O00Oo000ooO0 = OO00Oo
     oOOoOo00o = 'plugin://plugin.video.SportsDevil/?mode=10&amp;item=catcher%3dstreams%26url=' + OOOooOooo00O0
     OOOooOooo00O0 = oOOoOo00o + '%26referer=' + O00Oo000ooO0
     OoO0O00IIiII ( Ii11iII1 , OOOooOooo00O0 , 4 , Oo0O0O0ooO0O , Iii1ii1II11i )
    elif len ( IIIIii ) > 1 :
     Ii11iII1 = re . compile ( '<title>(.+?)</title>' ) . findall ( iIi11Ii1 ) [ 0 ]
     Oo0O0O0ooO0O = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( iIi11Ii1 ) [ 0 ]
     Iii1ii1II11i = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( iIi11Ii1 ) [ 0 ]
     OoO0O00IIiII ( Ii11iII1 , url2 , 8 , Oo0O0O0ooO0O , Iii1ii1II11i )
     if 80 - 80: iIIIiI11 . iiiii11iII1
     if 25 - 25: OoOoOO00 . II111iiii / i111IiI . O0o * OoO0O00 . I1IiiI
   elif '<folder>' in iIi11Ii1 :
    Oo0oOOo = re . compile ( '<title>(.+?)</title>.+?folder>(.+?)</folder>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>' ) . findall ( iIi11Ii1 )
    for Ii11iII1 , OOOooOooo00O0 , Oo0O0O0ooO0O , Iii1ii1II11i in Oo0oOOo :
     if 58 - 58: II111iiii * O0o * I1ii11iIi11i / O0o
     if OOOooOooo00O0 in I1i1I :
      Oo0OO ( Ii11iII1 , OOOooOooo00O0 , 1 , Oo0O0O0ooO0O , Iii1ii1II11i )
     else :
      Oo0OO ( Ii11iII1 , OOOooOooo00O0 , 10 , Oo0O0O0ooO0O , Iii1ii1II11i )
   else :
    IIIIii = re . compile ( '<link>(.+?)</link>' ) . findall ( iIi11Ii1 )
    if len ( IIIIii ) == 1 :
     Oo0oOOo = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>' ) . findall ( iIi11Ii1 )
     oO0o0OOOO = len ( iI1iI1I1i1I )
     for Ii11iII1 , OOOooOooo00O0 , Oo0O0O0ooO0O , Iii1ii1II11i in Oo0oOOo :
      if 'youtube.com/playlist' in OOOooOooo00O0 :
       Oo0OO ( Ii11iII1 , OOOooOooo00O0 , 2 , Oo0O0O0ooO0O , Iii1ii1II11i )
      else :
       O0O0OoOO0 ( Ii11iII1 , OOOooOooo00O0 , 2 , Oo0O0O0ooO0O , Iii1ii1II11i )
    elif len ( IIIIii ) > 1 :
     Ii11iII1 = re . compile ( '<title>(.+?)</title>' ) . findall ( iIi11Ii1 ) [ 0 ]
     Oo0O0O0ooO0O = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( iIi11Ii1 ) [ 0 ]
     Iii1ii1II11i = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( iIi11Ii1 ) [ 0 ]
     O0O0OoOO0 ( Ii11iII1 , url2 , 3 , Oo0O0O0ooO0O , Iii1ii1II11i )
  except : pass
  iiiI1I11i1 ( oOOoOo00o )
  if 49 - 49: I1IiiI % oOo0Oo . oOo0Oo . IIIII * oOo0Oo
def OOOO00ooo0Ooo ( ) :
 O0oOO0 = O0ooo0O0oo0 ( i1111 )
 if len ( O0oOO0 ) > 1 :
  oo0oOo = xbmcaddon . Addon ( ) . getAddonInfo ( 'path' )
  o000O0o = os . path . join ( os . path . join ( oo0oOo , '' ) , 'compare.txt' )
  iI1iII1 = open ( o000O0o )
  oO0OOoo0OO = iI1iII1 . read ( )
  if oO0OOoo0OO == O0oOO0 : pass
  else :
   O0ii1ii1ii ( '[B][COLOR lime]S[/COLOR][COLOR white]tream[/COLOR][/B] [B][COLOR lime]A[/COLOR][COLOR white]rmy[/COLOR][/B] [B][COLOR lime]I[/COLOR][COLOR white]nformation[/COLOR][/B]' , O0oOO0 )
   oooooOoo0ooo = open ( o000O0o , "w" )
   oooooOoo0ooo . write ( O0oOO0 )
   oooooOoo0ooo . close ( )
   if 6 - 6: IIIII - I1 + iIii1I11I1II1 - iII111ii - i11iIiiIii
   if 79 - 79: OoOoOO00 - O0 * OoO0O00 + OoOoOO00 % O0 * O0
def oOOo0 ( name , url , iconimage , fanart ) :
 if 54 - 54: O0 - iIIIiI11 % O0o
 print "------------ In get encrypted content ------------"
 OOoO = url
 oOOoOo00o = o0OOoo0OO0OOO ( url )
 if 46 - 46: OoO0O00 . Oo0Ooo - OoooooooOO
 print "------------ open_encrypted_url complete ------------"
 if 93 - 93: i111IiI
 if 'XXX>yes</XXX' in oOOoOo00o :
  if o0oOoO00o == '' :
   i1IIIiiII1 = xbmcgui . Dialog ( )
   OOOOoOoo0O0O0 = i1IIIiiII1 . yesno ( 'Adult Content' , 'You have opted to show adult content' , '' , 'Please set a password to prevent accidental access' , 'Cancel' , 'OK' )
   if OOOOoOoo0O0O0 == 1 :
    OOOo00oo0oO = xbmc . Keyboard ( '' , 'Set Password' )
    OOOo00oo0oO . doModal ( )
   if ( OOOo00oo0oO . isConfirmed ( ) ) :
    IIiIi1iI = OOOo00oo0oO . getText ( )
    iIiiiI . setSetting ( 'password' , IIiIi1iI )
   else : quit ( )
   if 35 - 35: I1 % O0 - O0
 if 'XXX>yes</XXX' in oOOoOo00o :
  if o0oOoO00o <> '' :
   i1IIIiiII1 = xbmcgui . Dialog ( )
   OOOOoOoo0O0O0 = i1IIIiiII1 . yesno ( 'Adult Content' , 'Please enter the password you set' , 'to continue' , '' , 'Cancel' , 'OK' )
   if OOOOoOoo0O0O0 == 1 :
    OOOo00oo0oO = xbmc . Keyboard ( '' , 'Enter Password' )
    OOOo00oo0oO . doModal ( )
   if ( OOOo00oo0oO . isConfirmed ( ) ) :
    IIiIi1iI = OOOo00oo0oO . getText ( )
   if IIiIi1iI <> o0oOoO00o :
    quit ( )
  else : quit ( )
  if 16 - 16: II111iiii % OoOoOO00 - II111iiii + I1
 if 'con>yes</con' in oOOoOo00o :
  if i1 == '' :
   i1IIIiiII1 = xbmcgui . Dialog ( )
   OOOOoOoo0O0O0 = i1IIIiiII1 . yesno ( 'Conspiracy Content' , 'You have opted to show Conspiracy content' , '' , 'Due to the Nature of Content ,Please set a password to prevent accidental access' , 'Cancel' , 'OK' )
   if OOOOoOoo0O0O0 == 1 :
    OOOo00oo0oO = xbmc . Keyboard ( '' , 'Set Password' )
    OOOo00oo0oO . doModal ( )
   if ( OOOo00oo0oO . isConfirmed ( ) ) :
    i1I1i = OOOo00oo0oO . getText ( )
    iIiiiI . setSetting ( 'Conspiracy Password' , i1I1i )
   else : quit ( )
   if 40 - 40: I1IiiI . iIii1I11I1II1 / I1IiiI / i11iIiiIii
 if 'con>yes</con' in oOOoOo00o :
  if i1 <> '' :
   i1IIIiiII1 = xbmcgui . Dialog ( )
   OOOOoOoo0O0O0 = i1IIIiiII1 . yesno ( 'Conspiracy Content' , 'Please enter the password you set' , 'to continue' , '' , 'Cancel' , 'OK' )
   if OOOOoOoo0O0O0 == 1 :
    OOOo00oo0oO = xbmc . Keyboard ( '' , 'Enter Password' )
    OOOo00oo0oO . doModal ( )
   if ( OOOo00oo0oO . isConfirmed ( ) ) :
    i1I1i = OOOo00oo0oO . getText ( )
   if i1I1i <> i1 :
    quit ( )
  else : quit ( )
  if 75 - 75: IIIII + o0oOOo0O0Ooo
 print 'Now reading data'
 iI1iI1I1i1I = re . compile ( '<item>(.+?)</item>' ) . findall ( oOOoOo00o )
 if 84 - 84: iIIIiI11 . i11iIiiIii . iIIIiI11 * I1ii11iIi11i - IIIII
 for iIi11Ii1 in iI1iI1I1i1I :
  print iIi11Ii1
  try :
   if '<channel>' in iIi11Ii1 :
    name = re . compile ( '<title>(.+?)</title>' ) . findall ( iIi11Ii1 ) [ 0 ]
    iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( iIi11Ii1 ) [ 0 ]
    fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( iIi11Ii1 ) [ 0 ]
    url = re . compile ( '<channel>(.+?)</channel>' ) . findall ( iIi11Ii1 ) [ 0 ]
    Oo0OO ( name , url , 6 , iconimage , fanart )
   if '<image>' in iIi11Ii1 :
    if 42 - 42: i11iIiiIii
    name = re . compile ( '<title>(.+?)</title>' ) . findall ( iIi11Ii1 ) [ 0 ]
    iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( iIi11Ii1 ) [ 0 ]
    fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( iIi11Ii1 ) [ 0 ]
    url = re . compile ( '<image>(.+?)</image>' ) . findall ( iIi11Ii1 ) [ 0 ]
    Oo0OO ( name , iconimage , 9 , iconimage , fanart )
   if '<sportsdevil>' in iIi11Ii1 :
    if 33 - 33: i111IiI - O0 * i1IIi * o0oOOo0O0Ooo - Oo0Ooo
    print '--------- sportsdevil add ---------'
    IIIIii = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( iIi11Ii1 )
    if len ( IIIIii ) == 1 :
     name = re . compile ( '<title>(.+?)</title>' ) . findall ( iIi11Ii1 ) [ 0 ]
     iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( iIi11Ii1 ) [ 0 ]
     url = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( iIi11Ii1 ) [ 0 ]
     O0o0 = re . compile ( '<referer>(.+?)</referer>' ) . findall ( iIi11Ii1 ) [ 0 ]
     OO00Oo = O0o0
     O0OOO0OOoO0O = "/"
     if not OO00Oo . endswith ( O0OOO0OOoO0O ) :
      O00Oo000ooO0 = OO00Oo + "/"
     else :
      O00Oo000ooO0 = OO00Oo
     oOOoOo00o = 'plugin://plugin.video.SportsDevil/?mode=10&amp;item=catcher%3dstreams%26url=' + url
     url = oOOoOo00o + '%26referer=' + O00Oo000ooO0
     OoO0O00IIiII ( name , url , 4 , iconimage , fanart )
    elif len ( IIIIii ) > 1 :
     name = re . compile ( '<title>(.+?)</title>' ) . findall ( iIi11Ii1 ) [ 0 ]
     iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( iIi11Ii1 ) [ 0 ]
     fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( iIi11Ii1 ) [ 0 ]
     OoO0O00IIiII ( name , OOoO , 8 , iconimage , fanart )
     if 32 - 32: OoooooooOO / iIii1I11I1II1 - o0oOOo0O0Ooo
   elif '<folder>' in iIi11Ii1 :
    Oo0oOOo = re . compile ( '<title>(.+?)</title>.+?folder>(.+?)</folder>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>' ) . findall ( iIi11Ii1 )
    for name , url , iconimage , fanart in Oo0oOOo :
     if url in I1i1I :
      Oo0OO ( name , url , 1 , iconimage , fanart )
     else :
      Oo0OO ( name , url , 10 , iconimage , fanart )
   else :
    IIIIii = re . compile ( '<link>(.+?)</link>' ) . findall ( iIi11Ii1 )
    if len ( IIIIii ) == 1 :
     Oo0oOOo = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>' ) . findall ( iIi11Ii1 )
     oO0o0OOOO = len ( iI1iI1I1i1I )
     for name , url , iconimage , fanart in Oo0oOOo :
      if 'youtube.com/playlist' in url :
       Oo0OO ( name , url , 2 , iconimage , fanart )
      else :
       O0O0OoOO0 ( name , url , 2 , iconimage , fanart )
    elif len ( IIIIii ) > 1 :
     if 91 - 91: i111IiI % i1IIi % iIii1I11I1II1
     print ( '---------------- simple file checking ----------------------------' )
     name = re . compile ( '<title>(.+?)</title>' ) . findall ( iIi11Ii1 ) [ 0 ]
     iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( iIi11Ii1 ) [ 0 ]
     fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( iIi11Ii1 ) [ 0 ]
     O0O0OoOO0 ( name , OOoO , 3 , iconimage , fanart )
  except : pass
  iiiI1I11i1 ( oOOoOo00o )
  if 20 - 20: O0o % I1 / I1 + I1
def III1IiiI ( name , url , iconimage , fanart ) :
 if 31 - 31: o0oOOo0O0Ooo . I1IiiI
 OOoO = url
 oOOoOo00o = ii11IIII11I ( url )
 if 'XXX>yes</XXX' in oOOoOo00o :
  if o0oOoO00o == '' :
   i1IIIiiII1 = xbmcgui . Dialog ( )
   OOOOoOoo0O0O0 = i1IIIiiII1 . yesno ( 'Adult Content' , 'You have opted to show adult content' , '' , 'Please set a password to prevent accidental access' , 'Cancel' , 'OK' )
   if OOOOoOoo0O0O0 == 1 :
    OOOo00oo0oO = xbmc . Keyboard ( '' , 'Set Password' )
    OOOo00oo0oO . doModal ( )
   if ( OOOo00oo0oO . isConfirmed ( ) ) :
    IIiIi1iI = OOOo00oo0oO . getText ( )
    iIiiiI . setSetting ( 'password' , IIiIi1iI )
   else : quit ( )
   if 81 - 81: OoOoOO00 / O0 . iIIIiI11 . I1IiiI
 if 'XXX>yes</XXX' in oOOoOo00o :
  if o0oOoO00o <> '' :
   i1IIIiiII1 = xbmcgui . Dialog ( )
   OOOOoOoo0O0O0 = i1IIIiiII1 . yesno ( 'Adult Content' , 'Please enter the password you set' , 'to continue' , '' , 'Cancel' , 'OK' )
   if OOOOoOoo0O0O0 == 1 :
    OOOo00oo0oO = xbmc . Keyboard ( '' , 'Enter Password' )
    OOOo00oo0oO . doModal ( )
   if ( OOOo00oo0oO . isConfirmed ( ) ) :
    IIiIi1iI = OOOo00oo0oO . getText ( )
   if IIiIi1iI <> o0oOoO00o :
    quit ( )
  else : quit ( )
  if 72 - 72: i1IIi / OoO0O00 + OoooooooOO - Oo0Ooo
 if 'con>yes</con' in oOOoOo00o :
  if i1 == '' :
   i1IIIiiII1 = xbmcgui . Dialog ( )
   OOOOoOoo0O0O0 = i1IIIiiII1 . yesno ( 'Conspiracy Content' , 'You have opted to show Conspiracy content' , '' , 'Due to the Nature of Content ,Please set a password to prevent accidental access' , 'Cancel' , 'OK' )
   if OOOOoOoo0O0O0 == 1 :
    OOOo00oo0oO = xbmc . Keyboard ( '' , 'Set Password' )
    OOOo00oo0oO . doModal ( )
   if ( OOOo00oo0oO . isConfirmed ( ) ) :
    i1I1i = OOOo00oo0oO . getText ( )
    iIiiiI . setSetting ( 'Conspiracy Password' , i1I1i )
   else : quit ( )
   if 29 - 29: I1ii11iIi11i + iiiii11iII1 % O0
 if 'con>yes</con' in oOOoOo00o :
  if i1 <> '' :
   i1IIIiiII1 = xbmcgui . Dialog ( )
   OOOOoOoo0O0O0 = i1IIIiiII1 . yesno ( 'Conspiracy Content' , 'Please enter the password you set' , 'to continue' , '' , 'Cancel' , 'OK' )
   if OOOOoOoo0O0O0 == 1 :
    OOOo00oo0oO = xbmc . Keyboard ( '' , 'Enter Password' )
    OOOo00oo0oO . doModal ( )
   if ( OOOo00oo0oO . isConfirmed ( ) ) :
    i1I1i = OOOo00oo0oO . getText ( )
   if i1I1i <> i1 :
    quit ( )
  else : quit ( )
  if 10 - 10: IIIII / iII111ii - I1IiiI * iIii1I11I1II1 - I1IiiI
 iI1iI1I1i1I = re . compile ( '<item>(.+?)</item>' ) . findall ( oOOoOo00o )
 for iIi11Ii1 in iI1iI1I1i1I :
  try :
   if '<channel>' in iIi11Ii1 :
    name = re . compile ( '<title>(.+?)</title>' ) . findall ( iIi11Ii1 ) [ 0 ]
    iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( iIi11Ii1 ) [ 0 ]
    fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( iIi11Ii1 ) [ 0 ]
    url = re . compile ( '<channel>(.+?)</channel>' ) . findall ( iIi11Ii1 ) [ 0 ]
    Oo0OO ( name , url , 6 , iconimage , fanart )
   if '<image>' in iIi11Ii1 :
    name = re . compile ( '<title>(.+?)</title>' ) . findall ( iIi11Ii1 ) [ 0 ]
    iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( iIi11Ii1 ) [ 0 ]
    fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( iIi11Ii1 ) [ 0 ]
    url = re . compile ( '<image>(.+?)</image>' ) . findall ( iIi11Ii1 ) [ 0 ]
    Oo0OO ( name , iconimage , 9 , iconimage , fanart )
   if '<sportsdevil>' in iIi11Ii1 :
    IIIIii = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( iIi11Ii1 )
    if len ( IIIIii ) == 1 :
     name = re . compile ( '<title>(.+?)</title>' ) . findall ( iIi11Ii1 ) [ 0 ]
     iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( iIi11Ii1 ) [ 0 ]
     url = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( iIi11Ii1 ) [ 0 ]
     O0o0 = re . compile ( '<referer>(.+?)</referer>' ) . findall ( iIi11Ii1 ) [ 0 ]
     OO00Oo = O0o0
     O0OOO0OOoO0O = "/"
     if not OO00Oo . endswith ( O0OOO0OOoO0O ) :
      O00Oo000ooO0 = OO00Oo + "/"
     else :
      O00Oo000ooO0 = OO00Oo
     oOOoOo00o = 'plugin://plugin.video.SportsDevil/?mode=10&amp;item=catcher%3dstreams%26url=' + url
     url = oOOoOo00o + '%26referer=' + O00Oo000ooO0
     OoO0O00IIiII ( name , url , 4 , iconimage , fanart )
    elif len ( IIIIii ) > 1 :
     name = re . compile ( '<title>(.+?)</title>' ) . findall ( iIi11Ii1 ) [ 0 ]
     iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( iIi11Ii1 ) [ 0 ]
     fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( iIi11Ii1 ) [ 0 ]
     OoO0O00IIiII ( name , OOoO , 8 , iconimage , fanart )
     if 97 - 97: I1ii11iIi11i + I1IiiI * I1 + O0o % i111IiI
   elif '<folder>' in iIi11Ii1 :
    Oo0oOOo = re . compile ( '<title>(.+?)</title>.+?folder>(.+?)</folder>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>' ) . findall ( iIi11Ii1 )
    for name , url , iconimage , fanart in Oo0oOOo :
     if 74 - 74: iiiii11iII1 - Oo0Ooo + OoooooooOO + iII111ii / OoOoOO00
     if url in I1i1I :
      Oo0OO ( name , url , 1 , iconimage , fanart )
     else :
      Oo0OO ( name , url , 10 , iconimage , fanart )
   else :
    IIIIii = re . compile ( '<link>(.+?)</link>' ) . findall ( iIi11Ii1 )
    if len ( IIIIii ) == 1 :
     Oo0oOOo = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>' ) . findall ( iIi11Ii1 )
     oO0o0OOOO = len ( iI1iI1I1i1I )
     for name , url , iconimage , fanart in Oo0oOOo :
      if 'youtube.com/playlist' in url :
       Oo0OO ( name , url , 2 , iconimage , fanart )
      else :
       O0O0OoOO0 ( name , url , 2 , iconimage , fanart )
    elif len ( IIIIii ) > 1 :
     name = re . compile ( '<title>(.+?)</title>' ) . findall ( iIi11Ii1 ) [ 0 ]
     iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( iIi11Ii1 ) [ 0 ]
     fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( iIi11Ii1 ) [ 0 ]
     O0O0OoOO0 ( name , OOoO , 3 , iconimage , fanart )
  except : pass
  iiiI1I11i1 ( oOOoOo00o )
  if 23 - 23: O0
def o00oO0oOo00 ( url ) :
 if 81 - 81: OoO0O00
 IIi1 = i11 + url
 oOOoOo00o = ii11IIII11I ( IIi1 )
 I1I1I = "<video>(.*?)</video>"
 OoOO000 = re . findall ( I1I1I , oOOoOo00o , re . DOTALL )
 if 14 - 14: iIIIiI11 - I1ii11iIi11i
 Ii1i1iI1iIIi = [ ]
 for I1Ii in OoOO000 :
  iIi11Ii1 = { }
  iIi11Ii1 [ "name" ] = O0oo00o0O ( I1Ii , "<name>([^<]+)</name>" )
  iIi11Ii1 [ "url" ] = base64 . b64decode ( b"cGx1Z2luOi8vcGx1Z2luLnZpZGVvLnlvdXR1YmUvcGxheS8/dmlkZW9faWQ9" ) + O0oo00o0O ( I1Ii , "<id>([^<]+)</id>" )
  iIi11Ii1 [ "author" ] = O0oo00o0O ( I1Ii , "<author>([^<]+)</author>" )
  iIi11Ii1 [ "iconimage" ] = O0oo00o0O ( I1Ii , "<iconimage>([^<]+)</iconimage>" )
  iIi11Ii1 [ "date" ] = O0oo00o0O ( I1Ii , "<date>([^<]+)</date>" )
  if 1 - 1: II111iiii
  O0O0OoOO0 ( '[COLOR white]' + iIi11Ii1 [ "name" ] + ' - on ' + iIi11Ii1 [ "date" ] + '[/COLOR]' , iIi11Ii1 [ "url" ] , 7 , iIi11Ii1 [ "iconimage" ] , Iii1ii1II11i )
  if 84 - 84: o0oOOo0O0Ooo % II111iiii . i11iIiiIii / OoO0O00
  if 80 - 80: iII111ii . i11iIiiIii - o0oOOo0O0Ooo
def iIiIIi1 ( ) :
 OOOo00oo0oO = xbmc . Keyboard ( '' , '[COLOR lime]S[/COLOR][COLOR white]earch[/COLOR] [B][COLOR lime]S[/COLOR][COLOR white]tream[/COLOR][/B] [B][COLOR lime]A[/COLOR][COLOR white]rmy[/COLOR][/B]' )
 OOOo00oo0oO . doModal ( )
 if ( OOOo00oo0oO . isConfirmed ( ) ) :
  I1IIII1i = OOOo00oo0oO . getText ( )
  I1IIII1i = I1IIII1i . upper ( )
 else : quit ( )
 oOOoOo00o = ii11IIII11I ( I11 )
 I1I11i = re . compile ( '<link>(.+?)</link>' ) . findall ( oOOoOo00o )
 for OOOooOooo00O0 in I1I11i :
  OOoO = OOOooOooo00O0
  oOOoOo00o = ii11IIII11I ( OOOooOooo00O0 )
  Ii1I1I1i1Ii = re . compile ( '<item>(.+?)</item>' ) . findall ( oOOoOo00o )
  for iIi11Ii1 in Ii1I1I1i1Ii :
   iI1iI1I1i1I = re . compile ( '<title>(.+?)</title>' ) . findall ( iIi11Ii1 )
   for i1Oo0oO00o in iI1iI1I1i1I :
    i1Oo0oO00o = i1Oo0oO00o . upper ( )
    if I1IIII1i in i1Oo0oO00o :
     try :
      if '<sportsdevil>' in iIi11Ii1 :
       Ii11iII1 = re . compile ( '<title>(.+?)</title>' ) . findall ( iIi11Ii1 ) [ 0 ]
       Oo0O0O0ooO0O = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( iIi11Ii1 ) [ 0 ]
       OOOooOooo00O0 = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( iIi11Ii1 ) [ 0 ]
       O0o0 = re . compile ( '<referer>(.+?)</referer>' ) . findall ( iIi11Ii1 ) [ 0 ]
       oOOoOo00o = 'plugin://plugin.video.SportsDevil/?mode=10&amp;item=catcher%3dstreams%26url=' + OOOooOooo00O0
       OOOooOooo00O0 = oOOoOo00o + '%26referer=' + O0o0
       if 'tp' in OOOooOooo00O0 :
        O0O0OoOO0 ( Ii11iII1 , OOOooOooo00O0 , 4 , Oo0O0O0ooO0O , iI111iI )
      elif '<folder>' in iIi11Ii1 :
       Oo0oOOo = re . compile ( '<title>(.+?)</title>.+?folder>(.+?)</folder>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>' ) . findall ( iIi11Ii1 )
       for Ii11iII1 , OOOooOooo00O0 , Oo0O0O0ooO0O , Iii1ii1II11i in Oo0oOOo :
        if 'tp' in OOOooOooo00O0 :
         Oo0OO ( Ii11iII1 , OOOooOooo00O0 , 1 , Oo0O0O0ooO0O , iI111iI )
      else :
       IIIIii = re . compile ( '<link>(.+?)</link>' ) . findall ( iIi11Ii1 )
       if len ( IIIIii ) == 1 :
        Oo0oOOo = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>' ) . findall ( iIi11Ii1 )
        oO0o0OOOO = len ( iI1iI1I1i1I )
        for Ii11iII1 , OOOooOooo00O0 , Oo0O0O0ooO0O , Iii1ii1II11i in Oo0oOOo :
         if 'youtube.com/playlist' in OOOooOooo00O0 :
          Oo0OO ( Ii11iII1 , OOOooOooo00O0 , 2 , Oo0O0O0ooO0O , iI111iI )
         else :
          if 'tp' in OOOooOooo00O0 :
           O0O0OoOO0 ( Ii11iII1 , OOOooOooo00O0 , 2 , Oo0O0O0ooO0O , iI111iI )
       elif len ( IIIIii ) > 1 :
        Ii11iII1 = re . compile ( '<title>(.+?)</title>' ) . findall ( iIi11Ii1 ) [ 0 ]
        Oo0O0O0ooO0O = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( iIi11Ii1 ) [ 0 ]
        O0O0OoOO0 ( Ii11iII1 , OOoO , 3 , Oo0O0O0ooO0O , iI111iI )
     except : pass
     if 13 - 13: IIIII * Oo0Ooo * oOo0Oo
     if 50 - 50: o0oOOo0O0Ooo * IIIII % O0
def OooOoOO0 ( name , url , iconimage ) :
 iI1i11iII111 = [ ]
 Iii1IIII11I = [ ]
 OOOoo0OO = [ ]
 oOOoOo00o = o0OOoo0OO0OOO ( url )
 oO0o0 = re . compile ( '<title>' + re . escape ( name ) + '</title>(.+?)</item>' , re . DOTALL ) . findall ( oOOoOo00o ) [ 0 ]
 iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( oO0o0 ) [ 0 ]
 IIIIii = re . compile ( '<link>(.+?)</link>' ) . findall ( oO0o0 )
 iI1Ii11iIiI1 = 1
 for OO0Oooo0oOO0O in IIIIii :
  o00O0 = OO0Oooo0oOO0O
  if '(' in OO0Oooo0oOO0O :
   OO0Oooo0oOO0O = OO0Oooo0oOO0O . split ( '(' ) [ 0 ]
   oOO0O00Oo0O0o = str ( o00O0 . split ( '(' ) [ 1 ] . replace ( ')' , '' ) )
   iI1i11iII111 . append ( OO0Oooo0oOO0O )
   Iii1IIII11I . append ( oOO0O00Oo0O0o )
  else :
   iI1i11iII111 . append ( OO0Oooo0oOO0O )
   Iii1IIII11I . append ( 'Link ' + str ( iI1Ii11iIiI1 ) )
  iI1Ii11iIiI1 = iI1Ii11iIiI1 + 1
 name = '[COLOR lime]' + name + '[/COLOR]'
 i1IIIiiII1 = xbmcgui . Dialog ( )
 ii1 = i1IIIiiII1 . select ( name , Iii1IIII11I )
 if ii1 < 0 :
  quit ( )
 else :
  url = iI1i11iII111 [ ii1 ]
  print url
  if urlresolver . HostedMediaFile ( url ) . valid_url ( ) : I1iIIiiIIi1i = urlresolver . HostedMediaFile ( url ) . resolve ( )
  elif liveresolver . isValid ( url ) == True : I1iIIiiIIi1i = liveresolver . resolve ( url )
  else : I1iIIiiIIi1i = url
  O0O0ooOOO = xbmcgui . ListItem ( name , iconImage = 'DefaultVideo.png' , thumbnailImage = iconimage )
  O0O0ooOOO . setPath ( I1iIIiiIIi1i )
  xbmcplugin . setResolvedUrl ( int ( sys . argv [ 1 ] ) , True , O0O0ooOOO )
  if 77 - 77: OoOoOO00 - II111iiii - oOo0Oo
def IiiiIIiIi1 ( name , url , iconimage ) :
 if 74 - 74: iIii1I11I1II1 * I1ii11iIi11i + OoOoOO00 / i1IIi / II111iiii . Oo0Ooo
 oooOo0OOOoo0 = 'plugin://plugin.video.SportsDevil/?mode=10&amp;item=catcher%3dstreams%26url='
 iI1i11iII111 = [ ]
 Iii1IIII11I = [ ]
 OOOoo0OO = [ ]
 OOoOOO0O000 = [ ]
 oOOoOo00o = ii11IIII11I ( url )
 oO0o0 = re . compile ( '<title>' + re . escape ( name ) + '</title>(.+?)</item>' , re . DOTALL ) . findall ( oOOoOo00o ) [ 0 ]
 IIIIii = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( oO0o0 )
 iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( oO0o0 ) [ 0 ]
 iI1Ii11iIiI1 = 1
 if 37 - 37: OoooooooOO - O0 - o0oOOo0O0Ooo
 for OO0Oooo0oOO0O in IIIIii :
  o00O0 = OO0Oooo0oOO0O
  if '(' in OO0Oooo0oOO0O :
   OO0Oooo0oOO0O = OO0Oooo0oOO0O . split ( '(' ) [ 0 ]
   oOO0O00Oo0O0o = str ( o00O0 . split ( '(' ) [ 1 ] . replace ( ')' , '' ) )
   iI1i11iII111 . append ( OO0Oooo0oOO0O )
   Iii1IIII11I . append ( oOO0O00Oo0O0o )
   OOoOOO0O000 . append ( 'Stream ' + str ( iI1Ii11iIiI1 ) )
  else :
   iI1i11iII111 . append ( OO0Oooo0oOO0O )
   Iii1IIII11I . append ( 'Link ' + str ( iI1Ii11iIiI1 ) )
  iI1Ii11iIiI1 = iI1Ii11iIiI1 + 1
 name = '[COLOR lime]' + name + '[/COLOR]'
 i1IIIiiII1 = xbmcgui . Dialog ( )
 ii1 = i1IIIiiII1 . select ( name , Iii1IIII11I )
 if ii1 < 0 :
  quit ( )
 else :
  OO00Oo = Iii1IIII11I [ ii1 ]
  O0OOO0OOoO0O = "/"
  if not OO00Oo . endswith ( O0OOO0OOoO0O ) :
   O00Oo000ooO0 = OO00Oo + "/"
  else :
   O00Oo000ooO0 = OO00Oo
  url = oooOo0OOOoo0 + iI1i11iII111 [ ii1 ] + "%26referer=" + O00Oo000ooO0
  print url
  if 77 - 77: O0o * iIii1I11I1II1
  xbmc . Player ( ) . play ( url )
  if 98 - 98: I1IiiI % I1 * OoooooooOO
def Oo ( name , url , iconimage ) :
 iIIiIi1 = True
 O0O0ooOOO = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage ) ; O0O0ooOOO . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
 iIIiIi1 = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = url , listitem = O0O0ooOOO )
 xbmc . Player ( ) . play ( url , O0O0ooOOO , False )
 if 74 - 74: i111IiI + o0oOOo0O0Ooo
def oO00O000oO0 ( name , url , iconimage ) :
 if 79 - 79: IIIII - OoooooooOO - iiiii11iII1 - iIii1I11I1II1 * O0o
 if not 'http' in url : url = 'http://' + url
 if 'youtube.com/playlist' in url :
  I1IIII1i = url . split ( 'list=' ) [ 1 ]
  Iii = iiIIIII1i1iI + I1IIII1i + o0oO0
  I1111i = urllib2 . Request ( Iii )
  I1111i . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' )
  i11Iiii = urllib2 . urlopen ( I1111i )
  oOOoOo00o = i11Iiii . read ( )
  i11Iiii . close ( )
  oOOoOo00o = oOOoOo00o . replace ( '\r' , '' ) . replace ( '\n' , '' ) . replace ( '  ' , '' )
  iI1iI1I1i1I = re . compile ( '"title": "(.+?)".+?"videoId": "(.+?)"' , re . DOTALL ) . findall ( oOOoOo00o )
  try :
   iIIii = re . compile ( '"nextPageToken": "(.+?)"' ) . findall ( oOOoOo00o ) [ 0 ]
   Iii = oo00 + iIIii + o00 + I1IIII1i + Oo0oO0ooo
   Oo0OO ( 'Next Page >>' , Iii , 2 , i1i1II , Iii1ii1II11i )
  except : pass
  if 92 - 92: I1 + iiiii11iII1 % O0o
  if 62 - 62: I1ii11iIi11i / i1IIi
  if 98 - 98: i1IIi / IIIII
  if 32 - 32: I1 * iIii1I11I1II1 / O0o
  for name , I11ii1IIiIi in iI1iI1I1i1I :
   url = 'https://www.youtube.com/watch?v=' + I11ii1IIiIi
   iconimage = 'https://i.ytimg.com/vi/' + I11ii1IIiIi + '/hqdefault.jpg'
   if not 'Private video' in name :
    if not 'Deleted video' in name :
     O0O0OoOO0 ( name , url , 2 , iconimage , Iii1ii1II11i )
     if 54 - 54: iIii1I11I1II1 % I1ii11iIi11i - O0o / iiiii11iII1 - OoO0O00 . IIIII
 if 'https://www.googleapis.com/youtube/v3' in url :
  I1IIII1i = re . compile ( 'playlistId=(.+?)&maxResults' ) . findall ( url ) [ 0 ]
  I1111i = urllib2 . Request ( url )
  I1111i . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' )
  i11Iiii = urllib2 . urlopen ( I1111i )
  oOOoOo00o = i11Iiii . read ( )
  i11Iiii . close ( )
  oOOoOo00o = oOOoOo00o . replace ( '\r' , '' ) . replace ( '\n' , '' ) . replace ( '  ' , '' )
  iI1iI1I1i1I = re . compile ( '"title": "(.+?)".+?"videoId": "(.+?)"' , re . DOTALL ) . findall ( oOOoOo00o )
  try :
   iIIii = re . compile ( '"nextPageToken": "(.+?)"' ) . findall ( oOOoOo00o ) [ 0 ]
   Iii = oo00 + iIIii + o00 + I1IIII1i + Oo0oO0ooo
   Oo0OO ( 'Next Page >>' , Iii , 2 , i1i1II , Iii1ii1II11i )
  except : pass
  if 11 - 11: I1ii11iIi11i . OoO0O00 * iIIIiI11 * OoooooooOO + oOo0Oo
  if 33 - 33: O0 * o0oOOo0O0Ooo - iII111ii % iII111ii
  if 18 - 18: iII111ii / Oo0Ooo * iII111ii + iII111ii * i11iIiiIii * I1ii11iIi11i
  for name , I11ii1IIiIi in iI1iI1I1i1I :
   url = 'https://www.youtube.com/watch?v=' + I11ii1IIiIi
   iconimage = 'https://i.ytimg.com/vi/' + I11ii1IIiIi + '/hqdefault.jpg'
   if not 'Private video' in name :
    if not 'Deleted video' in name :
     O0O0OoOO0 ( name , url , 2 , iconimage , Iii1ii1II11i )
     if 11 - 11: oOo0Oo / OoOoOO00 - iIIIiI11 * OoooooooOO + OoooooooOO . OoOoOO00
     if 26 - 26: I1 % I1ii11iIi11i
     if 76 - 76: iIIIiI11 * i111IiI
 if "plugin://" in url :
  url = "PlayMedia(" + url + ")"
  xbmc . executebuiltin ( url )
  quit ( )
  if 52 - 52: O0o
 if urlresolver . HostedMediaFile ( url ) . valid_url ( ) : I1iIIiiIIi1i = urlresolver . HostedMediaFile ( url ) . resolve ( )
 elif liveresolver . isValid ( url ) == True : I1iIIiiIIi1i = liveresolver . resolve ( url )
 else : I1iIIiiIIi1i = url
 O0O0ooOOO = xbmcgui . ListItem ( name , iconImage = 'DefaultVideo.png' , thumbnailImage = iconimage )
 O0O0ooOOO . setPath ( I1iIIiiIIi1i )
 xbmcplugin . setResolvedUrl ( int ( sys . argv [ 1 ] ) , True , O0O0ooOOO )
 if 19 - 19: I1IiiI
def i11i ( url ) :
 if 73 - 73: O0o
 xbmc . Player ( ) . play ( url )
 if 70 - 70: iIii1I11I1II1
def ii11IIII11I ( url ) :
 try :
  I1111i = urllib2 . Request ( url )
  I1111i . add_header ( 'User-Agent' , 'obsession' )
  i11Iiii = urllib2 . urlopen ( I1111i )
  oOOoOo00o = i11Iiii . read ( )
  i11Iiii . close ( )
  oOOoOo00o = oOOoOo00o . replace ( '\n' , '' ) . replace ( '\r' , '' ) . replace ( '<fanart></fanart>' , '<fanart>x</fanart>' ) . replace ( '<thumbnail></thumbnail>' , '<thumbnail>x</thumbnail>' ) . replace ( '<utube>' , '<link>https://www.youtube.com/watch?v=' ) . replace ( '</utube>' , '</link>' )
  print oOOoOo00o
  return oOOoOo00o
 except : quit ( )
 if 31 - 31: iIIIiI11 - I1IiiI % iIii1I11I1II1
def o0OOoo0OO0OOO ( url ) :
 if 92 - 92: i1IIi - iIii1I11I1II1
 print "--------- open_encrypted_url --------"
 try :
  I1111i = urllib2 . Request ( url )
  I1111i . add_header ( 'User-Agent' , 'obsession' )
  i11Iiii = urllib2 . urlopen ( I1111i )
  oOOoOo00o = i11Iiii . read ( )
  print "--------- link --------" , oOOoOo00o
  IIIIIIii1 = oOOO00o ( Ii1iIIIi1ii , oOOoOo00o )
  print "--------- decoded --------" , IIIIIIii1
  i11Iiii . close ( )
  IIIIIIii1 = IIIIIIii1 . replace ( '\n' , '' ) . replace ( '\r' , '' ) . replace ( '<fanart></fanart>' , '<fanart>x</fanart>' ) . replace ( '<thumbnail></thumbnail>' , '<thumbnail>x</thumbnail>' ) . replace ( '<utube>' , '<link>https://www.youtube.com/watch?v=' ) . replace ( '</utube>' , '</link>' )
  print IIIIIIii1
  return IIIIIIii1
 except : quit ( )
 if 88 - 88: OoO0O00
 if 71 - 71: I1ii11iIi11i
def O0ooo0O0oo0 ( url ) :
 I1111i = urllib2 . Request ( url )
 I1111i . add_header ( 'User-Agent' , 'obsession' )
 i11Iiii = urllib2 . urlopen ( I1111i )
 oOOoOo00o = i11Iiii . read ( )
 i11Iiii . close ( )
 print oOOoOo00o
 return oOOoOo00o
 if 7 - 7: I1ii11iIi11i - I1IiiI . iIii1I11I1II1 - i1IIi
def o0OOOoO0 ( ) :
 o0OoOo00o0o = [ ]
 I1II1I11I1I = sys . argv [ 2 ]
 if len ( I1II1I11I1I ) >= 2 :
  OoOO0o = sys . argv [ 2 ]
  i1II1 = OoOO0o . replace ( '?' , '' )
  if ( OoOO0o [ len ( OoOO0o ) - 1 ] == '/' ) :
   OoOO0o = OoOO0o [ 0 : len ( OoOO0o ) - 2 ]
  i11i1 = i1II1 . split ( '&' )
  o0OoOo00o0o = { }
  for iI1Ii11iIiI1 in range ( len ( i11i1 ) ) :
   IiiiiI1i1Iii = { }
   IiiiiI1i1Iii = i11i1 [ iI1Ii11iIiI1 ] . split ( '=' )
   if ( len ( IiiiiI1i1Iii ) ) == 2 :
    o0OoOo00o0o [ IiiiiI1i1Iii [ 0 ] ] = IiiiiI1i1Iii [ 1 ]
 return o0OoOo00o0o
 if 87 - 87: o0oOOo0O0Ooo
 if 29 - 29: I1IiiI % O0o - I1IiiI / O0o . i1IIi
def i11III1111iIi ( name , url , mode , iconimage , itemcount , isFolder = False ) :
 I1i111I = name . partition ( '(' )
 Ooo = ""
 Oo0oo0O0o00O = ""
 if len ( I1i111I ) > 0 :
  Ooo = I1i111I [ 0 ]
  Oo0oo0O0o00O = I1i111I [ 2 ] . partition ( ')' )
 if len ( Oo0oo0O0o00O ) > 0 :
  Oo0oo0O0o00O = Oo0oo0O0o00O [ 0 ]
 I1i11 = metahandlers . MetaData ( )
 IiIi1I1 = I1i11 . get_meta ( 'movie' , name = Ooo , year = Oo0oo0O0o00O )
 IiIIi1 = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 iIIiIi1 = True
 O0O0ooOOO = xbmcgui . ListItem ( name , iconImage = IiIi1I1 [ 'cover_url' ] , thumbnailImage = IiIi1I1 [ 'cover_url' ] )
 O0O0ooOOO . setInfo ( type = "Video" , infoLabels = IiIi1I1 )
 IIIIiii1IIii = [ ]
 IIIIiii1IIii . append ( ( 'Movie Information' , 'XBMC.Action(Info)' ) )
 O0O0ooOOO . addContextMenuItems ( IIIIiii1IIii , replaceItems = False )
 if not IiIi1I1 [ 'backdrop_url' ] == '' : O0O0ooOOO . setProperty ( 'fanart_image' , IiIi1I1 [ 'backdrop_url' ] )
 else : O0O0ooOOO . setProperty ( 'fanart_image' , Iii1ii1II11i )
 iIIiIi1 = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = IiIIi1 , listitem = O0O0ooOOO , isFolder = isFolder , totalItems = itemcount )
 return iIIiIi1
 if 38 - 38: O0o + II111iiii % oOo0Oo % OoOoOO00 - I1 / OoooooooOO
def Oo0OO ( name , url , mode , iconimage , fanart , description = '' ) :
 IiIIi1 = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&fanart=" + urllib . quote_plus ( fanart )
 iIIiIi1 = True
 O0O0ooOOO = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 O0O0ooOOO . setInfo ( type = "Video" , infoLabels = { "Title" : name , 'plot' : description } )
 O0O0ooOOO . setProperty ( 'fanart_image' , fanart )
 if 'plugin://' in url : IiIIi1 = url
 iIIiIi1 = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = IiIIi1 , listitem = O0O0ooOOO , isFolder = True )
 return iIIiIi1
 if 73 - 73: o0oOOo0O0Ooo * O0 - i11iIiiIii
 if 85 - 85: I1 % i111IiI + IIIII / o0oOOo0O0Ooo . iiiii11iII1 + O0o
 if 62 - 62: i11iIiiIii + i11iIiiIii - o0oOOo0O0Ooo
def O0O0OoOO0 ( name , url , mode , iconimage , fanart , description = '' ) :
 if 28 - 28: i111IiI . i111IiI % iIii1I11I1II1 * iIii1I11I1II1 . o0oOOo0O0Ooo / i111IiI
 if '.ts' in url :
  url = 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;name=' + name + '&amp;url=' + url
 IiIIi1 = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&fanart=" + urllib . quote_plus ( fanart )
 iIIiIi1 = True
 O0O0ooOOO = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 O0O0ooOOO . setProperty ( 'fanart_image' , fanart )
 if 'plugin://' not in url :
  O0O0ooOOO . setProperty ( "IsPlayable" , "true" )
 if 'plugin://' in url : IiIIi1 = url
 iIIiIi1 = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = IiIIi1 , listitem = O0O0ooOOO , isFolder = False )
 return iIIiIi1
 if 27 - 27: OoO0O00 + oOo0Oo - i1IIi
def OoO0O00IIiII ( name , url , mode , iconimage , fanart , description = '' ) :
 if 69 - 69: iIIIiI11 - O0 % I1ii11iIi11i + i11iIiiIii . OoOoOO00 / OoO0O00
 if '.ts' in url :
  url = 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;name=' + name + '&amp;url=' + url
 IiIIi1 = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&fanart=" + urllib . quote_plus ( fanart )
 iIIiIi1 = True
 O0O0ooOOO = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 O0O0ooOOO . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
 O0O0ooOOO . setProperty ( "Fanart_Image" , fanart )
 if 'plugin://' not in url :
  O0O0ooOOO . setProperty ( "IsPlayable" , "true" )
 if 'plugin://' in url : IiIIi1 = url
 iIIiIi1 = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = IiIIi1 , listitem = O0O0ooOOO , isFolder = False )
 return iIIiIi1
 if 79 - 79: O0 * i11iIiiIii - iIIIiI11 / iIIIiI11
def i1O0 ( url ) :
 if 32 - 32: I1 - Oo0Ooo % OoooooooOO . i111IiI / iIIIiI11 + I1IiiI
 o0O0oO0O00O0o = "ShowPicture(" + url + ')'
 xbmc . executebuiltin ( o0O0oO0O00O0o )
 sys . exit ( 1 )
 if 28 - 28: Oo0Ooo + OoO0O00 * O0o % iiiii11iII1 . IIIII % O0
def O0oo00o0O ( text , pattern ) :
 if 16 - 16: IIIII - iIii1I11I1II1 / I1IiiI . II111iiii + iIii1I11I1II1
 iIiIiIiI = ""
 try :
  i11OOoo = re . findall ( pattern , text , flags = re . DOTALL )
  iIiIiIiI = i11OOoo [ 0 ]
 except :
  iIiIiIiI = ""
  if 50 - 50: OoO0O00
 return iIiIiIiI
 if 43 - 43: II111iiii . iiiii11iII1 / I1ii11iIi11i
 if 20 - 20: I1IiiI
 if 95 - 95: i111IiI - I1IiiI
 if 34 - 34: oOo0Oo * I1IiiI . i1IIi * oOo0Oo / oOo0Oo
 if 30 - 30: I1ii11iIi11i + Oo0Ooo / Oo0Ooo % I1ii11iIi11i . I1ii11iIi11i
def O0ii1ii1ii ( heading , text ) :
 id = 10147
 xbmc . executebuiltin ( 'ActivateWindow(%d)' % id )
 xbmc . sleep ( 500 )
 O0O0Oo00 = xbmcgui . Window ( id )
 oOoO00o = 50
 while ( oOoO00o > 0 ) :
  try :
   xbmc . sleep ( 10 )
   oOoO00o -= 1
   O0O0Oo00 . getControl ( 1 ) . setLabel ( heading )
   O0O0Oo00 . getControl ( 5 ) . setText ( text )
   return
  except :
   pass
   if 100 - 100: o0oOOo0O0Ooo + O0o * o0oOOo0O0Ooo
def iiiI1I11i1 ( link ) :
 try :
  iI1iI1I1i1I = re . compile ( '<layouttype>(.+?)</layouttype>' ) . findall ( link ) [ 0 ]
  if layout == 'thumbnail' : xbmc . executebuiltin ( 'Container.SetViewMode(500)' )
  else : xbmc . executebuiltin ( 'Container.SetViewMode(50)' )
 except : pass
 if 80 - 80: o0oOOo0O0Ooo * O0 - I1
OoOO0o = o0OOOoO0 ( ) ; OOOooOooo00O0 = None ; Ii11iII1 = None ; oo00O00Oo = None ; IIIII1II = None ; Oo0O0O0ooO0O = None
try : IIIII1II = urllib . unquote_plus ( OoOO0o [ "site" ] )
except : pass
try : OOOooOooo00O0 = urllib . unquote_plus ( OoOO0o [ "url" ] )
except : pass
try : Ii11iII1 = urllib . unquote_plus ( OoOO0o [ "name" ] )
except : pass
try : oo00O00Oo = int ( OoOO0o [ "mode" ] )
except : pass
try : Oo0O0O0ooO0O = urllib . unquote_plus ( OoOO0o [ "iconimage" ] )
except : pass
try : Iii1ii1II11i = urllib . unquote_plus ( OoOO0o [ "fanart" ] )
except : pass
if 35 - 35: iIii1I11I1II1
if 42 - 42: iII111ii . I1IiiI . i1IIi + OoOoOO00 + O0o + I1IiiI
if 31 - 31: i111IiI . O0o - oOo0Oo . OoooooooOO / OoooooooOO
if oo00O00Oo == None or OOOooOooo00O0 == None or len ( OOOooOooo00O0 ) < 1 : iii11I111 ( )
elif oo00O00Oo == 1 : III1IiiI ( Ii11iII1 , OOOooOooo00O0 , Oo0O0O0ooO0O , Iii1ii1II11i )
elif oo00O00Oo == 2 : oO00O000oO0 ( Ii11iII1 , OOOooOooo00O0 , Oo0O0O0ooO0O )
elif oo00O00Oo == 3 : OooOoOO0 ( Ii11iII1 , OOOooOooo00O0 , Oo0O0O0ooO0O )
elif oo00O00Oo == 4 : Oo ( Ii11iII1 , OOOooOooo00O0 , Oo0O0O0ooO0O )
elif oo00O00Oo == 5 : iIiIIi1 ( )
elif oo00O00Oo == 6 : o00oO0oOo00 ( OOOooOooo00O0 )
elif oo00O00Oo == 7 : i11i ( OOOooOooo00O0 )
elif oo00O00Oo == 8 : IiiiIIiIi1 ( Ii11iII1 , OOOooOooo00O0 , Oo0O0O0ooO0O )
elif oo00O00Oo == 9 : i1O0 ( OOOooOooo00O0 )
elif oo00O00Oo == 10 : oOOo0 ( Ii11iII1 , OOOooOooo00O0 , Oo0O0O0ooO0O , Iii1ii1II11i )
xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )