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

import datetime
import os
import sys
import shutil
import xbmc
import xbmcaddon
import xbmcgui

import filetools

#----------------------------------------------------------------
# TUTORIAL #
def Addon_Genre(genre='adult',custom_url=''):
    """
[COLOR=gold]PREMIUM FEATURE FOR ADDONS EXCLUSIVELY SUPPORTED AT NOOBSANDNERDS[/COLOR]
If you'd like to hook into this please take a look at the README.

Please Note: Although this hooks into the NaN framework to pull genres you can use this without
having to hook into their framework if you have a custom url which returns results in the same format.
Your url must return a dictionary of items in this format: {"addon_name":"addon_id","addon_name_2":"addon_id_2"}

Return a dictionary of add-ons which match a specific genre.

CODE: Addon_Genre([genre, custom_url])

AVAILABLE PARAMS:
    
    genre  -  By default this is set to 'adult' which will return
    a dictionary of all known adult add-ons. For a full list of all
    the available genres you can filter by take a look at the Add-on Portal
    link below. If you click on each of the genre links then look at the
    url you'll be able to see the name to use. For example if you click on
    "Dev Tools" you'll see the url shows as 'devtools' and that's what you'd
    send through to this function if you only wanted those to show.
    http://noobsandnerds.com/addons/category/genres/

    custom_url  -  If you have your own custom url which returns genres
    you can enter it here and use that rather than rely on NaN categorisation.

EXAMPLE CODE:
space_addons = koding.Addon_Genre(genre='space')
if space_addons:
    my_return = 'LIST OF AVAILABLE SPACE BASED ADD-ONS:\n\n'

# Convert the dictionary into a list:
    space_addons = space_addons.items()
    for item in space_addons:
        my_return += '[COLOR=gold]Name:[/COLOR] %s   |   [COLOR=dodgerblue]ID:[/COLOR] %s\n' % (item[0],item[1])
    koding.Text_Box('SPACE ADD-ONS',my_return)
~"""
    import binascii
    from __init__       import Main
    from filetools      import Text_File
    from systemtools    import Timestamp
    from web            import Open_URL
    
    dialog      = xbmcgui.Dialog()
    local_path  = binascii.hexlify(genre)
    cookie_path = xbmc.translatePath("special://profile/addon_data/script.module.python.koding.aio/cookies/")
    final_path  = os.path.join(cookie_path,local_path)
    if not os.path.exists(cookie_path):
        os.makedirs(cookie_path)

    if os.path.exists(final_path):
        modified = os.path.getmtime(final_path)
        old = int(modified)
        now = int(Timestamp('epoch'))
# Add a 24hr wait so we don't kill server
        if now > (modified+86400):
            if custom_url == '':
                Main('addon_list|g:%s'%genre)
            else:
                addon_list = Open_URL(custom_url)
                try:
                    addon_list = eval(addon_list)
                    Text_File(final_path,"w",binascii.hexlify(str(addon_list)) )
                except:
                    pass

# Create new file if it doesn't exist
    else:
        if custom_url == '':
            Main('addon_list|g:%s'%genre)
        else:
            addon_list = Open_URL(custom_url)
            try:
                addon_list = eval(addon_list)
                Text_File(final_path,"w",binascii.hexlify(str(addon_list)) )
            except:
                pass

    if os.path.exists(final_path):
        try:
            addon_list = eval(binascii.unhexlify(Text_File(final_path, 'r')))
            return addon_list
        except:
            return False
    else:
        return False
