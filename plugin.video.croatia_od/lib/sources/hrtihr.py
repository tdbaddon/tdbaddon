# -*- coding: utf-8 -*-

from lib.modules.webutils import *
import requests,json,uuid

class hrtiLogin():
    def __init__(self,username,password,bitrate):
        self.username=username
        self.password=password
        self.session=requests.Session()
        self.headers={}
        self.cookies=self.session.cookies
        self.headers['cookies']=self.cookies
        self.headers['User-agent']='Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36 OPR/33.0.1990.35 (Edition beta)'
        uuid_url = 'https://hrti.hrt.hr/client_api.php/config/identify/format/json'
        resp_data = self.session.post(uuid_url, data = '{"application_publication_id":"all_in_one"}' , headers=self.headers).content
        data=json.loads(resp_data)
        self.uuid = data['uuid']
        put_data = '{"application_publication_id":"all_in_one","uuid":"%s","screen_height":1080,"screen_width":1920,"os":"Windows","os_version":"NT 4.0","device_model_string_id":"chrome 42.0.2311.135","application_version":"1.1"}'%self.uuid
        resp_data = self.session.put(uuid_url, data = put_data , headers=self.headers).text
        data=json.loads(resp_data)
        self.session_id = data['session_id']
        self.local_bitrate = bitrate
        self.doLogin()
        # if self.local_bitrate != self.user_bitrate:
        #     self.changeBitrate()

    def doLogin(self):
        self.login_data = '{"username":"%s","password": "%s"}'%(self.username, self.password)
        self.login_url = 'https://hrti.hrt.hr/client_api.php/user/login/session_id/%s/format/json'%self.session_id
        resp = self.session.post(self.login_url, data = self.login_data, headers = self.headers)
        data = json.loads(resp.text)
        self.session_token = data['session_token']
        self.stream_token = data['secure_streaming_token']
        self.user_pin = data['pin_code']
        self.user_id = data['id']
        self.user_bitrate = int(data['bitrate'])
        self.subscriber_id = data['subscriber_id']
        self.external_id = data['external_id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']


    def changeBitrate(self):
        bitrate_url='https://hrti.hrt.hr/client_api.php/user/update/session_id/%s/access_token/%s/format/json'%(self.session_id,self.access_token)
        a=self.session.put(bitrate_url, data='{"bitrate" : "%s" }'%self.local_bitrate, headers=self.headers)



