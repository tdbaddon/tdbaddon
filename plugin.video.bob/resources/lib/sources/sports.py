# coding=utf-8
"""Collection of functions related to scraping sport sources"""
import time

import requests
from BeautifulSoup import BeautifulSoup
from resources.lib.modules import proxy
from datetime import datetime, timedelta


def get_acesoplisting():
    """
get listings from acespoplisting.in
    :return: listing from website in bob list xml format
    :rtype: str
    """
    import xbmc
    xml = "<fanart>https://www.dropbox.com/s/x3zg9ovot6vipjh/smoke_men-wallpaper-1920x1080.jpg?raw=true</fanart>\n\n\n" \
          "<item>\n" \
          "\t<title>[COLORred]Will require Plexus addon to watch Acestream links.[/COLOR]</title>\n" \
          "\t<link> </link>\n" \
          "\t<thumbnail> </thumbnail>\n" \
          "</item>\n\n" \
          "<item>\n" \
          "\t<title>[COLORred]Download in Community Portal.[/COLOR]</title>\n" \
          "\t<link> </link>\n" \
          "\t<thumbnail> </thumbnail>\n" \
          "</item>\n\n" \
          "<item>\n" \
          "\t<title>[COLORpurple]############## [COLORcyan]Live Sporting Events[COLORpurple] ##############[/COLOR]</title>\n" \
          "\t<link> </link>\n" \
          "\t<thumbnail> </thumbnail>\n" \
          "</item>\n"

    try:
        html = proxy.get2("http://www.acesoplisting.in/", 'class="table-responsive"')
        scraped_html = BeautifulSoup(html)
        table = scraped_html.findAll("table", attrs={'class': 'table table-striped table-bordered table-condensed'})[-1]
        rows = table.findAll("tr")
        is_today = False
        day_xml = ""
        found_links = False
        for row in rows:
            headers = row.findAll("th")
            cells = row.findAll("td")
            if len(headers) > 0:
                date = headers[0].text.strip()
                today_number = time.gmtime().tm_mday
                if str(today_number) in date:
                    is_today = True
                if is_today:
                    day_xml = "\n" \
                              "<item>\n" \
                              "\t<title>%s</title>\n" \
                              "\t<link></link>\n" \
                              "\t<thumbnail></thumbnail>\n" \
                              "</item>\n" % date
            elif is_today:
                if len(cells) < 5:
                    continue
                event_time = cells[0].text.strip()
                split_time = event_time.split(":")
                event_hours = int(split_time[0])
                event_minutes = split_time[1]
                est_event_hours = event_hours - 4

                if est_event_hours >= 4:
                    xml += day_xml
                    day_xml = ""
                if est_event_hours < 0:
                    est_event_hours = 24 - abs(est_event_hours)
                if est_event_hours >= 12:
                    if not est_event_hours == 12:
                        est_event_hours -= 12
                    suffix = "PM"
                else:
                    suffix = "AM"
                event_time = "%s:%s %s" % (est_event_hours, event_minutes, suffix)

                sport = cells[1].text.strip()
                match = cells[2].text.replace("\n", "").strip()
                match = " ".join(match.split())
                league = cells[3].text.strip()
                if league == "USA NFL":
                    thumbnail = "http://organizationalphysics.com/wp-content/uploads/2013/12/NFLShield.png"
                elif league == "WWE":
                    thumbnail = "http://i.imgur.com/UsYsZ.png"
                elif league == "USA NBA":
                    thumbnail = "https://lh3.googleusercontent.com/gfS15xuST6IP3e-ZDy63XLNl-ZxxTqo-NxXuIy5dKWQIjX_8s_T0Sz1mgTc0-78juBc=w170"
                elif league == "PREMIER LEAGUE":
                    thumbnail = "https://d1fy1ym40biffm.cloudfront.net/images/logos/leagues/f633765f43fafaf2120a1bb9b2a7babd4f0d9380ed1bc72925c29ba18ace9269.png"
                elif sport == "SOCCER":
                    thumbnail = "http://themes.zozothemes.com/mist/sports/wp-content/uploads/sites/6/2015/10/soccer-player.png"
                elif sport == "MOTOGP":
                    thumbnail = "https://www.bestvpnprovider.com/wp-content/uploads/2015/05/MotoGp_Logo.jpg"
                elif sport == "FORMULA 1":
                    thumbnail = "http://d3t1wwu6jp9wzs.cloudfront.net/wp-content/uploads/2016/05/photo.jpg"
                elif sport == "UFC":
                    thumbnail = "http://img3.wikia.nocookie.net/__cb20130511014401/mixedmartialarts/images/c/c5/UFC_logo.png"
                else:
                    thumbnail = ""

                links = cells[4].findAll("a")

                if len(links) != 0:
                    found_links = True
                for link in links:
                    href = link["href"]
                    if "acestream://" in href:
                        xml += "\n" \
                               "<item>\n" \
                               "\t<title>[COLORlime]%s -[COLORorange]  %s[COLORred]  Acestreams[COLORwhite] %s EST[/COLOR]</title>\n" \
                               "\t<link>plugin://program.plexus/?mode=1&url=%s&name=TA+Sports</link>\n" \
                               "\t<thumbnail>%s</thumbnail>\n" \
                               "</item>\n" % (sport, match, event_time, href, thumbnail)
                    elif "sop://" in href:
                        xml += "\n" \
                               "<item>\n" \
                               "\t<title>[COLORlime]%s -[COLORorange]  %s[COLORblue]  Sopcast[COLORwhite] %s EST[/COLOR]</title>\n" \
                               "\t<link>plugin://program.plexus/?url=%s&mode=2&name=TASPORTS</link>\n" \
                               "\t<thumbnail>%s</thumbnail>\n" \
                               "</item>\n" % (sport, match, event_time, href, thumbnail)
        if not found_links:
            xml = "<fanart>https://www.dropbox.com/s/x3zg9ovot6vipjh/smoke_men-wallpaper-1920x1080.jpg?raw=true</fanart>\n\n\n" \
                  "<item>\n" \
                  "\t<title>[COLORred]Will require Plexus addon to watch Acestream links.[/COLOR]</title>\n" \
                  "\t<link> </link>\n" \
                  "\t<thumbnail> </thumbnail>\n" \
                  "</item>\n\n" \
                  "<item>\n" \
                  "\t<title>[COLORred]Download in Community Portal.[/COLOR]</title>\n" \
                  "\t<link> </link>\n" \
                  "\t<thumbnail> </thumbnail>\n" \
                  "</item>\n\n" \
                  "<item>\n" \
                  "\t<title>[COLORpurple]############## [COLORcyan]Live Sporting Events[COLORpurple] ##############[/COLOR]</title>\n" \
                  "\t<link> </link>\n" \
                  "\t<thumbnail> </thumbnail>\n" \
                  "</item>\n" \
                  "\n" \
                  "<item>\n" \
                  "\t<title>Currently No Games Available</title>\n" \
                  "\t<link></link>\n" \
                  "\t<thumbnail></thumbnail>\n" \
                  "</item>\n"
        return xml
    except:
        pass


