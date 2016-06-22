from resources.lib.modules import client,webutils
import re,sys,xbmcgui,os
from addon.common.addon import Addon
addon = Addon('plugin.video.castaway', sys.argv)

AddonPath = addon.get_path()
IconPath = AddonPath + "/resources/media/"
def icon_path(filename):
    return os.path.join(IconPath, filename)

class info():
    def __init__(self):
        self.mode = 'arenavision'
        self.name = 'Arenavision.in'
        self.icon = icon_path('av.jpg')
        self.categorized = False
        self.paginated = False
        self.multilink = True

class main():
    def __init__(self):
        self.base = 'http://arenavision.in' 
        self.headers = { "Cookie" : "beget=begetok; has_js=1;" }       

    def links(self,url):
        links = url.strip('/').split('/')
        links=self.__prepare_links(links)
        return links

    def channels(self):
        import requests
        
        result = client.request('http://arenavision.in/agenda', headers=self.headers)
        match = re.findall('Bruselas(.*?)</footer>', result, re.DOTALL)[0]
        events = re.findall('(\d+/\d+/\d+)\s*(\d+:\d+)\s*CET\s*(.+?)\s*\((.+?)\)(.+?)<',match)
        events = self.__prepare_events(events)
        return events
    

    @staticmethod
    def convert_time(time,date):
        li = time.split(':')
        li2 = date.split('/')
        hour,minute=li[0],li[1]
        day,month,year = li2[0],li2[1],li2[2]
        import datetime
        from resources.lib.modules import pytzimp
        d = pytzimp.timezone(str(pytzimp.timezone('Europe/Ljubljana'))).localize(datetime.datetime(2000 + int(year), int(month), int(day), hour=int(hour), minute=int(minute)))
        timezona= addon.get_setting('timezone_new')
        my_location=pytzimp.timezone(pytzimp.all_timezones[int(timezona)])
        convertido=d.astimezone(my_location)
        fmt = "%A, %B %d, %Y"
        fm2 = "%H:%M"
        time=convertido.strftime(fmt)
        tm = convertido.strftime(fm2)
        return tm,time

    

    def __prepare_events(self,events):
        new = []
        date_old = ''
        for event in events:
            try:
                date,time,title,sport,url = event
                time, date = self.convert_time(time,date)
                if date != date_old:
                    date_old = date
                    new.append(('x','[COLOR yellow]%s[/COLOR]'%date, info().icon))
                    continue
                
                title = '[COLOR orange](%s)[/COLOR] (%s) [B]%s[/B]'%(time,sport,title)
                title = title.encode('utf-8')
                new.append((url,title, info().icon))
            except:
                pass
        
        return new

    def __prepare_links(self,links):
        new=[]        
        
        for link in links:
            url = self.base + '/' + link.lower()
            title = link
            new.append((url,title))
        return new