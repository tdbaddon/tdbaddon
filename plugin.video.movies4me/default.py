'''
kinkin
'''

import urllib,urllib2,re,xbmcaddon,xbmcplugin,xbmcgui,os
import settings
import time,datetime
from datetime import date, timedelta
from threading import Timer
from helpers import clean_file_name
from hashlib import md5
import hashlib
import json
import glob
import shutil
from threading import Thread
from t0mm0.common.net import Net
from helpers import clean_file_name
net = Net()
from metahandler import metahandlers
metainfo = metahandlers.MetaData()


ADDON = settings.addon()
FAV = settings.favourites_file()
QUALITY = settings.quality()
ENABLE_META = settings.enable_meta()
MOVIE_PATH = settings.movie_directory()
TRAILER_RESTRICT = settings.restrict_trailer()
TRAILER_QUALITY = settings.trailer_quality()
TRAILER_ONECLICK = settings.trailer_one_click()
CACHE_PATH = settings.cache_path()
addon_path = os.path.join(xbmc.translatePath('special://home/addons'), '')
fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.movies4me', 'fanart.jpg'))
iconart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.movies4me', 'icon.png'))
base_url = 'http://www.hdmoviezone.net/'
trans_table = ''.join( [chr(i) for i in range(128)] + [' '] * 128 )


def open_url(url, cache_time=3600):
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Linux; <Android Version>; <Build Tag etc.>) AppleWebKit/<WebKit Rev>(KHTML, like Gecko) Chrome/<Chrome Rev> Safari/<WebKit Rev>')
    h = hashlib.md5(url).hexdigest()
    cache_file = os.path.join(CACHE_PATH, h)
    age = get_file_age(cache_file)
    print "Movies4ME.........FILE AGE IS " + str(age)
    if age > 0 and age < cache_time:
        r = read_from_file(cache_file, silent=True)
        print "Movies4ME.........use CACHE"
        if r:
            return r
    else:
        response = urllib2.urlopen(req)
        link=response.read()
        write_to_file(cache_file, link)
        print "Movies4ME.........NO CACHE"
        response.close()
        return link
		
def open_az_url(url,cache_time=3600):
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Linux; <Android Version>; <Build Tag etc.>) AppleWebKit/<WebKit Rev>(KHTML, like Gecko) Chrome/<Chrome Rev> Safari/<WebKit Rev>')
    req.add_header('Host','	www.google.com')
    h = hashlib.md5(url).hexdigest()
    cache_file = os.path.join(CACHE_PATH, h)
    age = get_file_age(cache_file)
    print "Movies4ME.........FILE AGE IS " + str(age)
    if age > 0 and age < cache_time:
        r = read_from_file(cache_file, silent=True)
        print "Movies4ME.........use CACHE"
        if r:
            return r
    else:
        response = urllib2.urlopen(req)
        link=response.read()
        write_to_file(cache_file, link)
        print "Movies4ME.........NO CACHE"
        response.close()
        return link
	
def get_file_age(file_path):
    try:    
        stat = os.stat(file_path)
        fileage = datetime.fromtimestamp(stat.st_mtime)
        now = datetime.now()
        delta = now - fileage
        return delta.seconds
    except:
        return -1
	
	
def CATEGORIES(name):
    addDir("Featured Movies", 'http://www.hdmoviezone.net/',11,iconart, '1','')
    addDir("Recent Movies", 'http://www.hdmoviezone.net/feed/?paged=',1,iconart, '1','')
    addDir("Movies by Genre", 'url',100,iconart, '','')
    addDir("Movies by Country", 'url',110,iconart, '','')
    addDir("Movies by Year", 'url',120,iconart, '','')
    addDir("A-Z", 'url',130,iconart, '','')
    addDir("Search", 'url',140,iconart, '','')
    addDir("Favourite Movies", 'url',9,iconart, '','')

def genres():
    header =  ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'War']
    for h in header:
        addDir(h, 'http://www.hdmoviezone.net/category/%s/feed/?paged=' % h,1,iconart, '1','')

