#-*- coding: utf-8 -*-

'''
    Ultimate Whitecream
    Copyright (C) 2015 Whitecream

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

__scriptname__ = "Ultimate Whitecream"
__author__ = "Whitecream"
__scriptid__ = "plugin.video.uwc"
__credits__ = "Whitecream, Fr33m1nd, anton40, NothingGnome"
__version__ = "1.1.45"

import urllib
import urllib2
import re
import cookielib
import os.path
import sys
import time
import tempfile
import sqlite3
import urlparse
import base64
from StringIO import StringIO
import gzip

import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon
import xbmcvfs
import cloudflare
from jsunpack import unpack


from url_dispatcher import URL_Dispatcher

url_dispatcher = URL_Dispatcher()



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
uwcicon = xbmc.translatePath(os.path.join(rootDir, 'icon.png'))

profileDir = addon.getAddonInfo('profile')
profileDir = xbmc.translatePath(profileDir).decode("utf-8")
cookiePath = os.path.join(profileDir, 'cookies.lwp')

if not os.path.exists(profileDir):
    os.makedirs(profileDir)

urlopen = urllib2.urlopen
cj = cookielib.LWPCookieJar(xbmc.translatePath(cookiePath))
Request = urllib2.Request

if cj != None:
    if os.path.isfile(xbmc.translatePath(cookiePath)):
        try:
            cj.load()
        except:
            try:
                os.remove(xbmc.translatePath(cookiePath))
                pass
            except:
                dialog.ok('Oh oh','The Cookie file is locked, please restart Kodi')
                pass
    cookie_handler = urllib2.HTTPCookieProcessor(cj)
    opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
else:
    opener = urllib2.build_opener()

urllib2.install_opener(opener)

favoritesdb = os.path.join(profileDir, 'favorites.db')

class StopDownloading(Exception):
    def __init__(self, value): self.value = value
    def __str__(self): return repr(self.value)

def downloadVideo(url, name):

    def _pbhook(downloaded, filesize, url=None,dp=None):
        try:
            percent = min((downloaded*100)/filesize, 100)
            currently_downloaded = float(downloaded) / (1024 * 1024)
            kbps_speed = int(downloaded / (time.clock() - start))
            if kbps_speed > 0:
                eta = (filesize - downloaded) / kbps_speed
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


    def getResponse(url, headers2, size):
        try:
            if size > 0:
                size = int(size)
                headers2['Range'] = 'bytes=%d-' % size

            req = Request(url, headers=headers2)

            resp = urlopen(req, timeout=30)
            return resp
        except:
            return None

    def doDownload(url, dest, dp):

        try: headers = dict(urlparse.parse_qsl(url.rsplit('|', 1)[1]))
        except: headers = dict('')

        if 'openload' in url:
            headers = openloadhdr
            
        if 'spankbang.com' in url:
            url = getVideoLink(url,url)

        url = url.split('|')[0]
        file = dest.rsplit(os.sep, 1)[-1]
        resp = getResponse(url, headers, 0)


        if not resp:
            xbmcgui.Dialog().ok("Ultimate Whitecream", 'Download failed', 'No response from server')
            return False

        try:    content = int(resp.headers['Content-Length'])
        except: content = 0

        try:    resumable = 'bytes' in resp.headers['Accept-Ranges'].lower()
        except: resumable = False
        if resumable:
            print "Download is resumable"

        if content < 1:
            xbmcgui.Dialog().ok("Ultimate Whitecream", 'Unknown filesize', 'Unable to download')
            return False

        size = 8192
        mb   = content / (1024 * 1024)

        if content < size:
            size = content

        total   = 0
        errors  = 0
        count   = 0
        resume  = 0
        sleep   = 0

        print 'Download File Size : %dMB %s ' % (mb, dest)
        f = xbmcvfs.File(dest, 'w')

        chunk  = None
        chunks = []

        while True:
            downloaded = total
            for c in chunks:
                downloaded += len(c)
            percent = min(100 * downloaded / content, 100)

            _pbhook(downloaded,content,url,dp)

            chunk = None
            error = False

            try:
                chunk  = resp.read(size)
                if not chunk:
                    if percent < 99:
                        error = True
                    else:
                        while len(chunks) > 0:
                            c = chunks.pop(0)
                            f.write(c)
                            del c

                        f.close()
                        print '%s download complete' % (dest)
                        return True

            except Exception, e:
                print str(e)
                error = True
                sleep = 10
                errno = 0

                if hasattr(e, 'errno'):
                    errno = e.errno

                if errno == 10035: # 'A non-blocking socket operation could not be completed immediately'
                    pass

                if errno == 10054: #'An existing connection was forcibly closed by the remote host'
                    errors = 10 #force resume
                    sleep  = 30

                if errno == 11001: # 'getaddrinfo failed'
                    errors = 10 #force resume
                    sleep  = 30

            if chunk:
                errors = 0
                chunks.append(chunk)
                if len(chunks) > 5:
                    c = chunks.pop(0)
                    f.write(c)
                    total += len(c)
                    del c

            if error:
                errors += 1
                count  += 1
                print '%d Error(s) whilst downloading %s' % (count, dest)
                xbmc.sleep(sleep*1000)

            if (resumable and errors > 0) or errors >= 10:
                if (not resumable and resume >= 50) or resume >= 500:
                    #Give up!
                    print '%s download canceled - too many error whilst downloading' % (dest)
                    return False

                resume += 1
                errors  = 0
                if resumable:
                    chunks  = []
                    #create new response
                    print 'Download resumed (%d) %s' % (resume, dest)
                    resp = getResponse(url, headers, total)
                else:
                    #use existing response
                    pass


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
            #urllib.urlretrieve(url,tmp_file,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
            downloaded = doDownload(url, tmp_file, dp)
            if downloaded:
                vidfile = xbmc.makeLegalFilename(download_path + clean_filename(name) + ".mp4")
                try:
                  os.rename(tmp_file, vidfile)
                  return vidfile
                except:
                  return tmp_file
            else: raise StopDownloading('Stopped Downloading')
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


def kodilog(logvar):
    xbmc.log(str(logvar))


def PLAYVIDEO(url, name, download=None):
    progress.create('Play video', 'Searching videofile.')
    progress.update( 10, "", "Loading video page", "" )
    videosource = getHtml(url, url)
    playvideo(videosource, name, download, url)


def playvideo(videosource, name, download=None, url=None):
    import urlresolver
    hosts = []
    if re.search('openload\.(?:co|io)?/', videosource, re.DOTALL | re.IGNORECASE):
        hosts.append('OpenLoad')
    if re.search('oload\.(?:co|io)?/', videosource, re.DOTALL | re.IGNORECASE):
        hosts.append('OpenLoad')
    if re.search('streamin\.to/', videosource, re.DOTALL | re.IGNORECASE):
        hosts.append('Streamin')
    if re.search('flashx\.tv/', videosource, re.DOTALL | re.IGNORECASE):
        hosts.append('FlashX')
    if re.search('mega3x\.net/', videosource, re.DOTALL | re.IGNORECASE):
        hosts.append('Mega3X')
    if re.search('streamcloud\.eu/', videosource, re.DOTALL | re.IGNORECASE):
        hosts.append('StreamCloud')
    if re.search('jetload\.tv/', videosource, re.DOTALL | re.IGNORECASE):
        hosts.append('Jetload')
    if re.search('videowood\.tv/', videosource, re.DOTALL | re.IGNORECASE):
        hosts.append('Videowood')
    if re.search('streamdefence.com/view\.php', videosource, re.DOTALL | re.IGNORECASE):
        hosts.append('Streamdefence')
    if re.search('datoporn.com', videosource, re.DOTALL | re.IGNORECASE):
        hosts.append('Datoporn')
    if re.search('<source', videosource, re.DOTALL | re.IGNORECASE):
        hosts.append('Direct Source')
    if not 'keeplinks' in url:
        if re.search('keeplinks\.eu/p', videosource, re.DOTALL | re.IGNORECASE):
            hosts.append('Keeplinks <--')
    if re.search('filecrypt.cc/Container', videosource, re.DOTALL | re.IGNORECASE):
        hosts.append('Filecrypt')
    if len(hosts) == 0:
        progress.close()
        notify('Oh oh','Couldn\'t find any video')
        return
    elif len(hosts) > 1:
        if addon.getSetting("dontask") == "true":
            vidhost = hosts[0]
        else:
            vh = dialog.select('Videohost:', hosts)
            if vh == -1:
                return
            vidhost = hosts[vh]
    else:
        vidhost = hosts[0]

    if vidhost == 'OpenLoad':
        progress.update( 40, "", "Loading Openload", "" )
        openloadurl = re.compile(r"//(?:www\.)?o(?:pen)?load\.(?:co|io)?/(?:embed|f)/([0-9a-zA-Z-_]+)", re.DOTALL | re.IGNORECASE).findall(videosource)
        openloadurl = chkmultivids(openloadurl)

        openloadurl1 = 'http://openload.io/embed/%s/' % openloadurl
        progress.update( 50, "", "Loading Openload", "Sending it to urlresolver" )
        try:
            video = urlresolver.resolve(openloadurl1)
            if video:
                progress.update( 80, "", "Loading Openload", "Found the video" )
                videourl = video
        except:
            notify('Oh oh','Couldn\'t find playable OpenLoad link')
            return

    elif vidhost == 'Streamin':
        progress.update( 40, "", "Loading Streamin", "" )
        streaminurl = re.compile(r"//(?:www\.)?streamin\.to/(?:embed-)?([0-9a-zA-Z]+)", re.DOTALL | re.IGNORECASE).findall(videosource)
        streaminurl = chkmultivids(streaminurl)
        streaminurl = 'http://streamin.to/embed-%s-670x400.html' % streaminurl
        progress.update( 50, "", "Loading Streamin", "Sending it to urlresolver")
        video = urlresolver.resolve(streaminurl)
        if video:
            progress.update( 80, "", "Loading Streamin", "Found the video" )
            videourl = video

    elif vidhost == 'FlashX':
        progress.update( 40, "", "Loading FlashX", "" )
        flashxurl = re.compile(r"//(?:www\.)?flashx\.tv/(?:embed-)?([0-9a-zA-Z]+)", re.DOTALL | re.IGNORECASE).findall(videosource)
        media_id = chkmultivids(flashxurl)
        flashxurl = 'http://www.flashx.tv/%s.html' % media_id
        progress.update( 50, "", "Loading FlashX", "Sending it to urlresolver" )
        video = urlresolver.resolve(flashxurl)
        if video:
            progress.update( 80, "", "Loading FlashX", "Found the video" )
            videourl = video

    elif vidhost == 'Mega3X':
        progress.update( 40, "", "Loading Mega3X", "" )
        mega3xurl = re.compile(r"(https?://(?:www\.)?mega3x.net/(?:embed-)?(?:[0-9a-zA-Z]+).html)", re.DOTALL | re.IGNORECASE).findall(videosource)
        mega3xurl = chkmultivids(mega3xurl)
        mega3xsrc = getHtml(mega3xurl,'', openloadhdr)
        mega3xjs = re.compile("<script[^>]+>(eval[^<]+)</sc", re.DOTALL | re.IGNORECASE).findall(mega3xsrc)
        progress.update( 80, "", "Getting video file from Mega3X", "" )
        mega3xujs = unpack(mega3xjs[0])
        videourl = re.compile('file:\s?"([^"]+m3u8)"', re.DOTALL | re.IGNORECASE).findall(mega3xujs)
        videourl = videourl[0]

    elif vidhost == 'Datoporn':
        progress.update( 40, "", "Loading Datoporn", "" )
        datourl = re.compile(r"//(?:www\.)?datoporn\.com/(?:embed-)?([0-9a-zA-Z]+)", re.DOTALL | re.IGNORECASE).findall(videosource)
        datourl = chkmultivids(datourl)
        datourl = "http://datoporn.com/embed-" + datourl + ".html"
        datosrc = getHtml(datourl,'', openloadhdr)
        try:
            datojs = re.compile("<script[^>]+>(eval[^<]+)</sc", re.DOTALL | re.IGNORECASE).findall(datosrc)
            datoujs = unpack(datojs[0])
        except:
            datoujs = datosrc
        progress.update( 80, "", "Getting video file from Datoporn", "" )
        videourl = re.compile('file:"([^"]+mp4)"', re.DOTALL | re.IGNORECASE).findall(datoujs)
        videourl = videourl[0]

    elif vidhost == 'StreamCloud':
        progress.update( 40, "", "Opening Streamcloud", "" )
        streamcloudurl = re.compile(r"//(?:www\.)?streamcloud\.eu?/([0-9a-zA-Z-_/.]+html)", re.DOTALL | re.IGNORECASE).findall(videosource)
        streamcloudurl = chkmultivids(streamcloudurl)
        streamcloudurl = "http://streamcloud.eu/" + streamcloudurl
        progress.update( 50, "", "Getting Streamcloud page", "" )
        schtml = postHtml(streamcloudurl)
        form_values = {}
        match = re.compile('<input.*?name="(.*?)".*?value="(.*?)">', re.DOTALL | re.IGNORECASE).findall(schtml)
        for name, value in match:
            form_values[name] = value.replace("download1","download2")
        progress.update( 60, "", "Grabbing video file", "" )
        newscpage = postHtml(streamcloudurl, form_data=form_values)
        videourl = re.compile('file:\s*"(.+?)",', re.DOTALL | re.IGNORECASE).findall(newscpage)[0]

    elif vidhost == 'Jetload':
        progress.update( 40, "", "Loading Jetload", "" )
        jlurl = re.compile(r'jetload\.tv/([^"]+)', re.DOTALL | re.IGNORECASE).findall(videosource)
        jlurl = chkmultivids(jlurl)
        jlurl = "http://jetload.tv/" + jlurl
        progress.update( 50, "", "Loading Jetload", "Sending it to urlresolver" )
        video = urlresolver.resolve(jlurl)
        if video:
            progress.update( 80, "", "Loading Jetload", "Found the video" )
            videourl = video
        # jlsrc = getHtml(jlurl, url)
        # videourl = re.compile(r'file: "([^"]+)', re.DOTALL | re.IGNORECASE).findall(jlsrc)
        # videourl = videourl[0]

    elif vidhost == 'Videowood':
        progress.update( 40, "", "Loading Videowood", "" )
        vwurl = re.compile(r"//(?:www\.)?videowood\.tv/(?:embed|video)/([0-9a-zA-Z]+)", re.DOTALL | re.IGNORECASE).findall(videosource)
        vwurl = chkmultivids(vwurl)
        vwurl = 'http://www.videowood.tv/embed/' + vwurl
        progress.update( 50, "", "Loading Videowood", "Sending it to urlresolver" )
        video = urlresolver.resolve(vwurl)
        if video:
            progress.update( 80, "", "Loading Videowood", "Found the video" )
            videourl = video

    elif vidhost == 'Keeplinks <--':
        progress.update( 40, "", "Loading Keeplinks", "" )
        klurl = re.compile(r"//(?:www\.)?keeplinks\.eu/p([0-9a-zA-Z/]+)", re.DOTALL | re.IGNORECASE).findall(videosource)
        klurl = chkmultivids(klurl)
        klurl = 'http://www.keeplinks.eu/p' + klurl
        kllink = getVideoLink(klurl, '')
        kllinkid = kllink.split('/')[-1]
        klheader = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive',
           'Cookie': 'flag['+kllinkid+'] = 1;'}
        klpage = getHtml(kllink, klurl, klheader)
        playvideo(klpage, name, download, klurl)
        return

    elif vidhost == 'Streamdefence':
        progress.update( 40, "", "Loading Streamdefence", "" )
        sdurl = re.compile(r'streamdefence\.com/view.php\?ref=([^"]+)"', re.DOTALL | re.IGNORECASE).findall(videosource)
        sdurl = chkmultivids(sdurl)
        sdurl = 'http://www.streamdefence.com/view.php?ref=' + sdurl
        sdsrc = getHtml(sdurl, url)
        progress.update( 80, "", "Getting video file from Streamdefence", "" )
        sdpage = streamdefence(sdsrc)
        playvideo(sdpage, name, download, sdurl)
        return

    elif vidhost == 'Filecrypt':
        progress.update( 40, "", "Loading Filecrypt", "" )
        fcurl = re.compile(r'filecrypt\.cc/Container/([^\.]+)\.html', re.DOTALL | re.IGNORECASE).findall(videosource)
        fcurl = chkmultivids(fcurl)
        fcurl = 'http://filecrypt.cc/Container/' + fcurl + ".html"
        fcsrc = getHtml(fcurl, url)
        fcmatch = re.compile(r"onclick=\"openLink.?'([\w\-]*)',", re.DOTALL | re.IGNORECASE).findall(fcsrc)
        progress.update( 80, "", "Getting video file from Filecrypt", "" )
        fcurls = ""
        for fclink in fcmatch:
            fcpage = "http://filecrypt.cc/Link/" + fclink + ".html"
            fcpagesrc = getHtml(fcpage, fcurl)
            fclink2 = re.search('<iframe .*? noresize src="(.*)"></iframe>', fcpagesrc)
            if fclink2:
                try:
                    fcurl2 = getVideoLink(fclink2.group(1), fcpage)
                    fcurls = fcurls + " " + fcurl2
                except:
                    pass
        playvideo(fcurls, name, download, fcurl)
        return

    elif vidhost == 'Direct Source':
        progress.update( 40, "", "Loading Direct source", "" )
        dsurl = re.compile("""<source.*?src=(?:"|')([^"']+)[^>]+>""", re.DOTALL | re.IGNORECASE).findall(videosource)
        dsurl = chkmultivids(dsurl)
        videourl = dsurl
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


def chkmultivids(videomatch):
    videolist = list(set(videomatch))
    if len(videolist) > 1:
        i = 1
        hashlist = []
        for x in videolist:
            hashlist.append('Video ' + str(i))
            i += 1
        mvideo = dialog.select('Multiple videos found', hashlist)
        if mvideo == -1:
            return
        return videolist[mvideo]
    else:
        return videomatch[0]

@url_dispatcher.register('9', ['name', 'url'])
def PlayStream(name, url):
    item = xbmcgui.ListItem(name, path = url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
    return


def getHtml(url, referer='', hdr=None, NoCookie=None, data=None):
    try:
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
    except urllib2.HTTPError as e:
        data = e.read()
        if e.code == 503 and 'cf-browser-verification' in data:
            data = cloudflare.solve(url,cj, USER_AGENT)
        else:
            raise urllib2.HTTPError()
    return data


def postHtml(url, form_data={}, headers={}, compression=True, NoCookie=None):
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
    if not NoCookie:
        try:
            cj.save(cookiePath)
        except: pass
    response.close()
    return data


def getHtml2(url):
    req = Request(url)
    response = urlopen(req, timeout=60)
    data = response.read()
    response.close()
    return data


def getVideoLink(url, referer, hdr=None, data=None):
    if not hdr:
        req2 = Request(url, data, headers)
    else:
        req2 = Request(url, data, hdr)
    if len(referer) > 1:
        req2.add_header('Referer', referer)
    url2 = urlopen(req2).geturl()
    return url2


def parse_query(query):
    toint = ['page', 'download', 'favmode', 'channel', 'section']
    q = {'mode': '0'}
    if query.startswith('?'): query = query[1:]
    queries = urlparse.parse_qs(query)
    for key in queries:
        if len(queries[key]) == 1:
            if key in toint:
                try: q[key] = int(queries[key][0])
                except: q[key] = queries[key][0]
            else:
                q[key] = queries[key][0]
        else:
            q[key] = queries[key]
    return q


def cleantext(text):
    text = text.replace('&#8211;','-')
    text = text.replace('&ndash;','-')
    text = text.replace('&#038;','&')
    text = text.replace('&#8217;','\'')
    text = text.replace('&#8216;','\'')
    text = text.replace('&#8230;','...')
    text = text.replace('&quot;','"')
    text = text.replace('&#039;','`')
    text = text.replace('&amp;','&')
    text = text.replace('&ntilde;','ñ')
    text = text.replace('&rsquo;','\'')
    return text


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def addDownLink(name, url, mode, iconimage, desc='', stream=None, fav='add', noDownload=False):
    contextMenuItems = []
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
    fanart = os.path.join(rootDir, 'fanart.jpg')
    if addon.getSetting('posterfanart') == 'true':
        fanart = iconimage
        liz.setArt({'poster': iconimage})
    liz.setArt({'fanart': fanart})
    if stream:
        liz.setProperty('IsPlayable', 'true')
    if len(desc) < 1:
        liz.setInfo(type="Video", infoLabels={"Title": name})
    else:
        liz.setInfo(type="Video", infoLabels={"Title": name, "plot": desc, "plotoutline": desc})
    video_streaminfo = {'codec': 'h264'}
    liz.addStreamInfo('video', video_streaminfo)
    contextMenuItems.append(('[COLOR hotpink]' + favtext + ' favorites[/COLOR]', 'xbmc.RunPlugin('+favorite+')'))
    if noDownload == False:
        contextMenuItems.append(('[COLOR hotpink]Download Video[/COLOR]', 'xbmc.RunPlugin('+dwnld+')'))
    liz.addContextMenuItems(contextMenuItems, replaceItems=False)
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
    fanart = os.path.join(rootDir, 'fanart.jpg')
    if addon.getSetting('posterfanart') == 'true':
        fanart = iconimage
        liz.setArt({'poster': iconimage})
    liz.setArt({'fanart': fanart})
    liz.setInfo(type="Video", infoLabels={"Title": name})

    if len(keyword) >= 1:
        keyw = (sys.argv[0] +
            "?mode=" + str('904') +
            "&keyword=" + urllib.quote_plus(keyword))
        contextMenuItems = []
        contextMenuItems.append(('[COLOR hotpink]Remove keyword[/COLOR]', 'xbmc.RunPlugin('+keyw+')'))
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
    ok = xbmcplugin.addDirectoryItem(handle=addon_handle, url=u, listitem=liz, isFolder=Folder)
    return ok

def _get_keyboard(default="", heading="", hidden=False):
    """ shows a keyboard and returns a value """
    keyboard = xbmc.Keyboard(default, heading, hidden)
    keyboard.doModal()
    if keyboard.isConfirmed():
        return unicode(keyboard.getText(), "utf-8")
    return default



# videowood decode copied from: https://github.com/schleichdi2/OpenNfr_E2_Gui-5.3/blob/4e3b5e967344c3ddc015bc67833a5935fc869fd4/lib/python/Plugins/Extensions/MediaPortal/resources/hosters/videowood.py
def videowood(data):
    parse = re.search('(....ωﾟ.*?);</script>', data)
    if parse:
        todecode = parse.group(1).split(';')
        todecode = todecode[-1].replace(' ','')

        code = {
            "(ﾟДﾟ)[ﾟoﾟ]" : "o",
            "(ﾟДﾟ) [return]" : "\\",
            "(ﾟДﾟ) [ ﾟΘﾟ]" : "_",
            "(ﾟДﾟ) [ ﾟΘﾟﾉ]" : "b",
            "(ﾟДﾟ) [ﾟｰﾟﾉ]" : "d",
            "(ﾟДﾟ)[ﾟεﾟ]": "/",
            "(oﾟｰﾟo)": '(u)',
            "3ﾟｰﾟ3": "u",
            "(c^_^o)": "0",
            "(o^_^o)": "3",
            "ﾟεﾟ": "return",
            "ﾟωﾟﾉ": "undefined",
            "_": "3",
            "(ﾟДﾟ)['0']" : "c",
            "c": "0",
            "(ﾟΘﾟ)": "1",
            "o": "3",
            "(ﾟｰﾟ)": "4",
            }
        cryptnumbers = []
        for searchword,isword in code.iteritems():
            todecode = todecode.replace(searchword,isword)
        for i in range(len(todecode)):
            if todecode[i:i+2] == '/+':
                for j in range(i+2, len(todecode)):
                    if todecode[j:j+2] == '+/':
                        cryptnumbers.append(todecode[i+1:j])
                        i = j
                        break
                        break
        finalstring = ''
        for item in cryptnumbers:
            chrnumber = '\\'
            jcounter = 0
            while jcounter < len(item):
                clipcounter = 0
                if item[jcounter] == '(':
                    jcounter +=1
                    clipcounter += 1
                    for k in range(jcounter, len(item)):
                        if item[k] == '(':
                            clipcounter += 1
                        elif item[k] == ')':
                            clipcounter -= 1
                        if clipcounter == 0:
                            jcounter = 0
                            chrnumber = chrnumber + str(eval(item[:k+1]))
                            item = item[k+1:]
                            break
                else:
                    jcounter +=1
            finalstring = finalstring + chrnumber.decode('unicode-escape')
        stream_url = re.search('=\s*(\'|")(.*?)$', finalstring)
        if stream_url:
            return stream_url.group(2)
    else:
        return


def streamdefence(html):
    if 'openload' in html:
        return html
    match = re.search(r'\("([^"]+)', html, re.DOTALL | re.IGNORECASE)
    if match:
        result = match.group()
        decoded = base64.b64decode(result)
    else:
        decoded = base64.b64decode(html)
    return streamdefence(decoded)


def searchDir(url, mode, page=None):
    conn = sqlite3.connect(favoritesdb)
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM keywords")
        for (keyword,) in c.fetchall():
            name = '[COLOR deeppink]' + urllib.unquote_plus(keyword) + '[/COLOR]'
            addDir(name, url, mode, '', page=page, keyword=keyword)
    except: pass
    addDir('[COLOR hotpink]Add Keyword[/COLOR]', url, 902, '', '', mode, Folder=False)
    addDir('[COLOR hotpink]Clear list[/COLOR]', '', 903, '', Folder=False)
    xbmcplugin.endOfDirectory(addon_handle)

@url_dispatcher.register('902', ['url', 'channel'])
def newSearch(url, channel):
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

@url_dispatcher.register('903')
def clearSearch():
    delallKeyword()
    xbmc.executebuiltin('Container.Refresh')


def addKeyword(keyword):
    xbmc.log(keyword)
    conn = sqlite3.connect(favoritesdb)
    c = conn.cursor()
    c.execute("INSERT INTO keywords VALUES (?)", (keyword,))
    conn.commit()
    conn.close()


def delallKeyword():
    conn = sqlite3.connect(favoritesdb)
    c = conn.cursor()
    c.execute("DELETE FROM keywords;")
    conn.commit()
    conn.close()

@url_dispatcher.register('904', ['keyword'])
def delKeyword(keyword):
    xbmc.log('keyword: ' + keyword)
    conn = sqlite3.connect(favoritesdb)
    c = conn.cursor()
    c.execute("DELETE FROM keywords WHERE keyword = '%s'" % keyword)
    conn.commit()
    conn.close()
    xbmc.executebuiltin('Container.Refresh')
