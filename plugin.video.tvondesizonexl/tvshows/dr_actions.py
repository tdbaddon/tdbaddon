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

from xoze.context import AddonContext, SnapVideo
from xoze.snapvideo import WatchVideo2US, Playwire, VideoWeed, CloudEC, LetWatch, \
    TVLogy, PlayU
from xoze.utils import file, http, jsonfile
from xoze.utils.cache import CacheManager
from xoze.utils.http import HttpClient
import BeautifulSoup
import base64
import logging
import pickle
import re
import time
import urllib
import xbmc  # @UnresolvedImport
import xbmcgui  # @UnresolvedImport

DIRECT_CHANNELS = {"Awards & Concerts":{"iconimage":"Awards.jpg",
                   "channelType": "IND",
                   "tvshow_episodes_url": "/forums/36-Awards-Performances-Concerts"},
                   "Latest & Exclusive Movies":{"iconimage":"Movies.jpeg",
                   "channelType": "IND",
                   "tvshow_episodes_url": "/forums/20-Latest-Exclusive-Movie-HQ"}}
 
LIVE_CHANNELS = {"MTunes":{"iconimage":"http://www.lyngsat-logo.com/logo/tv/mm/m_tunes_hd.png",
                        "channelType": "IND",
                        "channelUrl": "http://akamaihd.wowzahls12.yuppcdn.net/live/mtunes/chunklist.m3u8|User-Agent=Apache"},
                 "Music India":{"iconimage":"http://www.lyngsat-logo.com/logo/tv/mm/music_india.png",
                        "channelType": "IND",
                        "channelUrl": "http://akamaihd.wowzahls12.yuppcdn.net/live/musicindia/chunklist.m3u8|User-Agent=Apache"},
                 "9XM":{"iconimage":"http://www.lyngsat-logo.com/logo/tv/num/9x_music.png",
                        "channelType": "IND",
                        "channelUrl": "http://d2ckk42trw29cy.cloudfront.net/9xmedia/ngrp:9xmusic_all/playlist.m3u8"},
                 "9X Jalwa":{"iconimage":"http://www.lyngsat-logo.com/logo/tv/num/9x_jalwa.png",
                             "channelType": "IND",
                             "channelUrl": "http://dls96d52aauuo.cloudfront.net/9xmedia/ngrp:9xjalwa_all/playlist.m3u8"},
                 "9x Tashan":{"iconimage":"http://www.lyngsat-logo.com/logo/tv/num/9x_tashan.png",
                              "channelType": "IND",
                              "channelUrl": "http://dhkvssi8he6y9.cloudfront.net/9xmedia/ngrp:9xtashan_all/playlist.m3u8"},
                 "9x Jhakaas":{"iconimage":"http://www.lyngsat-logo.com/logo/tv/num/9x_jhakaas.png",
                              "channelType": "IND",
                              "channelUrl": "http://d20rca8w7x9af9.cloudfront.net/9xmedia/ngrp:9xjhakaas_all/playlist.m3u8"},
                 "IBN7": {"iconimage":"http://www.lyngsat-logo.com/logo/tv/ii/ibn7.png",
                          "channelType": "IND",
                          "channelUrl": "http://ibn7_hls-lh.akamaihd.net/i/ibn7_hls_n_1@174951/index_3_av-b.m3u8?sd=10&play-only=backup&rebase=on"},
                 "India TV": {"iconimage":"http://www.lyngsat-logo.com/logo/tv/ii/india_tv_in.png",
                              "channelType": "IND",
                              "channelUrl": "http://indiatvnews-lh.akamaihd.net/i/ITV_1@199237/master.m3u8"}						  
                 }

BASE_WSITE_URL = base64.b64decode('aHR0cDovL3d3dy5kZXNpcnVsZXoubmV0')
    
def check_cache(req_attrib, modelMap):
    logging.getLogger().debug('Check cache ***********************')
    logging.getLogger().debug(req_attrib)
    refresh_cache = True
    context = AddonContext()
    filepath = file.resolve_file_path(context.get_addon_data_path(), extraDirPath='data', filename='DR_Channels.json', makeDirs=True)
    refresh = context.get_addon().getSetting('drForceRefresh')
    if refresh == None or refresh != 'true':
        modified_time = file.get_last_modified_time(filepath)
        if modified_time is not None:
            diff = long((time.time() - modified_time) / 3600)
            if diff < 720:
                refresh_cache = False
            else:
                logging.getLogger().debug('DR_Channels.json was last created 30 days ago, refreshing data.')
    else:
        logging.getLogger().debug('Request to force refresh.')
    modelMap['refresh_cache'] = refresh_cache
    modelMap['cache_filepath'] = filepath


