# -*- coding: utf-8 -*-

'''
    Specto Add-on
    Copyright (C) 2016 mrknow

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import hashlib,base64
from resources.lib.lib import jsunpack

jsunpack_init = base64.urlsafe_b64decode('IzIxMzMyMTIxMigqJjI1NjIxMjMzMjFl')
pierwszatv_apiid = jsunpack.jsunpack_keys(jsunpack_init,'amVidA==')
pierwszatv_checksum = hashlib.md5(pierwszatv_apiid + jsunpack.jsunpack_keys(jsunpack_init,'jWaUq6SiopiiqA==')).hexdigest()
