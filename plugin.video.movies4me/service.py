'''
author: kinkin
'''

import time,datetime
import xbmc
import xbmcaddon
import settings
from datetime import date, timedelta
ADDON = settings.addon()

class AutoUpdater:             
    def runProgram(self):
        self.last_run = 0
        while not xbmc.abortRequested:
            if settings.enable_subscriptions():
                try:
                    next_run  = datetime.datetime.fromtimestamp(time.mktime(time.strptime(ADDON.getSetting('service_time').encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S")))
                    now = datetime.datetime.now()
                    if now > next_run:
                        xbmc.executebuiltin('RunPlugin(plugin://plugin.video.movies4me/?name=service&url=service&mode=155&list=service)')
                except:
                    pass
            xbmc.sleep(1000)


xbmc.log("[Movies4ME] Cleaning cache...")
AutoUpdater().runProgram()
