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

def Check_Playback():
    import xbmc
    import xbmcgui
# Check if playback works
    isdialog = True
    counter = 1
    dp = xbmcgui.DialogProgress()

# Check if the progress window is active and wait for playback
    while isdialog:
        xbmc.log('### Current Window: %s' % xbmc.getInfoLabel('System.CurrentWindow'))
        xbmc.log('### Current XML: %s' % xbmc.getInfoLabel('Window.Property(xmlfile)'))
        xbmc.log('### Progress Dialog active, sleeping for %s seconds' % counter)
        xbmc.sleep(1000)
        if xbmc.getCondVisibility('Window.IsActive(progressdialog)') or (xbmc.getInfoLabel('Window.Property(xmlfile)') == 'DialogProgress.xml'):
            isdialog = True
        else:
            isdialog = False
        counter += 1
        xbmc.log('counter: %s' % counter)

# Given the DialogProgress 10 seconds to finish and it's still up - time to close it
        if counter == 10:
            try:
                xbmc.log('attempting to send click to close dp')
                xbmc.executebuiltin('SendClick()')
                if dp.iscanceled():
                    dp.close()
            except:
                xbmc.log('### FAILED TO CLOSE DP')

    isplaying = xbmc.Player().isPlaying()
    counter   = 1

# If xbmc player is not yet active give it some time to initialise
    while not isplaying and counter <10:
        xbmc.sleep(1000)
        isplaying = xbmc.Player().isPlaying()
        xbmc.log('### XBMC Player not yet active, sleeping for %s seconds' % counter)
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
                    xbmc.log('### Playback active but time at zero, trying to unpause')
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
        xbmc.log('### Busy dialog active, sleeping for %ss' % counter)
        xbmc.sleep(1000)
        isbusy  = xbmc.getCondVisibility('Window.IsActive(busydialog)')
        counter += 1
        if counter == 5:
            xbmc.executebuiltin('Dialog.Close(busydialog)')

    if not success:
        xbmc.executebuiltin('PlayerControl(Stop)')
        xbmc.log('### Failed playback, stopped stream')
        return False

    else:
        return True
#----------------------------------------------------------------    
