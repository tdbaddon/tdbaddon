import xbmc, xbmcgui, xbmcplugin
import urllib2,urllib,cgi, re, urlresolver  
import urlparse
import HTMLParser
import xbmcaddon
from operator import itemgetter
import traceback,cookielib
import base64,os,  binascii
import CustomPlayer,uuid
from time import time
import base64,sys
try:
    import json
except:
    import simplejson as json

__addon__       = xbmcaddon.Addon()
__addonname__   = __addon__.getAddonInfo('name')
__icon__        = __addon__.getAddonInfo('icon')
addon_id = 'plugin.video.ZemTV-shani'
selfAddon = xbmcaddon.Addon(id=addon_id)
profile_path =  xbmc.translatePath(selfAddon.getAddonInfo('profile'))
S365COOKIEFILE='s365CookieFile.lwp'
S365COOKIEFILE=os.path.join(profile_path, S365COOKIEFILE)



def tr(param1 , param2 , param3):
    _loc4_ = 0;
    _loc5_= "";
    _loc6_ = None
    if( ord(param1[- 2]) == param2 and ord(param1[2]) == param3):
        _loc5_ = "";
        _loc4_ = len(param1)- 1;
        while(_loc4_ >= 0):
            _loc5_ = _loc5_ + param1[_loc4_]
            _loc4_-=1;
        param1 = _loc5_;
        _loc6_ = int(param1[-2:]);
        print 'xx',_loc6_
        param1 = param1[2:];
        param1 = param1[0:-3];
        _loc6_ = _loc6_ / 2;
        if(_loc6_ < len(param1)):
            _loc4_ = _loc6_;
        while(_loc4_ < len(param1)):
            param1 = param1[0:_loc4_]+ param1[_loc4_ + 1:]
            _loc4_ = _loc4_ + _loc6_ * 1;

        param1 = param1 + "!";

    return param1;

def swapme(st, fromstr , tostr):
    st=st.replace(tostr,"___") 
    st=st.replace(fromstr,tostr)
    st=st.replace("___", fromstr)
    return st

     
def decode(encstring):
    encstring=tr(encstring ,114,65)
    mc_from="0BwtxmczunMQR6vVlND3LXa4oA"
    mc_to="p9U1bsyZIHf8YWg5GiJ2Tekd7="
    if 1==2:#encstring.endswith("!"):
        encstring=encstring[:-1]
        mc_from="ngU08IuldVHosTmZz9kYL2bayE"
        mc_to="v7ec41D6GpBtXx3QJRiN5WwMf="

    st=encstring
    for i in range(0,len(mc_from)):
        st=swapme(st, mc_from[i], mc_to[i])
    print st
    return st.decode("base64")
    
def getUrl(mainurl, cookieJar=None,post=None, timeout=20, headers=None, useproxy=True):
    url=mainurl
    cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
    opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
    #opener = urllib2.install_opener(opener)
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
    if headers:
        for h,hv in headers:
            req.add_header(h,hv)
    
    if '|' in url:
        url,header_in_page=url.split('|')
        header_in_page=header_in_page.split('&')
        
        for h in header_in_page:
            
            n,v=h.split('=')
            req.add_header(h,v)
    link=""
    try:
        response = opener.open(req,post,timeout=timeout)
        link=response.read()
        response.close()
    except: pass
    if link=="" and useproxy: 
        return getUrlWithWebProxy(mainurl,cookieJar,post,timeout,headers)
    return link;

    #function arcfour(k,d) {var o='';s=new Array();var n=256;l=k.length;for(var i=0;i<n;i++){s[i]=i;}for(var j=i=0;i<n;i++){j=(j+s[i]+k.charCodeAt(i%l))%n;var x=s[i];s[i]=s[j];s[j]=x;}for(var i=j=y=0;y<d.length;y++){i=(i+1)%n;j=(j+s[i])%n;x=s[i];s[i]=s[j];s[j]=x;o+=String.fromCharCode(d.charCodeAt(y)^s[(s[i]+s[j])%n]);}return o;}
