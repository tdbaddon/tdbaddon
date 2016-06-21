# -*- coding: utf-8 -*-
from resources.lib.modules import client,webutils,control
from resources.lib.modules.log_utils import log
import re,urllib,json,time
import requests

def resolve(url):
	expires = int(control.setting('hrti_expire'))
	stream_token = control.setting('hrti_token')
	if expires - int(time.time())<0:
		stream_token,expires = getToken()
		if stream_token=='x':
			return ''
		control.set_setting('hrti_expire',expires)
		control.set_setting('hrti_token',stream_token)

	url += '&token=%s&token_expiration=%s|User-Agent=Mozilla/5.0'%(stream_token,expires)
	return url


	
# from resources.lib.resolvers import hrti
# token,expire = hrti.getToken()
# url = "https://prd-hrt.spectar.tv/player/get_smil/id/45388/video_id/45388/token/%s/asset_type/Movie/playlist_template/nginx/channel_name/hrvatski_kraljevi_raanje_kneevine_dokumentarna_serija_17_hd_/playlist.m3u8?foo=bar"%token
# xbmc.Player().play(url)

def getToken():
	username = control.setting('hrti_user')
	password = control.setting('hrti_pass')
	if username=='' or password=='':
		control.infoDialog('Unesite korisničko ime i lozinku za hrti.hr!')
		return 'x','x'
	session=requests.Session()
	headers={}
	cookies=session.cookies
	headers['cookies']=cookies
	headers['User-agent']=client.agent()
	uuid_url = 'https://hrti.hrt.hr/client_api.php/config/identify/format/json'
	resp_data = session.post(uuid_url, data = '{"application_publication_id":"all_in_one"}' , headers=headers).content
	data=json.loads(resp_data)

	uuid = data['uuid']
	
	put_data = '{"application_publication_id":"all_in_one","uuid":"%s","screen_height":1080,"screen_width":1920,"os":"Windows","os_version":"NT 4.0","device_model_string_id":"chrome 42.0.2311.135","application_version":"1.1"}'%uuid
	resp_data = session.put(uuid_url, data = put_data , headers=headers).text
	data=json.loads(resp_data)

	session_id = data['session_id']

	login_data = '{"username":"%s","password": "%s"}'%(username, password)
	login_url = 'https://hrti.hrt.hr/client_api.php/user/login/session_id/%s/format/json'%session_id
	resp = session.post(login_url, data = login_data, headers = headers)
	data = json.loads(resp.text)
	try:
		session_token = data['session_token']
	except:
		control.infoDialog('Provjerite korisničko ime i lozinku za hrti.hr!')
		return 'x','x'

	stream_token = data['secure_streaming_token']
	user_pin = data['pin_code']
	user_id = data['id']
	user_bitrate = int(data['bitrate'])
	subscriber_id = data['subscriber_id']
	external_id = data['external_id']
	first_name = data['first_name']
	last_name = data['last_name']

	str_token = stream_token.split('/')[0]
	expire = stream_token.split('/')[-1]
	return str_token,expire


def get_live():
	url = 'https://hrti-static.hrt.hr/rev-2c161c5/client_api.php/channel/all/application_id/all_in_one/instance_id/11/language/hr/format/json'
	data = json.loads(client.request(url))

def get_stream(id,external_id):
	url = 'https://prd-hrt-live.morescreens.com/{EXTERNAL_ID}/01.m3u8?video_id={ID}&authority_instance_id=spectar-prd-hrt&token={STREAM_TOKEN}&token_expiration={TOKEN_EXPIRE}|User-Agent=Mozilla/5.0'
	url = replace_values(id=id,external_id=external_id)
	return url
