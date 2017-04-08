'''
Created on Dec 17, 2013

@author: ajdeveloped@gmail.com

This file is part of XOZE. 

XOZE is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

XOZE is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with XOZE.  If not, see <http://www.gnu.org/licenses/>.
'''

import base64
import logging
import pickle
import re
import time
import urllib

import BeautifulSoup

import xbmc  # @UnresolvedImport
import xbmcgui  # @UnresolvedImport
from xoze.context import AddonContext, SnapVideo
from xoze.snapvideo import WatchVideo2US, VideoWeed, CloudEC, LetWatch, PlayU, \
    TVLogy, Playwire, Streamin, Watchers, VidWatch
from xoze.utils import file, http, jsonfile
from xoze.utils.cache import CacheManager
from xoze.utils.http import HttpClient


DIRECT_CHANNELS = {"Awards & Concerts":{"iconimage":"Awards.jpg",
                   "channelType": "IND",
                   "tvshow_episodes_url": "/forums/36-Awards-Performances-Concerts"},
                   "Latest & Exclusive Movies":{"iconimage":"Movies.jpeg",
                   "channelType": "IND",
                   "tvshow_episodes_url": "/forums/20-Latest-Exclusive-Movie-HQ"}}
 
LIVE_CHANNELS = {"9XM":{"iconimage":"http://www.lyngsat.com/logo/tv/num/9x_music.png|Referer=http://www.lyngsat.com/",
                        "channelType": "IND",
                        "channelUrl": "http://ind19-lh.akamaihd.net/i/ind19_9xm@440010/master.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"},
                 "9XJhakaas":{"iconimage":"http://www.lyngsat.com/logo/tv/num/9x_jhakaas.png|Referer=http://www.lyngsat.com/",
                        "channelType": "IND",
                        "channelUrl": "http://ind28-lh.akamaihd.net/i/ind28_9xjhakaas@424619/master.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"},
                 "Aajtak":{"iconimage":"http://www.lyngsat.com/logo/tv/aa/aaj_tak.png|Referer=http://lyngsat.com",
                        "channelType": "IND",
                        "channelUrl": "http://vidgyor.com/prod/aajtak/aajtak_auth.json"},
                 "9XTashan":{"iconimage":"https://www.lyngsat.com/logo/tv/num/9x_tashan.png|Referer=http://www.lyngsat.com/",
                        "channelType": "IND",
                        "channelUrl": "http://ind28-lh.akamaihd.net/i/ind28_9xtashan@424619/master.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"},
                 "IBN7": {"iconimage":"http://www.lyngsat.com/logo/tv/ii/ibn7.png|Referer=http://www.lyngsat.com/",
                          "channelType": "IND",
                          "channelUrl": "http://ibn7_hls-lh.akamaihd.net/i/ibn7_hls_n_1@174951/index_3_av-b.m3u8?sd=10&play-only=backup&rebase=on|User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"},
                 "India TV": {"iconimage":"http://www.lyngsat.com/logo/tv/ii/india_tv_in.png|Referer=http://www.lyngsat.com/",
                              "channelType": "IND",
                              "channelUrl": "http://indiatvnews-lh.akamaihd.net/i/ITV_1@199237/master.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"},
                 "NDTV 24x7": {"iconimage":"http://www.lyngsat.com/logo/tv/nn/ndtv_24x7.png|Referer=http://www.lyngsat.com/",
                              "channelType": "IND",
                              "channelUrl": "http://ndtvstream-lh.akamaihd.net/i/ndtv_24x7_1@300633/master.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"},
                 "NDTV India": {"iconimage":"http://www.lyngsat.com/logo/tv/nn/ndtv_india.png|Referer=http://www.lyngsat.com/",
                              "channelType": "IND",
                              "channelUrl": "http://ndtvstream-lh.akamaihd.net/i/ndtv_india_1@300634/master.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"},
                 "NDTV Prime": {"iconimage":"http://www.lyngsat.com/logo/tv/nn/ndtv_prime.png|Referer=http://www.lyngsat.com/",
                              "channelType": "IND",
                              "channelUrl": "http://ndtvstream-lh.akamaihd.net/i/ndtv_profit_1@300635/master.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"},
                 "NDTV GoodTimes": {"iconimage":"http://www.lyngsat.com/logo/tv/nn/ndtv_good_times.png|Referer=http://www.lyngsat.com/",
                              "channelType": "IND",
                              "channelUrl": "http://ndtv.live-s.cdn.bitgravity.com/cdn-live-b3/_definst_/ndtv/live/ndtvgoodtime.smil/playlist.m3u8"}
                 }

BASE_WSITE_URL = base64.b64decode('aHR0cDovL3d3dy5kZXNpdHZib3gubmV0')
    
def check_cache(req_attrib, modelMap):
    logging.getLogger().debug('DTB - Check cache ***********************')
    logging.getLogger().debug(req_attrib)
    refresh_cache = True
    context = AddonContext()
    filepath = file.resolve_file_path(context.get_addon_data_path(), extraDirPath='data', filename='DTB_Channels.json', makeDirs=True)
    refresh = context.get_addon().getSetting('dtbForceRefresh')
    if refresh == None or refresh != 'true':
        modified_time = file.get_last_modified_time(filepath)
        if modified_time is not None:
            diff = long((time.time() - modified_time) / 3600)
            if diff < 720:
                refresh_cache = False
            else:
                logging.getLogger().debug('DTB_Channels.json was last created 30 days ago, refreshing data.')
    else:
        logging.getLogger().debug('Request to force refresh.')
    modelMap['refresh_cache'] = refresh_cache
    modelMap['cache_filepath'] = filepath


