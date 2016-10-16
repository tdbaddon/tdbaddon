import urllib2,xbmc,xbmcaddon,os,re

PLUGIN='plugin.video.pakindia'
ADDON = xbmcaddon.Addon(id=PLUGIN)
datapath = xbmc.translatePath(ADDON.getAddonInfo('profile'))
paki=os.path.join(datapath, "pak")

if os.path.exists(datapath) == False:
        os.makedirs(datapath)


            
def random_generator(size=32):
      import random,string
      chars=string.ascii_lowercase + string.digits
      return ''.join(random.choice(chars) for x in range(size))

KEY= random_generator().upper()
ADDON.setSetting('pak_key',KEY)

try :
        DATA_URL='https://app.dynns.com/keys/litefree.php'
        request = urllib2.Request(DATA_URL)
        base64string = 'YW11OkBkbkBuODQ5'
        request.add_header("User-Agent",KEY) 
        request.add_header("Authorization", "Basic %s" % base64string)   
        ADDON.setSetting('pakuser',urllib2.urlopen(request).read())
except:pass

try :
 import base64
 import time
 TIME = time.time()
 second= str(TIME).split('.')[0]
 first =int(second)+69296929
 token=base64.b64encode('%s@2nd2@%s' % (str(first),second))
 devnum=ADDON.getSetting('pakuser')[-3:]
 DATA_URL='https://app.dynns.com/app_panelnew/output.php/playlist?type=xml&deviceSn=%s&token=%s'  %(devnum,token)
 request = urllib2.Request(DATA_URL)
 base64string = 'YWRtaW46QWxsYWgxQA=='
 request.add_header("User-Agent",KEY) 
 request.add_header("Authorization", "Basic %s" % base64string)   
 i1iIIII = urllib2.urlopen(request).read()
 match=re.compile('<programURL>(.+?)</programURL>').findall(i1iIIII)[0]

 if match: 
         I1 = open ( paki , mode = 'w' )
         I1 . write ( i1iIIII )
except : pass



def ip():
    request = urllib2.Request('https://app.dynns.com/keys/ip_check.php')	
    request.add_header("Host",'app.dynns.com')
    request.add_header("User-Agent",'Pak%20TV/1.0 CFNetwork/758.5.3 Darwin/15.6.0')
    link = urllib2.urlopen(request).read()
    match=link.split(': ')[1]
    return match

                     
def TEMPLATE():
        SM_TEMPLATE='''<SOAP-ENV:Envelope SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:tns="http://scriptbaker.com/saveDeviceIdService">
            <SOAP-ENV:Body>
            <tns:db.saveId xmlns:tns="http://app.dynns.com/saveDeviceIdService">
            <id xsi:type="xsd:string">%s chulbulpanday</id>
            <name xsi:type="xsd:string">%s</name>
            </tns:db.saveId>
            </SOAP-ENV:Body>
            </SOAP-ENV:Envelope>'''
        
        
        return SM_TEMPLATE%(ip(),KEY)
    
try:
    SM_TEMPLATE=TEMPLATE()
except:pass

try:
    
    http_headers = {"Host": "app.dynns.com",
                    "Content-Type": "text/xml; charset=ISO-8859-1",
                    "Connection": "keep-alive",
                    "SOAPAction": "http://app.dynns.com/saveDeviceIdService/tns:db.saveId",
                    "Proxy-Connection": "keep-alive",
                    "Accept": "*/*",
                    "User-Agent": KEY,
                    "Content-Length":  str(len(SM_TEMPLATE)),
                    "Accept-Language": "en-gb",
                    "Accept-Encoding": "gzip, deflate"}
                         
    request_object = urllib2.Request('https://app.dynns.com/apisoap/index.php', SM_TEMPLATE, http_headers)
    response = urllib2.urlopen(request_object)
    html_string = response.read()
    xbmc.log(html_string)
except:pass
