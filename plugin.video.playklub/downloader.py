import xbmcgui
import urllib

def download(url, dest, dialogprocess = None):
    if not dialogprocess:
        dialogprocess = xbmcgui.DialogProgress()
        dialogprocess.create("Kodi UK Wizard","Downloading & Installing File",' ', ' ')
    dialogprocess.update(0)
    urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dialogprocess))
 
def _pbhook(numblocks, blocksize, filesize, url, dialogprocess):
    try:
        percent = min((numblocks*blocksize*100)/filesize, 100)
        dialogprocess.update(percent)
    except:
        percent = 100
        dialogprocess.update(percent)
    if dialogprocess.iscanceled(): 
        raise Exception("Canceled")
        dialogprocess.close()
