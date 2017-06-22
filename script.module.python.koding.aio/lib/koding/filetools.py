# -*- coding: utf-8 -*-

# script.module.python.koding.aio
# Python Koding AIO (c) by whufclee (info@totalrevolution.tv)

# Python Koding AIO is licensed under a
# Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.

# You should have received a copy of the license along with this
# work. If not, see http://creativecommons.org/licenses/by-nc-nd/4.0.

# IMPORTANT: If you choose to use the special noobsandnerds features which hook into their server
# please make sure you give approptiate credit in your add-on description (noobsandnerds.com)
# 
# Please make sure you've read and understood the license, this code can NOT be used commercially
# and it can NOT be modified and redistributed. If you're found to be in breach of this license
# then any affected add-ons will be blacklisted and will not be able to work on the same system
# as any other add-ons which use this code. Thank you for your cooperation.

import os
import shutil
import sys
import xbmc
import xbmcgui

from systemtools import Last_Error

dp       = xbmcgui.DialogProgress()
dialog   = xbmcgui.Dialog()
HOME     = xbmc.translatePath('special://home')
PROFILE  = xbmc.translatePath('special://profile')
DATABASE = os.path.join(PROFILE,'Database')
#----------------------------------------------------------------    
# TUTORIAL #
def Archive_Tree(sourcefile, destfile, exclude_dirs=['temp'], exclude_files=['kodi.log','kodi.old.log','xbmc.log','xbmc.old.log','spmc.log','spmc.old.log'], message_header = 'ARCHIVING', message = 'Creating archive'):
    """
Archive a folder path including all sub-folders.
There is a good chance this will be depreciated and merged with the Compress function
in future. We will continue to keep this working but just a heads up the features in this
such as custom messages will more than likely get ported into the Compress function at
a later date so it may we worth using that as that has better functionality.

Optional exclude_dirs and exclude_files lists can be sent through and these will be skipped

IMPORTANT: There is a known bug where some certain compressed tar.gz files
can cause the system to hang and a bad zipfile will continue to be made until
it runs out of space on your storage device. In the unlikely event you encounter
this issue just add the file(s) to your exclude list.

CODE: Archive_Tree(sourcefile, destfile, [exclude_dirs, exclude_files, message_header, message]):

AVAILABLE PARAMS:

    (*) sourcefile   - This is the source folder of where you want to start the archive process

    (*) destfile     - This is the file path you want to save the archive as (don't forget to
    add the actual filename at end of path)

    exclude_dirs   - This is optional, if you have folder names you want to exclude just
    add them here as a list item

    exclude_files  - This is optional, if you have specific file names you want to
    exclude just add them here as a list item

    message_header - This is optional, you can give the dialog progress window a title.
    The default is "ARCHIVING"

    message        - This is optional, the default text in the dialog progress window
    will be "Creating archive" unless changed here.

EXAMPLE CODE:
HOME = xbmc.translatePath('special://home')
DST = os.path.join(HOME,'test.zip')
koding.Archive_Tree(HOME, DST)
~"""
    import zipfile
    import time
    import xbmcaddon
    xbmc.log('ARCHIVE IN PROGRESS',2)
    module_id        =  'script.module.python.koding.aio'
    this_module      =  xbmcaddon.Addon(id=module_id)
    folder_size      =  Folder_Size(sourcefile,'mb')
    available_space  =  Free_Space(HOME,'mb')
    if os.path.exists(sourcefile):
        choice = True
        if float(available_space) < float(folder_size):
            choice = dialog.yesno(this_module.getLocalizedString(30809), this_module.getLocalizedString(30810), this_module.getLocalizedString(30811) % folder_size, this_module.getLocalizedString(30812) % available_space, yeslabel = this_module.getLocalizedString(30813), nolabel = this_module.getLocalizedString(30814))
        if choice:
            zipobj       = zipfile.ZipFile(destfile , 'w', zipfile.ZIP_DEFLATED)
            rootlen      = len(sourcefile)
            for_progress = []
            contents     = []
            
            dp.create(message_header, message)

            for base, dirs, files in os.walk(sourcefile):
                for file in files:
                    contents.append(file)
            total_items =len(contents)
            xbmc.log(str(contents),2)
            
            for base, dirs, files in os.walk(sourcefile):
                dirs[:] = [d for d in dirs if d not in exclude_dirs]
                files[:] = [f for f in files if f not in exclude_files and not 'crashlog' in f and not 'stacktrace' in f]
                
                for file in files:
                    try:
                        for_progress.append(file) 
                        progress = len(for_progress) / float(total_items) * 100  
                        dp.update(0,"Backing Up",'[COLOR yellow]%s[/COLOR]'%d, 'Please Wait')
                        file_path = os.path.join(base, file)
                    except:
                        pass
                    try:
                        timestamp_1980 = 315532800
                        file_date = os.path.getmtime(file_path)                    
                        if file_date < timestamp_1980:
                            xbmc.log('OLD File date: %s'%file_date, 2)
                            os.utime(file_path,(315536400, 315536400))
                        zipobj.write(file_path, file_path[rootlen:])  
                    except:
                        xbmc.log('Failed to backup: %s'%file_path, 2)

                    if dp.iscanceled():
                        sys.exit()
            zipobj.close()
            dp.close()
    else:
        dialog.ok(this_module.getLocalizedString(30965),this_module.getLocalizedString(30815) % sourcefile)
