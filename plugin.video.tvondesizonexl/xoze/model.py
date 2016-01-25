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
from xoze.lib import importlib
import logging

class MoveManager(object):
    """ MoveManager manages 
            *  the execution of move
            *  passing appropriate input parameters to each move function.
            *  invoking controller callback function for changing the view."""
            
    def __init__(self, dispatch_view_func, redirect_action_func, addon, addon_path):
        self._dispatch_view = dispatch_view_func
        self._redirect_action_func = redirect_action_func
        self._addon_path = addon_path
        logging.getLogger().info('MoveManager initialized.')
        
        
    def execute_moves(self, moves, req_attrib):
        if moves is None or len(moves) == 0:
            logging.getLogger().debug('No moves found for execution, return now.')
            return
        else:
            logging.getLogger().debug('total moves to be executed: %s' % (len(moves)))
            modelMap = {}
            for move in moves:
                logging.getLogger().debug('move to be executed: %s.%s' % (move.module, move.function))
                module = importlib.import_module(move.module, self._addon_path)
                function = getattr(module, move.function)
                """Each function call returns True or False or None value to indicate if the process can proceed with next move execution"""
                proceed_ind = None
                try:
                    proceed_ind = function(req_attrib, modelMap)
                except Exception,e:
                    modelMap['error-occurred'] = True
                    modelMap['error'] = e
                    proceed_ind = False
                
                if move.view_id is not None:
                    logging.getLogger().debug('move has a view: %s' % (move.view_id))
                    self._dispatch_view(move.view_id, modelMap)
                if proceed_ind is not None:
                    if proceed_ind is False:
                        logging.getLogger().error('received not to proceed indicator from last move: %s.%s' % (move.module, move.function))
                        break
                    elif proceed_ind.startswith('redirect:'):
                        self._redirect_action_func(proceed_ind.replace('redirect:', '', 1), req_attrib)
                        break
                
            return modelMap
        
    def do_clean(self):
        """This function clean all objects created by this object and will also call do_clean() functions of its child objects where ever applicable. Call to this function is internal, donot make explicit call."""
        del self._dispatch_view
        del self._addon_path
