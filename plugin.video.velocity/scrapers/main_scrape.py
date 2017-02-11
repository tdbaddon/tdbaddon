import xbmcaddon
import xbmcplugin
import xbmcgui
import xbmc
import xbmcvfs
import urllib, urllib2
import urlparse
import sys
import os
import re
import urlresolver
import time
from threading import Thread
from Queue import Queue
import json
from libs import viewsetter

import iwatchonline,primewire,afdah_scraper,icefilms,putlocker_both
from libs import kodi,trakt_auth
from libs import log_utils
from t0mm0.common.addon import Addon

addon_id=kodi.addon_id
artwork = xbmc.translatePath(os.path.join('special://home','addons',addon_id,'resources','art/'))
fanart = artwork+'fanart.jpg'
ADDON = xbmcaddon.Addon(id=kodi.addon_id)
addon_id=kodi.addon_id
addon = Addon(addon_id, sys.argv)

MAX_ERRORS = 10
all_source = []
def wrapper(func, arg,arg2,arg3, queue):
	queue.put(func(arg,arg2,arg3))


def find_source(name,thumb,media,movie_title):

    if media == 'shows':
        find_sourceTV(name, thumb, media, movie_title)
    else:
        try:
            if thumb is None:
                thumb = ''
            else:
                thumb = thumb

            title = name[:-7]
            movie_year = name[-6:]
            year = movie_year.replace('(', '').replace(')', '')
            video_type = 'movies'
            total_items = 0

            t1 = Thread(target=go_ice, args=(video_type, title, year))
            #############PRIMEWIRE########################
            t2 = Thread(target=go_prime, args=(video_type, title, year))
            ##############IWATCH COMPLETE####################
            t3 = Thread(target=go_iwatch, args=(video_type, title, year))
            #############AFDAH COMPLETE##################
            t4 = Thread(target=go_afdah, args=(video_type, title, year))
            ############PUTLOCKER COMPLETE##################
            t5 = Thread(target=go_putlocker, args=(video_type, title, year))

            t1.start()
            t2.start()
            t3.start()
            t4.start()
            t5.start()

            t1.join()
            t2.join()
            t3.join()
            t4.join()
            t5.join()

            for a in all_source:
                    if a:
                        b = sorted(a, reverse=False)
                        try:
                            for e in b :
                                #total_items =len(e)
                                #kodi.log(total_items)
                                if 'debrid' in e:
                                    premium = " [COLOR gold]"+str(e['debrid'])+" [/COLOR]"
                                else:
                                    premium = ''
                                hostname = e['hostname']
                                provider = "[COLOR white]["+hostname+"][/COLOR] - "
                                names = e['host']
                                urls = e['url']
                                if e['views'] == None:
                                    views = ''
                                else:
                                    views = " [COLOR green]Views "+e['views']+"[/COLOR]"
                                if e['quality'] == None:
                                    quals = ''
                                else:quals =" [COLOR red]["+ e['quality']+"][/COLOR]"
                                menu_items=[]
                                menu_items.append(('[COLOR gold]Add to Downloads[/COLOR]',      'XBMC.Container.Update(%s)' % addon.build_plugin_url({'mode':'setup_download', 'name':name,'url':urls,'thumb':thumb, 'media':media,'movie_title':movie_title})))

#TODO Make Dialog Selections
                                # passname = []
                                # pro_list = {'proname': provider + names + quals + views + premium, 'url': urls,'movie_title':movie_title,'thumb':thumb,'media':media }
                                #
                                # passname.append(pro_list)
                                # pick_list(passname)





                                kodi.addDir(provider+names+quals+views+premium,urls,'get_link',thumb,movie_title+movie_year,total_items,'','movies',menu_items=menu_items,is_playable='true',fanart=fanart)
                                viewsetter.set_view('files')
                        except:
                            pass

        except Exception as e:
                log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
                if kodi.get_setting('error_notify') == "true":
                    kodi.notify(header='Movie Scrapers',msg='(error) %s  %s' % (str(e), ''),duration=5000,sound=None)
                return



