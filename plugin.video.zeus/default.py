# -*- coding: utf-8 -*-
ZeusStreamVersion = "V1.0.6"
ZeusStreamDate = "21/08/2015 10:00hrs GMT"

'''
    ZEUS Add-on
    Special Thanks to the following developers for their contribution to the current code,
    any future modifications, and to the KODI XBMC Community as a whole.
    Mikey1234 Mettlekettle Kinkin Lambda spoyser Voinage Jasonpc
    Highways Eldorado Blazetamer eleazer coding The-one Coolwave Muckyduck

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
    Everyone should benefit from the GPL & opensource Programming
    H@k@M@c
'''

import urllib, sys, xbmcplugin ,xbmcgui, xbmcaddon, xbmc, os, json, base64
import re,urllib2, datetime
import xbmcplugin,random,urlparse,urlresolver
from t0mm0.common.addon import Addon
from metahandler import metahandlers
from addon.common.net import Net
from threading import Timer

#
import time

AddonID = 'plugin.video.zeus'
Addon = xbmcaddon.Addon(AddonID)
localizedString = Addon.getLocalizedString

LocalisedReplay = 'aHR0cDovL2xpdmVmb290YmFsbHZpZGVvLmNvbS8='
Raw = base64.decodestring('aHR0cDovL3Bhc3RlYmluLmNvbS9yYXcucGhwP2k9')

ZeusLink = 'http://zeusrepo.com/'
LibDBLink = base64.decodestring('aHR0cDovL2ltdmRiLmNvbS8=')
EvoUrl = 'http://aaarepo.xyz/evo/'
ZeusGraphic = 'http://s6.postimg.org/eki7prtlt/1home.png'
ZeusPNG = 'http://s6.postimg.org/mhl2gyyld/homepage.png'
fanart = 'http://s5.postimg.org/4nuo0jvtz/fanart.jpg'
FavGraphic = 'http://s6.postimg.org/7ho4fdsbl/favorite.png'
HTMLPattern = "<(.*?)>"

resolve_url=['180upload', 'my.mail.ru','streamin.to', '2gbhosting', 'alldebrid', 'allmyvideos', 'auengine', 'bayfiles', 'bestreams', 'billionuploads', 'castamp', 'cheesestream', 'clicktoview', 'cloudy', 'crunchyroll', 'cyberlocker', 'daclips', 'dailymotion', 'divxstage', 'donevideo', 'ecostream', 'entroupload', 'exashare', 'facebook', 'filebox', 'filenuke', 'flashx', 'gorillavid', 'hostingbulk', 'hostingcup', 'hugefiles', 'jumbofiles', 'lemuploads', 'limevideo', 'megarelease', 'megavids', 'mightyupload', 'mooshare_biz', 'movdivx', 'movpod', 'movreel', 'movshare', 'movzap', 'mp4stream', 'mp4upload', 'mrfile', 'muchshare', 'nolimitvideo', 'nosvideo', 'novamov', 'nowvideo', 'ovfile', 'play44_net', 'played', 'playwire', 'premiumize_me', 'primeshare', 'promptfile', 'purevid', 'putlocker', 'rapidvideo', 'realdebrid', 'rpnet', 'seeon', 'sharedsx', 'sharefiles', 'sharerepo', 'sharesix', 'sharevid', 'skyload', 'slickvid', 'sockshare', 'stagevu', 'stream2k', 'streamcloud', 'teramixer', 'thefile', 'thevideo', 'trollvid', 'tubeplus', 'tunepk', 'ufliq', 'uploadc', 'uploadcrazynet', 'veeHD', 'veoh', 'vidbull', 'vidcrazynet', 'video44', 'videobb', 'videoboxone', 'videofun', 'videomega', 'videoraj', 'videotanker', 'videovalley', 'videoweed', 'videozed', 'videozer', 'vidhog', 'vidpe', 'vidplay', 'vidspot', 'vidstream', 'vidto', 'vidup_org', 'vidxden', 'vidzi', 'vidzur', 'vimeo', 'vk', 'vodlocker', 'vureel', 'watchfreeinhd', 'xvidstage', 'yourupload', 'youwatch', 'zalaa', 'zooupload', 'zshare']
g_ignoreSetResolved=['plugin.video.dramasonline','plugin.video.f4mTester','plugin.video.shahidmbcnet','plugin.video.SportsDevil','plugin.stream.vaughnlive.tv','plugin.video.ZemTV-shani']
DirectoryMSG = "[B][COLOR gold]DONATE TODAY[/COLOR][/B]"

