'''
Created on Dec 11, 2013

@author: ajdeveloped@gmail.com

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
from xoze.utils.patterns import Singleton

# Simple key-value cache
class CacheManager(Singleton):
    
    def __initialize__(self):
        self.cache_obj = {}
        
    def put(self, key, value):
        self.cache_obj[key] = value
        
    def get(self, key):
        return self.cache_obj.get(key)
        
    def has(self, key):
        return self.cache_obj.has_key(key)
    
    def remove(self, key):
        if self.has(key):
            return self.cache_obj.pop(key)
        else:
            return None

    def do_clean(self):
        del self.cache_obj
