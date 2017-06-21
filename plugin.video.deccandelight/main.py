"""
    Deccan Delight Kodi Addon
    Copyright (C) 2016 gujal

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
"""

import sys
from urlparse import parse_qsl
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
from BeautifulSoup import BeautifulSoup, SoupStrainer
import abc, urllib, re, requests, json
import resources.lib.jsunpack as jsunpack
import urlresolver

try:
    import StorageServer
except:
    import storageserverdummy as StorageServer

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])

_addon = xbmcaddon.Addon()
_addonname = _addon.getAddonInfo('name')
_icon = _addon.getAddonInfo('icon')
_fanart = _addon.getAddonInfo('fanart')
_path = _addon.getAddonInfo('path')
_ipath = _path + '/resources/images/'
_spath = 'resources.scrapers'
_settings = _addon.getSetting

cache = StorageServer.StorageServer("deccandelight", _settings('timeout'))

mozhdr = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'}

class abstractclassmethod(classmethod):
    __isabstractmethod__ = True

    def __init__(self, callable):
        callable.__isabstractmethod__ = True
        super(abstractclassmethod, self).__init__(callable)

class Scraper(object):
    __metaclass__ = abc.ABCMeta
    
    def __init__(self):
        self.ipath = _ipath
        self.hdr = mozhdr
        self.settings = _settings
        self.adult = _settings('adult')
        self.nicon = self.ipath + 'next.png'
        
    def get_nicon(self):
        return self.nicon
    
    def get_SearchQuery(self,sitename):
        keyboard = xbmc.Keyboard()
        keyboard.setHeading('Search ' + sitename)
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_text = keyboard.getText()

        return search_text

    def get_vidhost(self,url):
        """
        Trim the url to get the video hoster
        :return vidhost
        """
        parts = url.split('/')[2].split('.')
        vidhost = '%s.%s'%(parts[len(parts)-2],parts[len(parts)-1])
        return vidhost

    def resolve_media(self,url,videos,vidtxt=''):
        non_str_list = ['olangal.', '#', 'magnet:', 'desihome.', 'thiruttuvcd',
                        'cineview', 'bollyheaven', 'videolinkz', 'moviefk.co',
                        'imdb.', 'mgid.', 'atemda.', 'movierulz.', 'facebook.', 
                        'm2pub', 'abcmalayalam', 'india4movie.co', '.filmlinks4u',
                        'tamilraja.', 'multiup.', 'filesupload.', 'fileorbs.',
                        'insurance-donate.', '.blogspot.', 'yodesi.net', 
                        'yomasti.co/ads', 'ads.yodesi.net', 'business-tv.me/ads']

        embed_list = ['cineview', 'bollyheaven', 'videolinkz', 'vidzcode',
                      'embedzone', 'embedsr', 'fullmovie-hd', 'adly.biz',
                      'embedscr', 'embedrip', 'movembed', 'power4link.us',
                      'watchmoviesonline4u', 'nobuffer.info', 'yomasti.co',
                      'techking.me', 'onlinemoviesworld.xyz', 'cinebix.com',
                      'desihome.', 'loan-forex.', 'filmshowonline.',
                      'vids.xyz', 'business-tv.me']
           
        if 'filmshowonline.net/media/' in url:
            try:
                r = requests.get(url, headers=self.hdr)
                clink = r.text
                cookies = r.cookies
                eurl = re.findall("var height.*?url: '(.*?)'", clink, re.DOTALL)[0]
                enonce = re.findall("var height.*?nonce.*?'(.*?)'", clink, re.DOTALL)[0]
                evid = re.findall("var height.*?link_id: ([^\s]*)", clink, re.DOTALL)[0]
                values = {'echo' : 'true',
                          'nonce' : enonce,
                          'width' : '848',
                          'height' : '480',
                          'link_id' : evid }
                headers = self.hdr
                headers['Referer'] = url
                headers['X-Requested-With'] = 'XMLHttpRequest'
                emurl = requests.post(eurl, data=values, headers=headers, cookies=cookies).text
                strurl = (re.findall('(http[^"]*)', emurl)[0]).replace('\\', '')
                if urlresolver.HostedMediaFile(strurl):
                    vidhost = self.get_vidhost(strurl)
                    if not vidtxt == '':
                        vidhost += ' | %s' % vidtxt
                    videos.append((vidhost,strurl))
            except:
                pass

        elif 'justmoviesonline.com' in url:
            try:
                html = requests.get(url, headers=mozhdr).text
                src = re.findall("atob\('(.*?)'",html)[0]
                strurl = re.findall('file":"(.*?)"',src.decode('base64'))[0]
                vidhost = self.get_vidhost(url) + ' | GVideo'
                strurl = urllib.quote_plus(strurl)
                videos.append((vidhost,strurl))
            except:
                pass
            
        elif 'videohost.site' in url or 'videohost1.com' in url:
            try:
                html = requests.get(url, headers=mozhdr).text
                pdata = eval(re.findall('Run\((.*?)\)',html)[0]).decode('base64')
                linkcode = jsunpack.unpack(pdata).replace('\\','')
                sources = json.loads(re.findall('sources:(.*?\}\])',linkcode)[0])
                for source in sources:    
                    strurl = source['file'] + '|Referer=%s'%url
                    vidhost = self.get_vidhost(url) + ' | GVideo | %s' % source['label']
                    strurl = urllib.quote_plus(strurl)
                    videos.append((vidhost,strurl))
            except:
                pass
                
        elif 'tamildbox' in url:
            try:
                link = requests.get(url, headers=mozhdr).text
                mlink = SoupStrainer('div', {'id':'player-embed'})
                dclass = BeautifulSoup(link, parseOnlyThese=mlink)       
                if 'unescape' in str(dclass):
                    etext = re.findall("unescape.'[^']*", str(dclass))[0]
                    etext = urllib.unquote(etext)
                    dclass = BeautifulSoup(etext)
                glink = dclass.iframe.get('src')
                if urlresolver.HostedMediaFile(glink):
                    vidhost = self.get_vidhost(glink)
                    videos.append((vidhost,glink))
                mlink = SoupStrainer('div', {'class':re.compile('^item-content')})
                dclass = BeautifulSoup(link, parseOnlyThese=mlink)
                glink = dclass.p.iframe.get('src')
                if urlresolver.HostedMediaFile(glink):
                    vidhost = self.get_vidhost(glink)
                    videos.append((vidhost,glink))
            except:
                pass

        elif any([x in url for x in embed_list]):
            clink = requests.get(url, headers=mozhdr).text
            csoup = BeautifulSoup(clink)
            try:
                for link in csoup.findAll('iframe'):
                    strurl = link.get('src')
                    if not any([x in strurl for x in non_str_list]):
                        if urlresolver.HostedMediaFile(strurl):
                            vidhost = self.get_vidhost(strurl)
                            if not vidtxt == '':
                                vidhost += ' | %s' % vidtxt
                            videos.append((vidhost,strurl))
                        else:
                            xbmc.log('-------> URLResolver cannot resolve : %s' % strurl)
            except:
                pass

            try:
                plink = csoup.find('a', {'class':'main-button dlbutton'})
                strurl = plink.get('href')
                if not any([x in strurl for x in non_str_list]):
                    if urlresolver.HostedMediaFile(strurl):
                        vidhost = self.get_vidhost(strurl)
                        if not vidtxt == '':
                            vidhost += ' | %s' % vidtxt
                        videos.append((vidhost,strurl))
            except:
                pass

            try:
                plink = csoup.find('div', {'class':'aio-pulse'})
                strurl = plink.find('a')['href']
                if not any([x in strurl for x in non_str_list]):
                    if urlresolver.HostedMediaFile(strurl):
                        vidhost = self.get_vidhost(strurl)
                        if not vidtxt == '':
                            vidhost += ' | %s' % vidtxt
                        videos.append((vidhost,strurl))
            except:
                pass

            try:
                plink = csoup.find('div', {'class':'entry-content rich-content'})
                strurl = plink.find('a')['href']
                if not any([x in strurl for x in non_str_list]):
                    if urlresolver.HostedMediaFile(strurl):
                        vidhost = self.get_vidhost(strurl)
                        if not vidtxt == '':
                            vidhost += ' | %s' % vidtxt
                        videos.append((vidhost,strurl))
            except:
                pass

            try:
                for linksSection in csoup.findAll('embed'):
                    strurl = linksSection.get('src')
                    if not any([x in strurl for x in non_str_list]):
                        if urlresolver.HostedMediaFile(strurl):
                            vidhost = self.get_vidhost(strurl)
                            if not vidtxt == '':
                                vidhost += ' | %s' % vidtxt
                            videos.append((vidhost,strurl))
            except:
                pass
                
        elif not any([x in url for x in non_str_list]):
            if urlresolver.HostedMediaFile(url):
                vidhost = self.get_vidhost(url)
                if not vidtxt == '':
                    vidhost += ' | %s' % vidtxt
                videos.append((vidhost,url))
            else:
                xbmc.log('-------> URLResolver cannot resolve : %s' % url)

        return
        
    def clean_title(self, title):
        cleanup = ['Watch Online Movie', 'Watch Onilne', 'Tamil Movie ', 'Tamil Dubbed', 'WAtch ', 'Online Free',
                   'Full Length', 'Latest Telugu',
                   'Full Movie Online Free', 'Full Movie Online', 'Watch Online ', 'Free HD', 'Online Full Movie',
                   'Full Free', 'Malayalam Movie', ' Malayalam ', 'Full Movies', 'Full Movie', 'Free Online',
                   'Movie Online', 'Watch ', 'movie online', 'Wach ', 'Movie Songs Online', 'Full Hindi',
                   'tamil movie songs online', 'tamil movie songs', 'movie songs online', 'Tamil Movie', ' Hindi',
                   'Hilarious Comedy Scenes', 'Super Comedy Scenes', 'Ultimate Comedy Scenes', 'Watch...',
                   'Super comedy Scenes', 'Comedy Scenes', 'hilarious comedy Scenes', '...', 'Telugu Movie',
                   'Sun TV Show', 'Vijay TV Show', 'Vijay Tv Show', 'Vijay TV Comedy Show', 'Hindi Movie',
                   'Vijay Tv Comedy Show', 'Vijay TV', 'Vijay Tv', 'Sun Tv Show', 'Download', 'Starring', u'\u2013',
                   'Tamil Full Movie', 'Tamil Horror Movie', 'Tamil Dubbed Movie', '|', '-', ' Full ', u'\u2019',
                   '/', 'Pre HDRip', '(DVDScr Audio)', 'PDVDRip', 'DVDSCR', '(HQ Audio)', 'HQ', ' Telugu',
                   'DVDScr', 'DVDscr', 'PreDVDRip', 'DVDRip', 'DVDRIP', 'WEBRip', 'WebRip', 'Movie', ' Punjabi',
                   'TCRip', 'HDRip', 'HDTVRip', 'HD-TC', 'HDTV', 'TVRip', '720p', 'DVD', 'HD', ' Dubbed', '( )',
                   '720p', '(UNCUT)', 'UNCUT', '(Clear Audio)', 'DTHRip', '(Line Audio)', ' Kannada', ' Hollywood',
                   'TS', 'CAM', 'Online Full', '[+18]', 'Streaming Free', 'Permalink to ', 'And Download', '()',
                   'Full English', ' English', 'Downlaod', 'Bluray', 'Online', ' Tamil', ' Bengali', ' Bhojpuri']
        
        for word in cleanup:
            if word in title:
                title = title.replace(word,'')

        title = title.strip()
        title = title.encode('utf8')
        return title

