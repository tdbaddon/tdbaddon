import unittest, sys
sys.argv = ['plugin.video.aftershock', '1']

from resources.lib.libraries import logger
from resources.lib.sources import apnaview_mv
from resources.lib.sources import crazy4ad_mv_tv
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

from resources.lib.sources import json_live
from resources.lib.sources import ditto_live
from resources.lib.sources import dynns_live
from resources.lib.sources import cinefun_live


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

    @unittest.skip("Working")
    def test_apnaview(self):
        call = apnaview_mv.source()
        self.source(call)

    @unittest.skip("Working")
    def test_crazy4ad(self):
        self.imdb = 'tt5165344'
        self.title = 'Rustom'
        self.year = '2016'
        call = crazy4ad_mv_tv.source()
        self.source(call)

    def test_desihdmovies(self):
        call = desihdmovies_mv.source()
        self.source(call)

    @unittest.skip("Working")
    def test_desihit(self):
        call = desihit_mv.source()
        self.source(call)

    @unittest.skip("Working")
    def test_ditto(self):
        self.imdb = 'tt3159708'
        self.title = 'Welcome Back'
        self.year = '2015'
        call = ditto_mv.source()
        self.source(call)

    @unittest.skip("Working")
    def test_einthusan(self):
        call = einthusan_mv.source()
        self.source(call)

    def test_erosnow(self):
        self.imdb = 'tt4501576'
        self.title = 'Dirty Politics'
        self.year = '2015'
        call = erosnow_mv.source()
        self.source(call)

    @unittest.skip("Working")
    def test_filmywap(self):
        call = filmywap_mv.source()
        self.source(call)

    @unittest.skip("Working")
    def test_hdbuffer(self):
        call = hdbuffer_mv.source()
        self.source(call)

    @unittest.skip("Working")
    def test_hevcfilm(self):
        call = hevcfilm_mv.source()
        self.source(call)

    @unittest.skip("Working")
    def test_hindilinks4u(self):
        call = hindilinks4u_mv.source()
        self.source(call)
    @unittest.skip("Working-Need improvement for the IP address handling")
    def test_hotstar(self):
        call = hotstar_mv.source()
        self.source(call)

    @unittest.skip("Working")
    def test_ibollytv(self):
        call = ibollytv_mv.source()
        self.source(call)

    @unittest.skip("Working")
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
        call = pubfilm_mv.source()
        self.source(call)

    def test_primewire(self):
        call = primewire_mv.source()
        self.source(call)

    @unittest.skip("Working")
    def test_putlocker(self):
        call = putlocker_mv.source()
        self.source(call)

    def test_putlocker(self):
        call = desirulez_mv_tv.source()
        self.source(call)

class TestingLive(unittest.TestCase):

    def source(self, call, generateJSON):
        sourceurl = call.getLiveSource(generateJSON)
        self.assertGreater(len(sourceurl), 0, 'No Sources found')

    def test_json(self):
        call = json_live.source()
        self.source(call, False)
    @unittest.skip("Working")
    def test_ditto(self):
        call = ditto_live.source()
        self.source(call, False)
    @unittest.skip("Working")
    def test_dittoGenerateJSON(self):
        call = ditto_live.source()
        self.source(call, True)

    def test_cinefunGenerateJSON(self):
        call = cinefun_live.source()
        self.source(call, True)

if __name__ == '__main__' :
    unittest.main()