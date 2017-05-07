import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcvfs,os,sys,datetime,string,hashlib,net
from resources.lib.modules.plugintools import *
import xbmcaddon
import json
from cookielib import CookieJar
from resources.lib.modules.common import *

def	vod_uktv(url):
    link = open_url(url)
    link = link
    
    matches = plugintools.find_multiple_matches(link,'<div class="span2">(.*?)</div>')
    
    for entry in matches:
       
        name       = plugintools.find_single_match(entry,'alt="(.+?)"')
        url        = plugintools.find_single_match(entry,'<a href="(.+?)"').replace('/shows/','http://uktvplay.uktv.co.uk/shows/')
        iconimage2 = plugintools.find_single_match(entry,'<img data-url="https://res.cloudinary.com/uktv/image/upload/t_XX/(.+?)"').encode("utf-8")
        iconimage  = 'https://res.cloudinary.com/uktv/image/upload/b_rgb:000000,w_235,c_fill,q_90,h_132/'+iconimage2
		
        addDir(name,url,11,iconimage)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
        xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
		
def	vod_uktvEp(url):
    link  = open_url(url)
    link  = link
    dupes = []
    
    matches  = plugintools.find_multiple_matches(link,'<div class="spanOneThird vod-episode clearfix(.*?)icon-healthy icon')
    featured = plugintools.find_multiple_matches(link,'<div id="vod-container"(.*?)<div class="spanOneThird ep-actions-box">')
    
    for entry in matches:
        try:
            name       = plugintools.find_single_match(entry,'data-title="(.+?)"').replace("&#39;","'")
            desc       = plugintools.find_single_match(entry,'data-teaser="(.+?)"')
            season     = plugintools.find_single_match(entry,'data-series="(.+?)"')
            episode    = plugintools.find_single_match(entry,'data-episode="(.+?)"')
            uvid       = plugintools.find_single_match(entry,'data-vidid="(.+?)"')
            if uvid in dupes: raise Exception()
            dupes.append(uvid)
            url        = 'http://c.brightcove.com/services/mobile/streaming/index/master.m3u8?videoId='+uvid
            iconimage2 = plugintools.find_single_match(entry,'<img data-url="https://res.cloudinary.com/uktv/image/upload/t_XX/(.+?)"').encode("utf-8")
            iconimage  = 'https://res.cloudinary.com/uktv/image/upload/b_rgb:000000,w_235,c_fill,q_90,h_132/'+iconimage2
    		
            addVOD(name+' (Series '+season+', Episode '+episode+')',url,1,iconimage,desc)
        except:
            pass
			
    for entry in featured:
        try:
            name       = plugintools.find_single_match(entry,'data-brand="(.+?)"').replace("&#39;","'")
            desc       = plugintools.find_single_match(entry,'<p class="teaser">(.+?)</p>')
            season     = plugintools.find_single_match(entry,'data-series="(.+?)"')
            episode    = plugintools.find_single_match(entry,'data-episode="(.+?)"')
            uvid       = plugintools.find_single_match(entry,'data-vidid="(.+?)"')
            if uvid in dupes: raise Exception()
            dupes.append(uvid)
            url        = 'http://c.brightcove.com/services/mobile/streaming/index/master.m3u8?videoId='+uvid
            iconimage2 = plugintools.find_single_match(entry,'<img data-url="https://res.cloudinary.com/uktv/image/upload/t_XX/(.+?)"').encode("utf-8")
            iconimage  = 'https://res.cloudinary.com/uktv/image/upload/b_rgb:000000,w_235,c_fill,q_90,h_132/'+iconimage2

            addVOD(name+' (Series '+season+', Episode '+episode+')',url,1,iconimage,desc)
        except:
            pass

    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.setContent(int(sys.argv[1]), 'episodes')