sites = {'01tgun': 'Tamil Gun : [COLOR yellow]Tamil[/COLOR]',
         '02rajt': 'Raj Tamil : [COLOR yellow]Tamil[/COLOR]',
         '03tyogi': 'Tamil Yogi : [COLOR yellow]Tamil[/COLOR]',
         '04runt': 'Run Tamil : [COLOR yellow]Tamil[/COLOR]',
         '05rasigan': 'Tamil Rasigan : [COLOR yellow]Tamil[/COLOR]',
         '06tamiltv': 'APKLand TV : [COLOR yellow]Tamil Live TV and VOD[/COLOR]',
         '07ttvs': 'Tamil TV Shows : [COLOR yellow]Tamil Catchup TV[/COLOR]',
         '11awatch': 'Andhra Watch : [COLOR yellow]Telugu[/COLOR]',
         '21abcm': 'ABC Malayalam : [COLOR yellow]Malayalam[/COLOR]',
         '22olangal': 'Olangal : [COLOR yellow]Malayalam[/COLOR]',
         '23lmtv': 'Live Malayalam : [COLOR yellow]Malayalam Live TV[/COLOR]',
         '24mserial': 'Malayalam Serials : [COLOR yellow]Malayalam Catchup TV[/COLOR]',
         '41hlinks': 'Hindi Links 4U : [COLOR yellow]Hindi[/COLOR]',
         '42desit': 'Desi Tashan : [COLOR yellow]Hindi Catchup TV[/COLOR]',
         '43yodesi': 'Yo Desi : [COLOR yellow]Hindi Catchup TV[/COLOR]',
         '44gmala': 'Hindi Geetmala : [COLOR yellow]Hindi Songs[/COLOR]',
         '51mhdtv': 'MHDTV Live : [COLOR magenta]Various Live TV[/COLOR]',
         '52aindia': 'Abroad India : [COLOR magenta]Various Live TV[/COLOR]',
         '53ozee': 'OZee : [COLOR magenta]Various Catchup TV[/COLOR]',
         '61apnav': 'Apna View : [COLOR magenta]Various[/COLOR]',
         '62tvcd': 'Thiruttu VCD : [COLOR magenta]Various[/COLOR]',
         '63mrulz': 'Movie Rulz : [COLOR magenta]Various[/COLOR]',
         '64i4movie': 'India 4 Movie : [COLOR magenta]Various[/COLOR]',
         '65moviefk': 'Movie FK : [COLOR magenta]Various[/COLOR]',
         '66mfish': 'Movie Fisher : [COLOR magenta]Various[/COLOR]',
         '67mersal': 'Mersalaayitten : [COLOR magenta]Various[/COLOR]',
         '68ttwist': 'Tamil Twists : [COLOR magenta]Various[/COLOR]',
         '69flinks': 'Film Links 4 U : [COLOR magenta]Various[/COLOR]',
         '70redm': 'Red Movies : [COLOR magenta]Various[/COLOR]',
         '71tvcds': 'Thiruttu VCDs : [COLOR magenta]Various[/COLOR]'}