def refresh_cache(req_attrib, modelMap):
    if not modelMap['refresh_cache']:
        return
    logging.getLogger().debug('Reloading cache...')
    
    tv_data = {"channels": {"Star Plus":
                  {"iconimage":"http://www.lyngsat.com/logo/tv/ss/star_plus_hk.png|Referer=http://www.lyngsat.com/",
                   "channelType": "IND",
                   "running_tvshows_url": "/star-plus/"},
                  "Zee TV":
                  {"iconimage":"http://www.lyngsat.com/logo/tv/zz/zee_tv_in.png|Referer=http://www.lyngsat.com/",
                   "channelType": "IND",
                   "running_tvshows_url": "/zee-tv/"},
                  "Sony TV":
                  {"iconimage":"http://www.lyngsat.com/logo/tv/ss/set_asia.png|Referer=http://www.lyngsat.com/",
                   "channelType": "IND",
                   "running_tvshows_url": "/sony-tv/"},
                  "Sony Pal":
                  {"iconimage":"http://www.lyngsat.com/logo/tv/ss/sony_pal_in.png|Referer=http://www.lyngsat.com/",
                   "channelType": "IND",
                   "running_tvshows_url": "/sony-pal/"},
                  "Life OK":
                  {"iconimage":"http://www.lyngsat.com/logo/tv/ll/life_ok_in.png|Referer=http://www.lyngsat.com/",
                   "channelType": "IND",
                   "running_tvshows_url": "/life-ok/"},
                  "Sahara One":
                  {"iconimage":"http://www.lyngsat.com/logo/tv/ss/sahara_one_in.png|Referer=http://www.lyngsat.com/",
                   "channelType": "IND",
                   "running_tvshows_url": "/sahara-one/"},
                  "Colors TV":
                  {"iconimage":"http://www.lyngsat.com/logo/tv/cc/colors_in.png|Referer=http://www.lyngsat.com/",
                   "channelType": "IND",
                   "running_tvshows_url": "/color-tv/"},
                  "Sab TV":
                  {"iconimage":"http://www.lyngsat.com/logo/tv/ss/sony_sab_tv_in.png|Referer=http://www.lyngsat.com/",
                   "channelType": "IND",
                   "running_tvshows_url": "/sab-tv/"},
                  "&TV":
                  {"iconimage":"http://www.lyngsat.com/logo/tv/aa/and_tv_in.png|Referer=http://www.lyngsat.com/",
                   "channelType": "IND",
                   "running_tvshows_url": "/and-tv/"},
                  "MTV":
                  {"iconimage":"http://www.lyngsat.com/logo/tv/mm/mtv_us.png|Referer=http://www.lyngsat.com/",
                   "channelType": "IND",
                   "running_tvshows_url": "/mtv-channel/"},
                  "Bindass TV":
                  {"iconimage":"http://www.lyngsat.com/logo/tv/bb/bindass_in.png|Referer=http://www.lyngsat.com/",
                   "channelType": "IND",
                   "running_tvshows_url": "/utv-bindass/"},
                  "Channel [V]":
                  {"iconimage":"http://www.lyngsat.com/logo/tv/cc/channel_v_in.png|Referer=http://www.lyngsat.com/",
                   "channelType": "IND",
                   "running_tvshows_url": "/channel-v/"},
                  "Zindagi TV":
                  {"iconimage":"http://www.lyngsat.com/logo/tv/zz/zee_zindagi_in.png|Referer=http://www.lyngsat.com/",
                   "channelType": "IND",
                   "running_tvshows_url": "/zindagi/"}
                }
            }
    current_index = 0
    tv_channels = tv_data['channels']
    total_iteration = len(tv_channels)
    progress_bar = modelMap['progress_control']
    channel_image = modelMap['channel_image_control']
    for tv_channel_name, tv_channel in tv_channels.iteritems():
        logging.getLogger().debug('About to retrieve tv shows for channel %s' % tv_channel_name)
        channel_image.setImage(tv_channel['iconimage'])
        channel_image.setVisible(True)
        loaded_tv_channel = __retrieve_channel_tv_shows__(tv_channel_name, tv_channel['running_tvshows_url'])
        tv_channel["running_tvshows"] = loaded_tv_channel["running_tvshows"]
        tv_channel["finished_tvshows"] = loaded_tv_channel["finished_tvshows"]
        channel_image.setVisible(False)
        current_index = current_index + 1
        percent = (current_index * 100) / total_iteration
        progress_bar.setPercent(percent)
        
    status = jsonfile.write_file(modelMap['cache_filepath'], tv_data)
    if status is not None:
        logging.getLogger().debug('Saved status = ' + str(status))
    CacheManager().put('dtb_tv_data', tv_data)
    AddonContext().get_addon().setSetting('dtbForceRefresh', 'false')
    
CHANNEL_TYPE_IND = 'IND'
CHANNEL_TYPE_PAK = 'PAK'

def load_channels(req_attrib, modelMap):
    logging.getLogger().debug('load channels...')
    tv_channels = _read_tv_channels_cache_(modelMap['cache_filepath'])['channels']
    
    tv_channel_items = []
    live_tv_channel_items = []
    
    display_channel_type = 1
    
    live_channels_all = {}
    live_channels_all.update(LIVE_CHANNELS)
    
    live_filepath = file.resolve_file_path(AddonContext().get_addon_data_path(), extraDirPath='data', filename='Live.json', makeDirs=True)
    live_file_channels = _read_live_tv_channels_cache_(live_filepath)
    if live_file_channels is not None:
        live_channels_all.update(live_file_channels)
    
    channel_names = live_channels_all.keys()
    channel_names.sort()
    for channel_name in channel_names:
        channel_obj = live_channels_all[channel_name]
        if((display_channel_type == 1 and channel_obj['channelType'] == CHANNEL_TYPE_IND)  or (display_channel_type == 0)):
            item = xbmcgui.ListItem(label=channel_name, iconImage=channel_obj['iconimage'], thumbnailImage=channel_obj['iconimage'])
            item.setProperty('channel-name', channel_name)
            item.setProperty('live-link', 'true')
            item.setProperty('direct-link', 'false')
            live_tv_channel_items.append(item)
    
    for channel_name in DIRECT_CHANNELS:
        channel_obj = DIRECT_CHANNELS[channel_name]
        if((display_channel_type == 1 and channel_obj['channelType'] == CHANNEL_TYPE_IND)  or (display_channel_type == 0)):
            item = xbmcgui.ListItem(label=channel_name, iconImage=channel_obj['iconimage'], thumbnailImage=channel_obj['iconimage'])
            item.setProperty('channel-name', channel_name)
            item.setProperty('direct-link', 'true')
            item.setProperty('live-link', 'false')
            tv_channel_items.append(item)
    
    channel_names = tv_channels.keys()
    channel_names.sort()
    for channel_name in channel_names:
        channel_obj = tv_channels[channel_name]
        if ((display_channel_type == 1 and channel_obj['channelType'] == CHANNEL_TYPE_IND) 
            or (display_channel_type == 2 and channel_obj['channelType'] == CHANNEL_TYPE_PAK) 
            or (display_channel_type == 0)):
            
            item = xbmcgui.ListItem(label=channel_name, iconImage=channel_obj['iconimage'], thumbnailImage=channel_obj['iconimage'])
            item.setProperty('channel-name', channel_name)
            item.setProperty('direct-link', 'false')
            item.setProperty('live-link', 'false')
            tv_channel_items.append(item)
     
    modelMap['tv_channel_items'] = tv_channel_items
    modelMap['live_tv_channel_items'] = live_tv_channel_items
    

