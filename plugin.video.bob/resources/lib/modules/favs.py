try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database

from resources.lib.modules import control
import urllib

table = "favorites"


def add_favorite(name, fav_type, link, poster, fanart):
    try:
        control.makeFile(control.dataPath)
        dbcon = database.connect(control.cacheFile)
        dbcur = dbcon.cursor()
        dbcur.execute(
            "CREATE TABLE IF NOT EXISTS %s (""name TEXT, ""fav_type TEXT, ""link TEXT, ""poster TEXT, ""fanart TEXT, ""UNIQUE(name, fav_type)"");" % table)
        dbcur.execute("INSERT INTO %s Values (?, ?, ?, ?, ?)" % table, (name.encode(), fav_type, link, poster, fanart))
        dbcon.commit()
        return True
    except:
        return False


def remove_favorite(name, fav_type, link):
    try:
        control.makeFile(control.dataPath)
        dbcon = database.connect(control.cacheFile)
        dbcur = dbcon.cursor()
        dbcur.execute("DELETE FROM %s WHERE name = \"%s\" AND fav_type = \"%s\"" % (table, name, fav_type))
        dbcon.commit()
        return True
    except:
        return False

def move_favorite(name,fav_type, link):
    import xbmcgui
    import xbmc
    try:
        control.makeFile(control.dataPath)
        dbcon = database.connect(control.cacheFile)
        dbcur = dbcon.cursor()
        dbcur.execute("SELECT DISTINCT(fav_type) from %s" % table)
        folders = []
        for row in dbcur:
            folders.append(row[0].title())
        folders.append("New Folder")
        selection = xbmcgui.Dialog().select("Select New Folder", folders)
        if selection != -1:
            selected_folder = folders[selection]
            if selected_folder == "New Folder":
                new_folder_name = xbmcgui.Dialog().input("Input New Name")
                if new_folder_name != "":
                    selected_folder = new_folder_name
            dbcur.execute("UPDATE %s SET fav_type = '%s'  WHERE name = \"%s\" and link=\"%s\"" % (table, selected_folder.lower(), name, link))
            dbcon.commit()
    except:
        return False


def get_favorites(fav_type, url):
    try:
        import resources.lib.indexers.bob
        indexer = resources.lib.indexers.bob.Indexer()
        control.makeFile(control.dataPath)
        dbcon = database.connect(control.cacheFile)
        dbcur = dbcon.cursor()
        dbcur.execute("SELECT * FROM %s WHERE fav_type = '%s'" % (table, fav_type))
        import xbmc
        for match in dbcur:
            name = match[0].encode("utf-8")
            link = match[2].encode("utf-8")
            poster = match[3]
            fanart = match[4]
            if match[2].endswith('.xml'):
                item = {'name': name, 'url': urllib.quote(link).replace("http%3A", "http:"), 'action': 'directory', 'folder': True,
                        'content': '%s-favs' % fav_type, 'poster': poster, 'fanart': fanart}
            else:
                year = indexer.bob_get_tag_content(link, "year", "")
                imdb = indexer.bob_get_tag_content(link, "imdb", "")
                title = indexer.bob_get_tag_content(link, "title", "")
                item = {'name': name, 'vip': "", 'url': link, 'action': "play", 'folder': False, 'poster': poster,
                        'banner': '0', 'fanart': fanart, 'content': '%s-favs' % fav_type, 'imdb': imdb, 'tvdb': '0',
                        'tmdb': '0', 'title': title, 'originaltitle': title, 'tvshowtitle': '', 'year': year,
                        'premiered': '', 'season': '', 'episode': ''}
            indexer.list.append(item)
        if indexer.list == []:
            item = {'name': '..', 'url': 'plugin://plugin.video.bob', 'action': 'plugin', 'folder': False,
                        'content': '', 'poster': '0', 'fanart': '0'}
            indexer.list.append(item)
        indexer.worker()
        indexer.add_directory(indexer.list, parent_url=url)

    except:
        return []


def get_favorites_menu(url):
    import resources.lib.indexers.bob
    indexer = resources.lib.indexers.bob.Indexer()
    try:
        control.makeFile(control.dataPath)
        dbcon = database.connect(control.cacheFile)
        dbcur = dbcon.cursor()
        dbcur.execute("SELECT DISTINCT(fav_type) from %s" % table)
        for row in dbcur:
            fav_type = row[0]
            if fav_type == "movie":
                poster = "http://norestrictions.club/norestrictions.club/main/icons/my_movies.jpg"
            elif fav_type == "tv show":
                poster = "http://norestrictions.club/norestrictions.club/main/icons/my_tv_shows.jpg"
            else:
                poster = "http://norestrictions.club/norestrictions.club/main/icons/my_blank.jpg"
            indexer.list.append({'name': fav_type.title(), 'url': url, 'action': 'getfavorites_%s' % fav_type, 'folder': True,
                                 'poster': poster})
        if indexer.list == []:
            import xbmcgui
            xbmcgui.Dialog().ok("Bob's Faves", "Add Your Bob Faves Here")
        indexer.worker()
        indexer.add_directory(indexer.list, parent_url=url)
    except:
        pass


def check_empty(fav_type = None):
    try:
        control.makeFile(control.dataPath)
        dbcon = database.connect(control.cacheFile)
        dbcur = dbcon.cursor()
        if not fav_type:
            dbcur.execute("SELECT * FROM %s" % (table))
        else:
            dbcur.execute("SELECT * FROM %s WHERE fav_type=%s" % (table, fav_type))
        for match in dbcur:
            return False
        return True
    except:
        return True