def refresh_cache(req_attrib, modelMap):
    if not modelMap['refresh_cache']:
        return
    logging.getLogger().debug('Reloading cache...')
    
    tv_data = {"channels": {"UTV Stars":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/uu/utv_stars.png",
                   "channelType": "IND",
                   "running_tvshows_url": "/forumdisplay.php?f=1274",
                   "finished_tvshows_url": "/forumdisplay.php?f=1435"},
                  "Star Plus":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/ss/star_plus.png",
                   "channelType": "IND",
                   "running_tvshows_url": "/forumdisplay.php?f=42",
                   "finished_tvshows_url": "/forumdisplay.php?f=209"},
                  "Zee TV":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/zz/zee_tv.png",
                   "channelType": "IND",
                   "running_tvshows_url": "/forumdisplay.php?f=73",
                   "finished_tvshows_url": "/forumdisplay.php?f=211"},
                  "Zee Anmol":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/zz/zee_anmol_in.png",
                   "channelType": "IND",
                   "running_tvshows_url": "/forumdisplay.php?f=2819",
                   "finished_tvshows_url": "/forumdisplay.php?f=2935"},
                  "Sony TV":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/ss/set_in.png",
                   "channelType": "IND",
                   "running_tvshows_url": "/forumdisplay.php?f=63",
                   "finished_tvshows_url": "/forumdisplay.php?f=210"},
                  "Sony Pal":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/ss/sony_pal_in.png",
                   "channelType": "IND",
                   "running_tvshows_url": "/forumdisplay.php?f=2757",
                   "finished_tvshows_url": None},
                  "Life OK":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/ll/life_ok_in.png",
                   "channelType": "IND",
                   "running_tvshows_url": "/forumdisplay.php?f=1375",
                   "finished_tvshows_url": "/forumdisplay.php?f=1581"},
                  "Star Jalsha":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/ss/star_jalsha.png",
                   "channelType": "IND",
                   "running_tvshows_url": "/forumdisplay.php?f=667",
                   "finished_tvshows_url": "/forumdisplay.php?f=1057"},
                  "Sahara One":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/ss/sahara_one.png",
                   "channelType": "IND",
                   "running_tvshows_url": "/forumdisplay.php?f=134",
                   "finished_tvshows_url": "/forumdisplay.php?f=213"},
                  "Colors TV":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/cc/colors_in.png",
                   "channelType": "IND",
                   "running_tvshows_url": "/forumdisplay.php?f=176",
                   "finished_tvshows_url": "/forumdisplay.php?f=374"},
                  "Sab TV":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/ss/sony_sab_tv.png",
                   "channelType": "IND",
                   "running_tvshows_url": "/forumdisplay.php?f=254",
                   "finished_tvshows_url": "/forumdisplay.php?f=454"},
                  "&TV":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/aa/and_tv_in.png",
                   "channelType": "IND",
                   "running_tvshows_url": "/forumdisplay.php?f=3138",
                   "finished_tvshows_url": None},
                  "MTV":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/mm/mtv_india.png",
                   "channelType": "IND",
                   "running_tvshows_url": "/forumdisplay.php?f=339",
                   "finished_tvshows_url": "/forumdisplay.php?f=532"},
                  "Bindass TV":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/uu/utv_bindass.png",
                   "channelType": "IND",
                   "running_tvshows_url": "/forumdisplay.php?f=504",
                   "finished_tvshows_url": "/forumdisplay.php?f=960"},
                  "Channel [V]":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/cc/channel_v_in.png",
                   "channelType": "IND",
                   "running_tvshows_url": "/forumdisplay.php?f=633",
                   "finished_tvshows_url": "/forumdisplay.php?f=961"},
                  "DD National":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/dd/dd_national.png",
                   "channelType": "IND",
                   "running_tvshows_url": "/forumdisplay.php?f=535",
                   "finished_tvshows_url": "/forumdisplay.php?f=801"},
                  "Ary Digital":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/aa/atn_ary_digital.png",
                   "channelType": "PAK",
                   "running_tvshows_url": "/forumdisplay.php?f=384",
                   "finished_tvshows_url": "/forumdisplay.php?f=950"},
                  "GEO TV":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/gg/geo_tv.png",
                   "channelType": "PAK",
                   "running_tvshows_url": "/forumdisplay.php?f=413",
                   "finished_tvshows_url": "/forumdisplay.php?f=894"},
                  "HUM TV":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/hh/hum_tv.png",
                   "channelType": "PAK",
                   "running_tvshows_url": "/forumdisplay.php?f=448",
                   "finished_tvshows_url": "/forumdisplay.php?f=794"},
                  "A PLUS":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/aa/a_plus.png",
                   "channelType": "PAK",
                   "running_tvshows_url": "/forumdisplay.php?f=1327",
                   "finished_tvshows_url": "/forumdisplay.php?f=1334"},
                  "POGO":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/pp/pogo.png",
                   "channelType": "IND",
                   "running_tvshows_url": "/forumdisplay.php?f=500",
                   "finished_tvshows_url": None},
                  "Disney Channel":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/dd/disney_channel_in.png",
                   "channelType": "IND",
                   "running_tvshows_url": "/forumdisplay.php?f=479",
                   "finished_tvshows_url": None},
                  "Discovery Kids":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/dd/discovery_kids_us.png",
                   "channelType": "IND",
                   "running_tvshows_url": "/forumdisplay.php?f=2096",
                   "finished_tvshows_url": "/forumdisplay.php?f=2340"},
                  "Hungama TV":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/hh/hungama.png",
                   "channelType": "IND",
                   "running_tvshows_url": "/forumdisplay.php?f=472",
                   "finished_tvshows_url": "/forumdisplay.php?f=2102"},
                  "Cartoon Network":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/cc/cartoon_network_in.png",
                   "channelType": "IND",
                   "running_tvshows_url": "/forumdisplay.php?f=509",
                   "finished_tvshows_url": None},
                  "WWE":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/ww/world_wrestling_entertainment.png",
                   "channelType": "IND",
                   "running_tvshows_url": "/forumdisplay.php?f=303",
                   "finished_tvshows_url": None},
                  "Star Pravah":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/ss/star_pravah.png",
                   "channelType": "IND",
                   "running_tvshows_url": "/forumdisplay.php?f=1138",
                   "finished_tvshows_url": "/forumdisplay.php?f=1466"},
                  "Zee Marathi":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/zz/zee_marathi.png",
                   "channelType": "IND",
                   "running_tvshows_url": "/forumdisplay.php?f=1299",
                   "finished_tvshows_url": "/forumdisplay.php?f=1467"},
                  "Star Vijay":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/ss/star_vijay_in.png",
                   "channelType": "IND",
                   "running_tvshows_url": "/forumdisplay.php?f=1609",
                   "finished_tvshows_url": "/forumdisplay.php?f=1747"},
                  "ZEE Bangla":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/zz/zee_bangla.png",
                   "channelType": "IND",
                   "running_tvshows_url": "/forumdisplay.php?f=676",
                   "finished_tvshows_url": "/forumdisplay.php?f=802"},
                  "Mahuaa TV":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/mm/mahuaa_bangla.png",
                   "channelType": "IND",
                   "running_tvshows_url": "/forumdisplay.php?f=772",
                   "finished_tvshows_url": "/forumdisplay.php?f=803"},
                  "Epic TV":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/ee/epic_in.png",
                   "channelType": "IND",
                   "running_tvshows_url": "/forumdisplay.php?f=2929",
                   "finished_tvshows_url": None},
                  "Zindagi TV":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/zz/zee_zindagi_in.png",
                   "channelType": "IND",
                   "running_tvshows_url": "/forumdisplay.php?f=2679",
                   "finished_tvshows_url": None},
                  "Zing TV":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/zz/zee_zing_asia.png",
                   "channelType": "IND",
                   "running_tvshows_url": "/forumdisplay.php?f=2624",
                   "finished_tvshows_url": None},
                  "Zee Q":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/zz/zee_q_in.png",
                   "channelType": "IND",
                   "running_tvshows_url": "/forumdisplay.php?f=2555",
                   "finished_tvshows_url": "/forumdisplay.php?f=2689"},
                  "Sonic":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/ss/sonic_nickelodeon.png",
                   "channelType": "IND",
                   "running_tvshows_url": "/forumdisplay.php?f=1533",
                   "finished_tvshows_url": "/forumdisplay.php?f=2234"}
                   
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
        __retrieve_channel_tv_shows__(tv_channel_name, tv_channel)
        channel_image.setVisible(False)
        current_index = current_index + 1
        percent = (current_index * 100) / total_iteration
        progress_bar.setPercent(percent)
        
    status = jsonfile.write_file(modelMap['cache_filepath'], tv_data)
    if status is not None:
        logging.getLogger().debug('Saved status = ' + str(status))
    CacheManager().put('tv_data', tv_data)
    AddonContext().get_addon().setSetting('drForceRefresh', 'false')
    