def load_favorite_tv_shows(req_attrib, modelMap):
    context = AddonContext()
    filepath = file.resolve_file_path(context.get_addon_data_path(), extraDirPath='data', filename='DTB_Favorites.json', makeDirs=False)
    logging.getLogger().debug('loading favorite tv shows from file : %s' % filepath)
    favorite_tv_shows = _read_favorite_tv_shows_cache_(filepath)
    if favorite_tv_shows is None:
        return
    favorite_tv_shows_items = []
    tv_show_names = favorite_tv_shows.keys()
    tv_show_names.sort()
    for tv_show_name in tv_show_names:
        favorite_tv_show = favorite_tv_shows[tv_show_name]
        item = xbmcgui.ListItem(label=tv_show_name, iconImage=favorite_tv_show['tv-show-thumb'], thumbnailImage=favorite_tv_show['tv-show-thumb'])
        item.setProperty('channel-type', favorite_tv_show['channel-type'])
        item.setProperty('channel-name', favorite_tv_show['channel-name'])
        item.setProperty('tv-show-name', tv_show_name)
        item.setProperty('tv-show-url', favorite_tv_show['tv-show-url'])
        item.setProperty('tv-show-thumb', favorite_tv_show['tv-show-thumb'])
        favorite_tv_shows_items.append(item)
        
    modelMap['favorite_tv_shows_items'] = favorite_tv_shows_items
    
def determine_direct_tv_channel(req_attrib, modelMap):
    if(req_attrib['direct-link'] == 'true'):
        logging.getLogger().debug('found direct channel redirect...')
        return 'redirect:dr-displayDirectChannelEpisodesList'
    
def determine_live_tv_channel(req_attrib, modelMap):
    if(req_attrib['live-link'] == 'true'):
        logging.getLogger().debug('found live channel redirect...')
        return 'redirect:dtb-watchLiveChannel'
    

def load_tv_shows(req_attrib, modelMap):
    logging.getLogger().debug('load tv shows...')
    
    tv_channels = CacheManager().get('dtb_tv_data')['channels']
    channel_name = req_attrib['channel-name']
    tv_channel = tv_channels[channel_name]
    channel_type = tv_channel['channelType']
    modelMap['channel_image'] = tv_channel['iconimage']
    modelMap['channel_name'] = channel_name
    selected_tv_show_name = ''
    if req_attrib.has_key('tv-show-name'):
        selected_tv_show_name = req_attrib['tv-show-name']
    tv_show_items = []
    index = 0
    if tv_channel.has_key('running_tvshows'):
        tv_shows = tv_channel['running_tvshows']
        logging.getLogger().debug('total tv shows to be displayed: %s' % str(len(tv_shows)))
        index = _prepare_tv_show_items_(tv_shows, channel_type, channel_name, selected_tv_show_name, tv_show_items, False, modelMap, index)
    
    hideFinishedShow = AddonContext().get_addon().getSetting('drHideFinished')
    
    if tv_channel.has_key('finished_tvshows') and hideFinishedShow is not None and hideFinishedShow == 'false':
        tv_shows = tv_channel["finished_tvshows"]
        logging.getLogger().debug('total finsihed tv shows to be displayed: %s' % str(len(tv_shows)))
        index = _prepare_tv_show_items_(tv_shows, channel_type, channel_name, selected_tv_show_name, tv_show_items, True, modelMap, index)
        
    modelMap['tv_show_items'] = tv_show_items
    
def load_direct_link_channel(req_attrib, modelMap):
    channel_name = req_attrib['channel-name']
    tv_channel = DIRECT_CHANNELS[channel_name]
    
    modelMap['channel_image'] = tv_channel['iconimage']
    modelMap['channel_name'] = channel_name
    
    req_attrib['tv-show-url'] = BASE_WSITE_URL + tv_channel['tvshow_episodes_url']
    req_attrib['tv-show-name'] = ''
    req_attrib['channel-type'] = tv_channel['channelType']
    

def re_me(data, re_patten):
    match = ''
    m = re.search(re_patten, data)
    if m != None:
        match = m.group(1)
    else:
        match = ''
    return match       
    
def watch_live(req_attrib, modelMap):
    channel_name = req_attrib['channel-name']
    
    live_filepath = file.resolve_file_path(AddonContext().get_addon_data_path(), extraDirPath='data', filename='Live.json', makeDirs=True)
    live_file_channels = _read_live_tv_channels_cache_(live_filepath)
    tv_channel = None
    if LIVE_CHANNELS.has_key(channel_name):
        tv_channel = LIVE_CHANNELS[channel_name]
    if live_file_channels is not None and live_file_channels.has_key(channel_name):
        tv_channel = live_file_channels[channel_name]
        
    item = xbmcgui.ListItem(label=channel_name, iconImage=tv_channel['iconimage'], thumbnailImage=tv_channel['iconimage'])
    if 'aajtak' in tv_channel['channelUrl']:
        html = HttpClient().get_html_content(url=tv_channel['channelUrl'])
        token = re.compile('\"token\"\:\"(.+?)\"').findall(html)[0]
        finalLink = "http://atcdn.vidgyor.com/at-origin/mobilelive/playlist.m3u8" + token
        item.setProperty('streamLink', finalLink)
    else:
        item.setProperty('streamLink', tv_channel['channelUrl'])

    modelMap['live_item'] = item
    