def get_hockey_recaps(page):
    """
get game recap listings from nhl
    :param str page: page of results to scrape
    :return: listing from website in bob list xml format
    :rtype: str
    """

    xml = "<fanart>http://www.shauntmax30.com/data/out/29/1189697-100-hdq-nhl-wallpapers.png</fanart>\n\n\n" \
          "<item>\n" \
          "\t<title>[COLORpurple]############## [COLORcyan]NHL Condensed Games[COLORpurple] ##############[/COLOR]</title>\n" \
          "\t<link></link>\n" \
          "\t<thumbnail></thumbnail>\n" \
          "</item>\n\n"

    recaps_json = requests.get(
        "http://search-api.svc.nhl.com/svc/search/v2/nhl_global_en/tag/content/gameRecap?page={0}&sort=new&type=video&hl=false&expand=image.cuts.640x360,image.cuts.1136x640".format(
            page)).json()
    for doc in recaps_json['docs']:
        referer = "{0}?tag=content&tagValue=gameRecap".format(doc['url'])
        asset_id = doc['asset_id']
        title = doc['title'].replace('Recap: ', '')
        game_date = None
        tags = doc["tags"]
        for tag in tags:
            if "type" in tag and tag["type"].lower() == "calendarEventId".lower() and "displayName" in tag:
                title = tag["displayName"]
            if "type" in tag and tag["type"].lower() == "gameId".lower() and "displayName" in tag:
                game_date_tag = tag["displayName"].split("-")
                if len(game_date_tag) > 1:
                    game_date = game_date_tag[1]
        if game_date:
            title = "{0} ({1})".format(title, game_date)
        image = doc['image']['cuts']['640x360']['src']
        try:
            url = "http://nhl.bamcontent.com/nhl/id/v1/{0}/details/web-v1.json".format(asset_id)
            video_json = requests.get(url, headers={'Referer': referer}).json()
        except:
            continue
        max_width = 0
        selected_url = ""
        for video_info in video_json['playbacks']:
            width = video_info['width']
            height = video_info['height']
            if width and width != 'null' and height and height != 'null':
                if width >= max_width:
                    max_width = width
                    selected_url = video_info["url"]
        xml += "<item>\n" \
               "\t<title>{0}</title>\n" \
               "\t<link>{1}</link>\n" \
               "\t<thumbnail>{2}</thumbnail>\n" \
               "</item>\n".format(title, selected_url, image)

    xml += "<dir>\n" \
           "\t<title>Next Page >></title>\n" \
           "\t<link>sport_hockeyrecaps{0}</link>\n" \
           "\t<thumbnail></thumbnail>\n" \
           "</dir>\n".format(int(page) + 1)

    return xml


