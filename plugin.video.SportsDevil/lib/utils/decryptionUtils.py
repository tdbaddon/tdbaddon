# -*- coding: utf-8 -*-
import pyDes
import urllib
import re
from regexUtils import parseTextToGroups
from javascriptUtils import JsFunctions, JsUnpacker, JsUnpackerV2, JsUnwiser, JsUnFunc, JsUnPP, JsUnPush
try: import json
except ImportError: import simplejson as json
try: from Crypto.Cipher import AES
except ImportError: import pyaes as AES

def encryptDES_ECB(data, key):
    data = data.encode()
    k = pyDes.des(key, pyDes.ECB, IV=None, pad=None, padmode=pyDes.PAD_PKCS5)
    d = k.encrypt(data)
    assert k.decrypt(d, padmode=pyDes.PAD_PKCS5) == data
    return d

def decryptDES_ECB(data, key):
    data = data.decode('base-64')
    k = pyDes.des(key, pyDes.ECB, IV=None, pad=None, padmode=pyDes.PAD_PKCS5)
    return k.decrypt(data, padmode=pyDes.PAD_PKCS5)

def gAesDec(data, key):
    from mycrypt import decrypt
    return decrypt(key,data)

def cjsAesDec(data, key):
    from mycrypt import decrypt
    enc_data = json.loads(data.decode('base-64'))
    ciphertext = 'Salted__' + enc_data['s'].decode('hex') + enc_data['ct'].decode('base-64')
    return json.loads(decrypt(key,ciphertext.encode('base-64')))

def m3u8AesDec(data, key):
    try:
        _in = data.split('.')
        unpad = lambda s : s[0:-ord(s[-1])]
        aes = AES.new(key.decode('hex'), AES.MODE_CBC, _in[1].decode('hex'))
        return unpad(aes.decrypt(_in[0].decode('hex')))
    except: return data

def zdecode(data):
    import csv
    csv.register_dialect('js', delimiter=',', quotechar="'", escapechar='\\')

    keys_regex = r'''eval\(.*?function\(([^\)]+)\){'''
    keys = [re.search(keys_regex, data).groups()[0]]

    values_regex = r'''.*(\w+)\s*=\s*\w+\((.*?)\);\s*eval\(\1'''
    values = [re.search(values_regex, data, re.DOTALL).groups()[1].replace('\n','')]

    key_list = [l for l in csv.reader(keys, dialect='js')][0]
    value_list = [l for l in csv.reader(values, dialect='js')][0]

    dictionary = dict(zip(key_list, value_list))

    symtab_regex = r'''\w+\[\w+\]=(\w+)\[\w+\]\|\|\w+'''
    sym_key = re.search(symtab_regex, data).groups()[0]
    symtab = dictionary[sym_key]

    split_regex = r'''(.*)\.split\('(.*)'\)'''
    _symtab, _splitter = re.search(split_regex, symtab).groups()
    splitter = re.sub(r"""'\s*\+\s*'""", '', _splitter)
    symtab = _symtab.split(splitter)

    tab_regex = r'''(\w+)=\1\.replace'''
    tab_key = re.search(tab_regex, data).groups()[0]
    tab = dictionary[tab_key]

    def lookup(match):
        return symtab[int(match.group(0))] or str(match.group(0))

    return re.sub(ur'\w+', lookup, tab)


def wdecode(data):
    from itertools import chain
    
    in_data = re.split('\W+',data)
    pos = in_data.index(max(in_data,key=len))
    codec = "".join(chain(*zip(in_data[pos][:5], in_data[pos+1][:5], in_data[pos+2][:5])))
    data = "".join(chain(*zip(in_data[pos][5:], in_data[pos+1][5:], in_data[pos+2][5:])))
    
    ring = 0
    res = []
    for i in xrange(0,len(data),2):
        modifier = -1
        if (ord(codec[ring]) % 2):
            modifier = 1
        res.append( chr( int(data[i:i+2],36) - modifier ) )
        
        ring = ring + 1
        if ring >= len(codec):
            ring = 0
    return ''.join(res)

def onetv(playpath):
    import random,time,md5
    from base64 import b64encode
    user_agent = 'Mozilla%2F5.0%20%28Linux%3B%20Android%205.1.1%3B%20Nexus%205%20Build%2FLMY48B%3B%20wv%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Version%2F4.0%20Chrome%2F43.0.2357.65%20Mobile%20Safari%2F537.36'
    token = "65rSw"+"UzRad"
    servers = ['185.152.66.39', '185.102.219.72', '185.59.221.109', '185.152.64.236', '185.59.222.232', '185.102.219.67', '185.102.218.56']
    time_stamp = str(int(time.time()) + 14400)
    to_hash = "{0}{1}/hls/{2}".format(token,time_stamp,playpath)
    out_hash = b64encode(md5.new(to_hash).digest()).replace("+", "-").replace("/", "_").replace("=", "")
    server = random.choice(servers)
    
    url = "hls://http://{0}/p2p/{1}?st={2}&e={3}".format(server,playpath,out_hash,time_stamp)
    return '{url}|User-Agent={user_agent}&referer={referer}'.format(url=url,user_agent=user_agent,referer='6d6f6264726f2e6d65'.decode('hex'))


