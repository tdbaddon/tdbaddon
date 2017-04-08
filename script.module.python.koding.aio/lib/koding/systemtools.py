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
# and it can NOT be modified and redistributed. Thank you.

import datetime
import os
import sys
import shutil
import xbmc
import xbmcgui

import filetools

try:    import simplejson as json
except: import json

try: from sqlite3 import dbapi2 as database
except: from pysqlite2 import dbapi2 as database

dialog = xbmcgui.Dialog()
#----------------------------------------------------------------
# TUTORIAL #
def Cleanup_String(my_string):
    """
Clean a string, removes whitespaces and common buggy formatting when pulling from websites

CODE: Cleanup_String(my_string)

    AVAILABLE PARAMS:
        
        (*) my_string   -  This is the main text you want cleaned up.
EXAMPLE CODE:
current_text = '" This is a string of text which should be cleaned up   /'
clean_text = koding.Cleanup_String(current_text)
xbmc.log(clean_text)
dialog.ok('CLEAN', clean_text)~"""
    import urllib
    bad_chars = ['/','\\',':',';','"',"'"]

    try:
        my_string = my_string.encode('utf8')
    except:
        pass
    
    my_string = urllib.unquote_plus(my_string)
    my_string = my_string.replace('&amp;','&')
    
    if len(my_string) > 4:
        if my_string[-4] == '.':
            my_string = my_string[:-4]
    
    my_string = my_string.strip()

    while my_string[0] in bad_chars or my_string[-1] in bad_chars:
        if my_string[-1] in bad_chars:
            my_string = my_string[:-1]
        if my_string[0] in bad_chars:
            my_string = my_string[1:]
        my_string = my_string.strip()

    return my_string
#----------------------------------------------------------------
# TUTORIAL #
def Colour_Text(text, colour1='dodgerblue',colour2='white'):
    """
Capitalize a string and make the first colour of each string blue and the rest of text white

CODE: Colour_Text(text, [color1, color2])

    AVAILABLE PARAMS:
        
        (*) text   -  This is the main text you want to change

        colour1 -  This is optional and is set as dodgerblue by default.
        This is the first letter of each word in the string

        colour2 -  This is optional and is set as white by default. 
        This is the colour of the text

IMPORTANT: I use the Queens English so please note the word "colour" has a 'u' in it!

EXAMPLE CODE:
current_text = 'This is a string of text which should be changed to dodgerblue and white with every first letter capitalised'
mytext = koding.Colour_Text(text=current_text, colour1='dodgerblue', colour2='white')
xbmc.log(current_text)
xbmc.log(mytext)
dialog.ok('CURRENT TEXT', current_text)
dialog.ok('NEW TEXT', mytext)~"""

    if text.startswith('[COLOR') and text.endswith('/COLOR]'):
        return text

    colour_clean = 0

    if ' ' in text:
        newname = ''
        text = text.split(' ')
        xbmc.log('text: %s'%text)
        for item in text:
            xbmc.log('checking: %s'%item)
            if len(item)==1 and item == '&':
                newname += ' &'
            if '[/COLOR]' in item:
                newname += ' '+item
            elif not item.startswith('[COLOR=') and not colour_clean:
                if item.startswith('(') or item.startswith('['):
                    newname += '[COLOR=yellow] '+item
                    colour_clean = 1
                else:
                    if item.isupper():
                        newname += '[COLOR=%s] %s[/COLOR]' % (colour1, item)
                    else:
                        xbmc.log('doing this bit')
                        try:
                            newname += '[COLOR=%s] %s[/COLOR][COLOR=%s]%s[/COLOR]' % (colour1, item[0].upper(), colour2, item[1:])
                        except:
                            try:
                                newname += '[COLOR=%s] %s[/COLOR][COLOR=%s][/COLOR]' % (colour1, item[0], colour2, item[1:])
                            except:
                                pass
            

            elif item.endswith(')') or item.endswith(']'):
                newname += ' '+item+'[/COLOR]'
                colour_clean = 0

            else:
                newname += ' '+item

    else:
        if text[0] == '(':
            newname = '[COLOR=%s]%s[/COLOR][COLOR=%s]%s[/COLOR][COLOR=%s]%s[/COLOR]' % (colour2, text[0], colour1, text[1].upper(), colour2, text[2:])
        else:
            newname = '[COLOR=%s]%s[/COLOR][COLOR=%s]%s[/COLOR]' % (colour1, text[0], colour2, text[1:])

    success = 0
    while success != 1:
        if newname.startswith(' '):
            newname = newname[1:]
        success = 1
    if newname.startswith('[COLOR=%s] ' % colour1):
        newname = '[COLOR=%s]%s' % (colour1, newname[19:])

    return newname
