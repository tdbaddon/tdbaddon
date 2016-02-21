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


import os,re,sys,base64,urllib,urlparse,random
import xbmc

from resources.lib.modules import cache
from resources.lib.modules import cachemeta
from resources.lib.modules import control
from resources.lib.modules import client
from resources.lib.modules import workers
from resources.lib.modules import views


phLink = 'http://mecca.watchkodi.com/phstreams.xml'
phNews = 'http://mecca.watchkodi.com/news.xml'
phSearch = 'http://%s/search/search.xml'
phTest = 'testings.xml'


def getCategory():
    getDirectory('0', phLink, '0', '0', '0', '0', close=False)
    addCategoryItem('VinMan FM', 'radioDirectory', 'radios.png')
    addCategoryItem('Cartoon Crazy','CartoonDirectory','cartoon.png')
    addCategoryItem('NHL', 'nhlDirectory', 'hockey.jpg')
    addCategoryItem('News Updates', 'dmode&url=%s' % phNews, 'news.gif')
    addCategoryItem(control.lang(30701).encode('utf-8'), 'openSettings', 'settings.png')
    addCategoryItem(control.lang(30721).encode('utf-8'), 'downloader', 'downloader.png')
    addCategoryItem(control.lang(30702).encode('utf-8'), 'search', 'search.png')

    if phTest in control.listDir(control.dataPath)[1]: addCategoryItem('Testings', 'localDirectory', 'home.png')

    endCategory()


def localDirectory():
    getDirectory('0', os.path.join(control.dataPath, phTest), '0', '0', '0', '0', local=True)


