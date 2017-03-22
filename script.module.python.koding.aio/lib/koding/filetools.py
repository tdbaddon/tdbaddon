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

def Extract(_in, _out, dp=None):
# Extract a zipfile, possibly add rar,7z and tar compatibility    
    import zipfile
    import xbmc

    if zipfile.is_zipfile(_in):
        zin = zipfile.ZipFile(_in,  'r')
        if dp:
            nFiles = float(len(zin.infolist()))
            count  = 0

            try:
                for item in zin.infolist():
                    count += 1
                    update = count / nFiles * 100
                    dp.update(int(update))
                    zin.extract(item, _out)
                return True

            except Exception, e:
                xbmc.log('Extraction Failed: %s'%str(e))
                return False
        else:
            try:
                zin.extractall(_out)
                return True
            except Exception, e:
                xbmc.log('Extraction Failed: %s'%str(e))
                return False
    else:
        xbmc.log('NOT A VALID ZIP FILE: %s' % _in)
#----------------------------------------------------------------