#----------------------------------------------------------------
# TUTORIAL #
def Cleanup_Textures(frequency=14,use_count=10):
    """
This will check for any cached artwork and wipe if it's not been accessed more than 10 times in the past x amount of days.

CODE: Cleanup_Textures([frequency])

    AVAILABLE PARAMS:
        
        frequency  -  This is an optional integer, be default it checks for any
        images not accessed in 14 days but you can use any amount of days here.

        use_count   -  This is an optional integer, be default it checks for any
        images not accessed more than 10 times. If you want to be more ruthless
        and remove all images not accessed in the past x amount of days then set this very high.

EXAMPLE CODE:
dialog.ok('Clean Textures','We are going to clear any old cached images not accessed at least 10 times in the past 5 days')
koding.Cleanup_Textures(5)~"""

    db   = filetools.DB_Path_Check('Textures')
    xbmc.log('### DB_PATH: %s' % db)
    conn = database.connect(db, timeout = 10, detect_types=database.PARSE_DECLTYPES, check_same_thread = False)
    conn.row_factory = database.Row
    c = conn.cursor()

    # Set paramaters to check in db, cull = the datetime (we've set it to 14 days) and useCount is the amount of times the file has been accessed
    cull     = datetime.datetime.today() - datetime.timedelta(days = frequency)

    # Create an array to store paths for images and ids for database
    ids    = []
    images = []

    c.execute("SELECT idtexture FROM sizes WHERE usecount < ? AND lastusetime < ?", (use_count, str(cull)))

    for row in c:
        ids.append(row["idtexture"])

    for id in ids:
        c.execute("SELECT cachedurl FROM texture WHERE id = ?", (id,))
        for row in c:
            images.append(row["cachedurl"])


# Clean up database
    for id in ids:       
        c.execute("DELETE FROM sizes   WHERE idtexture = ?", (id,))
        c.execute("DELETE FROM texture WHERE id        = ?", (id,))

    c.execute("VACUUM")
    conn.commit()
    c.close()

    xbmc.log("### Automatic Cache Removal: %d Old Textures removed" % len(images))

# Delete files
    thumbfolder = xbmc.translatePath('special://home/userdata/Thumbnails')
    for image in images:
        path = os.path.join(thumbfolder, image)
        try:
            os.remove(path)
        except:
            kodi.log(Last_Error())
#----------------------------------------------------------------
# TUTORIAL #
def Clear_Data(addonid):
    """
If you want to offer the option to clear the cookie data then you can add the
following code in your settings.xml. This will wipe the cookies folder - could
be useful if things like the initial run code sent back from server alters or
the base urls have changed.

<setting id="clear_data"    label="Re-check Server" type="action"   action="RunScript(special://home/addons/script.module.python.koding.aio/lib/koding/__init__.py,clear_data,your.plugin.id)"  option="close"  visible="true"/>~"""

    root_path = os.path.join(xbmc.translatePath('special://profile/addon_data'),addonid)
    
    try:
        xbmc.log('data cleared from: %s' % addonid)
        shutil.rmtree(os.path.join(root_path, 'cookies'))
        return True
    except:
        xbmc.log('failed to clear data from: %s' % addonid)
        return False
