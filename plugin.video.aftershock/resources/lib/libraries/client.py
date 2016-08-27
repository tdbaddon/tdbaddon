# -*- coding: utf-8 -*-

'''
    Copyright (C) 2015 lambda

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import re,sys,urllib2,HTMLParser, time, urlparse, gzip, StringIO, cookielib, urllib

import control
import traceback
from resources.lib.libraries import cache

def request(url, close=True, error=False, proxy=None, post=None, headers=None, mobile=False, referer=None, cookie=None, output='', timeout='30', debug=False, compression=False, limit=None):
    try:
        handlers = []
        if not proxy == None:
            handlers += [urllib2.ProxyHandler({'http':'%s' % (proxy)}), urllib2.HTTPHandler]
            opener = urllib2.build_opener(*handlers)
            opener = urllib2.install_opener(opener)
        if output == 'cookie' or not close == True:
            import cookielib
            cookies = cookielib.LWPCookieJar()
            handlers += [urllib2.HTTPHandler(), urllib2.HTTPSHandler(), urllib2.HTTPCookieProcessor(cookies)]
            opener = urllib2.build_opener(*handlers)
            opener = urllib2.install_opener(opener)
        try:
            if sys.version_info < (2, 7, 9): raise Exception()
            import ssl; ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            handlers += [urllib2.HTTPSHandler(context=ssl_context)]
            opener = urllib2.build_opener(*handlers)
            opener = urllib2.install_opener(opener)
        except:
            pass

        try: headers.update(headers)
        except: headers = {}
        if 'User-Agent' in headers:
            pass
        elif not mobile == True:
            #headers['User-Agent'] = 'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'
            headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
        else:
            headers['User-Agent'] = 'Apple-iPhone/701.341'
        if 'referer' in headers:
            pass
        elif referer == None:
            headers['referer'] = url
        else:
            headers['referer'] = referer
        if not 'Accept-Language' in headers:
            headers['Accept-Language'] = 'en-US'
        if 'cookie' in headers:
            pass
        elif not cookie == None:
            headers['cookie'] = cookie

        request = urllib2.Request(url, data=post, headers=headers)

        for i in range(0,3):
            try:
                response = urllib2.urlopen(request, timeout=int(timeout))
                break
            except urllib2.HTTPError as response:
                if debug :
                    retryafter = int(response.headers['Retry-After'])
                    time.sleep(retryafter)
                if response.code == 503:
                    if 'cf-browser-verification' in response.read(5242880):

                        netloc = '%s://%s' % (urlparse.urlparse(url).scheme, urlparse.urlparse(url).netloc)

                        cf = cache.get(cfcookie, 168, netloc, headers['User-Agent'], timeout)

                        headers['Cookie'] = cf

                        request = urllib2.Request(url, data=post, headers=headers)

                        response = urllib2.urlopen(request, timeout=int(timeout))
                        break
                    elif error == False:
                        return

                elif error == False:
                    return
            except:
                import traceback
                traceback.print_exc()
                pass
        if output == 'cookie':
            result = []
            for c in cookies: result.append('%s=%s' % (c.name, c.value))
            result = "; ".join(result)
        elif output == 'response':
            if limit == '0':
                result = (str(response.code), response.read(224 * 1024))
            elif not limit == None:
                result = (str(response.code), response.read(int(limit) * 1024))
            else:
                result = (str(response.code), response.read(5242880))
        elif output == 'chunk':
            content = int(response.headers['Content-Length'])
            if content < (2048 * 1024): return
            result = response.read(16 * 1024)
        elif output == 'extended':
            try: cookie = '; '.join(['%s=%s' % (i.name, i.value) for i in cookies])
            except: pass
            try: cookie = cf
            except: pass
            content = response.headers
            result = response.read(5242880)
            return (result, headers, content, cookie)
        elif output == 'geturl':
            result = response.geturl()
        else:
            if limit == '0':
                result = response.read(224 * 1024)
            elif not limit == None:
                result = response.read(int(limit) * 1024)
            else:
                result = response.read(5242880)
        try:
            if response.headers['content-encoding'].lower() == 'gzip':
                result = gzip.GzipFile(fileobj=StringIO.StringIO(result)).read()
        except:
            pass

        if close == True:
            response.close()

        return result
    except:
        return

def source(url, close=True, error=False, proxy=None, post=None, headers=None, mobile=False, referer=None, cookie=None, output='', timeout='30', compression=False, limit=None):
    return request(url, close, error, proxy, post, headers, mobile, referer, cookie, output, timeout, compression, limit)

def cfcookie(netloc, ua, timeout):
    try:
        headers = {'User-Agent': ua}

        request = urllib2.Request(netloc, headers=headers)

        try:
            response = urllib2.urlopen(request, timeout=int(timeout))
        except urllib2.HTTPError as response:
            result = response.read(5242880)

        jschl = re.findall('name="jschl_vc" value="(.+?)"/>', result)[0]

        init = re.findall('setTimeout\(function\(\){\s*.*?.*:(.*?)};', result)[-1]

        builder = re.findall(r"challenge-form\'\);\s*(.*)a.v", result)[0]

        decryptVal = parseJSString(init)

        lines = builder.split(';')

        for line in lines:

            if len(line) > 0 and '=' in line:

                sections=line.split('=')
                line_val = parseJSString(sections[1])
                decryptVal = int(eval(str(decryptVal)+sections[0][-1]+str(line_val)))

        answer = decryptVal + len(urlparse.urlparse(netloc).netloc)

        query = '%s/cdn-cgi/l/chk_jschl?jschl_vc=%s&jschl_answer=%s' % (netloc, jschl, answer)

        if 'type="hidden" name="pass"' in result:
            passval = re.findall('name="pass" value="(.*?)"', result)[0]
            query = '%s/cdn-cgi/l/chk_jschl?pass=%s&jschl_vc=%s&jschl_answer=%s' % (netloc, urllib.quote_plus(passval), jschl, answer)
            time.sleep(5)

        cookies = cookielib.LWPCookieJar()
        handlers = [urllib2.HTTPHandler(), urllib2.HTTPSHandler(), urllib2.HTTPCookieProcessor(cookies)]
        opener = urllib2.build_opener(*handlers)
        opener = urllib2.install_opener(opener)

        try:
            request = urllib2.Request(query, headers=headers)
            response = urllib2.urlopen(request, timeout=int(timeout))
        except:
            pass

        cookie = '; '.join(['%s=%s' % (i.name, i.value) for i in cookies])

        return cookie
    except:
        pass

def parseJSString(s):
    try:
        offset=1 if s[0]=='+' else 0
        val = int(eval(s.replace('!+[]','1').replace('!![]','1').replace('[]','0').replace('(','str(')[offset:]))
        return val
    except:
        pass

def parseDOM(html, name=u"", attrs={}, ret=False):
    # Copyright (C) 2010-2011 Tobias Ussing And Henrik Mosgaard Jensen

    if isinstance(html, str):
        try:
            html = [html.decode("utf-8")] # Replace with chardet thingy
        except:
            html = [html]
    elif isinstance(html, unicode):
        html = [html]
    elif not isinstance(html, list):
        return u""

    if not name.strip():
        return u""

    ret_lst = []
    for item in html:
        temp_item = re.compile('(<[^>]*?\n[^>]*?>)').findall(item)
        for match in temp_item:
            item = item.replace(match, match.replace("\n", " "))

        lst = []
        for key in attrs:
            lst2 = re.compile('(<' + name + '[^>]*?(?:' + key + '=[\'"]' + attrs[key] + '[\'"].*?>))', re.M | re.S).findall(item)
            if len(lst2) == 0 and attrs[key].find(" ") == -1:  # Try matching without quotation marks
                lst2 = re.compile('(<' + name + '[^>]*?(?:' + key + '=' + attrs[key] + '.*?>))', re.M | re.S).findall(item)

            if len(lst) == 0:
                lst = lst2
                lst2 = []
            else:
                test = range(len(lst))
                test.reverse()
                for i in test:  # Delete anything missing from the next list.
                    if not lst[i] in lst2:
                        del(lst[i])

        if len(lst) == 0 and attrs == {}:
            lst = re.compile('(<' + name + '>)', re.M | re.S).findall(item)
            if len(lst) == 0:
                lst = re.compile('(<' + name + ' .*?>)', re.M | re.S).findall(item)

        if isinstance(ret, str):
            lst2 = []
            for match in lst:
                attr_lst = re.compile('<' + name + '.*?' + ret + '=([\'"].[^>]*?[\'"])>', re.M | re.S).findall(match)
                if len(attr_lst) == 0:
                    attr_lst = re.compile('<' + name + '.*?' + ret + '=(.[^>]*?)>', re.M | re.S).findall(match)
                for tmp in attr_lst:
                    cont_char = tmp[0]
                    if cont_char in "'\"":
                        # Limit down to next variable.
                        if tmp.find('=' + cont_char, tmp.find(cont_char, 1)) > -1:
                            tmp = tmp[:tmp.find('=' + cont_char, tmp.find(cont_char, 1))]

                        # Limit to the last quotation mark
                        if tmp.rfind(cont_char, 1) > -1:
                            tmp = tmp[1:tmp.rfind(cont_char)]
                    else:
                        if tmp.find(" ") > 0:
                            tmp = tmp[:tmp.find(" ")]
                        elif tmp.find("/") > 0:
                            tmp = tmp[:tmp.find("/")]
                        elif tmp.find(">") > 0:
                            tmp = tmp[:tmp.find(">")]

                    lst2.append(tmp.strip())
            lst = lst2
        else:
            lst2 = []
            for match in lst:
                endstr = u"</" + name

                start = item.find(match)
                end = item.find(endstr, start)
                pos = item.find("<" + name, start + 1 )

                while pos < end and pos != -1:
                    tend = item.find(endstr, end + len(endstr))
                    if tend != -1:
                        end = tend
                    pos = item.find("<" + name, pos + 1)

                if start == -1 and end == -1:
                    temp = u""
                elif start > -1 and end > -1:
                    temp = item[start + len(match):end]
                elif end > -1:
                    temp = item[:end]
                elif start > -1:
                    temp = item[start + len(match):]

                if ret:
                    endstr = item[end:item.find(">", item.find(endstr)) + 1]
                    temp = match + temp + endstr

                item = item[item.find(temp, item.find(match)) + len(temp):]
                lst2.append(temp)
            lst = lst2
        ret_lst += lst

    return ret_lst

def replaceHTMLCodes(txt):
    txt = re.sub("(&#[0-9]+)([^;^0-9]+)", "\\1;\\2", txt)
    txt = txt.replace('&#8236;','')
    txt = HTMLParser.HTMLParser().unescape(txt)
    txt = txt.replace("&quot;", "\"")
    txt = txt.replace("&amp;", "&")
    return txt

def getVideoID(url):
    try :
        return re.compile('(id|url|v|si|sim|data-config|file)=(.+?)/').findall(url + '/')[0][1]
    except:
        return

def urlRewrite(url):
    urlReWriteDict = [{'host':'letwatch.php','url':'http://letwatch.us/embed-%s-650x400.html'},
                      {'host':'playwire.php','url':'http://config.playwire.com/%s/player.json'},
                      {'host':'dailymotion.php','url':'http://www.dailymotion.com/embed/video/%s'},
                      {'host':'speedplay.php','url':'http://speedplay.me/embed-%s.html'},
                      {'host':'watchvideo.php','url':'http://watchvideo.us/embed-%s.html'},
                      {'host':'cloudy.php','url':'http://www.cloudy.ec/embed.php?id=%s&width=650&height=410'},
                      {'host':'tvlogy.php','url':'http://tvlogy.to/watch.php?v=%s'},
                      {'host':'idowatch.php','url':'http://idowatch.us/embed-%s.html'},
                      {'host':'playu.php','url':'http://playu.net/embed-%s-700x440.html'},
                      {'host':'nowvideo.php','url':'http://embed.nowvideo.sx/embed.php?v=%s&amp;wmode=direct&amp;autoplay=true&controls=false'},
                      {'host':'openload.php','url':'https://openload.co/embed/%s/'},
                      {'host':'thevideo.php','url':'http://www.thevideo.me/embed-%s-650x400.html'},
                      {'host':'vodlocker.php','url':'http://vodlocker.com/embed-%s-650x400.html'}]
    try :
        videoID = getVideoID(url)
        for i in urlReWriteDict:
            try :
                if re.compile(i['host']).findall(url)[0]:
                    return i['url'] % videoID
            except:
                pass
        return url
    except:
        return url

def host(url):
    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
    return str(host)

def agent():
    return 'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'

def printException(function):
    try :debug = True if control.setting('debug') == 'true' else False
    except: debug = True
    if debug:
        print 'Exception in %s' % (function)
        traceback.print_exc()
