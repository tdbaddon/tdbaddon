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
from resources.lib.libraries import client
from resources.lib.libraries import jsunpack


def resolve(url):
    try:
        O = {
            '___': 0,
            '$$$$': "f",
            '__$': 1,
            '$_$_': "a",
            '_$_': 2,
            '$_$$': "b",
            '$$_$': "d",
            '_$$': 3,
            '$$$_': "e",
            '$__': 4,
            '$_$': 5,
            '$$__': "c",
            '$$_': 6,
            '$$$': 7,
            '$___': 8,
            '$__$': 9,
            '$_': "constructor",
            '$$': "return",
            '_$': "o",
            '_': "u",
            '__': "t",
        }


        url = url.replace('/f/', '/embed/')

        result = client.request(url)

        result = re.search('(eval\(function.*?)</script>', result, re.DOTALL).group(1)

        result = jsunpack.unpack(result)
        result = result.replace('\\\\', '\\')

        result = re.search('(O=.*?)(?:$|</script>)', result, re.DOTALL).group(1)
        result = re.search('O\.\$\(O\.\$\((.*?)\)\(\)\)\(\);', result)

        s1 = result.group(1)
        s1 = s1.replace(' ', '')
        s1 = s1.replace('(![]+"")', 'false')
        s3 = ''
        for s2 in s1.split('+'):
            if s2.startswith('O.'):
                s3 += str(O[s2[2:]])
            elif '[' in s2 and ']' in s2:
                key = s2[s2.find('[') + 3:-1]
                s3 += s2[O[key]]
            else:
                s3 += s2[1:-1]

        s3 = s3.replace('\\\\', '\\')
        s3 = s3.decode('unicode_escape')
        s3 = s3.replace('\\/', '/')
        s3 = s3.replace('\\\\"', '"')
        s3 = s3.replace('\\"', '"')

        url = re.search('<source\s+src="([^"]+)', s3).group(1)
        return url
    except:
        return