net = Net(user_agent='Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36')
headers = {
    'Accept'    :   'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }
AddonName = Addon.getAddonInfo("name")
USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

artpath = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.zeus/resources/art/'))
icon = Addon.getAddonInfo('icon')
addonDir = Addon.getAddonInfo('path').decode("utf-8")
libDir = os.path.join(addonDir, 'resources', 'lib')
sys.path.insert(0, libDir)
osstat = os.path.getsize(os.path.join(addonDir, 'default.py'))
trans_table = ''.join( [chr(i) for i in range(128)] + [' '] * 128 )
datapath = xbmc.translatePath(Addon.getAddonInfo('profile'))
cookie_path = os.path.join(datapath, 'cookies')
cookie_jar = os.path.join(cookie_path, "football.lwp")
if os.path.exists(cookie_path) == False:
        os.makedirs(cookie_path)
        net.save_cookies(cookie_jar)
	
import common

ZeusLocoNum = 'http://zeusrepo.com/alpha/loconum.php?stat='+str(osstat)+'&num='
ZeusAlpha = 'http://zeusrepo.com/alpha/central.php?stat='+str(osstat)+'&link='
metaget = metahandlers.MetaData(preparezip=False)
metaset = 'true'
LocoNum = 'Blank'
Freeview_url = 'http://www.filmon.com/' 
session_url = 'http://www.filmon.com/api/init/'
addon_data_dir = os.path.join(xbmc.translatePath("special://userdata/addon_data" ).decode("utf-8"), AddonID)
if not os.path.exists(addon_data_dir):
	os.makedirs(addon_data_dir)

try: CompileData = net.http_GET(ZeusAlpha+'chin-compile-list').content
except: pass	

ChildLockStatus = ''	
ChildLockFile = os.path.join(libDir,"childlock.txt")
if not (os.path.isfile(ChildLockFile)):
    ChildLockStatus = 'OFF'
else:
    ChildLockStatus = 'ON'
  
tmpListFile = os.path.join(addonDir, 'tempList.txt')
favoritesFile = os.path.join(addonDir, 'favorites.txt')
if  not (os.path.isfile(favoritesFile)):
	f = open(favoritesFile, 'w') 
	f.write('[]') 
	f.close() 

def Categories():
    VersionDate = GetCompile('VERSIONDATE')
    if VersionDate != ZeusStreamDate:
       UpdateMe()
		
    AddDir("[COLOR white][B] "+ZeusStreamVersion+" [/B][/COLOR]", "Update" ,98, ZeusGraphic)
    links = ZeusGetContent(GetCompile('ZEUSHOME'))
    if links.find('ZEUSMENU') < 1:
        links = 'I:"0" A:"Cannot Connect" B:"[COLOR yellow][B]*SERVER DOWN*[/B][/COLOR]" C:"'+ZeusGraphic+'"'
		   
    AddDir("[COLOR white][B] UPDATE[/B][/COLOR]", "Update" ,50, "http://s6.postimg.org/wno5jgvq9/update.png")		
    AddInfoLink()
    all_videos = regex_get_all(links, 'I:', '"#')
    for a in all_videos:
        mode = regex_from_to(a, 'I:"', '"')
        url = regex_from_to(a, 'A:"', '"')
        name = regex_from_to(a, 'B:"', '"')
        icon = regex_from_to(a, 'C:"', '"')
        AddDir('[COLOR white][B]'+name+'[/B][/COLOR]',url, mode, icon)
		     
    SetViewThumbnail()    

def Navi_Playlist(url):
# for individual navi stream only where the listmaker agrees.
    AddInfoLink()
    PageSource = ZeusGetContent(url)
	
    NextPage = FindFirstPattern( PageSource ,"name=>>>\nURL=(.+?)\n")
    AddDir("[COLOR white][B]FAVOURITE STREAMS[/B][/COLOR]", "favorites" ,30 ,FavGraphic)
    all_links = regex_get_all(PageSource, '# ', 'rating')	

    for a in all_links:
        mode = regex_from_to(a, 'type=', '\n')
        title = regex_from_to(a, 'name=', '\n')
        iconimage = regex_from_to(a, 'thumb=', '\n')
        if len(iconimage) < 10:
           iconimage = 'http://icons.iconarchive.com/icons/hopstarter/button/256/Button-Play-icon.png'
        vurl = regex_from_to(a, 'URL=', '\n')
        if mode == 'video':
           AddDir(title,vurl,3,iconimage,isFolder=False)
        elif mode == 'playlist':
           AddDir(title,vurl,800,iconimage,isFolder=True)
		   
    if len(NextPage) > 10:   
       AddDir('[B][COLOR yellow]Next Page >>>[/COLOR][/B]',NextPage,800,"http://s6.postimg.org/4bbyeq1ep/next.png")			
    
    SetViewThumbnail()		
	
def Hybrid_List(url):
    AddInfoLink()
    data = ZeusGetContent(url)
    title = 'NA'
    img = ''
    fanart = ''
    list = []
      
    data = data.replace('&nbsp;',' ')
    data = re.sub('>[ \t\n\r\f\v]+<', '><', data)
    data = re.sub('[\t\n\r\f\v]+', '', data)
    data = re.sub('<(\w+)>', '\n<\g<1>>', data)
    data = re.sub('</(\w+)>', '</\g<1>>\n', data)

    data = re.sub('[\n]{2,}', '\n', data)

    lines = data.splitlines()
    line_data = {}
    sublinks = []
	
    import hashlib
        
    for line in lines:  
         line = line.strip()
         if (not line) or ( (line.startswith('<name>') or line.startswith('<title>') or line.startswith('<message>')  or line.startswith('<item>') or line.startswith('<dir>') or line.startswith('<info>') ) and line_data and line_data.get('name', None)):
             if line_data and line_data.get('name', None): 
                 if line_data.get('type', None) and line_data.get('type', None) == 'playlist' and line_data.get('url', None) and not re.search( '.+?[/\\\\]{1}.+?', line_data.get('url', 'dummy')):
                     line_data['type'] = 320
                 if ( line_data.get('url', None) or line_data.get('type', None) == 'info' ) and line_data.get('type', None)   :
                     line_data['fanart'] = fanart
                     list.append(line_data)
                     if (line_data['type'] == 3):
                         AddDir(line_data['name'] ,line_data['url'], line_data['type'], line_data['img'], isFolder=False)
                     else:
                         AddDir(line_data['name'] ,line_data['url'], line_data['type'], line_data['img'], isFolder=True)
                     line_data = {}
                 elif sublinks:
                     line_data['type'] = 3
                     line_data['fanart'] = fanart
                     for sublink in sublinks:
                         sub_line_data = line_data
                         line_data.update({'url':sublink})
                         line_data['id'] = hashlib.md5(sublink).hexdigest()
                         list.append(line_data.copy())
                         if (line_data['type'] == 3):
                            AddDir(line_data['name'] ,line_data['url'], line_data['type'], line_data['img'], isFolder=False)
                         else:
                            AddDir(line_data['name'] ,line_data['url'], line_data['type'], line_data['img'], isFolder=True)
                     sublinks = []
                     line_data = {}
             if not line: continue
         
         if line.startswith('<dir>'):
            line_data['type'] = 301
         elif line.startswith('<item>'):
             line_data['type'] = 3
         elif line.startswith('<message>'):
             l_name = re.search('<message>(.*)</message>', line)
             if not l_name: continue
             l_name = l_name.group(1)
             if not l_name: continue
             line_data['name'] = l_name
             line_data['title'] = line_data['name']
             line_data['type'] = 320                
         elif line.startswith('<name>'):
             l_name = re.search('<name>(.*)</name>', line)
             if not l_name: continue
             l_name = l_name.group(1)
             if not l_name: continue
             line_data['name'] = l_name
             line_data['title'] = line_data['name']
             line_data['type'] = 301
         elif line.startswith('<title>'):
             l_name = re.search('<title>(.*)</title>', line)
             if not l_name: continue
             l_name = l_name.group(1)
             if not l_name: continue
             line_data['name'] = l_name
             line_data['title'] = line_data['name']
             line_data['type'] = 3
         elif line.startswith('<link>') and '</link>' in line:
             l_link = re.search('<link>(.*)</link>', line)
             if not l_link: continue
             l_link = l_link.group(1)
             if not l_link: continue
             l_link = l_link.strip()
             if l_link.startswith('<sublink>'):
                  for sublink in re.finditer('<sublink>(.+?)</sublink>', l_link):
                     if not sublink: continue
                     sublink = sublink.group(1)
                     if not sublink: continue                        
                     sublinks.append(sublink)
             else:                    
                 line_data['url'] = l_link
                 line_data['id'] = hashlib.md5(line_data['url'].lower()).hexdigest()
                 if not line_data.get('type', None):
                     if line_data['url'].endswith('.xml'):
                         line_data['type'] = 301
                     else:
                         line_data['type'] = 3
         elif line.startswith('<link>') and '</link>' not in line:
             continue
         elif line.startswith('<sublink>'):            
             for sublink in re.finditer('<sublink>(.+?)</sublink>', line):
                 if not sublink: continue
                 sublink = sublink.group(1)
                 if not sublink: continue
                 sublinks.append(sublink)    
         elif line.startswith('<thumbnail>'):
             l_thumb = re.search('<thumbnail>(.*)</thumbnail>', line)
             if not l_thumb: continue
             line_data['img'] = l_thumb.group(1)
     
    if line_data and line_data.get('name', None): 
         if line_data.get('type', None) and line_data.get('type', None) == 'playlist' and line_data.get('url', None) and not re.search( '.+?[/\\\\]{1}.+?', line_data.get('url', 'dummy')):
             line_data['type'] = 320
         if ( line_data.get('url', None) or line_data.get('type', None) == 'info') and line_data.get('type', None)   :
             line_data['fanart'] = fanart

             if (line_data['type'] == 3):
                 AddDir(line_data['name'] ,line_data['url'], line_data['type'], line_data['img'], isFolder=False)
             else:
                 AddDir(line_data['name'] ,line_data['url'], line_data['type'], line_data['img'], isFolder=True)

             line_data = {}
         elif sublinks:
             line_data['type'] = 3
             line_data['fanart'] = fanart
             for sublink in sublinks:
                 sub_line_data = line_data
                 line_data.update({'url':sublink})

                 if (line_data['type'] == 3):
                     AddDir(line_data['name'] ,line_data['url'], 3, line_data['img'], isFolder=False)
                 else:
                     AddDir(line_data['name'] ,line_data['url'], line_data['type'], line_data['img'], isFolder=True)

             sublinks = []
             line_data = {}
     
    SetViewThumbnail()	

def StreamLive(url):
#    BaseURL = GetCompile('STREAM247')
			
    BaseURL = 'https://www.streamlive.to/channels/'
    NextPage = url.replace('?p=4&q=','?p=5&q=')
    NextPage = url.replace('?p=3&q=','?p=4&q=')
    NextPage = url.replace('?p=2&q=','?p=3&q=')
    NextPage = url.replace('?p=1&q=','?p=2&q=')
	
    PageSource = ZeusGetContent(BaseURL+url)
    PageSource = regex_from_to(PageSource, '<ul class="clist clearfix">', '<strong>Page: </strong>') 
    all_videos = regex_get_all(PageSource, '<li', '</li>')
    AddInfoLink()	
    ListCount = 0	
    for a in all_videos:
        vurl = regex_from_to(a, '<a href="', '"')
        iconimage = regex_from_to(a, 'src="', '"')
        name = regex_from_to(a, 'alt="', '"')
        AddDir(name,vurl,630,iconimage)
 
    AddDir('[B][COLOR white]Next Page[/COLOR][/B]', NextPage ,620,'http://s6.postimg.org/4bbyeq1ep/next.png')
	
    SetViewThumbnail()

def StreamLiveLink(name,url,iconimage):
    PageSource = ZeusGetContent(url)
    print PageSource
    if 'Question: ' in PageSource:
       HakaMacEq = regex_from_to(PageSource, "Question: ", "=")
       HakaMacEq = HakaMacEq.replace('x','*').replace(' ','')   
	   
       print(eval(HakaMacEq))
       HakaMacEq = str(eval(HakaMacEq))
       print url+'?captcha='+HakaMacEq
       PageSource = ZeusGetContent(url+'?captcha='+HakaMacEq)
       print PageSource
	   
    vurl = regex_from_to(PageSource, "'file': '", ".',") 
    AddInfoLink()	
#    vurl = vurl + '|User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36'
    AddDir(name,vurl,3,iconimage,isFolder=False)
		
    SetViewThumbnail()
	
def Stream247(url):
    BaseURL = GetCompile('STREAM247')
    PageSource = ZeusGetContent(BaseURL+url)
    PageSource = regex_from_to(PageSource, '<div class="main-content">', '<footer id="t3-footer"') 
    all_videos = regex_get_all(PageSource, '<a class="article-link"', 'alt="')
    AddInfoLink()	
    ListCount = 0	
    for a in all_videos:
        vurl = BaseURL + regex_from_to(a, 'href="', '">')
        iconimage = BaseURL + regex_from_to(a, 'src="', '"')
        name = regex_from_to(a, 'img title="', '"')
        AddDir(name,vurl,38,iconimage)
    
    SetViewThumbnail()

def Stream247_Links(name,url,iconimage):
    BaseURL = GetCompile('STREAM247') + url
    PageSource = ZeusGetContent(url)
    background = BaseURL + regex_from_to(PageSource,'poster="','"')
    PageSource = regex_from_to(PageSource, '<div class="vjs-container-intrinsic-ratio">', '<script>var mypostertimeout') 
    all_videos = regex_get_all(PageSource, '<video id="live_player"', 'type="video/mp4">')
    AddInfoLink()	
    for a in all_videos:
        vurl = regex_from_to(a, 'src="', '"') + '|User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36'
        AddDir(name,vurl,3,iconimage,isFolder=False, background=background)
		
    SetViewThumbnail()

#hakamac
def SearchEuropa():
    SearchEntered = SearchBox()
    EuropaHome('?s='+SearchEntered)
	
def EuropaHome(url):
    ThisPageNo = FindFirstPattern(url, '/page/(.+?)/')
    if len(ThisPageNo) > 0:
        NextPage = url.replace('/page/'+str(int(ThisPageNo)),'/page/'+str(int(ThisPageNo) + 1))
    else:
        if url[0:3] == '?s=':
            NextPage = '/page/2/'+url
        else:
            NextPage = url+'/page/2/'
		
    PageSource = ZeusGetContent(GetCompile('EUROPA1')+url)
    AddDir('[B][COLOR white]'+regex_from_to(PageSource,'<span class="pages">','</span>')+'[/COLOR][/B]', NextPage ,550,'http://s6.postimg.org/4bbyeq1ep/next.png')
    AddInfoLink()
    AddDir("[COLOR white][B]YOUR FAVOURITE STREAMS HERE[/B][/COLOR]", "favorites" ,30 ,FavGraphic)
    AddDir("[COLOR white][B]SEARCH[/B][/COLOR]", "favorites" ,580 ,"http://s6.postimg.org/na1ile6xt/search.png")

    all_Links = regex_get_all(PageSource, '<h2 class="entry-title">', '<span class="author">')
    ListCount = 0	
    for a in all_Links:
        vurl = regex_from_to(a, '<a href="', '"')
        name = regex_from_to(a, 'rel="bookmark">', '</a>')
        NameDate = regex_from_to(a, 'pubdate="pubdate">','</time></a>')
        name = CLEAN(name).encode('utf-8')
        iconimage = 'http://2.bp.blogspot.com/_UqUwVPikChs/SmrNn69GuzI/AAAAAAAAJx0/xPsCAW9sSR8/s320/solo_-ottavima-volley-team-captain-17724.png'
        AddDir('[COLOR white]'+name+'[/COLOR] [COLOR gold] Updated '+NameDate+'[/COLOR]',str(vurl),560,iconimage,isFolder=True)
        ListCount = ListCount + 1
        if ListCount > 100:
            break	
    if url[0:3] <> '?s=':
         AddDir('[B][COLOR white]Next Page[/COLOR][/B]', NextPage ,550,'http://s6.postimg.org/4bbyeq1ep/next.png')
    SetViewList()


def EuropaList(url):
    PageSource = ZeusGetContent(url)
    iconimage = 'http://s6.postimg.org/hgyt6teap/freeiptv.png'
    AddInfoLink()
    AddDir("[COLOR white][B]ADD WORKING LINKS HERE TO FAVOURITES[/B][/COLOR]", "favorites" ,30 ,FavGraphic)

    PageSource = PageSource.replace('rtmp://$OPT:rtmp-raw=','').replace('\t','')
    PageSource = regex_from_to(PageSource, '<div class="entry-content">', '</div><!-- .entry-content -->')
    PageSource = re.sub(HTMLPattern, '', PageSource)
    PageSource = replaceHTMLCodes(PageSource)
    ListCount = 0
    name = 'Link'
    matches=re.compile('(.+?)\n',re.DOTALL).findall(PageSource)
    for Info in matches:
        if len(Info) > 1:
            if 'rtmp' in Info or 'rtme' in Info or 'http' in Info or 'rtsp' in Info or 'mms' in Info or 'mmsh' in Info:
                name = CLEAN(name).encode('utf-8')
                try: 
                    AddDir('[COLOR lime]'+name+'[/COLOR]',Info, 3, iconimage,isFolder=False)
                    name='Link'
                    url = ''
                except:
                    pass
            else:
                name =  re.sub('#EXTINF(.*?),','', Info) 
            ListCount = ListCount + 1
        if ListCount > 50:
             break  
			 
    if ListCount == 0:
	   AddDir('[COLOR red]SORRY NO WORKING LINKS HERE TRY ANOTHER SECTION[/COLOR]','BLANK',999,'http://s5.postimg.org/sp2sjkbxj/underconstruction.png')

    SetViewList()
			
def LaLineaLista(url):
    PageSource = ZeusGetContent(ZeusAlpha+url)
    PageTitle = regex_from_to(PageSource, 'PAGETITLE"', '"')
    PageIcon = regex_from_to(PageSource, 'PAGEICON"', '"')
    PageBackground = regex_from_to(PageSource, 'PAGEBACKGROUND"', '"')
    if len(PageTitle) > 1:
        AddDir("[COLOR yellow][B]"+ PageTitle +"[/B][/COLOR]", "Blank" ,98 ,PageIcon,background=PageBackground)

    LineTarget = "http://youtube.com"
    LineImage = PageIcon
    LineBackground = PageBackground

    PageSource = regex_from_to(PageSource, '########1', '########2')
    matches=re.compile('(.+?)\n',re.DOTALL).findall(PageSource)
    for Info in matches:
        if 'PIC"' in Info:
            LineImage = regex_from_to(Info, 'PIC"', '"')
        elif 'LINK"' in Info:
            LineTarget = regex_from_to(Info, 'LINK"', '"')
        elif 'LINEBACKGROUND"' in Info:
            LineBackground = regex_from_to(Info, 'LINEBACKGROUND"', '"')
        else:
            AddDir('[COLOR white]'+Info+'[/COLOR]',LineTarget, 60, LineImage,background=LineBackground,isFolder=False)

    SetViewList()
	
def VodlockerxScrape(url):
    Base_URL = GetCompile('VODLOCKERX')+ url
    link = ZeusGetContent(Base_URL)
    AddInfoLink()
    
    ThisPageNo = FindFirstPattern(Base_URL, '/date/(.+?)')
    if len(ThisPageNo) > 0:
        NextPage = url.replace('/date/'+str(int(ThisPageNo)),'/date/'+str(int(ThisPageNo) + 1))
    else:
        NextPage = url+'/date/2'

    count = 0
    all_videos = regex_get_all(link, '<div class="item" style="text-align:center">', 'alt=" " style="width:130px;height:190px;background-color: #717171;"/>')
    for a in all_videos:
        vurl = regex_from_to(a, '<a href="'+GetCompile('VODLOCKERX'), '" class="spec-border-ie" title="">')
        name = vurl.replace('-',' ').upper().replace('MOVIE/',' ').upper()
        iconimage = regex_from_to(a, 'src="', '"')
        vurl = GetCompile('VODLOCKERX') + vurl
        count = count + 1
        AddDir('[B][COLOR yellow]'+name+'[/COLOR][/B]',vurl,240,iconimage)
    
    if count == 42:
        AddDir('[B][COLOR pink]Next Page[/COLOR][/B]', NextPage ,230,'http://s6.postimg.org/4bbyeq1ep/next.png')

    SetViewThumbnail()	
	
def VodlockerxSources(name,url,iconimage):
    link = ZeusGetContent(url)
    AddInfoLink()
    link = regex_from_to(link, '<div class="breakaway-wrapper" id="video-pages-wrapper">', '<textarea id="problem"></textarea>')

    count = 0
    all_videos = regex_get_all(link, '<ul class="filter"', 'Play Now</a></li>')
    for a in all_videos:
        vurl = regex_from_to(a, '<a href="', '" target="_blank">')
        if vurl.find('idownloadplay') < 1:
           count = count + 1
           AddDir(name + '[COLOR yellow] Source:' + str(count)+  '[/COLOR]',vurl,3,iconimage,isFolder=False)
    
    if count == 0:
       AddDir('[B][COLOR red]UPDATING PLEASE CHECK LATER [/COLOR][/B]', ' ',999,'http://s6.postimg.org/4bbyeq1ep/next.png')

    SetViewList()	

def SearchVodlockerx():	
    WhatSearched = SearchBox()
    Base_URL = 'http://www.vodlockerx.com/index.php?menu=search&query=' + WhatSearched
    link = ZeusGetContent(Base_URL)
    AddInfoLink()

    count = 0
    all_videos = regex_get_all(link, '<div class="span-6 inner-6 tt  view">', '<div class="title-overflow"></div>')
    for a in all_videos:
        vurl = regex_from_to(a, '<a href="http://www.vodlockerx.com/', '" class="spec-border-ie" title="">')
        name = vurl.replace('-',' ').upper().replace('MOVIE/',' ').upper()
        iconimage = regex_from_to(a, 'src="', '"')
        vurl = 'http://www.vodlockerx.com/' + vurl
        count = count + 1
        AddDir('[B][COLOR yellow]'+name+'[/COLOR][/B]',vurl,240,iconimage)
 
    SetViewThumbnail()	
	

def UFCSection(url):
    link = ZeusGetContent(url)
    nextpage = ''
    if link.find('rel="next') > 0:
       nextpage = regex_from_to(link, '<link rel="next" href="//', '"/>')
	   
    link = regex_from_to(link, '<div class="nag cf">', '<div class="loop-nav pag-nav">') 
    all_videos = regex_get_all(link, '<div id="post', '<span class="overlay"></span>')
    for a in all_videos:
        title = regex_from_to(a, ' title="', '"')
        vurl = regex_from_to(a, ' href="', '"')
        iconimage = "http://" + regex_from_to(a, '<img src="//', '" alt=')
        AddDir(title,vurl,15,iconimage)

    if len(nextpage) > 0:
       nextpage = 'http://' + nextpage
       AddDir('[B][COLOR yellow]Next Page >>>[/COLOR][/B]',nextpage,9,"http://s6.postimg.org/4bbyeq1ep/next.png")

    SetViewThumbnail()	
	
def UFCScrape(url):
    link = ZeusGetContent(url)
    iconimage = regex_from_to(link, '<meta name="twitter:image:src" content="', '"/>') 
    link = regex_from_to(link, '<div class="entry-content rich-content">', '<div id="extras">') 
    all_videos = regex_get_all(link, '<a class="small cool-blue vision-button"', '</a>')
 
    c=0
    for a in all_videos:
        vurl = regex_from_to(a, 'button" href="', '" target="')
        if 'protect.cgi' not in vurl:
            c=c+1
            title = "[COLOR gold] Source ["+str(c)+"] [/COLOR]" + regex_from_to(a, 'blank">', '</a>')
            AddDir(title,vurl,16,iconimage)

def StreamUFC(name,url,thumb):
    name2 = name
    url2 = url
		
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        streamlink = urlresolver.resolve(urllib2.urlopen(req).url)
        addLinkMovies(name2,streamlink,thumb)
    except:
        Notify('small','ZEUS VIDEO Sorry Link Removed:', 'Please try another one.',9000)
		   
def AddInfoLink():
    AddDir(DirectoryMSG,'chin-info', 6, "http://s6.postimg.org/fr7wa8azl/donate.png", isFolder=True)
	

def PlayVimeo(url):
#Thanks to lambda for this
    url = 'http://player.vimeo.com/video/'+url+'/config'
    try: 
        link = ZeusGetContent(url)
        link = json.loads(link)
        u = link['request']['files']['h264']
        url = None
        try: url = u['hd']['url']
        except: pass
        try: url = u['sd']['url']
        except: pass
        Playurl = "PlayMedia("+url+")"
        xbmc.executebuiltin(Playurl)
    except: pass
	
		
def PlayYoutubeView(url):
    try:
        url = "PlayMedia(plugin://plugin.video.youtube/?action=play_video&videoid="+url+")"
        xbmc.executebuiltin(url)
    except:
        xbmc.executebuiltin("XBMC.Notification(ZEUS VIDEO,This host is not supported or resolver is broken::,10000)")
	   
def StreamsList(url):
    links = 'I:"0" A:"Cannot Connect" B:"[COLOR yellow][B]*OFFSHORE DOWN*[/B][/COLOR]" C:"'+ZeusGraphic+"'"
    StreamlistURL = ''
    if url[:4].lower() == "evo-":
        StreamlistURL = EvoUrl
    elif url[:5].lower() == "chin-":
        StreamlistURL = ZeusAlpha
    else:
        StreamlistURL = Raw
		
    links = ZeusGetContent(StreamlistURL + url)
    SetViewLayout = "50"

    LayoutType = re.compile('FORMAT"(.+?)"').findall(links)
    if LayoutType:
       SetViewLayout = str(LayoutType)
       SetViewLayout = SetViewLayout.replace('[u\'','').replace(']','').replace('\'','')
 	
    if 'chin-info' not in url:
        AddInfoLink()

    all_videos = regex_get_all(links, 'I:', '"#')
    for a in all_videos:
        mode = regex_from_to(a, 'I:"', '"')
        url = regex_from_to(a, 'A:"', '"')
        name = regex_from_to(a, 'B:"', '"')
        icon = regex_from_to(a, 'C:"', '"')
        if mode == '60' or mode == '3' or mode == '61': 
           AddDir('[COLOR white]'+name+'[/COLOR]',url, mode, icon,isFolder=False)
        else:
           AddDir('[COLOR white]'+name+'[/COLOR]',url, mode, icon)
		   
    xbmc.executebuiltin("Container.SetViewMode("+str(SetViewLayout)+")")
	
def StreamM3U(url):
    links = '#A:-1,INVALID LIST \r\n http://youtube.com'
    StreamlistURL = ''
    if url[:4].lower() == "evo-":
        StreamlistURL = EvoUrl
    elif url[:5].lower() == "chin-":
        StreamlistURL = ZeusAlpha
    else:
        StreamlistURL = Raw

    links = ZeusGetContent(StreamlistURL + url)
	    
    SetViewLayout = "50"
     
    LayoutType = re.compile('FORMAT"(.+?)"').findall(links)
    if LayoutType:
       SetViewLayout = str(LayoutType)
       SetViewLayout = SetViewLayout.replace('[u\'','').replace(']','').replace('\'','')
	   
    links = links.replace('#AAASTREAM:','#A:').replace('#EXTINF:','#A:')
    matches=re.compile('^#A:-?[0-9]*(.*?),(.*?)\n(.*?)$',re.I+re.M+re.U+re.S).findall(links)

    for params, name, url in matches:
        item_param = params
#        if ChildLockStatus <> 'ON':
        AddDir('[COLOR lime]'+name+'[/COLOR]',url, 3, ZeusGraphic,isFolder=False)

    xbmc.executebuiltin("Container.SetViewMode("+str(SetViewLayout)+")")
	
def LockedIndex(url):
    links = 'I:"0" A:"Cannot Connect" B:"[COLOR yellow][B]*OFFSHORE DOWN*[/B][/COLOR]" C:"'+ZeusGraphic+"'"
    StreamlistURL = ''
    if url[:4].lower() == "evo-":
       StreamlistURL = EvoUrl
    else:
	   StreamlistURL = ZeusAlpha
	
    links = ZeusGetContent(StreamlistURL + url)
	
    if url[:4].lower() == "evo-":
       links = links.replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('<name>','<title>').replace('</name>','</title>').replace('</p>','\r\n').replace('&nbsp;','').replace('&#8221;','"').replace('&#8243;','"').replace('<!-- EVO LINK','\n').replace('END EVO -->','').replace('<p>','').replace('&#038;','&').replace('&#8211;','--').replace('<br />','').replace('&#215;','x')
       links = links.replace('<a href="','').replace('</a>&#8220;#','"')
	   
    SetViewLayout = "50"
     
    LayoutType = re.compile('FORMAT"(.+?)"').findall(links)
    if LayoutType:
       SetViewLayout = str(LayoutType)
       SetViewLayout = SetViewLayout.replace('[u\'','').replace(']','').replace('\'','')
	   
    AddInfoLink()
    if ChildLockStatus == 'OFF':
       AddDir('[COLOR green][B]ChildLock is OFF[/B][/COLOR] Click here to Activate' ,"Childlock",400,"http://s6.postimg.org/z4w8fqo4h/childlock.png",isFolder=False)  
    else:
       AddDir('[COLOR red][B]ChildLock is ON[/B][/COLOR] Click here to Deactivate' ,"Childlock",400,"http://s6.postimg.org/z4w8fqo4h/childlock.png",isFolder=False)  
	
    all_videos = regex_get_all(links, 'I:', '"#')
    for a in all_videos:
        mode = regex_from_to(a, 'I:"', '"')
        url = regex_from_to(a, 'A:"', '"')
        name = regex_from_to(a, 'B:"', '"')
        icon = regex_from_to(a, 'C:"', '"')
        if ChildLockStatus == 'OFF':
           AddDir('[COLOR lime]'+name+'[/COLOR]',url, mode, icon)
				
    xbmc.executebuiltin("Container.SetViewMode("+str(SetViewLayout)+")")

def ChildLock():
#h@k@m@c
    pwd = ''	
    KeyboardMessage = 'Type Password to deactivate Childlock (case sensitive)'
    ChildLockFile = os.path.join(libDir,"childlock.txt")
    try:
        f = open(ChildLockFile,'r')
        pwd = f.read()
        pwd = regex_from_to(pwd, '{', '}')
        f.close()
    except:
        pwd = ""
        KeyboardMessage = 'Type Password to Activate Childlock (case sensitive)'
	
    passwordEntered = ''
    keyboard = xbmc.Keyboard(passwordEntered, KeyboardMessage)
    keyboard.doModal()
    if keyboard.isConfirmed():
       passwordEntered = keyboard.getText() .replace(' ','+')
       if passwordEntered == None:
          return False
	
    if len(passwordEntered) == 0: 
        xbmcgui.Dialog().ok('ZEUS VIDEO Childlock', 'No Password entered. No action taken')
        return	   
    else:
        xbmcgui.Dialog().ok('ZEUS VIDEO Childlock', 'Password Entered: '+passwordEntered)
	   
    if len(passwordEntered) > 0 and pwd =='':
        try:
            f = open(ChildLockFile, 'w') 
            f.write('{'+passwordEntered+'}') 
            f.close()
            ChildLockStatus == 'ON'
            xbmcgui.Dialog().ok('ZEUS Childlock', 'Childlock Activation Successful', 'Return to ZEUS Home Page')			
        except:
            ChildLockStatus == 'OFF'
            xbmcgui.Dialog().ok('ZEUS Childlock', 'Childlock Activation Failed', 'Exit Afterdark & Return')

    if len(passwordEntered) > 0 and pwd == passwordEntered:	
        try:
            os.remove(ChildLockFile)
            xbmcgui.Dialog().ok('ZEUS Childlock', 'ChildLock removed', 'Return to ZEUS Home Page')
        except:
            xbmcgui.Dialog().ok('ZEUS Childlock', 'Cannot remove childlock', 'Reboot and try again')  
	   
    if len(passwordEntered) > 0 and pwd <> passwordEntered and len(pwd) > 0:
       xbmcgui.Dialog().ok('ZEUS Childlock', 'Password incorrect Childlock still active')

def Xham_Cats(url):
    Xham_Category = url
    PageSource = ZeusGetContent(GetCompile('HAMSTER1'))
    PageSource = RemoveBitsMovie(PageSource)
    iconimage = ''
	
    if Xham_Category == 'Straight':
       PageSource = regex_from_to(PageSource,'<div class="title">Straight</div>', '<div class="catName">') 
       iconimage = 'http://s13.postimg.org/h0ioz9kk7/straight.png'
    elif Xham_Category == 'Gays':
       PageSource = regex_from_to(PageSource,'<div class="title">Gays</div>', '<div id="footer">')
       iconimage = 'http://s3.postimg.org/x6qcgvisz/gay.png'
    else:
       PageSource = regex_from_to(PageSource,'<div class="title">Transsexuals</div>', '<div class="catName">')
       iconimage = 'http://s23.postimg.org/y3sy9ak0r/transsexual.png'

    all_links = regex_get_all(PageSource, '<a class="btnBig" href="', '</a>')
    AddInfoLink()
    for a in all_links:
        vurl = regex_from_to(a, '<a class="btnBig" href="', '">')
        name = regex_from_to(a, '     ', '</a>')
        
        if name.find('div>') > 0:
           name = name[name.find('div>')+4:]
        name = name.strip().upper()
        title = '[COLOR gold]'+ name +'[/COLOR]'
        
        AddDir(title,vurl,610,iconimage)
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )		
    SetViewList()

