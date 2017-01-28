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
from model import MoveManager
from view import ViewRenderer
import logging

class ActionController(object):
    """Controls the execution of actions based on on action_id and also takes care of View dispatch based on view_id"""
    def __init__(self, actions, views, addon, addon_path):
        self._move_manager = MoveManager(self.dispatch_view, self.redirect_action, addon, addon_path)
        self._view_renderer = ViewRenderer(self.do_action, addon, addon_path)
        self._actions = actions
        self._views = views
        logging.getLogger().debug('ActionController ready to control actions...')
        
    def do_action(self, action_id, req_attrib={}):
        logging.getLogger().debug('do action: %s' % (action_id))
        modelMap = None
        for action in self._actions:
            if action.id == action_id:
                modelMap = self._move_manager.execute_moves(action.moves, req_attrib)
                break
        if action_id == 'start':
            self._view_renderer.display_addon_window()
        elif action_id == 'end':
            self._view_renderer.close_addon_window()
        return modelMap
    
    
    def redirect_action(self, action_id, req_attrib={}):
        self.do_action(action_id, req_attrib)
        
    def dispatch_view(self, view_id, modelMap):
        logging.getLogger().debug('dispatch view: %s' % (view_id))
        for view in self._views:
            if view.id == view_id:
                self._view_renderer.render(view, modelMap)
                break
            
    def do_clean(self):
        """This function clean all objects created by this object and will also call do_clean() functions of its child objects where ever applicable. Call to this function is internal, donot make explicit call."""
        self._move_manager.do_clean()
        self._view_renderer.do_clean()
        del self._move_manager
        del self._view_renderer
        del self._actions
        del self._views
