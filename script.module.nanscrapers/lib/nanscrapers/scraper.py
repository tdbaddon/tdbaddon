import abc
import xbmcaddon

abstractstaticmethod = abc.abstractmethod
class abstractclassmethod(classmethod):
    __isabstractmethod__ = True

    def __init__(self, callable):
        callable.__isabstractmethod__ = True
        super(abstractclassmethod, self).__init__(callable)

class Scraper:
    __metaclass__ = abc.ABCMeta
    domains = ['localdomain']
    name = "Scraper"

    @classmethod
    def get_setting(cals, key):
        return xbmcaddon.Addon('script.module.nanscrapers').getSetting(key)

    @classmethod
    def _is_enabled(clas):
        return clas.get_setting(clas.name + '_enabled') == 'true'

    @classmethod
    def get_settings_xml(clas):
        xml = [
            '<setting id="%s_enabled" ''type="bool" label="Enabled" default="true"/>' % (clas.name)
        ]
        return xml

    def scrape_movie(self, title, year, imdb):
        """
scrapes scraper site for movie links
        :param str title: movie title
        :param str year: year the movie came out
        :param str imdb: imdb identifier
        :return: a list of video sources represented by dicts with format:
          {'source': video source (str), 'quality': quality (str), 'scraper': scraper name (str) , 'url': url (str), 'direct': bool}
        :rtype: list(dict[str,str or bool])
        """
        pass

    def scrape_episode(self,title, show_year, year, season, episode, imdb, tvdb):
        """
scrapes scraper site for episode links
        :param str title: title of the tv show
        :param str show_year: year tv show started
        :param str year: year episode premiered
        :param str season: season number of the episode
        :param str episode: episode number
        :param str imdb: imdb identifier
        :param str tvdb: tvdb identifier
        :return: a list of video sources represented by dicts with format:
          {'source': video source (str), 'quality': quality (str), 'scraper': scraper name (str) , 'url': url (str), 'direct': bool}
        :rtype: list(dict[str,str or bool])
        """
        pass

    def scrape_music(self, title, artist):
        """
scrapes scraper site for song links
        :param title: song title
        :param artist: song artist
        :return: a list of music sources represented by dicts with format:
          {'source': music source (str), 'quality': quality (str), 'scraper': scraper name (str) , 'url': url (str), 'direct': bool}
        :rtype: list(dict[str,str or bool])
        """
        pass
