import unittest, sys
sys.argv = ['plugin.video.aftershock', '1']

from resources.lib.libraries import logger
from resources.lib.sources import apnaview_mv
from resources.lib.sources import crazy4ad_mv
from resources.lib.sources import desihdmovies_mv
from resources.lib.sources import desihit_mv
from resources.lib.sources import ditto_mv
from resources.lib.sources import einthusan_mv
from resources.lib.sources import erosnow_mv
from resources.lib.sources import filmywap_mv
from resources.lib.sources import hdbuffer_mv
from resources.lib.sources import hevcfilm_mv
from resources.lib.sources import hindilinks4u_mv
from resources.lib.sources import hotstar_mv
from resources.lib.sources import ibollytv_mv
from resources.lib.sources import movie25_mv
from resources.lib.sources import ninemovies_mv
from resources.lib.sources import onemovies_mv
from resources.lib.sources import playindiafilms_mv
from resources.lib.sources import pubfilm_mv
from resources.lib.sources import putlocker_mv
from resources.lib.sources import primewire_mv
from resources.lib.sources import desirulez_mv_tv
from resources.lib.sources import dltube_mv
from resources.lib.sources import miradetodo_mv
from resources.lib.sources import movies14_mv
from resources.lib.sources import movieshd_mv
from resources.lib.sources import rlsmovies_mv
from resources.lib.sources import ymovies_mv

from resources.lib.sources import json_live
from resources.lib.sources import ditto_live
from resources.lib.sources import dynns_live
from resources.lib.sources import cinefun_live
from resources.lib.sources import swift_live
from resources.lib.sources import iptv_live


class TestingMovies(unittest.TestCase):
    def setUp(self):
        self.imdb = 'tt3595298'
        self.title = 'Prem Ratan Dhan Payo'
        self.year = '2015'

    def source(self, call):
        movieUrl = call.get_movie(self.imdb, self.title, self.year)
        self.assertIsNotNone(movieUrl, 'Movie URL Not Found')
        logger.debug('[%s] Movie URL : %s' % (call.__class__, movieUrl))

        sourceurl = call.get_sources(movieUrl)
        self.assertGreater(len(sourceurl), 0, 'No Sources found')

    def test_apnaview(self):
        call = apnaview_mv.source()
        self.source(call)

    def test_crazy4ad(self):
        self.imdb = 'tt5165344'
        self.title = 'Rustom'
        self.year = '2016'
        call = crazy4ad_mv.source()
        self.source(call)

    def test_desihdmovies(self):
        self.imdb = 'tt5165344'
        self.title = 'Rustom'
        self.year = '2016'
        call = desihdmovies_mv.source()
        self.source(call)

    def test_desihit(self):
        call = desihit_mv.source()
        self.source(call)

    def test_ditto(self):
        self.imdb = 'tt3159708'
        self.title = 'Welcome Back'
        self.year = '2015'
        call = ditto_mv.source()
        self.source(call)

    def test_einthusan(self):
        call = einthusan_mv.source()
        self.source(call)

    def test_erosnow(self):
        self.imdb = 'tt4501576'
        self.title = 'Dirty Politics'
        self.year = '2015'
        call = erosnow_mv.source()
        self.source(call)

    def test_filmywap(self):
        call = filmywap_mv.source()
        self.source(call)

    def test_hdbuffer(self):
        call = hdbuffer_mv.source()
        self.source(call)

    def test_hevcfilm(self):
        call = hevcfilm_mv.source()
        self.source(call)

    def test_hindilinks4u(self):
        call = hindilinks4u_mv.source()
        self.source(call)
    def test_hotstar(self):
        call = hotstar_mv.source()
        self.source(call)

    def test_ibollytv(self):
        call = ibollytv_mv.source()
        self.source(call)

    def test_movie25(self):
        call = movie25_mv.source()
        self.source(call)

    def test_ninemovies(self):
        call = ninemovies_mv.source()
        self.source(call)

    def test_onemovies(self):
        call = onemovies_mv.source()
        self.source(call)

    @unittest.skip("BROKEN")
    def test_playindiafilms(self):
        call = playindiafilms_mv.source()
        self.source(call)


    def test_pubfilm(self):
        self.imdb = 'tt4387040'
        self.title = 'Airlift'
        self.year = '2016'
        call = pubfilm_mv.source()
        self.source(call)

    def test_primewire(self):
        self.imdb = 'tt5165344'
        self.title = 'Rustom'
        self.year = '2016'
        call = primewire_mv.source()
        self.source(call)

    def test_putlocker(self):
        self.imdb = 'tt5165344'
        self.title = 'Rustom'
        self.year = '2016'
        call = putlocker_mv.source()
        self.source(call)

    def test_desirulez(self):
        call = desirulez_mv_tv.source()
        self.source(call)
    def test_dltube(self):
        call = dltube_mv.source()
        self.source(call)
    def test_miradetodo_mv(self):
        call = miradetodo_mv.source()
        self.source(call)
    def test_movies14_mv(self):
        call = movies14_mv.source()
        self.source(call)
    def test_movieshd_mv_tv(self):
        self.imdb = 'tt5165344'
        self.title = 'Rustom'
        self.year = '2016'
        call = movieshd_mv.source()
        self.source(call)
    def test_rlsmovies_mv_tv(self):
        call = rlsmovies_mv.source()
        self.source(call)
    def test_ymovies_mv_tv(self):
        call = ymovies_mv.source()
        self.source(call)

