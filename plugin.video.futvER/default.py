import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import re, string, sys, os
import urlresolver
import HTMLParser
from TheYid.common.addon import Addon
from TheYid.common.net import Net

addon_id = 'plugin.video.futvER'
plugin = xbmcaddon.Addon(id=addon_id)
DB = os.path.join(xbmc.translatePath("special://database"), 'futvER.db')
net = Net()
addon = Addon('plugin.video.futvER', sys.argv)
AddonPath = addon.get_path()
IconPath = AddonPath + "/icons/"
FanartPath = AddonPath + "/icons/"
mode = addon.queries['mode']
url = addon.queries.get('url', None)
url1 = addon.queries.get('url1', None)
content = addon.queries.get('content', None)
query = addon.queries.get('query', None)
startPage = addon.queries.get('startPage', None)
numOfPages = addon.queries.get('numOfPages', None)
listitem = addon.queries.get('listitem', None)
urlList = addon.queries.get('urlList', None)
section = addon.queries.get('section', None)
img = addon.queries.get('img', None)
text = addon.queries.get('text', None)

#-----------------------------------------------------------------------------------------------------------------------------------------#

def GetTitles6(section, url, startPage= '1', numOfPages= '1'): 
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
                match = re.compile('class="wb-image"><img src="(.+?)"></a>\s*?<!-- Wb Center -->\s*?<div class="wb-center">\s*?<h3 class="wb-name"><a href="(.+?)">(.+?)</a></h3>', re.DOTALL).findall(html)
                for img, movieUrl, name in match:
                        addon.add_directory({'mode': 'GetTitles1', 'section': section, 'url': movieUrl, 'img': img , 'text': name}, {'title': name}, img= img, fanart= 'http://images.forwallpaper.com/files/thumbs/preview/64/646017__cinema_p.jpg')      
                addon.add_directory({'mode': 'GetTitles6', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart= 'http://images.forwallpaper.com/files/thumbs/preview/64/646017__cinema_p.jpg')      
        setView('tvshows', 'tvshows-view')
    except:
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#-----------------------------------------------------------------------------------------------------------------------------------------#

def GetTitles3(section, url): 
    try:
        pageUrl = url
        print pageUrl
        html = net.http_GET(pageUrl).content                  
        match = re.compile(''' class="hb-image" style="background.+?'(.+?)'.+?"></a>\s*?<div class="hb-right">\s*?<a title=".+?" href="(.+?)" class="episode">(.+?)</a>''', re.DOTALL).findall(html)
        for img, movieUrl, name in match:
                addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl, 'img': img , 'text': name}, {'title': name}, img= img, fanart= 'http://images.forwallpaper.com/files/thumbs/preview/64/646017__cinema_p.jpg')      
    except:
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetTitles4(section, url): 
    try:
        pageUrl = url
        print pageUrl
        html = net.http_GET(pageUrl).content                  
        match = re.compile('''<div class="home-box ">\s*?<a href="(.+?)" class="hb-image" style="background.+?'(.+?)'.+?"></a>\s*?<div class="hb-right">\s*?<a href=".+?" class="serie">.+?</a>\s*?<a href=".+?" class="episode">(.+?)</a>''', re.DOTALL).findall(html)
        for movieUrl, img, name in match:
                addon.add_directory({'mode': 'GetTitles1', 'section': section, 'url': movieUrl, 'img': img , 'text': name}, {'title': name}, img= img, fanart= 'http://images.forwallpaper.com/files/thumbs/preview/64/646017__cinema_p.jpg')      
    except:
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#-----------------------------------------------------------------------------------------------------------------------------------------#

