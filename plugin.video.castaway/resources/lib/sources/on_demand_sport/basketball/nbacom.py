from __future__ import unicode_literals
from resources.lib.modules import client,webutils
import re,urlparse,json, datetime, sys, os, time
from addon.common.addon import Addon

addon = Addon('plugin.video.castaway', sys.argv)

AddonPath = addon.get_path()
IconPath = AddonPath + "/resources/media/"
def icon_path(filename):
    return os.path.join(IconPath, filename)


class info():
    def __init__(self):
    	self.mode = 'nbacom'
        self.name = 'nba.com'
        self.icon = 'nbacom.jpeg'
        self.paginated = True
        self.categorized = True
        self.multilink = False


class main():
	def __init__(self,url = 'http://nbahd.com'):
		self.base = 'http://nbahd.com'
		self.url = url

	def categories(self):
		categs=[['http://searchapp2.nba.com/nba-search/query.jsp?section=channels%2F*%7Cgames%2F*%7Cflip_video_diaries%7Cfiba&sort=recent&hide=true&type=advvideo&npp=15&start=1','NBA Video (All feeds)',icon_path(info().icon)],
		['http://searchapp2.nba.com/nba-search/query.jsp?section=channels%2Ftop_plays&sort=recent&hide=true&type=advvideo&npp=15&start=1','Top Plays',icon_path(info().icon)],
		['http://searchapp2.nba.com/nba-search/query.jsp?section=games%2F*%7Cchannels%2Fplayoffs&sort=recent&hide=true&type=advvideo&npp=15&start=1','Highlights',icon_path(info().icon)]]
		return categs

	def items(self):
		html=client.request(self.url)
		textarea = client.parseDOM(html, "textarea", attrs = { "id": "jsCode" })[0]
		content = textarea.replace("\\'","\\\\'").replace('\\\\"','\\\\\\"').replace('\\n','').replace('\\t','').replace('\\x','')
		query = json.loads(content)
		results = query['results'][0]
		items=[]
		for i in range(len(results)):
			link='http://www.nba.com/video/' + results[i]['id'].replace('/video','')+'.xml'
			print(results[i]['metadata']['media'])
			mediaDateUts = time.ctime(float(results[i]['mediaDateUts']))
			date = datetime.datetime.fromtimestamp(time.mktime(time.strptime(mediaDateUts, '%a %b %d %H:%M:%S %Y'))).strftime('%d.%m.%Y')
			title=results[i]['title']
			thumb=results[i]['metadata']['media']['600x336']['uri']
			length=results[i]['metadata']['video']['length']
			desc=results[i]['metadata']['media']['excerpt']

			title=title+' ( %s )'%date
			items+=[(title,link,thumb)]
		return items

	def resolve(self, link):
	    link=link.replace('/index.html','')
	    soup = webutils.get_soup(link)
	    bitrate = addon.get_setting('nba_bitrate')
	    link=soup.find('file',{'bitrate':'%s'%bitrate}).getText()
	    return link




	def next_page(self):
		current = re.findall("start=(\d+)",self.url)[0]
		link = self.url.replace("start=%s"%current,"start=")
		next = str(int(current)+15)
		next_page = link + next
		return next_page