CHANNEL_TYPE_IND = 'IND'
CHANNEL_TYPE_PAK = 'PAK'

def load_channels(req_attrib, modelMap):
    logging.getLogger().debug('load channels...')
    tv_channels = _read_tv_channels_cache_(modelMap['cache_filepath'])['channels']
    
    tv_channel_items = []
    live_tv_channel_items = []
    
    display_channel_type = int(AddonContext().get_addon().getSetting('drChannelType'))
    
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
    filepath = file.resolve_file_path(context.get_addon_data_path(), extraDirPath='data', filename='DR_Favorites.json', makeDirs=False)
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
        return 'redirect:dr-watchLiveChannel'
    

def load_tv_shows(req_attrib, modelMap):
    logging.getLogger().debug('load tv shows...')
    
    tv_channels = CacheManager().get('tv_data')['channels']
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
    
    favorites = CacheManager().get('tv_favorites')
    if favorites is None:
        favorites = {}
    elif favorites.has_key(tv_show_name):
        favorites.pop(tv_show_name)
    
    favorites[tv_show_name] = {'tv-show-name':tv_show_name, 'tv-show-thumb':tv_show_thumb, 'tv-show-url':tv_show_url, 'channel-name':channel_name, 'channel-type':channel_type}
    context = AddonContext()
    filepath = file.resolve_file_path(context.get_addon_data_path(), extraDirPath='data', filename='DR_Favorites.json', makeDirs=False)
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
    favorites = CacheManager().get('tv_favorites')
    if favorites is None:
        favorites = {}
    elif favorites.has_key(favorite):
        favorites.pop(favorite)
    
    context = AddonContext()
    filepath = file.resolve_file_path(context.get_addon_data_path(), extraDirPath='data', filename='DR_Favorites.json', makeDirs=False)
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
            url = url + '/page' + req_attrib['tv-show-page']
    logging.getLogger().debug('load tv show episodes...' + url)
