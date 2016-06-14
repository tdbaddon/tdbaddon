# -*- coding: utf-8 -*-

'''
    Croatia On Demand Add-on
    Copyright (C) 2016 natko1412
    Copyright (C) 2015 Blazetamer
    Copyright (C) 2015 lambda
    Copyright (C) 2015 spoyser
    Copyright (C) 2015 crzen

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


import re,os,sys,urllib,urllib2,urlparse,time,threading

from resources.lib.modules import control
from resources.lib.modules import cache
import pyxbmct.addonwindow as pyxbmct

downloadPath = control.setting('downloadPath')
property = control.addonInfo('id') + '.downloader'



def downloader():
    thumb = control.addonThumb() ; fanart = control.addonFanart()

    status = control.window.getProperty(property + '.status')

    if not downloadPath == '':
        item = control.item('[COLOR FF00b8ff]Preuzimanja[/COLOR]', iconImage=thumb, thumbnailImage=thumb)
        item.addContextMenuItems([], replaceItems=True)
        item.setProperty('fanart_image', fanart)
        control.addItem(handle=int(sys.argv[1]), url=downloadPath, listitem=item, isFolder=True)

    if status == 'downloading':
        item = control.item('[COLOR red]Zaustavi preuzimanja[/COLOR]', iconImage=thumb, thumbnailImage=thumb)
        item.addContextMenuItems([], replaceItems=True)
        item.setProperty('fanart_image', fanart)
        control.addItem(handle=int(sys.argv[1]), url=sys.argv[0]+'?mode=stopDownload', listitem=item, isFolder=True)
    else:
        item = control.item('[COLOR FF00b8ff]Pokreni preuzimanja[/COLOR]', iconImage=thumb, thumbnailImage=thumb)
        item.addContextMenuItems([], replaceItems=True)
        item.setProperty('fanart_image', fanart)
        control.addItem(handle=int(sys.argv[1]), url=sys.argv[0]+'?mode=startDownload', listitem=item, isFolder=True)

    if status == 'downloading':
        item = control.item('[COLOR gold]Status preuzimanja[/COLOR]', iconImage=thumb, thumbnailImage=thumb)
        item.addContextMenuItems([], replaceItems=True)
        item.setProperty('Fanart_Image', fanart)
        control.addItem(handle=int(sys.argv[1]), url=sys.argv[0]+'?mode=statusDownload', listitem=item, isFolder=True)

    def download(): return []
    result = cache.get(download, 600000000, table='rel_dl')

    for i in result:
        try:
            cm = []
            cm.append(('Ukloni iz reda čekanja', 'RunPlugin(%s?mode=removeDownload&url=%s)' % (sys.argv[0], urllib.quote_plus(i['url']))))
            item = control.item(i['name'], iconImage=i['image'], thumbnailImage=i['image'])
            item.addContextMenuItems(cm, replaceItems=True)
            item.setProperty('fanart_image', fanart)
            item.setProperty('Video', 'true')
            item.setProperty('IsPlayable', 'true')
            control.addItem(handle=int(sys.argv[1]), url=i['url'], listitem=item)
        except:
            pass

    control.directory(int(sys.argv[1]), cacheToDisc=True)


def addDownload(name, url, image, resolved=False):
    if resolved:
        resolved = url
    try:
        def download(): return []
        result = cache.get(download, 600000000, table='rel_dl')
        result = [i['name'] for i in result]
    except:
        pass

    if name in result:
        return control.infoDialog('Stavka je već dodana u red čekanja', name)

    try:
        if not resolved:
            import urlresolver
            resolved = urlresolver.resolve(url)
    except:
        return control.infoDialog('Unplayable stream')
        pass

    try:
        u = resolved.split('|')[0]
        try: headers = dict(urlparse.parse_qsl(url.rsplit('|', 1)[1]))
        except: headers = dict('')

        ext = os.path.splitext(urlparse.urlparse(u).path)[1][1:].lower()
        if ext == 'm3u8': raise Exception()
        #if not ext in ['mp4', 'mkv', 'flv', 'avi', 'mpg']: ext = 'mp4'
        try:    name = name.decode('utf-8')
        except: pass
        name=re.sub('[^-a-zA-Z0-9_.() ]+', '', name)
        name=name.rstrip('.')
        dest = name + '.' + ext

        req = urllib2.Request(u, headers=headers)
        resp = urllib2.urlopen(req, timeout=30)
        size = int(resp.headers['Content-Length'])
        size = ' %.2f GB' % (float(size) / 1073741824)

        no = control.yesnoDialog(dest, 'Veličina datoteke je ' + size, 'Nastaviti s preuzimanjem?', name + ' - ' + 'Potvrdi preuzimanje', 'Potvrdi', 'Prekini')

        if no: return
    except:
        return control.infoDialog('Nije moguće preuzeti')
        pass

    def download(): return [{'name': name, 'url': url, 'image': image}]
    result = cache.get(download, 600000000, table='rel_dl')
    result = [i for i in result if not i['url'] == url]
    def download(): return result + [{'name': name, 'url': url, 'image': image}]
    result = cache.get(download, 0, table='rel_dl')

    control.infoDialog('Datoteka dodana u red čekanja', name)


def removeDownload(url):
    try:
        def download(): return []
        result = cache.get(download, 600000000, table='rel_dl')
        if result == '': result = []
        result = [i for i in result if not i['url'] == url]
        if result == []: result = ''

        def download(): return result
        result = cache.get(download, 0, table='rel_dl')

        control.refresh()
    except:
        control.infoDialog('Morate ručno ukloniti datoteku', 'Nije moguće ukloniti datoteku')


def startDownload():
    if downloadPath == '':
        return control.infoDialog('Prvo postavite mapu preuzimanja u postavkama', 'Datoteka nije preuzeta')

    control.execute('RunPlugin(%s?mode=startDownloadThread)' % sys.argv[0])


def startDownloadThread():
    dlThread = downloadThread()
    dlThread.start()


def stopDownload():
    dlThread = downloadThread()
    dlThread.kill()


def statusDownload():
    window = MyDownloads('Status/Informacije o preuzimanju')
    window.doModal()
    del window


class MyDownloads(pyxbmct.AddonDialogWindow):

    def __init__(self, title='downloadThread'):
        super(MyDownloads, self).__init__(title)
        self.setGeometry(700, 450, 9, 3)
        self.set_info_controls()
        self.set_active_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)


    def set_info_controls(self):
        self.placeControl(pyxbmct.Label('[B][COLOR gold]'+control.window.getProperty(property + '.name')+'[/COLOR][/B]', alignment=pyxbmct.ALIGN_CENTER), 0, 1, 1, 1)

        self.placeControl(pyxbmct.Label('Veličina datoteke', alignment=pyxbmct.ALIGN_CENTER), 1, 0)
        self.placeControl(pyxbmct.Label(control.window.getProperty(property + '.size'), alignment=pyxbmct.ALIGN_CENTER), 2, 0)

        self.placeControl(pyxbmct.Label('Preuzeto', alignment=pyxbmct.ALIGN_CENTER), 1, 1)
        self.placeControl(pyxbmct.Label(control.window.getProperty(property + '.percent'), alignment=pyxbmct.ALIGN_CENTER), 2, 1)

        self.placeControl(pyxbmct.Label('Brzina preuzimanja', alignment=pyxbmct.ALIGN_CENTER), 1, 2)
        self.placeControl(pyxbmct.Label(control.window.getProperty(property + '.speed'), alignment=pyxbmct.ALIGN_CENTER), 2, 2)

        self.placeControl(pyxbmct.Image(control.window.getProperty(property + '.image')), 3, 1, 6, 1)


    def set_active_controls(self):
        self.button = pyxbmct.Button('Zatvori')
        self.placeControl(self.button, 8, 2)
        self.connect(self.button, self.close)

        self.button2 = pyxbmct.Button('Zaustavi preuzimanje')
        self.placeControl(self.button2, 8, 0)
        self.connect(self.button2, lambda: self.stopDownload())


    def set_navigation(self):
        self.button.controlUp(self.button2)
        self.button.controlDown(self.button2)
        self.button.controlRight(self.button2)
        self.button.controlLeft(self.button2)
        self.button2.controlUp(self.button)
        self.button2.controlDown(self.button)
        self.button2.controlRight(self.button)
        self.button2.controlLeft(self.button)
        self.setFocus(self.button)


    def setAnimation(self, control):
        control.setAnimations([('WindowOpen', 'effect=fade start=0 end=100 time=200',), ('WindowClose', 'effect=fade start=100 end=0 time=300',)])


    def stopDownload(self):
        stopDownload()
        self.close()


class downloadThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)


    def run(self):
        def download(): return []
        result = cache.get(download, 600000000, table='rel_dl')

        for item in result:
            self.name = item['name'] ; self.image = item['image'] ; self.url = item['url']

            sysname = self.name.translate(None, '\/:*?"<>|').strip('.')

            url = self.url.split('|')[0]
            try: headers = dict(urlparse.parse_qsl(self.url.rsplit('|', 1)[1]))
            except: headers = dict('')

            ext = os.path.splitext(urlparse.urlparse(url).path)[1][1:].lower()
            if not ext in ['mp4', 'mkv', 'flv', 'avi', 'mpg', 'mp3']: ext = 'mp4'

            dest = os.path.join(downloadPath, 'CoD Preuzimanja')
            control.makeFile(dest)


            dest = os.path.join(dest, sysname + '.' + ext)

            control.infoDialog(self.name + ' se preuzima', 'Preuzimanja pokrenuta', self.image, time=7000)

            try:
                req = urllib2.Request(url, headers=headers)
                resp = urllib2.urlopen(req, timeout=30)
            except Exception,e:
                removeDownload(self.url)
                print '%s ERROR - File Failed To Open' % (dest)
                continue

            try: self.size = int(resp.headers['Content-Length'])
            except: self.size = 0

            if self.size < 1:
                removeDownload(self.url)
                print '%s Unknown filesize - Unable to download' % (dest)
                continue

            try:  resumable = 'bytes' in resp.headers['Accept-Ranges'].lower()
            except: resumable = False

            size = 1024 * 1024
            if self.size < size: size = self.size

            gb = '%.2f GB' % (float(self.size) / 1073741824)

            start = time.clock()

            total = 0 ; notify = 0 ; errors = 0 ; count = 0 ; resume = 0 ; sleep = 0

            self.clear()

            control.window.setProperty(property + '.status', 'downloading')
            control.window.setProperty(property + '.name', str(self.name))
            control.window.setProperty(property + '.image', str(self.image))
            control.window.setProperty(property + '.size', str(gb))

            f = control.openFile(dest, 'wb')

            chunk  = None
            chunks = []

            while True:
                downloaded = total
                for c in chunks:
                    downloaded += len(c)

                percent = min(100 * downloaded / self.size, 100)
                
                self.speed = str(int((downloaded / 1024) / (time.clock() - start))) + ' KB/s'
                self.percent = str(percent) + '%'

                control.window.setProperty(property + '.percent', str(self.percent))
                control.window.setProperty(property + '.speed', str(self.speed))

                if percent >= notify:
                    control.infoDialog('Preuzeto %s' % self.percent, self.name, self.image, time=5000)
                    notify += 10


                chunk = None
                error = False

                try:        
                    chunk  = resp.read(size)
                    if not chunk:
                        if self.percent < 99:
                            error = True
                        else:
                            while len(chunks) > 0:
                                c = chunks.pop(0)
                                f.write(c)
                                del c

                            f.close()
                            print '%s download complete' % (dest)
                            break

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
                    control.sleep(sleep*1000)

                if (resumable and errors > 0) or errors >= 10:
                    if (not resumable and resume >= 50) or resume >= 500:
                        #Give up!
                        print '%s download canceled - too many error whilst downloading' % (dest)
                        break

                    resume += 1
                    errors  = 0
                    if resumable:
                        chunks  = []
                        #create new response
                        print 'Download resumed (%d) %s' % (resume, dest)
                        h = headers ; h['Range'] = 'bytes=%d-' % int(total)
                        try: resp = urllib2.urlopen(urllib2.Request(url, headers=h), timeout=10)
                        except: resp = None
                    else:
                        #use existing response
                        pass

                if control.window.getProperty(property + '.status') == 'stop':
                    control.infoDialog('Proces završen', 'Preuzimanja', time=5000)
                    return self.clear()


            self.clear()

            control.infoDialog(self.name + ' Dovršeno', 'Preuzimanje dovršeno', self.image, time=5000)
            removeDownload(self.url)


        control.infoDialog('Proces završen', 'Preuzimanja', time=5000)
        return


    def kill(self):
        control.window.setProperty(property + '.status', 'stop')


    def clear(self):
        control.window.clearProperty(property + '.status') 
        control.window.clearProperty(property + '.name')
        control.window.clearProperty(property + '.image')
        control.window.clearProperty(property + '.percent')
        control.window.clearProperty(property + '.speed')
        control.window.clearProperty(property + '.size')
        control.refresh()

