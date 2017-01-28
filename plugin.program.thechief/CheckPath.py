
#

import xbmc
import xbmcgui
import xbmcaddon
import os

ADDON        =  xbmcaddon.Addon(id='plugin.program.thechief')
zip          =  ADDON.getSetting('zip')
d            =  xbmcgui.Dialog()

def CheckPath():
    path = xbmc.translatePath(os.path.join(zip,'testCBFolder'))
    print path
    try:
        os.makedirs(path)
        os.removedirs(path)
        d.ok('[COLOR=white]SUCCESS[/COLOR]', 'Great news, the path you chose is writeable.', 'Some of these builds are rather big, we recommend', 'a minimum of 1GB storage space.')
    except:
        d.ok('[COLOR=white]CANNOT WRITE TO PATH[/COLOR]', 'Kodi cannot write to the path you\'ve chosen. Please click OK', 'in the settings menu to save the path then try again.', 'Some devices give false results, we recommend using a USB stick as the backup path.')

if __name__ == '__main__':
    CheckPath()