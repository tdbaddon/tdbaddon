import xbmcgui
import urllib

def download(url, dest, dp = None):
    if not dp:
        dp = xbmcgui.DialogProgress()
        dp.create("Status...","Checking Installation",' ', ' ')
    dp.update(0)
    urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))

def _pbhook(numblocks, blocksize, filesize, url, dp):
    try:
        percent = min((numblocks*blocksize*100)/filesize, 100)
        dp.update(percent)
    except:
        percent = 100
        dp.update(percent)
    if dp.iscanceled():
        dp.close()
        raise Exception("Canceled")



# def download(url, dest, dp=None):
#     if not dp:
#         dp = xbmcgui.DialogProgress()
#         dp.create("Status...", "Checking Installation", ' ', ' ')
#     dp.update(0)
#     u = urllib.urlopen(url)
#     with open(dest, 'wb') as f:
#         meta = u.info()
#         file_size = int(meta.getheaders("Content-Length")[0])
#         file_size_dl = 0
#         chunk_sz = 908192
#         while True:
#             buffer = u.read(chunk_sz)
#             if not buffer: break
#             file_size_dl += len(buffer)
#             f.write(buffer)
#             percent = min((file_size_dl * 100) / file_size, 100)
#             status = r'%3.2f%%    %10d' % (file_size_dl * 100. / file_size, file_size_dl)
#             dp.update(percent,'Downloading and Configuring ','Please Wait',status)
#             if dp.iscanceled():
#                 break
#                 raise Exception("Canceled")
#     dp.close()
#     f.close()