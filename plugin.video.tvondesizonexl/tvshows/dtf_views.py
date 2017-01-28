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
        
        window.getControl(201).setVisible(False)
        window.getControl(202).setVisible(False)
        window.getControl(203).setVisible(True)
        window.getControl(204).setVisible(True)
        window.getControl(206).setVisible(True)
        window.getControl(205).setLabel("LOADING TV SHOWS...")
        window.getControl(200).setVisible(True)
        modelMap['progress_control'] = window.getControl(206)
        
def show_soon_view(modelMap, window):
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
    
    window.getControl(201).setVisible(False)
    window.getControl(202).setVisible(False)
    window.getControl(203).setVisible(True)
    window.getControl(204).setVisible(True)
    window.getControl(206).setVisible(False)
    window.getControl(205).setLabel("COMING SOON, USE [B]DESIRULEZ[/B] SOURCE.")
    window.getControl(200).setVisible(True)
    
def show_channels_view(modelMap, window):
    window.getControl(200).setVisible(False)
    window.getControl(300).setVisible(False)
    window.getControl(400).setVisible(False)
    window.getControl(500).setVisible(False)
    window.getControl(600).setVisible(False)
    window.getControl(100).setVisible(True)
    window.getControl(102).reset()
    window.getControl(102).addItems(modelMap['tv_channel_items'])
    window.setFocusId(102)

def show_tv_shows_view(modelMap, window):
    window.getControl(200).setVisible(False)
    window.getControl(400).setVisible(False)
    window.getControl(500).setVisible(False)
    window.getControl(600).setVisible(False)
    window.getControl(100).setVisible(False)
    window.getControl(300).setVisible(True)
    logging.getLogger().debug('total tv shows: %s' % str(len(modelMap['tv_show_items'])))
    window.getControl(305).reset()
    window.getControl(305).addItems(modelMap['tv_show_items'])
    window.setFocusId(305)
    window.getControl(303).setLabel(modelMap['channel_name'])
    image = xbmcgui.ControlImage(30, 30, 174, 147, filename=modelMap['channel_image'], aspectRatio=0, colorDiffuse='0xFFD1EEFC')
    window.addControl(image)
    CacheManager().put('channel_image', modelMap['channel_image'])
    controls = CacheManager().get('controls_to_be_deleted')
    controls.append(image)
    logging.getLogger().debug('Inside VIEWS:list of temp controls to add size : %s' % str(len(controls)))
    
def show_tv_show_episodes_view(modelMap, window):
    image = xbmcgui.ControlImage(30, 30, 174, 147, filename=CacheManager().get('channel_image'), aspectRatio=0, colorDiffuse='0xFFD1EEFC')
    window.addControl(image)
    controls = CacheManager().get('controls_to_be_deleted')
    controls.append(image)
    if modelMap.has_key('error-occurred') and modelMap['error-occurred']:
        logging.getLogger().debug('found an error message...')
        window.getControl(500).setVisible(False)
        window.getControl(600).setVisible(True)
        logging.getLogger().exception(modelMap['error'])
    else:
        logging.getLogger().debug('total tv show episodes: %s' % str(len(modelMap['tv_show_episode_items'])))
        window.getControl(305).setEnabled(False)
        window.getControl(401).reset()
        window.getControl(401).addItems(modelMap['tv_show_episode_items'])
        window.getControl(400).setVisible(True)
        window.getControl(500).setVisible(False)
        window.getControl(600).setVisible(False)
        window.setFocusId(401)
    
def hide_tv_show_episodes_view(modelMap, window):
    image = xbmcgui.ControlImage(30, 30, 174, 147, filename=CacheManager().get('channel_image'), aspectRatio=0, colorDiffuse='0xFFD1EEFC')
    window.addControl(image)
    controls = CacheManager().get('controls_to_be_deleted')
    controls.append(image)
    window.getControl(401).reset()
    window.getControl(400).setVisible(False)
    window.getControl(500).setVisible(False)
    window.getControl(600).setVisible(False)
    window.getControl(305).setEnabled(True)
    window.setFocusId(305)
    
    
def show_tv_show_episode_videos_view(modelMap, window):
    image = xbmcgui.ControlImage(30, 30, 174, 147, filename=CacheManager().get('channel_image'), aspectRatio=0, colorDiffuse='0xFFD1EEFC')
    window.addControl(image)
    controls = CacheManager().get('controls_to_be_deleted')
    controls.append(image)
    if modelMap.has_key('error-occurred') and modelMap['error-occurred']:
        logging.getLogger().debug('found an error message...')
        window.getControl(500).setVisible(False)
        window.getControl(600).setVisible(True)
        logging.getLogger().exception(modelMap['error'])
    else:
        modelMap['progress_control'] = window.getControl(502)
        window.getControl(501).setLabel('RESOLVING VIDEOS TO BE PLAYED, PLEASE WAIT...')
    

def play_video_streams(modelMap, window):
    image = xbmcgui.ControlImage(30, 30, 174, 147, filename=CacheManager().get('channel_image'), aspectRatio=0, colorDiffuse='0xFFD1EEFC')
    window.addControl(image)
    controls = CacheManager().get('controls_to_be_deleted')
    controls.append(image)
    window.getControl(500).setVisible(False)
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
    return req_attrib_map
    
def handle_tv_show_selected(window, control_id):
    logging.getLogger().debug('handle tv show selection... ')
    list_control = window.getControl(control_id)
    item = list_control.getSelectedItem()
    
    req_attrib_map = {}
    if item is not None:
        logging.getLogger().debug('handle tv show selected : %s ' % item.getProperty('tv-show-name'))
        req_attrib_map['channel-type'] = item.getProperty('channel-type')
        req_attrib_map['tv-show-name'] = item.getProperty('tv-show-name')
        req_attrib_map['tv-show-url'] = item.getProperty('tv-show-url')
        window.getControl(500).setVisible(True)
        window.getControl(501).setLabel('LOADING EPISODES FOR [B]' + req_attrib_map['tv-show-name'] + '[/B]...')
        
    return req_attrib_map


def handle_tv_show_episode_selected(window, control_id):
    logging.getLogger().debug('handle tv show episode selection... ')
    list_control = window.getControl(control_id)
    item = list_control.getSelectedItem()
    
    req_attrib_map = {}
    if item is not None:
        logging.getLogger().debug('handle tv show episode selected : %s : with page = %s' % (item.getProperty('tv-show-name'), item.getProperty('tv-show-page')))
        req_attrib_map['channel-type'] = item.getProperty('channel-type')
        req_attrib_map['tv-show-name'] = item.getProperty('tv-show-name')
        req_attrib_map['tv-show-url'] = item.getProperty('tv-show-url')
        req_attrib_map['tv-show-page'] = item.getProperty('tv-show-page')
        req_attrib_map['episode-name'] = item.getProperty('episode-name')
        req_attrib_map['episode-url'] = item.getProperty('episode-url')
        window.getControl(500).setVisible(True)
        window.getControl(501).setLabel('LOADING VIDEOS FOR [B]' + req_attrib_map['episode-name'] + '[/B]...')
        
    return req_attrib_map