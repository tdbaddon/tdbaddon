import sys, re, base64

sys.argv = ['plugin.video.aftershock', '1']


try :
    # playItem
    #params = {'name': 'Piku (2015)', 'tvdb': '0', 'content': 'movie', 'source': '[{"url": "http://www.mediaplaybox.com/video/Piku_Eng_Sub_Part_1##http://www.mediaplaybox.com/video/Piku_Eng_Sub_Part_2##http://www.mediaplaybox.com/video/Piku_Eng_Sub_Part_3##http://www.mediaplaybox.com/video/Piku_Eng_Sub_Part_4", "label": "02 | [B]PLAYINDIAFILMS[/B] | MEDIAPLAYBOX | [B][I]HD [/I][/B] [4]", "source": "mediaplaybox", "parts": "4", "provider": "PlayIndiaFilms", "quality": "HD"}]', 'imdb': 'tt3767372', 'year': '2015', 'action': 'playItem'}
    #params = {'action': 'movies', 'lang': 'hi', 'url': '/browse/hindi?order=desc&sort=date&page=2', 'provider': 'apnaview_mv'}
    #params =  {'action': 'movies', 'lang': 'tamil', 'url': 'HD', 'provider': 'playindiafilms_mv'}
    params = {'tmdb': '362136', 'name': 'Prem Ratan Dhan Payo (2015)', 'title': 'Prem Ratan Dhan Payo', 'meta': '{"rating": "6.6", "tmdb": "362136", "code": "tt3595298", "imdb": "tt3595298", "year": "2015", "duration": "10440", "plot": "Loosely based on the novel The prince and the Pauper. Ever loving Prem is respected and loved by all and Vijay (also played by Salman Khan) is in the world of hatred and violence. They change their identities temporarily to discover the other side of the world.", "votes": "11", "title": "Prem Ratan Dhan Payo", "fanart": "http://image.tmdb.org/t/p/original/9fVjhznaYPcQF7eHZ08CkytmTbL.jpg", "mpaa": "NR", "writer": "Sooraj R. Barjatya", "poster": "http://image.tmdb.org/t/p/w500/8mfZyMKdyXGjwr27dCCBUp4fwVG.jpg", "director": "Sooraj R. Barjatya", "studio": "Fox Star Studios", "genre": "Drama / Action / Romance", "metacache": false, "lang": "hindi", "name": "Prem Ratan Dhan Payo (2015)", "premiered": "2015-11-11", "originaltitle": "Prem Ratan Dhan Payo", "cast": [["Salman Khan", "Prem/Vijay"], ["Sonam Kapoor", "Maithili"], ["Neil Nitin Mukesh", "Yuvraj Ajay Singh"], ["Anupam Kher", "Diwan"], ["Swara Bhaskar", "Chandrika"], ["Deepak Dobriyal", "Kanhaiya"], ["Arman Kohli", "Chirag Singh"], ["Manoj Joshi", "Bhandari"]], "tagline": "Loosely based on the novel The prince and the Pauper", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Prem+Ratan+Dhan+Payo+%282015%29"}', 'imdb': 'tt3595298', 'year': '2015', 'action': 'sources'}
    #params = {'tmdb': '0', 'tvdb': '0', 'tvshowtitle': 'Fear Factor Khatron Ke Khiladi Season 7', 'year': '0', 'url': 'forums/3683-Fear-Factor-Khatron-Ke-Khiladi-Season-7?s=faad8efe3f12248ca229f8be39eb3035', 'imdb': '0', 'provider': 'desirulez_tv', 'action': 'episodes', 'tvrage': '0'}
    #params = {'tmdb': '0', 'episode': '0', 'name': '1st March 2016', 'title': '1st March 2016', 'tvdb': '0', 'season': '0', 'tvshowtitle': 'Yeh Rishta Kya Kehlata Hai', 'year': '0', 'date': '0', 'meta': '{"tvshowurl": "forums/3699-Yeh-Rishta-Kya-Kehlata-Hai?s=333166e47513e1996d0c8fde0871acc2", "title": "1st March 2016", "url": "threads/861109-Yeh-Rishta-Kya-Kehlata-Hai-1st-March-2016-Watch-Online?s=333166e47513e1996d0c8fde0871acc2", "tvshowtitle": "Yeh Rishta Kya Kehlata Hai", "provider": "desirulez_tv", "duration": "1800", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Yeh+Rishta+Kya+Kehlata+Hai", "name": "1st March 2016"}', 'imdb': '0', 'provider': 'desirulez_tv', 'action': 'sources', 'tvrage': '0', 'alter': '0'}
    #params = {'action': 'movies', 'lang': 'marathi', 'url': 'added', 'provider': 'ibollytv_mv'}
    #params = {'action': 'movies', 'lang': 'marathi', 'url': '/watch-marathi-movies-online?page=2&', 'provider': 'ibollytv_mv'}
    #params = {'tmdb': '0', 'name': 'Shasan (2016)', 'title': 'Shasan', 'meta': '{"name": "Shasan (2016)", "title": "Shasan", "poster": "http://cdn1.marathistars.com/wp-content/uploads/2015/09/Shasan-Marathi-Movie-Poster.jpg", "next": "/watch-marathi-movies-online?page=2&", "originaltitle": "Shasan", "imdb": "tt5061416", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Shasan+%282016%29", "year": "2016", "duration": "7200", "metacache": false}', 'imdb': 'tt5061416', 'year': '2016', 'action': 'sources'}
    #params = {'tmdb': '0', 'name': 'Aligrah (2016)', 'title': 'Aligrah', 'meta': '{"name": "Aligrah (2016)", "title": "Aligrah", "poster": "http://www.apnaview.com/img/poster/50cd90328418ef3d066268408804b78b.jpg", "originaltitle": "Aligrah", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Aligrah+%282016%29", "year": "2016", "duration": "7200", "metacache": false}', 'imdb': '0', 'year': '2016', 'action': 'sources'}
    #params = {'tmdb': '376869', 'name': 'Neerja (2016)', 'title': 'Neerja', 'meta': '{"rating": "8.5", "code": "tt5286444", "tmdb": "376869", "imdb": "tt5286444", "year": "2016", "duration": "7320", "plot": "Neerja is a portrayal on the life of the courageous Neerja Bhanot, who sacrificed her life while protecting the lives of 359 passengers on the Pan Am flight 73 in 1986. The flight was hijacked by a terrorist organization.", "votes": "3", "title": "Neerja", "fanart": "http://image.tmdb.org/t/p/original/sJbviiOJ15k4gcaDrdRDmyjvJvh.jpg", "tagline": "Fear Gave Her Courage", "writer": "Saiwyn Qadras", "poster": "http://image.tmdb.org/t/p/w500/97qsAXZ31E2VYfQY2zgy4djxOWE.jpg", "director": "Ram Madhvani", "studio": "T-Series", "genre": "Drama / History", "metacache": true, "name": "Neerja (2016)", "premiered": "2016-02-19", "originaltitle": "Neerja", "cast": [["Sonam Kapoor", "Neerja Bhanot"], ["Shabana Azmi", "Rama Bhanot"], ["Shekhar Ravjiani", "Jaideep"]], "mpaa": "UA", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Neerja+%282016%29"}', 'imdb': 'tt5286444', 'year': '2016', 'action': 'sources'}
    #params = {'action': 'movies', 'lang': 'marathi', 'url': 'theaters', 'provider': 'ibollytv_mv'}
    #params = {'action': 'movies', 'lang': 'marathi', 'url': '/watch-marathi-movies-online?sort=latest&year=2016&page=2', 'provider': 'ibollytv_mv'}
    #params = {'action': 'movies', 'lang': 'punjabi', 'url': 'theaters', 'provider': 'ibollytv_mv'}
    #params = {'action': 'movies', 'lang': 'kannada', 'url': 'added', 'provider': 'ibollytv_mv'}
    #params = {'tmdb': '0', 'episode': '0', 'name': '7th March 2016', 'title': '7th March 2016', 'tvdb': '0', 'season': '0', 'tvshowtitle': 'Yeh Rishta Kya Kehlata Hai', 'year': '0', 'date': '0', 'meta': '{"tvshowurl": "forums/3699-Yeh-Rishta-Kya-Kehlata-Hai?s=fa29871dc1e6cd307816b20f0b40635a", "title": "7th March 2016", "url": "threads/862392-Yeh-Rishta-Kya-Kehlata-Hai-7th-March-2016-Watch-Online?s=fa29871dc1e6cd307816b20f0b40635a", "tvshowtitle": "Yeh Rishta Kya Kehlata Hai", "provider": "desirulez_tv", "duration": "1800", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Yeh+Rishta+Kya+Kehlata+Hai", "name": "7th March 2016"}', 'imdb': '0', 'provider': 'desirulez_tv', 'action': 'sources', 'tvrage': '0', 'alter': '0'}
    #params = {'tmdb': '375199', 'name': 'Jai Gangaajal (2016)', 'title': 'Jai Gangaajal', 'meta': '{"rating": "5.8", "tmdb": "375199", "code": "tt4979082", "imdb": "tt4979082", "year": "2016", "duration": "7200", "plot": "The film features SP Abha Mathur who is appointed the first female SP of Bankipur district, Bihar. She then goes against the Local MLA of Bankipur and henchmen of Lakhisarai district.", "votes": "4", "title": "Jai Gangaajal", "fanart": "http://image.tmdb.org/t/p/original/7IcjAPk6XgIBObtN2XwrimcK9nH.jpg", "tagline": "The film features SP Abha Mathur who is appointed the first female SP of Bankipur district, Bihar", "writer": "Prakash Jha", "next": "/browse/hindi?order=desc&sort=date&page=2", "poster": "http://image.tmdb.org/t/p/w500/vE9nbc4xRweq1u2SWo15RW7DmMd.jpg", "director": "Prakash Jha / Shyam Kaushal", "studio": "Prakash Jha Productions", "genre": "Drama / Action", "metacache": true, "name": "Jai Gangaajal (2016)", "premiered": "2016-03-04", "originaltitle": "Jai Gangaajal", "cast": [["Priyanka Chopra", "SP Abha Mathur"], ["Prakash Jha", "Beant Singh"], ["Manav Kaul", ""], ["Ayush Mahesh Khedekar", ""], ["Murli Sharma", ""], ["Vega Tamotia", ""], ["Rahul Bhat", ""], ["Ninad Kamat", ""]], "mpaa": "U", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Jai+Gangaajal+%282016%29"}', 'imdb': 'tt4979082', 'year': '2016', 'action': 'sources'}
    #params = {'action': 'movies', 'lang': 'hindi', 'url': 'HD', 'provider': 'hdbuffer_mv'}
    #params = {'action': 'movies', 'lang': 'hindi', 'url': '/category/hindi/dvdbluraymovies-hindionline/page/2', 'provider': 'hdbuffer_mv'}
    #params = {'tmdb': '0', 'episode': '0', 'name': '16th March 2016', 'title': '16th March 2016', 'tvdb': '0', 'season': '0', 'tvshowtitle': 'Naya Akbar Birbal', 'year': '0', 'date': '0', 'meta': '{"tvshowurl": "forums/3907-Naya-Akbar-Birbal?s=6838cea62281fd5d6859a494701cb944", "title": "16th March 2016", "url": "threads/868075-Naya-Akbar-Birbal-16th-March-2016-Watch-Online?s=6838cea62281fd5d6859a494701cb944", "tvshowtitle": "Naya Akbar Birbal", "provider": "desirulez_tv", "duration": "1800", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Naya+Akbar+Birbal", "name": "16th March 2016"}', 'imdb': '0', 'provider': 'desirulez_tv', 'action': 'sources', 'tvrage': '0', 'alter': '0'}
    params = {'tmdb': '0', 'episode': '0', 'name': '17th March 2016', 'title': '17th March 2016', 'tvdb': '0', 'season': '0', 'tvshowtitle': 'Yeh Rishta Kya Kehlata Hai', 'year': '0', 'date': '0', 'meta': '{"tvshowurl": "forums/3699-Yeh-Rishta-Kya-Kehlata-Hai?s=6838cea62281fd5d6859a494701cb944", "title": "17th March 2016", "url": "threads/867745-Yeh-Rishta-Kya-Kehlata-Hai-17th-March-2016-Watch-Online?s=4acb3d8814fd47034837ed84019d41f6", "tvshowtitle": "Yeh Rishta Kya Kehlata Hai", "provider": "desirulez_tv", "duration": "1800", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Yeh+Rishta+Kya+Kehlata+Hai", "name": "17th March 2016"}', 'imdb': '0', 'provider': 'desirulez_tv', 'action': 'sources', 'tvrage': '0', 'alter': '0'}
    #params = {'tmdb': '0', 'episode': '0', 'name': '17th March 2016', 'title': '17th March 2016', 'tvdb': '0', 'season': '0', 'tvshowtitle': 'Naya Akbar Birbal', 'year': '0', 'date': '0', 'meta': '{"tvshowurl": "forums/3907-Naya-Akbar-Birbal?s=3e8596e6ac1a066a9d512af311637e66", "title": "17th March 2016", "url": "threads/869793-Naya-Akbar-Birbal-17th-March-2016-Watch-Online?s=3e8596e6ac1a066a9d512af311637e66", "tvshowtitle": "Naya Akbar Birbal", "provider": "desirulez_tv", "duration": "1800", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Naya+Akbar+Birbal", "name": "17th March 2016"}', 'imdb': '0', 'provider': 'desirulez_tv', 'action': 'sources', 'tvrage': '0', 'alter': '0'}
    #params = {'tmdb': '0', 'episode': '0', 'name': '19th March 2016', 'title': '19th March 2016', 'tvdb': '0', 'season': '0', 'tvshowtitle': 'Yeh Rishta Kya Kehlata Hai', 'date': '0', 'meta': '{"tvshowurl": "forums/3699-Yeh-Rishta-Kya-Kehlata-Hai?s=f89dd369e57fac9ac40b629533d84805", "title": "19th March 2016", "url": "threads/869714-Yeh-Rishta-Kya-Kehlata-Hai-19th-March-2016-Watch-Online?s=f89dd369e57fac9ac40b629533d84805", "tvshowtitle": "Yeh Rishta Kya Kehlata Hai", "provider": "desirulez_tv", "duration": "1800", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Yeh+Rishta+Kya+Kehlata+Hai", "name": "19th March 2016"}', 'imdb': '0', 't': '20160320195523951000', 'year': '0', 'action': 'play', 'tvrage': '0', 'alter': '0'}
    #params = {'action': 'tvshows', 'url': 'forumdisplay.php?f=3165', 'provider': 'desirulez_tv'}
    #params = {'action': 'movies', 'lang': 'hindi', 'url': '/category/hindi/dvdbluraymovies-hindionline/page/2', 'provider': 'hdbuffer_mv'}
    #params = {'tmdb': '191714', 'name': 'The Lunchbox (2013)', 'title': 'The Lunchbox', 'meta': '{"rating": "7.1", "code": "tt2350496", "tmdb": "191714", "imdb": "tt2350496", "year": "2013", "duration": "6240", "plot": "A mistaken delivery in Mumbai\'s famously efficient lunchbox delivery system (Mumbai\'s Dabbawallahs) connects a young housewife to a stranger in the dusk of his life. They build a fantasy world together through notes in the lunchbox. Gradually, this fantasy threatens to overwhelm their reality.", "votes": "108", "title": "The Lunchbox", "fanart": "http://image.tmdb.org/t/p/original/k9qLDoyIogooakZsDgZF9chb6hu.jpg", "tagline": "A mistaken delivery in Mumbai\'s famously efficient lunchbox delivery system (Mumbai\'s Dabbawallahs) connects a young housewife to a stranger in the dusk of his life", "writer": "Ritesh Batra", "next": "", "poster": "http://image.tmdb.org/t/p/w500/xFJqU1W5WlJiKr4Witnb7h9HNHn.jpg", "director": "Ritesh Batra", "studio": "UTV Motion Pictures", "genre": "Drama / Romance", "metacache": false, "name": "The Lunchbox (2013)", "premiered": "2013-09-19", "originaltitle": "The Lunchbox", "cast": [["Irrfan Khan", "Saajan Fernandes"], ["Nimrat Kaur", "Ila"], ["Nawazuddin Siddiqui", "Shaikh"], ["Denzil Smith", "Mr. Shroff"], ["Bharati Achrekar", "Mrs. Deshpande"], ["Nakul Vaid", "Rajeev"], ["Yashvi Puneet Nagar", "Yavshi"], ["Lillete Dubey", "Ila\'s Mother"], ["Shruti Bapna", "Mehrunnisa"]], "mpaa": "PG", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=The+Lunchbox+%282013%29"}', 'imdb': 'tt2350496', 'year': '2013', 'action': 'sources'}
    #params = {'action': 'movies', 'lang': 'hindi', 'url': 'theaters', 'provider': 'apnaview_mv'}
    #params = {'tmdb': '0', 'name': 'Ki & Ka (2016)', 'title': 'Ki & Ka', 'meta': '{"name": "Ki & Ka (2016)", "title": "Ki & Ka", "poster": "http://www.apnaview.com/img/poster/2209aafb27601c60b4e0bf315e9764e8.jpg", "next": "/browse/hindi?year=2016&order=desc&sort=date&page=2", "originaltitle": "Ki & Ka", "imdb": "tt1037475", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Ki+%26+Ka+%282016%29", "year": "2016", "duration": "7200", "metacache": false}', 'imdb': 'tt1037475', 'year': '2016', 'action': 'sources'}
    #params = {'action': 'download', 'source': '[{"url": "https://openload.co/embed/P-irqGW8ylM/", "direct": false, "label": "01 | [B]DESIHIT[/B] | OPENLOAD | [B][I]HD [/I][/B]", "source": "openload.co", "parts": "1", "provider": "DesiHit", "quality": "HD"}]', 'image': 'http://image.tmdb.org/t/p/w500/vE9nbc4xRweq1u2SWo15RW7DmMd.jpg', 'name': 'Jai Gangaajal (2016)'}
    #params = {'action': 'playItem', 'content': 'live', 'name': 'Zee TV HD', 'source': '[{"url": "http://www.dittotv.com/livetv/linkname=Zee TV HD","provider":"ditto", "label":"ditto", "source": "ditto", "quality":"HD"}]'}
    #params = {'action': 'playItem', 'content': 'live', 'name': '&TV',       'source': "{'url': 'http://www.dittotv.com/livetv/linkname=&TV', 'source': 'ditto', 'label': 'ditto', 'quality': 'HD', 'provider': 'ditto'}"}
    #params = {'action': 'playItem', 'content': 'live', 'name': 'Raj News Telugu', 'source': "[{'url': 'http://www.dittotv.com/livetv/linkname=Raj News Telugu', 'source': 'ditto', 'label': 'ditto', 'quality': 'HD', 'provider': 'ditto'}]"}
    #params = {'action': 'movies', 'lang': 'hindi', 'url': 'theaters', 'provider': 'apnaview_mv'}
    #params = {'tmdb': '362045', 'name': 'Bajirao Mastani (2015)', 'title': 'Bajirao Mastani', 'meta': '{"rating": "7.0", "code": "tt3735246", "tmdb": "362045", "imdb": "tt3735246", "year": "2015", "duration": "9000", "plot": "A historical account of the romance between the Maratha general, Baji Rao I and Mastani, a Muslim princess.", "votes": "18", "title": "Bajirao Mastani", "fanart": "http://image.tmdb.org/t/p/original/pZVL7yJdKqR7oAa4J8fUUOwuiGG.jpg", "tagline": "A historical account of the romance between the Maratha general, Baji Rao I and Mastani, a Muslim princess.", "writer": "Prakash Kapadia", "next": "", "poster": "http://image.tmdb.org/t/p/w500/h6t2eLxievyA5GrthmpmE2uzB9W.jpg", "director": "Sanjay Leela Bhansali", "studio": "SLB Films", "genre": "War / History / Romance", "metacache": true, "name": "Bajirao Mastani (2015)", "premiered": "2015-12-18", "originaltitle": "Bajirao Mastani", "cast": [["Ranveer Singh", "Baji Rao I"], ["Deepika Padukone", "Mastani"], ["Priyanka Chopra", "Kashibai"], ["Tanvi Azmi", "Radhabai, Bajirao\'s mother."], ["Vaibhav Tatwawadi", "Chimaji Appa, Baji Rao\'s younger brother"], ["Mahesh Manjrekar", "Maratha Emperor \'Chhattrapati Shahu\'"], ["Milind Soman", "Ambaji Panth"], ["Sanjay Mishra", ""], ["Aditya Pancholi", "Panth Pratinidhi"]], "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Bajirao+Mastani+%282015%29"}', 'imdb': 'tt3735246', 'year': '2015', 'action': 'sources'}
    #params = {'tmdb': '362136', 'name': 'Prem Ratan Dhan Payo (2015)', 'title': 'Prem Ratan Dhan Payo', 'meta': '{"rating": "5.7", "code": "tt3595298", "tmdb": "362136", "imdb": "tt3595298", "year": "2015", "duration": "10440", "plot": "Loosely based on the novel The prince and the Pauper. Ever loving Prem is respected and loved by all and Vijay (also played by Salman Khan) is in the world of hatred and violence. They change their identities temporarily to discover the other side of the world.", "votes": "20", "title": "Prem Ratan Dhan Payo", "fanart": "http://image.tmdb.org/t/p/original/9fVjhznaYPcQF7eHZ08CkytmTbL.jpg", "tagline": "Loosely based on the novel The prince and the Pauper", "writer": "Sooraj R. Barjatya", "next": "", "poster": "http://image.tmdb.org/t/p/w500/weXScKHG1UzfYcRuefzr6EaoTke.jpg", "director": "Sooraj R. Barjatya", "studio": "Fox Star Studios", "genre": "Drama / Action / Romance", "metacache": true, "name": "Prem Ratan Dhan Payo (2015)", "premiered": "2015-11-11", "originaltitle": "Prem Ratan Dhan Payo", "cast": [["Salman Khan", "Prem/Vijay"], ["Sonam Kapoor", "Maithili"], ["Neil Nitin Mukesh", "Yuvraj Ajay Singh"], ["Anupam Kher", "Diwan"], ["Swara Bhaskar", "Chandrika"], ["Deepak Dobriyal", "Kanhaiya"], ["Arman Kohli", "Chirag Singh"], ["Manoj Joshi", "Bhandari"]], "mpaa": "NR", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Prem+Ratan+Dhan+Payo+%282015%29"}', 'imdb': 'tt3595298', 'year': '2015', 'action': 'sources'}
    #params = {'tmdb': '0', 'episode': '0', 'name': '23rd August 2016', 'title': '23rd August 2016', 'tvdb': '0', 'season': '0', 'tvshowtitle': 'Sasural Simar Ka', 'year': '0', 'date': '0', 'meta': '{"tvshowurl": "forums/3948-Sasural-Simar-Ka", "title": "23rd August 2016", "url": "threads/932059-Sasural-Simar-Ka-23rd-August-2016-Watch-Online?s=cb6f09ff7feca743d2681cacf53bf6b8", "tvshowtitle": "Sasural Simar Ka", "provider": "desirulez_tv", "duration": "1800", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Sasural+Simar+Ka", "name": "23rd August 2016"}', 'imdb': '0', 'provider': 'desirulez_tv', 'action': 'sources', 'tvrage': '0', 'alter': '0'}
    #params = {'action': 'playItem', 'content': 'live', 'name': 'Colors', 'source': '[{"url": "83", "label": "Resolving Colors", "source": "uktvnow", "meta": "{\\"poster\\": \\"http://www.lyngsat-logo.com/logo/tv/cc/colors_in.png\\", \\"iconImage\\": \\"http://www.lyngsat-logo.com/logo/tv/cc/colors_in.png\\"}", "provider": "uktvnow", "quality": "HD"}]'}
    #params = {'action': 'play', 'content': 'live', 'name': 'Color Hd'}
    #params = {}
    params = {'tmdb': '0', 'episode': '0', 'name': '27th September 2016', 'title': '27th September 2016', 'tvdb': '0', 'season': '0', 'tvshowtitle': 'Sasural Simar Ka', 'year': '0', 'date': '0', 'meta': '{"tvshowurl": "forums/3948-Sasural-Simar-Ka", "title": "27th September 2016", "url": "threads/957870-Sasural-Simar-Ka-27th-September-2016-Watch-Online?s=0d84ed1dab42c4a5abd7f366af8d4b53", "tvshowtitle": "Sasural Simar Ka", "next": "forums/3948-Sasural-Simar-Ka/page2?s=0d84ed1dab42c4a5abd7f366af8d4b53", "provider": "desirulez_tv", "duration": "1800", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Sasural+Simar+Ka", "name": "27th September 2016"}', 'imdb': '0', 'provider': 'desirulez_tv', 'action': 'sources', 'tvrage': '0', 'alter': '0'}
    params = {'tmdb': '388333', 'name': 'M.S. Dhoni: The Untold Story (2016)', 'title': 'M.S. Dhoni: The Untold Story', 'meta': '{"rating": "5.8", "code": "tt4169250", "tmdb": "388333", "imdb": "tt4169250", "year": "2016", "duration": "11040", "plot": "The film is based on the life of Indian cricketer and the current captain of the Indian national cricket team, Mahendra Singh Dhoni.", "votes": "2", "title": "M.S. Dhoni: The Untold Story", "fanart": "http://image.tmdb.org/t/p/original/2tTtuHpbROSqzqu8Zi6U0hZr6Gc.jpg", "tagline": "The man you know... The journey you don\'t.", "writer": "Neeraj Pandey / Nandu Kamte", "next": "http://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&languages=hi&count=40&start=1&start=1&sort=release_date,desc&page=2&ref_=adv_nxt", "poster": "http://image.tmdb.org/t/p/w500/311gCwnNJgyoNEPWR9GJ2JBGJAm.jpg", "director": "Neeraj Pandey", "studio": "Fox Star Studios", "genre": "Drama", "metacache": true, "premiered": "2016-09-02", "originaltitle": "M.S. Dhoni: The Untold Story", "cast": [["Anupam Kher", "Pan Singh"], ["Kiara Advani", "Sakshi Singh Rawat / Sakshi Singh Dhoni"], ["Sushant Singh Rajput", "M. S. Dhoni"], ["Herry Tangiri", "Yuvraj Singh (as Herry Tangri)"], ["Disha Patani", "Priyanka Jha"], ["Bhumika Chawla", "Jayanti Gupta, Dhoni\'s sister"], ["Rajesh Sharma", ""], ["John Abraham", "Himself (Cameo)"]], "mpaa": "UA", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=M.S.+Dhoni%3A+The+Untold+Story+%282016%29"}', 'imdb': 'tt4169250', 't': '20161003003606950000', 'year': '2016', 'action': 'play'}
    params = {'tmdb': '39083', 'tvdb': '273190', 'tvshowtitle': 'Sasural Simar Ka', 'year': '0', 'url': 'forums/3948-Sasural-Simar-Ka', 'imdb': 'tt1934806', 'provider': 'desirulez_tv', 'action': 'episodes', 'tvrage': '0'}
    params = {'action': 'playItem', 'source': '[{"debrid": "", "url": "http://streamin.to/embed-6qpnqixizf9r-730x480.html", "direct": false, "label": "06 | [B]IBOLLYTV[/B] | STREAMIN ", "source": "streamin.to", "parts": "1", "provider": "iBollyTV", "quality": ""}]', 'content': 'movie', 'title': 'M.S. Dhoni: The Untold Story'}
    params = {'tmdb': '0', 'episode': '0', 'name': '29th September 2016', 'title': '29th September 2016', 'tvdb': '0', 'season': '0', 'tvshowtitle': 'Sasural Simar Ka', 'year': '0', 'date': '0', 'meta': '{"tvshowurl": "forums/3948-Sasural-Simar-Ka", "title": "29th September 2016", "url": "threads/959493-Sasural-Simar-Ka-29th-September-2016-Watch-Online?s=83954be3616f4aab7e388876a7cb3a79", "tvshowtitle": "Sasural Simar Ka", "provider": "desirulez_tv", "duration": "1800", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Sasural+Simar+Ka", "name": "29th September 2016"}', 'imdb': '0', 'provider': 'desirulez_tv', 'action': 'addItem', 'tvrage': '0', 'alter': '0'}
    params = {'tmdb': '0', 'name': 'Bajrangi Bhaijaan (2015)', 'title': 'Bajrangi Bhaijaan', 'meta': '{"rating": "8.1", "votes": "43,778", "code": "tt3863552", "cast": [["Salman Khan", ""], ["Kareena Kapoor", ""], ["Nawazuddin Siddiqui", ""], ["Harshaali Malhotra", ""]], "plot": "A little mute girl from a Pakistan village gets lost on her return back from a trip to India. In Kurukshetra, she meets Pawan - a devout Hanuman Bakth - who is in the midst of a challenge posed by his lover\'s father. In trying to discover her parents, he develops an unshakable bond with the kid. He tries to get into Pakistan through a path righteous to his conscience and later, with a smart Pakistani news reporter for company and makes the search, a story that captures the imagination of the public in both countries.", "fanart": "https://walter.trakt.us/images/movies/000/221/962/fanarts/medium/46dbb493c7.jpg", "poster": "https://walter.trakt.us/images/movies/000/221/962/posters/medium/48d0c4a563.jpg", "title": "Bajrangi Bhaijaan", "originaltitle": "Bajrangi Bhaijaan", "premiered": "2015-07-17", "next": "http://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&languages=hi&count=40&start=1&start=1&sort=release_date,desc&page=4&ref_=adv_nxt", "director": "Kabir Khan", "writer": "Vijayendra Prasad / Vijayendra Prasad / Kabir Khan / Parveez Sheikh / Asad Hussain / Kausar Munir / Kabir Khan", "imdb": "tt3863552", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Bajrangi+Bhaijaan+%282015%29", "year": "2015", "duration": "9780", "genre": "Action / Comedy / Drama", "metacache": false}', 'imdb': 'tt3863552', 't': '20161006155052626000', 'year': '2015', 'action': 'play'}
    #params = {'tmdb': '0', 'name': 'Baar Baar Dekho (2016)', 'title': 'Baar Baar Dekho', 'meta': '{"rating": "7.7", "votes": "107", "code": "tt5197544", "cast": [["Sidharth Malhotra", ""], ["Katrina Kaif", ""], ["Sayani Gupta", ""], ["Rajit Kapoor", ""]], "plot": "\'Baar Baar Dekho\' is a love-story, which unfolds through flash-backs and flash-forwards. Recently actor Sidharth Malhotra has revealed that, the movie has a unique and has a very unusual storyline. The film is neither science fiction nor does it revolve around time travel. The styling is currently underway. Film has started in 2015 September for which Katrina and Sidharth had shot in London.", "fanart": "https://walter.trakt.us/images/movies/000/234/732/fanarts/original/31167425c6.jpg", "poster": "https://walter.trakt.us/images/movies/000/234/732/posters/medium/6d61985db8.jpg", "title": "Baar Baar Dekho", "originaltitle": "Baar Baar Dekho", "premiered": "2016-09-09", "next": "http://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&languages=hi&count=40&start=1&start=1&sort=release_date,desc&page=2&ref_=adv_nxt", "director": "Nitya Mehra", "writer": "Sri Rao / Nitya Mehra / Sri Rao / Anuvab Pal / Anvita Dutt", "imdb": "tt5197544", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Baar+Baar+Dekho+%282016%29", "year": "2016", "duration": "8460", "genre": "Action / Comedy / Drama", "metacache": false}', 'imdb': 'tt5197544', 't': '20161006162305514000', 'year': '2016', 'action': 'play'}
    #params = {'tmdb': '0', 'name': 'Rustom (2016)', 'title': 'Rustom', 'meta': '{"rating": "7.3", "votes": "6,499", "code": "tt5165344", "cast": [["Akshay Kumar", ""], ["Ileana", ""], ["Esha Gupta", ""], ["Manoj Bajpayee", ""]], "plot": "Naval officer Rustom Pavri returns from his posting and finds his wife Cynthia is away from home since last two days his marriages is on the rocks when he finds love letters in cupboard which indicates that Cynthia has found love in one of his friend Vikram Makhija an arrogant business tycoon ,Rustom then issues a pistol from Naval Ship\'s Armory and shoots Vikram three times in his chest living him dead and surrender himself to senior inspector Vincent Lobo.", "fanart": "https://walter.trakt.us/images/movies/000/234/965/fanarts/medium/e982aad610.jpg", "poster": "https://walter.trakt.us/images/movies/000/234/965/posters/medium/c853ec5030.jpg", "title": "Rustom", "originaltitle": "Rustom", "premiered": "2016-08-12", "next": "http://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&languages=hi&count=40&start=1&start=1&sort=release_date,desc&page=2&ref_=adv_nxt", "director": "Dharmendra Suresh Desai", "writer": "Vipul K. Rawal", "imdb": "tt5165344", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Rustom+%282016%29", "year": "2016", "duration": "8880", "genre": "Crime / Drama / Mystery", "metacache": false}', 'imdb': 'tt5165344', 't': '20161006162610402000', 'year': '2016', 'action': 'play'}
    #params = {'tmdb': '330431', 'name': 'NH10 (2015)', 'title': 'NH10', 'meta': '{"rating": "6.22", "votes": "9", "tmdb": "330431", "name": "NH10 (2015)", "title": "NH10", "fanart": "http://image.tmdb.org/t/p/original/4A6QmdOzfFMe2HSIi2BZMHMJOXy.jpg", "tagline": "A woman, stacked against all odds, manages to not just stick it out but indeed give it back.", "plot": "A woman, stacked against all odds, manages to not just stick it out but indeed give it back.", "poster": "http://image.tmdb.org/t/p/w500/15xjX0ULsnnJpegmTwlfmDn4drO.jpg", "next": "", "originaltitle": "NH10", "premiered": "2015-03-13", "year": "2015", "duration": "7200", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=NH10+%282015%29", "metacache": false}', 'imdb': '0', 't': '20161007092138014000', 'year': '2015', 'action': 'play'}
    params = {'tmdb': '0', 'name': 'Laal Rang (2016)', 'title': 'Laal Rang', 'meta': '{"rating": "8.1", "votes": "508", "code": "tt5600714", "cast": [["Piaa Bajpai", ""], ["Meenakshi Dixit", ""], ["Rajneesh Duggal", ""], ["Randeep Hooda", ""]], "plot": "A social drama full of black humour set in the milieu of Karnal\'s blood theft mafia.", "poster": "https://walter.trakt.us/images/movies/000/236/958/posters/medium/eb78eb0e15.jpg", "title": "Laal Rang", "originaltitle": "Laal Rang", "premiered": "2016-04-22", "next": "http://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&languages=hi&count=40&start=1&start=1&sort=release_date,desc&page=2&ref_=adv_nxt", "director": "Syed Ahmad Afzal", "writer": "Syed Ahmad Afzal / Pankaj Matta", "imdb": "tt5600714", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Laal+Rang+%282016%29", "year": "2016", "duration": "8820", "genre": "Action / Crime / Drama", "metacache": false}', 'imdb': 'tt5600714', 't': '20161007092758021000', 'year': '2016', 'action': 'play'}
    params = {'tmdb': '0', 'name': 'Welcome Back (2015)', 'title': 'Welcome Back', 'meta': '{"rating": "4.2", "votes": "4,200", "code": "tt3159708", "cast": [["Anil Kapoor", ""], ["Nana Patekar", ""], ["Dimple Kapadia", ""], ["John Abraham", ""]], "plot": "Uday Shetty and Majnu Bhai have left the underworld, and are now big businessmen. Two women, Chandni and Maharani, enter their life. Chandni is the new love in Uday Shetty and Majnu\'s life and both friends dream of tying the knot with her. However, Appa - Uday\'s father, plays spoilsport by bringing in his other daughter, Ranjana. He tells Uday Shetty to get her married to someone from a good family. Maharani puts a condition that only after her sister is married, will Chandni will marry one of them. Now, a search to find a suitable husband for Ranjana starts.", "fanart": "https://walter.trakt.us/images/movies/000/222/591/fanarts/medium/713cbb56bd.jpg", "poster": "https://walter.trakt.us/images/movies/000/222/591/posters/medium/fd484fdff3.jpg", "title": "Welcome Back", "originaltitle": "Welcome Back", "premiered": "2015-09-04", "next": "http://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&languages=hi&count=40&start=1&start=1&sort=release_date,desc&page=4&ref_=adv_nxt", "director": "Anees Bazmee", "writer": "Anees Bazmee / Rajeev Kaul / Rajeev Kaul / Anees Bazmee / Rajan Aggarwal / Praful Parekh / Raaj Shaandilyaa", "imdb": "tt3159708", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Welcome+Back+%282015%29", "year": "2015", "duration": "9120", "genre": "Action / Comedy / Crime", "metacache": false}', 'imdb': 'tt3159708', 't': '20161007095717834000', 'year': '2015', 'action': 'play'}

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

    # test search sources
    from resources.lib.sources import einthusan_mv
    from resources.lib.sources import playindiafilms_mv
    from resources.lib.sources import client
    from resources.lib.indexers import movies
    from resources.lib.indexers import episodes

    from resources.lib.sources import sources
    from resources.lib.sources import live_logo
    #live_logo.source().getLivePosters()
    from resources.lib.sources import dynns_live
    from resources.lib.indexers import movies
    from resources.lib.libraries import analytics
    #analytics.sendAnalytics('Installed-3.9.10')
    #url = 'http://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&languages=%s&count=40&start=1&sort=release_date,desc&start=1' % 'hi'
    #movies.movies().get(url, lang='hi')
    #dynns_live.source().getLiveSource()
    #sources().play(name, title, year, imdb, tmdb, tvdb, tvrage, season, episode, tvshowtitle, alter, date, meta, url)
    source = sources().getSources(name, title, year, imdb, tmdb, tvdb, tvrage, season, episode, tvshowtitle, alter, date, meta)

    '''import json, urllib
    source = {"provider":provider, "url":url, "quality":'HD', "label":provider, "source":provider}
    tmp=json.dumps([source])
    print tmp
    tmp= urllib.quote_plus(tmp)
    print tmp
    tmp = urllib.unquote_plus(tmp)
    print json.loads(tmp)'''


except:
    from resources.lib.libraries import client
    import traceback
    traceback.print_exc()
    client.printException('aftershock-testharness')