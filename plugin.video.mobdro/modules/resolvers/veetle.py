# -*- coding: utf-8 -*-

import time
import json
import md5
import base64
import plugintools
import urllib
import urllib2
import StringIO
import gzip
import random

URL_AKAMAI_PROXY = 'http://127.0.0.1:64653/veetle/%s'

def parse_veetle(params):
    try:
        params = json.loads(params)
        server_url = params["url"]
        plugintools.log("URL: " + server_url)
        channel_id = params["channelId"]
        plugintools.log("CHANNEL ID: " + channel_id)
        
        req = urllib2.Request(server_url)
        response = urllib2.urlopen(req)
        if response.info().get('Content-Encoding') == 'gzip':
            buf = StringIO.StringIO(response.read())
            gzip_f = gzip.GzipFile(fileobj=buf)
            response = gzip_f
        
        response = response.read().decode("utf-8").encode("utf-8")            
        
        response = json.loads(response)
        
        for item in response["payload"]:
            print item["channelId"] + ", " + channel_id
            if item["channelId"] == channel_id:
                url = "http://veetle.com/index.php/stream/ajaxStreamLocation/" + channel_id + "_" + item["sessionId"] + "/flash"
                plugintools.log("PARSING: " + url)
                req = urllib2.Request(url)
                response = urllib2.urlopen(req)
                response = response.read()
                plugintools.log("RESPONSE: " + response)
                response = json.loads(response)
                url = response["payload"]
                url = base64.encodestring(url).replace('\n', '')
                if response["payload"]:
                    return URL_AKAMAI_PROXY % url
                return ""

        return ""
    except KeyError:
        return ""