def pick_list(pro_list):
    kodi.log(pro_list)
    for e in pro_list:

        play_name=[]
        play_name.append(e['proname'])
        dialog = xbmcgui.Dialog()
        index = dialog.select('Choose Your Desired Provider', play_name)
        if index > -1:
            try:
                get_link(e['url'],e['movie_title'],e['thumb'],e['media'])
                # if hoster['url']:
                #     hoster_url = hoster['class'].resolve_link(hoster['url'])
                #     log_utils.log('Attempting to play url: %s as direct: %s from: %s' % (
                #         hoster_url, hoster['direct'], hoster['class'].get_name()))
                #     return hoster_url, hoster['direct']
            except Exception as e:
                log_utils.log('Error (%s) while trying to resolve %s' % (str(e), hoster['url']),
                              xbmc.LOGERROR)

        return None, None

def find_sourceTV(name,thumb,media,movie_title):

    try:
        if thumb is None:
            thumb = ''
        else:
            thumb = thumb

        #############Constants########################
        title = movie_title[:-7]
        movie_year = movie_title[-6:]
        year = movie_year.replace('(', '').replace(')', '')
        video_type = 'shows'
        total_items = 0
        t1 = Thread(target=go_ice_tv, args=(video_type, title, year,name))
        #############PRIMEWIRE########################
        t2 = Thread(target=go_prime_tv, args=(video_type, title, year,name))
        ##############IWATCH COMPLETE####################
        t3 = Thread(target=go_iwatch_tv, args=(video_type, title, year,name))
        ############PUTLOCKER COMPLETE##################
        t4 = Thread(target=go_putlocker_tv, args=(video_type, title, year,name))

        t1.start()
        t2.start()
        t3.start()
        t4.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()


        for a in all_source:
                if a:
                    b = sorted(a, reverse=False)
                    try:
                        for e in b :
                            if 'debrid' in e:
                                premium = " [COLOR gold]" + str(e['debrid']) + " [/COLOR]"
                            else:
                                premium = ''
                            hostname = e['hostname']
                            provider = "[COLOR white][" + hostname + "][/COLOR] - "
                            names = e['host']
                            urls = e['url']
                            if e['views'] == None:
                                views = ''
                            else:
                                views = " [COLOR green]Views " + e['views'] + "[/COLOR]"
                            if e['quality'] == None:
                                quals = ''
                            else:
                                quals = " [COLOR red][" + e['quality'] + "][/COLOR]"
                            menu_items=[]
                            menu_items.append(('[COLOR gold]Add to Downloads[/COLOR]',      'XBMC.Container.Update(%s)' % addon.build_plugin_url({'mode':'setup_download', 'name':name,'url':urls,'thumb':thumb, 'media':media,'movie_title':movie_title})))
                            kodi.addDir(provider + names + quals + views + premium,urls,'get_tv_link',thumb,movie_title,total_items,'',name,menu_items=menu_items,is_playable='true',fanart=fanart)
                            #kodi.addDir(provider+names+' ['+quals+']'+' [COLOR gold]'+str(premium)+'[/COLOR]',urls,'get_tv_link',thumb,movie_title,total_items,'',name,menu_items=menu_items,is_playable='true',fanart=fanart)
                            viewsetter.set_view('files')
                    except:
                        pass




    except Exception as e:
            log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
            if kodi.get_setting('error_notify') == "tru# e":
                kodi.notify(header='Scraper',msg='(error) %s  %s' % (str(e), ''),duration=5000,sound=None)


def make_vid_params(video_type, title, year, season, episode, ep_title, ep_airdate):
    return '|%s|%s|%s|%s|%s|%s|%s|' % (video_type, title, year, season, episode, ep_title, ep_airdate)




