'''
Created on Oct 5, 2013

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

from xoze.utils import system
import os

def resolve_file_path(baseDirPath, extraDirPath=None, filename=None, makeDirs=False):
    _filepath = system.get_translated_path(baseDirPath)
    if extraDirPath != None:
        _filepath = os.path.join(_filepath, extraDirPath)
    if makeDirs and not os.path.exists(_filepath):
        os.makedirs(_filepath, mode=0777)
    if filename != None:
        _filepath = os.path.join(_filepath, filename)
    return _filepath

def delete_file(filepath):
    _filepath = resolve_file_path(filepath)
    if os.path.exists(_filepath):
        os.remove(_filepath)

def does_file_exist(filepath):
    _filepath = resolve_file_path(filepath)
    return os.path.exists(_filepath)

def get_last_modified_time(filepath):
    _filepath = resolve_file_path(filepath)
    if os.path.exists(_filepath):
        return os.path.getmtime(filepath)
    else:
        return None
