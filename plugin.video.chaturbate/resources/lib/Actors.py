# -*- coding=utf8 -*-
#******************************************************************************
# Actors.py
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
import re
import urllib2

from resources.lib.Config import Config

class Actors(object):

    # Regulärer Ausdruck um den Darsteller und das Tumbnail zu ermitteln
    _REGEX_Name_and_Image = re.compile(r'<li>\s+<a href="/(.*?)/".*?<img src="(http.*?://.*?)"')

    CATEGORY_URL = {
        "Featured":     Config.CHATURBATE_URL_FEATURED,
        "Weiblich":     Config.CHATURBATE_URL_WEIBLICH,
        "Maennlich":    Config.CHATURBATE_URL_MAENNLICH,
        "Paar":         Config.CHATURBATE_URL_PAAR,
        "Transsexual":  Config.CHATURBATE_URL_TRANSSEXUAL
        }

    def __init__(self):
        self._last_page = False

    def names_and_images(self, category, page):
        "Liefert eine Liste mit Name/Thumbnail Tuple."
        return self._REGEX_Name_and_Image.findall(self._get_streams_page(category, page))

    def reached_last_page(self):
        return self._last_page
        
    def _get_streams_page(self, category, page):
        "Liefert die Homepage in einem String."
        url = self.CATEGORY_URL[category] + "?page=%d" % int(page)
        data = urllib2.urlopen(url).readlines()
        data = " ".join(data)
        data = data.replace("\n","")
        if not "endless_page_link" in data:
            self._last_page = True
        return data

