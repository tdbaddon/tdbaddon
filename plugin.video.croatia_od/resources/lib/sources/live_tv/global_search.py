# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from resources.lib.modules import control,mb_resolvers
from resources.lib.modules.log_utils import log
import sys,os,xbmc,urllib,urllib2,json

AddonPath = control.addonPath
IconPath = AddonPath + "/resources/media/"
def icon_path(filename):
    return os.path.join(IconPath, filename)

class info():
    def __init__(self):
    	self.mode = 'global_search'
        self.name = 'Pretraga kanala'
        self.icon = 'search.png'
        self.paginated = False
        self.categorized = False
        self.multilink = False

class main():
	def __init__(self,url = ''):
		self.base = ''
		self.url = url

	def channels(self):
		out = []
		keyboard = xbmc.Keyboard('', 'Pretraži TV kanale', False)
		keyboard.doModal()
		if keyboard.isConfirmed():
			query = keyboard.getText()
			out = self.get_results(query)
			
		return out

	def get_results(self,query):


		global c_url
		global c_data
		global c_headers
		global results
		
		#c_url = "https://api.mobdro.sx/streambot/v3/search"
		c_url = "https://api.mobdro.sx/streambot/v4/search"
		c_headers = {"User-Agent":"Mobdro/5.0", "Referer":"api.mobdro.sx"}
		#c_data = {'query':term,'parental':0,'languages':'[]','alphabetical':0,'token':'XNZSGC]FSUQ]YP]D','signature':'1083937564'}
		c_data = {'query':query,'parental':0,'languages':'[]','alphabetical':0,'token':self.gettoken()}
		c_data = urllib.urlencode(c_data)
	    
	    # Fetch channel list
		req = urllib2.Request(c_url, c_data, c_headers)
		response = urllib2.urlopen(req)
		response = response.read()
		
		results = json.loads(response)
		results = self.edit_results(results)

		return results


	def edit_results(self,results):
		out = []
		supported_sites = ["url", "youtube", "biggestplayer", "relayer", "veetle", "vaughnlive", "rtmpdump", "filmon", "ustream", "livestream", "twitch", "iliveto"]
		for result in results:
			for site in supported_sites:
				tr = result.get(site,None)
				if not tr:
					continue
				if result[site]:
					
					if site == "rtmpdump":
						if not result[site].get('rtmp',None):
							continue

						rtmp = result[site]['rtmp']
						for key in result[site].keys():
							if result[site][key]:
								rtmp +=' %s=%s'%(key,result[site][key])
						url = rtmp
						title = result['name']
						img = result['img']
						out.append((url,title,img))
					else:
						item_data = {
                             "type":site,
                             "data":result[site]
                		}
                		
						title = result['name']
						img = result['img']
						url = mb_resolvers.resolve(item_data)
						out.append((url,title,img))
		return out






	def gettoken(self):
	    atime=control.setting("authtime")
	    currentauth=control.setting("currentauth")
	    refreshtoken=True
	    import time
	    now=time.time()
	    try:
	        if not currentauth==""  and not atime=="" and now-float(atime)<(2*60*60): #2 hours
	            return currentauth
	    except: pass
	    if refreshtoken:
	        c_url = "https://api.mobdro.sx/utils/auth"
	        c_headers = {"User-Agent":"Dalvik/1.6.0 (Linux; U; Android 4.2.2;)"}
	        c_data = {'signature':"577195216"}
	        c_data = urllib.urlencode(c_data)
	        # Fetch channel list
	        req = urllib2.Request(c_url, c_data, c_headers)
	        response = urllib2.urlopen(req)
	        response = response.read()
	        results = json.loads(response)
	        token=results["token"]


	        control.set_setting("authtime",str(now))
	        control.set_setting("currentauth",token)
	        return token

	def resolve(self,url):
		import liveresolver
		return liveresolver.resolve(url)
	


	
