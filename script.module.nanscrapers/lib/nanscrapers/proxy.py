import random
import urllib
import urllib2
import urlparse

from nanscrapers.common import random_agent


def get(url, check, headers=None, data=None):
    if headers is None:
        headers = {
            'User-Agent': random_agent(),
        }
        try:
            request = urllib2.Request(url, headers=headers, data=data)
            html = urllib2.urlopen(request, timeout=10).read()
            if check in str(html): return html
        except:
            pass

    try:
        new_url = get_proxy_url() % urllib.quote_plus(url)
        headers['Referer'] = 'http://%s/' % urlparse.urlparse(new_url).netloc
        request = urllib2.Request(new_url, headers=headers)
        response = urllib2.urlopen(request, timeout=10)
        html = response.read()
        response.close()
        if check in html: return html
    except:
        pass

    try:
        new_url = get_proxy_url() % urllib.quote_plus(url)
        headers['Referer'] = 'http://%s/' % urlparse.urlparse(new_url).netloc
        request = urllib2.Request(new_url, headers=headers)
        html = urllib2.urlopen(request, timeout=10).read()
        if check in html: return html
    except:
        pass

    return


def get_raw(url, headers=None, data=None):
    if headers is None:
        headers = {
            'User-Agent': random_agent(),
        }

    try:
        new_url = get_proxy_url() % urllib.quote_plus(url)
        headers['Referer'] = 'http://%s/' % urlparse.urlparse(new_url).netloc
        request = urllib2.Request(new_url, headers=headers)
        response = urllib2.urlopen(request, timeout=10)
        return response
    except:
        pass


def get_proxy_url():
    return random.choice([
        #'http://alter-ip.com/index.php?hl=3c0&q=%s',
        'http://buka.link/browse.php?b=20&u=%s&b=0&f=norefer',
        #'http://dontfilter.us/browse.php?b=20&u=%s',
        #'http://free-proxyserver.com/browse.php?b=20&u=%s',
        'http://www.freeopenproxy.com/browse.php?b=20&u=%s',
        'http://www.justproxy.co.uk/index.php?hl=2e5&q=%s',
        #'http://protectproxy.com/browse.php?b=20&u=%s',
        'http://proxite.net/browse.php?b=20&u=%s',
        'http://www.proxythis.info/index.php?hl=2e5&q=%s',
        'http://quickprox.com/browse.php?b=20&u=%s',
        'http://unblock-proxy.com/browse.php?b=20&u=%s&b=0&f=norefer',
        'http://www.unblockmyweb.com/browse.php?b=20&u=%s',
        #'http://unblocksite.org/view.php?b=20&u=%s',
        'http://unblockthatsite.net/ahora.php?b=20&u=%s',
    ])