def countries():
    header =  ['USA', 'UK', 'Australia', 'Canada', 'China', 'Denmark', 'Finland', 'France', 'Germany', 'Hong Kong', 'India', 'Italy', 'Japan', 'South Korea', 'Spain', 'Sweden', 'Thailand']
    for h in header:
        addDir(h, 'http://www.hdmoviezone.net/category/%s/feed/?paged=' % h,1,iconart, '1','')
	
def years():
    header =  ['2015', '2014', '2013', '2012', '2011', '2010', '2009', '2008', '2007', '2006', '2005', '2004', '2003', '2002', '2001', '2000', '1999']
    for h in header:
        addDir(h, 'http://www.hdmoviezone.net/category/%s/feed/?paged=' % h,1,iconart, '1','')
		
def a_z(url):#http://www.hdmoviezone.net/category/a/feed/?orderby=title&order=ASC&paged=2
    header =  ['09', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U','V', 'W', 'X', 'Y', 'Z']
    for h in header:
        addDir(h, 'http://www.hdmoviezone.net/category/%s/feed/?orderby=title&order=ASC&paged=' % h.lower(),1,iconart, '1','')

def all_movies(chname,url,start):
    dp = xbmcgui.DialogProgress()
    dp.create("Movies4ME",'Getting titles')
    dp.update(0)
    origurl = url
    if chname != 'search':
        #url = "%s%s%s" % (url,start,'&max-results=50')
        url = "%s%s" % (url.replace('/?paged=1',''),start)
        nextstart = int(start) + 1
    link = open_url(url).translate(trans_table)#.replace('\\"', '<>')#.replace('\\"', '<>')
    #print link
    if chname == 'search':
        all_data = regex_get_all(link, ',"title":{"type":"text', ']')
    else:
        all_data = regex_get_all(link, '<item>', '</item>')
    nItem = len(all_data)
    count = 0
    for a in all_data:
        try:
            title = regex_from_to(a, '<title>', '</title>')
            year = title[len(title)-5:-1]
            title1 = title[:-6].replace('&#8217',"'").rstrip()
        except:
            pass
        try:
            iconimage = regex_from_to(a, 'mediainfo" image="', '"').replace('\/', '/')
            file = regex_from_to(a, 'file="', '"')
        except:
            pass
        if 'HD Movie Zone - ' not in title:
            count = count + 1
            titlelist = str(count) + ' of ' + str(nItem) + ': ' + title
            progress = count / float(nItem) * 100               
            dp.update(int(progress), 'Adding title',titlelist)#;
            if dp.iscanceled():
                return
            if ENABLE_META:
                infoLabels = get_meta(title1.replace(' (Cam version)','').replace('\u0026','&'),'movie',year=year)
                if infoLabels['title']=='':
                    name=title
                else:
                    name=infoLabels['title'] + ' (' + str(infoLabels['year']) + ')'
                if infoLabels['cover_url']=='':
                    iconimage=iconimage
                else:
                    iconimage=infoLabels['cover_url']
            else:
                infoLabels =None
                iconimage=iconimage
                name = title
            addDirPlayable(title.replace('\u0026','&'),file,2,iconimage,title,infoLabels=infoLabels)
    if chname != 'search':
        addDir("Next Page >>", origurl,1,iconart, str(nextstart),'')
    setView('movies', 'movies-view')
	
def featured_movies(chname,url,start):
    dp = xbmcgui.DialogProgress()
    dp.create("Movies4ME",'Getting titles')
    dp.update(0)
    origurl = url
    link = open_url(url).translate(trans_table).replace('\t', '').replace('\n', '')#.replace('\\"', '<>')
    print link
    if chname!='search':
        link=regex_from_to(link,'<div id="popularcarousel">','<div id="primary"')
    match=re.compile('<a href="(.+?)">(.+?)alt="(.+?)" border=(.+?)src="(.+?)"').findall(link)
    nItem = len(match)
    count = 0
    for u,d1,title,d2,iconimage in match:
        year = title[len(title)-5:-1]
        title1 = title[:-6].replace('&#8217',"'").rstrip()
        if 'xxxxx' not in title:
            count = count + 1
            titlelist = str(count) + ' of ' + str(nItem) + ': ' + title
            progress = count / float(nItem) * 100               
            dp.update(int(progress), 'Adding title',titlelist)#;
            if dp.iscanceled():
                return
            if ENABLE_META:
                infoLabels = get_meta(title1.replace(' (Cam version)','').replace('\u0026','&'),'movie',year=year)
                if infoLabels['title']=='':
                    name=title
                else:
                    name=infoLabels['title'] + ' (' + str(infoLabels['year']) + ')'
                if infoLabels['cover_url']=='':
                    iconimage=iconimage
                else:
                    iconimage=infoLabels['cover_url']
            else:
                infoLabels =None
                iconimage=iconimage
                name = title
            addDirPlayable(title.replace('\u0026','&').replace('&#8211;','-'),u,12,iconimage,title,infoLabels=infoLabels)#
    setView('movies', 'movies-view')
	
def featured_file(name,url,iconimage):
    link=open_url(url)
    file = regex_from_to(link, 'file="','"')
    play_channel(name,file,iconimage)
	
def search():
    keyboard = xbmc.Keyboard('', 'Search', False)
    keyboard.doModal()
    if keyboard.isConfirmed():
        query = keyboard.getText()
        if len(query) > 0:
            url = 'http://www.hdmoviezone.net/feed/?s=%s&paged=1' % urllib.quote(query)
            search_movies('search',url,"1")
			
def search_movies(name,url,start):
    dp = xbmcgui.DialogProgress()
    dp.create("Movies4ME",'Getting titles')
    dp.update(0)
    origurl = url
    link = open_url(url).translate(trans_table).replace('\t', '').replace('\n', '')#.replace('\\"', '<>')
    link=regex_from_to(link,'<item>','</channel>')
    match=re.compile('<title>(.+?)</title><link>h(.+?)</link>(.+?)<div file="(.+?)" height(.+?)image="(.+?)"').findall(link)
    nItem = len(match)
    count = 0
    for title,url,d1,u,d2,iconimage in match:
        year = title[len(title)-5:-1]
        title1 = title[:-6].replace('&#8217',"'").rstrip()
        if 'xxxxx' not in title:
            count = count + 1
            titlelist = str(count) + ' of ' + str(nItem) + ': ' + title
            progress = count / float(nItem) * 100               
            dp.update(int(progress), 'Adding title',titlelist)#;
            if dp.iscanceled():
                return
            if ENABLE_META:
                infoLabels = get_meta(title1.replace(' (Cam version)','').replace('\u0026','&'),'movie',year=year)
                if infoLabels['title']=='':
                    name=title
                else:
                    name=infoLabels['title'] + ' (' + str(infoLabels['year']) + ')'
                if infoLabels['cover_url']=='':
                    iconimage=iconimage
                else:
                    iconimage=infoLabels['cover_url']
            else:
                infoLabels =None
                iconimage=iconimage
                name = title
            addDirPlayable(title.replace('\u0026','&').replace('&#8211;','-'),u,2,iconimage,title,infoLabels=infoLabels)#
    setView('movies', 'movies-view')
	
def get_meta(name,types=None,year=None,season=None,episode=None,imdb=None,episode_title=None):
    if 'movie' in types:
        meta = metainfo.get_meta('movie',clean_file_name(name, use_blanks=False),year)
        infoLabels = {'rating': meta['rating'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],'plot': meta['plot'],'title': meta['title'],'cover_url': meta['cover_url'],'fanart': meta['backdrop_url'],'Aired': meta['premiered'],'year': meta['year']}
    return infoLabels
	
        
def play_channel(name,url,iconimage):

    min = 1920
    max = 0
    url1 = 'http://gl.hdmoviezone.net/hdmzgl.php'
    header_dict = {}
    form_data = {}
    form_data['url'] = url
    header_dict['Accept'] = 'text/html, */*; q=0.01'
    header_dict['Host'] = 'hdmozo.com'
    header_dict['Connection'] = 'keep-alive'
    header_dict['Referer'] = 'http://www.hdmoviezone.net'
    header_dict['Origin'] = 'http://www.hdmoviezone.net'
    header_dict['Pragma'] = 'no-cache'
    header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.2; rv:24.0) Gecko/20100101 Firefox/24.0'
    trans_table = ''.join( [chr(i) for i in range(128)] + [' '] * 128 )#url,h,w,type
    req = net.http_POST(url1,form_data=form_data, headers=header_dict).content.translate(trans_table).rstrip().replace('\/', '/')
    match = re.compile('"url":"(.+?)","height":(.+?),"width":(.+?),"type":"(.+?)"').findall(req)
    for url,h,w,type in match:
        width = int(w)
        if 'video' in type:
            dimension = "%sx%s" % (w,h)
            if QUALITY == 'HD' and width > max:
                min = width
                max = width
                playlink = url
            elif QUALITY == 'SD' and width < min:
                min = width
                max = width
                playlink = url
    try:
        play_movie(name,playlink,iconimage)
    except:
        notification(name, "[COLOR red]" + 'No source available' + "[/COLOR]", '4000', iconimage)

		