def _prepare_tv_show_items_(tv_shows, channel_type, channel_name, selected_tv_show_name, tv_show_items, is_finished_shows, modelMap, index):
    tv_shows.sort()
    for tv_show in tv_shows:
        name = tv_show['name']
        if is_finished_shows:
            name = name + ' [COLOR gray]finished[/COLOR]'
        item = xbmcgui.ListItem(label=name)
        item.setProperty('channel-type', channel_type)
        item.setProperty('channel-name', channel_name)
        item.setProperty('tv-show-name', name)
        if is_finished_shows:
            item.setProperty('tv-show-finished', 'true')
        else:
            item.setProperty('tv-show-finished', 'false')
        item.setProperty('tv-show-url', tv_show['url'])
        tv_show_items.append(item)
        if selected_tv_show_name == name:
            modelMap['selected_tv_show_item'] = index
        index = index + 1
    return index

def empty_function(req_attrib, modelMap):
    return

def add_tv_show_favorite(req_attrib, modelMap):
    logging.getLogger().debug('add tv show favorite...')
    tv_show_url = req_attrib['tv-show-url']
    tv_show_name = req_attrib['tv-show-name']
    tv_show_thumb = req_attrib['tv-show-thumb']
    channel_type = req_attrib['channel-type']
    channel_name = req_attrib['channel-name']
    logging.getLogger().debug('add tv show favorite...' + tv_show_url)
    
    favorites = CacheManager().get('dtb_tv_favorites')
    if favorites is None:
        favorites = {}
    elif favorites.has_key(tv_show_name):
        favorites.pop(tv_show_name)
    
    favorites[tv_show_name] = {'tv-show-name':tv_show_name, 'tv-show-thumb':tv_show_thumb, 'tv-show-url':tv_show_url, 'channel-name':channel_name, 'channel-type':channel_type}
    context = AddonContext()
    filepath = file.resolve_file_path(context.get_addon_data_path(), extraDirPath='data', filename='DTB_Favorites.json', makeDirs=False)
    logging.getLogger().debug(favorites)
    _write_favorite_tv_shows_cache_(filepath, favorites)
    
    notification = "XBMC.Notification(%s,%s,%s,%s)" % (tv_show_name, 'ADDED TO FAVORITES', 2500, tv_show_thumb)
    xbmc.executebuiltin(notification)
    
def load_remove_tv_show_favorite(req_attrib, modelMap):
    logging.getLogger().debug('load remove tv show favorite...')
    modelMap['tv-show-name'] = req_attrib['tv-show-name']
    modelMap['tv-show-thumb'] = req_attrib['tv-show-thumb']
    logging.getLogger().debug('display remove tv show favorite...')

    
def remove_favorite(req_attrib, modelMap):
    logging.getLogger().debug('remove tv show favorite...')
    favorite = CacheManager().get('selected_favorite')
    favorite_thumb = CacheManager().get('selected_favorite_thumb')
    favorites = CacheManager().get('dtb_tv_favorites')
    if favorites is None:
        favorites = {}
    elif favorites.has_key(favorite):
        favorites.pop(favorite)
    
    context = AddonContext()
    filepath = file.resolve_file_path(context.get_addon_data_path(), extraDirPath='data', filename='DTB_Favorites.json', makeDirs=False)
    logging.getLogger().debug(favorites)
    _write_favorite_tv_shows_cache_(filepath, favorites)
    
    notification = "XBMC.Notification(%s,%s,%s,%s)" % (favorite, 'REMOVED FAVORITE', 2500, favorite_thumb)
    xbmc.executebuiltin(notification)
    
    modelMap['reload_favorite_tv_shows_items'] = True
    if len(favorites) > 0:
        favorite_tv_shows_items = []
        for tv_show_name in favorites:
            favorite_tv_show = favorites[tv_show_name]
            item = xbmcgui.ListItem(label=tv_show_name, iconImage=favorite_tv_show['tv-show-thumb'], thumbnailImage=favorite_tv_show['tv-show-thumb'])
            item.setProperty('channel-type', favorite_tv_show['channel-type'])
            item.setProperty('channel-name', favorite_tv_show['channel-name'])
            item.setProperty('tv-show-name', tv_show_name)
            item.setProperty('tv-show-url', favorite_tv_show['tv-show-url'])
            item.setProperty('tv-show-thumb', favorite_tv_show['tv-show-thumb'])
            favorite_tv_shows_items.append(item)
            
        modelMap['favorite_tv_shows_items'] = favorite_tv_shows_items
    
    
def load_tv_show_episodes(req_attrib, modelMap):
    logging.getLogger().debug('load tv show episodes...')
    url = req_attrib['tv-show-url']
    tv_show_url = req_attrib['tv-show-url']
    tv_show_name = req_attrib['tv-show-name']
    channel_type = req_attrib['channel-type']
    channel_name = req_attrib['channel-name']
    currentPage = 1
    
    if req_attrib.has_key('tv-show-page') and req_attrib['tv-show-page'] != '':
        currentPage = int(req_attrib['tv-show-page'])
        if currentPage != 1:
            url = url + 'page/' + req_attrib['tv-show-page'] + '/'
    logging.getLogger().debug('load tv show episodes...' + url)
    contentDiv = BeautifulSoup.SoupStrainer('div', {'class':'item_content'})
    soup = HttpClient().get_beautiful_soup(url=url + '?tag=video', parseOnlyThese=contentDiv)
#     soup = BeautifulSoup.BeautifulSoup(HttpClient().get_html_content(url=url)).findAll('div', {'id':'contentBody'})[0]
    
    tv_show_episode_items = []
    
    threads = soup.findAll('h4')
    tv_show_episode_items.extend(__retrieveTVShowEpisodes__(threads, tv_show_name, channel_type, channel_name))
    logging.getLogger().debug('In DTB: total tv show episodes: %s' % str(len(tv_show_episode_items)))
    
    pagesDiv = soup.findChild('p', {'class':'pagination'})
    if pagesDiv is not None:
        pagesInfoTags = pagesDiv.findAllNext('a')
        for pagesInfoTag in pagesInfoTags:
            logging.getLogger().debug(pagesInfoTag)
            pageInfo = re.compile('page/(.+?)/').findall(pagesInfoTag['href'])
            
            if len(pageInfo) > 0:
                if re.search('Old', pagesInfoTag.getText(), re.IGNORECASE):
                    item = xbmcgui.ListItem(label='<< Older Entries')
                elif re.search('Next', pagesInfoTag.getText(), re.IGNORECASE):
                    item = xbmcgui.ListItem(label='Next Entries >>')
                item.setProperty('tv-show-page', pageInfo[0][0])
                item.setProperty('channel-type', channel_type)
                item.setProperty('channel-name', channel_name)
                item.setProperty('tv-show-name', tv_show_name)
                item.setProperty('tv-show-url', tv_show_url)
                tv_show_episode_items.append(item)
            else:
                item = xbmcgui.ListItem(label='Newest Entries >>')
                item.setProperty('tv-show-page', '1')
                item.setProperty('channel-type', channel_type)
                item.setProperty('channel-name', channel_name)
                item.setProperty('tv-show-name', tv_show_name)
                item.setProperty('tv-show-url', tv_show_url)
                tv_show_episode_items.append(item)
    
    modelMap['tv_show_episode_items'] = tv_show_episode_items
    