def getDirectory(name, url, audio, image, fanart, content, close=True, local=False):
    if local == True:
        f = control.openFile(url) ; result = f.read() ; f.close()
    else:
        result = cache.get(client.request, 0, url)

    try: r = base64.b64decode(result)
    except: r = ''
    if '</' in r: result = r

    result = str(result).replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')

    try: fanart = re.findall('<fanart>(.+?)</fanart>', result)[0]
    except: fanart = '0'


    try:
        notify = re.compile('<notify>(.+?)</notify>').findall(result)[0]

        vip = re.findall('<poster>(.+?)</poster>', result)[0]
        if not re.search('[a-zA-Z]', vip): raise Exception()

        def message(vip): return (vip+version)

        check = cache.get(message, 600000000, vip, table='rel_vip')

        version = re.findall('<new>(.+?)</new>', notify)[0]
        if not version.isdigit(): raise Exception()

        if check == (vip+version): raise Exception()

        title = '[B]Announcement From %s![/B]' % vip
        msg1 = re.findall('<message1>(.+?)</message1>', notify)[0]
        msg2 = re.findall('<message2>(.+?)</message2>', notify)[0]
        msg3 = re.findall('<message3>(.+?)</message3>', notify)[0]

        check = cache.get(message, 0, vip, table='rel_vip')

        control.dialog.ok(str(title), str(msg1), str(msg2), str(msg3))
    except:
        pass


    infos = re.compile('<info>(.+?)</info>').findall(result)

    for info in infos:
        try:
            name = re.findall('<message>(.+?)</message>', info)[0]

            try: image = re.findall('<thumbnail>(.+?)</thumbnail>', info)[0]
            except: image = '0'

            addDirectoryItem(name, '0', '0', image, image, fanart, '0', '0', {})
        except:
            pass


    popups = re.compile('<popup>(.+?)</popup>').findall(result)

    for popup in popups:
        try:
            name = re.findall('<name>(.+?)</name>', popup)[0]

            url = re.findall('<popImage>(.+?)</popImage>', popup)[0]

            try: image = re.findall('<thumbnail>(.+?)</thumbnail>', popup)[0]
            except: image = '0'

            try: audio = re.findall('<sound>(.+?)</sound>', popup)[0]
            except: audio = '0'

            addDirectoryItem(name, url, 'openDialog', image, image, fanart, audio, '0', {})
        except:
            pass


    special = re.compile('<name>([^<]+)</name><link>([^<]+)</link><thumbnail>([^<]+)</thumbnail><date>([^<]+)</date>').findall(result)
    for name, url, image, date in special:
        if re.search(r'\d+', date): name += ' [COLOR red] Updated %s[/COLOR]' % date
        addDirectoryItem(name, url, 'ndmode', image, image, fanart, '0', '0', {})

    special = re.compile('<name>([^<]+)</name><link>([^<]+)</link><thumbnail>([^<]+)</thumbnail><mode>([^<]+)</mode>').findall(result)
    for name, url, image, action in special:
        if not url == phNews: addDirectoryItem(name, url, action, image, image, fanart, '0', '0', {})



    meta = False

    try: content = re.findall('<meta>(.+?)</meta>', result)[0]
    except: content = '0'

    try: tvshow = re.findall('<tvshow>(.+?)</tvshow>', result)[0]
    except: tvshow = '0'

    if content in ['seasons', 'episodes'] and tvshow == '0':
        content = '0'

    if content in ['movies', 'tvshows'] and control.setting('meta') == 'true':
        try:
            from metahandler import metahandlers
            metaget = metahandlers.MetaData(preparezip=False)
            meta = True
        except:
            meta = False

    elif content in ['seasons', 'episodes']:
        try:
            from metahandler import metahandlers
            metaget = metahandlers.MetaData(preparezip=False)
            #tvd = metaget.get_meta('tvshow', tvshow)
            tvd = cachemeta.get(metaget.get_meta, 24, 'tvshow', tvshow, '', '', '')
        except:
            tvd = {}


    dirs = re.compile('<dir>(.+?)</dir>').findall(result)

    totalItems = len(dirs)

    for dir in dirs:
        try:
            data = {}

            name = re.findall('<name>(.+?)</name>', dir)[0]

            url = re.findall('<link>(.+?)</link>', dir)[0]

            try: image = re.findall('<thumbnail>(.+?)</thumbnail>', dir)[0]
            except: image = '0'

            try: fanart2 = re.findall('<fanart>(.+?)</fanart>', dir)[0]
            except: fanart2 = fanart

            if meta == True and content =='tvshows':
                try:
                    title = cleantitle(name).encode('utf-8')
                    data = {'title': title, 'tvshowtitle': title}

                    #data = metaget.get_meta('tvshow', title)
                    data = cachemeta.get(metaget.get_meta, 24, 'tvshow', title, '', '', '')

                    metafanart = data['backdrop_url']
                    if not metafanart == '': fanart2 = metafanart
                except:
                    pass

            elif content =='tvshows':
                try:
                    title = cleantitle(name).encode('utf-8')
                    data = {'title': title, 'tvshowtitle': title}
                except:
                    pass

            elif content =='seasons':
                try:
                    title = cleantitle(tvshow).encode('utf-8')
                    data = {'title': title, 'tvshowtitle': title}

                    data.update(tvd)

                    metafanart = tvd['backdrop_url']
                    if not metafanart == '': fanart2 = metafanart
                except:
                    pass
            if ("HUDDLE") in name:
               
                addDirectoryItem(name,'', url, image, image, fanart2, '0', content, data,totalItems=totalItems)
            else:
                addDirectoryItem(name, url, 'ndmode', image, image, fanart2, '0', content, data, totalItems=totalItems)
        except:
            pass

    items = re.compile('<item>(.+?)</item>').findall(result)

    try: sort = re.findall('<sort>(.+?)</sort>', result)[0]
    except: sort = ''
    if sort == 'yes': items = sorted(items)
    totalItems = len(items)

    for item in items:
        try:

            data = {}

            name = re.findall('<title>(.+?)</title>', item)[0]

            url = re.findall('<link>(.+?)</link>', item)[0]

            try: image = image2 = re.findall('<thumbnail>(.+?)</thumbnail>', item)[0]
            except: image = image2 = '0'

            try: fanart2 = re.findall('<fanart>(.+?)</fanart>', item)[0]
            except: fanart2 = fanart

            if meta == True and content == 'movies':
                try:
                    title = cleantitle(name).encode('utf-8')
                    data = {'title': title}

                    title, year = re.compile('(.+?)[(](\d{4})[)]').findall(name)[0]
                    title = cleantitle(title).encode('utf-8')
                    data = {'title': title, 'year': year}

                    #data = metaget.get_meta('movie', title, year=year)
                    data = cachemeta.get(metaget.get_meta, 24, 'movie', title, '', '', year)

                    metaimage = data['cover_url']
                    if not metaimage == '': image = metaimage
                    metafanart = data['backdrop_url']
                    if not metafanart == '': fanart2 = metafanart
                except:
                    pass

            elif content =='movies':
                try:
                    title = cleantitle(name).encode('utf-8')
                    data = {'title': title}

                    title, year = re.compile('(.+?)[(](\d{4})[)]').findall(name)[0]
                    title = cleantitle(title).encode('utf-8')
                    data = {'title': title, 'year': year}
                except:
                    pass

            elif content == 'episodes':
                try:
                    title = cleantitle(name).encode('utf-8')
                    data = {'title': title, 'tvshowtitle': tvshow}
                except:
                    pass
                try:
                    i = cleaneptitle(tvshow, title)
                    title, season, episode = i[0].encode('utf-8'), i[1], i[2]
                    data = {'title': title, 'tvshowtitle': tvshow, 'season': season, 'episode': episode}
                except:
                    pass
                try:
                    data.update({'year': tvd['year'], 'imdb_id' : tvd['imdb_id'], 'tvdb_id' : tvd['tvdb_id'], 'tvshowtitle': tvd['TVShowTitle'], 'genre' : tvd['genre'], 'studio': tvd['studio'], 'status': tvd['status'], 'duration' : tvd['duration'], 'rating': tvd['rating'], 'mpaa' : tvd['mpaa'], 'plot': tvd['plot'], 'cast': tvd['cast']})

                    metafanart = tvd['backdrop_url']
                    if not metafanart == '': image = fanart2 = metafanart
                except:
                    pass


            if 'sublink' in url:
                addDirectoryItem(name, url, 'subDirectory', image, image2, fanart2, '0', content, data, tvshow=tvshow, totalItems=totalItems, isFolder=True)
            else:
                addDirectoryItem(name, url, 'resolveUrl', image, image2, fanart2, '0', content, data, totalItems=totalItems, isFolder=False)
        except:
            pass

    endDirectory(content, close)