def play_movie(name,url,iconimage):
    listitem = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage, path=url)
    xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
    handle = str(sys.argv[1])    
    if handle != "-1":
        listitem.setProperty("IsPlayable", "true")
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
    else:
        xbmcPlayer.play(url, listitem)
    

def view_trailer(name, url, iconimage):

    menu_texts = []
    menu_data = []
    menu_res = []
    menu_list_item = []
    title1 = name[:-6].rstrip()
    pDialog = xbmcgui.DialogProgress()
    pDialog.create('Searching for trailer')
    dialog = xbmcgui.Dialog()
    try:
        url = "http://www.hd-trailers.net/movie/" + title1.lower().replace(' ','-').replace(':','-')
        response = open_url(url)
        match=re.compile('href="http://(.+?)" rel=(.+?)title="(.+?)">(.+?)</a></td>').findall(response) 
        if len(match)==0:
            url = "http://www.hd-trailers.net/movie/" + title1.lower().replace(' ','-').replace(':','-').replace('and','-')
            response = open_gurl(url)
            match=re.compile('href="http://(.+?)" rel=(.+?)title="(.+?)">(.+?)</a></td>').findall(response) 
            if len(match)==0:
                dialog.ok("Trailer Search", 'No trailers found for:', name) 
                return
        for url, info, title, res in match:
            if url.find('apple')>0:
                url = '%s|User-Agent=QuickTime' % ("http://" + url)
            elif url.find('youtube')>0:
                video_id = url.replace('www.youtube.com/watch?v=','')
                url = (
                    'plugin://plugin.video.youtube/'
                    '?action=play_video&videoid=%s' % video_id
                )
            else:
                url = "http://" + url
            if TRAILER_RESTRICT:
                if url.find('yahoo')<0 and res==TRAILER_QUALITY:
                    menu_texts.append("[%s] %s" % (res, clean_file_name(title, use_blanks=False)))
                    menu_list_item.append(clean_file_name(title, use_blanks=False))
                    menu_data.append(url)
                    menu_res.append(res)
            else:
                if url.find('yahoo')<0:
                    menu_texts.append("[%s] %s" % (res, clean_file_name(title, use_blanks=False)))
                    menu_list_item.append(clean_file_name(title, use_blanks=False))
                    menu_data.append(url)
                    menu_res.append(res)
					
        if TRAILER_ONECLICK:
            menu_id =0
        else:
            menu_id = dialog.select('Select Trailer', menu_texts)
        if(menu_id < 0):
            return (None, None)
            dialog.close()
        else:	
            url = menu_data[menu_id]
            name = menu_texts[menu_id]
            list_item = menu_list_item[menu_id]
			
        pDialog.close()
    
        listitem = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage, path=url)
        xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
        handle = str(sys.argv[1])    
        if handle != "-1":
            listitem.setProperty("IsPlayable", "true")
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
        else:
            xbmcPlayer.play(url, listitem)
    except:
        dialog.ok("Trailer Search", 'No trailers found for:', name)	
		

