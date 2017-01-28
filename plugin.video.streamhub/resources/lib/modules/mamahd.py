import xbmc,os,re,sys,hashlib,urllib,urlparse,json,base64,random,datetime,urllib2,cookielib,traceback,requests

def getUrl(url, cookieJar=None,post=None, timeout=20, headers=None,jsonpost=False):

    cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
    opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
    #opener = urllib2.install_opener(opener)
    header_in_page=None
    if '|' in url:
        url,header_in_page=url.split('|')
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
    if headers:
        for h,hv in headers:
            req.add_header(h,hv)
    if header_in_page:
        header_in_page=header_in_page.split('&')
        
        for h in header_in_page:
            if len(h.split('='))==2:
                n,v=h.split('=')
            else:
                vals=h.split('=')
                n=vals[0]
                v='='.join(vals[1:])
                #n,v=h.split('=')
            #print n,v
            req.add_header(n,v)
            
    if jsonpost:
        req.add_header('Content-Type', 'application/json')
    response = opener.open(req,post,timeout=timeout)
    if response.info().get('Content-Encoding') == 'gzip':
            from StringIO import StringIO
            import gzip
            buf = StringIO( response.read())
            f = gzip.GzipFile(fileobj=buf)
            link = f.read()
    else:
        link=response.read()
    response.close()
    return link;

def playmamahd(url):
    headers=[('Referer','http://mamahd.com/index.html'),('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')]

    watchHtml=getUrl(url,headers=headers)
    videframe=re.findall('<iframe wid.*?src="(.*?)"' ,watchHtml)[0]
    watchHtml=getUrl(videframe,headers=headers)
    if 'hdcast' in watchHtml or 'static.bro' in watchHtml:
        return playHDCast(videframe, "http://mamahd.com/")

def playHDCast(url, mainref, altref=None):
    try:
        cookieJar=getHDCASTCookieJar()
        firstframe=url
        pageURl=mainref
        agent='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
        headers=[('Referer',pageURl),('User-Agent',agent)]                       
        result = getUrl(firstframe, headers=headers, cookieJar=cookieJar)

        regid='<script.*?id=[\'"](.*?)[\'"].*?width=[\'"]?(.*?)[\'"]?\;.*?height=[\'"]?(.*?)[\'"]?\;.*?src=[\'"](.*?)[\'"]'
        id,wd,ht, jsurl=re.findall(regid,result)[0]
        finalpageUrl=''
        headers=[('Referer',pageURl),('User-Agent',agent)]                       


        jsresult = getUrl(jsurl, headers=headers, cookieJar=cookieJar)
        broadcast=False
        if not 'bro.adca' in jsresult:
            regjs='src=[\'"](.*?)[\'"]'
            embedUrl=re.findall(regjs,jsresult)[0]
            embedUrl+=id+'&vw='+wd+'&vh='+ht
        else:
            broadcast=True
            regjs="var url = '(.*?)'"
            embedUrl=re.findall(regjs,jsresult)[0]
            embedUrl='http://bro.adca.st'+embedUrl+id+'&width='+wd+'&height='+ht
        headers=[('Referer',altref if not altref==None else mainref),('User-Agent',agent)]                             
        result=getUrl(embedUrl, headers=headers, cookieJar=cookieJar)

        if not broadcast:# in result:
            if 'blockscript=' in result: #ok captcha here
                try:
                    tries=0
                    while 'blockscript=' in result and tries<2:
                        tries+=1
                        xval=re.findall('name="x" value="(.*?)"',result)[0]
                        urlval=re.findall('name="url" value="(.*?)"',result)[0]
                        blocscriptval=re.findall('name="blockscript" value="(.*?)"',result)[0]
                        imageurl=re.findall('<td nowrap><img src="(.*?)"',result)[0].replace('&amp;','&')             
                        if not imageurl.startswith('http'):
                            imageurl='http://hdcast.org'+imageurl
                        headersforimage=[('Referer',embedUrl),('Origin','http://hdcast.org'),('User-Agent',agent)]     
                        captchaval=getHDCastCaptcha(imageurl,cookieJar,headersforimage , tries )
                        if captchaval=="": break
                        post={'blockscript':blocscriptval, 'x':xval, 'url':urlval,'val':captchaval}
                        post = urllib.urlencode(post)
                        
                        result=getUrl(embedUrl,post=post, headers=headersforimage, cookieJar=cookieJar)
                        cookieJar.save (HDCASTCookie,ignore_discard=True)
                        result=getUrl(embedUrl, headers=headers, cookieJar=cookieJar)
                        xbmc.log(str(result))
                except: 
                    print 'error in catpcha'
                    traceback.print_exc(file=sys.stdout)
            streamurl = re.findall('<div id=[\'"]player.*\s*<iframe.*?src=(.*?)\s',result)
            if len(streamurl)>0:
                headers=[('Referer',embedUrl),('User-Agent',agent)]                             
                html=getUrl(streamurl[0].replace('&amp;','&'),headers=headers, cookieJar=cookieJar)
                streamurl = re.findall('file:["\'](.*?)["\']',html)[0]
                return (streamurl + '|User-Agent='+ agent +'&Referer=' + embedUrl)
            if 'rtmp' in result:
                print 'rtmp'
                streamurl= re.findall('"(rtmp.*?)"' , result)[0]
                cookieJar.save (HDCASTCookie,ignore_discard=True)
                return (streamurl + ' timeout=20 live=1')
            else:
                Msg="Links not found, try again"
                dialog = xbmcgui.Dialog()
                ok = dialog.ok('Link parsing failed', Msg)
                return False
                
        else:
            headers=[('Referer',embedUrl),('User-Agent',agent),('X-Requested-With','XMLHttpRequest')]                             
            token=getUrl('http://bro.adca.st/getToken.php',headers=headers, cookieJar=cookieJar )
            token=re.findall('"token":"(.*?)"',token)[0]
            streamurl = re.findall('curl = "(.*?)"',result)[0]
            streamurl=base64.b64decode(streamurl)
            cookieJar.save (HDCASTCookie,ignore_discard=True)
            return (streamurl + token + '|User-Agent=' + agent + '&Referer=' + embedUrl)

    except:
        traceback.print_exc(file=sys.stdout)
        return False
		
def getHDCASTCookieJar(updatedUName=False):
    cookieJar=None
    try:
        cookieJar = cookielib.LWPCookieJar()
        if not updatedUName:
            cookieJar.load(HDCASTCookie,ignore_discard=True)
    except: 
        cookieJar=None

    if not cookieJar:
        cookieJar = cookielib.LWPCookieJar()
    return cookieJar

def getHDCastCaptcha(imageurl,cookieJar, headers, tries):
    retcaptcha=""
    if 1==1:
        local_captcha = os.path.join(profile_path, "captchaC%s.img"%str(tries) )
        localFile = open(local_captcha, "wb")
        localFile.write(getUrl(imageurl,cookieJar,headers=headers))
        localFile.close()
        cap=""#cap=parseCaptcha(local_captcha)
        #if originalcaptcha:
        #    cap=parseCaptcha(local_captcha)
        #print 'parsed cap',cap
        if cap=="":
            solver = InputWindow(captcha=local_captcha)
            retcaptcha = solver.get()
    return retcaptcha