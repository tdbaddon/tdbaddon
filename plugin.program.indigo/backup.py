import xbmc, xbmcaddon, xbmcgui, os, sys
import shutil
import urllib
import time

import zipfile

from libs import kodi
from libs import viewsetter


dp = xbmcgui.DialogProgress()
AddonTitle = kodi.addon.getAddonInfo('name')
AddonID = kodi.addon_id
addon_id = kodi.addon_id
selfAddon = xbmcaddon.Addon(id=AddonID)
backupfull = selfAddon.getSetting('backup_database')
backupaddons = selfAddon.getSetting('backup_addon_data')
PACKAGES = xbmc.translatePath(os.path.join('special://home/addons/' + 'packages'))
dialog = xbmcgui.Dialog()
ICON = xbmc.translatePath(os.path.join('special://home/addons/' + AddonID, 'icon.png'))
HOME = xbmc.translatePath('special://home/')
USERDATA = xbmc.translatePath(os.path.join('special://home/userdata', ''))
zip = kodi.get_setting("zip")
USB = xbmc.translatePath(os.path.join(zip))
EXCLUDES_FOLDER = xbmc.translatePath(os.path.join(USERDATA, 'BACKUP'))
ADDON_DATA = xbmc.translatePath(os.path.join(USERDATA, 'addon_data'))
addon_path = xbmc.translatePath(os.path.join('special://home', 'addons', ''))
NAVI = xbmc.translatePath(os.path.join(addon_path, 'script.navi-x'))
DATABASES = xbmc.translatePath(os.path.join(USERDATA, 'Database'))


def check_path():
    if zip == "Click Here":
        kodi.openSettings(addon_id, id1=0, id2=0)
        sys.exit(0)
    if HOME in USB:
        dialog = xbmcgui.Dialog()
        dialog.ok(AddonTitle, 'Invalid backup path. The selected path will may be removed during backup and cause an error. Please pick another path that is not in the Kodi directory')
        kodi.openSettings(addon_id, id1=0, id2=0)
        sys.exit(0)
    # if not os.path.exists(USB):
    # 	os.makedirs(USB)


def _get_keyboard(default="", heading="", hidden=False):
    """ shows a keyboard and returns a value """
    keyboard = xbmc.Keyboard(default, heading, hidden)
    keyboard.doModal()
    if keyboard.isConfirmed():
        return unicode(keyboard.getText(), "utf-8")
    return default


def Backup():
    guisuccess = 1
    check_path()
    if os.path.exists(PACKAGES):
        shutil.rmtree(PACKAGES)
    vq = _get_keyboard(heading="Enter a name for this backup")
    if not vq: return False, 0
    title = urllib.quote_plus(vq)
    backup_zip = xbmc.translatePath(os.path.join(USB, title + '.zip'))
    exclude_dirs = ['backupdir', 'cache', 'Thumbnails', 'temp', 'Databases']
    exclude_files = ["spmc.log", "spmc.old.log", "xbmc.log", "xbmc.old.log", "kodi.log", "kodi.old.log",
                     "Textures13.db", "fretelly.log", "freetelly.old.log"]
    message_header = "Indigo is creating the backup..."
    message_header2 = "Indigo is creating the backup..."
    message1 = "Archiving..."
    message2 = ""
    message3 = ""
    FIX_SPECIAL(USERDATA)
    ARCHIVE_CB(HOME, backup_zip, message_header2, message1, message2, message3, exclude_dirs, exclude_files)
    time.sleep(1)
    dialog.ok("[COLOR gold][B]SUCCESS![/B][/COLOR]", 'Your backup was completed successfully!.', "Backup Location: ",
              '[COLOR=yellow]' + backup_zip + '[/COLOR]')


def FullBackup():
    guisuccess = 1
    check_path()
    # if not os.path.exists(USB):
    #     os.makedirs(USB)
    vq = _get_keyboard(heading="Enter a name for this backup")
    if not vq: return False, 0
    title = urllib.quote_plus(vq)
    backup_zip = xbmc.translatePath(os.path.join(USB, title + '.zip'))
    exclude_dirs = ['backupdir', 'cache', 'temp']
    exclude_files = ["spmc.log", "spmc.old.log", "xbmc.log", "xbmc.old.log", "kodi.log", "kodi.old.log", "fretelly.log",
                     "freetelly.old.log"]
    message_header = "Indigo Is Creating A  Full  Backup..."
    message_header2 = "Indigo Is Creating A  Full  Backup..."
    message1 = "Archiving..."
    message2 = ""
    message3 = ""
    FIX_SPECIAL(USERDATA)
    ARCHIVE_CB(HOME, backup_zip, message_header2, message1, message2, message3, exclude_dirs, exclude_files)
    time.sleep(1)
    dialog.ok("[COLOR gold][B]SUCCESS![/B][/COLOR]", 'Your backup was completed successfully!.', "Backup Location: ",
              '[COLOR=yellow]' + backup_zip + '[/COLOR]')


