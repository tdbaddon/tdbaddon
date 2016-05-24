
import re
import os
import urllib
import urllib2
import cookielib
from urlparse import urlparse, parse_qs
from traceback import format_exc

import StorageServer
from bs4 import BeautifulSoup
import xmltodict

import xbmcplugin
import xbmcgui
import xbmcaddon
import xbmcvfs

addon = xbmcaddon.Addon()
language = addon.getLocalizedString
addon_profile = xbmc.translatePath(addon.getAddonInfo('profile'))
addon_id = addon.getAddonInfo('id')
addon_version = addon.getAddonInfo('version')
icon = addon.getAddonInfo('icon')
fanart = addon.getAddonInfo('fanart')
cookie_file = os.path.join(addon_profile, 'cookie_file')
cookie_jar = cookielib.LWPCookieJar(cookie_file)
cache = StorageServer.StorageServer("testkitchen", 2)
kitchen_url = 'http://www.americastestkitchen.com'
country_url = 'http://www.cookscountry.com'
cooks_url = 'http://www.cooksillustrated.com'


def addon_log(string):
    try:
        log_message = string.encode('utf-8', 'ignore')
    except:
        log_message = 'addonException: addon_log'
    xbmc.log("[%s-%s]: %s" %(addon_id, addon_version, log_message),level=xbmc.LOGNOTICE)


def make_request(url, data=None, headers=None):
    addon_log('Request URL: %s' %url)
    if headers is None:
        headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:25.0) Gecko/20100101 Firefox/25.0',
                   'Referer' : 'http://www.americastestkitchen.com'}
    if not xbmcvfs.exists(cookie_file):
        cookie_jar.save()
    cookie_jar.load(cookie_file, ignore_discard=True, ignore_expires=True)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
    urllib2.install_opener(opener)
    try:
        req = urllib2.Request(url, data, headers)
        response = urllib2.urlopen(req)
        data = response.read()
        # addon_log(str(response.info()))
        cookie_jar.save(cookie_file, ignore_discard=False, ignore_expires=False)
        response.close()
        return data
    except urllib2.URLError, e:
        addon_log('We failed to open "%s".' %url)
        if hasattr(e, 'reason'):
            addon_log('We failed to reach a server.')
            addon_log('Reason: ', e.reason)
        if hasattr(e, 'code'):
            addon_log('We failed with error code - %s.' %e.code)


def get_soup(url):
    try:
        soup = BeautifulSoup(make_request(url), "html.parser")
        return soup
    except:
        addon_log('get_soup Exception: %s' %format_exc())
            
            
def cache_categories():
    soup = get_soup(kitchen_url + '/episodes')
    cats = {'base': kitchen_url, 'items': {}}
    items = soup.find('aside', class_='browse')('div', class_='expand')
    for i in items:
        cats['items'][i.a.string] = [(x.string, x['href']) for x in i.nav('a')]
    return repr(cats)
        
        
def cache_country_categories():
    soup = get_soup(country_url + '/episodes')
    cats = {'base': country_url, 'items': {}}
    items = soup.find('section', class_='browse')('h2')
    for i in items:
        cats['items'][i.a.string] = [(x.string, x['href']) for x in i.findNext('nav')('a')]
    return repr(cats)
    
    
def cache_cooks_categories():
    soup = get_soup(cooks_url + '/videos')
    cats = {'base': cooks_url, 'items': {}}
    items = soup.find('section', class_='browse')('h2')
    for i in items:
        cats['items'][i.a.string] = [(x.string, x['href']) for x in i.findNext('nav')('a')]
    return repr(cats)
    
    
def display_categories(cats):
    for i in cats['items'].keys():
        add_dir(i, cats['base'], 1, icon)

        
def display_category(key, url):
    if url == cooks_url:
        cats = eval(cache.cacheFunction(cache_cooks_categories))
        print cats
    elif url == kitchen_url:
        cats = eval(cache.cacheFunction(cache_categories))
    elif url == country_url:
        cats = eval(cache.cacheFunction(cache_country_categories))
    for i in cats['items'][key]:
        add_dir(i[0], cats['base'] + i[1], 2, icon)
        
        
