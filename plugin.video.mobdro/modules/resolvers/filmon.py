# -*- coding: utf-8 -*-

import json
import plugintools
import urllib
import urllib2
import re

def parse_filmon(params):
    try:
        session_url = "http://www.filmon.com/api/init?&app_android_test=false&channelProvider=ipad&app_version=2.0.12&app_android_device_tablet=false&app_android_device_manufacturer=SAMSUNG&app_secret=wis9Ohmu7i&app_id=android-native&app_android_api_version=15&b=12&f=norefer"
        req = urllib2.Request(session_url)
        req.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36")
        response = urllib2.urlopen(req)
        response = response.read().decode("utf-8").encode("utf-8")
        
        response = json.loads(response.encode("utf-8").decode("string_escape"))
        url = "http://www.filmon.com/tv/api/channel/" + params + "?session_key=" + response["session_key"] 
        req = urllib2.Request(url)
        req.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36")
        response = urllib2.urlopen(req)
        response = response.read().decode("utf-8").encode("utf-8")
        try:
            response = json.loads(response.encode("utf-8").decode("string_escape"))
        except:
            response = json.loads(response)
            
        stream_url = ""
    
        for stream in response["streams"]:
            print "url: " + stream["url"]
            stream_url = stream["url"]
            if stream["name"] == "HD":
                break
        print "stream_url: " + stream_url
        return stream_url
    except:
        return ""