def subDirectory(name, url, audio, image, fanart, tvshow, content):
    match = re.compile('<sublink>(.+?)</sublink>').findall(url)
    if len(match) == 0: return

    try:
        title = cleantitle(name).encode('utf-8')
        data = {'title': title}
    except:
        pass

    try:
        if not content == 'movies': raise Exception()

        title = cleantitle(name).encode('utf-8')
        data = {'title': title}

        title, year = re.compile('(.+?)[(](\d{4})[)]').findall(name)[0]
        title = cleantitle(title).encode('utf-8')
        data = {'title': title, 'year': year}

        from metahandler import metahandlers
        metaget = metahandlers.MetaData(preparezip=False)

        #data = metaget.get_meta('movie', title, year=year)
        data = cachemeta.get(metaget.get_meta, 24, 'movie', title, '', '', year)

        metaimage = data['cover_url']
        if not metaimage == '': image = metaimage
        metafanart = data['backdrop_url']
        if not metafanart == '': fanart = metafanart
    except:
        pass

    try:
        if tvshow == '0' and not content == 'episodes': raise Exception()

        try:
            title = cleantitle(name).encode('utf-8')
            data = {'title': title, 'tvshowtitle': tvshow}
        except:
            pass
        try:
            i = cleaneptitle(tvshow, title)
            title, season, episode = i[0].encode('utf-8'), i[1], i[2]
            data = {'title': title, 'tvshowtitle': tvshow, 'season': season, 'episode': episode}
        except:
            pass

        from metahandler import metahandlers
        metaget = metahandlers.MetaData(preparezip=False)
        tvd = metaget.get_meta('tvshow', tvshow)
        tvd = cachemeta.get(metaget.get_meta, 24, 'tvshow', tvshow, '', '', '')

        data.update({'year': tvd['year'], 'imdb_id' : tvd['imdb_id'], 'tvdb_id' : tvd['tvdb_id'], 'tvshowtitle': tvd['TVShowTitle'], 'genre' : tvd['genre'], 'studio': tvd['studio'], 'status': tvd['status'], 'duration' : tvd['duration'], 'rating': tvd['rating'], 'mpaa' : tvd['mpaa'], 'plot': tvd['plot'], 'cast': tvd['cast']})

        metafanart = tvd['backdrop_url']
        if not metafanart == '': image = fanart = metafanart
    except:
        pass

    for i in range(0, len(match)):
        url = match[i]
        label = '%s %s %s' % (name, control.lang(30704).encode('utf-8'), str(i+1))
        addDirectoryItem(label, url, 'resolveUrl', image, image, fanart, '0', content, data, isFolder=False)

    control.directory(int(sys.argv[1]), cacheToDisc=True)


