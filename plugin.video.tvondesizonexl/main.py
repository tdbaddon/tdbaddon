'''
Created on Nov 24, 2013

@author: ajju
'''
from xoze.lib.jsonrpclib.jsonrpc import Server
import logging
import sys

try:
    if len(sys.argv) >= 3:
        from xoze.utils import http
        sysParams = str(sys.argv[2])
        logging.getLogger().debug('Found params %s' % sysParams)
        params = http.parse_url_params(sysParams)
        videoLink = params['videoLink']
        logging.getLogger().debug(videoLink)
        client = Server('http://localhost:%d/TVonDESIZONE' % 11421)
        response = client.resolveStream(videoLink=videoLink)
        logging.getLogger().debug(response)
        if response['status'] == 'success':
            logging.getLogger().debug(response['streamLink'])
            import xbmcgui, xbmcplugin  # @UnresolvedImport
            xbmcplugin.setResolvedUrl(int(sys.argv[ 1 ]), True, xbmcgui.ListItem(path=response['streamLink']))
        elif response['status'] == 'exception':
            logging.getLogger().error(response['message'])
        
    else:
        from xoze.context import AddonContext
        addon_context = AddonContext(addon_id='plugin.video.tvondesizonexl', conf={'contextFiles':['actions.xml', 'dr_actions.xml', 'dtb_actions.xml'], 'webServiceEnabled':True, 'webServicePath':'/TVonDESIZONE', 'webServicePort':11421})
        import xbmc #@UnresolvedImport
        xbmc.executebuiltin('Dialog.Close(busydialog)')
        addon_context.get_current_addon().get_action_controller().do_action('start')
        addon_context.do_clean()
        del addon_context
except Exception, e:
    logging.getLogger().exception(e)
    raise e
