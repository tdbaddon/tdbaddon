# -*- coding: utf-8 -*-

import xbmcaddon
import time
import json
import md5
import base64
import urllib
import urllib2
import StringIO
import gzip
import random



def parse_veetle(params):
    try:
        params = json.loads(params)
        server_url = params["url"]
        channel_id = params["channelId"]
        
        req = urllib2.Request(server_url)
        response = urllib2.urlopen(req)
        if response.info().get('Content-Encoding') == 'gzip':
            buf = StringIO.StringIO(response.read())
            gzip_f = gzip.GzipFile(fileobj=buf)
            response = gzip_f
        
        response = response.read().decode("utf-8").encode("utf-8")            
        
        response = json.loads(response)
        
        for item in response["payload"]:
            if item["channelId"] == channel_id:
                url = "http://veetle.com/index.php/stream/ajaxStreamLocation/" + channel_id + "_" + item["sessionId"] + "/flash"
                req = urllib2.Request(url)
                response = urllib2.urlopen(req)
                response = response.read()
                response = json.loads(response)
                url = response["payload"]
                return url

        return ""
    except KeyError:
        return ""
