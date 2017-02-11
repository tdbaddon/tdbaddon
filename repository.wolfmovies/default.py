import base64 , hashlib , os , random , re , requests , shutil , string , sys , urllib
import xbmc , xbmcaddon , xbmcgui , xbmcplugin , xbmcvfs
from addon . common . addon import Addon
from addon . common . net import Net
if 64 - 64: i11iIiiIii
if 65 - 65: O0 / iIii1I11I1II1 % OoooooooOO - i1IIi
if 73 - 73: II111iiii
IiII1IiiIiI1 = 'repository.wolfmovies'
iIiiiI1IiI1I1 = xbmcaddon . Addon ( id = IiII1IiiIiI1 )
o0OoOoOO00 = Addon ( IiII1IiiIiI1 , sys . argv )
I11i = iIiiiI1IiI1I1 . getAddonInfo ( 'name' )
O0O = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + IiII1IiiIiI1 + '/resources/art/' ) )
Oo = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + IiII1IiiIiI1 , 'icon.png' ) )
I1ii11iIi11i = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + IiII1IiiIiI1 , 'fanart.jpg' ) )
I1IiI = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
o0OOO = iIiiiI1IiI1I1 . getSetting ( 'enable_shows' )
iIiiiI = iIiiiI1IiI1I1 . getSetting ( 'base_url' )
Iii1ii1II11i = requests . session ( )
iI111iI = Net ( )
if 34 - 34: iii1I1I / O00oOoOoO0o0O . O0oo0OO0 + Oo0ooO0oo0oO . I1i1iI1i - II
if 100 - 100: i11Ii11I1Ii1i . ooO - OOoO / ooo0Oo0 * i1 - OOooo0000ooo
if 79 - 79: o0000o0o0000o + Ii1Ii1iiii11 % i11Ii11I1Ii1i / Ii1Ii1iiii11 + o0000o0o0000o - iIii1I11I1II1
def oooO0oOOOOo0o ( ) :
 O00OoOoo00 ( '[B][COLOR lime]Search[/COLOR][/B]' , 'url' , 8 , Oo , I1ii11iIi11i , '' )
 O00OoOoo00 ( '[B][COLOR lime]Latest[/COLOR][/B]' , iIiiiI + '/movie/filter/movie/latest/all/all/all/all/all' , 1 , Oo , I1ii11iIi11i , '' )
 O00OoOoo00 ( '[B][COLOR lime]Genre[/COLOR][/B]' , iIiiiI + '/movie/filter/all' , 9 , Oo , I1ii11iIi11i , '' )
 O00OoOoo00 ( '[B][COLOR lime]Year[/COLOR][/B]' , iIiiiI + '/movie/filter/all' , 11 , Oo , I1ii11iIi11i , '' )
 if o0OOO == 'true' : O00OoOoo00 ( '[B][COLOR lime]TV[/COLOR][/B]' , 'url' , 4 , Oo , I1ii11iIi11i , '' )
 if 31 - 31: O0oo0OO0 + II111iiii
 if 13 - 13: ooO * i11Ii11I1Ii1i * iii1I1I
def oOOOO ( ) :
 O00OoOoo00 ( '[B][COLOR lime]Most Favorite[/COLOR][/B]' , iIiiiI + '/movie/filter/series/favorite/all/all/all/all/all' , 2 , Oo , I1ii11iIi11i , '' )
 O00OoOoo00 ( '[B][COLOR lime]Most Ratings[/COLOR][/B]' , iIiiiI + '/movie/filter/series/rating/all/all/all/all/all' , 2 , Oo , I1ii11iIi11i , '' )
 O00OoOoo00 ( '[B][COLOR lime]Most Viewed[/COLOR][/B]' , iIiiiI + '/movie/filter/series/view/all/all/all/all/all' , 2 , Oo , I1ii11iIi11i , '' )
 O00OoOoo00 ( '[B][COLOR lime]Top IMDB[/COLOR][/B]' , iIiiiI + '/movie/filter/series/imdb_mark/all/all/all/all/all' , 2 , Oo , I1ii11iIi11i , '' )
 O00OoOoo00 ( '[B][COLOR lime]Country[/COLOR][/B]' , iIiiiI + '/movie/filter/series' , 10 , Oo , I1ii11iIi11i , '' )
 O00OoOoo00 ( '[B][COLOR lime]Search[/COLOR][/B]' , 'url' , 8 , Oo , I1ii11iIi11i , '' )
 O00OoOoo00 ( '[B][COLOR lime]Latest[/COLOR][/B]' , iIiiiI + '/movie/filter/series/latest/all/all/all/all/all' , 2 , Oo , I1ii11iIi11i , '' )
 O00OoOoo00 ( '[B][COLOR lime]Genre[/COLOR][/B]' , iIiiiI + '/movie/filter/series' , 9 , Oo , I1ii11iIi11i , '' )
 O00OoOoo00 ( '[B][COLOR lime]Year[/COLOR][/B]' , iIiiiI + '/movie/filter/series' , 11 , Oo , I1ii11iIi11i , '' )
 if 45 - 45: o0000o0o0000o + ooo0Oo0
 if 17 - 17: I1i1iI1i
def o00ooooO0oO ( url ) :
 oOoOo00oOo = Ooo00O00O0O0O ( url )
 oOoOo00oOo = oOoOo00oOo . encode ( 'ascii' , 'ignore' )
 OooO0OO = re . compile ( '<input class="genre-ids" value="(.*?)" name=".*?"\n.*?type="checkbox" >(.*?)</label>' ) . findall ( oOoOo00oOo )
 for iiiIi , IiIIIiI1I1 in OooO0OO :
  IiIIIiI1I1 = IiIIIiI1I1 . replace ( ' ' , '' )
  if '/series' in url :
   iiiIi = iIiiiI + '/movie/filter/series/latest/' + iiiIi + '/all/all/all/all'
   O00OoOoo00 ( '[B][COLOR lime]%s[/COLOR][/B]' % IiIIIiI1I1 , iiiIi , 2 , Oo , I1ii11iIi11i , '' )
  else :
   iiiIi = iIiiiI + '/movie/filter/movie/latest/' + iiiIi + '/all/all/all/all'
   O00OoOoo00 ( '[B][COLOR lime]%s[/COLOR][/B]' % IiIIIiI1I1 , iiiIi , 1 , Oo , I1ii11iIi11i , '' )
   if 86 - 86: i11iIiiIii + ooo0Oo0 + Ii1Ii1iiii11 * OOoO + I1i1iI1i
   if 61 - 61: O0oo0OO0 / i11iIiiIii
def IiIiIi ( url ) :
 oOoOo00oOo = Ooo00O00O0O0O ( url )
 oOoOo00oOo = oOoOo00oOo . encode ( 'ascii' , 'ignore' )
 OooO0OO = re . compile ( '<input class="country-ids" value="(.*?)" name=".*?"\n.*?type="checkbox" >(.*?)</label>' ) . findall ( oOoOo00oOo )
 for iiiIi , IiIIIiI1I1 in OooO0OO :
  IiIIIiI1I1 = IiIIIiI1I1 . replace ( ' ' , '' )
  if '/series' in url :
   iiiIi = iIiiiI + '/movie/filter/series/latest/all/' + iiiIi + '/all/all/all'
   O00OoOoo00 ( '[B][COLOR lime]%s[/COLOR][/B]' % IiIIIiI1I1 , iiiIi , 2 , Oo , I1ii11iIi11i , '' )
  else :
   iiiIi = iIiiiI + '/movie/filter/movie/latest/all/' + iiiIi + '/all/all/all'
   O00OoOoo00 ( '[B][COLOR lime]%s[/COLOR][/B]' % IiIIIiI1I1 , iiiIi , 1 , Oo , I1ii11iIi11i , '' )
   if 40 - 40: i11Ii11I1Ii1i . Oo0ooO0oo0oO . O00oOoOoO0o0O . i1IIi
   if 33 - 33: ooo0Oo0 + II111iiii % i11iIiiIii . Ii1Ii1iiii11 - iii1I1I
def O00oooo0O ( url ) :
 oOoOo00oOo = Ooo00O00O0O0O ( url )
 oOoOo00oOo = oOoOo00oOo . encode ( 'ascii' , 'ignore' )
 OooO0OO = re . compile ( 'value="(.*?)" name="year"\n.*?>(.*?)</label>' ) . findall ( oOoOo00oOo )
 for iiiIi , IiIIIiI1I1 in OooO0OO :
  IiIIIiI1I1 = IiIIIiI1I1 . replace ( ' ' , '' )
  if '/series' in url :
   iiiIi = iIiiiI + '/movie/filter/series/latest/all/all/' + iiiIi + '/all/all'
   O00OoOoo00 ( '[B][COLOR lime]%s[/COLOR][/B]' % IiIIIiI1I1 , iiiIi , 2 , Oo , I1ii11iIi11i , '' )
   if 22 - 22: OoooooooOO % OOoO - i1 . iIii1I11I1II1 * i11iIiiIii
  else :
   iiiIi = iIiiiI + '/movie/filter/movie/latest/all/all/' + iiiIi + '/all/all'
   O00OoOoo00 ( '[B][COLOR lime]%s[/COLOR][/B]' % IiIIIiI1I1 , iiiIi , 1 , Oo , I1ii11iIi11i , '' )
   if 32 - 32: O00oOoOoO0o0O * O0 % i11Ii11I1Ii1i % ooo0Oo0 . OOooo0000ooo
 if '/series' in url :
  O00OoOoo00 ( '[B][COLOR lime]Older[/COLOR][/B]' , iIiiiI + '/movie/filter/series/latest/all/all/older-2012/all/all' , 2 , Oo , I1ii11iIi11i , '' )
 else :
  O00OoOoo00 ( '[B][COLOR lime]Older[/COLOR][/B]' , iIiiiI + '/movie/filter/movie/latest/all/all/older-2012/all/all' , 1 , Oo , I1ii11iIi11i , '' )
  if 61 - 61: Ii1Ii1iiii11
def oOOO00o ( url ) :
 oOoOo00oOo = Ooo00O00O0O0O ( url )
 oOoOo00oOo = oOoOo00oOo . encode ( 'ascii' , 'ignore' ) . decode ( 'ascii' )
 o0OoOoOO00 . log ( '#######################link = ' + str ( oOoOo00oOo ) )
 O0O00o0OOO0 = Ii1iIIIi1ii ( oOoOo00oOo , 'class="ml-item">' , '</h2></span>' )
 for o0oo0o0O00OO in O0O00o0OOO0 :
  IiIIIiI1I1 = o0oO ( o0oo0o0O00OO , 'title="' , '"' ) . replace ( "&amp;" , "&" ) . replace ( '&#39;' , "'" ) . replace ( '&quot;' , '"' ) . replace ( '&#39;' , "'" )
  url = o0oO ( o0oo0o0O00OO , 'href="' , '"' ) . replace ( "&amp;" , "&" )
  Oo = o0oO ( o0oo0o0O00OO , 'original="' , '"' )
  I1i1iii = o0oO ( o0oo0o0O00OO , 'mli-quality">' , '<' )
  if 'Season' not in IiIIIiI1I1 :
   O00OoOoo00 ( '[B][COLOR lime]%s[/COLOR][/B][B][I][COLOR orange](%s)[/COLOR][/I][/B]' % ( IiIIIiI1I1 , I1i1iii ) , url + 'watching.html' , 3 , Oo , I1ii11iIi11i , '' )
 try :
  i1iiI11I = re . compile ( '<li class="next"><a href="(.*?)" data-ci-pagination-page=".*?" rel="next">' ) . findall ( oOoOo00oOo ) [ 0 ]
  O00OoOoo00 ( '[B][COLOR orange]Next Page>>>[/COLOR][/B]' , i1iiI11I , 1 , Oo , I1ii11iIi11i , '' )
 except : pass
 iiii ( 'movies' , 'show-view' )
 if 54 - 54: II * ooO
 if 13 - 13: OOooo0000ooo + Oo0ooO0oo0oO - OoooooooOO + o0000o0o0000o . i1 + O0oo0OO0
def Ii ( url ) :
 oOoOo00oOo = Ooo00O00O0O0O ( url )
 oOoOo00oOo = oOoOo00oOo . encode ( 'ascii' , 'ignore' ) . decode ( 'ascii' )
 O0O00o0OOO0 = Ii1iIIIi1ii ( oOoOo00oOo , 'class="ml-item">' , '</h2></span>' )
 for o0oo0o0O00OO in O0O00o0OOO0 :
  IiIIIiI1I1 = o0oO ( o0oo0o0O00OO , 'title="' , '"' ) . replace ( "&amp;" , "&" ) . replace ( '&#39;' , "'" ) . replace ( '&quot;' , '"' ) . replace ( '&#39;' , "'" )
  url = o0oO ( o0oo0o0O00OO , 'href="' , '"' ) . replace ( "&amp;" , "&" )
  Oo = o0oO ( o0oo0o0O00OO , 'original="' , '"' )
  #dis = regex_from_to(a, '<p>', '</p>').replace("&amp;","&").replace('&#39;',"'").replace('&quot;','"').replace('&#39;',"'")
  if 'Season' in IiIIIiI1I1 :
   O00OoOoo00 ( '[B][COLOR lime]%s[/COLOR][/B]' % IiIIIiI1I1 , url + 'watching.html' , 6 , Oo , I1ii11iIi11i , '' )
 try :
  i1iiI11I = re . compile ( '<li class="next"><a href="(.*?)" data-ci-pagination-page=".*?" rel="next">' ) . findall ( oOoOo00oOo ) [ 0 ]
  O00OoOoo00 ( '[B][COLOR orange]Next Page>>>[/COLOR][/B]' , i1iiI11I , 2 , Oo , I1ii11iIi11i , '' )
 except : pass
 iiii ( 'tvshows' , 'show-view' )
 if 57 - 57: iIii1I11I1II1 * ooo0Oo0
 if 61 - 61: I1i1iI1i / O0oo0OO0 + Ii1Ii1iiii11 * i11Ii11I1Ii1i / i11Ii11I1Ii1i
OoOo = '87wwxtp3dqii'
iI = '7bcq9826avrbi6m49vd7shxkn985mhod'
if 60 - 60: OOoO / OOoO
if 46 - 46: ooo0Oo0 * ooO - O0oo0OO0 * i11Ii11I1Ii1i - o0000o0o0000o
def oo0 ( url ) :
 oOoOo00oOo = Ooo00O00O0O0O ( url )
 o00 = url
 OooOooo = re . compile ( 'id: "(.*?)"' ) . findall ( oOoOo00oOo ) [ 0 ]
 O000oo0O = iIiiiI + '/ajax/v2_get_episodes/' + OooOooo
 OOOO = Ooo00O00O0O0O ( O000oo0O )
 i11i1 = Ii1iIIIi1ii ( OOOO , '"server-10"' , '"clearfix"' )
 O0O00o0OOO0 = Ii1iIIIi1ii ( str ( i11i1 ) , '<a' , '</a>' )
 for o0oo0o0O00OO in O0O00o0OOO0 :
  IiIIIiI1I1 = o0oO ( o0oo0o0O00OO , 'title="' , '"' ) . replace ( "&amp;" , "&" ) . replace ( '&#39;' , "'" ) . replace ( '&quot;' , '"' ) . replace ( '&#39;' , "'" )
  IIIii1II1II = i1I1iI ( )
  oo0OooOOo0 = o0oO ( o0oo0o0O00OO , 'episode-id="' , '"' )
  if 92 - 92: i1 . OOoO + I1i1iI1i
  IiII1I11i1I1I = hashlib . md5 ( oo0OooOOo0 + OoOo ) . hexdigest ( ) + '=%s' % IIIii1II1II
  oO0Oo = re . findall ( r'<img title=.*?src="(.*?)"' , str ( oOoOo00oOo ) , re . I | re . DOTALL ) [ 0 ]
  oOOoo0Oo = { 'Accept' : 'image/webp,image/*,*/*;q=0.8' , 'Accept-Encoding' : 'gzip, deflate, sdch, br' ,
 'Accept-Language' : 'en-US,en;q=0.8' , 'Referer' : o00 , 'User-Agent' : I1IiI }
  o00OO00OoO = Iii1ii1II11i . get ( oO0Oo , headers = oOOoo0Oo , verify = False ) . cookies . get_dict ( )
  for OOOO0OOoO0O0 in o00OO00OoO :
   o00OO00OoO = OOOO0OOoO0O0 + '=' + o00OO00OoO [ OOOO0OOoO0O0 ]
  o0oo0o0O00OO = oo0OooOOo0 + iI
  O0Oo000ooO00 = IIIii1II1II
  oO0 = Ii1iIiII1ii1 ( o0oo0o0O00OO , O0Oo000ooO00 )
  o00OO00OoO = '%s; %s' % ( o00OO00OoO , IiII1I11i1I1I )
  if 62 - 62: iIii1I11I1II1 * Oo0ooO0oo0oO
  o0oo0o0O00OO = oo0OooOOo0 + iI
  O0Oo000ooO00 = IIIii1II1II
  oO0 = Ii1iIiII1ii1 ( o0oo0o0O00OO , O0Oo000ooO00 )
  oOOoo0Oo = o00 + '\+' + o00OO00OoO
  url = iIiiiI + '/ajax/v2_get_sources/' + oo0OooOOo0 + '?hash=' + urllib . quote ( oO0 ) . encode ( 'utf8' )
  O00OoOoo00 ( '[B][COLOR lime]%s[/COLOR][/B]' % IiIIIiI1I1 , url , 7 , Oo , I1ii11iIi11i , oOOoo0Oo )
 iiii ( 'tvshows' , 'show-view' )
 if 26 - 26: i1 . o0000o0o0000o
 if 68 - 68: O0oo0OO0
def IIi1iIIiI ( url ) :
 oOoOo00oOo = Ooo00O00O0O0O ( url )
 o00 = url
 OooOooo = re . compile ( 'id: "(.*?)"' ) . findall ( oOoOo00oOo ) [ 0 ]
 O000oo0O = iIiiiI + '/ajax/v2_get_episodes/' + OooOooo
 oO0Oo = re . findall ( r'<img title=.*?src="(.*?)"' , str ( oOoOo00oOo ) , re . I | re . DOTALL ) [ 0 ]
 oOOoo0Oo = { 'Accept' : 'image/webp,image/*,*/*;q=0.8' , 'Accept-Encoding' : 'gzip, deflate, sdch, br' ,
 'Accept-Language' : 'en-US,en;q=0.8' , 'Referer' : o00 , 'User-Agent' : I1IiI }
 o00OO00OoO = Iii1ii1II11i . get ( oO0Oo , headers = oOOoo0Oo , verify = False ) . cookies . get_dict ( )
 for OOOO0OOoO0O0 in o00OO00OoO :
  o00OO00OoO = OOOO0OOoO0O0 + '=' + o00OO00OoO [ OOOO0OOoO0O0 ]
 oOoOo00oOo = Ooo00O00O0O0O ( O000oo0O )
 try :
  O0O00o0OOO0 = Ii1iIIIi1ii ( oOoOo00oOo , '"server-10"' , '"clearfix"' )
  for o0oo0o0O00OO in O0O00o0OOO0 :
   oo0OooOOo0 = o0oO ( o0oo0o0O00OO , 'episode-id="' , '"' )
   IIIii1II1II = i1I1iI ( )
   IiII1I11i1I1I = hashlib . md5 ( oo0OooOOo0 + OoOo ) . hexdigest ( ) + '=%s' % IIIii1II1II
   o00OO00OoO = '%s; %s' % ( o00OO00OoO , IiII1I11i1I1I )
   o0oo0o0O00OO = oo0OooOOo0 + iI
   O0Oo000ooO00 = IIIii1II1II
   oO0 = Ii1iIiII1ii1 ( o0oo0o0O00OO , O0Oo000ooO00 )
   O0OoO = iIiiiI + '/ajax/v2_get_sources/' + oo0OooOOo0 + '?hash=' + urllib . quote ( oO0 ) . encode ( 'utf8' )
   oOOoo0Oo = { 'Accept-Encoding' : 'gzip, deflate, sdch' , 'Cookie' : o00OO00OoO , 'Referer' : o00 ,
 'User-Agent' : I1IiI , 'x-requested-with' : 'XMLHttpRequest' , 'Accept' : 'application/json, text/javascript, */*; q=0.01' }
   oOoOo00oOo = Iii1ii1II11i . get ( O0OoO , headers = oOOoo0Oo ) . text
   url = re . compile ( '"file":"(.*?)"' ) . findall ( oOoOo00oOo ) [ 0 ]
   url = url . replace ( '&amp;' , '&' ) . replace ( '\/' , '/' )
   OO = xbmcgui . ListItem ( IiIIIiI1I1 , iconImage = 'DefaultVideo.png' , thumbnailImage = I1III )
   OO . setInfo ( type = 'Video' , infoLabels = { "Title" : IiIIIiI1I1 } )
   OO . setProperty ( "IsPlayable" , "true" )
   OO . setPath ( url )
   xbmcplugin . setResolvedUrl ( int ( sys . argv [ 1 ] ) , True , OO )
 except :
  O0O00o0OOO0 = Ii1iIIIi1ii ( oOoOo00oOo , '"server-8"' , '"clearfix"' )
  for o0oo0o0O00OO in O0O00o0OOO0 :
   oo0OooOOo0 = o0oO ( o0oo0o0O00OO , 'episode-id="' , '"' )
   IIIii1II1II = i1I1iI ( )
   IiII1I11i1I1I = hashlib . md5 ( oo0OooOOo0 + OoOo ) . hexdigest ( ) + '=%s' % IIIii1II1II
   o00OO00OoO = '%s; %s' % ( o00OO00OoO , IiII1I11i1I1I )
   o0oo0o0O00OO = oo0OooOOo0 + iI
   O0Oo000ooO00 = IIIii1II1II
   oO0 = Ii1iIiII1ii1 ( o0oo0o0O00OO , O0Oo000ooO00 )
   O0OoO = iIiiiI + '/ajax/v2_get_sources/' + oo0OooOOo0 + '?hash=' + urllib . quote ( oO0 ) . encode ( 'utf8' )
   oOOoo0Oo = { 'Accept-Encoding' : 'gzip, deflate, sdch' , 'Cookie' : o00OO00OoO , 'Referer' : o00 ,
 'User-Agent' : I1IiI , 'x-requested-with' : 'XMLHttpRequest' , 'Accept' : 'application/json, text/javascript, */*; q=0.01' }
   oOoOo00oOo = Iii1ii1II11i . get ( O0OoO , headers = oOOoo0Oo ) . text
   url = re . compile ( '"file":"(.*?)"' ) . findall ( oOoOo00oOo ) [ 0 ]
   url = url . replace ( '&amp;' , '&' ) . replace ( '\/' , '/' )
   OO = xbmcgui . ListItem ( IiIIIiI1I1 , iconImage = 'DefaultVideo.png' , thumbnailImage = I1III )
   OO . setInfo ( type = 'Video' , infoLabels = { "Title" : IiIIIiI1I1 } )
   OO . setProperty ( "IsPlayable" , "true" )
   OO . setPath ( url )
   xbmcplugin . setResolvedUrl ( int ( sys . argv [ 1 ] ) , True , OO )
 if 63 - 63: ooO % i11Ii11I1Ii1i * i11Ii11I1Ii1i * O0oo0OO0 / II
 if 74 - 74: II111iiii
 if 75 - 75: I1i1iI1i . Ii1Ii1iiii11
 if 54 - 54: II111iiii % Oo0ooO0oo0oO % OOoO % iIii1I11I1II1 + iIii1I11I1II1 * Ii1Ii1iiii11
 if 87 - 87: Ii1Ii1iiii11 * O00oOoOoO0o0O % i11iIiiIii % Oo0ooO0oo0oO - ooO
 if 68 - 68: o0000o0o0000o % i1IIi . OOooo0000ooo . II
 if 92 - 92: i1 . o0000o0o0000o
 if 31 - 31: o0000o0o0000o . Oo0ooO0oo0oO / O0
 if 89 - 89: Oo0ooO0oo0oO
 if 68 - 68: O0oo0OO0 * OoooooooOO % O0 + O0oo0OO0 + Ii1Ii1iiii11
def i11i1I1 ( url , description ) :
 ii1I = re . split ( r"\+" , str ( description ) , re . I )
 o00 = ii1I [ 0 ]
 IiII1I11i1I1I = ii1I [ 1 ]
 oOOoo0Oo = { 'Referer' : o00 , 'Cookie' : IiII1I11i1I1I , 'user-agent' : I1IiI , 'x-requested-with' : 'XMLHttpRequest' }
 oOoOo00oOo = requests . get ( url , headers = oOOoo0Oo , allow_redirects = False ) . text
 url = re . compile ( '"file":"(.*?)"' ) . findall ( oOoOo00oOo ) [ 0 ]
 url = url . replace ( '&amp;' , '&' ) . replace ( '\/' , '/' )
 OO = xbmcgui . ListItem ( IiIIIiI1I1 , iconImage = 'DefaultVideo.png' , thumbnailImage = I1III )
 OO . setInfo ( type = 'Video' , infoLabels = { "Title" : IiIIIiI1I1 } )
 OO . setProperty ( "IsPlayable" , "true" )
 OO . setPath ( url )
 xbmcplugin . setResolvedUrl ( int ( sys . argv [ 1 ] ) , True , OO )
 if 67 - 67: i11iIiiIii - i1IIi % II . O0
 if 77 - 77: OOooo0000ooo / iii1I1I
def I1 ( query , type ) :
 if query :
  iiIii = query . replace ( ' ' , '+' )
 else :
  ooo0O = xbmc . Keyboard ( '' , 'Type in Query' )
  ooo0O . doModal ( )
  if ( ooo0O . isConfirmed ( ) ) :
   iiIii = ooo0O . getText ( ) . replace ( ' ' , '+' )
   if iiIii == '' :
    xbmc . executebuiltin ( "XBMC.Notification([COLOR gold][B]EMPTY QUERY[/B][/COLOR],Aborting search,7000," + Oo + ")" )
    return
   else : pass
 oOoO0o00OO0 = iIiiiI + '/movie/search/' + iiIii
 print oOoO0o00OO0
 oOoOo00oOo = Ooo00O00O0O0O ( oOoO0o00OO0 )
 oOoOo00oOo = oOoOo00oOo . encode ( 'ascii' , 'ignore' ) . decode ( 'ascii' )
 O0O00o0OOO0 = Ii1iIIIi1ii ( oOoOo00oOo , 'ml-item">' , '</h2></span>' )
 for o0oo0o0O00OO in O0O00o0OOO0 :
  IiIIIiI1I1 = o0oO ( o0oo0o0O00OO , 'title="' , '"' ) . replace ( "&amp;" , "&" ) . replace ( '&#39;' , "'" ) . replace ( '&quot;' , '"' ) . replace ( '&#39;' , "'" )
  oOoO0o00OO0 = o0oO ( o0oo0o0O00OO , 'href="' , '"' ) . replace ( "&amp;" , "&" )
  Oo = o0oO ( o0oo0o0O00OO , 'original="' , '"' )
  if 7 - 7: ooO + o0000o0o0000o + O0
  if 'Season' in IiIIIiI1I1 :
   if type != 'tv' :
    O00OoOoo00 ( '[B][COLOR lime]%s[/COLOR][/B]' % IiIIIiI1I1 , oOoO0o00OO0 + 'watching.html' , 6 , Oo , I1ii11iIi11i , '' )
  else :
   if type != 'movie' :
    O00OoOoo00 ( '[B][COLOR lime]%s[/COLOR][/B]' % IiIIIiI1I1 , oOoO0o00OO0 + 'watching.html' , 3 , Oo , I1ii11iIi11i , '' )
    if 9 - 9: II111iiii . I1i1iI1i - Ii1Ii1iiii11 / I1i1iI1i
    if 46 - 46: OOoO . ooO * OOoO % i1IIi
def o0oO ( text , from_string , to_string , excluding = True ) :
 if excluding :
  try : iIIiII = re . search ( "(?i)" + from_string + "([\S\s]+?)" + to_string , text ) . group ( 1 )
  except : iIIiII = ''
 else :
  try : iIIiII = re . search ( "(?i)(" + from_string + "[\S\s]+?" + to_string + ")" , text ) . group ( 1 )
  except : iIIiII = ''
 return iIIiII
 if 38 - 38: o0000o0o0000o
 if 7 - 7: O0 . i1 % II - iii1I1I - iIii1I11I1II1
def Ii1iIIIi1ii ( text , start_with , end_with ) :
 iIIiII = re . findall ( "(?i)(" + start_with + "[\S\s]+?" + end_with + ")" , text )
 return iIIiII
 if 36 - 36: OOooo0000ooo % Ii1Ii1iiii11 % O00oOoOoO0o0O - II
 if 22 - 22: iIii1I11I1II1 / O00oOoOoO0o0O * II % i1
def OOOo00oo0oO ( a ) :
 O0Oo000ooO00 = str ( a )
 IIiIi1iI = ord ( O0Oo000ooO00 [ 0 ] )
 if 0xD800 <= IIiIi1iI and IIiIi1iI <= 0xDBFF :
  i1IiiiI1iI = IIiIi1iI
  if len ( O0Oo000ooO00 ) == 1 :
   return IIiIi1iI
  i1iIi = ord ( O0Oo000ooO00 [ 1 ] )
  return ( ( i1IiiiI1iI - 0xD800 ) * 0x400 ) + ( i1iIi - 0xDC00 ) + 0x10000
  if 68 - 68: i11iIiiIii % II + i11iIiiIii
 if 0xDC00 <= IIiIi1iI and IIiIi1iI <= 0xDFFF :
  return IIiIi1iI
 return IIiIi1iI
 if 31 - 31: II111iiii . iii1I1I
def Ii1iIiII1ii1 ( a , b ) :
 i1IiiiI1iI = ''
 OOOO0OOoO0O0 = 0
 for OOOO0OOoO0O0 , i1iIi in enumerate ( a ) :
  II1I = b [ OOOO0OOoO0O0 % len ( b ) - 1 ]
  i1iIi = int ( OOOo00oo0oO ( i1iIi ) + OOOo00oo0oO ( II1I ) )
  i1IiiiI1iI += chr ( i1iIi )
  if 84 - 84: OOooo0000ooo . i11iIiiIii . OOooo0000ooo * II - OOoO
 return base64 . b64encode ( i1IiiiI1iI )
 if 42 - 42: i11iIiiIii
 if 33 - 33: i1 - O0 * i1IIi * I1i1iI1i - O00oOoOoO0o0O
 if 32 - 32: OoooooooOO / iIii1I11I1II1 - I1i1iI1i
def i1I1iI ( size = 16 , chars = string . ascii_letters + string . digits ) :
 return '' . join ( random . choice ( chars ) for x in range ( size ) )
 if 91 - 91: i1 % i1IIi % iIii1I11I1II1
 if 20 - 20: ooO % ooo0Oo0 / ooo0Oo0 + ooo0Oo0