def get_nhl_games(epg_date=""):
    import xbmc
    import string
    if epg_date == "":
        epg_date = datetime.now()
        now_time = time.gmtime().tm_hour
        if now_time <= 4 or now_time >= 23:
            epg_date -= timedelta(hours=4)
        epg_date = epg_date.strftime("%Y-%m-%d")
    xml = ""
    epgurl = "http://statsapi.web.nhl.com/api/v1/schedule?startDate=%s&endDate=%s&expand=schedule.teams,schedule.game.content.media.epg" \
             % (epg_date, epg_date)
    content = requests.get(epgurl).json()
    if not "totalItems" in content or content['totalItems'] <= 0 or not "dates" in content or len(
            content["dates"]) == 0:
        return xml
    start_xmls = {}
    for game_date in content["dates"]:
        if game_date["totalItems"] > 0:
            xml += "\n" \
                   "<item>\n" \
                   "\t<title>[COLORred]%s NHL Schedule in 5000k[/COLOR]</title>\n" \
                   "\t<link></link>\n" \
                   "\t<thumbnail>https://upload.wikimedia.org/wikipedia/en/thumb/e/e4/NHL_Logo_former.svg/996px-NHL_Logo_former.svg.png</thumbnail>\n" \
                   "\t<fanart>http://i.imgur.com/HI05fqX.jpg</fanart>\n" \
                   "</item>\n" % (datetime.strptime(game_date["date"], "%Y-%m-%d").strftime("%A, %b %d"))
            for game in game_date["games"]:
                try:
                    start_time = datetime.strptime(game["gameDate"], "%Y-%m-%dT%H:%M:%SZ")
                    start_time -= timedelta(hours=5)
                    start_time = start_time.strftime("%I:%M %p EST")
                    if not start_time in start_xmls:
                        start_xmls[start_time] = "\n" \
                                                 "<item>\n" \
                                                 "\t<title>[COLORred]| [COLORorange]%s [COLORred]|[/COLOR]</title>\n" \
                                                 "\t<link></link>\n" \
                                                 "\t<thumbnail>https://upload.wikimedia.org/wikipedia/en/thumb/e/e4/NHL_Logo_former.svg/996px-NHL_Logo_former.svg.png</thumbnail>\n" \
                                                 "\t<fanart>http://i.imgur.com/HI05fqX.jpg</fanart>\n" \
                                                 "</item>\n" % (start_time)
                    home = game['teams']['home']['team']['name'].encode("utf-8").replace("\xc3\xa9", "e")
                    away = game['teams']['away']['team']['name'].encode("utf-8").replace("\xc3\xa9", "e")
                    title = "[COLORgray]%s @ %s[/COLOR]" % (away, home)
                    image = "https://upload.wikimedia.org/wikipedia/en/thumb/e/e4/NHL_Logo_former.svg/996px-NHL_Logo_former.svg.png"
                    for stream in game["content"]["media"]["epg"]:
                        if stream["title"] == "Recap":
                            try:
                                image = stream['items'][0]['image']['cuts']['640x360']['src']
                            except:
                                pass

                    for stream in game["content"]["media"]["epg"]:
                        if stream["title"] == "NHLTV":
                            game_title = ""
                            home_content_url = ""
                            away_content_url = ""
                            for item in stream['items']:
                                game_title = item["mediaFeedType"].lower()
                                if game_title not in ["home", "away"]:
                                    continue
                                feed_id = item["mediaPlaybackId"]
                                if game_title == "home":
                                    home_content_url = "http://mf.svc.nhl.com/m3u8/%s/%s%s" % (epg_date, feed_id, 'l3c')
                                elif game_title == "away":
                                    away_content_url = "http://mf.svc.nhl.com/m3u8/%s/%s%s" % (epg_date, feed_id, 'l3c')
                            start_xmls[start_time] += "\n" \
                                                      "<dir>\n" \
                                                      "\t<title>%s</title>\n" \
                                                      "\t<link>sport_nhl_home_away(%s,%s,%s,%s)</link>\n" \
                                                      "\t<thumbnail>%s</thumbnail>\n" \
                                                      "\t<fanart>http://i.imgur.com/HI05fqX.jpg</fanart>\n" \
                                                      "</dir>\n" % (
                                                          title, title, home_content_url, away_content_url, image,
                                                          image)
                except:
                    continue
            keys = sorted(start_xmls.keys())
            for key in keys:
                xml += start_xmls[key]

            return xml
        else:
            return ""


