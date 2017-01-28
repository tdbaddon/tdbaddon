import requests
from BeautifulSoup import BeautifulSoup as bs
import re
import urllib
import json
import xbmc,pickle
import cache,client,control,os
from log_utils import log
COOKIE = os.path.join(control.dataPath,'TVMcookies')

#login class & user specific methods
class MazeLogin():
	def log(self,msg):
		xbmc.log("### [TV Maze sync] - %s" % (msg.encode('utf-8'), ), level=xbmc.LOGNOTICE)


	def load_cookies(self):
		try:
			with open(COOKIE,'rb') as f:
				cookies = pickle.load(f)
				return cookies
		except:
			return False

	def login(self):
		#get session token
		self.log('Getting session token...')
		

		session = requests.Session()
		html = session.get(self.base_url).text
		self.token = bs(html).find('input',{'type':'hidden'})['value']
		control.set_setting('tvm_token',self.token)

		#login to tvmaze
		payload = {'_csrf': self.token,'LoginForm[password]':self.password,'LoginForm[username]':self.username,'LoginForm[rememberMe]':'0', 'LoginForm[rememberMe]':'1'}
		check = session.post(self.base_url, data=payload)
		check = ((check.text).encode('ascii','ignore'))
		if 'Unknown username/email' in check:
			self.log('Unknown username/email')
			self.login_error=True
			self.login_message='Unknown username/email'
		elif 'Incorrect password' in check:
			self.log('Incorrect password')
			self.login_error=True
			self.login_message='Incorrect password'
		else:
			self.login_error=False
			self.login_message='Logged in successfully'
			
		with open(COOKIE, 'wb') as f:
			pickle.dump(session.cookies, f)


	def get_session(self):
		session = requests.Session()
		cookies = self.load_cookies()
		session.headers.update({'X-CSRF-Token':control.setting('tvm_token')})

		if not cookies:
			self.login()
			session.cookies = self.load_cookies()
			session.headers.update({'X-CSRF-Token':control.setting('tvm_token')})
			return session

		session.cookies = cookies
		not_logged = 'Login | Keep track of your favorite shows' in session.get('http://www.tvmaze.com/dashboard').text
		if not_logged:
			self.login()
			session.headers.update({'X-CSRF-Token':control.setting('tvm_token')})
			session.cookies = self.load_cookies()
			return session
				
		return session



	#initial login, create login session
	#args: username, password -> tvmaze login information
	def __init__(self,username,password):
		self.username=username
		self.password=password
		self.followed_num=0
		self.updated_watched=0
		self.already_watched=0
		self.failed=0
		self.headers = {}
		self.base_url = 'http://www.tvmaze.com/site/login'
		self.token = control.setting('tvm_token')
		self.headers['X-CSRF-Token'] = self.token

		self.session = self.get_session()
		
		
		self.headers['User-agent']='TVMaze Kodi add-on'



	#follow/unfollow 
	#args: id -> tvmaze id of the item (either show,person,network or web channel)
	#kwargs: type (int/str 1,2,3 or 4 ) -> 1 for shows, 2 for people, 3 for networks, 4 for web_channels (default is 1)
	#returns: 0 if failed, 1 if item followed, -1 if item unfollowed
	def toggle_follow(self,id,type='1'):
		self.session = self.get_session()
		types=['http://www.tvmaze.com/follow/toggle?show_id=%s&widget=small','http://www.tvmaze.com/follow/toggle?person_id=%s&widget=small','http://www.tvmaze.com/follow/toggle?network_id=%s&widget=small','http://www.tvmaze.com/follow/toggle?webChannel_id=%s&widget=small']

		url=types[int(type)-1] % id
		#show_url='http://www.tvmaze.com/follow/toggle?show_id=%s&widget=small' %tvshow_id

		#post the follow
		follow = self.session.post(url,headers=self.headers).text
		if 'page not found' in follow.lower() or 'error occured' in follow.lower():
			self.log('Wrong post data or some other error. (404 Page Not Found)')
			return 0
		else:
			method=bs(follow).find('a')['title']

			if method == 'Click to follow':
				self.log ('Unfollowed show (id= %s)'%id)
				return -1
			elif method =='Click to unfollow':
				self.log('Followed show (id= %s)'%id)
				self.followed_num+=1
				return 1



	def rate_item(sell,id, rating, type):
		self.session = self.get_session()
		post = 'http://www.tvmaze.com/vote/vote?%s_id=%s'%(type,id)
		data = {'vote' : rating}
		self.session.post(post, data=data, headers=headers)


	#mark watched/unwatched
	#args : episode_id 
	#returns 0 if failed, 1 if marked as watched, -1 if marked as unwatched
	def toggle_episode_watch(self,episode_id):
		self.session = self.get_session()
		ep_url='http://www.tvmaze.com/watch/toggle?episode_id=%s&widget=small'%episode_id

		watched=self.session.post(ep_url,headers=self.headers).text

		if 'page not found' in watched.lower() or 'error occured' in watched.lower():
			self.log('Wrong post data or some other error. (404 Page Not Found)')
			return 0
		else:
			method=bs(watched).find('i')['class']
			if 'active' in method:
				self.log ('Marked episode as watched (id= %s)'%episode_id)
				return 1
			else :
				self.log('Marked episode as unwatched (id= %s)'%episode_id)
				return -1

	#check if user follows an item
	#args: id -> tvmaze id of the item
	#kwargs: type (int/str 1,2,3 or 4 ) -> 1 for shows, 2 for people, 3 for networks, 4 for web_channels (default is 1)
	#returns True if followed, False if not followed
	def isFollowed(self,id,type='1'):
		self.session = self.get_session()
		types=['http://www.tvmaze.com/follow/toggle?show_id=%s&widget=small','http://www.tvmaze.com/follow/toggle?person_id=%s&widget=small','http://www.tvmaze.com/follow/toggle?network_id=%s&widget=small','http://www.tvmaze.com/follow/toggle?webChannel_id=%s&widget=small']

		url=types[int(type)-1] % id
		#post the follow
		follow = self.session.post(url,headers=self.headers).text
		self.session.post(url,headers=self.headers)
		if method == 'Click to follow':
			self.log('isFollowed (%s) = True'%id)
			return True
		elif method =='Click to unfollow':
			self.log('isFollowed (%s) = False'%id)
			return False

	#check if user watched an episode
	#args: episode_id ->
	#returns True if watched, False if not watched
	def isWatched(self,episode_id):
		self.session = self.get_session()
		ep_url='http://www.tvmaze.com/watch/toggle?episode_id=%s&widget=small'%episode_id
		watched=self.session.post(ep_url,headers=self.headers).text
		method=bs(watched).find('i')['class']
		self.session.post(ep_url,headers=self.headers)
		if 'active' in method:
			self.log('isWatched (%s) = False'%episode_id)
			return False
		else :
			self.log('isWatched (%s) = True'%episode_id)
			return True

	#get url for ical .ics file (users personal calendar)
	#returns string url to the ics file, False if failed
	def get_calendar(self):
		self.session = self.get_session()
		url='http://www.tvmaze.com/dashboard/index'
		html=self.session.get(url).text
		try:
			ical_url=bs(html).find('div',{'id':'feed-panel'}).findAll('p')[1].find('a')['href']
			self.log('Calendar url:'+ ical_url)
			return ical_url
		except:
			return False


	#get list of followed items
	#args: type ->str 'shows', 'people', 'networks' or 'web_channels'
	#kwargs: sort -> sort method: 1 for 'Followed least recently', 2 for 'Followed most recently', 3 for 'A to Z' and 4 for 'Z to A'
	#returns array of tvmaze ids
	def getFollowed(self,type,sort='1'):
		self.session = self.get_session()
		url='http://www.tvmaze.com/dashboard/follows?sort=%s'%sort
		html=self.session.get(url).text
		tags=bs(html).find('div',{'id':'follow-list'})
		if type=='shows':
			reg='show_id=(\d+)'
		elif type=='people':
			reg='/people/(\d+)/'
		elif type=='networks':
			reg='/networks/(\d+)/'
		elif type=='web_channels':
			reg='/webchannels/(\d+)/'

		items=re.compile(reg).findall(str(tags))
		return items
		

	#get list of unwatched episodes for show
	#args: tvshow_id -> tvmaze id for a wanted show
	#returns an array of tvmaze episode ids
	def get_unwatched_episodes(self,tvshow_id):
		self.session = self.get_session()
		url='http://www.tvmaze.com/watch/show?show_id=%s'%tvshow_id
		html=self.session.get(url).text
		items=bs(html).find('div',{'class':'watch-list'}).find('tbody').findAll('tr')
		for item in items:
			watchstate=item.find('i')['class']
			if 'active' not in watchstate:
				id=item['data-key']
				ids+=[id]
		return ids


	def mark_watched(self,show,season,episod):
		self.session = self.get_session()
		try:
			import cache
			meta=Metadata(show,season=season,episode=episod)
			
			show_id,meta=cache.get(meta.get_single_show,480,show)
			
			

			episodes=cache.get(meta.get_episodes,24,show_id)
			for episode in episodes:
				if str(episode['season']).lstrip('0')==str(season) and str(episode['number']).lstrip('0')==str(episod):
					ep_id=episode['id']
					break

			if not cache.get(self.isWatched,24,ep_id):
				self.log('Episode %s is not watched, setting it to watched.'%ep_id)
				a=self.toggle_episode_watch(ep_id)
				self.updated_watched+=1
				return a
			else:
				self.already_watched+=1
				self.log('Episode %s already watched, pass...'%ep_id)
				return 1
		except:
			self.failed+=1
			return 0

	def mark_watched_scrobble(self,show,season,episod,imdb=None):

		#try:
			self.session = self.get_session()
			meta=Metadata(show,season=season,episode=episod)
			
			show_id,metas=meta.get_single_show(show,imdb=imdb)
			
			
			ep_id = meta.get_single_episode(show_id,season,episod)['id']
			

			if not self.isWatched(ep_id):
				self.log('Episode %s is not watched, setting it to watched.'%ep_id)
				a = self.toggle_episode_watch(ep_id)
				return a
			else:
				self.log('Episode %s already watched, pass...'%ep_id)		
				return True
		#except:
		#	return 0

	


