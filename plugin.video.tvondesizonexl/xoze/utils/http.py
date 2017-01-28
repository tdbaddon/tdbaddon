'''
Created on Dec 9, 2013

@author: ajdeveloped@gmail.com

This file is part of XOZE. 

XOZE is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

XOZE is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with XOZE.  If not, see <http://www.gnu.org/licenses/>.
'''
from BeautifulSoup import BeautifulSoup
from urllib2 import HTTPError
from xoze.utils.patterns import Singleton
import cookielib
import htmlentitydefs
import httplib
import logging
import re
import urllib
import urllib2
'''
Created on Oct 29, 2011

@author: ajju
'''

'''
To handle incomplete read issue
'''
def patch_http_response_read(func):
    def inner(*args):
        try:
            return func(*args)
        except httplib.IncompleteRead, e:
            return e.partial

    return inner
httplib.HTTPResponse.read = patch_http_response_read(httplib.HTTPResponse.read)


def parse_url_params(url):
    params = {}
    if url is None:
        return params
    paramstring = url
    if len(paramstring) >= 2:
        paramstring = paramstring.replace('?', '')
        if (paramstring[len(paramstring) - 1] == '/'):
            paramstring = paramstring[0:len(paramstring) - 2]
        pairsofparams = paramstring.split('&')
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                params[splitparams[0]] = urllib.unquote_plus(splitparams[1])
    return params

def get_redirected_url(url, data=None):
    opener = urllib2.build_opener(urllib2.HTTPRedirectHandler)
    if data == None:
        return opener.open(url).url
    else:
        return opener.open(url, data).url

def unescape(url):
    htmlCodes = [
                 ['&', '&amp;'],
                 ['<', '&lt;'],
                 ['>', '&gt;'],
                 ['"', '&quot;'],
                 ]
    for code in htmlCodes:
        url = url.replace(code[1], code[0])
    return url


def cUConvert(m): return unichr(int(m.group(1)))
def cTConvert(m): return unichr(htmlentitydefs.name2codepoint.get(m.group(1), 32))

def convertHTMLCodes(html):
    try:
        html = re.sub('&#(\d{1,5});', cUConvert, html.decode('utf-8', 'replace'))
        html = re.sub('&(\w+?);', cTConvert, html)
    except Exception, e:
        logging.getLogger().error(e)
    return html

def getUserAgentForXBMCPlay():
    return 'User-Agent=' + urllib.quote_plus('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_1) AppleWebKit/534.48.3 (KHTML, like Gecko) Version/5.1 Safari/534.48.3' + '&Accept=' + urllib.quote_plus('text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8') + '&Accept_Encoding=' + urllib.quote_plus('gzip, deflate'))

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_1) AppleWebKit/534.48.3 (KHTML, like Gecko) Version/5.1 Safari/534.48.3'}
# , 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept_Encoding':'gzip, deflate'
# HttpClient
class HttpClient(Singleton):
    
    def __initialize__(self):
        self.__cookiejar = cookielib.LWPCookieJar()
        self.__cookiesEnabled = False
        
    def enable_cookies(self, cookieJar=None, cookiesFilePath=None):
        if cookieJar is not None:
            self.__cookiejar = cookieJar
        elif cookiesFilePath is not None:
            self.load_cookies_from_file(cookiesFilePath)
        else:
            cookieJar = self.__cookiejar
        http_cookiejar = urllib2.HTTPCookieProcessor(cookieJar)
        opener = urllib2.build_opener(http_cookiejar)
        urllib2.install_opener(opener)
        urllib2.HTTPSHandler(debuglevel=1)
        self.__cookiesEnabled = True
        
        
    def disable_cookies(self):
        urllib2.install_opener(None)
        self.__cookiesEnabled = False
        
    def save_cookies_to_file(self, filepath):
        self.__cookiejar.save(filename=filepath, ignore_discard=True, ignore_expires=True)
        
    def load_cookies_from_file(self, filepath):
        self.__cookiejar.load(filename=filepath, ignore_discard=True, ignore_expires=True)
    
    def get_cookie_jar(self):
        return self.__cookiejar
    
    def get_cookie_string(self):
        cookies = ''
        if self.__cookiejar is not None:
            for cookie in self.__cookiejar:
                cookies = cookies + cookie.name + '=' + cookie.value + '; '
        return cookies
    
    def get_html_content(self, url, params=None, headers=None, accept_500_error=False):
        if headers is None:
            headers = HEADERS
        data = None
        if params is not None:
            data = urllib.urlencode(params)
        req = urllib2.Request(url, data, headers)
        if self.__cookiesEnabled and self.__cookiejar is not None:
            self.__cookiejar.add_cookie_header(req);
        html = None
        try:
            response = urllib2.urlopen(req)
            html = response.read()
            response.close()
        except HTTPError, e:
            if accept_500_error and e.getcode() == 500:
                html = e.read()
            else:
                raise
        return html
    
    def get_response(self, url, params=None, headers=None):
        if headers is None:
            headers = HEADERS
        data = None
        if params is not None:
            data = urllib.urlencode(params)
        req = urllib2.Request(url, data, headers)
        if self.__cookiesEnabled and self.__cookiejar is not None:
            self.__cookiejar.add_cookie_header(req);
        response = urllib2.urlopen(req)
        return response
    
    def get_response_for_request(self, req, headers=None):
        if headers is None:
            headers = HEADERS
        for key in headers.keys():
            req.add_header(key, headers[key])
        if self.__cookiesEnabled and self.__cookiejar is not None:
            self.__cookiejar.add_cookie_header(req);
        response = urllib2.urlopen(req)
        return response
    
    def get_beautiful_soup(self, url, params=None, headers=None, parseOnlyThese=None, accept_500_error=False):
        return BeautifulSoup(self.get_html_content(url, params, headers, accept_500_error), parseOnlyThese=parseOnlyThese)
        
    def add_http_cookies_to_url(self, url, addHeaders=True, addCookies=True, extraExtraHeaders={}):
        url = url + '|'
        if addHeaders:
            url = url + getUserAgentForXBMCPlay() + '&'
        if addCookies:
            url = url + 'Cookie=' + urllib.quote_plus(self.get_cookie_string()) + '&'
        for extraHeaderName in extraExtraHeaders:
            url = url + extraHeaderName + '=' + urllib.quote_plus(extraExtraHeaders[extraHeaderName])
        return url
    
    def do_clean(self):
        del self.__cookiejar
        del self.__cookiesEnabled
