# -*- coding: utf-8 -*-

import plugintools
import urllib
import urllib2
import re

def parse_vaughnlive(params):
    try:
        server_url = "http://mvn.vaughnsoft.net/video/edge/live_" + params
        plugintools.log("URL: " + server_url)
            
        req = urllib2.Request(server_url)
        req.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36")
        response = urllib2.urlopen(req)
        response = response.read().decode("utf-8").encode("utf-8")
        stream_hash = re.search('mvnkey-(.+)', response).group(1)

        server = re.search('(.+?);', response).group(1)
        rtmpUrl = "rtmp://%s/live App=live?%s Playpath=%s_%s  swfUrl=http://%s%s live=true pageUrl=http://%s/embed/video/%s?viewers=true&watermark=left&autoplay=true" % (server, stream_hash, "live", params, "vaughnlive.tv", "http://vaughnlive.tv/4319513358/swf/VaughnSoftPlayer.swf", "vaughnlive.tv", params)        

        return rtmpUrl
    except:
        return ""