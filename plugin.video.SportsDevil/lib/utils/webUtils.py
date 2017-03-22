# -*- coding: utf-8 -*-

import os
import re
import urllib
import urlparse
import requests
import socket
import time
from cookielib import LWPCookieJar
from HTMLParser import HTMLParser
from fileUtils import fileExists, setFileContent, getFileContent

#------------------------------------------------------------------------------
socket.setdefaulttimeout(30)

#use ipv4 only
origGetAddrInfo = socket.getaddrinfo

def getAddrInfoWrapper(host, port, family=0, socktype=0, proto=0, flags=0):
    return origGetAddrInfo(host, port, socket.AF_INET, socktype, proto, flags)

# replace the original socket.getaddrinfo by our version
socket.getaddrinfo = getAddrInfoWrapper
#------------------------------------------------------------------------------

'''
    REQUEST classes
'''

class BaseRequest(object):
    
    def __init__(self, cookie_file=None):
        self.cookie_file = cookie_file
        self.s = requests.Session()
        self.s.cookies = LWPCookieJar(self.cookie_file)
        if fileExists(self.cookie_file):
            self.s.cookies.load(ignore_discard=True)
        self.s.headers.update({'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'})
        self.s.headers.update({'Accept-Language' : 'en-US,en;q=0.5'})
        self.url = ''

    def fixurl(self, url):
        #url is unicode (quoted or unquoted)
        try:
            #url is already quoted
            url = url.encode('ascii')
        except:
            #quote url if it is unicode
            parsed_link = urlparse.urlsplit(url)
            parsed_link = parsed_link._replace(netloc=parsed_link.netloc.encode('idna'),
                                               path=urllib.quote(parsed_link.path.encode('utf-8')),
                                               query=urllib.quote(parsed_link.query.encode('utf-8'),safe='+?=&'),
                                               fragment=urllib.quote(parsed_link.fragment.encode('utf-8')))
            url = parsed_link.geturl().encode('ascii')
        #url is str (quoted)
        return url

    def getSource(self, url, form_data, referer, xml=False, mobile=False):
        url = self.fixurl(url)

        if not referer:
            referer = url
        else:
            referer = self.fixurl(referer.replace('wizhdsports.be','wizhdsports.is').replace('ibrod.tv','www.ibrod.tv').replace('livetv123.net','livetv.sx'))
        
        headers = {'Referer': referer}
        if mobile:
            self.s.headers.update({'User-Agent' : 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13E238 Safari/601.1'})
            
        if xml:
            headers['X-Requested-With'] = 'XMLHttpRequest'

        if 'cndhlsstream.pw' in urlparse.urlsplit(url).netloc:
            del self.s.headers['Accept-Encoding']
        if 'skstream.tv' in urlparse.urlsplit(url).netloc:
            del self.s.headers['Accept-Encoding']
        if 'bstream.tech' in urlparse.urlsplit(url).netloc:
            del self.s.headers['Accept-Encoding']
        if 'bcast.site' in urlparse.urlsplit(url).netloc:
            del self.s.headers['Accept-Encoding']
        if 'bcast.pw' in urlparse.urlsplit(url).netloc:
            del self.s.headers['Accept-Encoding']
        if 'live247.online' in urlparse.urlsplit(url).netloc:
            del self.s.headers['Accept-Encoding']
        if 'indexstream.tv' in urlparse.urlsplit(url).netloc:
            del self.s.headers['Accept-Encoding']
        
        if 'streamlive.to' in urlparse.urlsplit(url).netloc:
            self.s.verify = False
        
        if form_data:
            #zo**tv
            if 'uagent' in form_data[0]:
                form_data[0] = ('uagent',self.s.headers['User-Agent'])

            r = self.s.post(url, headers=headers, data=form_data, timeout=20)
        else:
            try:
                r = self.s.get(url, headers=headers, timeout=20)
            except (requests.exceptions.MissingSchema):
                return 'pass'
        
        #many utf8 encodings are specified in HTTP body not headers and requests only checks headers, maybe use html5lib
        #https://github.com/kennethreitz/requests/issues/2086
        if 'streamlive.to' in urlparse.urlsplit(url).netloc \
        or 'sport365.live' in urlparse.urlsplit(url).netloc \
        or 'vipleague' in urlparse.urlsplit(url).netloc \
        or 'cinestrenostv.tv' in urlparse.urlsplit(url).netloc \
        or 'batmanstream.com' in urlparse.urlsplit(url).netloc \
        or 'sportcategory.com' in urlparse.urlsplit(url).netloc:
            r.encoding = 'utf-8'
        if 'lfootball.ws' in urlparse.urlsplit(url).netloc:
            r.encoding = 'windows-1251'

        response  = r.text

        if 'beget=begetok' in response: # av
            _cookie = requests.cookies.create_cookie('beget','begetok',domain=urlparse.urlsplit(url).netloc,path='/')
            self.s.cookies.set_cookie(_cookie)
            r = self.s.get(url, headers=headers, timeout=20)
            response  = r.text

        if 'fromCharCode,sucuri_cloudproxy_js' in response: # sebn
            from sucuri import sucuri_decode
            sucuri_name, sucuri_value = sucuri_decode(response)
            sucuri_cookie = requests.cookies.create_cookie(sucuri_name,sucuri_value,domain=urlparse.urlsplit(url).netloc,path='/',
                                                           discard=False,expires=(time.time() + 86400))
            self.s.cookies.set_cookie(sucuri_cookie)
            r = self.s.get(url, headers=headers, timeout=20)
            response  = r.text

        if len(response) > 10:
            self.s.cookies.save(ignore_discard=True)

        self.s.close()
        return HTMLParser().unescape(response)


#------------------------------------------------------------------------------

class DemystifiedWebRequest(BaseRequest):

    def __init__(self, cookiePath):
        super(DemystifiedWebRequest,self).__init__(cookiePath)

    def getSource(self, url, form_data, referer='', xml=False, mobile=False, demystify=False):
        data = super(DemystifiedWebRequest, self).getSource(url, form_data, referer, xml, mobile)
        if not data:
            return None

        if not demystify:
            # remove comments
            r = re.compile('<!--.*?(?!//)--!*>', re.IGNORECASE + re.DOTALL + re.MULTILINE)
            m = r.findall(data)
            if m:
                for comment in m:
                    data = data.replace(comment,'')
        else:
            import decryptionUtils as crypt
            data = crypt.doDemystify(data)

        return data

#------------------------------------------------------------------------------

class CachedWebRequest(DemystifiedWebRequest):

    def __init__(self, cookiePath, cachePath):
        super(CachedWebRequest,self).__init__(cookiePath)
        self.cachePath = cachePath
        self.cachedSourcePath = os.path.join(self.cachePath, 'page.html')
        self.currentUrlPath = os.path.join(self.cachePath, 'currenturl')
        self.lastUrlPath = os.path.join(self.cachePath, 'lasturl')

    def __setLastUrl(self, url):
        setFileContent(self.lastUrlPath, url)

    def __getCachedSource(self):
        try:
            data = getFileContent(self.cachedSourcePath)
        except:
            pass
        return data

    def getLastUrl(self):
        return getFileContent(self.lastUrlPath)
        

    def getSource(self, url, form_data, referer='', xml=False, mobile=False, ignoreCache=False, demystify=False):
        if 'tvone.xml' in url:
            self.cachedSourcePath = url
            data = self.__getCachedSource()
            return data
        if '.r.de.a2ip.ru' in url:
            parsed_link = urlparse.urlsplit(url)
            parsed_link = parsed_link._replace(netloc=parsed_link.netloc.replace('.r.de.a2ip.ru','').decode('rot13'))
            url = parsed_link.geturl()
        if 'calls/get/source' in url:
            ignoreCache = True
            
        if url == self.getLastUrl() and not ignoreCache:
            data = self.__getCachedSource()
        else:
            data = super(CachedWebRequest,self).getSource(url, form_data, referer, xml, mobile, demystify)
            if data:
                # Cache url
                self.__setLastUrl(url)
                # Cache page
                setFileContent(self.cachedSourcePath, data)
        return data