#     contentDiv = BeautifulSoup.SoupStrainer('div', {'id':'contentBody'})
#     soup = HttpClient().get_beautiful_soup(url=url, parseOnlyThese=contentDiv)
    soup = BeautifulSoup.BeautifulSoup(HttpClient().get_html_content(url=url)).findAll('div', {'id':'contentBody'})[0]
    
    tv_show_episode_items = []
    if currentPage == 1:
        logging.getLogger().debug('get sticky threads for current page : %s' % str(currentPage))
        threads = soup.find('ol', {'class':'stickies', 'id':'stickies'})
        tv_show_episode_items.extend(__retrieveTVShowEpisodes__(threads, tv_show_name, channel_type, channel_name))
    
    threads = soup.find('ol', {'class':'threads', 'id':'threads'})
    tv_show_episode_items.extend(__retrieveTVShowEpisodes__(threads, tv_show_name, channel_type, channel_name))
    logging.getLogger().debug('In DR: total tv show episodes: %s' % str(len(tv_show_episode_items)))
    
    pagesDiv = soup.find('div', {'class':'threadpagenav'})
    if pagesDiv is not None:
        pagesInfoTag = pagesDiv.find('a', {'class':re.compile(r'\bpopupctrl\b')})
        if pagesInfoTag is not None:
            pageInfo = re.compile('Page (.+?) of (.+?) ').findall(pagesInfoTag.getText() + ' ')
            totalPages = int(pageInfo[0][1])
            for page in range(1, totalPages + 1):
                if page != currentPage:
                    pageName = ''
                    if page < currentPage:
                        pageName = '[B]     <-    Page #' + str(page) + '[/B]'
                    else:
                        pageName = '[B]     ->    Page #' + str(page) + '[/B]'
                    
                    item = xbmcgui.ListItem(label=pageName)
                    item.setProperty('channel-type', channel_type)
                    item.setProperty('channel-name', channel_name)
                    item.setProperty('tv-show-name', tv_show_name)
                    item.setProperty('tv-show-url', tv_show_url)
                    if page != 1:
                        item.setProperty('tv-show-page', str(page))
                    tv_show_episode_items.append(item)
    
    modelMap['tv_show_episode_items'] = tv_show_episode_items
    