def get_link(url,movie_title,thumb,media):
    #kodi.log("Name IS NOW = " + movie_title)
    hmf = urlresolver.HostedMediaFile(url)
    ##########################################
    if hmf:
        try:
            url = urlresolver.resolve(url)
            params = {'url':url, 'title':movie_title, 'thumb':thumb}
            listitem = xbmcgui.ListItem(path=url, iconImage=thumb, thumbnailImage=thumb)
            listitem.setProperty('fanart_image', fanart)

            listitem.setPath(url)
            listitem.setInfo('video', params)

            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
            movie_name = movie_title[:-6]
            movie_name = '"'+movie_name+'"'
            movie_year_full = movie_title[-6:]
            movie_year = movie_year_full.replace('(','').replace(')','')
            if kodi.get_setting('trakt_oauth_token'):
                xbmc.sleep(30000)
                kodi.log( "Velocity: Movie Scrobble  Start")
                try:
                    trakt_auth.start_movie_watch(movie_name,movie_year)
                except Exception as e:
                    log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
                    if kodi.get_setting('error_notify') == "true":
                        kodi.notify(header='Scrobble not loggged', msg='%s  %s' % (str(e), ''), duration=5000, sound=None)
            xbmc.sleep(30000)
            if kodi.get_setting('trakt_oauth_token'):
                check_player(movie_name,movie_year)
        except Exception as e:
            log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
            kodi.notify(header='Try Another Source', msg='Link Removed or Failed', duration=4000, sound=None)

    if not hmf:
        try:
            params = {'url':url, 'title':movie_title, 'thumb':thumb}
            addon.add_video_item(params, {'title':movie_title}, img=thumb)
            liz=xbmcgui.ListItem(movie_title, iconImage="DefaultFolder.png", thumbnailImage=thumb)
            xbmc.sleep(1000)
            liz.setPath(str(url))
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
            #xbmc.Player ().play(url, liz, False)
            movie_name = movie_title[:-6]
            movie_name = '"'+movie_name+'"'
            movie_year_full = movie_title[-6:]
            movie_year = movie_year_full.replace('(','').replace(')','')
            if kodi.get_setting('trakt_oauth_token'):
                xbmc.sleep(30000)
                print "Velocity: Movie Scrobble  Start"
                try:
                    trakt_auth.start_movie_watch(movie_name,movie_year)
                except Exception as e:
                    log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
                    if kodi.get_setting('error_notify') == "true":
                        kodi.notify(header='Scrobble not loggged', msg='%s  %s' % (str(e), ''), duration=5000, sound=None)

            xbmc.sleep(30000)
            if kodi.get_setting('trakt_oauth_token'):
                check_player(movie_name,movie_year)
        except Exception as e:
            log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
            kodi.notify(header='Try Another Source', msg='Link Removed or Failed', duration=4000, sound=None)




def get_tv_link(url,movie_title,thumb,media):
    hmf = urlresolver.HostedMediaFile(url)
    ##########################################
    if hmf:
        url = urlresolver.resolve(url)
    if not hmf:
        url = url
    try:

        params = {'url': url, 'title': media, 'thumb': thumb}
        listitem = xbmcgui.ListItem(path=url, iconImage=thumb, thumbnailImage=thumb)
        listitem.setProperty('fanart_image', fanart)
        listitem.setPath(url)
        listitem.setInfo('video', params)

        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
        movie_name = movie_title[:-6]
        movie_name = '"'+movie_name+'"'
        movie_year_full = movie_title[-6:]
        movie_year = movie_year_full.replace('(','').replace(')','')
        if kodi.get_setting('trakt_oauth_token'):
            xbmc.sleep(30000)
            log_utils.log("Velocity: TV Show Scrobble  Start")
            try:
                trakt_auth.start_tv_watch(movie_name,media)
            except Exception as e:
                    log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
                    if kodi.get_setting('error_notify') == "true":
                        kodi.notify(header='Scrobble not loggged', msg='%s  %s' % (str(e), ''), duration=5000, sound=None)
        xbmc.sleep(30000)
        if kodi.get_setting('trakt_oauth_token'):
            check_tv_player(movie_name,media)

    except Exception as e:
            log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
            kodi.notify(header='Try Another Source', msg='Link Removed or Failed', duration=4000, sound=None)

