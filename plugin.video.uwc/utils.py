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
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

from jsbeautifier import beautify

__scriptname__ = "Ultimate Whitecream"
__author__ = "mortael"
__scriptid__ = "plugin.video.uwc"
__credits__ = "mortael, Fr33m1nd, anton40"
__version__ = "1.0.63"

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


def PLAYVIDEO(url, name, download=None):
    progress.create('Play video', 'Searching videofile.')
    progress.update( 10, "", "Loading video page", "" )
    videosource = getHtml(url, url)
    playvideo(videosource, name, download, url)


def playvideo(videosource, name, download=None, url=None):
    hosts = []
    if re.search('videomega\.tv/', videosource, re.DOTALL | re.IGNORECASE):
        hosts.append('VideoMega')
    if re.search('openload\.', videosource, re.DOTALL | re.IGNORECASE):
        hosts.append('OpenLoad')
    if re.search('streamin.to', videosource, re.DOTALL | re.IGNORECASE):
        hosts.append('Streamin')          
    if re.search('www.flashx.tv', videosource, re.DOTALL | re.IGNORECASE):
        hosts.append('FlashX')
    if len(hosts) == 0:
        progress.close()
        dialog.ok('Oh oh','Couldn\'t find any video')
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
                dialog.ok('Oh oh','Couldn\'t find playable videomega link')
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
        videopage = getHtml('http://videomega.tv/view.php?ref='+hashref[0], url)
        videourl = re.compile('<source src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(videopage)
        videourl = videourl[0]
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
            dialog.ok('Oh oh','Couldn\'t find playable OpenLoad link')
    elif vidhost == 'Streamin':
        progress.update( 40, "", "Loading Streamin", "" )
        streaminurl = re.compile('<iframe.*?src="(http://streamin\.to[^"]+)"', re.DOTALL | re.IGNORECASE).findall(videosource)
        streaminsrc = getHtml2(streaminurl[0])
        videohash = re.compile('h=([^"]+)', re.DOTALL | re.IGNORECASE).findall(streaminsrc)
        videourl = re.compile('image: "(http://[^/]+/)', re.DOTALL | re.IGNORECASE).findall(streaminsrc)
        progress.update( 80, "", "Getting video file from Streamin", "" )
        videourl = videourl[0] + videohash[0] + "/v.mp4"
    elif vidhost == 'FlashX':
        progress.update( 40, "", "Loading FlashX", "" )
        flashxurl = re.compile(r"//(?:www\.)?flashx\.tv/(?:embed-)?([0-9a-zA-Z]+)", re.DOTALL | re.IGNORECASE).findall(videosource)
        flashxurl = 'http://flashx.tv/embed-%s-670x400.html' % flashxurl[0]
        flashxsrc = getHtml2(flashxurl)
        progress.update( 60, "", "Grabbing video file", "" )
        flashxurl2 = re.compile('<a href="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(flashxsrc)
        flashxsrc2 = getHtml2(flashxurl2[0])
        progress.update( 70, "", "Grabbing video file", "" ) 
        flashxjs = re.compile("<script type='text/javascript'>([^<]+)</sc", re.DOTALL | re.IGNORECASE).findall(flashxsrc2)
        progress.update( 80, "", "Getting video file from FlashX", "" )
        flashxujs = beautify(flashxjs[0])
        videourl = re.compile(r'\[{\s+file: "([^"]+)",', re.DOTALL | re.IGNORECASE).findall(flashxujs)
        videourl = videourl[0]
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


def getHtml(url, referer, hdr=None, NoCookie=None):
    if not hdr:
        req = Request(url, '', headers)
    else:
        req = Request(url, '', hdr)
    if len(referer) > 1:
        req.add_header('Referer', referer)
    response = urlopen(req, timeout=60)
    data = response.read()
    if not NoCookie:
        cj.save(cookiePath)
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
    text = text.replace('&#8230;','...')
    text = text.replace('&quot;','"')
    text = text.replace('&#039;','`')
    text = text.replace('&amp;','&')
    return text


def addDownLink(name, url, mode, iconimage, desc, stream=None):
    u = (sys.argv[0] +
         "?url=" + urllib.quote_plus(url) +
         "&mode=" + str(mode) +
         "&name=" + urllib.quote_plus(name))
    dwnld = (sys.argv[0] +
         "?url=" + urllib.quote_plus(url) +
         "&mode=" + str(mode) +
         "&download=" + str(1) +
         "&name=" + urllib.quote_plus(name))         
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    if stream:
        liz.setProperty('IsPlayable', 'true')
    if len(desc) < 1:
        liz.setInfo(type="Video", infoLabels={"Title": name})
    else:
        liz.setInfo(type="Video", infoLabels={"Title": name, "plot": desc, "plotoutline": desc})
    liz.addContextMenuItems([('Download Video', 'xbmc.RunPlugin('+dwnld+')')])
    ok = xbmcplugin.addDirectoryItem(handle=addon_handle, url=u, listitem=liz, isFolder=False)
    return ok
    

def addDir(name, url, mode, iconimage, page=None):
    u = (sys.argv[0] +
         "?url=" + urllib.quote_plus(url) +
         "&mode=" + str(mode) +
         "&page=" + str(page) +
         "&name=" + urllib.quote_plus(name))
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name})
    ok = xbmcplugin.addDirectoryItem(handle=addon_handle, url=u, listitem=liz, isFolder=True)
    return ok
    
