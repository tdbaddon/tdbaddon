import sys, re, base64

sys.argv = ['plugin.video.aftershock', '1']


try :
    params = {'tmdb': '362136', 'name': 'Prem Ratan Dhan Payo (2015)', 'title': 'Prem Ratan Dhan Payo', 'meta': '{"rating": "6.6", "tmdb": "362136", "code": "tt3595298", "imdb": "tt3595298", "year": "2015", "duration": "10440", "plot": "Loosely based on the novel The prince and the Pauper. Ever loving Prem is respected and loved by all and Vijay (also played by Salman Khan) is in the world of hatred and violence. They change their identities temporarily to discover the other side of the world.", "votes": "11", "title": "Prem Ratan Dhan Payo", "fanart": "http://image.tmdb.org/t/p/original/9fVjhznaYPcQF7eHZ08CkytmTbL.jpg", "mpaa": "NR", "writer": "Sooraj R. Barjatya", "poster": "http://image.tmdb.org/t/p/w500/8mfZyMKdyXGjwr27dCCBUp4fwVG.jpg", "director": "Sooraj R. Barjatya", "studio": "Fox Star Studios", "genre": "Drama / Action / Romance", "metacache": false, "lang": "hindi", "name": "Prem Ratan Dhan Payo (2015)", "premiered": "2015-11-11", "originaltitle": "Prem Ratan Dhan Payo", "cast": [["Salman Khan", "Prem/Vijay"], ["Sonam Kapoor", "Maithili"], ["Neil Nitin Mukesh", "Yuvraj Ajay Singh"], ["Anupam Kher", "Diwan"], ["Swara Bhaskar", "Chandrika"], ["Deepak Dobriyal", "Kanhaiya"], ["Arman Kohli", "Chirag Singh"], ["Manoj Joshi", "Bhandari"]], "tagline": "Loosely based on the novel The prince and the Pauper", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Prem+Ratan+Dhan+Payo+%282015%29"}', 'imdb': 'tt3595298', 'year': '2015', 'action': 'sources'}
    params = {'tmdb': '0', 'episode': '0', 'name': '27th September 2016', 'title': '27th September 2016', 'tvdb': '0', 'season': '0', 'tvshowtitle': 'Sasural Simar Ka', 'year': '0', 'date': '0', 'meta': '{"tvshowurl": "forums/3948-Sasural-Simar-Ka", "title": "27th September 2016", "url": "threads/957870-Sasural-Simar-Ka-27th-September-2016-Watch-Online?s=0d84ed1dab42c4a5abd7f366af8d4b53", "tvshowtitle": "Sasural Simar Ka", "next": "forums/3948-Sasural-Simar-Ka/page2?s=0d84ed1dab42c4a5abd7f366af8d4b53", "provider": "desirulez_tv", "duration": "1800", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Sasural+Simar+Ka", "name": "27th September 2016"}', 'imdb': '0', 'provider': 'desirulez_tv', 'action': 'sources', 'tvrage': '0', 'alter': '0'}
    params = {'tmdb': '388333', 'name': 'M.S. Dhoni: The Untold Story (2016)', 'title': 'M.S. Dhoni: The Untold Story', 'meta': '{"rating": "5.8", "code": "tt4169250", "tmdb": "388333", "imdb": "tt4169250", "year": "2016", "duration": "11040", "plot": "The film is based on the life of Indian cricketer and the current captain of the Indian national cricket team, Mahendra Singh Dhoni.", "votes": "2", "title": "M.S. Dhoni: The Untold Story", "fanart": "http://image.tmdb.org/t/p/original/2tTtuHpbROSqzqu8Zi6U0hZr6Gc.jpg", "tagline": "The man you know... The journey you don\'t.", "writer": "Neeraj Pandey / Nandu Kamte", "next": "http://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&languages=hi&count=40&start=1&start=1&sort=release_date,desc&page=2&ref_=adv_nxt", "poster": "http://image.tmdb.org/t/p/w500/311gCwnNJgyoNEPWR9GJ2JBGJAm.jpg", "director": "Neeraj Pandey", "studio": "Fox Star Studios", "genre": "Drama", "metacache": true, "premiered": "2016-09-02", "originaltitle": "M.S. Dhoni: The Untold Story", "cast": [["Anupam Kher", "Pan Singh"], ["Kiara Advani", "Sakshi Singh Rawat / Sakshi Singh Dhoni"], ["Sushant Singh Rajput", "M. S. Dhoni"], ["Herry Tangiri", "Yuvraj Singh (as Herry Tangri)"], ["Disha Patani", "Priyanka Jha"], ["Bhumika Chawla", "Jayanti Gupta, Dhoni\'s sister"], ["Rajesh Sharma", ""], ["John Abraham", "Himself (Cameo)"]], "mpaa": "UA", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=M.S.+Dhoni%3A+The+Untold+Story+%282016%29"}', 'imdb': 'tt4169250', 't': '20161003003606950000', 'year': '2016', 'action': 'play'}
    params = {'tmdb': '39083', 'tvdb': '273190', 'tvshowtitle': 'Sasural Simar Ka', 'year': '0', 'url': 'forums/3948-Sasural-Simar-Ka', 'imdb': 'tt1934806', 'provider': 'desirulez_tv', 'action': 'episodes', 'tvrage': '0'}
    params = {'action': 'playItem', 'source': '[{"debrid": "", "url": "http://streamin.to/embed-6qpnqixizf9r-730x480.html", "direct": false, "label": "06 | [B]IBOLLYTV[/B] | STREAMIN ", "source": "streamin.to", "parts": "1", "provider": "iBollyTV", "quality": ""}]', 'content': 'movie', 'title': 'M.S. Dhoni: The Untold Story'}
    params = {'tmdb': '0', 'episode': '0', 'name': '29th September 2016', 'title': '29th September 2016', 'tvdb': '0', 'season': '0', 'tvshowtitle': 'Sasural Simar Ka', 'year': '0', 'date': '0', 'meta': '{"tvshowurl": "forums/3948-Sasural-Simar-Ka", "title": "29th September 2016", "url": "threads/959493-Sasural-Simar-Ka-29th-September-2016-Watch-Online?s=83954be3616f4aab7e388876a7cb3a79", "tvshowtitle": "Sasural Simar Ka", "provider": "desirulez_tv", "duration": "1800", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Sasural+Simar+Ka", "name": "29th September 2016"}', 'imdb': '0', 'provider': 'desirulez_tv', 'action': 'addItem', 'tvrage': '0', 'alter': '0'}
    params = {'tmdb': '0', 'name': 'Bajrangi Bhaijaan (2015)', 'title': 'Bajrangi Bhaijaan', 'meta': '{"rating": "8.1", "votes": "43,778", "code": "tt3863552", "cast": [["Salman Khan", ""], ["Kareena Kapoor", ""], ["Nawazuddin Siddiqui", ""], ["Harshaali Malhotra", ""]], "plot": "A little mute girl from a Pakistan village gets lost on her return back from a trip to India. In Kurukshetra, she meets Pawan - a devout Hanuman Bakth - who is in the midst of a challenge posed by his lover\'s father. In trying to discover her parents, he develops an unshakable bond with the kid. He tries to get into Pakistan through a path righteous to his conscience and later, with a smart Pakistani news reporter for company and makes the search, a story that captures the imagination of the public in both countries.", "fanart": "https://walter.trakt.us/images/movies/000/221/962/fanarts/medium/46dbb493c7.jpg", "poster": "https://walter.trakt.us/images/movies/000/221/962/posters/medium/48d0c4a563.jpg", "title": "Bajrangi Bhaijaan", "originaltitle": "Bajrangi Bhaijaan", "premiered": "2015-07-17", "next": "http://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&languages=hi&count=40&start=1&start=1&sort=release_date,desc&page=4&ref_=adv_nxt", "director": "Kabir Khan", "writer": "Vijayendra Prasad / Vijayendra Prasad / Kabir Khan / Parveez Sheikh / Asad Hussain / Kausar Munir / Kabir Khan", "imdb": "tt3863552", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Bajrangi+Bhaijaan+%282015%29", "year": "2015", "duration": "9780", "genre": "Action / Comedy / Drama", "metacache": false}', 'imdb': 'tt3863552', 't': '20161006155052626000', 'year': '2015', 'action': 'play'}
    params = {'tmdb': '0', 'name': 'Rustom (2016)', 'title': 'Rustom', 'meta': '{"rating": "7.3", "votes": "6,499", "code": "tt5165344", "cast": [["Akshay Kumar", ""], ["Ileana", ""], ["Esha Gupta", ""], ["Manoj Bajpayee", ""]], "plot": "Naval officer Rustom Pavri returns from his posting and finds his wife Cynthia is away from home since last two days his marriages is on the rocks when he finds love letters in cupboard which indicates that Cynthia has found love in one of his friend Vikram Makhija an arrogant business tycoon ,Rustom then issues a pistol from Naval Ship\'s Armory and shoots Vikram three times in his chest living him dead and surrender himself to senior inspector Vincent Lobo.", "fanart": "https://walter.trakt.us/images/movies/000/234/965/fanarts/medium/e982aad610.jpg", "poster": "https://walter.trakt.us/images/movies/000/234/965/posters/medium/c853ec5030.jpg", "title": "Rustom", "originaltitle": "Rustom", "premiered": "2016-08-12", "next": "http://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&languages=hi&count=40&start=1&start=1&sort=release_date,desc&page=2&ref_=adv_nxt", "director": "Dharmendra Suresh Desai", "writer": "Vipul K. Rawal", "imdb": "tt5165344", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Rustom+%282016%29", "year": "2016", "duration": "8880", "genre": "Crime / Drama / Mystery", "metacache": false}', 'imdb': 'tt5165344', 't': '20161006162610402000', 'year': '2016', 'action': 'play'}
    params = {'tmdb': '330431', 'name': 'NH10 (2015)', 'title': 'NH10', 'meta': '{"rating": "6.22", "votes": "9", "tmdb": "330431", "name": "NH10 (2015)", "title": "NH10", "fanart": "http://image.tmdb.org/t/p/original/4A6QmdOzfFMe2HSIi2BZMHMJOXy.jpg", "tagline": "A woman, stacked against all odds, manages to not just stick it out but indeed give it back.", "plot": "A woman, stacked against all odds, manages to not just stick it out but indeed give it back.", "poster": "http://image.tmdb.org/t/p/w500/15xjX0ULsnnJpegmTwlfmDn4drO.jpg", "next": "", "originaltitle": "NH10", "premiered": "2015-03-13", "year": "2015", "duration": "7200", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=NH10+%282015%29", "metacache": false}', 'imdb': '0', 't': '20161007092138014000', 'year': '2015', 'action': 'play'}
    params = {'tmdb': '0', 'name': 'Welcome Back (2015)', 'title': 'Welcome Back', 'meta': '{"rating": "4.2", "votes": "4,200", "code": "tt3159708", "cast": [["Anil Kapoor", ""], ["Nana Patekar", ""], ["Dimple Kapadia", ""], ["John Abraham", ""]], "plot": "Uday Shetty and Majnu Bhai have left the underworld, and are now big businessmen. Two women, Chandni and Maharani, enter their life. Chandni is the new love in Uday Shetty and Majnu\'s life and both friends dream of tying the knot with her. However, Appa - Uday\'s father, plays spoilsport by bringing in his other daughter, Ranjana. He tells Uday Shetty to get her married to someone from a good family. Maharani puts a condition that only after her sister is married, will Chandni will marry one of them. Now, a search to find a suitable husband for Ranjana starts.", "fanart": "https://walter.trakt.us/images/movies/000/222/591/fanarts/medium/713cbb56bd.jpg", "poster": "https://walter.trakt.us/images/movies/000/222/591/posters/medium/fd484fdff3.jpg", "title": "Welcome Back", "originaltitle": "Welcome Back", "premiered": "2015-09-04", "next": "http://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&languages=hi&count=40&start=1&start=1&sort=release_date,desc&page=4&ref_=adv_nxt", "director": "Anees Bazmee", "writer": "Anees Bazmee / Rajeev Kaul / Rajeev Kaul / Anees Bazmee / Rajan Aggarwal / Praful Parekh / Raaj Shaandilyaa", "imdb": "tt3159708", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Welcome+Back+%282015%29", "year": "2015", "duration": "9120", "genre": "Action / Comedy / Crime", "metacache": false}', 'imdb': 'tt3159708', 't': '20161007095717834000', 'year': '2015', 'action': 'play'}
    params = {'action': 'tvshows', 'url': 'forumdisplay.php?f=176', 'name': 'Colors TV', 'provider': 'desirulez_tv'}
    params = {'tmdb': '0', 'episode': '0', 'name': '12th October 2016', 'title': '12th October 2016', 'tvdb': '0', 'season': '0', 'tvshowtitle': 'Bhabhiji Ghar Pe Hai', 'date': '0', 'meta': '{"tvshowurl": "forums/3143-Bhabhiji-Ghar-Pe-Hai", "title": "12th October 2016", "url": "threads/966418-Bhabhiji-Ghar-Pe-Hai-12th-October-2016-Watch-Online?s=f52027d78b6289d8dab777de23bffc4f", "tvshowtitle": "Bhabhiji Ghar Pe Hai", "provider": "desirulez_mv_tv", "duration": "1800", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Bhabhiji+Ghar+Pe+Hai", "name": "12th October 2016"}', 'imdb': '0', 't': '20161014092408332000', 'year': '0', 'action': 'play', 'tvrage': '0', 'alter': '0'}
    params = {'action': 'play', 'content': 'live', 'name': 'AND TV HD'}
    params = {'action': 'tvshows', 'url': 'forumdisplay.php?f=176', 'name': 'Colors TV', 'provider': 'desirulez_mv_tv'}
    params = {'tmdb': '0', 'episode': '0', 'name': '20th October 2016', 'title': '20th October 2016', 'tvdb': '0', 'season': '0', 'tvshowtitle': 'Bigg Boss 10', 'date': '0', 'meta': '{"tvshowurl": "forums/3994-Bigg-Boss-10", "title": "20th October 2016", "url": "threads/968883-Bigg-Boss-10-20th-October-2016-Watch-Online-2-hours-maha-episode?s=e002c7988b973fe76e8ffe8d634f89a0", "tvshowtitle": "Bigg Boss 10", "provider": "desirulez_mv_tv", "duration": "1800", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Bigg+Boss+10", "name": "20th October 2016"}', 'imdb': '0', 't': '20161020230608467000', 'year': '0', 'action': 'play', 'tvrage': '0', 'alter': '0'}
    #params = {'tmdb': '0', 'episode': '0', 'name': '20th October 2016', 'title': '20th October 2016', 'tvdb': '0', 'season': '0', 'tvshowtitle': 'Sasural Simar Ka', 'date': '0', 'meta': '{"tvshowurl": "forums/3948-Sasural-Simar-Ka", "title": "20th October 2016", "url": "threads/968880-Sasural-Simar-Ka-20th-October-2016-Watch-Online?s=6bfa8a53e72f5c9666a8bf487f22eb8c", "tvshowtitle": "Sasural Simar Ka", "provider": "desirulez_mv_tv", "duration": "1800", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Sasural+Simar+Ka", "name": "20th October 2016"}', 'imdb': '0', 't': '20161023225302497000', 'year': '0', 'action': 'play', 'tvrage': '0', 'alter': '0'}


    try:
        action = params['action']
    except:
        action = None
    try:
        name = params['name']
    except:
        name = None
    try:
        title = params['title']
    except:
        title = None
    try:
        year = params['year']
    except:
        year = None
    try:
        imdb = params['imdb']
    except:
        imdb = '0'
    try:
        tmdb = params['tmdb']
    except:
        tmdb = '0'
    try:
        tvdb = params['tvdb']
    except:
        tvdb = '0'
    try:
        tvrage = params['tvrage']
    except:
        tvrage = '0'
    try:
        season = params['season']
    except:
        season = None
    try:
        episode = params['episode']
    except:
        episode = None
    try:
        tvshowtitle = params['tvshowtitle']
    except:
        tvshowtitle = None
    try:
        tvshowtitle = params['show']
    except:
        pass
    try:
        alter = params['alter']
    except:
        alter = '0'
    try:
        alter = params['genre']
    except:
        pass
    try:
        date = params['date']
    except:
        date = None
    try:
        url = params['url']
    except:
        url = None
    try:
        image = params['image']
    except:
        image = None
    try:
        meta = params['meta']
    except:
        meta = None
    try:
        query = params['query']
    except:
        query = None
    try:
        source = params['source']
    except:
        source = None
    try:
        content = params['content']
    except:
        content = None
    try:
        provider = params['provider']
    except:
        provider = None

    try:
        lang = params['lang']
    except:
        lang = None

    from resources.lib.indexers import movies
    from resources.lib.indexers import tvshows
    from resources.lib import sources
    from resources.lib.libraries import debrid
    from resources.lib.libraries import client
    from resources.lib.resolvers import dailymotion
    from resources.lib import resolvers
    from resources.lib.sources import einthusan_mv
    url = einthusan_mv.source().get_sources('9068')
    result = client.request(url[0]['url'])
    if result == None: raise Exception()
    resolvers.request('http://playu.net/embed-azyk92idrbcj-700x440.html', None)
    #debrid.resolver('http://www.dailymotion.com/embed/video/x50xm71', 'realdebrid')
    debrid.resolve('http://www.dailymotion.com/video/x29cn4o', 'realdebrid')
    #tvshows.tvshows().get(url, provider=provider, network=name)
    # test search sources
    #source = sources().getSources(name, title, year, imdb, tmdb, tvdb, tvrage, season, episode, tvshowtitle, alter, date, meta)
    #sources.sources().play(name, title, year, imdb, tmdb, tvdb, tvrage, season, episode, tvshowtitle, alter, date, meta, url)
    #from resources.lib.indexers import tvshows
    #tvshows.tvshows().get(url, provider=provider, network=name)
    from resources.lib.sources import filmywap_mv
    filmywap_mv.source().get_sources('abc')

except:
    from resources.lib.libraries import client
    import traceback
    traceback.print_exc()
    client.printException('aftershock-testharness')