def __retrieveTVShowEpisodes__(threads, tv_show_name, channel_type, channel_name):
    tv_show_episode_items = []
    logging.getLogger().debug(threads)
    if threads is None:
        return []
    aTags = threads.findAll('a', {'class':re.compile(r'\btitle\b')})
    logging.getLogger().debug(aTags)
    videoEpisodes = []
    for aTag in aTags:
        episodeName = aTag.getText()
        if not re.search(r'\b(Watch|Episode|Video|Promo)\b', episodeName, re.IGNORECASE):
            pass
        else:
            videoEpisodes.append(aTag)
            
    if len(videoEpisodes) == 0:
        videoEpisodes = aTags
        
    for aTag in videoEpisodes:
        episodeName = aTag.getText()
        titleInfo = http.unescape(episodeName)
        titleInfo = titleInfo.replace(tv_show_name, '')
        titleInfo = titleInfo.replace(' - Video Watch Online', '')
        titleInfo = titleInfo.replace(' - Video Watch online', '')
        titleInfo = titleInfo.replace('Video Watch Online', '')
        titleInfo = titleInfo.replace('Video Watch online', '')
        titleInfo = titleInfo.replace('Watch Online', '')
        titleInfo = titleInfo.replace('Watch online', '')
        titleInfo = titleInfo.replace('Watch', '')      
        titleInfo = titleInfo.replace('Video', '')
        titleInfo = titleInfo.replace('video', '')
        titleInfo = titleInfo.replace('-', '')
        titleInfo = titleInfo.replace('/ Download', '')
        titleInfo = titleInfo.replace('/Download', '')
        titleInfo = titleInfo.replace('Download', '')
        titleInfo = titleInfo.strip()
#         movieInfo = re.compile("(.+?)\((\d+)\)").findall(titleInfo)
#         if(len(movieInfo) >= 1 and len(movieInfo[0]) >= 2):
#             title = unicode(movieInfo[0][0].rstrip()).encode('utf-8')
#             year = unicode(movieInfo[0][1]).encode('utf-8')
#             item.add_moving_data('movieTitle', title)
#             item.add_moving_data('movieYear', year)
        
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
        return 'redirect:dr-displayShowEpisodesList'

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
    tv_data = CacheManager().get('tv_data')
    if tv_data is None:
        tv_data = jsonfile.read_file(filepath)
        CacheManager().put('tv_data', tv_data)
    return tv_data

def _read_live_tv_channels_cache_(filepath):
    live_tv_data = CacheManager().get('live_tv_data')
    if live_tv_data is None:
        live_tv_data = jsonfile.read_file(filepath)
        CacheManager().put('live_tv_data', live_tv_data)
    return live_tv_data

def _read_favorite_tv_shows_cache_(filepath):
    favorites = CacheManager().get('tv_favorites')
    if favorites is None:
        favorites = jsonfile.read_file(filepath)
        CacheManager().put('tv_favorites', favorites)
    return favorites

def _write_favorite_tv_shows_cache_(filepath, data):
    CacheManager().put('tv_favorites', data)
    jsonfile.write_file(filepath, data)


def __retrieve_tv_shows__(tv_channel_url):
    logging.getLogger().debug(tv_channel_url)
    tv_shows = []
    if tv_channel_url is None:
        return tv_shows
    tv_channel_url = BASE_WSITE_URL + tv_channel_url
    logging.getLogger().debug(tv_channel_url)
