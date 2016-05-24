import urllib2
import json
import re, os, cookielib
import simplejson as json
import xbmc, xbmcgui
from addon.common.net import Net
from addon.common.addon import Addon
net = Net()
addon = Addon('plugin.video.icefilms')


CLIENT_ID = 'V24WI7BW2OHJW'
USER_AGENT = 'Icefilms for Kodi/%s' % (addon.get_version())
INTERVALS = 5

class RealDebrid:

    def __init__(self):
        self.hosters = None
        self.hosts = None
        self.headers = {'User-Agent': USER_AGENT}

    def get_media_url(self, host_link, retry=False):
        try:
            dialog = xbmcgui.DialogProgress()
            dialog.create('Resolving', 'Resolving Link Using Real-Debrid...')       
            dialog.update(0)
            
            url = 'https://api.real-debrid.com/rest/1.0/unrestrict/link'
            headers = self.headers
            headers['Authorization'] = 'Bearer %s' % (addon.get_setting('realdebrid_token'))
            data = {'link': host_link}
            result = net.http_POST(url, form_data=data, headers=headers).content
            dialog.update(100)
        except urllib2.HTTPError as e:
            if not retry and e.code == 401:
                if addon.get_setting('realdebrid_refresh'):
                    self.refresh_token()
                    return self.get_media_url(host_link, retry=True)
                else:
                    addon.set_setting('realdebrid_client_id', '')
                    addon.set_setting('realdebrid_client_secret', '')
                    addon.set_setting('realdebrid_token', '')
                    raise Exception('Real Debrid Auth Failed & No Refresh Token')
            else:
                try:
                    js_result = json.loads(e.read())
                    if 'error' in js_result:
                        msg = js_result['error']
                    else:
                        msg = 'Unknown Error (1)'
                except:
                    msg = 'Unknown Error (2)'
                raise Exception('Real Debrid Error: %s (%s)' % (msg, e.code))
        except Exception as e:
            raise Exception('Unexpected Exception during RD Unrestrict: %s' % (e))
        else:
            js_result = json.loads(result)
            links = []
            link = self.__get_link(js_result)
            if link is not None: links.append(link)
            if 'alternative' in js_result:
                for alt in js_result['alternative']:
                    link = self.__get_link(alt)
                    if link is not None: links.append(link)
                    
            if len(links) == 1 or addon.get_setting('realdebrid_autopick') == 'true':
                return links[0][1]
            elif len(links) > 1:
                sd = xbmcgui.Dialog()
                ret = sd.select('Select a Link', [link[0] for link in links])
                if ret > -1:
                    return links[ret][1]
            else:
                raise Exception('No usable link from Real Debrid')
        finally:
            dialog.close()
            
    def __get_link(self, link):
        if 'download' in link:
            if 'quality' in link:
                label = '[%s] %s' % (link['quality'], link['download'])
            else:
                label = link['download']
            return (label, link['download'])
        
    def refresh_token(self):
        url = 'https://api.real-debrid.com/oauth/v2/token'
        client_id = addon.get_setting('realdebrid_client_id')
        client_secret = addon.get_setting('realdebrid_client_secret')
        refresh_token = addon.get_setting('realdebrid_refresh')
        data = {'client_id': client_id, 'client_secret': client_secret, 'code': refresh_token, 'grant_type': 'http://oauth.net/grant_type/device/1.0'}
        addon.log_debug('Refreshing Expired Real Debrid Token: |%s|%s|' % (client_id, refresh_token))
        try:
            js_result = json.loads(net.http_POST(url, data, headers=self.headers).content)
            addon.log_debug('Refreshed Real Debrid Token: |%s|' % (js_result))
            addon.set_setting('realdebrid_token', js_result['access_token'])
            addon.set_setting('realdebrid_refresh', js_result['refresh_token'])
        except Exception as e:
            # empty all auth settings to force a re-auth on next use
            addon.set_setting('realdebrid_client_id', '')
            addon.set_setting('realdebrid_client_secret', '')
            addon.set_setting('realdebrid_token', '')
            addon.set_setting('realdebrid_refresh', '')
            raise Exception('Unable to Refresh Real Debrid Token: %s' % (e))
    
    def authorize_resolver(self):
        url = 'https://api.real-debrid.com/oauth/v2/device/code?client_id=%s&new_credentials=yes' % (CLIENT_ID)
        js_result = json.loads(net.http_GET(url, headers=self.headers).content)
        pd = xbmcgui.DialogProgress()
        line1 = 'Go to URL: %s' % (js_result['verification_url'])
        line3 = 'When prompted enter: %s' % (js_result['user_code'])
        try:
            pd.create('Icefilms Real Debrid Authorization', line1, '' ,line3)
            pd.update(0)
            expires = js_result['expires_in']
            count_interval = js_result['interval']
            total_interval = 0
            interval = count_interval * 1000
            device_code = js_result['device_code']
            while True:
                try:
                    url = 'https://api.real-debrid.com/oauth/v2/device/credentials?client_id=%s&code=%s' % (CLIENT_ID, device_code)
                    js_result = json.loads(net.http_GET(url, headers=self.headers).content)
                except Exception as e:
                    addon.log_debug('Exception during RD auth: %s' % (e))
                    for _ in range(INTERVALS):
                        if pd.iscanceled(): return False
                        xbmc.sleep(interval / INTERVALS)
                    total_interval += count_interval
                    pd.update(int(float(100.0 / int(expires)) * total_interval))
                else:
                    break
        finally:
            pd.close()
            
        url = 'https://api.real-debrid.com/oauth/v2/token'
        data = {'client_id': js_result['client_id'], 'client_secret': js_result['client_secret'], 'code': device_code, 'grant_type': 'http://oauth.net/grant_type/device/1.0'}
        addon.set_setting('realdebrid_client_id', js_result['client_id'])
        addon.set_setting('realdebrid_client_secret', js_result['client_secret'])
        addon.log_debug('Authorizing Real Debrid: %s' % (js_result['client_id']))
        js_result = json.loads(net.http_POST(url, data, headers=self.headers).content)
        addon.log_debug('Authorizing Real Debrid Result: |%s|' % (js_result))
        addon.set_setting('realdebrid_token', js_result['access_token'])
        addon.set_setting('realdebrid_refresh', js_result['refresh_token'])
        
    def get_all_hosters(self):
        if self.hosters is None:
            try:
                url = 'https://api.real-debrid.com/rest/1.0/hosts/regex'
                self.hosters = []
                js_result = json.loads(net.http_GET(url, headers=self.headers).content)
                regexes = [regex.lstrip('/').rstrip('/').replace('\/', '/') for regex in js_result]
                self.hosters = [re.compile(regex) for regex in regexes]
            except Exception as e:
                addon.log_error('Error getting RD regexes: %s' % (e))
            finally:
                addon.log_debug('RealDebrid hosters : %s' % self.hosters)
                return self.hosters
              
    def get_hosts(self):
        if self.hosters is None:
            try:
                self.hosts = []
                url = 'https://api.real-debrid.com/rest/1.0/hosts/domains'
                self.hosts = json.loads(net.http_GET(url, headers=self.headers).content)
            except Exception as e:
                addon.log_error('Error getting RD hosts: %s' % (e))
            finally:
                addon.log_debug('RealDebrid hosts : %s' % self.hosts)
                return self.hosts

    def valid_host(self, host):
        if addon.get_setting('realdebrid-account') == 'false': return False
        addon.log_debug('Checking if host is supported by RD: %s' % host)
        self.get_hosts()
        if host.startswith('www.'): host = host.replace('www.', '')
        if any(host in item for item in self.hosts):
            return True
        else:
            return False

    def clear_client(self):
        addon.log('Clearing out client secret keys and tokens...')
        addon.set_setting('realdebrid_client_id', '')
        addon.set_setting('realdebrid_client_secret', '')
        addon.set_setting('realdebrid_token', '')
        addon.set_setting('realdebrid_refresh', '')
