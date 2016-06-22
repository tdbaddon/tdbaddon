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

import urllib, urllib2, re, cookielib, os, sys, socket
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

import utils


def Main():
    List('https://www.myfreecams.com/mfc2/php/online_models_splash.php')


def List(url):
    listhtml = utils.getHtml2(url)
    match = re.compile("model_detail=(.*?)&.*?img src=(.*?)jpg.*?</div>", re.DOTALL | re.IGNORECASE).findall(listhtml)
    for name, img in match:
        name = utils.cleantext(name)
        img = img + 'jpg'
        url = img[32:-17]
        if len(url) == 7:
            url = '10' + url
        else:
            url = '1' + url
        utils.addDownLink(name, url, 272, img, '', noDownload=True)
    xbmcplugin.endOfDirectory(utils.addon_handle)
    

def findurl(url, name):
    dp = xbmcgui.DialogProgress()
    dp.create("Searching webcamlink","Searching webcamlink for:",name)
    count = 0
    for videoid in range(492, 438, -1): #54
        dp.update(int(count))
        videotest = ''
        testurl = 'http://video%s.myfreecams.com:1935/NxServer/mfc_%s.f4v_aac/playlist.m3u8' % (videoid, url)
        try: videotest = urllib2.urlopen(testurl, timeout=3)
        except: pass
        if videotest:
            dp.update(100)
            dp.close()        
            return testurl
        count = count + 0.7
        if dp.iscanceled():
            dp.close()
            break
    for videoid in range(419, 404, -1): #15
        dp.update(int(count))
        videotest = ''
        testurl = 'http://video%s.myfreecams.com:1935/NxServer/mfc_%s.f4v_aac/playlist.m3u8' % (videoid, url)
        try: videotest = urllib2.urlopen(testurl, timeout=3)
        except: pass
        if videotest:
            dp.update(100)
            dp.close()        
            return testurl
        count = count + 0.7
        if dp.iscanceled():
            dp.close()
            break
    for videoid in range(371, 340, -1): #31
        dp.update(int(count))
        videotest = ''
        testurl = 'http://video%s.myfreecams.com:1935/NxServer/mfc_%s.f4v_aac/playlist.m3u8' % (videoid, url)
        try: videotest = urllib2.urlopen(testurl, timeout=3)
        except: pass
        if videotest:
            dp.update(100)
            dp.close()        
            return testurl
        count = count + 0.7
        if dp.iscanceled():
            dp.close()
            break            
    for videoid in range(627, 600, -1): #27
        dp.update(int(count))
        videotest = ''
        testurl = 'http://video%s.myfreecams.com:1935/NxServer/mfc_%s.f4v_aac/playlist.m3u8' % (videoid, url)
        try: videotest = urllib2.urlopen(testurl, timeout=3)
        except: pass
        if videotest:
            dp.update(100)
            dp.close()        
            return testurl
        count = count + 0.7
        if dp.iscanceled():
            dp.close()
            break            
    return ''


def Playvid(url, name):
    testurl = findurl(url, name)
    if testurl.startswith('http'):
        videourl = testurl
        iconimage = xbmc.getInfoImage("ListItem.Thumb")
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})
        listitem.setProperty("IsPlayable","true")
        if int(sys.argv[1]) == -1:
            pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
            pl.clear()
            pl.add(videourl, listitem)
            xbmc.Player().play(pl)
        else:
            listitem.setPath(str(videourl))
            xbmcplugin.setResolvedUrl(utils.addon_handle, True, listitem)
    else:
        utils.notify('Oh oh','Couldn\'t find a playable webcam link')