def doDemystify(data):
    escape_again=False
    
    #init jsFunctions and jsUnpacker
    jsF = JsFunctions()
    jsU = JsUnpacker()
    jsU2 = JsUnpackerV2()
    jsUW = JsUnwiser()
    jsUF = JsUnFunc()
    jsUP = JsUnPP()
    JsPush = JsUnPush()

    # unescape
    r = re.compile('a1=["\'](%3C(?=[^\'"]*%\w\w)[^\'"]+)["\']')
    while r.findall(data):
        for g in r.findall(data):
            quoted=g
            data = data.replace(quoted, urllib.unquote_plus(quoted))
    
    
    r = re.compile('unescape\(\s*["\']((?=[^\'"]*%\w\w)[^\'"]+)["\']')
    while r.findall(data):
        for g in r.findall(data):
            quoted=g
            data = data.replace(quoted, urllib.unquote_plus(quoted))
            
    r = re.compile("""('%[\w%]{100,130}')""")
    while r.findall(data):
        for g in r.findall(data):
            quoted=g
            data = data.replace(quoted, "unescape({0})".format(urllib.unquote_plus(quoted)))
    
    r = re.compile('unescape\(\s*["\']((?=[^\'"]*\\u00)[^\'"]+)["\']')
    while r.findall(data):
        for g in r.findall(data):
            quoted=g
            data = data.replace(quoted, quoted.decode('unicode-escape'))

    r = re.compile('(\'\+dec\("\w+"\)\+\')')
    while r.findall(data):
        for g in r.findall(data):
            r2 = re.compile('dec\("(\w+)"\)')
            for dec_data in r2.findall(g):
                res = ''
                for i in dec_data:
                    res = res + chr(ord(i) ^ 123)
            data = data.replace(g, res)

    #sebn
    r = re.compile(r"""(?:file|src|source):\s*(window\.atob\(['"][^'"]+['"]\))""")
    if r.findall(data):
        for g in r.findall(data):
            r2 = re.compile(r"""window\.atob\(['"]([^'"]+)['"]\)""")
            for base64_data in r2.findall(g):
                data = data.replace(g, urllib.unquote(base64_data.decode('base-64')))

    #r = re.compile('((?:eval\(decodeURIComponent\(|window\.)atob\([\'"][^\'"]+[\'"]\)+)')
    #while r.findall(data):
        #for g in r.findall(data):
            #r2 = re.compile('(?:eval\(decodeURIComponent\(|window\.)atob\([\'"]([^\'"]+)[\'"]\)+')
            #for base64_data in r2.findall(g):
                #data = data.replace(g, urllib.unquote(base64_data.decode('base-64')))
                
    r = re.compile('(<script.*?str=\'@.*?str.replace)')
    while r.findall(data):
        for g in r.findall(data):
            r2 = re.compile('.*?str=\'([^\']+)')
            for escape_data in r2.findall(g):
                data = data.replace(g, urllib.unquote(escape_data.replace('@','%')))
       
    r = re.compile('(base\([\'"]*[^\'"\)]+[\'"]*\))')
    while r.findall(data):
        for g in r.findall(data):
            r2 = re.compile('base\([\'"]*([^\'"\)]+)[\'"]*\)')
            for base64_data in r2.findall(g):
                data = data.replace(g, urllib.unquote(base64_data.decode('base-64')))
                escape_again=True
    
    r = re.compile('\?i=([^&]+)&r=([^&\'"]+)')
    for g in r.findall(data):
        print g
        try:
            _a, _b =  g[0].split('%2F')
            _res = (_a+'=').decode('base-64')+'?'+_b.decode('base-64')
            data = data.replace(g[0], _res)
            data = data.replace(g[1], urllib.unquote(g[1]).decode('base-64'))
        except:
            pass

    if 'var enkripsi' in data:
        r = re.compile(r"""enkripsi="([^"]+)""")
        gs = r.findall(data)
        if gs:
            for g in gs:
                s=''
                for i in g:
                    s+= chr(ord(i)^2)
                data = data.replace("""enkripsi=\""""+g, urllib.unquote(s))

    if """.replace(""" in data:
        r = re.compile(r""".replace\(["'](...[^"']+)["'],\s*["']([^"']*)["']\)""")
        gs = r.findall(data)
        if gs:
            for g in gs:
                if '\\' in g[0]:
                    data = data.replace(g[0].lower(),g[1])
                data = data.replace(g[0],g[1])

    # JS P,A,C,K,E,D
    if jsU2.containsPacked(data):
        data = jsU2.unpackAll(data)
        escape_again=True

    if jsU.containsPacked(data):
        data = jsU.unpackAll(data)
        escape_again=True

    # JS W,I,S,E
    if jsUW.containsWise(data):
        data = jsUW.unwiseAll(data)
        escape_again=True

    # Js unFunc
    if jsUF.cointainUnFunc(data):
        data = jsUF.unFuncALL(data)
        escape_again=True

    if jsUP.containUnPP(data):
        data = jsUP.UnPPAll(data)
        escape_again=True

    if JsPush.containUnPush(data):
        data = JsPush.UnPush(data)

    try: 
        data = zdecode(data)
        escape_again=True
    except: pass
    # unescape again
    if escape_again:
        data = doDemystify(data)
    return data
