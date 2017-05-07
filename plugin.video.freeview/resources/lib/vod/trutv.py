import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcvfs,os,sys,datetime,string,hashlib,net
from resources.lib.modules.plugintools import *
import xbmcaddon
import json
from cookielib import CookieJar
from resources.lib.modules.common import *

def	vod_trutv():
    response = open_url('http://www.trutv.co.uk/catch-up/json_data')
    link     = json.loads(response)
    data     = link['Video']
    for field in data:
        name      = field['title']
        desc      = field['description']
        series    = field['metadata']['Series']
        episode   = field['metadata']['EpisodeNum']
        uvid      = field['uvid']
        iconimage = field['image_w640']
		
        url = 'https://d2q1b32gh59m9o.cloudfront.net/player/config?callback=ssmp&client=trutv&type=vod&apiKey=0Vc6De4Fo5He2Qt2Ez7Sp8Qg5Uu4Sv&videoId=%s&format=jsonp' % str(uvid)
        
        addVOD(name+' (Series '+series+', Episode '+episode+')',url,4,iconimage,desc)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
        xbmcplugin.setContent(int(sys.argv[1]), 'episodes')