def get_nhl_home_away(title, home_content_url, away_content_url, image):
    import xbmc
    import random, string
    seed = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(241))
    xml = ""
    for content_url in [home_content_url, away_content_url]:
        if content_url == home_content_url:
            game_title = "HOME"
        elif content_url == away_content_url:
            game_title = "AWAY"
        else:
            game_title = title
        try:
            request = requests.get(content_url)
            if request.status_code < 400:
                play_url = request.content
            else:
                play_url = ""
                game_title += " NOT PLAYING YET"
        except:
            continue
        if not play_url is "" and not requests.request('HEAD', play_url, cookies={'mediaAuth': seed}).status_code < 400:
            play_url = play_url.replace('l3c', 'akc')
        game_xml = "<item>\n" \
                   "\t<title>{0}</title>\n" \
                   "\t<link>{1}</link>\n" \
                   "\t<thumbnail>{2}</thumbnail>\n" \
                   "\t<fanart>http://i.imgur.com/HI05fqX.jpg</fanart>\n" \
                   "</item>\n".format(game_title, play_url, image)
        xml += game_xml
    return xml


def get_nfl_games(season="", week=""):
    import xmltodict
    import xbmc
    username = 'condor13'
    password = 'condor13'

    base_url = 'https://gamepass.nfl.com/nflgp'
    servlets_url = base_url + '/servlets'
    simlple_console_url = servlets_url + '/simpleconsole'
    login_url = base_url + '/secure/nfllogin'
    session = requests.Session()

    session.post(login_url, data={'username': username, 'password': password})  # login

    simlple_console_data = session.post(simlple_console_url, data={'isflex': 'true'}).content
    simlple_console_dict = xmltodict.parse(simlple_console_data)
    current_season = simlple_console_dict['result']['currentSeason']
    current_week = simlple_console_dict['result']['currentWeek']
    if season == "":
        season = current_season
    if week == "":
        week = current_week

    game_data = session.post(servlets_url + '/games',
                             data={'isFlex': 'true', 'season': season, 'week': week}).content

    game_data_dict = xmltodict.parse(game_data)['result']
    games = game_data_dict['games']['game']
    if isinstance(games, dict):
        games = [games]
    xml = ""
    start_xmls = {}
    thumbnail = "http://www.officialpsds.com/images/thumbs/NFL-Logo-psd95853.png"
    fanart = "http://wallpapercave.com/wp/8iHFIg1.png"
    for game in games:
        if not 'hasProgram' in game:  # no stream
            continue
        if "programId" in game:  # only full games
            homecity = game["homeTeam"]["city"] or ""
            homename = game["homeTeam"]["name"] or ""
            home = "%s %s" % (homecity, homename)
            awaycity = game["awayTeam"]["city"] or ""
            awayname = game["awayTeam"]["name"] or ""
            away = "%s %s" % (awaycity, awayname)
            start_time = datetime(*(time.strptime(game['gameTimeGMT'], '%Y-%m-%dT%H:%M:%S.000')[0:6]))
            start_time -= timedelta(hours=5)
            start_time = start_time.strftime("%Y-%m-%d %I:%M %p EST")
            start_xmls[start_time] = "\n" \
                                     "<item>\n" \
                                     "\t<title>[COLORred]| [COLORorange]%s [COLORred]|[/COLOR]</title>\n" \
                                     "\t<link></link>\n" \
                                     "\t<thumbnail>%s</thumbnail>\n" \
                                     "\t<fanart>%s</fanart>\n" \
                                     "</item>\n" % (start_time, thumbnail, fanart)
            game_title = home + " vs. " + away
            game_title = " ".join(game_title.split())
            game_id = game["id"]

            start_xmls[start_time] += "<dir>\n" \
                                      "\t<title>{0}</title>\n" \
                                      "\t<link>sport_nfl_get_game({1})</link>\n" \
                                      "\t<thumbnail>{2}</thumbnail>\n" \
                                      "\t<fanart>{3}</fanart>\n" \
                                      "</dir>\n".format(game_title, game_id, thumbnail, fanart)

    keys = sorted(start_xmls.keys())
    for key in keys:
        xml += start_xmls[key]

    return xml


