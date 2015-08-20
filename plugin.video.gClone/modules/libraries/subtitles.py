# -*- coding: utf-8 -*-

'''
    gClone Add-on
    Copyright (C) 2015 NVTTeam

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
import os
import zlib
import base64
import xmlrpclib
import control
import xbmc


langDict = {'Afrikaans': 'afr', 'Albanian': 'alb', 'Arabic': 'ara', 'Armenian': 'arm', 'Basque': 'baq', 'Bengali': 'ben', 'Bosnian': 'bos', 'Breton': 'bre', 'Bulgarian': 'bul', 'Burmese': 'bur', 'Catalan': 'cat', 'Chinese': 'chi', 'Croatian': 'hrv', 'Czech': 'cze', 'Danish': 'dan', 'Dutch': 'dut', 'English': 'eng', 'Esperanto': 'epo', 'Estonian': 'est', 'Finnish': 'fin', 'French': 'fre', 'Galician': 'glg', 'Georgian': 'geo', 'German': 'ger', 'Greek': 'ell', 'Hebrew': 'heb', 'Hindi': 'hin', 'Hungarian': 'hun', 'Icelandic': 'ice', 'Indonesian': 'ind', 'Italian': 'ita', 'Japanese': 'jpn', 'Kazakh': 'kaz', 'Khmer': 'khm', 'Korean': 'kor', 'Latvian': 'lav', 'Lithuanian': 'lit', 'Luxembourgish': 'ltz', 'Macedonian': 'mac', 'Malay': 'may', 'Malayalam': 'mal', 'Manipuri': 'mni', 'Mongolian': 'mon', 'Montenegrin': 'mne', 'Norwegian': 'nor', 'Occitan': 'oci', 'Persian': 'per', 'Polish': 'pol', 'Portuguese': 'por,pob', 'Portuguese(Brazil)': 'pob,por', 'Romanian': 'rum', 'Russian': 'rus', 'Serbian': 'scc', 'Sinhalese': 'sin', 'Slovak': 'slo', 'Slovenian': 'slv', 'Spanish': 'spa', 'Swahili': 'swa', 'Swedish': 'swe', 'Syriac': 'syr', 'Tagalog': 'tgl', 'Tamil': 'tam', 'Telugu': 'tel', 'Thai': 'tha', 'Turkish': 'tur', 'Ukrainian': 'ukr', 'Urdu': 'urd'}

quality = ['bluray', 'hdrip', 'brrip', 'bdrip', 'dvdrip', 'webrip', 'hdtv']


def get(name, imdb, season, episode):
    try:
        langs = []
        try: langs.append(langDict[control.setting('sublang1')])
        except: pass
        try: langs.append(langDict[control.setting('sublang2')])
        except: pass

        try: subLang = xbmc.Player().getSubtitles()
        except: subLang = ''
        if subLang == langs[0]: raise Exception()

        server = xmlrpclib.Server('http://api.opensubtitles.org/xml-rpc', verbose=0)
        token = server.LogIn('', '', 'en', 'XBMC_Subtitles_v1')['token']

        sublanguageid = ','.join(langs) ; imdbid = re.sub('[^0-9]', '', imdb)

        if not (season == '' or episode == ''):
            result = server.SearchSubtitles(token, [{'sublanguageid': sublanguageid, 'imdbid': imdbid, 'season': season, 'episode': episode}])['data']
            fmt = ['hdtv']
        else:
            result = server.SearchSubtitles(token, [{'sublanguageid': sublanguageid, 'imdbid': imdbid}])['data']
            try: vidPath = xbmc.Player().getPlayingFile()
            except: vidPath = ''
            fmt = re.split('\.|\(|\)|\[|\]|\s|\-', vidPath)
            fmt = [i.lower() for i in fmt]
            fmt = [i for i in fmt if i in quality]

        filter = []
        result = [i for i in result if i['SubSumCD'] == '1']

        for lang in langs:
            filter += [i for i in result if i['SubLanguageID'] == lang and any(x in i['MovieReleaseName'].lower() for x in fmt)]
            filter += [i for i in result if i['SubLanguageID'] == lang and any(x in i['MovieReleaseName'].lower() for x in quality)]
            filter += [i for i in result if i['SubLanguageID'] == lang]

        try: lang = xbmc.convertLanguage(filter[0]['SubLanguageID'], xbmc.ISO_639_1)
        except: lang = filter[0]['SubLanguageID']

        content = [filter[0]['IDSubtitleFile'],]
        content = server.DownloadSubtitles(token, content)
        content = base64.b64decode(content['data'][0]['data'])
        content = zlib.decompressobj(16+zlib.MAX_WBITS).decompress(content)

        subtitle = xbmc.translatePath('special://temp/')
        subtitle = os.path.join(subtitle, 'TemporarySubs.%s.srt' % lang)
        
        file = control.openFile(subtitle, 'w')
        file.write(str(content))
        file.close()

        xbmc.sleep(1000)
        xbmc.Player().setSubtitles(subtitle)
    except:
        pass

