addon_id = 'plugin.video.dnatv'
data_folder = 'special://userdata/addon_data/' + addon_id
Url = 'https://raw.githubusercontent.com/macblizzard/dnarepo/master/plugin.video.dnatv/userdata/'
File = ['http_mw1_iptv66_tv-genres', 'http_mw1_iptv66_tv', 'settings.xml']

def download(url, dest, dp = None):
    if not dp:
        dp = xbmcgui.DialogProgress()
#        dp.create("Loading")
#    dp.update(0)
    urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
 
def _pbhook(numblocks, blocksize, filesize, url, dp):
    try:
       
        dp.update
    except:
        
        dp.update(percent)

for file in File:
	url = Url + file
	fix = xbmc.translatePath(os.path.join( data_folder, file))
	download(url, fix)