def favourites():
    if os.path.isfile(FAV):
        s = read_from_file(FAV)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list1 = list.split('<>')
                title = list1[0]
                title = title.replace('->-', ' & ')
                url = list1[1]
                thumb = list1[2]
                year = title[len(title)-5:-1]
                title1 = title[:-6].rstrip()
                if ENABLE_META:
                    infoLabels = get_meta(title1.replace(' (Cam version)','').replace('\u0026','&'),'movie',year=year)
                    if infoLabels['title']=='':
                        name=title
                    else:
                        name=infoLabels['title'] + ' (' + str(infoLabels['year']) + ')'
                    if infoLabels['cover_url']=='':
                        iconimage=iconimage
                    else:
                        iconimage=infoLabels['cover_url']
                else:
                    infoLabels =None
                    iconimage=thumb
                    name = title
                addDirPlayable(title,url,2,iconimage,'fav',infoLabels=infoLabels)
    setView('movies', 'movies-view')
				
def download(name, url, iconimage, dir):

    min = 1920
    max = 0
    url1 = 'http://hdmozo.com/hdmzgl.php'
    header_dict = {}
    form_data = {}
    form_data['url'] = url
    header_dict['Accept'] = 'text/html, */*; q=0.01'
    header_dict['Host'] = 'hdmozo.com'
    header_dict['Connection'] = 'keep-alive'
    header_dict['Referer'] = 'http://www.hdmoviezone.net'
    header_dict['Origin'] = 'http://www.hdmoviezone.net'
    header_dict['Pragma'] = 'no-cache'
    header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.2; rv:24.0) Gecko/20100101 Firefox/24.0'
    trans_table = ''.join( [chr(i) for i in range(128)] + [' '] * 128 )#url,h,w,type
    req = net.http_POST(url1,form_data=form_data, headers=header_dict).content.translate(trans_table).rstrip().replace('\/', '/')
    match = re.compile('"url":"(.+?)","height":(.+?),"width":(.+?),"type":"(.+?)"').findall(req)
    for url,h,w,type in match:
        width = int(w)
        if 'video' in type:
            dimension = "%sx%s" % (w,h)
            if QUALITY == 'HD' and width > max:
                min = width
                max = width
                playlink = url
            elif QUALITY == 'SD' and width < min:
                min = width
                max = width
                playlink = url
    filename = name.replace(':','') + '.mp4'
    WAITING_TIME = 5
    data_path = os.path.join(dir, filename)
    dlThread = DownloadFileThread(name, playlink, data_path, WAITING_TIME)
    dlThread.start()
    wait_dl_only(WAITING_TIME, "Starting Download")
    if os.path.exists(data_path):
        notification('Download started', name, '3000', iconimage)
        scan_library()
		