def  arcfour(k,d):
    o='';    
    n=256;
    l=len(k);
    s=range(0,n)    
    i=0
    j=0
    for i in range(0,n):      
       
        j=(j+s[i]+ord(k[i%l]))%n;

        x=s[i];
        s[i]=s[j];
        s[j]=x;
        #if (i==0): print s
    i=0
    j=0    
    for y in range(0,len(d)):#(var i=j=y=0;y<d.length;y++)
        i=(i+1)%n;
        j=(j+s[i])%n;
        x=s[i];
        s[i]=s[j];
        s[j]=x;
        o+=chr(ord(d[y])^s[(s[i]+s[j])%n]);

    return o;

        
def getUrlWithWebProxy(url, cookieJar=None,post=None, timeout=20, headers=None):


    import urllib,re
    #print 'webproxyurl before',url
    if cookieJar==None:
        cookieJar=cookielib.LWPCookieJar()
    te=getUrl('http://proxy.marbenak.com/',cookieJar=cookieJar,useproxy=False)
    c=re.findall('\{u\:\'(.*?)\'',te)[0]
    ss= arcfour(c,url[4:])
    bb='21'#re.findall('\},b:\'(.*?)\'',te)[0]
    referer='norefer'
    if headers:
        for h,hv in headers:
            if h=='Referer':
                referer=hv
    
    rs=getUrl('http://proxy.marbenak.com/browse.php?u=%s&b=%s&f=%s'%(urllib.quote_plus(ss.encode('base64')),bb,referer),cookieJar=cookieJar, headers=headers ,useproxy=False)

    rr='[\'"]\/browse.php\?u\=(.*?)["\']'
    ec=re.findall(rr,rs)
    c=re.findall('\{u\:\'(.*?)\'',rs)[0]

    for enc in ec:
        
        try:
            dtext=arcfour(c,urllib.unquote(enc.split('&amp;')[0]).decode("base64"))
            #print enc
            #print dtext
            rs=rs.replace('/browse.php?u='+enc,'http'+dtext)
            
            
        except: pass
    #print 'webproxyurl',url,rs
    return rs

    

def setProxy():
    #proxyhtml=getUrl('http://gatherproxy.com/proxylist/country/?c=Australia')
    selfAddon.setSetting( id="sport365proxyserver" ,value="185.72.246.41")    
    selfAddon.setSetting( id="sport365proxyport" ,value="3128")    
    return True
    
    
def proxyserverAndPort():
    return selfAddon.getSetting(id="sport365proxyserver"),selfAddon.getSetting(id="sport365proxyport")    
    
    
def getUrlWithProxy(url, cookieJar=None,post=None, timeout=20, headers=None):
#    from socksipyhandler import SocksiPyHandler
    proxyserver,proxyport=proxyserverAndPort()
    print 'in proxy',proxyserver,proxyport,url
    
    cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)    
    opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler(),urllib2.ProxyHandler({ 'http'  : '%s:%s'%(proxyserver,proxyport)}))    
    
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
    if headers:
        for h,hv in headers:
            req.add_header(h,hv)

    response = opener.open(req,post,timeout=timeout)
    link=response.read()
    response.close()
    return link;

    