def get_episodes(url):
    base_url = [i for i in [kitchen_url, cooks_url, country_url] if i in url][0]
    soup = get_soup(url)
    if base_url == cooks_url:
        try:
            items = soup.find('section', class_='browse-results content')('div', class_='result')
        except:
            notify('Error getting episodes')
            addon_log('addonException: %s' %format_exc())
            return
        for i in items:
            add_dir(i.a.h2.string, base_url + i.a['href'], 3, icon, False)
        return
    try:
        items = soup.find('ul', class_='figure-list')('figure')
    except:
        items = None
    if items:
        for i in items:
            try:
                title = i.find('span', class_='title').string.encode('utf-8')
            except:
                title = i.figcaption.a.string.encode('utf-8')
            thumb = 'http:' + i.img['src']
            add_dir(title, base_url + i.a['href'], 3, thumb, False)
    else:
        try:
            items = soup.find('div', class_='atk list-results')('div', class_='result')
        except:
            notify('Error getting episodes')
            return
        for i in items:
            title = i.span.string.encode('utf-8')
            add_dir(i.span.string, base_url + i.a['href'], 3, icon, False)
        
        
def resolve_url(page_url, retry=False):
    soup = get_soup(page_url)
    pattern = re.compile("VideoPlayer\('(.+?)','(.+?)', '.+?', '.+?'\);")
    pattern_1 = re.compile("VideoPlayer\('(.+?)', '(.+?)', '.+?', '.+?'\);")
    entry_id = None
    scripts = soup('script')
    for i in scripts:
        [(entry_id, iframe_id) for iframe_id, entry_id in pattern.findall(i.get_text())]
        if entry_id:
            break
    if entry_id is None:
        for i in scripts:
            [(entry_id, iframe_id) for iframe_id, entry_id in pattern_1.findall(i.get_text())]
            if entry_id:
                break
    if entry_id is None:
        if '/science/' in page_url:
            try:
                [(entry_id, iframe_id) for iframe_id, entry_id in
                    pattern.findall(soup.find('a', class_='science')['onclick'])]
                if entry_id is None:
                    [(entry_id, iframe_id) for iframe_id, entry_id in
                        pattern_1.findall(soup.find('a', class_='science')['onclick'])]
            except:
                pass
    if entry_id is None:
        addon_log('No matching pattern')
        logged_in = check_login(scripts)
        if logged_in == 'Subscription not enabled':
            notify('This video requires a subscription')
            return
        elif logged_in == 'Already logged in':
            notify('Addon Error: did not find video ID')
            return
        else:
            if not retry:
                logged_in = login(page_url)
                if logged_in:
                    addon_log('Retry after logging in')
                    return resolve_url(page_url, True)
                else:
                    return
            else:
                notify('Addon Error: did not find video ID')
                addon_log('Retry Failed: %s' %page_url)
                return
        
    smil_url = ('http://cdnapi.kaltura.com/p/1445801/sp/144580100/playManifest/entryId/%s'
                '/format/hdnetworksmil/protocol/http/cdnHost/cdnbakmi.kaltura.com/uiConfId/%s/a/a.smil?')
    data = make_request(smil_url %(entry_id, iframe_id))
    streams_dict = xmltodict.parse(data)
    server = streams_dict['smil']['head']['meta'][1]['@content']
    items = [(i['@src'], i['@system-bitrate']) for i in streams_dict['smil']['body']['switch']['video']]
    preferred_rate = addon.getSetting('preferred_rate')
    selected = None
    if preferred_rate == '0':
        selected = items[0][0]
    elif preferred_rate == '3':
        selected = items[-1][0]
    elif preferred_rate == '2':
        selected = items[-2][0]
    elif preferred_rate == '1':
        if len(items) >= 4:
            selected = items[-3][0]
        else:
            selected = items[-2][0]
    else:
        dialog = xbmcgui.Dialog()
        ret = dialog.select(language(30010), [language(30009) + i[1] for i in items])
        if ret > -1:
            selected = items[ret][0]
    if selected:
        return 'http://cdnbakmi.kaltura.com' + selected.split('forceproxy/true')[0] + 'name/a.mp4'
    
    