class TestingLive(unittest.TestCase):
    def test_getLiveSources(self):
        from resources.lib.sources import sources
        name = None
        title = None
        year = None
        imdb = None
        tmdb = None
        tvdb = None
        tvrage = None
        season = None
        episode = None
        tvshowtitle = None
        alter = None
        date = None
        meta = None
        sourceList = sources().getSources(name, title, year, imdb, tmdb, tvdb, tvrage, season, episode, tvshowtitle,
                                          alter, date, meta)

    def source(self, call, generateJSON):
        sourceurl = call.getLiveSource()
        self.assertGreater(len(sourceurl), 0, 'No Sources found')
        return

    def test_json(self):
        call = json_live.source()
        self.source(call, False)

    def test_ditto(self):
        call = ditto_live.source()
        self.source(call, False)

    def test_cinefun(self):
        call = cinefun_live.source()
        self.source(call, False)

    def test_cinefunGenerateJSON(self):
        call = cinefun_live.source()
        self.source(call, True)

    def test_dittoGenerateJSON(self):
        call = ditto_live.source()
        self.source(call, True)

    def test_swiftGenerateJSON(self):
        call = swift_live.source()
        self.source(call, True)

    def test_dydnsGenerateJSON(self):
        call = dynns_live.source()
        self.source(call, True)

    def test_swiftGenerateJSON(self):
        call = swift_live.source()
        self.source(call, True)

    def test_iptvGenerateJSON(self):
        call = iptv_live.source()
        self.source(call, True)

    def test_cinefunZeeTVHD(self):
        from resources.lib.sources import sources
        item = {"name": "ZEE TV HD", "url": "73833", "debrid": '', "direct": False, "source": "cinefun",
                "provider": "cinefun", "quality": "HD"}
        sources().sourcesResolve(item)

    def test_dydnsPlayAajTak(self):
        from resources.lib.sources import sources
        item = {"name": "AAJ TAK", "url": "http://live1.dyndns.tv:8081/iptv/aajtak/playlist.m3u8", "debrid": '',
                "direct": False, "source": "dynns", "provider": "dynns", "quality": "HD"}
        sources().sourcesResolve(item)

    def test_swiftPlay9XJalwa(self):
        from resources.lib.sources import sources
        item = {"name": "9X JALWA", "url": "http://163.172.142.242:8081/swiftnew/9xjalwa/playlist.m3u8", "debrid": '',
                "poster": "C:\\Users\\vgupta2\\AppData\\Roaming\\Kodi\\addons\\script.aftershock.artwork\\resources\\media\\logos\\9x_jalwa.png",
                "direct": False, "source": "swift",
                "meta": "{\"poster\": \"C:\\\\Users\\\\vgupta2\\\\AppData\\\\Roaming\\\\Kodi\\\\addons\\\\script.aftershock.artwork\\\\resources\\\\media\\\\logos\\\\9x_jalwa.png\", \"iconImage\": \"C:\\\\Users\\\\vgupta2\\\\AppData\\\\Roaming\\\\Kodi\\\\addons\\\\script.aftershock.artwork\\\\resources\\\\media\\\\logos\\\\9x_jalwa.png\", \"thumb\": \"C:\\\\Users\\\\vgupta2\\\\AppData\\\\Roaming\\\\Kodi\\\\addons\\\\script.aftershock.artwork\\\\resources\\\\media\\\\logos\\\\9x_jalwa.png\"}",
                "provider": "swift", "quality": "HD"}
        sources().sourcesResolve(item)



if __name__ == '__main__' :
    unittest.main()