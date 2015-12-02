# -*- coding=utf8 -*-
#******************************************************************************
# Config.py
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
import xbmc

class Config(object):
    "Die wichtigsten Konfigurationsparameter zusammengefasst."
    
    PLUGIN_NAME    = "plugin.video.chaturbate"
    THUMBNAILS_URL = "http://cdn-i.highwebmedia.com/roomimage"
    CHATURBATE_URL = "http://de.chaturbate.com/"
    
    CHATURBATE_URL_FEATURED    = CHATURBATE_URL 
    CHATURBATE_URL_WEIBLICH    = CHATURBATE_URL + "female-cams/"
    CHATURBATE_URL_MAENNLICH   = CHATURBATE_URL + "male-cams/"
    CHATURBATE_URL_PAAR        = CHATURBATE_URL + "couple-cams/"
    CHATURBATE_URL_TRANSSEXUAL = CHATURBATE_URL + "transsexual-cams/"
    
    SCRIPT_INSERT_FAVORITE = "insert_actor.py"
    SCRIPT_REMOVE_FAVORITE = "remove_actor.py"
    
    FAVORITS_DB = xbmc.translatePath(
        "special://profile/addon_data/%s/Favorits.db" % PLUGIN_NAME
    )
