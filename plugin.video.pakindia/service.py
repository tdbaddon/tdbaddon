import urllib2 , xbmc , xbmcaddon , os , re
if 64 - 64: i11iIiiIii
OO0o = 'plugin.video.pakindia'
Oo0Ooo = xbmcaddon . Addon ( id = OO0o )
O0O0OO0O0O0 = xbmc . translatePath ( Oo0Ooo . getAddonInfo ( 'profile' ) )
iiiii = os . path . join ( O0O0OO0O0O0 , "world" )
ooo0OO = os . path . join ( O0O0OO0O0O0 , "pak" )
if os . path . exists ( O0O0OO0O0O0 ) == False :
 os . makedirs ( O0O0OO0O0O0 )
 if 18 - 18: II111iiii . OOO0O / II1Ii / oo * OoO0O00
 if 2 - 2: ooOO00oOo % oOo0O0Ooo * Ooo00oOo00o . oOoO0oo0OOOo + iiiiIi11i
 if 24 - 24: II11iiII / OoOO0ooOOoo0O + o0000oOoOoO0o * i1I1ii1II1iII % oooO0oo0oOOOO
O0oO = ''
def o0oO0 ( i , t1 , t2 = [ ] ) :
 oo00 = O0oO
 for o00 in t1 :
  oo00 += chr ( o00 )
  i += 1
  if i > 1 :
   oo00 = oo00 [ : - 1 ]
   i = 0
 for o00 in t2 :
  oo00 += chr ( o00 )
  i += 1
  if i > 1 :
   oo00 = oo00 [ : - 1 ]
   i = 0
 return oo00
 if 62 - 62: II1ii - o0oOoO00o . iIi1IIii11I + oo0 * o0oOoO00o % o0oOoO00o
 if 22 - 22: oooO0oo0oOOOO . o0oOoO00o
I11 = o0oO0 ( 0 , [ 104 , 162 , 116 , 157 , 116 , 89 , 112 , 151 , 58 , 134 , 47 ] , [ 48 , 47 , 137 , 97 , 28 , 100 , 50 , 115 , 144 , 116 , 212 , 114 , 101 , 101 , 33 , 97 , 249 , 109 , 115 , 115 , 195 , 46 , 132 , 100 , 147 , 121 , 215 , 110 , 42 , 110 , 242 , 115 , 98 , 46 , 9 , 99 , 251 , 111 , 53 , 109 , 146 , 47 , 128 , 97 , 117 , 112 , 238 , 112 , 12 , 115 , 197 , 47 , 108 , 115 , 113 , 101 , 20 , 114 , 176 , 118 , 168 , 105 , 155 , 99 , 65 , 101 , 61 , 95 , 188 , 102 , 174 , 105 , 226 , 108 , 78 , 101 , 71 , 115 , 129 , 47 ] )
if 98 - 98: i11iIiiIii * ooOO00oOo % II1ii * II1ii * OoO0O00
try :
        DATA_URL='https://app.dynns.com/keys/pakindiahdlitenewf.php'
        request = urllib2.Request(DATA_URL)
        base64string = 'YW11OkBkbkBuODQ5'
        request.add_header("User-Agent","Pak%20TV/1.0 CFNetwork/758.2.8 Darwin/15.0.0") 
        request.add_header("Authorization", "Basic %s" % base64string)   
        Oo0Ooo.setSetting('pakuser',urllib2.urlopen(request).read())
except:pass

try :
 import base64
 import time
 TIME = time.time()
 second= str(TIME).split('.')[0]
 first =int(second)+69296929
 token=base64.b64encode('%s@2nd2@%s' % (str(first),second))
 devnum=Oo0Ooo.getSetting('pakuser')[-3:]
 DATA_URL='https://app.dynns.com/app_panelnew/output.php/playlist?type=xml&deviceSn=%s&token=%s'  %(devnum,token)
 request = urllib2.Request(DATA_URL)
 base64string = 'YWRtaW46QWxsYWgxQA=='
 request.add_header("User-Agent",Oo0Ooo.getSetting('pakuser'))
 #request.add_header("allsite_lang","NL")
 request.add_header("Authorization", "Basic %s" % base64string)
 i1iIIII = urllib2.urlopen(request).read()
 match=re.compile('<programURL>(.+?)</programURL>').findall(i1iIIII)[0]
 if match:

     I1 = open ( ooo0OO , mode = 'w' )
     I1 . write ( i1iIIII )
except : pass
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3