class DownloadFileThread(Thread):
    def __init__(self, name, url, data_path, WAITING_TIME):
        self.data = url
        self.path = data_path
        self.waiting = WAITING_TIME
        self.name = name
        Thread.__init__(self)

    def run(self):
        start_time = time.time() + 20 + self.waiting
        waiting = self.waiting
        path = self.path
        data = self.data
        name = self.name
        urllib.urlretrieve(data, path)
        notification('Download finished', name, '5000', iconart)
				
	
def add_favourite(name, url, iconimage, dir, text):
    list_data = "%s<>%s<>%s" % (name,url,iconimage)
    add_to_list(list_data, dir)
    notification(name, "[COLOR lime]" + text + "[/COLOR]", '4000', url)
	
def remove_from_favourites(name, url, iconimage, dir, text):
    list_data = "%s<>%s<>%s" % (name,url,iconimage)
    remove_from_list(list_data, dir)
    notification(name, "[COLOR orange]" + text + "[/COLOR]", '4000', url)
	
def add_to_library(name, url, iconimage):
    create_strm_file(name, url, "2", MOVIE_PATH, iconimage, name)
    notification(name, "[COLOR lime]Added to Library[/COLOR]", '3000', iconimage)
    if xbmc.getCondVisibility('Library.IsScanningVideo') == False:           
        xbmc.executebuiltin('UpdateLibrary(video)')
		
def create_directory(dir_path, dir_name=None):
    if dir_name:
        dir_path = os.path.join(dir_path, dir_name)
    dir_path = dir_path.strip()
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path

