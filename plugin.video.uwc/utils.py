#-*- coding: utf-8 -*-

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

import urllib, urllib2, re, cookielib, os.path, sys, socket, time, tempfile, string
import xbmc, xbmcplugin, xbmcgui, xbmcaddon, sqlite3

from jsunpack import unpack

from StringIO import StringIO
import gzip

__scriptname__ = "Ultimate Whitecream"
__author__ = "mortael"
__scriptid__ = "plugin.video.uwc"
__credits__ = "mortael, Fr33m1nd, anton40"
__version__ = "1.0.95"

USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

headers = {'User-Agent': USER_AGENT,
           'Accept': '*/*',
           'Connection': 'keep-alive'}
           
openloadhdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}           

addon_handle = int(sys.argv[1])
addon = xbmcaddon.Addon(id=__scriptid__)

progress = xbmcgui.DialogProgress()
dialog = xbmcgui.Dialog()

rootDir = addon.getAddonInfo('path')
if rootDir[-1] == ';':
    rootDir = rootDir[0:-1]
rootDir = xbmc.translatePath(rootDir)
resDir = os.path.join(rootDir, 'resources')
imgDir = os.path.join(resDir, 'images')
streams = xbmc.translatePath(os.path.join(rootDir, 'streamlist.m3u'))
uwcicon = xbmc.translatePath(os.path.join(rootDir, 'icon.png'))

profileDir = addon.getAddonInfo('profile')
profileDir = xbmc.translatePath(profileDir).decode("utf-8")
cookiePath = os.path.join(profileDir, 'cookies.lwp')

if not os.path.exists(profileDir):
    os.makedirs(profileDir)

urlopen = urllib2.urlopen
cj = cookielib.LWPCookieJar()
Request = urllib2.Request

if cj != None:
    if os.path.isfile(xbmc.translatePath(cookiePath)):
        try:
            cj.load(xbmc.translatePath(cookiePath))
        except:
            try:
                os.remove(xbmc.translatePath(cookiePath))
                pass
            except:
                dialog.ok('Oh oh','The Cookie file is locked, please restart Kodi')
                pass
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
else:
    opener = urllib2.build_opener()

urllib2.install_opener(opener)

favoritesdb = os.path.join(profileDir, 'favorites.db')

class StopDownloading(Exception):
    def __init__(self, value): self.value = value 
    def __str__(self): return repr(self.value)

