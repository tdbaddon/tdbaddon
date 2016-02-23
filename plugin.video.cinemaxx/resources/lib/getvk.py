#------------------------------------------------------------
#
# based on getvk.py
# by Ivo Brhel, vdo < vdo.pure at gmail.com >
# https://code.google.com/p/getvk/
#
#------------------------------------------------------------

import re

def getVkVideos(html):
	html = html.replace('amp;', '')
	
	vars = dict.fromkeys(['video_host', 'video_uid', 'video_vtag'])
	
	for var in vars.iterkeys():
		value = re.search(var + r' ?= ?[\'"](.+?)[\'"]', html)
		if not value: return
		vars[var] = value.group(1).strip()
	
	vars['video_host'] = formatUrl(vars['video_host'])
	
	video_urls = []
	
	regex = r'(' + vars['video_vtag'] + '\.([240|360|480|720|1080]+)\.mp4)'
	match = re.compile(regex, re.DOTALL).findall(html)
	match = sorted(list(set(match)))
	if len(match) > 0:
		for quality in match:
			name = "[vk.com] %sp" % (quality[1])
			url = "%s/u%s/videos/%s" % (vars['video_host'], vars['video_uid'], quality[0])
			video_urls.append([name, url])
	
	match = re.search(r'video_no_flv = [\'"](.+?)[\'"];', html)
	noflv = match.group(1).strip() if match else ""
	
	if noflv == "0" and vars['video_uid'] != "0":
		name = "[vk.com] FLV"
		url = "%s/u%s/videos/%s.flv" % (vars['video_host'], vars['video_uid'], vars['video_vtag'])
		video_urls[0:0] = [[name, url]]
	
	elif vars['video_uid'] == "0":
		match = re.search(r'vkid=([^\&]+)\&', html)
		if match:
			vkid = match.group(1).strip()
			url = "%s/assets/videos/%s%s.vk.flv" % (vars['video_host'], vars['video_tag'], vkid)
			video_urls[0:0] = [["[vk.com] FLV", url]]
	
	return video_urls


def formatUrl(url):
	if not url.startswith('http'):
		url = url + 'http://'
	if url.endswith('/'):
		url = url[:-1]
	return url
