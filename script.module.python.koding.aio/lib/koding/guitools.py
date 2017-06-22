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
import sys
import xbmc
import xbmcgui
from systemtools import Last_Error

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
def Keyboard(heading='',default='',hidden=False,return_false=False,autoclose=False,kb_type='alphanum'):
    """
Show an on-screen keyboard and return the string

CODE: koding.Keyboard([default, heading, hidden, return_false, autoclose, kb_type])

AVAILABLE PARAMS:

    heading  -  Optionally enter a heading for the text box.

    default  -  This is optional, if set this will act as the default text shown in the text box

    hidden   -  Boolean, if set to True the text will appear as hidden (starred out)

    return_false - By default this is set to False and when escaping out of the keyboard
    the default text is returned (or an empty string if not set). If set to True then
    you'll receive a return of False.

    autoclose - By default this is set to False but if you want the keyboard to auto-close
    after a period of time you can send through an integer. The value sent through needs to
    be milliseconds, so for example if you want it to close after 3 seconds you'd send through
    3000. The autoclose function only works with standard alphanumeric keyboard types.

    kb_type  -  This is the type of keyboard you want to show, by default it's set to alphanum.
    A list of available values are listed below:

        'alphanum'  - A standard on-screen keyboard containing alphanumeric characters.
        'numeric'   - An on-screen numerical pad.
        'date'      - An on-screen numerical pad formatted only for a date.
        'time'      - An on-screen numerical pad formatted only for a time.
        'ipaddress' - An on-screen numerical pad formatted only for an IP Address.
        'password'  - A standard keyboard but returns value as md5 hash. When typing
        the text is starred out, once you've entered the password you'll get another
        keyboard pop up asking you to verify. If the 2 match then your md5 has is returned.


EXAMPLE CODE:
mytext = koding.Keyboard(heading='Type in the text you want returned',default='test text')
dialog.ok('TEXT RETURNED','You typed in:', '', '[COLOR=dodgerblue]%s[/COLOR]'%mytext)
dialog.ok('AUTOCLOSE ENABLED','This following example we\'ve set the autoclose to 3000. That\'s milliseconds which converts to 3 seconds.')
mytext = koding.Keyboard(heading='Type in the text you want returned',default='this will close in 3s',autoclose=3000)
dialog.ok('TEXT RETURNED','You typed in:', '', '[COLOR=dodgerblue]%s[/COLOR]'%mytext)
mytext = koding.Keyboard(heading='Enter a number',kb_type='numeric')
dialog.ok('NUMBER RETURNED','You typed in:', '', '[COLOR=dodgerblue]%s[/COLOR]'%mytext)
dialog.ok('RETURN FALSE ENABLED','All of the following examples have "return_false" enabled. This means if you escape out of the keyboard the return will be False.')
mytext = koding.Keyboard(heading='Enter a date',return_false=True,kb_type='date')
dialog.ok('DATE RETURNED','You typed in:', '', '[COLOR=dodgerblue]%s[/COLOR]'%mytext)
mytext = koding.Keyboard(heading='Enter a time',return_false=True,kb_type='time')
dialog.ok('TIME RETURNED','You typed in:', '', '[COLOR=dodgerblue]%s[/COLOR]'%mytext)
mytext = koding.Keyboard(heading='IP Address',return_false=True,kb_type='ipaddress',autoclose=5)
dialog.ok('IP RETURNED','You typed in:', '', '[COLOR=dodgerblue]%s[/COLOR]'%mytext)
mytext = koding.Keyboard(heading='Password',kb_type='password')
dialog.ok('MD5 RETURN','The md5 for this password is:', '', '[COLOR=dodgerblue]%s[/COLOR]'%mytext)
~"""
    kb_type = eval( 'xbmcgui.INPUT_%s'%kb_type.upper() )
    if hidden:
        hidden = eval( 'xbmcgui.%s_HIDE_INPUT'%kb_type.upper() )
    keyboard = dialog.input(heading,default,kb_type,hidden,autoclose)

    if keyboard != '':
        return unicode(keyboard, "utf-8")
    
    elif not return_false:
        return default
    
    else:
        return False
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
def OK_Dialog(title,message):
    """
This will bring up a short text message in a dialog.ok window.

CODE: OK_Dialog(title,message)

AVAILABLE PARAMS:

    (*) title  -  This is title which appears in the header of the window.

    (*) message  -  This is the main text you want to appear.

EXAMPLE CODE:
koding.OK_Dialog(title='TEST DIALOG',message='This is a test dialog ok box. Click OK to quit.')
~"""
    dialog.ok(title,message)
#----------------------------------------------------------------
# TUTORIAL #
def Select_Dialog(title,options,key=True):
    """
This will bring up a selection of options to choose from. The options are
sent through as a list and only one can be selected - this is not a multi-select dialog.

CODE: Select_Dialog(title,options,[key])

AVAILABLE PARAMS:

    (*) title  -  This is title which appears in the header of the window.

    (*) options  -  This is a list of the options you want the user to be able to choose from.

    key  -  By default this is set to True so you'll get a return of the item number. For example
    if the user picks "option 2" and that is the second item in the list you'll receive a return of
    1 (0 would be the first item in list and 1 is the second). If set to False you'll recieve a return
    of the actual string associated with that key, in this example the return would be "option 2".

EXAMPLE CODE:
my_options = ['Option 1','Option 2','Option 3','Option 4','Option 5']
mychoice = koding.Select_Dialog(title='TEST DIALOG',options=my_options,key=False)
koding.OK_Dialog(title='SELECTED ITEM',message='You selected: [COLOR=dodgerblue]%s[/COLOR]\nNow let\'s try again - this time we will return a key...'%mychoice)
mychoice = koding.Select_Dialog(title='TEST DIALOG',options=my_options,key=True)
koding.OK_Dialog(title='SELECTED ITEM',message='The item you selected was position number [COLOR=dodgerblue]%s[/COLOR] in the list'%mychoice)
~"""
    mychoice = dialog.select(title,options)
    if key:
        return mychoice
    else:
        return options[mychoice]
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
# TUTORIAL #
def YesNo_Dialog(title,message,yes=None,no=None):
    """
This will bring up a short text message in a dialog.yesno window. This will
return True or False

CODE: YesNo_Dialog(title,message,[yeslabel,nolabel])

AVAILABLE PARAMS:

    (*) title  -  This is title which appears in the header of the window.

    (*) message  -  This is the main text you want to appear.

    yes  -  Optionally change the default "YES" to a custom string

    no  -  Optionally change the default "NO" to a custom string

EXAMPLE CODE:
mychoice = koding.YesNo_Dialog(title='TEST DIALOG',message='This is a yes/no dialog with custom labels.\nDo you want to see an example of a standard yes/no.',yes='Go on then',no='Nooooo!')
if mychoice:
    koding.YesNo_Dialog(title='STANDARD DIALOG',message='This is an example of a standard one without sending custom yes/no params through.')
~"""
    choice = dialog.yesno(title,message,yeslabel=yes,nolabel=no)
    return choice
#----------------------------------------------------------------
