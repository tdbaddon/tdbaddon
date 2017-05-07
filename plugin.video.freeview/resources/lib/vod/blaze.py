import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcvfs,os,sys,datetime,string,hashlib,net
from resources.lib.modules.plugintools import *
import xbmcaddon
import json
from cookielib import CookieJar
from resources.lib.modules.common import *

def	vod_blaze():
    url   = 'http://www.blaze.tv/catchup?page='
    link  = open_url(url+'0')
    link += open_url(url+'1')
    link += open_url(url+'2')
    link += open_url(url+'3')
    link += open_url(url+'4')
    link += open_url(url+'5')
    link += open_url(url+'6')
    link += open_url(url+'7')
    link += open_url(url+'8')
    link += open_url(url+'9')
    link += open_url(url+'10')
    link += open_url(url+'11')
    link += open_url(url+'12')
    link += open_url(url+'13')
    link += open_url(url+'14')
    link += open_url(url+'15')
    link += open_url(url+'16')
    link += open_url(url+'17')
    link += open_url(url+'18')
    link += open_url(url+'19')
    link += open_url(url+'20')
    link += open_url(url+'21')
    link += open_url(url+'22')
    link += open_url(url+'23')
    link += open_url(url+'24')
    link += open_url(url+'25')
    link += open_url(url+'26')
    link += open_url(url+'27')
    link += open_url(url+'28')
    link += open_url(url+'29')
    link += open_url(url+'30')
    link += open_url(url+'31')
    link += open_url(url+'32')
    link += open_url(url+'33')
    link += open_url(url+'34')
    link += open_url(url+'35')
    link += open_url(url+'36')
    link += open_url(url+'37')
    link += open_url(url+'38')
    link += open_url(url+'39')
    link += open_url(url+'40')
    link += open_url(url+'41')
    link += open_url(url+'42')
    link += open_url(url+'43')
    link += open_url(url+'44')
    link += open_url(url+'45')
    link += open_url(url+'46')
    link += open_url(url+'47')
    link += open_url(url+'48')
    link += open_url(url+'49')
    link += open_url(url+'50')
    link  = link
	
    matches = plugintools.find_multiple_matches(link,'<div class="item">(.*?)<div class="caption">')
    
    for entry in matches:
       
        name      = plugintools.find_single_match(entry,'data-episode="(.+?)"').replace('Series:','(Series ').replace(' Episode:',', Episode ')
        uvid      = plugintools.find_single_match(entry,'data-uvid="(.+?)"')
        url       = 'https://d2q1b32gh59m9o.cloudfront.net/player/config?callback=ssmp&client=blaze&type=vod&apiKey=0Vc6De4Fo5He2Qt2Ez7Sp8Qg5Uu4Sv&videoId='+uvid+'&format=jsonp'
        iconimage = plugintools.find_single_match(entry,'src="(.+?)"')
		
        addLink(name+')',url,4,iconimage)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
        xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
