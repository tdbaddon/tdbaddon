'''
Created on Nov 30, 2013

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
import logging

def show_start_view(modelMap, window):
    logging.getLogger().debug('starting addon')

def show_wish_view(modelMap, window):
    logging.getLogger().debug('starting wish window')
    window.getControl(100).setVisible(False)
    window.getControl(200).setVisible(False)
    window.getControl(300).setVisible(False)
    window.getControl(400).setVisible(False)
    window.getControl(500).setVisible(False)
    window.getControl(600).setVisible(False)
    window.getControl(800).setVisible(False)
    window.getControl(900).setVisible(False)
    window.getControl(700).setVisible(True)
    window.setFocusId(701)


def handle_wish_closed(window, control_id):
    logging.getLogger().debug('closing wish and proceed')
    window.getControl(700).setVisible(False)
    
def handle_init(window, control_id):
    window.getControl(100).setVisible(False)
    window.getControl(200).setVisible(False)
    window.getControl(300).setVisible(False)
    window.getControl(400).setVisible(False)
    window.getControl(500).setVisible(False)
    window.getControl(600).setVisible(False)
    window.getControl(700).setVisible(False)
    window.getControl(800).setVisible(False)
    window.getControl(900).setVisible(False)
    window.getControl(1000).setVisible(False)
    window.getControl(1100).setVisible(True)
    window.getControl(1200).setVisible(False)
    window.setFocusId(1100)
    displayBackControl = AddonContext().get_addon().getSetting('displayBackControl')
    if displayBackControl is not None and displayBackControl == 'true':
        window.getControl(10).setVisible(True)
    else:
        window.getControl(10).setVisible(False)
    
def show_tv_source_view(modelMap, window):
    window.getControl(100).setVisible(False)
    window.getControl(200).setVisible(False)
    window.getControl(300).setVisible(False)
    window.getControl(400).setVisible(False)
    window.getControl(500).setVisible(False)
    window.getControl(600).setVisible(False)
    window.getControl(800).setVisible(False)
    window.getControl(1000).setVisible(False)
    window.getControl(1100).setVisible(False)
    window.getControl(1202).reset()
    window.getControl(1200).setVisible(True)
    window.getControl(1202).addItems(modelMap['tv_sources_items'])
    window.setFocusId(1202)
    
def handle_tv_source_selected(window, control_id):
    logging.getLogger().debug('handle tv source selection... ')
    list_control = window.getControl(control_id)
    item = list_control.getSelectedItem()
    
    req_attrib_map = {}
    if item is not None:
        logging.getLogger().debug('handle tv source selected : %s ' % item.getProperty('source-name'))
        req_attrib_map['source-id'] = item.getProperty('source-id')
        
    return req_attrib_map