def _get_keyboard(default="", heading="", hidden=False):
    """ shows a keyboard and returns a value """
    keyboard = xbmc.Keyboard(default, heading, hidden)
    keyboard.doModal()
    if keyboard.isConfirmed():
        return unicode(keyboard.getText(), "utf-8")
    return default
 

def decodeOpenLoad(html):

    aastring = re.search(r"<video(?:.|\s)*?<script\s[^>]*?>((?:.|\s)*?)</script", html, re.DOTALL | re.IGNORECASE).group(1)
    
    aastring = aastring.replace("((ﾟｰﾟ) + (ﾟｰﾟ) + (ﾟΘﾟ))", "9")
    aastring = aastring.replace("((ﾟｰﾟ) + (ﾟｰﾟ))","8")
    aastring = aastring.replace("((ﾟｰﾟ) + (o^_^o))","7")
    aastring = aastring.replace("((o^_^o) +(o^_^o))","6")
    aastring = aastring.replace("((ﾟｰﾟ) + (ﾟΘﾟ))","5")
    aastring = aastring.replace("(ﾟｰﾟ)","4")
    aastring = aastring.replace("((o^_^o) - (ﾟΘﾟ))","2")
    aastring = aastring.replace("(o^_^o)","3")
    aastring = aastring.replace("(ﾟΘﾟ)","1")
    aastring = aastring.replace("(c^_^o)","0")
    aastring = aastring.replace("(ﾟДﾟ)[ﾟεﾟ]","\\")
    aastring = aastring.replace("(3 +3 +0)","6")
    aastring = aastring.replace("(3 - 1 +0)","2")
    aastring = aastring.replace("(1 -0)","1")
    aastring = aastring.replace("(4 -0)","4")

    decodestring = re.search(r"\\\+([^(]+)", aastring, re.DOTALL | re.IGNORECASE).group(1)
    decodestring = "\\+"+ decodestring
    decodestring = decodestring.replace("+","")
    decodestring = decodestring.replace(" ","")
    
    decodestring = decode(decodestring)
    decodestring = decodestring.replace("\\/","/")
    
    videourl = re.search(r'vr="([^"]+)', decodestring, re.DOTALL | re.IGNORECASE).group(1)
    return videourl

def decode(encoded):
    for octc in (c for c in re.findall(r'\\(\d{2,3})', encoded)):
        encoded = encoded.replace(r'\%s' % octc, chr(int(octc, 8)))
    return encoded.decode('utf8')