def unwise_func( w, i, s, e):
    lIll = 0;
    ll1I = 0;
    Il1l = 0;
    ll1l = [];
    l1lI = [];
    while True:
        if (lIll < 5):
            l1lI.append(w[lIll])
        elif (lIll < len(w)):
            ll1l.append(w[lIll]);
        lIll+=1;
        if (ll1I < 5):
            l1lI.append(i[ll1I])
        elif (ll1I < len(i)):
            ll1l.append(i[ll1I])
        ll1I+=1;
        if (Il1l < 5):
            l1lI.append(s[Il1l])
        elif (Il1l < len(s)):
            ll1l.append(s[Il1l]);
        Il1l+=1;
        if (len(w) + len(i) + len(s) + len(e) == len(ll1l) + len(l1lI) + len(e)):
            break;

    lI1l = ''.join(ll1l)#.join('');
    I1lI = ''.join(l1lI)#.join('');
    ll1I = 0;
    l1ll = [];
    for lIll in range(0,len(ll1l),2):
        #print 'array i',lIll,len(ll1l)
        ll11 = -1;
        if ( ord(I1lI[ll1I]) % 2):
            ll11 = 1;
        #print 'val is ', lI1l[lIll: lIll+2]
        l1ll.append(chr(    int(lI1l[lIll: lIll+2], 36) - ll11));
        ll1I+=1;
        if (ll1I >= len(l1lI)):
            ll1I = 0;
    ret=''.join(l1ll)
    if 'eval(function(w,i,s,e)' in ret:
#        print 'STILL GOing'
        ret=re.compile('eval\(function\(w,i,s,e\).*}\((.*?)\)').findall(ret)[0]
        return get_unwise(ret)
    else:
#        print 'FINISHED'
        return ret
def get_unwise( str_eval):
    page_value=""
    try:
        ss="w,i,s,e=("+str_eval+')'
        exec (ss)
        page_value=unwise_func(w,i,s,e)
    except: traceback.print_exc(file=sys.stdout)
    #print 'unpacked',page_value
    return page_value  
def get365CookieJar(updatedUName=False):
    cookieJar=None
    try:
        cookieJar = cookielib.LWPCookieJar()
        if not updatedUName:
            cookieJar.load(S365COOKIEFILE,ignore_discard=True)
    except: 
        cookieJar=None

    if not cookieJar:
        cookieJar = cookielib.LWPCookieJar()
    return cookieJar    
def get365Key(cookieJar,url=None, useproxy=True):
    headers=[('User-Agent','AppleCoreMedia/1.0.0.13A452 (iPhone; U; CPU OS 9_0_2 like Mac OS X; en_gb)')]
    import time
    if not url:
        mainhtml=getUrl("http://www.sport365.live/en/main",headers=headers, cookieJar=cookieJar)
        #print 'mainhtml',mainhtml
        try:
            kurl=re.findall("src=\"(http.*?/wrapper.js.*?)\"",mainhtml)[0]
        except:
            kurl='http://s1.medianetworkinternational.com/js/wrapper.js?'+str(int(time.time()))
    else:
        kurl=url
    
    khtml=getUrl(kurl,headers=headers, cookieJar=cookieJar)
    if khtml=="": 
        if setProxy():
            kkey=getUrl(kurl,headers=headers, cookieJar=cookieJar)        
    kstr=re.compile('eval\(function\(w,i,s,e\).*}\((.*?)\)').findall(khtml)[0]
    kunc=get_unwise(kstr)
    #print kunc    
    
    kkey=re.findall('aes_key="(.*?)"',kunc)
    kkey=re.findall('aes\(\)\{return "(.*?)"',kunc)
    return kkey[0]
def Colored(text = '', colorid = '', isBold = False):
    if colorid == 'ZM':
        color = 'FF11b500'
    elif colorid == 'EB':
        color = 'FFe37101'
    elif colorid == 'bold':
        return '[B]' + text + '[/B]'
    else:
        color = colorid
        
    if isBold == True:
        text = '[B]' + text + '[/B]'
    return '[COLOR ' + color + ']' + text + '[/COLOR]'	