#----------------------------------------------------------------    
# TUTORIAL #
def Compress(src,dst,compression='zip',parent=False):
    """
Compress files in either zip or tar format. This will most likely be replacing
Archive_Tree longer term as this has better functionality but it's currently
missing the custom message and exclude files options.

CODE: Compress(src,dst,[compression,parent])

AVAILABLE PARAMS:

    (*) src  -  This is the source folder you want to compress

    (*) dst  -  This is the destination file you want to create

    compression  -  By default this is set to 'zip' but you can also use 'tar'

    parent  -  By default this is set to False which means it will compress
    everything inside the path given. If set to True it will do the same but
    it will include the parent folder name - ideal if you want to zip up
    an add-on folder and be able to install via Kodi Settings.

EXAMPLE CODE:
koding_path = xbmc.translatePath('special://home/addons/script.module.python.koding.aio')
zip_dest = xbmc.translatePath('special://home/test_addon.zip')
zip_dest2 = xbmc.translatePath('special://home/test_addon2.zip')
tar_dest = xbmc.translatePath('special://home/test_addon.tar')
tar_dest2 = xbmc.translatePath('special://home/test_addon2.tar')
koding.Compress(src=koding_path,dst=zip_dest,compression='zip',parent=True)
koding.Compress(src=koding_path,dst=zip_dest2,compression='zip',parent=False)
koding.Compress(src=koding_path,dst=tar_dest,compression='tar',parent=True)
koding.Compress(src=koding_path,dst=tar_dest2,compression='tar',parent=False)
koding.Text_Box('CHECK HOME FOLDER','If you check your Kodi home folder you should now have 4 different compressed versions of the Python Koding add-on.\n\ntest_addon.zip: This has been zipped up with parent set to True\n\ntest_addon2.zip: This has been zipped up with parent set to False.\n\ntest_addon.tar: This has been compressed using tar format and parent set to True\n\ntest_addon2.tar: This has been compressed using tar format and parent set to False.\n\nFeel free to manually delete these.')
~"""
    if parent:
        import zipfile
        import tarfile
        directory = os.path.dirname(dst)
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except:
                dialog.ok('ERROR','The destination directory you gave does not exist and it wasn\'t possible to create it.')
                return
        if compression == 'zip':
            zip = zipfile.ZipFile(dst, 'w', compression=zipfile.ZIP_DEFLATED)
        elif compression == 'tar':
            zip = tarfile.open(dst, mode='w')
        root_len = len(os.path.dirname(os.path.abspath(src)))
        for root, dirs, files in os.walk(src):
            archive_root = os.path.abspath(root)[root_len:]

            for f in files:
                    fullpath = os.path.join(root, f)
                    archive_name = os.path.join(archive_root, f)
                    if compression == 'zip':
                        zip.write(fullpath, archive_name, zipfile.ZIP_DEFLATED)
                    elif compression == 'tar':
                        zip.add(fullpath, archive_name)
        zip.close()
    else:
        if compression == 'zip':
            shutil.make_archive(dst.replace('.zip',''), 'zip', src)
        elif compression == 'tar':
            shutil.make_archive(dst.replace('.tar',''), 'tar', src)
#----------------------------------------------------------------    
# TUTORIAL #
def Convert_Special(filepath=xbmc.translatePath('special://home')):
    """
Convert physcial paths stored in text files to their special:// equivalent.

CODE: Convert_Special([filepath])

AVAILABLE PARAMS:

    filepath  -  This is the path you want to scan, by default it's set to the Kodi HOME directory.

EXAMPLE CODE:
koding.Convert_Special()
~"""    
    import urllib
    for root, dirs, files in os.walk(filepath):
        for file in files:
            if file.endswith(".xml") or file.endswith(".hash") or file.endswith("properies") or file.endswith(".ini"):
                contents     = Text_File(os.path.join(root,file), 'r')
                encodedpath  = urllib.quote(HOME)
                encodedpath2 = encodedpath.replace('%3A','%3a').replace('%5C','%5c')
                newfile = contents.replace(HOME, 'special://home/').replace(encodedpath, 'special://home/').replace(encodedpath2, 'special://home/')
                Text_File(os.path.join(root, file), 'w', newfile)
