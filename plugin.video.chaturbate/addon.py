# -*- coding=utf8 -*-
#******************************************************************************
# addon.py
#------------------------------------------------------------------------------
#
# Copyright (c) 2014 LivingOn <LivingOn@xmail.net>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#******************************************************************************
import os
import sys
import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
import urllib

from resources.lib.Config import Config
from resources.lib.ChunkPlayer import ChunkPlayer
from resources.lib.Texture13DB import Texture13DB
from resources.lib.Actors import Actors
from resources.lib.Favorits import Favorits
from resources.lib.OnlineStatus import OnlineStatus

class Chaturbate(object):
    "XBMC-AddOn zum Zugriff auf die Hauptseite von www.chaturbate.com."
     
    _plugin_id      = None
    _addon          = None
    _streams        = None
    
    def __init__(self):
        "Initialisiere AddOn."
        self._register_addon()
        self._process_request()
        
    def _register_addon(self):
        "Registriere AddOn."
        self._plugin_id = int(sys.argv[1])
        self._addon = xbmcaddon.Addon(id = Config.PLUGIN_NAME)
        self._create_settings_file()

    def _process_request(self):
        "Ermittel die Benutzeranfrage und führe sie aus."
        if sys.argv[2]:
            urlparam = sys.argv[2]
            if "?actor=" in urlparam:
                self._play_stream(urlparam)
            elif "?category=" in urlparam:
                self._create_submenue_actors(urlparam)
            elif "?submenue=Kategorien" in urlparam:
                self._create_submenue_category()
            elif "?submenue=Favoriten" in urlparam:
                self._create_submenue_favorits()
            elif "?submenue=Aufzeichnungen" in urlparam:
                self._start_filemanager()
        else:
            self._create_submenues()
 
    def _create_submenues(self):
        submenues = (
            (30110, "Kategorien"), 
            (30115, "Favoriten"), 
            (30120, "Aufzeichnungen")
        )
        items = []
        for (i18n, submenue) in submenues:
            url = sys.argv[0] + "?" + urllib.urlencode({
                'submenue' : submenue,
            })
            item = xbmcgui.ListItem(self._addon.getLocalizedString(i18n))
            items.append((url, item, True))
        xbmcplugin.addDirectoryItems(self._plugin_id, items)
        xbmcplugin.endOfDirectory(self._plugin_id)

    def _create_submenue_category(self):
        categories = (
            (30130, "Featured"), 
            (30135, "Weiblich"),
            (30140, "Maennlich"),
            (30145, "Paar"),
            (30150, "Transsexual")
        )
        items = []
        for (i18n, category) in categories:
            url = sys.argv[0] + "?" + urllib.urlencode({
                'category' : category,
                'page' : 1
            })
            item = xbmcgui.ListItem(self._addon.getLocalizedString(i18n))
            items.append((url, item, True))
        xbmcplugin.addDirectoryItems(self._plugin_id, items)
        xbmcplugin.endOfDirectory(self._plugin_id)
 
    def _create_submenue_actors(self, urlparam):
        Texture13DB.clean_database()
        category, page = urlparam.split("&")
        category = category.split("=")[1]
        page = page.split("=")[1]
        self._create_actor_list(category, page)
        
    def _create_submenue_favorits(self):
        items = []
        Texture13DB.clean_database()
        actor_list = Favorits(Config.FAVORITS_DB).actor_list()
        actor_list.sort()
        status = OnlineStatus()
        for (actor, url, image) in actor_list:
            if status.is_online(image):
                item = xbmcgui.ListItem(actor, iconImage=image)
                item.addContextMenuItems(
                    self._create_context_menu_remove(actor)
                )
                items.append((url, item, True))
        xbmcplugin.addDirectoryItems(self._plugin_id, items)
        xbmcplugin.endOfDirectory(self._plugin_id, cacheToDisc=True)
        xbmc.executebuiltin("Container.SetViewMode(500)")
        
    def _start_filemanager(self):
        folder = self._addon.getSetting("record_folder")
        xbmc.executebuiltin('ActivateWindow(Filemanager,%s)' % folder) 
 
    def _create_actor_list(self, category, page):
        "Erzeuge die Darstellerliste."
        items = []
        actors = Actors()
        for actor in actors.names_and_images(category, page):
            name, image = actor
            url = sys.argv[0] + "?" + urllib.urlencode({'actor' : name})
            image = "%s/%s.jpg" % (Config.THUMBNAILS_URL, name)
            item = xbmcgui.ListItem(name, iconImage=image)            
            item.addContextMenuItems( 
                self._create_context_menu_add(name, url, image)
            )
            items.append((url, item, True,))
        url = sys.argv[0] + "?" + urllib.urlencode({
                'category' : category,
                'page' : int(page) + 1
        })
        if not actors.reached_last_page():
            items.append((url, 
                xbmcgui.ListItem(
                    self._addon.getLocalizedString(30160), 
                    iconImage='DefaultFolder.png') , True
                )
            )            
        xbmcplugin.addDirectoryItems(self._plugin_id, items)
        xbmcplugin.endOfDirectory(self._plugin_id, cacheToDisc=True)
        xbmc.executebuiltin("Container.SetViewMode(500)")

    def _create_context_menu_add(self, name, url, image):
        command = []
        add_cmd = "XBMC.RunScript(%s, %s)" % (
            "%s/%s" % (self._get_base_dir(), Config.SCRIPT_INSERT_FAVORITE),
            "%s|%s|%s" % (name, url, image)
        )
        command.append((self._addon.getLocalizedString(30170), add_cmd,))
        return command

    def _create_context_menu_remove(self, name):
        command = []
        remove_cmd = "XBMC.RunScript(%s, %s)" % (
            "%s/%s" % (self._get_base_dir(), Config.SCRIPT_REMOVE_FAVORITE),
            name
        )
        command.append((self._addon.getLocalizedString(30175), remove_cmd,))
        return command

    def _play_stream(self, urlparam):
        "Spiele den Stream mit dem ChunkPlayer ab."
        actor = urlparam.split("=")[1]
        cp = ChunkPlayer(self._plugin_id)
        cp.play_stream(actor)

    def _create_settings_file(self):
        self._addon.setSetting("","")

    def _get_base_dir(self):
        return os.path.dirname(__file__) 
            
if __name__ == "__main__":
    Chaturbate()
                