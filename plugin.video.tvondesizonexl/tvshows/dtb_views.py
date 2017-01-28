'''
Created on Dec 23, 2013

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
from xoze.utils.cache import CacheManager
import logging
import xbmcgui, xbmc  # @UnresolvedImport
from xoze.utils import system

def show_refresh_view(modelMap, window):
    logging.getLogger().debug('Refresh cache attribute: %s' % str(modelMap['refresh_cache']))
    if modelMap['refresh_cache']:
        window.getControl(201).setVisible(False)
        window.getControl(202).setVisible(False)
        window.getControl(203).setVisible(False)
        window.getControl(204).setVisible(False)
        window.getControl(300).setVisible(False)
        window.getControl(100).setVisible(False)
        window.getControl(400).setVisible(False)
        window.getControl(500).setVisible(False)
        window.getControl(600).setVisible(False)
        window.getControl(800).setVisible(False)
        window.getControl(900).setVisible(False)
        window.getControl(1000).setVisible(False)
        window.getControl(1100).setVisible(False)
        window.getControl(1200).setVisible(False)
        
        window.getControl(201).setVisible(False)
        window.getControl(202).setVisible(False)
        window.getControl(203).setVisible(True)
        window.getControl(204).setVisible(True)
        window.getControl(206).setPercent(0)
        window.getControl(206).setVisible(True)
        window.getControl(205).setLabel("LOADING TV SHOWS...")
        window.getControl(200).setVisible(True)
        modelMap['progress_control'] = window.getControl(206)
        image = xbmcgui.ControlImage(440, 320, 118, 100, filename="", aspectRatio=0, colorDiffuse='0xFFF7F7F7')
        window.addControl(image)
        image.setVisible(False)
        controls = CacheManager().get('controls_to_be_deleted')
        controls.append(image)
        modelMap['channel_image_control'] = image
    
def show_channels_view(modelMap, window):
    window.getControl(200).setVisible(False)
    window.getControl(300).setVisible(False)
    window.getControl(400).setVisible(False)
    window.getControl(500).setVisible(False)
    window.getControl(600).setVisible(False)
    window.getControl(800).setVisible(False)
    window.getControl(1000).setVisible(False)
    window.getControl(1100).setVisible(False)
    window.getControl(1200).setVisible(False)
    window.getControl(105).reset()
    window.getControl(106).setVisible(False)
    if modelMap.has_key('favorite_tv_shows_items') and modelMap['favorite_tv_shows_items'] is not None and len(modelMap['favorite_tv_shows_items']) > 0:
        window.getControl(105).setVisible(True)
        window.getControl(105).addItems(modelMap['favorite_tv_shows_items'])
        window.getControl(104).setVisible(False)
        window.getControl(1042).setVisible(False)
    else:
        window.getControl(104).setVisible(True)
        window.getControl(1042).setVisible(True)
        window.getControl(105).setVisible(False)
    
    window.getControl(100).setVisible(True)
    window.getControl(102).reset()
    window.getControl(102).addItems(modelMap['tv_channel_items'])
    window.setFocusId(102)
    if len(modelMap['live_tv_channel_items']) > 0:
        window.getControl(108).reset()
        window.getControl(108).addItems(modelMap['live_tv_channel_items'])
        window.setFocusId(108)

def show_tv_shows_view(modelMap, window):
    window.getControl(200).setVisible(False)
    window.getControl(400).setVisible(False)
    window.getControl(600).setVisible(False)
    window.getControl(800).setVisible(False)
    window.getControl(900).setVisible(False)
    window.getControl(100).setVisible(False)
    window.getControl(1000).setVisible(False)
    window.getControl(1100).setVisible(False)
    window.getControl(1200).setVisible(False)
    window.getControl(300).setVisible(True)
    window.getControl(305).setEnabled(True)
    logging.getLogger().debug('total tv shows: %s' % str(len(modelMap['tv_show_items'])))
    window.getControl(305).reset()
    window.getControl(305).addItems(modelMap['tv_show_items'])
    window.setFocusId(305)
    if modelMap.has_key('selected_tv_show_item'):
        window.getControl(305).selectItem(modelMap['selected_tv_show_item'])
    
    window.getControl(303).setLabel(modelMap['channel_name'])
    image = xbmcgui.ControlImage(30, 30, 174, 147, filename=modelMap['channel_image'], aspectRatio=0, colorDiffuse='0xFFF7F7F7')
    window.addControl(image)
    CacheManager().put('channel_image', modelMap['channel_image'])
    controls = CacheManager().get('controls_to_be_deleted')
    controls.append(image)
    logging.getLogger().debug('Inside VIEWS:list of temp controls to add size : %s' % str(len(controls)))
    
def show_tv_show_episodes_view(modelMap, window):
    image = xbmcgui.ControlImage(30, 30, 174, 147, filename=CacheManager().get('channel_image'), aspectRatio=0, colorDiffuse='0xFFF7F7F7')
    window.addControl(image)
    controls = CacheManager().get('controls_to_be_deleted')
    controls.append(image)
    if modelMap.has_key('error-occurred') and modelMap['error-occurred']:
        logging.getLogger().debug('found an error message...')
        window.getControl(500).setVisible(False)
        system.hide_busy_dialog()
        window.getControl(600).setVisible(True)
        window.getControl(305).setEnabled(True)
        logging.getLogger().exception(modelMap['error'])
    else:
        logging.getLogger().debug('total tv show episodes: %s' % str(len(modelMap['tv_show_episode_items'])))
        window.getControl(305).setEnabled(False)
        window.getControl(401).reset()
        window.getControl(401).addItems(modelMap['tv_show_episode_items'])
        window.getControl(400).setVisible(True)
        window.getControl(500).setVisible(False)
        system.hide_busy_dialog()
        window.getControl(600).setVisible(False)
        window.setFocusId(401)
        
def show_tv_channel_episodes_loading_view(modelMap, window):
    #window.getControl(500).setVisible(True)
    #window.getControl(501).setLabel('LOADING CONTENT FOR [B]' + modelMap['channel_name'] + '[/B]...')
    system.show_busy_dialog()
        
def show_tv_channel_episodes_view(modelMap, window):
    window.getControl(200).setVisible(False)
    window.getControl(300).setVisible(False)
    window.getControl(400).setVisible(False)
    window.getControl(600).setVisible(False)
    window.getControl(800).setVisible(False)
    window.getControl(900).setVisible(False)
    window.getControl(100).setVisible(False)
    window.getControl(1001).setLabel(modelMap['channel_name'])
    image = xbmcgui.ControlImage(30, 30, 174, 147, filename=modelMap['channel_image'], aspectRatio=0, colorDiffuse='0xFFF7F7F7')
    window.addControl(image)
    CacheManager().put('channel_image', modelMap['channel_image'])
    controls = CacheManager().get('controls_to_be_deleted')
    controls.append(image)
    system.hide_busy_dialog()
    if modelMap.has_key('error-occurred') and modelMap['error-occurred']:
        logging.getLogger().debug('found an error message...')
        window.getControl(500).setVisible(False)
        system.hide_busy_dialog()
        window.getControl(600).setVisible(True)
        logging.getLogger().exception(modelMap['error'])
    else:
        logging.getLogger().debug('total tv show episodes: %s' % str(len(modelMap['tv_show_episode_items'])))
        window.getControl(1002).reset()
        window.getControl(1002).addItems(modelMap['tv_show_episode_items'])
        window.getControl(1000).setVisible(True)
        window.getControl(500).setVisible(False)
        system.hide_busy_dialog()
        window.getControl(600).setVisible(False)
        window.setFocusId(1002)
    
def show_tv_show_episode_videos_list_view(modelMap, window):
    image = xbmcgui.ControlImage(30, 30, 174, 147, filename=CacheManager().get('channel_image'), aspectRatio=0, colorDiffuse='0xFFF7F7F7')
    window.addControl(image)
    controls = CacheManager().get('controls_to_be_deleted')
    controls.append(image)
    window.getControl(401).reset()
    window.getControl(300).setVisible(False)
    window.getControl(400).setVisible(False)
    window.getControl(500).setVisible(False)
    system.hide_busy_dialog()
    window.getControl(600).setVisible(False)
    
    window.getControl(804).reset()
    logging.getLogger().debug('Channel name in show_tv_show_episode_videos_list_view = %s' % modelMap['channel-name'])
    window.getControl(801).setLabel(modelMap['channel-name'])
    window.getControl(802).setLabel(modelMap['tv-show-name'])
    window.getControl(803).setLabel(modelMap['episode-name'])
    window.getControl(804).addItems(modelMap['videos-item-list'])
    window.getControl(800).setVisible(True)
    window.setFocusId(804)
    
    
def show_tv_channel_episode_videos_list_view(modelMap, window):
    image = xbmcgui.ControlImage(30, 30, 174, 147, filename=CacheManager().get('channel_image'), aspectRatio=0, colorDiffuse='0xFFF7F7F7')
    window.addControl(image)
    controls = CacheManager().get('controls_to_be_deleted')
    controls.append(image)
    window.getControl(500).setVisible(False)
    system.hide_busy_dialog()
    window.getControl(600).setVisible(False)
    window.getControl(1000).setVisible(False)
    
    window.getControl(804).reset()
    logging.getLogger().debug('Channel name in show_tv_show_episode_videos_list_view = %s' % modelMap['channel-name'])
    window.getControl(801).setLabel(modelMap['channel-name'])
    window.getControl(802).setLabel(modelMap['tv-show-name'])
    window.getControl(803).setLabel(modelMap['episode-name'])
    window.getControl(804).addItems(modelMap['videos-item-list'])
    window.getControl(800).setVisible(True)
    window.setFocusId(804)
    
def show_tv_show_options(modelMap, window):
    image = xbmcgui.ControlImage(30, 30, 174, 147, filename=CacheManager().get('channel_image'), aspectRatio=0, colorDiffuse='0xFFF7F7F7')
    window.addControl(image)
    
    controls = CacheManager().get('controls_to_be_deleted')
    controls.append(image)
    
    if modelMap.has_key('error-occurred') and modelMap['error-occurred']:
        logging.getLogger().debug('found an error message...')
        window.getControl(500).setVisible(False)
        system.hide_busy_dialog()
        window.getControl(600).setVisible(True)
        window.getControl(305).setEnabled(True)
        logging.getLogger().exception(modelMap['error'])
    else:
        window.getControl(502).setPercent(100)
        window.getControl(500).setVisible(False)
        system.hide_busy_dialog()
        window.getControl(502).setPercent(0)
        logging.getLogger().debug(len(modelMap['tv-show-images']))
        window.getControl(901).reset()
        
        window.getControl(901).addItems(modelMap['tv-show-images'])
        window.getControl(900).setVisible(True)
        window.getControl(305).setEnabled(False)
        window.setFocusId(901)
        logging.getLogger().debug('list visible')
        
def show_remove_favorite(modelMap, window):
    CacheManager().put('selected_favorite', modelMap['tv-show-name'])
    CacheManager().put('selected_favorite_thumb', modelMap['tv-show-thumb'])
    print window.getControl(106)
    window.getControl(106).setVisible(True)
    window.setFocusId(106)
    logging.getLogger().debug('button control active, use now!!!')
    
def hide_remove_favorite(modelMap, window):
    CacheManager().remove('selected_favorite')
    CacheManager().remove('selected_favorite_thumb')
    window.getControl(106).setVisible(False)
    if modelMap.has_key('reload_favorite_tv_shows_items') and modelMap['reload_favorite_tv_shows_items']:
        window.getControl(105).reset()
        if modelMap.has_key('favorite_tv_shows_items') and modelMap['favorite_tv_shows_items'] is not None and len(modelMap['favorite_tv_shows_items']) > 0:
            window.getControl(105).setVisible(True)
            window.getControl(105).addItems(modelMap['favorite_tv_shows_items'])
            window.getControl(104).setVisible(False)
            window.getControl(1042).setVisible(False)
        else:
            window.getControl(104).setVisible(True)
            window.getControl(1042).setVisible(True)
            window.getControl(105).setVisible(False)
    window.setFocusId(102)
    
def hide_tv_show_options(modelMap, window):
    image = xbmcgui.ControlImage(30, 30, 174, 147, filename=CacheManager().get('channel_image'), aspectRatio=0, colorDiffuse='0xFFF7F7F7')
    window.addControl(image)
    controls = CacheManager().get('controls_to_be_deleted')
    controls.append(image)
    window.getControl(901).reset()

    window.getControl(900).setVisible(False)
    window.getControl(305).setEnabled(True)
    window.setFocusId(305)
    
    
def hide_tv_show_episodes_view(modelMap, window):
    image = xbmcgui.ControlImage(30, 30, 174, 147, filename=CacheManager().get('channel_image'), aspectRatio=0, colorDiffuse='0xFFF7F7F7')
    window.addControl(image)
    controls = CacheManager().get('controls_to_be_deleted')
    controls.append(image)
    window.getControl(401).reset()
    window.getControl(400).setVisible(False)
    window.getControl(500).setVisible(False)
    system.hide_busy_dialog()
    window.getControl(600).setVisible(False)
    window.getControl(305).setEnabled(True)
    window.setFocusId(305)
    
    
def hide_tv_show_episode_videos_list_view(modelMap, window):
    image = xbmcgui.ControlImage(30, 30, 174, 147, filename=CacheManager().get('channel_image'), aspectRatio=0, colorDiffuse='0xFFF7F7F7')
    window.addControl(image)
    controls = CacheManager().get('controls_to_be_deleted')
    controls.append(image)
    window.getControl(800).setVisible(False)
    window.getControl(305).setEnabled(True)
    window.getControl(300).setVisible(True)
    window.getControl(600).setVisible(False)
    window.getControl(500).setVisible(False)
    system.hide_busy_dialog()
    window.setFocusId(305)
    
def hide_tv_channel_episode_videos_list_view(modelMap, window):
    image = xbmcgui.ControlImage(30, 30, 174, 147, filename=CacheManager().get('channel_image'), aspectRatio=0, colorDiffuse='0xFFF7F7F7')
    window.addControl(image)
    controls = CacheManager().get('controls_to_be_deleted')
    controls.append(image)
    window.getControl(800).setVisible(False)
    window.getControl(1000).setVisible(True)
    window.getControl(600).setVisible(False)
    window.getControl(500).setVisible(False)
    system.hide_busy_dialog()
    window.setFocusId(1002)
    
    
def show_tv_show_episode_videos_view(modelMap, window):
    image = xbmcgui.ControlImage(30, 30, 174, 147, filename=CacheManager().get('channel_image'), aspectRatio=0, colorDiffuse='0xFFF7F7F7')
    window.addControl(image)
    controls = CacheManager().get('controls_to_be_deleted')
    controls.append(image)
    if modelMap.has_key('error-occurred') and modelMap['error-occurred']:
        logging.getLogger().debug('found an error message...')
        window.getControl(500).setVisible(False)
        system.hide_busy_dialog()
        window.getControl(600).setVisible(True)
        logging.getLogger().exception(modelMap['error'])
    else:
        window.getControl(502).setPercent(0)
        modelMap['progress_control'] = window.getControl(502)
        window.getControl(501).setLabel('RESOLVING VIDEOS TO BE PLAYED, PLEASE WAIT...')
    

def play_video_streams(modelMap, window):
    image = xbmcgui.ControlImage(30, 30, 174, 147, filename=CacheManager().get('channel_image'), aspectRatio=0, colorDiffuse='0xFFF7F7F7')
    window.addControl(image)
    controls = CacheManager().get('controls_to_be_deleted')
    controls.append(image)
    window.getControl(500).setVisible(False)
    system.hide_busy_dialog()
    logging.getLogger().debug('play video streams found')
    if modelMap.has_key('error-occurred') and modelMap['error-occurred']:
        logging.getLogger().debug('found an error message...')
        window.getControl(600).setVisible(True)
        logging.getLogger().exception(modelMap['error'])
    else:
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        video_items = modelMap['video_streams']
        logging.getLogger().debug('total video streams found = %s' % str(len(video_items)))
        for video_item in video_items:
            playlist.add(url=video_item.getProperty('streamLink'), listitem=video_item)
        logging.getLogger().debug('Playlist size = %s ' % str(playlist.size()))
        xbmc.Player().play(playlist)
    
    
def watch_live_channel(modelMap, window):
    video_item = modelMap['live_item']
    xbmc.Player().play(video_item.getProperty('streamLink'), video_item)
    
    
def handle_select_event(window, control_id):
    try:
        logging.getLogger().debug(window.getFocus())
    except:
        pass
    

def handle_channel_selected(window, control_id):
    logging.getLogger().debug('handle channel selection... ')
    list_control = window.getControl(control_id)
    item = list_control.getSelectedItem()
    req_attrib_map = {}
    if item is not None:
        logging.getLogger().debug('handle channel selected : %s ' % item.getProperty('channel-name'))
        req_attrib_map['channel-name'] = item.getProperty('channel-name')
        req_attrib_map['direct-link'] = item.getProperty('direct-link')
        req_attrib_map['live-link'] = item.getProperty('live-link')
    return req_attrib_map

def handle_favorite_tv_show_selected(window, control_id):
    logging.getLogger().debug('handle favorite tv show selection... ')
    list_control = window.getControl(control_id)
    item = list_control.getSelectedItem()
    req_attrib_map = {}
    if item is not None:
        logging.getLogger().debug('handle tv show selected : %s ' % item.getProperty('tv-show-name'))
        req_attrib_map['channel-type'] = item.getProperty('channel-type')
        req_attrib_map['channel-name'] = item.getProperty('channel-name')
        req_attrib_map['tv-show-name'] = item.getProperty('tv-show-name')
        req_attrib_map['tv-show-url'] = item.getProperty('tv-show-url')
        
        notification = "XBMC.Notification(%s,%s,%s,%s)" % (req_attrib_map['tv-show-name'], 'LOADING EPISODES... ', 2500, 'icon.png')
        xbmc.executebuiltin(notification)
        system.show_busy_dialog()
    
#         window.getControl(500).setVisible(True)
#         window.getControl(501).setLabel('LOADING EPISODES FOR [B]' + req_attrib_map['tv-show-name'] + '[/B]...')
    return req_attrib_map

def handle_favorite_tv_show_selected_for_remove(window, control_id):
    logging.getLogger().debug('handle favorite tv show selection for remove... ')
    list_control = window.getControl(control_id)
    item = list_control.getSelectedItem()
    req_attrib_map = {}
    if item is not None:
        logging.getLogger().debug('handle tv show selected : %s ' % item.getProperty('tv-show-name'))
        req_attrib_map['channel-type'] = item.getProperty('channel-type')
        req_attrib_map['channel-name'] = item.getProperty('channel-name')
        req_attrib_map['tv-show-name'] = item.getProperty('tv-show-name')
        req_attrib_map['tv-show-url'] = item.getProperty('tv-show-url')
        req_attrib_map['tv-show-thumb'] = item.getProperty('tv-show-thumb')
    return req_attrib_map

def handle_tv_show_selected_for_options(window, control_id):
    logging.getLogger().debug('handle tv show selection for options... ')
    list_control = window.getControl(control_id)
    item = list_control.getSelectedItem()
    
    req_attrib_map = {}
    if item is not None:
        logging.getLogger().debug('handle tv show selected : %s ' % item.getProperty('tv-show-name'))
        req_attrib_map['channel-type'] = item.getProperty('channel-type')
        req_attrib_map['channel-name'] = item.getProperty('channel-name')
        req_attrib_map['tv-show-name'] = item.getProperty('tv-show-name')
        req_attrib_map['tv-show-url'] = item.getProperty('tv-show-url')
        window.getControl(305).setEnabled(False)
        
#         window.getControl(500).setVisible(True)
#         window.getControl(502).setPercent(0)
#         window.getControl(501).setLabel('LOADING IMAGES FOR [B]' + req_attrib_map['tv-show-name'] + '[/B]...')
        
        notification = "XBMC.Notification(%s,%s,%s,%s)" % (req_attrib_map['tv-show-name'], 'LOADING IMAGES... ', 2500, 'icon.png')
        xbmc.executebuiltin(notification)
        system.show_busy_dialog()
        
    return req_attrib_map


def handle_tv_show_favorite_selected(window, control_id):
    logging.getLogger().debug('handle tv show favorite selection... ')
    list_control = window.getControl(control_id)
    item = list_control.getSelectedItem()
    
    req_attrib_map = {}
    if item is not None:
        logging.getLogger().debug('handle add to tv show favorite selected : %s ' % item.getProperty('tv-show-name'))
        req_attrib_map['channel-type'] = item.getProperty('channel-type')
        req_attrib_map['channel-name'] = item.getProperty('channel-name')
        req_attrib_map['tv-show-name'] = item.getProperty('tv-show-name')
        req_attrib_map['tv-show-url'] = item.getProperty('tv-show-url')
        req_attrib_map['tv-show-thumb'] = item.getProperty('tv-show-thumb')
        
    return req_attrib_map
    
    
def handle_tv_show_selected(window, control_id):
    logging.getLogger().debug('handle tv show selection... ')
    list_control = window.getControl(control_id)
    item = list_control.getSelectedItem()
    
    req_attrib_map = {}
    if item is not None:
        logging.getLogger().debug('handle tv show selected : %s ' % item.getProperty('tv-show-name'))
        req_attrib_map['channel-type'] = item.getProperty('channel-type')
        req_attrib_map['channel-name'] = item.getProperty('channel-name')
        req_attrib_map['tv-show-name'] = item.getProperty('tv-show-name')
        req_attrib_map['tv-show-url'] = item.getProperty('tv-show-url')
        window.getControl(305).setEnabled(False)
        
#         window.getControl(500).setVisible(True)
#         window.getControl(501).setLabel('LOADING EPISODES FOR [B]' + req_attrib_map['tv-show-name'] + '[/B]...')
        
        notification = "XBMC.Notification(%s,%s,%s,%s)" % (req_attrib_map['tv-show-name'], 'LOADING EPISODES... ', 2500, 'icon.png')
        xbmc.executebuiltin(notification)
        system.show_busy_dialog()
        
    return req_attrib_map


def handle_tv_show_episode_selected(window, control_id):
    logging.getLogger().debug('handle tv show episode selection... ')
    list_control = window.getControl(control_id)
    item = list_control.getSelectedItem()
    
    req_attrib_map = {}
    if item is not None:
        logging.getLogger().debug('handle tv show episode selected : %s : with page = %s' % (item.getProperty('tv-show-name'), item.getProperty('tv-show-page')))
        req_attrib_map['channel-type'] = item.getProperty('channel-type')
        req_attrib_map['channel-name'] = item.getProperty('channel-name')
        req_attrib_map['tv-show-name'] = item.getProperty('tv-show-name')
        req_attrib_map['tv-show-url'] = item.getProperty('tv-show-url')
        req_attrib_map['tv-show-page'] = item.getProperty('tv-show-page')
        req_attrib_map['episode-name'] = item.getProperty('episode-name')
        req_attrib_map['episode-url'] = item.getProperty('episode-url')
        window.getControl(600).setVisible(False)
#         window.getControl(500).setVisible(True)
#         window.getControl(501).setLabel('LOADING VIDEOS FOR [B]' + req_attrib_map['episode-name'] + '[/B]...')

        notification = "XBMC.Notification(%s,%s,%s,%s)" % (req_attrib_map['tv-show-name']+ ' - ' + req_attrib_map['episode-name'], 'LOADING VIDEOS... ', 2500, 'icon.png')
        xbmc.executebuiltin(notification)
        system.show_busy_dialog()
        
        logging.getLogger().debug('Channel name in handle_tv_show_episode_selected = %s' % req_attrib_map['channel-name'])
    return req_attrib_map

def handle_tv_show_episode_video_selected(window, control_id):
    logging.getLogger().debug('handle tv show episode video selection... ')
    
    list_control = window.getControl(control_id)
    item = list_control.getSelectedItem()
    
    req_attrib_map = {}
    if item is not None:
        logging.getLogger().debug('handle tv show episode video source : %s : and continuous play item  = %s' % (item.getProperty('videoSourceName'), item.getProperty('isContinuousPlayItem')))
        
        req_attrib_map['video-source-name'] = item.getProperty('videoSourceName')
        req_attrib_map['is-playlist'] = item.getProperty('isContinuousPlayItem')
        if req_attrib_map['is-playlist'] == 'true':
            req_attrib_map['videos'] = item.getProperty('videosList')
        else:
            req_attrib_map['video-link'] = item.getProperty('videoLink')
            req_attrib_map['video-title'] = item.getProperty('videoTitle')
        window.getControl(600).setVisible(False)
        
#         window.getControl(500).setVisible(True)
#         window.getControl(501).setLabel('LOADING VIDEOS FROM [B]' + req_attrib_map['video-source-name'] + '[/B]...')

        notification = "XBMC.Notification(%s,%s,%s,%s)" % (req_attrib_map['video-source-name'], 'LOADING VIDEOS... ', 2500, 'icon.png')
        xbmc.executebuiltin(notification)
        system.show_busy_dialog()
        
        req_attrib_map['progress_control'] = window.getControl(502)
        
    return req_attrib_map