#----------------------------------------------------------------    
# TUTORIAL #
def Create_Paths(path=''):
    """
Send through a path to a file, if the directories required do not exist this will create them.

CODE: Create_Paths(path)

AVAILABLE PARAMS:

    (*) path  -  This is the full path including the filename. The path
    sent through will be split up at every instance of '/'

EXAMPLE CODE:
my_path = xbmc.translatePath('special://home/test/testing/readme.txt')
koding.Create_Paths(path=my_path)
dialog.ok('PATH CREATED','Check in your Kodi home folder and you should now have sub-folders of /test/testing/.','[COLOR=gold]Press ok to remove these folders.[/COLOR]')
shutil.rmtree(xbmc.translatePath('special://home/test'))
~"""
    if path != '' and not os.path.isdir(path) and not os.path.exists(path):
        root_path = path.split(os.sep)
        if root_path[-1] == '':
            root_path.pop()
        root_path.pop()
        final_path = ''
        for item in root_path:
            final_path = os.path.join(final_path,item)
        if not os.path.exists(final_path):
            os.makedirs(final_path)
#----------------------------------------------------------------    
# TUTORIAL #
def DB_Path_Check(db_path):
    """
If you need to find out the current "real" database in use then this is the function for you.
It will scan for a specific database type (e.g. addons) and return the path to the one which was last updated.
This is particularly useful if the system has previously updated to a newer version rather than a fresh install
or if they've installed a "build" which contained old databases.

CODE: DB_Path_Check(db_path)

AVAILABLE VALUES:

    (*) db_path  -  This is the string the database starts with.
    If you want to find the path for the addons*.db you would use "addons"
    as the value, if you wanted to find the path of the MyVideos*.db you would use
    "myvideos" etc. - it is not case sensitive.

EXAMPLE CODE:
dbpath = koding.DB_Path_Check(db_path='addons')
dialog.ok('ADDONS DB','The path to the current addons database is:',dbpath)
~"""
    finalfile = 0
    databasepath = os.listdir(DATABASE)
    for item in databasepath:
        if item.lower().endswith('.db') and item.lower().startswith(db_path.lower()):
            mydb         = os.path.join(DATABASE,item)
            lastmodified = os.path.getmtime(mydb)
            if lastmodified>finalfile:
                finalfile = lastmodified
                gooddb   = mydb
    return gooddb
#---------------------------------------------------------------------------------------------------
# TUTORIAL #
def Delete_Crashlogs(extra_paths=[]):
    """
Delete all kodi crashlogs. This function will retun the amount of successfully removed crashlogs.

CODE: Delete_Crashlogs([extra_paths])

AVAILABLE PARAMS:
    extra_paths  -  By default this will search for crashlogs for xbmc,
    kodi and spmc. If you want to add compatibility for other forks of
    Kodi please send through a list of the files you want deleted. The
    format to use needs to be like example shown below.

EXAMPLE CODE:
# Lets setup some extra crashlog types for tvmc and ftmc kodi forks
log_path =  xbmc.translatePath('special://logpath/')
tvmc_path = os.path.join(log_path,'tvmc_crashlog*.*')
ftmc_path = os.path.join(log_path,'ftmc_crashlog*.*')


deleted_files = koding.Delete_Crashlogs(extra_paths=[tvmc_path, ftmc_path])
if deleted_files > 0:
    dialog.ok('CRASHLOGS DELETED','Congratulations, a total of %s crashlogs have been deleted.')
else:
    dialog.ok('NO CRASHLOGS','No crashlogs could be found on the system.')
~"""
    import glob
    log_path =  xbmc.translatePath('special://logpath/')
    xbmc_path = (os.path.join(log_path, 'xbmc_crashlog*.*'))
    kodi_path = (os.path.join(log_path, 'kodi_crashlog*.*'))
    spmc_path = (os.path.join(log_path, 'spmc_crashlog*.*'))
    paths = [xbmc_path, kodi_path, spmc_path]
    total = 0
    for items in paths:
        for file in glob.glob(items):
            try:
                 os.remove(file)
                 total+=1
            except:
                pass
    return total
#----------------------------------------------------------------
# TUTORIAL #
def Delete_Files(filepath = HOME, filetype = '*.txt', subdirectories=False):
    """
Delete all specific filetypes in a path (including sub-directories)

CODE: Delete_Files([filepath, filetype, subdirectories])

AVAILABLE PARAMS:
    
    (*) filepath  -  By default this points to the Kodi HOME folder (special://home).
    The path you send through must be a physical path and not special://

    (*) filetype  -  The type of files you want to delete, by default it's set to *.txt

    subdirectories  -  By default it will only search the folder given, if set to True
    all filetypes listed above will be deleted in the sub-directories too.

WARNING: This is an extremely powerful and dangerous tool! If you wipe your whole system
by putting in the wrong path then it's your own stupid fault!

EXAMPLE CODE:
delete_path = xbmc.translatePath('special://profile/addon_data/test')
dialog.ok('DELETE FILES','All *.txt files will be deleted from:', '', '/userdata/addon_data/test/')
koding.Delete_Files(filepath=delete_path, filetype='.txt', subdirectories=True)
~"""    
    if filepath == '/' or filepath == '.' or filepath == '' or (filepath[1]==':' and len(filepath)<4):
        dialog.ok('IDTenT ERROR!!!','You are trying to wipe your whole system!!!','Be more careful in future, not everyone puts checks like this in their code!')
        return

    if os.path.exists(filepath):
        filetype = filetype.replace('*','')

        if subdirectories:
            for parent, dirnames, filenames in os.walk(filepath):
                for fn in filenames:
                    if fn.lower().endswith(filetype):
                        os.remove(os.path.join(parent, fn))

        else:
            for delete_file in os.listdir(filepath):
                delete_path = os.path.join(filepath,delete_file)
                if delete_path.endswith(filetype):
                    try:
                        os.remove(delete_path)
                    except:
                        kodi.log(Last_Error())
    else:
        xbmc.log('### Cannot delete files as directory does not exist: %s' % filepath)
