'''
    Ultimate Whitecream
    Copyright (C) 2016 mortael
    Copyright (C) 2016 anton40
 
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
 
 
def Main():
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','http://xxxstreams.org/',423,'','')
    #utils.addDir('[COLOR hotpink]Search[/COLOR]','http://xxxstreams.org/?s=',424,'','')
    List('http://xxxstreams.org/page/1')
    xbmcplugin.endOfDirectory(utils.addon_handle)
 
 
def List(url):
    html = utils.getHtml(url, '')
    match = re.compile('<div class="entry-content">.*?<img src="([^"]+)".*?<a href="([^"]+)" class="more-link">.+?<span class="screen-reader-text">([^"]+)</span>', re.DOTALL | re.IGNORECASE).findall(html)
    for img, videopage, name in match:
        name = utils.cleantext(name)
        utils.addDownLink(name, videopage, 422, img, '')
    try:
        nextp = re.compile('<a class="next.*?href="(.+?)">', re.DOTALL | re.IGNORECASE).findall(html)
        utils.addDir('Next Page', nextp[0], 421,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)
 
 
def Playvid(url, name, download):
    url = url.split('#')[0]
    utils.PLAYVIDEO(url, name, download)
 
 
def Categories(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('<li.+?class=".+?menu-item-object-post_tag.+?"><a href="(.+?)">(.+?)</a></li>').findall(cathtml)
    for catpage, name in match:
        utils.addDir(name, catpage, 421, '')    
    xbmcplugin.endOfDirectory(utils.addon_handle)
 
#def Search(url, keyword=None):
#    searchUrl = url
#    if not keyword:
#        utils.searchDir(url, 414)
#    else:
#        title = keyword.replace(' ','+')
#        searchUrl = searchUrl + title
#        List(searchUrl)