def __retrieveTVShowEpisodes__(threads, tv_show_name, channel_type, channel_name):
    tv_show_episode_items = []
    logging.getLogger().debug(threads)
    if threads is None:
        return []
    for thread in threads:
        aTag = thread.findNext('a')
        episodeName = aTag.getText()
        titleInfo = http.unescape(episodeName)
        titleInfo = titleInfo.replace(tv_show_name, '')
        titleInfo = titleInfo.replace('Full Episode Watch Online', '')
        titleInfo = titleInfo.replace('Watch Online', '')
        titleInfo = titleInfo.strip()

        item = xbmcgui.ListItem(label=titleInfo)
        
        episode_url = str(aTag['href'])
        if not episode_url.lower().startswith(BASE_WSITE_URL):
            if episode_url[0] != '/':
                episode_url = '/' + episode_url
            episode_url = BASE_WSITE_URL + episode_url
        item.setProperty('tv-show-name', tv_show_name)
        item.setProperty('channel-type', channel_type)
        item.setProperty('channel-name', channel_name)
        item.setProperty('episode-name', titleInfo)
        item.setProperty('episode-url', episode_url)
        tv_show_episode_items.append(item)
        
    return tv_show_episode_items


def determine_tv_show_episode_videos(req_attrib, modelMap):
    logging.getLogger().debug('determine tv show episode videos...')
    if req_attrib['episode-url'] is None or req_attrib['episode-url'] == '':
        return 'redirect:dtb-displayShowEpisodesList'

def load_tv_show_episode_videos(req_attrib, modelMap):
    logging.getLogger().debug('load tv show episode videos...')
    list_items = _retrieve_video_links_(req_attrib, modelMap)
    
    ''' Following new cool stuff is to get Smart Direct Play Feature'''
    playNowItem = __findPlayNowStream__(list_items)
    logging.getLogger().debug('found play now stream... ')
    modelMap['selected-playlist-item'] = playNowItem['selected']
    modelMap['backup-playlist-item'] = playNowItem['backup']
    
def load_tv_show_episode_videos_list(req_attrib, modelMap):
    logging.getLogger().debug('load tv show episode videos list...')
    list_items = _retrieve_video_links_(req_attrib, modelMap)
    modelMap['videos-item-list'] = list_items

def load_selected_playlist_streams(req_attrib, modelMap):
    selected_playlist_item = modelMap['selected-playlist-item']
    video_items = None
    if selected_playlist_item is not None:
        selected_playlist = selected_playlist_item.getProperty('videoPlayListItemsKey')
        logging.getLogger().debug('load selected playlist streams... %s' % selected_playlist)
        playlist_items = modelMap[selected_playlist]
        try:
            video_items = _retrieve_playlist_streams_(modelMap['progress_control'], playlist_items)
        except:
            modelMap['progress_control'].setPercent(0)
            pass
    if video_items is None:
        backup_playlist_item = modelMap['backup-playlist-item']
        backup_playlist = backup_playlist_item.getProperty('videoPlayListItemsKey')
        logging.getLogger().debug('load backup playlist streams... %s' % backup_playlist)
        playlist_items = modelMap[backup_playlist]
        video_items = _retrieve_playlist_streams_(modelMap['progress_control'], playlist_items)
    
    modelMap['video_streams'] = video_items
    
    
def _retrieve_playlist_streams_(progress_bar, playlist_items):
    lazyLoadStream = AddonContext().get_addon().getSetting('drLazyLoadStream')
    current_index = 1
    total_iteration = len(playlist_items)
    video_items = []
    for item in playlist_items:
        logging.getLogger().debug('About to retrieve video link %s' % item)
        video_item = None
        if lazyLoadStream is None or lazyLoadStream == 'false':
            video_item = SnapVideo().resolveVideoStream(item['videoLink'])
        else:
            video_item = _create_video_stream_item(item['videoLink'], str(current_index))
        video_items.append(video_item)
        percent = (current_index * 100) / total_iteration
        progress_bar.setPercent(percent)
        current_index = current_index + 1
    return video_items


def load_selected_video_playlist_streams(req_attrib, modelMap):
    progress_bar = req_attrib['progress_control']
    progress_bar.setPercent(0)
    video_items = None
    if req_attrib['is-playlist'] == 'true':
        playlist_items = pickle.loads(req_attrib['videos'])
        video_items = _retrieve_playlist_streams_(progress_bar, playlist_items)
    else:
        video_items = []
        video_item = SnapVideo().resolveVideoStream(req_attrib['video-link'])
        video_items.append(video_item)
        progress_bar.setPercent(100)
    modelMap['video_streams'] = video_items
    
    
def _create_video_stream_item(videoLink, inx=''):
    videoHostingInfo = SnapVideo().findVideoHostingInfo(videoLink)
    label = videoHostingInfo.get_name() + inx
    item = xbmcgui.ListItem(label=label, iconImage=videoHostingInfo.get_icon(), thumbnailImage=videoHostingInfo.get_icon())
    item.setProperty('streamLink', 'plugin://plugin.video.tvondesizonexl/?videoLink=' + urllib.quote_plus(videoLink))
    return item


def _read_tv_channels_cache_(filepath):
    tv_data = CacheManager().get('dtb_tv_data')
    if tv_data is None:
        tv_data = jsonfile.read_file(filepath)
        CacheManager().put('dtb_tv_data', tv_data)
    return tv_data

def _read_live_tv_channels_cache_(filepath):
    live_tv_data = CacheManager().get('live_tv_data')
    if live_tv_data is None:
        live_tv_data = jsonfile.read_file(filepath)
        CacheManager().put('live_tv_data', live_tv_data)
    return live_tv_data

