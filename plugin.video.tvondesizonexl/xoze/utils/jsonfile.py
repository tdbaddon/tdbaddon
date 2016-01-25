'''
Created on Oct 11, 2013

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
from file import resolve_file_path
import os
try:
    import json
except ImportError:
    import simplejson as json



def read_file(filepath):
    _filepath = resolve_file_path(filepath)
    if os.path.exists(_filepath):
        fc = open(_filepath, 'r')
        obj = json.load(fc, encoding='utf-8')
        fc.close()
        return obj
    else:
        return None


def write_file(filepath, obj):
    _filepath = resolve_file_path(filepath)
    fc = open(_filepath, 'w')
    status = json.dump(obj, fc, encoding='utf-8')
    fc.close()
    return status
