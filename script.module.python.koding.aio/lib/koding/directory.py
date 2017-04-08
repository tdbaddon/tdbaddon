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

import sys
import urllib
import xbmc
import xbmcgui
import xbmcplugin

dialog = xbmcgui.Dialog()
mode   = ''
#----------------------------------------------------------------
# TUTORIAL #
def Add_Dir(name, url, mode, folder = False, icon = '', fanart = '', description = 'N/A', info_labels ='', content_type=''):
    """
This allows you to create a list item/folder inside your add-on.
Please take a look at your addon default.py comments for more information
(presuming you created one at http://totalrevolution.tv)

CODE: Add_Dir(name, url, mode, [folder, icon, fanart, description, info_labels, content_type]))

AVAILABLE PARAMS:

    (*) name  -  This is the name you want to show for the list item

    (*) url   -  This is a temporary global variable (string), when you click on
    another list item it will change to whatever you have that set to

    (*) mode  -  The mode you want to open when this item is clicked, this is set
    in your master_modes dictionary (see template add-on linked above)

    folder       -  This is an optional boolean, by default it's set to False.
    True will open into a folder rather than an executable command

    icon         -  The path to the thumbnail you want to use for this list item

    fanart       -  The path to the fanart you want to use for this list item

    description  - A description of your list item, it's skin dependant but this
    usually appears below the thumbnail

    info_labels  - You can send through any number of info_labels via this option.
    For full details on the infolabels available please check the pydocs.
    When passing through infolabels you need to use this format:
    info_labels='genre : comedy ~ title : test video'
    
    IMPORTANT: The colon separating the key from value and the tilda separating each
    infolabel MUST have a space either side.

    content_type - By default this will set the content_type for kodi to a blank string
    which is what Kodi expects for generic category listings. There are plenty of different
    types though and when set Kodi will perform different actions (such as access the
    database looking for season/episode information for the list item).

    WARNING: Setting the wrong content type for your listing can cause the system to
    log thousands of error reports in your log, cause the system to lag and make
    thousands of unnecessary db calls - sometimes resulting in a crash. You can find
    details on the content_types available here: http://forum.kodi.tv/showthread.php?tid=299107
~"""

    from __init__ import dolog
# Check we're in an appropriate section for the content type set
    dolog(xbmc.getInfoLabel('Window.Property(xmlfile)'))
    song_only_modes  = ['songs','artist','album','song','music']
    video_only_modes = ['sets','tvshows','seasons','actors','directors','unknown','video','set','movie','tvshow','season','episode']
    if xbmc.getInfoLabel('Window.Property(xmlfile)') == 'MyVideoNav.xml' and content_type in song_only_modes:
        content_type = ''
    if xbmc.getInfoLabel('Window.Property(xmlfile)') == 'MyMusicNav.xml' and content_type in video_only_modes:
        content_type = ''


# Grab the infolabels sent through and split them up into a proper dictionary
    my_infolabels = { "Title": name, "FileName" : name}
    if not 'Plot:' in info_labels:
        my_infolabels['Plot'] = description
    final_labels  = []
    if info_labels != '':
        if not ' ~ ' in info_labels:
            final_labels.append(info_labels)
        else:
            final_labels = info_labels.split(' ~ ')

        for item in final_labels:
            key, value = item.split(' : ')
            my_infolabels[key] = value

    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=icon)
    liz.setInfo( type=content_type, infoLabels = my_infolabels)
    # liz.setArt({"thumb":,"icon:"})
    liz.setProperty( "Fanart_Image", fanart )

    if url.startswith("plugin://"):
        u = url
        listitem.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz)
    
    else:
        u   = sys.argv[0]
        u += "?mode="           +str(mode)
        u += "&url="            +urllib.quote_plus(url)
        u += "&name="           +urllib.quote_plus(name)
        u += "&iconimage="      +urllib.quote_plus(icon)
        u += "&fanart="         +urllib.quote_plus(fanart)
        u += "&description="    +urllib.quote_plus(description)
        
        if folder:
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        
        else:
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False) 
#----------------------------------------------------------------
def Default_Mode():
    """ internal command ~"""
    dialog = xbmcgui.Dialog()
    dialog.ok('MODE ERROR','You\'ve tried to call Add_Dir() without a valid mode, check you\'ve added the mode into the master_modes dictionary')
