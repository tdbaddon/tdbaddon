from resources.lib.modules import client,webutils,convert
import re,sys,xbmcgui
from addon.common.addon import Addon
from resources.lib.modules.log_utils import log

addon = Addon('plugin.video.castaway', sys.argv)

class info():
    def __init__(self):
        self.mode = 'vipbox'
        self.name = 'Vipleague.me'
        self.icon = 'vipbox.png'
        self.categorized = True
        self.paginated = False
        self.multilink = True

class main():
    def __init__(self):
        self.base = 'http://www.vipleague.me'        

    def links(self,url):
        result = client.request(url)
        ls = client.parseDOM(result, 'div', attrs={'class':'linkRow'})
        links = self.__prepare_links(ls)
        return links

    def events(self,url):
        result = client.request(url)
        result = convert.unescape(result.decode('utf-8'))
        reg = re.compile('(<h1 class="leagues".+?align="left"[^>]*>\s*<a([^>]*)>\s*<span class="[^"]+ ([^"]*)">[^>]*><span gday="[^"]*" class="matchtime">([\d:]*)</span>\s*([^<]+)\s*</a>\s*</h1>)')
        events = re.findall(reg,result)
        events = self.__prepare_events(events)
        return events

    def categories(self):
        soup = webutils.get_soup(self.base)
        cats = soup.find('table',{'class':'menuTable'}).findAll('td')
        categories = self.__prepare_cats(cats)
        return categories


    def __prepare_cats(self,cats):
        out = [('http://www.vipleague.me/live-now.html','[B]Live Now[/B]','live.png')]
        for cat in cats:
            try:
                id = cat.find('a')['href']
                url = self.base + id
                id = self.__checkID(id)
                title = cat.getText()
                img = 'icons/%s.png'%id
                out.append((url,title,img))
            except:
                pass

        return out

    def __checkID(self,id):
        id = id.replace('-','_').replace('/sports/','').replace('.html','')
        if id in ['formula_1','moto_gp','motorsports']:
            return 'f1'
        if id in ['ufc','wwe','boxing']:
            return 'fighting'
        if id == 'aussie_rules':
            return 'rugby'
        if id == 'football':
            return 'soccer'
        if id == 'american_football':
            return 'football'
        if id =='ice_hockey':
            return 'hockey'
        if id=='water_sports':
            return 'waterpolo'
        if id=='winter_sports':
            return 'skiing'
        if id =='http://www.strikeout.co':
            return 'baseball'
        if id =='http://www.homerun.re':
            return 'cricket'

        else:
            return id

    @staticmethod
    def convert_time(time):
        
        li = time.split(':')
        hour,minute=li[0],li[1]
        
        import datetime
        from resources.lib.modules import pytzimp
        d = pytzimp.timezone(str(pytzimp.timezone('Europe/London'))).localize(datetime.datetime(2000 , 1, 1, hour=int(hour), minute=int(minute)))
        timezona= addon.get_setting('timezone_new')
        my_location=pytzimp.timezone(pytzimp.all_timezones[int(timezona)])
        convertido=d.astimezone(my_location)
        fmt = "%H:%M"
        time=convertido.strftime(fmt)
        return time

    def __prepare_events(self,events):
        new = []
        for event in events:
            url = re.findall('href="(.+?)"',event[1])[0]
            sport = event[2]
            title = re.findall('class="matchtime">.+?</span>\s*([^<]+)\s*</a>\s*</h1>',event[0])[0]
            time = self.convert_time(event[3])
            title = '[COLOR orange](%s)[/COLOR] (%s) [B]%s[/B]'%(time,sport,title)
            new.append((url,title.encode('utf-8', 'xmlcharrefreplace')))
        
        return new

    
    def __prepare_links(self,rows):
        new=[]
        precheck = addon.get_setting('link_precheck')
        if precheck=='true':
            pDialog = xbmcgui.DialogProgress()
            pDialog.create('Checking links', 'Checking links...')
        for row in rows:
            pl_name = client.parseDOM(row, 'div', attrs={'class':'playerName'})[0]
            pl_name = re.sub('<[^<]+?>', '', pl_name)
            links = client.parseDOM(row, 'div', attrs={'class':'gameLinks'})[0]
            names = client.parseDOM(links,'a')
            urls = client.parseDOM(links,'a', ret='href')
            events = client.parseDOM(links,'a', ret='title')
            for i in range(len(urls)):
                url = self.base + urls[i]
                evento = events[i]
                ln_num = names[i]
                title = "%s %s (%s)"%(evento, ln_num, pl_name)
                if not 'bet' in pl_name.lower():
                    new.append((url,title))

        return new

    def resolve(self,url):
        import liveresolver
        return liveresolver.resolve(url,cache_timeout=0)