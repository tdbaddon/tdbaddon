#!/usr/bin/env python

# Links and info about metacontainers.
# Update this file to update the containers.

# Size is in MB

#return dictionary of strings and integers
def get():
          containers = {} 

          #date updated
          containers['date'] = 'Dec 2016'
          
          containers['url_tuxen'] = 'http://user.gosub.dk/eldorado/'
          containers['url_2shared'] = 'http://www.2shared.com/file/zuXnOkxP/video_cache_20150121.html'
          containers['url_offshore'] = 'https://offshoregit.com/Eldorado/xbmc-addons/raw/master/icefilms.metadata/'
          
          #--- Database Meta Container ---# 
          containers['db_filename'] = 'video_cache_20161220.zip'
          containers['db_size'] = 10

          return containers
