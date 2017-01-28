# -*- coding: utf-8 -*-

import json
import urllib
import urllib2
import re
import StringIO
import gzip

def parse_iliveto(params):
    # try:
    server_url = params["url"]
    url_token = params["url_token"]
            
    req = urllib2.Request(server_url)
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 5.0; en-US; rv:1.9.0.20) Gecko/20111022 Firefox/5.0")
    req.add_header("Accept-Encoding", "gzip")
    response = urllib2.urlopen(req)

    cookies = response.info().get('Set-Cookie')
    if response.info().get('Content-Encoding') == 'gzip':
        buf = StringIO.StringIO(response.read())
        gzip_f = gzip.GzipFile(fileobj=buf)
        response = gzip_f    
    response = response.read().decode("utf-8").encode("utf-8").decode("string_escape")
    url = re.search('streamer: "(.+?)"', response).group(1)
    url = url.replace("\\/", "/")
    
    file = re.search('file: "(.+?).flv"', response).group(1)
    
    req = urllib2.Request(url_token)
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 5.0; en-US; rv:1.9.0.20) Gecko/20111022 Firefox/5.0")
    req.add_header("Accept-Encoding", "gzip")
    req.add_header("Referer", server_url)
    req.add_header("Cookie", cookies);
    response = urllib2.urlopen(req)
    if response.info().get('Content-Encoding') == 'gzip':
        buf = StringIO.StringIO(response.read())
        gzip_f = gzip.GzipFile(fileobj=buf)
        response = gzip_f
    response = response.read().decode("utf-8").encode("utf-8").decode("string_escape")
    token = json.loads(response)
    token = token["token"]

    print "STREAMLIVE2: " + url + "/" + file + " token=" + token + " pageURL=" + server_url + " playpath=" + file + " tcURL= swfUrl=http://www.streamlive.to/ads/streamlive.swf swfVfy=true live=true"
    
    return url + "/" + file + " token=" + token + " pageURL=" + server_url + " playpath=" + file + " tcURL= swfUrl=http://www.streamlive.to/ads/streamlive.swf swfVfy=true live=true"
    # except:
    #    return ""