#----------------------------------------------------------------
# TUTORIAL #
def Delete_Folders(filepath='', ignore=[]):
    """
Completely delete a folder and all it's sub-folders. With the ability to add
an ignore list for any folders/files you don't want removed.

CODE: Delete_Folders(filepath, [ignore])

AVAILABLE PARAMS:
    
    (*) filepath  -  Use the physical path you want to remove (not special://)

    ignore  -  A list of paths you want to ignore. These need to be sent
    through as physical paths so just use xbmc.translatePath when creating
    your list and these can be folder paths or filepaths.

WARNING: This is an extremely powerful and dangerous tool! If you wipe important
system files from your system by putting in the wrong path then I'm afraid that's
your own stupid fault! A check has been put in place so you can't accidentally
wipe the whole root.

EXAMPLE CODE:
delete_path = xbmc.translatePath('special://profile/py_koding_test')

# Create new test directory to remove
if not os.path.exists(delete_path):
    os.makedirs(delete_path)

# Fill it with some dummy files
file1 = os.path.join(delete_path,'file1.txt')
file2 = os.path.join(delete_path,'file2.txt')
file3 = os.path.join(delete_path,'file3.txt')
koding.Dummy_File(dst=file1, size=10, size_format='kb')
koding.Dummy_File(dst=file2, size=10, size_format='kb')
koding.Dummy_File(dst=file3, size=10, size_format='kb')

dialog.ok('TEST FILE CREATED','If you look in your addon_data folder you should now see a new test folder containing 3 dummy files. The folder name is \'py_koding_test\'.')
if dialog.yesno('DELETE FOLDER','Everything except file1.txt will now be removed from:', '/userdata/py_koding_test/','Do you want to continue?'):
    koding.Delete_Folders(filepath=delete_path, ignore=[file1])
~"""
    exclude_list = ['','/','\\','C:/','storage']

# Check you're not trying to wipe root!
    if filepath in exclude_list:
        dialog.ok('FILEPATH REQUIRED','You\'ve attempted to remove files but forgot to pass through a valid filepath. Luckily this failsafe check is in place or you could have wiped your whole system!')

# If there's some ignore files we run through deleting everything but those files
    elif len(ignore) > 0:
        for root, dirs, files in os.walk(filepath, topdown=False):
            if not root in ignore:
                for file in files:
                    file_path = os.path.join(root,file)
                    if file_path not in ignore:
                        try:
                            os.remove(file_path)
                        except:
                            pass

                if len(os.listdir(root)) == 0:
                    try:
                        os.rmdir(root)
                    except:
                        pass

# If a simple complete wipe of a directory and all sub-directories is required we use this
    elif os.path.exists(filepath) and filepath != '':
        shutil.rmtree(filepath, ignore_errors=True)
        xbmc.executebuiltin('Container.Refresh')
#----------------------------------------------------------------
# TUTORIAL #
def Dummy_File(dst= xbmc.translatePath('special://home/dummy.txt'), size='10', size_format='mb'):
    """
Create a dummy file in whatever location you want and with the size you want.
Use very carefully, this is designed for testing purposes only. Accidental
useage can result in the devices storage becoming completely full in just a
few seconds. If using a cheap poor quality device (like many android units)
then you could even end up killing the device as some of them are made
with very poor components which are liable to irreversable corruption.

CODE: koding.Dummy_File(dest, [size, size_format])

AVAILABLE PARAMS:

    dst          - This is the destination folder, make sure it's a physical path and not
    "special://...". This needs to be a FULL path including the file extension. By default
    this is set to special://home/dummy.txt

    size         -  This is an optional integer, by default a file of 10 MB will be created.

    size_format  -  By default this is set to 'mb' (megabytes) but you can change this to
    'b' (bytes), 'kb' (kilobytes), 'gb' (gigabytes)

EXAMPLE CODE:
dummy = xbmc.translatePath('special://home/test_dummy.txt')
koding.Dummy_File(dst=dummy, size=100, size_format='b')
dialog.ok('DUMMY FILE CREATED','Check your Kodi home folder and you should see a 100 byte test_dummy.txt file.','[COLOR=gold]Press OK to delete this file.[/COLOR]')
os.remove(dummy)
~"""
    if size_format == 'kb':
        size = float(size*1024)
    elif size_format == 'mb':
        size = float(size*1024) * 1024
    elif size_format == 'gb':
        size = float(size*1024) * 1024 * 1024

    xbmc.log('format: %s  size: %s'%(size_format, size), 2)

    f = open(dst,"wb")
    f.seek(size-1)
    f.write("\0")
    f.close()