def Xham_FindLinks(url):
    PageSource = ZeusGetContent(url)
    NextPageUrl = regex_from_to(PageSource, '<link rel="next" href="', '">')
    PageSource = regex_from_to(PageSource,"id='vListTop'>", "<div id='adBottom'>")
    PageSource = RemoveBitsMovie(PageSource)
    all_links = regex_get_all(PageSource, "<div class='video'>", "</div>")
    AddInfoLink()
    for a in all_links:
        vurl = regex_from_to(a, "<a href='", "'  ")
        name = regex_from_to(a, 'alt="', '"')
        iconimage = regex_from_to(a, "class='hRotator' ><img src='", "' ")
        if len(iconimage) < 5:
           iconimage = 'http://s23.postimg.org/5pvk434rv/adultmovies.png'
        name = name.strip()
        title = '[COLOR gold]'+ name +'[/COLOR]'
        
        url = Xham_Stream(vurl)
        AddDir(title,url,3,iconimage,isFolder=False)
	
    if len(NextPageUrl) > 10:
        AddDir('[B][COLOR yellow]Next Page >>>[/COLOR][/B]',NextPageUrl,610,"http://s6.postimg.org/4bbyeq1ep/next.png")

    SetViewThumbnail()
			   
def Xham_Stream(url):
    PageSource = ZeusGetContent(url)
    PageSource = regex_from_to(PageSource,"file: '", "',")
    return PageSource
	
