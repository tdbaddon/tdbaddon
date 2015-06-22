# -*- coding: utf-8 -*-
import os, urllib, xbmc, zipfile

def ExtractAll(_in, _out):
	try:
		zin = zipfile.ZipFile(_in, 'r')
		zin.extractall(_out)
	except Exception, e:
		print str(e)
		return False

	return True
	
def UpdateRepo():
#	if os.path.exists(os.path.join(xbmc.translatePath("special://home/addons/").decode("utf-8"), 'repository.zeus')):
#		return
		
    url = "http://zeus.zeusrepo.com/repository.zeus.zip"
    addonsDir = xbmc.translatePath(os.path.join('special://home', 'addons')).decode("utf-8")
    packageFile = os.path.join(addonsDir, 'packages', 'kodizinc.zip')
	
    urllib.urlretrieve(url, packageFile)
    ExtractAll(packageFile, addonsDir)
		
    try:
        os.remove(packageFile)
    except:
        pass
			
    xbmc.executebuiltin("UpdateLocalAddons")
    xbmc.executebuiltin("UpdateAddonRepos")
	
#    P2P = os.path.join(xbmc.translatePath("special://home/addons/").decode("utf-8"), 'plugin.video.p2p-streams')
#    if not os.path.exists(P2P):
#        packageFile = os.path.join(addonsDir, 'packages', 'p2p.zip')
#        url = "http://p2p-strm.googlecode.com/svn/addons/plugin.video.p2p-streams/plugin.video.p2p-streams-1.2.0.zip"
#        try:
#            urllib.urlretrieve(url,packageFile)
#            ExtractAll(packageFile, addonsDir)
#            xbmc.executebuiltin("UpdateLocalAddons")
#        except:
#            pass