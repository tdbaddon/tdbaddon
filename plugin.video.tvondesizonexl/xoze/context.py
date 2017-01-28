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
from controller import ActionController
from objects import Actions, Action, Move, Service, View, Event
from webservice import ServicePublisher
from xoze.snapvideo import Snapper, STREAM_QUAL_HD_1080, STREAM_QUAL_HD_720, \
    STREAM_QUAL_SD, STREAM_QUAL_LOW
from xoze.utils import file, system
from xoze.utils.cache import CacheManager
from xoze.utils.http import HttpClient
from xoze.utils.patterns import Singleton
import elementtree.ElementTree as ET
import logging
import time
import xbmcgui  # @UnresolvedImport

NAMESPACE = "{https://code.google.com/p/apple-tv2-xbmc/xoze/}"

class XozeContext(object):
    """Context contains information of complete XOZE xml, which defines the moves to be executed in an action, mapping between service and action."""
    
    def __init__(self, addon_context_files, addon, addon_path, addon_data_path):
        self._addon = addon
        self._addon_path = addon_path
        self._addon_data_path = addon_data_path
        
        self._xoze = Actions()
        for filepath in addon_context_files:
            self._load_actions(file.resolve_file_path(baseDirPath=addon_path, filename=filepath))
        self._initialize_mvc()
    
    
    def _load_actions(self, filepath):
        """loads content of xoze.xml in python objects. this should be STEP 1 for starting application."""
        _filepath = file.resolve_file_path(filepath)
        logging.getLogger().info('reading actions from file: <%s>, which exists: <%s>' % (_filepath, file.does_file_exist(_filepath)))
        
        actions_elem = ET.parse(open(_filepath, "r")).getroot()
        for elem in actions_elem.getchildren():
            if elem.tag == '{0}action'.format(NAMESPACE):
                self._xoze.actions.append(self._load_action(elem))
            elif elem.tag == '{0}service'.format(NAMESPACE):
                self._xoze.services.append(self._load_service(elem))
            elif elem.tag == '{0}view'.format(NAMESPACE):
                self._xoze.views.append(self._load_view(elem))
            else:
                logging.getLogger().error('found UNKNOWN tag: <%s>' % (elem))
            
            
    def _load_action(self, elem):
        logging.getLogger().debug('reading action tag: <%s>' % (elem.attrib['id']))
        action = Action(elem.attrib['id'])
        for move_elem in elem.getchildren():
            action.moves.append(self._load_move(move_elem))
        return action

    def _load_move(self, elem):
        logging.getLogger().debug('----- move from current action: <%s.%s>' % (elem.attrib['module'], elem.attrib['function']))
        move = Move(elem.attrib['module'], elem.attrib['function'])
        if(elem.attrib.has_key('view-id')):
            move.set_view_id(elem.attrib['view-id'])
        return move
    
    def _load_service(self, elem):
        logging.getLogger().debug('reading service tag: <%s> for action: <%s>' % (elem.attrib['path'], elem.attrib['action-id']))
        return Service(elem.attrib['path'], elem.attrib['action-id'], elem.attrib['module'], elem.attrib['function'])
    
    
    def _load_view(self, elem):
        logging.getLogger().debug('reading view tag: <%s>' % (elem.attrib['id']))
        view = View(elem.attrib['id'], elem.attrib['module'], elem.attrib['function'])
        for event_elem in elem.getchildren():
            view.events.append(self._load_event(event_elem))
        return view
    
    
    def _load_event(self, elem):
        logging.getLogger().debug('----- event from current view: <%s>' % (elem.attrib['intent']))
        if(elem.attrib.has_key('module') and elem.attrib.has_key('function')):
            if(elem.attrib.has_key('action-id')):
                return Event(elem.attrib['control-id'], elem.attrib['intent'], elem.attrib['action-id'], elem.attrib['module'], elem.attrib['function'])
            else:
                return Event(elem.attrib['control-id'], elem.attrib['intent'], None, elem.attrib['module'], elem.attrib['function'])
        elif(elem.attrib.has_key('action-id')):
            return Event(elem.attrib['control-id'], elem.attrib['intent'], elem.attrib['action-id'])
        else:
            # This case should never happen
            logging.getLogger().error('Loading failed: An event should have at least action-id or module function defined. Exiting now...')
            raise Exception('Loading failed', 'event is not having minimum required fields')
            
        

    def _initialize_mvc(self):
        """creates controller part MVC which is responsible to initialize and control both Model and View. this should be STEP 2 for starting application."""
        self._action_controller = ActionController(self._xoze.actions, self._xoze.views, self._addon, self._addon_path);
        
    
    def get_action_controller(self):
        return self._action_controller
        
        
    def do_clean(self):
        """This function clean all objects created by this object and will also call do_clean() functions of its child objects where ever applicable. Call to this function is internal, donot make explicit call."""
        self._action_controller.do_clean()
        del self._addon
        del self._addon_path
        del self._addon_data_path
        del self._xoze
        del self._action_controller