#----------------------------------------------------------------
# TUTORIAL #
def Addon_Info(id='',addon_id=''):
    """
Retrieve details about an add-on, lots of built-in values are available
such as path, version, name etc.

CODE: Addon_Setting(id, [addon_id])

AVAILABLE PARAMS:
            
    (*) id  -  This is the name of the id you want to retrieve.
    The list of built in id's you can use (current as of 15th April 2017)
    are: author, changelog, description, disclaimer, fanart, icon, id, name,
    path, profile, stars, summary, type, version

    addon_id  -  By default this will use your current add-on id but you
    can access any add-on you want by entering an id in here.
    
EXAMPLE CODE:
dialog.ok('ADD-ON INFO','We will now try and pull name and version details for our current running add-on.')
version = koding.Addon_Info(id='version')
name = koding.Addon_Info(id='name')
dialog.ok('NAME AND VERSION','[COLOR=dodgerblue]Add-on Name:[/COLOR] %s' % name,'[COLOR=dodgerblue]Version:[/COLOR] %s' % version)
~"""
    import xbmcaddon
    if addon_id == '':
        addon_id = Caller()
    ADDON = xbmcaddon.Addon(id=addon_id)
    if id == '':
        dialog.ok('ENTER A VALID ID','You\'ve called the Addon_Info function but forgot to add an ID. Please correct your code and enter a valid id to pull info on (e.g. "version")')
    else:
        return ADDON.getAddonInfo(id=id)
#----------------------------------------------------------------
# TUTORIAL #
def Addon_Install(addon_id,confirm=True,silent=0,repo_install=1):
    """
[COLOR=gold]PREMIUM FEATURE FOR ADDONS EXCLUSIVELY SUPPORTED AT NOOBSANDNERDS[/COLOR]
If you'd like to hook into this please take a look at the README.

Install an add-on and all dependencies matching the version of Kodi
you're currently running. If the add-on install takes a while to kick
in (spinning wheel) it just means that particular add-on hasn't yet
been cached in the db, the next time someone hits that add-on it will be instant.

CODE: Addon_Install(addon_id, [confirm, silent, repo_install])

AVAILABLE PARAMS:
    
    addon_id  -  This is the add-on id you want to install.
    The Add-on Portal will be scanned for an add-on and all the
    dependencies will also be scanned. A list of possible download
    locations are then populated server side and the best ones which
    match your needs are installed (matching dependencies with your
    current running version of Kodi to make sure bad modules aren't
    installed).

    confirm  -  By default this is set to True which means the user
    will get a choice of whether to install the add-on or not. Set to
    false if you want to force this add-on without any dialogs.

    silent  -  By default this is set to False which means there will
    always be a dialog appear showing the install process. Set this to
    True if you'd prefer to silently auto install the content.
        
    repo_install  -  This will allow you to automatically install the
    relevant repo, offer to install the repo or do not install the repo.
    See the available values below.
    
    The team at NaN take great care to try and make sure the relevant
    add-ons are matched against the official developers repo and the
    daily script which scans repositories also does a lot of clever
    assignment processes. However due to the sheer amount of
    "developers" re-uploading others content there's always a chance
    an add-on may get marked up against the wrong repo. If you notice
    an add-on is marked against the wrong repo please consider updating
    the details via the Add-on Portal (EDIT ADDON button) or notifying
    a member of the team at the nooobsandnerds forum and they can
    manually get it rectified. Thank you.

    AVAILABLE VALUES:

        0 - This will not install the repo the add-on was found on.

        1 - This will automatically install the repo the add-on is found on.
        If you don't send through a value this will be used as the default.
        
        2 - This will ask user if they want to install the repo the add-on was found on.

EXAMPLE CODE:
dialog.ok('INSTALL NAN TUTORIALS','We will now attempt to install NaN Tutorials add-on.')
if os.path.exists(xbmc.translatePath('special://home/addons/plugin.video.nantus')):
    dialog.ok('ALREADY INSTALLED','We cannot install NaN Tutorials as it\'s already installed!')
else:
    koding.Addon_Install(addon_id='plugin.video.nantuts',confirm=True,silent=0,repo_install=1)
~"""
    from __init__ import Main
    if silent == True:
        silent = 1
    elif silent == False:
        silent = 0

    if confirm == True:
        confirm = 2
    else:
        confirm = 0

    kodi_version = str(xbmc.getInfoLabel("System.BuildVersion")[:2])
    Main('addoninstall|id:%s~version:%s~repo:%s~silent:%s~installtype:%s' % (addon_id, kodi_version, repo_install, silent, confirm))

