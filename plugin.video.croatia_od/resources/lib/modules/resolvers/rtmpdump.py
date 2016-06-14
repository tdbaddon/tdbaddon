# -*- coding: utf-8 -*-

import json

def parse_rtmpdump(params):
    try:
        print repr(params)
        base_url = ""
        url_params = ""
        
        for key in params:
            if (key == "rtmp"):
                base_url = params[key]
            else:
                if params[key]:
                    url_params = url_params + " " + key + "=" + params[key]
                
        print "rtmpdump url: " + base_url + " " + url_params
        return base_url + url_params
    except KeyError:
        return ""