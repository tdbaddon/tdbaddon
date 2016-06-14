from resources.lib.modules import client,decryptionUtils
from resources.lib.modules.log_utils import log
import re,urllib,urlparse

def resolve(url):
	try:
		try:
			referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
		except:
			referer=url
		out=[]
		html = client.request(url,referer=referer)
		html = decryptionUtils.doDemystify(html)
		url = re.findall('\{file:\s*[\"\']([^\"\']+)',html)[0]
		return url
	except:
		return 