#----------------------------------------------------------------
# TUTORIAL #
def Addon_List(enabled=True, inc_new=False):
    """
Return a list of enabled or disabled add-ons found in the database.

CODE: Addon_List([enabled, inc_new])

AVAILABLE PARAMS:
    
    enabled  -  By default this is set to True which means you'll
    get a list of all the enabled add-ons found in addons*.db but
    if you want a list of all the disabled ones just set this to
    False.

    inc_new  -  This will also add any new add-on folders found on
    your system that aren't yet in the database (ie ones that have
    been recently been manually extracted but not scanned in). By
    default this is set to False.
        
EXAMPLE CODE:
enabled_list = Addon_List(enabled=True)
disabled_list = Addon_List(enabled=False)
my_return = ''

for item in enabled_list:
    my_return += '[COLOR=lime]ENABLED:[/COLOR] %s\n' % item
for item in disabled_list:
    my_return += '[COLOR=red]DISABLED:[/COLOR] %s\n' % item
Text_Box('ADDON STATUS',my_return)
~"""
    from database   import DB_Query
    from guitools   import Text_Box
    from filetools  import DB_Path_Check, Get_Contents
    
    enabled_list  = []
    disabled_list = []
    addons_db     = DB_Path_Check('addons')
    on_system     = DB_Query(addons_db,'SELECT addonID, enabled from installed')

# Create a list of enabled and disabled add-ons already on system
    for item in on_system:
        if item["enabled"]:
            enabled_list.append(item["addonID"])
        else:
            disabled_list.append(item["addonID"])

    if inc_new:
        ADDONS    = xbmc.translatePath('special://home/addons')
        my_addons = Get_Contents(path=ADDONS, exclude_list=['packages','temp'])
        for item in my_addons:
            addon_id = Get_Addon_ID(item)
            if not addon_id in enabled_list and not addon_id in disabled_list:
                disabled_list.append(addon_id)

    if enabled:
        return enabled_list
    else:
        return disabled_list
#----------------------------------------------------------------
# TUTORIAL #
def Addon_Setting(setting='',value='return_default',addon_id=''):
    """
Change or retrieve an add-on setting.

CODE: Addon_Setting(setting, [value, addon_id])

AVAILABLE PARAMS:
            
    (*) setting  -  This is the name of the setting you want to access, by
    default this function will return the value but if you add the
    value param shown below it will CHANGE the setting.

    value  -  If set this will change the setting above to whatever value
    is in here.

    addon_id  -  By default this will use your current add-on id but you
    can access any add-on you want by entering an id in here.
    
EXAMPLE CODE:
dialog.ok('ADDON SETTING','We will now try and pull the language settings for the YouTube add-on')
if os.path.exists(xbmc.translatePath('special://home/addons/plugin.video.youtube')):
    my_setting = koding.Addon_Setting(setting='youtube.language',addon_id='plugin.video.youtube')
    dialog.ok('YOUTUBE SETTING','[COLOR=dodgerblue]Setting name:[/COLOR] youtube.language','[COLOR=dodgerblue]Value:[/COLOR] %s' % my_setting)
else:
    dialog.ok('YOUTUBE NOT INSTALLED','Sorry we cannot run this example as you don\'t have YouTube installed.')
~"""
    import xbmcaddon
    if addon_id == '':
        addon_id = Caller()
    ADDON = xbmcaddon.Addon(id=addon_id)
    if value == 'return_default':
        mysetting = ADDON.getSetting(setting)
        return mysetting
    else:
        ADDON.setSetting(id=setting, value=value)