def getLinks():
    cookieJar=get365CookieJar()
    kkey=get365Key(cookieJar,useproxy=False)
        
    headers=[('User-Agent','AppleCoreMedia/1.0.0.13A452 (iPhone; U; CPU OS 9_0_2 like Mac OS X; en_gb)')]

    liveurl="http://www.sport365.live/en/events/-/1/-/-"+'/'+str(getutfoffset())
    linkshtml=getUrl(liveurl,headers=headers, cookieJar=cookieJar)
    reg="images\/types.*?(green|red).*?px;\">(.*?)<\/td><td style=\"borde.*?>(.*?)<\/td><td.*?>(.*?)<\/td.*?__showLinks.*?,.?\"(.*?)\".*?\">(.*?)<"
    sportslinks=re.findall(reg,linkshtml)
    print 'got links',sportslinks
    progress = xbmcgui.DialogProgress()
    progress.create('Progress', 'Fetching Live Links')
    #print sportslinks
    c=0
    cookieJar.save (S365COOKIEFILE,ignore_discard=True)

    import HTMLParser
    h = HTMLParser.HTMLParser()
    ret=[]
    import jscrypto
    for tp,tm,nm,lng,lnk,cat in sportslinks:
        c+=1
        cat=cat.split("/")[0]
        progress.update( (c*100/len(sportslinks)), "", "fetting links for "+nm, "" )
        try:    
            lnk=json.loads(lnk.decode("base64"))
            lnk=jscrypto.decode(lnk["ct"],kkey,lnk["s"].decode("hex"))
            #print lnk
            lnk=lnk.replace('\\/','/').replace('"',"")
         
            qty=""
            cat=cat.replace('&nbsp;','')
            lng=lng.replace('&nbsp;','')
            mm=nm.replace('&nbsp;','')
            #print nm,tp
            if 'span' in lng:
                lng=lng.split('>')
                qty=lng[-2].split('<')[0]
                lng= lng[-1]
            if len(lng)>0:
                lng=Colored("[" +lng+"]","orange")
            if len(qty)>0:
                qty=Colored("["+qty+"]","red")
                
            
            if not lnk.startswith("http"):
                lnk='http://www.sport365.live'+lnk
            #print lnk
            if tp=="green":
                lnk=base64.b64encode("Sports365:"+base64.b64encode(lnk))
                #addDir(Colored(cat.capitalize()+": "+tm+" : "+ qty+lng+nm  ,'ZM') ,lnk,11 ,"",isItFolder=False)
                ret+=[(cat.capitalize()+": "+tm+" : "+ qty+lng+nm ,lnk,True)]
            else:
                ret+=[(cat.capitalize()+": "+tm+" : "+ qty+lng+nm ,lnk,False)]
        except: traceback.print_exc(file=sys.stdout)
        progress.close()
    return ret
def total_seconds(dt):
    # Keep backward compatibility with Python 2.6 which doesn't have
    # this method
    import datetime
    if hasattr(datetime, 'total_seconds'):
        return dt.total_seconds()
    else:
        return (dt.microseconds + (dt.seconds + dt.days * 24 * 3600) * 10**6) / 10**6
        
def getutfoffset():
    import time
    from datetime import datetime

    ts = time.time()
    utc_offset = total_seconds((   datetime.fromtimestamp(ts)-datetime.utcfromtimestamp(ts)))/60
              
    return int(utc_offset)
    
def selectMatch(url):
    #return "http://012-180.sport365.tech:43911/ls/38e59757cc13f10968253344378a8d6637aa391672a53601f03aab5f496959a5/1471368842/57b2c8434797a306029265/57b34f33eccd9/index.m3u8|Referer=%s&User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36&X-Requested-With=ShockwaveFlash/22.0.0.209&Cookie=%s"%("http://h5.adshell.net/flash","PHPSESSID=n2v7leegtqd2ljdksn2k0p8ql6")

    url=select365(url)
    if url=="": return 
    import HTMLParser
    h = HTMLParser.HTMLParser()

    #urlToPlay=base64.b64decode(url)
    cookieJar=get365CookieJar()
    html=getUrl(url,headers=[('Referer','http://www.sport365.live/en/main')],cookieJar=cookieJar)
    #print html
    reg="iframe frameborder=0.*?src=\"(.*?)\""
    linkurl=re.findall(reg,html)
    #print 'linkurl',linkurl
    if len(linkurl)==0:
        reg="http://www.sport365.live.*?'\/(.*?)'\)"
        linkurl=re.findall(reg,html)[0]
        linkurl="http://www.sport365.live/en/player/f/"+linkurl
        html=getUrl(h.unescape(linkurl),cookieJar=cookieJar)
        reg="iframe frameborder=0.*?src=\"(.*?)\""
        linkurl=re.findall(reg,html)[0]
