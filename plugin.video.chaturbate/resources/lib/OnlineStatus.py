# -*- coding=utf8 -*-
#******************************************************************************
# OnlineStatus.py
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
import urllib2
import hashlib

class OnlineStatus(object):
    "Prüft ob der Actor z.Zt. online ist."
    
    def __init__(self):
        self._offline_hash = None
    
    def is_online(self, imageurl):
        if not self._offline_hash:
            url_not_exists = imageurl[:-1]
            self._offline_hash = self._get_image_hash(url_not_exists)
        return self._get_image_hash(imageurl) != self._offline_hash
        
    def _get_image_hash(self, url):
        md5 = hashlib.md5()
        md5.update(urllib2.urlopen(url).read())
        return md5.hexdigest()