#----------------------------------------------------------------
# TUTORIAL #
def Extract(_in, _out, dp=None, show_error=False):
    """
This function will extract a zip or tar file and return true or false so unlike the
builtin xbmc function "Extract" this one will pause code until it's completed the action.

CODE: koding.Extract(src,dst,[dp])
dp is optional, by default it is set to false

AVAILABLE PARAMS:

    (*) src    - This is the source file, the actual zip/tar. Make sure this is a full path to
    your zip file and also make sure you're not using "special://". This extract function
    is only compatible with .zip/.tar/.tar.gz files

    (*) dst    - This is the destination folder, make sure it's a physical path and not
    "special://...". This needs to be a FULL path, if you want it to extract to the same
    location as where the zip is located you still have to enter the full path.

    dp - This is optional, if you pass through the dp function as a DialogProgress()
    then you'll get to see the status of the extraction process. If you choose not to add
    this paramater then you'll just get a busy spinning circle icon until it's completed.
    See the example below for a dp example.

    show_error - By default this is set to False, if set to True an error dialog 
    will appear showing details of the file which failed to extract.

EXAMPLE CODE:
dp = xbmcgui.DialogProgress()
dp.create('Extracting Zip','Please Wait')
if koding.Extract(_in=src,_out=dst,dp=dp,show_error=True):
    dialog.ok('YAY IT WORKED!','Successful extraction complete')
else:
    dialog.ok('BAD NEWS!','UH OH SOMETHING WENT HORRIBLY WRONG')
~"""
    import tarfile
    import xbmcaddon
    import zipfile

    module_id   = 'script.module.python.koding.aio'
    this_module = xbmcaddon.Addon(id=module_id)
    nFiles      = 0
    count       = 0

    if os.path.exists(_in):
        if zipfile.is_zipfile(_in):
            zin      = zipfile.ZipFile(_in,  'r')
            nFiles   = float(len(zin.infolist()))
            contents = zin.infolist()

        elif tarfile.is_tarfile(_in):
            zin      = tarfile.open(_in)
            contents = [tarinfo for tarinfo in zin.getmembers()]
            nFiles   = float(len(contents))
       
        if nFiles > 0:
            if dp:
                try:
                    for item in contents:
                        count += 1
                        update = count / nFiles * 100
                        dp.update(int(update))
                        zin.extract(item, _out)
                    zin.close()
                    return True

                except:
                    xbmc.log(Last_Error())
                    return False
            else:
                try:
                    zin.extractall(_out)
                    return True
                except:
                    xbmc.log(Last_Error())
                    return False
        
        else:
            xbmc.log('NOT A VALID ZIP OR TAR FILE: %s' % _in,2)
    else:
        if show_error:
            dialog.ok(this_module.getLocalizedString(30965),this_module.getLocalizedString(30815) % _in)
#----------------------------------------------------------------
# TUTORIAL #
def Fresh_Install():
    """
Attempt to completely wipe your install. Currently this only supports
LE/OE/Android. On LE/OE it will perform a hard reset and on Android it
will wipe the data for the current running app (untested)

CODE:  Fresh_Install()

EXAMPLE CODE:
if dialog.yesno('TOTAL WIPEOUT!','This will attempt give you a totally fresh install of Kodi.','Are you sure you want to continue?'):
    if dialog.yesno('[COLOR=gold]FINAL CHANCE!!![/COLOR]','If you click Yes this WILL attempt to wipe your install', '[COLOR=dodgerblue]ARE YOU 100% CERTAIN YOU WANT TO WIPE?[/COLOR]'):
        clean_state = koding.Fresh_Install()
        if not clean_state:
            dialog.ok('SYSTEM NOT SUPPORTED','Your platform is not yet supported by this function, you will have to manually wipe.')
~"""
    from systemtools import Running_App, Get_ID
    if xbmc.getCondVisibility("System.HasAddon(service.libreelec.settings)") or xbmc.getCondVisibility("System.HasAddon(service.openelec.settings)"):
        resetpath='storage/.cache/reset_oe'
        Text_File(resetpath,'w')
        xbmc.executebuiltin('reboot')
    elif xbmc.getCondVisibility('System.Platform.Android'):
        import subprocess
        running   = Running_App()
        cleanwipe = subprocess.Popen(['exec ''pm clear '+str(running)+''], executable='/system/bin/sh', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, preexec_fn=Get_ID(setid=True)).communicate()[0]
    else:
        return False
