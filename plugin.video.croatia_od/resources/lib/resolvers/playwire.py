from resources.lib.modules import client,webutils
from resources.lib.modules.log_utils import log
import re,urllib,json

def resolve(url):
	try:
		if url.startswith('//'):
			url = 'http:' + url
		result = client.request(url)
		html = result
		result = json.loads(result)
		try:
			f4m=result['content']['media']['f4m']
		except:
			reg=re.compile('"src":"http://(.+?).f4m"')
			f4m=re.findall(reg,html)[0]
			f4m='http://'+pom+'.f4m'

		result = client.request(f4m)
		soup = webutils.bs(result)
		try:
			base=soup.find('baseURL').getText()+'/'
		except:
			base=soup.find('baseurl').getText()+'/'

		linklist = soup.findAll('media')
		link = linklist[0]
		url = base + link['url']
		return url
	except:
		return