#----------------------------------------------------------------
# TUTORIAL #
def Grab_Params(extras, keys = '', separator = '<~>'):
    """
This will allow you to send multiple values through via the Add_Dir
function just as one string (url). This is then split up into however
many values you want.

CODE: Grab_Params(extras, keys, [separator]))

AVAILABLE PARAMS:

    (*) extras  -  This is the string you want to split into a list of values.
    Each value needs to be split by <~> (unless a different separator is sent through).
    A good example of sending through name, DOB and sex would be: 'Mark<~>01.02.1976<~>male'

    (*) keys    -  These are the keys (variable names) you want to assign the split
    extras to. They need to be comma separated so using the above extras example
    you could use something like this: key='name,DOB,sex'.

    separator  -  This is optional, if you want to change the default separator you can do
    so here. Make sure it's something unique not used anywhere else in the string.

EXAMPLE CODE:
raw_string = 'Mark<~>01.02.1976<~>male'
vars = 'name,DOB,sex'
params = koding.Grab_Params(extras=raw_string, keys=vars)
dialog.ok('RAW STRING','We\'re going to send through the following string','[COLOR=dodgerblue]%s[/COLOR]'%raw_string,'Click OK to see the results.')
dialog.ok('GRAB PARAMS RESULTS','Name: %s'%params["name"], 'DOB: %s'%params["DOB"], 'Sex: %s'%params["sex"])
~"""
    params_array = {}
    keyerror     = False
    keys         = keys.replace(' ','').strip()
    if keys.endswith(','):
        keys = keys[:-1]
    if ',' in keys:
        keys = keys.split(',')
        keylen = len(keys)
    elif keys != '':
        keyerror = True
    else:
        dialog.ok('KEY ERROR','You\'ve called the Grab_Params function but not provided any keys')
        return

    if separator in extras and not keyerror:
        split_url = extras.split(separator)
        if len(split_url) == keylen:
            counter   = 0
            for item in split_url:
                params_array[keys[counter]] = item
                counter += 1
            return params_array
        else:
            keyerror = True
    else:
        keyerror = True

    if keyerror:
        dialog.ok('KEY ERROR','You\'ve called Grab_Params() but there\'s no need. The url you passed through does not contain '
            'any instances of %s which means there\'s nothing to split. Remove the Grab_Params function and just access url directly.'%separator)
        return
#----------------------------------------------------------------    
# TUTORIAL #
def Populate_List(url, start_point=r'<li+.<a href="', end_point=r'</a+.</li>', separator = r">", skip=['..','.','Parent Directory']):
    """
If you have a basic index web page or a webpage with a common
structure of displaying links (on all pages) then you can use this
to populate an add-on. It's capable of cleverly working out what
needs to be sent through as a directory and what's a playable item.

CODE: Populate_List(url, [start_point, end_point, separator, skip):

AVAILABLE PARAMS:

    (*) url  -  The start page of where to pull the first links from

    start_point  -  Send through the code tags you want to search for in the
    webpage. By default it's setup for a standard indexed site so the start_point
    is '<li+.<a href="'. The code will then grab every instance of start_point to end_point.

    end_point    -  Send through the code tags you want to search for in the
    webpage. By default it's setup for a standard indexed site so the end_point
    is '</a+.</li>'. The code will then grab every instance of start_point to end_point.

    separator  -  This is the point in the grabbed links (from above) where you want
    to split the string into a url and a display name. The default is ">".

    skip       -  By default this is set to ['..', '.', 'Parent Directory']. This is
    a list of links you don't want to appear in your add-on listing.

EXAMPLE CODE:
link ='http://totalrevolution.tv/videos/'
sp   ='<a href="'
ep   ='</a>'
sep  = '">'
koding.Populate_List(url=link, start_point=sp, end_point=ep, separator=sep)
~"""
    import re
    import urlparse
    from __init__       import dolog
    from filetools      import Find_In_Text
    from systemtools    import Cleanup_String
    from video          import Play_Video
    from web            import Open_URL, Get_Extension, Cleanup_URL

    badlist = []
    if '<~>' in url:
        params      = Grab_Params(extras=url,keys='url,start,end,separator,skip')
        url         = params['url']
        start_point = params['start']
        end_point   = params['end']
        separator   = params['separator']
        skip        = params['skip']
    raw_content = Open_URL(url).replace('\n','').replace('\r','').replace('\t','')
    raw_list    = Find_In_Text(content=raw_content,start=start_point,end=end_point,show_errors=False)
    if raw_list != None:
        for item in raw_list:
            cont = True
            try:
                dolog('ITEM: %s'%item)
                new_sep = re.search(separator, item).group()
                link, title = item.split(new_sep)
            except:
                dolog('^ BAD ITEM, adding to badlist')
                badlist.append(item)
                cont = False
                # break
            if cont:
                title       = Cleanup_String(title)
                if title not in skip:
    # Make sure the link we've grabbed isn't a full web address
                    if not '://' in link:
                        link        = urlparse.urljoin(url, link)
                    link        = Cleanup_URL(link)
                    extension   = Get_Extension(link)

                    if not link.endswith('/') and extension == '':
                        link = link+'/'
                    if extension == '' and not 'mms://' in link:
                        Add_Dir(name=title, url=link+'<~>%s<~>%s<~>%s<~>%s'%(start_point,end_point,separator,skip),mode='populate_list',folder=True)
                    else:
                        Add_Dir(name=title, url=link,mode='play_video',folder=False)
    else:
        Add_Dir(name='Link 1', url=params["url"],mode='play_video',folder=False)
    if len(badlist)>0:
        dialog.ok('ERROR IN REGEX','The separator used is not working, an example raw match from the web page has now been printed to the log.')
        for item in badlist:
            dolog('BADLIST ITEM: %s'%item)