#----------------------------------------------------------------
# TUTORIAL #
def Find_In_Text(content, start, end, show_errors = False):
    """
Regex through some text and return a list of matches.
Please note this will return a LIST so even if only one item is found
you will still need to access it as a list, see example below.

CODE: koding.Find_In_Text(content, start, end, [show_errors])

AVAILABLE PARAMS:
    
    (*) content  -  This is the string to search

    (*) start    -  The start search string

    (*) end      -  The end search string

    show_errors  -  Default is False, if set to True the code will show help
    dialogs for bad code.

EXAMPLE CODE:
textsearch = 'This is some text so lets have a look and see if we can find the words "lets have a look"'
search_result = koding.Find_In_Text(textsearch, 'text so ', ' and see')
dialog.ok('SEARCH RESULT','You searched for the start string of "text so " and the end string of " and see". Your result is: %s' % search_result[0])

# Please note: we know for a fact there is only one result which is why we're only accessing list item zero.
# If we were expecting more than one return we would probably do something more useful and loop through in a for loop.
~"""
    import re
    if content == None or content == False:
        if show_errors:
            dialog.ok('ERROR WITH REGEX','No content sent through - there\'s nothing to scrape. Please check the website address is still active (details at bottom of log).')
            xbmc.log(content)
        return
    if end != '':
        links = re.findall('%s([\s\S]*?)%s' % (start, end), content)
    if len(links)>0:
        return links
    else:
        if show_errors:
            xbmc.log(content)
            dialog.ok('ERROR WITH REGEX','Please check your regex, there was content sent through to search but there are no matches for the regex supplied. The raw content has now been printed to the log')
        return None
#----------------------------------------------------------------
# TUTORIAL #
def Free_Space(dirname = HOME, filesize = 'b'):
    """
Show the amount of available free space in a path, this can be returned in a number of different formats.

CODE: Free_Space([dirname, filesize])

AVAILABLE PARAMS:

    dirname  - This optional, by default it will tell you how much space is available in your special://home
    folder. If you require information for another path (such as a different partition or storage device)
    then enter the physical path. This currently only works for local paths and not networked drives.

    filesize - By default you'll get a return of total bytes, however you can get the value as bytes,
    kilobytes, megabytes, gigabytes and terabytes..

        VALUES:
        'b'  = bytes (integer)
        'kb' = kilobytes (float to 1 decimal place)
        'mb' = kilobytes (float to 2 decimal places)
        'gb' = kilobytes (float to 3 decimal places)
        'tb' = terabytes (float to 4 decimal places)

EXAMPLE CODE:
HOME = xbmc.translatePath('special://home')
my_space = koding.Free_Space(HOME, 'gb')
dialog.ok('Free Space','Available space in HOME: %s GB' % my_space)
~"""
    import ctypes
    filesize = filesize.lower()
    if xbmc.getCondVisibility('system.platform.windows'):
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(dirname), None, None, ctypes.pointer(free_bytes))
        finalsize = free_bytes.value
    else:
        st = os.statvfs(dirname)
        finalsize =  st.f_bavail * st.f_frsize
    if filesize == 'b':
        return finalsize
    elif filesize == 'kb':
        return "%.1f" % (float(finalsize / 1024))
    elif filesize == 'mb':
        return "%.2f" % (float(finalsize / 1024) / 1024)
    elif filesize == 'gb':
        return "%.3f" % (float(finalsize / 1024) / 1024 / 1024)
    elif filesize == 'tb':
        return "%.4f" % (float(finalsize / 1024) / 1024 / 1024 / 1024)
#----------------------------------------------------------------
# TUTORIAL #
def Folder_Size(dirname = HOME, filesize = 'b'):
    """
Return the size of a folder path including sub-directories,
this can be returned in a number of different formats.

CODE: koding.Folder_Size([dirname, filesize])

AVAILABLE PARAMS:

    dirname  - This optional, by default it will tell you how much space is available in your
    special://home folder. If you require information for another path (such as a different
    partition or storage device) then enter the physical path. This currently only works for
    local paths and not networked drives.

    filesize - By default you'll get a return of total bytes, however you can get the value as
    bytes, kilobytes, megabytes, gigabytes and terabytes..

        VALUES:
        'b'  = bytes (integer)
        'kb' = kilobytes (float to 1 decimal place)
        'mb' = kilobytes (float to 2 decimal places)
        'gb' = kilobytes (float to 3 decimal places)
        'tb' = terabytes (float to 4 decimal places)

EXAMPLE CODE:
HOME = xbmc.translatePath('special://home')
home_size = Folder_Size(HOME, 'mb')
dialog.ok('Folder Size','KODI HOME: %s MB' % home_size)
~"""
    finalsize = 0
    for dirpath, dirnames, filenames in os.walk(dirname):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            finalsize += os.path.getsize(fp)
    if filesize == 'b':
        return finalsize
    elif filesize == 'kb':
        return "%.1f" % (float(finalsize / 1024))
    elif filesize == 'mb':
        return "%.2f" % (float(finalsize / 1024) / 1024)
    elif filesize == 'gb':
        return "%.3f" % (float(finalsize / 1024) / 1024 / 1024)
    elif filesize == 'tb':
        return "%.4f" % (float(finalsize / 1024) / 1024 / 1024 / 1024)
