'''
    Rave player XBMC Addon
    Copyright (C) 2014 tcz009 @TheYid009 TheYid's REPO

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
#####################################################################-Rave player-#########################################################################################

import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import urllib, urllib2
import re, string, sys, os
from TheYid.common.addon import Addon
from TheYid.common.net import Net
from htmlentitydefs import name2codepoint as n2cp
import HTMLParser
import urlresolver

addon_id = 'plugin.audio.raveplayer'
plugin = xbmcaddon.Addon(id=addon_id)
DB = os.path.join(xbmc.translatePath("special://database"), 'raveplayer.db')
net = Net()
addon = Addon('plugin.audio.raveplayer', sys.argv)
mode = addon.queries['mode']
url = addon.queries.get('url', None)
content = addon.queries.get('content', None)
query = addon.queries.get('query', None)
listitem = addon.queries.get('listitem', None)
img = addon.queries.get('img', None)
text = addon.queries.get('text', None)

BASE_URL = 'http://oitj.casiotone.org/'
BASE_URL2 = 'http://20bensons.com/'
BASE_URL3 = 'http://www.ravetapepacks.com/'
BASE_URL4 = 'http://deepinsidetheoldskool.blogspot.co.uk/'
BASE_URL5 = 'http://www.thebeatsanctuary.co.uk/'
BASE_URL6 = 'http://ratpack.podomatic.com/'
BASE_URL7 = 'http://www.ukraves.co.uk/'
BASE_URL8 = 'http://oldskool.podomatic.com/'
BASE_URL9 = 'http://mikusmusik.blogspot.co.uk/'
BASE_URL11 = 'http://mixtapes.demodulated.com/'
BASE_URL13 = 'http://www.rave-archive.com/'
BASE_URL14 = 'http://www.thewire.co.uk/'
BASE_URL15 = 'https://raw.githubusercontent.com/TheYid/yidpics/master'
BASE_URL17 = 'https://archive.org/'
BASE_URL18 = 'http://torontoravemixtapearchive.com/'
BASE_URL20 = 'http://www.dj-jedi.com/'
BASE_URL21 = 'http://www.djliondub.com/'
BASE_URL22 = 'http://www.john-b.com/'
BASE_URL23 = 'http://dnbforum.com/'
BASE_URL24 = 'http://djtrudos.podomatic.com/'
BASE_URL27 = 'http://hardcorehighlights.com/'
BASE_URL31 = 'http://www.thepiratearchive.net/'
BASE_URL32 = 'http://grimetapes.tumblr.com/'
BASE_URL35 = 'http://www.braindamageradio.com/'
BASE_URL36 = 'http://www.oldskoolanthemz.com/'
BASE_URL38 = 'http://www.oldskoolanthemz.com/'
BASE_URL39 = 'http://artmeetsscience.co.uk/'
BASE_URL40 = 'http://www.twiceasnice.co.uk/'
BASE_URL41 = 'http://www.radionecks.co.uk/'
BASE_URL42 = 'http://jungletapes.com/'

############################################################################### Get links #############################################################################################

#---------------------------------------------------------------------------- jungletapes ----------------------------------------------------------------------------#

def GetLinks42(url, text, img):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<a href="/show/(.+?)">(.+?)</a>').findall(content)
        for url, name in match:
                url = 'http://www.jungletapes.com/show/' + url
                addon.add_directory({'mode': 'GetLinks42a', 'url': url, 'listitem': listitem, 'text':  name, 'img' : img}, {'title': name.strip()}, img = 'http://jungletapes.com/sites/default/files/jungle_tapes_large_logo.png', fanart = 'http://i.imgur.com/yXimypO.jpg?1')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks42a(url, text, img):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('href="http://www.jungletapes.com/sites/default/files/Tapes/(.+?)" title="(.+?)">').findall(content)
        match1 = re.compile('href="http://www.jungletapes.com/sites/default/files/Tapes/(.+?)"').findall(content)
        for url, name in match:
                addon.add_directory({'mode': 'PlayVideo', 'url': 'http://www.jungletapes.com/sites/default/files/Tapes/' + url, 'listitem': listitem, 'text':  url.replace('-', ' '), 'img' : img}, {'title': name + ' - ' + url.replace('-', ' ')}, img = 'http://jungletapes.com/sites/default/files/jungle_tapes_large_logo.png', fanart = 'http://i.imgur.com/yXimypO.jpg?1')
        for url in match1:
                addon.add_directory({'mode': 'PlayVideo', 'url': 'http://www.jungletapes.com/sites/default/files/Tapes/' + url, 'listitem': listitem, 'text':  url, 'img' : img}, {'title': url}, img = 'http://jungletapes.com/sites/default/files/jungle_tapes_large_logo.png', fanart = 'http://i.imgur.com/yXimypO.jpg?1')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


##.replace(' ', ' ')# \s*? ##url = url.replace(' ', ' ')##
#---------------------------------------------------------------------------- oneinthejungle ----------------------------------------------------------------------------#

def GetLinks(url, text, img):                                             
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<td><a href="(.+?)">(.+?)</a>').findall(content)
        for url, name in match:
                addon.add_directory({'mode': 'PlayVideo', 'url': 'http://oitj.casiotone.org/' + url, 'listitem': listitem, 'text' : name.strip(), 'img' : img}, {'title':  name.strip()}, img = 'http://images-mix.netdna-ssl.com/w/318/h/318/q/90/upload/images/extaudio/6d90c82e-aa53-4d69-85a7-bf3504baa5ae.png', fanart = 'http://www.rhythm22.com/wp-content/uploads/2010/04/1-In-The-Jungle.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------ 20bensons ----------------------------------------------------------------------------#

def GetLinks2(url, text, img):                                           
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('href="(.+?)">(.+?)</a>').findall(content)
        for url, name in match:
                url = url.replace(' ','%20')
                addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem, 'text' : name.strip(), 'img' : img}, {'title':  name.strip()}, img = 'http://www.zigsam.at/l07/B_Cig/BensonHedgesSpeciaF-20fJP197.jpg', fanart = 'http://cs11180.vk.me/u19162043/47140284/x_977c8c97.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------- ravetapepacks -------------------------------------------------------------------------------------#

def GetLinks3(url, text, img):  
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html                                          
        match = re.compile('<li class=".+?"><a href="(.+?)" >(.+?)</a>').findall(content)
        for url, name in match:
                addon.add_directory({'mode': 'GetLinks3a', 'url': url, 'listitem': listitem, 'text' : name.strip(), 'img' : img}, {'title': name.strip()}, img = 'http://fc09.deviantart.net/fs25/f/2008/111/a/8/Cassette_tape_by_Quick_Stop.png', fanart = 'http://24.media.tumblr.com/tumblr_md33y3uDzM1qkcj9ro4_1280.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks3a(url, text, img):     
    try:                                      
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        CLEAN(html)
        content = html
        match = re.compile('<h1 class="entry-title">\s*?<a href="(.+?)" rel="bookmark">(.+?)</a>').findall(content)
        match2 = re.compile('<h3 class="assistive-text">Post navigation</h3>\s*?<div class="nav-previous"><a href="http://www.ravetapepacks.com/(.+?)" ><span class="meta-nav">.+?</span> Older posts</a></div>').findall(content)
        for url, name in match:
                addon.add_directory({'mode': 'GetLinks3b', 'url':  url, 'listitem': listitem, 'text' : name.strip(), 'img' : img}, {'title':  name.strip()}, img = 'http://fc09.deviantart.net/fs25/f/2008/111/a/8/Cassette_tape_by_Quick_Stop.png', fanart = 'http://24.media.tumblr.com/tumblr_md33y3uDzM1qkcj9ro4_1280.jpg')
        for url in match2:
                addon.add_directory({'mode': 'GetLinks3a', 'url':  'http://www.ravetapepacks.com/' + url.replace('&#038;paged=', '&paged='), 'listitem': listitem, 'text' : name.strip(), 'img' : img}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img = 'https://raw.githubusercontent.com/MrEntertainment/EntertainmentREPO/master/plugin.video.theyidrh/icons/nextpage1.png', fanart = 'http://24.media.tumblr.com/tumblr_md33y3uDzM1qkcj9ro4_1280.jpg')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site mite be down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks3b(url, text, img):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match1 = re.compile('href="http://www.ravetapepacks.com/wp-content/(.+?)"><img').findall(content)
        match = re.compile('<a href="http://www.ravetapepacks.com/music/(.+?)">(.+?)</a>').findall(content)
        match2 = re.compile('<p><a title=".+?" href="http://www.ravetapepacks.com/music/(.+?)" target="_blank">(.+?)</a>').findall(content)
        for img in match1:
                addon.add_directory({'mode': 'GetLinks', 'listitem': listitem, 'text' : text, 'img' : img}, {'title': '[COLOR orchid][B]' + text + '[/COLOR][/B]'}, img = 'http://www.ravetapepacks.com/wp-content/' + img, fanart = 'http://24.media.tumblr.com/tumblr_md33y3uDzM1qkcj9ro4_1280.jpg')
        for url, name in match + match2:
                addon.add_directory({'mode': 'PlayVideo', 'url': 'http://www.ravetapepacks.com/music/' + url, 'listitem': listitem, 'text' : name.strip(), 'img' : img}, {'title':  name.strip()}, img = 'http://fc09.deviantart.net/fs25/f/2008/111/a/8/Cassette_tape_by_Quick_Stop.png', fanart = 'http://24.media.tumblr.com/tumblr_md33y3uDzM1qkcj9ro4_1280.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
#\s*?#
#------------------------------------------------------------------------ deepinsidetheoldskool -------------------------------------------------------------------------------------#

def GetLinks4(url, text, img):                                          
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile("<a dir='ltr' href='(.+?)'>(.+?)</a>").findall(content)
        for url, name in match:
                addon.add_directory({'mode': 'GetLinks4a', 'url': url, 'listitem': listitem, 'text' : name.strip(), 'img' : img}, {'title':  name.strip()}, img = 'https://d13yacurqjgara.cloudfront.net/users/393408/screenshots/1849974/attachments/310000/thumbnail/mix-tape-icon.jpg', fanart = 'https://phaven-prod.s3.amazonaws.com/files/image_part/asset/376411/zJiIP2IgvAoFrWjDxG6FfyZosnE/medium_abbfabb_03.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks4a(url, text, img):                                             
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile("<h3 class='post-title entry-title' itemprop='.+?'>\s*?<a href='(.+?)'>(.+?)</a>").findall(content)
        for url, name in match:
                addon.add_directory({'mode': 'GetLinks4b', 'url':  url, 'listitem': listitem, 'text' : name.strip(), 'img' : img}, {'title':  name.strip()}, img = 'https://d13yacurqjgara.cloudfront.net/users/393408/screenshots/1849974/attachments/310000/thumbnail/mix-tape-icon.jpg', fanart = 'https://phaven-prod.s3.amazonaws.com/files/image_part/asset/376411/zJiIP2IgvAoFrWjDxG6FfyZosnE/medium_abbfabb_03.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks4b(url, text, img):                                             
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<a href="http://deepinside.demodulated.com/(.+?)">.+?</a>').findall(content)
        for url in match:
                addon.add_directory({'mode': 'PlayVideo', 'url':  'http://deepinside.demodulated.com/' + url, 'listitem': listitem, 'text' : url, 'img' : img},  {'title':  url.replace('%20', ' ').replace('_', ' ')}, img = 'https://d13yacurqjgara.cloudfront.net/users/393408/screenshots/1849974/attachments/310000/thumbnail/mix-tape-icon.jpg', fanart = 'https://phaven-prod.s3.amazonaws.com/files/image_part/asset/376411/zJiIP2IgvAoFrWjDxG6FfyZosnE/medium_abbfabb_03.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------ ratpack ---------------------------------------------------------------------------------#

def GetLinks6(url, text, img):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<a href="(.+?)" class="podcast-title header2" target="_blank" title=".+?">(.+?)</a>').findall(content)
        for url, name in match:
                addon.add_directory({'mode': 'GetLinks6a', 'url': url, 'listitem': listitem, 'text' : name.strip(), 'img' : img}, {'title':  name.strip()}, img = 'http://media.ents24network.com/image/000/000/527/942171df2ccf89033bf2454012f1cb47b817fa9d.jpg', fanart = 'http://www.boomartistsagency.com/image/2/1170/454/2/images/profiles/_ratpack2-5118cb539b5f9.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks6a(url, text, img):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('"media_url":"(.+?)",').findall(content)
        for url in match:
                addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem, 'text' : url, 'img' : img}, {'title':  url}, img = 'http://media.ents24network.com/image/000/000/527/942171df2ccf89033bf2454012f1cb47b817fa9d.jpg', fanart = 'http://hardcorewillneverdie.com/eswe/pagez/flyerz/helter2.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#--------------------------------------------------------------------------- ukraves -------------------------------------------------------------------------------------#

def GetLinks7(url, text, img):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<h2><a href="(.+?)" target="new">(.+?)</a></h2>').findall(content)
        for url, name in match:
                addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem, 'text' : name.strip(), 'img' : img}, {'title':  name.strip()}, img = 'http://image.spreadshirt.com/image-server/v1/compositions/19412958/views/1,width=280,height=280,appearanceId=1.png/ecstasy-pill-dove-generation-t-shirt_design.png', fanart = 'http://i383.photobucket.com/albums/oo273/Senbonzakura_8/takeecstesyyoumaydiebutitllbefunalo.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#----------------------------------------------------------------------------- mikusmusik ----------------------------------------------------------------------------------#

def GetLinks9a(url, text, img):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        CLEAN(html)
        content = html
        match = re.compile("<a dir='ltr' href='(.+?)'>(.+?)</a>").findall(content)
        for url, name in match:
                addon.add_directory({'mode': 'GetLinks9b', 'url': url, 'listitem': listitem, 'text' : name.strip(), 'img' : img}, {'title':  name.strip()}, img = 'http://static.tvtropes.org/pmwiki/pub/images/Pirate_radio_station_5417.jpg', fanart = 'http://s29.postimg.org/xwiy1he6f/fanart.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks9b(url, text, img):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        CLEAN(html)
        content = html
        match = re.compile("<h3 class='post-title entry-title' itemprop='name'>\s*?<a href='(.+?)'>(.+?)</a>").findall(content)
        for url, name in match:
                addon.add_directory({'mode': 'GetLinks9c', 'url': url, 'listitem': listitem}, {'title':  name.strip(), 'text' : name.strip(), 'img' : img}, img = 'http://static.tvtropes.org/pmwiki/pub/images/Pirate_radio_station_5417.jpg', fanart = 'http://s29.postimg.org/xwiy1he6f/fanart.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks9c(url, text, img):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        CLEAN(html)
        content = html
        match = re.compile('<a href="http://www.terraincognita.co.uk/(.+?)"').findall(content)
        for url in match:
                addon.add_directory({'mode': 'PlayVideo', 'url': 'http://www.terraincognita.co.uk/' + url, 'listitem': listitem, 'text' : url, 'img' : img}, {'title':  url.replace('%20', ' ').replace('_', ' ').replace('musik/', '').replace('pirate radio/', '')}, img = 'http://static.tvtropes.org/pmwiki/pub/images/Pirate_radio_station_5417.jpg', fanart = 'http://s29.postimg.org/xwiy1he6f/fanart.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#--------------------------------------------------------------------------------- demodulated -----------------------------------------------------------------------------#

def GetLinks11(url, text, img):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        CLEAN(html)
        content = html
        match = re.compile('<li class="cat-item cat-item-.+?"><a href="(.+?)" >(.+?)</a>').findall(content)
        for url, name in match:
                addon.add_directory({'mode': 'GetLinks11a', 'url': url, 'listitem': listitem, 'text' : name.strip(), 'img' : img}, {'title':  name.strip()}, img = 'http://bonuscut.files.wordpress.com/2013/08/mixtape_cassette-13651.jpg', fanart = 'https://chronicle-vitae-production.s3.amazonaws.com/uploads/user_article/photo/133/full_11112013-mixtapes.gif')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks11a(url, text, img):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        CLEAN(html)
        content = html
        match = re.compile('<h2><a href="(.+?)" rel="bookmark" title=".+?">(.+?)</a></h2>').findall(content)
        for url, name in match:
                addon.add_directory({'mode': 'GetLinks11b', 'url': url, 'listitem': listitem, 'text' : name.strip(), 'img' : img}, {'title':  name.strip()}, img = 'http://bonuscut.files.wordpress.com/2013/08/mixtape_cassette-13651.jpg', fanart = 'http://img.wallpaperstock.net:81/vintage-cassette-retro-player-wallpapers_36465_1920x1080.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks11b(url, text, img):                                          
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        CLEAN(html)
        content = html
        match = re.compile('href="http://www.demodulated.com/music/mixsets/(.+?)">.+?</a></strong>').findall(content)
        for url in match:
                addon.add_directory({'mode': 'PlayVideo', 'url': 'http://www.demodulated.com/music/mixsets/' + url, 'listitem': listitem, 'text' : url, 'img' : img}, {'title':  url}, img = 'http://urbanlegendkampala.com/wp-content/uploads/2013/11/Mixtape-Image.jpg', fanart = 'http://img.wallpaperstock.net:81/vintage-cassette-retro-player-wallpapers_36465_1920x1080.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------- rave-archive ---------------------------------------------------------------------------------#

def GetLinks13(url, text, img):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        CLEAN(html)
        content = html
        match = re.compile("<a href='(.+?)' class='.+?' title='.+?' style='.+?'>(.+?)</a>").findall(content)
        for url, name in match:
                addon.add_directory({'mode': 'GetLinks13a', 'url': url, 'listitem': listitem, 'text' : name.strip(), 'img' : img}, {'title':  name.strip()}, img = 'https://pbs.twimg.com/profile_images/3335360596/3d9ebe5623ae5be2bab14a54625a2537.jpeg', fanart = 'http://junglejunglesound.files.wordpress.com/2013/04/jungle_logo_net.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks13a(url, text, img):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        CLEAN(html)
        content = html
        match = re.compile('<a href="(.+?)" rel="bookmark" title="(.+?)" class="img-bevel video">\s*?<img width="200" height="200" src="(.+?)" class="attachment-article-thumb wp-post-image"').findall(content)
        for url, name, img in match:
                addon.add_directory({'mode': 'GetLinks13b', 'url': url, 'listitem': listitem, 'text' : name.strip(), 'img' : img}, {'title':  name.strip()}, img =img, fanart = 'http://wallpapersus.com/wp-content/uploads/2012/02/music-animals-audio-jungle.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks13b(url, text, img):                                           
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        CLEAN(html)
        content = html
        match = re.compile('<a href="http://ravearchive.mediafire.com/file/(.+?)" target="_blank">.+?</a>').findall(content)
        match2 = re.compile('<p style="text-align: center;"><a href="http://ravearchive.mediafire.com/listen/(.+?)" target="_blank">.+?</a></p>').findall(content)
        match3 = re.compile('<a href="http://ravearchive.mediafire.com/file/(.+?)">.+?</a>').findall(content)
        match4 = re.compile('<iframe class=".+?" style=".+?" src="(.+?)"></iframe>').findall(content)
        for url in match:
                addon.add_directory({'mode': 'PlayVideo', 'url': 'http://ravearchive.mediafire.com/file/' + url, 'listitem': listitem, 'text' : url, 'img' : img}, {'title':  url.replace('_', ' ').replace('/', ' ').replace('%26', ' ')}, img = 'https://pbs.twimg.com/profile_images/3335360596/3d9ebe5623ae5be2bab14a54625a2537.jpeg', fanart = 'http://aerosoul.co.uk/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/j/u/junglist_logo_on_dark_navy_jm_hoodie.png')
        for url in match2:
                addon.add_directory({'mode': 'GetLinks13c', 'url': 'http://ravearchive.mediafire.com/listen/' + url, 'listitem': listitem, 'text' : url, 'img' : img}, {'title':  url.replace('_', ' ').replace('/', ' ').replace('%26', ' ')}, img = 'https://pbs.twimg.com/profile_images/3335360596/3d9ebe5623ae5be2bab14a54625a2537.jpeg', fanart = 'http://aerosoul.co.uk/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/j/u/junglist_logo_on_dark_navy_jm_hoodie.png')
        for url in match3:
                addon.add_directory({'mode': 'PlayVideo', 'url': 'http://ravearchive.mediafire.com/file/' + url, 'listitem': listitem, 'text' : url, 'img' : img}, {'title':  url.replace('_', ' ').replace('/', ' ').replace('%26', ' ')}, img = 'https://pbs.twimg.com/profile_images/3335360596/3d9ebe5623ae5be2bab14a54625a2537.jpeg', fanart = 'http://aerosoul.co.uk/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/j/u/junglist_logo_on_dark_navy_jm_hoodie.png')
        for url in match4:
                addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title': 'video links not supported', 'text' : url, 'img' : img}, img = 'https://pbs.twimg.com/profile_images/3335360596/3d9ebe5623ae5be2bab14a54625a2537.jpeg', fanart = 'http://aerosoul.co.uk/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/j/u/junglist_logo_on_dark_navy_jm_hoodie.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks13c(url, text, img):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        CLEAN(html)
        content = html
        match = re.compile('id="audioControlGroup">   <a href="(.+?)" target="_blank"><div').findall(content)
        for url in match:
                addon.add_directory({'mode': 'PlayVideo', 'url': 'https://www.mediafire.com/' + url, 'listitem': listitem, 'text' : url, 'img' : img}, {'title':  '[COLOR blue][B]LOAD STREAM[/B][/COLOR] ' + url}, img = 'https://pbs.twimg.com/profile_images/3335360596/3d9ebe5623ae5be2bab14a54625a2537.jpeg', fanart = 'http://junglejunglesound.files.wordpress.com/2013/04/jungle_logo_net.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------- the beat sanctuary -------------------------------------------------------------------------------------#

def GetLinks5(url, text, img):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('class="level2 item4 first"><a href="(.+?)" class="level2 item4 first"><span>(Frog and Nightgown)</span>').findall(content)
        match1 = re.compile('class="level2 item5"><a href="(.+?)" class="level2 item5"><span>(The Gass Club)</span>').findall(content)
        match2 = re.compile('class="level2 item7"><a href="(.+?)" class="level2 item7"><span>(MOS Demo Tapes)</span>').findall(content)
        match4 = re.compile('class="level3 item2"><a href="(.+?)" class="level3 item2"><span>(Risk FM)</span>').findall(content)
        match5 = re.compile('class="level3 item3"><a href="(.+?)" class="level3 item3"><span>(Pleasure FM)</span').findall(content)
        match6 = re.compile('class="level3 item4"><a href="(.+?)" class="level3 item4"><span>(Friction FM)</span>').findall(content)
        match7 = re.compile('class="level3 item5 last"><a href="(.+?)" class="level3 item5 last"><span>(Soundz FM)</span>').findall(content)
        for url, name in match + match1 + match2 + match4 + match5 + match6 + match7:
                addon.add_directory({'mode': 'GetLinks5a', 'url': 'http://www.thebeatsanctuary.co.uk/' + url, 'listitem': listitem, 'text':  name.strip(), 'img' : img}, {'title':  name.strip()}, img = 'http://i2.wp.com/musicyouneed.net/wp-content/uploads/2013/03/MYN-The-Underground.jpg?resize=290%2C290', fanart = 'https://googledrive.com/host/0B99lcOwdwe5MUDRsdkgyWS1Kems/dj-bass-music-wallpaper.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks5a(url, text, img):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile("file': 'https://dl.dropboxusercontent.com/u/(.+?)'").findall(content)
        for url in match:
                addon.add_directory({'mode': 'PlayVideo', 'url': 'https://dl.dropboxusercontent.com/u/' + url, 'listitem': listitem, 'text':  url, 'img' : img}, {'title':  url}, img = 'http://i2.wp.com/musicyouneed.net/wp-content/uploads/2013/03/MYN-The-Underground.jpg?resize=290%2C290', fanart = 'https://lh6.ggpht.com/clu-N-hZ_xyCgGm5JwtVLRXX59eSMfl59RXf9MQd23lZVvQgoa2aQNdGHU-eEfaYZMeO=h900')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------- thewire -------------------------------------------------------------------------------------#

def GetLinks14(url, text, img):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        CLEAN(html)
        content = html
        match = re.compile('<a href=".+?" data-file="(.+?)" class=".+?" title=".+?" rel="nofollow">(.+?)</a>').findall(content)
        for url, name in match:
                addon.add_directory({'mode': 'PlayVideo', 'url': 'http://www.thewire.co.uk/' + url, 'listitem': listitem, 'text':  name.strip(), 'img' : img}, {'title':  name.strip()}, img = 'http://www.hcmf.co.uk/uploads/images/197wirelogoblockurlcopy.jpg?1253097636', fanart = 'http://alicepettey.com/wp-content/uploads/2012/03/The_Wire_Logo.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------- github -------------------------------------------------------------------------------------#

def GetLinks15(url, text, img):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        CLEAN(html)
        content = html
        match = re.compile('<>title="(.+?)" href="(.+?)" />< src="(.+?)"').findall(content)
        for name, url, img in match:
                addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem, 'text':  name.strip(), 'img' : img}, {'title':  name.strip()}, img=img , fanart = 'http://i1.sndcdn.com/artworks-000047576476-bckt74-original.jpg?77d7a69')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------- github vids ----------------------------------------------------------------------------------------#

def GetLinksvids(url):
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        CLEAN(html)
        content = html
        match = re.compile('<>title="(.+?)" href="(.+?)" /><').findall(content)
        for name, url in match:
                if urlresolver.HostedMediaFile(url= url):
                        addon.add_directory({'mode': 'PlayVideo1', 'url': url, 'listitem': listitem}, {'title':  name.strip()}, img= 'http://www.londonpirates.co.uk/PBVid.jpg' , fanart = 'http://fc04.deviantart.net/fs70/i/2011/326/4/5/pirate_radio_wallpaper_by_pastorgavin-d4gz73g.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def PlayVideo1(url, listitem):
    try:
        print 'in PlayVideo %s' % url
        stream_url = urlresolver.HostedMediaFile(url).resolve()
        xbmc.Player().play(stream_url)
        addon.add_directory({'mode': 'help'}, {'title':  '[COLOR slategray][B]^^^ Press back ^^^[/B] [/COLOR]'},'','')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry Link may have been removed ![/B][/COLOR],[COLOR lime][B]Please try a different link/host !![/B][/COLOR],7000,"")")

#------------------------------------------------------------------------------- ltj Bukem Mixtapes Collection -------------------------------------------------------------------------------------#

def GetLinks17(url, text, img):                                                                                       
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        CLEAN(html)
        content = html
        match = re.compile('<div class="format-file">\s*?<div class="down-rite">(.+?)</div>\s*?<a class="stealth download-pill" href="/download/175bpm.plLtjBukemMixtapesCollection/(.+?).mp3">\s*?(.+?)\s*?<span class="iconochive-download"').findall(content)
        for time, url, name in match:
                addon.add_directory({'mode': 'PlayVideo', 'url': 'https://archive.org/download/175bpm.plLtjBukemMixtapesCollection/' + url + '.mp3', 'listitem': listitem, 'text':  name, 'img' : img}, {'title':  name + '-' + ' ' + time}, img = 'http://www.djsets.co.uk/Compilations/ltjbukem/ltj-bukem.jpg', fanart = 'http://soulsinaction.com/wp-content/uploads/2015/01/lauralewis_ltj-bukem_forum_low_resimg_6919.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#a------------------------------------------------------------------------------- Helter Skelter Collection -----######

def GetLinks17a(url, text, img):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        CLEAN(html)
        content = html
        match = re.compile('<div class="format-file">\s*?<div class="down-rite">(.+?)</div>\s*?<a class="stealth download-pill" href="/download/(.+?).mp3">\s*?(.+?)\s*?<span class="iconochive-download"').findall(content)
        for time, url, name in match:
                addon.add_directory({'mode': 'PlayVideo', 'url': 'https://archive.org/download/' + url + '.mp3', 'listitem': listitem, 'text':  name, 'img' : img}, {'title':  name + '-' + ' ' + time}, img = 'http://www.djsets.co.uk/Compilations/helterskelter/hs3.jpg', fanart = 'http://www.oldskoolanthemz.com/forum/attachments/file-sharing/27640d1224888916-dj-warlock-helter-skelter-zoom-9-12-95-untitled.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------- toronto rave mixtape archive -------------------------------------------------------------------------------------#

def GetLinks18(url, text, img):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        CLEAN(html)
        content = html
        match = re.compile('<li><a href="(.+?)"><span>(Jungle / Hardcore)</span></a></li>').findall(content)
        match1 = re.compile('<li><a href="(.+?)"><span>(House / Techno)</span></a></li>').findall(content)
        match2 = re.compile('<li><a href="(.+?)"><span>(Studio)</span></a></li>').findall(content)
        match3 = re.compile('<li><a href="(.+?)"><span>(X-Static)</span></a></li>').findall(content)
        for url, name in match + match1 + match2 + match3:
                addon.add_directory({'mode': 'GetLinks18a', 'url': 'http://torontoravemixtapearchive.com/' + url, 'listitem': listitem, 'text':  name.strip(), 'img' : img}, {'title':  name.strip()}, img = 'http://www.torontoravemixtapearchive.com/images/promo/trma.jpg', fanart = 'http://dropthebeatz.com/wp-content/uploads/2013/08/EDMcrowd.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks18a(url, text, img):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        CLEAN(html)
        content = html
        match = re.compile('>.+?<a href="http://www.torontoravemixtapearchive.com/files/(.+?)">').findall(content)
        match1 = re.compile('>.+?-.+?- <a href="http://www.torontoravemixtapearchive.com/files/(.+?)">').findall(content)
        match2 = re.compile('>Download </a><br />\s*?<a href="http://www.torontoravemixtapearchive.com/files/(.+?)">').findall(content)
        match4 = re.compile('N.+?<a href="http://www.torontoravemixtapearchive.com/files/(.+?)">').findall(content)
        match3 = re.compile('Andy.+?<a href="http://www.torontoravemixtapearchive.com/files/(.+?)">').findall(content)
        match5 = re.compile('k.+?<a href="http://www.torontoravemixtapearchive.com/files/(.+?)">').findall(content)
        match6 = re.compile(' 1.+?<a href="http://www.torontoravemixtapearchive.com/files/(.+?)">').findall(content)
        for url in match + match1 + match2 + match3 + match4 + match5 + match6:
                url = url.replace(' ','%20')
                url = url.replace('_','%20')
                addon.add_directory({'mode': 'PlayVideo', 'url': 'http://www.torontoravemixtapearchive.com/files/' + url, 'listitem': listitem, 'text':  url, 'img' : img}, {'title': url.replace('%20', ' ').replace('mixtapes/', ' ').replace('%', ' ').replace('x-static/', ' ')}, img = 'http://www.torontoravemixtapearchive.com/images/promo/trma.jpg', fanart = 'http://b.vimeocdn.com/ts/437/750/437750726_1280.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------- dj jedi -------------------------------------------------------------------------------------#

def GetLinks20(url, text, img):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        CLEAN(html)
        content = html
        match = re.compile('<p><a href="(.+?)" onClick=".+?"><strong>(.+?)</strong></a></p>').findall(content)
        for url, name in match:
                addon.add_directory({'mode': 'PlayVideo', 'url': 'http://www.dj-jedi.com/' + url, 'listitem': listitem, 'text':  name.strip(), 'img' : img}, {'title':  name.strip()}, img = 'http://www.dj-jedi.com/images/dj_jedi_logo.gif', fanart = 'http://andberlin.com/wp-content/uploads/2013/05/Lights-at-Berlin-Summer-Rave-2013.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------- liondub -------------------------------------------------------------------------------------#

def GetLinks21(url, text, img):  
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        CLEAN(html)
        content = html
        match = re.compile('<a href="http://www.djliondub.com/(.+?)" target="_blank">(.+?)</a>').findall(content)
        for url, name in match:
                addon.add_directory({'mode': 'PlayVideo', 'url': 'http://www.djliondub.com/' + url, 'listitem': listitem, 'text':  name.strip(), 'img' : img}, {'title':  name.strip()}, img = 'http://www.djliondub.com/LIONDUB_B+W_LOGO.jpg', fanart = 'http://blog.dubspot.com/files/2011/03/ldlabe.jpeg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))                                          

#------------------------------------------------------------------------------- john-b -------------------------------------------------------------------------------------#

def GetLinks22(url, text, img):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<p>LINK FOR DIRECT DOWNLOAD OF MP3: <a href="http://podcast.johnbpodcast.com/content/(.+?)"').findall(content)
        for url in match:
                addon.add_directory({'mode': 'PlayVideo', 'url': 'http://podcast.johnbpodcast.com/content/' + url, 'listitem': listitem, 'text':  url, 'img' : img}, {'title':  url}, img = 'http://beta-recordings.com/images/Blog.jpg', fanart = 'http://img.nnov.org/data/myupload/1/75/1075294/4724778-img-6211.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------- dj ez -------------------------------------------------------------------------------------#

def GetLinks23(url, text, img):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        CLEAN(html)
        content = html
        match = re.compile('<br />\s*?(.+?)<br />\s*?<a href="http://www.mediafire.com/(.+?)" target="_blank"').findall(content)
        for name, url in match:
                addon.add_directory({'mode': 'GetLinks23a', 'url': 'http://www.mediafire.com/' + url, 'listitem': listitem, 'text':  name, 'img' : img}, {'title':  name}, img = 'http://3.bp.blogspot.com/-jRPq1Szx0Js/TjaX0R0DFTI/AAAAAAAAANE/6ds6AbbuD2s/s320/dj+ez+photo', fanart = 'http://turksandunderdog.com/wp-content/uploads/2014/02/DJ-EZ-turks-and-underdog.jpeg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks23a(url, text, img):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        CLEAN(html)
        content = html
        match = re.compile('kNO = "http://download(.+?)"').findall(content)
        for url in match:
                addon.add_directory({'mode': 'PlayVideo', 'url': 'http://download' + url, 'listitem': listitem, 'text':  url, 'img' : img}, {'title':  url.replace('_', ' ')}, img = 'http://wallpoper.com/images/00/06/93/69/turntable_00069369.jpg', fanart = 'http://i1.ytimg.com/vi/Busq9tROYlo/maxresdefault.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


#------------------------------------------------------------------------------- hng -------------------------------------------------------------------------------------#

def GetLinks24(url, text, img):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<a href="(.+?)" class="podcast-title header2" target="_blank" title=".+?">(.+?)</a>').findall(content)
        for url, name in match:
                addon.add_directory({'mode': 'GetLinks24a', 'url': url, 'listitem': listitem, 'text':  name.strip(), 'img' : img}, {'title':  name.strip()}, img = 'http://assets.podomatic.net/ts/cf/4b/3d/djtrudos/1400x1400_9185047.jpg', fanart = 'http://i1.ytimg.com/vi/LxXDk61hrcY/hqdefault.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks24a(url, text, img):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('"media_url":"(.+?)",').findall(content)
        for url in match:
                addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem, 'text':  url, 'img' : img}, {'title':  url}, img = 'http://assets.podomatic.net/ts/cf/4b/3d/djtrudos/1400x1400_9185047.jpg', fanart = 'http://i1.ytimg.com/vi/LxXDk61hrcY/hqdefault.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------- Hardcore Highlights -------------------------------------------------------------------------------------#

def GetLinks27(url, text, img):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        CLEAN(html)
        content = html
        match = re.compile('<blockquote><p>(.+?)<br />\s*?<a href="(.+?)" target="_blank">.+?</a></p></blockquote>').findall(content)
        for name, url in match:
                addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem, 'text':  name.strip(), 'img' : img}, {'title':  name.strip()}, img = 'http://s28.postimg.org/qvbsfp7v1/Hardcore_Highlights_Small.png', fanart = 'http://wallpoper.com/images/00/41/10/87/abstract-hardcore_00411087.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------- thepiratearchive -------------------------------------------------------------------------------------#

def GetLinks31(url, text, img):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        CLEAN(html)
        content = html
        match = re.compile('href="http://www.piratearchive.co.uk/(.+?)">(.+?)<').findall(content)
        for url, name in match:
                addon.add_directory({'mode': 'PlayVideo', 'url':'http://www.piratearchive.co.uk/' + url, 'listitem': listitem, 'text':  name.strip(), 'img' : img}, {'title': name.strip()}, img = 'http://i192.photobucket.com/albums/z274/thedjguy/raveSp.jpg', fanart = 'http://dash.coolsmartphone.com/wp-content/uploads/2014/07/t1.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks31a(url, text, img):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        CLEAN(html)
        content = html
        match2 = re.compile('href="http://www.piratearchive.co.uk/westmids/kool/(.+?)">(.+?)</a></td>').findall(content)
        for url, name in match2:
                url = url.replace('&amp;','&')
                addon.add_directory({'mode': 'PlayVideo', 'url': 'http://www.piratearchive.co.uk/westmids/kool/' + url, 'listitem': listitem, 'text':  name.strip(), 'img' : img}, {'title': name.strip()}, img = 'http://i192.photobucket.com/albums/z274/thedjguy/raveSp.jpg', fanart = 'http://dash.coolsmartphone.com/wp-content/uploads/2014/07/t1.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#                url = url.replace('&amp;','&')
#------------------------------------------------------------------------------- grimetapes -------------------------------------------------------------------------------------#

def GetLinks32(url, text, img):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        CLEAN(html)
        content = html
        match = re.compile('<div class="post_text_body title_text"><a href="(.+?)">(.+?)<').findall(content)
        for url, name in match:
                addon.add_directory({'mode': 'GetLinks32a', 'url': url, 'listitem': listitem, 'text':  name.strip(), 'img' : img}, {'title':  name.strip()}, img = 'http://sd.keepcalm-o-matic.co.uk/i/keep-calm-and-listen-to-grime-27.png', fanart = 'http://i.ytimg.com/vi/2S0APTthTpI/hqdefault.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks32a(url, text, img):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        CLEAN(html)
        content = html
        match = re.compile('<div class=".+?" id=".+?"><div class=".+?"><div class=".+?"><div class=".+?">(.+?)</div><div id=".+?" class=".+?"><p><a href="(.+?)">.+?</a></p></div></div></div></div>').findall(content)
        for name, url in match:
                addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem, 'text':  name.strip(), 'img' : img}, {'title':  name.strip()}, img = 'http://sd.keepcalm-o-matic.co.uk/i/keep-calm-and-listen-to-grime-27.png', fanart = 'http://i.ytimg.com/vi/2S0APTthTpI/hqdefault.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------- braindamage -------------------------------------------------------------------------------------#

def GetLinks35(url, text, img):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        CLEAN(html)
        content = html
        match = re.compile('<span class="medium_text1"><a href="(.+?)" >(.+?)</a> </span>').findall(content)
        for url, name in match:
                addon.add_directory({'mode': 'GetLinks35a', 'url': 'http://www.braindamageradio.com/' + url, 'listitem': listitem, 'text':  name.strip(), 'img' : img}, {'title':  name.strip()}, img = 'http://www.braindamageradio.com/templates/skinnydesigns-base/images/logo.png', fanart = 'http://2.bp.blogspot.com/_WldfNndrX0k/TBTztaKCkAI/AAAAAAAABSI/uU1tq3XgRZg/s1600/BRAIN+DAMAGE+WALLPAPER+2.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks35a(url, text, img):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        CLEAN(html)
        content = html
        match = re.compile('<span class="link_medium_text1"><a href="(.+?)">Download</a>').findall(content)
        for url in match:
                addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem, 'text':  url, 'img' : img}, {'title':  'Load Stream : ' + text}, img = 'http://www.braindamageradio.com/templates/skinnydesigns-base/images/logo.png', fanart = 'http://2.bp.blogspot.com/_WldfNndrX0k/TBTztaKCkAI/AAAAAAAABSI/uU1tq3XgRZg/s1600/BRAIN+DAMAGE+WALLPAPER+2.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------- oldskoolanthemz -------------------------------------------------------------------------------------#

def GetLinks36(url, text, img):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        CLEAN(html)
        content = html
        match = re.compile('<li><a href="(.+?)">(.+?)</a></li>').findall(content)
        for url, name in match:
                addon.add_directory({'mode': 'PlayVideo', 'url': 'http://www.oldskoolanthemz.com/media/Mix%20Archive/Misc/' + url, 'listitem': listitem, 'text':  url, 'img' : img}, {'title':  name.strip()}, img = 'http://i192.photobucket.com/albums/z274/thedjguy/raveSp.jpg', fanart = 'http://www.pulsarmedia.eu/data/media/24/Music%20in%20Pictures%20(63).jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------- oldskoolanthemz Collection -------------------------------------------------------------------------------------#

def GetLinks38(url, text, img):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        CLEAN(html)
        content = html
        match = re.compile('<li><a href="(.+?)">(.+?).mp3</a></li>').findall(content)
        for url, name in match:
                addon.add_directory({'mode': 'PlayVideo', 'url': 'http://www.oldskoolanthemz.com/media/Tune%20Archive/Early%20House/' + url, 'listitem': listitem, 'text' : name, 'img' : img}, {'title':  name}, img = 'http://pixabay.com/static/uploads/photo/2014/04/02/10/13/vinyl-303160_640.png', fanart = 'http://www.beat.com.au/sites/default/files/images/article/header/2010/november/197563926818f401532b.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks38a(url, text, img):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        CLEAN(html)
        content = html
        match = re.compile('<li><a href="(.+?)">(.+?).mp3</a></li>').findall(content)
        for url, name in match:
                addon.add_directory({'mode': 'PlayVideo', 'url': 'http://www.oldskoolanthemz.com/media/Tune%20Archive/Nu%20Skool/' + url, 'listitem': listitem, 'text' : name, 'img' : img}, {'title':  name}, img = 'http://pixabay.com/static/uploads/photo/2014/04/02/10/13/vinyl-303160_640.png', fanart = 'http://www.beat.com.au/sites/default/files/images/article/header/2010/november/197563926818f401532b.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks38b(url, text, img):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        CLEAN(html)
        content = html
        match = re.compile('<li><a href="(.+?)">(.+?).mp3</a></li>').findall(content)
        for url, name in match:
                addon.add_directory({'mode': 'PlayVideo', 'url': 'http://www.oldskoolanthemz.com/media/Tune%20Archive/Old%20Skool%20Classics/' + url, 'listitem': listitem, 'text' : name, 'img' : img}, {'title':  name}, img = 'http://pixabay.com/static/uploads/photo/2014/04/02/10/13/vinyl-303160_640.png', fanart = 'http://www.beat.com.au/sites/default/files/images/article/header/2010/november/197563926818f401532b.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks38c(url, text, img):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        CLEAN(html)
        content = html
        match = re.compile('<li><a href="(.+?)">(.+?).mp3</a></li>').findall(content)
        for url, name in match:
                addon.add_directory({'mode': 'PlayVideo', 'url': 'http://www.oldskoolanthemz.com/media/Tune%20Archive/Old%20Skool%20Hardcore/' + url, 'listitem': listitem, 'text' : name, 'img' : img}, {'title':  name}, img = 'http://pixabay.com/static/uploads/photo/2014/04/02/10/13/vinyl-303160_640.png', fanart = 'http://www.beat.com.au/sites/default/files/images/article/header/2010/november/197563926818f401532b.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------- AMS -------------------------------------------------------------------------------------#

def GetLinks39(url, text, img):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        CLEAN(html)
        content = html
        match = re.compile('<a href="(.+?)">.+?</a>.+?-').findall(content)
        for url in match:
                addon.add_directory({'mode': 'GetLinks39a', 'url': 'http://artmeetsscience.co.uk/tapes/' + url, 'listitem': listitem, 'text':  url, 'img' : 'http://artmeetsscience.co.uk/tapes/' + url}, {'title':  url.replace('%20', ' ').replace('/', '').replace('?C=N;O=D', '          ~ Links Provided by artmeetsscience.co.uk ~').replace('%0d', '').replace('Sign Up', '').replace('Log In', '').replace('SearchDance', '').replace('Paradise Volume 1', '             ~ Keeping Jungle Alive ~')}, img = 'http://www.livinproof.co.uk/wordpress/wp-content/uploads/junglist_540.jpg', fanart = 'http://artmeetsscience.co.uk/images/holding.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks39a(url, text, img):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        CLEAN(html)
        content = html
        match = re.compile('<a href="(.+?)">(.+?)</a>.+?M').findall(content)
        for url, name in match:
                url= img + url
                addon.add_directory({'mode': 'PlayVideo', 'url': url.replace('&amp;', '&'), 'listitem': listitem, 'text':  url.replace('%20', ' ').replace('http://artmeetsscience.co.uk/tapes/', '').replace('/', ' - ').replace('_', ' '), 'img' : img}, {'title':  url.replace('%20', ' ').replace('http://artmeetsscience.co.uk/tapes/', '').replace('/', ' - ').replace('?C=N;O=D', '').replace('_', ' ')}, img = 'http://www.livinproof.co.uk/wordpress/wp-content/uploads/junglist_540.jpg', fanart = 'http://artmeetsscience.co.uk/images/holding.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------- twiceasnice -------------------------------------------------------------------------------------#

def GetLinks40(url, text, img):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        CLEAN(html)
        content = html
        match = re.compile('<p id=".+?-show" class="featured-image">\s*?<a href="(.+?)"  title="(.+?)"><img src=".+?src=(.+?)&amp;zc=0&amp;h=230" alt=".+?" /></a>').findall(content)
        match1 = re.compile('<li class="current">.+?</li>\s*?<li><a href="(.+?)" title="Go to page.+?">(.+?)</a></li>').findall(content)
        for url, name, img in match:
                addon.add_directory({'mode': 'GetLinks40a', 'url': url, 'listitem': listitem, 'text':  name, 'img' : 'http://www.twiceasnice.co.uk/' + img}, {'title':  name}, img = 'http://www.twiceasnice.co.uk/' + img, fanart = 'http://www.twiceasnice.co.uk/media/201110/window2[1].jpg')
        for url, name in match1:
                addon.add_directory({'mode': 'GetLinks40', 'url': 'http://www.twiceasnice.co.uk/mix/' + name, 'listitem': listitem, 'text':  name, 'img' : img}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]' + name}, img = 'https://raw.githubusercontent.com/MrEntertainment/EntertainmentREPO/master/plugin.video.theyidrh/icons/nextpage1.png', fanart = 'http://www.twiceasnice.co.uk/media/201110/window2[1].jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks40a(url, text, img):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        CLEAN(html)
        content = html
        match = re.compile('''<iframe scrolling=".+?" frameborder=".+?" width=".+?" height=".+?" src=".+?"></iframe><form><input type="button" value="Download Now" onClick="window.location.href='(.+?)'"></form>''').findall(content)
        for url in match:
                addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem, 'text':  text, 'img' : img}, {'title':  text}, img = img, fanart = 'http://www.twiceasnice.co.uk/media/201110/window2[1].jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------- radionecks -------------------------------------------------------------------------------------#

def GetLinks41(url, text, img):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<br />(.+?)- <!-- m --><a class="postlink" href=".+?">(.+?)</a>').findall(content)
        for name, url in match:
                addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem, 'text':  name.replace('<br', '').replace('/', '').replace('>', ''), 'img' : img}, {'title':  name.replace('<br', '').replace('/', '').replace('>', '')}, img = 'https://pbs.twimg.com/profile_images/2151054574/moblogo1_400x400.jpg', fanart = 'http://i.imgur.com/yXimypO.jpg?1')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


##.replace(' ', ' ')# \s*? ##url = url.replace(' ', ' ')##
######################################################################### clean ###########################################################################################

def CLEAN(string):
    def substitute_entity(match):
        ent = match.group(3)
        if match.group(1) == "#":
            if match.group(2) == '':
                return unichr(int(ent))
            elif match.group(2) == 'x':
                return unichr(int('0x'+ent, 16))
        else:
            cp = n2cp.get(ent)
            if cp: return unichr(cp)
            else: return match.group()
    entity_re = re.compile(r'&(#?)(x?)(\d{1,5}|\w{1,8});')
    return entity_re.subn(substitute_entity, string)[0]

############################################################################# Play Video #####################################################################################

def PlayVideo(url, listitem, text, img):
        addon_handle = int(sys.argv[1])
        xbmcplugin.setContent(addon_handle, 'audio')
        li = xbmcgui.ListItem('[COLOR dodgerblue][B]PLAY STREAM[/B][/COLOR] : ' + text, iconImage='http://www.sayerhamilton.com/resources/images/hear/tape.png', thumbnailImage= 'http://www.sayerhamilton.com/resources/images/hear/tape.png')
        li.setProperty('fanart_image', 'http://i218.photobucket.com/albums/cc291/FMonyourdial/KEV/I%20PARTY/rave-babie-blue-lights.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
        xbmcplugin.endOfDirectory(addon_handle)

################################################################################ ListItem #################################################################################

def GetMediaInfo(html):
        listitem = xbmcgui.ListItem()
        match = re.search('og:title" content="(.+?) \((.+?)\)', html)
        if match:
                print match.group(1) + ' : '  + match.group(2)
                listitem.setInfo('video', {'Title': match.group(1), 'Year': int(match.group(2)) } )
        return listitem

################################################################################# menus ####################################################################################################

#------------------------------------------------------------------------------------------ MainMenu ----------------------------------------------------------------------------#

def MainMenu():    #homescreen
        addon.add_directory({'mode': 'RadioMenu'}, {'title':  '[COLOR orchid][B]Live Radio [/COLOR](Streaming)[/B]'}, img = 'http://radio.aljalia.tv/images/on_air.png', fanart = 'http://tamtam.mao-jp.com/wp-content/uploads/2014/04/news12112012-4c.png')
        addon.add_directory({'mode': 'VRadioMenu'}, {'title':  '[COLOR plum][B]Live Radio [/COLOR](Video Streaming)[/B]'}, img = 'http://cynthiastott.com/wp-content/uploads/2013/07/on-air.png', fanart = 'http://wallpoper.com/images/00/27/33/92/radio-dial_00273392.jpg')
        addon.add_directory({'mode': 'RaMenu'}, {'title':  '[COLOR thistle][B]Pirate Radio [/COLOR](Archives)[/B]'}, img = 'http://www.jgenvironmental.co.uk/wp-content/uploads/2013/03/radio-waves-hi.png', fanart = 'http://upload.wikimedia.org/wikipedia/commons/9/93/Video_tape_archive_storage_(6498637005).jpg')
        addon.add_directory({'mode': 'ArchiveMenu'}, {'title':  '[COLOR green][B]Rave Tape packs & Dj sets [/COLOR](Archives)[/B]'}, img = 'http://www.missiongiant.com/navBar/Cassette-Tape.jpg', fanart = 'http://2.bp.blogspot.com/-1stPxBQVgrk/TyHnBXUxYCI/AAAAAAAAAhU/uOQNvSSRr8c/s1600/1218_bg.jpg')
        addon.add_directory({'mode': 'PodMenu'}, {'title':  '[COLOR chartreuse][B]Podcasts [/COLOR](Archives)[/B]'}, img = 'http://www.digitaldjhub.com/wp-content/uploads/podcast-logo.png', fanart = 'http://p1.pichost.me/i/37/1597754.jpg')
        addon.add_directory({'mode': 'StMenu'}, {'title':  '[COLOR royalblue][B]Single Tunes [/COLOR](Archives)[/B]'}, img = 'http://pixabay.com/static/uploads/photo/2014/04/02/10/13/vinyl-303160_640.png', fanart = 'http://www.beat.com.au/sites/default/files/images/article/header/2010/november/197563926818f401532b.jpg')
        addon.add_directory({'mode': 'HngMenu'}, {'title':  '[COLOR coral][B]House & Garage [/COLOR](Archives)[/B]'}, img = 'http://cps-static.rovicorp.com/3/JPG_400/MI0001/759/MI0001759699.jpg?partner=allrovi.com', fanart = 'http://jack-records.com/wp-content/uploads/2011/12/0.jpg')
        addon.add_directory({'mode': 'HelpMenu'}, {'title':  '[COLOR gold][B]TWITTER [/B][/COLOR] [COLOR aqua][B][I]@TheYid009 [/B][/I][/COLOR]'}, img = 'https://raw.githubusercontent.com/MrEntertainment/EntertainmentREPO/master/repository.entertainmentrepo/icon.png', fanart = 'http://s30.postimg.org/elc1pa6qp/fanart.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#-------------------------------------------------------------------------------------------- HelpMenu ---------------------------------------------------------------------#

def HelpMenu():   
        dialog = xbmcgui.Dialog()
        dialog.ok("TheYid's REPO", "1 man 1 repo", "FOR donations goto ","http://bit.do/theyidsrepo")

#------------------------------------------------------------------------------------------- RaMenu ---------------------------------------------------------------------#

def RaMenu(): 
        addon.add_directory({'mode': 'GetLinks15', 'url': BASE_URL15 + '/vids.txt'}, {'title':  '[COLOR deeppink][B]***Rave player Specials*** [/COLOR] (Pirate Radio History videos)[/B]'}, img = 'https://blog52.files.wordpress.com/2008/04/lpfm.jpg', fanart = 'http://non-fiction.eu/wp-content/uploads/2013/04/pirate_radio_2.jpg')
        addon.add_directory({'mode': 'ArMenu'}, {'title':  '[COLOR green][B]The Pirate Archive [/COLOR](All Genres, 1988 to present day)[/B]'}, img = 'http://www.thepiratearchive.net/wordpress/wp-content/uploads/2013/01/logo4e300w.png', fanart = 'http://oi60.tinypic.com/30a8c3n.jpg')
        addon.add_directory({'mode': 'GetLinks', 'url': BASE_URL + '/'}, {'title':  '[COLOR green][B]One In The Jungle [/COLOR](BBC Radio 1)[/B]'}, img = 'http://images-mix.netdna-ssl.com/w/318/h/318/q/90/upload/images/extaudio/6d90c82e-aa53-4d69-85a7-bf3504baa5ae.png', fanart = 'http://4.bp.blogspot.com/-ByJompomPtM/Tzb9-SOCseI/AAAAAAAAAMU/-Zc6FiSMM18/s1600/photo.jpg')
        addon.add_directory({'mode': 'GetLinks9a', 'url': BASE_URL9 + '/'}, {'title':  '[COLOR green][B]mikus Musik [/COLOR](All Genres)[/B]'}, img = 'http://3.bp.blogspot.com/-iDTTgsZBiBA/TwHRQBfrEKI/AAAAAAAAATs/8lTy5Va4_is/s1600/MIKUS.gif', fanart = 'http://s23.postimg.org/4sn8qcp8b/fanart.jpg')
        addon.add_directory({'mode': 'GetLinks42', 'url': BASE_URL42 + '/tapes'}, {'title':  '[COLOR green][B]Jungle Tapes [/COLOR](Toronto jungle radio shows )[/B]'}, img = 'http://jungletapes.com/sites/default/files/jungle_tapes_large_logo.png', fanart = 'http://neworleans.media.indypgh.org/uploads/2005/11/tbfa_transmitter_9-12-05.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def ArMenu(): 
        addon.add_directory({'mode': 'GetLinks15', 'url': BASE_URL15 + '/radioshows.txt'}, {'title':  '[COLOR gold][B]Oldskool Radio Specials [/COLOR] (The Lost Tapes)[/B]'}, img = 'http://s12.postimg.org/3szbuobot/icon.png', fanart = 'http://4.bp.blogspot.com/_8V97VYqI3Po/S7Md-Sd5OcI/AAAAAAAABGk/haepgezjFqw/s1600/24897_410278471302_133985331302_5619646_2569052_n.jpg')
        #addon.add_directory({'mode': 'GetLinks31', 'url': BASE_URL31 + '/girls-fm-london/'}, {'title':  '[COLOR green][B]Girls FM - London [/COLOR] (oldskool dj sets)[/B]'}, img = 'http://www.subulahanews.com/wp-content/uploads/2013/09/fm-logo-red.png', fanart = 'http://4.bp.blogspot.com/_8V97VYqI3Po/S7Md-Sd5OcI/AAAAAAAABGk/haepgezjFqw/s1600/24897_410278471302_133985331302_5619646_2569052_n.jpg')
        #addon.add_directory({'mode': 'GetLinks31', 'url': BASE_URL31 + '/premier-fm-essex/'}, {'title':  '[COLOR green][B]Premier FM - essex [/COLOR] (oldskool dj sets)[/B]'}, img = 'http://www.thepiratearchive.net/wordpress/wp-content/uploads/2014/02/StationLogo-300x42.jpg', fanart = 'http://4.bp.blogspot.com/_8V97VYqI3Po/S7Md-Sd5OcI/AAAAAAAABGk/haepgezjFqw/s1600/24897_410278471302_133985331302_5619646_2569052_n.jpg')
        addon.add_directory({'mode': 'GetLinks31a', 'url': BASE_URL31 + 'kool-fm-birmingham/'}, {'title':  '[COLOR green][B]Kool FM - birmingham [/COLOR] (oldskool dj sets)[/B]'}, img = 'http://s0.hulkshare.com/song_images/original/1/b/a/1ba96478934405ef5a9a2528947804ec.jpg?dd=1388552400')
        #addon.add_directory({'mode': 'GetLinks31', 'url': BASE_URL31 + 'centreforce-radio-london/'}, {'title':  '[COLOR green][B]Centreforce FM - London [/COLOR] (oldskool dj sets)[/B]'}, img = 'http://i.ytimg.com/vi/ujOon-c2T-4/0.jpg', fanart = 'http://4.bp.blogspot.com/_8V97VYqI3Po/S7Md-Sd5OcI/AAAAAAAABGk/haepgezjFqw/s1600/24897_410278471302_133985331302_5619646_2569052_n.jpg')
        #addon.add_directory({'mode': 'GetLinks31', 'url': BASE_URL31 + 'fantasy-fm-london/'}, {'title':  '[COLOR green][B]Fantasy FM - London [/COLOR] (oldskool dj sets)[/B]'}, img = 'http://www.thepiratearchive.net/wordpress/wp-content/uploads/2013/07/FantasyFM-London-Logo-300x198.jpg', fanart = 'http://4.bp.blogspot.com/_8V97VYqI3Po/S7Md-Sd5OcI/AAAAAAAABGk/haepgezjFqw/s1600/24897_410278471302_133985331302_5619646_2569052_n.jpg')
        addon.add_directory({'mode': 'GetLinks31', 'url': BASE_URL31 + 'kiss-ldn/'}, {'title':  '[COLOR green][B]kiss FM - London [/COLOR] (oldskool dj sets)[/B]'}, img = 'http://www.thepiratearchive.net/wordpress/wp-content/uploads/2013/01/KissFM-London-DONE1.jpg', fanart = 'http://4.bp.blogspot.com/_8V97VYqI3Po/S7Md-Sd5OcI/AAAAAAAABGk/haepgezjFqw/s1600/24897_410278471302_133985331302_5619646_2569052_n.jpg')
        addon.add_directory({'mode': 'GetLinks31', 'url': BASE_URL31 + 'fresh/'}, {'title':  '[COLOR green][B]Fresh FM - Leicester[/COLOR] (oldskool dj sets)[/B]'}, img = 'http://www.thepiratearchive.net/wordpress/wp-content/uploads/2013/04/FreshLogo1.jpg', fanart = 'http://4.bp.blogspot.com/_8V97VYqI3Po/S7Md-Sd5OcI/AAAAAAAABGk/haepgezjFqw/s1600/24897_410278471302_133985331302_5619646_2569052_n.jpg')
        addon.add_directory({'mode': 'GetLinks31', 'url': BASE_URL31 + 'dream/'}, {'title':  '[COLOR green][B]Dream FM - Leeds [/COLOR] (oldskool dj sets)[/B]'}, img = 'http://www.thepiratearchive.net/wordpress/wp-content/uploads/2013/04/DreamLogo2.jpg', fanart = 'http://4.bp.blogspot.com/_8V97VYqI3Po/S7Md-Sd5OcI/AAAAAAAABGk/haepgezjFqw/s1600/24897_410278471302_133985331302_5619646_2569052_n.jpg')
        addon.add_directory({'mode': 'GetLinks31', 'url': BASE_URL31 + 'dbc/'}, {'title':  '[COLOR green][B]DBC - London [/COLOR] (oldskool dj sets)[/B]'}, img = 'http://www.thepiratearchive.net/wordpress/wp-content/uploads/2013/01/dbc20logohj7-300x267.gif', fanart = 'http://4.bp.blogspot.com/_8V97VYqI3Po/S7Md-Sd5OcI/AAAAAAAABGk/haepgezjFqw/s1600/24897_410278471302_133985331302_5619646_2569052_n.jpg')
        #addon.add_directory({'mode': 'GetLinks31', 'url': BASE_URL31 + 'passion-bristol/'}, {'title':  '[COLOR green][B]Passion FM - Bristol [/COLOR] (oldskool dj sets)[/B]'}, img = 'https://fbexternal-a.akamaihd.net/safe_image.php?d=AQByp4lgCMD2CWHd&w=377&h=197&url=http%3A%2F%2Fwww.passionrb.com%2Fwp-content%2Fuploads%2F2013%2F09%2FRefreshWebsiteBANNER2.jpg&cfs=1', fanart = 'http://4.bp.blogspot.com/_8V97VYqI3Po/S7Md-Sd5OcI/AAAAAAAABGk/haepgezjFqw/s1600/24897_410278471302_133985331302_5619646_2569052_n.jpg')

        addon_handle = int(sys.argv[1]) 
        xbmcplugin.setContent(addon_handle, 'audio')
        url = 'https://archive.org/download/repoman008_gmail_Pink/centreforce.m3u'
        li = xbmcgui.ListItem('[COLOR green][B]Centreforce FM - London [/COLOR] (oldskool dj sets)[/B]', iconImage='http://i.ytimg.com/vi/ujOon-c2T-4/0.jpg', thumbnailImage='http://i.ytimg.com/vi/ujOon-c2T-4/0.jpg')
        li.setProperty('fanart_image', 'http://4.bp.blogspot.com/_8V97VYqI3Po/S7Md-Sd5OcI/AAAAAAAABGk/haepgezjFqw/s1600/24897_410278471302_133985331302_5619646_2569052_n.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        xbmcplugin.setContent(addon_handle, 'audio')
        url = 'https://archive.org/download/repoman008_gmail_Pink/kiss.m3u'
        li = xbmcgui.ListItem('[COLOR green][B]Kiss - London [/COLOR] (oldskool dj sets)[/B]', iconImage='http://www.thepiratearchive.net/wordpress/wp-content/uploads/2013/01/KissFM-London-DONE1.jpg', thumbnailImage='http://www.thepiratearchive.net/wordpress/wp-content/uploads/2013/01/KissFM-London-DONE1.jpg')
        li.setProperty('fanart_image', 'http://4.bp.blogspot.com/_8V97VYqI3Po/S7Md-Sd5OcI/AAAAAAAABGk/haepgezjFqw/s1600/24897_410278471302_133985331302_5619646_2569052_n.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        xbmcplugin.setContent(addon_handle, 'audio')
        url = 'https://archive.org/download/repoman008_gmail_Pink/kool.m3u'
        li = xbmcgui.ListItem('[COLOR green][B]Kool FM - birmingham (A) [/COLOR] (oldskool dj sets)[/B]', iconImage='http://koolfm.org.uk/assets/images/koolfm.png', thumbnailImage='http://koolfm.org.uk/assets/images/koolfm.png')
        li.setProperty('fanart_image', 'http://4.bp.blogspot.com/_8V97VYqI3Po/S7Md-Sd5OcI/AAAAAAAABGk/haepgezjFqw/s1600/24897_410278471302_133985331302_5619646_2569052_n.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        xbmcplugin.setContent(addon_handle, 'audio')
        url = 'https://archive.org/download/koollondon/koollondon.m3u'
        li = xbmcgui.ListItem('[COLOR green][B]Kool fm london [/COLOR] (oldskool dj sets)[/B]', iconImage='http://s0.hulkshare.com/song_images/original/1/b/a/1ba96478934405ef5a9a2528947804ec.jpg?dd=1388552400', thumbnailImage='http://s0.hulkshare.com/song_images/original/1/b/a/1ba96478934405ef5a9a2528947804ec.jpg?dd=1388552400')
        li.setProperty('fanart_image', 'http://4.bp.blogspot.com/_8V97VYqI3Po/S7Md-Sd5OcI/AAAAAAAABGk/haepgezjFqw/s1600/24897_410278471302_133985331302_5619646_2569052_n.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        xbmcplugin.setContent(addon_handle, 'audio')
        url = 'https://archive.org/download/repoman008_gmail_Pink/rush.m3u'
        li = xbmcgui.ListItem('[COLOR green][B]Weekend Rush [/COLOR] (oldskool dj sets)[/B]', iconImage='http://hackneyhistory.files.wordpress.com/2013/01/piratees.jpg', thumbnailImage='http://hackneyhistory.files.wordpress.com/2013/01/piratees.jpg')
        li.setProperty('fanart_image', 'http://4.bp.blogspot.com/_8V97VYqI3Po/S7Md-Sd5OcI/AAAAAAAABGk/haepgezjFqw/s1600/24897_410278471302_133985331302_5619646_2569052_n.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        xbmcplugin.setContent(addon_handle, 'audio')
        url = 'https://archive.org/download/repoman008_gmail_Pink/magic.m3u'
        li = xbmcgui.ListItem('[COLOR green][B]Pure Magic 90.2 FM [/COLOR] (oldskool dj sets)[/B]', iconImage='https://raw.githubusercontent.com/TheYid/yidpics/master/icons/IMG_5390.JPG', thumbnailImage='https://raw.githubusercontent.com/TheYid/yidpics/master/icons/IMG_5390.JPG')
        li.setProperty('fanart_image', 'http://4.bp.blogspot.com/_8V97VYqI3Po/S7Md-Sd5OcI/AAAAAAAABGk/haepgezjFqw/s1600/24897_410278471302_133985331302_5619646_2569052_n.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------------------ HngMenu ----------------------------------------------------------------------------#

def HngMenu():
        addon.add_directory({'mode': 'GetLinks15', 'url': BASE_URL15 + '/radioshows2.txt'}, {'title':  '[COLOR gold][B]Rave player Specials [/COLOR] (Club Sets)[/B]'}, img = 'http://www.ubuzz.net/photos/albums/powerhouse_unders/Middlesbrough/07_12_06/normal_100_4534.JPG', fanart = 'http://www.djsets.co.uk/pixebay/rave.jpg')
        addon.add_directory({'mode': 'GetLinks40', 'url': BASE_URL40 + 'mix/1'}, {'title':  '[COLOR turquoise][B]TwiceasNice [/COLOR] (HnG)[/B]'}, img = 'http://www.twiceasnice.co.uk/asset/images/header_image[2]_02.png', fanart = 'http://www.twiceasnice.co.uk/media/201110/window2[1].jpg')
        addon.add_directory({'mode': 'GetLinks5', 'url': BASE_URL5 + '/'}, {'title':  '[COLOR turquoise][B]The beat sanctuary [/COLOR] (oldskool HnG)[/B]'}, img = 'http://s2.postimg.org/mpw0uvq95/icon.png', fanart = 'http://gb.designcalibre.com/wp-content/uploads/2012/05/Music-Djs-2.jpg')
        addon.add_directory({'mode': 'GetLinks14', 'url': BASE_URL14 + 'audio/tracks/a-brief-history-of-grime-tapes'}, {'title':  '[COLOR turquoise][B]The wire [/COLOR] (Garage & Grime)[/B]'}, img = 'http://www.hcmf.co.uk/uploads/images/197wirelogoblockurlcopy.jpg?1253097636', fanart = 'http://alicepettey.com/wp-content/uploads/2012/03/The_Wire_Logo.jpg')
        addon.add_directory({'mode': 'GetLinks23', 'url': BASE_URL23 + 'threads/ez-old-skool-garage-sets.43637/'}, {'title':  '[COLOR mediumseagreen][B]DJ EZ [/COLOR] (Mixtapes Collection)[/B]   [COLOR blue] **[/COLOR]'}, img = 'http://3.bp.blogspot.com/-jRPq1Szx0Js/TjaX0R0DFTI/AAAAAAAAANE/6ds6AbbuD2s/s320/dj+ez+photo', fanart = 'http://www.sotonight.net/wp-content/uploads/2013/10/dj-ez-garden-party-3-large.jpg')
        addon.add_directory({'mode': 'GetLinks24', 'url': BASE_URL24 + '/'}, {'title':  '[COLOR chartreuse][B]Official Sidewinder UK Garage [/COLOR] (Podcasts)[/B]'}, img = 'http://assets.podomatic.net/ts/cf/4b/3d/djtrudos/1400x1400_9185047.jpg', fanart = 'http://cdn.shopify.com/s/files/1/0236/1879/files/SunCity_Crowd2_large.jpg?1396')
        addon.add_directory({'mode': 'GetLinks32', 'url': BASE_URL32 + '/'}, {'title':  '[COLOR green][B]Grimetapes [/COLOR] (Garage & Grime)[/B]'}, img = 'http://4.bp.blogspot.com/_DbazE44PZA0/SKmh-lAeK_I/AAAAAAAAAAM/RvhMZj8Y5wU/S1600-R/logo3-full.JPG', fanart = 'http://i.ytimg.com/vi/2S0APTthTpI/hqdefault.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------------------ PodMenu ----------------------------------------------------------------------------#

def PodMenu(): 
        addon.add_directory({'mode': 'GetLinks20', 'url': BASE_URL20 + 'dj_jedi_audio.php'}, {'title':  '[COLOR chartreuse][B]Dj jedi [/COLOR](Olskool, Hardcore)[/B]'}, img = 'http://www.dj-jedi.com/images/dj_jedi_logo.gif', fanart = 'http://archive-media.nyafuu.org/wg/image/1367/08/1367087842578.png')
        addon.add_directory({'mode': 'GetLinks6', 'url': BASE_URL6 + '/'}, {'title':  '[COLOR chartreuse][B]RatPack [/COLOR](Oldskool)[/B]'}, img = 'http://www.harderfaster.net/images/features/11332.ratpack2.jpg', fanart = 'http://static.inlog.org/wp-content/uploads/2013/04/front-590x390.jpg')
        addon.add_directory({'mode': 'GetLinks22', 'url': BASE_URL22 + 'site/category/podcast/'}, {'title':  '[COLOR chartreuse][B]John B [/COLOR] (Drum & Bass)[/B]'}, img = 'http://beta-recordings.com/images/Blog.jpg', fanart = 'http://i1.sndcdn.com/artworks-000028058053-5vxdam-original.jpg?77d7a69')
        addon.add_directory({'mode': 'GetLinks35', 'url': BASE_URL35 + 'mixes/old-skool-hardcore-breaks-acid-house/menu/page:1/limit:200/'}, {'title':  '[COLOR chartreuse][B]Brain Damage Radio [/COLOR](Olskool, Hardcore +)[/B]'}, img = 'http://www.braindamageradio.com/templates/skinnydesigns-base/images/logo.png', fanart = 'http://2.bp.blogspot.com/_WldfNndrX0k/TBTztaKCkAI/AAAAAAAABSI/uU1tq3XgRZg/s1600/BRAIN+DAMAGE+WALLPAPER+2.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------------------ ArchiveMenu ----------------------------------------------------------------------------#

def ArchiveMenu():
        addon.add_directory({'mode': 'GetLinksvids', 'url': BASE_URL15 + '/vids2.txt'}, {'title':  '[COLOR palevioletred][B]***Rave player Specials*** [/COLOR] (Utube Rave Documentaries)[/B]'}, img = 'http://s28.postimg.org/xjrgkbmd9/image.jpg', fanart = 'http://cdn.7boom.mx/content/boom-img/8630e9b6.jpeg')
        addon.add_directory({'mode': 'GetLinksvids', 'url': BASE_URL15 + '/vids3.txt'}, {'title':  '[COLOR deeppink][B]***Rave player Specials*** [/COLOR] (Rave Reminiscing)[/B]'}, img = 'http://s28.postimg.org/xjrgkbmd9/image.jpg', fanart = 'http://s27.postimg.org/xvs5paxyb/fanart.jpg')
        addon.add_directory({'mode': 'GetLinks15', 'url': BASE_URL15 + '/dnb.txt'}, {'title':  '[COLOR gold][B]Rave player Specials [/COLOR] (Rave Dj Sets)[/B]'}, img = 'http://s28.postimg.org/uwfyuzepp/cassettetdk.jpg', fanart = 'http://amgroup.com/news/wp-content/uploads/2013/04/IMG_4470-Custom.jpg') 
        addon.add_directory({'mode': 'GetLinks3', 'url': BASE_URL3 + '/'}, {'title':  '[COLOR green][B]Rave tape packs [/COLOR](Archive)[/B]'}, img = 'http://fc09.deviantart.net/fs25/f/2008/111/a/8/Cassette_tape_by_Quick_Stop.png', fanart = 'http://s27.postimg.org/3qdp1snnn/hhhgggg.jpg')
        addon.add_directory({'mode': 'GetLinks39', 'url': BASE_URL39 + '/tapes/'}, {'title':  '[COLOR green][B]Art Meets Science [/COLOR](Tape packs)[/B]'}, img = 'http://www.livinproof.co.uk/wordpress/wp-content/uploads/junglist_540.jpg', fanart = 'http://a1.l3-images.myspacecdn.com/images01/99/78257f742f7a14ceda417f06e5ddce24/l.jpg')
        addon.add_directory({'mode': 'GetLinks36', 'url': BASE_URL36 + '/media/Mix%20Archive/Misc/'}, {'title':  '[COLOR green][B]Oldskool Anthemz [/COLOR](Archive)[/B]'}, img = 'http://www.oldskoolanthemz.com/forum/images/vbclone/logo1.png', fanart = 'http://s27.postimg.org/3qdp1snnn/hhhgggg.jpg')
        addon.add_directory({'mode': 'GetLinks4', 'url': BASE_URL4 + '/'}, {'title':  '[COLOR green][B]Deepinside the oldskool [/COLOR](Archive)[/B]'}, img = 'http://4.bp.blogspot.com/-xUYf3AS2taA/Tzp8B6wEfbI/AAAAAAAAAgs/l2wmJAdqGSU/s1600/Nicky%2BBlackmarket%2B-%2BHardcore%2B17%2B-%2BAugust%2B1993.jpg', fanart = 'https://phaven-prod.s3.amazonaws.com/files/image_part/asset/376411/zJiIP2IgvAoFrWjDxG6FfyZosnE/medium_abbfabb_03.jpg')
        addon.add_directory({'mode': 'GetLinks13', 'url': BASE_URL13 + '/'}, {'title':  '[COLOR green][B]Rave-archive [/COLOR](Archive)[/B]'}, img = 'https://pbs.twimg.com/profile_images/3335360596/3d9ebe5623ae5be2bab14a54625a2537.jpeg', fanart = 'http://s11.postimg.org/vhd2897k3/fanart.jpg')
        addon.add_directory({'mode': 'GetLinks11', 'url': BASE_URL11 + '/'}, {'title':  '[COLOR green][B]Demodulated mixtapes [/COLOR](Archive)[/B]'}, img = 'http://urbanlegendkampala.com/wp-content/uploads/2013/11/Mixtape-Image.jpg', fanart = 'http://bigghostlimited.com/wp-content/uploads/2013/09/MIxtape.gif')
        addon.add_directory({'mode': 'GetLinks18', 'url': BASE_URL18 + '/'}, {'title':  '[COLOR green][B]Toronto rave mixtape [/COLOR](Archive)[/B]   [COLOR red] *[/COLOR]'}, img = 'http://www.torontoravemixtapearchive.com/images/promo/trma.jpg', fanart = 'http://torontoravemixtapearchive.com/images/promo/DavidRyanTapes.jpg')
        addon.add_directory({'mode': 'GetLinks17', 'url': BASE_URL17 + '/details/175bpm.plLtjBukemMixtapesCollection'}, {'title':  '[COLOR greenyellow][B]L T J Bukem [/COLOR](Tape Collection)[/B]'}, img = 'http://drumtrip.co.uk/wp-content/uploads/bukem.gif', fanart = 'http://www.htbackdrops.org/v2/albums/userpics/10257/orig_LTJ_Bukem.jpg')
        addon.add_directory({'mode': 'GetLinks21', 'url': BASE_URL21 + 'version.html'}, {'title':  '[COLOR greenyellow][B]LionDub  [/COLOR](Tape Collection)[/B]'}, img = 'http://www.djliondub.com/LIONDUB_B+W_LOGO.jpg', fanart = 'http://www.zona6.org/site/images/slide_liondub.jpg')
        addon.add_directory({'mode': 'GetLinks17a', 'url': BASE_URL17 + '/details/175bpm.pl-HelterSkelterCollection'}, {'title':  '[COLOR greenyellow][B]Helter Skelter [/COLOR] (Tape Collection)[/B]'}, img = 'http://rave.space.net.au/graphics/hskelter.jpg', fanart = 'http://www.fantazia.org.uk/flyerlibrary/images/HelterSkelter_170993_f.jpg')
        addon.add_directory({'mode': 'GetLinks2', 'url': BASE_URL2 + '/soundmanager2/demo/page-player/20bensons.html'}, {'title':  '[COLOR greenyellow][B]20bensons rave [/COLOR](Tape Collection)[/B]'}, img = 'http://www.zigsam.at/l07/B_Cig/BensonHedgesSpeciaF-20fJP197.jpg', fanart = 'http://bigghostlimited.com/wp-content/uploads/2013/09/MIxtape.gif')
        addon.add_directory({'mode': 'GetLinks7', 'url': BASE_URL7 + '/category_Event_Mixes_1.htm'}, {'title':  '[COLOR springgreen][B]UK raves [/COLOR](Tape Collection)[/B]'}, img = 'https://pbs.twimg.com/profile_images/3337802286/571a3ecdec1efb53e30cf19c00f45212.jpeg', fanart = 'http://www.fantazia.org.uk/Event%20info/Pics/11fantaziasummertime.jpg')
        addon.add_directory({'mode': 'GetLinks27', 'url': BASE_URL27 + '/mix-archive/live-sets/'}, {'title':  '[COLOR springgreen][B]Hardcore Highlights [/COLOR] (Tape Collection)[/B]'}, img = 'http://s28.postimg.org/qvbsfp7v1/Hardcore_Highlights_Small.png', fanart = 'http://wallpoper.com/images/00/41/10/87/abstract-hardcore_00411087.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1])) 

#------------------------------------------------------------------------------------------ Single tune Menu ----------------------------------------------------------------------------#

def StMenu(): 
        addon.add_directory({'mode': 'GetLinks38', 'url': BASE_URL38 + '/media/Tune%20Archive/Early%20House/'}, {'title':  '[COLOR greenyellow][B]Early House [/COLOR](Single tracks)[/B]'}, img = 'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-xpa1/v/t1.0-1/c41.41.517.517/s160x160/9166_10151207543098036_1151203569_n.jpg?oh=5df066cdefc786391daadbf69e67a353&oe=55C2E6F1&__gda__=1443082162_0a0efe8901c1f803bc364d8ad1f73cec', fanart = 'http://i.ytimg.com/vi/hU9PM4LRgJc/0.jpg')
        addon.add_directory({'mode': 'GetLinks38a', 'url': BASE_URL38 + '/media/Tune%20Archive/Nu%20Skool/'}, {'title':  '[COLOR greenyellow][B]Nu Skool [/COLOR](Single tracks)[/B]'}, img = 'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-xpa1/v/t1.0-1/c41.41.517.517/s160x160/9166_10151207543098036_1151203569_n.jpg?oh=5df066cdefc786391daadbf69e67a353&oe=55C2E6F1&__gda__=1443082162_0a0efe8901c1f803bc364d8ad1f73cec', fanart = 'http://i.ytimg.com/vi/hU9PM4LRgJc/0.jpg')
        addon.add_directory({'mode': 'GetLinks38b', 'url': BASE_URL38 + '/media/Tune%20Archive/Old%20Skool%20Classics/'}, {'title':  '[COLOR greenyellow][B]Old Skool Classics [/COLOR](Single tracks)[/B]'}, img = 'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-xpa1/v/t1.0-1/c41.41.517.517/s160x160/9166_10151207543098036_1151203569_n.jpg?oh=5df066cdefc786391daadbf69e67a353&oe=55C2E6F1&__gda__=1443082162_0a0efe8901c1f803bc364d8ad1f73cec', fanart = 'http://i.ytimg.com/vi/hU9PM4LRgJc/0.jpg')
        addon.add_directory({'mode': 'GetLinks38c', 'url': BASE_URL38 + '/media/Tune%20Archive/Old%20Skool%20Hardcore/'}, {'title':  '[COLOR greenyellow][B]Old Skool Hardcore [/COLOR](Single tracks)[/B]'}, img = 'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-xpa1/v/t1.0-1/c41.41.517.517/s160x160/9166_10151207543098036_1151203569_n.jpg?oh=5df066cdefc786391daadbf69e67a353&oe=55C2E6F1&__gda__=1443082162_0a0efe8901c1f803bc364d8ad1f73cec', fanart = 'http://i.ytimg.com/vi/hU9PM4LRgJc/0.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1])) 

#------------------------------------------------------------------------------------------ RadioMenu ----------------------------------------------------------------------------#

def RadioMenu():  
        addon_handle = int(sys.argv[1]) 
        xbmcplugin.setContent(addon_handle, 'audio')

        addon.add_directory({'mode': 'GetLinks41', 'url': BASE_URL41 + '/viewtopic.php?f=4&t=477'}, {'title':  '[COLOR green][B]London station internet stream links [/COLOR] >>[/B] >>'}, img = 'https://pbs.twimg.com/profile_images/2151054574/moblogo1_400x400.jpg', fanart = 'http://i.imgur.com/yXimypO.jpg?1')


        addon.add_directory({'mode': 'RadioMenu', '': '', '': '',
                             '': '', '': ''}, {'title':  ''}, img = 'http://www.systemslibrarian.co.za/images/Broken%20links.jpg', fanart = 'http://s30.postimg.org/elc1pa6qp/fanart.jpg')

        url = 'http://uk1-pn.webcast-server.net:8698'
        li = xbmcgui.ListItem('[COLOR lightseagreen][B]Kool London[/B][/COLOR] [COLOR lime](((Live)))[/COLOR]  (Old skool, Jungle, Drum & Bass + more) [COLOR gold]*****[/COLOR]', thumbnailImage= 'http://s30.postimg.org/5r870dash/icon.png')
        li.setProperty('fanart_image', 'http://koollondon.com/images/stories/kool-timetable-jan-2015.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)


        addon.add_directory({'mode': 'RadioMenu', '': '', '': '',
                             '': '', '': ''}, {'title':  ''}, img = 'http://www.systemslibrarian.co.za/images/Broken%20links.jpg', fanart = 'http://s30.postimg.org/elc1pa6qp/fanart.jpg')

        url = 'http://192.99.11.97:8000'
        li = xbmcgui.ListItem('[COLOR blue][B]Rave Tape Radio[/B][/COLOR] [COLOR lime] (((LIVE))) [/COLOR]  (Oldskool TapePacks 24/7))', thumbnailImage= 'http://d1i6vahw24eb07.cloudfront.net/s182965d.png')
        li.setProperty('fanart_image', 'http://s12.postimg.org/rkd8gen7h/fanart.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://78.129.224.8/~livegig/mediacp/system/playlist.php?id=1&type=asx'
        li = xbmcgui.ListItem('[COLOR dodgerblue][B]Oldskool Anthemz Radio[/B][/COLOR] [COLOR lime](((Live)))[/COLOR]  (Oldskool)', thumbnailImage= 'http://www.oldskoolanthemz.com/images/cms/osafacebookconnect.jpg')
        li.setProperty('fanart_image', 'http://s12.postimg.org/rkd8gen7h/fanart.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://178.33.115.87:8004/;stream.mp3'
        li = xbmcgui.ListItem('[COLOR dodgerblue][B]Only Oldskool Radio[/B][/COLOR] [COLOR lime](((Live)))[/COLOR]  (Oldskool)', thumbnailImage= 'http://i1.sndcdn.com/artworks-000074359327-1jmjy6-original.jpg?435a760')
        li.setProperty('fanart_image', 'http://s12.postimg.org/rkd8gen7h/fanart.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'https://albireo.shoutca.st/tunein/ravrad00.pls'
        li = xbmcgui.ListItem('[COLOR dodgerblue][B]Nu-Perception Radio  [/B][/COLOR] [COLOR lime](((Live)))[/COLOR]  (Oldskool)', thumbnailImage= 'http://www.nu-perceptionradio.com/img/album_nocover.jpg')
        li.setProperty('fanart_image', 'http://s12.postimg.org/rkd8gen7h/fanart.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://www.nu-rave.com:8000/nurave24.m3u'
        li = xbmcgui.ListItem('[COLOR dodgerblue][B]Nu-Rave Radio[/B][/COLOR] [COLOR lime](((Live)))[/COLOR]  (oldskool + more)', thumbnailImage= 'http://static.house-mixes.com/s3/webmixes-images/accounts-430903/artwork/4375333d-7acd-44a7-8ea8-474368bd20e3.jpg/360/45/true')
        li.setProperty('fanart_image', 'http://s12.postimg.org/rkd8gen7h/fanart.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://icy-e-bl-09-boh.sharp-stream.com/kisstory.mp3.m3u'
        li = xbmcgui.ListItem('[COLOR dodgerblue][B]kisstory [/B][/COLOR] [COLOR lime](((Live)))[/COLOR]  (Club classics)', thumbnailImage= 'http://www.getmemedia.com/public/ideas/Opp/6857/Kisstory.jpg')
        li.setProperty('fanart_image', 'http://s12.postimg.org/rkd8gen7h/fanart.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        addon.add_directory({'mode': 'RadioMenu', '': '', '': '',
                             '': '', '': ''}, {'title':  ''}, img = 'http://www.systemslibrarian.co.za/images/Broken%20links.jpg', fanart = 'http://s30.postimg.org/elc1pa6qp/fanart.jpg')

        url = 'http://webstreamer.co.uk:41940/;'
        li = xbmcgui.ListItem('[COLOR mediumaquamarine][B]Pure Music 247[/B][/COLOR] [COLOR lime](((Live)))[/COLOR]  (House + much more)', iconImage='http://puremusic247.com/images/dj-Copyedittest.gif', thumbnailImage= 'http://puremusic247.com/images/dj-Copyedittest.gif')
        li.setProperty('fanart_image', 'http://djautograph.com/wp-content/uploads/2013/10/House_Music_by_Labelrx.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://50.7.184.106:8631/listen.pls'
        li = xbmcgui.ListItem('[COLOR mediumaquamarine][B]Central Radio UK[/B][/COLOR] [COLOR lime](((Live)))[/COLOR] (Dance + much more)', iconImage='http://s13.postimg.org/jcdhx5pqf/image.png', thumbnailImage= 'http://s13.postimg.org/jcdhx5pqf/image.png')
        li.setProperty('fanart_image', 'http://www.mrwallpaper.com/wallpapers/Music-equipment.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://server2.unitystreams.com:8008'
        li = xbmcgui.ListItem('[COLOR mediumaquamarine][B]Play Back uk Radio [/B][/COLOR] [COLOR lime](((Live)))[/COLOR]   (House & oldskool Garage)', thumbnailImage= 'https://pbs.twimg.com/media/Bm5ZdVRIEAA9bSI.jpg')
        li.setProperty('fanart_image', 'http://www.playbackuk.com/downloads/playbackukcom_3DPicture.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://78.129.228.187:8008/;stream/1'
        li = xbmcgui.ListItem('[COLOR mediumaquamarine][B]House fm [/B][/COLOR] [COLOR lime](((Live)))[/COLOR]  (House)', thumbnailImage= 'http://i1.sndcdn.com/artworks-000049756393-x4gokq-crop.jpg?435a760')
        li.setProperty('fanart_image', 'http://www.strictlyhousefm.co.uk/wp-content/uploads/2012/10/strictly-house-6.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://shine879.internetdomainservices.com:8204/'
        li = xbmcgui.ListItem('[COLOR mediumaquamarine][B]Shine879 [/B][/COLOR] [COLOR lime](((Live)))[/COLOR]  (House & oldskool Garage + more)', thumbnailImage= 'https://lh4.ggpht.com/0rdHZ2GOZYeiDfo1jyuWzbiFa9VIHNulX8qvTgXG3bHWMxO28mrxxUrT2VYWeQgaU4k=w300')
        li.setProperty('fanart_image', 'http://dnbvideo.ru/wp-content/uploads/2013/09/antinox-liquid-drum-n-bass-4-1080p-hq.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://stream.dnsgb.net:8046/listen.pls'
        li = xbmcgui.ListItem('[COLOR mediumaquamarine][B]Passion fm [/B][/COLOR] [COLOR lime](((Live)))[/COLOR]  (House & oldskool Garage)', thumbnailImage= 'https://d2uykijsw1jrmd.cloudfront.net/media/cache/d3/4c/d34cdd381be73a94e7d762afeef97ec7.jpg')
        li.setProperty('fanart_image', 'http://i1.sndcdn.com/artworks-000028046982-dxmeig-original.jpg?164b459')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://198.144.148.12:9002/listen.pls'
        li = xbmcgui.ListItem('[COLOR mediumaquamarine][B]Point Blank fm [/B][/COLOR] [COLOR lime](((Live)))[/COLOR]  (House + more)', thumbnailImage= 'http://i1.sndcdn.com/artworks-000050041757-a1ox54-original.jpg?164b459')
        li.setProperty('fanart_image', 'https://pbs.twimg.com/profile_images/1351770720/PB_Logo_Small.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://50.7.158.42:8066/'
        li = xbmcgui.ListItem('[COLOR mediumaquamarine][B]Reaction Radio  [/B][/COLOR] [COLOR lime](((Live)))[/COLOR]  (House + more)', thumbnailImage= 'http://www.reactionradio.co.uk/data/ckeditor/click_here_-_listen_live_-_new_version.jpg')
        li.setProperty('fanart_image', 'http://wordpress.mediatel.co.uk/wp-content/uploads/2013/10/Radio-Rajar.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://193.27.42.226:8192/mosdir.mp3'
        li = xbmcgui.ListItem('[COLOR mediumaquamarine][B]Ministry of Sound Radio[/B][/COLOR] [COLOR lime](((Live)))[/COLOR]  (House + more)', thumbnailImage= 'http://i1.sndcdn.com/artworks-000070064884-tec6ir-original.jpg?f775e59')
        li.setProperty('fanart_image', 'http://1.bp.blogspot.com/-pXdClkxvZu8/TleccVYC3EI/AAAAAAAAAic/A7aV-CrKcaU/s1600/Ministry-of-Sound.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://65.60.52.122:8220/listen.pls'
        li = xbmcgui.ListItem('[COLOR mediumaquamarine][B]Flex fm [/B][/COLOR] [COLOR lime](((Live)))[/COLOR]  (House + more)', thumbnailImage= 'http://images-mix.netdna-ssl.com/w/300/h/300/q/85/upload/images/extaudio/69a90686-6d2f-4fbe-9a61-b7f90c955cc7.jpg')
        li.setProperty('fanart_image', 'http://photos-h.ak.fbcdn.net/hphotos-ak-frc3/t1.0-0/c13.0.935.623/s720x720/428247_523439234355303_19226475_n.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)


        addon.add_directory({'mode': 'RadioMenu', '': '', '': '',
                             '': '', '': ''}, {'title':  ''}, img = 'http://www.systemslibrarian.co.za/images/Broken%20links.jpg', fanart = 'http://s30.postimg.org/elc1pa6qp/fanart.jpg')

        url = 'http://78.129.228.187:8034/listen.pls'
        li = xbmcgui.ListItem('[COLOR lightseagreen][B]Rude fm [/B][/COLOR] [COLOR lime](((Live)))[/COLOR]  (Drum & Bass)', thumbnailImage= 'http://surroundsoundrecordings.co.uk/wp-content/uploads/2011/09/rudelogo.jpg')
        li.setProperty('fanart_image', 'http://s3.amazonaws.com/quietus_production/images/articles/14317/rude_fm_1390324837_crop_550x388.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://stream1.jungletrain.net:8000/'
        li = xbmcgui.ListItem('[COLOR lightseagreen][B]Jungle Train [/B][/COLOR] [COLOR lime](((Live)))[/COLOR]  (Drum & Bass)', thumbnailImage= 'http://i1.sndcdn.com/artworks-000000487986-yhoaa3-crop.jpg?164b459')
        li.setProperty('fanart_image', 'http://i1.ytimg.com/vi/X6eoT1kVWkM/maxresdefault.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://shouthost.com.18.streams.bassdrive.com:8398'
        li = xbmcgui.ListItem('[COLOR lightseagreen][B]Bass Drive [/B][/COLOR] [COLOR lime](((Live)))[/COLOR]  (Drum & Bass)', thumbnailImage= 'http://i1.sndcdn.com/avatars-000019466696-vv1udx-crop.jpg?164b459')
        li.setProperty('fanart_image', 'http://www.wallsave.com/wallpapers/1920x1200/drum-and-bass/398404/drum-and-bass-bassdrive-view-topic-398404.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://bassjunkees.com/m3u'
        li = xbmcgui.ListItem('[COLOR lightseagreen][B]Bass Junkees [/B][/COLOR] [COLOR lime](((Live)))[/COLOR]  (Drum & Bass)', thumbnailImage= 'http://static.rad.io/images/broadcasts/bf/40/4993/w175.png')
        li.setProperty('fanart_image', 'http://i1.sndcdn.com/artworks-000032545848-tw4hg5-original.jpg?77d7a69')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://198.154.112.233:8702/;'
        li = xbmcgui.ListItem('[COLOR lightseagreen][B]Origin fm  [/B][/COLOR] [COLOR lime](((Live)))[/COLOR]  (Drum & Bass)', thumbnailImage= 'http://www.londonpirates.co.uk/Origin/logolarge.jpg')
        li.setProperty('fanart_image', 'http://seanceradio.co.uk/wp-content/uploads/2013/10/Untitled-3.gif')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://cast2.serverhostingcenter.com/tunein.php/lsimpson/playlist.asx'
        li = xbmcgui.ListItem('[COLOR lightseagreen][B]Renegade Radio  [/B][/COLOR] [COLOR lime](((Live)))[/COLOR]  (Drum & Bass + more)', thumbnailImage= 'https://pbs.twimg.com/profile_images/713650373/Renegade_Logo_lrg_no_Out_300dpi.png')
        li.setProperty('fanart_image', 'http://static.squarespace.com/static/51366b7ee4b055d8b61b6dac/t/52379872e4b0cb8c5f9b1b48/1379375223226/Renegade%20Radio%20New%20Logo.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://stressfactor.co.uk/listen.m3u'
        li = xbmcgui.ListItem('[COLOR lightseagreen][B]Stress Factor  [/B][/COLOR] [COLOR lime](((Live)))[/COLOR]  (Drum & Bass + more)', thumbnailImage= 'http://www.patricks.be/katongeren/images/algemeen/stressfactor.jpg')
        li.setProperty('fanart_image', 'http://www.sintcordula.be/wp-content/gallery/stressfactor/img_1697.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        addon.add_directory({'mode': 'RadioMenu', '': '', '': '',
                             '': '', '': ''}, {'title':  ''}, img = 'http://www.systemslibrarian.co.za/images/Broken%20links.jpg', fanart = 'http://s30.postimg.org/elc1pa6qp/fanart.jpg')

        url = 'http://www.kraftyradio.com/listen.asx'
        li = xbmcgui.ListItem('[COLOR lightseagreen][B]Krafty Radio  [/B][/COLOR] [COLOR lime](((Live)))[/COLOR]  (Hardcore + more)', thumbnailImage= 'http://whiskers.com/krafty/krafty.png')
        li.setProperty('fanart_image', 'http://retrodjservice.com/yahoo_site_admin/assets/images/deejay-wallpapers_7051_1920x1200.42223626_std.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://37.187.90.201:2199/tunein/slipmatt.pls'
        li = xbmcgui.ListItem('[COLOR lightseagreen][B]DJ Slipmatt Radio  [/B][/COLOR] [COLOR lime](((Live)))[/COLOR]  (Oldskool + Hardcore)', thumbnailImage= 'http://i1.sndcdn.com/avatars-000000911994-xt7goc-crop.jpg?30a2558')
        li.setProperty('fanart_image', 'http://i1.ytimg.com/vi/sy9SV25ALII/maxresdefault.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        addon.add_directory({'mode': 'RadioMenu', '': '', '': '',
                             '': '', '': ''}, {'title':  ''}, img = 'http://www.systemslibrarian.co.za/images/Broken%20links.jpg', fanart = 'http://s30.postimg.org/elc1pa6qp/fanart.jpg')

        addon.add_directory({'mode': 'RadioMenu', '': '', '': '',
                             '': '', '': ''}, {'title':  '[COLOR mediumvioletred]~[/COLOR][COLOR crimson][B]Report broken links to @TheYid009 on twitter[/B][/COLOR][COLOR mediumvioletred]~[/COLOR]'}, img = 'http://www.systemslibrarian.co.za/images/Broken%20links.jpg', fanart = 'http://s30.postimg.org/elc1pa6qp/fanart.jpg')

        xbmcplugin.endOfDirectory(addon_handle)

#------------------------------------------------------------------------------------------ VRadioMenu ----------------------------------------------------------------------------#

def VRadioMenu():  
        addon_handle = int(sys.argv[1]) 
        xbmcplugin.setContent(addon_handle, 'audio')

        url = 'rtmp://85.234.141.95:1935/live/myStream'
        li = xbmcgui.ListItem('[COLOR lightseagreen][B]Rough Tempo [/B][/COLOR]  [COLOR red](Video Stream)[/COLOR]  [COLOR lime](((Live)))[/COLOR]  (Drum n Bass)', thumbnailImage= 'http://www.roughtempo.com/fbimage.jpg')
        li.setProperty('fanart_image', 'http://s18.postimg.org/wxt9kuvpl/maxresdefault.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'rtmp://w10.streamgb.com:1935/kool/kool'
        li = xbmcgui.ListItem('[COLOR dodgerblue][B]Kool London  [/B][/COLOR] [COLOR red](Testing Video stream) [/COLOR]  [COLOR lime](((Live)))[/COLOR]  (Drum n Bass)', thumbnailImage= 'http://s30.postimg.org/5r870dash/icon.png')
        li.setProperty('fanart_image', 'http://koollondon.com/images/stories/kool-timetable-may-2015.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        addon.add_directory({'mode': 'RadioMenu', '': '', '': '',
                             '': '', '': ''}, {'title':  '[COLOR mediumvioletred]~[/COLOR][COLOR blue][B]Report broken links to @TheYid009 on twitter[/B][/COLOR][COLOR mediumvioletred]~[/COLOR]'}, img = 'http://www.systemslibrarian.co.za/images/Broken%20links.jpg', fanart = 'http://s30.postimg.org/elc1pa6qp/fanart.jpg')

        xbmcplugin.endOfDirectory(addon_handle)

################################################################################# mode #########################################################################################

if mode == 'main': 
	MainMenu()
elif mode == 'RadioMenu':
        RadioMenu()
elif mode == 'VRadioMenu':
        VRadioMenu()
elif mode == 'ArchiveMenu':
        ArchiveMenu()
elif mode == 'PodMenu':
        PodMenu()
elif mode == 'HngMenu':
        HngMenu()
elif mode == 'HelpMenu':
        HelpMenu()
elif mode == 'RaMenu':
        RaMenu()
elif mode == 'ArMenu':
        ArMenu()
elif mode == 'StMenu':
        StMenu()
elif mode == 'GetLinks':
	GetLinks(url, text, img)
elif mode == 'GetLinks2':
	GetLinks2(url, text, img)
elif mode == 'GetLinks3':
	GetLinks3(url, text, img)
elif mode == 'GetLinks3a':
	GetLinks3a(url, text, img)
elif mode == 'GetLinks3b':
	GetLinks3b(url, text, img)
elif mode == 'GetLinks4':
	GetLinks4(url, text, img)
elif mode == 'GetLinks4a':
	GetLinks4a(url, text, img)
elif mode == 'GetLinks4b':
	GetLinks4b(url, text, img)
elif mode == 'GetLinks5':
	GetLinks5(url, text, img)
elif mode == 'GetLinks5a':
	GetLinks5a(url, text, img)
elif mode == 'GetLinks6':
	GetLinks6(url, text, img)
elif mode == 'GetLinks6a':
	GetLinks6a(url, text, img)
elif mode == 'GetLinks7':
	GetLinks7(url, text, img)
elif mode == 'GetLinks9a':
	GetLinks9a(url, text, img)
elif mode == 'GetLinks9b':
	GetLinks9b(url, text, img)
elif mode == 'GetLinks9c':
	GetLinks9c(url, text, img)
elif mode == 'GetLinks11':
	GetLinks11(url, text, img)
elif mode == 'GetLinks11a':
	GetLinks11a(url, text, img)
elif mode == 'GetLinks11b':
	GetLinks11b(url, text, img)
elif mode == 'GetLinks13':
	GetLinks13(url, text, img)
elif mode == 'GetLinks13a':
	GetLinks13a(url, text, img)
elif mode == 'GetLinks13b':
	GetLinks13b(url, text, img)
elif mode == 'GetLinks13c':
	GetLinks13c(url, text, img)
elif mode == 'GetLinks14':
	GetLinks14(url, text, img)
elif mode == 'GetLinks15':
	GetLinks15(url, text, img)
elif mode == 'GetLinks17':
	GetLinks17(url, text, img)
elif mode == 'GetLinks17a':
	GetLinks17a(url, text, img)
elif mode == 'GetLinks18':
	GetLinks18(url, text, img)
elif mode == 'GetLinks18a':
	GetLinks18a(url, text, img)
elif mode == 'GetLinks20':
	GetLinks20(url, text, img)
elif mode == 'GetLinks21':
	GetLinks21(url, text, img)
elif mode == 'GetLinks22':
	GetLinks22(url, text, img)
elif mode == 'GetLinks23':
	GetLinks23(url, text, img)
elif mode == 'GetLinks23a':
	GetLinks23a(url, text, img)
elif mode == 'GetLinks24':
	GetLinks24(url, text, img)
elif mode == 'GetLinks24a':
	GetLinks24a(url, text, img)
elif mode == 'GetLinks27':
	GetLinks27(url, text, img)
elif mode == 'GetLinks31':
	GetLinks31(url, text, img)
elif mode == 'GetLinks31a':
	GetLinks31a(url, text, img)
elif mode == 'GetLinks32':
	GetLinks32(url, text, img)
elif mode == 'GetLinks32a':
	GetLinks32a(url, text, img)
elif mode == 'GetLinks35':
	GetLinks35(url, text, img)
elif mode == 'GetLinks35a':
	GetLinks35a(url, text, img)
elif mode == 'GetLinks36':
	GetLinks36(url, text, img)
elif mode == 'GetLinks38':
	GetLinks38(url, text, img)
elif mode == 'GetLinks38a':
	GetLinks38a(url, text, img)
elif mode == 'GetLinks38b':
	GetLinks38b(url, text, img)
elif mode == 'GetLinks38c':
	GetLinks38c(url, text, img)
elif mode == 'GetLinks39':
	GetLinks39(url, text, img)
elif mode == 'GetLinks39a':
	GetLinks39a(url, text, img)
elif mode == 'GetLinks40':
	GetLinks40(url, text, img)
elif mode == 'GetLinks40a':
	GetLinks40a(url, text, img)
elif mode == 'GetLinks41':
	GetLinks41(url, text, img)
elif mode == 'GetLinks42':
	GetLinks42(url, text, img)
elif mode == 'GetLinks42a':
	GetLinks42a(url, text, img)
elif mode == 'GetLinksvids':
	GetLinksvids(url)
elif mode == 'PlayVideo':
	PlayVideo(url, listitem, text, img)
elif mode == 'PlayVideo1':
	PlayVideo1(url, listitem)

xbmcplugin.endOfDirectory(int(sys.argv[1]))