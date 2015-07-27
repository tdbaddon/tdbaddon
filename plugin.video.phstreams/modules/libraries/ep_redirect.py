# -*- coding: utf-8 -*-

'''
    Genesis Add-on
    Copyright (C) 2015 lambda

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
'''


import re
import urllib
import cache
import cleantitle
import client
import json


def get(title, year, imdb, tvdb, season, episode, show, date, genre):
    try:
        redirect = False
        if len(season) > 3: redirect = True
        genre = [i.strip() for i in genre.split('/')]
        genre = [i for i in genre if any(x == i for x in ['Reality', 'Game Show', 'Talk Show'])]
        if not len(genre) == 0: redirect = True
        blocks = ['73141']
        if tvdb in blocks: redirect = True
        if redirect == False: raise Exception()
    except:
        return (season, episode)

    try:
        tvrage = cache.get(getTVrageId, 8640, imdb, tvdb, show, year)
        if tvrage == None: raise Exception()
    except:
        return (season, episode)

    try:
        result = cache.get(getTVrageEpisode, 8640, tvrage, title, date, season, episode)
        if result == None: raise Exception()
        return (result[0], result[1])
    except:
        return (season, episode)


def getTVrageId(imdb, tvdb, show, year):
    try:
        from modules.indexers import trakt
        if not imdb.startswith('tt'): imdb = 'tt' + imdb
        result = trakt.getTVShowSummary(imdb)
        result = json.loads(result)
        tvrage = result['ids']['tvrage']
        if tvrage == None: raise Exception()
        return str(tvrage)
    except:
        pass

    try:
        query = urllib.quote_plus(show)
        query = 'http://services.tvrage.com/feeds/search.php?show=%s' % query
        result = client.request(query, timeout='5')
        result = client.parseDOM(result, "show")
        show = cleantitle.tv(show)
        years = [str(year), str(int(year)+1), str(int(year)-1)]
        result = [i for i in result if show == cleantitle.tv(client.replaceHTMLCodes(client.parseDOM(i, "name")[0])) and any(x in client.parseDOM(i, "started")[0] for x in years)][0]
        tvrage = client.parseDOM(result, "showid")[0]
        return str(tvrage)
    except:
        pass


def getTVrageEpisode(tvrage, title, date, season, episode):
    monthMap = {'01':'Jan', '02':'Feb', '03':'Mar', '04':'Apr', '05':'May', '06':'Jun', '07':'Jul', '08':'Aug', '09':'Sep', '10':'Oct', '11':'Nov', '12':'Dec'}
    title = cleantitle.tv(title)

    try:
        url = 'http://www.tvrage.com/shows/id-%s/episode_list/all' % tvrage
        result = client.request(url, timeout='5')
        search = re.compile('<td.+?><a.+?title=.+?season.+?episode.+?>(\d+?)x(\d+?)<.+?<td.+?>(\d+?/.+?/\d+?)<.+?<td.+?>.+?href=.+?>(.+?)<').findall(result.replace('\n',''))
        d = '%02d/%s/%s' % (int(date.split('-')[2]), monthMap[date.split('-')[1]], date.split('-')[0])
        match = [i for i in search if d == i[2]]
        if len(match) == 1: return (str('%01d' % int(match[0][0])), str('%01d' % int(match[0][1])))
        match = [i for i in search if title == cleantitle.tv(i[3])]
        if len(match) == 1: return (str('%01d' % int(match[0][0])), str('%01d' % int(match[0][1])))
    except:
        pass

    try:
        url = 'http://epguides.com/common/exportToCSV.asp?rage=%s' % tvrage
        result = client.request(url, timeout='5')
        search = re.compile('\d+?,(\d+?),(\d+?),.+?,(\d+?/.+?/\d+?),"(.+?)",.+?,".+?"').findall(result)
        d = '%02d/%s/%s' % (int(date.split('-')[2]), monthMap[date.split('-')[1]], date.split('-')[0][-2:])
        match = [i for i in search if d == i[2]]
        if len(match) == 1: return (str('%01d' % int(match[0][0])), str('%01d' % int(match[0][1])))
        match = [i for i in search if title == cleantitle.tv(i[3])]
        if len(match) == 1: return (str('%01d' % int(match[0][0])), str('%01d' % int(match[0][1])))
    except:
        pass

