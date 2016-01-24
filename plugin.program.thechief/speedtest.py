
#
#Thanks go to the-one who created the initial speedtest code for me in early 2014
#That code broke but it didn't take too much to fix it, if you get problems it's most likely
#down to the fact that you need to use another download link that plays nicely with XBMC/Kodi

import xbmc, xbmcplugin
import xbmcgui
import xbmcaddon
import urllib
import time
import os
import sys

ADDON_ID   = 'plugin.program.thechief'
ADDON      =  xbmcaddon.Addon(id=ADDON_ID)
HOME       =  ADDON.getAddonInfo('path')
ARTPATH    =  'http://totalxbmc.tv/totalrevolution/art/' + os.sep
FANART     =  'http://totalxbmc.tv/totalrevolution/art/fanart.jpg'
addon_name="Speed Test"

max_Bps = 0.0
currently_downloaded_bytes = 0.0

#-----------------------------------------------------------------------------------------------------------------
def download(url, dest, dp = None):
    if not dp:
        dp = xbmcgui.DialogProgress()
        dp.create("Speed Test","Testing your internet speed...",' ', ' ')
    dp.update(0)
    start_time=time.time()
    
    try:
        urllib.urlretrieve(url, dest, lambda nb, bs, fs: _pbhook(nb, bs, fs, dp, start_time))
    except:
        pass
    
    # return time taken
    return ( time.time() - start_time )
#-----------------------------------------------------------------------------------------------------------------
def _pbhook(numblocks, blocksize, filesize, dp, start_time):
        
        global max_Bps
        global currently_downloaded_bytes
        
        try: 
            percent = min(numblocks * blocksize * 100 / filesize, 100) 
            currently_downloaded_bytes = float(numblocks) * blocksize
            currently_downloaded = currently_downloaded_bytes / (1024 * 1024) 
            Bps_speed = currently_downloaded_bytes / (time.time() - start_time) 
            if Bps_speed > 0:                                                 
                eta = (filesize - numblocks * blocksize) / Bps_speed 
                if Bps_speed > max_Bps: max_Bps = Bps_speed
            else: 
                eta = 0 
            kbps_speed = Bps_speed * 8 / 1024 
            mbps_speed = kbps_speed / 1024 
            total = float(filesize) / (1024 * 1024) 
            mbs = '%.02f MB of %.02f MB' % (currently_downloaded, total) 
            e = 'Speed: %.02f Mb/s ' % mbps_speed
            e += 'ETA: %02d:%02d' % divmod(eta, 60) 
            dp.update(percent, mbs, e)
        except: 
            currently_downloaded_bytes = float(filesize)
            percent = 100 
            dp.update(percent) 
        if dp.iscanceled(): 
            dp.close() 
            raise Exception("Cancelled")
#-----------------------------------------------------------------------------------------------------------------
def make_dir(mypath, dirname):
    ''' Creates sub-directories if they are not found. '''
    import xbmcvfs
    
    if not xbmcvfs.exists(mypath): 
        try:
            xbmcvfs.mkdirs(mypath)
        except:
            xbmcvfs.mkdir(mypath)
    
    subpath = os.path.join(mypath, dirname)
    
    if not xbmcvfs.exists(subpath): 
        try:
            xbmcvfs.mkdirs(subpath)
        except:
            xbmcvfs.mkdir(subpath)
            
    return subpath
#-----------------------------------------------------------------------------------------------------------------
def GetEpochStr():
    import datetime
    time_now=datetime.datetime.now()
    
    import time
    epoch=time.mktime(time_now.timetuple())+(time_now.microsecond/1000000.)
    
    epoch_str = str('%f' % epoch)
    epoch_str = epoch_str.replace('.','')
    epoch_str = epoch_str[:-3]

    return epoch_str
#-----------------------------------------------------------------------------------------------------------------
def runtest(url):
    addon_profile_path = xbmc.translatePath(ADDON.getAddonInfo('profile'))
    speed_test_files_dir = make_dir(addon_profile_path, 'speedtestfiles')
    speed_test_download_file = os.path.join(speed_test_files_dir, GetEpochStr() + '.speedtest')
    timetaken = download(url, speed_test_download_file)
    os.remove(speed_test_download_file)
    avgspeed = ((currently_downloaded_bytes / timetaken) * 8 / ( 1024 * 1024 ))
    maxspeed = (max_Bps * 8/(1024*1024))
    if avgspeed < 2:
        livestreams = 'Very low quality streams may work'
        onlinevids = 'Expect buffering, do not try HD'
    elif avgspeed < 2.5:
        livestreams = 'You should be ok for SD content only'
        onlinevids = 'SD/DVD quality should be ok, do not try HD'
    elif avgspeed < 5:
        livestreams = 'Some HD streams may struggle, SD will be fine'
        onlinevids = 'Most will be fine, some Blurays may struggle'
    elif avgspeed < 10:
        livestreams = 'All streams including HD should stream fine'
        onlinevids = 'Most will be fine, some Blurays may struggle'
    else:
        livestreams = 'All streams including HD should stream fine'
        onlinevids = 'You can play all files with no problems'
    print "Average Speed: " + str(avgspeed)
    print "Max. Speed: " + str(maxspeed)
    dialog = xbmcgui.Dialog()
    ok = dialog.ok('Speed Test - Results',
#    '[COLOR blue]Duration:[/COLOR] %.02f secs' % timetaken,
    '[COLOR blue]Average Speed:[/COLOR] %.02f Mb/s ' % avgspeed,
    '[COLOR blue]Live Streams:[/COLOR] ' + livestreams,
    '[COLOR blue]Online Video:[/COLOR] ' + onlinevids,
#    '[COLOR blue]Maximum Speed:[/COLOR] %.02f Mb/s ' % maxspeed,
    )