def getSearch():
    addDirectoryItem('%s...' % control.lang(30702).encode('utf-8'), '0', 'searchDirectory', '0', '0', '0', '0', '0', {})
    addDirectoryItem(control.lang(30703).encode('utf-8'), '0', 'clearSearch', '0', '0', '0', '0', '0', {})

    try:
        def search(): return
        result = cache.get(search, 600000000, table='rel_srch')
        for q in result:
                try: addDirectoryItem('%s...' % q, q, 'searchDirectory2', '0', '0', '0', '0', '0', {})
                except: pass
    except:
        pass

    control.directory(int(sys.argv[1]), cacheToDisc=True)


def searchDirectory(query=None):
    if (query == None or query == ''):
        keyboard = control.keyboard('', control.lang(30702).encode('utf-8'))
        keyboard.doModal()
        if not (keyboard.isConfirmed()): return
        query = keyboard.getText()

    if (query == None or query == ''): return

    def search(): return [query]
    result = cache.get(search, 600000000, table='rel_srch')
    def search(): return [x for y,x in enumerate((result + [query])) if x not in (result + [query])[:y]]
    result = cache.get(search, 0, table='rel_srch')


    global global_search ; global_search = []

    def worker(url):
        global_search.append(str(client.request(url)))

    servers = client.request(phLink)
    servers = str(servers).replace('\n','')
    servers = re.findall('</name><link>(.+?)</link>', servers)
    servers = [urlparse.urlparse(i).netloc for i in servers]
    servers = [phSearch % i for i in servers if not 'mecca' in i]

    threads = []
    for server in servers: threads.append(workers.Thread(worker, server))
    [i.start() for i in threads]
    [i.join() for i in threads]

    urls = []
    for i in global_search:
        try: r = base64.b64decode(i)
        except: r = ''
        if '</' in r: urls += [r]
        else: urls += [i]

    global_search = []

    urls = [str(i).replace('\n','') for i in urls]
    urls = [re.findall('<link>(.+?)</link>', i)[:30] for i in urls]
    urls = sum(urls, [])

    threads = []
    for url in urls: threads.append(workers.Thread(worker, url))
    [i.start() for i in threads]
    [i.join() for i in threads]

    links = []
    for i in global_search:
        try: r = base64.b64decode(i)
        except: r = ''
        if '</' in r: links += [r]
        else: links += [i]

    global_search = []

    for link in links:
        try:
            link = str(link).replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')

            try: fanart = re.findall('<fanart>(.+?)</fanart>', link)[0]
            except: fanart = '0'

            try: vip = re.findall('<poster>(.+?)</poster>', link)[0]
            except: vip = ''

            if vip == 'Team Phoenix': vip = ''

            try: content = re.findall('<meta>(.+?)</meta>', link)[0]
            except: content = '0'

            try: tvshow = re.findall('<tvshow>(.+?)</tvshow>', link)[0]
            except: tvshow = '0'

            if content in ['seasons', 'episodes'] and tvshow == '0':
                content = '0'


            dirs = re.compile('<dir>(.+?)</dir>').findall(link)

            for dir in dirs:
                try:
                    data = {}

                    name = re.findall('<name>(.+?)</name>', dir)[0]
                    name = cleantitle(name)

                    if not query.lower() in name.lower() : raise Exception()

                    url = re.findall('<link>(.+?)</link>', dir)[0]

                    try: image = re.findall('<thumbnail>(.+?)</thumbnail>', dir)[0]
                    except: image = '0'

                    try: fanart2 = re.findall('<fanart>(.+?)</fanart>', dir)[0]
                    except: fanart2 = fanart

                    if content =='tvshows':
                        try:
                            title = cleantitle(name).encode('utf-8')
                            data = {'title': title, 'tvshowtitle': title}
                        except:
                            pass

                    if re.search('[a-zA-Z]', vip): name += ' [COLOR orange]%s[/COLOR]' % vip

                    addDirectoryItem(name, url, 'ndmode', image, image, fanart2, '0', content, data)
                except:
                    pass


            items = re.compile('<item>(.+?)</item>').findall(link)

            for item in items:
                try:

                    data = {}

                    name = re.findall('<title>(.+?)</title>', item)[0]
                    name = cleantitle(name)

                    if not query.lower() in name.lower() : raise Exception()

                    url = re.findall('<link>(.+?)</link>', item)[0]

                    try: image = re.findall('<thumbnail>(.+?)</thumbnail>', item)[0]
                    except: image = '0'

                    try: fanart2 = re.findall('<fanart>(.+?)</fanart>', item)[0]
                    except: fanart2 = fanart

                    if content =='movies':
                        try:
                            title = cleantitle(name).encode('utf-8')
                            data = {'title': title}

                            title, year = re.compile('(.+?)[(](\d{4})[)]').findall(name)[0]
                            title = cleantitle(title).encode('utf-8')
                            data = {'title': title, 'year': year}
                        except:
                            pass

                    if re.search('[a-zA-Z]', vip): name += ' [COLOR orange]%s[/COLOR]' % vip

                    if 'sublink' in url:
                        addDirectoryItem(name, url, 'subDirectory', image, image, fanart2, '0', content, data, isFolder=True)
                    else:
                        addDirectoryItem(name, url, 'resolveUrl', image, image, fanart2, '0', content, data, isFolder=False)
                except:
                    pass
        except:
            pass

    control.directory(int(sys.argv[1]), cacheToDisc=True)