#----------------------------------------------------------------
# TUTORIAL #
def Adult_Toggle(adult_list=[],disable=True):
    """
Remove/Enable a list of add-ons, these are put into a containment area until enabled again.

CODE: Adult_Toggle(adult_list, [disable])

AVAILABLE PARAMS:
            
    (*) adult_list  -  A list containing all the add-ons you want to be disabled.

    disable  -  By default this is set to true so any add-ons in the list sent
    through will be disabled. Set to False if you want to enable the hidden add-ons.
~"""
    from filetools   import Move_Tree
    from systemtools import End_Path

    adult_store = xbmc.translatePath("special://profile/addon_data/script.module.python.koding.aio/adult_store")
    if not os.path.exists(adult_store):
        os.makedirs(adult_store)
    my_addons = Installed_Addons()
    if disable:
        for item in my_addons:
            if item != None:
                item = item["addonid"]
                if item in adult_list:
                    try:
                        addon_path = xbmcaddon.Addon(id=item).getAddonInfo("path")
                    except:
                        addon_path = os.path.join(addon_dir,item)
                    Toggle_Addons(addon=item, enable=False, safe_mode=False, refresh=True)
                    path_id = End_Path(addon_path)
                    if os.path.exists(addon_path):
                        Move_Tree(addon_path,os.path.join(adult_store,path_id))
    else:
        KODI_VER    = int(float(xbmc.getInfoLabel("System.BuildVersion")[:2]))
        ADDONS      = xbmc.translatePath('special://home/addons')
        addon_vault = []
        if os.path.exists(adult_store):
            for item in os.listdir(adult_store):
                store_dir = os.path.join(adult_store,item)
                addon_dir = os.path.join(ADDONS, item)
                if os.path.isdir(store_dir):
                    Move_Tree(store_dir,addon_dir)
                    addon_vault.append(item)
        if KODI_VER >= 16:
            Toggle_Addons(addon=addon_vault, safe_mode=True, refresh=True)
        else:
            Refresh(['addons','repos'])
#----------------------------------------------------------------
# TUTORIAL #
def Caller(my_return='addon'):
    """
Return the add-on id or path of the script which originally called
your function. If it's been called through a number of add-ons/scripts
you can grab a list of paths that have been called.

CODE: Caller(my_return)

AVAILABLE PARAMS:
    
    my_return  -  By default this is set to 'addon', view the options below:
        
        'addon' : Return the add-on id of the add-on to call this function.
        
        'addons': Return a list of all add-on id's called to get to this function.
        
        'path'  : Return the full path to the script which called this funciton.
        
        'paths' : Return a list of paths which have been called to get to this
        final function.
        
EXAMPLE CODE:
my_addon = koding.Caller(my_return='addon')
my_addons = koding.Caller(my_return='addons')
my_path = koding.Caller(my_return='path')
my_paths = koding.Caller(my_return='paths')

dialog.ok('ADD-ON ID', 'Addon id you called this function from:','[COLOR=dodgerblue]%s[/COLOR]' % my_addon)
dialog.ok('SCRIPT PATH', 'Script which called this function:','[COLOR=dodgerblue]%s[/COLOR]' % my_path)

addon_list = 'Below is a list of add-on id\'s which have been called to get to this final piece of code:\n\n'
for item in my_addons:
    addon_list += item+'\n'
koding.Text_Box('ADD-ON LIST', addon_list)
koding.Sleep_If_Window_Active(10147)
path_list = 'Below is a list of scripts which have been called to get to this final piece of code:\n\n'
for item in my_paths:
    path_list += item+'\n'
koding.Text_Box('ADD-ON LIST', path_list)
~"""
    import inspect
    stack       = inspect.stack()
    last_stack  = len(stack)-1
    stack_array = []
    addon_array = []
    for item in stack:
        last_stack = item[1].replace('<string>','')
        last_stack = last_stack.strip()
        stack_array.append(last_stack)
        try:
            scrap,addon_id = last_stack.split('addons%s'%os.sep)
            addon_id = addon_id.split(os.sep)[0]
            addon_id = Get_Addon_ID(addon_id)
            if addon_id not in addon_array:
                addon_array.append(addon_id)
        except:
            pass

    if my_return == 'addons':
        return addon_array
    if my_return == 'addon':
        return addon_array[len(addon_array)-1]
    if my_return == 'path':
        return stack_array[len(stack_array)-1]
    if my_return == 'paths':
        return stack_array
#----------------------------------------------------------------
def Check_Deps(addon_path, depfiles = []):
    import re
    from filetools import Text_File
    exclude_list = ['xbmc.gui','script.module.metahandler','kodi.resource','xbmc.core','xbmc.metadata','xbmc.addon','xbmc.json','xbmc.python']
    try:
        readxml = Text_File(os.path.join(addon_path,'addon.xml'),'r')
        dmatch   = re.compile('import addon="(.+?)"').findall(readxml)
        for requires in dmatch:
            if not requires in exclude_list and not requires in depfiles:
                depfiles.append(requires)
    except:
        pass
    return depfiles