class Player(xbmc.Player):
    def __init__(self):
        log_utils.log('Velocity Service: starting...')
        xbmc.Player.__init__(self)
        self.win = xbmcgui.Window(10000)
        #self.reset()

    def onPlayBackStarted(self):
        log_utils.log('Service: Playback Started')


    def onPlayBackStopped(self):
        log_utils.log('Service: Playback Stopped')
        #print" RUN A STOP COMMAND"

    def onPlayBackEnded(self):
        log_utils.log('Service: Playback Ended')

        self.onPlayBackStopped()


def check_player(name,year):

    monitor = Player()

    errors = 0
    while not xbmc.abortRequested:
        try:
            #print"CHECK ONE"
            isPlaying = monitor.isPlaying()
            if  monitor.isPlayingVideo():
                monitor._lastPos = monitor.getTime()
               # print  monitor._lastPos
            else:
                print "Velocity: Scrobble Movie End"
                trakt_auth.stop_movie_watch(name,year)
                break
        except Exception as e:
            errors += 1
            if errors >= MAX_ERRORS:
                log_utils.log('Service: Error (%s) received..(%s/%s)...Ending Service...' % (e, errors, MAX_ERRORS), log_utils.LOGERROR)
                break
            else:
                log_utils.log('Service: Error (%s) received..(%s/%s)...Continuing Service...' % (e, errors, MAX_ERRORS), log_utils.LOGERROR)
        else:
            errors = 0

        xbmc.sleep(1000)



def check_tv_player(name,media):

    monitor = Player()

    errors = 0
    while not xbmc.abortRequested:
        try:
            isPlaying = monitor.isPlaying()
            if  monitor.isPlayingVideo():
                monitor._lastPos = monitor.getTime()
                #print  monitor._lastPos
            else:
                print "Velocity: Scrobble TV Show End"
                trakt_auth.stop_tv_watch(name,media)
                break
        except Exception as e:
            errors += 1
            if errors >= MAX_ERRORS:
                log_utils.log('Service: Error (%s) received..(%s/%s)...Ending Service...' % (e, errors, MAX_ERRORS), log_utils.LOGERROR)
                break
            else:
                log_utils.log('Service: Error (%s) received..(%s/%s)...Continuing Service...' % (e, errors, MAX_ERRORS), log_utils.LOGERROR)
        else:
            errors = 0

        xbmc.sleep(1000)


#######Real Debrid Check
def apply_urlresolver(hosters):
    filter_debrid = kodi.get_setting('filter_debrid') == 'true'
    show_debrid = kodi.get_setting('show_debrid') == 'true'
    if not filter_debrid and not show_debrid:
        print "RETURNING NON FILTERED"
        return hosters
## New Resolver
    try:
        import urlresolver.plugnplay
        resolvers = urlresolver.plugnplay.man.implementors(urlresolver.UrlResolver)
        debrid_resolvers = [resolver for resolver in resolvers if resolver.isUniversal() and resolver.get_setting('enabled') == 'true']
    except:
        import urlresolver
        debrid_resolvers = [resolver() for resolver in urlresolver.relevant_resolvers(order_matters=True) if resolver.isUniversal()]