def _read_favorite_tv_shows_cache_(filepath):
    favorites = CacheManager().get('dtb_tv_favorites')
    if favorites is None:
        favorites = jsonfile.read_file(filepath)
        CacheManager().put('dtb_tv_favorites', favorites)
    return favorites

def _write_favorite_tv_shows_cache_(filepath, data):
    CacheManager().put('dtb_tv_favorites', data)
    jsonfile.write_file(filepath, data)


def __retrieve_tv_shows__(tv_channel_url):
    tv_channel = {}
    tv_channel["running_tvshows"] = []
    tv_channel["finished_tvshows"] = []
    
    logging.getLogger().debug('TV Channel URL: ' + tv_channel_url)
    tv_shows = tv_channel["running_tvshows"]
    if tv_channel_url is None:
        return tv_shows
    tv_channel_url = BASE_WSITE_URL + tv_channel_url
    logging.getLogger().debug(tv_channel_url)
    contentDiv = BeautifulSoup.SoupStrainer('li', {'class': re.compile(r'\bcat-item cat-item-\b')})
    soup = HttpClient().get_beautiful_soup(url=tv_channel_url, parseOnlyThese=contentDiv)
#     soup = BeautifulSoup.BeautifulSoup(HttpClient().get_html_content(url=tv_channel_url)).findAll('div', {'id':'forumbits', 'class':'forumbits'})[0]
    for title_tag in soup.findAll('li'):
        aTag = title_tag.findNext('a')
        tv_show_url = str(aTag['href'])
        if tv_show_url[0:4] != "http":
            tv_show_url = BASE_WSITE_URL + '/' + tv_show_url
        tv_show_name = aTag.getText()
        if not re.search('-completed-shows', tv_show_url, re.IGNORECASE):
            tv_shows.append({"name":http.unescape(tv_show_name), "url":tv_show_url, "iconimage":""})
        else:
            tv_shows = tv_channel["finished_tvshows"]
    return tv_channel
    
    
def __retrieve_channel_tv_shows__(tv_channel_name, tv_channel_url):
    tv_channel = {}
    try:
        tv_channel = __retrieve_tv_shows__(tv_channel_url)
        if(len(tv_channel["running_tvshows"]) == 0):
            tv_channel["running_tvshows"].append({"name":"ERROR: UNABLE TO LOAD. Share message on http://forum.xbmc.org/showthread.php?tid=115583", "url":BASE_WSITE_URL + tv_channel["running_tvshows_url"]})
    except Exception, e:
        logging.getLogger().exception(e)
        logging.getLogger().debug('Failed to load a channel <%s>. continue retrieval of next tv show' % tv_channel_name)
    return tv_channel


def _retrieve_video_links_(req_attrib, modelMap):
    
    modelMap['channel-name'] = req_attrib['channel-name']
    modelMap['tv-show-name'] = req_attrib['tv-show-name']
    modelMap['episode-name'] = req_attrib['episode-name']
    
    video_source_id = 1
    video_source_img = None
    video_source_name = None
    video_part_index = 0
    video_playlist_items = []
    ignoreAllLinks = False
    
    list_items = []
    contentDiv = BeautifulSoup.SoupStrainer('div', {'class':'entry_content'})
    soup = HttpClient().get_beautiful_soup(url=req_attrib['episode-url'], parseOnlyThese=contentDiv)
#     soup = BeautifulSoup.BeautifulSoup(HttpClient().get_html_content(url=req_attrib['episode-url'])).findAll('blockquote', {'class':re.compile(r'\bpostcontent\b')})[0]
      
    centerTag = soup.findNext('center')
    logging.getLogger().debug(centerTag)
    prevChild = ''
    prevAFont = None
    isHD = 'false'
    videoSource = ''
    for child in soup.findChildren():
        if child.name == 'span':
            if len(video_playlist_items) > 0:
                list_items.append(__preparePlayListItem__(video_source_id, video_source_img, video_source_name, video_playlist_items, modelMap, isHD))
            
            logging.getLogger().debug(videoSource)
            videoSource = child.getText()
            if(re.search('720p', videoSource, re.I)):
                isHD = 'true'
            else:
                isHD = 'false'
            if video_source_img is not None:
                video_source_id = video_source_id + 1
                video_source_img = None
                video_source_name = None
                video_part_index = 0
                video_playlist_items = []
            ignoreAllLinks = False
        elif not ignoreAllLinks and child.name == 'a':
            if (str(child['href']) != 'https://www.facebook.com/iamdesirulez'):       
                video_part_index = video_part_index + 1
                video_link = {}
                video_link['videoTitle'] = 'Source #' + str(video_source_id) + ' | ' + 'Part #' + str(video_part_index) + ' | ' + child.getText()
                video_link['videoLink'] = str(child['href'])
                video_link['videoSource'] = videoSource
                try:
                    try:
                        __prepareVideoLink__(video_link)
                    except Exception, e:
                        logging.getLogger().exception(e)
                        video_hosting_info = SnapVideo().findVideoHostingInfo(video_link['videoLink'])
                        if video_hosting_info is None or video_hosting_info.get_name() == 'UrlResolver by t0mm0':
                            raise
                        video_link['videoSourceImg'] = video_hosting_info.get_icon()
                        video_link['videoSourceName'] = video_hosting_info.get_name()
                    video_playlist_items.append(video_link)
                    video_source_img = video_link['videoSourceImg']
                    video_source_name = video_link['videoSourceName']
                
                    item = xbmcgui.ListItem(label='Source #' + str(video_source_id) + ' | ' + 'Part #' + str(video_part_index) , iconImage=video_source_img, thumbnailImage=video_source_img)
                    item.setProperty('videoLink', video_link['videoLink'])
                    item.setProperty('videoTitle', video_link['videoTitle'])
                    item.setProperty('videoSourceName', video_source_name)
                    item.setProperty('isContinuousPlayItem', 'false')
                    list_items.append(item)
                
                    prevAFont = child.findChild('font')
                except:
                    logging.getLogger().error('Unable to recognize a source = ' + str(video_link['videoLink']))
                    video_source_img = None
                    video_source_name = None
                    video_part_index = 0
                    video_playlist_items = []
                    ignoreAllLinks = True
                    prevAFont = None
        prevChild = child.name
    if len(video_playlist_items) > 0:
        list_items.append(__preparePlayListItem__(video_source_id, video_source_img, video_source_name, video_playlist_items, modelMap, isHD))
    return list_items


