import xbmc, xbmcplugin, xbmcaddon, xbmcgui, xbmcvfs

import urllib
import urllib2
import requests
import json
import os
import re
import sys

from addon.common.addon import Addon
from metahandler import metahandlers


addon_id = 'plugin.video.mutttsnutz'
addon = Addon(addon_id, sys.argv)
Addon = xbmcaddon.Addon(addon_id)

try:
    import StorageServer
except:
    import storageserverdummy as StorageServer
cache = StorageServer.StorageServer(addon_id)

cookie_path = os.path.join( xbmc.translatePath( addon.get_profile()), 'cookies' )
cookie_jar = os.path.join( cookie_path , 'cookiejar.lwp')

try:
    os.makedirs(os.path.dirname(cookie_jar))
except OSError:
    pass

baseUrl = 'http://m.afdah.org'
url = addon.queries.get('url', '')
name = addon.queries.get('name', '')
year = addon.queries.get('year', '')
mode = addon.queries.get('mode', '')
img = addon.queries.get('img', '')
fanart = addon.queries.get('fanart', '')
imdb = addon.queries.get('imdb', '')
infol = addon.queries.get('infol', '')
cookie = addon.queries.get('cookie', '')

auto_play = addon.get_setting('autoplay')
def_quality = addon.get_setting('default_quality')

User_Agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'



menu = [
    ( 'content', baseUrl, 'Movies'),
    ( 'content', baseUrl+'/most_viewed', 'Most Viewed'),
    ( 'content', baseUrl+'/recent_movies', 'Recent Movies'),
    ( 'year', baseUrl, 'By Year'),
    ( 'year', baseUrl, 'By Genre'),
    ( 'search', baseUrl, '[COLOR blue][B]SEARCH[/B][/COLOR]'),
    ( 'settings', baseUrl, ' Settings'),
    ]


def MAIN( menu ):
    #TOTALXBMCSUX()
    for (mode, url, name) in menu:
        addon.add_directory({'mode': mode, 'url': url, 'name': name},{'title': name})
    
    

def settings():
    addon.add_directory({'mode': 'meta'},{'title': 'Metadata Settings'},
                        img='https://raw.githubusercontent.com/Eldorados/script.module.metahandler/master/icon.png',
                        is_folder=False)
    addon.add_directory({'mode': 'adset'},{'title': 'Addon Settings'},
                        img=addon.get_icon(),is_folder=False)

def Year( url, name ):
    addon.log('Year %s'% name)

    res_url = []
    res_year = []

    headers = {}
    headers['User-Agent'] = User_Agent
    html = requests.get(url, headers=headers).text

    if re.search('Year',name, re.I):
        r = re.findall(r'an\>Years(.*?)\<li class=\"has', html, re.I|re.DOTALL)
        pattern = 'href=\"(.*?)\"\>\<span\>(\d+)\<\/span\>'
        title = 'Select Year'
        
    if re.search('Genre',name, re.I):
        r = re.findall(r'an\>Genres(.*?)\<\/ul\>\<\/li\>', html, re.I|re.DOTALL)
        pattern = 'href=\"(.*?)\"\>\<span\>(.*?)\<\/span'
        title = 'Select Genre'
        
    if r:
        result = re.findall(r''+pattern+'', r[0])
        if r:
            for url, year in result:
                res_url.append( baseUrl+url )
                res_year.append( year )

            dialog = xbmcgui.Dialog()
            ret = dialog.select( title,res_year)
            if ret == -1:
                MAIN( menu )
            elif ret > -1:
                content( res_url[ret] )


def Search( url ):
    addon.log('Search')

    keyboard = xbmc.Keyboard()
    keyboard.setHeading(addon.get_name()+': Search [COLOR red][B]*HD*[/COLOR][/B] Movies')
    
    keyboard.doModal()

    if keyboard.isConfirmed():
        searcht=keyboard.getText()
        if not searcht:
            addon.show_ok_dialog(['empty search not allowed'.title()], addon.get_name())
            Search( url )
    else:
        MAIN( menu )
    import urllib
    url = baseUrl+'/results?q=%s' % ( urllib.quote_plus( searcht ))

    content( url )

def SuperSearch( query ):
    addon.log('SuperSearch')
    searcht=query
    import urllib
    url = baseUrl+'/results?q=%s' % ( urllib.quote_plus( searcht ))
    content( url )

