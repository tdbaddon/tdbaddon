import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import re, string, sys, os
import urlresolver
import HTMLParser
from TheYid.common.addon import Addon
from TheYid.common.net import Net

addon_id = 'plugin.video.mitER'
plugin = xbmcaddon.Addon(id=addon_id)
DB = os.path.join(xbmc.translatePath("special://database"), 'mitER.db')
net = Net()
addon = Addon('plugin.video.mitER', sys.argv)
BASE_URL = 'http://www.allwrestling.net/'
AddonPath = addon.get_path()
IconPath = AddonPath + "/icons/"
FanartPath = AddonPath + "/icons/"
mode = addon.queries['mode']
url = addon.queries.get('url', None)
content = addon.queries.get('content', None)
query = addon.queries.get('query', None)
startPage = addon.queries.get('startPage', None)
numOfPages = addon.queries.get('numOfPages', None)
listitem = addon.queries.get('listitem', None)
urlList = addon.queries.get('urlList', None)
section = addon.queries.get('section', None)
img = addon.queries.get('img', None)
text = addon.queries.get('text', None)

def GetTitles(section, url, startPage= '1', numOfPages= '1'): 
    try:
        pageUrl = url
        if int(startPage)> 1:
                pageUrl = url + '/page/' + startPage + '/'
        print pageUrl
        html = net.http_GET(pageUrl).content
        start = int(startPage)
        end = start + int(numOfPages)
        for page in range( start, end):
                if ( page != start):
                        pageUrl = url + '/page/' + str(page) + '/'
                        html = net.http_GET(pageUrl).content                      
                match = re.compile('\s*?<span class="clip">\s*?<img src="//(.+?)" alt=".+?" /><span class="vertical-align"></span>\s*?</span>\s*?<span class="overlay"></span>\s*?</a>\s*?</div>\s*?<div class="data">\s*?<h2 class="entry-title"><a href="(.+?)" rel="bookmark" title=".+?">Watch (.+?)</a></h2>', re.DOTALL).findall(html)
                for img, movieUrl, name in match:
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl, 'img': 'http://' + img , 'text': name}, {'title': name.replace('Online Free', '').replace('Full Show', '')}, img= 'http://' + img, fanart= 'http://images.forwallpaper.com/files/thumbs/preview/64/646017__cinema_p.jpg')      
                addon.add_directory({'mode': 'GetTitles', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart= 'http://images.forwallpaper.com/files/thumbs/preview/64/646017__cinema_p.jpg')      
        setView('tvshows', 'tvshows-view')
    except:
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks(section, url, img, text):
    try:
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('</span>(.+?)</b></p>\s*?<p style="text-align: center;"><a href="(.+?)"').findall(content)
        match1 = re.compile('http://www.multiup.org/download/(.+?)"').findall(content)
        #match2 = re.compile('<p style="text-align: center;"><b>.+?<span style=".+?">(.+?)</span>.+?</b></p>\s*?<p style="text-align: center;"><a href="http://www.gagatrends.com/cgi-bin/.+?id=(.+?)"').findall(content)
        listitem = GetMediaInfo(content)
        for url in match1:
                addon.add_directory({'mode': 'GetLinks3', 'url': 'http://www.multiup.org/en/mirror/' + url, 'listitem': listitem, 'img': img, 'text': text}, {'title':  'Multiup.org  : ' + text}, img= img, fanart= 'http://imgprix.com/web/wallpapers/private-cinema-room/2560x1600.jpg') 
        for name, url in match:
                host = GetDomain(url)
                if urlresolver.HostedMediaFile(url= url):
                        title = url.rpartition('/')
                        title = title[2].replace('.html', '')
                        title = title.replace('.htm', '')
                        host = host.replace('embed.','')
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title': host + ' : ' + title  + ' : ' + name.replace(')', '').replace('</b></span>', '')}, img= img, fanart= 'http://imgprix.com/web/wallpapers/private-cinema-room/2560x1600.jpg')
        #for name, url in match2:
        #        url = url.replace('&amp;','')
        #        addon.add_directory({'mode': 'GetLinks2', 'url': 'http://www.gagatrends.com/bin/wwetalk.php?wid=' + url, 'listitem': listitem, 'img': img, 'text': text}, {'title': url + '  ' + name}, img= img, fanart= 'http://imgprix.com/web/wallpapers/private-cinema-room/2560x1600.jpg') 
    except:
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))


def GetLinks2(section, url, img, text):
    try:
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('src="(http://www.dailymotion.com/embed/video/.+?)" allowfullscreen></iframe>').findall(content)
        match1 = re.compile("src='(.+?)'").findall(content)
        match2 = re.compile('https://openload.co/embed/\s*?(.+?)"').findall(content)
        listitem = GetMediaInfo(content)
        for url in match + match1 + match2:
                host = GetDomain(url)
                if urlresolver.HostedMediaFile(url= url):
                        title = url.rpartition('/')
                        title = title[2].replace('.html', '')
                        title = title.replace('.htm', '')
                        host = host.replace('embed.','')
                        addon.add_directory({'mode': 'PlayVideo', 'url': 'http://www.dailymotion.com/embed/video' + url, 'listitem': listitem}, {'title': host + ' : ' + url}, img= img, fanart= 'http://imgprix.com/web/wallpapers/private-cinema-room/2560x1600.jpg')
    except:
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))


