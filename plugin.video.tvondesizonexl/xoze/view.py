'''
Created on Sep 28, 2013

@author: 'ajdeveloped'

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
from xoze.lib import importlib, MyFont
from xoze.utils import system
from xoze.utils.cache import CacheManager
import logging
try:
    import xbmcgui  # @UnresolvedImport
except:
    from xoze.alternatives import xbmcdummy as xbmcgui


class ViewRenderer(object):
    
    def __init__(self, do_action_func, addon, addon_path):
        self._do_action_func = do_action_func
        self._addon_path = addon_path
        self._theme = addon.getSetting('theme')
        window_name = 'AddonWindow.xml'
        if self._theme is None or self._theme == '' or self._theme == '0':
            window_name = 'AddonWindow.xml'
        else:
            window_name = 'AddonWindow_' + self._theme + '.xml'
        logging.getLogger().debug('Going to load fonts.')
        MyFont.FontModifier(addon_path).loadMyFontFile()
        logging.getLogger().debug('Going to load window with name: %s' % window_name)
        self._addon_window = AddonWindow(window_name, addon_path)
        self._addon_window.set_handle_event_func(self.handle_event)
        self._current_view = None
        CacheManager().put('controls_to_be_deleted', [])
        
    
    def render(self, view, modelMap):
        """Invokes service response builder that prepares map of key-value pairs to be returned in response."""
        module = importlib.import_module(view.module, self._addon_path)
        function = getattr(module, view.function)
        self._current_view = view
        """Delete temporary controls created using python in last view. Example ControlImage created in python... """
        controls_to_delete = CacheManager().remove('controls_to_be_deleted')
        if controls_to_delete is not None:
            logging.getLogger().debug('List of controls to remove size : %s' % str(len(controls_to_delete)))
            self._addon_window.removeControls(controls_to_delete)
            del controls_to_delete
            CacheManager().put('controls_to_be_deleted', [])
        
        """Each function call returns Service Response map"""
        function(modelMap, self._addon_window)
    
    def handle_event(self, intent, control_id=0):
        logging.getLogger().debug('handling an event for intent : %s on control : %s' % (intent, str(control_id)))
        req_attr_map = None
        action_id = None
        for event in self._current_view.events:
            if((event.intent == intent and (event.control_id == str(control_id) or event.control_id == '')) or event.intent == ''):
                """Invokes service response builder that prepares map of key-value pairs to be returned in response."""
                if event.module is not None:
                    logging.getLogger().debug('Executing module : %s.%s' % (event.module, event.function))
                    module = importlib.import_module(event.module, self._addon_path)
                    function = getattr(module, event.function)
                    """Each function call returns Service Response map"""
                    req_attr_map = function(self._addon_window, control_id)
                action_id = event.action_id
        if action_id is not None:
            self._do_action_func(action_id, req_attr_map)
    
    def display_addon_window(self):
        self._addon_window.doModal()
        
    def close_addon_window(self):
        self._addon_window.close()
    
    def do_clean(self):
        """This function clean all objects created by this object and will also call do_clean() functions of its child objects where ever applicable. Call to this function is internal, donot make explicit call."""
        if self._current_view is not None:
            del self._current_view
        if self._addon_window is not None:
            del self._addon_window
        del self._addon_path


# define ACTION_NONE                    0
# define ACTION_MOVE_LEFT               1
# define ACTION_MOVE_RIGHT              2
# define ACTION_MOVE_UP                 3
# define ACTION_MOVE_DOWN               4
# define ACTION_PAGE_UP                 5
# define ACTION_PAGE_DOWN               6
# define ACTION_SELECT_ITEM             7
# define ACTION_HIGHLIGHT_ITEM          8
# define ACTION_PARENT_DIR              9
# define ACTION_PREVIOUS_MENU          10
# define ACTION_SHOW_INFO              11

# define ACTION_MOUSE_LEFT_CLICK       100
# define ACTION_MOUSE_RIGHT_CLICK      101
# define ACTION_MOUSE_MIDDLE_CLICK     102
# define ACTION_MOUSE_DOUBLE_CLICK     103
# define ACTION_MOUSE_WHEEL_UP         104
# define ACTION_MOUSE_WHEEL_DOWN       105

ACTION_INTENT_TEXT_MAPPING = {0: 'ACTION_NONE', 1:'ACTION_MOVE_LEFT', 2:'ACTION_MOVE_RIGHT', 3:'ACTION_MOVE_UP', 4:'ACTION_MOVE_DOWN', 5:'ACTION_PAGE_UP', 6:'ACTION_PAGE_DOWN', 7:'ACTION_SELECT_ITEM', 8:'ACTION_HIGHLIGHT_ITEM', 9:'ACTION_PARENT_DIR', 10:'ACTION_PREVIOUS_MENU', 11:'ACTION_SHOW_INFO', 92:'ACTION_NAV_BACK', 100:'ACTION_MOUSE_LEFT_CLICK', 101:'ACTION_MOUSE_RIGHT_CLICK', 102:'ACTION_MOUSE_MIDDLE_CLICK', 103:'ACTION_MOUSE_DOUBLE_CLICK', 104:'ACTION_MOUSE_WHEEL_UP', 105:'ACTION_MOUSE_WHEEL_DOWN', 117:'ACTION_CONTEXT_MENU', 135:'ACTION_ENTER', 401:'ACTION_TOUCH_TAP', 410:'ACTION_TOUCH_TAP_TEN', 411:'ACTION_TOUCH_LONGPRESS', 420:'ACTION_TOUCH_LONGPRESS_TEN'}

class AddonWindow(xbmcgui.WindowXML):
    
    def onInit(self):
        logging.getLogger().debug('Window OnInit called...')
        system.hide_busy_dialog()
        self._handle_event_func('INIT')
    
    def set_handle_event_func(self, handle_event_func):
        self._handle_event_func = handle_event_func
    
    def onAction(self, action):
        logging.getLogger().debug(action.getId())
        if ACTION_INTENT_TEXT_MAPPING.has_key(action.getId()):
            try:
                fucused_control_id = self.getFocusId()
                self._handle_event_func(ACTION_INTENT_TEXT_MAPPING.get(action.getId()), fucused_control_id)
            except:
                self._handle_event_func(ACTION_INTENT_TEXT_MAPPING.get(action.getId()))

    def onClick(self, control):
        pass
        # logging.getLogger().debug('Click event received for control %s' % str(control))
        
    def onFocus(self, control):
        pass
        # logging.getLogger().debug('Focus event received for control %s' % str(control))