def III1IiiI ( ) :
 iIi1 = [ ]
 IIIII11I1IiI = sys . argv [ 2 ]
 if len ( IIIII11I1IiI ) >= 2 :
  i1I = sys . argv [ 2 ]
  OoOO = i1I . replace ( '?' , '' )
  if ( i1I [ len ( i1I ) - 1 ] == '/' ) :
   i1I = i1I [ 0 : len ( i1I ) - 2 ]
  ooOOO0 = OoOO . split ( '&' )
  iIi1 = { }
  for OOOO0OOoO0O0 in range ( len ( ooOOO0 ) ) :
   o0o = { }
   o0o = ooOOO0 [ OOOO0OOoO0O0 ] . split ( '=' )
   if ( len ( o0o ) ) == 2 :
    iIi1 [ o0o [ 0 ] ] = o0o [ 1 ]
 return iIi1
 if 73 - 73: OOooo0000ooo * II + iii1I1I . Ii1Ii1iiii11
 if 70 - 70: o0000o0o0000o - O00oOoOoO0o0O / ooo0Oo0
def O00OoOoo00 ( name , url , mode , iconimage , fanart , description ) :
 O00OOOOOoo0 = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&iconimage=" + urllib . quote_plus ( iconimage ) + "&description=" + urllib . quote_plus ( description )
 ii1 = True
 OO = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 OO . setInfo ( type = "Video" , infoLabels = { "Title" : name , "Plot" : description } )
 OO . setProperty ( 'fanart_image' , fanart )
 if mode == 3 or mode == 7 :
  OO . setProperty ( "IsPlayable" , "true" )
  ii1 = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = O00OOOOOoo0 , listitem = OO , isFolder = False )
 else :
  ii1 = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = O00OOOOOoo0 , listitem = OO , isFolder = True )
 return ii1
 if 11 - 11: OOooo0000ooo * iii1I1I . iIii1I11I1II1 % OoooooooOO + i1
 if 78 - 78: O0oo0OO0 . ooO + O0oo0OO0 / OOoO / O0oo0OO0
def oO0O00OoOO0 ( name , url , mode , iconimage , fanart , description = '' ) :
 if 82 - 82: II111iiii . OOooo0000ooo - iIii1I11I1II1 - OOooo0000ooo * II111iiii
 if 77 - 77: iIii1I11I1II1 * O0oo0OO0
 OO = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 OO . setInfo ( type = "Video" , infoLabels = { "Title" : name , 'plot' : description } )
 OO . setProperty ( 'fanart_image' , fanart )
 ii1 = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = url , listitem = OO , isFolder = False )
 return ii1
 if 95 - 95: iii1I1I + i11iIiiIii
 if 6 - 6: Ii1Ii1iiii11 / i11iIiiIii + i1 * i11Ii11I1Ii1i
def Ooo00O00O0O0O ( url ) :
 oOOoo0Oo = { }
 oOOoo0Oo [ 'User-Agent' ] = I1IiI
 oOoOo00oOo = Iii1ii1II11i . get ( url , headers = oOOoo0Oo , verify = False ) . text
 oOoOo00oOo = oOoOo00oOo . encode ( 'ascii' , 'ignore' )
 return oOoOo00oOo
 if 80 - 80: II111iiii
 if 83 - 83: OOoO . i11iIiiIii + II111iiii . I1i1iI1i * OOoO
def iiii ( content , viewType ) :
 if content :
  if 53 - 53: II111iiii
  if 31 - 31: O0oo0OO0
  xbmcplugin . setContent ( int ( sys . argv [ 1 ] ) , content )
 if o0OoOoOO00 . get_setting ( 'auto-view' ) == 'true' :
  if 80 - 80: o0000o0o0000o . i11iIiiIii - I1i1iI1i
  print o0OoOoOO00 . get_setting ( viewType )
  if o0OoOoOO00 . get_setting ( viewType ) == 'Info' :
   iIiIIi1 = '504'
  elif o0OoOoOO00 . get_setting ( viewType ) == 'Info2' :
   iIiIIi1 = '503'
  elif o0OoOoOO00 . get_setting ( viewType ) == 'Info3' :
   iIiIIi1 = '515'
  elif o0OoOoOO00 . get_setting ( viewType ) == 'Fanart' :
   iIiIIi1 = '508'
  elif o0OoOoOO00 . get_setting ( viewType ) == 'Poster Wrap' :
   iIiIIi1 = '501'
  elif o0OoOoOO00 . get_setting ( viewType ) == 'Big List' :
   iIiIIi1 = '51'
  elif o0OoOoOO00 . get_setting ( viewType ) == 'Low List' :
   iIiIIi1 = '724'
  elif o0OoOoOO00 . get_setting ( viewType ) == 'Default View' :
   iIiIIi1 = o0OoOoOO00 . get_setting ( 'default-view' )
   if 7 - 7: Ii1Ii1iiii11 - O00oOoOoO0o0O - i11Ii11I1Ii1i + Ii1Ii1iiii11
  print viewType
  print iIiIIi1
  if 26 - 26: ooo0Oo0
  xbmc . executebuiltin ( "Container.SetViewMode(%s)" % ( int ( iIiIIi1 ) ) )
  if 35 - 35: ooo0Oo0 - iii1I1I % I1i1iI1i . OoooooooOO % ooo0Oo0
 xbmcplugin . addSortMethod ( handle = int ( sys . argv [ 1 ] ) , sortMethod = xbmcplugin . SORT_METHOD_UNSORTED )
 xbmcplugin . addSortMethod ( handle = int ( sys . argv [ 1 ] ) , sortMethod = xbmcplugin . SORT_METHOD_LABEL )
 xbmcplugin . addSortMethod ( handle = int ( sys . argv [ 1 ] ) , sortMethod = xbmcplugin . SORT_METHOD_VIDEO_RATING )
 xbmcplugin . addSortMethod ( handle = int ( sys . argv [ 1 ] ) , sortMethod = xbmcplugin . SORT_METHOD_DATE )
 xbmcplugin . addSortMethod ( handle = int ( sys . argv [ 1 ] ) , sortMethod = xbmcplugin . SORT_METHOD_PROGRAM_COUNT )
 xbmcplugin . addSortMethod ( handle = int ( sys . argv [ 1 ] ) , sortMethod = xbmcplugin . SORT_METHOD_VIDEO_RUNTIME )
 xbmcplugin . addSortMethod ( handle = int ( sys . argv [ 1 ] ) , sortMethod = xbmcplugin . SORT_METHOD_GENRE )
 xbmcplugin . addSortMethod ( handle = int ( sys . argv [ 1 ] ) , sortMethod = xbmcplugin . SORT_METHOD_MPAA_RATING )
 if 47 - 47: i1 - ooo0Oo0 . II111iiii + OoooooooOO . i11iIiiIii
 if 94 - 94: I1i1iI1i * ooo0Oo0 / O00oOoOoO0o0O / ooo0Oo0
i1I = III1IiiI ( )
oOoO0o00OO0 = None
IiIIIiI1I1 = None
oO0O0OO0O = None
I1III = None
OOOoOoO = None
Ii1I1i = None
type = None
if 99 - 99: i11Ii11I1Ii1i . i1 + Ii1Ii1iiii11 % i11Ii11I1Ii1i . i11iIiiIii % O0
if 78 - 78: II + ooO - o0000o0o0000o
try :
 oOoO0o00OO0 = urllib . unquote_plus ( i1I [ "url" ] )
except :
 pass
try :
 IiIIIiI1I1 = urllib . unquote_plus ( i1I [ "name" ] )
except :
 pass
try :
 I1III = urllib . unquote_plus ( i1I [ "iconimage" ] )
except :
 pass
try :
 oO0O0OO0O = int ( i1I [ "mode" ] )
except :
 pass
try :
 OOOoOoO = urllib . unquote_plus ( i1I [ "description" ] )
except :
 pass
try :
 Ii1I1i = urllib . unquote_plus ( i1I [ "query" ] )
except :
 pass
try :
 type = urllib . unquote_plus ( i1I [ "type" ] )
except :
 pass
 if 38 - 38: I1i1iI1i - i11Ii11I1Ii1i + iIii1I11I1II1 / Oo0ooO0oo0oO % O00oOoOoO0o0O
 if 57 - 57: O0oo0OO0 / Ii1Ii1iiii11
if oO0O0OO0O == None or oOoO0o00OO0 == None or len ( oOoO0o00OO0 ) < 1 :
 oooO0oOOOOo0o ( )
 if 29 - 29: iIii1I11I1II1 + Oo0ooO0oo0oO * O0oo0OO0 * ooO . iii1I1I * iii1I1I
elif oO0O0OO0O == 1 :
 oOOO00o ( oOoO0o00OO0 )
 if 7 - 7: OOooo0000ooo * o0000o0o0000o % ooo0Oo0 - I1i1iI1i
elif oO0O0OO0O == 2 :
 Ii ( oOoO0o00OO0 )
 if 13 - 13: ooo0Oo0 . i11iIiiIii
elif oO0O0OO0O == 3 :
 IIi1iIIiI ( oOoO0o00OO0 )
 if 56 - 56: II % O0 - iii1I1I
elif oO0O0OO0O == 4 :
 oOOOO ( )
 if 100 - 100: ooo0Oo0 - O0 % i11Ii11I1Ii1i * ooO + iii1I1I
elif oO0O0OO0O == 6 :
 oo0 ( oOoO0o00OO0 )
 if 88 - 88: OoooooooOO - O0oo0OO0 * O0 * OoooooooOO . OoooooooOO
elif oO0O0OO0O == 7 :
 i11i1I1 ( oOoO0o00OO0 , OOOoOoO )
 if 33 - 33: o0000o0o0000o + i1 * i11Ii11I1Ii1i / iIii1I11I1II1 - iii1I1I
elif oO0O0OO0O == 8 :
 I1 ( Ii1I1i , type )
 if 54 - 54: o0000o0o0000o / ooO . i11Ii11I1Ii1i % i1
 if 57 - 57: i11iIiiIii . II - ooo0Oo0 - i11Ii11I1Ii1i + Oo0ooO0oo0oO
elif oO0O0OO0O == 9 :
 o00ooooO0oO ( oOoO0o00OO0 )
 if 63 - 63: Oo0ooO0oo0oO * i1
elif oO0O0OO0O == 10 :
 IiIiIi ( oOoO0o00OO0 )
 if 69 - 69: O0 . O0oo0OO0
elif oO0O0OO0O == 11 :
 O00oooo0O ( oOoO0o00OO0 )
 if 49 - 49: iii1I1I - OOoO
 if 74 - 74: iIii1I11I1II1 * II + Oo0ooO0oo0oO / i1IIi / II111iiii . O00oOoOoO0o0O
 if 62 - 62: OoooooooOO * iii1I1I
 if 58 - 58: Oo0ooO0oo0oO % I1i1iI1i
 if 50 - 50: o0000o0o0000o . I1i1iI1i
xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
if 97 - 97: O0 + Oo0ooO0oo0oO
if 89 - 89: I1i1iI1i + O0oo0OO0 * OOoO * ooo0Oo0
if 37 - 37: OoooooooOO - O0 - I1i1iI1i
if 77 - 77: ooO * iIii1I11I1II1
if 98 - 98: iii1I1I % ooo0Oo0 * OoooooooOO
if 51 - 51: iIii1I11I1II1 . Oo0ooO0oo0oO / i11Ii11I1Ii1i + I1i1iI1i
if 33 - 33: Ii1Ii1iiii11 . II111iiii % i1 + I1i1iI1i
if 71 - 71: O00oOoOoO0o0O % ooO
if 98 - 98: OOoO % i11iIiiIii % Ii1Ii1iiii11 + ooo0Oo0
if 78 - 78: II % i11Ii11I1Ii1i / i1 - iIii1I11I1II1
if 69 - 69: o0000o0o0000o
if 11 - 11: iii1I1I
if 16 - 16: ooo0Oo0 + OOooo0000ooo * O0 % i1IIi . iii1I1I
if 67 - 67: OoooooooOO / iii1I1I * ooo0Oo0 + OOoO
if 65 - 65: OoooooooOO - II / Ii1Ii1iiii11 / II111iiii / i1IIi
if 71 - 71: o0000o0o0000o + ooo0Oo0
if 28 - 28: ooO
if 38 - 38: Ii1Ii1iiii11 % II111iiii % OOoO / O0oo0OO0 + Oo0ooO0oo0oO / i1IIi
if 54 - 54: iIii1I11I1II1 % II - ooO / i11Ii11I1Ii1i - O0oo0OO0 . OOoO
if 11 - 11: II . O0oo0OO0 * OOooo0000ooo * OoooooooOO + Ii1Ii1iiii11
if 33 - 33: O0 * I1i1iI1i - o0000o0o0000o % o0000o0o0000o
if 18 - 18: o0000o0o0000o / O00oOoOoO0o0O * o0000o0o0000o + o0000o0o0000o * i11iIiiIii * II
if 11 - 11: Ii1Ii1iiii11 / Oo0ooO0oo0oO - OOooo0000ooo * OoooooooOO + OoooooooOO . Oo0ooO0oo0oO
if 26 - 26: ooo0Oo0 % II
if 76 - 76: OOooo0000ooo * i1
if 52 - 52: ooO
if 19 - 19: iii1I1I
if 25 - 25: ooo0Oo0 / Ii1Ii1iiii11
if 31 - 31: ooO . O0 % iii1I1I . I1i1iI1i + OOooo0000ooo
if 71 - 71: o0000o0o0000o . II111iiii
if 62 - 62: OoooooooOO . OOoO
if 61 - 61: Oo0ooO0oo0oO - ooO - i1IIi
if 25 - 25: O0 * OOoO + II . I1i1iI1i . I1i1iI1i
if 58 - 58: iii1I1I
if 53 - 53: i1IIi
if 59 - 59: I1i1iI1i
if 81 - 81: Oo0ooO0oo0oO - Oo0ooO0oo0oO . i1
if 73 - 73: OOoO % i11iIiiIii - iii1I1I
if 7 - 7: O0 * i11iIiiIii * ooo0Oo0 + Ii1Ii1iiii11 % O0oo0OO0 - Ii1Ii1iiii11
if 39 - 39: O00oOoOoO0o0O * ooO % ooO - OoooooooOO + I1i1iI1i - OOoO
if 23 - 23: i11iIiiIii
if 30 - 30: I1i1iI1i - i1IIi % II111iiii + OOoO * iIii1I11I1II1
if 81 - 81: OOooo0000ooo % i1IIi . iIii1I11I1II1
if 4 - 4: i11iIiiIii % O0oo0OO0 % i1IIi / OOooo0000ooo
if 6 - 6: i1 / iii1I1I % ooO - iii1I1I
if 31 - 31: ooO
if 23 - 23: o0000o0o0000o . OOooo0000ooo
if 92 - 92: Oo0ooO0oo0oO + o0000o0o0000o * ooo0Oo0 % iii1I1I
if 42 - 42: O00oOoOoO0o0O
if 76 - 76: iii1I1I * i1 % o0000o0o0000o
if 57 - 57: iIii1I11I1II1 - i1IIi / o0000o0o0000o - O0 * OoooooooOO % II111iiii
if 68 - 68: OoooooooOO * OOoO % Oo0ooO0oo0oO - OOooo0000ooo
if 34 - 34: o0000o0o0000o . iIii1I11I1II1 * Oo0ooO0oo0oO * i11Ii11I1Ii1i / o0000o0o0000o / II
if 78 - 78: O00oOoOoO0o0O - I1i1iI1i / Oo0ooO0oo0oO
if 10 - 10: i1 + O00oOoOoO0o0O * II + iIii1I11I1II1 / o0000o0o0000o / II
if 42 - 42: iii1I1I
if 38 - 38: ooO + II111iiii % Ii1Ii1iiii11 % Oo0ooO0oo0oO - ooo0Oo0 / OoooooooOO
if 73 - 73: I1i1iI1i * O0 - i11iIiiIii
if 85 - 85: ooo0Oo0 % i1 + OOoO / I1i1iI1i . i11Ii11I1Ii1i + ooO
if 62 - 62: i11iIiiIii + i11iIiiIii - I1i1iI1i
if 28 - 28: i1 . i1 % iIii1I11I1II1 * iIii1I11I1II1 . I1i1iI1i / i1
if 27 - 27: O0oo0OO0 + Ii1Ii1iiii11 - i1IIi
if 69 - 69: OOooo0000ooo - O0 % II + i11iIiiIii . Oo0ooO0oo0oO / O0oo0OO0
if 79 - 79: O0 * i11iIiiIii - OOooo0000ooo / OOooo0000ooo
if 48 - 48: O0
if 93 - 93: i11iIiiIii - iii1I1I * II * OOoO % O0 + OoooooooOO
if 25 - 25: OOooo0000ooo + ooo0Oo0 / Ii1Ii1iiii11 . I1i1iI1i % O0 * O0oo0OO0
if 84 - 84: Ii1Ii1iiii11 % ooo0Oo0 + i11iIiiIii
if 28 - 28: O00oOoOoO0o0O + O0oo0OO0 * ooO % i11Ii11I1Ii1i . OOoO % O0
if 16 - 16: OOoO - iIii1I11I1II1 / iii1I1I . II111iiii + iIii1I11I1II1
if 19 - 19: O0oo0OO0 - O00oOoOoO0o0O . O0
if 60 - 60: II111iiii + O00oOoOoO0o0O
if 9 - 9: Ii1Ii1iiii11 * OoooooooOO - iIii1I11I1II1 + Oo0ooO0oo0oO / O0oo0OO0 . O0oo0OO0
if 49 - 49: II111iiii
if 25 - 25: OoooooooOO - iii1I1I . iii1I1I * i11Ii11I1Ii1i
if 81 - 81: i1 + OOooo0000ooo
if 98 - 98: iii1I1I
if 95 - 95: Ii1Ii1iiii11 / Ii1Ii1iiii11
if 30 - 30: II + O00oOoOoO0o0O / O00oOoOoO0o0O % II . II
if 55 - 55: Ii1Ii1iiii11 - OOoO + II111iiii + i1 % ooo0Oo0
if 41 - 41: i1IIi - OOoO - ooo0Oo0
if 8 - 8: O0oo0OO0 + o0000o0o0000o - I1i1iI1i % O00oOoOoO0o0O % I1i1iI1i * i11Ii11I1Ii1i
if 9 - 9: O00oOoOoO0o0O - i11iIiiIii - ooO * ooo0Oo0 + Ii1Ii1iiii11
if 44 - 44: II111iiii
if 52 - 52: II - O00oOoOoO0o0O + II % I1i1iI1i
if 35 - 35: iIii1I11I1II1
if 42 - 42: o0000o0o0000o . iii1I1I . i1IIi + Oo0ooO0oo0oO + ooO + iii1I1I
if 31 - 31: i1 . ooO - Ii1Ii1iiii11 . OoooooooOO / OoooooooOO
if 56 - 56: O0oo0OO0 / i11Ii11I1Ii1i / i11iIiiIii + OoooooooOO - O00oOoOoO0o0O - OOoO
if 21 - 21: O0 % OOooo0000ooo . iii1I1I / II111iiii + OOooo0000ooo
if 53 - 53: i11Ii11I1Ii1i - iii1I1I - i11Ii11I1Ii1i * i1
if 71 - 71: O0 - iIii1I11I1II1
if 12 - 12: ooO / I1i1iI1i
if 42 - 42: O00oOoOoO0o0O
if 19 - 19: i11Ii11I1Ii1i % II * iIii1I11I1II1 + iii1I1I
if 46 - 46: O00oOoOoO0o0O
if 1 - 1: i1
if 97 - 97: ooO + i1 + O0 + i11iIiiIii
if 77 - 77: I1i1iI1i / OoooooooOO
if 46 - 46: I1i1iI1i % iIii1I11I1II1 . i1 % i1 + i11iIiiIii
if 72 - 72: iIii1I11I1II1 * ooo0Oo0 % Ii1Ii1iiii11 / O0oo0OO0
if 35 - 35: Ii1Ii1iiii11 + i1IIi % II % OOoO + i11Ii11I1Ii1i
if 17 - 17: i1IIi
if 21 - 21: O00oOoOoO0o0O
if 29 - 29: OOoO / II111iiii / Ii1Ii1iiii11 * ooO
if 10 - 10: o0000o0o0000o % OOooo0000ooo * OOooo0000ooo . OOoO / ooo0Oo0 % ooO
if 49 - 49: O0oo0OO0 / i11Ii11I1Ii1i + O0 * I1i1iI1i
if 28 - 28: Ii1Ii1iiii11 + i11iIiiIii / OOoO % Oo0ooO0oo0oO % O00oOoOoO0o0O - O0
if 54 - 54: i1IIi + II111iiii
if 83 - 83: II - iii1I1I + ooO
if 5 - 5: ooo0Oo0
if 46 - 46: OOooo0000ooo
if 45 - 45: Ii1Ii1iiii11
if 21 - 21: i11Ii11I1Ii1i . o0000o0o0000o . ooO / O00oOoOoO0o0O / o0000o0o0000o
if 17 - 17: ooO / ooO / OOoO
if 1 - 1: i1IIi . i11iIiiIii % ooO
if 82 - 82: iIii1I11I1II1 + O00oOoOoO0o0O . iIii1I11I1II1 % OOooo0000ooo / ooo0Oo0 . ooo0Oo0
if 14 - 14: I1i1iI1i . ooO . OOoO + OoooooooOO - ooO + OOooo0000ooo
if 9 - 9: ooo0Oo0
if 59 - 59: iii1I1I * II111iiii . O0
if 56 - 56: ooo0Oo0 - i1 % iii1I1I - I1i1iI1i
if 51 - 51: O0 / Ii1Ii1iiii11 * iIii1I11I1II1 + II + I1i1iI1i
if 98 - 98: iIii1I11I1II1 * II * ooO + Ii1Ii1iiii11 % i11iIiiIii % O0
if 27 - 27: O0
if 79 - 79: I1i1iI1i - OOoO + I1i1iI1i . i11Ii11I1Ii1i
if 28 - 28: i1IIi - i1
if 54 - 54: i1 - O0 % ooO
if 73 - 73: O0 . Oo0ooO0oo0oO + iii1I1I - OOoO % OOoO . OOoO
if 17 - 17: ooo0Oo0 - OoooooooOO % ooo0Oo0 . OOooo0000ooo / i11iIiiIii % i1
if 28 - 28: OOoO
if 58 - 58: Oo0ooO0oo0oO
if 37 - 37: O00oOoOoO0o0O - iIii1I11I1II1 / II
if 73 - 73: i11iIiiIii - OOooo0000ooo
if 25 - 25: OoooooooOO + OOooo0000ooo * II
if 92 - 92: iii1I1I + OOoO + O0 / I1i1iI1i + o0000o0o0000o
if 18 - 18: Ii1Ii1iiii11 * Oo0ooO0oo0oO . i1 / II / i11iIiiIii
if 21 - 21: i11Ii11I1Ii1i / II + ooo0Oo0 + OoooooooOO
if 91 - 91: i11iIiiIii / i1IIi + i1 + Ii1Ii1iiii11 * i11iIiiIii
if 66 - 66: iIii1I11I1II1 % i1IIi - O0 + OOoO * o0000o0o0000o . OOooo0000ooo
if 52 - 52: Ii1Ii1iiii11 + O0 . i1 . II . O0oo0OO0
if 97 - 97: iii1I1I / i1
if 71 - 71: II111iiii / i1IIi . II % OoooooooOO . Oo0ooO0oo0oO
if 41 - 41: i1IIi * II111iiii / OoooooooOO . ooO
if 83 - 83: i1 . O0 / O00oOoOoO0o0O / ooO - II111iiii
if 100 - 100: O0oo0OO0
if 46 - 46: Oo0ooO0oo0oO / iIii1I11I1II1 % i1 . iIii1I11I1II1 * i1
if 38 - 38: II - i1 / O0 . o0000o0o0000o
if 45 - 45: o0000o0o0000o
if 83 - 83: Oo0ooO0oo0oO . OoooooooOO
if 58 - 58: i11iIiiIii + OoooooooOO % OoooooooOO / OOooo0000ooo / i11iIiiIii
if 62 - 62: O0oo0OO0 / II
if 7 - 7: OoooooooOO . OOooo0000ooo
if 53 - 53: ooo0Oo0 % ooo0Oo0 * I1i1iI1i + Oo0ooO0oo0oO
if 92 - 92: OoooooooOO + i1IIi / ooo0Oo0 * O0
if 100 - 100: Ii1Ii1iiii11 % iIii1I11I1II1 * II111iiii - i1
if 92 - 92: Ii1Ii1iiii11
if 22 - 22: O00oOoOoO0o0O % i1 * II / ooO % i11iIiiIii * OOoO
if 95 - 95: OoooooooOO - OOooo0000ooo * iii1I1I + Oo0ooO0oo0oO
if 10 - 10: I1i1iI1i / i11iIiiIii
if 92 - 92: OOoO . o0000o0o0000o
if 85 - 85: II . o0000o0o0000o
if 78 - 78: Ii1Ii1iiii11 * o0000o0o0000o + iIii1I11I1II1 + iIii1I11I1II1 / o0000o0o0000o . ooo0Oo0
if 97 - 97: Ii1Ii1iiii11 / o0000o0o0000o % i1IIi % II
if 18 - 18: iIii1I11I1II1 % OOoO
if 95 - 95: Ii1Ii1iiii11 + i11iIiiIii * o0000o0o0000o - i1IIi * o0000o0o0000o - iIii1I11I1II1
if 75 - 75: OoooooooOO * OOooo0000ooo
if 9 - 9: OOooo0000ooo - II111iiii + O0 / iIii1I11I1II1 / i11iIiiIii
if 39 - 39: OOooo0000ooo * O00oOoOoO0o0O + iIii1I11I1II1 - OOooo0000ooo + ooO
if 69 - 69: O0
if 85 - 85: Ii1Ii1iiii11 / O0
if 18 - 18: I1i1iI1i % O0 * II
if 62 - 62: o0000o0o0000o . OOooo0000ooo . OoooooooOO
if 11 - 11: ooO / OOoO
if 73 - 73: i1IIi / i11iIiiIii
if 58 - 58: O00oOoOoO0o0O . II111iiii + i11Ii11I1Ii1i - i11iIiiIii / II111iiii / O0
if 85 - 85: Oo0ooO0oo0oO + ooO
if 10 - 10: OOooo0000ooo / O0oo0OO0 + Oo0ooO0oo0oO / i1IIi
if 27 - 27: ooo0Oo0
if 67 - 67: iii1I1I
if 55 - 55: II - i1 * I1i1iI1i + Oo0ooO0oo0oO * Oo0ooO0oo0oO * O0
if 91 - 91: o0000o0o0000o - ooO % iIii1I11I1II1 - OoooooooOO % Ii1Ii1iiii11
if 98 - 98: O0oo0OO0 . O0oo0OO0 * i11Ii11I1Ii1i * II111iiii * o0000o0o0000o
if 92 - 92: O00oOoOoO0o0O
if 40 - 40: Oo0ooO0oo0oO / OOooo0000ooo
if 79 - 79: O0oo0OO0 - iIii1I11I1II1 + ooo0Oo0 - o0000o0o0000o
if 93 - 93: II111iiii . iii1I1I - O00oOoOoO0o0O + Oo0ooO0oo0oO
if 61 - 61: II111iiii
if 15 - 15: i11iIiiIii % iii1I1I * OOoO / o0000o0o0000o
if 90 - 90: i1
if 31 - 31: ooO + O0
if 87 - 87: Ii1Ii1iiii11
if 45 - 45: O0oo0OO0 / OoooooooOO - i1 / ooo0Oo0 % OOooo0000ooo
if 83 - 83: iii1I1I . iIii1I11I1II1 - OOooo0000ooo * i11iIiiIii
if 20 - 20: i1IIi * o0000o0o0000o + II111iiii % I1i1iI1i % i11Ii11I1Ii1i
if 13 - 13: O00oOoOoO0o0O
if 60 - 60: II * iii1I1I
if 17 - 17: ooO % O00oOoOoO0o0O / II . OOooo0000ooo * ooO - II111iiii
if 41 - 41: ooo0Oo0
if 77 - 77: o0000o0o0000o
if 65 - 65: II111iiii . iii1I1I % i11Ii11I1Ii1i * O0oo0OO0
if 38 - 38: Oo0ooO0oo0oO / i1 % O00oOoOoO0o0O
if 11 - 11: i1 - i11Ii11I1Ii1i + II111iiii - iIii1I11I1II1
if 7 - 7: OOooo0000ooo - OOoO / II111iiii * ooo0Oo0 . i1 * i1
if 61 - 61: OOoO % Ii1Ii1iiii11 - O0oo0OO0 / O00oOoOoO0o0O
if 4 - 4: OoooooooOO - i1IIi % ooo0Oo0 - ooO * I1i1iI1i
if 85 - 85: OoooooooOO * iIii1I11I1II1 . i1 / OoooooooOO % iii1I1I % O0
if 36 - 36: ooo0Oo0 / II111iiii / OOooo0000ooo / OOooo0000ooo + II
if 95 - 95: OOooo0000ooo
if 51 - 51: II111iiii + OOooo0000ooo . i1IIi . II + Oo0ooO0oo0oO * iii1I1I
if 72 - 72: i11Ii11I1Ii1i + i11Ii11I1Ii1i / II111iiii . OoooooooOO % ooo0Oo0
if 49 - 49: i11Ii11I1Ii1i . O0oo0OO0 - O00oOoOoO0o0O * OoooooooOO . O00oOoOoO0o0O
if 2 - 2: OoooooooOO % ooO
if 63 - 63: iii1I1I % iIii1I11I1II1
if 39 - 39: i1 / II111iiii / II % iii1I1I
if 89 - 89: o0000o0o0000o + OoooooooOO + o0000o0o0000o * i1IIi + iIii1I11I1II1 % OOoO
if 59 - 59: ooO + i11iIiiIii
if 88 - 88: i11iIiiIii - Ii1Ii1iiii11
if 67 - 67: ooO . O00oOoOoO0o0O + Oo0ooO0oo0oO - OoooooooOO
if 70 - 70: ooO / II111iiii - iIii1I11I1II1 - i1
if 11 - 11: iIii1I11I1II1 . OoooooooOO . II111iiii / i1IIi - OOoO
if 30 - 30: Oo0ooO0oo0oO
if 21 - 21: i11iIiiIii / o0000o0o0000o % ooO * O0 . OOoO - iIii1I11I1II1
if 26 - 26: II111iiii * Oo0ooO0oo0oO
if 10 - 10: II111iiii . i1
if 32 - 32: ooo0Oo0 . OOooo0000ooo . OoooooooOO - O0oo0OO0 + i11Ii11I1Ii1i
if 88 - 88: i1
if 19 - 19: II111iiii * OOooo0000ooo + ooo0Oo0
if 65 - 65: ooO . o0000o0o0000o . O0oo0OO0 . i1 - ooO
if 19 - 19: i11iIiiIii + i1 % Ii1Ii1iiii11
if 14 - 14: O0oo0OO0 . II111iiii . OOoO / ooo0Oo0 % II - Ii1Ii1iiii11
if 67 - 67: OOoO - ooO . i1IIi
if 35 - 35: i1 + Ii1Ii1iiii11 - i11Ii11I1Ii1i . i1 . OOooo0000ooo
if 87 - 87: Oo0ooO0oo0oO
if 25 - 25: i1IIi . O0oo0OO0 - Oo0ooO0oo0oO / O0oo0OO0 % O0oo0OO0 * iIii1I11I1II1
if 50 - 50: O0oo0OO0 . i11iIiiIii - i11Ii11I1Ii1i . i11Ii11I1Ii1i
if 31 - 31: ooO / O00oOoOoO0o0O * i1IIi . Oo0ooO0oo0oO
if 57 - 57: ooO + iIii1I11I1II1 % i1IIi % iii1I1I
if 83 - 83: I1i1iI1i / i11iIiiIii % iIii1I11I1II1 . OOoO % i11Ii11I1Ii1i . OoooooooOO
if 94 - 94: ooo0Oo0 + iIii1I11I1II1 % O0oo0OO0
if 93 - 93: ooo0Oo0 - ooO + iIii1I11I1II1 * I1i1iI1i + o0000o0o0000o . i1
if 49 - 49: OoooooooOO * OOoO - O00oOoOoO0o0O . i11Ii11I1Ii1i
if 89 - 89: Ii1Ii1iiii11 + ooo0Oo0 * Ii1Ii1iiii11 / Ii1Ii1iiii11
if 46 - 46: O0oo0OO0
if 71 - 71: OOoO / OOoO * i11Ii11I1Ii1i * i11Ii11I1Ii1i / II111iiii
if 35 - 35: ooO * I1i1iI1i * iii1I1I % O00oOoOoO0o0O . Oo0ooO0oo0oO
if 58 - 58: OOoO + II111iiii * i1 * i11iIiiIii - iIii1I11I1II1
if 68 - 68: OoooooooOO % II111iiii
if 26 - 26: II111iiii % i11iIiiIii % iIii1I11I1II1 % OOoO * OOoO * II
if 24 - 24: II111iiii % o0000o0o0000o - Ii1Ii1iiii11 + iii1I1I * II
if 2 - 2: ooo0Oo0 - OOooo0000ooo
if 83 - 83: i11Ii11I1Ii1i % I1i1iI1i % ooo0Oo0 - II111iiii * ooO / OoooooooOO
if 18 - 18: O0oo0OO0 + iIii1I11I1II1 - II111iiii - iii1I1I
if 71 - 71: OoooooooOO
if 33 - 33: o0000o0o0000o
if 62 - 62: II + ooo0Oo0 + i1IIi / OoooooooOO
if 7 - 7: I1i1iI1i + i1IIi . iii1I1I / O00oOoOoO0o0O
if 22 - 22: Ii1Ii1iiii11 - Ii1Ii1iiii11 % ooO . o0000o0o0000o + i11Ii11I1Ii1i
if 63 - 63: iii1I1I % o0000o0o0000o * I1i1iI1i + o0000o0o0000o / O00oOoOoO0o0O % i1
if 45 - 45: OOooo0000ooo
if 20 - 20: OoooooooOO * I1i1iI1i * O0 . ooO
if 78 - 78: iIii1I11I1II1 + OOoO - ooo0Oo0 * o0000o0o0000o - OoooooooOO % Oo0ooO0oo0oO
if 34 - 34: O0
if 80 - 80: i1IIi - O00oOoOoO0o0O / O0oo0OO0 - i11iIiiIii
if 68 - 68: i11Ii11I1Ii1i - II % O0 % o0000o0o0000o
if 11 - 11: O0 / O0oo0OO0 % ooO + I1i1iI1i + iIii1I11I1II1
if 40 - 40: Ii1Ii1iiii11 - ooO . ooo0Oo0 * O00oOoOoO0o0O % o0000o0o0000o
if 56 - 56: i11iIiiIii . I1i1iI1i - iii1I1I * OOoO
if 91 - 91: i11Ii11I1Ii1i + OoooooooOO - i1IIi
if 84 - 84: ooo0Oo0 / OOooo0000ooo
if 86 - 86: Oo0ooO0oo0oO * II111iiii - O0 . Oo0ooO0oo0oO % iIii1I11I1II1 / ooO
if 11 - 11: iii1I1I * i11Ii11I1Ii1i + II / II
if 37 - 37: i11iIiiIii + i1IIi
if 23 - 23: i1 + OOoO . Oo0ooO0oo0oO * iii1I1I + II
if 18 - 18: OOooo0000ooo * I1i1iI1i . OOooo0000ooo / O0
if 8 - 8: I1i1iI1i
if 4 - 4: II + II * Ii1Ii1iiii11 - Oo0ooO0oo0oO
if 78 - 78: ooo0Oo0 / II111iiii % Oo0ooO0oo0oO
if 52 - 52: ooO - i1 * i11Ii11I1Ii1i
if 17 - 17: OoooooooOO + ooO * OOoO * Oo0ooO0oo0oO
if 36 - 36: O0 + O00oOoOoO0o0O
if 5 - 5: O00oOoOoO0o0O * Oo0ooO0oo0oO
if 46 - 46: Ii1Ii1iiii11
if 33 - 33: i1 - II111iiii * OoooooooOO - O00oOoOoO0o0O - ooO
if 84 - 84: o0000o0o0000o + O00oOoOoO0o0O - Oo0ooO0oo0oO * Oo0ooO0oo0oO
if 61 - 61: OoooooooOO . i11Ii11I1Ii1i . OoooooooOO / O00oOoOoO0o0O
if 72 - 72: i1IIi
if 82 - 82: Oo0ooO0oo0oO + OoooooooOO / i11iIiiIii * II . OoooooooOO
if 63 - 63: II
if 6 - 6: Ii1Ii1iiii11 / II
if 57 - 57: OOoO
if 67 - 67: O0oo0OO0 . Ii1Ii1iiii11
if 87 - 87: i11Ii11I1Ii1i % ooo0Oo0
if 83 - 83: II111iiii - OOoO
if 35 - 35: i1IIi - iIii1I11I1II1 + i1IIi
if 86 - 86: iIii1I11I1II1 + Oo0ooO0oo0oO . i11iIiiIii - ooo0Oo0
if 51 - 51: Oo0ooO0oo0oO
if 14 - 14: OOooo0000ooo % i11Ii11I1Ii1i % O00oOoOoO0o0O - i11iIiiIii
if 53 - 53: ooo0Oo0 % O00oOoOoO0o0O
if 59 - 59: ooO % iIii1I11I1II1 . i1IIi + II111iiii * OOooo0000ooo
if 41 - 41: ooo0Oo0 % II
if 12 - 12: ooO
if 69 - 69: OoooooooOO + ooO
if 26 - 26: O00oOoOoO0o0O + ooO / O0oo0OO0 % Oo0ooO0oo0oO % II + II111iiii
if 31 - 31: OOoO % ooO * OOoO
if 45 - 45: i1IIi . iii1I1I + ooO - OoooooooOO % Ii1Ii1iiii11
if 1 - 1: iIii1I11I1II1
if 93 - 93: i1IIi . i11iIiiIii . O00oOoOoO0o0O
if 99 - 99: OOoO - o0000o0o0000o - i11Ii11I1Ii1i % O0oo0OO0
if 21 - 21: II111iiii % II . i1IIi - OoooooooOO
if 4 - 4: OoooooooOO . Ii1Ii1iiii11
if 78 - 78: II + OOoO - O0
if 10 - 10: o0000o0o0000o % iii1I1I
if 97 - 97: OoooooooOO - o0000o0o0000o
if 58 - 58: iIii1I11I1II1 + O0
if 30 - 30: Ii1Ii1iiii11 % i1 * ooO - II * ooo0Oo0 % Ii1Ii1iiii11
if 46 - 46: i11iIiiIii - O0 . i11Ii11I1Ii1i
if 100 - 100: iii1I1I / I1i1iI1i * i1 . O0 / ooO
if 83 - 83: o0000o0o0000o
if 48 - 48: II111iiii * ooO * o0000o0o0000o
if 50 - 50: OOooo0000ooo % i1IIi
if 21 - 21: OoooooooOO - iIii1I11I1II1
if 93 - 93: i11Ii11I1Ii1i - I1i1iI1i % Oo0ooO0oo0oO . Oo0ooO0oo0oO - Ii1Ii1iiii11
if 90 - 90: Ii1Ii1iiii11 + II111iiii * II / ooo0Oo0 . I1i1iI1i + I1i1iI1i
if 40 - 40: Ii1Ii1iiii11 / Oo0ooO0oo0oO % i11iIiiIii % II / iii1I1I
if 62 - 62: i1IIi - Oo0ooO0oo0oO
if 62 - 62: i1IIi + O00oOoOoO0o0O % OOooo0000ooo
if 28 - 28: II . i1IIi
if 10 - 10: O0oo0OO0 / O00oOoOoO0o0O
if 15 - 15: i1 . Oo0ooO0oo0oO / i1 * OOoO - iii1I1I % II
if 57 - 57: O0 % Oo0ooO0oo0oO % i11Ii11I1Ii1i
if 45 - 45: II + II111iiii * i11iIiiIii
if 13 - 13: OoooooooOO * i11Ii11I1Ii1i - ooo0Oo0 / ooO + OOoO + OOooo0000ooo
if 39 - 39: iIii1I11I1II1 - OoooooooOO
if 81 - 81: II - O0 * OoooooooOO
if 23 - 23: II111iiii / i11Ii11I1Ii1i
if 28 - 28: O00oOoOoO0o0O * Ii1Ii1iiii11 - O0oo0OO0
if 19 - 19: OOoO
if 67 - 67: O0 % iIii1I11I1II1 / OOooo0000ooo . i11iIiiIii - ooo0Oo0 + O0
if 27 - 27: ooO
if 89 - 89: II111iiii / i11Ii11I1Ii1i
if 14 - 14: ooO . iii1I1I * Ii1Ii1iiii11 + II111iiii - Ii1Ii1iiii11 + ooO
if 18 - 18: i11Ii11I1Ii1i - I1i1iI1i - iii1I1I - iii1I1I
if 54 - 54: O00oOoOoO0o0O + iii1I1I / i1 . iii1I1I * Oo0ooO0oo0oO
if 1 - 1: Oo0ooO0oo0oO * O0oo0OO0 . i1IIi / O00oOoOoO0o0O . II + O00oOoOoO0o0O
if 17 - 17: O00oOoOoO0o0O + O0oo0OO0 / ooo0Oo0 / i1 * ooO
if 29 - 29: O0oo0OO0 % OoooooooOO * i11Ii11I1Ii1i / II111iiii - i11Ii11I1Ii1i
if 19 - 19: i11iIiiIii
if 54 - 54: II111iiii . OOoO
if 73 - 73: Oo0ooO0oo0oO . iii1I1I
if 32 - 32: Oo0ooO0oo0oO * iii1I1I % Ii1Ii1iiii11 * ooo0Oo0 . O0
if 48 - 48: i1 * i1
if 13 - 13: ooo0Oo0 / OOoO + Oo0ooO0oo0oO . I1i1iI1i % Ii1Ii1iiii11
if 48 - 48: iii1I1I / i11iIiiIii - I1i1iI1i * i11Ii11I1Ii1i / OoooooooOO
if 89 - 89: iIii1I11I1II1 / iii1I1I - II111iiii / ooo0Oo0 . i11iIiiIii . ooo0Oo0
if 48 - 48: O0 + O0 . o0000o0o0000o - Ii1Ii1iiii11
if 63 - 63: i11Ii11I1Ii1i
if 71 - 71: i1IIi . ooo0Oo0 * i1 % OoooooooOO + ooO
if 36 - 36: OOooo0000ooo
if 49 - 49: ooO / OoooooooOO / iii1I1I
if 74 - 74: o0000o0o0000o % II
if 7 - 7: II111iiii
if 27 - 27: i11Ii11I1Ii1i . OoooooooOO + i11iIiiIii
if 86 - 86: OOoO / I1i1iI1i - I1i1iI1i + II + i11Ii11I1Ii1i
if 33 - 33: I1i1iI1i . i1 . OOooo0000ooo . i1IIi
if 49 - 49: II
if 84 - 84: OOoO - O00oOoOoO0o0O / O0 - o0000o0o0000o
if 21 - 21: O0 * O0 % II
if 94 - 94: OOoO + II111iiii % i11iIiiIii
if 8 - 8: Ii1Ii1iiii11 * O0
if 73 - 73: I1i1iI1i / i11Ii11I1Ii1i / OOoO / O0oo0OO0
if 11 - 11: Oo0ooO0oo0oO + OOooo0000ooo - OoooooooOO / O0oo0OO0
if 34 - 34: Ii1Ii1iiii11
if 45 - 45: Ii1Ii1iiii11 / O00oOoOoO0o0O / ooo0Oo0
if 44 - 44: II - ooo0Oo0 / II111iiii * O0oo0OO0 * O00oOoOoO0o0O
if 73 - 73: I1i1iI1i - iii1I1I * i1IIi / i11iIiiIii * ooO % II111iiii
if 56 - 56: OoooooooOO * O00oOoOoO0o0O . O00oOoOoO0o0O . II
if 24 - 24: O00oOoOoO0o0O . OOoO * ooo0Oo0 % i1 / ooO
if 58 - 58: iii1I1I - II % O0 . iii1I1I % O0oo0OO0 % OOooo0000ooo
if 87 - 87: i11Ii11I1Ii1i - i11iIiiIii
if 78 - 78: i11iIiiIii / iIii1I11I1II1 - I1i1iI1i
if 23 - 23: OOoO
if 40 - 40: I1i1iI1i - II111iiii / O00oOoOoO0o0O
if 14 - 14: II
if 5 - 5: I1i1iI1i . iIii1I11I1II1 % iIii1I11I1II1
if 56 - 56: OoooooooOO - OOoO - i1IIi
if 8 - 8: o0000o0o0000o / ooO . iii1I1I + II / i11iIiiIii
if 31 - 31: Ii1Ii1iiii11 - iIii1I11I1II1 + i1 . O00oOoOoO0o0O / OOooo0000ooo % iIii1I11I1II1
if 6 - 6: OOooo0000ooo * i11iIiiIii % iIii1I11I1II1 % i11iIiiIii + I1i1iI1i / i1IIi
if 53 - 53: OOoO + iIii1I11I1II1
if 70 - 70: II
if 67 - 67: OoooooooOO
if 29 - 29: O0 - i11iIiiIii - II111iiii + ooO * OOooo0000ooo
if 2 - 2: i1IIi - Ii1Ii1iiii11 + iii1I1I . I1i1iI1i * I1i1iI1i / Oo0ooO0oo0oO
if 93 - 93: i1IIi
if 53 - 53: OoooooooOO + O00oOoOoO0o0O + i11Ii11I1Ii1i
if 24 - 24: i1 - OOooo0000ooo - i1 * II . OoooooooOO / OOooo0000ooo
if 66 - 66: O00oOoOoO0o0O
if 97 - 97: i1IIi - OoooooooOO / o0000o0o0000o * iii1I1I
if 55 - 55: I1i1iI1i . i1
if 87 - 87: I1i1iI1i % iIii1I11I1II1
if 100 - 100: o0000o0o0000o . iii1I1I * o0000o0o0000o - iii1I1I . OOoO * ooo0Oo0
if 89 - 89: O0oo0OO0 + OOooo0000ooo * o0000o0o0000o
if 28 - 28: OoooooooOO . i11Ii11I1Ii1i % II / i1IIi / ooO
if 36 - 36: I1i1iI1i + OOoO - OOooo0000ooo + iIii1I11I1II1 + OoooooooOO
if 4 - 4: II111iiii . OOoO + ooo0Oo0 * o0000o0o0000o . Ii1Ii1iiii11
if 87 - 87: Oo0ooO0oo0oO / O0oo0OO0 / i11iIiiIii
if 74 - 74: i11Ii11I1Ii1i / II % I1i1iI1i
if 88 - 88: Oo0ooO0oo0oO - i11iIiiIii % I1i1iI1i * OOoO + II
if 52 - 52: II111iiii . iii1I1I + Oo0ooO0oo0oO % O0oo0OO0
if 62 - 62: I1i1iI1i
if 15 - 15: OOoO + ooo0Oo0 . ooO * O0oo0OO0 . Oo0ooO0oo0oO
if 18 - 18: i1IIi % II111iiii + o0000o0o0000o % ooo0Oo0
if 72 - 72: iIii1I11I1II1
if 45 - 45: O00oOoOoO0o0O - I1i1iI1i % o0000o0o0000o
if 38 - 38: o0000o0o0000o % ooO - OoooooooOO
if 87 - 87: O0oo0OO0 % iii1I1I
if 77 - 77: iIii1I11I1II1 - i1IIi . i11Ii11I1Ii1i
if 26 - 26: I1i1iI1i * OOooo0000ooo . i1IIi
if 59 - 59: O0 + i1IIi - I1i1iI1i
if 62 - 62: i11iIiiIii % ooO . OOooo0000ooo . ooO
if 84 - 84: i11iIiiIii * O0oo0OO0
if 18 - 18: ooO - ooo0Oo0 - Oo0ooO0oo0oO / o0000o0o0000o - O0
if 30 - 30: O0 + II + II111iiii
if 14 - 14: I1i1iI1i / ooO - iIii1I11I1II1 - i11Ii11I1Ii1i % Ii1Ii1iiii11
if 49 - 49: Ii1Ii1iiii11 * i11Ii11I1Ii1i / I1i1iI1i / O00oOoOoO0o0O * iIii1I11I1II1
if 57 - 57: Oo0ooO0oo0oO - i11Ii11I1Ii1i / Ii1Ii1iiii11 % i11iIiiIii
if 3 - 3: i1 . Ii1Ii1iiii11 % iii1I1I + II
if 64 - 64: i1IIi
if 29 - 29: I1i1iI1i / i11iIiiIii / iii1I1I % i11Ii11I1Ii1i % i11iIiiIii
if 18 - 18: ooO + o0000o0o0000o
if 80 - 80: i11Ii11I1Ii1i + I1i1iI1i * ooo0Oo0 + O0oo0OO0
if 75 - 75: OOoO / I1i1iI1i / ooO / OOooo0000ooo % Ii1Ii1iiii11 + II111iiii
if 4 - 4: i1 - O00oOoOoO0o0O - OOooo0000ooo - OOoO % i11iIiiIii / O0oo0OO0
if 50 - 50: Ii1Ii1iiii11 + i1IIi
if 31 - 31: ooo0Oo0
if 78 - 78: i11iIiiIii + I1i1iI1i + o0000o0o0000o / I1i1iI1i % iIii1I11I1II1 % OOooo0000ooo
if 83 - 83: iIii1I11I1II1 % Oo0ooO0oo0oO % I1i1iI1i % o0000o0o0000o . II % O0
if 47 - 47: I1i1iI1i
if 66 - 66: iii1I1I - OOooo0000ooo
if 33 - 33: iii1I1I / O0oo0OO0
if 12 - 12: II111iiii
if 2 - 2: i1IIi - iii1I1I + OOoO . II111iiii
if 25 - 25: i11Ii11I1Ii1i
if 34 - 34: Oo0ooO0oo0oO . iIii1I11I1II1 % O0
if 43 - 43: II - i1
if 70 - 70: i1 / ooO % Ii1Ii1iiii11 - ooo0Oo0
if 47 - 47: i1
if 92 - 92: ooO + Oo0ooO0oo0oO % i1IIi
if 23 - 23: o0000o0o0000o - ooO + ooo0Oo0 - Oo0ooO0oo0oO * Oo0ooO0oo0oO . O00oOoOoO0o0O
if 47 - 47: i11Ii11I1Ii1i % iIii1I11I1II1
if 11 - 11: iii1I1I % ooo0Oo0 - O0oo0OO0 - i11Ii11I1Ii1i + I1i1iI1i
if 98 - 98: i1 + ooo0Oo0 - O0oo0OO0
if 79 - 79: ooO / o0000o0o0000o . Oo0ooO0oo0oO - II
if 47 - 47: OoooooooOO % O0 * i1 . ooo0Oo0
if 38 - 38: O0 - OOooo0000ooo % o0000o0o0000o
if 64 - 64: iIii1I11I1II1
if 15 - 15: II + ooO / II / o0000o0o0000o
if 31 - 31: Ii1Ii1iiii11 + O0 + Ii1Ii1iiii11 . iIii1I11I1II1 + O00oOoOoO0o0O / I1i1iI1i
if 6 - 6: O00oOoOoO0o0O % OOooo0000ooo * OOoO / iii1I1I + O00oOoOoO0o0O
if 39 - 39: Oo0ooO0oo0oO - O00oOoOoO0o0O / i1 * OoooooooOO
if 100 - 100: O0 . OOoO . O0oo0OO0 + O0 * i11Ii11I1Ii1i
if 42 - 42: i11Ii11I1Ii1i % OoooooooOO + I1i1iI1i
if 56 - 56: OoooooooOO + II - i1
if 24 - 24: I1i1iI1i + Ii1Ii1iiii11 + OOoO - iIii1I11I1II1
if 49 - 49: OOoO . Ii1Ii1iiii11 * Oo0ooO0oo0oO % OOooo0000ooo . O0
if 48 - 48: O0 * ooo0Oo0 - O0 / ooo0Oo0 + Oo0ooO0oo0oO
if 52 - 52: O0oo0OO0 % ooo0Oo0 * II111iiii
if 4 - 4: OOoO % O0 - OoooooooOO + Ii1Ii1iiii11 . i11Ii11I1Ii1i % II111iiii
if 9 - 9: II111iiii * II111iiii . i11iIiiIii * iIii1I11I1II1
if 18 - 18: O0oo0OO0 . II111iiii % Oo0ooO0oo0oO % ooo0Oo0
if 87 - 87: iIii1I11I1II1 . OoooooooOO * Oo0ooO0oo0oO
if 100 - 100: O0oo0OO0 / i1IIi - iii1I1I % ooo0Oo0 - iIii1I11I1II1
if 17 - 17: OOoO / I1i1iI1i % O00oOoOoO0o0O
if 71 - 71: OOooo0000ooo . o0000o0o0000o . O0oo0OO0
if 68 - 68: i11iIiiIii % i11Ii11I1Ii1i * O0oo0OO0 * OOooo0000ooo * II111iiii + O0
if 66 - 66: OOoO % II % OoooooooOO
if 34 - 34: I1i1iI1i / i1 % O0 . O0oo0OO0 . i1IIi
if 29 - 29: O0 . o0000o0o0000o
if 66 - 66: i11Ii11I1Ii1i * iIii1I11I1II1 % iIii1I11I1II1 * OOooo0000ooo - Ii1Ii1iiii11 - OOooo0000ooo
if 70 - 70: o0000o0o0000o + i11Ii11I1Ii1i
if 93 - 93: o0000o0o0000o + ooo0Oo0
if 33 - 33: O0
if 78 - 78: O0 / II111iiii * O0oo0OO0
if 50 - 50: OoooooooOO - iIii1I11I1II1 + i1IIi % o0000o0o0000o - iIii1I11I1II1 % O0
if 58 - 58: OOooo0000ooo + iIii1I11I1II1
if 65 - 65: II111iiii - o0000o0o0000o % I1i1iI1i - Oo0ooO0oo0oO * i1 + ooo0Oo0
if 79 - 79: Ii1Ii1iiii11 . Oo0ooO0oo0oO % o0000o0o0000o - O00oOoOoO0o0O
if 69 - 69: Ii1Ii1iiii11 - I1i1iI1i . Ii1Ii1iiii11
if 9 - 9: i11Ii11I1Ii1i % i11iIiiIii / O00oOoOoO0o0O
if 20 - 20: i11Ii11I1Ii1i * O0 + OOoO - OoooooooOO . OOoO
if 60 - 60: I1i1iI1i . I1i1iI1i / i1
if 45 - 45: O0 . i11iIiiIii % i1 . Oo0ooO0oo0oO % OOooo0000ooo % iIii1I11I1II1
if 58 - 58: iIii1I11I1II1 . Oo0ooO0oo0oO - i11iIiiIii * iIii1I11I1II1 % i11iIiiIii / iii1I1I
if 80 - 80: II / iIii1I11I1II1 % Oo0ooO0oo0oO
if 80 - 80: O0oo0OO0 % i1
if 99 - 99: Ii1Ii1iiii11 / iIii1I11I1II1 - ooo0Oo0 * II % iii1I1I
if 13 - 13: O0oo0OO0
if 70 - 70: o0000o0o0000o + O0 . i11Ii11I1Ii1i * ooo0Oo0
if 2 - 2: OoooooooOO . ooO . OOooo0000ooo
if 42 - 42: ooO % i11Ii11I1Ii1i / O0oo0OO0 - i11Ii11I1Ii1i * i11iIiiIii
if 19 - 19: i11Ii11I1Ii1i * iii1I1I % i11iIiiIii
if 24 - 24: I1i1iI1i
if 10 - 10: I1i1iI1i % ooo0Oo0 / ooO
if 28 - 28: ooO % Ii1Ii1iiii11
if 48 - 48: i11iIiiIii % i11Ii11I1Ii1i
if 29 - 29: i1 + i11iIiiIii % OOoO
if 93 - 93: Oo0ooO0oo0oO % iIii1I11I1II1
if 90 - 90: iii1I1I - ooO / ooo0Oo0 / O0 / OOoO
if 87 - 87: Oo0ooO0oo0oO / OOooo0000ooo + iIii1I11I1II1
if 93 - 93: iIii1I11I1II1 + i11Ii11I1Ii1i % Ii1Ii1iiii11
if 21 - 21: ooO
if 6 - 6: OOooo0000ooo
if 46 - 46: OOooo0000ooo + i11Ii11I1Ii1i
if 79 - 79: OoooooooOO - OOooo0000ooo * OOooo0000ooo . Oo0ooO0oo0oO
if 100 - 100: II111iiii * OOoO % iii1I1I / II
if 90 - 90: II . Ii1Ii1iiii11 . Oo0ooO0oo0oO . ooo0Oo0
if 4 - 4: ooo0Oo0 + Oo0ooO0oo0oO % II / i11iIiiIii
if 74 - 74: II111iiii . O0 - iii1I1I + OOooo0000ooo % i11iIiiIii % Oo0ooO0oo0oO
if 78 - 78: ooo0Oo0 + Oo0ooO0oo0oO + OOooo0000ooo - OOooo0000ooo . i11iIiiIii / O0oo0OO0
if 27 - 27: ooo0Oo0 - O0 % OOoO * o0000o0o0000o . OOooo0000ooo % iIii1I11I1II1
if 37 - 37: OoooooooOO + O0 - i1IIi % Ii1Ii1iiii11
if 24 - 24: Oo0ooO0oo0oO
if 94 - 94: i1IIi * i1IIi % II111iiii + ooO
if 28 - 28: iii1I1I
if 49 - 49: OOoO . I1i1iI1i % i11Ii11I1Ii1i / ooo0Oo0
if 95 - 95: O0 * Oo0ooO0oo0oO * OOooo0000ooo . Ii1Ii1iiii11 / iIii1I11I1II1
if 28 - 28: OOooo0000ooo + i11Ii11I1Ii1i - Ii1Ii1iiii11 / iIii1I11I1II1 - iii1I1I
if 45 - 45: O0 / i1IIi * i11Ii11I1Ii1i * O0oo0OO0
if 35 - 35: II / i1 % iii1I1I + iIii1I11I1II1
if 79 - 79: Oo0ooO0oo0oO / Ii1Ii1iiii11
if 77 - 77: O00oOoOoO0o0O
if 46 - 46: o0000o0o0000o
if 72 - 72: i1 * ooO
if 67 - 67: i1IIi
if 5 - 5: II111iiii . OoooooooOO
if 57 - 57: iii1I1I
if 35 - 35: OoooooooOO - o0000o0o0000o / O0oo0OO0
if 50 - 50: Oo0ooO0oo0oO
if 33 - 33: OOoO
if 98 - 98: Oo0ooO0oo0oO % II111iiii
if 95 - 95: iIii1I11I1II1 - o0000o0o0000o - ooO + o0000o0o0000o % II . iii1I1I
if 41 - 41: O0 + i11Ii11I1Ii1i . i1IIi - II111iiii * I1i1iI1i . O0oo0OO0
if 68 - 68: I1i1iI1i
if 20 - 20: o0000o0o0000o - o0000o0o0000o
if 37 - 37: OOooo0000ooo
if 37 - 37: O00oOoOoO0o0O / OOooo0000ooo * O0
if 73 - 73: i1 * i1 / Ii1Ii1iiii11
if 43 - 43: II . i1IIi . OOooo0000ooo + O0 * ooo0Oo0 * O0
if 41 - 41: II + ooo0Oo0 % OoooooooOO . II + i1 . i1
if 31 - 31: i11iIiiIii + II111iiii . i1 * Oo0ooO0oo0oO
if 66 - 66: Oo0ooO0oo0oO + i1IIi % II111iiii . O0 * II % II
if 87 - 87: ooO + I1i1iI1i . i1 - OoooooooOO
if 6 - 6: iIii1I11I1II1 * OoooooooOO
if 28 - 28: O00oOoOoO0o0O * I1i1iI1i / o0000o0o0000o
if 52 - 52: O0 / I1i1iI1i % i1 * iii1I1I % ooO
if 69 - 69: II
if 83 - 83: I1i1iI1i
if 38 - 38: o0000o0o0000o + OoooooooOO . i1IIi
if 19 - 19: i1 - I1i1iI1i - ooo0Oo0 - Oo0ooO0oo0oO . i1 . o0000o0o0000o
if 48 - 48: i1 + OOooo0000ooo
if 60 - 60: OOoO + i1 . OOooo0000ooo / i1IIi . iIii1I11I1II1
if 14 - 14: ooO
if 79 - 79: ooo0Oo0
if 76 - 76: iIii1I11I1II1
if 80 - 80: iIii1I11I1II1 . O0 / ooo0Oo0 % ooo0Oo0
if 93 - 93: OoooooooOO * O00oOoOoO0o0O
if 10 - 10: o0000o0o0000o * OoooooooOO + OOoO - II / II . i11iIiiIii
if 22 - 22: o0000o0o0000o / I1i1iI1i
if 98 - 98: i1IIi
if 51 - 51: II + Ii1Ii1iiii11 + O00oOoOoO0o0O / i1IIi + i1IIi
if 12 - 12: iIii1I11I1II1 . ooo0Oo0 . II % iii1I1I . II111iiii . i11Ii11I1Ii1i
if 32 - 32: II + OOooo0000ooo / O0 / Oo0ooO0oo0oO * OoooooooOO % Ii1Ii1iiii11
if 50 - 50: O0oo0OO0
if 66 - 66: iIii1I11I1II1
if 41 - 41: o0000o0o0000o . O0 * iii1I1I * II
if 100 - 100: i1
if 73 - 73: II % II111iiii
if 79 - 79: Oo0ooO0oo0oO + O0oo0OO0 - II111iiii + ooo0Oo0
if 11 - 11: i11Ii11I1Ii1i + iIii1I11I1II1
if 10 - 10: O0
if 68 - 68: ooO + i11Ii11I1Ii1i . O0 . ooo0Oo0 % i1IIi % ooO
if 50 - 50: OOooo0000ooo + I1i1iI1i
if 96 - 96: O0oo0OO0
if 92 - 92: O00oOoOoO0o0O / i11iIiiIii + II
if 87 - 87: Oo0ooO0oo0oO % iIii1I11I1II1
if 72 - 72: ooO . ooO - II
if 48 - 48: O00oOoOoO0o0O - Ii1Ii1iiii11 + O00oOoOoO0o0O - iii1I1I * i11iIiiIii . i1
if 35 - 35: OOooo0000ooo . O0 + O00oOoOoO0o0O + ooO + i1IIi
if 65 - 65: O0 * iii1I1I / iii1I1I . Oo0ooO0oo0oO
if 87 - 87: II111iiii * II % O00oOoOoO0o0O * O00oOoOoO0o0O
if 58 - 58: ooO . I1i1iI1i + iii1I1I % O00oOoOoO0o0O - O0oo0OO0
if 50 - 50: i1 % II111iiii - Ii1Ii1iiii11 . i1IIi + O0 % i1
if 10 - 10: i1 . i1IIi + ooo0Oo0
if 66 - 66: O0oo0OO0 % I1i1iI1i
if 21 - 21: Oo0ooO0oo0oO - OoooooooOO % i11iIiiIii
if 71 - 71: i1IIi - OOoO * o0000o0o0000o + i11Ii11I1Ii1i - O0oo0OO0 % II
if 63 - 63: iIii1I11I1II1 + ooO . O0oo0OO0 / iii1I1I
if 84 - 84: i1IIi
if 42 - 42: II111iiii - O0oo0OO0 - OoooooooOO . i1 / Oo0ooO0oo0oO
if 56 - 56: i11iIiiIii - iIii1I11I1II1 . II111iiii
if 81 - 81: OOooo0000ooo / Oo0ooO0oo0oO * OOooo0000ooo . O0
if 61 - 61: O0oo0OO0 * ooO + o0000o0o0000o . iIii1I11I1II1 % OOoO . o0000o0o0000o
if 53 - 53: o0000o0o0000o * OOooo0000ooo / iIii1I11I1II1 / iii1I1I % II
if 39 - 39: O0oo0OO0 / OoooooooOO . O0oo0OO0 * II / Oo0ooO0oo0oO
if 38 - 38: O0oo0OO0 / Ii1Ii1iiii11 % o0000o0o0000o * OOoO + i11iIiiIii % Ii1Ii1iiii11
if 61 - 61: o0000o0o0000o - ooo0Oo0 % II / Ii1Ii1iiii11 / i1 + iIii1I11I1II1
if 87 - 87: o0000o0o0000o + Ii1Ii1iiii11 + O0 / i1IIi % OOooo0000ooo / o0000o0o0000o
if 64 - 64: O0oo0OO0 % OOooo0000ooo . o0000o0o0000o % O0oo0OO0 + OOoO * OOooo0000ooo
if 83 - 83: I1i1iI1i % i11Ii11I1Ii1i + OOoO % i11iIiiIii + O0
if 65 - 65: iIii1I11I1II1 % i11Ii11I1Ii1i + O0 / OoooooooOO
if 52 - 52: ooo0Oo0 % ooO * iii1I1I % OOoO + ooO / i1
if 80 - 80: OoooooooOO + OOooo0000ooo
if 95 - 95: o0000o0o0000o / i11Ii11I1Ii1i * o0000o0o0000o - OoooooooOO * OoooooooOO % O0oo0OO0
if 43 - 43: O00oOoOoO0o0O . o0000o0o0000o
if 12 - 12: o0000o0o0000o + ooO + OOoO . OOooo0000ooo / ooo0Oo0
if 29 - 29: OOooo0000ooo . Ii1Ii1iiii11 - II111iiii
if 68 - 68: iIii1I11I1II1 + II111iiii / i11Ii11I1Ii1i
if 91 - 91: Oo0ooO0oo0oO % iIii1I11I1II1 . iii1I1I
if 70 - 70: OOoO % II111iiii % O0 . i1IIi / o0000o0o0000o
if 100 - 100: II * i11iIiiIii % i11Ii11I1Ii1i / O00oOoOoO0o0O / Ii1Ii1iiii11 + II
if 59 - 59: o0000o0o0000o - OOooo0000ooo
if 14 - 14: iIii1I11I1II1 - iIii1I11I1II1
if 5 - 5: OOooo0000ooo
if 84 - 84: II111iiii * i11Ii11I1Ii1i * II111iiii % OOooo0000ooo / iii1I1I
if 100 - 100: OOooo0000ooo . ooo0Oo0 - iIii1I11I1II1 . i11iIiiIii / II111iiii
if 71 - 71: o0000o0o0000o * O00oOoOoO0o0O . OOoO
if 49 - 49: OOooo0000ooo * O0 . OOooo0000ooo
if 19 - 19: II111iiii - OOooo0000ooo
if 59 - 59: I1i1iI1i * O0oo0OO0 - ooo0Oo0 . ooO
if 89 - 89: ooO
if 69 - 69: Ii1Ii1iiii11 - OoooooooOO * O0
if 84 - 84: Ii1Ii1iiii11 + i11iIiiIii - ooO * Ii1Ii1iiii11
if 33 - 33: Ii1Ii1iiii11 % i1IIi - i11Ii11I1Ii1i . O0 / O0
if 96 - 96: OoooooooOO + OOooo0000ooo * O0
if 86 - 86: ooo0Oo0
if 29 - 29: iIii1I11I1II1 - O0oo0OO0 + iii1I1I % iIii1I11I1II1 % ooO
if 84 - 84: OOooo0000ooo + II + ooo0Oo0 + i1
if 62 - 62: i11iIiiIii + Oo0ooO0oo0oO + i1IIi
if 69 - 69: Oo0ooO0oo0oO
if 63 - 63: O0oo0OO0 / Oo0ooO0oo0oO * iIii1I11I1II1 . o0000o0o0000o
if 85 - 85: i11iIiiIii / i11iIiiIii . O0oo0OO0 . O0
if 67 - 67: II111iiii / I1i1iI1i . ooO . OoooooooOO
if 19 - 19: OOooo0000ooo . II / Oo0ooO0oo0oO
if 68 - 68: Ii1Ii1iiii11 / OoooooooOO * OOoO / i11Ii11I1Ii1i
if 88 - 88: I1i1iI1i
if 1 - 1: OoooooooOO
if 48 - 48: Ii1Ii1iiii11 * Oo0ooO0oo0oO - Ii1Ii1iiii11 - ooO + ooO
if 40 - 40: i11iIiiIii . iIii1I11I1II1
if 2 - 2: i1IIi * i11Ii11I1Ii1i - i11Ii11I1Ii1i + OoooooooOO % Oo0ooO0oo0oO / Oo0ooO0oo0oO
if 3 - 3: OoooooooOO
if 71 - 71: OOooo0000ooo + i1IIi - i1 - i11iIiiIii . OOoO - Ii1Ii1iiii11
if 85 - 85: II - Oo0ooO0oo0oO / II + ooO - i1
if 49 - 49: O0oo0OO0 - O0 / O0oo0OO0 * Oo0ooO0oo0oO + o0000o0o0000o
if 35 - 35: II111iiii . iii1I1I / i1IIi / iii1I1I * i11Ii11I1Ii1i
if 85 - 85: II111iiii . Ii1Ii1iiii11 % ooO % OOoO
if 80 - 80: i11Ii11I1Ii1i * OOoO / iIii1I11I1II1 % i11Ii11I1Ii1i / iIii1I11I1II1
if 42 - 42: i1IIi / i11iIiiIii . O00oOoOoO0o0O * i1 . i11iIiiIii * O0
if 44 - 44: i1IIi . iii1I1I / i11iIiiIii + OOooo0000ooo
if 27 - 27: ooO
if 52 - 52: o0000o0o0000o % Oo0ooO0oo0oO + iIii1I11I1II1 * i11Ii11I1Ii1i . ooo0Oo0
if 95 - 95: iIii1I11I1II1 . OOooo0000ooo - OoooooooOO * O0oo0OO0 / I1i1iI1i
if 74 - 74: i11Ii11I1Ii1i
if 34 - 34: i1
if 44 - 44: i1IIi % iii1I1I % I1i1iI1i
if 9 - 9: O00oOoOoO0o0O % OoooooooOO - ooo0Oo0
if 43 - 43: O0oo0OO0 % O0oo0OO0
if 46 - 46: O00oOoOoO0o0O % iIii1I11I1II1 . i1 . O0 * Ii1Ii1iiii11 / OoooooooOO
if 7 - 7: i11Ii11I1Ii1i - O0 * OOoO - I1i1iI1i - II111iiii
if 41 - 41: iii1I1I - o0000o0o0000o % II111iiii . o0000o0o0000o - OOoO
if 45 - 45: ooo0Oo0 - ooO
if 70 - 70: O0oo0OO0 % iii1I1I / iii1I1I . OOoO % Ii1Ii1iiii11 . II111iiii
if 10 - 10: ooo0Oo0 - i11iIiiIii . II % i1IIi
if 78 - 78: iIii1I11I1II1 * O00oOoOoO0o0O . O00oOoOoO0o0O - ooO . iIii1I11I1II1
if 30 - 30: Ii1Ii1iiii11 + Ii1Ii1iiii11 % OOooo0000ooo - I1i1iI1i - II
if 36 - 36: OOoO % ooO
if 72 - 72: iii1I1I / i1 - O0 + OOoO
if 83 - 83: O0
if 89 - 89: O00oOoOoO0o0O + II - I1i1iI1i
if 40 - 40: O0oo0OO0 + O0oo0OO0
if 94 - 94: i1 * iIii1I11I1II1 . OOoO
if 13 - 13: iIii1I11I1II1 * Oo0ooO0oo0oO / o0000o0o0000o % Ii1Ii1iiii11 + i11Ii11I1Ii1i
if 41 - 41: II
if 5 - 5: O00oOoOoO0o0O
if 100 - 100: ooo0Oo0 + iIii1I11I1II1
if 59 - 59: OOooo0000ooo
if 89 - 89: Oo0ooO0oo0oO % iIii1I11I1II1
if 35 - 35: II + o0000o0o0000o - Oo0ooO0oo0oO % i11Ii11I1Ii1i % I1i1iI1i % Oo0ooO0oo0oO
if 45 - 45: iii1I1I * ooO % O0oo0OO0
if 24 - 24: Ii1Ii1iiii11 - OOoO * i11Ii11I1Ii1i
if 87 - 87: ooo0Oo0 - II % II . i11Ii11I1Ii1i / II
if 6 - 6: Oo0ooO0oo0oO / iIii1I11I1II1 * OoooooooOO * i11iIiiIii
if 79 - 79: OOooo0000ooo % O0oo0OO0
if 81 - 81: i11iIiiIii + i11iIiiIii * O0oo0OO0 + OOooo0000ooo
if 32 - 32: O0 . OoooooooOO
if 15 - 15: iii1I1I . O0oo0OO0
if 17 - 17: i11iIiiIii / O00oOoOoO0o0O . O0oo0OO0 / iii1I1I
if 38 - 38: i1IIi . II % ooo0Oo0 + iIii1I11I1II1 + O0
if 47 - 47: O0oo0OO0 + OOooo0000ooo / II111iiii
if 97 - 97: II / iii1I1I % O0 + i1IIi - Ii1Ii1iiii11
if 38 - 38: I1i1iI1i % o0000o0o0000o + i11iIiiIii + i1 + Ii1Ii1iiii11 / i11iIiiIii
if 94 - 94: i1 - O00oOoOoO0o0O + i11Ii11I1Ii1i
if 59 - 59: OOoO . iii1I1I - iIii1I11I1II1 + iIii1I11I1II1
if 56 - 56: i11Ii11I1Ii1i + Ii1Ii1iiii11
if 32 - 32: II111iiii + Oo0ooO0oo0oO % Ii1Ii1iiii11 / Oo0ooO0oo0oO + II
if 2 - 2: i11iIiiIii - o0000o0o0000o + O0oo0OO0 % OOoO * ooo0Oo0
if 54 - 54: O0 - i1 . ooO % i1 + i1
if 36 - 36: ooO % i11iIiiIii
if 47 - 47: i1IIi + II111iiii . O00oOoOoO0o0O * i11Ii11I1Ii1i . OOoO / i1IIi
if 50 - 50: o0000o0o0000o / i1IIi % OoooooooOO
if 83 - 83: II * II + ooO
if 57 - 57: O0 - O0 . II / I1i1iI1i / ooo0Oo0
if 20 - 20: ooO * II111iiii - Oo0ooO0oo0oO - i11Ii11I1Ii1i * o0000o0o0000o
if 6 - 6: Ii1Ii1iiii11 + ooO / O00oOoOoO0o0O + OOooo0000ooo % II111iiii / O0oo0OO0
if 45 - 45: OoooooooOO
if 9 - 9: OOoO . O0oo0OO0 * i1IIi . OoooooooOO
if 32 - 32: Oo0ooO0oo0oO . II % iii1I1I - II111iiii
if 11 - 11: O0 + iii1I1I
if 80 - 80: i11Ii11I1Ii1i % i11Ii11I1Ii1i % O0 - i11iIiiIii . i1 / O0
if 13 - 13: iii1I1I + O0 - II % O00oOoOoO0o0O / ooo0Oo0 . i1IIi
if 60 - 60: O00oOoOoO0o0O . OOooo0000ooo % iii1I1I - o0000o0o0000o
if 79 - 79: OoooooooOO / II . O0
if 79 - 79: i11Ii11I1Ii1i - II111iiii
if 43 - 43: i1IIi + O0 % O0oo0OO0 / ooo0Oo0 * iii1I1I
if 89 - 89: iii1I1I . O00oOoOoO0o0O + II . O0 % I1i1iI1i
if 84 - 84: OoooooooOO + o0000o0o0000o / iii1I1I % ooO % II * iii1I1I
if 58 - 58: O0oo0OO0 - Oo0ooO0oo0oO . i11iIiiIii % i11iIiiIii / i1IIi / i11Ii11I1Ii1i
if 24 - 24: iii1I1I * i1IIi % Ii1Ii1iiii11 / O0 + i11iIiiIii
if 12 - 12: II / ooo0Oo0
if 5 - 5: OoooooooOO
if 18 - 18: iii1I1I % OoooooooOO - i1 . i11iIiiIii * O00oOoOoO0o0O % ooo0Oo0
if 12 - 12: i1IIi / ooO % Ii1Ii1iiii11 * OOooo0000ooo * O0 * iIii1I11I1II1
if 93 - 93: O00oOoOoO0o0O / II + i1IIi * i11Ii11I1Ii1i . OoooooooOO
if 54 - 54: O0 / OOooo0000ooo % Ii1Ii1iiii11 * i1IIi * O0
if 48 - 48: I1i1iI1i . i11Ii11I1Ii1i % Oo0ooO0oo0oO - Oo0ooO0oo0oO
if 33 - 33: OOoO % II111iiii + O0oo0OO0
if 93 - 93: i1IIi . OOooo0000ooo / iii1I1I + OOooo0000ooo
if 58 - 58: II + O0 . O00oOoOoO0o0O + Oo0ooO0oo0oO - O0oo0OO0 - Oo0ooO0oo0oO
if 41 - 41: O00oOoOoO0o0O / i1IIi / O00oOoOoO0o0O - i1 . I1i1iI1i
if 65 - 65: O0 * i11iIiiIii . OoooooooOO / iii1I1I / i1
if 69 - 69: Ii1Ii1iiii11 % Ii1Ii1iiii11
if 76 - 76: i11iIiiIii * i1 / O0oo0OO0 % II + ooO
if 48 - 48: iIii1I11I1II1 % i1IIi + Oo0ooO0oo0oO % I1i1iI1i
if 79 - 79: Oo0ooO0oo0oO % iii1I1I % ooo0Oo0 / i1IIi % O0oo0OO0
if 56 - 56: iIii1I11I1II1 - i11iIiiIii * i1
if 84 - 84: ooO + ooo0Oo0 + I1i1iI1i
if 33 - 33: ooo0Oo0
if 93 - 93: Ii1Ii1iiii11
if 34 - 34: i11Ii11I1Ii1i - Ii1Ii1iiii11 * O00oOoOoO0o0O / I1i1iI1i
if 19 - 19: II
if 46 - 46: iIii1I11I1II1 . i11iIiiIii - Oo0ooO0oo0oO % O0 / II111iiii * i1IIi
if 66 - 66: O0
if 52 - 52: O0oo0OO0 * OoooooooOO
if 12 - 12: O0 + OOooo0000ooo * i1IIi . O0oo0OO0
if 71 - 71: o0000o0o0000o - I1i1iI1i - ooO
if 28 - 28: iIii1I11I1II1
if 7 - 7: I1i1iI1i % OOooo0000ooo * Oo0ooO0oo0oO
if 58 - 58: OOooo0000ooo / OOoO + II111iiii % i1 - OoooooooOO
if 25 - 25: Oo0ooO0oo0oO % OoooooooOO * O00oOoOoO0o0O - i1IIi * II111iiii * i11Ii11I1Ii1i
if 30 - 30: OOoO % Oo0ooO0oo0oO / II * O0 * ooo0Oo0 . iii1I1I
if 46 - 46: Oo0ooO0oo0oO - O0
if 70 - 70: OOoO + O00oOoOoO0o0O * iIii1I11I1II1 . iii1I1I * OOoO
if 49 - 49: I1i1iI1i
if 25 - 25: i1 . OoooooooOO * iIii1I11I1II1 . I1i1iI1i / O0 + ooo0Oo0
if 68 - 68: O00oOoOoO0o0O
if 22 - 22: ooO
if 22 - 22: i1 * OOoO - O00oOoOoO0o0O * O0 / i11iIiiIii
if 78 - 78: O00oOoOoO0o0O * O0 / Ii1Ii1iiii11 + OoooooooOO + ooO
if 23 - 23: i1 % OoooooooOO / iIii1I11I1II1 + II / i1IIi / I1i1iI1i
if 94 - 94: i1IIi
if 36 - 36: iii1I1I + O00oOoOoO0o0O
if 46 - 46: i1
if 65 - 65: i1IIi . II / Ii1Ii1iiii11
if 11 - 11: OOooo0000ooo * Ii1Ii1iiii11 / Ii1Ii1iiii11 - ooO
if 68 - 68: iii1I1I % OOooo0000ooo - OOooo0000ooo / iii1I1I + II - O00oOoOoO0o0O
if 65 - 65: Ii1Ii1iiii11 - i1IIi
if 62 - 62: OOoO / i11Ii11I1Ii1i % O00oOoOoO0o0O . OoooooooOO / i11iIiiIii / o0000o0o0000o
if 60 - 60: iii1I1I % i11Ii11I1Ii1i / I1i1iI1i % i11Ii11I1Ii1i * i11iIiiIii / i1
if 34 - 34: o0000o0o0000o - ooO
if 25 - 25: i11Ii11I1Ii1i % iii1I1I + i11iIiiIii + O0 * OoooooooOO
if 64 - 64: i1IIi
if 10 - 10: o0000o0o0000o % O0 / iii1I1I % OOoO
if 25 - 25: II111iiii / O0oo0OO0
if 64 - 64: O0 % Ii1Ii1iiii11
if 40 - 40: I1i1iI1i + OOoO
if 77 - 77: i11iIiiIii % OOooo0000ooo + o0000o0o0000o % OoooooooOO - OOoO
if 26 - 26: O00oOoOoO0o0O + O0 - iIii1I11I1II1
if 47 - 47: OoooooooOO
if 2 - 2: Oo0ooO0oo0oO % o0000o0o0000o * O00oOoOoO0o0O * Oo0ooO0oo0oO
if 65 - 65: i11iIiiIii + O00oOoOoO0o0O * OoooooooOO - O0oo0OO0
if 26 - 26: I1i1iI1i % ooO + ooO % OOoO * i11iIiiIii / i1
if 64 - 64: i11Ii11I1Ii1i % Oo0ooO0oo0oO / II111iiii % Ii1Ii1iiii11 - i1
if 2 - 2: o0000o0o0000o - II + I1i1iI1i * O0oo0OO0 / i1
if 26 - 26: ooO * O00oOoOoO0o0O
if 31 - 31: OOoO * i11Ii11I1Ii1i . ooo0Oo0
if 35 - 35: OOoO
if 94 - 94: Ii1Ii1iiii11 / i11iIiiIii % O0
if 70 - 70: OOoO - O00oOoOoO0o0O / OoooooooOO % OoooooooOO
if 95 - 95: OoooooooOO % OoooooooOO . ooo0Oo0
if 26 - 26: i11Ii11I1Ii1i + OOooo0000ooo - II111iiii . II111iiii + II + Oo0ooO0oo0oO
if 68 - 68: O0
if 76 - 76: II
if 99 - 99: I1i1iI1i
if 1 - 1: ooo0Oo0 * Oo0ooO0oo0oO * O0oo0OO0 + O00oOoOoO0o0O
if 90 - 90: o0000o0o0000o % O00oOoOoO0o0O - O00oOoOoO0o0O . iIii1I11I1II1 / ooO + OOoO
if 89 - 89: i11Ii11I1Ii1i
if 87 - 87: i1 % O00oOoOoO0o0O
if 62 - 62: O0oo0OO0 + Ii1Ii1iiii11 / i1 * i11iIiiIii
if 37 - 37: i1
if 33 - 33: O0oo0OO0 - O0 - O0oo0OO0
if 94 - 94: OOooo0000ooo * OOoO * OoooooooOO / I1i1iI1i . OOooo0000ooo - I1i1iI1i
if 13 - 13: ooO / OOooo0000ooo - O0oo0OO0 / ooO . i1IIi
if 22 - 22: O0 - OOoO + o0000o0o0000o . ooo0Oo0 * i1IIi
if 26 - 26: iIii1I11I1II1 * I1i1iI1i . OOoO
if 10 - 10: o0000o0o0000o * i11Ii11I1Ii1i % O00oOoOoO0o0O - OOoO % O00oOoOoO0o0O
if 65 - 65: i1 * iIii1I11I1II1 / O0 . OOoO
if 94 - 94: O00oOoOoO0o0O . Ii1Ii1iiii11 * i11iIiiIii - I1i1iI1i . i1
if 98 - 98: ooO + ooo0Oo0
if 52 - 52: O00oOoOoO0o0O / Oo0ooO0oo0oO - o0000o0o0000o . i1
if 50 - 50: iIii1I11I1II1 - i1 - OOoO
if 60 - 60: iIii1I11I1II1 * Ii1Ii1iiii11
if 71 - 71: Oo0ooO0oo0oO % O00oOoOoO0o0O % Ii1Ii1iiii11
if 34 - 34: OOoO / OOoO % OOooo0000ooo . Oo0ooO0oo0oO / O00oOoOoO0o0O
if 99 - 99: Ii1Ii1iiii11 * iii1I1I - Ii1Ii1iiii11 % ooo0Oo0
if 40 - 40: ooO / OOooo0000ooo / iIii1I11I1II1 + ooo0Oo0
if 59 - 59: OOoO * OoooooooOO + ooO . iIii1I11I1II1 / i1IIi
if 75 - 75: OOoO . ooO - iIii1I11I1II1 * O0oo0OO0 * i1
if 93 - 93: Ii1Ii1iiii11
if 18 - 18: Ii1Ii1iiii11
if 66 - 66: i11Ii11I1Ii1i * i11iIiiIii + Oo0ooO0oo0oO / ooO
if 96 - 96: ooO + ooO % OOooo0000ooo % ooO
if 28 - 28: iIii1I11I1II1 + Oo0ooO0oo0oO . I1i1iI1i % i11iIiiIii
if 58 - 58: OOoO / OoooooooOO % i11Ii11I1Ii1i + O0oo0OO0
if 58 - 58: O0
if 91 - 91: i1 / II . i1 - I1i1iI1i + II
if 72 - 72: ooo0Oo0 . OOooo0000ooo * II / II / i1
if 13 - 13: i1IIi
if 17 - 17: i11iIiiIii * I1i1iI1i * I1i1iI1i + O0oo0OO0
if 95 - 95: iii1I1I
if 95 - 95: ooO % II + I1i1iI1i % Ii1Ii1iiii11
if 36 - 36: O0 / i1IIi % II111iiii / i1
if 96 - 96: O00oOoOoO0o0O / i11Ii11I1Ii1i . II111iiii . O00oOoOoO0o0O
if 91 - 91: II111iiii . ooO + I1i1iI1i
if 8 - 8: ooO * O00oOoOoO0o0O / i1 - O0oo0OO0 - OoooooooOO
if 100 - 100: i11Ii11I1Ii1i . iIii1I11I1II1 . iIii1I11I1II1
if 55 - 55: i11Ii11I1Ii1i
if 37 - 37: OOooo0000ooo / i11iIiiIii / O00oOoOoO0o0O
if 97 - 97: o0000o0o0000o . OOoO / iii1I1I
if 83 - 83: OOoO - II * i11Ii11I1Ii1i
if 90 - 90: O00oOoOoO0o0O * iii1I1I
if 75 - 75: II - Oo0ooO0oo0oO * i11iIiiIii . OoooooooOO - O00oOoOoO0o0O . OOoO
if 6 - 6: OOoO * i11Ii11I1Ii1i / OoooooooOO % ooo0Oo0 * I1i1iI1i
if 28 - 28: OOooo0000ooo * iii1I1I % OOooo0000ooo
if 95 - 95: O0 / OOoO . o0000o0o0000o
if 17 - 17: OOoO
if 56 - 56: Ii1Ii1iiii11 * I1i1iI1i + OOoO
if 48 - 48: OOooo0000ooo * O0oo0OO0 % o0000o0o0000o - OOoO
if 72 - 72: i1IIi % Ii1Ii1iiii11 % OOooo0000ooo % i11Ii11I1Ii1i - i11Ii11I1Ii1i
if 97 - 97: I1i1iI1i * O0 / I1i1iI1i * O0oo0OO0 * O00oOoOoO0o0O
if 38 - 38: o0000o0o0000o
if 25 - 25: iIii1I11I1II1 % II111iiii / OOoO / II
if 22 - 22: i11Ii11I1Ii1i * i1
if 4 - 4: Oo0ooO0oo0oO - i11Ii11I1Ii1i + iii1I1I
if 36 - 36: OOooo0000ooo
if 19 - 19: Oo0ooO0oo0oO . I1i1iI1i . OoooooooOO
if 13 - 13: ooO . O00oOoOoO0o0O / II111iiii
if 43 - 43: iIii1I11I1II1 % O0oo0OO0
if 84 - 84: O00oOoOoO0o0O
if 44 - 44: OoooooooOO * i11iIiiIii / O00oOoOoO0o0O
if 75 - 75: OoooooooOO . ooO + O0oo0OO0 / ooo0Oo0 - iii1I1I % ooo0Oo0
if 89 - 89: i1 * iIii1I11I1II1 + i11iIiiIii . OoooooooOO
if 51 - 51: ooO / Ii1Ii1iiii11 + O0oo0OO0 % Oo0ooO0oo0oO / ooo0Oo0
if 25 - 25: I1i1iI1i
if 25 - 25: Ii1Ii1iiii11 * i1 / OOoO / OOoO % I1i1iI1i
if 19 - 19: i11Ii11I1Ii1i - iIii1I11I1II1 / Ii1Ii1iiii11 . O0oo0OO0 * O0 - O0
if 41 - 41: i1IIi - iii1I1I
if 48 - 48: iii1I1I - II111iiii / O0oo0OO0 + iii1I1I
if 5 - 5: O0
if 75 - 75: o0000o0o0000o + iIii1I11I1II1
if 19 - 19: iii1I1I + i11iIiiIii . OOooo0000ooo - OOoO / ooo0Oo0 + I1i1iI1i
if 38 - 38: O00oOoOoO0o0O / iIii1I11I1II1 * iIii1I11I1II1 % II
if 92 - 92: OOoO / O0 * iii1I1I - OOoO
if 99 - 99: i11iIiiIii % OoooooooOO
if 56 - 56: OOooo0000ooo * o0000o0o0000o
if 98 - 98: OOoO + O0 * o0000o0o0000o + i11iIiiIii - ooO - iIii1I11I1II1
if 5 - 5: ooO % O00oOoOoO0o0O % OOooo0000ooo % Ii1Ii1iiii11
if 17 - 17: ooo0Oo0 + II111iiii + OoooooooOO / ooO / OOooo0000ooo
if 80 - 80: I1i1iI1i % i1IIi / OOoO
if 56 - 56: i1IIi . i11iIiiIii
if 15 - 15: II111iiii * i11Ii11I1Ii1i % i1 / i11iIiiIii - i11Ii11I1Ii1i + O00oOoOoO0o0O
if 9 - 9: OOoO - i11Ii11I1Ii1i + O0 / i1 % i1IIi
if 97 - 97: I1i1iI1i * Ii1Ii1iiii11
if 78 - 78: OOoO . ooO + i11Ii11I1Ii1i * i1 - i1IIi
if 27 - 27: ooo0Oo0 % i1IIi . O00oOoOoO0o0O % o0000o0o0000o
if 10 - 10: OOooo0000ooo / OoooooooOO
if 50 - 50: i11iIiiIii - OoooooooOO . i11Ii11I1Ii1i + O0 . i1IIi
if 91 - 91: I1i1iI1i . i1 % O00oOoOoO0o0O - i1 . i11Ii11I1Ii1i % i11iIiiIii
if 25 - 25: iIii1I11I1II1
if 63 - 63: Ii1Ii1iiii11
if 96 - 96: OOoO
if 34 - 34: Oo0ooO0oo0oO / O0oo0OO0 - iii1I1I . O0 . ooO
if 63 - 63: i1
if 11 - 11: i1 - iIii1I11I1II1
if 92 - 92: O0oo0OO0
if 15 - 15: OOooo0000ooo / OOooo0000ooo + iIii1I11I1II1 % OoooooooOO
if 12 - 12: Ii1Ii1iiii11
if 36 - 36: o0000o0o0000o . OOooo0000ooo * OoooooooOO - I1i1iI1i
if 60 - 60: ooO . i1 / iIii1I11I1II1 + ooO * o0000o0o0000o
if 82 - 82: i11iIiiIii . iIii1I11I1II1 * iii1I1I - OOoO + ooo0Oo0
if 48 - 48: II
if 96 - 96: Ii1Ii1iiii11 . OoooooooOO
if 39 - 39: ooO + O0oo0OO0
if 80 - 80: ooO % O0oo0OO0 / Oo0ooO0oo0oO
if 54 - 54: O00oOoOoO0o0O % O0oo0OO0 - ooO - OOoO
if 71 - 71: Ii1Ii1iiii11 . i11iIiiIii
if 56 - 56: O0 * i1 + i1 * iIii1I11I1II1 / Ii1Ii1iiii11 * o0000o0o0000o
if 25 - 25: iIii1I11I1II1 . OOoO * i11iIiiIii + O00oOoOoO0o0O * OOoO
if 67 - 67: i1
if 88 - 88: O00oOoOoO0o0O
if 8 - 8: II
if 82 - 82: OoooooooOO
if 75 - 75: II111iiii % iii1I1I + ooO % OoooooooOO / OOooo0000ooo
if 4 - 4: i11iIiiIii - ooO % II * o0000o0o0000o % I1i1iI1i
if 71 - 71: Ii1Ii1iiii11 . Ii1Ii1iiii11 - iIii1I11I1II1
if 22 - 22: OoooooooOO / II % i1 * Oo0ooO0oo0oO
if 32 - 32: OoooooooOO % i11Ii11I1Ii1i % iIii1I11I1II1 / O0
if 61 - 61: II111iiii . O0 - ooo0Oo0 - II / i11iIiiIii - II111iiii
if 98 - 98: ooo0Oo0 - iii1I1I . i11iIiiIii * O00oOoOoO0o0O
if 29 - 29: ooo0Oo0 / Ii1Ii1iiii11 % OOoO
if 10 - 10: iIii1I11I1II1 % OoooooooOO % II
if 39 - 39: II111iiii * Oo0ooO0oo0oO . O0 * OOoO
if 89 - 89: ooo0Oo0 - Ii1Ii1iiii11 . OOoO - o0000o0o0000o - iii1I1I
if 79 - 79: OOooo0000ooo + OOooo0000ooo + ooo0Oo0
if 39 - 39: O0 - OoooooooOO
if 63 - 63: iIii1I11I1II1 % I1i1iI1i * Ii1Ii1iiii11
if 79 - 79: O0
if 32 - 32: II111iiii . O0 + ooo0Oo0 / Oo0ooO0oo0oO / OOooo0000ooo / ooO
if 15 - 15: II
if 4 - 4: OOooo0000ooo + iIii1I11I1II1 * i1 + O00oOoOoO0o0O * I1i1iI1i % II111iiii
if 88 - 88: i11Ii11I1Ii1i - i1IIi % i11iIiiIii % II111iiii * OoooooooOO
if 40 - 40: O00oOoOoO0o0O
if 47 - 47: Oo0ooO0oo0oO
if 65 - 65: O0 + o0000o0o0000o % ooo0Oo0 * iii1I1I / Ii1Ii1iiii11 / Oo0ooO0oo0oO
if 71 - 71: i11iIiiIii / Oo0ooO0oo0oO . i11Ii11I1Ii1i
if 33 - 33: i11Ii11I1Ii1i
if 39 - 39: O0oo0OO0 + O0 + Ii1Ii1iiii11 * II111iiii % O0 - O0
if 41 - 41: OOooo0000ooo % I1i1iI1i
if 67 - 67: O0 % o0000o0o0000o
if 35 - 35: iii1I1I . Oo0ooO0oo0oO + OoooooooOO % O00oOoOoO0o0O % ooO
if 39 - 39: ooo0Oo0
if 60 - 60: ooO
if 62 - 62: o0000o0o0000o * OOoO
if 74 - 74: Oo0ooO0oo0oO . iIii1I11I1II1
if 87 - 87: Ii1Ii1iiii11
if 41 - 41: Oo0ooO0oo0oO . iIii1I11I1II1 % Ii1Ii1iiii11 + O0
if 22 - 22: I1i1iI1i + O00oOoOoO0o0O . Ii1Ii1iiii11 + II * i1 . i11iIiiIii
if 90 - 90: ooO * Oo0ooO0oo0oO - O00oOoOoO0o0O + I1i1iI1i
if 53 - 53: OoooooooOO . OoooooooOO + I1i1iI1i - i1 + ooO
if 44 - 44: o0000o0o0000o - OOooo0000ooo
if 100 - 100: i11Ii11I1Ii1i . O0oo0OO0 - ooo0Oo0 + O0 * O0oo0OO0
if 59 - 59: II111iiii
if 43 - 43: O00oOoOoO0o0O + OoooooooOO
if 47 - 47: Ii1Ii1iiii11
if 92 - 92: OOoO % i11iIiiIii % O00oOoOoO0o0O
if 23 - 23: II111iiii * i1
if 80 - 80: o0000o0o0000o / i11iIiiIii + OoooooooOO
if 38 - 38: II % Ii1Ii1iiii11 + i1IIi * OoooooooOO * i11Ii11I1Ii1i
if 83 - 83: iIii1I11I1II1 - Ii1Ii1iiii11 - o0000o0o0000o / O0oo0OO0 - O0
if 81 - 81: ooo0Oo0 - i11Ii11I1Ii1i * II / o0000o0o0000o
if 21 - 21: O0oo0OO0
if 63 - 63: OOoO . O0 * OOoO + iIii1I11I1II1
if 46 - 46: i1IIi + II111iiii * i1IIi - ooo0Oo0
if 79 - 79: II111iiii - i11Ii11I1Ii1i * II - Oo0ooO0oo0oO . II
if 11 - 11: O0 * Oo0ooO0oo0oO
if 37 - 37: Oo0ooO0oo0oO + O0 . O0 * O00oOoOoO0o0O % o0000o0o0000o / i1
if 18 - 18: OoooooooOO
if 57 - 57: Ii1Ii1iiii11 . Oo0ooO0oo0oO * I1i1iI1i - OoooooooOO
if 75 - 75: i11iIiiIii / I1i1iI1i . OOooo0000ooo . i1IIi . i1IIi / OOoO
if 94 - 94: Ii1Ii1iiii11 + iii1I1I
if 56 - 56: Oo0ooO0oo0oO % I1i1iI1i
if 40 - 40: ooO / OOooo0000ooo
if 29 - 29: ooo0Oo0 - ooo0Oo0 / Ii1Ii1iiii11
if 49 - 49: OOoO + i11Ii11I1Ii1i % O0oo0OO0 - O00oOoOoO0o0O - O0 - OoooooooOO
if 4 - 4: II111iiii - i11Ii11I1Ii1i % O00oOoOoO0o0O * i11iIiiIii
if 18 - 18: O00oOoOoO0o0O % O0
if 66 - 66: iIii1I11I1II1 % i11iIiiIii / iii1I1I
if 47 - 47: II * i11Ii11I1Ii1i + iIii1I11I1II1 - i11Ii11I1Ii1i / OOooo0000ooo
if 86 - 86: OOooo0000ooo
if 43 - 43: iii1I1I / i1 / Ii1Ii1iiii11 + iIii1I11I1II1 + OoooooooOO
if 33 - 33: II111iiii - OOooo0000ooo - Ii1Ii1iiii11
if 92 - 92: O0oo0OO0 * OOooo0000ooo
if 92 - 92: i11Ii11I1Ii1i
if 7 - 7: i1
if 73 - 73: O0oo0OO0 % II
if 32 - 32: ooO + i1 + iIii1I11I1II1 * O00oOoOoO0o0O
if 62 - 62: i11iIiiIii
if 2 - 2: iii1I1I
if 69 - 69: OoooooooOO / O00oOoOoO0o0O * o0000o0o0000o
if 99 - 99: II111iiii * iIii1I11I1II1 % O0 * i11Ii11I1Ii1i / II111iiii % OoooooooOO
if 14 - 14: OOooo0000ooo . OOooo0000ooo % Ii1Ii1iiii11
if 42 - 42: I1i1iI1i . ooO - Ii1Ii1iiii11
if 33 - 33: II111iiii / O0 / OOooo0000ooo - OOoO - i1IIi
if 8 - 8: i11iIiiIii . i1 / iIii1I11I1II1 / II / OOooo0000ooo - ooo0Oo0
if 32 - 32: I1i1iI1i . i1IIi * O00oOoOoO0o0O
if 98 - 98: ooo0Oo0 - II111iiii / iii1I1I . i11Ii11I1Ii1i * OOooo0000ooo . OOoO
if 25 - 25: i11iIiiIii / Oo0ooO0oo0oO - o0000o0o0000o / O0oo0OO0 . I1i1iI1i . I1i1iI1i
if 6 - 6: i11Ii11I1Ii1i . OOoO
if 43 - 43: II + I1i1iI1i
if 50 - 50: i11Ii11I1Ii1i % i1IIi * O0
if 4 - 4: iIii1I11I1II1 . i1IIi
if 63 - 63: iIii1I11I1II1 + OOooo0000ooo % i1IIi / iii1I1I % II111iiii
if 60 - 60: I1i1iI1i . Oo0ooO0oo0oO % o0000o0o0000o / iii1I1I / O0
if 19 - 19: i11iIiiIii . iii1I1I + II111iiii / ooO . II * Ii1Ii1iiii11
if 59 - 59: iIii1I11I1II1 / II % Ii1Ii1iiii11
if 84 - 84: iIii1I11I1II1 / iii1I1I . Oo0ooO0oo0oO % OOoO
if 99 - 99: O00oOoOoO0o0O + i11iIiiIii
if 36 - 36: ooo0Oo0 * o0000o0o0000o * iIii1I11I1II1 - OOoO % i11iIiiIii
if 98 - 98: iIii1I11I1II1 - i1IIi + Ii1Ii1iiii11 % OOoO + Ii1Ii1iiii11 / i11Ii11I1Ii1i
if 97 - 97: OOooo0000ooo % Ii1Ii1iiii11 + II111iiii - OOooo0000ooo % O0oo0OO0 + Ii1Ii1iiii11
if 31 - 31: I1i1iI1i
if 35 - 35: Oo0ooO0oo0oO + ooo0Oo0 * Ii1Ii1iiii11 / Oo0ooO0oo0oO
if 69 - 69: Ii1Ii1iiii11 . ooO - iii1I1I
if 29 - 29: i11iIiiIii . II / iii1I1I . ooO + i11iIiiIii
if 26 - 26: OOooo0000ooo / ooo0Oo0 - OoooooooOO
if 9 - 9: OoooooooOO * II
if 9 - 9: O00oOoOoO0o0O + i1
if 64 - 64: O0 * iii1I1I / iii1I1I
if 57 - 57: II / OoooooooOO % II . O0 / II
if 63 - 63: OOooo0000ooo + iIii1I11I1II1 + iii1I1I + o0000o0o0000o
if 72 - 72: O0oo0OO0 + i11iIiiIii + II
if 96 - 96: i11Ii11I1Ii1i % i1IIi / I1i1iI1i
if 13 - 13: II111iiii - O00oOoOoO0o0O % i11iIiiIii + i1
if 88 - 88: O0 . i11Ii11I1Ii1i % iii1I1I
if 10 - 10: iii1I1I + O0
if 75 - 75: O0 % iIii1I11I1II1 / Oo0ooO0oo0oO % ooO / OOooo0000ooo
if 31 - 31: i11iIiiIii * Oo0ooO0oo0oO
if 69 - 69: i11iIiiIii
if 61 - 61: O0
if 21 - 21: O0oo0OO0 % iIii1I11I1II1 . O0oo0OO0
if 99 - 99: I1i1iI1i * ooO % i11Ii11I1Ii1i * i11Ii11I1Ii1i + OoooooooOO
if 82 - 82: OOoO / Oo0ooO0oo0oO - ooO / Ii1Ii1iiii11
if 50 - 50: ooO + O0oo0OO0 . i11iIiiIii + II + i11iIiiIii
if 31 - 31: i11Ii11I1Ii1i * o0000o0o0000o . Oo0ooO0oo0oO * OOoO
if 28 - 28: OOooo0000ooo + iii1I1I - O00oOoOoO0o0O % ooO . OOoO + iii1I1I
if 72 - 72: ooo0Oo0 / O00oOoOoO0o0O / i11Ii11I1Ii1i * Oo0ooO0oo0oO + ooO
if 58 - 58: I1i1iI1i % iii1I1I . iii1I1I * O0oo0OO0 - OOooo0000ooo . OoooooooOO
if 10 - 10: o0000o0o0000o
if 48 - 48: i1 * i1IIi % OoooooooOO * ooo0Oo0 * O0oo0OO0
if 7 - 7: i1 . ooo0Oo0 . i1 - o0000o0o0000o
if 33 - 33: Ii1Ii1iiii11 + OoooooooOO - O0oo0OO0 / i1IIi / OoooooooOO
if 82 - 82: II / ooO - i1 / O00oOoOoO0o0O * O0oo0OO0
if 55 - 55: OoooooooOO
if 73 - 73: Oo0ooO0oo0oO - II % O00oOoOoO0o0O + II - O0 . O0oo0OO0
if 38 - 38: O0
if 79 - 79: i1IIi . i11Ii11I1Ii1i
if 34 - 34: o0000o0o0000o * II111iiii
if 71 - 71: OOooo0000ooo
if 97 - 97: II
if 86 - 86: O00oOoOoO0o0O - ooO . Oo0ooO0oo0oO . II111iiii * iii1I1I . II111iiii
if 34 - 34: I1i1iI1i . o0000o0o0000o % OOooo0000ooo - O0 / o0000o0o0000o
if 91 - 91: i11iIiiIii % o0000o0o0000o * i11Ii11I1Ii1i - II . o0000o0o0000o
if 28 - 28: i11iIiiIii
if 51 - 51: iii1I1I + Ii1Ii1iiii11 * O0 . ooo0Oo0
if 82 - 82: ooO * II % ooo0Oo0 . ooO
if 43 - 43: O0oo0OO0 . Ii1Ii1iiii11 * O00oOoOoO0o0O
if 20 - 20: i1IIi . i1IIi - OOoO
if 89 - 89: Ii1Ii1iiii11 - OOoO . O0 % OoooooooOO . i11iIiiIii
if 35 - 35: II111iiii / Oo0ooO0oo0oO - O0 . II111iiii
if 55 - 55: O00oOoOoO0o0O % i1IIi * OOoO
if 95 - 95: ooO / II111iiii - I1i1iI1i % o0000o0o0000o . OOoO
if 63 - 63: iIii1I11I1II1 / Ii1Ii1iiii11
if 24 - 24: O00oOoOoO0o0O / iIii1I11I1II1 % ooO * Oo0ooO0oo0oO - iIii1I11I1II1
if 50 - 50: II111iiii
if 39 - 39: II111iiii . Oo0ooO0oo0oO - O00oOoOoO0o0O * i1IIi . OoooooooOO
if 44 - 44: iii1I1I
if 55 - 55: i11Ii11I1Ii1i . o0000o0o0000o * o0000o0o0000o
if 82 - 82: iii1I1I % O0oo0OO0 % OOoO + OOoO
if 6 - 6: O00oOoOoO0o0O
if 73 - 73: o0000o0o0000o * II + I1i1iI1i - O00oOoOoO0o0O . OOoO
if 93 - 93: i11iIiiIii
if 80 - 80: i1IIi . iii1I1I - i11Ii11I1Ii1i + ooO + i1 % i11Ii11I1Ii1i
if 13 - 13: II111iiii / Oo0ooO0oo0oO / Oo0ooO0oo0oO + Ii1Ii1iiii11
if 49 - 49: O0 / II111iiii * iii1I1I - OoooooooOO . II111iiii % OOooo0000ooo
if 13 - 13: i11Ii11I1Ii1i . iIii1I11I1II1 . ooO . OOooo0000ooo
if 58 - 58: OOoO
if 7 - 7: II111iiii / OOooo0000ooo % OOoO + iii1I1I - O0
if 45 - 45: iii1I1I / i1 + i11Ii11I1Ii1i + OOooo0000ooo
if 15 - 15: iii1I1I % O0oo0OO0
if 66 - 66: i11Ii11I1Ii1i * i11iIiiIii . o0000o0o0000o
if 92 - 92: i11Ii11I1Ii1i
if 81 - 81: I1i1iI1i % iii1I1I - i1 / i11iIiiIii
if 73 - 73: O0 * o0000o0o0000o . i1IIi
if 51 - 51: O0oo0OO0 - i1 % O0 - Oo0ooO0oo0oO
if 53 - 53: i1 / i1IIi / i1IIi
if 77 - 77: OOoO + i1IIi . OOoO
if 89 - 89: I1i1iI1i + ooO * i11Ii11I1Ii1i
if 45 - 45: i1 - I1i1iI1i . ooo0Oo0
if 41 - 41: II111iiii . iii1I1I / O0oo0OO0 . Ii1Ii1iiii11
if 58 - 58: OOooo0000ooo % i11iIiiIii * II111iiii . II
if 94 - 94: i11iIiiIii . ooO + iIii1I11I1II1 * o0000o0o0000o * o0000o0o0000o
if 36 - 36: OOoO - OOooo0000ooo . OOooo0000ooo
if 60 - 60: i11iIiiIii * O00oOoOoO0o0O % O0oo0OO0 + O0oo0OO0
if 84 - 84: iIii1I11I1II1 + OoooooooOO
if 77 - 77: O0 * II * i11Ii11I1Ii1i + O0oo0OO0 + II - o0000o0o0000o
if 10 - 10: II + OOooo0000ooo
if 58 - 58: iii1I1I + OoooooooOO / i1 . Ii1Ii1iiii11 % I1i1iI1i / II
if 62 - 62: II111iiii
if 12 - 12: OOooo0000ooo + II111iiii
if 92 - 92: o0000o0o0000o % iIii1I11I1II1 - i1 / i11iIiiIii % Ii1Ii1iiii11 * I1i1iI1i
if 80 - 80: i1
if 3 - 3: II * OOoO
if 53 - 53: iIii1I11I1II1 / i1 % O0oo0OO0 + OOooo0000ooo / Ii1Ii1iiii11
if 74 - 74: O00oOoOoO0o0O
if 8 - 8: iii1I1I % II111iiii - I1i1iI1i - OOoO % iii1I1I
if 93 - 93: ooo0Oo0 * i1 / ooO
if 88 - 88: i11Ii11I1Ii1i
if 1 - 1: O00oOoOoO0o0O
if 95 - 95: OoooooooOO / OOoO % OoooooooOO / Ii1Ii1iiii11 * OOooo0000ooo
if 75 - 75: O0
if 56 - 56: O0oo0OO0 / II111iiii
if 39 - 39: Oo0ooO0oo0oO - OoooooooOO - i1IIi / II111iiii
if 49 - 49: O00oOoOoO0o0O + O0 + OOooo0000ooo . II111iiii % Ii1Ii1iiii11
if 33 - 33: Oo0ooO0oo0oO . iIii1I11I1II1 / OOoO % ooo0Oo0
if 49 - 49: O0oo0OO0 + II111iiii / OOooo0000ooo - O0 % ooo0Oo0
if 27 - 27: O0oo0OO0 + O00oOoOoO0o0O
if 92 - 92: iii1I1I % i1
if 31 - 31: OoooooooOO - i11Ii11I1Ii1i / o0000o0o0000o
if 62 - 62: i11iIiiIii - OOoO
if 81 - 81: OOoO
if 92 - 92: ooO - O00oOoOoO0o0O - OoooooooOO / OOooo0000ooo - i1IIi
if 81 - 81: i1IIi / o0000o0o0000o % i11iIiiIii . iIii1I11I1II1 * Oo0ooO0oo0oO + OoooooooOO
if 31 - 31: i1IIi % II111iiii
if 13 - 13: iIii1I11I1II1 - II111iiii % O0 . ooo0Oo0 % O0oo0OO0
if 2 - 2: OoooooooOO - ooo0Oo0 % i11Ii11I1Ii1i / iii1I1I / I1i1iI1i
if 3 - 3: II111iiii / ooO
if 48 - 48: Ii1Ii1iiii11 . II
if 49 - 49: i1IIi - Oo0ooO0oo0oO . O00oOoOoO0o0O + iIii1I11I1II1 - Ii1Ii1iiii11 / O00oOoOoO0o0O
if 24 - 24: i11Ii11I1Ii1i - i1 / Ii1Ii1iiii11
if 10 - 10: Oo0ooO0oo0oO * i1IIi
if 15 - 15: OOoO + i1IIi - II111iiii % iii1I1I
if 34 - 34: iii1I1I
if 57 - 57: ooO . ooo0Oo0 % I1i1iI1i
if 32 - 32: OOoO / OOooo0000ooo - O0 * iIii1I11I1II1
if 70 - 70: OoooooooOO % OoooooooOO % O0oo0OO0
if 98 - 98: O0oo0OO0
if 18 - 18: OOoO + O00oOoOoO0o0O - O0oo0OO0 / o0000o0o0000o / ooO
if 53 - 53: ooO + I1i1iI1i . i11Ii11I1Ii1i / OOoO
if 52 - 52: o0000o0o0000o + o0000o0o0000o
if 73 - 73: I1i1iI1i . i11iIiiIii % OoooooooOO + Ii1Ii1iiii11 . OoooooooOO / ooO
if 54 - 54: Oo0ooO0oo0oO . OoooooooOO
if 36 - 36: i11Ii11I1Ii1i / II111iiii * OOooo0000ooo % II
if 31 - 31: II111iiii + ooO - OoooooooOO . OOoO
if 28 - 28: ooo0Oo0 . II
if 77 - 77: II % II111iiii
if 81 - 81: Oo0ooO0oo0oO % ooo0Oo0 / O0 * iIii1I11I1II1 % OOooo0000ooo . iii1I1I
if 90 - 90: I1i1iI1i
if 44 - 44: I1i1iI1i / II . O00oOoOoO0o0O + Oo0ooO0oo0oO
if 32 - 32: OOooo0000ooo - Ii1Ii1iiii11 * i1 * OOoO
if 84 - 84: ooo0Oo0 + II % iii1I1I + i11iIiiIii
if 37 - 37: OOoO % II / Ii1Ii1iiii11
if 94 - 94: OOoO / O0oo0OO0 . I1i1iI1i
if 1 - 1: O00oOoOoO0o0O . II111iiii
if 93 - 93: II111iiii . i11iIiiIii + II111iiii % i11Ii11I1Ii1i
if 98 - 98: o0000o0o0000o * i11Ii11I1Ii1i * Oo0ooO0oo0oO + ooo0Oo0 * i1
if 4 - 4: OOooo0000ooo
if 16 - 16: iIii1I11I1II1 * i1 + i11Ii11I1Ii1i . O0 . I1i1iI1i
if 99 - 99: i11iIiiIii - i1
if 85 - 85: o0000o0o0000o % II
if 95 - 95: O0oo0OO0 * ooO * i1 . I1i1iI1i
if 73 - 73: O0oo0OO0
if 28 - 28: OoooooooOO - OOoO
if 84 - 84: II111iiii
if 36 - 36: ooO - Oo0ooO0oo0oO - iIii1I11I1II1
if 10 - 10: II / ooo0Oo0 * i1IIi % O0 + OOoO
if 25 - 25: o0000o0o0000o - ooo0Oo0 / O0 . OoooooooOO % iii1I1I . i1IIi
if 19 - 19: II111iiii / II111iiii % II + i11Ii11I1Ii1i + i11Ii11I1Ii1i + i1
if 4 - 4: I1i1iI1i + OOoO / i1 + i1IIi % I1i1iI1i % i1
if 80 - 80: ooo0Oo0
if 26 - 26: iIii1I11I1II1 . OoooooooOO - iIii1I11I1II1
if 59 - 59: II + OOoO . i11Ii11I1Ii1i
if 87 - 87: O0oo0OO0
if 34 - 34: o0000o0o0000o . Oo0ooO0oo0oO / i11iIiiIii / i1
if 46 - 46: O00oOoOoO0o0O + II111iiii * iii1I1I + ooO
if 31 - 31: ooo0Oo0 * I1i1iI1i * ooo0Oo0 + O0oo0OO0 * I1i1iI1i . o0000o0o0000o
if 89 - 89: OoooooooOO * ooo0Oo0 * iii1I1I . Ii1Ii1iiii11 * ooo0Oo0 / i1
if 46 - 46: i11iIiiIii
if 15 - 15: O0 / i1IIi / i1IIi . i1 % Oo0ooO0oo0oO + iii1I1I
if 48 - 48: o0000o0o0000o % i1 % ooo0Oo0 % iIii1I11I1II1 . ooo0Oo0
if 14 - 14: i1 * O0oo0OO0 % O0 + OOoO + II
if 23 - 23: O00oOoOoO0o0O % i1 + ooo0Oo0 - o0000o0o0000o
if 65 - 65: OoooooooOO
if 22 - 22: ooO + II111iiii + O00oOoOoO0o0O
if 83 - 83: Ii1Ii1iiii11
if 43 - 43: ooO
if 84 - 84: ooO . OOooo0000ooo . i1
if 2 - 2: O00oOoOoO0o0O - Oo0ooO0oo0oO
if 49 - 49: ooo0Oo0 + II111iiii / i11Ii11I1Ii1i - Oo0ooO0oo0oO % Oo0ooO0oo0oO + iii1I1I
if 54 - 54: Ii1Ii1iiii11 % O00oOoOoO0o0O - ooO
if 16 - 16: II * i1 / OOoO
if 46 - 46: II111iiii
if 13 - 13: OOooo0000ooo + II111iiii % iii1I1I
if 30 - 30: OoooooooOO - i11iIiiIii + i11Ii11I1Ii1i / O00oOoOoO0o0O - i11iIiiIii
if 74 - 74: O0 . OOoO
if 64 - 64: Ii1Ii1iiii11 / i1IIi % i1
if 84 - 84: Oo0ooO0oo0oO - O00oOoOoO0o0O . Ii1Ii1iiii11 . OOooo0000ooo - O00oOoOoO0o0O
if 99 - 99: o0000o0o0000o
if 75 - 75: Ii1Ii1iiii11 . ooO / OOooo0000ooo
if 84 - 84: OoooooooOO . iii1I1I / I1i1iI1i
if 86 - 86: O00oOoOoO0o0O % Oo0ooO0oo0oO
if 77 - 77: ooo0Oo0 % ooO / i11Ii11I1Ii1i
if 91 - 91: O0oo0OO0 / O0oo0OO0 . II111iiii . Ii1Ii1iiii11 - iii1I1I
if 23 - 23: iii1I1I
if 7 - 7: i1 % II
if 64 - 64: o0000o0o0000o + i11iIiiIii
if 35 - 35: Oo0ooO0oo0oO + i1IIi % ooO
if 68 - 68: OOooo0000ooo . Ii1Ii1iiii11
if 64 - 64: i1IIi + O00oOoOoO0o0O * iii1I1I / ooO
if 3 - 3: O00oOoOoO0o0O / Ii1Ii1iiii11 + Ii1Ii1iiii11 . II
if 50 - 50: iIii1I11I1II1 * i11Ii11I1Ii1i
if 85 - 85: i1IIi
if 100 - 100: OoooooooOO / OOoO % O0oo0OO0 + ooo0Oo0
if 42 - 42: O00oOoOoO0o0O / OOooo0000ooo . ooo0Oo0 * iii1I1I
if 54 - 54: Oo0ooO0oo0oO * i1 + O0oo0OO0
if 93 - 93: I1i1iI1i / iii1I1I
if 47 - 47: O00oOoOoO0o0O * ooO
if 98 - 98: i11Ii11I1Ii1i - i11Ii11I1Ii1i . Ii1Ii1iiii11
if 60 - 60: iii1I1I * II / O0 + OOoO + OOooo0000ooo
if 66 - 66: OOooo0000ooo * O00oOoOoO0o0O . OoooooooOO * o0000o0o0000o
if 93 - 93: OOooo0000ooo / i1IIi
if 47 - 47: Ii1Ii1iiii11 - ooo0Oo0
if 98 - 98: i11Ii11I1Ii1i . o0000o0o0000o / Oo0ooO0oo0oO . Ii1Ii1iiii11
if 1 - 1: ooO
if 87 - 87: O0 * II111iiii + iIii1I11I1II1 % i11Ii11I1Ii1i % i11iIiiIii - Oo0ooO0oo0oO
if 73 - 73: i1 + ooo0Oo0
if 37 - 37: i11Ii11I1Ii1i - iIii1I11I1II1 + II111iiii . ooo0Oo0 % iIii1I11I1II1
if 17 - 17: o0000o0o0000o + i1IIi % O0
if 65 - 65: OOooo0000ooo
if 50 - 50: II111iiii / O0oo0OO0
if 79 - 79: II - iIii1I11I1II1 % i1IIi / O00oOoOoO0o0O + II111iiii
if 95 - 95: i11Ii11I1Ii1i
if 48 - 48: OOoO / iIii1I11I1II1 % II111iiii
if 39 - 39: i1IIi . II / OOoO / OOoO
if 100 - 100: OoooooooOO - OoooooooOO + OOooo0000ooo
if 32 - 32: Oo0ooO0oo0oO * I1i1iI1i / OoooooooOO
if 90 - 90: o0000o0o0000o
if 35 - 35: II111iiii / ooo0Oo0
if 79 - 79: Oo0ooO0oo0oO + o0000o0o0000o * i1 * ooo0Oo0
if 53 - 53: ooO / O00oOoOoO0o0O
if 10 - 10: II . I1i1iI1i
if 75 - 75: O0 * i1IIi - OOoO / ooO % ooO / Oo0ooO0oo0oO
if 5 - 5: O0 - i1 / o0000o0o0000o . I1i1iI1i
if 7 - 7: II - Oo0ooO0oo0oO
if 54 - 54: i11Ii11I1Ii1i / iIii1I11I1II1 / OoooooooOO . i1IIi - Oo0ooO0oo0oO
if 57 - 57: iIii1I11I1II1 * ooo0Oo0 * i1 / i11Ii11I1Ii1i
if 46 - 46: ooo0Oo0
if 61 - 61: I1i1iI1i / Ii1Ii1iiii11 - II111iiii
if 87 - 87: II / iii1I1I
if 45 - 45: Oo0ooO0oo0oO * Ii1Ii1iiii11 / OoooooooOO + O0oo0OO0 . o0000o0o0000o / O0oo0OO0
if 64 - 64: ooo0Oo0 / i1IIi % iii1I1I - I1i1iI1i
if 11 - 11: II - OoooooooOO
if 16 - 16: OOooo0000ooo % OoooooooOO - Ii1Ii1iiii11 * ooo0Oo0 - ooo0Oo0
if 27 - 27: OOooo0000ooo + iIii1I11I1II1 / O00oOoOoO0o0O + O0oo0OO0 % O00oOoOoO0o0O + O0oo0OO0
if 77 - 77: O00oOoOoO0o0O * Ii1Ii1iiii11 % ooo0Oo0
if 2 - 2: OOoO / O00oOoOoO0o0O / ooo0Oo0 / II / OoooooooOO
if 22 - 22: iIii1I11I1II1 * iii1I1I / OOoO + Oo0ooO0oo0oO
if 98 - 98: ooO
if 69 - 69: II111iiii + O00oOoOoO0o0O - i11Ii11I1Ii1i . O00oOoOoO0o0O / iIii1I11I1II1 * iIii1I11I1II1
if 75 - 75: O0oo0OO0 % OoooooooOO
if 16 - 16: O0 / i1IIi
if 58 - 58: I1i1iI1i / i11iIiiIii / O0 % OOoO % iii1I1I
if 86 - 86: OOooo0000ooo + Oo0ooO0oo0oO / iii1I1I + OOoO % OOoO / i11iIiiIii
if 12 - 12: Oo0ooO0oo0oO + I1i1iI1i . o0000o0o0000o
if 52 - 52: O0oo0OO0
if 4 - 4: ooo0Oo0 % II + OOoO - II
if 98 - 98: ooo0Oo0 - O0 * i11Ii11I1Ii1i * ooo0Oo0 * ooo0Oo0
if 44 - 44: OOooo0000ooo + OOoO
if 66 - 66: i11Ii11I1Ii1i
if 34 - 34: i1 % i11iIiiIii + i11iIiiIii - i1
if 2 - 2: II111iiii + i1IIi
if 68 - 68: ooO + ooo0Oo0
if 58 - 58: OOooo0000ooo * ooo0Oo0 . i1IIi
if 19 - 19: i11Ii11I1Ii1i
if 85 - 85: Ii1Ii1iiii11 - iii1I1I / i1IIi / O0oo0OO0 / II111iiii
if 94 - 94: iIii1I11I1II1 + OOooo0000ooo
if 44 - 44: O0oo0OO0 + OOoO % O0oo0OO0 + i1IIi + i1 + O0
if 18 - 18: iIii1I11I1II1 % iIii1I11I1II1 % i11Ii11I1Ii1i + iii1I1I % Ii1Ii1iiii11 / ooo0Oo0
if 36 - 36: Oo0ooO0oo0oO . i11iIiiIii
if 81 - 81: O00oOoOoO0o0O * i1 * O0oo0OO0
if 85 - 85: O0 * i11Ii11I1Ii1i
if 39 - 39: II111iiii * iii1I1I - iIii1I11I1II1
if 25 - 25: OoooooooOO . ooo0Oo0 % i1 . OOooo0000ooo
if 67 - 67: OoooooooOO + o0000o0o0000o / Ii1Ii1iiii11
if 75 - 75: OOooo0000ooo / OoooooooOO . iii1I1I + o0000o0o0000o - II111iiii
if 33 - 33: OOooo0000ooo / OOooo0000ooo . i11iIiiIii * II + I1i1iI1i
if 16 - 16: OOooo0000ooo
if 10 - 10: Oo0ooO0oo0oO . OOooo0000ooo * iIii1I11I1II1 - i11Ii11I1Ii1i - Oo0ooO0oo0oO / o0000o0o0000o
if 13 - 13: i11Ii11I1Ii1i + Oo0ooO0oo0oO % OOooo0000ooo % OoooooooOO
if 22 - 22: o0000o0o0000o
if 23 - 23: O0
if 41 - 41: i1IIi . ooO / Ii1Ii1iiii11 / I1i1iI1i % OOooo0000ooo - ooo0Oo0
if 14 - 14: II - i11iIiiIii * o0000o0o0000o
if 39 - 39: OoooooooOO
if 19 - 19: i11iIiiIii
if 80 - 80: iii1I1I
if 58 - 58: i11Ii11I1Ii1i + II % Oo0ooO0oo0oO
if 22 - 22: iIii1I11I1II1 - ooo0Oo0 / iii1I1I * OOooo0000ooo
if 26 - 26: I1i1iI1i + ooO - I1i1iI1i + O00oOoOoO0o0O . i11Ii11I1Ii1i
if 97 - 97: i1IIi
if 46 - 46: II
if 30 - 30: O0oo0OO0 / O0 * I1i1iI1i * o0000o0o0000o + OoooooooOO * i1
if 23 - 23: OOoO
if 36 - 36: OOooo0000ooo . i1 - i1IIi + o0000o0o0000o
if 54 - 54: OoooooooOO . i11Ii11I1Ii1i - i1
if 76 - 76: o0000o0o0000o
if 61 - 61: Ii1Ii1iiii11 / II111iiii * Ii1Ii1iiii11 * Oo0ooO0oo0oO * o0000o0o0000o . i11iIiiIii
if 26 - 26: o0000o0o0000o / Ii1Ii1iiii11 - O0oo0OO0 . iIii1I11I1II1
if 83 - 83: Ii1Ii1iiii11 % ooo0Oo0 / O00oOoOoO0o0O - i1 / O0
if 97 - 97: iIii1I11I1II1 * OOoO
if 95 - 95: O0oo0OO0
if 68 - 68: iIii1I11I1II1 . iIii1I11I1II1 / Oo0ooO0oo0oO - II111iiii - iIii1I11I1II1
if 75 - 75: Ii1Ii1iiii11 . iii1I1I * II111iiii
if 99 - 99: iIii1I11I1II1 * II + OOooo0000ooo
if 70 - 70: i1IIi % Ii1Ii1iiii11 . II - OOooo0000ooo + ooO
if 84 - 84: i11Ii11I1Ii1i + II111iiii * II111iiii % I1i1iI1i / i1 + Ii1Ii1iiii11
if 9 - 9: i1
if 25 - 25: ooO - ooo0Oo0 . OOoO
if 57 - 57: I1i1iI1i + O00oOoOoO0o0O * II - Ii1Ii1iiii11 % iIii1I11I1II1 - ooo0Oo0
if 37 - 37: O0oo0OO0 * OOoO + ooo0Oo0 + II * I1i1iI1i
if 95 - 95: ooo0Oo0 - i11iIiiIii % i11iIiiIii - O0 * o0000o0o0000o
if 81 - 81: II111iiii * iii1I1I % i1IIi * i11iIiiIii + Oo0ooO0oo0oO
if 100 - 100: i1IIi % ooo0Oo0
if 55 - 55: iii1I1I + i1
if 85 - 85: i11Ii11I1Ii1i + i1 % i1 / OOoO . iii1I1I - Oo0ooO0oo0oO
if 19 - 19: OOoO / i1 + OOooo0000ooo
if 76 - 76: iIii1I11I1II1 / o0000o0o0000o - II % I1i1iI1i % ooO + OoooooooOO
if 10 - 10: O0oo0OO0 * OOoO / O00oOoOoO0o0O - o0000o0o0000o
if 11 - 11: OOooo0000ooo % II / Ii1Ii1iiii11 . i11iIiiIii + ooO - II111iiii
if 50 - 50: i1IIi * i11Ii11I1Ii1i / i11iIiiIii / i11iIiiIii / i11Ii11I1Ii1i
if 84 - 84: II - i1 + II
if 63 - 63: OOoO * Ii1Ii1iiii11 % II111iiii % o0000o0o0000o + iii1I1I * O00oOoOoO0o0O
if 96 - 96: OOooo0000ooo
if 99 - 99: iIii1I11I1II1 - Ii1Ii1iiii11
if 79 - 79: iii1I1I + i11Ii11I1Ii1i % OOoO % i11Ii11I1Ii1i
if 56 - 56: II + i11Ii11I1Ii1i . O0oo0OO0 + OoooooooOO * II - O0
if 35 - 35: ooO . OOoO . o0000o0o0000o - OOoO % OOoO + o0000o0o0000o
if 99 - 99: I1i1iI1i + ooO
if 34 - 34: o0000o0o0000o * I1i1iI1i . iii1I1I % i11iIiiIii
if 61 - 61: iIii1I11I1II1 + i11Ii11I1Ii1i * OOoO - i1IIi % i11Ii11I1Ii1i
if 76 - 76: i11Ii11I1Ii1i / Oo0ooO0oo0oO
if 12 - 12: o0000o0o0000o
if 58 - 58: O0oo0OO0 + iIii1I11I1II1 % O0 + OOoO + Oo0ooO0oo0oO * OoooooooOO
if 41 - 41: i11Ii11I1Ii1i * iii1I1I
if 76 - 76: i11Ii11I1Ii1i . O0 * OoooooooOO + Ii1Ii1iiii11
if 53 - 53: O00oOoOoO0o0O
if 3 - 3: OOooo0000ooo - OoooooooOO * OoooooooOO - iii1I1I / o0000o0o0000o * II
if 58 - 58: OOooo0000ooo % iIii1I11I1II1 / i11iIiiIii % I1i1iI1i . o0000o0o0000o * i1
if 32 - 32: OoooooooOO + I1i1iI1i
if 91 - 91: Ii1Ii1iiii11 - o0000o0o0000o * o0000o0o0000o
if 55 - 55: iIii1I11I1II1 + iii1I1I - O00oOoOoO0o0O
if 24 - 24: O0oo0OO0 / o0000o0o0000o + i1 * OOoO * i1
if 10 - 10: iii1I1I - II - O00oOoOoO0o0O - I1i1iI1i
if 21 - 21: OoooooooOO + o0000o0o0000o
if 43 - 43: i11iIiiIii . II . i11Ii11I1Ii1i
if 31 - 31: ooo0Oo0 % I1i1iI1i % o0000o0o0000o . II / I1i1iI1i * i11Ii11I1Ii1i
if 74 - 74: iii1I1I . Ii1Ii1iiii11 / i1 . OOooo0000ooo
if 74 - 74: O00oOoOoO0o0O / o0000o0o0000o % o0000o0o0000o . OOooo0000ooo
if 72 - 72: i1IIi
if 21 - 21: o0000o0o0000o . ooO / i11iIiiIii * i1IIi
if 82 - 82: Ii1Ii1iiii11 * O00oOoOoO0o0O % i11iIiiIii * i1IIi . ooO
if 89 - 89: OOooo0000ooo - i1IIi - OOooo0000ooo
if 74 - 74: O0oo0OO0 % O0oo0OO0
if 28 - 28: Oo0ooO0oo0oO % i11Ii11I1Ii1i - ooO + ooO + i11Ii11I1Ii1i / iIii1I11I1II1
if 91 - 91: iii1I1I / II111iiii * ooO
if 94 - 94: II111iiii - iIii1I11I1II1 - iIii1I11I1II1
if 83 - 83: II * iIii1I11I1II1 + Oo0ooO0oo0oO * i1IIi . OoooooooOO % ooo0Oo0
if 81 - 81: O0oo0OO0 - iIii1I11I1II1
if 60 - 60: o0000o0o0000o
if 77 - 77: iii1I1I / II
if 95 - 95: o0000o0o0000o * i1IIi + i11Ii11I1Ii1i
if 40 - 40: II111iiii
if 7 - 7: ooO / O0oo0OO0
if 88 - 88: i1IIi
if 53 - 53: Ii1Ii1iiii11 . ooO . I1i1iI1i + i11Ii11I1Ii1i
if 17 - 17: iIii1I11I1II1 + i1IIi . II + ooo0Oo0 % i1IIi . i11Ii11I1Ii1i
if 57 - 57: i11Ii11I1Ii1i
if 92 - 92: II111iiii - O0oo0OO0 - ooO % iii1I1I - Oo0ooO0oo0oO * o0000o0o0000o
if 16 - 16: iIii1I11I1II1 + OoooooooOO - Ii1Ii1iiii11 * OOooo0000ooo
if 37 - 37: i1
if 15 - 15: I1i1iI1i % O0oo0OO0 / i1
if 36 - 36: O0oo0OO0 + O0oo0OO0 % O00oOoOoO0o0O + O00oOoOoO0o0O / i1IIi % i1IIi
if 20 - 20: ooO * i11Ii11I1Ii1i
if 91 - 91: O0oo0OO0 % i1IIi - iIii1I11I1II1 . ooO
if 31 - 31: i11Ii11I1Ii1i % i1IIi . OoooooooOO - I1i1iI1i + OoooooooOO
if 45 - 45: ooO + OOoO / OoooooooOO - ooo0Oo0 + OoooooooOO
if 42 - 42: iIii1I11I1II1 * iii1I1I * o0000o0o0000o
if 62 - 62: ooO * O0 % OOooo0000ooo . OOooo0000ooo . iii1I1I
if 91 - 91: i1IIi . i1
if 37 - 37: i1 - OOoO + iIii1I11I1II1 / o0000o0o0000o - O0oo0OO0 . I1i1iI1i
if 62 - 62: II
if 47 - 47: o0000o0o0000o % ooO * O0oo0OO0 . iIii1I11I1II1 % O00oOoOoO0o0O + OoooooooOO
if 2 - 2: o0000o0o0000o % OoooooooOO - Ii1Ii1iiii11 * II * OOooo0000ooo
if 99 - 99: iIii1I11I1II1 . O00oOoOoO0o0O / Ii1Ii1iiii11 . ooO % iii1I1I * OOoO
if 95 - 95: i11Ii11I1Ii1i
if 80 - 80: OOooo0000ooo
if 42 - 42: OoooooooOO * II111iiii
if 53 - 53: o0000o0o0000o + i1IIi . O0oo0OO0 / i11iIiiIii + ooo0Oo0 % Oo0ooO0oo0oO
if 9 - 9: Ii1Ii1iiii11 . OOoO - O00oOoOoO0o0O . o0000o0o0000o
if 39 - 39: ooO
if 70 - 70: OOooo0000ooo % O0oo0OO0 % iii1I1I
if 95 - 95: Oo0ooO0oo0oO - o0000o0o0000o / O0 * iii1I1I - I1i1iI1i
if 12 - 12: iIii1I11I1II1 % O00oOoOoO0o0O . i1 . OOooo0000ooo % i11iIiiIii
if 2 - 2: i11Ii11I1Ii1i * i11Ii11I1Ii1i . Oo0ooO0oo0oO * ooo0Oo0 * iIii1I11I1II1
if 13 - 13: OOoO / O0 . i11iIiiIii * i1IIi % i11iIiiIii
if 8 - 8: Oo0ooO0oo0oO - OoooooooOO
if 99 - 99: II111iiii / OOooo0000ooo % OoooooooOO . i11iIiiIii
if 18 - 18: I1i1iI1i . Ii1Ii1iiii11
if 70 - 70: OoooooooOO . Ii1Ii1iiii11 / i11Ii11I1Ii1i . i11Ii11I1Ii1i - I1i1iI1i
if 29 - 29: OOoO % ooO - Ii1Ii1iiii11
if 26 - 26: O0 . OOoO + i1 - ooo0Oo0 . OOoO
if 2 - 2: II . O00oOoOoO0o0O * ooO % II111iiii . i1
if 46 - 46: Oo0ooO0oo0oO + iii1I1I % OoooooooOO * i11iIiiIii - O00oOoOoO0o0O
if 47 - 47: i1 * Oo0ooO0oo0oO * OOooo0000ooo
if 46 - 46: ooo0Oo0
if 42 - 42: iIii1I11I1II1
if 32 - 32: O00oOoOoO0o0O - ooo0Oo0 . OoooooooOO - OoooooooOO - O00oOoOoO0o0O . iIii1I11I1II1
if 34 - 34: O00oOoOoO0o0O
if 31 - 31: i1IIi - OOoO + o0000o0o0000o + Ii1Ii1iiii11 . Ii1Ii1iiii11 . O0
if 33 - 33: i1IIi / i1 * O0oo0OO0
if 2 - 2: i11Ii11I1Ii1i . ooO
if 43 - 43: iIii1I11I1II1
if 29 - 29: OOooo0000ooo % Ii1Ii1iiii11 + O0oo0OO0 . i1IIi + iii1I1I
if 24 - 24: o0000o0o0000o / ooo0Oo0 * II - OoooooooOO / iii1I1I . i11Ii11I1Ii1i
if 98 - 98: i1IIi - i1
if 49 - 49: I1i1iI1i . ooo0Oo0 . i11Ii11I1Ii1i
if 9 - 9: OOooo0000ooo - II111iiii * O0oo0OO0
if 78 - 78: iIii1I11I1II1 / O0 * i11Ii11I1Ii1i / i1 / Oo0ooO0oo0oO
if 15 - 15: Ii1Ii1iiii11 / i11Ii11I1Ii1i
if 54 - 54: Ii1Ii1iiii11 - iIii1I11I1II1 - OOoO % ooo0Oo0 / II111iiii
if 80 - 80: i11iIiiIii % iIii1I11I1II1 / i11iIiiIii
if 66 - 66: Oo0ooO0oo0oO . iIii1I11I1II1 * II - ooo0Oo0 - iIii1I11I1II1
if 28 - 28: Oo0ooO0oo0oO % OoooooooOO
if 13 - 13: OOooo0000ooo . O00oOoOoO0o0O - OOoO / i11Ii11I1Ii1i - O00oOoOoO0o0O - iii1I1I
if 84 - 84: II111iiii
if 57 - 57: O0 * iIii1I11I1II1 % O0 . OoooooooOO
if 53 - 53: ooo0Oo0 / iii1I1I * ooo0Oo0 + I1i1iI1i + i11Ii11I1Ii1i - O00oOoOoO0o0O
if 16 - 16: O0oo0OO0 % o0000o0o0000o . i1IIi / II - O0
if 85 - 85: i1IIi . i1IIi
if 16 - 16: iii1I1I - ooO % ooo0Oo0 . ooO + II % i11iIiiIii
if 59 - 59: i11iIiiIii - OOoO
if 59 - 59: OoooooooOO * I1i1iI1i / o0000o0o0000o
if 75 - 75: I1i1iI1i - OoooooooOO
if 21 - 21: iii1I1I + iIii1I11I1II1 / i11iIiiIii / i11Ii11I1Ii1i
if 66 - 66: OoooooooOO + i1 . OOooo0000ooo % i1IIi
if 58 - 58: ooO % i1 * O0 + II - OOooo0000ooo
if 26 - 26: i1IIi / iii1I1I / OOoO + OOoO
if 46 - 46: o0000o0o0000o % II + ooo0Oo0
if 67 - 67: iIii1I11I1II1 . i11iIiiIii . i11iIiiIii . i11iIiiIii / OOoO + Ii1Ii1iiii11
if 10 - 10: Ii1Ii1iiii11 - O00oOoOoO0o0O % II111iiii
if 66 - 66: iIii1I11I1II1 . iIii1I11I1II1
if 46 - 46: o0000o0o0000o * i11Ii11I1Ii1i . ooo0Oo0 * o0000o0o0000o * iIii1I11I1II1 / OOoO
if 46 - 46: II111iiii % II . ooO . O00oOoOoO0o0O / i11iIiiIii + O0oo0OO0
if 47 - 47: OOooo0000ooo . ooO
if 96 - 96: OOoO % II111iiii / Ii1Ii1iiii11 % ooO / Ii1Ii1iiii11 % i11iIiiIii
if 57 - 57: OOoO - OOoO % II111iiii % O00oOoOoO0o0O . I1i1iI1i % O00oOoOoO0o0O
if 91 - 91: iii1I1I - O0oo0OO0 - O00oOoOoO0o0O - ooo0Oo0 * iIii1I11I1II1
if 68 - 68: O0oo0OO0 % O0 * iIii1I11I1II1 / i11Ii11I1Ii1i * I1i1iI1i + ooO
if 89 - 89: Ii1Ii1iiii11 * iii1I1I . i11Ii11I1Ii1i
if 75 - 75: Ii1Ii1iiii11 - i1 % i1 + Ii1Ii1iiii11 * I1i1iI1i - II
if 26 - 26: OOoO * ooo0Oo0 % iii1I1I + i1
if 38 - 38: i1 - O00oOoOoO0o0O / ooo0Oo0 + i11Ii11I1Ii1i . i1 + OOooo0000ooo
if 19 - 19: ooo0Oo0
if 51 - 51: iIii1I11I1II1
if 8 - 8: O0oo0OO0 / I1i1iI1i % i1 . i11iIiiIii . OoooooooOO . ooo0Oo0
if 8 - 8: O0oo0OO0 * O00oOoOoO0o0O
if 41 - 41: O00oOoOoO0o0O / O0oo0OO0 / Oo0ooO0oo0oO - i11iIiiIii - Oo0ooO0oo0oO
if 4 - 4: OOoO . OOooo0000ooo
if 39 - 39: ooO . O00oOoOoO0o0O - Oo0ooO0oo0oO * i11iIiiIii
if 4 - 4: Oo0ooO0oo0oO * O0 - OOoO
if 72 - 72: OOoO + Ii1Ii1iiii11 / iii1I1I . OOooo0000ooo % O0oo0OO0 / i11iIiiIii
if 13 - 13: o0000o0o0000o % I1i1iI1i + ooO + o0000o0o0000o + i11iIiiIii - II
if 70 - 70: II111iiii * II111iiii . iii1I1I
if 11 - 11: i1
if 20 - 20: ooo0Oo0 . o0000o0o0000o % ooo0Oo0
if 5 - 5: ooO + i1
if 23 - 23: o0000o0o0000o % iIii1I11I1II1 . OOoO
if 95 - 95: O00oOoOoO0o0O + i11iIiiIii % ooO - i11Ii11I1Ii1i
if 11 - 11: II / O0 + II111iiii
if 95 - 95: o0000o0o0000o + OOooo0000ooo * iIii1I11I1II1
if 17 - 17: O0oo0OO0 - O00oOoOoO0o0O * O0 / ooo0Oo0
if 19 - 19: i1IIi - iIii1I11I1II1 . OOoO
if 2 - 2: ooo0Oo0
if 12 - 12: i11iIiiIii - iIii1I11I1II1 * OOooo0000ooo * i1
if 19 - 19: O0 + i11Ii11I1Ii1i + I1i1iI1i
if 81 - 81: iIii1I11I1II1
if 51 - 51: I1i1iI1i . II * ooo0Oo0 / O00oOoOoO0o0O * II111iiii / O0
if 44 - 44: i11iIiiIii % o0000o0o0000o % i11Ii11I1Ii1i + OOoO * i11Ii11I1Ii1i . ooo0Oo0
if 89 - 89: OoooooooOO % II111iiii - O0oo0OO0 % i11iIiiIii
if 7 - 7: OOooo0000ooo
if 15 - 15: O00oOoOoO0o0O + i1 + iii1I1I * I1i1iI1i
if 33 - 33: I1i1iI1i * O00oOoOoO0o0O
if 88 - 88: o0000o0o0000o % ooO - Oo0ooO0oo0oO - Oo0ooO0oo0oO . iii1I1I
if 52 - 52: II111iiii / II111iiii / iii1I1I - o0000o0o0000o
if 91 - 91: iii1I1I + I1i1iI1i % II111iiii + O0oo0OO0
if 66 - 66: iIii1I11I1II1 * II111iiii % O00oOoOoO0o0O % iii1I1I - ooo0Oo0
if 59 - 59: OOooo0000ooo % i11Ii11I1Ii1i
if 21 - 21: OoooooooOO % Oo0ooO0oo0oO - Oo0ooO0oo0oO / II / I1i1iI1i
if 15 - 15: Ii1Ii1iiii11 / Ii1Ii1iiii11 % OoooooooOO . o0000o0o0000o
if 93 - 93: II * II / OoooooooOO
if 6 - 6: II * O00oOoOoO0o0O + iIii1I11I1II1
if 19 - 19: O0 % II111iiii * I1i1iI1i
if 27 - 27: ooO * OOooo0000ooo / i11iIiiIii - i11Ii11I1Ii1i + II111iiii
if 43 - 43: II - II111iiii
if 56 - 56: II . i1IIi / i1 % i11Ii11I1Ii1i / O0 * OOoO
if 98 - 98: O0 + i1
if 23 - 23: OoooooooOO . iIii1I11I1II1 / i1IIi
if 31 - 31: O00oOoOoO0o0O - iIii1I11I1II1 / OOoO . O0oo0OO0
if 74 - 74: O00oOoOoO0o0O - II111iiii - OOooo0000ooo
if 50 - 50: iii1I1I - i11Ii11I1Ii1i + i11Ii11I1Ii1i * OOoO + i11Ii11I1Ii1i
if 70 - 70: i1IIi % O0oo0OO0 / i1IIi
if 30 - 30: Oo0ooO0oo0oO - i11iIiiIii
if 94 - 94: Oo0ooO0oo0oO % i1
if 39 - 39: Oo0ooO0oo0oO + o0000o0o0000o % O0
if 26 - 26: Ii1Ii1iiii11 + Oo0ooO0oo0oO
if 17 - 17: II - i1 % O00oOoOoO0o0O * O0 % O0 * ooO
if 6 - 6: o0000o0o0000o
if 46 - 46: II111iiii * o0000o0o0000o
if 23 - 23: i1IIi - O0
if 6 - 6: Ii1Ii1iiii11 % OoooooooOO * o0000o0o0000o - OOooo0000ooo
if 24 - 24: OOoO / iIii1I11I1II1 . OoooooooOO % Oo0ooO0oo0oO . ooo0Oo0
if 73 - 73: o0000o0o0000o
if 25 - 25: OOooo0000ooo
if 77 - 77: I1i1iI1i . iIii1I11I1II1 . OoooooooOO . iIii1I11I1II1
if 87 - 87: II111iiii - OoooooooOO / i1IIi . ooo0Oo0 - O00oOoOoO0o0O . i11iIiiIii
if 47 - 47: O00oOoOoO0o0O % O0oo0OO0 - Ii1Ii1iiii11 - O00oOoOoO0o0O * i11Ii11I1Ii1i
if 72 - 72: I1i1iI1i % I1i1iI1i + i1 + II / O00oOoOoO0o0O
if 30 - 30: O00oOoOoO0o0O + iii1I1I + i11iIiiIii / O0oo0OO0
if 64 - 64: OOooo0000ooo
if 80 - 80: iii1I1I - i11iIiiIii / O0oo0OO0 / Oo0ooO0oo0oO + Oo0ooO0oo0oO
if 89 - 89: O0 + OOooo0000ooo * o0000o0o0000o
if 30 - 30: Oo0ooO0oo0oO
if 39 - 39: II + I1i1iI1i + o0000o0o0000o + OOooo0000ooo
if 48 - 48: o0000o0o0000o / Ii1Ii1iiii11 . iIii1I11I1II1
if 72 - 72: i1IIi . I1i1iI1i
if 3 - 3: Oo0ooO0oo0oO % II111iiii - O0
if 52 - 52: O0oo0OO0
if 49 - 49: ooo0Oo0 . II % Ii1Ii1iiii11 . O00oOoOoO0o0O * ooO
if 44 - 44: iIii1I11I1II1 / O0 * O00oOoOoO0o0O + iii1I1I . Ii1Ii1iiii11
if 20 - 20: i1 + I1i1iI1i . o0000o0o0000o / i11iIiiIii
if 7 - 7: Oo0ooO0oo0oO / Oo0ooO0oo0oO . o0000o0o0000o * O0 + OOooo0000ooo + i11Ii11I1Ii1i
if 98 - 98: II111iiii * OOooo0000ooo - iii1I1I % I1i1iI1i - i1 % II
if 69 - 69: i1IIi % O0oo0OO0 % o0000o0o0000o / Ii1Ii1iiii11 / Ii1Ii1iiii11
if 6 - 6: II111iiii % II % i1IIi * Ii1Ii1iiii11
if 47 - 47: O0
if 55 - 55: O0oo0OO0 % O0 / OoooooooOO
if 49 - 49: iii1I1I . O0oo0OO0 * OoooooooOO % i11iIiiIii + iIii1I11I1II1 * i1IIi
if 88 - 88: II * i1 + II111iiii
if 62 - 62: OoooooooOO
if 33 - 33: O0 . i11iIiiIii % I1i1iI1i
if 50 - 50: Ii1Ii1iiii11
if 81 - 81: i11iIiiIii * iIii1I11I1II1 / O00oOoOoO0o0O * ooO
if 83 - 83: i11iIiiIii - iii1I1I * i11iIiiIii
if 59 - 59: i1 - OoooooooOO / Ii1Ii1iiii11 + II . I1i1iI1i - i1
if 29 - 29: i11Ii11I1Ii1i
if 26 - 26: O0 % ooO - OOooo0000ooo . ooO
if 70 - 70: I1i1iI1i + OOoO / i1 + Ii1Ii1iiii11 / iii1I1I
if 33 - 33: OoooooooOO . O0
if 59 - 59: iIii1I11I1II1
if 45 - 45: O0
if 78 - 78: OOoO - iIii1I11I1II1 + o0000o0o0000o - II - o0000o0o0000o
if 21 - 21: OoooooooOO . O0 / i11iIiiIii
if 86 - 86: Oo0ooO0oo0oO / ooO
if 40 - 40: iIii1I11I1II1 / Ii1Ii1iiii11 / iii1I1I + II * ooO
if 1 - 1: O0oo0OO0 * Ii1Ii1iiii11 + OOooo0000ooo . i11Ii11I1Ii1i / Ii1Ii1iiii11
if 91 - 91: ooo0Oo0 + OOoO - O00oOoOoO0o0O % Oo0ooO0oo0oO . i1
if 51 - 51: ooO / OOoO
if 51 - 51: Ii1Ii1iiii11 * i11Ii11I1Ii1i - o0000o0o0000o + i1
if 46 - 46: I1i1iI1i - i11iIiiIii % O0oo0OO0 / ooo0Oo0 - Oo0ooO0oo0oO
if 88 - 88: i11Ii11I1Ii1i * iii1I1I / O0oo0OO0 - ooO / i1IIi . o0000o0o0000o
if 26 - 26: i11iIiiIii - Ii1Ii1iiii11
if 45 - 45: Ii1Ii1iiii11 + II111iiii % i1
if 55 - 55: Ii1Ii1iiii11 - i11Ii11I1Ii1i % iii1I1I
if 61 - 61: Ii1Ii1iiii11
if 22 - 22: iIii1I11I1II1 / Ii1Ii1iiii11 / iii1I1I - I1i1iI1i
if 21 - 21: i11Ii11I1Ii1i . i11iIiiIii * OOoO . ooO / ooO
if 42 - 42: OoooooooOO / o0000o0o0000o . I1i1iI1i / O0 - OOooo0000ooo * OOooo0000ooo
if 1 - 1: ooo0Oo0 % o0000o0o0000o
if 97 - 97: Oo0ooO0oo0oO
if 13 - 13: Oo0ooO0oo0oO % ooO . O0 / O00oOoOoO0o0O % O00oOoOoO0o0O
if 19 - 19: o0000o0o0000o % Ii1Ii1iiii11 - Ii1Ii1iiii11 % iii1I1I . ooO - OoooooooOO
if 100 - 100: iii1I1I + ooo0Oo0 + I1i1iI1i . i1IIi % OoooooooOO
if 64 - 64: O0 % i1IIi * o0000o0o0000o - ooo0Oo0 + O00oOoOoO0o0O
if 65 - 65: Oo0ooO0oo0oO . i11iIiiIii
if 36 - 36: i11Ii11I1Ii1i * i1 + OOooo0000ooo * i1 . II - iIii1I11I1II1
if 14 - 14: OOoO * i11Ii11I1Ii1i + i11iIiiIii
if 84 - 84: i1 / II111iiii
if 86 - 86: iii1I1I
if 97 - 97: II111iiii
if 38 - 38: iii1I1I
if 42 - 42: I1i1iI1i
if 8 - 8: i11iIiiIii / Ii1Ii1iiii11
if 33 - 33: o0000o0o0000o * OOooo0000ooo - O0 + iii1I1I / OOooo0000ooo
if 19 - 19: i1IIi % II111iiii
if 85 - 85: OOooo0000ooo - I1i1iI1i % ooO - II111iiii
if 56 - 56: ooo0Oo0 * i11iIiiIii
if 92 - 92: II111iiii - O0 . o0000o0o0000o
if 59 - 59: Oo0ooO0oo0oO
if 47 - 47: II111iiii - II - ooo0Oo0
if 9 - 9: II - OOooo0000ooo
if 64 - 64: i1IIi
if 71 - 71: OOooo0000ooo * I1i1iI1i
if 99 - 99: I1i1iI1i
if 28 - 28: OoooooooOO % O0 - ooO / I1i1iI1i / iii1I1I
if 41 - 41: II111iiii * OOooo0000ooo / O0oo0OO0 . i11Ii11I1Ii1i
if 50 - 50: OoooooooOO + iIii1I11I1II1 / i11Ii11I1Ii1i / ooO . i11iIiiIii . Ii1Ii1iiii11
if 75 - 75: iIii1I11I1II1 % Ii1Ii1iiii11 / ooO - i1 % i11iIiiIii
if 11 - 11: OOoO . ooo0Oo0
if 87 - 87: ooO + ooO
if 45 - 45: i1IIi - O00oOoOoO0o0O
if 87 - 87: Oo0ooO0oo0oO - O0oo0OO0 * O0oo0OO0 / ooo0Oo0 . OOoO * I1i1iI1i
if 21 - 21: II111iiii
if 29 - 29: Oo0ooO0oo0oO % ooo0Oo0
if 7 - 7: i1IIi / OOooo0000ooo / i1
if 97 - 97: O0oo0OO0 + iIii1I11I1II1
if 79 - 79: Ii1Ii1iiii11 + i11Ii11I1Ii1i - II111iiii . O00oOoOoO0o0O
if 26 - 26: OOooo0000ooo
if 52 - 52: O0 + Ii1Ii1iiii11
if 11 - 11: i1IIi / o0000o0o0000o * II * o0000o0o0000o * Ii1Ii1iiii11 - i11iIiiIii
if 96 - 96: II % II
if 1 - 1: iii1I1I . ooo0Oo0
if 26 - 26: i11Ii11I1Ii1i - Ii1Ii1iiii11 % O00oOoOoO0o0O - i11Ii11I1Ii1i + OOooo0000ooo
if 33 - 33: ooo0Oo0 + Oo0ooO0oo0oO - II + iIii1I11I1II1 % i1IIi * OOooo0000ooo
if 21 - 21: O0 * Ii1Ii1iiii11 % O0oo0OO0
if 14 - 14: O0 / o0000o0o0000o / Ii1Ii1iiii11 + OOooo0000ooo - OOooo0000ooo
if 10 - 10: O0 - II / o0000o0o0000o % Oo0ooO0oo0oO / OoooooooOO / ooo0Oo0
if 73 - 73: Ii1Ii1iiii11 + OOooo0000ooo % I1i1iI1i . II / ooO . o0000o0o0000o
if 76 - 76: OOoO . II * OoooooooOO % i1
if 24 - 24: OoooooooOO
if 83 - 83: O0 / O0oo0OO0
if 62 - 62: OOoO
if 73 - 73: ooo0Oo0 % O0oo0OO0 * ooO
if 84 - 84: O00oOoOoO0o0O
if 18 - 18: OoooooooOO
if 85 - 85: OoooooooOO . O0oo0OO0 . O0oo0OO0
if 70 - 70: OOoO
if 72 - 72: o0000o0o0000o - Ii1Ii1iiii11 - iii1I1I - i1 + ooO - i1IIi
if 45 - 45: O0oo0OO0 * iii1I1I
if 61 - 61: i1 % II111iiii / Oo0ooO0oo0oO % II . iIii1I11I1II1 % O0
if 74 - 74: II * i11Ii11I1Ii1i + i1 % O0
if 18 - 18: i1IIi % OOooo0000ooo . O0 - O0 - O0 - II111iiii
if 55 - 55: Oo0ooO0oo0oO . iIii1I11I1II1 * ooO % iIii1I11I1II1 . O0oo0OO0
if 43 - 43: ooo0Oo0 . ooO + iii1I1I * i11iIiiIii
if 2 - 2: ooO
if 3 - 3: iii1I1I . i1 % O0 - Ii1Ii1iiii11 / O0
if 79 - 79: ooo0Oo0 + i11Ii11I1Ii1i % Ii1Ii1iiii11 % iii1I1I
if 68 - 68: II111iiii - OoooooooOO / iIii1I11I1II1 - I1i1iI1i % II111iiii
if 53 - 53: i1 . i11Ii11I1Ii1i / O00oOoOoO0o0O . O0oo0OO0 . i11iIiiIii
if 60 - 60: II111iiii
if 25 - 25: O00oOoOoO0o0O + I1i1iI1i - O0oo0OO0
if 57 - 57: II111iiii . i1IIi
if 33 - 33: i1 + O00oOoOoO0o0O % OOoO . i11Ii11I1Ii1i
if 6 - 6: OOooo0000ooo + II
if 62 - 62: i11Ii11I1Ii1i . o0000o0o0000o - OoooooooOO * II111iiii . i11iIiiIii
if 13 - 13: iIii1I11I1II1 * I1i1iI1i - i11iIiiIii
if 63 - 63: OoooooooOO * o0000o0o0000o
if 50 - 50: O00oOoOoO0o0O - I1i1iI1i % II111iiii . O0 . i11Ii11I1Ii1i % II111iiii
if 18 - 18: OOoO % OoooooooOO + O0oo0OO0 / OOoO
if 37 - 37: i1IIi - ooo0Oo0 / OOooo0000ooo . II111iiii % Ii1Ii1iiii11
if 39 - 39: ooo0Oo0 % i11iIiiIii * O0oo0OO0
if 23 - 23: ooO + Ii1Ii1iiii11 / i11iIiiIii * O00oOoOoO0o0O . O0oo0OO0
if 28 - 28: i1 - I1i1iI1i
if 92 - 92: O00oOoOoO0o0O % I1i1iI1i - Ii1Ii1iiii11 / Ii1Ii1iiii11 / Oo0ooO0oo0oO
if 84 - 84: ooO
if 4 - 4: OOooo0000ooo . o0000o0o0000o / ooo0Oo0 / i1 + II111iiii
if 32 - 32: i1IIi + iIii1I11I1II1 . II . OOoO - ooo0Oo0
if 55 - 55: II / OoooooooOO - O0oo0OO0 / iii1I1I
if 23 - 23: OOoO * o0000o0o0000o * I1i1iI1i - iii1I1I % Oo0ooO0oo0oO + I1i1iI1i
if 41 - 41: OOooo0000ooo * OoooooooOO . Ii1Ii1iiii11 % i11iIiiIii
if 11 - 11: iIii1I11I1II1 . o0000o0o0000o - O00oOoOoO0o0O / OOoO + II111iiii
if 29 - 29: OOoO . i11iIiiIii + i1IIi - ooo0Oo0 + O0 . iii1I1I
if 8 - 8: I1i1iI1i
if 78 - 78: i1IIi - O00oOoOoO0o0O
if 48 - 48: ooo0Oo0 - OoooooooOO + o0000o0o0000o % I1i1iI1i - Oo0ooO0oo0oO . iii1I1I
if 42 - 42: o0000o0o0000o
if 70 - 70: I1i1iI1i / OOoO + i11Ii11I1Ii1i % iii1I1I % O00oOoOoO0o0O + O0oo0OO0
if 80 - 80: ooO
if 12 - 12: ooo0Oo0
if 2 - 2: OoooooooOO
if 100 - 100: O00oOoOoO0o0O / O0 * i11iIiiIii * OoooooooOO
if 46 - 46: O0 % OoooooooOO
if 22 - 22: i1 + OoooooooOO - Oo0ooO0oo0oO - O0oo0OO0 * o0000o0o0000o - i11Ii11I1Ii1i
if 99 - 99: Ii1Ii1iiii11 / iii1I1I . ooo0Oo0 - ooo0Oo0 * iii1I1I
if 24 - 24: OOoO * O0oo0OO0 - i11Ii11I1Ii1i / iIii1I11I1II1 - O00oOoOoO0o0O . ooO
if 2 - 2: Ii1Ii1iiii11 - O0 - II / OOoO * Oo0ooO0oo0oO
if 26 - 26: II + o0000o0o0000o - i11Ii11I1Ii1i + OOooo0000ooo % ooO
if 84 - 84: OOoO % ooo0Oo0 % O0 * I1i1iI1i
if 15 - 15: i11Ii11I1Ii1i - iIii1I11I1II1 - II111iiii - OOooo0000ooo % II
if 80 - 80: OOooo0000ooo * i1 . i1IIi % ooo0Oo0 % II + Ii1Ii1iiii11
if 6 - 6: II . i11Ii11I1Ii1i . O0oo0OO0 + OOooo0000ooo
if 65 - 65: II / Ii1Ii1iiii11
if 23 - 23: ooO / ooO * I1i1iI1i * ooO
if 57 - 57: i1
if 29 - 29: iii1I1I
if 41 - 41: o0000o0o0000o * O0oo0OO0 - i1 . ooo0Oo0
if 41 - 41: iIii1I11I1II1 - O0 - II - i11Ii11I1Ii1i + o0000o0o0000o
if 22 - 22: O0 % OOooo0000ooo % i1 % iii1I1I
if 34 - 34: i1 . O00oOoOoO0o0O % II . i1 % OOooo0000ooo / OOooo0000ooo
if 84 - 84: ooo0Oo0
if 1 - 1: i11Ii11I1Ii1i - O00oOoOoO0o0O * iIii1I11I1II1 * O00oOoOoO0o0O * i1IIi
if 9 - 9: i1 - i1
if 3 - 3: O0 + O0 - O0 - O0 % OoooooooOO + i11Ii11I1Ii1i
if 20 - 20: O0oo0OO0 + OOoO . II111iiii / i11iIiiIii
if 50 - 50: OoooooooOO / O0oo0OO0 % iIii1I11I1II1
if 41 - 41: II % II + OOooo0000ooo . i1 % o0000o0o0000o * Ii1Ii1iiii11
if 57 - 57: ooo0Oo0 . o0000o0o0000o . II111iiii % OoooooooOO * O0 + iIii1I11I1II1
if 94 - 94: i1IIi * O0oo0OO0 * Oo0ooO0oo0oO
if 93 - 93: Ii1Ii1iiii11 / ooO * O0
if 17 - 17: O0oo0OO0 / Ii1Ii1iiii11 % iii1I1I
if 47 - 47: O00oOoOoO0o0O * O0oo0OO0 / I1i1iI1i * iii1I1I
if 60 - 60: II / OOooo0000ooo . i11iIiiIii / O0oo0OO0 % II111iiii
if 6 - 6: i1 % I1i1iI1i + o0000o0o0000o
if 91 - 91: I1i1iI1i + O0 * i11Ii11I1Ii1i * OOooo0000ooo * II
if 83 - 83: OoooooooOO
if 52 - 52: I1i1iI1i / Oo0ooO0oo0oO % i11Ii11I1Ii1i % O0oo0OO0 / OOooo0000ooo % I1i1iI1i
if 88 - 88: ooO / i11iIiiIii / ooo0Oo0 / i11iIiiIii * II % OOoO
if 43 - 43: Oo0ooO0oo0oO * O0oo0OO0 % i1IIi * ooo0Oo0 + iIii1I11I1II1
if 80 - 80: I1i1iI1i . i1 . OoooooooOO
if 63 - 63: Ii1Ii1iiii11 . ooO
if 66 - 66: iii1I1I
if 99 - 99: O0oo0OO0 % O0 . o0000o0o0000o - II . O00oOoOoO0o0O / Oo0ooO0oo0oO
if 60 - 60: II
if 78 - 78: i11Ii11I1Ii1i + II111iiii
if 55 - 55: OoooooooOO
if 90 - 90: iii1I1I
if 4 - 4: ooO % Ii1Ii1iiii11 - ooO - I1i1iI1i
if 30 - 30: OOooo0000ooo
if 34 - 34: i11Ii11I1Ii1i - II111iiii - I1i1iI1i + i1 + o0000o0o0000o
if 70 - 70: OoooooooOO + O0oo0OO0 * O00oOoOoO0o0O
if 20 - 20: i11iIiiIii - II111iiii - Ii1Ii1iiii11 % i11Ii11I1Ii1i . Ii1Ii1iiii11
if 50 - 50: iIii1I11I1II1 + o0000o0o0000o - OOoO - OoooooooOO
if 84 - 84: Oo0ooO0oo0oO - OOoO
if 80 - 80: i11iIiiIii % ooO - O00oOoOoO0o0O % ooO
if 89 - 89: ooo0Oo0 * OOoO + Oo0ooO0oo0oO / i11iIiiIii
if 68 - 68: OoooooooOO * OOoO
if 86 - 86: I1i1iI1i / Oo0ooO0oo0oO
if 40 - 40: i1
if 62 - 62: Ii1Ii1iiii11 / ooO
if 74 - 74: i1 % o0000o0o0000o / o0000o0o0000o - iIii1I11I1II1 - II111iiii + ooO
if 92 - 92: OOoO % o0000o0o0000o
if 18 - 18: Ii1Ii1iiii11 + o0000o0o0000o / ooO / i11Ii11I1Ii1i + iIii1I11I1II1 % OOooo0000ooo
if 94 - 94: OOoO
if 37 - 37: i11Ii11I1Ii1i
if 52 - 52: II * iii1I1I . ooO + i1IIi % i11Ii11I1Ii1i / iIii1I11I1II1
if 68 - 68: o0000o0o0000o - Oo0ooO0oo0oO . i11iIiiIii + I1i1iI1i
if 71 - 71: i11iIiiIii / i1IIi * iii1I1I / Oo0ooO0oo0oO
if 33 - 33: OOoO . O00oOoOoO0o0O
if 89 - 89: i1 + i1IIi - OOooo0000ooo + Ii1Ii1iiii11 . II111iiii
if 85 - 85: iIii1I11I1II1 - ooo0Oo0 * O00oOoOoO0o0O . i11Ii11I1Ii1i + o0000o0o0000o
if 13 - 13: O0 + iIii1I11I1II1 % II111iiii + iIii1I11I1II1
if 85 - 85: iii1I1I * iIii1I11I1II1 . i1 / i1
if 43 - 43: iii1I1I
if 78 - 78: O0oo0OO0 % II111iiii + Oo0ooO0oo0oO / iii1I1I
if 34 - 34: I1i1iI1i % II + ooo0Oo0 * OOoO / i11Ii11I1Ii1i
if 18 - 18: Ii1Ii1iiii11
if 92 - 92: O0oo0OO0 % iIii1I11I1II1 / OOooo0000ooo * i1 . i1IIi + i11Ii11I1Ii1i
if 24 - 24: OOooo0000ooo . i1 * OOooo0000ooo % i11iIiiIii . i11iIiiIii + i1IIi
if 64 - 64: iIii1I11I1II1 / OOooo0000ooo / O00oOoOoO0o0O - II
if 100 - 100: OOooo0000ooo + i1IIi * O0oo0OO0
if 64 - 64: i11Ii11I1Ii1i * i11iIiiIii . O00oOoOoO0o0O
if 52 - 52: O00oOoOoO0o0O / Ii1Ii1iiii11 / i1 - I1i1iI1i / i1
if 74 - 74: i1IIi . iIii1I11I1II1
if 85 - 85: iii1I1I
if 10 - 10: O0 . II111iiii / OoooooooOO
if 72 - 72: OoooooooOO . I1i1iI1i + O0
if 46 - 46: Oo0ooO0oo0oO * OOoO / i11Ii11I1Ii1i + O00oOoOoO0o0O + OOooo0000ooo
if 95 - 95: I1i1iI1i - ooo0Oo0
if 67 - 67: II * O00oOoOoO0o0O % I1i1iI1i
if 19 - 19: Oo0ooO0oo0oO . ooO . OoooooooOO
if 79 - 79: ooO * Ii1Ii1iiii11 * iii1I1I * II / II
if 62 - 62: Ii1Ii1iiii11 * ooo0Oo0 % II - i1IIi - II
if 24 - 24: ooO
if 71 - 71: OOooo0000ooo - i1IIi
if 56 - 56: Oo0ooO0oo0oO + i11Ii11I1Ii1i
if 74 - 74: i1 / o0000o0o0000o / II111iiii - i1 / i11Ii11I1Ii1i % OOoO
if 19 - 19: OOooo0000ooo % OoooooooOO + OoooooooOO
if 7 - 7: i1IIi
if 91 - 91: Oo0ooO0oo0oO - Oo0ooO0oo0oO . OOooo0000ooo
if 33 - 33: o0000o0o0000o - iIii1I11I1II1 / ooo0Oo0 % O0
if 80 - 80: OOooo0000ooo % OoooooooOO - OOooo0000ooo
if 27 - 27: o0000o0o0000o - I1i1iI1i * II - iii1I1I
if 22 - 22: O00oOoOoO0o0O % OoooooooOO - O00oOoOoO0o0O - i1 . ooo0Oo0
if 100 - 100: II111iiii / o0000o0o0000o / i1 - II * iIii1I11I1II1
if 7 - 7: i1IIi . OOooo0000ooo % i11iIiiIii * II . OOoO % II
if 35 - 35: iii1I1I
if 48 - 48: OoooooooOO % OoooooooOO - O0oo0OO0 . Oo0ooO0oo0oO
if 22 - 22: Ii1Ii1iiii11 . i11iIiiIii . OoooooooOO . i1IIi
if 12 - 12: Oo0ooO0oo0oO % ooO + i11Ii11I1Ii1i . O0 % iIii1I11I1II1
if 41 - 41: OoooooooOO
if 13 - 13: OOoO + o0000o0o0000o - o0000o0o0000o % i11Ii11I1Ii1i / OOoO
if 4 - 4: iii1I1I + ooO - OOooo0000ooo + i1
if 78 - 78: ooo0Oo0
if 29 - 29: II111iiii
if 79 - 79: iIii1I11I1II1 - i11iIiiIii + Ii1Ii1iiii11 - II111iiii . iIii1I11I1II1
if 84 - 84: O00oOoOoO0o0O % OOoO * O0 * OOoO
if 66 - 66: ooO / iIii1I11I1II1 - Oo0ooO0oo0oO % O0 . Ii1Ii1iiii11
if 12 - 12: O00oOoOoO0o0O + iii1I1I
if 37 - 37: i1IIi * i11iIiiIii
if 95 - 95: i11iIiiIii % o0000o0o0000o * O00oOoOoO0o0O + i1IIi . O0 + II
if 7 - 7: O0oo0OO0 * i11iIiiIii * iIii1I11I1II1 / ooO / o0000o0o0000o
if 35 - 35: i1 * ooO
if 65 - 65: II111iiii % i1IIi
if 13 - 13: O0oo0OO0 * o0000o0o0000o + O00oOoOoO0o0O - OOooo0000ooo
if 31 - 31: O0oo0OO0
if 68 - 68: O0oo0OO0 + i1IIi / iIii1I11I1II1 + II111iiii * iIii1I11I1II1 + II
if 77 - 77: i11iIiiIii - o0000o0o0000o . II % O00oOoOoO0o0O . ooo0Oo0
if 9 - 9: I1i1iI1i
if 55 - 55: ooO % iIii1I11I1II1 + OOoO . Ii1Ii1iiii11
if 71 - 71: i11iIiiIii / i1IIi + Oo0ooO0oo0oO
if 23 - 23: i11iIiiIii
if 88 - 88: II111iiii - i1 / OoooooooOO
if 71 - 71: II
if 19 - 19: O00oOoOoO0o0O - O0oo0OO0 + i11iIiiIii / iIii1I11I1II1
if 1 - 1: OOooo0000ooo % i1IIi
if 41 - 41: O0oo0OO0 * O0oo0OO0 / i1 + II . I1i1iI1i
if 84 - 84: i11iIiiIii + O0oo0OO0 * iii1I1I + II / ooo0Oo0
if 80 - 80: II
if 67 - 67: II111iiii
if 2 - 2: I1i1iI1i - O0 * ooo0Oo0 % OOooo0000ooo
if 64 - 64: i1IIi . Ii1Ii1iiii11
if 7 - 7: i11Ii11I1Ii1i . i1 - i1 / o0000o0o0000o % O00oOoOoO0o0O
if 61 - 61: i11Ii11I1Ii1i - II / i1 % II + O0oo0OO0 / O00oOoOoO0o0O
if 10 - 10: i11iIiiIii / Oo0ooO0oo0oO
if 27 - 27: iii1I1I / OoooooooOO
if 74 - 74: II % o0000o0o0000o - O0oo0OO0 * OOoO . OoooooooOO * O0oo0OO0
if 99 - 99: Oo0ooO0oo0oO . i1 - OoooooooOO - O0
if 6 - 6: ooO
if 3 - 3: O0 - o0000o0o0000o * ooo0Oo0 * ooO / ooo0Oo0
if 58 - 58: ooo0Oo0 * iIii1I11I1II1 + Ii1Ii1iiii11 . Ii1Ii1iiii11
if 74 - 74: Ii1Ii1iiii11 - I1i1iI1i * OOooo0000ooo % Ii1Ii1iiii11
if 93 - 93: iIii1I11I1II1 / Oo0ooO0oo0oO % O00oOoOoO0o0O * o0000o0o0000o - O0oo0OO0 - I1i1iI1i
if 44 - 44: OoooooooOO
if 82 - 82: Oo0ooO0oo0oO . Oo0ooO0oo0oO
if 10 - 10: O00oOoOoO0o0O * II . i11Ii11I1Ii1i . OoooooooOO . ooO * II
if 80 - 80: o0000o0o0000o + OOoO . o0000o0o0000o + ooO
if 85 - 85: i11iIiiIii . OOoO + ooo0Oo0 / ooo0Oo0
if 43 - 43: OOooo0000ooo . OoooooooOO - II111iiii
if 90 - 90: iii1I1I - iIii1I11I1II1 + II * ooO * i11Ii11I1Ii1i
if 19 - 19: o0000o0o0000o * II111iiii % O00oOoOoO0o0O - i1IIi
if 27 - 27: Oo0ooO0oo0oO . O0 / II . iIii1I11I1II1
if 15 - 15: ooo0Oo0 + O0oo0OO0 % iIii1I11I1II1 - II - i1IIi % I1i1iI1i
if 54 - 54: OOooo0000ooo - II111iiii . Ii1Ii1iiii11 + ooo0Oo0
if 45 - 45: i11Ii11I1Ii1i + II111iiii . i1 / II
if 76 - 76: ooo0Oo0 + i1 - OOooo0000ooo * iIii1I11I1II1 % i1IIi
if 72 - 72: Ii1Ii1iiii11 + II111iiii . O0 - i1 / OoooooooOO . o0000o0o0000o
if 28 - 28: iIii1I11I1II1 . O0
if 32 - 32: OoooooooOO
if 29 - 29: II
if 41 - 41: ooo0Oo0
if 49 - 49: ooo0Oo0 % II111iiii . ooo0Oo0 - I1i1iI1i - OOoO * OOooo0000ooo
if 47 - 47: O0 . I1i1iI1i / ooo0Oo0 * i1
if 63 - 63: o0000o0o0000o - i11Ii11I1Ii1i - i1 - Ii1Ii1iiii11 / i11Ii11I1Ii1i + O0oo0OO0
if 94 - 94: OOooo0000ooo / iii1I1I . II111iiii
if 32 - 32: i11Ii11I1Ii1i . ooO % ooO . Oo0ooO0oo0oO
if 37 - 37: ooO + O0 + ooO . i1 . I1i1iI1i
if 78 - 78: iii1I1I / OOoO + I1i1iI1i . O00oOoOoO0o0O / O0
if 49 - 49: II
if 66 - 66: I1i1iI1i . II
if 18 - 18: O00oOoOoO0o0O + OOooo0000ooo
if 79 - 79: O0oo0OO0 - O0 + II111iiii % ooo0Oo0 . iii1I1I
if 43 - 43: iii1I1I % II * ooo0Oo0
if 31 - 31: ooo0Oo0 / i1
if 3 - 3: OOooo0000ooo
if 37 - 37: ooo0Oo0 * OoooooooOO * OOoO + O00oOoOoO0o0O . iii1I1I
if 61 - 61: ooO . ooO
if 17 - 17: II111iiii / Ii1Ii1iiii11
if 80 - 80: ooO * O0oo0OO0 + ooo0Oo0
if 62 - 62: OoooooooOO . O0 % O00oOoOoO0o0O
if 98 - 98: I1i1iI1i * O00oOoOoO0o0O - ooo0Oo0 . Ii1Ii1iiii11
if 2 - 2: O00oOoOoO0o0O - Ii1Ii1iiii11 % iIii1I11I1II1
if 88 - 88: o0000o0o0000o - O0oo0OO0
if 79 - 79: i1
if 45 - 45: II111iiii + i1 . OOoO . O0 * i1IIi - ooo0Oo0
if 48 - 48: II + O00oOoOoO0o0O
if 76 - 76: II
if 98 - 98: II111iiii + iii1I1I - II . ooo0Oo0
if 51 - 51: ooo0Oo0 + i11iIiiIii * O0oo0OO0 % O00oOoOoO0o0O / iii1I1I - iIii1I11I1II1
if 20 - 20: o0000o0o0000o . OOoO . ooo0Oo0 + OOoO - ooO * i11Ii11I1Ii1i
if 82 - 82: O0oo0OO0
if 78 - 78: II111iiii / OOoO - i11iIiiIii + II * O00oOoOoO0o0O
if 17 - 17: Oo0ooO0oo0oO
if 72 - 72: i1 . O00oOoOoO0o0O - i11iIiiIii / iii1I1I
if 64 - 64: i11Ii11I1Ii1i
if 80 - 80: I1i1iI1i % iIii1I11I1II1
if 63 - 63: OOooo0000ooo * i11iIiiIii
if 86 - 86: OOoO % OOoO - Oo0ooO0oo0oO + o0000o0o0000o / iii1I1I * OoooooooOO
if 26 - 26: II111iiii * i1 + I1i1iI1i / O0 + i1IIi - OOoO
if 56 - 56: ooO
if 76 - 76: i1IIi % iIii1I11I1II1 - I1i1iI1i + OOooo0000ooo - OOoO
if 81 - 81: II + OoooooooOO - ooO * O0
if 100 - 100: iIii1I11I1II1 - Oo0ooO0oo0oO
if 28 - 28: O00oOoOoO0o0O . O0 . OOoO
if 60 - 60: II111iiii + o0000o0o0000o / i11Ii11I1Ii1i % OoooooooOO - i1IIi
if 57 - 57: Ii1Ii1iiii11
if 99 - 99: O00oOoOoO0o0O + o0000o0o0000o % Ii1Ii1iiii11 - I1i1iI1i
if 52 - 52: II
if 93 - 93: i1 . i11iIiiIii
if 24 - 24: ooO . O0oo0OO0 + o0000o0o0000o . i11Ii11I1Ii1i - II % i1
if 49 - 49: O0 . O00oOoOoO0o0O / ooo0Oo0
if 29 - 29: II / i11Ii11I1Ii1i * O0 - i11iIiiIii - O0oo0OO0 + ooo0Oo0
if 86 - 86: iii1I1I / II * ooo0Oo0 % i11iIiiIii
if 20 - 20: i1 . OoooooooOO + i1 + Ii1Ii1iiii11 * II
if 44 - 44: i11iIiiIii
if 69 - 69: ooO * O0 + i11iIiiIii
if 65 - 65: O0 / i1 . i1IIi * i1 / iIii1I11I1II1 - i11Ii11I1Ii1i
if 93 - 93: Oo0ooO0oo0oO % i11iIiiIii - ooo0Oo0 % O0oo0OO0
if 55 - 55: I1i1iI1i . II
if 63 - 63: i11Ii11I1Ii1i
if 79 - 79: II - i11Ii11I1Ii1i - I1i1iI1i . ooO
if 65 - 65: i11iIiiIii . O0oo0OO0 % i1 + OOooo0000ooo - i11iIiiIii
if 60 - 60: o0000o0o0000o
if 14 - 14: O00oOoOoO0o0O % i11Ii11I1Ii1i * i1 - i11iIiiIii / II * i11iIiiIii
if 95 - 95: iIii1I11I1II1 + Oo0ooO0oo0oO . iii1I1I + Oo0ooO0oo0oO * OOoO + ooO
if 14 - 14: ooo0Oo0 - O0
if 68 - 68: II111iiii - II - O0oo0OO0 * iIii1I11I1II1 / iii1I1I * II
if 45 - 45: o0000o0o0000o * OOoO / iIii1I11I1II1 / iii1I1I % II111iiii
if 49 - 49: ooo0Oo0 / i1 . i1 . i1 + i11iIiiIii % OOoO
if 7 - 7: OOooo0000ooo * Ii1Ii1iiii11 + Oo0ooO0oo0oO
if 22 - 22: i1
if 48 - 48: II . iii1I1I
if 73 - 73: O0 . o0000o0o0000o - OoooooooOO % OOoO % i1IIi
if 14 - 14: o0000o0o0000o + ooo0Oo0 * O00oOoOoO0o0O
if 49 - 49: O00oOoOoO0o0O
if 57 - 57: O0 * Ii1Ii1iiii11 - i1 - iIii1I11I1II1 * i1
if 9 - 9: OOooo0000ooo . OOoO
if 23 - 23: O0 % OoooooooOO - O0 . iii1I1I + i11iIiiIii
if 96 - 96: Ii1Ii1iiii11 % O0
if 51 - 51: iii1I1I - i1 / II . II + II
if 87 - 87: II111iiii . ooo0Oo0 * O0oo0OO0
if 74 - 74: I1i1iI1i % Oo0ooO0oo0oO . i1 % o0000o0o0000o . O0 % II111iiii
if 5 - 5: i11Ii11I1Ii1i - OoooooooOO / Oo0ooO0oo0oO
if 30 - 30: OOoO % I1i1iI1i + i1IIi * OoooooooOO * O0oo0OO0 - II111iiii
if 55 - 55: O0oo0OO0
if 20 - 20: Ii1Ii1iiii11 * o0000o0o0000o * I1i1iI1i - Ii1Ii1iiii11
if 32 - 32: ooo0Oo0 * i11Ii11I1Ii1i
if 85 - 85: i11iIiiIii . O0oo0OO0 + O0oo0OO0
if 28 - 28: O00oOoOoO0o0O
if 62 - 62: O00oOoOoO0o0O + OoooooooOO / i1
if 60 - 60: ooo0Oo0 / Oo0ooO0oo0oO . OOoO % ooO
if 61 - 61: O0 . ooo0Oo0 . O0 * i11iIiiIii * II111iiii / o0000o0o0000o
if 69 - 69: OOoO
if 17 - 17: OOoO
if 38 - 38: o0000o0o0000o % ooO
if 9 - 9: O0 . iIii1I11I1II1
if 44 - 44: II % OOooo0000ooo
if 6 - 6: O0oo0OO0
if 82 - 82: iIii1I11I1II1 . OOoO / OOooo0000ooo / ooO * II111iiii % i11Ii11I1Ii1i
if 62 - 62: II111iiii
if 96 - 96: OOoO % Oo0ooO0oo0oO * II
if 94 - 94: O00oOoOoO0o0O - i1IIi . O0 % O00oOoOoO0o0O . Ii1Ii1iiii11
if 63 - 63: i11iIiiIii % II % iii1I1I . OOooo0000ooo * I1i1iI1i + ooO
if 77 - 77: I1i1iI1i
if 63 - 63: Ii1Ii1iiii11 * i11Ii11I1Ii1i + Ii1Ii1iiii11 * ooo0Oo0 + O00oOoOoO0o0O / II
if 15 - 15: O0 . II * II
if 65 - 65: o0000o0o0000o + O0 % I1i1iI1i
if 72 - 72: ooO . Oo0ooO0oo0oO / II111iiii
if 69 - 69: ooO * II111iiii - Ii1Ii1iiii11 - i1IIi + i11iIiiIii
if 50 - 50: OoooooooOO * i1IIi / i11Ii11I1Ii1i
if 83 - 83: i1IIi
if 38 - 38: OoooooooOO * iIii1I11I1II1
if 54 - 54: OoooooooOO . o0000o0o0000o
if 71 - 71: ooo0Oo0
if 31 - 31: OOoO . i11iIiiIii . O0oo0OO0 * O00oOoOoO0o0O % ooo0Oo0 . I1i1iI1i
if 92 - 92: OoooooooOO / O0 * i1IIi + iIii1I11I1II1
if 93 - 93: Ii1Ii1iiii11 % o0000o0o0000o
if 46 - 46: II * Oo0ooO0oo0oO * OOooo0000ooo * II . II
if 43 - 43: Ii1Ii1iiii11 . i1IIi
if 68 - 68: OOooo0000ooo % O00oOoOoO0o0O . O0 - Oo0ooO0oo0oO + II . i11iIiiIii
if 45 - 45: iii1I1I
if 17 - 17: OoooooooOO - Ii1Ii1iiii11 + ooo0Oo0 . OoooooooOO % O00oOoOoO0o0O
if 92 - 92: o0000o0o0000o - ooO % O0oo0OO0 - I1i1iI1i % i1IIi
if 38 - 38: II . OOoO / Oo0ooO0oo0oO % OOoO
if 10 - 10: O0 . iii1I1I * I1i1iI1i / i1
if 61 - 61: O00oOoOoO0o0O - o0000o0o0000o
if 51 - 51: i1 * Ii1Ii1iiii11 / O0 / O0
if 52 - 52: OoooooooOO % O0
if 56 - 56: i11Ii11I1Ii1i - i1IIi * OoooooooOO - II111iiii
if 28 - 28: i1IIi / OOoO . I1i1iI1i
if 11 - 11: O00oOoOoO0o0O * OoooooooOO - i11iIiiIii
if 13 - 13: i11iIiiIii . O0 / ooO * i1IIi
if 14 - 14: OOooo0000ooo + OOooo0000ooo . OOoO / ooo0Oo0 . iIii1I11I1II1
if 10 - 10: II111iiii . ooO / i1
if 35 - 35: i1 / O00oOoOoO0o0O + O0 * iIii1I11I1II1 - O0
if 3 - 3: II
if 42 - 42: OOoO % O00oOoOoO0o0O + OOooo0000ooo - OOoO . iIii1I11I1II1 - ooo0Oo0
if 27 - 27: i1 % O00oOoOoO0o0O . II . i1IIi % Oo0ooO0oo0oO . I1i1iI1i
if 37 - 37: i1 + o0000o0o0000o * ooo0Oo0 + OOooo0000ooo
if 39 - 39: O0 * O00oOoOoO0o0O - iii1I1I + ooo0Oo0 / II111iiii
if 66 - 66: Ii1Ii1iiii11 + i11Ii11I1Ii1i % OoooooooOO
if 23 - 23: i11Ii11I1Ii1i . Oo0ooO0oo0oO + iIii1I11I1II1
if 17 - 17: OOooo0000ooo
if 12 - 12: i1IIi . O0oo0OO0
if 14 - 14: ooO + II111iiii % ooO . i11Ii11I1Ii1i * Ii1Ii1iiii11
if 54 - 54: Ii1Ii1iiii11 * OOoO - o0000o0o0000o
if 15 - 15: i1 / O0
if 61 - 61: i1IIi / i1IIi + Ii1Ii1iiii11 . o0000o0o0000o * Ii1Ii1iiii11
if 19 - 19: I1i1iI1i . II111iiii / i1IIi
if 82 - 82: O0 / i1 * O0oo0OO0 - OOoO + O00oOoOoO0o0O
if 47 - 47: II * iii1I1I / II + ooo0Oo0 * II111iiii
if 78 - 78: o0000o0o0000o - i1IIi + Oo0ooO0oo0oO + O00oOoOoO0o0O * II * I1i1iI1i
if 97 - 97: i1IIi
if 29 - 29: iii1I1I
if 37 - 37: II * o0000o0o0000o * iii1I1I * O0
if 35 - 35: iii1I1I - II * i1 + OOooo0000ooo / i1IIi
if 46 - 46: O00oOoOoO0o0O . Ii1Ii1iiii11 % O00oOoOoO0o0O / II111iiii * Ii1Ii1iiii11 * ooO
if 59 - 59: o0000o0o0000o * i1
if 31 - 31: OOoO / O0
if 57 - 57: i1IIi % Ii1Ii1iiii11
if 69 - 69: I1i1iI1i
if 69 - 69: o0000o0o0000o
if 83 - 83: iIii1I11I1II1 . I1i1iI1i + o0000o0o0000o . OoooooooOO / Ii1Ii1iiii11 + II111iiii
if 90 - 90: ooo0Oo0 * i1 / ooO
if 68 - 68: Oo0ooO0oo0oO
if 65 - 65: i11Ii11I1Ii1i
if 82 - 82: I1i1iI1i
if 80 - 80: i1IIi % Oo0ooO0oo0oO + O0oo0OO0 - OoooooooOO / iIii1I11I1II1 + o0000o0o0000o
if 65 - 65: ooo0Oo0
if 71 - 71: o0000o0o0000o % o0000o0o0000o . i11Ii11I1Ii1i + i11iIiiIii - i11iIiiIii
if 16 - 16: iIii1I11I1II1 / iii1I1I / o0000o0o0000o - i11iIiiIii . Ii1Ii1iiii11 / ooO
if 13 - 13: I1i1iI1i % O0 - o0000o0o0000o * OoooooooOO / O00oOoOoO0o0O - OoooooooOO
if 78 - 78: i11Ii11I1Ii1i % OoooooooOO
if 73 - 73: iii1I1I % Ii1Ii1iiii11 % OOooo0000ooo + i1IIi - OoooooooOO / i11Ii11I1Ii1i
if 78 - 78: OoooooooOO % i11Ii11I1Ii1i - i11iIiiIii
if 37 - 37: OOooo0000ooo % ooo0Oo0 % i1IIi
if 23 - 23: Ii1Ii1iiii11 - O0 + i11iIiiIii
if 98 - 98: OoooooooOO
if 61 - 61: I1i1iI1i . OOooo0000ooo . O0 + OoooooooOO + O0
if 65 - 65: i1IIi * ooO * OoooooooOO - OOooo0000ooo . i1 - O0oo0OO0
if 71 - 71: ooo0Oo0 * Oo0ooO0oo0oO
if 33 - 33: i1IIi . i1IIi * OoooooooOO % o0000o0o0000o * I1i1iI1i
if 64 - 64: Ii1Ii1iiii11 / Ii1Ii1iiii11 + II * ooO % ooO
if 87 - 87: O0oo0OO0 * O00oOoOoO0o0O
if 83 - 83: i1IIi * o0000o0o0000o - OOooo0000ooo / ooo0Oo0
if 48 - 48: i11Ii11I1Ii1i . II111iiii - Oo0ooO0oo0oO % i1IIi . Oo0ooO0oo0oO
if 32 - 32: ooo0Oo0 * iii1I1I - ooO . O00oOoOoO0o0O / O0 + ooo0Oo0
if 67 - 67: Oo0ooO0oo0oO % O00oOoOoO0o0O
if 7 - 7: i11iIiiIii % II / o0000o0o0000o % O00oOoOoO0o0O - O0oo0OO0
if 73 - 73: II
if 92 - 92: i11iIiiIii + O0 * OOoO
if 60 - 60: I1i1iI1i / O00oOoOoO0o0O
if 19 - 19: iIii1I11I1II1 . O0oo0OO0 / OoooooooOO
if 2 - 2: O0 - O0 % o0000o0o0000o / II
if 76 - 76: O0oo0OO0 * i11Ii11I1Ii1i - O0oo0OO0
if 57 - 57: OoooooooOO / Oo0ooO0oo0oO + i11Ii11I1Ii1i . ooo0Oo0
if 14 - 14: i11iIiiIii % ooO * I1i1iI1i * Oo0ooO0oo0oO
if 55 - 55: o0000o0o0000o * ooO * o0000o0o0000o
if 70 - 70: O0 . ooo0Oo0
if 33 - 33: ooO * ooo0Oo0
if 64 - 64: i11iIiiIii . iIii1I11I1II1
if 7 - 7: Oo0ooO0oo0oO % Ii1Ii1iiii11 + Oo0ooO0oo0oO - Oo0ooO0oo0oO * i11iIiiIii % O0oo0OO0
if 57 - 57: ooO / O0oo0OO0 + II
if 60 - 60: O0 * O00oOoOoO0o0O % ooO + OOooo0000ooo . O0oo0OO0 . O00oOoOoO0o0O
if 70 - 70: OOoO . II * i11Ii11I1Ii1i
if 97 - 97: i11Ii11I1Ii1i . iIii1I11I1II1 - ooO
if 23 - 23: II % OOoO
if 18 - 18: OoooooooOO . i1IIi + II111iiii
if 99 - 99: o0000o0o0000o - II - iii1I1I - o0000o0o0000o + O0oo0OO0 + II111iiii
if 34 - 34: o0000o0o0000o * OOoO
if 31 - 31: OOooo0000ooo . i11Ii11I1Ii1i
if 40 - 40: ooo0Oo0 - OOoO / II111iiii * i1IIi + OOooo0000ooo * II111iiii
if 53 - 53: II - i11iIiiIii . O0oo0OO0 / Oo0ooO0oo0oO - o0000o0o0000o
if 99 - 99: ooo0Oo0 - OOooo0000ooo - i1IIi / i11iIiiIii . OOooo0000ooo
if 58 - 58: ooO
if 12 - 12: iii1I1I . I1i1iI1i * OoooooooOO
if 64 - 64: Oo0ooO0oo0oO + OOooo0000ooo - i1IIi . II111iiii . O0oo0OO0
if 31 - 31: i11Ii11I1Ii1i . i1 - OOoO . iIii1I11I1II1 + OOoO . Oo0ooO0oo0oO
if 86 - 86: II - II / i1 - II * i1 + o0000o0o0000o
if 61 - 61: O00oOoOoO0o0O / II111iiii / O00oOoOoO0o0O / i1IIi . O00oOoOoO0o0O - OOooo0000ooo
if 30 - 30: OoooooooOO % ooO
if 14 - 14: Oo0ooO0oo0oO / O0oo0OO0 / i11iIiiIii - Oo0ooO0oo0oO / I1i1iI1i - ooO
if 81 - 81: i1 % ooo0Oo0 . Ii1Ii1iiii11
if 66 - 66: II * ooo0Oo0 / OoooooooOO * O0 % ooO
if 49 - 49: II111iiii . iii1I1I * O0 * ooo0Oo0 / o0000o0o0000o * OoooooooOO
if 82 - 82: O00oOoOoO0o0O / ooo0Oo0 / ooo0Oo0 % ooo0Oo0
if 20 - 20: Ii1Ii1iiii11
if 63 - 63: iIii1I11I1II1 . O0oo0OO0
if 100 - 100: i1IIi * i1IIi
if 26 - 26: ooO . O0oo0OO0 % Oo0ooO0oo0oO
if 94 - 94: OOooo0000ooo
if 15 - 15: ooo0Oo0 - OOooo0000ooo / O0
if 28 - 28: o0000o0o0000o . i1IIi / II
if 77 - 77: i11iIiiIii / o0000o0o0000o / i11iIiiIii % Oo0ooO0oo0oO - o0000o0o0000o
if 80 - 80: o0000o0o0000o % Oo0ooO0oo0oO . OoooooooOO . II111iiii % OOooo0000ooo
if 6 - 6: o0000o0o0000o % OOooo0000ooo / ooo0Oo0 + o0000o0o0000o . i11Ii11I1Ii1i
if 70 - 70: iIii1I11I1II1 / ooo0Oo0
if 61 - 61: O0 * I1i1iI1i + o0000o0o0000o - ooO . iii1I1I - OOooo0000ooo
if 7 - 7: II
if 81 - 81: O00oOoOoO0o0O % II111iiii % I1i1iI1i / OOoO
if 95 - 95: Oo0ooO0oo0oO - O0 % OoooooooOO
if 13 - 13: i11iIiiIii
if 54 - 54: ooO . II * OOoO % o0000o0o0000o . O0 * OOooo0000ooo
if 87 - 87: ooo0Oo0 % II * O00oOoOoO0o0O
if 59 - 59: O00oOoOoO0o0O / OOoO - iIii1I11I1II1 * iIii1I11I1II1
if 18 - 18: OOoO * II / i11iIiiIii / iIii1I11I1II1 * OoooooooOO . ooO
if 69 - 69: O00oOoOoO0o0O * Ii1Ii1iiii11
if 91 - 91: I1i1iI1i . Ii1Ii1iiii11 / O0oo0OO0 / i11iIiiIii * I1i1iI1i
if 52 - 52: iii1I1I - i11iIiiIii / OOooo0000ooo . i11Ii11I1Ii1i
if 38 - 38: i11Ii11I1Ii1i + OoooooooOO * Oo0ooO0oo0oO % i11Ii11I1Ii1i
if 91 - 91: i1IIi - II * iii1I1I
if 24 - 24: Oo0ooO0oo0oO * ooo0Oo0
if 17 - 17: O0oo0OO0 . iii1I1I * O0
if 81 - 81: ooO
if 58 - 58: II111iiii . o0000o0o0000o . ooo0Oo0 * OoooooooOO / ooo0Oo0 / OOoO
if 41 - 41: OOoO + O0oo0OO0 . i1
if 73 - 73: i11iIiiIii * iii1I1I + I1i1iI1i / i11Ii11I1Ii1i
if 56 - 56: i1IIi
if 11 - 11: i11iIiiIii % I1i1iI1i / OOoO * OoooooooOO
if 82 - 82: OOooo0000ooo
if 10 - 10: O00oOoOoO0o0O % ooO / OOoO * OOooo0000ooo - I1i1iI1i
if 54 - 54: i11iIiiIii / iIii1I11I1II1 % II / iii1I1I . iIii1I11I1II1 / i1
if 1 - 1: o0000o0o0000o / Oo0ooO0oo0oO * Oo0ooO0oo0oO - I1i1iI1i % ooo0Oo0
if 96 - 96: OOooo0000ooo / ooo0Oo0 % O0oo0OO0 . iIii1I11I1II1
if 30 - 30: OOoO - O0oo0OO0
if 15 - 15: OoooooooOO
if 31 - 31: II111iiii
if 62 - 62: iIii1I11I1II1 % o0000o0o0000o % II * OOooo0000ooo
if 87 - 87: OOooo0000ooo
if 45 - 45: i11Ii11I1Ii1i + II111iiii * O0 % ooO . iIii1I11I1II1
if 55 - 55: OOooo0000ooo
if 43 - 43: ooO
if 17 - 17: i11iIiiIii
if 94 - 94: OoooooooOO - OOooo0000ooo + i11Ii11I1Ii1i . OoooooooOO / i1IIi
if 53 - 53: o0000o0o0000o % II
if 17 - 17: OoooooooOO % ooo0Oo0 % O0
if 46 - 46: i1 + o0000o0o0000o % OoooooooOO * II
if 89 - 89: OOooo0000ooo - OOooo0000ooo % i1 / OOoO + i11Ii11I1Ii1i - OOooo0000ooo
if 97 - 97: ooo0Oo0 % Oo0ooO0oo0oO / II / iIii1I11I1II1 * OoooooooOO * ooO
if 80 - 80: i11Ii11I1Ii1i / O0
if 55 - 55: iii1I1I * OOoO / O0 % Oo0ooO0oo0oO
if 71 - 71: i11iIiiIii * Oo0ooO0oo0oO * ooO + i11Ii11I1Ii1i + O00oOoOoO0o0O
if 59 - 59: OOooo0000ooo
if 54 - 54: ooO
if 27 - 27: Oo0ooO0oo0oO - O0oo0OO0 + I1i1iI1i + Ii1Ii1iiii11 . O0oo0OO0
if 86 - 86: II111iiii - OoooooooOO - Ii1Ii1iiii11 % i1
if 16 - 16: Ii1Ii1iiii11 + O00oOoOoO0o0O + OoooooooOO
if 87 - 87: iii1I1I . i11Ii11I1Ii1i / OOooo0000ooo - OoooooooOO
if 33 - 33: i11Ii11I1Ii1i % O0oo0OO0 . iIii1I11I1II1 / OOooo0000ooo
if 3 - 3: ooo0Oo0 + O0oo0OO0
if 60 - 60: O0oo0OO0 . Oo0ooO0oo0oO - II - iii1I1I - II111iiii % O00oOoOoO0o0O
if 62 - 62: O0 + i1 - i1 % iIii1I11I1II1
if 47 - 47: o0000o0o0000o + iii1I1I
if 40 - 40: iIii1I11I1II1 % ooo0Oo0 + II111iiii - iii1I1I
if 80 - 80: i11Ii11I1Ii1i
if 81 - 81: OoooooooOO / Ii1Ii1iiii11 * iIii1I11I1II1 . O00oOoOoO0o0O + i11Ii11I1Ii1i / O0
if 84 - 84: II111iiii - I1i1iI1i
if 78 - 78: OOooo0000ooo
if 58 - 58: i11iIiiIii - Oo0ooO0oo0oO
if 67 - 67: II / i1 + iIii1I11I1II1 % iii1I1I
if 99 - 99: Ii1Ii1iiii11 . ooo0Oo0
if 92 - 92: i1IIi
if 68 - 68: O0oo0OO0 % OOooo0000ooo - i11Ii11I1Ii1i - Ii1Ii1iiii11 . O00oOoOoO0o0O
if 30 - 30: OoooooooOO % I1i1iI1i + Ii1Ii1iiii11 * O0oo0OO0
if 57 - 57: OOoO + iIii1I11I1II1 . O0oo0OO0 + i11Ii11I1Ii1i
if 4 - 4: ooo0Oo0
if 43 - 43: i1IIi . iii1I1I * iIii1I11I1II1 * i11iIiiIii - ooO + Ii1Ii1iiii11
if 56 - 56: O00oOoOoO0o0O % i11iIiiIii / ooo0Oo0 . o0000o0o0000o . O0oo0OO0 - Oo0ooO0oo0oO
if 32 - 32: o0000o0o0000o / i11Ii11I1Ii1i / iii1I1I
if 22 - 22: O0oo0OO0 - Oo0ooO0oo0oO . O00oOoOoO0o0O + I1i1iI1i
if 69 - 69: i11Ii11I1Ii1i - iii1I1I
if 10 - 10: i1IIi / i1 . II111iiii * i1IIi % OoooooooOO
if 83 - 83: OOoO . ooO + o0000o0o0000o * OOoO . o0000o0o0000o + i11Ii11I1Ii1i
if 64 - 64: ooo0Oo0 . I1i1iI1i - i1IIi
if 35 - 35: II % OoooooooOO
if 59 - 59: iii1I1I % OOoO
if 32 - 32: iii1I1I * O0 + O0
if 34 - 34: OOooo0000ooo
if 5 - 5: O0oo0OO0 . iii1I1I
if 48 - 48: O00oOoOoO0o0O - O0oo0OO0 . OOoO - iIii1I11I1II1 % ooo0Oo0
if 47 - 47: i1 / OoooooooOO - II111iiii
if 91 - 91: Oo0ooO0oo0oO + I1i1iI1i
if 23 - 23: i1IIi
if 9 - 9: i1IIi % o0000o0o0000o - O0oo0OO0 * Oo0ooO0oo0oO . I1i1iI1i
if 18 - 18: ooo0Oo0 . Oo0ooO0oo0oO + i1 . iii1I1I + OoooooooOO . O0oo0OO0
if 31 - 31: o0000o0o0000o - OOoO
if 49 - 49: iIii1I11I1II1 - iIii1I11I1II1 - Oo0ooO0oo0oO + OOooo0000ooo / Oo0ooO0oo0oO
if 74 - 74: OoooooooOO + II % O0
if 32 - 32: II + II
if 89 - 89: Ii1Ii1iiii11 + i11Ii11I1Ii1i + ooo0Oo0 - ooO
if 12 - 12: Oo0ooO0oo0oO - I1i1iI1i - o0000o0o0000o / OOoO
if 17 - 17: O0oo0OO0 - o0000o0o0000o - II111iiii / o0000o0o0000o / ooo0Oo0
if 30 - 30: ooO * II % II + i1 * OOooo0000ooo
if 33 - 33: I1i1iI1i + OOoO * O0 * O0oo0OO0 . II
if 74 - 74: i1 * i1 * I1i1iI1i / i11Ii11I1Ii1i
if 91 - 91: i11iIiiIii . II / II111iiii
if 97 - 97: ooo0Oo0 % i1IIi % OOooo0000ooo + O00oOoOoO0o0O - O0 - OOoO
if 64 - 64: ooo0Oo0 - i1
if 12 - 12: i1IIi
if 99 - 99: II111iiii - II * OOooo0000ooo
if 3 - 3: OOooo0000ooo - II * i1 * II + O00oOoOoO0o0O
if 15 - 15: II * ooo0Oo0 / i1 . I1i1iI1i / ooo0Oo0 % Oo0ooO0oo0oO
if 75 - 75: OoooooooOO % i11iIiiIii % iIii1I11I1II1 % II / i11iIiiIii
if 96 - 96: Ii1Ii1iiii11 * i11Ii11I1Ii1i / iIii1I11I1II1 / OOoO
if 5 - 5: I1i1iI1i
if 83 - 83: OOoO * iii1I1I . II111iiii * i1IIi % O0
if 35 - 35: Oo0ooO0oo0oO % O0oo0OO0 + O0 * I1i1iI1i % II
if 57 - 57: i11Ii11I1Ii1i / OOoO
if 63 - 63: Ii1Ii1iiii11 * O0oo0OO0 * Ii1Ii1iiii11 + Oo0ooO0oo0oO
if 25 - 25: i1 * Oo0ooO0oo0oO / iii1I1I / OOooo0000ooo
if 11 - 11: ooO + i11iIiiIii
if 14 - 14: Oo0ooO0oo0oO / OOooo0000ooo + O0oo0OO0 - ooo0Oo0
if 38 - 38: o0000o0o0000o
if 30 - 30: II111iiii + OOoO . i11iIiiIii + iIii1I11I1II1
if 100 - 100: i11Ii11I1Ii1i * I1i1iI1i / i1
if 92 - 92: Ii1Ii1iiii11 / i11iIiiIii * ooO
if 55 - 55: Ii1Ii1iiii11
if 1 - 1: O0oo0OO0
if 43 - 43: iIii1I11I1II1 - ooO - I1i1iI1i + II - o0000o0o0000o % II
if 58 - 58: Oo0ooO0oo0oO
if 27 - 27: OOooo0000ooo * ooO - OoooooooOO . ooo0Oo0 - II111iiii
if 62 - 62: iii1I1I / iIii1I11I1II1 * OOoO
if 84 - 84: OOooo0000ooo - Oo0ooO0oo0oO . OOooo0000ooo + Ii1Ii1iiii11 . i1
if 96 - 96: ooo0Oo0 % i1 * ooo0Oo0 % iii1I1I . I1i1iI1i / I1i1iI1i
if 7 - 7: O0oo0OO0 - Ii1Ii1iiii11 % i1IIi
if 24 - 24: O0oo0OO0 % O0 % OOoO
if 61 - 61: Ii1Ii1iiii11 . i1 / Ii1Ii1iiii11 * OoooooooOO
if 13 - 13: II111iiii
if 17 - 17: II111iiii
if 66 - 66: OOooo0000ooo * i11Ii11I1Ii1i
if 73 - 73: i11iIiiIii + O0 % O0
if 70 - 70: II111iiii * OoooooooOO - ooo0Oo0 + i11Ii11I1Ii1i * O0
if 49 - 49: i11Ii11I1Ii1i . ooo0Oo0 . Oo0ooO0oo0oO - II
if 74 - 74: Ii1Ii1iiii11 % II * i1IIi
if 18 - 18: Oo0ooO0oo0oO
if 30 - 30: II111iiii
if 27 - 27: i1IIi - iIii1I11I1II1 + O0 % O00oOoOoO0o0O / ooO + i1IIi
if 48 - 48: O00oOoOoO0o0O
if 70 - 70: OoooooooOO * i11iIiiIii
if 60 - 60: OOooo0000ooo / iIii1I11I1II1 + OoooooooOO - II * i11iIiiIii
if 47 - 47: O0 . iii1I1I / Ii1Ii1iiii11 % i11iIiiIii
if 47 - 47: ooo0Oo0 . Oo0ooO0oo0oO . iIii1I11I1II1 . I1i1iI1i
if 39 - 39: I1i1iI1i
if 89 - 89: OoooooooOO + i1 . o0000o0o0000o / ooo0Oo0
if 75 - 75: iIii1I11I1II1 * i1 / Oo0ooO0oo0oO * II111iiii . i1IIi
if 6 - 6: ooo0Oo0 % ooo0Oo0 / OoooooooOO * i11Ii11I1Ii1i . iii1I1I . i1IIi
if 59 - 59: OOoO . OOoO * iii1I1I - ooo0Oo0 % Oo0ooO0oo0oO
if 19 - 19: OoooooooOO / O00oOoOoO0o0O - o0000o0o0000o . Oo0ooO0oo0oO
if 8 - 8: OOoO % Ii1Ii1iiii11 . iIii1I11I1II1
if 95 - 95: I1i1iI1i + i11iIiiIii . II . Ii1Ii1iiii11 . I1i1iI1i
if 93 - 93: i1
if 55 - 55: II111iiii % I1i1iI1i - O0oo0OO0
if 48 - 48: Ii1Ii1iiii11 * iIii1I11I1II1 % Oo0ooO0oo0oO
if 100 - 100: II111iiii - i11iIiiIii + O0oo0OO0 % Ii1Ii1iiii11 - iIii1I11I1II1 * i11iIiiIii
if 30 - 30: O0oo0OO0 . O0oo0OO0 . ooo0Oo0 % ooo0Oo0 * i1IIi * i11Ii11I1Ii1i
if 74 - 74: OoooooooOO
if 33 - 33: I1i1iI1i - II111iiii
if 95 - 95: OoooooooOO
if 23 - 23: II111iiii + OOoO / O0 . OOoO . o0000o0o0000o + iIii1I11I1II1
if 2 - 2: i1IIi . O0 / I1i1iI1i . II111iiii / O0oo0OO0 % i1IIi
if 12 - 12: I1i1iI1i
if 58 - 58: iIii1I11I1II1 * ooo0Oo0 . Ii1Ii1iiii11 . O00oOoOoO0o0O * ooo0Oo0
if 63 - 63: Oo0ooO0oo0oO . OOoO * I1i1iI1i - OOoO % OOoO
if 62 - 62: OOoO - Ii1Ii1iiii11 / Ii1Ii1iiii11
if 95 - 95: Oo0ooO0oo0oO - i1IIi / o0000o0o0000o . Ii1Ii1iiii11 % ooO - i1IIi
if 12 - 12: i1
if 96 - 96: O0
if 89 - 89: II - O00oOoOoO0o0O
if 26 - 26: Ii1Ii1iiii11 % Ii1Ii1iiii11 / II111iiii / i1
if 2 - 2: i1IIi / i11iIiiIii + iii1I1I
if 95 - 95: II / OOooo0000ooo % iIii1I11I1II1 + O0
if 6 - 6: OOooo0000ooo
if 73 - 73: I1i1iI1i % I1i1iI1i . ooO * II - ooo0Oo0
if 97 - 97: OOooo0000ooo
if 15 - 15: O0 - iii1I1I / i1IIi . o0000o0o0000o
if 64 - 64: Ii1Ii1iiii11 / i1IIi
if 100 - 100: II111iiii
if 16 - 16: ooo0Oo0
if 96 - 96: I1i1iI1i / o0000o0o0000o % ooo0Oo0 - Ii1Ii1iiii11
if 35 - 35: ooO
if 90 - 90: i11iIiiIii
if 47 - 47: O0oo0OO0 . i11iIiiIii
if 9 - 9: Oo0ooO0oo0oO - OOoO . OoooooooOO % Ii1Ii1iiii11
if 13 - 13: O0oo0OO0 * iIii1I11I1II1 + II111iiii - O00oOoOoO0o0O - Oo0ooO0oo0oO
if 43 - 43: i1 / o0000o0o0000o * iii1I1I % Ii1Ii1iiii11 % iii1I1I
if 18 - 18: O0oo0OO0
if 99 - 99: i1 / i11Ii11I1Ii1i . i11iIiiIii / OOoO + i1IIi - OOoO
if 50 - 50: i1IIi
if 56 - 56: O0oo0OO0 + o0000o0o0000o / ooo0Oo0
if 75 - 75: Oo0ooO0oo0oO
if 96 - 96: I1i1iI1i * OOoO * O00oOoOoO0o0O
if 36 - 36: OoooooooOO + Ii1Ii1iiii11 . i11Ii11I1Ii1i * Ii1Ii1iiii11 + OOooo0000ooo
if 45 - 45: i11Ii11I1Ii1i / i1 + II - O00oOoOoO0o0O - Ii1Ii1iiii11 . iIii1I11I1II1
if 52 - 52: iii1I1I + i1IIi . i1 * iii1I1I
if 31 - 31: O00oOoOoO0o0O % iIii1I11I1II1 . O0
if 80 - 80: OOoO / O00oOoOoO0o0O + II
if 18 - 18: II111iiii - i1 / iIii1I11I1II1 % Oo0ooO0oo0oO % II / I1i1iI1i
if 47 - 47: ooO
if 24 - 24: ooo0Oo0 % I1i1iI1i
if 87 - 87: I1i1iI1i % i1 / Ii1Ii1iiii11 - OOooo0000ooo + i11iIiiIii
if 85 - 85: OoooooooOO * OOooo0000ooo . ooO / i1 / OoooooooOO
if 87 - 87: O0oo0OO0
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3