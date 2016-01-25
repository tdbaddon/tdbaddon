'''
Created on Nov 24, 2013

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
import logging
import xbmcgui  # @UnresolvedImport

def start_addon(req_attrib, modelMap):
    logging.getLogger().debug('Hello ***********************')
    logging.getLogger().debug(req_attrib)
    
def check_wish(req_attrib, modelMap):
    logging.getLogger().debug('Wish needed ***********************')
    
    logging.getLogger().debug('Wish settings = %s' % AddonContext().get_addon().getSetting('wishDisplayed'))
    displayedCounter = AddonContext().get_addon().getSetting('wishDisplayed')
    if displayedCounter == '' or displayedCounter == 'hide':
        if int(AddonContext().get_addon().getSetting('tvShowsSource')) == 0:
            return 'redirect:displaySourceList'
        else:
            return 'redirect:determineSource'

def end_menu(req_attrib, modelMap):
    logging.getLogger().debug('end menu ***********************')
    if int(AddonContext().get_addon().getSetting('tvShowsSource')) == 0:
        return 'redirect:displaySourceList'
    else:
        return 'redirect:end'
    
def display_wish(req_attrib, modelMap):
    logging.getLogger().debug('Wish needed ***********************')
    displayedCounter = int(AddonContext().get_addon().getSetting('wishDisplayed'))
    modelMap['displayedCounter'] = displayedCounter
    
def load_source_list(req_attrib, modelMap):
    logging.getLogger().debug('TV Source List ***********************')
    tv_sources_items = []
    item = xbmcgui.ListItem(label='DesiRulez', iconImage='desirulez.png', thumbnailImage='desirulez.png')
    item.setProperty('source-id', '1')
    item.setProperty('source-name', 'DesiRulez')
    tv_sources_items.append(item)
    item = xbmcgui.ListItem(label='DesiTVBox', iconImage='desitvbox.gif', thumbnailImage='desitvbox.gif')
    item.setProperty('source-id', '2')
    item.setProperty('source-name', 'DesiTVBox')
    tv_sources_items.append(item)
    modelMap['tv_sources_items'] = tv_sources_items
    
def determine_source(req_attrib, modelMap):
    if req_attrib is not None and req_attrib.has_key('source-id'):
        sourceChosen = int(req_attrib['source-id'])
    else:
        sourceChosen = int(AddonContext().get_addon().getSetting('tvShowsSource'))
    if sourceChosen == 1:
        return 'redirect:dr-checkCache'
    elif sourceChosen == 2:
        return 'redirect:dtb-checkCache'
    
def end_addon(req_attrib, modelMap):
    logging.getLogger().debug('BYE bye ***********************')
    logging.getLogger().debug(req_attrib)
    
def resolve_stream(req_attrib, modelMap):
    logging.getLogger().debug('Resolve stream...')
    logging.getLogger().debug(req_attrib)
    modelMap['video_item'] = SnapVideo().resolveVideoStream(req_attrib['videoLink'])
    
def set_stream_in_response(modelMap):
    video_item = modelMap['video_item']
    response = {'status':'success'}
    response['streamLink'] = video_item.getProperty('streamLink')
    return response