def XMLRead500(url):
    StreamlistURL = ''
    if url[:4].lower() == "evo-":
        StreamlistURL = EvoUrl
    elif url[:5].lower() == "chin-":
        StreamlistURL = ZeusAlpha
    else:
        StreamlistURL = Raw
		
    try: links = net.http_GET(StreamlistURL + url).content
    except: return

    links = links.encode('ascii', 'ignore').decode('ascii')
   
    SetViewLayout = "50"
     
    LayoutType = re.compile('FORMAT"(.+?)"').findall(links)
    if LayoutType:
       SetViewLayout = str(LayoutType)
       SetViewLayout = SetViewLayout.replace('[u\'','').replace(']','').replace('\'','')
    
    AddInfoLink()
	
    all_videos = regex_get_all(links, 'I:', '"#')
    for a in all_videos:
        mode = regex_from_to(a, 'I:"', '"')
        vurl = regex_from_to(a, 'A:"', '"')
        name = regex_from_to(a, 'B:"', '"')
        icon = regex_from_to(a, 'C:"', '"')

        AddDir('[COLOR lime]'+name+'[/COLOR]',vurl, mode, icon)
		   
    
    all_videos = regex_get_all(links, '<item>', '</item>')
    for a in all_videos:
        background = ''
        vurl = regex_from_to(a, '<link>', '</link>').replace('  ', ' ')
        name = regex_from_to(a, '<title>', '</title>')
        icon = regex_from_to(a, '<thumbnail>', '</thumbnail>')
        background = regex_from_to(a, '<fanart>', '</fanart>')
        if len(background) < 5:
            background = icon

        AddDir('[COLOR lime]'+name+'[/COLOR]',vurl, 3, icon,isFolder=False, background=background)
    list = m3u2list(StreamlistURL + url)
    for channel in list:
        name = common.GetEncodeString(channel["display_name"])
        mode = 46 if channel["url"].find("youtube") > 0 else 3

        AddDir(name ,channel["url"], mode, ZeusGraphic, isFolder=False)
		
    xbmc.executebuiltin("Container.SetViewMode("+str(SetViewLayout)+")")	

def m3u2list(url):
    response = ZeusGetContent(url)
    response = response.replace('#AAASTREAM:','#A:')
    response = response.replace('#EXTINF:','#A:')
    matches=re.compile('^#A:-?[0-9]*(.*?),(.*?)\n(.*?)$',re.I+re.M+re.U+re.S).findall(response)
    li = []
    for params, display_name, url in matches:
        item_data = {"params": params, "display_name": display_name, "url": url}
        li.append(item_data)
    list = []
    for channel in li:
        item_data = {"display_name": channel["display_name"], "url": channel["url"]}
        matches=re.compile(' (.+?)="(.+?)"',re.I+re.M+re.U+re.S).findall(channel["params"])
        for field, value in matches:
            item_data[field.strip().lower().replace('-', '_')] = value.strip()
        list.append(item_data)
    return list
	
def YouTube_List(url): 
# H@k@M@c
    if "channel" in url:
        url = 'https://www.youtube.com/' + url + '/videos'
    else:
        url = 'https://www.youtube.com/user/' + url + '/videos'
		
    link = ZeusGetContent(url)

    AddInfoLink()
    all_videos = regex_get_all(link, '<h3 class="yt-lockup-title">', '</span></h3>')
    for a in all_videos:
        name = regex_from_to(a, 'title="', '"').replace("&amp;","&")
        name = replaceHTMLCodes(name)
        video_id = regex_from_to(a, 'href="', '"').replace("&amp;","&")
        video_id = video_id[9:]
        icon = 'http://i.ytimg.com/vi/' + str(video_id) + '/0.jpg'
        AddDir(name , video_id, 60, icon, isFolder=False)

    SetViewThumbnail()
	
def Channel_Scraper(url): 
# H@k@M@c
    AddInfoLink()
    if '##NOSEARCH##' not in url and '&page=' not in url:
        ChannelSearchLink(url)
    else:
        url = url.replace('##NOSEARCH##','')
		
    if 'youtube.com' not in url:
        url = GetCompile('CHANNELQ1') + url

    PageNo = 0
    if "&page=" in url:
         PageNo = regex_from_to(url, '&page=', '::::')
         if int(PageNo) > 0: 
             NextNo = int(PageNo) + 1
             Nexturl = url.replace("&page=" + PageNo,"&page=" + str(NextNo))
    else:
         PageNo = 2
         Nexturl = url + '&page=2::::'
    url = url.replace('::::','')
    link = ZeusGetContent(url)
    Count = 0
    
    all_videos = regex_get_all(link, GetCompile('CHANNELL1'), GetCompile('CHANNELR1'))
    for a in all_videos:
        name = regex_from_to(a, 'dir="ltr">', '</a><span').replace("&amp;","&")
        name = replaceHTMLCodes(name)
        video_id = regex_from_to(a, 'href="', '"').replace("&amp;","&")
        video_id = video_id[9:]
        icon = 'http://i.ytimg.com/vi/' + str(video_id) + '/0.jpg'
        if "title" not in name:
            Count = Count + 1
            AddDir(name , video_id, 60, icon, isFolder=False)

    if PageNo < 1:
         AddDir('NOTHING FOUND' , 'NADA', 9999, 'http://s6.postimg.org/4uln1qi75/support.png', isFolder=False)
			
    if PageNo > 0:
        AddDir('NEXT PAGE' , Nexturl, 59, 'http://s6.postimg.org/4bbyeq1ep/next.png', isFolder=True)

    SetViewThumbnail()

def ChannelSearchLink(url):
     AddDir('SEARCH' , url, 58, 'http://s6.postimg.org/na1ile6xt/search.png', isFolder=True)
	 
def SearchChannel(url):
    SearchEntered = SearchBox()
    Channel_Scraper(url + '+'+SearchEntered)

def SearchBox():
    SearchEntered = ''
    keyboard = xbmc.Keyboard(SearchEntered, 'Zeus Search')
    keyboard.doModal()
    if keyboard.isConfirmed():
       SearchEntered = keyboard.getText() .replace(' ','+')

    return 	SearchEntered	  
	
def FindFirstPattern(text,pattern):
    result = ""
    try:    
        matches = re.findall(pattern,text, flags=re.DOTALL)
        result = matches[0]
    except:
        result = ""

    return result

def LookLocoNum():
    LocoNum = ''
    LocoFile = os.path.join(libDir, 'loconum')

    try:
        f = open(LocoFile,'r')
        LocoLink = f.read()
        LocoNum = regex_from_to(LocoLink, '{', '}')
        f.close()
    except:
        pass
    Lockitin = '&extra=' + urllib.quote_plus(addonDir)
    if LocoNum == '':
       LocoNum = ZeusGetContent(ZeusLocoNum+'blank'+Lockitin)
    else:
       LocoNum = ZeusGetContent(ZeusLocoNum+LocoNum+Lockitin)

    f = open(LocoFile, 'w')
    f.write('{'+LocoNum+'}') 
    f.close()
	
	
def FullMatches(url):
    custurlreplay = str(base64.decodestring(LocalisedReplay))
    link = ZeusGetContent(custurlreplay+url)

    r='<div class="cover"><a href="(.+?)" rel="bookmark" title="(.+?)">.+?<img src="(.+?)".+?<p class="postmetadata longdate" rel=".+?">(.+?)/(.+?)/(.+?)</p>'
    match=re.compile(r,re.DOTALL).findall(link)
    AddInfoLink()
    for vurl,name,iconimage,month,day,year in match:
        _date='%s/%s/%s'%(day,month,year)  
        name='%s-[COLOR gold][%s][/COLOR]'%(name,_date)    
        AddDir(name,vurl,152,iconimage)
    
    nextpage=re.compile('</span><a class="page larger" href="(.+?)">').findall(link)
    if nextpage:
       vurl = str(nextpage)
       vurl = vurl.replace('[u\'','')
       vurl = vurl.replace(']','')
       vurl = vurl.replace('\'','')
       AddDir('[B][COLOR yellow]Next Page >>>[/COLOR][/B]',vurl,151,"http://s6.postimg.org/4bbyeq1ep/next.png")

    SetViewThumbnail()	

def SearchReplays():
        search_entered = ''
        keyboard = xbmc.Keyboard(search_entered, 'Search Zeus Replays')
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_entered = keyboard.getText() .replace(' ','+')
            if search_entered == None:
                return False
        link=OPEN_MAGIC('http://www.google.com/cse?cx=partner-pub-9069051203647610:8413886168&ie=UTF-8&q=%s&sa=Search&ref=livefootballvideo.com/highlights'%search_entered)
        match=re.compile('" href="(.+?)" onmousedown=".+?">(.+?)</a>').findall(link)
        for url,dirtyname in match: 
            import HTMLParser
            cleanname= HTMLParser.HTMLParser().unescape(dirtyname)
            name= cleanname.replace('<b>','').replace('</b>','')
            AddDir(name,url,152,'')
        SetViewList()	 
		
