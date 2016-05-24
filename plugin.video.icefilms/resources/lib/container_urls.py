#!/usr/bin/env python

# Links and info about metacontainers.
# Update this file to update the containers.

# Size is in MB

#return dictionary of strings and integers
def get():
          containers = {} 

          #date updated
          containers['date'] = 'Feb 2015'
          
          containers['url_tuxen'] = 'http://user.gosub.dk/eldorado/'
          containers['url_2shared'] = 'http://www.2shared.com/file/zuXnOkxP/video_cache_20150121.html'
          
          #--- Database Meta Container ---# 
          containers['db_filename'] = 'video_cache_20150121.zip'
          containers['db_size'] = 7
                    
          #--- Movie Meta Container ---# 

          #basic container        
          containers['mv_covers_filename'] = 'movie_covers.zip'
          containers['mv_cover_size'] = 89
          
          containers['mv_backdrop_filename'] = 'movie_backdrops.zip'
          containers['mv_backdrop_size'] = 1100
          
          #--- TV   Meta  Container ---#

          #basic container       
          containers['tv_covers_filename'] = 'tv_covers.zip'
          containers['tv_cover_size'] = 223

          containers['tv_banners_filename'] = 'tv_banners.zip'
          containers['tv_banners_size'] = 94

          containers['tv_backdrop_filename'] = 'tv_backdrops.zip'
          containers['tv_backdrop_size'] = 395
          
          
          #additional container
          containers['tv_add_url'] = ''
          containers['tv_add_size'] = 0       


          return containers
