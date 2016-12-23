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
    params = {'action': 'tvshows', 'url': 'star-plus', 'name': 'Star Plus', 'provider': 'yodesi_tv'}
    #params = {'tmdb': '0', 'episode': '0', 'name': '20th October 2016', 'title': '20th October 2016', 'tvdb': '0', 'season': '0', 'tvshowtitle': 'Bigg Boss 10', 'date': '0', 'meta': '{"tvshowurl": "forums/3994-Bigg-Boss-10", "title": "20th October 2016", "url": "threads/968883-Bigg-Boss-10-20th-October-2016-Watch-Online-2-hours-maha-episode?s=e002c7988b973fe76e8ffe8d634f89a0", "tvshowtitle": "Bigg Boss 10", "provider": "desirulez_mv_tv", "duration": "1800", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Bigg+Boss+10", "name": "20th October 2016"}', 'imdb': '0', 't': '20161020230608467000', 'year': '0', 'action': 'play', 'tvrage': '0', 'alter': '0'}
    #params = {'tmdb': '0', 'episode': '0', 'name': '20th October 2016', 'title': '20th October 2016', 'tvdb': '0', 'season': '0', 'tvshowtitle': 'Sasural Simar Ka', 'date': '0', 'meta': '{"tvshowurl": "forums/3948-Sasural-Simar-Ka", "title": "20th October 2016", "url": "threads/968880-Sasural-Simar-Ka-20th-October-2016-Watch-Online?s=6bfa8a53e72f5c9666a8bf487f22eb8c", "tvshowtitle": "Sasural Simar Ka", "provider": "desirulez_mv_tv", "duration": "1800", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Sasural+Simar+Ka", "name": "20th October 2016"}', 'imdb': '0', 't': '20161023225302497000', 'year': '0', 'action': 'play', 'tvrage': '0', 'alter': '0'}
    params = {'action': 'tvshows', 'url': 'forumdisplay.php?f=176', 'name': 'Colors TV', 'provider': 'desirulez_mv_tv'}
    params = {'tmdb': '0', 'name': 'Dear Life (2016)', 'title': 'Dear Life', 'meta': '{"rating": "8.8", "votes": "12,001", "code": "tt5946128", "cast": [["Shah Rukh Khan", ""], ["Alia Bhatt", ""], ["Angad Bedi", ""], ["Kunal Kapoor", ""]], "plot": "This is the story of Kaira, a budding cinematographer in search of perfect life. A chance encounter with Jug, an unconventional thinker, helps her gain new perspective about life. She discovers that happiness is all about finding comfort in life\'s imperfections.", "mpaa": "UNRATED", "title": "Dear Zindagi", "originaltitle": "Dear Life", "poster": "https://images-na.ssl-images-amazon.com/images/M/MV5BZWQzYWI3ZGMtYzgyYy00OWZkLWEwODYtNGNiMTZhODBkNzUyL2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyNjY1MTg4Mzc@._V1_UY98_SX500_AL_.jpg", "next": "http://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&languages=hi&count=40&start=1&start=1&sort=release_date,desc&page=2&ref_=adv_nxt", "director": "Gauri Shinde", "writer": "Gauri Shinde", "imdb": "tt5946128", "premiered": "2016-11-25", "year": "2016", "duration": "9060", "genre": "Drama / Romance", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Dear+Life+%282016%29", "metacache": false}', 'imdb': 'tt5946128', 't': '20161130010806547000', 'year': '2016', 'action': 'play'}
    params = {'action': 'movies', 'url': 'http://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&languages=hi&count=40&start=1&sort=release_date,desc&start=1'}
    params = {'action': 'play', 'content': 'live', 'name': 'ABP NEWS'}

    params = {'action': 'play', 'content': 'live', 'name': '& PICTURES HD'}
    #params = {'tmdb': '0', 'episode': '0', 'name': '12th December 2016', 'title': '12th December 2016', 'tvdb': '0', 'season': '10', 'tvshowtitle': 'Bigg Boss 10', 'date': '0', 'meta': '{"tvshowurl": "forums/3994-Bigg-Boss-10", "title": "12th December 2016", "url": "threads/987786-Bigg-Boss-10-12th-December-2016-Watch-Online?s=cc583847a54ad97a7ef547a9da3fcf8f", "season": "10", "tvshowtitle": "Bigg Boss 10", "next": "forums/3994-Bigg-Boss-10/page2?s=cc583847a54ad97a7ef547a9da3fcf8f", "provider": "desirulez_mv_tv", "duration": "1800", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Bigg+Boss+10", "name": "12th December 2016"}', 'imdb': '0', 't': '20161212203135593000', 'year': '0', 'action': 'play', 'tvrage': '0', 'alter': '0'}
    #params = {'tmdb': '0', 'episode': '0', 'name': '10th December 2016', 'title': '10th December 2016', 'tvdb': '0', 'season': '9', 'tvshowtitle': 'Jhalak Dikhhla Jaa Season 9', 'date': '0', 'meta': '{"tvshowurl": "forums/4034-Jhalak-Dikhhla-Jaa-Season-9", "title": "10th December 2016", "url": "threads/986369-Jhalak-Dikhhla-Jaa-Season-9-10th-December-2016-Watch-Online?s=584dc5e1564eed456f2a25be7f86e6ea", "season": "9", "tvshowtitle": "Jhalak Dikhhla Jaa Season 9", "next": "forums/4034-Jhalak-Dikhhla-Jaa-Season-9/page2?s=584dc5e1564eed456f2a25be7f86e6ea", "provider": "desirulez_mv_tv", "duration": "1800", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Jhalak+Dikhhla+Jaa+Season+9", "name": "10th December 2016"}', 'imdb': '0', 't': '20161213000802688000', 'year': '0', 'action': 'play', 'tvrage': '0', 'alter': '0'}

    # desihit
    #params = {'tmdb': '0', 'episode': '0', 'name': '15th December 2016', 'title': '15th December 2016', 'tvdb': '0', 'season': '10', 'tvshowtitle': 'Bigg Boss 10', 'date': '0', 'meta': '{"tvshowurl": "forums/3994-Bigg-Boss-10", "title": "15th December 2016", "url": "threads/989694-Bigg-Boss-10-15th-December-2016-Watch-Online?s=b4f2b23f90f0fbf473f679887a785b0b", "season": "10", "tvshowtitle": "Bigg Boss 10", "next": "forums/3994-Bigg-Boss-10/page2?s=b4f2b23f90f0fbf473f679887a785b0b", "provider": "desirulez_mv_tv", "duration": "1800", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Bigg+Boss+10", "name": "15th December 2016"}', 'imdb': '0', 't': '20161216013558647000', 'year': '0', 'action': 'play', 'tvrage': '0', 'alter': '0'}
    #params = {'tmdb': '0', 'episode': '0', 'name': '15th December 2016', 'title': '15th December 2016', 'tvdb': '0', 'season': '0', 'tvshowtitle': 'Yeh Rishta Kya Kehlata Hai', 'date': '0', 'meta': '{"tvshowurl": "forums/3943-Yeh-Rishta-Kya-Kehlata-Hai", "title": "15th December 2016", "url": "threads/989675-Yeh-Rishta-Kya-Kehlata-Hai-15th-December-2016-Watch-Online?s=b4f2b23f90f0fbf473f679887a785b0b", "tvshowtitle": "Yeh Rishta Kya Kehlata Hai", "next": "forums/3943-Yeh-Rishta-Kya-Kehlata-Hai/page2?s=b4f2b23f90f0fbf473f679887a785b0b", "provider": "desirulez_mv_tv", "duration": "1800", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Yeh+Rishta+Kya+Kehlata+Hai", "name": "15th December 2016"}', 'imdb': '0', 't': '20161216014224647000', 'year': '0', 'action': 'play', 'tvrage': '0', 'alter': '0'}
    #params = {'tmdb': '0', 'episode': '0', 'name': '11th December 2016', 'title': '11th December 2016', 'tvdb': '0', 'season': '5', 'tvshowtitle': 'Koffee With Karan Season 5 (Star World)', 'date': '0', 'meta': '{"name": "11th December 2016", "title": "11th December 2016", "url": "threads/986992-Koffee-With-Karan-Season-5-11th-December-2016-Watch-Online?s=b9f8288314dd3a877ab603c37d41a779", "season": "5", "tvshowtitle": "Koffee With Karan Season 5 (Star World)", "provider": "desirulez_mv_tv", "duration": "1800", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Koffee+With+Karan+Season+5+%28Star+World%29", "tvshowurl": "forums/4480-Koffee-With-Karan-Season-5-Star-World"}', 'imdb': '0', 't': '20161216020518662000', 'year': '0', 'action': 'play', 'tvrage': '0', 'alter': '0'}


    select = None

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
    from resources.lib.indexers import episodes
    from resources.lib import sources
    from resources.lib.libraries import debrid
    from resources.lib.libraries import client
    from resources.lib.resolvers import dailymotion
    from resources.lib import resolvers
    from resources.lib.sources import einthusan_mv

    from resources.lib.libraries import user


    '''
    result = '#EXTINF:-1,|VIP|HINDI:ZOOM\nhttp://live.softiptv.com:9900/live/525/525/17682.m3u8\n#EXTINF:-1,|VIP|HINDI:ZeeTv HD INddia\nhttp://live.softiptv.com:9900/live/525/525/17683.m3u8\n#EXTINF:-1,|VIP|HINDI:Zee Action\nnhttp://live.softiptv.com:9900/live/525/525/17684.m3u8'
    reg = '#EXTINF:-1,.*(Yupp|in|hindi|punjabi|telugu|tamil|marathi|Malyalam|Kannada|BENGALI):(.*)\s*(.*)'
    result = result.replace('\r', '')
    result = re.findall(reg, result, re.IGNORECASE)
    print result
    '''

    from resources.lib.libraries import livemeta
    #livemeta.source().getLiveNames()

    from resources.lib.sources import sources
    sources().play(name, title, year, imdb, tmdb, tvdb, tvrage, season, episode, tvshowtitle, alter, date, meta, url, select)

    #movies.movies().get(url, idx, provider, lang)

    #sources.sources().play(name, title, year, imdb, tmdb, tvdb, tvrage, season, episode, tvshowtitle, alter, date, meta, url)

    from resources.lib.indexers import tvshows
    #tvshows.tvshows().get(url, provider=provider, network=name)
    #episodes.episodes().get('Bigg Boss', year, imdb, tmdb, tvdb, tvrage, provider='yodesi_tv', url='http://www.yodesi.net/category/colors/bigg-boss-season-10/')
    #from resources.lib.sources import filmywap_mv
    #filmywap_mv.source().get_sources('abc')

    #from resources.lib.sources import badtameezdil_tv
    #url = 'http://badtameezdil.net/watch-video-bigg-boss-10-14th-december-2016-full-episode-60/'
    #badtameezdil_tv.source().get_sources(url)
    #from resources.lib.sources import dynns_live
    #dynns_live.source().getLiveSource()
    #url = 'http://live1.dyndns.tv:8081/maid/lamhe/playlist.m3u8'
    #dynns_live.source().resolve(url, None)

    from resources.lib.indexers import livetv
    livetv.channels().get()

    #from resources.lib.sources import cinefun_live
    #cinefun_live.source().resolve("95616", None)

    #from resources.lib.sources import iptv_live
    #iptv_live.source().getLiveSource(True)

    #from resources.lib.libraries import control
    #control.delete('*.json')

    #from resources.lib.sources import swift_live
    #swift_live.source().resolve('http://163.172.142.242:8081/swiftiptv/9xjalwa/playlist.m3u8', None)

    #from resources.lib.libraries import cleantitle
    #print cleantitle.live('COLORS TV HD ( ENTERTAINMENT )')
    #print cleantitle.live('COLORS TV INDIA')
    #print cleantitle.live('COLORS TV APAC')
    #print cleantitle.live('COLORS TV (LOCAL TIME)')


except:
    from resources.lib.libraries import client
    import traceback
    traceback.print_exc()
    client.printException('aftershock-testharness')