import resources.scrapers.tgun
import resources.scrapers.rajt
import resources.scrapers.tyogi
import resources.scrapers.runt
import resources.scrapers.abcm
import resources.scrapers.olangal
import resources.scrapers.mersal
import resources.scrapers.lmtv
import resources.scrapers.tvcd
import resources.scrapers.tamiltv
import resources.scrapers.ttvs
import resources.scrapers.redm
import resources.scrapers.mrulz
import resources.scrapers.i4movie
import resources.scrapers.moviefk
import resources.scrapers.mfish
import resources.scrapers.yodesi
import resources.scrapers.ttwist
import resources.scrapers.tvcds
import resources.scrapers.flinks
import resources.scrapers.hlinks
import resources.scrapers.desit
import resources.scrapers.apnav
import resources.scrapers.aindia
import resources.scrapers.mserial
import resources.scrapers.gmala
import resources.scrapers.awatch
import resources.scrapers.ozee
import resources.scrapers.rasigan
import resources.scrapers.mhdtv

def list_sites():
    """
    Create the Sites menu in the Kodi interface.
    """
    listing = []
    for site,title in sorted(sites.iteritems()):
        if _settings(site[2:]) == 'true':
            item_icon = _ipath + '%s.png'%site[2:]
            list_item = xbmcgui.ListItem(label=title)
            list_item.setArt({'thumb': item_icon,
                              'icon': item_icon,
                              'fanart': _fanart})
            url = '{0}?action=1&site={1}'.format(_url, site[2:])
            is_folder = True
            listing.append((url, list_item, is_folder))

    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.endOfDirectory(_handle)