def clearSearch():
    cache.clear('rel_srch')
    control.refresh()


def resolveUrl(url, direct=True):
    try:
        dialog = None
        dialog = control.progressDialog
        dialog.create(control.addonInfo('name'), control.lang(30726).encode('utf-8'))
        dialog.update(0)
    except:
        pass

    try:
        if not '</regex>' in url: raise Exception()
        from resources.lib.modules import regex
        u = regex.resolve(url)
        if not u == None: url = u
    except:
        pass


    try:
        if not '.f4m'in url: raise Exception()
        ext = url.split('?')[0].split('&')[0].split('|')[0].rsplit('.')[-1].replace('/', '').lower()
        if not ext == 'f4m': raise Exception()
        from resources.lib.modules.f4mproxy.F4mProxy import f4mProxyHelper
        f4mlabel = cleantitle(control.infoLabel('listitem.label'))
        f4micon = control.infoLabel('listitem.icon')
        return f4mProxyHelper().playF4mLink(url, f4mlabel, None, None, '', f4micon)
    except:
        pass


    try:
        if not url.startswith('rtmp'): raise Exception()
        if len(re.compile('\s*timeout=(\d*)').findall(url)) == 0: url += ' timeout=10'
        return playItem(url, dialog)
    except:
        pass


    try:
        url = url.split('<source>')[0]

        domain = (urlparse.urlparse(url).netloc).lower()

        s = []
        path = os.path.join(control.addonInfo('path'), 'resources', 'lib', 'sources')
        for d in os.listdir(path):
            try: s += [(d, re.findall('self\.domains\s*=\s*\[(.+?)\]', open(os.path.join(path, d), 'r').read())[0].split(','))]
            except: pass
        s = [(i[0].replace('.py', ''), [x.replace('\'', '').replace('\"', '').strip() for x in i[1]]) for i in s]
        s = [i[0] for i in s if any(x in domain for x in i[1])]
        if len(s) > 0: direct = False

        import urlresolver
        hostDict = urlresolver.plugnplay.man.implementors(urlresolver.UrlResolver)
        hostDict = [i.domains for i in hostDict]
        hostDict = [i for i in hostDict if not '*' in i]
        hostDict = [i.lower() for i in reduce(lambda x, y: x+y, hostDict)]
        hostDict = [x for y,x in enumerate(hostDict) if x not in hostDict[:y]]

        hostcapDict = ['hugefiles.net', 'kingfiles.net', 'openload.io', 'openload.co']

        call = __import__('resources.lib.sources.%s' % s[0], globals(), locals(), ['object'], -1).source()

        sources = call.sources(url, hostDict, hostDict)

        random.shuffle(sources)

        filter = []
        filter += [i for i in sources if i['direct'] == True]
        filter += [i for i in sources if i['direct'] == False]
        sources = filter

        filter = []
        filter += [i for i in sources if i['quality'] == '1080p' and not i['source'].lower() in hostcapDict]
        filter += [i for i in sources if i['quality'] == '1080p' and i['source'].lower() in hostcapDict]
        filter += [i for i in sources if i['quality'] == 'HD' and not i['source'].lower() in hostcapDict]
        filter += [i for i in sources if i['quality'] == 'HD' and i['source'].lower() in hostcapDict]
        filter += [i for i in sources if i['quality'] == 'SD' and not i['source'].lower() in hostcapDict]
        filter += [i for i in sources if i['quality'] == 'SCR' and not i['source'].lower() in hostcapDict]
        filter += [i for i in sources if i['quality'] == 'CAM' and not i['source'].lower() in hostcapDict]
        sources = filter

        try: dialog.update(50, control.lang(30726).encode('utf-8'), str(' '))
        except: pass

        u = None

        for i in range(len(sources)):
            try:
                try:
                    if dialog.iscanceled(): break
                    if xbmc.abortRequested == True: return sys.exit()
                except:
                    pass

                url = call.resolve(sources[i]['url'])
                if url == None: raise Exception()

                if not sources[i]['direct'] == True:
                    url = urlresolver.HostedMediaFile(url=sources[i]['url']).resolve()

                if url == False: raise Exception()

                try: headers = dict(urlparse.parse_qsl(url.rsplit('|', 1)[1]))
                except: headers = dict('')

                if url.startswith('http') and '.m3u8' in url:
                    result = client.request(url.split('|')[0], headers=headers, output='geturl', timeout='20')
                    if result == None: raise Exception()

                elif url.startswith('http'):
                    result = client.request(url.split('|')[0], headers=headers, output='chunk', timeout='20')
                    if result == None: raise Exception()

                u = url ; break
            except:
                pass

        if not u == None: return playItem(u, dialog)
    except:
        pass


    try:
        import urlresolver
        if urlresolver.HostedMediaFile(url).valid_url() == True: direct = False
        u = urlresolver.HostedMediaFile(url=url).resolve()
        if not u == False: return playItem(u, dialog)
    except:
        pass


    try:
        domain = '.'.join((urlparse.urlparse(url).netloc).split('.')[-2:]).lower()

        s = []
        path = os.path.join(control.addonInfo('path'), 'resources', 'lib', 'resolvers')
        for d in os.listdir(path):
            try: s += [(d, re.findall('domains\s*=\s*\[(.+?)\]', open(os.path.join(path, d), 'r').read())[0].split(','))]
            except: pass
        s = [(i[0], [x.replace('\'', '').replace('\"', '').strip() for x in i[1]]) for i in s]
        s = [i[0].replace('.py', '') for i in s if domain in i[1]]
        if len(s) > 0: direct = False

        u = __import__('resources.lib.resolvers.%s' % s[0], globals(), locals(), ['object'], -1).resolve(url)

        if not u == None: return playItem(u, dialog)
    except:
        pass


    if direct == True: return playItem(url, dialog)


    try: dialog.close()
    except: pass

    return control.infoDialog(control.lang(30705).encode('utf-8'))


