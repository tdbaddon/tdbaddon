import os
import xbmcgui
import xbmc
import time
import urllib
import urllib2
import re

import json

from bs4 import BeautifulSoup



class MovieDB:

	linkImagem = 'http://image.tmdb.org/t/p/original'
	generos = {}

	def __init__(self, api_key, lingua):
		self.api_key = api_key
		self.lingua = lingua
		self.getGeneros()

	def abrir_url(self, url):
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		return link

	def getGeneros(self):
		url = self.abrir_url('http://api.themoviedb.org/3/genre/movie/list?api_key='+self.api_key)
		soup = json.loads(url)



		for genero in soup["genres"].keys():
			self.generos[genero["id"]] = genero["name"]

		print "GENEROS NOVOS ==========================>"
		print self.generos

	def getMovieInfo(self, idIMDb):

		url = self.abrir_url('https://api.themoviedb.org/3/find/'+idIMDb+'?external_source=imdb_id&language='+self.lingua+'&api_key='+self.api_key)
		soup = json.loads(url)

		print soup

		data = {}
		data["name"] = soup["movie_results"]["original_title"]
		data["poster"] = self.linkImagem+soup["movie_results"]["poster_path"]
		data["genre"] = soup.firstaired.text
		data["plot"] = soup["movie_results"]["overview"]
		return json.dumps(data)

    def getTrailer(self, idIMDb):
        url = self.abrir_url('http://api.themoviedb.org/3/movie/' + idIMDb +'/trailers?api_key=' + self.api_key)
        try:
            data = json.loads(url)
        except:
            data = ''
        try:
            youtube_id = 'plugin://plugin.video.youtube/?action=play_video&videoid=' + str(data['youtube'][0]['source'])
        except:
            youtube_id= ''
        return str(youtube_id)
