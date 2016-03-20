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
import re,sys,urllib,urllib2,urlparse,random,base64
from resources.lib.modules import control
from resources.lib.modules import client
from resources.lib.modules import cloudflare
from resources.lib.modules import directstream


cartoonArt = 'http://phoenixtv.offshorepastebin.com/art/cartoon/art%s.png'
animeArt = 'http://phoenixtv.offshorepastebin.com/art/anime/art%s.png'


def cartoon():
    addDirectoryItem('Cartoon Search', 'CCsearch', '0', cartoonArt % (random.randint(1,10)), 'http://phoenixtv.offshorepastebin.com/art/cartoon/fanart.jpg')
    addDirectoryItem('Cartoon Genres', 'CartoonCrazy', '0', cartoonArt % (random.randint(1,10)), 'http://phoenixtv.offshorepastebin.com/art/cartoon/fanart.jpg')
    addDirectoryItem('Anime Search','ACsearch', '0', animeArt % (random.randint(1,12)), 'http://phoenixtv.offshorepastebin.com/art/anime/fanart.jpg')
    addDirectoryItem('Anime Genres','AnimeCrazy', '0', animeArt % (random.randint(1,12)), 'http://phoenixtv.offshorepastebin.com/art/anime/fanart.jpg')
    addDirectoryItem('Anime Latest','AClast', '0', animeArt % (random.randint(1,12)), 'http://phoenixtv.offshorepastebin.com/art/anime/fanart.jpg')
    endCategory()



def CartoonCrazy(image, fanart):
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
            name = item[7:].upper()
            name = client.replaceHTMLCodes(name)
            name = name.encode('utf-8')

            url = item
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            addDirectoryItem(name, 'CCcat', cartoonArt % (random.randint(1,10)), image, fanart, url)
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

        addDirectoryItem('[I]NEXT[/I]', 'CCcat', cartoonArt % (random.randint(1,10)), image, fanart, next)
    except:
        pass

    movieCategory()


def CCsearch(url, image, fanart):
    keyboard = control.keyboard('', control.lang(30702).encode('utf-8'))
    keyboard.setHeading(control.infoLabel('ListItem.Label'))
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
        url = urlparse.urljoin('http://kisscartoon.me', url)

        result = cloudflare.request(url)

        url = []
        items = client.parseDOM(result,'select', attrs={'id':'selectQuality'}) 
        items = client.parseDOM(items, 'option', ret='value')
        for i in items:
            try: url.append({'q': directstream.googletag(base64.b64decode(i))[0]['quality'], 'u': base64.b64decode(i)})
            except: pass
        items = sorted(url, key=lambda k: k['q'])

        player().run(items[0]['u'])
    except:
        return


  
def AnimeCrazy(image, fanart):
    try:
        url = 'http://www.animedreaming.tv/genres/'

        result = client.request(url)

        items = client.parseDOM(result, 'ul', attrs={'class': 'genre_page_box'})[0]
        items = client.parseDOM(items, 'li') 
    except:
        return

    for item in items:
        try:
            name =client.parseDOM(item, 'a')[0]
            name = name.upper()
            name = client.replaceHTMLCodes(name)
            name = name.encode('utf-8')

            url = client.parseDOM(item, 'a', ret='href')[0]
            url = urlparse.urljoin('http://www.animedreaming.tv', url)
            url = url.replace(' ','%20')
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            addDirectoryItem(name, 'ACcat', animeArt % (random.randint(1,12)), image, fanart, url+'/?filter=newest&req=anime')
        except:
            pass

    endDirectory()    
    

def ACcat(url, image, fanart):   
    try:
        result = client.request(url)

        items = client.parseDOM(result, 'div', attrs={'id': 'left_content'})[0]
        items = client.parseDOM(items, 'li')
    except:
        return

    for item in items:
        try:
            name = client.parseDOM(item, 'a')[0]
            if '>Movie<' in name: raise Exception()
            name = re.sub('<.+?>|</.+?>|\\\\|\n', '', name).strip()
            name = client.replaceHTMLCodes(name)
            name = name.encode('utf-8')

            url = client.parseDOM(item, 'a', ret='href')[0]
            url = urlparse.urljoin('http://www.animedreaming.tv', url)
            url = url.replace(' ','%20')
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            thumb = [i for i in url.split('/') if not i == ''][-1]
            thumb = 'http://www.animedreaming.tv/anime-images-big/%s.jpg' % thumb
            thumb = thumb.encode('utf-8')
        
            addDirectoryItem(name, 'ACpart', thumb, image, fanart, url)
        except:
            pass

    movieCategory()


def ACsearch(url, image, fanart):
    keyboard = control.keyboard('', control.lang(30702).encode('utf-8'))
    keyboard.setHeading(control.infoLabel('ListItem.Label'))
    keyboard.doModal()
    if not keyboard.isConfirmed(): return

    search = keyboard.getText()
    search = re.sub(r'\W+|\s+','+', search)
    if search == '': return

    url = 'http://www.animedreaming.tv/search.php?searchquery='+search
    url = url.encode('utf-8')

    ACcat(url, image, fanart)


