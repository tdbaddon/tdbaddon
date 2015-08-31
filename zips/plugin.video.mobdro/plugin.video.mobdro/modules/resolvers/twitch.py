# -*- coding: utf-8 -*-

import json
import urllib
import urllib2

def parse_twitch(params):
    try:
        req = urllib2.Request("http://api.twitch.tv/api/channels/" + params + "/access_token")       
        response = urllib2.urlopen(req)
        response = response.read().decode("utf-8").encode("utf-8")
        response = json.loads(response) 
        token = urllib.quote(response["token"])
        sig = response["sig"]
        
        return "http://usher.justin.tv/api/channel/hls/" + params + ".m3u8?token=" + token + "&sig=" + sig
    except:
        pass