def create_file(dir_path, file_name=None):
    if file_name:
        file_path = os.path.join(dir_path, file_name)
    file_path = file_path.strip()
    if not os.path.exists(file_path):
        f = open(file_path, 'w')
        f.write('')
        f.close()
    return file_path
	
def create_strm_file(name, url, mode, dir_path, iconimage, showname):
    try:
        strm_string = create_url(name, mode, url=url, iconimage=iconimage, showname=showname)
        filename = clean_file_name("%s.strm" % name)
        path = os.path.join(dir_path, filename)
        if not os.path.exists(path):
            stream_file = open(path, 'w')
            stream_file.write(strm_string)
            stream_file.close()
    except:
        xbmc.log("[Movies4Me] Error while creating strm file for : " + name)
		
def create_url(name, mode, url, iconimage, showname):
    name = urllib.quote(str(name))
    data = urllib.quote(str(url))
    iconimage = urllib.quote(str(iconimage))
    showname = urllib.quote(str(showname))
    mode = str(mode)
    url = sys.argv[0] + '?name=%s&url=%s&mode=%s&iconimage=%s&showname=%s' % (name, data, mode, iconimage, showname)
    return url
	
def get_subscriptions():
    try:
        if os.path.isfile(SUB):
            s = read_from_file(SUB)
            search_list = s.split('\n')
            for list in search_list:
                if list != '':
                    list1 = list.split('QQ')
                    title = list1[0]
                    url = list1[1]
                    thumb = list1[2]
                    create_tv_show_strm_files(title, url, list, "false")
    except:
        xbmc.log("[TVonline] Failed to fetch subscription")

def regex_from_to(text, from_string, to_string, excluding=True):
    if excluding:
        r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
    else:
        r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
    return r

def regex_get_all(text, start_with, end_with):
    r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
    return r

def strip_text(r, f, t, excluding=True):
    r = re.search("(?i)" + f + "([\S\s]+?)" + t, r).group(1)
    return r


def find_list(query, search_file):
    try:
        content = read_from_file(search_file) 
        lines = content.split('\n')
        index = lines.index(query)
        return index
    except:
        return -1
		
def add_to_list(list, file):
    if find_list(list, file) >= 0:
        return

    if os.path.isfile(file):
        content = read_from_file(file)
    else:
        content = ""

    lines = content.split('\n')
    s = '%s\n' % list
    for line in lines:
        if len(line) > 0:
            s = s + line + '\n'
    write_to_file(file, s)
    
def remove_from_list(list, file):
    index = find_list(list, file)
    if index >= 0:
        content = read_from_file(file)
        lines = content.split('\n')
        lines.pop(index)
        s = ''
        for line in lines:
            if len(line) > 0:
                s = s + line + '\n'
        write_to_file(file, s)
        xbmc.executebuiltin("Container.Refresh")
		
def write_to_file(path, content, append=False, silent=False):
    try:
        if append:
            f = open(path, 'a')
        else:
            f = open(path, 'w')
        f.write(content)
        f.close()
        return True
    except:
        if not silent:
            print("Could not write to " + path)
        return False

def read_from_file(path, silent=False):
    try:
        f = open(path, 'r')
        r = f.read()
        f.close()
        return str(r)
    except:
        if not silent:
            print("Could not read from " + path)
        return None

def wait_dl_only(time_to_wait, title):
    print 'Waiting ' + str(time_to_wait) + ' secs'    

    progress = xbmcgui.DialogProgress()
    progress.create(title)
    
    secs = 0
    percent = 0
    
    cancelled = False
    while secs < time_to_wait:
        secs = secs + 1
        percent = int((100 * secs) / time_to_wait)
        secs_left = str((time_to_wait - secs))
        remaining_display = ' waiting ' + secs_left + ' seconds for download to start...'
        progress.update(percent, remaining_display)
        xbmc.sleep(1000)
        if (progress.iscanceled()):
            cancelled = True
            break
    if cancelled == True:     
        print 'wait cancelled'
        return False
    else:
        print 'Done waiting'
        return True

		
def scan_library():
    if xbmc.getCondVisibility('Library.IsScanningVideo') == False:           
        xbmc.executebuiltin('UpdateLibrary(video)')
		