def AClast(url, image, fanart):   
    try:
        url = 'http://www.animedreaming.tv/latest-anime-episodes/'

        result = client.request(url)

        items = client.parseDOM(result, 'div', attrs={'id': 'left_content'})[0]
        items = client.parseDOM(items, 'zi')
    except:
        return

    for item in items:
        try:
            name = client.parseDOM(item, 'a')[0]
            if '>Movie<' in name: raise Exception()
            name = re.sub('<.+?>|</.+?>|\\\\|\n', '', name).strip()
            name = client.replaceHTMLCodes(name)
            name = name.encode('utf-8')

            url = client.parseDOM(item, 'a', ret='href')[0]
            url = urlparse.urljoin('http://www.animedreaming.tv', url)
            url = url.replace(' ','%20')
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            thumb = client.parseDOM(item, 'img', ret='src')[0]
            thumb = urlparse.urljoin('http://www.animedreaming.tv', thumb)
            thumb = thumb.replace(' ','%20')
            thumb = client.replaceHTMLCodes(thumb)
            thumb = thumb.encode('utf-8')

            addDirectoryItem(name, 'ACstream', thumb, image, fanart, url)
        except:
            pass

    episodeCategory()


def ACpart(url, image, fanart):
    try:
        result = client.request(url)

        index = []
        items = client.parseDOM(result, 'ul', attrs={'class': 'cat_page_box'})[-1]
        items = client.parseDOM(items, 'li')
    except:
        return

    for item in items[::-1]:
        try:
            name = client.parseDOM(item, 'a')[0]
            name = re.sub('<.+?>|</.+?>|\\\\|\n', ' ', name).strip()
            name = re.sub('Watch$', '', name).strip()
            name = client.replaceHTMLCodes(name)
            name = name.encode('utf-8')

            url = client.parseDOM(item, 'a', ret='href')[0]
            url = urlparse.urljoin('http://www.animedreaming.tv', url)
            url = url.replace(' ','%20')
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            index.append({'name': name, 'url': url})
        except:
            pass

    if len(index) == 1: return ACstream(index[0]['url'])

    for i in index: addDirectoryItem(i['name'], 'ACstream', image, image, fanart, i['url'])

    episodeCategory()


def ACstream(url):
    try:
        import urlresolver

        result = client.request(url)

        items = client.parseDOM(result, 'div', attrs = {'class': 'generic-video-item'})
        items = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'span', attrs = {'class': 'type'})) for i in items]
        items = [(i[0][0], i[1][0].lower()) for i in items if len(i[0]) > 0 and len(i[1]) > 0]


        host = 'veevr'
        pattern = '(?://|\.)(veevr.com)/(?:videos|embed)/([A-Za-z0-9]+)'
        link = 'http://veevr.com/embed/%s'

        try: url = [link % re.search(pattern, result).groups()[1]]
        except: url = []
        try: url += [i[0] for i in items if i[1] == host]
        except: pass
        for i in url:
            try:
                if 'animedreaming.' in i: i = link % re.search(pattern, client.request(i)).groups()[1]

                u = client.request(i)
                u = client.parseDOM(u, 'source', ret='src', attrs = {'type': 'video.+?'})[-1]
                u = client.request(u, output='geturl')

                r = int(urllib2.urlopen(u, timeout=15).headers['Content-Length'])
                if r > 1048576: return player().run(u)
            except:
                pass


        host = 'mp4upload'
        pattern = '(?://|\.)(mp4upload\.com)/(?:embed-)?([0-9a-zA-Z]+)'
        link = 'http://www.mp4upload.com/embed-%s.html'

        try: url = [link % re.search(pattern, result).groups()[1]]
        except: url = []
        try: url += [i[0] for i in items if i[1] == host]
        except: pass
        for i in url:
            try:
                if 'animedreaming.' in i: i = link % re.search(pattern, client.request(i)).groups()[1]

                u = urlresolver.HostedMediaFile(i).resolve()
                if not u == False: return player().run(u)
            except:
                pass


        host = 'engine'
        pattern = '(?://|\.)(auengine\.com)/embed.php\?file=([0-9a-zA-Z\-_]+)[&]*'
        link = 'http://www.auengine.com/embed.php?file=%s'

        try: url = [link % re.search(pattern, result).groups()[1]]
        except: url = []
        try: url += [i[0] for i in items if i[1] == host]
        except: pass
        for i in url:
            try:
                if 'animedreaming.' in i: i = link % re.search(pattern, client.request(i)).groups()[1]

                u = urlresolver.HostedMediaFile(i).resolve()
                if not u == False: return player().run(u)
            except:
                pass
    except:
        return



def addDirectoryItem(name, action, thumb, image, fanart, url='0'):
    if thumb == '0': thumb = image
    u = '%s?action=%s&url=%s&image=%s&fanart=%s' % (sys.argv[0], str(action), urllib.quote_plus(url), urllib.quote_plus(thumb), urllib.quote_plus(fanart))
    item = control.item(name, iconImage=thumb, thumbnailImage=thumb)

    try: item.setArt({'poster': thumb, 'tvshow.poster': thumb, 'season.poster': thumb, 'banner': thumb, 'tvshow.banner': thumb, 'season.banner': thumb})
    except: pass
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
        control.idle()
        title = control.infoLabel('ListItem.Label')
        image = control.infoLabel('ListItem.Icon')
        item = control.item(path=url, iconImage=image, thumbnailImage=image)
        try: item.setArt({'icon': image})
        except: pass
        item.setInfo(type='Video', infoLabels = {'title': title})
        control.player.play(url, item)

        for i in range(0, 240):
            if self.isPlayingVideo(): break
            control.sleep(1000)

    def onPlayBackStarted(self):
        control.sleep(200)
        control.idle()


