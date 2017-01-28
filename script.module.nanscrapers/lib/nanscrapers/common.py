import HTMLParser
import json
import random
import re
import urllib2
import urlparse


def clean_title(title):
    if title == None: return
    title = re.sub('&#(\d+);', '', title)
    title = re.sub('(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
    title = title.replace('&quot;', '\"').replace('&amp;', '&')
    title = re.sub('\n|([[].+?[]])|([(].+?[)])|\s(vs|v[.])\s|(:|;|-|"|,|\'|\_|\.|\?)|\s', '', title)
    return title.lower()


def random_agent():
    BR_VERS = [
        ['%s.0' % i for i in xrange(18, 43)],
        ['37.0.2062.103', '37.0.2062.120', '37.0.2062.124', '38.0.2125.101', '38.0.2125.104', '38.0.2125.111',
         '39.0.2171.71', '39.0.2171.95', '39.0.2171.99', '40.0.2214.93', '40.0.2214.111',
         '40.0.2214.115', '42.0.2311.90', '42.0.2311.135', '42.0.2311.152', '43.0.2357.81', '43.0.2357.124',
         '44.0.2403.155', '44.0.2403.157', '45.0.2454.101', '45.0.2454.85', '46.0.2490.71',
         '46.0.2490.80', '46.0.2490.86', '47.0.2526.73', '47.0.2526.80'],
        ['11.0']]
    WIN_VERS = ['Windows NT 10.0', 'Windows NT 7.0', 'Windows NT 6.3', 'Windows NT 6.2', 'Windows NT 6.1',
                'Windows NT 6.0', 'Windows NT 5.1', 'Windows NT 5.0']
    FEATURES = ['; WOW64', '; Win64; IA64', '; Win64; x64', '']
    RAND_UAS = ['Mozilla/5.0 ({win_ver}{feature}; rv:{br_ver}) Gecko/20100101 Firefox/{br_ver}',
                'Mozilla/5.0 ({win_ver}{feature}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{br_ver} Safari/537.36',
                'Mozilla/5.0 ({win_ver}{feature}; Trident/7.0; rv:{br_ver}) like Gecko']
    index = random.randrange(len(RAND_UAS))
    return RAND_UAS[index].format(win_ver=random.choice(WIN_VERS), feature=random.choice(FEATURES),
                                  br_ver=random.choice(BR_VERS[index]))


def replaceHTMLCodes(txt):
    txt = re.sub("(&#[0-9]+)([^;^0-9]+)", "\\1;\\2", txt)
    txt = HTMLParser.HTMLParser().unescape(txt)
    txt = txt.replace("&quot;", "\"")
    txt = txt.replace("&amp;", "&")
    return txt


def vk(url):
    try:
        try:
            oid, id = urlparse.parse_qs(urlparse.urlparse(url).query)['oid'][0], \
                      urlparse.parse_qs(urlparse.urlparse(url).query)['id'][0]
        except:
            oid, id = re.compile('\/video(.*)_(.*)').findall(url)[0]
        try:
            hash = urlparse.parse_qs(urlparse.urlparse(url).query)['hash'][0]
        except:
            hash = vk_hash(oid, id)

        u = 'http://api.vk.com/method/video.getEmbed?oid=%s&video_id=%s&embed_hash=%s' % (oid, id, hash)

        headers = {'User-Agent': random_agent()}

        request = urllib2.Request(u, headers=headers)
        result = urllib2.urlopen(request).read()

        result = re.sub(r'[^\x00-\x7F]+', ' ', result)

        try:
            result = json.loads(result)['response']
        except:
            result = vk_private(oid, id)

        url = []
        try:
            url += [{'quality': '720', 'url': result['url720']}]
        except:
            pass
        try:
            url += [{'quality': '540', 'url': result['url540']}]
        except:
            pass
        try:
            url += [{'quality': '480', 'url': result['url480']}]
        except:
            pass
        if not url == []: return url
        try:
            url += [{'quality': '360', 'url': result['url360']}]
        except:
            pass
        if not url == []: return url
        try:
            url += [{'quality': '240', 'url': result['url240']}]
        except:
            pass

        if not url == []: return url

    except:
        return


def vk_hash(oid, id):
    try:
        url = 'http://vk.com/al_video.php?act=show_inline&al=1&video=%s_%s' % (oid, id)

        headers = {'User-Agent': random_agent()}

        request = urllib2.Request(url, headers=headers)
        result = urllib2.urlopen(request).read()
        result = result.replace('\'', '"').replace(' ', '')

        hash = re.compile('"hash2":"(.+?)"').findall(result)
        hash += re.compile('"hash":"(.+?)"').findall(result)
        hash = hash[0]

        return hash
    except:
        return


def vk_private(oid, id):
    try:
        url = 'http://vk.com/al_video.php?act=show_inline&al=1&video=%s_%s' % (oid, id)

        headers = {'User-Agent': random_agent()}

        request = urllib2.Request(url, headers=headers)
        result = urllib2.urlopen(request).read()
        result = re.compile('var vars *= *({.+?});').findall(result)[0]
        result = re.sub(r'[^\x00-\x7F]+', ' ', result)
        result = json.loads(result)

        return result
    except:
        return


def odnoklassniki(url):
    try:
        url = re.compile('//.+?/.+?/([\w]+)').findall(url)[0]
        url = 'http://ok.ru/dk?cmd=videoPlayerMetadata&mid=%s' % url

        headers = {'User-Agent': random_agent()}

        request = urllib2.Request(url, headers=headers)
        result = urllib2.urlopen(request).read()
        result = re.sub(r'[^\x00-\x7F]+', ' ', result)

        result = json.loads(result)['videos']

        try:
            hd = [{'quality': '1080', 'url': i['url']} for i in result if i['name'] == 'full']
        except:
            pass
        try:
            hd += [{'quality': 'HD', 'url': i['url']} for i in result if i['name'] == 'hd']
        except:
            pass
        try:
            sd = [{'quality': 'SD', 'url': i['url']} for i in result if i['name'] == 'sd']
        except:
            pass
        try:
            sd += [{'quality': 'SD', 'url': i['url']} for i in result if i['name'] == 'low']
        except:
            pass
        try:
            sd += [{'quality': 'SD', 'url': i['url']} for i in result if i['name'] == 'lowest']
        except:
            pass
        try:
            sd += [{'quality': 'SD', 'url': i['url']} for i in result if i['name'] == 'mobile']
        except:
            pass

        url = hd + sd[:1]
        if not url == []: return url

    except:
        return

def googletag(url):
    quality = re.compile('itag=(\d*)').findall(url)
    quality += re.compile('=m(\d*)$').findall(url)
    try:
        quality = quality[0]
    except:
        return []

    if quality in ['37', '137', '299', '96', '248', '303', '46']:
        return [{'quality': '1080', 'url': url}]
    elif quality in ['22', '84', '136', '298', '120', '95', '247', '302', '45', '102']:
        return [{'quality': '720', 'url': url}]
    elif quality in ['35', '44', '135', '244', '94']:
        return [{'quality': '480', 'url': url}]
    elif quality in ['18', '34', '43', '82', '100', '101', '134', '243', '93']:
        return [{'quality': '480', 'url': url}]
    elif quality in ['5', '6', '36', '83', '133', '242', '92', '132']:
        return [{'quality': '480', 'url': url}]
    else:
        return []