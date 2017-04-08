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
import shutil
import xbmc
import xbmcgui

from __init__    import dolog
from systemtools import Last_Error, Show_Busy

dp            = xbmcgui.DialogProgress()
check_started = xbmc.translatePath('special://profile/addon_data/script.module.python.koding.aio/temp/playback_in_progress')
#----------------------------------------------------------------    
# TUTORIAL #
def Check_Playback():
    """
This function will return true or false based on video playback. Simply start a stream
(whether via an add-on, direct link to URL or local storage doesn't matter), the code will
then work out if playback is successful. This uses a number of checks and should take into
account all potential glitches which can occur during playback. The return should happen
within a second or two of playback being successful (or not).

CODE: Check_Playback()

EXAMPLE CODE:
xbmc.Player().play('http://totalrevolution.tv/videos/python_koding/Browse_To_Folder.mov')
isplaying = koding.Check_Playback()
if isplaying:
    dialog.ok('PLAYBACK SUCCESSFUL','Congratulations, playback was successful')
    xbmc.Player().stop()
else:
    dialog.ok('PLAYBACK FAILED','Sorry, playback failed :(')~"""

    if not os.path.exists(check_started):
        os.makedirs(check_started)
    isdialog = True
    counter = 1

# Check if the progress window is active and wait for playback
    while isdialog:
        dolog('### Current Window: %s' % xbmc.getInfoLabel('System.CurrentWindow'))
        dolog('### Current XML: %s' % xbmc.getInfoLabel('Window.Property(xmlfile)'))
        dolog('### Progress Dialog active, sleeping for %s seconds' % counter)
        xbmc.sleep(1000)
        if xbmc.getCondVisibility('Window.IsActive(progressdialog)') or (xbmc.getInfoLabel('Window.Property(xmlfile)') == 'DialogProgress.xml'):
            isdialog = True
        else:
            isdialog = False
        counter += 1
        dolog('counter: %s' % counter)

# Given the DialogProgress 10 seconds to finish and it's still up - time to close it
        if counter == 10:
            try:
                dolog('attempting to send click to close dp')
                xbmc.executebuiltin('SendClick()')
                if dp.iscanceled():
                    dp.close()
            except:
                dolog('### FAILED TO CLOSE DP')

    isplaying = xbmc.Player().isPlaying()
    counter   = 1
    if xbmc.Player().isPlayingAudio():
        return True
# If xbmc player is not yet active give it some time to initialise
    while not isplaying and counter <10:
        xbmc.sleep(1000)
        isplaying = xbmc.Player().isPlaying()
        dolog('### XBMC Player not yet active, sleeping for %s seconds' % counter)
        counter += 1

    success = 0
    counter = 0

# If it's playing give it time to physically start streaming then attempt to pull some info
    if isplaying:
        xbmc.sleep(1000)
        while not success and counter < 10:
            try:
                infotag = xbmc.Player().getVideoInfoTag()
                vidtime = xbmc.Player().getTime()
                if vidtime > 0:
                    success = 1

# If playback doesn't start automatically (buffering) we force it to play
                else:
                    dolog('### Playback active but time at zero, trying to unpause')
                    xbmc.executebuiltin('PlayerControl(Play)')
                    xbmc.sleep(2000)
                    vidtime = xbmc.Player().getTime()
                    if vidtime > 0:
                        success = 1

# If no infotag or time could be pulled then we assume playback failed, try and stop the xbmc.player
            except:
                counter += 1
                xbmc.sleep(1000)

# Check if the busy dialog is still active from previous locked up playback attempt
    isbusy  = xbmc.getCondVisibility('Window.IsActive(busydialog)')
    counter   = 1
    while isbusy:
        dolog('### Busy dialog active, sleeping for %ss' % counter)
        xbmc.sleep(1000)
        isbusy  = xbmc.getCondVisibility('Window.IsActive(busydialog)')
        counter += 1
        if counter == 5:
            xbmc.executebuiltin('Dialog.Close(busydialog)')

    if not success:
        xbmc.executebuiltin('PlayerControl(Stop)')
        dolog('### Failed playback, stopped stream')
        shutil.rmtree(check_started)
        return False

    else:
        shutil.rmtree(check_started)
        return True
#----------------------------------------------------------------    
def Play_Video(video, showbusy=True):
    dolog('### ORIGINAL VIDEO: %s'%video)
    import urlresolver
    try:    import simplejson as json
    except: import json

    playback = False
    if showbusy:
        Show_Busy()