#----------------------------------------------------------------
# TUTORIAL #
def Default_Setting(setting='',addon_id='',reset=False):
    """
This will return the DEFAULT value for a setting (as set in resources/settings.xml)
and optionally reset the current value back to this default. If you pass through
the setting as blank it will return a dictionary of all default settings.

CODE:  Default_Setting(setting, [addon_id, reset])

AVAILABLE PARAMS:

    setting  -  The setting you want to retreive the value for.
    Leave blank to return a dictionary of all settings

    addon_id  -  This is optional, if not set it will use the current id.

    reset  -  By default this is set to False but if set to true and it will
    reset the current value to the default.

EXAMPLE CODE:
youtube_path = xbmc.translatePath('special://home/addons/plugin.video.youtube')
if os.path.exists(youtube_path):
    my_value = koding.Default_Setting(setting='youtube.region', addon_id='plugin.video.youtube', reset=False)
    dialog.ok('YOUTUBE SETTING','Below is a default setting for plugin.video.youtube:','Setting: [COLOR=dodgerblue]youtube.region[/COLOR]','Value: [COLOR=dodgerblue]%s[/COLOR]' % my_value)
else:
    dialog.ok('YOUTUBE NOT INSTALLED','We cannot run this example as it uses the YouTube add-on which has not been found on your system.')
~"""
    import re
    from filetools   import Text_File
    from systemtools import Data_Type

    if addon_id == '':
        addon_id = Caller()
    values = {}
    addon_path = Addon_Info(id='path',addon_id=addon_id)
    settings_path = os.path.join(addon_path,'resources','settings.xml')
    content = Text_File(settings_path,'r').splitlines()
    for line in content:
        if 'id="' in line and 'default="' in line:
            idx = re.compile('id="(.*?)"').findall(line)
            idx = idx[0] if (len(idx) > 0) else ''
            value = re.compile('default="(.*?)"').findall(line)
            value = value[0] if (len(value) > 0) else ''
            if setting != '' and idx == setting:
                values = value
                break
            elif idx != '' and value != '' and setting == '':
                values[idx] = value
    if reset:
        if Data_Type(values) == 'dict':
            for item in values.items():
                Addon_Setting(addon_id=addon_id,setting=item[0],value=item[1])
        elif setting != '':
            Addon_Setting(addon_id=addon_id,setting=setting,value=value)
    return values
#----------------------------------------------------------------
# TUTORIAL #
def Dependency_Check(addon_id = 'all', recursive = False):
    """
This will return a list of all dependencies required by an add-on.
This information is grabbed directly from the currently installed addon.xml for that id.

CODE:  Dependency_Check([addon_id, recursive])

AVAILABLE PARAMS:

    addon_id  -  This is optional, if not set it will return a list of every
    dependency required from all installed add-ons. If you only want to
    return results of one particular add-on then send through the id.

    recursive  -  By default this is set to False but if set to true and you
    also send through an individual addon_id it will return all dependencies
    required for that addon id AND the dependencies of the dependencies.

EXAMPLE CODE:
current_id = xbmcaddon.Addon().getAddonInfo('id')
dependencies = koding.Dependency_Check(addon_id=current_id, recursive=True)
clean_text = ''
for item in dependencies:
    clean_text += item+'\n'
koding.Text_Box('Modules required for %s'%current_id,clean_text)
~"""
    import xbmcaddon
    import re
    from filetools import Text_File
    ADDONS       = xbmc.translatePath('special://home/addons')
    depfiles     = []

    if addon_id == 'all':
        for name in os.listdir(ADDONS):
            if name != 'packages' and name != 'temp':
                try:
                    addon_path = os.path.join(ADDONS,name)
                    depfiles = Check_Deps(addon_path)
                except:
                    pass
    else:
        try:
            addon_path = xbmcaddon.Addon(id=addon_id).getAddonInfo('path')
        except:
            addon_path = os.path.join(ADDONS,addon_id)

        depfiles = Check_Deps(addon_path)

        if recursive:
            dep_path = None
            for item in depfiles:
                try:
                    dep_path = xbmcaddon.Addon(id=item).getAddonInfo('path')
                except:
                    dep_path = os.path.join(ADDONS,item)

            if dep_path:
                depfiles = Check_Deps(dep_path)

    return depfiles