def ADDON_DATA_BACKUP():
    guisuccess = 1
    if not os.path.exists(USB):
        os.makedirs(USB)
    vq = _get_keyboard(heading="Enter a name for this backup")
    if not vq:
        return False, 0
    title = urllib.quote_plus(vq)
    backup_zip = xbmc.translatePath(os.path.join(USB, title + '_addon_data.zip'))
    exclude_dirs = ['']
    exclude_files = [""]
    message_header = "Indigo Is Creating Addon Data Backup..."
    message_header2 = "Indigo Is Creating Addon Data Backup..."
    message1 = "Archiving..."
    message2 = ""
    message3 = ""
    FIX_SPECIAL(ADDON_DATA)
    ARCHIVE_CB(ADDON_DATA, backup_zip, message_header2, message1, message2, message3, exclude_dirs, exclude_files)
    time.sleep(1)
    dialog.ok("[COLOR gold][B]SUCCESS![/B][/COLOR]", 'Your backup was completed successfully!.', "Backup Location: ",
              '[COLOR=yellow]' + backup_zip + '[/COLOR]')


def ARCHIVE_CB(sourcefile, destfile, message_header, message1, message2, message3, exclude_dirs, exclude_files):
    zipobj = zipfile.ZipFile(destfile, 'w', zipfile.ZIP_DEFLATED)
    rootlen = len(sourcefile)
    for_progress = []
    ITEM = []
    dp.create(message_header, message1, message2, message3)
    for base, dirs, files in os.walk(sourcefile):
        for file in files:
            ITEM.append(file)
    N_ITEM = len(ITEM)
    for base, dirs, files in os.walk(sourcefile):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        files[:] = [f for f in files if f not in exclude_files]
        for file in files:
            try:
                for_progress.append(file)
                progress = len(for_progress) / float(N_ITEM) * 100
                dp.update(int(progress), "Archiving..", '[COLOR blue]%s[/COLOR]' % file, '')
                fn = os.path.join(base, file)
                zipobj.write(fn, fn[rootlen:])
            except:
                pass
    zipobj.close()
    dp.close()


def FIX_SPECIAL(url):
    HOME = xbmc.translatePath('special://')
    dialog = xbmcgui.Dialog()
    dp.create(AddonTitle, "Renaming paths...", '', '')
    url = HOME
    for root, dirs, files in os.walk(url):
        for file in files:
            if file.endswith(".xml"):
                dp.update(0, "Fixing", "[COLOR dodgerblue]" + file + "[/COLOR]", "Please wait.....")
                a = open((os.path.join(root, file))).read()
                b = a.replace(HOME, 'special://home')
                f = open((os.path.join(root, file)), mode='w')
                f.write(str(b))
                f.close()


def Restore():
    # (os.listdir(USB))
    for file in os.listdir(USB):
        if file.endswith(".zip"):
            url = xbmc.translatePath(os.path.join(USB, file))
            kodi.addItem(file, url, 'read_zip', '', '', '')


def READ_ZIP(url):
    if not "_addon_data" in url:
        if not "tv_guide" in url:
            if dialog.yesno(AddonTitle, "[COLOR smokewhite]" + url + "[/COLOR]", "Do you want to restore this backup?"):
                # skinswap()
                WIPE_BACKUPRESTORE()
                _out = xbmc.translatePath(os.path.join('special://', 'home'))
            else:
                sys.exit(1)
        else:
            if dialog.yesno(AddonTitle, "[COLOR smokewhite]" + url + "[/COLOR]", "Do you want to restore this backup?"):
                _out = GUIDE
            else:
                sys.exit(1)
    else:
        if dialog.yesno(AddonTitle, "[COLOR smokewhite]" + url + "[/COLOR]", "Do you want to restore this backup?"):
            _out = ADDON_DATA
        else:
            sys.exit(1)

    _in = url
    dp.create(AddonTitle, "Restoring File:", _in, '')
    unzip(_in, _out, dp)

    if not "addon_data" in url:
        if not "tv_guide" in url:
            # dialog.ok(AddonTitle,'Restore Successful, please restart XBMC/Kodi for changes to take effect.','','')
            dialog.ok(AddonTitle, "Installation Complete.", "", "Click OK to exit Kodi and then restart to complete .")
            xbmc.executebuiltin('ShutDown')
        else:
            dialog.ok(AddonTitle, 'Your TDB TV Guide settings have been restored.', '', '')
    else:
        dialog.ok(AddonTitle, 'Your Addon Data settings have been restored.', '', '')