def downloadVideo(url, name):

    def _pbhook(numblocks, blocksize, filesize, url=None,dp=None):
        try:
            percent = min((numblocks*blocksize*100)/filesize, 100)
            currently_downloaded = float(numblocks) * blocksize / (1024 * 1024)
            kbps_speed = int((numblocks*blocksize) / (time.clock() - start))
            if kbps_speed > 0:
                eta = (filesize - numblocks * blocksize) / kbps_speed
            else:
                eta = 0
            kbps_speed = kbps_speed / 1024
            total = float(filesize) / (1024 * 1024)
            mbs = '%.02f MB of %.02f MB' % (currently_downloaded, total)
            e = 'Speed: %.02f Kb/s ' % kbps_speed
            e += 'ETA: %02d:%02d' % divmod(eta, 60) 
            dp.update(percent,'',mbs,e)
        except:
            percent = 100
            dp.update(percent)
        if dp.iscanceled():
            dp.close()
            raise StopDownloading('Stopped Downloading')
            
    def clean_filename(s):
        if not s:
            return ''
        badchars = '\\/:*?\"<>|\''
        for c in badchars:
            s = s.replace(c, '')
        return s;            

    download_path = addon.getSetting('download_path')
    if download_path == '':
        try:
            download_path = xbmcgui.Dialog().browse(0, "Download Path", 'myprograms', '', False, False)
            addon.setSetting(id='download_path', value=download_path)
            if not os.path.exists(download_path):
                os.mkdir(download_path)
        except:
            pass
    if download_path != '':
        dp = xbmcgui.DialogProgress()
        name = name.split("[")[0]
        dp.create("Ultimate Whitecream Download",name[:50])
        tmp_file = tempfile.mktemp(dir=download_path, suffix=".mp4")
        tmp_file = xbmc.makeLegalFilename(tmp_file)        
        start = time.clock()
        try:
            urllib.urlretrieve(url,tmp_file,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
            vidfile = xbmc.makeLegalFilename(download_path + clean_filename(name) + ".mp4")
            try:
              os.rename(tmp_file, vidfile)
              return vidfile
            except:
              return tmp_file            
        except:
            while os.path.exists(tmp_file):
                try:
                    os.remove(tmp_file)
                    break
                except:
                    pass


def notify(header=None, msg='', duration=5000):
    if header is None: header = 'Ultimate Whitecream'
    builtin = "XBMC.Notification(%s,%s, %s, %s)" % (header, msg, duration, uwcicon)
    xbmc.executebuiltin(builtin)


def PLAYVIDEO(url, name, download=None):
    progress.create('Play video', 'Searching videofile.')
    progress.update( 10, "", "Loading video page", "" )
    videosource = getHtml(url, url)
    playvideo(videosource, name, download, url)


def playvideo(videosource, name, download=None, url=None):
    hosts = []
    if re.search('videomega\.tv/', videosource, re.DOTALL | re.IGNORECASE):
        hosts.append('VideoMega')
    if re.search('openload\.(?:co|io)?/', videosource, re.DOTALL | re.IGNORECASE):
        hosts.append('OpenLoad')
    if re.search('streamin\.to/', videosource, re.DOTALL | re.IGNORECASE):
        hosts.append('Streamin')          
    if re.search('flashx\.tv/', videosource, re.DOTALL | re.IGNORECASE):
        hosts.append('FlashX')
    if re.search('mega3x\.net/', videosource, re.DOTALL | re.IGNORECASE):
        hosts.append('Mega3X')
    if re.search('streamcloud\.eu/', videosource, re.DOTALL | re.IGNORECASE):
        hosts.append('StreamCloud')         
    if len(hosts) == 0:
        progress.close()
        notify('Oh oh','Couldn\'t find any video')
        return
    elif len(hosts) > 1:
        if addon.getSetting("dontask") == "true":
            vidhost = hosts[0]            
        else:
            vh = dialog.select('Videohost:', hosts)
            vidhost = hosts[vh]
    else:
        vidhost = hosts[0]
    
    if vidhost == 'VideoMega':
        progress.update( 40, "", "Loading videomegatv", "" )
        if re.search("videomega.tv/iframe.js", videosource, re.DOTALL | re.IGNORECASE):
            hashref = re.compile("""javascript["']>ref=['"]([^'"]+)""", re.DOTALL | re.IGNORECASE).findall(videosource)
        elif re.search("videomega.tv/iframe.php", videosource, re.DOTALL | re.IGNORECASE):
            hashref = re.compile(r"iframe\.php\?ref=([^&]+)&", re.DOTALL | re.IGNORECASE).findall(videosource)
        elif re.search("videomega.tv/view.php", videosource, re.DOTALL | re.IGNORECASE):
            hashref = re.compile(r'view\.php\?ref=([^"]+)', re.DOTALL | re.IGNORECASE).findall(videosource)
        elif re.search("videomega.tv/cdn.php", videosource, re.DOTALL | re.IGNORECASE):
            hashref = re.compile(r'cdn\.php\?ref=([^"]+)', re.DOTALL | re.IGNORECASE).findall(videosource)
        elif re.search("videomega.tv/\?ref=", videosource, re.DOTALL | re.IGNORECASE):
            hashref = re.compile(r'videomega.tv/\?ref=([^"]+)', re.DOTALL | re.IGNORECASE).findall(videosource)
        else:
            hashkey = re.compile("""hashkey=([^"']+)""", re.DOTALL | re.IGNORECASE).findall(videosource)
            if not hashkey:
                notify('Oh oh','Couldn\'t find playable videomega link')
                return
            if len(hashkey) > 1:
                i = 1
                hashlist = []
                for x in hashkey:
                    hashlist.append('Video ' + str(i))
                    i += 1
                vmvideo = dialog.select('Multiple videos found', hashlist)
                hashkey = hashkey[vmvideo]
            else: hashkey = hashkey[0]
            hashpage = getHtml('http://videomega.tv/validatehash.php?hashkey='+hashkey, url)
            hashref = re.compile('ref="([^"]+)', re.DOTALL | re.IGNORECASE).findall(hashpage)
        progress.update( 80, "", "Getting video file from Videomega", "" )
        vmhost = 'http://videomega.tv/view.php?ref=' + hashref[0]
        videopage = getHtml(vmhost, url)
        vmpacked = re.compile(r"(eval\(.*\))\s+</", re.DOTALL | re.IGNORECASE).findall(videopage)
        vmunpacked = unpack(vmpacked[0])
        videourl = re.compile('src",\s?"([^"]+)', re.DOTALL | re.IGNORECASE).findall(vmunpacked)
        videourl = videourl[0]
        videourl = videourl + '|Referer=' + vmhost + '&User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'
    elif vidhost == 'OpenLoad':
        progress.update( 40, "", "Loading Openload", "" )
        openloadurl = re.compile(r"//(?:www\.)?openload\.(?:co|io)?/(?:embed|f)/([0-9a-zA-Z-_]+)", re.DOTALL | re.IGNORECASE).findall(videosource)
        openloadlist = list(set(openloadurl))
        if len(openloadlist) > 1:
            i = 1
            hashlist = []
            for x in openloadlist:
                hashlist.append('Video ' + str(i))
                i += 1
            olvideo = dialog.select('Multiple videos found', hashlist)
            openloadurl = openloadlist[olvideo]
        else: openloadurl = openloadurl[0]
        
        openloadurl1 = 'http://openload.co/embed/%s/' % openloadurl

        try:
            openloadsrc = getHtml(openloadurl1, '', openloadhdr)
            progress.update( 80, "", "Getting video file from OpenLoad", "")
            videourl = decodeOpenLoad(openloadsrc)
        except:
            notify('Oh oh','Couldn\'t find playable OpenLoad link')
            return
    elif vidhost == 'Streamin':
        progress.update( 40, "", "Loading Streamin", "" )
        streaminurl = re.compile(r"//(?:www\.)?streamin\.to/(?:embed-)?([0-9a-zA-Z]+)", re.DOTALL | re.IGNORECASE).findall(videosource)
        streaminurl = 'http://streamin.to/embed-%s-670x400.html' % streaminurl[0]
        streaminsrc = getHtml2(streaminurl)
        videohash = re.compile('\?h=([^"]+)', re.DOTALL | re.IGNORECASE).findall(streaminsrc)
        videourl = re.compile('image: "(http://[^/]+/)', re.DOTALL | re.IGNORECASE).findall(streaminsrc)
        progress.update( 80, "", "Getting video file from Streamin", "" )
        videourl = videourl[0] + videohash[0] + "/v.mp4"
    elif vidhost == 'FlashX':
        progress.update( 40, "", "Loading FlashX", "" )
        flashxurl = re.compile(r"//(?:www\.)?flashx\.tv/(?:embed-)?([0-9a-zA-Z]+)", re.DOTALL | re.IGNORECASE).findall(videosource)
        flashxlist = list(set(flashxurl))
        if len(flashxlist) > 1:
            i = 1
            hashlist = []
            for x in flashxlist:
                hashlist.append('Video ' + str(i))
                i += 1
            fxvideo = dialog.select('Multiple videos found', hashlist)
            flashxurl = flashxlist[fxvideo]
        else: flashxurl = flashxurl[0]        
        flashxurl = 'http://flashx.tv/embed-%s-670x400.html' % flashxurl
        flashxsrc = getHtml2(flashxurl)
        progress.update( 60, "", "Grabbing video file", "" )
        flashxurl2 = re.compile('<a href="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(flashxsrc)
        flashxsrc2 = getHtml2(flashxurl2[0])
        progress.update( 70, "", "Grabbing video file", "" ) 
        flashxjs = re.compile("<script type='text/javascript'>([^<]+)</sc", re.DOTALL | re.IGNORECASE).findall(flashxsrc2)
        progress.update( 80, "", "Getting video file from FlashX", "" )
        try: flashxujs = unpack(flashxjs[0])
        except: flashxujs = flashxjs[0]
        videourl = re.compile(r'\[{\s?file:\s?"([^"]+)",', re.DOTALL | re.IGNORECASE).findall(flashxujs)
        videourl = videourl[0]
    elif vidhost == 'Mega3X':
        progress.update( 40, "", "Loading Mega3X", "" )
        mega3xurl = re.compile('src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(videosource)
        mega3xsrc = getHtml(mega3xurl[0],'', openloadhdr)
        mega3xjs = re.compile("<script[^>]+>(eval[^<]+)</sc", re.DOTALL | re.IGNORECASE).findall(mega3xsrc)
        progress.update( 80, "", "Getting video file from Mega3X", "" )
        mega3xujs = unpack(mega3xjs[0])
        videourl = re.compile('file:\s?"([^"]+mp4)"', re.DOTALL | re.IGNORECASE).findall(mega3xujs)
        videourl = videourl[0]  
    elif vidhost == 'StreamCloud':
        progress.update( 40, "", "Opening Streamcloud", "" )
        streamcloudurl = re.compile(r"//(?:www\.)?streamcloud\.eu?/([0-9a-zA-Z-_/.]+html)", re.DOTALL | re.IGNORECASE).findall(videosource)
        streamcloudlist = list(set(streamcloudurl))
        if len(streamcloudlist) > 1:
            i = 1
            hashlist = []
            for x in streamcloudlist:
                hashlist.append('Video ' + str(i))
                i += 1
            scvideo = dialog.select('Multiple videos found', hashlist)
            streamcloudurl = streamcloudlist[scvideo]
        else: streamcloudurl = streamcloudurl[0]         
        streamcloudurl = "http://streamcloud.eu/" + streamcloudurl
        progress.update( 50, "", "Getting Streamcloud page", "" )
        schtml = postHtml(streamcloudurl)
        form_values = {}
        match = re.compile('<input.*?name="(.*?)".*?value="(.*?)">', re.DOTALL | re.IGNORECASE).findall(schtml)
        for name, value in match:
            form_values[name] = value.replace("download1","download2")
        progress.update( 60, "", "Grabbing video file", "" )    
        newscpage = postHtml(streamcloudurl, form_data=form_values)
        videourl = re.compile('file: "(.+?)",', re.DOTALL | re.IGNORECASE).findall(newscpage)[0]  
    progress.close()
    playvid(videourl, name, download)


def playvid(videourl, name, download=None):
    if download == 1:
        downloadVideo(videourl, name)
    else:
        iconimage = xbmc.getInfoImage("ListItem.Thumb")
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})
        xbmc.Player().play(videourl, listitem)


def PlayStream(name, url):
    item = xbmcgui.ListItem(name, path = url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
    return


def getHtml(url, referer, hdr=None, NoCookie=None, data=None):
    if not hdr:
        req = Request(url, data, headers)
    else:
        req = Request(url, data, hdr)
    if len(referer) > 1:
        req.add_header('Referer', referer)
    if data:
        req.add_header('Content-Length', len(data))
    response = urlopen(req, timeout=60)
    if response.info().get('Content-Encoding') == 'gzip':
        buf = StringIO( response.read())
        f = gzip.GzipFile(fileobj=buf)
        data = f.read()
        f.close()
    else:
        data = response.read()    
    if not NoCookie:
        # Cope with problematic timestamp values on RPi on OpenElec 4.2.1
        try:
            cj.save(cookiePath)
        except: pass
    response.close()
    return data

    
def postHtml(url, form_data={}, headers={}, compression=True):
    _user_agent = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.1 ' + \
                  '(KHTML, like Gecko) Chrome/13.0.782.99 Safari/535.1'
    req = urllib2.Request(url)
    if form_data:
        form_data = urllib.urlencode(form_data)
        req = urllib2.Request(url, form_data)
    req.add_header('User-Agent', _user_agent)
    for k, v in headers.items():
        req.add_header(k, v)
    if compression:
        req.add_header('Accept-Encoding', 'gzip')
    response = urllib2.urlopen(req)
    data = response.read()
    cj.save(cookiePath)
    response.close()
    return data

    
def getHtml2(url):
    req = Request(url)
    response = urlopen(req, timeout=60)
    data = response.read()
    response.close()
    return data 

    
def getVideoLink(url, referer):
    req2 = Request(url, '', headers)
    req2.add_header('Referer', referer)
    url2 = urlopen(req2).geturl()
    return url2


def cleantext(text):
    text = text.replace('&#8211;','-')
    text = text.replace('&#038;','&')
    text = text.replace('&#8217;','\'')
    text = text.replace('&#8216;','\'')
    text = text.replace('&#8230;','...')
    text = text.replace('&quot;','"')
    text = text.replace('&#039;','`')
    text = text.replace('&amp;','&')
    text = text.replace('&ntilde;','ñ')
    return text


def addDownLink(name, url, mode, iconimage, desc, stream=None, fav='add'):
    if fav == 'add': favtext = "Add to"
    elif fav == 'del': favtext = "Remove from"
    u = (sys.argv[0] +
         "?url=" + urllib.quote_plus(url) +
         "&mode=" + str(mode) +
         "&name=" + urllib.quote_plus(name))
    dwnld = (sys.argv[0] +
         "?url=" + urllib.quote_plus(url) +
         "&mode=" + str(mode) +
         "&download=" + str(1) +
         "&name=" + urllib.quote_plus(name))
    favorite = (sys.argv[0] +
         "?url=" + urllib.quote_plus(url) +
         "&fav=" + fav +
         "&favmode=" + str(mode) +
         "&mode=" + str('900') +
         "&img=" + urllib.quote_plus(iconimage) +
         "&name=" + urllib.quote_plus(name))         
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setArt({'thumb': iconimage, 'icon': iconimage})
    if stream:
        liz.setProperty('IsPlayable', 'true')
    if len(desc) < 1:
        liz.setInfo(type="Video", infoLabels={"Title": name})
    else:
        liz.setInfo(type="Video", infoLabels={"Title": name, "plot": desc, "plotoutline": desc})
    liz.addContextMenuItems([('[COLOR hotpink]Download Video[/COLOR]', 'xbmc.RunPlugin('+dwnld+')'),
    ('[COLOR hotpink]' + favtext + ' favorites[/COLOR]', 'xbmc.RunPlugin('+favorite+')')])
    ok = xbmcplugin.addDirectoryItem(handle=addon_handle, url=u, listitem=liz, isFolder=False)
    return ok
    

def addDir(name, url, mode, iconimage, page=None, channel=None, section=None, keyword='', Folder=True):
    u = (sys.argv[0] +
         "?url=" + urllib.quote_plus(url) +
         "&mode=" + str(mode) +
         "&page=" + str(page) +
         "&channel=" + str(channel) +
         "&section=" + str(section) +
         "&keyword=" + urllib.quote_plus(keyword) +
         "&name=" + urllib.quote_plus(name))
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setArt({'thumb': iconimage, 'icon': iconimage})
    liz.setInfo(type="Video", infoLabels={"Title": name})
    ok = xbmcplugin.addDirectoryItem(handle=addon_handle, url=u, listitem=liz, isFolder=Folder)
    return ok
    
def _get_keyboard(default="", heading="", hidden=False):
    """ shows a keyboard and returns a value """
    keyboard = xbmc.Keyboard(default, heading, hidden)
    keyboard.doModal()
    if keyboard.isConfirmed():
        return unicode(keyboard.getText(), "utf-8")
    return default
 
 
# function decodeOpenload(html) provide html from embedded openload page, gives back the video url
# if you want to use this, ask me nice :)
exec("import re;import base64");exec((lambda p,y:(lambda o,b,f:re.sub(o,b,f))(r"([0-9a-f]+)",lambda m:p(m,y),base64.b64decode("NDIgNTAoMjMpOgoKCSMgNTAgMzggNDYgMjYsIDJjIDM3IDM5IDNkIDJmIDJlIDI5IDopCgkxNSA9IDQ3LmIoMjUiPDEyKD86LnxcMzIpKj88MTZcMzJbXj5dKj8+KCg/Oi58XDMyKSo/KTwvMTYiLCAyMywgNDcuNTEgfCA0Ny4zMCkuNTIoMSkKCgkxNSA9IDE1LjM2KCIxZCIsIiIpCgkxNSA9IDE1LjM2KCIoNDAgKyA0MCArIDRlKSIsICI5IikKCTE1ID0gMTUuMzYoIig0MCArIDQwKSIsIjgiKQoJMTUgPSAxNS4zNigiKDQwICsgKDFhXjMzXjFhKSkiLCI3IikKCTE1ID0gMTUuMzYoIigoMWFeMzNeMWEpICsoMWFeMzNeMWEpKSIsIjYiKQoJMTUgPSAxNS4zNigiKDQwICsgNGUpIiwiNSIpCgkxNSA9IDE1LjM2KCI0MCIsIjQiKQoJMTUgPSAxNS4zNigiKCgxYV4zM14xYSkgLSA0ZSkiLCIyIikKCTE1ID0gMTUuMzYoIigxYV4zM14xYSkiLCIzIikKCTE1ID0gMTUuMzYoIjRlIiwiMSIpCgkxNSA9IDE1LjM2KCIoKyErW10pIiwiMSIpCgkxNSA9IDE1LjM2KCIoY14zM14xYSkiLCIwIikKCTE1ID0gMTUuMzYoIigwKzApIiwiMCIpCgkxNSA9IDE1LjM2KCIxNCIsIlxcIikgIAoJMTUgPSAxNS4zNigiKDMgKzMgKzApIiwiNiIpCgkxNSA9IDE1LjM2KCIoMyAtIDEgKzApIiwiMiIpCgkxNSA9IDE1LjM2KCIoIStbXSshK1tdKSIsIjIiKQoJMTUgPSAxNS4zNigiKC1+LX4yKSIsIjQiKQoJMTUgPSAxNS4zNigiKC1+LX4xKSIsIjMiKQoJMTUgPSAxNS4zNigiKC1+MCkiLCIxIikKCTE1ID0gMTUuMzYoIigtfjEpIiwiMiIpCgkxNSA9IDE1LjM2KCIoLX4zKSIsIjQiKQoJMTUgPSAxNS4zNigiKDAtMCkiLCIwIikKCQoJMTggPSA0Ny5iKDI1IlxcXCsoW14oXSspIiwgMTUsIDQ3LjUxIHwgNDcuMzApLjUyKDEpCgkxOCA9ICJcXCsiKyAxOAoJMTggPSAxOC4zNigiKyIsIiIpCgkxOCA9IDE4LjM2KCIgIiwiIikKCQoJMTggPSAzMSgxOCkKCTE4ID0gMTguMzYoIlxcLyIsIi8iKQoJCgkzYSAnMTEnIDJhIDE4OgoJCTEwID0gNDcuNDgoMjUiMTFcKGFcKyhcZCspIiwgNDcuNTEgfCA0Ny4zMCkuM2UoMTgpWzBdCgkJMTAgPSAyMigxMCkKCQkyMCA9IDQ3LjQ4KDI1IihcKFxkW14pXStcKSkiLCA0Ny41MSB8IDQ3LjMwKS4zZSgxOCkKCQkyZiAxYyAyYSAyMDoKCQkJZiA9IDQ3LjQ4KDI1IihcZCspLChcZCspIiwgNDcuNTEgfCA0Ny4zMCkuM2UoMWMpCgkJCTFmID0gMTAgKyAyMihmWzBdWzBdKQoJCQkxZSA9IDIxKDIyKGZbMF1bMV0pLDFmKQoJCQkxOCA9IDE4LjM2KDFjLDFlKQoJCTE4ID0gMTguMzYoIisiLCIiKQoJCTE4ID0gMTguMzYoIlwiIiwiIikKCQk0OSA9IDQ3LmIoMjUiKDNiW15cfV0rKSIsIDE4LCA0Ny41MSB8IDQ3LjMwKS41MigxKQoJMjQ6CgkJNDkgPSA0Ny5iKDI1IjQ0XDMyPz1cMzI/XCJ8JyhbXlwiJ10rKSIsIDE4LCA0Ny41MSB8IDQ3LjMwKS41MigxKQoJCgkxOSA9ICIxNy4xMi4iICsgIjRiIiArICI0ZiIgKyAiYyIKCTJkID0gIjE3LjEyLiIgKyAiNGMiICsgIjFhIiArICIyNSIgKyAiNTMiICsgImEiICsgImUiICsgIjRhIgoJCgkzYSAxOSAyYSAzNS4xYignM2MnKToKCQk0ZCA9IDQ5CgkyNDoKCQk0ZCA9ICIzNDovLzQzLjI3LjNmLzMyLzEzLzJiLjQxPzQ1PTEiCgkyOCA0ZA==")))(lambda a,b:b[int("0x"+a.group(1),16)],"0|1|2|3|4|5|6|7|8|9|a|search|c|d|e|match1|base|toString|video|2ds5o61a22srpob|(ﾟДﾟ)[ﾟεﾟ]|aastring|script|plugin|decodestring|check1|o|getAddonInfo|repl|(ﾟДﾟ)[ﾟεﾟ]+(oﾟｰﾟo)+ ((c^_^o)-(c^_^o))+ (-~0)+ (ﾟДﾟ) ['c']+ (-~-~1)+|repl2|base2|match|base10toN|int|html|else|r|mortael|dropbox|return|credit|in|ahahah|please|check2|proper|for|IGNORECASE|decode|s|_|https|addon|replace|leave|made|this|if|http|path|line|findall|com|(ﾟｰﾟ)|mp4|def|www|vr|dl|by|re|compile|videourl|l|u|m|videourl2|(ﾟΘﾟ)|w|decodeOpenLoad|DOTALL|group|t".split("|")))





def decode(encoded):
    for octc in (c for c in re.findall(r'\\(\d{2,3})', encoded)):
        encoded = encoded.replace(r'\%s' % octc, chr(int(octc, 8)))
    return encoded.decode('utf8')


def base10toN(num,n):
    num_rep={10:'a',
         11:'b',
         12:'c',
         13:'d',
         14:'e',
         15:'f',
         16:'g',
         17:'h',
         18:'i',
         19:'j',
         20:'k',
         21:'l',
         22:'m',
         23:'n',
         24:'o',
         25:'p',
         26:'q',
         27:'r',
         28:'s',
         29:'t',
         30:'u',
         31:'v',
         32:'w',
         33:'x',
         34:'y',
         35:'z'}
    new_num_string=''
    current=num
    while current!=0:
        remainder=current%n
        if 36>remainder>9:
            remainder_string=num_rep[remainder]
        elif remainder>=36:
            remainder_string='('+str(remainder)+')'
        else:
            remainder_string=str(remainder)
        new_num_string=remainder_string+new_num_string
        current=current/n
    return new_num_string


def searchDir(url, mode):
    conn = sqlite3.connect(favoritesdb)
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM keywords")
        for (keyword,) in c.fetchall():
            name = '[COLOR deeppink]' + urllib.unquote_plus(keyword) + '[/COLOR]'
            addDir(name, url, mode, '', keyword=keyword)
    except: pass
    addDir('[COLOR hotpink]Add Keyword[/COLOR]', url, 902, '', '', mode, Folder=False)
    addDir('[COLOR hotpink]Clear list[/COLOR]', '', 903, '', Folder=False)
    xbmcplugin.endOfDirectory(addon_handle)

def newSearch(url, mode):
    vq = _get_keyboard(heading="Searching for...")
    if (not vq): return False, 0
    title = urllib.quote_plus(vq)
    addKeyword(title)
    xbmc.executebuiltin('Container.Refresh')
    #searchcmd = (sys.argv[0] +
    #     "?url=" + urllib.quote_plus(url) +
    #     "&mode=" + str(mode) +
    #     "&keyword=" + urllib.quote_plus(title))
    #xbmc.executebuiltin('xbmc.RunPlugin('+searchcmd+')')


def clearSearch():
    delKeyword()
    xbmc.executebuiltin('Container.Refresh')


def addKeyword(keyword):
    xbmc.log(keyword)
    conn = sqlite3.connect(favoritesdb)
    c = conn.cursor()
    c.execute("INSERT INTO keywords VALUES (?)", (keyword,))
    conn.commit()
    conn.close()


def delKeyword():
    conn = sqlite3.connect(favoritesdb)
    c = conn.cursor()
    c.execute("DELETE FROM keywords;")
    conn.commit()
    conn.close()