#----------------------------------------------------------------
# TUTORIAL #
def DB_Query(db_path, query, values=''):
    """
Open a database and either return an array of results with the SELECT SQL command or perform an action such as INSERT, UPDATE, CREATE.

CODE:  DB_Query(db_path, query, [values])

AVAILABLE PARAMS:

    (*) db_path -  the full path to the database file you want to access.
    (*) query   -  this is the actual db query you want to process, use question marks for values

    values  -  a list of values, even if there's only one value it must be sent through as a list item.

IMPORTANT: Directly accessing databases which are outside of your add-ons domain is very much frowned
upon. If you need to access a built-in kodi database (as shown in example below) you should always use
the JSON-RPC commands where possible. 

EXAMPLE CODE:
import filetools
dbpath = filetools.DB_Path_Check('addons')
db_query = koding.DB_Query(db_path=dbpath, query='SELECT * FROM addons WHERE addonID LIKE ? AND addonID NOT LIKE ?', values=['%youtube%','%script.module%'])
koding.Text_Box('DB SEARCH RESULTS',str(db_query))~"""

    db_dict = []
    con = database.connect(db_path)
    cur = con.cursor()
    
    if query.upper().startswith('SELECT'):
        if values == '':
            cur.execute(query)
        else:
            cur.execute(query, values)

        names = list(map(lambda x: x[0], cur.description))

        for rows in iter(cur.fetchmany, []):
            for row in rows:
                temp_dict = {}
                for idx,col in enumerate(cur.description):
                    temp_dict[col[0]] = row[idx]
                db_dict.append(temp_dict)
        return db_dict

    elif query.upper().startswith('CREATE'):
        cur.execute(query)
        con.commit()

# ANY NON SELECT QUERY (UPDATE, INSERT ETC.)
    else:
        if values == '':
            cur.executemany(query)
            con.commit()
        else:
            cur.executemany(query, values)
            con.commit()

    cur.close()
#----------------------------------------------------------------
# TUTORIAL #
def ID_Generator(size=15):
    """
This will generate a random string made up of uppercase & lowercase ASCII
characters and digits - it does not contain special characters.

CODE:  ID_Generator([size])
size is an optional paramater.

AVAILABLE PARAMS:

    size - just send through an integer, this is the length of the string you'll get returned.
    So if you want a password generated that's 20 characters long just use ID_Generator(20). The default is 15.

EXAMPLE CODE:
my_password = koding.ID_Generator(20)
dialog.ok('ID GENERATOR','Password generated:', '', '[COLOR=dodgerblue]%s[/COLOR]' % my_password)~"""

    import string
    import random

    chars=string.ascii_uppercase + string.digits + string.ascii_lowercase
    return ''.join(random.choice(chars) for _ in range(size))