def unzip(_in, _out, dp):
    zin = zipfile.ZipFile(_in, 'r')
    nFiles = float(len(zin.infolist()))
    count = 0

    try:
        for item in zin.infolist():
            count += 1
            update = count / nFiles * 100
            dp.update(int(update), '', '', '[COLOR dodgerblue][B]' + str(item.filename) + '[/B][/COLOR]')
            try:
                zin.extract(item, _out)
            except Exception, e:
                print str(e)


    except Exception, e:
        print str(e)
        return False

    return True


def ListBackDel():
    addonfolder = xbmc.translatePath(os.path.join('special://', 'home'))
    for file in os.listdir(USB):
        if file.endswith(".zip"):
            url = xbmc.translatePath(os.path.join(USB, file))
            kodi.addDir(file, url, 'do_del_backup', '')


def DeleteBackup(url):
    if dialog.yesno(AddonTitle, "[COLOR smokewhite]" + url + "[/COLOR]", "Do you want to delete this backup?"):
        os.remove(url)
        dialog.ok(AddonTitle, "[COLOR smokewhite]" + url + "[/COLOR]", "Successfully deleted.")


def DeleteAllBackups():
    if dialog.yesno(AddonTitle, "Do you want to delete all backups?"):
        shutil.rmtree(USB)
        os.makedirs(USB)
        dialog.ok(AddonTitle, "All backups successfully deleted.")


##############################    END    #########################################


# elif mode==101:
# 		backuprestore.DeleteBackup(url)




def WIPE_BACKUPRESTORE():
    dp.create(AddonTitle, "Restoring Kodi.", 'In Progress.............', 'Please Wait')
    try:
        for root, dirs, files in os.walk(HOME, topdown=True):
            dirs[:] = [d for d in dirs if d not in EXCLUDES]
            for name in files:
                try:
                    os.remove(os.path.join(root, name))
                    os.rmdir(os.path.join(root, name))
                except:
                    pass
            else:
                continue

            for name in dirs:
                try:
                    os.rmdir(os.path.join(root, name)); os.rmdir(root)
                except:
                    pass
    except:
        pass

    dp.create(AddonTitle, "Cleaning Install", 'Removing old folders.', 'Please Wait')
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()

    if os.path.exists(NAVI):
        try:
            shutil.rmtree(NAVI)
        except:
            pass

    if os.path.exists(DATABASES):
        try:
            for root, dirs, files in os.walk(DATABASES, topdown=True):
                dirs[:] = [d for d in dirs]
                for name in files:
                    try:
                        os.remove(os.path.join(root, name))
                        os.rmdir(os.path.join(root, name))
                    except:
                        pass

                for name in dirs:
                    try:
                        os.rmdir(os.path.join(root, name)); os.rmdir(root)
                    except:
                        pass
        except:
            pass

    if os.path.exists(ADDON_DATA):
        try:
            for root, dirs, files in os.walk(ADDON_DATA, topdown=True):
                dirs[:] = [d for d in dirs]
                for name in files:
                    try:
                        os.remove(os.path.join(root, name))
                        os.rmdir(os.path.join(root, name))
                    except:
                        pass

                for name in dirs:
                    try:
                        os.rmdir(os.path.join(root, name)); os.rmdir(root)
                    except:
                        pass
        except:
            pass


def REMOVE_EMPTY_FOLDERS():
    # initialize the counters
    empty_count = 0
    used_count = 0
    try:
        for curdir, subdirs, files in os.walk(HOME):
            if len(subdirs) == 0 and len(files) == 0:  # check for empty directories. len(files) == 0 may be overkill
                empty_count += 1  # increment empty_count
                os.rmdir(curdir)  # delete the directory
                # kodi.log("Successfully Removed: "+curdir)
            elif len(subdirs) > 0 and len(files) > 0:  # check for used directories
                used_count += 1  # increment
    except:
        pass


def BACKUPMENU():
    kodi.addItem('[COLOR white]Select Backup Location[/COLOR]', 'url', 'display_backup_settings', '',
                 description="Choose the location to which you wish to store your backups!")
    kodi.addItem('[COLOR white]Full Backup (All Files and Folders Included)[/COLOR]', 'url', 'full_backup', '',
                 description="Backup everything possible!")
    kodi.addItem('[COLOR white]Backup No Database (No Database Files Included)[/COLOR]', 'url', 'small_backup', '',
                 description="Backup your Kodi configuration without unnecessary database files!")
    kodi.addDir('[COLOR white]Restore Backup[/COLOR]', '', 'do_backup_restore', '',
                description="Restore your Kodi configuration from a backup!")
    kodi.addDir('[COLOR white]Delete Backup[/COLOR]', '', 'del_backup', '',
                description="Erase any backups you have saved!")

    viewsetter.set_view("sets")