def content( url ):
    headers = {}
    name = ''
    headers['User-Agent'] = User_Agent
    html = requests.get(url, headers=headers).text

    pagen = re.findall(r't_page\"\>(\d+)\<\/a\>\<a\shref=\"(.*?page\=)\d+\".*?ge=(\d+)\"\>\>\>', html, re.I)
    if len(pagen) == 0:
        pagen = re.findall(r't_page\"\>(\d+)\<\/a\>\<a\shref=\"(.*?page\=)\d+\"', html, re.I)
        if len(pagen) != 0:
            for current, nextp in pagen:
                name = 'Page %s' % current
        else:
            pagen = re.findall(r't_page\"\>(\d+)\<\/a\>\<a\shref=\"(.*?page\=)\d+\"', html, re.I)
            if len(pagen) == 0:
                pagen = re.findall(r'ging\"\>\<a\shref=\"(.*?)\".*?nt_page\"\>(\d+)\<\/a', html, re.I)
                for preurl, current in pagen:
                    name = 'Page %s' % current
                    nextp = preurl+'?page='
    else:
        for current, nextp, total in pagen:
            name = 'Page %s of %s Pages Available' % ( current, total )
            
    addon.add_item({},{'title': name},is_folder=False)


    r = re.findall(r'<h3><a\stitle=\"(.*?)\s\(\d+.*?\"\shref=\"(.*?)\".*?\<b\>Year\<\/b\>\:\s(\d+)\s\-\s\<b\>Quality\<\/b\>\:\s(.*?)$',
                   html, re.I|re.DOTALL|re.M)
    totalitems = len(r)

    if r:
        for name, url, year, quality in r:
            if '1080p' in quality: quality = '[COLOR blue][B]['+quality+'][/COLOR][/B]'
            elif '720p' in quality: quality = '[COLOR green][B]['+quality+'][/COLOR][/B]'
            elif '360' in quality: quality = '[COLOR red][B]['+quality+'][/COLOR][/B]'
            meta = getMeta( name, year)

            if meta['trailer']:
                contextmenu_items=[('[COLOR blue][B]W[/B]atch [B]T[/B]railer[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'playtrailer', 'url':meta['trailer']}))]
                meta['title'] = name+' '+quality+' [COLOR gold][B][Trailer Available][/B][/COLOR]'
            else:
                contextmenu_items= []
                meta['title'] = name+' '+quality+' [COLOR gold][B][No Trailer Available][/B][/COLOR]'

            path = pathfromname(name)
            if not os.path.exists(path):
                contextmenu_items.append(['[COLOR lime][B]A[/B]dd [B]T[/B]o [B]L[/B]ibrary[/COLOR]','XBMC.RunPlugin(%s)' %
                                          addon.build_plugin_url({'mode': 'add2lib', 'url': baseUrl+url, 'name': name, 'infol': meta, 'img': meta['cover_url'],
                                                                  'fanart':meta['backdrop_url'], 'infol': 'libmeta', 'year': year})])
            if os.path.exists(path):
                contextmenu_items.append(['[COLOR red][B]R[/B]emove [B]F[/B]rom [B]L[/B]ibrary[/COLOR]','XBMC.RunPlugin(%s)' %
                                          addon.build_plugin_url({'mode': 'remromlib', 'url': baseUrl+url, 'name': name, 'infol': meta, 'img': meta['cover_url'],
                                                                  'fanart':meta['backdrop_url'], 'infol': 'libmeta', 'year': year})])
            
            addon.add_video_item({'mode': 'playstream', 'url': baseUrl+url, 'name': name, 'infol': meta},
                                 infolabels=meta, contextmenu_items=contextmenu_items, img=meta['cover_url'],
                                 fanart=meta['backdrop_url'], resolved=False, total_items=totalitems)
        try:addon.add_directory({'mode': 'content', 'url':  baseUrl+nextp+str(int(current)+1)},{'title': '>>Next Page>>>'})
        except:pass
        try:
            if int(current) > 1:
                addon.add_directory({'mode': 'content', 'url':  baseUrl+nextp+str(int(current)-1)},{'title': '<<<Previous Page<<'})
        except:pass
    setView('movies', 'movie-view')

            
    

def playtrailer( url ):
    addon.log('Play Trailer %s' % url)
    notification( addon.get_name(), 'fetching trailer', addon.get_icon())
    xbmc.executebuiltin("PlayMedia(%s)"%url)


            

def getMeta( name, year):
    mg = metahandlers.MetaData()
    meta = mg.get_meta('movie', name=name, year=year)
    return meta


def add2lib( url, name, infol, img, fanart, year ):

    img = 'http://oi62.tinypic.com/dvgj1t.jpg'
    addon.log('Add To Library %s , %s, %s' % (name,year,url))

    path = xbmc.translatePath( addon.get_setting('movie-folder') )
    string = 'plugin://plugin.video.mutttsnutz/?mode=playstream&url='+url+'&name='+name+'&infol='
    filename = '%s.strm' % name
    path = xbmc.makeLegalFilename( xbmc.translatePath(os.path.join( path, name, filename )))

    if not xbmcvfs.exists(os.path.dirname(path)):
        try:
            try: xbmcvfs.mkdirs(os.path.dirname(path))
            except: os.mkdir(os.path.dirname(path))
        except:
            addon.log('FAILED to create directory')

    if xbmcvfs.exists(path):
        addon.log( name+' Already in the library' )
        notification( addon.get_name()+' allready added', name, img)
        return
    
    notification( addon.get_name()+' adding to library', name+' adding to library', img)
    strm = xbmcvfs.File(path, 'w')
    strm.write(string)
    strm.close()
    xbmc.executebuiltin("UpdateLibrary(video)")

def remfromlib( url, name, infol, img, fanart, year ):
    addon.log('Remove %s From Library' % name)
    dialog = xbmcgui.Dialog()
    ok = dialog.ok(addon.get_name(), 'Are you sure you want to [COLOR red][B]REMOVE[/COLOR][/B]', name.title(),'From XBMC/KODI library?')
    if ok:
        import shutil
        path = pathfromname(name)
        shutil.rmtree( path )
        notification( addon.get_name(), name+' Removed From library', img)
        xbmc.executebuiltin("CleanLibrary(video)")
        

    
def notification(title, message, icon):
    addon.show_small_popup( addon.get_name()+title.title(), message.title(), 5000, icon)
    return

def pathfromname(name):
    path = xbmc.translatePath( addon.get_setting('movie-folder') )
    return (xbmc.makeLegalFilename( os.path.join( path, name )))
        
    

    
def playStreamUrl( url, infol, name ):
    import requests
    addon.log('Playstream %s'%url)

    url = re.split(r'#', url, re.I)[0]
    headers = {}
    headers['User-Agent'] = User_Agent
    html = requests.get(url, headers=headers).text

    form_data={'v': re.search(r'v\=(.*?)$',url,re.I).group(1)}
    headers = {'host': 'm.afdah.org', 'content-type':'application/x-www-form-urlencoded; charset=UTF-8',
               'origin':'https://m.afdah.org', 'referer': url,
               'user-agent':'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_2 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5','x-requested-with':'XMLHttpRequest'}
    r = requests.post('https://m.afdah.org/video_info/html5', data=form_data, headers=headers)

    res_quality = []
    res_token = []
    qt = re.findall(r'\"(\d+p)\".*?(\/get_video.*?)\"', str(r.text), re.I|re.DOTALL)
    defst = re.findall(r'p\'\,\s\'(\/get_video.*?)\'', str(qt[0]), re.I|re.DOTALL)[0]

    for quality, token in qt:
        if '1080p' in quality: quality = '[COLOR blue][B]['+quality+'][/COLOR][/B]'
        elif '720p' in quality: quality = '[COLOR green][B]['+quality+'][/COLOR][/B]'
        elif '360' in quality: quality = '[COLOR red][B]['+quality+'][/COLOR][/B]'
            
        res_quality.append( quality )
        res_token.append( token )

    if len(qt) >1:
        auto = qt[1]
        addon.log('Autoplay: %s , Quality: %s' % ( auto_play, def_quality ))

        if auto_play == 'false':
            addon.log('Autoplay: False, Quality: %s' % ( def_quality ))
            dialog = xbmcgui.Dialog()
            ret = dialog.select('Select Stream Quality',res_quality)
            if ret == -1:
                return
            elif ret > -1:
                tokenurl = baseUrl+res_token[ret]
        else:
            try:
                if re.search(def_quality, str(res_quality)):
                    qual = []
                    r = re.findall(r'B\]\[(\d+p)\]\[\/C', str(res_quality))
                    if r:
                        for r in r:
                            qual.append(r)
                        
                        qual_ret = qual.index(def_quality)
                        tokenurl = baseUrl+res_token[qual_ret]
                else:
                    tokenurl = baseUrl+re.search(r'\,\s\'(.*?)\'', str(auto)).group(1)
            except Exception, e:
                addon.log('Autoplay error: %s' % str(e))
                notification( addon.get_name()+' Something went wrong', 'Playing '+name+', in lower quality', addon.get_icon())
                tokenurl = baseUrl+defst
        
                
                
    else:
        tokenurl = baseUrl+token

    headers={'accept':'*/*', 'accept-encoding':'identity;q=1, *;q=0', 'accept-language':'en-GB,en-US;q=0.8,en;q=0.6',
             'cache-control':'no-cache', 'dnt':'1', 'pragma':'no-cache', 'range':'bytes=0-','referer': str(url),
             'user-agent':'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_2 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5','x-requested-with':'XMLHttpRequest'}
    r = requests.get(tokenurl, headers=headers,allow_redirects=False)

    if r:
        t = re.search(r'(https\:\/\/redirector\.googlevideo.*?)\'',str(r.headers), re.I)

    
        if t:
            videourl = t.group(1)
        else:
            videourl = re.search(r'\s(https://.*?googleuserconten.*?)\'', str(r.headers), re.I).group(1)
            
        r = requests.get(videourl, headers={'Referer':str(url), 'user-agent':'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_2 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5','x-requested-with':'XMLHttpRequest'},
                         allow_redirects=False)
        if r:
            streamurl=r.headers['location']
            listitem = xbmcgui.ListItem(path=str(streamurl), iconImage='', thumbnailImage='')
            listitem.setProperty('IsPlayable', 'true')
            listitem.setPath(str(streamurl))
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)

            

''' Why recode whats allready written and works well,
    Thanks go to Eldrado for it '''

def setView(content, viewType):
        
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    #if addon.get_setting('auto-view') == 'true':

    #    print addon.get_setting(viewType)
    #    if addon.get_setting(viewType) == 'Info':
    #        VT = '515'
    #    elif addon.get_setting(viewType) == 'Wall':
    #        VT = '501'
    #    elif viewType == 'default-view':
    #        VT = addon.get_setting(viewType)

    #    print viewType
    #    print VT
        
    #    xbmc.executebuiltin("Container.SetViewMode(%s)" % ( int(VT) ) )

    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_PROGRAM_COUNT )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RUNTIME )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_GENRE )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_MPAA_RATING )
    

