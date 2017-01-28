# -*- coding: utf-8 -*-

import urllib
import urllib2
import re

IPHONE_UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F70 Safari/600.1.4'

def parse_livestream(params):
    req = urllib2.Request(params)       
    req.add_header('User-Agent', IPHONE_UA)
    response = urllib2.urlopen(req)
    response = response.read().decode("utf-8").encode("utf-8")
    stream_url = re.search('"m3u8_url":"(.+?)"', response).group(1)
    print "stream_url: " + stream_url
    
    
    try:
        print "M3U8!!!" + stream_url
        req = urllib2.Request(stream_url)
        response = urllib2.urlopen(req)                    
        master = response.read()
        response.close()
        cookie = ''
        try:
            print "response cookie: " + response.info().getheader('Set-Cookie')
            cookie =  urllib.quote(response.info().getheader('Set-Cookie'))
        except:
            pass

        print "Cookie: " + cookie
        print "Master: " + master

        line = re.compile("(.+?)\n").findall(master)  

        for temp_url in line:
            print "temp_url: " + temp_url
            if '.m3u8' in temp_url:
                temp_url = temp_url+'|User-Agent='+IPHONE_UA              
                if cookie != '':
                    temp_url = temp_url + '&Cookie='+cookie

                return temp_url
    except:
        pass