def list_menu(site):
    """
    Create the Site menu in the Kodi interface.
    """
    scraper = eval('%s.%s.%s()'%(_spath,site,site))
    #scraper = eval('%s.%s()'%(site,site))
    menu,mode,icon = cache.cacheFunction(scraper.get_menu)
    listing = []
    for title,iurl in sorted(menu.iteritems()):
        if 'MMMM' in iurl:
            niurl = iurl.split('MMMM')[0]
            nmode = iurl.split('MMMM')[1]
            list_item = xbmcgui.ListItem(label=title[2:])
            list_item.setArt({'thumb': icon,
                              'icon': icon,
                              'fanart': _fanart})
            url = '{0}?action={1}&site={2}&iurl={3}'.format(_url, nmode, site, urllib.quote(niurl))
            is_folder = True
            listing.append((url, list_item, is_folder))
        elif 'Adult' not in title:
            list_item = xbmcgui.ListItem(label=title[2:])
            list_item.setArt({'thumb': icon,
                              'icon': icon,
                              'fanart': _fanart})
            url = '{0}?action={1}&site={2}&iurl={3}'.format(_url, mode, site, urllib.quote(iurl))
            is_folder = True
            listing.append((url, list_item, is_folder))
        elif _settings('adult') == 'true':
            list_item = xbmcgui.ListItem(label=title[2:])
            list_item.setArt({'thumb': icon,
                              'icon': icon,
                              'fanart': _fanart})
            url = '{0}?action={1}&site={2}&iurl={3}'.format(_url, mode, site, urllib.quote(iurl))
            is_folder = True
            listing.append((url, list_item, is_folder))            
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.endOfDirectory(_handle)