def get_nfl_game(game_id):
    import xmltodict
    import m3u8
    import urllib
    import xbmc
    streams = {}
    username = 'condor13'
    password = 'condor13'

    base_url = 'https://gamepass.nfl.com/nflgp'
    servlets_url = base_url + '/servlets'
    simlple_console_url = servlets_url + '/simpleconsole'
    login_url = base_url + '/secure/nfllogin'
    session = requests.Session()

    session.post(login_url, data={'username': username, 'password': password})  # login
    simlple_console_data = session.post(simlple_console_url, data={'isflex': 'true'}).content
    simlple_console_dict = xmltodict.parse(simlple_console_data)
    current_season = simlple_console_dict['result']['currentSeason']
    current_week = simlple_console_dict['result']['currentWeek']

    thumbnail = "http://www.officialpsds.com/images/thumbs/NFL-Logo-psd95853.png"
    fanart = "http://wallpapercave.com/wp/8iHFIg1.png"

    url = servlets_url + '/publishpoint'

    headers = {'User-Agent': 'iPad'}
    post_data = {'id': game_id, 'type': 'game', 'nt': '1', 'gt': 'archive'}
    m3u8_data = session.post(url, data=post_data, headers=headers).content

    try:
        m3u8_dict = xmltodict.parse(m3u8_data)['result']
    except:
        post_data = {'id': game_id, 'type': 'game', 'nt': '1', 'gt': 'live'}
        m3u8_data = session.post(url, data=post_data, headers=headers).content
        m3u8_dict = xmltodict.parse(m3u8_data)['result']

    m3u8_url = m3u8_dict['path'].replace('_ipad', '')
    m3u8_param = m3u8_url.split('?', 1)[-1]
    m3u8_header = {'Cookie': 'nlqptid=' + m3u8_param,
                   'User-Agent': 'Safari/537.36 Mozilla/5.0 AppleWebKit/537.36 Chrome/31.0.1650.57',
                   'Accept-encoding': 'identity, gzip, deflate',
                   'Connection': 'keep-alive'}

    try:
        m3u8_manifest = session.get(m3u8_url).content
    except:
        m3u8_manifest = False

    if m3u8_manifest:
        m3u8_obj = m3u8.loads(m3u8_manifest)
        if m3u8_obj.is_variant:  # if this m3u8 contains links to other m3u8s
            for playlist in m3u8_obj.playlists:
                bitrate = int(playlist.stream_info.bandwidth) / 1000
                streams[str(bitrate)] = m3u8_url[:m3u8_url.rfind('/') + 1] + playlist.uri + '?' + m3u8_url.split('?')[
                    1] + '|' + urllib.urlencode(m3u8_header)
        else:
            game_xml = "<item>\n" \
                       "\t<title>stream</title>\n" \
                       "\t<link>{1}</link>\n" \
                       "\t<thumbnail>{2}</thumbnail>\n" \
                       "\t<fanart>{3}</fanart>\n" \
                       "</item>\n".format(m3u8_url, thumbnail, fanart)
            return game_xml

    xml = ''

    keys = sorted(streams.keys(), key=lambda key: int(key))
    for key in keys:
        game_xml = "<item>\n" \
                   "\t<title>{0} kbps</title>\n" \
                   "\t<link>{1}</link>\n" \
                   "\t<thumbnail>{2}</thumbnail>\n" \
                   "\t<fanart>{3}</fanart>\n" \
                   "</item>\n".format(key, streams[key], thumbnail, fanart)

        xml += game_xml
    return xml