#----------------------------------------------------------------
# TUTORIAL #
def Installed_Addons(types='unknown', content ='unknown', properties = ''):
    """
This will send back a list of currently installed add-ons on the system.
All the three paramaters you can send through to this function are optional,
by default (without any params) this function will return a dictionary of all
installed add-ons. The dictionary will contain "addonid" and "type" e.g. 'xbmc.python.pluginsource'.

Available filters:

types: If you only want to retrieve details for specific types of add-ons then use this filter.
Unfortunately only one type can be filtered at a time, it is not yet possible to filter multiple
types all in one go. Please check the official wiki for the add-on types avaialble but here is an
example if you only wanted to show installed repositories:
koding.Installed_Addons(types='xbmc.addon.repository')

content: Just as above unfortunately only one content type can be filtered at a time, you can filter
by video,audio,image and executable. If you want to only return installed add-ons which appear in
the video add-ons section you would use this:
koding.Installed_Addons(content='video')

properties: By default a dictionary containing "addonid" and "type" will be returned for all found
add-ons meeting your criteria. However you can add any properties in here available in the add-on xml
(check official Wiki for properties available). Unlike the above two options you can choose to add
multiple properties to your dictionary, see example below:
koding.Installed_Addons(properties='name,thumbnail,description')

Of course you can use as many of these params as you wish, they are all optional but if you wanted you could use something like this:

EXAMPLE CODE:
my_video_plugins = koding.Installed_Addons(types='xbmc.python.pluginsource', content='video', properties='name')
koding.Text_Box('LIST OF VIDEO PLUGINS',str(my_video_plugins))~"""

    addon_dict = []
    if properties != '':
        properties = properties.replace(' ','')
        properties = '"%s"' % properties
        properties = properties.replace(',','","')
    
    query = '{"jsonrpc":"2.0", "method":"Addons.GetAddons","params":{"properties":[%s],"enabled":"all","type":"%s","content":"%s"}, "id":1}' % (properties,types,content)
    response = xbmc.executeJSONRPC(query)
    data = json.loads(response)
    if "result" in data:
        addon_dict = data["result"]["addons"]
    return addon_dict
#----------------------------------------------------------------
# TUTORIAL #
def Last_Error():
    """
Return details of the last error produced, perfect for try/except statements

CODE: Last_Error()

EXAMPLE CODE:
try:
    xbmc.log(this_should_error)
except:
koding.Text_Box('ERROR MESSAGE',Last_Error())~"""

    import traceback
    error = traceback.format_exc()
    return error
#----------------------------------------------------------------
# TUTORIAL #
def Open_Settings(addon_id=sys.argv[0], stop_script = True):
    """
By default this will open the current add-on settings but if you pass through an addon_id it will open the settings for that add-on.

CODE: Open_Settings([addon_id, stop_script])

AVAILABLE PARAMS:

    addon_id    - This optional, it can be any any installed add-on id. If nothing is passed
    through the current add-on settings will be opened.

    stop_script - By default this is set to True, as soon as the addon settings are opened
    the current script will stop running. If you pass through as False then the script will
    continue running in the background - opening settings does not pause a script, Kodi just
    see's it as another window being opened.

EXAMPLE CODE:
koding.Open_Settings('plugin.video.youtube')~"""
    import xbmcaddon

    ADDON = xbmcaddon.Addon(id=addon_id)
    ADDON.openSettings(addon_id)
    if stop_script:
        try:
            sys.exit()
        except:
            pass
#----------------------------------------------------------------
# TUTORIAL #
def Show_Busy(status=True):
    """
This will show/hide a "working" symbol.

CODE: Show_Busy(True)

AVAILABLE PARAMS:

    status - This optional, by default it's True which means the "working" symbol appears. False will disable.

EXAMPLE CODE:
dialog.ok('BUSY SYMBOL','Press OK to show a busy dialog which restricts any user interaction. We have added a sleep of 5 seconds at which point it will disable.')
koding.Show_Busy()
xbmc.sleep(5000)
koding.Show_Busy(False)~"""

    if status:
        xbmc.executebuiltin("ActivateWindow(busydialog)")
    else:
        xbmc.executebuiltin("Dialog.Close(busydialog)")
#----------------------------------------------------------------
# TUTORIAL #
def Set_Setting(setting_type, setting, value = ''):
    """
Use this to set built-in kodi settings via JSON or set skin settings. The value paramater is only required for JSON and string commands. Available options are below:

CODE: koding.Set_Setting(setting, setting_type, [value])

AVAILABLE PARAMS:
    
    setting_type - The type of setting type you want to change, available types are:

        string (sets a skin string, requires a value)
        bool_true (sets a skin boolean to true, no value required)
        bool_false (sets a skin boolean to false, no value required)
        (!) kodi_setting (sets values found in guisettings.xml)
        (!) addon_enable (enables/disables an addon. setting = addon_id, value = true/false)
        (!) json (WIP - setitng = method, value = params, see documentation on JSON-RPC API here: http://kodi.wiki/view/JSON-RPC_API)

        (!) = These will return True or False if successful

setting - This is the name of the setting you want to change, it could be a setting from the kodi settings or a skin based setting.

value: This is the value you want to change the setting to.


EXAMPLE CODE:
koding.Set_Setting('kodi_setting', 'lookandfeel.enablerssfeeds', 'false')~"""

    try:

