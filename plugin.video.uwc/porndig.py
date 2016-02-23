'''
    Ultimate Whitecream
    Copyright (C) 2016 mortael

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

from StringIO import StringIO
import gzip

addon = utils.addon

USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

headers = {'User-Agent': USER_AGENT,
           'X-Requested-With': 'XMLHttpRequest',
           'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
           'Accept': '*/*',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'en-US,en;q=0.8,nl;q=0.6',
           'Connection': 'keep-alive'}

pdreferer = 'http://www.porndig.com/videos/'

def Main(name):
    if 'Amateurs' in name:
        addon.setSetting('pdsection', '1')
    else:
        addon.setSetting('pdsection', '0')
    utils.addDir('[COLOR hotpink]Categories[/COLOR]', 'http://www.porndig.com/videos/', 293, '', '')
    if addon.getSetting("pdsection") == '0':
        utils.addDir('[COLOR hotpink]Studios[/COLOR]', 'http://www.porndig.com/studios/load_more_studios', 294, '', 0)
        utils.addDir('[COLOR hotpink]Pornstars[/COLOR]', 'http://www.porndig.com/pornstars/load_more_pornstars', 295, '', 0)
    List(0, '', 0)


def Categories(caturl):
    if addon.getSetting("pdsection") == '1':
        caturl = 'http://www.porndig.com/amateur/videos/'
    urldata = utils.getHtml(caturl, pdreferer, headers, data='')
    urldata = re.compile(
        '<select name="filter_1" class="js_loader_category_select js_category_select filter_select_item">(.*?)</select>',
        re.DOTALL | re.IGNORECASE).findall(urldata)
    reobj = re.compile(r'value="(\d+)"[^>]*?>([^<]+)<', re.DOTALL | re.IGNORECASE).findall(urldata[0])
    for catchannel, catname in reobj:
        utils.addDir(catname, '', 291, '', 0, catchannel, 3)
    xbmcplugin.endOfDirectory(utils.addon_handle)


def VideoListData(page, channel):
    sort = 'date'
    offset = page * 100
    if addon.getSetting("pdsection") == '1':
        catid = 4
    else:
        catid = 1
    values = {'main_category_id': catid,
              'type': 'post',
              'name': 'category_videos',
              'filters[filter_type]': sort,
              'filters[filter_period]': '',
              'offset': offset}
    return urllib.urlencode(values)
    
def CatListData(page, channel):
    sort = 'date'
    offset = page * 100
    if addon.getSetting("pdsection") == '1':
        catid = 4
    else:
        catid = 1    
    values = {'main_category_id': catid,
              'type': 'post',
              'name': 'category_videos',
              'filters[filter_type]': sort,
              'filters[filter_period]': '',
              'offset': offset,
              'category_id[]': channel}
    return urllib.urlencode(values)

def VideoListStudio(page, channel):
    sort = 'date'
    offset = page * 65
    values = {'main_category_id': '1',
              'type': 'post',
              'name': 'studio_related_videos',
              'filters[filter_type]': sort,
              'filters[filter_period]': '',
              'offset': offset,
              'content_id': channel}
    return urllib.urlencode(values)

def VideoListPornstar(page, channel):
    sort = 'date'
    offset = page * 65
    values = {'main_category_id': '1',
              'type': 'post',
              'name': 'pornstar_related_videos',
              'filters[filter_type]': sort,
              'filters[filter_period]': '',
              'offset': offset,
              'content_id': channel}
    return urllib.urlencode(values)

def StudioListData(page):
    offset = page * 60
    values = {'main_category_id': '1',
              'type': 'studio',
              'name': 'top_studios',
              'filters[filter_type]': 'likes',
              'starting_letter': '',
              'offset': offset}
    return urllib.urlencode(values)

def PornstarListData(page):
    offset = page * 60
    values = {'main_category_id': '1',
              'type': 'pornstar',
              'name': 'top_pornstars',
              'filters[filter_type]': 'likes',
              'country_code': '',
              'starting_letter': '',
              'offset': offset}
    return urllib.urlencode(values)


def Pornstars(url, page):
    data = PornstarListData(page)
    urldata = utils.getHtml(url, pdreferer, headers, data=data)
    urldata = ParseJson(urldata)
    i = 0
    match = re.compile(r'pornstar_([\d]+).*?alt="([^"]+)".*?Videos</div> <div class="value">([\d]+)',
                       re.DOTALL | re.IGNORECASE).findall(urldata)
    for ID, studio, videos in match:
        title = studio + " Videos: [COLOR deeppink]" + videos + "[/COLOR]"
        img = "http://static2.porndig.com/media/default/pornstars/pornstar_" + ID + ".jpg"
        utils.addDir(title, '', 291, img, '', ID, 2)
        i += 1
    if i >= 60:
        page += 1
        utils.addDir('Page ' + str(page), url, 295, '', page)
    xbmcplugin.endOfDirectory(utils.addon_handle)


def Studios(url, page):
    data = StudioListData(page)
    urldata = utils.getHtml(url, pdreferer, headers, data=data)
    urldata = ParseJson(urldata)
    i = 0
    match = re.compile(r'studio_([\d]+).*?alt="([^"]+)".*?Videos</div> <div class="value">([\d]+)',
                       re.DOTALL | re.IGNORECASE).findall(urldata)
    for ID, studio, videos in match:
        title = studio + " Videos: [COLOR deeppink]" + videos + "[/COLOR]"
        img = "http://static2.porndig.com/media/default/studios/studio_" + ID + ".jpg"
        utils.addDir(title, '', 291, img, '', ID, 1)
        i += 1
    if i >= 60:
        page += 1
        utils.addDir('Page ' + str(page), url, 294, '', page)
    xbmcplugin.endOfDirectory(utils.addon_handle)


def List(page, channel, section):
    if section == 0:
        data = VideoListData(page, channel)
        maxresult = 100
    elif section == 1:
        data = VideoListStudio(page, channel)
        maxresult = 65
    elif section == 2:
        data = VideoListPornstar(page, channel)
        maxresult = 65
    elif section == 3:
        data = CatListData(page, channel)
        maxresult = 100
    urldata = utils.getHtml("http://www.porndig.com/posts/load_more_posts", pdreferer, headers, data=data)
    urldata = ParseJson(urldata)
    i = 0
    match = re.compile(
        r'<a.*?href="([^"]+)" title="([^"]+)">.*?</h2>(.*?)</div>.?<img src="([^"]+)".*?>.*?<span class="pull-left">(\d[^\s<]+)',
        re.DOTALL | re.IGNORECASE).findall(urldata)
    for url, name, hd, img, duration in match:
        if len(hd) > 2:
            if hd.find('full') > 0:
                hd = " [COLOR yellow]FULLHD[/COLOR] "
            else:
                hd = " [COLOR orange]HD[/COLOR] "
        else:
            hd = " "
        url = "http://www.porndig.com" + url
        name = name + hd + "[COLOR deeppink]" + duration + "[/COLOR]"
        utils.addDownLink(name, url, 292, img, '')
        i += 1
    if i >= maxresult:
        page += 1
        name = 'Page ' + str(page)
        utils.addDir(name, '', 291, '', page, channel, section)
    xbmcplugin.endOfDirectory(utils.addon_handle)


def Playvid(url, name, download=None):
    videopage = utils.getHtml(url, pdreferer, headers, data='')
    links = re.compile('<a href="([^"]+)" class="post_download_link clearfix">[^>]+>.*?(\d+p).*?<',
                       re.DOTALL | re.IGNORECASE).findall(videopage)
    videourl = getVideoUrl(links)
    videourl = utils.getVideoLink(videourl, url)
    if download == 1:
        utils.downloadVideo(videourl, name)
    else:
        iconimage = xbmc.getInfoImage("ListItem.Thumb")
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})
        xbmc.Player().play(videourl, listitem)


def getVideoUrl(testquality):
    print testquality
    p240 = findx('240p', testquality)
    p360 = findx('360p', testquality)
    p270 = findx('270p', testquality)
    p480 = findx('480p', testquality)
    p540 = findx('540p', testquality)
    p720 = findx('720p', testquality)
    p1080 = findx('1080p', testquality)

    if p240 is not None:
        try: testurl = testquality[p240[0]][0]
        except: pass
    if p270 is not None:
        try: testurl = testquality[p270[0]][0]
        except: pass
    if p360 is not None:
        try: testurl = testquality[p360[0]][0]
        except: pass
    if p480 is not None:
        try: testurl = testquality[p480[0]][0]
        except: pass
    if p540 is not None:
        try: testurl = testquality[p540[0]][0]
        except: pass
    if p720 is not None:
        try: testurl = testquality[p720[0]][0]
        except: pass
    if p1080 is not None:
        try: testurl = testquality[p1080[0]][0]
        except: pass
    return testurl


def findx(needle, haystack):
    if needle == haystack: return []
    # Strings are iterable, too
    if isinstance(haystack, str) and len(haystack) <= 1: return None
    try:
        for i, e in enumerate(haystack):
            r = findx(needle, e)
            if r is not None:
                r.insert(0, i)
                return r
    except TypeError:
        pass
    return None


def ParseJson(urldata):
    urldata = re.sub(r"(?si)\\/", "/", urldata)
    urldata = re.sub(r'(?si)\\"', '"', urldata)
    urldata = re.sub(r"(?si)\\t", " ", urldata)
    urldata = re.sub(r"(?si)\\n", " ", urldata)
    urldata = re.sub(r"(?si)\s{2,}", " ", urldata)
    return urldata