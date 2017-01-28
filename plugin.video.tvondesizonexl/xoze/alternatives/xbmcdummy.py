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
import logging

LOGDEBUG = logging.DEBUG
LOGINFO = logging.INFO
LOGWARNING = logging.WARNING
LOGERROR = logging.ERROR
LOGSEVERE = logging.CRITICAL

abortRequested = True

def translatePath(filepath):
    return filepath

def log(msg, level):
    print(msg)

class Addon(object):
    
    def __init__(self, id):
        print id
        
    def getAddonInfo(self, info):
        return ''
    
    def getSetting(self, key):
        return ''

class WindowXML(object):
    def __init__(self, xml):
        print xml
        
class ControlLabel(object):
    def __init__(self, x, y, width, height, font, textColor, alignment):
        print 'Label'
        
class ControlButton(object):
    def __init__(self, x, y, width, height, font, textColor, alignment):
        print 'Label'
        
class ControlFadeLabel(object):
    
    def __init__(self, x, y, width, height, font, textColor, alignment):
        print 'Fade Label'
    
def executebuiltin(msg):
    print msg