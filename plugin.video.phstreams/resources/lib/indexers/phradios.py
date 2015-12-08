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


import sys,urllib
from resources.lib.libraries import control
from resources.lib.libraries import client


mediaPath = control.addonInfo('path') + '/resources/media/phradios/'


def radioDirectory():
    addCategoryItem('1FM', 'radio1fm', '1fm-icon.png', '1fm-fanart.jpg')
    addCategoryItem('181FM', 'radio181fm', '181fm-icon.png', '181fm-fanart.jpg')
    addCategoryItem('RadioTunes', 'radiotunes', 'radiotunes-icon.png', 'radiotunes-fanart.jpg')
    endCategory()


def radio1fm(image, fanart):
    try:
        url = 'http://1.fm/home/showstations?stations=showall'

        result = client.request(url)
        a = client.parseDOM(result, 'div', attrs={'class': 'staionitemcont'})
        b = client.parseDOM(result, 'div', attrs={'class': 'contbtnrgt'})
        items = zip(a, b)
    except:
        return

    for item in items:
        try:
            name = client.parseDOM(item[1], 'a', ret='rel')[0]
            name = client.replaceHTMLCodes(name)
            name = name.encode('utf-8')

            url = client.parseDOM(item[1], 'a', ret='data-scsrv')[0]
            if not url.startswith('http'): url = 'http://%s' % url
            url += ':%s' % client.parseDOM(item[1], 'a', ret='data-hiaac')[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            thumb = client.parseDOM(item[0], 'img', ret='src')[0]
            thumb = thumb.rsplit('?', 1)[0]
            thumb = client.replaceHTMLCodes(thumb)
            thumb = thumb.encode('utf-8')

            addDirectoryItem(name, url, thumb, image, fanart)
        except:
            pass

    endDirectory()


def radio181fm(image, fanart):
    try:
        url = 'http://www.181.fm/index.php?p=mp3links'

        result = client.request(url)
        items = client.parseDOM(result, 'td', attrs={'id': 'rightlinks'})
    except:
        pass

    for item in items:
        try:
            if not item.startswith('http://'): raise Exception()

            name = items[:items.index(item)]
            name = [i for i in name if not 'http://' in i][-1]
            name = client.replaceHTMLCodes(name)
            name = name.encode('utf-8')

            url = item
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            addDirectoryItem(name, url, '0', image, fanart)
        except:
            pass

    endDirectory()


def radiotunes(image, fanart):
    try:
        url = 'http://radiotunes.com/channels'

        result = client.request(url)
        result = client.parseDOM(result, 'ul', attrs={'id': 'channel-nav'})[0]
        items = client.parseDOM(result, 'li')
    except:
        pass

    for item in items:
        try:
            name = client.parseDOM(item, 'span')[0]
            name = client.replaceHTMLCodes(name)
            name = name.encode('utf-8')

            url = client.parseDOM(item, 'a', ret='href')[0]
            url = url.replace('/', '')
            url = 'http://pub7.radiotunes.com:80/radiotunes_%s_aac' % url
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            thumb = client.parseDOM(item, 'img', ret='src')[0]
            thumb = thumb.rsplit('?', 1)[0]
            if thumb.startswith('//'): thumb = 'http:%s' % thumb
            thumb = client.replaceHTMLCodes(thumb)
            thumb = thumb.encode('utf-8')

            addDirectoryItem(name, url, thumb, image, fanart)
        except:
            pass

    endDirectory()


def addCategoryItem(name, action, image, fanart, isFolder=True):
    u = '%s?action=%s&image=%s&fanart=%s' % (sys.argv[0], str(action), urllib.quote_plus(image), urllib.quote_plus(fanart))
    item = control.item(name, iconImage=mediaPath+image, thumbnailImage=mediaPath+image)
    item.addContextMenuItems([], replaceItems=False)
    item.setProperty('Fanart_Image', mediaPath+fanart)
    control.addItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=isFolder)


def endCategory():
    if control.skin == 'skin.confluence': control.execute('Container.SetViewMode(500)')
    control.directory(int(sys.argv[1]), cacheToDisc=True)


def addDirectoryItem(name, url, thumb, image, fanart):
    if not thumb == '0': image = thumb

    u = '%s?action=radioResolve&name=%s&url=%s&image=%s&fanart=%s' % (sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image), urllib.quote_plus(fanart))

    if not image.startswith('http://'): image = mediaPath+image
    meta = {'title': name, 'album': name, 'artist': name, 'comment': name}

    item = control.item(name, iconImage=image, thumbnailImage=image)
    item.setInfo(type='Music', infoLabels = meta)
    item.addContextMenuItems([], replaceItems=False)
    item.setProperty('Fanart_Image', mediaPath+fanart)
    #item.setProperty('IsPlayable', 'true')
    control.addItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=False)


def endDirectory():
    control.directory(int(sys.argv[1]), cacheToDisc=True)


def radioResolve(name, url, image):
    if not image.startswith('http://'): image = mediaPath+image
    meta = {'title': name, 'album': name, 'artist': name, 'comment': name}
    item = control.item(path=url, iconImage=image, thumbnailImage=image)
    item.setInfo(type='Music', infoLabels = meta)
    control.player.play(url, item)