#----------------------------------------------------------------
# TUTORIAL #
def Get_Contents(path,folders=True,subfolders=False,exclude_list=[],full_path=True,filter=''):
    """
Return a list of either files or folders in a given path.

CODE:  Get_Contents(path, [folders, subfolders, exclude_list, full_path, filter])

AVAILABLE PARAMS:
    
    (*) path  -  This is the path you want to search, no sub-directories are scanned.
    
    folders  -  By default this is set to True and the returned list will only
    show folders. If set to False the returned list will show files only.

    exclude_list  -  Optionally you can add a list of items you don't want returned

    full_path  -  By default the entries in the returned list will contain the full
    path to the folder/file. If you only want the file/folder name set this to False.

    subfolders  -  By default this is set to False but if set to true it will check
    all sub-directories and not just the directory sent through.

    filter  -  If you want to only return files ending in a specific string you
    can add details here. For example to only show '.xml' files you would send
    through filter='.xml'.

EXAMPLE CODE:
ADDONS = xbmc.translatePath('special://home/addons')
addon_folders = koding.Get_Contents(path=ADDONS, folders=True, exclude_list=['packages','temp'], full_path=False)
results = ''
for item in addon_folders:
    results += 'FOLDER: [COLOR=dodgerblue]%s[/COLOR]\n'%item
koding.Text_Box('ADDON FOLDERS','Below is a list of folders found in the addons folder (excluding packages and temp):\n\n%s'%results)
~"""
    final_list = []
# Check all items in the given path
    if not subfolders:
        for item in os.listdir(path):
            item_path = os.path.join(path,item)
            if folders and os.path.isdir(item_path) and item not in exclude_list:
                if full_path:
                    final_list.append(item_path)
                else:
                    final_list.append(item)

            elif not folders and not os.path.isdir(item_path) and item not in exclude_list:
                if full_path:
                    final_list.append(item_path)
                else:
                    final_list.append(item)

# Traverse through all subfolders
    else:
        for root, dirnames, filenames in os.walk(path):
            if not folders:
                for filename in filenames:
                    file_path = os.path.join(root, filename)
                    if filter=='':
                        if full_path:
                            final_list.append(file_path)
                        else:
                            final_list.append(filename)

                    elif file_path.endswith(filter):
                        if full_path:
                            final_list.append(file_path)
                        else:
                            final_list.append(filename)
            else:
                for dirname in dirnames:
                    if full_path:
                        final_list.append(os.path.join(root, dirname))
                    else:
                        final_list.append(dirname)
    return final_list
#----------------------------------------------------------------
# TUTORIAL #
def md5_check(src,string=False):
    """
Return the md5 value of string/file/directory, this will return just one unique value.

CODE: md5_check(src,[string])

AVAILABLE PARAMS:

    (*) src  -  This is the source you want the md5 value of.
    This can be a string, path of a file or path to a folder.

    string  -  By default this is set to False but if you want to send
    through a string rather than a path set this to True.

EXAMPLE CODE:
home = xbmc.translatePath('special://home')
home_md5 = koding.md5_check(home)
dialog.ok('md5 Check', 'The md5 of your home folder is:', '[COLOR=dodgerblue]%s[/COLOR]'%home_md5)

guisettings = xbmc.translatePath('special://profile/guisettings.xml')
guisettings_md5 = koding.md5_check(guisettings)
dialog.ok('md5 Check', 'The md5 of your guisettings.xml:', '[COLOR=dodgerblue]%s[/COLOR]'%guisettings_md5)

mystring = 'This is just a random text string we\'ll get the md5 value of'
myvalue = koding.md5_check(src=mystring,string=True)
dialog.ok('md5 String Check', 'String to get md5 value of:', '[COLOR=dodgerblue]%s[/COLOR]'%mystring)
dialog.ok('md5 String Check', 'The md5 value of your string:', '[COLOR=dodgerblue]%s[/COLOR]'%myvalue)
~"""
    import hashlib
    import os

    SHAhash = hashlib.md5()
    if not os.path.exists(src) and not string:
        return -1

# If source is a file
    if string:
        return hashlib.md5(src).hexdigest()
# If source is a file
    elif not os.path.isdir(src):
        return hashlib.md5(open(src,'rb').read()).hexdigest()

# If source is a directory
    else:
        try:
            for root, dirs, files in os.walk(src):
              for names in files:
                filepath = os.path.join(root,names)
                try:
                  f1 = open(filepath, 'rb')
                except:
                  f1.close()
                  continue

            while 1:
# Read file in as little chunks
              buf = f1.read(4096)
              if not buf : break
              SHAhash.update(hashlib.md5(buf).hexdigest())
            f1.close()
        except:
            return -2

        return SHAhash.hexdigest()