#     contentDiv = BeautifulSoup.SoupStrainer('div', {'id':'forumbits', 'class':'forumbits'})
#     soup = HttpClient().get_beautiful_soup(url=tv_channel_url, parseOnlyThese=contentDiv)
    soup = BeautifulSoup.BeautifulSoup(HttpClient().get_html_content(url=tv_channel_url)).findAll('div', {'id':'forumbits', 'class':'forumbits'})[0]
    for title_tag in soup.findAll('h2', {'class':'forumtitle'}):
        aTag = title_tag.find('a')
        tv_show_url = str(aTag['href'])
        if tv_show_url[0:4] != "http":
            tv_show_url = BASE_WSITE_URL + '/' + tv_show_url
        tv_show_name = aTag.getText()
        if not re.search('Past Shows', tv_show_name, re.IGNORECASE):
            tv_shows.append({"name":http.unescape(tv_show_name), "url":tv_show_url, "iconimage":""})
    return tv_shows
    
    
def __retrieve_channel_tv_shows__(tv_channel_name, tv_channel):
    running_tvshows = []
    finished_tvshows = []
    try:
        running_tvshows = __retrieve_tv_shows__(tv_channel["running_tvshows_url"])
        if(len(running_tvshows) == 0):
            running_tvshows.append({"name":"ERROR: UNABLE TO LOAD. Share message on http://forum.xbmc.org/showthread.php?tid=115583", "url":BASE_WSITE_URL + tv_channel["running_tvshows_url"]})
    except Exception, e:
        logging.getLogger().exception(e)
        logging.getLogger().debug('Failed to load a channel <%s>. continue retrieval of next tv show' % tv_channel_name)
    try:
        finished_tvshows = __retrieve_tv_shows__(tv_channel["finished_tvshows_url"])
    except Exception, e:
        logging.getLogger().exception(e)
        logging.getLogger().debug('Failed to load a channel <%s>. continue retrieval of next tv show' % tv_channel_name)
    tv_channel["running_tvshows"] = running_tvshows
    tv_channel["finished_tvshows"] = finished_tvshows


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
    
