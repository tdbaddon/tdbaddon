# -*- coding: utf-8 -*-

import plugintools
import urllib
import urllib2
import re

def parse_biggestplayer(params):
    try:
        server_url = params["url"]
        referer = params["referer"]
                
        req = urllib2.Request(server_url)
        req.add_header("Referer",referer)
        response = urllib2.urlopen(req)
        response = response.read().decode("utf-8").encode("utf-8")
        url = re.search('file: "(.+?)"', response).group(1)
    
        return url
    except:
        return ""