def playItem(url, dialog=None):
    try:
        try: dialog.close()
        except: pass

        meta = {}
        for i in ['title', 'originaltitle', 'tvshowtitle', 'year', 'season', 'episode', 'genre', 'rating', 'votes', 'director', 'writer', 'plot', 'tagline']:
            try: meta[i] = control.infoLabel('listitem.%s' % i)
            except: pass
        meta['title'] = cleantitle(meta['title'])
        meta = dict((k,v) for k, v in meta.iteritems() if not v == '')
        if not 'title' in meta: meta['title'] = cleantitle(control.infoLabel('listitem.label'))
        icon = control.infoLabel('listitem.icon')

        item = control.item(path=url, iconImage=icon, thumbnailImage=icon)
        item.setInfo(type='Video', infoLabels = meta)
        control.player.play(url, item)
    except:
        pass


def addCategoryItem(name, action, image, isFolder=True):
    u = '%s?action=%s' % (sys.argv[0], str(action))
    image = control.addonInfo('path') + '/resources/media/phstreams/' + image
    item = control.item(name, iconImage=image, thumbnailImage=image)
    item.addContextMenuItems([], replaceItems=False)
    item.setProperty('Fanart_Image', control.addonInfo('fanart'))
    control.addItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=isFolder)


def addDirectoryItem(name, url, action, image, image2, fanart, audio, content, data, tvshow='0', totalItems=0, isFolder=True):
    if not str(image).lower().startswith('http'): image = control.addonInfo('icon')

    if not str(image2).lower().startswith('http'): image2 = control.addonInfo('icon')

    if not str(fanart).lower().startswith('http'): fanart = control.addonInfo('fanart')

    sysaddon = sys.argv[0]

    u = '%s?name=%s&url=%s&audio=%s&image=%s&fanart=%s&tvshow=%s&content=%s&action=%s' % (sysaddon, urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(audio), urllib.quote_plus(image), urllib.quote_plus(fanart), str(tvshow), str(content), str(action))

    cm = []

    if content in ['movies', 'tvshows']:
        data.update({'trailer': '%s?action=trailer&name=%s' % (sysaddon, urllib.quote_plus(name))})
        cm.append((control.lang(30707).encode('utf-8'), 'RunPlugin(%s?action=trailer&name=%s)' % (sysaddon, urllib.quote_plus(name))))

    if not 'plot' in data:
        data.update({'plot': control.lang(30706).encode('utf-8')})


    if content == 'movies':
        cm.append((control.lang(30708).encode('utf-8'), 'XBMC.Action(Info)'))
    elif content in ['tvshows', 'seasons']:
        cm.append((control.lang(30709).encode('utf-8'), 'XBMC.Action(Info)'))
    elif content == 'episodes':
        cm.append((control.lang(30710).encode('utf-8'), 'XBMC.Action(Info)'))


    if content == 'movies' and not isFolder == True:
        downloadFile = name
        try: downloadFile = '%s (%s)' % (data['title'], data['year'])
        except: pass
        cm.append((control.lang(30722).encode('utf-8'), 'RunPlugin(%s?action=addDownload&name=%s&url=%s&image=%s)' % (sysaddon, urllib.quote_plus(downloadFile), urllib.quote_plus(url), urllib.quote_plus(image))))

    elif content == 'episodes' and not isFolder == True:
        downloadFile = name
        try: downloadFile = '%s S%02dE%02d' % (data['tvshowtitle'], int(data['season']), int(data['episode']))
        except: pass
        cm.append((control.lang(30722).encode('utf-8'), 'RunPlugin(%s?action=addDownload&name=%s&url=%s&image=%s)' % (sysaddon, urllib.quote_plus(downloadFile), urllib.quote_plus(url), urllib.quote_plus(image))))


    if content == 'movies':
        cm.append((control.lang(30711).encode('utf-8'), 'RunPlugin(%s?action=addView&content=movies)' % sysaddon))
    elif content == 'tvshows':
        cm.append((control.lang(30712).encode('utf-8'), 'RunPlugin(%s?action=addView&content=tvshows)' % sysaddon))
    elif content == 'seasons':
        cm.append((control.lang(30713).encode('utf-8'), 'RunPlugin(%s?action=addView&content=seasons)' % sysaddon))
    elif content == 'episodes':
        cm.append((control.lang(30714).encode('utf-8'), 'RunPlugin(%s?action=addView&content=episodes)' % sysaddon))


    if content in ['movies', 'episodes']:
        replaceItems = True
        cm.append((control.lang(30725).encode('utf-8'), 'RunPlugin(%s?action=openSettings)' % sysaddon))
    else:
        replaceItems = False


    item = control.item(name, iconImage='DefaultFolder.png', thumbnailImage=image)
    try: item.setArt({'poster': image2, 'tvshow.poster': image2, 'season.poster': image2, 'banner': image, 'tvshow.banner': image, 'season.banner': image})
    except: pass
    item.addContextMenuItems(cm, replaceItems=replaceItems)
    item.setProperty('Fanart_Image', fanart)
    item.setInfo(type='Video', infoLabels=data)

    control.addItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=totalItems,isFolder=isFolder)


