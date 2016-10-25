# -*- coding: utf-8 -*-



import re,urlparse,json,urllib2
from resources.lib.modules import client

def resolve(link):
 
		req = urllib2.Request("http://45.62.245.50/arconai.php?u="+link, None, useragent)
	try:
		html = urllib2.urlopen(req).read()
	except urllib2.HTTPError, e:
		xbmc.log(html)
		xbmc.log(str(e))
	return html
	except:
        return

