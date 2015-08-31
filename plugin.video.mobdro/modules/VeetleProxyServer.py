import urllib2
import xbmc, xbmcaddon, xbmcplugin, xbmcgui
import plugintools
#import akamaiSecureHD

addon = xbmcaddon.Addon()
akamaiProxyServer = xbmc.translatePath(addon.getAddonInfo('path') + "/modules/akamaiSecureHD.py")

def getUrl(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/13.0')
    response = urllib2.urlopen(req, timeout=30)
    link = response.read()
    response.close()
    return link

def run():
    try:
        #plugintools.log('Checking proxy server...')
        getUrl("http://127.0.0.1:64653/version")
        proxyIsRunning = False
        #plugintools.log('Proxy server is running')
    except:
        proxyIsRunning = False
        #plugintools.log('Proxy server is not running')
    if not proxyIsRunning:
        #plugintools.log('Starting proxy server...')
        #plugintools.log(akamaiProxyServer)
        #akamaiSecureHD.server_start()
        xbmc.executebuiltin('RunScript(' + akamaiProxyServer + ')')
        #plugintools.log('Proxy server started')