def endCategory():
    if control.skin == 'skin.confluence': control.execute('Container.SetViewMode(500)')
    control.directory(int(sys.argv[1]), cacheToDisc=True)


def endDirectory(content, close):
    if content in ['movies', 'tvshows', 'seasons', 'episodes']:
        control.content(int(sys.argv[1]), content)

    if close == True: control.directory(int(sys.argv[1]), cacheToDisc=True)

    if close == True and content in ['movies', 'tvshows', 'seasons', 'episodes']:
        views.setView(content)


def cleantitle(name):
    name = re.sub('(\.|\_|\(|\[|\s)(Link \d*|link \d*)(\.|\_|\)|\]|$)', '', name)
    name = re.sub('\(\d{4}.+?\d{4}\)$', '', name)
    name = re.sub('\s\[COLOR.+?\].+?\[/COLOR\]|\[/COLOR\]\[COLOR.+?\]\s.+?\[/COLOR\]|\[COLOR.+?\]|\[/COLOR\]', '', name)
    name = re.sub('\s\s+', ' ', name)
    name = name.strip()
    return name


def cleaneptitle(tvshow, name):
    try:
        p = re.compile('(S\d*E\d*)').findall(name)
        p += re.compile('(s\d*e\d*)').findall(name)
        p += re.compile('(Season \d* Episode \d*)').findall(name)
        p += re.compile('(\d*x Episode \d*)').findall(name)
        p += re.compile('(\d*x\d*)').findall(name)
        p = p[0]

        name = name.replace(tvshow, '').replace(p, '')
        name = re.sub('-|:', '', name)
        name = re.sub('\s\s+', ' ', name)
        name = name.strip()

        season = re.compile('(\d*)').findall(p)
        season = [i for i in season if i.isdigit()][0]
        season = '%01d' % int(season)

        episode = re.compile('(\d*)').findall(p)
        episode = [i for i in episode if i.isdigit()][-1]
        episode = '%01d' % int(episode)

        if re.match('[A-Z0-9]', name) == None:
            name = '%s S%02dE%02d' % (tvshow, int(season), int(episode))

        return (name, season, episode)
    except:
        return


