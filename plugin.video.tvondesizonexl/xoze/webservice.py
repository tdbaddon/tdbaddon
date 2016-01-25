'''
Created on Oct 13, 2013

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
from threading import Thread
from xoze.lib import importlib
from xoze.lib.jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer, \
    SimpleJSONRPCRequestHandler
from xoze.utils import system
from xoze.utils.patterns import Singleton
import logging
import time


class ServicePublisher(object):
    """Provides following functionality:
        * Register services listed in xoze.xml
        * Start JSON RPC Server
        * Executes service response builders
    """
    
    def __init__(self, addon_context, services, action_controller, context_root, service_port, addon_path):
        self._addon_context = addon_context
        self._services = services
        self._action_controller = action_controller
        self._context_root = context_root
        self._service_port = service_port
        self._server = None
        self._addon_path = addon_path
        
    
    def _service_method(self, name, **params):
        """This method is called for each service request that corresponds to an action. It invokes action using id. After action execution, invokes service response builder."""
        action_id = None
        for service in self._services:
            if name == service.path:
                action_id = service.action_id
                break
        service_resp = None
        try:
            modelMap = self._action_controller.do_action(action_id, params)
            service_resp = self._invoke_resp_builder(service.module, service.function, modelMap)
            logging.getLogger().debug('service response: ')
            logging.getLogger().debug(service_resp)
        except Exception, e:
            logging.getLogger().error('exception occurred for service name: %s' % (name))
            logging.getLogger().exception(e)
            service_resp = {"status":"exception", "message":"an unexpected error occurred, please check your input"}
        return service_resp
    
    
    def _invoke_resp_builder(self, module_name, function_name, modelMap):
        """Invokes service response builder that prepares map of key-value pairs to be returned in response."""
        module = importlib.import_module(module_name, self._addon_path)
        function = getattr(module, function_name)
        """Each function call returns Service Response map"""
        return function(modelMap)
    
    
    def publish_services(self):
        """This method registers the services and starts the JSON RPC server to listen incoming requests."""
        logging.getLogger().debug('publishing web services using JSON RPC Server instance for service path: %s' % (self._context_root))
        if len(self._services) == 0:
            logging.getLogger().error('no services defined for registration, end this service program now.')
            return
        self._server = JSONRPCServer(context_root=self._context_root, server_port=self._service_port)
        for service in self._services:
            self._server.registerService(service.path, self._service_method)
            logging.getLogger().debug('service registered = %s @ %s' % (service.path, self._context_root))
        self._server.start()
        
        
    def unpublish_services(self):
        self._server.stop()
        
        
    def do_clean(self):
        del self._services
        del self._action_controller
        del self._context_root
        del self._service_port
        del self._server
        del self._addon_path


def log_request(self, *args, **kwargs):
    """ Making the server output 'quiet' """
    logging.getLogger().debug("-------Service Request---------")
    logging.getLogger().debug(args)
    logging.getLogger().debug(kwargs)
    logging.getLogger().debug("----------------")
    pass


class JSONRPCServer(Singleton):
    """Configuring JSON RPC Server. Only one instance is defined using Singleton pattern."""
    
    def __initialize__(self, context_root='/', server_port=8080):
        logging.getLogger().debug('initializing JSON RPC Server : path=%s port=%s' % (context_root, server_port))
        SimpleJSONRPCRequestHandler.log_request = log_request
        SimpleJSONRPCRequestHandler.rpc_paths = (context_root)
        self.server = SimpleJSONRPCServer(('', server_port))
        
    def registerService(self, serviceName, function):
        self.server.register_function(function, name=serviceName)
        
    def start(self):
        self.server_proc = Thread(target=self.server.serve_forever)
        self.server_proc.daemon = True
        self.server_proc.start()
        self.started = True
    
    def stop(self):
        try:
            if self.started:
                self.server.shutdown()
            self.server.server_close()
        except:
            pass
    