#     content = BeautifulSoup.SoupStrainer('blockquote', {'class':re.compile(r'\bpostcontent\b')})
#     soup = HttpClient().get_beautiful_soup(url=req_attrib['episode-url'], parseOnlyThese=content)
    soup = BeautifulSoup.BeautifulSoup(HttpClient().get_html_content(url=req_attrib['episode-url'])).findAll('blockquote', {'class':re.compile(r'\bpostcontent\b')})[0]
    
    for e in soup.findAll('br'):
        e.extract()
    
    # Removing the child font within font to handle where the font gets changed at the end for HQ    
    for e in soup.find('font').findAll('font'):
        e.extract()    
    
    logging.getLogger().debug(soup)
    if soup.has_key('div'):
        soup = soup.findChild('div', recursive=False)
    prevChild = ''
    prevAFont = None
    isHD = 'false'
    videoSource = ''
    for child in soup.findChildren():
        if (child.name == 'img' or child.name == 'b' or (child.name == 'font' and not child.findChild('a'))):
            if (child.name == 'b' and prevChild == 'a') or (child.name == 'font' and child == prevAFont):
                continue
            else:
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
        elif not ignoreAllLinks and child.name == 'a' and not re.search('multi', str(child['href']), re.IGNORECASE):
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
    if re.search('videos.desihome.info', video_url, flags=re.I):
        new_video_url = __parseDesiHomeUrl__(video_url)
    if new_video_url is None:        
        
        video_id = re.compile('(id|url|v|si|sim|d)=(.+?)/').findall(video_url + '/')[0][1]                
        
        if re.search('dm(\d*).php', video_url, flags=re.I) or ((re.search('([a-z]*).tv/', video_url, flags=re.I) or re.search('([a-z]*).net/', video_url, flags=re.I) or re.search('([a-z]*).com/', video_url, flags=re.I) or re.search('([a-z]*).me/', video_url, flags=re.I)) and not video_id.isdigit() and re.search('dailymotion', video_source, flags=re.I)):
            new_video_url = 'http://www.dailymotion.com/embed/video/' + video_id + '&'                        
        elif re.search('(flash.php|fp.php|wire.php|pw.php)', video_url, flags=re.I) or ((re.search('([a-z]*).tv/', video_url, flags=re.I) or re.search('([a-z]*).net/', video_url, flags=re.I) or re.search('([a-z]*).com/', video_url, flags=re.I) or re.search('([a-z]*).me/', video_url, flags=re.I)) and video_id.isdigit() and re.search('flash', video_source, flags=re.I)):
            new_video_url = 'http://config.playwire.com/videos/' + video_id + '/'         
        elif re.search('playu.php', video_url, flags=re.I) or re.search('playu', video_source, flags=re.I):
            new_video_url = 'http://playu.net/embed-' + video_id + '-540x304.html'
        elif re.search('watchvideo.php', video_url, flags=re.I) or re.search('watchvideo', video_source, flags=re.I):
            new_video_url = 'http://watchvideo2.us/embed-' + video_id + '-540x304.html'
        elif re.search('idowatch.php', video_url, flags=re.I) or re.search('idowatch', video_source, flags=re.I):
            new_video_url = 'http://idowatch.net/embed-' + video_id + '-520x400.html'
        elif re.search('tvlogy', video_source, flags=re.I):
            new_video_url = 'http://tvlogy.com/watch.php?v=' + video_id + '&' 
        elif re.search('(youtube|u|yt)(\d*).php', video_url, flags=re.I):
            new_video_url = 'http://www.youtube.com/watch?v=' + video_id + '&'
        elif re.search('mega.co.nz', video_url, flags=re.I):
            new_video_url = video_url
        elif re.search('(put|pl).php', video_url, flags=re.I):
            new_video_url = 'http://www.putlocker.com/file/' + video_id
        elif re.search('letwatch.php', video_url, flags=re.I) or ((re.search('([a-z]*).tv/', video_url, flags=re.I) or re.search('([a-z]*).net/', video_url, flags=re.I) or re.search('([a-z]*).com/', video_url, flags=re.I) or re.search('([a-z]*).me/', video_url, flags=re.I)) and not video_id.isdigit() and (re.search('letwatch', video_source, flags=re.I) or re.search('let watch', video_source, flags=re.I))):
            new_video_url = 'http://letwatch.us/embed-' + str(video_id) + '-595x430.html'
        elif re.search('(cl|cloud).php', video_url, flags=re.I) or ((re.search('([a-z]*).tv/', video_url, flags=re.I) or re.search('([a-z]*).net/', video_url, flags=re.I) or re.search('([a-z]*).com/', video_url, flags=re.I) or re.search('([a-z]*).me/', video_url, flags=re.I)) and not video_id.isdigit() and re.search('cloudy', video_source, flags=re.I)):
            new_video_url = 'https://www.cloudy.ec/embed.php?id=' + str(video_id)
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
        elif re.search('videotanker.php', video_url, flags=re.I) or ((re.search('([a-z]*).tv/', video_url, flags=re.I) or re.search('([a-z]*).net/', video_url, flags=re.I) or re.search('([a-z]*).com/', video_url, flags=re.I) or re.search('([a-z]*).me/', video_url, flags=re.I)) and video_id.isdigit() and (re.search('video tanker', video_source, flags=re.I) or re.search('videotanker', video_source, flags=re.I))):
            new_video_url = 'http://videotanker.co/player/embed_player.php?vid=' + video_id + '&'

    
    video_hosting_info = SnapVideo().findVideoHostingInfo(new_video_url)
    video_link['videoLink'] = new_video_url
    video_link['videoSourceImg'] = video_hosting_info.get_icon()
    video_link['videoSourceName'] = video_hosting_info.get_name()



def __parseDesiHomeUrl__(video_url):
    video_link = None
    logging.getLogger().debug('video_url = ' + video_url)
    html = HttpClient().get_html_content(url=video_url)
    if re.search('dailymotion.com', html, flags=re.I):
        video_link = 'http://www.dailymotion.com/' + re.compile('dailymotion.com/(.+?)"').findall(html)[0] + '&'
    elif re.search('hostingbulk.com', html, flags=re.I):
        video_link = 'http://hostingbulk.com/' + re.compile('hostingbulk.com/(.+?)"').findall(html)[0] + '&'
    elif re.search('movzap.com', html, flags=re.I):
        video_link = 'http://movzap.com/' + re.compile('movzap.com/(.+?)"').findall(html)[0] + '&'
    return video_link


PREFERRED_DIRECT_PLAY_ORDER = [TVLogy.VIDEO_HOSTING_NAME, Playwire.VIDEO_HOSTING_NAME, LetWatch.VIDEO_HOST_NAME, VideoWeed.VIDEO_HOST_NAME, WatchVideo2US.VIDEO_HOSTING_NAME, PlayU.VIDEO_HOST_NAME]

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
                    
                if ((source_name == PlayU.VIDEO_HOST_NAME or source_name == Playwire.VIDEO_HOSTING_NAME) and backupSource is None):
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