def REPLAYSGETLINKS(name,url):#  cause mode is empty in this one it will go back to first directory
    link = ZeusGetContent(url)
    AddInfoLink()
    if "proxy.link=lfv*" in link :
        import decrypter
        match = re.compile('proxy\.link=lfv\*(.+?)&').findall(link)
        match = uniqueList(match)
        match = [decrypter.decrypter(198,128).decrypt(i,base64.urlsafe_b64decode('Y0ZNSENPOUhQeHdXbkR4cWJQVlU='),'ECB').split('\0')[0] for i in match]
        for url in match:

            url = replaceHTMLCodes(url)
            if url.startswith('//') : url = 'http:' + url
            url = url.encode('utf-8')  
            _name=url.split('://')[1] 
            _name=_name.split('/')[0].upper()
            ReplaysAddDir( name+' - [COLOR red]%s[/COLOR]'%_name , url , 120 , ZeusGraphic , '' )
    if "www.youtube.com/embed/" in link :
        r = 'youtube.com/embed/(.+?)"'
        match = re.compile(r,re.DOTALL).findall(link)
        yt= match[0]
        iconimage = 'http://i.ytimg.com/vi/%s/0.jpg' % yt.replace('?rel=0','')
        url = 'plugin://plugin.video.youtube/?path=root/video&action=play_video&videoid=%s' % yt.replace('?rel=0','')
        ReplaysAddDir( name+' - [COLOR red]YOUTUBE[/COLOR]' , url , 120 , iconimage , '' )
    if "dailymotion.com" in link :
        r = 'src="http://www.dailymotion.com/embed/video/(.+?)\?.+?"></iframe>'
        match = re.compile(r,re.DOTALL).findall(link)
        for url in match :
            ReplaysAddDir ( name+' - [COLOR red]DAILYMOTION[/COLOR]' , url , 120 , ZeusGraphic, '' )
    if "http://videa" in link :
        r = 'http://videa.+?v=(.+?)"'
        match = re.compile(r,re.DOTALL).findall(link)
        for url in match :
            ReplaysAddDir (name+' - [COLOR red]VIDEA[/COLOR]',url,120,ZeusGraphic, '' )
            
    if "rutube.ru" in link :
        r = 'ttp://rutube.ru/video/embed/(.+?)\?'
        match = re.compile(r,re.DOTALL).findall(link)
        for url in match :
            ReplaysAddDir (name+' - [COLOR red]RUTUBE[/COLOR]',url,120,ZeusGraphic, '' )
    if 'cdn.playwire.com' in link :
        r = 'cdn.playwire.com/bolt/js/embed.min.js.+?data-publisher-id="(.+?)".+?data-config="(.+?)">'
        match = re.compile(r,re.DOTALL).findall(link)
        for id ,vid in match :
            
            url=vid.replace('player.json','manifest.f4m')
            ReplaysAddDir (name+' - [COLOR red]PLAYWIRE[/COLOR]',url,120,ZeusGraphic, '' )
    if "vk.com" in link :
        r = '<iframe src="http://vk.com/(.+?)"'
        match = re.compile(r,re.DOTALL).findall(link)
        for url in match :
            ReplaysAddDir (name+' - [COLOR red]VK.COM[/COLOR]','http://vk.com/'+url,120,ZeusGraphic, '' )
    if "mail.ru" in link :
        r = 'http://videoapi.my.mail.ru/videos/embed/(.+?)\.html'
        match = re.compile(r,re.DOTALL).findall(link)
        for url in match :
            ReplaysAddDir (name+' - [COLOR red]MAIL.RU[/COLOR]','http://videoapi.my.mail.ru/videos/%s.json'%url,120,ZeusGraphic, '' )            
          

def PLAYSTREAM(name,url,iconimage):
        if 'YOUTUBE' in name:
            link = str(url)
        elif 'VIDEA' in name:
            try:
                url=url.split('-')[1]
            except:
                url=url
            link = GrabVidea(url)
        elif 'VK.COM' in name:
            link = GrabVK(url)

        elif 'MAIL.RU' in name:
            link = GrabMailRu(url)

            
        elif 'RUTUBE' in name:
            try:
                html = 'http://rutube.ru/api/play/trackinfo/%s/?format=xml'% url.replace('_ru','')
                link = net.http_GET(html).content
                r = '<m3u8>(.+?)</m3u8>'
                match = re.compile(r,re.DOTALL).findall(link)
                if match:
                    link=match[0]
                else:
                    dialog = xbmcgui.Dialog()
                    dialog.ok("Football Replays", '','Sorry Video Is Private', '')
                    return
            except:
                dialog = xbmcgui.Dialog()
                dialog.ok("Football Replays", '','Sorry Video Is Private', '')
                return
        elif 'PLAYWIRE' in name:
            link = net.http_GET(url).content
 #           link = OPEN_URL(url)
            r = '<baseURL>(.+?)</baseURL>.+?media url="(.+?)"'
            match = re.compile(r,re.DOTALL).findall(link)
            if match:
                link=match[0][0]+'/'+match[0][1]
                
                
        elif 'DAILYMOTION' in name:
            try:
                url = url.split('video/')[1]
            except:
                url = url
            link = getStreamUrl(url)
        try:
            liz=xbmcgui.ListItem(name, iconImage=ZeusGraphic, thumbnailImage=iconimage)
            liz.setInfo( type="Video", infoLabels={ "Title": name} )
            liz.setProperty("IsPlayable","true")
            liz.setPath(link)
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
        except:pass
        
 
def GrabMailRu(url):
    print 'RESOLVING VIDEO.MAIL.RU VIDEO API LINK'
      
    items = []
    quality = "???"
    data = getData(url)
    cookie = net.get_cookies()
    for x in cookie:

         for y in cookie[x]:

              for z in cookie[x][y]:
                   
                   l= (cookie[x][y][z])
    name=[]
    url=[]
    r = '"key":"(.+?)","url":"(.+?)"'
    match = re.compile(r,re.DOTALL).findall(data)
    for quality,stream in match:
        name.append(quality.title())
        

  
        test = str(l)
        test = test.replace('<Cookie ','')
        test = test.replace(' for .my.mail.ru/>','')
        url.append(stream +'|Cookie='+test)

    return url[xbmcgui.Dialog().select('Please Select Resolution', name)]

def getData(url,headers={}):
    net.save_cookies(cookie_jar)
    req = urllib2.Request(url)
    req.add_header('User-Agent', USER_AGENT)
    response = urllib2.urlopen(req)
    data=response.read()
    response.close()
    return data
	
def ReplaysAddDir(name,url,mode,iconimage,page):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&page="+str(page)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name} )
        if mode == 120:
            liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def uniqueList(name):
    uniques = []
    for n in name:
        if n not in uniques:
            uniques.append(n)
    return uniques  

def replaceHTMLCodes(txt):
    import HTMLParser

    # Fix missing ; in &#<number>;
    txt = re.sub("(&#[0-9]+)([^;^0-9]+)", "\\1;\\2", makeUTF8(txt))

    txt = HTMLParser.HTMLParser().unescape(txt)
    txt = txt.replace("&amp;", "&")
    return txt  

def makeUTF8(data):
    return data
    try:
        return data.decode('utf8', 'xmlcharrefreplace') # was 'ignore'
    except:
        s = u""
        for i in data:
            try:
                i.decode("utf8", "xmlcharrefreplace") 
            except:
                log("Can't convert character", 4)
                continue
            else:
                s += i
        return s  

def getStreamUrl(id):
    maxVideoQuality = "1080p"
    content = net.http_GET("http://www.dailymotion.com/embed/video/"+id).content

    if content.find('"statusCode":410') > 0 or content.find('"statusCode":403') > 0:
        xbmc.executebuiltin('XBMC.Notification(Info:,Not Found (DailyMotion)!,5000)')
        return ""
    else:
        matchFullHD = re.compile('"stream_h264_hd1080_url":"(.+?)"', re.DOTALL).findall(content)
        matchHD = re.compile('"stream_h264_hd_url":"(.+?)"', re.DOTALL).findall(content)
        matchHQ = re.compile('"stream_h264_hq_url":"(.+?)"', re.DOTALL).findall(content)
        matchSD = re.compile('"stream_h264_url":"(.+?)"', re.DOTALL).findall(content)
        matchLD = re.compile('"stream_h264_ld_url":"(.+?)"', re.DOTALL).findall(content)
        url = ""
        if matchFullHD and maxVideoQuality == "1080p":
            url = urllib.unquote_plus(matchFullHD[0]).replace("\\", "")
        elif matchHD and (maxVideoQuality == "720p" or maxVideoQuality == "1080p"):
            url = urllib.unquote_plus(matchHD[0]).replace("\\", "")
        elif matchHQ:
            url = urllib.unquote_plus(matchHQ[0]).replace("\\", "")
        elif matchSD:
            url = urllib.unquote_plus(matchSD[0]).replace("\\", "")
        elif matchLD:
            url = urllib.unquote_plus(matchLD[0]).replace("\\", "")
        return url

def SEARCHTV(url):
    keyb = xbmc.Keyboard('', 'Zeus Search TV Shows')
    keyb.doModal()
    if (keyb.isConfirmed()):
        AddInfoLink()
        search = keyb.getText()
        encode=urllib.quote(search)
        url = 'search.php?key='+encode
        links = ZeusGetContent(GetCompile('TV1')+url)
        links = regex_from_to(links, '<div class="found">', '</div>')
        links = RemoveBitsMovie(links)
        all_genres = regex_get_all(links, '<ul><li>', '</li></ul>')
        for a in all_genres:
            url = regex_from_to(a, '<a href="', '"')
            name = regex_from_to(a, '">', '<').lstrip()
            name = CLEAN(name)
            AddDir(name,url,87,ZeusPNG,background=GetCompile('TVBackground'))

	
def TVLatestAdded(url):
    links = ZeusGetContent(GetCompile('TV1')+url)
    links = regex_from_to(links, '<div class="home">', '</div>')
    links = RemoveBitsMovie(links)
    AddInfoLink()
    match=re.compile('<li><a href="/(.+?)">(.+?)</a></li>',re.DOTALL).findall(str(links))
    for url,name in match:
        name = CLEAN(name)
        searcher = url.replace('/','')
        AddDir(name,url,87,ZeusPNG,background=GetCompile('TVBackground'))
				
    SetViewList() 
	
def GetSeasons(url):
    links = ZeusGetContent(GetCompile('TV1')+url)
    links = regex_from_to(links, '<div class="leftpage_top">', '<div class="addthis">')
    links = RemoveBitsMovie(links)
    AddInfoLink()
    match=re.compile("<h3><a href='/(.+?)'>(.+?)</a></h3>",re.DOTALL).findall(str(links))
    for url,name in match:
        name = CLEAN(name)
        AddDir(name,url,88,ZeusPNG,background=GetCompile('TVBackground'))
				
    SetViewList() 
	
def TVGetSeasonLinks(url):
    links = ZeusGetContent(GetCompile('TV1')+url)
    links = regex_from_to(links, '<h3>', '<div class="addthis">')
    links = RemoveBitsMovie(links)
    AddInfoLink()
    match=re.compile("<a href='/(.+?)'><strong>(.+?)</a>",re.DOTALL).findall(str(links))
    for url,name in match:
        name = CLEAN(name)
        name = re.sub(HTMLPattern, '', name)
        AddDir(name,url,81,ZeusPNG,background=GetCompile('TVBackground'))
				
    SetViewList() 

def ZeusGetContent(url):
    Data = net.http_GET(url).content
    Data = Data.encode('ascii', 'ignore').decode('ascii')
    return Data	

def NEWEPISODESTV(url):
    links = ZeusGetContent(GetCompile('TV1')+url)
    links = regex_from_to(links, '<div class="home">', '</div>')
    links = RemoveBitsMovie(links)
    AddInfoLink()
    
    match=re.compile('<li><a href="/(.+?)">(.+?)</a></li>',re.DOTALL).findall(links)
    for url,name in match:
        name = CLEAN(name)
        url = url+'/'
        AddDir(name,url,81,ZeusPNG,background=GetCompile('TVBackground'))
    
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )	
    SetViewList()
		
	
def NEWLINKS(url):
        links = ZeusGetContent(url)
        links = RemoveBitsMovie(links)
        links = regex_from_to(links, '<div class="leftpage_frame">', '<div class="foot"')
        AddInfoLink()
        match=re.compile('<li><a href="/(.+?)" >(.+?)</a></li><li>',re.DOTALL).findall(str(SelectOut))
        for url,name in match:
                name = CLEAN(name)
                searcher = url.replace('/','')
                AddDir(name,url,80,ZeusPNG,background=GetCompile('TVBackground'))
				
        SetViewList()
		