def Transform():
    if addon.get_setting('transform') == 'true':
        return
    if xbmcvfs.exists(xbmc.translatePath('special://masterprofile/sources.xml')):
        with open(xbmc.translatePath(os.path.join( addon.get_path(), 'resources', 'sourcesapp.xml'))) as f:
            sourcesapp = f.read()
            f.close()
        with open(xbmc.translatePath('special://masterprofile/sources.xml'), 'r+') as f:
            my_file = f.read()
            if re.search(r'http://transform.mega-tron.tv/', my_file):
                addon.log('Transform Source Found in sources.xml, Not adding.')
                return
            addon.log('Adding Transform source in sources.xml')
            my_file = re.split(r'</files>\n</sources>\n', my_file)
            my_file = my_file[0]+sourcesapp
            f.seek(0)
            f.truncate()
            f.write(my_file)
            f.close()
            Addon.setSetting(id='transform', value='true')
            

    else:
        xbmcvfs.copy(xbmc.translatePath(os.path.join( addon.get_path(), 'resources', 'sources.xml')),
                       xbmc.translatePath('special://masterprofile/sources.xml'))
        Addon.setSetting(id='transform', value='true')

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

params=get_params(); query=None
try: query=urllib.unquote_plus(params.get('query', ''))
except: pass



if mode == 'main':
    MAIN( menu )
elif mode == 'content':
    content( url )
elif mode == 'year':
    Year( url, name )
elif mode == 'search':
    Search( url )
elif mode == 'supersearch':
    SuperSearch( query )
elif mode == 'settings':
    settings()
elif mode == 'playtrailer':
    playtrailer( url )
elif mode == 'playstream':
    playStreamUrl( url, infol, name )
elif mode == 'add2lib':
    add2lib( url, name, infol, img, fanart, year )
elif mode == 'remromlib':
    remfromlib( url, name, infol, img, fanart, year )
    
    
    
    
elif mode == 'resolv':
    import urlresolver
    urlresolver.display_settings()
    
elif mode == 'meta':
    import metahandler
    metahandler.display_settings()
    
elif mode == 'adset':
    addon.show_settings()
    
    
    


#setView( None, 'default-view')
xbmcplugin.endOfDirectory(int(sys.argv[1]))
