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
dialog.ok('FOLDER DETAILS','Folder path: [COLOR=dodgerblue]%s[/COLOR]'%folder)
~"""    
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
dialog.ok('FOLDER DETAILS','Folder path: [COLOR=dodgerblue]%s[/COLOR]'%folder)
~"""
    if not path.endswith(os.sep):
        path += os.sep
    try:
        text = dialog.browse(type=1, heading=header, shares='myprograms', mask=extension, useThumbs=False, treatAsFolder=True, defaultt=path)
    except:
        text = dialog.browse(type=1, heading=header, s_shares='myprograms', mask=extension, useThumbs=False,
                             treatAsFolder=True, defaultt=path)
    return text
#----------------------------------------------------------------    
# TUTORIAL #
def Countdown(title='COUNTDOWN STARTED', message='A quick simple countdown example.', update_msg='Please wait, %s seconds remaining.', wait_time=10, allow_cancel=True, cancel_msg='[COLOR=gold]Sorry, this process cannot be cancelled[/COLOR]'):
    """
Bring up a countdown timer and return true if waited or false if cancelled.

CODE: Countdown(title, message, update_msg, wait_time, allow_cancel, cancel_msg):

AVAILABLE PARAMS:

    title  -  The header string in the dialog window, the default is:
    'COUNTDOWN STARTED'

    message   -  A short line of info which will show on the first line
    of the dialog window just below the title. Default is:
    'A quick simple countdown example.'

    update_msg  - The message you want to update during the countdown.
    This must contain a %s which will be replaced by the current amount
    of seconds that have passed. The default is:
    'Please wait, %s seconds remaining.'

    wait_time  -  This is the amount of seconds you want the countdown to
    run for. The default is 10.

    allow_cancel  -  By default this is set to true and the user can cancel
    which will result in False being returned. If this is set to True
    they will be unable to cancel.

    cancel_msg  -  If allow_cancel is set to False you can add a custom
    message when the user tries to cancel. The default string is:
    '[COLOR=gold]Sorry, this process cannot be cancelled[/COLOR]'

EXAMPLE CODE:
dialog.ok('COUNTDOWN EXAMPLE', 'Press OK to bring up a countdown timer', '', 'Try cancelling the process.')
my_return = koding.Countdown(title='COUNTDOWN EXAMPLE', message='Quick simple countdown message (cancel enabled).', update_msg='%s seconds remaining', wait_time=5)
if my_return:
    dialog.ok('SUCCESS!','Congratulations you actually waited through the countdown timer without cancelling!')
else:
    dialog.ok('BORED MUCH?','What happened, did you get bored waiting?', '', '[COLOR=dodgerblue]Let\'s set off another countdown you CANNOT cancel...[/COLOR]')
    koding.Countdown(title='COUNTDOWN EXAMPLE', message='Quick simple countdown message (cancel disabled).', update_msg='%s seconds remaining', wait_time=5, allow_cancel=False, cancel_msg='[COLOR=gold]Sorry, this process cannot be cancelled[/COLOR]')
~"""
    dp        = xbmcgui.DialogProgress()
    current   = 0
    increment = 100 / wait_time
    cancelled = False

    dp.create(title)
    while current <= wait_time:
        if (dp.iscanceled()):
            if allow_cancel:
                cancelled = True
                break
            else:
                dp.create(title,cancel_msg)

        if current != 0: 
            xbmc.sleep(1000)

        remaining = wait_time - current
        if remaining == 0: 
            percent = 100
        else: 
            percent = increment * current
        
        remaining_display = update_msg % remaining
        dp.update(percent, message, remaining_display)

        current += 1

    if cancelled == True:     
        return False
    else:
        return True        
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
dialog.ok('TEXT RETURNED','You typed in:', '', '[COLOR=dodgerblue]%s[/COLOR]'%mytext)
~"""
    keyboard = xbmc.Keyboard(default, heading, hidden)
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        return unicode(keyboard.getText(), "utf-8")
    return default
#----------------------------------------------------------------    
# TUTORIAL #
def Notify(title, message, duration=2000, icon='special://home/addons/script.module.python.koding.aio/resources/update.png'):
    """
Show a short notification for x amount of seconds

CODE: koding.Notify(title, message, [duration, icon])

AVAILABLE PARAMS:

    (*) title    -  A short title to show on top line of notification

    (*) message  -  A short message to show on the bottom line of notification

    duration  -  An integer in milliseconds, the default to show the notification for is 2000

    icon      -  The icon to show in notification bar, default is the update icon from this module. 

EXAMPLE CODE:
koding.Notify(title='TEST NOTIFICATION', message='This is a quick 5 second test', duration=5000)
~"""
    xbmc.executebuiltin('XBMC.Notification(%s, %s, %s, %s)' % (title , message , duration, icon))
#----------------------------------------------------------------
# TUTORIAL #
def Show_Busy(status=True, sleep=0):
    """
This will show/hide a "working" symbol.

CODE: Show_Busy([status, sleep])

AVAILABLE PARAMS:

    status - This optional, by default it's True which means the "working"
    symbol appears. False will disable.

    sleep  -  If set the busy symbol will appear for <sleep> amount of
    milliseconds and then disappear.

EXAMPLE CODE:
dialog.ok('BUSY SYMBOL','Press OK to show a busy dialog which restricts any user interaction. We have added a sleep of 5 seconds at which point it will disable.')
koding.Show_Busy(sleep=5000)
dialog.ok('BUSY SYMBOL','We will now do the same but with slightly different code')
koding.Show_Busy(status=True)
xbmc.sleep(5000)
koding.Show_Busy(status=False)
~"""
    if status:
        xbmc.executebuiltin("ActivateWindow(busydialog)")
        if sleep:
            xbmc.sleep(sleep)
            xbmc.executebuiltin("Dialog.Close(busydialog)")
    else:
        xbmc.executebuiltin("Dialog.Close(busydialog)")
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
koding.Text_Box('TEST HEADER','Just some random text... Use kodi tags for new lines, colours etc.')
~"""
    xbmc.executebuiltin("ActivateWindow(10147)")
    controller = xbmcgui.Window(10147)
    xbmc.sleep(500)
    controller.getControl(1).setLabel(header)
    controller.getControl(5).setText(message)
#----------------------------------------------------------------    