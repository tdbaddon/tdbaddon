'''
Created on 22 jan 2012

@author: Batch
'''
import os
import urllib
import urllib2
import cookielib
import hashlib
from filehelpers import get_file_age, read_from_file, write_to_file

USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

def get_url(url, params=None, referer=None, cookie_jar=None, cache=None, cache_time=3600):
    print url
    if cache:
        h = hashlib.md5(url).hexdigest()
        cache_file = os.path.join(cache, h)
        age = get_file_age(cache_file)
        if age > 0 and age < cache_time:
            r = read_from_file(cache_file, silent=True)
            if r:
                return r
    
    if params:
        paramsenc = urllib.urlencode(params)
        req = urllib2.Request(url, paramsenc)
    else:
        req = urllib2.Request(url)

    req.add_header('User-Agent', USER_AGENT)
    if referer:
        req.add_header('Referer', referer)
        
    if cookie_jar:
        cj = cookielib.LWPCookieJar()
        try:
            cj.load(cookie_jar, ignore_discard=True)
        except:
            print "Could not load cookie jar file."
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        response = opener.open(req)
        cj.save(cookie_jar, ignore_discard=True)
    else:
        response = urllib2.urlopen(req)
    body = response.read()
    response.close()
    
    if cache:
        write_to_file(cache_file, body)
    
    return body

def get_file_size(url):
    usock = urllib2.urlopen(url)
    size = usock.info().get('Content-Length')
    if size is None:    
        size = 0
    size = float(size) # in bytes
    size = size / 1024.0# in KB (KiloBytes)
    size = size / 1024.0# in MB
    size = size / 1024.0# in GB

    return size
	
def get_file_size_MB(url):
    usock = urllib2.urlopen(url)
    size = usock.info().get('Content-Length')
    if size is None:    
        size = 0
    size = float(size) # in bytes
    size = size / 1024.0# in KB (KiloBytes)
    size = size / 1024.0# in MB

    return size
	