##   End New Resolver
    filtered_hosters = []
    debrid_hosts = {}
    unk_hosts = {}
    known_hosts = {}


    for hoster in hosters:
        #print "HOSTERS ARE: "+str(hoster)
        if 'direct' in hoster and hoster['direct'] == False and hoster['host']:
            host = hoster['host']
            host = (host.lower())
            #
            if kodi.get_setting('filter_debrid')=='true':
                if host in unk_hosts:
                    # log_utils.log('Unknown Hit: %s from %s' % (host, hoster['class'].get_name()), log_utils.LOGDEBUG)
                    unk_hosts[host] += 1
                    continue
                elif host in known_hosts:
                    # log_utils.log('Known Hit: %s from %s' % (host, hoster['class'].get_name()), log_utils.LOGDEBUG)
                    known_hosts[host] += 1
                    filtered_hosters.append(hoster)
                else:
                    hmf = urlresolver.HostedMediaFile(host=host, media_id='dummy')  # use dummy media_id to force host validation
                    if hmf:
                        # log_utils.log('Known Miss: %s from %s' % (host, hoster['class'].get_name()), log_utils.LOGDEBUG)
                        known_hosts[host] = known_hosts.get(host, 0) + 1
                        filtered_hosters.append(hoster)
                    else:
                        # log_utils.log('Unknown Miss: %s from %s' % (host, hoster['class'].get_name()), log_utils.LOGDEBUG)
                        unk_hosts[host] = unk_hosts.get(host, 0) + 1
                        continue
            else:
                filtered_hosters.append(hoster)

            if host in debrid_hosts:
                log_utils.log('Debrid cache found for %s: %s' % (host, debrid_hosts[host]), log_utils.LOGDEBUG)
                hoster['debrid'] = debrid_hosts[host]
                #print debrid_hosts[host]
            else:
                temp_resolvers = []
                for resolver in debrid_resolvers:
                    if resolver.valid_url('', host):
                        #print resolver.name
                        rname= resolver.name.replace('Real-Debrid','RD').replace('Premiumize.me','PRE')
                        temp_resolvers.append(rname.upper())
                        #temp_resolvers.append(resolver.name.upper())
                        if kodi.get_setting('debug') == "true":
                            print '%s supported by: %s' % (host, temp_resolvers)
                        debrid_hosts[host] = temp_resolvers
                    else:
                         hoster['debrid'] = ''
                if temp_resolvers:
                    hoster['debrid'] = temp_resolvers
                    #print temp_resolvers
        else:
            filtered_hosters.append(hoster)

    #log_utils.log('Discarded Hosts: %s' % (sorted(unk_hosts.items(), key=lambda x: x[1], reverse=True)), xbmc.LOGDEBUG)
    if kodi.get_setting('debug') == "true":
        kodi.log( "FILTERED HOSTERS ARE =" +str(filtered_hosters))
    return filtered_hosters


#################Scraper Functions###################################
def go_ice(video_type, title, year):

    if kodi.get_setting('ice_films') == 'true':
        icesearch = icefilms.Scraper()
        icesource = icesearch.search(video_type, title, year)
        for e in icesource:
            icesources = icesearch.get_sources(e)
            #total_items = total_items + len(icesources)
            all_source.append(icesources)
    else:
        sources = []
        all_source.append(sources)

def go_prime(video_type, title, year):

    if kodi.get_setting('primewire') == 'true':
        primesearch = primewire.Scraper()
        primesource = primesearch.search(video_type, title, year)
        for e in primesource:
            primesources = primesearch.get_sources(e)
            #total_items = total_items + len(primesources)
            all_source.append(primesources)
    else:
        sources = []
        all_source.append(sources)

def go_iwatch(video_type, title, year):

    if kodi.get_setting('iwatchon') == 'true':
        iwatchsearch = iwatchonline.Scraper()
        iwatchsource = iwatchsearch.search(video_type, title, year)
        for e in iwatchsource:
            iwatchsources = iwatchsearch.get_sources(e, video_type)
            #total_items = total_items + len(iwatchsources)
            all_source.append(iwatchsources)
    else:
        sources = []
        all_source.append(sources)

