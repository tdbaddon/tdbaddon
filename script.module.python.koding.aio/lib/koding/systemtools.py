# script.module.python.koding.aio
# Python Koding AIO (c) by whufclee

# Python Koding AIO is licensed under a
# Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.

# You should have received a copy of the license along with this
# work. If not, see http://creativecommons.org/licenses/by-nc-nd/4.0.

# IMPORTANT: If you choose to use the special noobsandnerds features which hook into their server
# please make sure you give approptiate credit in your add-on description (noobsandnerds.com)
# 
# Please make sure you've read and understood the license, this code can NOT be used commercially
# and it can NOT be modified and redistributed. Thank you.

def Clear_Data(addonid):
# Clear the data from your cookie folder
    import os
    import shutil
    import xbmc

    root_path = os.path.join(xbmc.translatePath('special://profile/addon_data'),addonid)
    
    try:
        xbmc.log('data cleared from: %s' % addonid)
        shutil.rmtree(os.path.join(root_path, 'cookies'))
        return True
    except:
        xbmc.log('failed to clear data from: %s' % addonid)
        return False
#----------------------------------------------------------------    
def ID_Generator(size=15):
# Generate a random string
    import string
    import random

    chars=string.ascii_uppercase + string.digits + string.ascii_lowercase
    return ''.join(random.choice(chars) for _ in range(size))
#----------------------------------------------------------------
def Installed_Addons(types='unknown', content ='unknown', properties = ''):
# Return a list of installed add-ons
    import xbmc
    
    try:
        import simplejson as json
    except:
        import json

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
def Last_Error():
# Return details of the last error, to be used in try/except statements
    import traceback
    error = traceback.format_exc()
    return error
#----------------------------------------------------------------
def Set_Setting(setting_type, setting, value = ''):
# Set a setting via json, this one requires a list to be sent through whereas Set_Setting() doesn't.
    import xbmc
    
    try:
        import simplejson as json
    except:
        import json

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
#-----------------------------------------------------------------------------
def Timestamp(mode = 'integer'):
# Return current timestamp in a variety of formats
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