#----------------------------------------------------------------
# TUTORIAL #
def Get_Addon_ID(folder):
    """
If you know the folder name of an add-on but want to find out the
addon id (it may not necessarily be the same as folder name) then
you can use this function. Even if the add-on isn't enabled on the
system this will regex out the add-on id.

CODE:  Get_Addon_ID(folder)

AVAILABLE PARAMS:
    
    folder  -  This is folder name of the add-on. Just the name not the path.

EXAMPLE CODE:
my_id = koding.Get_Addon_ID(folder='script.module.python.koding.aio')
dialog.ok('ADDON ID','The add-on id found is:','[COLOR=dodgerblue]%s[/COLOR]'%my_id)
~"""
    from filetools import Text_File
    import re
    ADDONS = xbmc.translatePath('special://home/addons')
    xmlpath = os.path.join(ADDONS, folder, 'addon.xml')
    if os.path.exists(xmlpath):
        contents = Text_File(xmlpath,'r')
        addon_id = re.compile('id="(.+?)"').findall(contents)
        addon_id = addon_id[0] if (len(addon_id) > 0) else ''
        return addon_id
    else:
        return folder
#----------------------------------------------------------------
# TUTORIAL #
def Installed_Addons(types='unknown', content ='unknown', properties = ''):
    """
This will send back a list of currently installed add-ons on the system.
All the three paramaters you can send through to this function are optional,
by default (without any params) this function will return a dictionary of all
installed add-ons. The dictionary will contain "addonid" and "type" e.g. 'xbmc.python.pluginsource'.

CODE: Installed_Addons([types, content, properties]):

AVAILABLE PARAMS:

    types       -  If you only want to retrieve details for specific types of add-ons
    then use this filter. Unfortunately only one type can be filtered at a time,
    it is not yet possible to filter multiple types all in one go. Please check
    the official wiki for the add-on types avaialble but here is an example if
    you only wanted to show installed repositories: koding.Installed_Addons(types='xbmc.addon.repository')

    content     -  Just as above unfortunately only one content type can be filtered
    at a time, you can filter by video,audio,image and executable. If you want to
    only return installed add-ons which appear in the video add-ons section you
    would use this: koding.Installed_Addons(content='video')

    properties  -  By default a dictionary containing "addonid" and "type" will be
    returned for all found add-ons meeting your criteria. However you can add any
    properties in here available in the add-on xml (check official Wiki for properties
    available). Unlike the above two options you can choose to add multiple properties
    to your dictionary, see example below:
    koding.Installed_Addons(properties='name,thumbnail,description')


EXAMPLE CODE:
my_video_plugins = koding.Installed_Addons(types='xbmc.python.pluginsource', content='video', properties='name')
final_string = ''
for item in my_video_plugins:
    final_string += 'ID: %s | Name: %s\n'%(item["addonid"], item["name"])
koding.Text_Box('LIST OF VIDEO PLUGINS',final_string)
~"""
    try:    import simplejson as json
    except: import json

    addon_dict = []
    if properties != '':
        properties = properties.replace(' ','')
        properties = '"%s"' % properties
        properties = properties.replace(',','","')
    
    query = '{"jsonrpc":"2.0", "method":"Addons.GetAddons","params":{"properties":[%s],"enabled":"all","type":"%s","content":"%s"}, "id":1}' % (properties,types,content)
    response = xbmc.executeJSONRPC(query)
    data = json.loads(response)
    if "result" in data:
        try:
            addon_dict = data["result"]["addons"]
        except:
            pass
    return addon_dict