# If the setting_type is kodi_setting we run the command to set the relevant values in guisettings.xml
        if setting_type == 'kodi_setting':
            setting = '"%s"' % setting
            value = '"%s"' % value

            query = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":%s,"value":%s}, "id":1}' % (setting, value)
            response = xbmc.executeJSONRPC(query)

            if 'error' in str(response):
                query = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":%s,"value":%s}, "id":1}' % (setting, value.replace('"',''))
                response = xbmc.executeJSONRPC(query)
                if 'error' in str(response):
                    xbmc.log('### Error With Setting: %s' % response)
                    return False
                else:
                    return True
            else:
                return True

# Set a skin string to <value>
        elif setting_type == 'string':
            xbmc.executebuiltin('Skin.SetString(%s,%s)' % (setting, value))

# Set a skin setting to true
        elif setting_type == 'bool_true':
            xbmc.executebuiltin('Skin.SetBool(%s)' % setting)

# Set a skin setting to false
        elif setting_type == 'bool_false':
            xbmc.executebuiltin('Skin.Reset(%s)' % setting)

# If we're enabling/disabling an addon        
        elif setting_type == 'addon_enable':
            xbmc.executebuiltin('UpdateLocalAddons')
            xbmc.sleep(500)
            query = '{"jsonrpc":"2.0", "method":"Addons.SetAddonEnabled","params":{"addonid":"%s", "enabled":%s}, "id":1}' % (setting, value)
            response = xbmc.executeJSONRPC(query)
            if 'error' in str(response):
                xbmc.log('### Error With Setting: %s' % response)
                return False
            else:
                return True

# If it's none of the above then it must be a json command so we use the setting_type as the method in json
        elif setting_type == 'json':
            query = '{"jsonrpc":"2.0", "method":"%s","params":{%s}, "id":1}' % (setting, value)
            response = xbmc.executeJSONRPC(query)
            if 'error' in str(response):
                xbmc.log('### Error With Setting: %s' % response)
                return False
            else:
                return True

    except Exception as e:
        xbmc.log(Last_Error())
        xbmc.log(str(e))
#----------------------------------------------------------------
def Timestamp(mode = 'integer'):
    """
This will return the timestamp in various formats. By default it returns as "integer" mode but other options are listed below:

CODE: koding.Timestamp(mode)
mode is optional, by default it's set as integer

AVAILABLE VALUES:

    'integer' -  An integer which is nice and easy to work with in Python (especially for
    finding out human readable diffs). The format returned is [year][month][day][hour][minutes][seconds]. 
    
    'epoch'   -  Unix Epoch format (calculated in seconds passed since 12:00 1st Jan 1970).

    'clean'   -  A clean user friendly time format: Tue Jan 13 10:17:09 2009

EXAMPLE CODE:
integer_time = koding.Timestamp('integer')
epoch_time = koding.Timestamp('epoch')
clean_time = koding.Timestamp('clean')
dialog.ok('CURRENT TIME','Integer: %s' % integer_time, 'Epoch: %s' % epoch_time, 'Clean: %s' % clean_time)~"""

    import time
    now = time.time()
    if mode == 'epoch':
        return now
    
    localtime = time.localtime(now)
    if mode == 'integer':
        return time.strftime('%Y%m%d%H%M%S', localtime)

    if mode == 'clean':
        return time.asctime(localtime)
#----------------------------------------------------------------