def notify(message):
    xbmc.executebuiltin("XBMC.Notification(%s, %s, 10000, %s)" %('Addon Notification', message, icon))


def get_params():
    p = parse_qs(sys.argv[2][1:])
    for i in p.keys():
        p[i] = p[i][0]
    return p

        
def add_dir(name, url, mode, iconimage, isfolder=True):
    params = {'name': name, 'url': url, 'mode': mode}
    url = '%s?%s' %(sys.argv[0], urllib.urlencode(params))
    listitem = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    listitem.setProperty( "Fanart_Image", fanart )
    infolabels = {"Title": name}
    if not isfolder:
        listitem.setProperty('IsPlayable', 'true')
    listitem.setInfo(type="Video", infoLabels=infolabels)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), url, listitem, isfolder)

    
def login(page_url):
    addon_log('Attempting login')
    base_urls = [kitchen_url, country_url, cooks_url]
    login_base = [i for i in base_urls if i in page_url][0].replace('http:', 'https:')
    soup = get_soup(login_base + '/sign_in')
    header = soup.find('div', class_='header', text='Sign into your account')
    items = header.findAllNext('input')
    post_data = {'user[password]': addon.getSetting('password'),
                 'user[email]': addon.getSetting('email')}
    for i in items:
        if i.has_key('name') and i['name'] == 'authenticity_token':
            post_data['authenticity_token'] = i['value'].encode('utf8')
        if i.has_key('name') and i['name'] == 'utf8':
            post_data['utf8'] = i['value'].encode('utf8')
    if post_data.has_key('authenticity_token'):
        post_url = login_base + '/sessions'
        login_data = make_request(post_url, urllib.urlencode(post_data))
        pattern = re.compile("\'email\': \'(.+?)\',\n      \'user_id\': \'(.+?)\',\n")
        [(email, userId) for email, userId in pattern.findall(login_data)]
        if userId and len(userId) > 0:
            addon_log('Logged in successfully')
            return True
        else:
            addon_log('Login Failed')
            notify('Login Failed')
            xbmc.sleep(5000)
    else:
        addon_log('Failed to get the authenticity_token')
            
            
def check_login(page_url):
    addon_log('Checking login')
    if addon.getSetting('sub_type') == 'false':
        logged_in = 'Subscription not enabled'
    else:
        cookie_jar.load(cookie_file, ignore_discard=False, ignore_expires=False)
        logged_in = False
        for i in cookie_jar:
            addon_log('%s: %s' %(i.name, i.domain))
            if i.name == 'auth_token' and i.domain in page_url:
                logged_in = 'Already logged in'
                break
        if not logged_in:
            logged_in = 'Not logged in'
    addon_log(logged_in)
    return logged_in


if not xbmcvfs.exists(addon_profile):
    xbmcvfs.mkdir(addon_profile)
    
params = get_params()

try:
    mode = int(params['mode'])
except:
    mode = None

addon_log(repr(params))

if mode == None:
    cats = eval(cache.cacheFunction(cache_categories))
    display_categories(cats)
    add_dir('Cooks Country', 'get_country', 4, icon)
    add_dir('Cooks Illustrated', 'get_cooks', 5, icon)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode == 1:
    display_category(params['name'], params['url'])
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
elif mode == 2:
    get_episodes(params['url'])
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode == 3:
    success = False
    resolved_url = resolve_url(params['url'])
    if resolved_url:
        success = True
    else:
        resolved_url = ''
    item = xbmcgui.ListItem(path=resolved_url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), success, item)

elif mode == 4:
    cats = eval(cache.cacheFunction(cache_country_categories))
    display_categories(cats)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode == 5:
    display_category('Browse Videos', cooks_url)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))