def TVGETSHOWS(url):
    SeasonPage = ZeusGetContent(GetCompile('TV1')+url)
    if '<h1>Latest Added</h1>' in SeasonPage:
        SeasonPage = regex_from_to(SeasonPage, '<div class="home">', '<div align="center" class="foot">')
        match=re.compile('<a href="/(.+?)">(.+?)</a>').findall(str(SeasonPage))
    elif '<h1>Most Popular</h1>' in SeasonPage:
        SeasonPage = regex_from_to(SeasonPage, '<div class="home">', '<div align="center" class="foot">')
        match=re.compile('<a href="/(.+?)">(.+?)</a>').findall(str(SeasonPage))
    elif '<h1>Genres</h1>' in SeasonPage:
        SeasonPage = regex_from_to(SeasonPage, '<div class="home">', '<div align="center" class="foot">')
        match=re.compile('<a href="/(.+?)">(.+?)</a>').findall(str(SeasonPage))
		
    AddInfoLink()
    for url,name in match:
        AddDir(name,url,87,ZeusPNG,background=GetCompile('TVBackground'))
	
    SetViewList()

def GETTVSOURCES(name,url):
    SelectOut = ZeusGetContent(GetCompile('TV1')+url)
    SelectOut = RemoveBitsMovie(SelectOut)
    SelectOut = regex_from_to(SelectOut, '<div id="linkname">', '</table>')
    all_genres = regex_get_all(SelectOut, '<ul id="linkname_nav">', '</a></li>')
    AddInfoLink()
    List=[]; ListU=[]; c=0
    for a in all_genres:
        url = regex_from_to(a, 'http://' , ';')
        url = url.replace("')","")
        Source = regex_from_to(a, ';">', '</a></li>').lstrip()
        c=c+1; List.append('Zeus Link ['+str(c)+'] '+ Source); ListU.append(url)
        
    dialog=xbmcgui.Dialog()
    rNo=dialog.select('Zeus Select A Source', List)
    if rNo>=0:
        rName=List[rNo]
        rURL=str("http://"+ListU[rNo])
        AddDir('[COLOR yellow]Replay '+name+'[/COLOR]',str(rURL),68,ZeusPNG,background=GetCompile('TVBackground'),isFolder=False)
        STREAMTV(name,rURL,ZeusPNG)
    else:
        pass
	
