from __future__ import division
import urllib2
def getUrl(url, cookieJar=None,post=None, timeout=20, headers=None,jsonpost=False):

    cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
    opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
    #opener = urllib2.install_opener(opener)
    header_in_page=None
    if '|' in url:
        url,header_in_page=url.split('|')
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
    req.add_header('Accept-Encoding','gzip')

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

def gettext():
    jsdata=getUrl('http://www.smartcric.com/js/video.js')
    if jsdata.startswith('var _'):
        return gettext2(jsdata)
    import re
    anchorreg='parseInt\((.*?)\)'
    ancdata=re.findall(anchorreg,jsdata)[0]
    parsedata=re.findall('\[([0-9,\,]*)\];var %s=(.*?);.+?[^(parse)]parseInt\((.*?)\)'%ancdata,jsdata)[0]

    maincode=parsedata[0]
    mathdata=parsedata[1]
    s= '[%s]'%maincode;
    s=eval(s)
    #s=[47, 42]
    ss=[]
    MathData = eval(mathdata)
    for a in s:
        try:
            ss+=chr(a-int(MathData))
        except: 
            print 'error'
    print repr(  ''.join(ss))
    return 'v1',''.join(ss)

def gettext2(jstext):
    import re
    regs="var _.*?(\[.*?\])"
    vals=re.findall(regs,jstext)[0]
    d1= '\n'.join(eval(vals))
    d2=re.findall(";jako=(.*?);",jstext)[0]
    return 'v2',d1,d2
    
    
    
    
    