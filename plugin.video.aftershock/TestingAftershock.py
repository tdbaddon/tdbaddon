import sys
import unittest

sys.argv = ['plugin.video.aftershock', '1']

from ashock.modules import logger

class TestingMovies(unittest.TestCase):
    def setUp(self):
        self.imdb = 'tt3595298'
        self.title = 'Prem Ratan Dhan Payo'
        self.year = '2015'


    def source(self, call):
        movieUrl = call.movie(self.imdb, self.title, self.year)
        self.assertIsNotNone(movieUrl, 'Movie URL Not Found')
        logger.debug('[%s] Movie URL : %s' % (call.__class__, movieUrl))

        sourceurl = call.sources(movieUrl)
        self.assertGreater(len(sourceurl), 0, 'No Sources found')

    def test_apnaview(self):
        from resources.lib.sources import apnaview
        call = apnaview.source()
        self.source(call)

    def test_bmoviez(self):
        self.imdb = 'tt5165344'
        self.title = 'Rustom'
        self.year = '2016'
        from resources.lib.sources import bmoviez
        call = bmoviez.source()
        self.source(call)

    def test_crazy4ad(self):
        self.imdb = 'tt5165344'
        self.title = 'Rustom'
        self.year = '2016'
        from resources.lib.sources import crazy4ad
        call = crazy4ad.source()
        self.source(call)

    def test_desihdmovies(self):
        self.imdb = 'tt5165344'
        self.title = 'Rustom'
        self.year = '2016'
        from resources.lib.sources import desihdmovies
        call = desihdmovies.source()
        self.source(call)

    def test_desirulez(self):
        from resources.lib.sources import desirulez
        call = desirulez.source()
        self.source(call)

    def test_dltube(self):
        from resources.lib.sources import dltube
        call = dltube.source()
        self.source(call)

    def test_einthusan(self):
        from resources.lib.sources import einthusan
        call = einthusan.source()
        self.source(call)

    def test_erosnow(self):
        self.imdb = 'tt4501576'
        self.title = 'Dirty Politics'
        self.year = '2015'
        from resources.lib.sources import erosnow
        call = erosnow.source()
        self.source(call)

    def test_filmywap(self):
        from resources.lib.sources import filmywap
        call = filmywap.source()
        self.source(call)

    def test_hdbuffer(self):
        from resources.lib.sources import hdbuffer
        call = hdbuffer.source()
        self.source(call)

    def test_hevcfilm(self):
        from resources.lib.sources import hevcfilm
        call = hevcfilm.source()
        self.source(call)

    def test_hindilinks4u(self):
        from resources.lib.sources import hindilinks4u
        call = hindilinks4u.source()
        self.source(call)

    def test_hotstar(self):
        from resources.lib.sources import hotstar
        call = hotstar.source()
        self.source(call)

    def test_ibollytv(self):
        from resources.lib.sources import ibollytv
        call = ibollytv.source()
        self.source(call)

    def test_mdesihit(self):
        from resources.lib.sources import mdesihit
        call = mdesihit.source()
        self.source(call)

    def test_mditto(self):
        self.imdb = 'tt3159708'
        self.title = 'Welcome Back'
        self.year = '2015'
        from resources.lib.sources import mditto
        call = mditto.source()
        self.source(call)

    def test_miradetodo(self):
        from resources.lib.sources import miradetodo
        call = miradetodo.source()
        self.source(call)

    def test_movie25(self):
        from resources.lib.sources import movie25
        call = movie25.source()
        self.source(call)

    def test_movies14(self):
        from resources.lib.sources import movies14
        call = movies14.source()
        self.source(call)

    def test_movieshd(self):
        self.imdb = 'tt5165344'
        self.title = 'Rustom'
        self.year = '2016'
        from resources.lib.sources import movieshd
        call = movieshd.source()
        self.source(call)

    def test_ninemovies(self):
        from resources.lib.sources import ninemovies
        call = ninemovies.source()
        self.source(call)

    def test_onemovies(self):
        from resources.lib.sources import onemovies
        call = onemovies.source()
        self.source(call)

    def test_primewire(self):
        self.imdb = 'tt5165344'
        self.title = 'Rustom'
        self.year = '2016'
        from resources.lib.sources import primewire
        call = primewire.source()
        self.source(call)

    def test_pubfilm(self):
        self.imdb = 'tt4387040'
        self.title = 'Airlift'
        self.year = '2016'
        from resources.lib.sources import pubfilm
        call = pubfilm.source()
        self.source(call)

    def test_putlocker(self):
        self.imdb = 'tt5165344'
        self.title = 'Rustom'
        self.year = '2016'
        from resources.lib.sources import putlocker
        call = putlocker.source()
        self.source(call)

    def test_rajtamil(self):
        self.title = 'Tharkappu'
        self.imdb = None
        self.year = '2016'
        from resources.lib.sources import rajtamil
        call = rajtamil.source()
        self.source(call)

    def test_rlsmovies(self):
        from resources.lib.sources import rlsmovies
        call = rlsmovies.source()
        self.source(call)

    def test_tamilgun(self):
        self.title = 'Tharkappu'
        self.imdb = None
        self.year = '2016'
        from resources.lib.sources import tamilgun
        call = tamilgun.source()
        self.source(call)

    def test_tamilyogi(self):
        self.title = 'Tharkappu'
        self.imdb = None
        self.year = '2016'
        from resources.lib.sources import tamilyogi
        call = tamilyogi.source()
        self.source(call)

    def test_watchfree(self):
        self.imdb = 'tt5165344'
        self.title = 'Rustom'
        self.year = '2016'
        from resources.lib.sources import watchfree
        call = watchfree.source()
        self.source(call)

    def test_ymovies(self):
        from resources.lib.sources import ymovies
        call = ymovies.source()
        self.source(call)

class TestingLive(unittest.TestCase):
    def test_getLiveSources(self):
        from resources.lib.sources import sources
        name = None
        title = None
        year = None
        imdb = None
        tvdb = None
        season = None
        episode = None
        tvshowtitle = None
        date = None
        meta = None
        sourceList = sources().getSources(name, title, year, imdb, tvdb, season, episode, tvshowtitle,
                                          date, meta)

    def source(self, call, generateJSON):
        from resources.lib.indexers import livetv
        livetv.sources().getLiveGenre()
        sourceurl = call.livetv()
        self.assertGreater(len(sourceurl), 0, 'No Sources found')
        return

    def test_cinefunGenerateJSON(self):
        from resources.lib.sources import cinefun
        call = cinefun.source()
        self.source(call, True)

    def test_dydnsGenerateJSON(self):
        from resources.lib.sources import dynns
        call = dynns.source()
        self.source(call, True)

    def test_iptvGenerateJSON(self):
        from resources.lib.sources import iptv
        call = iptv.source()
        self.source(call, True)

    def test_dittoGenerateJSON(self):
        from resources.lib.sources import lditto
        call = lditto.source()
        self.source(call, True)

    def test_solidGenerateJSON(self):
        from resources.lib.sources import solid
        call = solid.source()
        self.source(call, True)

    def test_staticGenerateJSON(self):
        from resources.lib.sources import staticjson
        call = staticjson.source()
        self.source(call, True)

    def test_swiftGenerateJSON(self):
        from resources.lib.sources import swift
        call = swift.source()
        self.source(call, True)

if __name__ == '__main__' :
    unittest.main()