def go_afdah(video_type, title, year):

    if kodi.get_setting('afdah') == 'true':
        afsearch = afdah_scraper.Scraper()
        afsource = afsearch.search(video_type, title, year)
        for e in afsource:
            afdahsources = afsearch.get_sources(e)
            #total_items = total_items + len(afdahsources)
            all_source.append(afdahsources)
    else:
        sources = []
        all_source.append(sources)

def go_putlocker(video_type, title, year):

    if kodi.get_setting('putlocker') == 'true':
        putsearch = putlocker_both.Scraper()
        putsource = putsearch.search(video_type, title, year)
        for e in putsource:
            putsources = putsearch.get_sources(e)
            #total_items = total_items + len(putsources)
            all_source.append(putsources)
    else:
        sources = []
        all_source.append(sources)

#############TV SCRAPERS################

def go_ice_tv(video_type, title, year,name):
    if kodi.get_setting('ice_films') == 'true':
        icesearch = icefilms.Scraper()
        icesource = icesearch.search(video_type, title, year)
        for e in icesource:
            url = e['url']
            # TV MAIN URL RETURNED HERE
            newseas = re.compile('S(.+?)E(.+?)  (?P<name>[A-Za-z\t .]+)').findall(name)
            for sea, epi, epi_title in newseas:
                video = make_vid_params('Episode', title, year, sea, epi, epi_title, '')
                iceepi = icesearch._get_episode_url(url, video, sea, epi)
                icehosters = icesearch.get_sources(iceepi)
                all_source.append(icehosters)
    else:
        sources = []
        all_source.append(sources)

def go_iwatch_tv(video_type, title, year,name):
    if kodi.get_setting('iwatchon') == 'true':
        iwatchsearch = iwatchonline.Scraper()
        iwatchsource = iwatchsearch.search(video_type, title, year)
        for e in iwatchsource:
            url = e['url']
            # TV MAIN URL RETURNED HERE
            newseas = re.compile('S(.+?)E(.+?)  (?P<name>[A-Za-z\t .]+)').findall(name)
            for sea, epi, epi_title in newseas:
                video = make_vid_params('Episode', title, year, sea, epi, epi_title, '')
                iwatchepi = iwatchsearch._get_episode_url(url, video, sea, epi)
                iwatchhosters = iwatchsearch.get_sources(iwatchepi, video_type)
                all_source.append(iwatchhosters)
    else:
        sources = []
        all_source.append(sources)

def go_prime_tv(video_type, title, year,name):
    if kodi.get_setting('primewire') == 'true':
        primesearch = primewire.Scraper()
        primesource = primesearch.search(video_type, title, year)
        for e in primesource:
            url = e['url']
            # TV MAIN URL RETURNED HERE
            newseas = re.compile('S(.+?)E(.+?)  (?P<name>[A-Za-z\t .]+)').findall(name)
            for sea, epi, epi_title in newseas:
                video = make_vid_params('Episode', title, year, sea, epi, epi_title, '')
                primeepi = primesearch._get_episode_url(url, video, sea, epi)
                primehosters = primesearch.get_sources(primeepi)
                all_source.append(primehosters)
    else:
        sources = []
        all_source.append(sources)

def go_putlocker_tv(video_type, title, year,name):
    if kodi.get_setting('putlocker') == 'true':
        putsearch = putlocker_both.Scraper()
        putsource = putsearch.search(video_type, title, year)
        for e in putsource:
            url = e['url']
            # TV MAIN URL RETURNED HERE
            newseas = re.compile('S(.+?)E(.+?)  (?P<name>[A-Za-z\t .]+)').findall(name)
            for sea, epi, epi_title in newseas:
                video = make_vid_params('Episode', title, year, sea, epi, epi_title, '')
                putepi = putsearch._get_episode_url(url, video, sea, epi)
                puthosters = putsearch.get_sources(putepi)
                all_source.append(puthosters)
    else:
        sources = []
        all_source.append(sources)