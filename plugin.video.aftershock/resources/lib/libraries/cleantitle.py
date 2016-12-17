# -*- coding: utf-8 -*-

'''
    Copyright (C) 2015 lamdba

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


import re,unicodedata

def movie(title):
    title = re.sub('\n|([[].+?[]])|([(].+?[)])|\s(vs|v[.])\s|(:|;|-|"|,|\'|\_|\.|\?)|\s', '', title).lower()
    return title

def tv(title):
    title = re.sub('\n|\s(|[(])(UK|US|AU|\d{4})(|[)])$|\s(vs|v[.])\s|(:|;|-|"|,|\'|\_|\.|\?)|\s', '', title).lower()
    return title

def live(title):
    title = title.upper()
    title = title.strip()
    title = re.sub('\n|\s(|[(]|[(]\s)(UK|APAC|EUR0PE|LOCAL TIME|INDIA|ENTERTAINMENT|EU|IN|\d{4})(|[)]|\s[)])$|\s(vs|v[.])\s|(:|;|-|"|,|\'|\_|\.|\?)', '', title)
    try : tmpTitle = cleanedNames[title]
    except: tmpTitle = None
    if not tmpTitle == None:
        title = tmpTitle
    return title

def geturl(title):
    if title == None: return
    title = title.lower()
    title = title.translate(None, ':*?"\'\.<>|&!,')
    title = title.replace('/', '-')
    title = title.replace(' ', '-')
    title = title.replace('--', '-')
    return title

def get(title):
    if title == None: return
    title = re.sub('&#(\d+);', '', title)
    title = re.sub('(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
    title = title.replace('&quot;', '\"').replace('&amp;', '&')
    title = re.sub('\n|([[].+?[]])|([(].+?[)])|\s(vs|v[.])\s|(:|;|-|"|,|\'|\_|\.|\?)|\s', '', title).lower()
    return title

def get_simple(title):
    if title == None: return
    title = title.lower()
    title = re.sub('(\d{4})', '', title)
    title = re.sub('&#(\d+);', '', title)
    title = re.sub('(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
    title = title.replace('&quot;', '\"').replace('&amp;', '&')
    title = re.sub('\n|\(|\)|\[|\]|\{|\}|\s(vs|v[.])\s|(:|;|-|"|,|\'|\_|\.|\?)|\s', '', title).lower()
    return title


def getsearch(title):
    if title == None: return
    title = title.lower()
    title = re.sub('&#(\d+);', '', title)
    title = re.sub('(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
    title = title.replace('&quot;', '\"').replace('&amp;', '&')
    title = re.sub('\\\|/|-|:|;|\*|\?|"|\'|<|>|\|', '', title).lower()
    return title


def query(title):
    if title == None: return
    title = title.replace('\'', '').rsplit(':', 1)[0]
    return title


def normalize(title):
    try:
        try: return title.decode('ascii').encode("utf-8")
        except: pass

        return str( ''.join(c for c in unicodedata.normalize('NFKD', unicode( title.decode('utf-8') )) if unicodedata.category(c) != 'Mn') )
    except:
        return title

cleanedNames = {'& PICTURE HD':'& PICTURES HD',
                '9X MUSIC':'9X M',
                '9X TASHAN PUNJABI':'9X TASHAN',
                'AAJ TAK NEWS':'AAJ TAK',
                'AAJ TAKK':'AAJ TAK',
                'AASTHA BHAJAN':'AASTHA',
                'AASTHA TV':'AASTHA',
                'AND PIC HD':'& PICTURES HD',
                'AND PIC SD':'& PICTURES',
                'AND PICTURE HD':'& PICTURES HD',
                'AND TV':'& TV',
                'AND TV HD':'& TV HD',
                'AND TV MUSIC HD':'& TV MUSIC HD',
                'ASTHA BHAJAN':'AASTHA',
                'ASTHA TV':'AASTHA',
                'CARTOON NETWORK HINDI':'CARTOON NETWORK',
                'COLORS TV':'COLORS',
                'COLORS TV HD':'COLORS HD',
                'DANGAL TV':'DANGAL',
                'DELHI AAJ TAK':'AAJ TAK DELHI',
                'DHAMMAL TV':'DHAMMAL',
                'DISCOVERY HD HINDI':'DISCOVERY HD',
                'ENTER 10':'ENTERR10',
                'ENTERR 10':'ENTERR10',
                'ENTERR10 MOVIES':'ENTERR10',
                'KTV TAMIL':'K TV TAMIL',
                'LIFE OK SD':'LIFE OK',
                'MOVIE OK':'MOVIES OK',
                'MUSIC':'MUSIC XPRESS',
                'NATIONAL GEOGRAPHIC HD HINDI':'NATIONAL GEOGRAPHIC HD',
                'NATIONAL GEOGRAPHIC HINDI':'NATIONAL GEOGRAPHIC',
                'NDTV NEWS ENGLISH':'NDTV',
                'NEWS18':'NEWS 18',
                'NICKELODEON HINDI':'NICK',
                'NICKELODEON JR HINDI':'NICK JR',
                'POGO TV':'POGO TV',
                'SAB TV':'SONY SAB',
                'SAB TV HD':'SONY SAB HD',
                'SANSKAR TV':'SANSKAR',
                'SET MAX':'SONY MAX',
                'SONY ENTERTAINMENT HD':'SONY TV',
                'SONY MAX2':'SONY MAX 2',
                'SONY SET MAX':'SONY MAX',
                'SONY SET MAX HD':'SONY MAX HD',
                'STAR GOLD SD':'STAR GOLD',
                'STAR JALSHA US':'STAR JALSHA',
                'STAR PLUS IND':'STAR PLUS',
                'STAR PLUS SD':'STAR PLUS',
                'STAR PRAVAAH US MARATHI':'STAR PRAVAAH MARATHI',
                'STAR SPORTS1SD':'STAR SPORTS 1',
                'STAR SPORTS2SD':'STAR SPORTS 2',
                'STAR USTUV':'STAR UTSAV',
                'STAR UTSUV MOVIES':'STAR UTSAV MOVIES',
                'STAR VIJAY HD TAMIL':'STAR VIJAY HD',
                'STAR WORLD HD':'STAR WORLD',
                'TEN2 HD':'TEN 2 HD',
                'TEN3 HD':'TEN 3 HD',
                'TENGOLF':'TEN GOLF',
                'TEZ NEWS':'AAJ TAK TEZ',
                'TIMES NOW NEWS':'TIMES NOW',
                'UTV MOVIES INTERNATIONAL':'UTV MOVIES',
                'ZEE ANMOL CINE':'ZEE ANMOL',
                'ZEE CINEMA USA':'ZEE CINEMA',
                'ZEE LIVING':'Z LIVING',
                'ZEE LIVING HD':'Z LIVING HD',
                'ZEE MARATHI USA':'ZEE MARATHI',
                'ZEE SALAM':'ZEE SALAAM',
                'ZEE TAAS24':'ZEE 24 TAAS',
                'ZEE TV ME':'ZEE TV',
                'ZEE TV SD':'ZEE TV',
                'ZINDAGI':'ZEE ZINDAGI',
                'ZINDAGI TV':'ZEE ZINDAGI',
                'ZING TV':'ZING'
                }

