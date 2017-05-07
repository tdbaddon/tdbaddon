import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcvfs,os,sys,datetime,string,hashlib,net
from resources.lib.modules.plugintools import *
import xbmcaddon
import json
from cookielib import CookieJar
from resources.lib.modules.common import *

def	vod_quest():
    link = open_url('http://www.questtv.co.uk/video/')
    link = link
    
    matches = plugintools.find_multiple_matches(link,'<div class="dni-video-playlist-thumb-box.*?">(.*?)</div>')
    
    for entry in matches:
       
        name      = plugintools.find_single_match(entry,'<h3 data-content="(.+?)">')
        uvid      = plugintools.find_single_match(entry,'data-videoid="(.+?)"')
        url       = 'http://c.brightcove.com/services/mobile/streaming/index/master.m3u8?videoId='+uvid
        iconimage = plugintools.find_single_match(entry,'<img src="(.+?)"')
		
        addLink(name,url,1,iconimage)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
        xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
