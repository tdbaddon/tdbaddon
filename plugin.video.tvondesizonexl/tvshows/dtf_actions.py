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
from xoze.context import AddonContext
from xoze.utils import file, http, jsonfile
from xoze.utils.cache import CacheManager
from xoze.utils.http import HttpClient
import BeautifulSoup
import logging
import time
import xbmcgui  # @UnresolvedImport


def coming_soon(req_attrib, modelMap):
    logging.getLogger().debug('DesiTVForum is coming soon to this add-on, please use desirulez!!')
    

def check_cache(req_attrib, modelMap):
    logging.getLogger().debug('Check cache for DTF ***********************')
    logging.getLogger().debug(req_attrib)
    refresh_cache = True
    context = AddonContext()
    filepath = file.resolve_file_path(context.get_addon_data_path(), extraDirPath='data', filename='DTF_Channels.json', makeDirs=True)
    logging.getLogger().debug(filepath)
    refresh = context.get_addon().getSetting('dtfForceRefresh')
    if refresh == None or refresh != 'true':
        modified_time = file.get_last_modified_time(filepath)
        if modified_time is not None:
            diff = long((time.time() - modified_time) / 3600)
            if diff < 720:
                refresh_cache = False
            else:
                logging.getLogger().debug('DTF_Channels.json was last created 30 days ago, refreshing data.')
    else:
        logging.getLogger().debug('Request to force refresh.')
    modelMap['refresh_cache'] = refresh_cache
    modelMap['cache_filepath'] = filepath



def refresh_cache(req_attrib, modelMap):
    if not modelMap['refresh_cache']:
        return
    logging.getLogger().debug('Reloading cache...')
    
    tv_data = {"channels": {"UTV Stars":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/uu/utv_stars.jpg",
                   "channelType": "IND",
                   "running_tvshows_url": "/television/utv-stars/"},
                  "Star Plus":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/ss/star_plus_in_hd.jpg",
                   "channelType": "IND",
                   "running_tvshows_url": "/television/star-plus/"},
                  "Zee TV":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/zz/zee_tv.jpg",
                   "channelType": "IND",
                   "running_tvshows_url": "/television/zee-tv/"},
                  "Sony TV":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/ss/set_in.jpg",
                   "channelType": "IND",
                   "running_tvshows_url": "/television/sony-tv/"},
                  "Life OK":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/ll/life_ok_in.jpg",
                   "channelType": "IND",
                   "running_tvshows_url": "/television/life-ok/"},
                  "Star Utsav":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/ss/star_utsav.jpg",
                   "channelType": "IND",
                   "running_tvshows_url": "/television/star-utsav/"},
                  "Sahara One":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/ss/sahara_one.jpg",
                   "channelType": "IND",
                   "running_tvshows_url": "/television/sahara-one/"},
                  "Colors TV":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/cc/colors_in.jpg",
                   "channelType": "IND",
                   "running_tvshows_url": "/television/colors-tv/"},
                  "Sab TV":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/ss/sony_sab_tv.jpg",
                   "channelType": "IND",
                   "running_tvshows_url": "/television/sabtv/"},
                  "MTV":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/mm/mtv_india.jpg",
                   "channelType": "IND",
                   "running_tvshows_url": "/television/mtv/"},
                  "Bindass TV":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/uu/utv_bindass.jpg",
                   "channelType": "IND",
                   "running_tvshows_url": "/television/bindass-tv/"},
                  "Channel [V]":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/cc/channel_v_in.jpg",
                   "channelType": "IND",
                   "running_tvshows_url": "/television/channel-v/"},
                  "DD National":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/dd/dd_national.jpg",
                   "channelType": "IND",
                   "running_tvshows_url": "/television/dd-national/"},
                  "Sun TV":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/ss/sun_tv_in.jpg",
                   "channelType": "IND",
                   "running_tvshows_url": "/television/sun-tv/"},
                  "Big Magic":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/bb/big_magic.jpg",
                   "channelType": "IND",
                   "running_tvshows_url": "/television/big-magic/"},
                  "Star One":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/ss/star_one.jpg",
                   "channelType": "IND",
                   "running_tvshows_url": "/television/star-one-tv/"},
                  "Star World Premiere HD":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/ss/star_world_premiere_hd_in.jpg",
                   "channelType": "IND",
                   "running_tvshows_url": "/television/star-world-premiere-hd/"},
                  "Star World":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/ss/star_world_in_hd.jpg",
                   "channelType": "IND",
                   "running_tvshows_url": "/television/star-world/"},
                  "NDTV Imagine":
                  {"iconimage":"http://upload.wikimedia.org/wikipedia/en/thumb/f/f7/NDTV_Imagine.svg/200px-NDTV_Imagine.svg.png",
                   "channelType": "IND",
                   "running_tvshows_url": "/television/ndtv-imagine/"},
                  "Real TV":
                  {"iconimage":"http://upload.wikimedia.org/wikipedia/en/8/82/RealTv.jpg",
                   "channelType": "IND",
                   "running_tvshows_url": "/television/real-tv/"},
                  "AXN":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/aa/axn_in.jpg",
                   "channelType": "IND",
                   "running_tvshows_url": "/television/axn/"},
                  "9X INX Media":
                  {"iconimage":"http://www.lyngsat-logo.com/logo/tv/num/9x_in.jpg",
                   "channelType": "IND",
                   "running_tvshows_url": "/television/9x-inx-media/"},
                  "Awards & Concerts":
                  {"iconimage":"http://1.bp.blogspot.com/-63HEiUpB9rk/T2oJwqA-O8I/AAAAAAAAG78/g4WdztLscJE/s1600/filmfare-awards-20121.jpg",
                   "channelType": "IND",
                   "running_tvshows_url": "/television/shows-concerts/"}
                }
            }
    current_index = 0
    tv_channels = tv_data['channels']
    total_iteration = len(tv_channels)
    progress_bar = modelMap['progress_control']
    for tv_channel_name, tv_channel in tv_channels.iteritems():
        logging.getLogger().debug('About to retrieve tv shows for channel %s' % tv_channel_name)
        __retrieve_channel_tv_shows__(tv_channel_name, tv_channel)
        current_index = current_index + 1
        percent = (current_index * 100) / total_iteration
        progress_bar.setPercent(percent)
        
    status = jsonfile.write_file(modelMap['cache_filepath'], tv_data)
    if status is not None:
        logging.getLogger().debug('Saved status = ' + str(status))
    CacheManager().put('tv_data', tv_data)
    AddonContext().get_addon().setSetting('dtfForceRefresh', 'false')
    