#----------------------------------------------------------------
# TUTORIAL #
def Move_Tree(src, dst, dp=None):
    """
Move a directory including all sub-directories to a new location.
This will automatically create the new location if it doesn't already
exist and it wierwrite any existing entries if they exist.

CODE: koding.Move_Tree(src, dst)

AVAILABLE PARAMS:

    (*) src  -  This is source directory that you want to copy

    (*) dst  -  This is the destination location you want to copy a directory to.

    dp - This is optional, if you pass through the dp function as a DialogProgress()
    then you'll get to see the status of the move process. See the example below for a dp example.

EXAMPLE CODE:
dp = xbmcgui.DialogProgress()
source = xbmc.translatePath('special://profile/move_test')

# Lets create a 500MB dummy file so we can move and see dialog progress
dummy = os.path.join(source,'dummy')
if not os.path.exists(source):
    os.makedirs(source)
koding.Dummy_File(dst=dummy+'1.txt', size=10, size_format='mb')
koding.Dummy_File(dst=dummy+'2.txt', size=10, size_format='mb')
koding.Dummy_File(dst=dummy+'3.txt', size=10, size_format='mb')
koding.Dummy_File(dst=dummy+'4.txt', size=10, size_format='mb')
koding.Dummy_File(dst=dummy+'5.txt', size=10, size_format='mb')
koding.Dummy_File(dst=dummy+'6.txt', size=10, size_format='mb')
dialog.ok('DUMMY FILE CREATED','If you want to check in your userdata folder you should have a new folder called "move_test" which has 6x 10MB dummy files.')

# This is optional but if you want to see a dialog progress then you'll need this
dp.create('MOVING FILES','Please Wait')

destination = xbmc.translatePath('special://home/My MOVED Dummy File')
koding.Move_Tree(source, destination, dp)
dialog.ok('CHECK YOUR KODI HOME FOLDER','Please check your Kodi home folder, the dummy file should now have moved in there. When you press OK it will be removed')
shutil.rmtree(destination)
~"""
    if dp:
        totalfiles = 0
        for root, dirs, files in os.walk(src):
            totalfiles += len(files)
        count = 0

    for src_dir, dirs, files in os.walk(src):
        dst_dir = src_dir.replace(src, dst, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.move(src_file, dst_dir)
            if dp:
                try:
                    count += 1
                    update = count / totalfiles * 100
                    dp.update(int(update))
                except:
                    pass
    try:
        shutil.rmtree(src)
    except:
        pass

    if dp:
        dp.close()
#----------------------------------------------------------------
# TUTORIAL #
def Split_Lines(raw_string, size):
    """
Splits up a piece of text into a list of lines x amount of chars in length.

CODE: koding.Split_Lines(raw_string, size)

AVAILABLE PARAMS:

    (*) raw_string  -  This is the text you want split up into lines

    (*) size        -  This is the maximum size you want the line length to be (in characters)

EXAMPLE CODE:
raw_string = 'This is some test code, let\'s take a look and see what happens if we split this up into lines of 20 chars per line'
my_list = koding.Split_Lines(raw_string,20)
koding.Text_Box('List of lines',str(my_list))
~"""    
    final_list=[""]
    for i in raw_string:
        length = len(final_list)-1
        if len(final_list[length]) < size:
            final_list[length]+=i
        else:
            final_list += [i]
    return final_list
#----------------------------------------------------------------
# TUTORIAL #
def Text_File(path, mode, text = ''):
    """
Open/create a text file and read/write to it.

CODE: koding.Text_File(path, mode, [text])

AVAILABLE PARAMS:
    
    (*) path  -  This is the path to the text file

    (*) mode  -  This can be 'r' (for reading) or 'w' (for writing)

    text  -  This is only required if you're writing to a file, this
    is the text you want to enter. This will completely overwrite any
    text already in the file.

EXAMPLE CODE:
HOME = xbmc.translatePath('special://home')
koding_test = os.path.join(HOME, 'koding_test.txt')
koding.Text_File(path=koding_test, mode='w', text='Well done, you\'ve created a text file containing this text!')
dialog.ok('CREATE TEXT FILE','If you check your home Kodi folder and you should now have a new koding_test.txt file in there.','[COLOR=gold]DO NOT DELETE IT YET![/COLOR]')
mytext = koding.Text_File(path=koding_test, mode='r')
dialog.ok('TEXT FILE CONTENTS','The text in the file created is:','[COLOR=dodgerblue]%s[/COLOR]'%mytext,'[COLOR=gold]CLICK OK TO DELETE THE FILE[/COLOR]')
try:
    os.remove(koding_test)
except:
    dialog.ok('FAILED TO REMOVE','Could not remove the file, looks like you might have it open in a text editor. Please manually remove yourself')
~"""
    try:
        textfile = open(path, mode)

        if mode == 'r':
            content  = textfile.read()
            textfile.close()
            return content

        if mode == 'w':
            textfile.write(text)
            textfile.close()
            return True

    except:
        xbmc.log(Last_Error())
        return False
#----------------------------------------------------------------
