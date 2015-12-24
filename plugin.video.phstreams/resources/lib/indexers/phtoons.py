# -*- coding: utf-8 -*-

'''
    Phoenix Add-on
    Copyright (C) 2015 Blazetamer
    Copyright (C) 2015 lambda

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


import xbmc
import re,sys,urllib,urlparse,base64
from resources.lib.libraries import control
from resources.lib.libraries import client
from resources.lib.libraries import cloudflare


mediaPath = control.addonInfo('path') + '/resources/media/phtoons/'


def CartoonDirectory():
    addDirectoryItem('Cartoon Crazy', 'CartoonCrazy', '0', mediaPath+'CartoonCrazy-icon.png', mediaPath+'CartoonCrazy-fanart.jpg')
    endCategory()


def CartoonCrazy(image, fanart):

    addDirectoryItem('[B]SEARCH[/B]', 'CCsearch', '0', mediaPath+'CCsearch.png', fanart, '')

    try:
        url = 'http://kisscartoon.me/CartoonList/'

        result = cloudflare.request(url)

        items = client.parseDOM(result, 'div', attrs={'id': 'container'})
        items = client.parseDOM(items, 'div', attrs={'id': 'rightside'})
        items = client.parseDOM(items, 'div', attrs={'class': 'barContent'})[1]       
        items = client.parseDOM(items, 'a', ret='href')
    except:
        return

    for item in items:
        try:
            name = '[B]'+ item[7:] +'[/B]'
            name = client.replaceHTMLCodes(name)
            name = name.encode('utf-8')

            url = item
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            addDirectoryItem(name, 'CCcat', image, image, fanart, url)
        except:
            pass

    endDirectory()


def CCcat(url, image, fanart):
    try:
        url = urlparse.urljoin('http://kisscartoon.me', url)

        result = cloudflare.request(url)
        result = re.sub('<tr\s+.+?>', '<tr>', result)

        items = client.parseDOM(result, 'tr')
    except:
        return

    for item in items:
        try:
            name = client.parseDOM(item, 'a')[0]
            name = name.replace('\n', '')
            name = '[B]'+ name +'[/B]'
            name = client.replaceHTMLCodes(name)
            name = name.encode('utf-8')

            url = client.parseDOM(item, 'a', ret='href')[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            thumb = client.parseDOM(item, 'img', ret='src')[0]
            thumb = thumb.replace('kisscartoon.me','cdn-c.whatbest.net')
            thumb = client.replaceHTMLCodes(thumb)
            thumb = thumb.encode('utf-8')

            addDirectoryItem(name, 'CCpart', thumb, image, fanart, url)
        except:
            pass

    try:
        next = client.parseDOM(result, 'ul', attrs={'class': 'pager'})[0]
        next = zip(client.parseDOM(next, 'a', ret='href'), client.parseDOM(next, 'a'))
        next = [i[0] for i in next if 'Next' in i[1]][0]

        addDirectoryItem('[I]NEXT[/I]', 'CCcat', image, image, fanart, next)
    except:
        pass

    movieCategory()


def CCsearch(url, image, fanart):
    keyboard = control.keyboard('', control.lang(30702).encode('utf-8'))
    keyboard.setHeading('CARTOON SEARCH')
    keyboard.doModal()

    if not keyboard.isConfirmed(): return

    search = keyboard.getText()
    search = re.sub(r'\W+|\s+','-', search)
    if search == '': return

    url = '/Search/Cartoon/'+search
    url = url.encode('utf-8')

    CCcat(url, image, fanart)


def CCpart(url, image, fanart):
    try:
        url = urlparse.urljoin('http://kisscartoon.me', url)

        result = cloudflare.request(url)

        items = client.parseDOM(result, 'table', attrs={'class': 'listing'})
        items = client.parseDOM(items, 'td')
        items = zip(client.parseDOM(items, 'a', ret='href'), client.parseDOM(items, 'a'))

        if len(items) == 1: return CCstream(items[0][0])
    except:
        return

    for item in items[::-1]:
        try:
            name = item[1]
            name = name.replace('\n', '')
            name = client.replaceHTMLCodes(name)
            name = name.encode('utf-8')

            url = item[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            addDirectoryItem(name,'CCstream',image,image,fanart,url)
        except:
            pass

    episodeCategory()


def CCstream(url):
    try:
        control.idle()

        url = urlparse.urljoin('http://kisscartoon.me', url)

        result = cloudflare.request(url)

        items = client.parseDOM(result,'select', attrs={'id':'selectQuality'}) 
        items = client.parseDOM(items, 'option', ret='value')

        url = []

        for item in items:
            try:
                u = base64.b64decode(item)
                u = u.encode('utf-8')

                if u[-3:] == 'm37': q = '1080P'
                elif u[-3:] == 'm22': q = '720P'
                elif u[-3:] == 'm18': q = '360P'
                else: q = 'UNKNOWN'

                url.append({'q': q, 'u': u})
            except:
                pass

        if len(url) > 1:
            q = [i['q'] for i in url]
            u = [i['u'] for i in url]
            select = control.selectDialog(q)
            if select == -1: return
            url = u[select]

        else:
            url = url[0]['u']

        player().run(url)
    except:
        return



def addDirectoryItem(name, action, thumb, image, fanart, url='0'):
    if thumb == '0': thumb = image
    u = '%s?action=%s&url=%s&image=%s&fanart=%s' % (sys.argv[0], str(action), urllib.quote_plus(url), urllib.quote_plus(thumb), urllib.quote_plus(fanart))
    item = control.item(name, iconImage=thumb, thumbnailImage=thumb)
    item.addContextMenuItems([], replaceItems=False)
    item.setProperty('Fanart_Image', fanart)
    control.addItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=True)


def endDirectory():
    control.directory(int(sys.argv[1]), cacheToDisc=True)


def endCategory():
    if control.skin == 'skin.confluence': control.execute('Container.SetViewMode(500)')
    control.directory(int(sys.argv[1]), cacheToDisc=True)


def movieCategory():
    control.content(int(sys.argv[1]), 'movies')
    if control.skin == 'skin.confluence': control.execute('Container.SetViewMode(500)')
    control.directory(int(sys.argv[1]), cacheToDisc=True)


def episodeCategory():
    control.content(int(sys.argv[1]), 'episodes')
    control.directory(int(sys.argv[1]), cacheToDisc=True)


class player(xbmc.Player):
    def __init__ (self):
        xbmc.Player.__init__(self)

    def run(self, url):
        title = control.infoLabel('ListItem.Label')
        image = control.infoLabel('ListItem.Icon')
        item = control.item(path=url, iconImage=image, thumbnailImage=image)
        item.setInfo(type='Video', infoLabels = {'title': title})
        control.player.play(url, item)

        for i in range(0, 240):
            if self.isPlayingVideo(): break
            control.sleep(1000)

    def onPlayBackStarted(self):
        control.sleep(200)
        control.idle()


