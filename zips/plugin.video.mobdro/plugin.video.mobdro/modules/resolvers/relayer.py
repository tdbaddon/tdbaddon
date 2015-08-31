# -*- coding: utf-8 -*-

import time
import json
import md5
import base64
import plugintools

def parse_relayer(params):
    try:
        params = json.loads(params)
        server = params["server"]
        playpath = params["playpath"]
        print "playpath: " + playpath
        password = params["password"]
        dir = params["dir"]
        expiration_time = params["expiration_time"]
        millis = int(round(time.time() * 1000))
        l = millis / 1000L + expiration_time
        
        arr = [password, l, dir, playpath]
        url = "%s%d/%s/%s"
        url = url % tuple(arr)
        url_md5 = md5.new(url).digest()
        url_base64 = base64.b64encode(url_md5)
        url_base64 = url_base64.replace("+", "-").replace("/", "_").replace("=", "")
        arr = [server, url_base64, l, playpath]
        url = "http://%s/live/%s/%d/%s"
        url = url % tuple(arr)
        return url
    except KeyError:
        return ""