class AddonContext(Singleton):
    """Context contains bridge to access addon information such as version, settings, startup configurations"""
    
    def __initialize__(self, addon_id, conf={'webServiceEnabled':False}):
        system.show_busy_dialog()
        self._addon_id = addon_id
        self._addon = system.get_addon(addon_id)
        self._addon_ver = self._addon.getAddonInfo('version')
        self._addon_path = self._addon.getAddonInfo('path')
        self._addon_profile_path = self._addon.getAddonInfo('profile')
        self._configurations = conf
        self._current_addon = None
        self._current_addon_id = None
        self._service_publisher = None
        logging.getLogger().debug('context to be initialized...')
        self._xoze_context = XozeContext(self.get_conf('contextFiles'), self.get_addon(), self.get_addon_path(), self.get_addon_data_path())
        logging.getLogger().debug('snapvideo to be initialized...')
        SnapVideo(context=self)  # To initialize
        logging.getLogger().debug('web services to be initialized...')
        self._start_services()
        
        
    def _start_services(self):
        """starts JSON RPC server if service layer needs to be enabled for current app. this should be STEP 3 for starting application."""
        if self.get_conf('webServiceEnabled'):
            self._service_publisher = ServicePublisher(self, self._xoze_context._xoze.services, self._xoze_context._action_controller, self.get_conf('webServicePath'), self.get_conf('webServicePort'), self._addon_path)
            self._service_publisher.publish_services()
    
        
    def enterServiceAddonMode(self):
        while not system.exit_signal:
            time.sleep(1)
        logging.getLogger().debug('exit signal received, going to stop JSON RPC Server instance for service path: %s' % (self._context_root))
        self._service_publisher.unpublish_services()
            
        
    def set_current_addon(self, addon_id, context_files):
        if(self._current_addon_id is None):
            logging.getLogger().info('going to load addon: <%s>' % addon_id)
        elif(self._current_addon_id == addon_id):
            return
        else:
            logging.getLogger().info('going to load addon: <%s> ; unload existing addon: <%s>' % (addon_id, self._current_addon_id))
            del self._current_addon_id
            del self._current_addon
        self._current_addon_id = addon_id
        addon = system.get_addon(addon_id)
        addon_ver = addon.getAddonInfo('version')
        addon_path = addon.getAddonInfo('path')
        addon_data_path = addon.getAddonInfo('profile')
        logging.getLogger().info('set current addon: <%s>, version: <%s>, addon-path: <%s>, addon-data-path: <%s>' % (addon_id, addon_ver, addon_path, addon_data_path))
        self._current_addon = XozeContext(context_files, addon, addon_path, addon_data_path)
        
        
    def get_current_addon(self):
        if(self._current_addon is None):
            return self._xoze_context
        else:
            return self._current_addon
        
    def get_addon(self):
        return self._addon
    
    def get_addon_path(self):
        return self._addon_path

    def get_addon_data_path(self):
        return self._addon_profile_path
    
    def get_conf(self, key):
        if self._configurations.has_key(key):
            return self._configurations[key]
        else:
            return None
        
    def do_clean(self):
        logging.getLogger().debug('addon exiting, deleting objects as part of exit plan...')
        self._xoze_context.do_clean()
        if self._current_addon is not None:
            self._current_addon.do_clean()
            del self._current_addon
            del self._current_addon_id
        if self._service_publisher is not None:
            self._service_publisher.unpublish_services()
            self._service_publisher.do_clean()
            del self._service_publisher
        del self._addon
        del self._addon_id
        del self._addon_ver
        del self._addon_path
        del self._addon_profile_path
        del self._configurations
        del self._xoze_context
        http_client = HttpClient()
        http_client.do_clean()
        del http_client
        cache_manager = CacheManager()
        cache_manager.do_clean()
        del cache_manager
        snap_video = SnapVideo()
        snap_video.do_clean()
        del snap_video
        


