'''
Created on Oct 11, 2013

@author: 'ajdeveloped'

This file is part of XOZE. 

XOZE is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

XOZE is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with XOZE.  If not, see <http://www.gnu.org/licenses/>.
'''
import base64
import pickle
import re


def serialize(obj):
    '''Dumps passed object as string and then encode it using base64'''
    return base64.b64encode(pickle.dumps(obj))

def deserialize(data):
    '''Decodes passed data string using base64 and loads it as object.'''
    return pickle.loads(base64.b64decode(data))

# Parse p,a,c,k,e,d string for video URL
def parse_packed_value(p, a, c, k):
    '''Famous JavaScript packed values parser'''
    while(c >= 1):
        c = c - 1
        if(k[c]):
            
            baseNStr = baseNencode(c, a)
            p = re.sub('\\b' + baseNStr + '\\b', k[c], p)
            
    return p

def baseNencode(number, N):
    if not isinstance(number, (int, long)):
        raise TypeError('number must be an integer')
    if number < 0:
        raise ValueError('number must be positive')
    alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'[0:N]
    baseN = ''
    while number:
        number, i = divmod(number, N)
        baseN = alphabet[i] + baseN
    return baseN or alphabet[0]


def baseNdecode(number, N):
    return int(number, N)     

# #Following set of operations are used for ENK decoding.

def _enk_dec_num(kode, enc):
    if re.search('fromCharCode', enc):
        x = ''
        for nbr in kode.split():
            x += chr(int(nbr) - 3)
        return x
    else:
        return None
    
def _enk_dec_swap(kode, enc):
    if re.search('charAt', enc) and not re.search('@', enc):
        x = ''
        i = 0
        while i < (len(kode) - 1):
            x += (kode[i + 1] + kode[i])
            i += 2
        return (x + (kode[len(kode) - 1] if i < len(kode) else ''))
    else:
        return None

def _enk_dec_skip(kode, enc):
    if re.search('charAt', enc) and re.search('@', enc):
        x = ''
        i = 0
        while i < len(kode):
            if(kode[i] == '|' and kode[i + 1] == '|'):
                x += '@'
            else:
                x += kode[i]
            i += 2
        return x
    else:
        return None
    
def _enk_dec_reverse(kode, enc):
    if re.search('reverse', enc):
        return kode[::-1]
    else:
        return None
    
ENK_DEC_FUNC = [_enk_dec_num, _enk_dec_skip, _enk_dec_swap, _enk_dec_reverse]


def enk_dekode(html):
    kodeParts = re.compile('var kode\="kode\=\\\\"(.+?)\\\\";(.+?);"').findall(html)
    if len(kodeParts) == 0:
        return None
    kode = None
    while len(kodeParts) == 1:
        kode = kodeParts[0][0].replace('BY_PASS_D', '"').replace('BY_PASS_S', '\'').replace('\\\\', '\\')
        enc = kodeParts[0][1].replace('BY_PASS_D', '"').replace('BY_PASS_S', '\'').replace('\\\\', '\\')
        for dec_func in ENK_DEC_FUNC:
            x = dec_func(kode, enc)
            if x is not None:
                kode = x
        kodeParts = re.compile('kode\="(.+?)";(.*)').findall(kode.replace('\\"', 'BY_PASS_D').replace('\\\'', 'BY_PASS_S'))
    dekoded = kode.replace('\\"', '"').replace('\\\'', '\'').replace('\\\\', '\\')
    return dekoded

