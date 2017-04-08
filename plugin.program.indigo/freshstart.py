from libs import kodi

AddonID = kodi.addon.getAddonInfo('id')
AddonTitle = kodi.addon.getAddonInfo('name')
import os, xbmc, shutil


def startup_freshstart():
    yes_pressed = kodi.yesnoDialog(AddonTitle,
                                   "Please confirm that you wish to factory restore your configuration.",
                                   "                This will result in the loss of all your current data!")
    if yes_pressed:
        addonPath = xbmc.translatePath(os.path.join('special://home'))
        enableBG16 = "UseCustomBackground,false"
        enableBG17 = "use_custom_bg,false"
        xEB('Skin.SetBool(%s)' % enableBG16)
        xEB('Skin.SetBool(%s)' % enableBG17)
        try:
            winString = xbmc.translatePath(os.path.join('special://xbmc/')).split('\\')[-2]
            winString = winString.split('_')
            winString = winString[0] + '_' + winString[-1]
            kodi.log(winString)
            winPath = addonPath.replace('\Roaming\Kodi', '\Local\Packages\%s\LocalCache\Roaming\Kodi') % winString
            if winPath: addonPath = winPath
        except:
            pass
        #  Directories and sub directories not to remove but to sort through
        dir_exclude = ('addons', 'packages', 'userdata', 'Database')
        #  Directories and sub directories Directories to ignore and leave intact
        sub_dir_exclude = ('metadata.album.universal', 'metadata.artists.universal',
                           'service.xbmc.versioncheck', 'metadata.common.musicbrainz.org',
                           'metadata.common.imdb.com')
        keep_indigo = kodi.yesnoDialog(AddonTitle,
                                       "Do you wish to keep Indigo installed for convenience after the factory restore?",
                                       " ")
        if keep_indigo:
            sub_dir_exclude = sub_dir_exclude + ('plugin.program.indigo',)
        # Files to ignore and not to be removed
        file_exclude = ('Addons26.db', 'kodi.log', 'Textures13.db', 'commoncache.db, Addons27.db')
        try:
            for (root, dirs, files) in os.walk(addonPath, topdown=True):
                dirs[:] = [dir for dir in dirs if dir not in sub_dir_exclude]
                files[:] = [file for file in files if file not in file_exclude]
                for folder in dirs:
                    try:
                        if folder not in dir_exclude: shutil.rmtree(os.path.join(root, folder))
                    except:
                        pass
                for file_name in files:
                    try:
                        os.remove(os.path.join(root, file_name))
                    except:
                        pass
            kodi.message(AddonTitle, "Done! , You are now back to a fresh Kodi configuration!",
                         "Click OK to exit Kodi and then restart to complete .")
            xbmc.executebuiltin('ShutDown')
        except Exception as e:
            kodi.log("Freshstart User files partially removed - " + str(e))
            kodi.message(AddonTitle, 'Done! , Freshstart User files partially removed',
                         'Please check the log')


def xEB(t):
    xbmc.executebuiltin(t)