class Metadata():
	def __init__(self,tvshow,maze_id='', season='', episode='',tvdbid='',tvrageid=''):
		self.tvshow=tvshow
		self.id=maze_id
		self.season=season
		self.episode=episode
		self.tvdb=tvdbid
		self.tvrage=tvrageid
		self.base_url='http://api.tvmaze.com'

	

	def get_meta_show(self):

		if self.id !='':
			url=self.base_url + '/shows/%s?embed=cast'
			html=read_url(url)
			dict=json.loads(html)
			tvshowtitle,type,language,genres,status,runtime=dict['name'],dict['type'],dict['language'],dict['genres'],dict['status'],dict['runtime']
			premiered,rating,network=dict['premiered'],dict['rating']['average'],dict['network']['name']
			tvrage,tvdb,imdb=dict['externals']['tvrage'],dict['externals']['thetvdb'],dict['externals']['imdb']
			thumb_med,thumb_big=dict['image']['medium'],dict['image']['original']
			summary=dict['summary']
			
	def get_single_show(self,show,imdb=None):
		if not imdb or imdb=='':
			url=self.base_url + '/singlesearch/shows?q=%s&embed[]=episodes&embed[]=cast'%(urllib.quote(show))
		else:
			log('Using imdb')
			import client
			url = self.base_url + '/lookup/shows?imdb=%s'%imdb
			url = client.request(url,output='geturl')

			url += '?embed[]=episodes&embed[]=cast'


		html=read_url(url)
		dict=json.loads(html)
		id,name,type,language,genres=dict['id'],dict['name'],dict['type'],dict['language'],dict['genres']
		status,runtime,premiered,rating,network=dict['status'],dict['runtime'],dict['premiered'],dict['rating']['average'],dict['network']['name']
		tvrage,tvdb,imdb=dict['externals']['tvrage'],dict['externals']['thetvdb'],dict['externals']['imdb']
		thumb_med,thumb_big=dict['image']['medium'],dict['image']['original']
		summary=dict['summary']
		persons=dict['_embedded']['cast']
		cast=[]
		for person in persons:
			name=person['person']['name']
			char=person['character']
			cast+=[(name,char)]
		meta={}
		meta['genre'],meta['castandrole'],meta['rating']=','.join(genres),cast,rating
		meta['plot'],meta['plotoutline'],meta['title'],meta['originaltitle'],meta['sorttitle'] =summary,summary,name,name,name
		meta['status'],meta['tvshowtitle'],meta['premiered']=status,name,premiered
		meta['thumbnail'],meta['thumbnail_big']=thumb_med,thumb_big

		return str(id),meta

	def get_single_episode(self,show_id,season,number):
		url = self.base_url + '/shows/%s/episodebynumber?season=%s&number=%s'%(show_id,season,number)
		html=read_url(url)
		dict=json.loads(html)
		return dict

	def get_episodes(self,show_id):
		url= self.base_url + '/shows/%s?embed=episodes'%show_id
		html=read_url(url)
		dict=json.loads(html)
		episodes=dict['_embedded']['episodes']
		return episodes

def read_url(url):
    return client.request(url)