def list_top(site,iurl):
    """
    Create the Site menu in the Kodi interface.
    """
    scraper = eval('%s.%s.%s()'%(_spath,site,site))
    #scraper = eval('%s.%s()'%(site,site))
    menu,mode = cache.cacheFunction(scraper.get_top,iurl)
    listing = []
    for title,icon,iurl in menu:
            list_item = xbmcgui.ListItem(label=title)
            list_item.setArt({'thumb': icon,
                              'icon': icon,
                              'fanart': _fanart})
            url = '{0}?action={1}&site={2}&iurl={3}'.format(_url, mode, site, urllib.quote(iurl))
            is_folder = True
            listing.append((url, list_item, is_folder))            
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.endOfDirectory(_handle)

def list_second(site,iurl):
    """
    Create the Site menu in the Kodi interface.
    """
    scraper = eval('%s.%s.%s()'%(_spath,site,site))
    #scraper = eval('%s.%s()'%(site,site))
    menu,mode = cache.cacheFunction(scraper.get_second,iurl)
    listing = []
    for title,icon,iurl in menu:
        list_item = xbmcgui.ListItem(label=title)
        list_item.setArt({'thumb': icon,
                          'icon': icon,
                          'fanart': _fanart})
        nextmode = mode
        if 'Next Page' in title:
            nextmode = 5
        url = '{0}?action={1}&site={2}&iurl={3}'.format(_url, nextmode, site, urllib.quote(iurl))
        is_folder = True
        if mode == 9 and 'Next Page' not in title:
            is_folder = False
            list_item.setProperty('IsPlayable', 'true')
            list_item.addStreamInfo('video', { 'codec': 'h264'})
        listing.append((url, list_item, is_folder))            
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.endOfDirectory(_handle)

def list_items(site,iurl):
    """
    Create the list of movies/episodes in the Kodi interface.
    """
    scraper = eval('%s.%s.%s()'%(_spath,site,site))
    #scraper = eval('%s.%s()'%(site,site))
    #if iurl.endswith(('?s=','query=','value=','words=')):
    if iurl.endswith('='):
        movies,mode = scraper.get_items(iurl)
    else:
        movies,mode = cache.cacheFunction(scraper.get_items,iurl)
    listing = []
    for movie in movies:
        title = movie[0]
        if title == '':
            title = 'Unknown'
        list_item = xbmcgui.ListItem(label=title)
        list_item.setInfo('video', {'title': title})
        if 'Next Page' in title:
            if mode == 9:
                nextmode = 7
            else:
                nextmode = mode - 1
            url = '{0}?action={1}&site={2}&iurl={3}'.format(_url, nextmode, site, urllib.quote(movie[2]))
            list_item.setArt({'thumb': movie[1],
                              'icon': movie[1],
                              'fanart': _fanart})            
        else:
            qtitle = urllib.quote(title)
            iurl = urllib.quote(movie[2])
            url = '{0}?action={1}&site={2}&title={3}&thumb={4}&iurl={5}'.format(_url, mode, site, qtitle, movie[1].encode('utf8'), iurl)
            list_item.setArt({'thumb': movie[1],
                              'icon': movie[1],
                              'fanart': _fanart})
        if mode == 9 and 'Next Page' not in title:
            is_folder = False
            list_item.setProperty('IsPlayable', 'true')
            list_item.addStreamInfo('video', { 'codec': 'h264'})
        else:
            is_folder = True
        listing.append((url, list_item, is_folder))
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.endOfDirectory(_handle)
    
def list_videos(site,title,iurl,thumb):
    """
    Create the list of playable videos in the Kodi interface.

    :param category: str
    """
    scraper = eval('%s.%s.%s()'%(_spath,site,site))
    #scraper = eval('%s.%s()'%(site,site))
    videos = cache.cacheFunction(scraper.get_videos,iurl)
    listing = []
    for video in videos:
        list_item = xbmcgui.ListItem(label=video[0])
        list_item.setArt({'thumb': thumb,
                          'icon': thumb,
                          'fanart': thumb})
        list_item.setInfo('video', {'title': title})
        list_item.addStreamInfo('video', { 'codec': 'h264'})
        list_item.setProperty('IsPlayable', 'true')
        url = '{0}?action=9&iurl={1}'.format(_url, video[1])
        is_folder = False
        listing.append((url, list_item, is_folder))

    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.endOfDirectory(_handle)

