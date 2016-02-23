'''
    Ultimate Whitecream
    Copyright (C) 2015 mortael

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
'''

import urllib, urllib2, re, cookielib, os.path, sys, socket
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

import utils

# 100 NLTUBES
# 101 NLVIDEOLIST
# 102 NLPLAYVID
# 103 NLCAT
# 104 NLSEARCH


sitelist = ['http://www.poldertube.nl', 'http://www.milf.nl', 'http://www.sextube.nl']



def NLTUBES(url, site):
    siteurl = sitelist[site]
    utils.addDir('[COLOR hotpink]Categories[/COLOR]', siteurl + '/categorieen',103,'', site)
    if site == 0:
        utils.addDir('[COLOR hotpink]Search[/COLOR]', siteurl + '/pornofilms/zoeken/',104,'', site)
    else:
        utils.addDir('[COLOR hotpink]Search[/COLOR]', siteurl + '/videos/zoeken/',104,'', site)
    NLVIDEOLIST(url, site)


def NLVIDEOLIST(url, site):
    siteurl = sitelist[site]
    link = utils.getHtml(url, '')
    match = re.compile(r'<article([^>]*)>.*?href="([^"]+)".*?src="([^"]+)".*?<h3>([^<]+)<.*?duration">[^\d]+([^\s<]+)(?:\s|<)', re.DOTALL | re.IGNORECASE).findall(link)
    for hd, url, img, name, duration in match:
        if len(hd) > 2:
            hd = " [COLOR orange]HD[/COLOR] "
        else:
            hd = " "    
        videourl = siteurl + url
        duration2 = "[COLOR deeppink]" +  duration + "[/COLOR]"
        utils.addDownLink(name + hd + duration2, videourl, 102, img, '')
    try:
        nextp=re.compile('<a href="([^"]+)" title="volg', re.DOTALL | re.IGNORECASE).findall(link)
        nextp = siteurl + nextp[0]
        utils.addDir('Next Page', nextp,101,'',site)
    except: pass
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def NLPLAYVID(url,name, download=None):
    videopage = utils.getHtml(url, '')
    videourl = re.compile('<source src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(videopage)
    videourl = videourl[0]
    if download == 1:
        utils.downloadVideo(videourl, name)
    else:    
        iconimage = xbmc.getInfoImage("ListItem.Thumb")
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})
        xbmc.Player().play(videourl, listitem)


def NLSEARCH(url, site, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 104)
    else:
        title = keyword.replace(' ','%20')
        searchUrl = searchUrl + title
        print "Searching URL: " + searchUrl
        NLVIDEOLIST(searchUrl, site)


def NLCAT(url, site):
    siteurl = sitelist[site]
    link = utils.getHtml(url, '')
    tags = re.compile('<div class="category".*?href="([^"]+)".*?<h2>([^<]+)<.*?src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(link)
    for caturl, catname, catimg in tags:
        catimg = siteurl + catimg
        utils.addDir(catname,caturl,101,catimg,site)