#----------------------------------------------------------------
# TUTORIAL #
def Open_Settings(addon_id='',focus='',click=False,stop_script=True):
    """
By default this will open the current add-on settings but if you pass through an addon_id it will open the settings for that add-on.

CODE: Open_Settings([addon_id, focus, click, stop_script])

AVAILABLE PARAMS:

    addon_id    - This optional, it can be any any installed add-on id. If nothing is passed
    through the current add-on settings will be opened.

    focus  -  This is optional, if not set the settings will just open to the first item
    in the list (normal behaviour). However if you want to open to a specific category and
    setting then enter the number in here separated by a dot. So for example if we want to
    focus on the 2nd category and 3rd setting in the list we'd send through focus='2.3'

    click  -  If you want the focused item to automatically be clicked set this to True.

    stop_script - By default this is set to True, as soon as the addon settings are opened
    the current script will stop running. If you pass through as False then the script will
    continue running in the background - opening settings does not pause a script, Kodi just
    see's it as another window being opened.

EXAMPLE CODE:
youtube_path = xbmc.translatePath('special://home/addons/plugin.video.youtube')
if os.path.exists(youtube_path):
    dialog.ok('YOUTUBE SETTINGS','We will now open the YouTube settings.','We will focus on category 2, setting 3 AND send a click.')
    koding.Open_Settings(addon_id='plugin.video.youtube',focus='2.3',click=True,stop_script=True)
else:
    dialog.ok('YOUTUBE NOT INSTALLED','We cannot run this example as it uses the YouTube add-on which has not been found on your system.')
~"""
    import xbmcaddon
    addon_id = Caller()
    xbmc.log('ADDON ID: %s'%addon_id,2)
    xbmc.executebuiltin('Addon.OpenSettings(%s)' % addon_id)
    if focus != '':
        category, setting = focus.split('.')
        xbmc.executebuiltin('SetFocus(%d)' % (int(category) + 99))
        xbmc.executebuiltin('SetFocus(%d)' % (int(setting) + 199))
    if click:
        xbmc.sleep(500)
        xbmc.executebuiltin('Action(Select,10140)')
    if stop_script:
        try:
            sys.exit()
        except:
            pass
#----------------------------------------------------------------
# TUTORIAL #
def Toggle_Addons(addon='all', enable=True, safe_mode=True, exclude_list=[], new_only=True, refresh=True):
    """
Send through either a list of add-on ids or one single add-on id.
The add-ons sent through will then be added to the addons*.db
and enabled or disabled (depending on state sent through).

WARNING: If safe_mode is set to False this directly edits the
addons*.db rather than using JSON-RPC. Although directly amending
the db is a lot quicker there is no guarantee it won't cause
severe problems in later versions of Kodi (this was created for v17).
DO NOT set safe_mode to False unless you 100% understand the consequences!

CODE:  Toggle_Addons([addon, enable, safe_mode, exclude_list, new_only, refresh])

AVAILABLE PARAMS:

    (*) addon  -  This can be a list of addon ids, one single id or
    'all' to enable/disable all. If enabling all you can still use
    the exclude_list for any you want excluded from this function.

    enable  -  By default this is set to True, if you want to disable
    the add-on(s) then set this to False.

    safe_mode  -  By default this is set to True which means the add-ons
    are enabled/disabled via JSON-RPC which is the method recommended by
    the XBMC foundation. Setting this to False will result in a much
    quicker function BUT there is no guarantee this will work on future
    versions of Kodi and it may even cause corruption in future versions.
    Setting to False is NOT recommended and you should ONLY use this if
    you 100% understand the risks that you could break multiple setups.

    exclude_list  -  Send through a list of any add-on id's you do not
    want to be included in this command.

    new_only  -  By default this is set to True so only newly extracted
    add-on folders will be enabled/disabled. This means that any existing
    add-ons which have deliberately been disabled by the end user are
    not affected.

    refresh  - By default this is set to True, it will refresh the
    current container and also force a local update on your add-ons db.

EXAMPLE CODE:
from systemtools import Refresh
xbmc.executebuiltin('ActivateWindow(Videos, addons://sources/video/)')
xbmc.sleep(2000)
dialog.ok('DISABLE YOUTUBE','We will now disable YouTube (if installed)')
koding.Toggle_Addons(addon='plugin.video.youtube', enable=False, safe_mode=True, exclude_list=[], new_only=False)
koding.Refresh('container')
xbmc.sleep(2000)
dialog.ok('ENABLE YOUTUBE','When you click OK we will enable YouTube (if installed)')
koding.Toggle_Addons(addon='plugin.video.youtube', enable=True, safe_mode=True, exclude_list=[], new_only=False)
koding.Refresh('container')
~"""
    from __init__       import dolog
    from filetools      import DB_Path_Check, Get_Contents
    from database       import DB_Query
    from systemtools    import Data_Type, Last_Error, Refresh, Set_Setting, Timestamp

    kodi_ver        = int(float(xbmc.getInfoLabel("System.BuildVersion")[:2]))
    addons_db       = DB_Path_Check('addons')
    data_type       = Data_Type(addon)
    state           = int(bool(enable))
    enabled_list    = []
    disabled_list   = []
    if kodi_ver >= 17:
        on_system   = DB_Query(addons_db,'SELECT addonID, enabled from installed')
