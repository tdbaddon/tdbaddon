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

import os
import xbmc
import xbmcgui

dialog = xbmcgui.Dialog()
#----------------------------------------------------------------    
# TUTORIAL #
def Browse_To_Folder(header='Select the folder you want to use', path = 'special://home'):
    """
Browse to a folder and return the path

CODE: koding.Browse_To_Folder([header, path])

AVAILABLE PARAMS:

    header  -  As the name suggests this is a string to be used for the header/title
    of the window. The default is "Select the folder you want to use".

    path    -  Optionally you can add a default path for the browse start folder.
    The default start position is the Kodi HOME folder.

EXAMPLE CODE:
folder = koding.Browse_To_Folder('Choose a folder you want to use')
dialog.ok('FOLDER DETAILS','Folder path: [COLOR=dodgerblue]%s[/COLOR]'%folder)~"""
    
    text = dialog.browse(3, header, 'files', '', False, False, path)
    return text
#----------------------------------------------------------------    
# TUTORIAL #
def Browse_To_File(header='Select the file you want to use', path = 'special://home/addons/', extension = ''):
    """
Browse to a file and return the path

CODE: koding.Browse_To_File([header, path, extension])

AVAILABLE PARAMS:

    header    -  As the name suggests this is a string to be used for the header/title
    of the window. The default is "Select the file you want to use".

    path      -  Optionally you can add a default path for the browse start folder.
    The default start position is the Kodi HOME folder.

    extension -  Optionally set extensions to filter by, let's say you only wanted
    zip and txt files to show you would send through '.zip|.txt'

EXAMPLE CODE:
folder = koding.Browse_To_File(header='Choose a file you want to use', path='special://home/userdata')
dialog.ok('FOLDER DETAILS','Folder path: [COLOR=dodgerblue]%s[/COLOR]'%folder)~"""
    if not path.endswith(os.sep):
        path += os.sep
    text = dialog.browse(type=1, heading=header, shares='myprograms', mask=extension, useThumbs=False, treatAsFolder=True, defaultt=path)
    return text
#----------------------------------------------------------------    
# TUTORIAL #
def Keyboard(heading='', default='', hidden=False):
    """
Show an on-screen keyboard and return the string

CODE: koding.Keyboard([default, heading, hidden])

AVAILABLE PARAMS:

    heading  -  Optionally enter a heading for the text box.

    default  -  This is optional, if set this will act as the default text shown in the text box

    hidden   -  Boolean, if set to True the text will appear as hidden (starred out)

EXAMPLE CODE:
mytext = koding.Keyboard(heading='Type in the text you want returned', default='test text')
dialog.ok('TEXT RETURNED','You typed in:', '', '[COLOR=dodgerblue]%s[/COLOR]'%mytext)~"""
    
    keyboard = xbmc.Keyboard(default, heading, hidden)
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        return unicode(keyboard.getText(), "utf-8")
    return default
#----------------------------------------------------------------    
# TUTORIAL #
def Text_Box(header, message):
    """
This will allow you to open a blank window and fill it with some text.

CODE: koding.Text_Box(header, message)

AVAILABLE PARAMS:

    (*) header  -  As the name suggests this is a string to be used for the header/title of the window

    (*) message -  Yes you've probably already gussed it, this is the main message text


EXAMPLE CODE:
koding.Text_Box('TEST HEADER','Just some random text... Use kodi tags for new lines, colours etc.')~"""

    xbmc.executebuiltin("ActivateWindow(10147)")
    controller = xbmcgui.Window(10147)
    xbmc.sleep(500)
    controller.getControl(1).setLabel(header)
    controller.getControl(5).setText(message)
#----------------------------------------------------------------    