def __preparePlayListItem__(video_source_id, video_source_img, video_source_name, video_playlist_items, modelMap, isHD):
    item = xbmcgui.ListItem(label='[B]Continuous Play[/B]' + ' | ' + 'Source #' + str(video_source_id) + ' | ' + 'Parts = ' + str(len(video_playlist_items)) , iconImage=video_source_img, thumbnailImage=video_source_img)
    item.setProperty('videoSourceName', video_source_name)
    item.setProperty('isContinuousPlayItem', 'true')
    item.setProperty('isHD', isHD)
    item.setProperty('videoPlayListItemsKey', 'playlist#' + str(video_source_id))
    item.setProperty('videosList', pickle.dumps(video_playlist_items))
    modelMap['playlist#' + str(video_source_id)] = video_playlist_items
    return item


def __prepareVideoLink__(video_link):
    logging.getLogger().debug(video_link)
    video_url = video_link['videoLink']
    video_source = video_link['videoSource']
    new_video_url = None
    if re.search('media.php\?id\=', video_url, flags=re.I):
        new_video_url = __parseDesiHomeUrl__(video_url)
    if new_video_url is None:        
        
        video_id = re.compile('(id|url|v|si|sim)=(.+?)/').findall(video_url + '/')[0][1]                
        
        if re.search('dm(\d*).php', video_url, flags=re.I) or ((re.search('([a-z]*).tv/', video_url, flags=re.I) or re.search('([a-z]*).net/', video_url, flags=re.I) or re.search('([a-z]*).com/', video_url, flags=re.I) or re.search('([a-z]*).me/', video_url, flags=re.I)) and not video_id.isdigit() and re.search('dailymotion', video_source, flags=re.I)):
            new_video_url = 'http://www.dailymotion.com/embed/video/' + video_id + '&'                    
        elif re.search('(flash.php|fp.php|wire.php|pw.php)', video_url, flags=re.I) or ((re.search('([a-z]*).tv/', video_url, flags=re.I) or re.search('([a-z]*).net/', video_url, flags=re.I) or re.search('([a-z]*).com/', video_url, flags=re.I) or re.search('([a-z]*).me/', video_url, flags=re.I)) and video_id.isdigit() and re.search('flash', video_source, flags=re.I)):
            new_video_url = 'http://config.playwire.com/videos/' + video_id + '/'            
        elif re.search('playu.php', video_url, flags=re.I) or re.search('playu', video_source, flags=re.I):
            new_video_url = 'http://playu.net/embed-' + video_id + '-540x304.html'
        elif re.search('watchvideo.php', video_url, flags=re.I) or re.search('watchvideo', video_source, flags=re.I):
            new_video_url = 'http://watchvideo2.us/embed-' + video_id + '-540x304.html'
        elif re.search('estream.php', video_url, flags=re.I) or re.search('estream', video_source, flags=re.I):
            new_video_url = 'https://estream.to/embed-' + video_id + '-540x304.html'
        elif re.search('streamin.php', video_url, flags=re.I) or re.search('streamin', video_source, flags=re.I):
            new_video_url = 'http://streamin.to/embed-' + video_id + '-520x400.html'
        elif re.search('watchers.php', video_url, flags=re.I) or re.search('watchers', video_source, flags=re.I):
            new_video_url = 'http://watchers.to/embed-' + video_id + '.html'
        elif re.search('idowatch.php', video_url, flags=re.I) or re.search('idowatch', video_source, flags=re.I):
            new_video_url = 'http://idowatch.net/embed-' + video_id + '-520x400.html'
        elif re.search('tvlogy', video_source, flags=re.I):
            new_video_url = 'http://tvlogy.to/watch.php?v=' + video_id + '&'
        elif re.search('vidwatch.php', video_url, flags=re.I) or re.search('vidwatch', video_source, flags=re.I):
            new_video_url = 'http://vidwatch3.me/embed-' + video_id + '-540x304.html'
        elif re.search('(youtube|u|yt)(\d*).php', video_url, flags=re.I):
            new_video_url = 'http://www.youtube.com/watch?v=' + video_id + '&'
        elif re.search('mega.co.nz', video_url, flags=re.I):
            new_video_url = video_url
        elif re.search('(put|pl).php', video_url, flags=re.I):
            new_video_url = 'http://www.putlocker.com/file/' + video_id
        elif re.search('(cl|cloud).php', video_url, flags=re.I) or ((re.search('([a-z]*).tv/', video_url, flags=re.I) or re.search('([a-z]*).net/', video_url, flags=re.I) or re.search('([a-z]*).com/', video_url, flags=re.I) or re.search('([a-z]*).me/', video_url, flags=re.I)) and not video_id.isdigit() and re.search('cloudy', video_source, flags=re.I)):
            new_video_url = 'https://www.cloudy.ec/embed.php?id=' + str(video_id)
        elif re.search('videohut.php', video_url, flags=re.I) or ((re.search('([a-z]*).tv/', video_url, flags=re.I) or re.search('([a-z]*).net/', video_url, flags=re.I) or re.search('([a-z]*).com/', video_url, flags=re.I) or re.search('([a-z]*).me/', video_url, flags=re.I)) and not video_id.isdigit() and re.search('video hut', video_source, flags=re.I)):
            new_video_url = 'http://www.videohut.to/embed.php?id=' + video_id
        elif re.search('letwatch.php', video_url, flags=re.I) or ((re.search('([a-z]*).tv/', video_url, flags=re.I) or re.search('([a-z]*).net/', video_url, flags=re.I) or re.search('([a-z]*).com/', video_url, flags=re.I) or re.search('([a-z]*).me/', video_url, flags=re.I)) and not video_id.isdigit() and re.search('letwatch', video_source, flags=re.I)):
            new_video_url = 'http://letwatch.us/embed-' + str(video_id) + '-620x496.html'
        elif re.search('videosky.php', video_url, flags=re.I) or ((re.search('([a-z]*).tv/', video_url, flags=re.I) or re.search('([a-z]*).net/', video_url, flags=re.I) or re.search('([a-z]*).com/', video_url, flags=re.I) or re.search('([a-z]*).me/', video_url, flags=re.I)) and not video_id.isdigit() and re.search('video sky', video_source, flags=re.I)):
            new_video_url = 'http://www.videosky.to/embed.php?id=' + str(video_id)
        elif re.search('(weed.php|vw.php)', video_url, flags=re.I):
            new_video_url = 'http://www.videoweed.es/file/' + video_id
        elif re.search('(sockshare.com|sock.com)', video_url, flags=re.I):
            new_video_url = video_url
        elif re.search('divxstage.php', video_url, flags=re.I):
            new_video_url = 'divxstage.eu/video/' + video_id + '&'
        elif re.search('(hostingbulk|hb).php', video_url, flags=re.I):
            new_video_url = 'hostingbulk.com/' + video_id + '&'
        elif re.search('(movshare|ms).php', video_url, flags=re.I):
            new_video_url = 'movshare.net/video/' + video_id + '&'
        elif re.search('mz.php', video_url, flags=re.I):
            new_video_url = 'movzap.com/' + video_id + '&'
        elif re.search('nv.php', video_url, flags=re.I):
            new_video_url = 'nowvideo.ch/embed.php?v=' + video_id + '&'
        elif re.search('nm.php', video_url, flags=re.I):
            new_video_url = 'novamov.com/video/' + video_id + '&'
        elif re.search('tune.php', video_url, flags=re.I) or ((re.search('([a-z]*).tv/', video_url, flags=re.I) or re.search('([a-z]*).net/', video_url, flags=re.I) or re.search('([a-z]*).com/', video_url, flags=re.I) or re.search('([a-z]*).me/', video_url, flags=re.I)) and video_id.isdigit() and re.search('tune.pk', video_source, flags=re.I)):
            new_video_url = 'tune.pk/play/' + video_id + '&'
        elif re.search('vshare.php', video_url, flags=re.I):
            new_video_url = 'http://vshare.io/d/' + video_id + '&'
        elif re.search('vidto.php', video_url, flags=re.I):
            new_video_url = 'http://vidto.me/' + video_id + '.html'
        elif re.search('videotanker.php', video_url, flags=re.I) or ((re.search('([a-z]*).tv/', video_url, flags=re.I) or re.search('([a-z]*).net/', video_url, flags=re.I) or re.search('([a-z]*).com/', video_url, flags=re.I) or re.search('([a-z]*).me/', video_url, flags=re.I)) and video_id.isdigit() and re.search('video tanker', video_source, flags=re.I)):
            new_video_url = 'http://videotanker.co/player/embed_player.php?vid=' + video_id + '&'

    
    video_hosting_info = SnapVideo().findVideoHostingInfo(new_video_url)
    video_link['videoLink'] = new_video_url
    video_link['videoSourceImg'] = video_hosting_info.get_icon()
    video_link['videoSourceName'] = video_hosting_info.get_name()