def get_condensed_nfl_games(season="", week=""):
    import xmltodict
    username = 'condor13'
    password = 'condor13'

    base_url = 'https://gamepass.nfl.com/nflgp'
    servlets_url = base_url + '/servlets'
    simlple_console_url = servlets_url + '/simpleconsole'
    login_url = base_url + '/secure/nfllogin'
    session = requests.Session()

    session.post(login_url, data={'username': username, 'password': password})  # login

    simlple_console_data = session.post(simlple_console_url, data={'isflex': 'true'}).content
    simlple_console_dict = xmltodict.parse(simlple_console_data)
    current_season = simlple_console_dict['result']['currentSeason']
    current_week = simlple_console_dict['result']['currentWeek']
    if season == "":
        season = current_season
    if week == "":
        week = current_week

    game_data = session.post(servlets_url + '/games',
                             data={'isFlex': 'true', 'season': season, 'week': week}).content
    game_data_dict = xmltodict.parse(game_data)['result']
    games = game_data_dict['games']['game']
    if isinstance(games, dict):
        games = [games]

    xml = ""
    start_xmls = {}
    thumbnail = "http://www.officialpsds.com/images/thumbs/NFL-Logo-psd95853.png"
    fanart = "http://wallpapercave.com/wp/8iHFIg1.png"
    for game in games:
        if not 'hasProgram' in game:  # no stream
            continue
        if "condensedId" in game:  # only condensed
            homecity = game["homeTeam"]["city"] or ""
            homename = game["homeTeam"]["name"] or ""
            home = "%s %s" % (homecity, homename)
            awaycity = game["awayTeam"]["city"] or ""
            awayname = game["awayTeam"]["name"] or ""
            away = "%s %s" % (awaycity, awayname)
            start_time = datetime(*(time.strptime(game['gameTimeGMT'], '%Y-%m-%dT%H:%M:%S.000')[0:6]))
            start_time -= timedelta(hours=5)
            start_time = start_time.strftime("%Y-%m-%d %I:%M %p EST")
            start_xmls[start_time] = "\n" \
                                     "<item>\n" \
                                     "\t<title>[COLORred]| [COLORorange]%s [COLORred]|[/COLOR]</title>\n" \
                                     "\t<link></link>\n" \
                                     "\t<thumbnail>%s</thumbnail>\n" \
                                     "\t<fanart>%s</fanart>\n" \
                                     "</item>\n" % (start_time, thumbnail, fanart)
            game_title = home + " vs. " + away
            game_title = " ".join(game_title.split())
            game_id = game["id"]

            start_xmls[start_time] += "<dir>\n" \
                                      "\t<title>{0}</title>\n" \
                                      "\t<link>sport_condensed_nfl_get_game({1})</link>\n" \
                                      "\t<thumbnail>{2}</thumbnail>\n" \
                                      "\t<fanart>{3}</fanart>\n" \
                                      "</dir>\n".format(game_title, game_id, thumbnail, fanart)

    keys = sorted(start_xmls.keys())
    for key in keys:
        xml += start_xmls[key]

    return xml


