import sys,traceback,urllib2,re
def createCookie(url,cj=None,agent='Mozilla/5.0 (Windows NT 6.1; rv:32.0) Gecko/20100101 Firefox/32.0'):
    urlData=''
    try:
        import urlparse,cookielib

        class NoRedirection(urllib2.HTTPErrorProcessor):    
            def http_response(self, request, response):
                return response

        def parseJSString(s):
            try:
                offset=1 if s[0]=='+' else 0
                val = int(eval(s.replace('!+[]','1').replace('!![]','1').replace('[]','0').replace('(','str(')[offset:]))
                return val
            except:
                pass

        #agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'
        if cj==None:
            cj = cookielib.CookieJar()

        opener = urllib2.build_opener(NoRedirection, urllib2.HTTPCookieProcessor(cj))
        opener.addheaders = [('User-Agent', agent)]
        response = opener.open(url)
        result=urlData = response.read()

        jschl = re.compile('name="jschl_vc" value="(.+?)"/>').findall(result)[0]

        init = re.compile('setTimeout\(function\(\){\s*.*?.*:(.*?)};').findall(result)[0]
        builder = re.compile(r"challenge-form\'\);\s*(.*)a.v").findall(result)[0]
        decryptVal = parseJSString(init)
        lines = builder.split(';')

        for line in lines:
            if len(line)>0 and '=' in line:
                sections=line.split('=')

                line_val = parseJSString(sections[1])
                decryptVal = int(eval(str(decryptVal)+sections[0][-1]+str(line_val)))

        answer = decryptVal + len(urlparse.urlparse(url).netloc)

        u='/'.join(url.split('/')[:-1])
        query = '%s/cdn-cgi/l/chk_jschl?jschl_vc=%s&jschl_answer=%s' % (u, jschl, answer)

        opener = urllib2.build_opener(NoRedirection, urllib2.HTTPCookieProcessor(cj))
        opener.addheaders = [('User-Agent', agent)]
        response = opener.open(query)
        #cookie = str(response.headers.get('Set-Cookie'))
        #response = opener.open(url)
        #print cj
        #print response.read()
        response.close()

        return urlData
    except:
        traceback.print_exc(file=sys.stdout)
        return urlData

