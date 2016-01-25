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
# XBMC
import logging
try:
    import xbmc  # @UnresolvedImport
except:
    from xoze.alternatives import xbmcdummy as xbmc
    
try:
    import xbmcaddon  # @UnresolvedImport
except:
    from xoze.alternatives import xbmcdummy as xbmcaddon


def get_translated_path(filepath):
    return xbmc.translatePath(filepath)


def get_addon(addon_id):
    return xbmcaddon.Addon(id=addon_id)

def show_busy_dialog():
    xbmc.executebuiltin('ActivateWindow(busydialog)')
show_busy_dialog
def hide_busy_dialog():
    xbmc.executebuiltin('Dialog.Close(busydialog)')


exit_signal = xbmc.abortRequested

def exit_addon():
    global exit_signal
    exit_signal = True

_trans_table = {
    logging.DEBUG: xbmc.LOGDEBUG,
    logging.INFO: xbmc.LOGINFO,
    logging.WARNING: xbmc.LOGWARNING,
    logging.ERROR: xbmc.LOGERROR,
    logging.CRITICAL: xbmc.LOGSEVERE,
}

class LoggingHandler(logging.Handler):
    def emit(self, record):
        if type(record.msg) is Exception:
            logging.exception(record.msg)
            import traceback
            traceback.print_exc()
        else:
            message = record.msg
            if type(message) is not str:
                message = str(message)
            xbmc_level = _trans_table[record.levelno]
            xbmc.log(message, xbmc_level)
