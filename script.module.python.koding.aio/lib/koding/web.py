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

def Download(url, dest, dp = None):
# Download a file
    import urllib
    import time

    start_time=time.time()
    urllib.urlretrieve(url, dest, lambda nb, bs, fs: Download_Progress(nb, bs, fs, dp, start_time))
#----------------------------------------------------------------    
def Download_Progress(numblocks, blocksize, filesize, dp, start_time):
# Show downoad progress, to be used in conjunction with function above
    import xbmcgui

    try: 
        percent = min(numblocks * blocksize * 100 / filesize, 100) 
        currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
        kbps_speed = numblocks * blocksize / (time.time() - start_time) 
        if kbps_speed > 0: 
            eta = (filesize - numblocks * blocksize) / kbps_speed 
        else: 
            eta = 0 
        kbps_speed = kbps_speed / 1024 
        total = float(filesize) / (1024 * 1024) 
        mbs = '%.02f MB of %.02f MB' % (currently_downloaded, total) 
        e = 'Speed: %.02f Kb/s ' % kbps_speed 
        e += 'ETA: %02d:%02d' % divmod(eta, 60) 
        if dp:
            dp.update(percent, mbs, e)
        if dp.iscanceled(): 
            dp.close()
    except: 
        percent = 100
        if dp:
            dp.update(percent) 
    if dp:
        if dp.iscanceled(): 
            dp.close()
#----------------------------------------------------------------    