def STREAMTV(name,url3,thumb):
    url = url3
    try:
        req = urllib2.Request(url3)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        url = url3				
        streamlink = urlresolver.resolve(urllib2.urlopen(req).url)
        liz=xbmcgui.ListItem(name, iconImage=iconimage,thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": name } )
#xbmc.Player().play(streamlink, liz)
#        addLinkMovies(name,streamlink,thumb)
        StreamTVPlay(name,streamlink,thumb)
    except:
        if len(url3) > 0:
             Notify('small','Sorry Link Removed:', 'Please try another one.',9000)
			 
def StreamTVPlay(name,streamlink,thumb):
        ok=True
        try: addon.resolve_url(streamlink)
        except: pass
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo('Video', infoLabels={ "Title": name } )
        contextMenuItems = []
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        xbmc.Player().play(streamlink, liz)
 #       ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)

#hakamac		
def GetBestMovieURL(url):
    LinkData = ''
    try:
       LinkData = net.http_GET(GetCompile('MOVIELINK1')+url).content
    except:
        LinkData = net.http_GET(GetCompile('MOVIELINK2')+url).content

    return LinkData


def GetCompile(data):
    ReturnString = regex_from_to(CompileData, data+'####', '####')
    return ReturnString

def SearchMovies():
    SearchEntered = SearchBox()
    GetMovies('search/search.php?q='+SearchEntered)
	
def GetMovies(url):
    AddInfoLink()
    
    PagePos = url.rfind('/')
    ThisPageNo = url[PagePos+1:]
    if 'search' not in ThisPageNo:
        StripTop = '<center><div class="content-box">'
        NextPageNo = int(ThisPageNo) + 1
        if ThisPageNo > 1:
            NextPage = url.replace('/'+str(ThisPageNo),'/'+str(NextPageNo))
    else:
        StripTop = 'Search Results For: "<font'
        NextPage = url + '/2'
		
    PageSource = GetBestMovieURL(url)
    PageSource = regex_from_to(PageSource, StripTop, '<div class="footer-box">') 
    PageSource = RemoveBitsMovie(PageSource)
    all_videos = regex_get_all(PageSource, '<td width="20%"', 'alt="')
    Count=0
    for a in all_videos:
        vurl = regex_from_to(a, '<a href="', '"')
        
        title = regex_from_to(a, 'title="', '"')
        title = title.encode('utf-8')
        iconimage = regex_from_to(a, '<img src="', '"')
        AddDir(title,vurl,710,iconimage,isFolder=True)
        Count=Count+1

    if Count == 25:
        AddDir('[B][COLOR white]Next Page[/COLOR][/B]', NextPage ,700,'http://s6.postimg.org/4bbyeq1ep/next.png')		
 
    SetViewThumbnail()
	
	
def GetMovieLinks(url):
    PageSource = ZeusGetContent(url)
    iconimage = regex_from_to(PageSource, '<meta property="og:image" content="', '"')  
    PageSource = regex_from_to(PageSource, 'Alternative Versions</h2>', 'Write a comment:') 
    AddInfoLink()	
    c=0
    all_videos = regex_get_all(PageSource, '<td class="entry">', '<td class="entry2"')
    for a in all_videos:
        vurl = regex_from_to(a, 'href="', '"')
        title = regex_from_to(a, '</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;', '</td>')
        title = title.encode('utf-8')
        if title <> ' Thevideos':
           c=c+1
           AddDir('[COLOR yellow]' + str(c)+':[/COLOR] [COLOR white]'+title+'[/COLOR]',vurl,3,iconimage,isFolder=False)
		
    SetViewList()
	
	
def RemoveBitsMovie(data):
    data = data.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('[','').replace(']','')
    return data


def GETGENRES(url):
    GenresPage = ZeusGetContent(url)
    GenresPage = regex_from_to(GenresPage, '<div class="tv_letter_nav"><ul>', '<div class="tv_all">')
    GenresPage = RemoveBitsMovie(GenresPage)
    match=re.compile("<a href=/(.+?)>(.+?)</a>",re.DOTALL).findall(str(GenresPage))
		
    AddInfoLink()
    for url,name in match:
        name = CLEAN(name)
        LetterBit = name[:1].upper()
        AddDir(name,url,83,"http://icons.iconarchive.com/icons/hydrattz/multipurpose-alphabet/256/Letter-"+LetterBit+"-blue-icon.png")

		
def ATOZ(url):
    AtoZPage = ZeusGetContent(GetCompile('TV1')+url)
    AtoZPage = regex_from_to(AtoZPage, '<a href="/tv-listings/0-9">0-9</a>', '<div class="home">')
    AtoZPage = RemoveBitsMovie(AtoZPage)
    match=re.compile('<a href="/(.+?)">(.+?)</a>',re.DOTALL).findall(str(AtoZPage))
    AddInfoLink()
    AddDir("Number 0-9","tv-listings/0-9",83,ZeusGraphic)
    for url,name in match:
        name = CLEAN(name)
        LetterBit = name[:1].upper()
        AddDir(name,url,83,"http://icons.iconarchive.com/icons/hydrattz/multipurpose-alphabet/256/Letter-"+LetterBit+"-blue-icon.png")
    SetViewThumbnail()
		
def GETATOZLIST(name,url):
    ATOZLIST = ZeusGetContent(GetCompile('TV1')+url)
    ATOZLIST = regex_from_to(ATOZLIST, '<div class="home">', '</div>')
    ATOZLIST = RemoveBitsMovie(ATOZLIST)
    match=re.compile('<a href="/(.+?)">(.+?)</a>',re.DOTALL).findall(ATOZLIST)
    dp = xbmcgui.DialogProgress()

    totalLinks = len(match)
    loadedLinks = 0
    dp.create('UPDATING ZEUS')
   
    AddInfoLink()
    for url,name in match:
        AddDir(name,url,84,ZeusGraphic)
        loadedLinks = loadedLinks + 1
        percent = (loadedLinks * 100)/totalLinks
        dp.update(percent)
    dp.update(100)
    dp.close()
    
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
	
    SetViewList()
			 
def GETATOZSEASON(name,url):
    SeasonPage = ZeusGetContent(GetCompile('TV1')+url)
    SeasonPage = regex_from_to(SeasonPage, 'target="_blank">IMDB</a><br/>', '<div class="addthis">') 
    SeasonPage = RemoveBitsMovie(SeasonPage)
    match=re.compile("<h3><a href='/(.+?)'>(.+?)</a></h3>",re.DOTALL).findall(str(SeasonPage))
    AddInfoLink()
    for url,name in match:
        AddDir(name,url,85,ZeusGraphic)
			 
def GETATOZEPISODE(name,url):
    EpisodePage = ZeusGetContent(GetCompile('TV1')+url)
    EpisodePage = regex_from_to(EpisodePage, 'target="_blank">IMDB</a><br/>', '<div class="addthis">') 
    EpisodePage = RemoveBitsMovie(EpisodePage)
    match=re.compile("<a href='/(.+?)'><strong>(.+?)</strong>(.+?)</a></li><li>",re.DOTALL).findall(str(EpisodePage))
    AddInfoLink()
    for url,Blank1,name in match:
         AddDir(name,url,81,ZeusGraphic)
      
def addLinkMovies(name,url,iconimage):
        download_enabled = 'False'
        ok=True
        try: addon.resolve_url(streamlink)
        except: pass
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo('Video', infoLabels={ "Title": name } )
        contextMenuItems = []
        if download_enabled == 'true':
                contextMenuItems = []
                contextMenuItems.append(('Download', 'XBMC.RunPlugin(%s?mode=9&name=%s&url=%s)' % (sys.argv[0], name, urllib.quote_plus(url))))
                liz.addContextMenuItems(contextMenuItems, replaceItems=True)

        liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        return ok
		
						   
def Notify(typeq,title,message,times, line2='', line3=''):
     if typeq == 'small':
            smallicon= "http://s6.postimg.org/mhl2gyyld/homepage.png"
            xbmc.executebuiltin("XBMC.Notification("+title+","+message+","''","+smallicon+")")
     elif typeq == 'big':
            dialog = xbmcgui.Dialog()
            dialog.ok(' '+title+' ', ' '+message+' ', line2, line3)
     else:
            dialog = xbmcgui.Dialog()
            dialog.ok(' '+title+' ', ' '+message+' ')

def OPEN_MAGIC(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent' , "Magic Browser")
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
	
def CLEAN(name):
        name = name.replace('&amp;','&')
        name = name.replace('&#x27;',"'")
        urllib.quote(u'\xe9'.encode('UTF-8'))
        name = name.replace(u'\xe9','e')
        urllib.quote(u'\xfa'.encode('UTF-8'))
        name = name.replace(u'\xfa','u')
        urllib.quote(u'\xed'.encode('UTF-8'))
        name = name.replace(u'\xed','i')
        urllib.quote(u'\xe4'.encode('UTF-8'))
        name = name.replace(u'\xe4','a')
        urllib.quote(u'\xf4'.encode('UTF-8'))
        name = name.replace(u'\xf4','o')
        urllib.quote(u'\u2013'.encode('UTF-8'))
        name = name.replace(u'\u2013','-')
        urllib.quote(u'\xe0'.encode('UTF-8'))
        name = name.replace(u'\xe0','a')
        try: name=messupText(name,True,True)
        except: pass
        try:name = name.decode('UTF-8').encode('UTF-8','ignore')
        except: pass
        name=name.replace('\u00a0',' ').replace('\u00ae','').replace('\u00e9','').replace('\u00e0','').replace('\u2013','').replace('\u00e7','').replace('\u00f1','').replace("&amp;","&").replace('&quot;','"').replace('<a href="','').replace('</a>&#8220;#','"')
        name=name.replace('&lt;','<').replace('&gt;','>').replace('<name>','<title>').replace('</name>','</title>').replace('</p>','\r\n').replace('&nbsp;','').replace('&#8221;','"').replace('&#8243;','"').replace('<!-- EVO LINK','\n').replace('END EVO -->','').replace('<p>','').replace('&#038;','&').replace('&#8211;','--').replace('<br />','').replace('&#215;','x')
	
        return name

def PlxCategory(url):
	tmpList = []
	list = common.plx2list(url)
	background = list[0]["background"]
	for channel in list[1:]:
		iconimage = "" if not channel.has_key("thumb") else common.GetEncodeString(channel["thumb"])
		name = common.GetEncodeString(channel["name"])
		if channel["type"] == 'playlist':
			AddDir("[COLOR blue][{0}][/COLOR]".format(name) ,channel["url"], 1, iconimage, background=background)
		else:
			AddDir(name, channel["url"], 3, iconimage, isFolder=False, background=background)
			tmpList.append({"url": channel["url"], "image": iconimage, "name": name.decode("utf-8")})
			
	common.SaveList(tmpListFile, tmpList)
			
		
def AddDir(name, url, mode, iconimage, description='', isFolder=True, background=None):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)

    if background == None:
       background=iconimage
	
    liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": description})
    liz.setProperty('fanart_image', background)
    if mode == 1 or mode == 2:
       liz.addContextMenuItems(items = [('{0}'.format(localizedString(10008).encode('utf-8')), 'XBMC.RunPlugin({0}?url={1}&mode=22)'.format(sys.argv[0], urllib.quote_plus(url)))])
    elif mode == 3:
        liz.setProperty('IsPlayable', 'true')
        liz.addContextMenuItems(items = [('{0}'.format(localizedString(10009).encode('utf-8')), 'XBMC.RunPlugin({0}?url={1}&mode=31&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), iconimage, name))])
    elif mode == 32:
        liz.setProperty('IsPlayable', 'true')
        liz.addContextMenuItems(items = [('{0}'.format(localizedString(10010).encode('utf-8')), 'XBMC.RunPlugin({0}?url={1}&mode=33&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), iconimage, name))])
		
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=isFolder)

def GetKeyboardText(title = "", defaultText = ""):
	keyboard = xbmc.Keyboard(defaultText, title)
	keyboard.doModal()
	text =  "" if not keyboard.isConfirmed() else keyboard.getText()
	return text

def GetSourceLocation(title, list):
	dialog = xbmcgui.Dialog()
	answer = dialog.select(title, list)
	return answer
	
def AddFavorites(url, iconimage, name):
	favList = common.ReadList(favoritesFile)
	for item in favList:
		if item["url"].lower() == url.lower():
			xbmc.executebuiltin("Notification({0}, '{1}' {2}, 5000, {3})".format(AddonName, name, localizedString(10011).encode('utf-8'), icon))
			return
    
	list = common.ReadList(tmpListFile)	
	for channel in list:
		if channel["name"].lower() == name.lower():
			url = channel["url"]
			iconimage = channel["image"]
			break
			
	if not iconimage:
		iconimage = ""
		
	data = {"url": url, "image": iconimage, "name": name.decode("utf-8")}
	
	favList.append(data)
	common.SaveList(favoritesFile, favList)
	xbmc.executebuiltin("Notification({0}, '{1}' {2}, 5000, {3})".format(AddonName, name, localizedString(10012).encode('utf-8'), icon))

def Freeview_Groups():
#A Big thanks to Kinkin for his code to help me do this
    dp = xbmcgui.DialogProgress()
    dp.create('ZEUS VIDEO Logging in to Server')
    Freeview_Get_Session()
    session_id = xbmcgui.Window(10000).getProperty("session_id")
    url = "%s%s%s" % (Freeview_url,'/tv/api/groups?session_key=', (session_id))
    link = Freeview_OPEN_URL(url)
    all_groups = regex_get_all(link, '{', '_count')
    for groups in all_groups:
        description=regex_from_to(groups,'channels":',',"channels').replace('[','').replace(']','').replace('"','')
        name = regex_from_to(groups, 'title":"', '",')
        iconimage = regex_from_to(groups, 'logo_148x148_uri":"', '",').replace('\\', '')
        url = regex_from_to(groups, 'group_id":"', '",')
        AddDir('[COLOR gold]'+name+'[/COLOR]',url, 310, iconimage, description, isFolder=True)
    
    dp.close()
    SetViewThumbnail()			
	
	
def Freeview_List(name,url,description):
    channels = description
    title = ''
    name_lst = []
    session_id = xbmcgui.Window(10000).getProperty("session_id")
    url = "%s%s%s%s%s" % (Freeview_url, 'api/group/', url, '?session_key=', session_id)
    link = Freeview_GET_URL(url).translate(trans_table)
    link=cleanlink(link)

    data=json.loads(link)
    channels=data['channels']
    for c in channels:
        channel_id=c['id']
        title=c['title']
        description=c['description']
        name_lst.append(title)
#        title="%s (%s)" % (title,channel_id)
        icon = 'http://static.filmon.com/couch/channels/%s/extra_big_logo.png' % channel_id
        AddDir('[COLOR gold]'+title+'[/COLOR]',str(channel_id), 320, icon,isFolder=False)

    SetViewThumbnail()
	
def Freeview_Play(name,url,iconimage):
    ChannelName = name
    dp = xbmcgui.DialogProgress()
    dp.create('Opening ' + name.upper())
    session_id = xbmcgui.Window(10000).getProperty("session_id")
    url = "%s%s%s%s%s" % (Freeview_url, 'api/channel/', url, '?session_key=', session_id)
    utc_now = datetime.datetime.now()
    channel_name=name.upper()
    try:
        link = Freeview_OPEN_URL(url)
    except:
        return
    p_name = name
    n_p_name = ""


    Method = 1
    streams = re.compile('"id":(.+?),"quality":"high","url":"(.+?)","name":"(.+?)","is_adaptive":"(.+?)","watch-timeout":(.+?)}').findall(link)
    if len(streams) < 1:
       streams = re.compile('"id":(.+?),"quality":"low","url":"(.+?)","name":"(.+?)","is_adaptive":"(.+?)","watch-timeout":(.+?)}').findall(link)
    
    if len(streams) < 1:
       Method = 2
       streams = re.compile('"id":(.+?),"quality":"high","url":"(.+?)""name":"(.+?)","is_adaptive":(.+?),"watch-timeout":"(.+?)"}').findall(link)
    if len(streams) < 1:
       Method = 2
       streams = re.compile('"id":(.+?),"quality":"low","url":"(.+?)","name":"(.+?)","is_adaptive":(.+?),"watch-timeout":(.+?)}').findall(link)
	   
    if len(streams) < 1:
	   return
    app = ''

    if Method == 1:
        for id,url,name,adaptive,wt in streams:
            url = url.replace("\/", "/")
            name = name
            id=id
            if name.endswith('m4v'):
                app = 'vodlast'
            else:
                app='live/?id=' + url.split('=')[1]
        swapout_url = regex_from_to(url,'rtmp://','/')
        STurl = str(url) + ' playpath=' + name + ' app=' + app + ' swfUrl=http://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf' + ' tcUrl=' + url + ' pageUrl=http://www.filmon.com/' + ' live=1 timeout=45 swfVfy=1'
    else:
        for id,url,name,adaptive,wt in streams:
            url = url.replace("\/", "/")
        swapout_url = regex_from_to(url,'rtmp://','/')
        STurl = str(url) + '/' + str(name)
    dp.update(75)	
    playlist = xbmc.PlayList(1)
    playlist.clear()
    listitem = xbmcgui.ListItem(ChannelName, iconImage=iconimage, thumbnailImage=iconimage)
    listitem.setInfo("Video", {"Title":ChannelName})
    listitem.setProperty('mimetype', 'video/x-msvideo')
    listitem.setProperty('IsPlayable', 'true')
    playlist.add(STurl,listitem)
    xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
    xbmcPlayer.play(playlist)
		
    dp.close()
	
	
def Freeview_OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
	
def Freeview_GET_URL(url):
    header_dict = {}
    header_dict['Accept'] = 'application/json, text/javascript, */*; q=0.01'
    header_dict['User-Agent'] = 'User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
    req = net.http_GET(url, headers=header_dict).content
    return req
	
def Freeview_Get_Session():
    try:
        session_id = xbmcgui.Window(10000).getProperty("session_id")
        url = "%s%s%s" % (Freeview_url,'/tv/api/groups?session_key=',(session_id))
        link = Freeview_OPEN_URL(url)
    except:
        xbmcgui.Window(10000).setProperty("session_id", '')
    if not xbmcgui.Window(10000).getProperty("session_id"):
        link = Freeview_OPEN_URL(session_url)
        match= re.compile('"session_key":"(.+?)"').findall(link)
        session_id=match[0]
        print "FilmOn.TV......Not logged in"
        xbmcgui.Window(10000).setProperty("session_id", session_id)
        Freeview_keep_session()
            
#    FILMON_SESSION = xbmcgui.Window(10000).getProperty("session_id")

def Freeview_keep_session():
    currentWindow = xbmcgui.getCurrentWindowId()
    session_id = xbmcgui.Window(10000).getProperty("session_id")
    url = "http://www.filmon.com/api/keep-alive?session_key=%s" % (session_id)
    Freeview_GET_URL(url)
    tloop = Timer(60.0, Freeview_keep_session)
    tloop.start()

def ResolveIT():
    InfoLabel = xbmc.getInfoLabel('Container.PluginName')
    print 'Label Hakamac >> ' + InfoLabel + '   ' + InfoLabel[-4:]
#    if InfoLabel[-2:] == 'us' or InfoLabel[-4:] == 'cbox':
    return 1
#    else:
#       return 0
	   
def cleanlink(link):
    data=link.replace('\u00a0',' ').replace('\u00ae','').replace('\u00e9','').replace('\u00e0','').replace('\u2013','').replace('\u00e7','').replace('\u00f1','')#
	
    return data

def x1Channels():
    url = "http://mobile.desistreams.tv/DesiStreams/index2.php?tag=get_all_channel"
    AddInfoLink()
    try: 
        links = net.http_GET(url).content
    except:
        AddDir('[COLOR red]SECTION UNDER MAINTENANCE PLEASE TRY AGAIN SHORTLY[/COLOR]','BLANK',999,'http://s5.postimg.org/sp2sjkbxj/underconstruction.png')
        AddDir('[COLOR yellow]GO TO http://zeusrepo.com   FOR MORE INFORMATION[/COLOR]','BLANK',999,'http://s5.postimg.org/sp2sjkbxj/underconstruction.png')
        SetViewList()
        return

    AddDir('[COLOR gold]** LINKS NOT WORKING? RELOAD THE LIST **[/COLOR]','Findus',0,ZeusGraphic)
    AddDir('[COLOR gold]** LINKS HERE CANNOT BE USED IN FAVOURITES **[/COLOR]','Findus',0,ZeusGraphic)
	
    links = links.replace('\/','/')
    Mainurl = 'http://mobile.desistreams.tv/'
    
    all_videos = regex_get_all(links, '{"id"', '}')
    for a in all_videos:
        mode = 3
        url = regex_from_to(a, '"stream_url":"', '"')
        name = regex_from_to(a, 'name":"', '"')
        icon = regex_from_to(a, '"img":"', '",')
        AddDir('[COLOR blue] '+name+' [/COLOR] Source 1' ,url, mode, Mainurl+icon, isFolder=False)
        url = regex_from_to(a, '"stream_url2":"', '"')
        name = regex_from_to(a, 'name":"', '"')
        icon = regex_from_to(a, '"img":"', '",')
        AddDir('[COLOR blue] '+name+'[/COLOR] Source 2' ,url, mode, Mainurl+icon, isFolder=False)
        url = regex_from_to(a, '"stream_url3":"', '"')
        name = regex_from_to(a, 'name":"', '"')
        icon = regex_from_to(a, '"img":"', '",')
        AddDir('[COLOR blue] '+name+'[/COLOR] Source 3' ,url, mode, Mainurl+icon, isFolder=False)
    
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
    SetViewList()
	
	
def ReportFaultDiag():
    xbmcgui.Dialog().ok('Zeus Video Support', 'For reporting faults, suggestions, general support',' ', 'or donations go to http://zeus.video')
	
def UpdateMe():
    dp = xbmcgui.DialogProgress()
    dp.create('UPDATING ZEUS VIDEO')
    dp.update(0)
    UpdateLinks = ZeusGetContent('http://zeus.video/updates/upgradezeus.php')
    if 'UPDATELIST' not in UpdateLinks:
       return
	   
    all_links = regex_get_all(UpdateLinks, 'I:', '"#')
    for a in all_links:
        dp.update(int(regex_from_to(a, 'I:"', '"')))
        Type = regex_from_to(a, 'A:"', '"')
        LocalFileName = regex_from_to(a, 'B:"', '"')
        url = regex_from_to(a, 'C:"', '"')
        if 'addonDir' in Type:
             localfile = os.path.join(addonDir,LocalFileName)
             urllib.urlretrieve(url,localfile)
        elif 'libDir' in Type:
             localfile = os.path.join(libDir,LocalFileName)
             urllib.urlretrieve(url,localfile)		

    import repobuild
    repobuild.UpdateRepo()
    #LookLocoNum()
    xbmc.executebuiltin("UpdateLocalAddons")
    xbmc.executebuiltin("UpdateAddonRepos")
    dp.update(100)       
    dp.close()
           
    xbmcgui.Dialog().ok('Zeus Video Updated', 'A reboot may be required. ', 'If you want the Zeus Project to continue', 'Donate as little as $2 at http://zeus.video')
	
def RemoveFavorties(url):
	list = common.ReadList(favoritesFile) 
	for channel in list:
		if channel["url"].lower() == url.lower():
			list.remove(channel)
			break
			
	common.SaveList(favoritesFile, list)
	xbmc.executebuiltin("XBMC.Container.Refresh()")

def YouTubeCode(url):
    try:
        url = "PlayMedia(plugin://plugin.video.youtube/?action=play_video&videoid="+url+")"
        xbmc.executebuiltin(url)
    except:
        xbmc.executebuiltin("XBMC.Notification(ZEUS VIDEO,This host is not supported or resolver is broken::,10000)")

def m3uCategory(url):
    url = Raw + url
    list = m3u2list(url)
    AddInfoLink()
    for channel in list:
		name = common.GetEncodeString(channel["display_name"])
		mode = 46 if channel["url"].find("youtube") > 0 else 3
		AddDir(name ,channel["url"], mode, ZeusGraphic, isFolder=False)

    SetViewList()

def ListFavorites():
    AddDir('[B][COLOR yellow]YOUR FAVOURITES LIST[/COLOR][/B]','BLANK',999,FavGraphic)	
    AddDir("[COLOR yellow][B]{0}[/B][/COLOR]".format(localizedString(10013).encode('utf-8')), "favorites" ,34 ,os.path.join(addonDir, "resources", "images", "bright_yellow_star.png"), isFolder=False)
    list = common.ReadList(favoritesFile)
    for channel in list:
		name = channel["name"].encode("utf-8")
		iconimage = channel["image"].encode("utf-8")
		AddDir(name, channel["url"], 32, iconimage, isFolder=False) 

	
						
def AddNewFavortie():
	chName = GetKeyboardText("{0}".format(localizedString(10014).encode('utf-8'))).strip()
	if len(chName) < 1:
		return
	chUrl = GetKeyboardText("{0}".format(localizedString(10015).encode('utf-8'))).strip()
	if len(chUrl) < 1:
		return
		
	favList = common.ReadList(favoritesFile)
	for item in favList:
		if item["url"].lower() == url.lower():
			xbmc.executebuiltin("Notification({0}, '{1}' {2}, 5000, {3})".format(AddonName, chName, localizedString(10011).encode('utf-8'), icon))
			return
			
	data = {"url": chUrl, "image": "", "name": chName.decode("utf-8")}
	
	favList.append(data)
	if common.SaveList(favoritesFile, favList):
		xbmc.executebuiltin("XBMC.Container.Update('plugin://{0}?mode=30&url=favorites')".format(AddonID))

def PlayUrl(name, url, iconimage=None):
	listitem = xbmcgui.ListItem(path=url, thumbnailImage=iconimage)
	listitem.setInfo(type="Video", infoLabels={ "Title": name })
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
	
def PlayURLResolver(name,url,iconimage):
    import commonresolvers
    resolved = commonresolvers.get(url).result
    if resolved:
        if isinstance(resolved,list):
            for k in resolved:
                quality = 'HD'
                if k['quality'] == 'HD'  :
                    resolver = k['url']
                    break
                elif k['quality'] == 'SD' :
                    resolver = k['url']        
                elif k['quality'] == '1080p' and addon.getSetting('1080pquality') == 'true' :
                    resolver = k['url']
                    break
        else:
            resolver = resolved       
        playsetresolved(resolver,name,iconimage)
    else: 
        xbmc.executebuiltin("XBMC.Notification(ZEUS VIDEO,This host is not supported or resolver is broken::,10000)")  
 
def playsetresolved(url,name,iconimage):
    if 'channel.php' in url:
        if ResolveIT() == 1:
            url = url + '&hash='
            url = url + GetCompile('HASHx14')
    url = url.replace('channel.php','channelx14.php') 
    liz = xbmcgui.ListItem(name, iconImage=iconimage)
    liz.setInfo(type='Video', infoLabels={'Title':name})
    liz.setProperty("IsPlayable","true")
    liz.setPath(url)
    
    try:
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    except:
        pass

     
    if '[COLOR lime]' in name and 'channel.php' not in url:
        name = name.replace("[COLOR lime]","").replace("[/COLOR]","")
        xbmc.sleep(20000)
        if xbmc.Player().isPlaying():
           Popit = 'alpha/chin-chan.php?zeusn=' + urllib.quote_plus(name) + '&zeusl=' + urllib.quote_plus(url)
           ZeusGetContent(ZeusLink + Popit)
        else:
           Popit = 'alpha/chin-chandown.php?zeusn=' + urllib.quote_plus(name) + '&zeusl=' + urllib.quote_plus(url)
           ZeusGetContent(ZeusLink + Popit)

	
def regex_from_to(text, from_string, to_string, excluding=True):
    if excluding:
	   try: r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
	   except: r = ''
    else:
       try: r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
       except: r = ''
    return r

def regex_get_all(text, start_with, end_with):
    r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
    return r

#hakamac thanks Roman_V_M
def SetViewThumbnail():
    skin_used = xbmc.getSkinDir()
    if skin_used == 'skin.confluence':
        xbmc.executebuiltin('Container.SetViewMode(500)')
    elif skin_used == 'skin.aeon.nox':
        xbmc.executebuiltin('Container.SetViewMode(511)') 
    else:
        xbmc.executebuiltin('Container.SetViewMode(500)')
   
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def SetViewList():
    xbmc.executebuiltin("Container.SetViewMode(50)")
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def setView(content, viewType):
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)

    xbmc.executebuiltin("Container.SetViewMode(true)")	

def get_params():
	param = []
	paramstring = sys.argv[2]
	if len(paramstring) >= 2:
		params = sys.argv[2]
		cleanedparams = params.replace('?','')
		if (params[len(params)-1] == '/'):
			params = params[0:len(params)-2]
		pairsofparams = cleanedparams.split('&')
		param = {}
		for i in range(len(pairsofparams)):
			splitparams = {}
			splitparams = pairsofparams[i].split('=')
			if (len(splitparams)) == 2:
				param[splitparams[0].lower()] = splitparams[1]
	return param

	
params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None
channels=None

try:
	url = urllib.unquote_plus(params["url"])
except:
	pass
try:
	name = urllib.unquote_plus(params["name"])
except:
	pass
try:
	iconimage = urllib.unquote_plus(params["iconimage"])
except:
	pass
try:        
	mode = int(params["mode"])
except:
	pass
try:        
	description = urllib.unquote_plus(params["description"])
except:
	pass

params=get_params(); url=None; name=None; mode=None; site=None; iconimage=None
try: site=urllib.unquote_plus(params["site"])
except: pass
try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try: channels=urllib.unquote_plus(params["channels"])
except: pass


	
if mode == None or len(AddonID) <> 17 or url == None or len(url) < 1 or mode == 99:
	Categories()
elif mode == 1:
	PlxCategory(url)
elif mode == 2:
    XMLRead500(url)
elif mode == 3 or mode == 32:
     PlayURLResolver(name,url,iconimage)
elif mode == 6:	
	StreamsList(url)
elif mode == 7:	
	LockedIndex(url)
elif mode == 9:
	UFCSection(url)
elif mode == 11:
	YouTube_List(url)
elif mode == 12:
    PlayURLResolver(name,url,iconimage)
elif mode == 14:
    PlayUrl(name, url, iconimage)
elif mode == 15:
	UFCScrape(url)
elif mode == 16:
	StreamUFC(name,url,iconimage)
elif mode == 20:
	XMLRead500(url)
elif mode == 30:
	ListFavorites()
elif mode == 31: 
	AddFavorites(url, iconimage, name) 
elif mode == 33:
	RemoveFavorties(url)
elif mode == 34:
	AddNewFavortie()
elif mode == 35:
    x1Channels()
elif mode == 37:	
    Stream247(url)
elif mode == 38:	
    Stream247_Links(name,url,iconimage)
elif mode == 40:	
	ReadUrl(url)
elif mode == 41:
	common.DelFile(favoritesFile)
elif mode == 45:	
	TV()
elif mode == 50:
    UpdateMe()
    sys.exit()
elif mode == 58:
	SearchChannel(url)
elif mode == 59:
	Channel_Scraper(url)
elif mode == 60 or mode == 46:	
    PlayYoutubeView(url)
elif mode == 61:
    PlayVimeo(url)
elif mode == 66:	
	VIDEOLINKS(name,url,iconimage)
elif mode == 68:
    STREAMTV(name,url,iconimage)
elif mode == 75:	
	TVLatestAdded(url)
elif mode == 76:	
	NEWLINKS(url)
elif mode == 77:	
	NEWEPISODESTV(url)
elif mode == 78:	
	SEARCHTV(url)
elif mode == 80:	
	TVGETSHOWS(url)
elif mode == 81:	
	GETTVSOURCES(name,url)
elif mode == 82:	
	ATOZ(url)
elif mode == 83:
	GETATOZLIST(name,url)
elif mode == 84:	
	GETATOZSEASON(name,url)
elif mode == 85:
	GETATOZEPISODE(name,url)
elif mode == 86:
	GETGENRES(url)
elif mode == 87:
	GetSeasons(url)
elif mode == 88:
	TVGetSeasonLinks(url)
elif mode == 98:
    sys.exit()
elif mode == 151:
	FullMatches(url)
elif mode == 152:
	REPLAYSGETLINKS(name,url)
elif mode == 153:
	NEXTPAGE(page)
elif mode == 154: 
	SearchReplays()
elif mode == 120:
    PLAYSTREAM(name,url,iconimage)
elif mode == 200: 	
	YouTube_List(url)
elif mode == 210: 	
	YouTubeCode(url)
elif mode == 220:	
    Hybrid_List(url)
elif mode == 230:	
    VodlockerxScrape(url)
elif mode == 240:	
	VodlockerxSources(name,url,iconimage)
elif mode == 250:
	SearchVodlockerx()
elif mode == 300:
    Freeview_Groups()
elif mode == 310:
    Freeview_List(name,url,description)
elif mode == 320:	
    Freeview_Play(name,url,iconimage)
elif mode == 400:	
	ChildLock()
elif mode == 500:
    EVO_Link()
elif mode == 510:
    EVO_Private()
elif mode == 520:
    StreamM3U(url)
elif mode == 550:
    EuropaHome(url)
elif mode == 560:
    EuropaList(url)
elif mode == 580:
    SearchEuropa()
elif mode == 600:
    Xham_Cats(url)
elif mode == 610:	
	Xham_FindLinks(url)
elif mode == 620:
    StreamLive(url)
elif mode == 630:
    StreamLiveLink(name,url,iconimage)
elif mode == 700:	
	GetMovies(url)
elif mode == 710:	
	GetMovieLinks(url)	
elif mode == 720:		
	SearchMovies()
elif mode == 800:	
	Navi_Playlist(url)
elif mode == 810:	
	LaLineaLista(url)
elif mode == 900:
	ReportFaultDiag()

xbmcplugin.endOfDirectory(int(sys.argv[1]))	



	
	

# h@k@M@c Code