#        print linkurl
    else:
        linkurl=linkurl[0]
    uurl=h.unescape(linkurl)
    print 'uurl',uurl
    if not uurl.startswith('http'):
        import urlparse
        uurl=urlparse.urljoin('http://www.fastflash.pw/', uurl)
        print 'newurl',uurl
    enclinkhtml=getUrl(uurl,cookieJar=cookieJar)
    reg='player_div", "st".*?file":"(.*?)"'
    enclink=re.findall(reg,enclinkhtml)
    usediv=False
    
    if len(enclink)==0:
        reg='name="f" value="(.*?)"'
        enclink=re.findall(reg,enclinkhtml)[0]  
        reg='name="s" value="(.*?)"'
        encst=re.findall(reg,enclinkhtml)[0]
        reg="\('action', ['\"](.*?)['\"]"
        postpage=re.findall(reg,enclinkhtml)
        if len(postpage)>0:
            
            reg='player_div", "st".*?file":"(.*?)"'
            post={'p':'http://cdn.adshell.net/swf/player.swf','s':encst,'f':enclink}
            post = urllib.urlencode(post)
            enclinkhtml2= getUrl(postpage[0],post=post, headers=[('Referer',linkurl),('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36')])
            #enclink=re.findall(reg,enclinkhtml2)
            if 'player_div' in enclinkhtml2>0:
                usediv=True
                #enclinkhtml=enclinkhtml2
                #print 'usediv',usediv
                reg="player_div\",.?\"(.*?)\",.?\"(.*?)\",(.*?)\)"
                encst,enclink,isenc=re.findall(reg,enclinkhtml2)[0]
                #print 'encst,enclink',encst,enclink,isenc
                isenc=isenc.strip();
                if isenc=="1":
                    reg="src=\"(.*?\\/wrapper.js.*)\""
                    wrapurl=re.findall(reg,enclinkhtml2)[0]
                    kkey=get365Key(cookieJar,url=wrapurl)
                    #print 'kkey',kkey
                    enclink=json.loads(enclink.decode("base64"))
                    import jscrypto
                    lnk=jscrypto.decode(enclink["ct"],kkey,enclink["s"].decode("hex"))
                    
                    #print lnk
                    enclink=lnk
                #enclink=enclink[0]
                #print 'enclink',enclink
                #reg='player_div", "st":"(.*?)"'
                #encst=re.findall(reg,enclinkhtml)[0]
        
    else:
        usediv=True
        #print 'usediv',usediv
        enclink=enclink[0]
        #print 'enclink',enclink
        reg='player_div", "st":"(.*?)"'
        encst=re.findall(reg,enclinkhtml)[0]
    #if usediv:
    #    print 'usediv',usediv
    #    enclink=enclink[0]
    #    print 'enclink',enclink
    #    reg='player_div", "st":"(.*?)"'
    #    encst=re.findall(reg,enclinkhtml)[0]
        
    decodedst=decode(encst)

    #print encst, decodedst
    reg='"stkey":"(.*?)"'
    sitekey=re.findall(reg,decodedst)[0]
    #sitekey="myFhOWnjma1omjEf9jmH9WZg91CC"#hardcoded
    urlToPlaymain=decode(enclink.replace(sitekey,""))
    urlToPlay= urlToPlaymain
    newcj=cookielib.LWPCookieJar();
    try:
        getUrl(urlToPlay, headers=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36'),('Referer','http://h5.adshell.net/flash')],cookieJar=newcj)
    except: pass
    print newcj
    return urlToPlaymain+"|Referer=%s&User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36&X-Requested-With=ShockwaveFlash/22.0.0.209&Cookie=PHPSESSID=%s"%("http://h5.adshell.net/flash",getCookiesString(newcj,'PHPSESSID').split('=')[-1])
    
def select365(url):
    print 'select365',url
    url=base64.b64decode(url)
    retUtl=""
    
    try:
        links=[]
        matchhtml=getUrl(url)        
        reg=".open\('(.*?)'.*?>(.*?)<"
        sourcelinks=re.findall(reg,matchhtml)
        b6=False

        enc=False
        if 1==2 and len(sourcelinks)==0:
            reg="showPopUpCode\\('(.*?)'.*?\\.write.*?d64\\(\\\\\\'(.*?)\\\\\\'\\)"
            sourcelinks=re.findall(reg,matchhtml)
            #print 'f',sourcelinks
            b6=True
        if 1==2 and len(sourcelinks)==0:
            reg="showPopUpCode\\('(.*?)'.*?\\.write.*?atob\\(\\\\\\'(.*?)\\\\\\'\\)"
            sourcelinks=re.findall(reg,matchhtml)
            #print 's',sourcelinks
            b6=True            
        if len(sourcelinks)==0:
            reg="showWindow\\('(.*?)',.*?>(.*?)<"
            sourcelinks=re.findall(reg,matchhtml)
            #print sourcelinks
            enc=True    
            b6=False
        if len(sourcelinks)==0:
            reg="showPopUpCode\\(.*?,.?'(.*?)'.*?,.*?,(.*?)\\)"
            sourcelinks=re.findall(reg,matchhtml)
            #print sourcelinks
            enc=True    
            b6=False
            
        #print 'sourcelinks',sourcelinks
        kkey=get365Key(get365CookieJar())
        if len(sourcelinks)==0:
            print 'No links',matchhtml
            #addDir(Colored("  -"+"No links available yet, Refresh 5 mins before start.",'') ,"" ,0,"", False, True,isItFolder=False)		#name,url,mode,icon
            return ""
        else:
            available_source=[]
            ino=0
            for curl,cname in sourcelinks:
                ino+=1
                try:
                    if b6:
                        curl,cname=cname,curl
                        #print b6,curl
                        curl=base64.b64decode(curl)
                        curl=re.findall('(http.*?)"',curl)[0]#+'/768/432'
                    if enc:
                        #print curl
                        curl=json.loads(curl.decode("base64"))
                        import jscrypto
                        #print curl["ct"],kkey,curl["s"]
                        curl=jscrypto.decode(curl["ct"],kkey,curl["s"].decode("hex"))
                        #print curl
                        curl=curl.replace('\\/','/').replace('"',"")
                        print 'fina;',curl
                        if 'window.atob' in curl:
                            reg="window\\.atob\(\\\\(.*?)\\\\\\)"
                            #print 'in regex',reg,curl
                            curl=re.findall(reg,curl)[0]
                            curl=base64.b64decode(curl)
                            curl=re.findall('(http.*?)"',curl)[0]#+'/768/432'
                            if not curl.split('/')[-2].isdigit():
                                curl+='/768/432'
                                
                    print curl
                    cname=cname.encode('ascii', 'ignore').decode('ascii')
                    #if not cname.startswith('link'):
                    cname='source# '+str(ino)
                    available_source.append(cname)
                    links+=[[cname,curl]]
                except:
                    traceback.print_exc(file=sys.stdout)
            if len(curl)==0:
                return ""
            if len(curl)==1:
                return links[0][1]
            dialog = xbmcgui.Dialog()
            index = dialog.select('Choose your link', available_source)
            if index > -1:
                return links[index][1]    

    except:
        traceback.print_exc(file=sys.stdout)
    return retUtl

    
def getCookiesString(cookieJar,cookieName=None):
    try:
        cookieString=""
        for index, cookie in enumerate(cookieJar):
            if cookieName==None:
                cookieString+=cookie.name + "=" + cookie.value +";"
            elif (cookieName==cookie.name or cookieName in cookie.name ):
                cookieString=cookie.name + "=" + cookie.value +";"
    except: pass
    print 'cookieString',cookieString
    return cookieString