def get_condensed_nfl_game(game_id):
    import xmltodict
    import m3u8
    import urllib
    import xbmc
    streams = {}
    username = 'condor13'
    password = 'condor13'

    base_url = 'https://gamepass.nfl.com/nflgp'
    servlets_url = base_url + '/servlets'
    simlple_console_url = servlets_url + '/simpleconsole'
    login_url = base_url + '/secure/nfllogin'
    session = requests.Session()

    session.post(login_url, data={'username': username, 'password': password})  # login
    simlple_console_data = session.post(simlple_console_url, data={'isflex': 'true'}).content
    simlple_console_dict = xmltodict.parse(simlple_console_data)
    current_season = simlple_console_dict['result']['currentSeason']
    current_week = simlple_console_dict['result']['currentWeek']

    thumbnail = "http://www.officialpsds.com/images/thumbs/NFL-Logo-psd95853.png"
    fanart = "http://wallpapercave.com/wp/8iHFIg1.png"

    url = servlets_url + '/publishpoint'

    headers = {'User-Agent': 'iPad'}
    post_data = {'id': game_id, 'type': 'game', 'nt': '1', 'gt': 'condensed'}
    m3u8_data = session.post(url, data=post_data, headers=headers).content

    try:
        m3u8_dict = xmltodict.parse(m3u8_data)['result']
    except:
        return ""

    m3u8_url = m3u8_dict['path'].replace('_ipad', '')
    m3u8_param = m3u8_url.split('?', 1)[-1]
    m3u8_header = {'Cookie': 'nlqptid=' + m3u8_param,
                   'User-Agent': 'Safari/537.36 Mozilla/5.0 AppleWebKit/537.36 Chrome/31.0.1650.57',
                   'Accept-encoding': 'identity, gzip, deflate',
                   'Connection': 'keep-alive'}

    try:
        m3u8_manifest = session.get(m3u8_url).content
    except:
        m3u8_manifest = False

    if m3u8_manifest:
        m3u8_obj = m3u8.loads(m3u8_manifest)
        if m3u8_obj.is_variant:  # if this m3u8 contains links to other m3u8s
            for playlist in m3u8_obj.playlists:
                bitrate = int(playlist.stream_info.bandwidth) / 1000
                streams[str(bitrate)] = m3u8_url[:m3u8_url.rfind('/') + 1] + playlist.uri + '?' + m3u8_url.split('?')[
                    1] + '|' + urllib.urlencode(m3u8_header)
        else:
            game_xml = "<item>\n" \
                       "\t<title>stream</title>\n" \
                       "\t<link>{1}</link>\n" \
                       "\t<thumbnail>{2}</thumbnail>\n" \
                       "\t<fanart>{3}</fanart>\n" \
                       "</item>\n".format(m3u8_url, thumbnail, fanart)
            return game_xml

    xml = ''

    keys = sorted(streams.keys(), key=lambda key: int(key))
    for key in keys:
        game_xml = "<item>\n" \
                   "\t<title>{0} kbps</title>\n" \
                   "\t<link>{1}</link>\n" \
                   "\t<thumbnail>{2}</thumbnail>\n" \
                   "\t<fanart>{3}</fanart>\n" \
                   "</item>\n".format(key, streams[key], thumbnail, fanart)

        xml += game_xml
    return xml
