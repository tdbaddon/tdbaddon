from __future__ import unicode_literals
from resources.lib.modules import client
import re,sys,xbmcgui,os
from addon.common.addon import Addon
addon = Addon('plugin.video.castaway', sys.argv)

AddonPath = addon.get_path()
IconPath = AddonPath + "/resources/media/"
def icon_path(filename):
    return os.path.join(IconPath, filename)

class info():
    def __init__(self):
    	self.mode = 'lmshows'
        self.name = 'LMShows.com'
        self.icon = 'lmshows.jpg'
        self.paginated = False
        self.categorized = False
        self.multilink = False
class main():
    def __init__(self):
        self.base = 'http://lmshows.se/'
        
    def channels(self):
        html = client.request(self.base)
        channels = re.findall('<li><a href="(.+?)" title="(.+?)" >.+?</a></li>',html)
        events = []
        unwanted = ['House','90\'s Hits','Trance','Vocal Trance','PsyTrance','Progressive','Top Hits','Love Music','Rain Sounds','Pacman','Koutack','Duck Hunt','Tic Tac Toe','Silversphere','Heat Rush USA','Sift Renegade 3 Defiance',
        'Super Mario Flash','Billards Master Pro','Super Mario Flash 2','Strike Force Heroes 2','Big Time Butter Baron']
        for c in channels:
            if c[0]=='#' or c[1] in unwanted:
                continue
            url = self.base + c[0]  
            title = c[1]
            events.append((url,title,icon_path(info().icon)))
        events=list(set(events))
        events.sort(key=lambda x: x[1])
        return events
        
    def resolve(self,url):
        import liveresolver
        return liveresolver.resolve(url,cache_timeout=0)