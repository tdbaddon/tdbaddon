import sys, ConfigParser, collections

sys.argv = ['plugin.video.aftershock', '1']


url = 'http://pastebin.com/raw/PfvnzZfi'

#mode = 'ini'
mode = 'm3u'

basePath = "../data/myaddons.%s" % mode

def createINI(items, basePath):
    cfgfile = open(basePath, 'w')
    section = "plugin.video.livestream"
    Config = ConfigParser.ConfigParser()
    Config.optionxform=str

    Config.add_section(section)
    for item in items:
        title = client.parseDOM(item, "title")[0]
        link = client.parseDOM(item, "link")[0]
        Config.set(section, title, link)
    Config.write(cfgfile)

    cfgfile.close()


def createM3U(items, basePath) :
    FORMAT_DESCRIPTOR = "#EXTM3U"
    RECORD_MARKER = "#EXTINF:"
    fp = file(basePath, "w")
    fp.write(FORMAT_DESCRIPTOR + "\n")
    for item in items:
        title = client.parseDOM(item, "title")[0]
        link = client.parseDOM(item, "link")[0]
        print 'Checking %s ' % title
        try : resolved = client.request(link, output='geturl', timeout='2')
        except: resolved = None
        if resolved == None:
            print '%s Not working' % title
            continue
        print link
        fp.write("%s:-1 tvg-id=\"%s\",%s\n" % (RECORD_MARKER, title, title))
        fp.write(link + "\n")
    fp.close()

try :
    from resources.lib.libraries import client
    result = client.request(url)
    items = client.parseDOM(result, "item")
    if mode == 'ini':
        createINI(items, basePath)
    elif mode == 'm3u':
        createM3U(items, basePath)
except:
    from resources.lib.libraries import client
    import traceback
    traceback.print_exc()