def GetTitles2(section, url, startPage= '1', numOfPages= '1'): 
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
                match = re.compile('class="wb-image"><img src="(.+?)"></a>\s*?<!-- Wb Center -->\s*?<div class="wb-center">\s*?<h3 class="wb-name"><a href="(.+?)">(.+?)</a></h3>', re.DOTALL).findall(html)
                for img, movieUrl, name in match:
                        addon.add_directory({'mode': 'GetTitles1', 'section': section, 'url': movieUrl, 'img': img , 'text': name}, {'title': name}, img= img, fanart= 'http://images.forwallpaper.com/files/thumbs/preview/64/646017__cinema_p.jpg')      
                addon.add_directory({'mode': 'GetTitles2', 'url': url, 'url1': url1, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart= 'http://images.forwallpaper.com/files/thumbs/preview/64/646017__cinema_p.jpg')      
        setView('tvshows', 'tvshows-view')
    except:
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------------------------------------------------------------------#

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
                match = re.compile('<div class="cb-first">\s*?<a href="(.+?)" class="c-image"><img alt=".+?" title="(.+?)" src="(.+?)"></a>', re.DOTALL).findall(html)
                for movieUrl, name, img in match:
                        addon.add_directory({'mode': 'GetTitles1', 'section': section, 'url': movieUrl, 'img': img , 'text': name}, {'title': name}, img= img, fanart= 'http://images.forwallpaper.com/files/thumbs/preview/64/646017__cinema_p.jpg')            
        setView('tvshows', 'tvshows-view')
    except:
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetTitles1(section, url): 
    try:
        pageUrl = url
        print pageUrl
        html = net.http_GET(pageUrl).content                  
        match = re.compile('</div>\s*?<a title="(.+?)" href="(.+?)">\s*?<div class="season">.+?</div>\s*?<div class="episode">.+?</div>\s*?<div class="e-name">(.+?)</div>', re.DOTALL).findall(html)
        for name, movieUrl, name1 in match:
                name1 = name1.replace('</div>', '')
                name1 = name1.replace('</a>', '')
                addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl, 'img': img , 'text': name}, {'title': name + ' : ' + name1}, img= img, fanart= 'http://images.forwallpaper.com/files/thumbs/preview/64/646017__cinema_p.jpg')      
    except:
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks(section, url, img, text):
    try:
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('data-actuallink="(.+?)">.+?</a>').findall(content)
        match1 = re.compile('<h2>(.+?)</h2>').findall(content)
        match2 = re.compile('<div class=".+?">\s*?<div class="title"></div>\s*?<span>(.+?)</span>\s*?<br>(.+?)<span>(.+?)</span>').findall(content)
        match3 = re.compile('<div class="desc">\s*?<span>(.+?)</span> <br>\s*?(.+?)<span>(.+?)</span>').findall(content)
        listitem = GetMediaInfo(content)
        for name in match1:
                addon.add_directory({'img': img}, {'title':  '[COLOR darkturquoise][B]' + name.strip() + '[/B] [/COLOR]'}, img= img, fanart= 'http://imgprix.com/web/wallpapers/private-cinema-room/2560x1600.jpg') 
        for url in match:
                host = GetDomain(url)
                if urlresolver.HostedMediaFile(url= url):
                        title = url.rpartition('/')
                        title = title[2].replace('.html', '')
                        title = title.replace('.htm', '')
                        host = host.replace('embed.','')
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title': host + ' : ' + title }, img= img, fanart= 'http://imgprix.com/web/wallpapers/private-cinema-room/2560x1600.jpg')
        for name, name1, name2 in match2 + match3:
                addon.add_directory({'img': img}, {'title':  '[COLOR red][B]' + name.strip() + ' ' + name1 + ' ' + name2 + '[/B] [/COLOR]'}, img= img, fanart= 'http://imgprix.com/web/wallpapers/private-cinema-room/2560x1600.jpg') 
    except:

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
        addon.add_directory({'mode': 'GetTitles3', 'section': 'ALL', 'url': BASE_URL + '/'}, {'title':  '[B]New Latest Episodes[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles4', 'section': 'ALL', 'url': BASE_URL + '/home/latest-this-week'}, {'title':  '[B]Popular Episodes This Week[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/home/new-series',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]New Series[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/home/popular-series',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Popular Series[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles2', 'section': 'ALL', 'url': BASE_URL + '/home/series',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Series[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')

        addon.add_directory({'mode': 'GenreMenu'}, {'title':  '[B]Genre[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'YearMenu'}, {'title':  '[B]Year[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')

        addon.add_directory({'mode': 'GetSearchQuery'},  {'title':  '[COLOR green]Search[/COLOR]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'ResolverSettings'}, {'title':  '[COLOR red]Resolver Settings[/COLOR]'}, img=IconPath + 'url1.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'ResolverSettings'}, {'title':  '[B][COLOR yellow] www.entertainmentrepo.com  [/B][/COLOR]'}, img=IconPath + 'newart.jpg', fanart=IconPath +  'newart.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GenreMenu(): 
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/genre/action',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Action[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/genre/Adventure',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Adventure[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/genre/Animation',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Animation[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/genre/Cartoon',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Cartoon[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/genre/Children',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Children[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/genre/Comedy',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Comedy[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/genre/Crime',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Crime[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/genre/Documentary',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Documentary[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/genre/Drama',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Drama[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/genre/Family',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Family[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/genre/Fantasy',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Fantasy[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')

        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/genre/Food',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Food[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/genre/game-show',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Game Show[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/genre/History',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]History[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/genre/home-and-garden',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Home & Garden[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/genre/Horror',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Horror[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/genre/Kids',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Kids[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/genre/Mini-Series',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Mini Series[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/genre/Music',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Music[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/genre/Mystery',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Mystery[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/genre/News',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]News[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/genre/Politics',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Politics[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')

        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/genre/Reality',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Reality[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/genre/Romance',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Romance[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/genre/Sci-Fi',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Sci-Fi[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/genre/Science-Fiction',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Science-Fiction[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/genre/Soap',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Soaps[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/genre/special-interest',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Special Interest[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/genre/Sport',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Sport[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/genre/Suspense',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Suspense[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/genre/Talk',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Talk[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/genre/talk-show',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Talk Show[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/genre/Thriller',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Thriller[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')

        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/genre/Travel',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Travel[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/genre/War',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]War[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/genre/Western',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Western[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def YearMenu(): 
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/2017',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]2017[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/2016',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]2016[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/2015',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]2015[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/2014',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]2014[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/2013',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]2013[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/2012',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]2012[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/2011',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]2011[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/2010',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]2010[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')

        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/2009',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]2009[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/2008',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]2008[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/2007',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]2007[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/2006',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]2006[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/2005',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]2005[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/2004',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]2004[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/2003',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]2003[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/2002',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]2002[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/2001',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]2001[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/2000',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]2000[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')

        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/1999',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]1999[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/1998',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]1998[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/1997',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]1997[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/1996',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]1996[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/1995',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]1995[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/1994',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]1994[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/1993',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]1993[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/1992',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]1992[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/1991',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]1991[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/1990',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]1990[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')

        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/1989',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]1989[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/1988',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]1988[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/1987',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]1987[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/1986',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]1986[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/1985',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]1985[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/1984',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]1984[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/1983',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]1983[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/1982',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]1982[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/1981',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]1981[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/1980',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]1980[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')

        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/1979',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]1979[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/1978',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]1978[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/1977',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]1977[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/1976',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]1976[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/1975',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]1975[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/1974',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]1974[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/1973',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]1973[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/1972',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]1972[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/1971',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]1971[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL + '/year/1970',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]1970[/B]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
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
        url = 'http://www.watchepisodes4.com/' + query
        url = url.replace(' ', '-')
        print url
        html = net.http_GET(url).content
        match = re.compile('</div>\s*?<a title="(.+?)" href="(.+?)">\s*?<div class="season">.+?</div>\s*?<div class="episode">.+?</div>\s*?<div class="e-name">(.+?)</div>').findall(html)
        for title, url, title1 in match:
                addon.add_directory({'mode': 'GetLinks', 'url': url, 'img': 'http://www.ilmioprofessionista.it/wp-content/uploads/2015/04/TVSeries3.png' }, {'title':  title + ' : ' + title1}, img= 'http://www.ilmioprofessionista.it/wp-content/uploads/2015/04/TVSeries3.png', fanart=FanartPath + 'fanart.jpg')
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
BASE_URL = 'http://www.watchepisodes3.com/'
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
elif mode == 'GetTitles2': 
	GetTitles2(section, url, startPage, numOfPages)
elif mode == 'GetTitles3': 
	GetTitles3(section, url)
elif mode == 'GetTitles4': 
	GetTitles4(section, url)
elif mode == 'GetTitles6': 
	GetTitles6(section, url, startPage, numOfPages)
elif mode == 'GetLinks':
	GetLinks(section, url, img, text)
elif mode == 'GetSearchQuery':
	GetSearchQuery()
elif mode == 'Search':
	Search(query)
elif mode == 'PlayVideo':
	PlayVideo(url, listitem)
elif mode == 'ResolverSettings':
        urlresolver.display_settings()
xbmcplugin.endOfDirectory(int(sys.argv[1]))