def resolve_url(url):
    duration=7500   
    try:
        stream_url = urlresolver.HostedMediaFile(url=url).resolve()
        # If urlresolver returns false then the video url was not resolved.
        if not stream_url or not isinstance(stream_url, basestring):
            try: msg = stream_url.msg
            except: msg = url
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%('URL Resolver',msg, duration, _icon))
            return False
    except Exception as e:
        try: msg = str(e)
        except: msg = url
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%('URL Resolver',msg, duration, _icon))
        return False
        
    return stream_url

def play_video(iurl):
    """
    Play a video by the provided path.

    :param path: str
    """
    streamer_list = ['tamilgun', 'mersalaayitten', 'mhdtvlive.',
                     'tamiltvsite.', 'cloudspro.', 'abroadindia.',
                     'hindigeetmala.','.mp4', 'googlevideo.' ,
                     'tamilhdtv.', 'andhrawatch.','justmoviesonline.',
                     '.mp3', 'ozee.']
    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=iurl)
    vid_url = play_item.getfilename()
    if any([x in vid_url for x in streamer_list]):
        if 'mersalaayitten' in vid_url:
            scraper = resources.scrapers.mersal.mersal()
            stream_url,srtfile = scraper.get_video(vid_url)
            play_item.setPath(stream_url)
            if srtfile:
                play_item.setSubtitles(['special://temp/mersal.srt', srtfile])
        elif 'hindigeetmala.' in vid_url:
            scraper = resources.scrapers.gmala.gmala()
            stream_url = scraper.get_video(vid_url)
            if stream_url:
                if 'youtube.' in stream_url:
                    stream_url = resolve_url(stream_url)
                play_item.setPath(stream_url)
        elif 'ozee.' in vid_url:
            scraper = resources.scrapers.ozee.ozee()
            stream_url = scraper.get_video(vid_url)
            if stream_url:
                play_item.setPath(stream_url)
        elif 'andhrawatch.' in vid_url:
            scraper = resources.scrapers.awatch.awatch()
            stream_url = scraper.get_video(vid_url)
            if stream_url:
                if 'youtube.' in stream_url:
                    stream_url = resolve_url(stream_url)
                play_item.setPath(stream_url)
        elif 'tamiltvsite.' in vid_url or 'tamilhdtv.' in vid_url:
            scraper = resources.scrapers.tamiltv.tamiltv()
            stream_url = scraper.get_video(vid_url)
            if stream_url:
                if 'youtube.' in stream_url:
                    stream_url = resolve_url(stream_url)
                play_item.setPath(stream_url)
        elif 'mhdtvlive.' in vid_url:
            scraper = resources.scrapers.lmtv.lmtv()
            stream_url = scraper.get_video(vid_url)
            if 'youtube.' in stream_url:
                stream_url = resolve_url(stream_url)
            play_item.setPath(stream_url)
        elif 'abroadindia.' in vid_url:
            scraper = resources.scrapers.aindia.aindia()
            stream_url = scraper.get_video(vid_url)
            if stream_url:
                if 'youtube.' in stream_url:
                    stream_url = resolve_url(stream_url)
                elif '.f4m' in stream_url:
                    qurl = urllib.quote_plus(stream_url)
                    stream_url = 'plugin://plugin.video.f4mTester/?streamtype=HDS&url=%s'%qurl
                elif '.ts' in stream_url:
                    qurl = urllib.quote_plus(stream_url)
                    stream_url = 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&url=%s'%qurl
                play_item.setPath(stream_url) 
    else:
        stream_url = resolve_url(vid_url)
        if stream_url:
            play_item.setPath(stream_url)    

    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)

def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring

    :param paramstring:
    Action Definitions:
    1 : List Site
    4 : List Top Menu (Channels, Languages)
    5 : List Secondary Menu (Shows, Categories)
    7 : List Individual Items (Movies, Episodes)
    8 : List Playable Videos
    9 : Play Video
    """
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin

    if params:
        if params['action'] == '1':
            list_menu(params['site'])
        elif params['action'] == '4':
            list_top(params['site'],params['iurl'])
        elif params['action'] == '5':
            list_second(params['site'],params['iurl'])   
        elif params['action'] == '7':
            list_items(params['site'],params['iurl'])
        elif params['action'] == '8':
            list_videos(params['site'],params['title'],params['iurl'],params['thumb'])
        elif params['action'] == '9':
            play_video(params['iurl'])
    else:
        list_sites()


if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])
