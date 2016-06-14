from resources.lib.modules import client
from resources.lib.modules.log_utils import log
import re,urllib,urlparse

def resolve(url):
	try:
		html = client.request(url)
		url2 = client.parseDOM(html,'iframe',ret='src')[0]
		html = client.request(url2)
		video = re.findall('file:[\"\'](.+?)[\"\']',html)[0]
		video+='|%s' %urllib.urlencode({'User-agent':client.agent(),'Referer':url2})
		return video
	except:
		return []