def __parseDesiHomeUrl__(video_url):
    video_link = None
    logging.getLogger().debug('video_url = ' + video_url)
    html = HttpClient().get_html_content(url=video_url)
    if re.search('\/d\.php\?id\=', html, flags=re.I):
        video_link = 'http://www.dailymotion.com/embed/video/' + re.compile('d.php\?id\=(.+?)"').findall(html)[0] + '&'
    elif re.search('config.playwire.com', html, flags=re.I):
        video_link = 'http://config.playwire.com/videos/' + re.compile('/v2/(.+?)/zeus.json"').findall(html)[0] + '/'
    elif re.search('tvlogy.to', html, flags=re.I):
        video_link = 'http://tvlogy.to/watch.php?v=' + re.compile('tvlogy\.to\/watch\.php\?v\=(.+?)"').findall(html)[0]
    elif re.search('hostingbulk.com', html, flags=re.I):
        video_link = 'http://hostingbulk.com/' + re.compile('hostingbulk.com/(.+?)"').findall(html)[0] + '&'
    elif re.search('movzap.com', html, flags=re.I):
        video_link = 'http://movzap.com/' + re.compile('movzap.com/(.+?)"').findall(html)[0] + '&'
    return video_link


PREFERRED_DIRECT_PLAY_ORDER = [Playwire.VIDEO_HOSTING_NAME, LetWatch.VIDEO_HOST_NAME, WatchVideo2US.VIDEO_HOSTING_NAME, PlayU.VIDEO_HOST_NAME]

def __findPlayNowStream__(new_items):
#     if AddonContext().get_addon().getSetting('autoplayback') == 'false':
#         return None
    logging.getLogger().debug('FINDING the source..')
    selectedIndex = None
    selectedSource = None
    hdSelected = False
    backupSource = None
    backupSourceName = None
    for item in new_items:
        if item.getProperty('isContinuousPlayItem') == 'true':
            source_name = item.getProperty('videoSourceName')
            try:
                logging.getLogger().debug(source_name)
                preference = PREFERRED_DIRECT_PLAY_ORDER.index(item.getProperty('videoSourceName'))
                if preference == 0 and (selectedIndex is None or selectedIndex != 0) and not hdSelected :
                    selectedSource = item
                    selectedIndex = 0
                elif selectedIndex is None or selectedIndex > preference:
                    selectedSource = item
                    selectedIndex = preference
                if item.getProperty('isHD') == 'true' and selectedIndex is not None:
                    hdSelected = True
                    
                if ((source_name == PlayU.VIDEO_HOST_NAME or source_name == VideoWeed.VIDEO_HOST_NAME) and backupSource is None):
                    logging.getLogger().debug("Added to backup plan: %s" % source_name)
                    backupSource = item
                    backupSourceName = source_name
                    
            except ValueError:
                logging.getLogger().debug("Exception for source : %s" % source_name)
                if source_name == PlayU.VIDEO_HOST_NAME and (backupSource is None or backupSourceName != PlayU.VIDEO_HOST_NAME):
                    logging.getLogger().debug("Added to backup plan: %s" % source_name)
                    backupSource = item
                    backupSourceName = source_name
                elif backupSource is None:
                    logging.getLogger().debug("Added to backup plan when Playwire not found: %s" % source_name)
                    backupSource = item
                    backupSourceName = source_name
                continue
    sources = {}
    sources['selected'] = selectedSource
    sources['backup'] = backupSource
    return sources

