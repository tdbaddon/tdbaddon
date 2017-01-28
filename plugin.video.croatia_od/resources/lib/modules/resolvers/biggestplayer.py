# -*- coding: utf-8 -*-

from resources.lib.modules import client,constants
import urllib
import re
from resources.lib.modules.log_utils import log

def parse_biggestplayer(params):
    try:
        url = params["url"]
        ref = url
        referer = params["referer"]
                
        html = client.request(url,referer=referer)
        url = re.search('file: "(.+?)"', html).group(1)
        url += '|%s' %urllib.urlencode({'User-agent':client.agent(),'Referer':ref,'X-Requested-With':constants.get_shockwave()})
        return url
    except:
        return ""