def GetLinks3(section, url, img, text):
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('style="width:97%;text-align:left"\s*?href="(.+?)"').findall(content)
        listitem = GetMediaInfo(content)
        for url in match:
                host = GetDomain(url)
                if urlresolver.HostedMediaFile(url= url):
                        title = url.rpartition('/')
                        title = title[2].replace('.html', '')
                        title = title.replace('.htm', '')
                        host = host.replace('embed.','')
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title': host + ' : ' + title }, img= img, fanart= 'http://imgprix.com/web/wallpapers/private-cinema-room/2560x1600.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


def PlayVideo(url, listitem):
    try:
        print 'in PlayVideo %s' % url
        stream_url = urlresolver.HostedMediaFile(url).resolve()
        xbmc.Player().play(stream_url)
        addon.add_directory({'mode': 'help'}, {'title':  '[COLOR slategray][B]^ Press back ^[/B] [/COLOR]'},'','')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry Link may have been removed ![/B][/COLOR],[COLOR lime][B]Please try a different link/host !![/B][/COLOR],7000,"")")

def GetDomain(url):
        tmp = re.compile('//(.+?)/').findall(url)
        domain = 'Unknown'
        if len(tmp) > 0 :
            domain = tmp[0].replace('www.', '')
        return domain

def GetMediaInfo(html):
        listitem = xbmcgui.ListItem()
        match = re.search('og:title" content="(.+?) \((.+?)\)', html)
        if match:
                print match.group(1) + ' : '  + match.group(2)
                listitem.setInfo('video', {'Title': match.group(1), 'Year': int(match.group(2)) } )
        return listitem

def MainMenu():   
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Latest Added[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/wwe/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Latest WWE[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/wwe/wwe-network/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Latest WWE Network[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/wwe/wwe-ppv/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Latest WWE PPVs[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/tna/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Latest TNA[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/ring-of-honor/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Latest ROH[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/more/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]More Wrestling[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/ufc/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Latest UFC[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/bellator/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Latest Bellator[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/mma/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]More MMA[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/more/interviews/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Interviews[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')


        #addon.add_directory({'mode': 'GenreMenu'}, {'title':  '[B]Movies by genre[/B]'}, img=IconPath + 'gen.png', fanart=FanartPath + 'fanart.jpg')
        #addon.add_directory({'mode': 'YearMenu'}, {'title':  '[B]Movies by year[/B]'}, img=IconPath + 'year.png', fanart=FanartPath + 'fanart.jpg')

        addon.add_directory({'mode': 'GetSearchQuery'},  {'title':  '[COLOR green]Search[/COLOR]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'ResolverSettings'}, {'title':  '[COLOR red]Resolver Settings[/COLOR]'}, img=IconPath + 'url1.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'ResolverSettings'}, {'title':  '[B][COLOR yellow] www.entertainmentrepo.com  [/B][/COLOR]'}, img=IconPath + 'newart.jpg', fanart=IconPath +  'newart.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GenreMenu(): 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/movie-genre/action/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]action [/COLOR] >>'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/movie-genre/adventure/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]adventure [/COLOR] >>'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/movie-genre/animation/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]animation [/COLOR] >>'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/movie-genre/biography/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]biography [/COLOR] >>'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def YearMenu(): 
        #addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/2017/',
                             #'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]2017 [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/2016/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]2016[/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/2015/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]2015 [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))



def GetSearchQuery():
	last_search = addon.load_data('search')
	if not last_search: last_search = ''
	keyboard = xbmc.Keyboard()
        keyboard.setHeading('Search')
	keyboard.setDefault(last_search)
	keyboard.doModal()
	if (keyboard.isConfirmed()):
                query = keyboard.getText()
                addon.save_data('search',query)
                Search(query)
	else:
                return

def Search(query):
        url = 'http://www.allwrestling.net/?s=' + query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<a class="clip-link" data-id=".+?" title="Watch (.+?)" href="(.+?)">\s*?<span class="clip">\s*?<img src="(.+?)"').findall(html)
        for title, url, img in match:
                addon.add_directory({'mode': 'GetLinks', 'url': url, 'img': img , 'text': title }, {'title':  title.replace('Online Free', '').replace('Full Show', '')}, img= img, fanart=FanartPath + 'fanart.jpg')
        setView('tvshows', 'tvshows-view')
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def setView(content, viewType):
	if content:
		xbmcplugin.setContent(int(sys.argv[1]), content)
	if addon.get_setting('auto-view') == 'true':
		xbmc.executebuiltin("Container.SetViewMode(%s)" % addon.get_setting(viewType) )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_PROGRAM_COUNT )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RUNTIME )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_GENRE )

if mode == 'main': 
	MainMenu()
elif mode == 'GenreMenu':
        GenreMenu()
elif mode == 'YearMenu':
        YearMenu()
elif mode == 'GetTitles': 
	GetTitles(section, url, startPage, numOfPages)
elif mode == 'GetTitles1': 
	GetTitles1(section, url)
elif mode == 'GetLinks':
	GetLinks(section, url, img, text)
elif mode == 'GetLinks1':
	GetLinks1(section, url, img, text)
elif mode == 'GetLinks2':
	GetLinks2(section, url, img, text)
elif mode == 'GetLinks3':
	GetLinks3(section, url, img, text)
elif mode == 'GetLinks4':
	GetLinks4(section, url, img, text)
elif mode == 'GetSearchQuery':
	GetSearchQuery()
elif mode == 'Search':
	Search(query)
elif mode == 'PlayVideo':
	PlayVideo(url, listitem)
elif mode == 'PlayVideo1':
	PlayVideo1(text, img, url, listitem)	
elif mode == 'ResolverSettings':
        urlresolver.display_settings()
xbmcplugin.endOfDirectory(int(sys.argv[1]))