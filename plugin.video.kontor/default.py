#!/usr/bin/python
# -*- coding: latin-1 -*-

"""
    This ia part of the xbmc addon Kontor by pcd@xtrend-alliance.com
    Copyright (C) 2015

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import xbmc,xbmcplugin
import xbmcgui
import sys
import urllib, urllib2
import time
import re
from htmlentitydefs import name2codepoint as n2cp
import httplib
import urlparse
from os import path, system
import socket
from urllib2 import Request, URLError, urlopen
from urlparse import parse_qs
from urllib import unquote_plus



thisPlugin = int(sys.argv[1])
addonId = "plugin.video.kontor"
dataPath = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
if not path.exists(dataPath):
       cmd = "mkdir -p " + dataPath
       system(cmd)
       
Host = "https://www.youtube.com/user/kontor/videos"

def getUrl(url):
        print "Here in getUrl url =", url
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link
	

#Host = "https://www.youtube.com/results?search_query=wwe+total+divas&page=3"
	
def showContent():
        names = []
        urls = []
        names.append("Kontor Videos")
        urls.append("https://www.youtube.com/user/kontor/videos")
        
        names.append("Kontor Heavy Rotation")
        urls.append("https://www.youtube.com/playlist?list=PLF7B92F492FDAE703")
        
#        names.append("Kontor Minimix")
#        urls.append("https://www.youtube.com/playlist?list=PLB9EFACD406B8B81E")
        
#        names.append("Kontor Festival")
#        urls.append("https://www.youtube.com/playlist?list=PLD1bKrYdYW5fIjIpF1QvDJ9ltgS3gb_IZ")
        
        i1 = 0           
        for name in names:
                        url1 = urls[i1]
                        pic = " "
                        #print "Here in Showcontent url1 =", url1
                        addDirectoryItem(name, {"name":name, "url":url1, "mode":2}, pic)
                        i1 = i1+1
        xbmcplugin.endOfDirectory(thisPlugin)

def getPage(name, urlmain):
                pages = [1, 2, 3, 4, 5, 6]

                for page in pages:
                        url = urlmain + "&page=" + str(page)
                        name = "Page " + str(page)
                        pic = " "
                        addDirectoryItem(name, {"name":name, "url":url, "mode":2}, pic)
                xbmcplugin.endOfDirectory(thisPlugin)

def getVideos(name1, urlmain):
	content = getUrl(urlmain)
	print "content B =", content
	if "playlist" in urlmain: 
	         regexvideo = '<tr class="pl-video yt-uix-.*?data-title="(.*?)".*?href="(.*?)".*?data-thumb="(.*?)"'
	else:	
	         regexvideo = 'span class="yt-thumb-default">.*?src="(.*?)".*?yt-ui-ellipsis-2" dir="ltr" title="(.*?)".*?href="(.*?)"'
	match = re.compile(regexvideo,re.DOTALL).findall(content)
        print "match =", match
        if "playlist" in urlmain:
            for name, url, pic in match:
                 name = name.replace('\|', '-')
                 name = name.replace('"', '')
                 name = name.replace('*', '')
                 url1 = "https://www.youtube.com" + url
                 pic = "http:" + pic 
                 print "Here in getVideos url =", url
	         addDirectoryItem(name, {"name":name, "url":url1, "mode":3}, pic) 
        else:                
            for pic, name, url in match:
                 name = name.replace('\|', '-')
                 name = name.replace('"', '')
                 name = name.replace('*', '')
                 url1 = "https://www.youtube.com" + url
                 pic = "http:" + pic 
                 print "Here in getVideos url =", url
	         addDirectoryItem(name, {"name":name, "url":url1, "mode":3}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)	         
        
def getVideos2(name, url):
                f = open("/tmp/xbmc_search.txt", "r")
                icount = 0
                for line in f.readlines(): 
                    sline = line
                    icount = icount+1
                    if icount > 0:
                           break

                name = sline.replace(" ", "+")
                url1 = "http://xhamster.com/search.php?q=" + name + "&qcat=video" 
                pages = [1, 2, 3, 4, 5, 6]
                for page in pages:
                        url = url1 + "&page=" + str(page)
                        print "Here in getVideos2 url =", url
                        name = "Page " + str(page)
                        pic = " "
                        addDirectoryItem(name, {"name":name, "url":url, "mode":5}, pic)
                xbmcplugin.endOfDirectory(thisPlugin)


        		
def getVideos3(name, url):
        print "Here in getVideos3 url =", url
        content = getUrl(url)
	print "content B2 =", content

 	
	regexvideo = "><div class='video'><a href='(.*?)'.*?alt=(.*?)/>"
	match = re.compile(regexvideo,re.DOTALL).findall(content)
        #print "match =", match
        for url, name in match:
                 name = name.replace('"', '')
                 name = name.replace('*', '')
                 pic = " " 
	         addDirectoryItem(name, {"name":name, "url":url, "mode":3}, pic)

        xbmcplugin.endOfDirectory(thisPlugin)	

        
def getVideos4(name1, urlmain):
        n1 = urlmain.find(".html",0)
        if (n1 < 0):
                return
        n2 = urlmain.rfind("-", 0, n1)
        if (n2 < 0):
                return
        pn = "4"
        url1 = urlmain[:(n2+1)]
        url2 = urlmain[n1:]
        ##print "Here in getVideos2 url1 =", url1
        ##print "Here in getVideos2 url2 =", url2
        url = url1 + pn + url2
        ##print "Here in getVideos2 url =", url
        content = getUrl(url)
	##print "content B2 =", content
        pos0 = content.find("Promoted Videos", 0)
        if (pos0 < 0):
                return
	pos1 = content.find("<div class='video'", pos0)
        if (pos1 < 0):
                return
        content = content[pos1:]
	
	regexvideo = "><a href='(.*?)'.*?alt=(.*?)/>"
	match = re.compile(regexvideo,re.DOTALL).findall(content)
        ##print "match =", match
        for url, name in match:
                 name = name.replace('"', '')
                 pic = " " 
	         addDirectoryItem(name, {"name":name, "url":url, "mode":3}, pic)
	name = "More videos"
	addDirectoryItem(name, {"name":name, "url":urlmain, "mode":7}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)	

def getVideos5(name1, urlmain):
        n1 = urlmain.find(".html",0)
        if (n1 < 0):
                return
        n2 = urlmain.rfind("-", 0, n1)
        if (n2 < 0):
                return
        pn = "5"
        url1 = urlmain[:(n2+1)]
        url2 = urlmain[n1:]
        ##print "Here in getVideos2 url1 =", url1
        ##print "Here in getVideos2 url2 =", url2
        url = url1 + pn + url2
        ##print "Here in getVideos2 url =", url
        content = getUrl(url)
	##print "content B2 =", content
        pos0 = content.find("Promoted Videos", 0)
        if (pos0 < 0):
                return
	pos1 = content.find("<div class='video'", pos0)
        if (pos1 < 0):
                return
        content = content[pos1:]
	
	regexvideo = "><a href='(.*?)'.*?alt=(.*?)/>"
	match = re.compile(regexvideo,re.DOTALL).findall(content)
        ##print "match =", match
        for url, name in match:
                 name = name.replace('"', '')
                 pic = " " 
	         addDirectoryItem(name, {"name":name, "url":url, "mode":3}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)	

                
def playVideo(name, url):

        import YDStreamExtractor
        YDStreamExtractor.disableDASHVideo(True) #Kodi (XBMC) only plays the video for DASH streams, so you don't want these normally. Of course these are the only 1080p streams on YouTube
        
##        url = "https://www.youtube.com/watch?v=" + url #a youtube ID will work as well and of course you could pass the url of another site
        vid = YDStreamExtractor.getVideoInfo(url,quality=1) #quality is 0=SD, 1=720p, 2=1080p and is a maximum
        stream_url = vid.streamURL() #This is what Kodi (XBMC) will play
        print "stream_url =", stream_url
        img = " "
        listitem = xbmcgui.ListItem(name, iconImage=img, thumbnailImage=img)
        playfile = xbmc.Player()
        playfile.play(stream_url, listitem)

          

std_headers = {
	'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.6) Gecko/20100627 Firefox/3.6.6',
	'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en-us,en;q=0.5',
}  

def addDirectoryItem(name, parameters={},pic=""):
    li = xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=pic)
    url = sys.argv[0] + '?' + urllib.urlencode(parameters)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li, isFolder=True)


def parameters_string_to_dict(parameters):
    ''' Convert parameters encoded in a URL to a dict. '''
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict

params = parameters_string_to_dict(sys.argv[2])
name =  str(params.get("name", ""))
url =  str(params.get("url", ""))
url = urllib.unquote(url)
mode =  str(params.get("mode", ""))

if not sys.argv[2]:
	ok = showContent()
else:
	if mode == str(1):
		ok = getPage(name, url)
        elif mode == str(2):
		ok = getVideos(name, url)        	
	elif mode == str(3):
		ok = playVideo(name, url)	
	elif mode == str(4):
		ok = getVideos2(name, url)	
	elif mode == str(5):
		ok = getVideos3(name, url)
	elif mode == str(6):
		ok = getVideos4(name, url)
	elif mode == str(7):
		ok = getVideos5(name, url)
		