# Play from a db entry - untested
    if video.isdigit():
        dolog('### Video is digit, presuming it\'s a db item')
        command = ('{"jsonrpc": "2.0", "id":"1", "method": "Player.Open","params":{"item":{"channelid":%s}}}' % url)
        xbmc.executeJSONRPC(command)
        playback = Check_Playback()
        is_in_progress = True
        progress_count = 0
        while is_in_progress:
            xbmc.sleep(1000)
            progress_count += 1
            dolog('Progress check is active, sleeping %s'%progress_count)
            is_in_progress = os.path.exists(check_started)

# if a plugin path is sent we try activate window
    elif video.startswith('plugin://'):
        try:
            dolog('Attempting to play via XBMC.ActivateWindow(10025, ...) method')
            xbmc.executebuiltin('XBMC.ActivateWindow(10025,%s)' % video)
            playback = Check_Playback()
            is_in_progress = True
            progress_count = 0
            while is_in_progress:
                xbmc.sleep(1000)
                progress_count += 1
                dolog('Progress check is active, sleeping %s'%progress_count)
                is_in_progress = os.path.exists(check_started)

        except:
            dolog(Last_Error())

# If an XBMC action has been sent through we do an executebuiltin command
    elif video.startswith('ActivateWindow') or video.startswith('RunAddon') or video.startswith('RunScript') or video.startswith('PlayMedia'):
        try:
            dolog('Attempting to play via xbmc.executebuiltin method')
            xbmc.executebuiltin('%s'%video)
            playback = Check_Playback()
            is_in_progress = True
            progress_count = 0
            while is_in_progress:
                xbmc.sleep(1000)
                progress_count += 1
                dolog('Progress check is active, sleeping %s'%progress_count)
                is_in_progress = os.path.exists(check_started)

        except:
            dolog(Last_Error())

    elif ',' in video:
# Standard xbmc.player method (a comma in url seems to throw urlresolver off)
        try:
            dolog('Attempting to play via xbmc.Player.play() method')
            xbmc.Player().play('%s'%video)
            playback = Check_Playback()
            is_in_progress = True
            progress_count = 0
            while is_in_progress:
                xbmc.sleep(1000)
                progress_count += 1
                dolog('Progress check is active, sleeping %s'%progress_count)
                is_in_progress = os.path.exists(check_started)

# Attempt to resolve via urlresolver
        except:
            try:
                dolog('Attempting to resolve via urlresolver module')
                dolog('video = %s'%video)
                hmf = urlresolver.HostedMediaFile(url=video, include_disabled=False, include_universal=True)
                if hmf.valid_url() == True:
                    video = hmf.resolve()
                    dolog('### VALID URL, RESOLVED: %s'%video)
                xbmc.executebuiltin('PlayMedia(%s)'%video)
                playback = Check_Playback()
                is_in_progress = True
                progress_count = 0
                while is_in_progress:
                    xbmc.sleep(1000)
                    progress_count += 1
                    dolog('Progress check is active, sleeping %s'%progress_count)
                    is_in_progress = os.path.exists(check_started)

            except:
                dolog(Last_Error())

    else:
# Attempt to resolve via urlresolver
        try:
            dolog('Attempting to resolve via urlresolver module')
            dolog('video = %s'%video)
            hmf = urlresolver.HostedMediaFile(url=video, include_disabled=False, include_universal=True)
            if hmf.valid_url() == True:
                video = hmf.resolve()
                dolog('### VALID URL, RESOLVED: %s'%video)
            xbmc.executebuiltin('PlayMedia(%s)'%video)
            playback = Check_Playback()
            is_in_progress = True
            progress_count = 0
            while is_in_progress:
                xbmc.sleep(1000)
                progress_count += 1
                dolog('Progress check is active, sleeping %s'%progress_count)
                is_in_progress = os.path.exists(check_started)

# Standard xbmc.player method
        except:
            try:
                dolog('Attempting to play via xbmc.Player.play() method')
                xbmc.Player().play('%s'%video)
                playback = Check_Playback()
                is_in_progress = True
                progress_count = 0
                while is_in_progress:
                    xbmc.sleep(1000)
                    progress_count += 1
                    dolog('Progress check is active, sleeping %s'%progress_count)
                    is_in_progress = os.path.exists(check_started)

            except:
                dolog(Last_Error())

    dolog('Playback status: %s' % playback)
    Show_Busy(False)
    return playback