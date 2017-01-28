
'''
Created on Oct 12, 2013

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

class Actions:
    """Holds the information read from xoze.xml."""

    def __init__(self):
        self.__services = []
        self.__actions = []
        self.__views = []


    def get_services(self):
        return self.__services


    def set_services(self, value):
        self.__services = value


    def del_services(self):
        del self.__services


    def get_actions(self):
        return self.__actions


    def get_views(self):
        return self.__views


    def set_actions(self, value):
        self.__actions = value


    def set_views(self, value):
        self.__views = value


    def del_actions(self):
        del self.__actions


    def del_views(self):
        del self.__views
        
    __actions = None
    __views = None
    __services = None
    actions = property(get_actions, set_actions, del_actions, "Actions allowed in XBMC add-on.")
    views = property(get_views, set_views, del_views, "Views set for various XBMC actions.")
    services = property(get_services, set_services, del_services, "services's docstring")
    
    
class Action:
    """ Action includes multiple moves that are executed in the sequence same as written in XML. 
        Each action is identified uniquely using attribute "id".
    """
    
    def __init__(self, action_id):
        self.__id = action_id
        self.__moves = []

    def get_id(self):
        return self.__id


    def get_moves(self):
        return self.__moves


    def set_id(self, value):
        self.__id = value


    def set_moves(self, value):
        self.__moves = value


    def del_id(self):
        del self.__id


    def del_moves(self):
        del self.__moves

    __id = None
    __moves = None
    id = property(get_id, set_id, del_id, "A unique identifier refers to an Action.")
    moves = property(get_moves, set_moves, del_moves, "Action contains a set of moves those are invoked in same sequence as written in XML. Moves are not related to each other.")
    
    
class Move:
    """ Move is an execution of module function. """

    def __init__(self, module, function):
        self.__module = module
        self.__function = function


    def get_view_id(self):
        return self.__view_id


    def set_view_id(self, value):
        self.__view_id = value


    def del_view_id(self):
        del self.__view_id


    def get_module(self):
        return self.__module


    def get_function(self):
        return self.__function


    def set_module(self, value):
        self.__module = value


    def set_function(self, value):
        self.__function = value


    def del_module(self):
        del self.__module


    def del_function(self):
        del self.__function

    
    __module = None
    __function = None
    __view_id = None
    module = property(get_module, set_module, del_module, "Module name is the python module within which given function will be picked and invoked.")
    function = property(get_function, set_function, del_function, "Function name contains the business logic to populate model information to be used for view.")
    view_id = property(get_view_id, set_view_id, del_view_id, "An optional view for this move if there is any change needed for UI after execution of this move.")
     
    
class View:
    """ View responsible for presenting content in a container defined using XBMC skin XML. The events fired from containers can be captured using event defined within View. """

    def __init__(self, view_id, module, function):
        self.__id = view_id
        self.__module = module
        self.__function = function
        self.__events = []

    def get_id(self):
        return self.__id


    def set_id(self, value):
        self.__id = value


    def del_id(self):
        del self.__id


    def get_module(self):
        return self.__module


    def get_function(self):
        return self.__function


    def get_events(self):
        return self.__events


    def set_module(self, value):
        self.__module = value


    def set_function(self, value):
        self.__function = value


    def set_events(self, value):
        self.__events = value
        

    def del_module(self):
        del self.__module


    def del_function(self):
        del self.__function


    def del_events(self):
        del self.__events

    __module = None
    __function = None
    __events = None
    __id = None
    
    module = property(get_module, set_module, del_module, "Module name is the python module within which given function will be picked and invoked.")
    function = property(get_function, set_function, del_function, "Function name contains the business logic to populate model information to be used for view.")
    events = property(get_events, set_events, del_events, "Events fired by view contents.")
    id = property(get_id, set_id, del_id, "id's docstring")
    
    
class Event:
    """ An event fired by content of View. """

    def __init__(self, control_id, intent, action_id=None, module=None, function=None):
        self.__module = module
        self.__function = function
        self.__action_id = action_id
        self.__control_id = control_id
        self.__intent = intent


    def get_module(self):
        return self.__module


    def get_function(self):
        return self.__function


    def get_action_id(self):
        return self.__action_id


    def get_control_id(self):
        return self.__control_id


    def get_intent(self):
        return self.__intent


    def set_module(self, value):
        self.__module = value


    def set_function(self, value):
        self.__function = value


    def set_action_id(self, value):
        self.__action_id = value


    def set_control_id(self, value):
        self.__control_id = value


    def set_intent(self, value):
        self.__intent = value


    def del_module(self):
        del self.__module


    def del_function(self):
        del self.__function


    def del_action_id(self):
        del self.__action_id


    def del_control_id(self):
        del self.__control_id


    def del_intent(self):
        del self.__intent

    
    __module = None
    __function = None
    __action_id = None
    __control_id = None
    __intent = None
    module = property(get_module, set_module, del_module, "Module name is the python module within which given function will be picked and invoked.")
    function = property(get_function, set_function, del_function, "Function name contains the business logic to populate model information to be used for view.")
    action_id = property(get_action_id, set_action_id, del_action_id, "A unique identifier refers to an Action.")
    control_id = property(get_control_id, set_control_id, del_control_id, "A unique identifier refers an control in XBMC skin XML.")
    intent = property(get_intent, set_intent, del_intent, "Event intention.")
    
    
class Service:
    """ An Action can be exposed as service through JSON-RPC library included in XOZE. """

    def __init__(self, path, action_id, module, function):
        self.__path = path
        self.__action_id = action_id
        self.__module = module
        self.__function = function

    def get_module(self):
        return self.__module


    def get_function(self):
        return self.__function


    def set_module(self, value):
        self.__module = value


    def set_function(self, value):
        self.__function = value


    def del_module(self):
        del self.__module


    def del_function(self):
        del self.__function


    def get_path(self):
        return self.__path


    def get_action_id(self):
        return self.__action_id


    def set_path(self, value):
        self.__path = value


    def set_action_id(self, value):
        self.__action_id = value


    def del_path(self):
        del self.__path


    def del_action_id(self):
        del self.__action_id
        
    
    __path = None
    __action_id = None
    __module = None
    __function = None
    path = property(get_path, set_path, del_path, "Service Path to perform an action")
    action_id = property(get_action_id, set_action_id, del_action_id, "A unique identifier refers to an Action.")
    module = property(get_module, set_module, del_module, "Module name is the python module within which given function will be picked and invoked.")
    function = property(get_function, set_function, del_function, "Function name contains the business logic to build set of values to be passed back in service response.")
    
    