CHANNEL_TYPE_IND = 'IND'
CHANNEL_TYPE_PAK = 'PAK'


def load_channels(req_attrib, modelMap):
    logging.getLogger().debug('load channels...')
    tv_channels = _read_tv_channels_cache_(modelMap['cache_filepath'])['channels']
    
    tv_channel_items = []
    
    display_channel_type = 1
    
    for channel_name in tv_channels:
        channel_obj = tv_channels[channel_name]
        if ((display_channel_type == 1 and channel_obj['channelType'] == CHANNEL_TYPE_IND) 
            or (display_channel_type == 2 and channel_obj['channelType'] == CHANNEL_TYPE_PAK) 
            or (display_channel_type == 0)):
            
            item = xbmcgui.ListItem(label=channel_name, iconImage=channel_obj['iconimage'], thumbnailImage=channel_obj['iconimage'])
            item.setProperty('channel-name', channel_name)
            tv_channel_items.append(item)
     
    modelMap['tv_channel_items'] = tv_channel_items

def load_tv_shows(req_attrib, modelMap):
    logging.getLogger().debug('load tv shows...')
    tv_channels = CacheManager().get('tv_data')['channels']
    channel_name = req_attrib['channel-name']
    tv_channel = tv_channels[channel_name]
    channel_type = tv_channel['channelType']
    modelMap['channel_image'] = tv_channel['iconimage']
    modelMap['channel_name'] = channel_name
    
    tv_show_items = []
    if tv_channel.has_key('running_tvshows'):
        tv_shows = tv_channel['running_tvshows']
        logging.getLogger().debug('total tv shows to be displayed: %s' % str(len(tv_shows)))
        for tv_show in tv_shows:
            name = tv_show['name']
            item = xbmcgui.ListItem(label=name)
            item.setProperty('channel-type', channel_type)
            item.setProperty('tv-show-name', name)
            item.setProperty('tv-show-url', tv_show['url'])
            tv_show_items.append(item)
    
    modelMap['tv_show_items'] = tv_show_items
    

def _read_tv_channels_cache_(filepath):
    tv_data = CacheManager().get('tv_data')
    if tv_data is None:
        tv_data = jsonfile.read_file(filepath)
        CacheManager().put('tv_data', tv_data)
    return tv_data

BASE_WSITE_URL = 'http://desitvforum.net'

def __retrieve_tv_shows__(tv_channel_url):
    tv_shows = []
    if tv_channel_url is None:
        return tv_shows
    tv_channel_url = BASE_WSITE_URL + tv_channel_url
    contentDiv = BeautifulSoup.SoupStrainer('div', {'class':'all-tv-shows'})
    soup = HttpClient().get_beautiful_soup(url=tv_channel_url, parseOnlyThese=contentDiv, accept_500_error=True)
    list_item = soup.find('ul')
    for item in list_item.findChildren('li'):
        aTag = item.findChild('a')
        
        tv_show_url = str(aTag['href'])
        if tv_show_url[0:4] != "http":
            tv_show_url = BASE_WSITE_URL + '/' + tv_show_url
        tv_show_name = aTag.getText()
        tv_shows.append({"name":http.unescape(tv_show_name), "url":tv_show_url, "iconimage":""})
    return tv_shows
    
    
def __retrieve_channel_tv_shows__(tv_channel_name, tv_channel):
    running_tvshows = []
    try:
        running_tvshows = __retrieve_tv_shows__(tv_channel["running_tvshows_url"])
        if(len(running_tvshows) == 0):
            running_tvshows.append({"name":"ENTER TO VIEW :: This is the only easy way to view!", "url":BASE_WSITE_URL + tv_channel["running_tvshows_url"]})
    except Exception, e:
        logging.getLogger().exception(e)
        logging.getLogger().debug('Failed to load a channel <%s>. continue retrieval of next tv show' % tv_channel_name)
    tv_channel["running_tvshows"] = running_tvshows
    

