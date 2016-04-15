from lib.modules.webutils import *
from live_tv import *
import re
import requests


def get_all_channels_serbiaplus():
	base_url = 'http://www.serbiaplus.com'
	url = base_url + '/menu1.html'
	html = read_url(url)
	regex = re.compile('<a href="(.+?)" target="_blank"><img src="(.+?)" width=".+?" height=".+?"')
	links = re.findall(regex,html)
	return links