NAMESPACE_SNAPPER = "{https://code.google.com/p/apple-tv2-xbmc/snappers/}"
class SnapVideo(Singleton):
    def __initialize__(self, context):
        snapper_filepath = file.resolve_file_path(context.get_addon_path(), extraDirPath='xoze/snapvideo', filename='snappers.xml', makeDirs=False)
        self._snappers = []
        logging.getLogger().debug('Loading snappers.xml from path... ' + snapper_filepath)
        actions_elem = ET.parse(open(snapper_filepath, "r")).getroot()
        for elem in actions_elem.getchildren():
            if elem.tag == '{0}snapper'.format(NAMESPACE_SNAPPER):
                    if elem.attrib.has_key('enabled') and elem.attrib['enabled'] == 'true':
                        self._snappers.append(Snapper(elem, context.get_addon_path()))
            else:
                logging.getLogger().error('found UNKNOWN tag: <%s>' % (elem))
    
    def findVideoHostingInfo(self, video_url):
        for snapper in self._snappers:
            if(snapper.isVideoHostedByYou(video_url)):
                return snapper.getVideoHostingInfo()
    
    def findVideoInfo(self, video_url):
        for snapper in self._snappers:
            if not snapper.isPlaylistSnapper():
                video_info = snapper.getVideoInfo(video_url)
                if video_info is not None:
                    return video_info
                
    def findPlaylistInfo(self, playlist_url):
        for snapper in self._snappers:
            if snapper.isPlaylistSnapper():
                video_info = snapper.getVideoInfo(playlist_url)
                if video_info is not None:
                    return video_info
                
    def resolveVideoStream(self, video_url):
        logging.getLogger().debug('about to resolve the link %s' % video_url)
        video_info = self.findVideoInfo(video_url)
        label = video_info.get_name()
        if label is None or label == '':
            label = video_info.get_video_host().get_name()
        image = ''
        logging.getLogger().debug('found the video stream stopped : %s' % str(video_info.get_stopped()))
        if video_info.get_stopped():
            raise Exception('Video Stopped!')
        if video_info.get_thumb_image() is not None:
            image = video_info.get_thumb_image()
        item = xbmcgui.ListItem(label=label, iconImage=image, thumbnailImage=image)
        
        qual_set = AddonContext().get_addon().getSetting('playbackqual')
        if qual_set == '':
            qual_set = '0'
        qual = int(qual_set)
        video_strm_link = video_info.get_stream_link(STREAM_QUAL_HD_1080)
        if video_strm_link is None or qual != 0:
            video_strm_link = video_info.get_stream_link(STREAM_QUAL_HD_720)
            if video_strm_link is None or qual == 2:
                video_strm_link = video_info.get_stream_link(STREAM_QUAL_SD)
                if video_strm_link is None:
                    video_strm_link = video_info.get_stream_link(STREAM_QUAL_LOW)
        item.setProperty('streamLink', video_strm_link)
        logging.getLogger().debug(video_strm_link)
        return item
    
    def do_clean(self):
        for snapper in self._snappers:
            snapper.do_clean()
        del self._snappers

