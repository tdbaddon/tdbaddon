#!/usr/bin/python
"""
    SALTS XBMC Addon
    Copyright (C) 2017 tknorris

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import urlparse
import random
import threading
import os
import json
import urllib
import kodi
import log_utils
import image_scraper
from SimpleHTTPServer import SimpleHTTPRequestHandler
from BaseHTTPServer import HTTPServer

class ValidationError(Exception):
    pass

class ImageProxy(object):
    def __init__(self, host=None):
        self.host = '127.0.0.1' if host is None else host
        self.running = False
        self.stop_server = False
        self.svr_thread = None
        self.httpd = None
    
    def run(self):
        self.svr_thread = threading.Thread(target=self.__start_proxy)
        self.svr_thread.daemon = True
        self.svr_thread.start()

    def __start_proxy(self):
        port = int(kodi.get_setting('proxy_port') or self.get_port())
        server_address = (self.host, port)
        log_utils.log('Starting Image Proxy: %s:%s' % (server_address), log_utils.LOGNOTICE)
        self.running = True
        self.httpd = MyHTTPServer(server_address, MyRequestHandler)
        self.httpd.serve_forever(.5)
        log_utils.log('Image Proxy Exitting: %s:%s' % (server_address), log_utils.LOGNOTICE)
        self.running = False
        self.httpd.server_close()

    def stop_proxy(self):
        if self.httpd is not None:
            self.httpd.shutdown()
        
        if self.svr_thread is not None:
            log_utils.log('Reaping proxy thread: %s' % (self.svr_thread))
            self.svr_thread.join()
            self.svr_thread = None

    @staticmethod
    def get_port():
        port = random.randint(10000, 65535)
        kodi.set_setting('proxy_port', port)
        return port

class MyHTTPServer(HTTPServer):
    def process_request(self, request, client_address):
        try: HTTPServer.process_request(self, request, client_address)
        except IOError as e: log_utils.log('Image Proxy Error: %s - %s' % (type(e), e), log_utils.LOGDEBUG)
        
class MyRequestHandler(SimpleHTTPRequestHandler):
    proxy_cache = {}
    LOG_FILE = kodi.translate_path(os.path.join(kodi.get_profile(), 'proxy.log'))
    try: log_fd = open(LOG_FILE, 'w')
    except: log_fd = None
    base_req = ['image_type', 'trakt_id', 'video_ids']
    required = {
        'Movie': base_req,
        'TV Show': base_req,
        'Season': base_req + ['season'],
        'Episode': base_req + ['season', 'episode'],
        'person': base_req + ['name', 'person_ids']
    }
    
    def _set_headers(self, code=200):
        self.send_response(code)
        self.end_headers()
        
    def __redirect(self, url):
        self.send_response(301)
        self.send_header('Location', url)
        self.end_headers()
        
    def log_message(self, format, *args):
        if self.log_fd is not None:
            self.log_fd.write('[%s] %s\n' % (self.log_date_time_string(), format % (args)))
        
    def do_HEAD(self):
        return self.do_GET()
        
    def do_POST(self):
        self._set_headers(400)
    
    def do_GET(self):
        try:
            fields = self.__validate(self.parse_query(self.path))
            key = (fields['video_type'], fields['trakt_id'], fields.get('season', ''), fields.get('episode', ''))
            if key in self.proxy_cache:
                images = self.proxy_cache[key]
            else:
                video_ids = json.loads(fields['video_ids'])
                if fields['video_type'] == image_scraper.OBJ_PERSON:
                    person_ids = json.loads(fields['person_ids'])
                    person = {'person': {'name': fields['name'], 'ids': person_ids}}
                    images = image_scraper.scrape_person_images(video_ids, person)
                else:
                    images = image_scraper.scrape_images(fields['video_type'], video_ids, fields.get('season', ''), fields.get('episode', ''), screenshots=True)
                self.proxy_cache[key] = images
                
            image_url = images[fields['image_type']]
            if image_url is None:
                self._set_headers()
            elif image_url.startswith('http'):
                self.__redirect(image_url)
            else:
                self._set_headers()
                with open(image_url) as f:
                    self.wfile.write(f.read())
        except ValidationError as e:
            self.__send_error(e)
    
    def __validate(self, params):
        if 'video_type' not in params:
            raise ValidationError('Missing Video Type')
        
        video_type = params['video_type']
        if video_type not in self.required:
            raise ValidationError('Unrecognized Video Type')
        
        required = self.required[video_type][:]
        for key in self.required[video_type]:
            if key in params: required.remove(key)
        
        if required:
            raise ValidationError('Missing Parameters: %s' % (', '.join(required)))
        
        return params
    
    def __send_error(self, msg):
        self.send_error(400, str(msg))

    @staticmethod
    def parse_query(path):
        q = {}
        query = urlparse.urlparse(path).query
        if query.startswith('?'): query = query[1:]
        queries = urlparse.parse_qs(query)
        for key in queries:
            if len(queries[key]) == 1:
                q[key] = urllib.unquote(queries[key][0])
            else:
                q[key] = queries[key]
        return q
