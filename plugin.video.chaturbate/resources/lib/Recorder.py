# -*- coding=utf8 -*-
#******************************************************************************
# Recorder.py
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
import xbmcaddon

class Recorder(object):
    
    def __init__(self, actor):
        "Initialisiert den Rekorder und liest die Settings aus."
        self._actor = actor
        self._filehandle = None
        addon = xbmcaddon.Addon() 
        self._active = True if addon.getSetting("record_active") == "true" else False
        if self._active:
            self._type = addon.getSetting("record_type")
            self._mode = addon.getSetting("record_mode")
            self._folder = addon.getSetting("record_folder").rstrip(os.sep)
            # bei einmaliger Aufnahme den Rekorder wieder deaktivieren
            if self._type == "0":
                addon.setSetting("record_active", "false")
            if not self._folder:
                self._active = False
    
    def open(self):
        "Öffnet die Ausgabedatei zum Anfügen oder Überschreiben."
        if self._active:
            mode = "wb" if self._mode == "1" else "ab"
            filename = "%s%s%s.mp4" % (self._folder, os.sep, self._actor)
            try:
                self._filehandle = open(filename, mode)
            except:
                self._active = False

    def write(self, chunk):
        "Schreibt einen Chunk in die Ausgabedatei."
        if self._active:
            self._filehandle.write(chunk)
        
    def close(self):
        "Schließt die Ausgabedatei."
        if self._active:
            self._filehandle.close()