# Create a list of enabled and disabled add-ons already on system
        enabled_list  = Addon_List(enabled=True)
        disabled_list = Addon_List(enabled=False)

# If addon has been sent through as a string we add into a list
    if data_type == 'unicode':
        addon = addon.encode('utf8')
        data_type = Data_Type(addon)

    if data_type == 'str' and addon!= 'all':
        addon = [addon,'']

# Grab all the add-on ids from addons folder
    if addon == 'all':
        addon     = []
        ADDONS    = xbmc.translatePath('special://home/addons')
        my_addons = Get_Contents(path=ADDONS, exclude_list=['packages','temp'])
        for item in my_addons:
            addon_id = Get_Addon_ID(item)
            addon.append(addon_id)

# Find out what is and isn't enabled in the addons*.db
    temp_list = []
    for addon_id in addon:
        if not addon_id in exclude_list and addon_id != '':
            dolog('CHECKING: %s'%addon_id)
            if addon_id in disabled_list and not new_only and enable:
                temp_list.append(addon_id)
            elif addon_id not in disabled_list and addon_id not in enabled_list:
                temp_list.append(addon_id)
            elif addon_id in enabled_list and not enable:
                temp_list.append(addon_id)
            elif addon_id in disabled_list and enable:
                temp_list.append(addon_id)
    addon = temp_list

# If you want to bypass the JSON-RPC mode and directly modify the db (READ WARNING ABOVE!!!)
    if not safe_mode and kodi_ver >= 17:
        installedtime   = Timestamp('date_time')
        insert_query    = 'INSERT or IGNORE into installed (addonID , enabled, installDate) VALUES (?,?,?)'
        update_query    = 'UPDATE installed SET enabled = ? WHERE addonID = ? '
        insert_values   = [addon, state, installedtime]
        try:
            for item in addon:
                DB_Query(addons_db, insert_query, [item, state, installedtime])
                DB_Query(addons_db, update_query, [state, item])
        except:
            dolog(Last_Error())
        if refresh:
            Refresh()

# Using the safe_mode (JSON-RPC)
    else:
        final_enabled = []
        if state:
            my_value = 'true'
            log_value = 'ENABLED'
        else:
            my_value = 'false'
            log_value = 'DISABLED'

        for my_addon in addon:

# If enabling the add-on then we also check for dependencies and enable them first
            if state:
                dolog('Checking dependencies for : %s'%my_addon)
                dependencies = Dependency_Check(addon_id=my_addon, recursive=True)

# traverse through the dependencies in reverse order attempting to enable
                for item in reversed(dependencies):
                    if not item in exclude_list and not item in final_enabled and not item in enabled_list:
                        dolog('Attempting to enable: %s'%item)
                        addon_set = Set_Setting(setting_type='addon_enable', setting=item, value = 'true')

# If we've successfully enabled then we add to list so we can skip any other instances
                        if addon_set:
                            dolog('%s now %s' % (my_addon, log_value))
                            final_enabled.append(item)

# Now the dependencies are enabled we need to enable the actual main add-on
            if not my_addon in final_enabled:
                addon_set = Set_Setting(setting_type='addon_enable', setting=my_addon, value = my_value)
            if addon_set:
                dolog('%s now %s' % (my_addon, log_value))
                final_enabled.append(addon)
    if refresh:
        Refresh(['addons','container'])
#----------------------------------------------------------------