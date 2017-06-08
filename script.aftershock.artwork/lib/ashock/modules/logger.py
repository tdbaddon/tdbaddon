# -*- coding: utf-8 -*-

'''
    Aftershock Add-on
    Copyright (C) 2017 Aftershockpy

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

import inspect

import control
import traceback
import xbmc

LOGDEBUG = xbmc.LOGDEBUG
LOGERROR = xbmc.LOGERROR
LOGFATAL = xbmc.LOGFATAL
LOGINFO = xbmc.LOGINFO
LOGNONE = xbmc.LOGNONE
LOGNOTICE = xbmc.LOGNOTICE
LOGSEVERE = xbmc.LOGSEVERE
LOGWARNING = xbmc.LOGWARNING

name = control.addonInfo('name')
version = control.addonInfo('version')

def debug(msg, caller=None):
    func = inspect.currentframe().f_back.f_code

    if caller is not None:
        caller = "%s.%s()" % (caller, func.co_name)
    log(msg, caller, level=LOGDEBUG)

def notice(msg, caller=None):
    func = inspect.currentframe().f_back.f_code

    if caller is not None:
        caller = "%s.%s()" % (caller, func.co_name)
    log(msg, caller, level=LOGNOTICE)

def warning(msg, caller=None):
    func = inspect.currentframe().f_back.f_code

    if caller is not None:
        caller = "%s.%s()" % (caller, func.co_name)
    log(msg, caller, level=LOGWARNING)

def error(msg, caller=None):
    if control.setting('debug') == 'true':
        func = inspect.currentframe().f_back.f_code

        if caller is not None:
            caller = "%s.%s()" % (caller, func.co_name)

            log('%s\n%s' % (msg , traceback.format_exc()), caller, level=LOGERROR)

def log(msg, caller, level=LOGDEBUG):
    # override message level to force logging when addon logging turned on
    if control.setting('debug') == 'true' and level == LOGDEBUG:
        level = LOGNOTICE

    try:
        if isinstance(msg, unicode):
            msg = '%s (ENCODED)' % (msg.encode('utf-8'))

        xbmc.log('[%s (%s)]: [%s] %s' % (name, version, caller, msg), level)
    except Exception as e:
        try: xbmc.log('Logging Failure: %s' % (e), level)
        except: pass  # just give up