def notification(title, message, ms, nart):
    xbmc.executebuiltin("XBMC.notification(" + title + "," + message + "," + ms + "," + nart + ")")
	
def setView(content, viewType):
	if content:
		xbmcplugin.setContent(int(sys.argv[1]), content)
		
def clear_cache():
    cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.movies4me/cache'), '')
		
    for root, dirs, files in os.walk(cache_path):
        for f in files:
            age = get_file_age(os.path.join(root, f))
            if age > 3600:
    	        os.unlink(os.path.join(root, f))
   

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param


def addDir(name,url,mode,iconimage,list,description):
        suffix = ""
        suffix2 = ""
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+str(iconimage)+"&list="+str(list)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name + suffix + suffix2, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description })
        liz.setProperty('fanart_image', fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
		
def addDirPlayable(name,url,mode,iconimage,showname,infoLabels=None):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&showname="+urllib.quote_plus(showname)
        ok=True
        contextMenuItems = []
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': showname })
        contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
        contextMenuItems.append(("[COLOR lime]Download[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=152&iconimage=%s)'%(sys.argv[0], urllib.quote(showname), urllib.quote(url), urllib.quote(iconimage))))
        contextMenuItems.append(("[COLOR cyan]View Trailer[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=150&iconimage=%s)'%(sys.argv[0], urllib.quote(name), urllib.quote(url), urllib.quote(iconimage))))
        contextMenuItems.append(("[COLOR lime]Add to XBMC Library[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=151&iconimage=%s)'%(sys.argv[0], urllib.quote(name), urllib.quote(url), urllib.quote(iconimage))))
        if showname != 'fav':
            contextMenuItems.append(("[COLOR lime]Save Movie to Favourites[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=8&iconimage=%s)'%(sys.argv[0],urllib.quote(name), urllib.quote(url), urllib.quote(iconimage))))
        if showname == 'fav':
            contextMenuItems.append(("[COLOR orange]Remove from Favourites[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=10&iconimage=%s)'%(sys.argv[0],urllib.quote(name), urllib.quote(url), urllib.quote(iconimage))))        
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        liz.setInfo( type="Video", infoLabels=infoLabels)
        try:
            liz.setProperty( "fanart_image", infoLabels['fanart'] )
        except:
            liz.setProperty('fanart_image', fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
		

params=get_params()

url=None
name=None
mode=None
iconimage=None



try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:
        start=urllib.unquote_plus(params["start"])
except:
        pass
try:
        list=urllib.unquote_plus(params["list"])
except:
        pass
try:
        showname=str(params["showname"])
except:
        pass
try:
        description=urllib.unquote_plus(params["description"])
except:
        pass


if mode==None or url==None or len(url)<1:
        CATEGORIES(name)
		
elif mode==1:
        all_movies(name,url,list)
		
elif mode==11:
        featured_movies(name,url,list)
	
elif mode==12:
        featured_file(name,url,iconimage)
        
elif mode==2:
        play_channel(name,url,iconimage)
		
elif mode==3:
        play_movie(name,url,iconimage)
		
elif mode==4:
        browse_channel(name,url,iconimage,False)
		
elif mode==5:
        play_video(name, url, iconimage,True)
		
elif mode==6:
        play_video(name, url, iconimage,False)
		
elif mode==7:
        channel_schedule(name,url,iconimage)
		
elif mode==8:
        add_favourite(name, url, iconimage, FAV, "Added to Favourites")
		
elif mode == 9:
        favourites()
		
elif mode == 10:
        remove_from_favourites(name, url, iconimage, FAV, "Removed from Favourites")
		
elif mode == 100:
        genres()
		
elif mode == 110:
        countries()
		
elif mode == 120:
        years()
		
elif mode == 130:
        a_z(url)
		
elif mode == 131:
        a_z_movies(name,url)
		
elif mode == 140:
        search()
		
elif mode == 150:
        view_trailer(name, url, iconimage)
		
elif mode == 151:
        add_to_library(name, url, iconimage)
		
elif mode == 152:
        download(name, url, iconimage, MOVIE_PATH)
		
elif mode == 155:
        clear_cache()
		
		
xbmcplugin.endOfDirectory(int(sys.argv[1]))


