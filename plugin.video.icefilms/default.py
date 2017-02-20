#!/usr/bin/python

#Icefilms.info v1.1.0 - Eldorado

#All code Copyleft (GNU GPL v2) Eldorado and icefilms-xbmc team

############### Imports ############################
#standard module imports
import sys,os
import time,re
import urllib,urllib2,base64
import random
import copy
import threading
import string
import traceback

reload(sys)
sys.setdefaultencoding('utf8')

############ Set prepare_zip to True in order to scrape the entire site to create a new meta pack ############
''' 
Setting to true will also enable a new menu option 'Create Meta Pack' which will scrape all categories and download covers & backdrops 
'''

#prepare_zip = True
prepare_zip = False


##############################################################################################################

import xbmc, xbmcplugin, xbmcgui, xbmcvfs, datetime

''' Use addon common library for http calls '''
try:
    from addon.common.net import Net
    from addon.common.addon import Addon
except Exception, e:
    xbmc.log('Failed to import script.module.addon.common: %s' % e)
    xbmcgui.Dialog().ok("Icefilms Import Failure", "Failed to import addon.common", "A component needed by Icefilms is missing on your system", "Please visit www.tvaddons.ag for support")
net = Net()

addon_id = 'plugin.video.icefilms'
addon = Addon(addon_id, sys.argv)
datapath = addon.get_profile()

try:
    from metahandler import metahandlers
    metahandler_version = metahandlers.common.addon.get_version()
    key = base64.b64decode('YzQ0ZDBjN2VkMTMyY2MyZWM5MDU4MWE3Y2ExYThmMDI=')
    metaget=metahandlers.MetaData(tmdb_api_key=key)
except Exception, e:
    addon.log_error('Failed to import script.module.metahandler: %s' % e)
    xbmcgui.Dialog().ok("Icefilms Import Failure", "Failed to import Metahandlers", "A component needed by Icefilms is missing on your system", "Please visit www.tvaddons.ag for support")

    
import urlresolver

########################### Queries ############################

url = addon.queries.get('url', '')
name = addon.queries.get('name', '')
imdbnum = addon.queries.get('imdbnum', '')
tmdbnum = addon.queries.get('tmdbnum', '')
mode = addon.queries.get('mode', '')
dirmode = addon.queries.get('dirmode', '')
season_num = addon.queries.get('season', '')
episode_num = addon.queries.get('episode', '')
video_type = addon.queries.get('videoType', '')
video_url = addon.queries.get('videoUrl', '')
stacked_parts = addon.queries.get('stackedParts', '')
nextPage = addon.queries.get('nextPage', '')
search = addon.queries.get('search', '')
video_id = addon.queries.get('t', '')

addon.log_debug('----------------Icefilms Addon Param Info----------------------')
addon.log_debug('--- Version: ' + str(addon.get_version()))
addon.log_debug('--- Mode: ' + str(mode))
addon.log_debug('--- DirMode: ' + str(dirmode))
addon.log_debug('--- URL: ' + str(url))
addon.log_debug('--- Video Id: ' + str(video_id))
addon.log_debug('--- Video Type: ' + str(video_type))
addon.log_debug('--- Video URL: ' + str(video_url))
addon.log_debug('--- Name: ' + str(name))
addon.log_debug('--- IMDB: ' + str(imdbnum))
addon.log_debug('--- TMDB: ' + str(tmdbnum))
addon.log_debug('--- Season: ' + str(season_num))
addon.log_debug('--- Episode: ' + str(episode_num))
addon.log_debug('--- MyHandle: ' + str(sys.argv[1]))
addon.log_debug('---------------------------------------------------------------')

################################################################

#get path to me
icepath = addon.get_path()

#append lib directory
sys.path.append( os.path.join( icepath, 'resources', 'lib' ) )

#imports of things bundled in the addon
import container_urls,clean_dirs,htmlcleaner
import debridroutines


#Check for DB in old location (cache folder), move it to addon profile if exists
special_db = os.path.join(xbmc.translatePath('special://temp/'), 'ice_cache.db')
if xbmcvfs.exists(special_db):
    if not xbmcvfs.copy(special_db, xbmc.translatePath(os.path.join(datapath, 'ice_cache.db'))):
        addon.log_error("copy error")
    else:
        xbmcvfs.rename(special_db, os.path.join(xbmc.translatePath('special://temp/'), 'ice_cache_old.db'))

#Database utilities
from db_utils import DB_Connection
db_connection = DB_Connection(addon)

from cleaners import *
from BeautifulSoup import BeautifulSoup
from xgoogle.search import GoogleSearch

#Common Cache
# plugin constants
dbg = False # Set to false if you don't want debugging

#Common Cache
try:
  import StorageServer
except:
  import storageserverdummy as StorageServer
cache = StorageServer.StorageServer(addon_id)

####################################################

############## Constants / Variables ###############

# global constants
ICEFILMS_URL = addon.get_setting('icefilms-url')
if not ICEFILMS_URL.endswith("/"):
    ICEFILMS_URL = ICEFILMS_URL + "/"

ICEFILMS_AJAX = ICEFILMS_URL+'membersonly/components/com_iceplayer/video.phpAjaxResp.php?s=%s&t=%s&app_id=if_' + addon.get_version()
ICEFILMS_AJAX_REFER = ICEFILMS_URL + 'membersonly/components/com_iceplayer/video.php?h=374&w=631&vid=%s&img='
ICEFILMS_REFERRER = ICEFILMS_URL
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36'
ACCEPT = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'

VideoType_Movies = 'movie'
VideoType_TV = 'tvshow'
VideoType_Season = 'season'
VideoType_Episode = 'episode'


#useful global strings:
iceurl = ICEFILMS_URL
meta_setting = addon.get_setting('use-meta')
downloadPath = addon.get_setting('download-folder')

#Auto-watch
currentTime = 1
totalTime = 0

callEndOfDirectory = True

#Variable for multi-part
finalPart = True

#Paths Etc
cookie_path = os.path.join(datapath, 'cookies')
downinfopath = os.path.join(datapath, 'downloadinfologs')
cookie_jar = os.path.join(cookie_path, 'cookiejar.lwp')
ice_cookie = os.path.join(cookie_path, 'icefilms.lwp')
art_path = os.path.join(icepath, 'resources', 'art')
               
####################################################

def xbmcpath(path,filename):
     translatedpath = os.path.join(xbmc.translatePath( path ), ''+filename+'')
     return translatedpath
  
def Notify(typeq,title,message,times, line2='', line3=''):
     #simplified way to call notifications. common notifications here.
     msgList = [message, line2, line3]
     if title == '':
          title='Icefilms Notification'
     if typeq == 'small' or typeq == 'Download Alert':
          if times == '':
               times='5000'
          smallicon=handle_file('smallicon')
          addon.show_small_popup(title=title, msg=message, delay=int(times), image=smallicon)
     elif typeq == 'big':
          addon.show_ok_dialog(msgList, title=title, is_error=False)
     else:
          addon.show_ok_dialog(msgList, title=title, is_error=False)


def handle_file(filename,getmode=''):
     #bad python code to add a get file routine.
     if filename == 'smallicon':
          return_file = xbmcpath(art_path,'smalltransparent2.png')
     elif filename == 'icon':
          return_file = xbmcpath(icepath, 'icon.png')          
     elif filename == 'homepage':
          return_file = xbmcpath(art_path,'homepage.png')
     elif filename == 'movies':
          return_file = xbmcpath(art_path,'movies.png')
     elif filename == 'music':
          return_file = xbmcpath(art_path,'music.png')
     elif filename == 'tvshows':
          return_file = xbmcpath(art_path,'tvshows.png')
     elif filename == 'movies_fav':
        return_file = xbmcpath(art_path,'movies_fav.png')
     elif filename == 'tvshows_fav':
        return_file = xbmcpath(art_path,'tvshows_fav.png')
     elif filename == 'other':
          return_file = xbmcpath(art_path,'other.png')
     elif filename == 'search':
          return_file = xbmcpath(art_path,'search.png')
     elif filename == 'standup':
          return_file = xbmcpath(art_path,'standup.png')
     elif filename == 'localpic':
          return_file = xbmcpath(art_path,'local_file.jpg')

     if getmode == '':
          return return_file
     if getmode == 'open':
          try:
               opened_return_file=openfile(return_file)
               return opened_return_file
          except:
               addon.log_debug('opening failed')
     
def openfile(filename):
    f = xbmcvfs.File(filename)
    contents = f.read()
    f.close()
    return contents


def save(filename,contents):  
    f = xbmcvfs.File(filename, 'w')
    f.write(contents)
    f.close()


def appendfile(filename,contents):  
    f = xbmcvfs.File(filename, 'a')
    f.write(contents)
    f.close()


def Startup_Routines():
     
     addon.log("startup")
     # avoid error on first run if no paths exists, by creating paths
     if not xbmcvfs.exists(datapath): xbmcvfs.mkdir(datapath)
     if not xbmcvfs.exists(downinfopath): xbmcvfs.mkdir(downinfopath)
     if not xbmcvfs.exists(cookie_path): xbmcvfs.mkdir(cookie_path)
              
     # Run the startup routines for special download directory structure 
     DLDirStartup()

     #Initialize cache DB
     db_connection.init_database()
     
     #Convert file system favourites to DB
     convert_favourites()
     
     # Run the login startup routines
     LoginStartup()
     
     # Run the container checking startup routines, if enable meta is set to true
     if meta_setting=='true': ContainerStartup()
     
     #Rescan Next Aired on startup - actually only rescans every 24hrs
     next_aired = str2bool(addon.get_setting('next-aired'))
     if next_aired:
         xbmc.executebuiltin("RunScript(%s, silent=true)" % os.path.join(icepath, 'resources/script.tv.show.next.aired/default.py'))


#Upgrade code to convert legacy file system based favourites to cache db
def convert_favourites():

    favpath=os.path.join(datapath, 'Favourites', '')
    backup_favpath = os.path.join(datapath, 'Favourites_Backup', '')
    moviefav=os.path.join(datapath, 'Favourites', 'Movies', '')
    tvfav=os.path.join(datapath, 'Favourites', 'TV', '')
    
    try:
        if xbmcvfs.exists(favpath):
        
            #Reset DB to start fresh
            db_connection.reset_db()
            
            #Process Movie favourites
            if xbmcvfs.exists(moviefav):
                moviedirs, moviefiles = xbmcvfs.listdir(moviefav)
                if moviefiles:
                    
                    for file in moviefiles:
                    
                        filecontents = openfile(os.path.join(moviefav, file))
                        
                        #split it into its component parts
                        info = favRead(filecontents)
                        new_url = parse_url(info[1])
                        
                        db_connection.save_favourite('movie', info[0], new_url, info[3])
                        
                        #if not xbmcvfs.delete(os.path.join(moviefav, file)):
                        #    raise Exception('Favourite Convert - error deleting movie fav file: %s' % file)

                #if not xbmcvfs.rmdir(moviefav):
                #    raise Exception('Favourite Convert - error deleting movie fav folder: %s' % moviefav)

            #Process TV favourites
            if xbmcvfs.exists(tvfav):
            
                tvdirs, tvfiles = xbmcvfs.listdir(tvfav)            
                if tvfiles:
                    
                    for file in tvfiles:
                    
                        filecontents = openfile(os.path.join(tvfav, file))
                        
                        #split it into its component parts
                        info = favRead(filecontents)

                        new_url = parse_url(info[1])

                        db_connection.save_favourite('tvshow', info[0], new_url, info[3])

                        #if not xbmcvfs.delete(os.path.join(tvfav, file)):
                        #    raise Exception('Favourite Convert - error deleting tv show fav file: %s' % file)                       

                #if not xbmcvfs.rmdir(tvfav):
                #    raise Exception('Favourite Convert - error deleting tv fav folder: %s' % tvfav)
                       
            #if not xbmcvfs.rmdir(favpath):
            #    raise Exception('Favourite Convert - error deleting favourite folder: %s' % favpath)

            if not xbmcvfs.rename(favpath, backup_favpath):
                raise Exception('Favourite Convert - error backing up favourites folder: %s' % favpath)
                
            
    except db_connection.db.IntegrityError, e:
        addon.log_error('Favourite Convert - Duplicate favourite attempted to be added: %s' % e)
        Notify('small', 'Icefilms Favourites', 'Error occured converting favourites to cache DB', '')
    except Exception, e:
        addon.log_error('Favourite Convert - error during processing: %s' % e)
        Notify('small', 'Icefilms Favourites', 'Error occured converting favourites to cache DB', '')


def parse_url(url):

    #Re-do the URL in case user has changed base URL in addon settings
    import urlparse
    split_url = urlparse.urlsplit(url)
    
    if split_url.path.startswith('/'):
        part_url = split_url.path[1:]
    else:
        part_url = split_url.path
        
    if split_url.query:
        part_url = part_url + "?" + split_url.query
        
    return part_url


def DLDirStartup():

  # Startup routines for handling and creating special download directory structure 
  SpecialDirs=addon.get_setting('use-special-structure')

  if SpecialDirs == 'true':

     if downloadPath:
        if xbmcvfs.exists(downloadPath):
          tvpath=os.path.join(downloadPath, 'TV Shows', '')
          moviepath=os.path.join(downloadPath, 'Movies', '')

          #IF BASE DIRECTORY STRUCTURE DOESN'T EXIST, CREATE IT
          if not xbmcvfs.exists(tvpath):
              xbmcvfs.mkdir(tvpath)

          if not xbmcvfs.exists(moviepath):
              xbmcvfs.mkdir(moviepath)

          else:
              #IF DIRECTORIES EXIST, CLEAN DIRECTORY STRUCTURE (REMOVE EMPTY DIRECTORIES)
               clean_dirs.do_clean(tvpath)
               clean_dirs.do_clean(moviepath)


def LoginStartup():

    #Get whether user has set an account to use.   
    HideSuccessfulLogin = str2bool(addon.get_setting('hide-successful-login-messages'))
            
def ContainerStartup():

     #Check for previous Icefilms metadata install and delete
     meta_folder = os.path.join(datapath, 'meta_caches', '')
     if xbmcvfs.exists(meta_folder):
         import shutil
         try:
             addon.log_debug('Removing previous Icefilms meta folder: %s' % meta_folder)
             xbmcvfs.rmdir(meta_folder)
         except Exception, e:
             addon.log_error('Failed to delete Icefilms meta folder: %s' % e)
             pass

     #Initialize MetaHandler classe
     mh=metahandlers.MetaData()   

     #Check meta cache DB if meta pack has been installed     
     meta_installed = mh.check_meta_installed(addon_id)
     
     #get containers dict from container_urls.py
     containers = container_urls.get()  
     
     local_install = False
     if addon.get_setting('meta_pack_location_option') == 'Custom':
         local_install = True
         meta_pack_locaton = addon.get_setting('meta_folder_location')
         if not meta_pack_locaton.endswith("/"):
             meta_pack_locaton = meta_pack_locaton + "/"
     else:
         meta_pack_locaton = containers['url_offshore']
                            
     if not meta_installed:

         #Offer to download the metadata DB
         dialog = xbmcgui.Dialog()
         ret = dialog.yesno('Download Meta Containers '+str(containers['date'])+' ?', 'There is a metadata container avaliable.','Install it to get meta information for videos.', 'Would you like to get it? Its a small '+str(containers['db_size'])+'MB download.','Remind me later', 'Install')
         
         if ret==True:

              #MetaContainer will clean up from previous installs, so good idea to always initialize at addon startup
              from metahandler import metacontainers
              mc = metacontainers.MetaContainer()
              work_path = mc.work_path
              
              #download dem files
              get_db_zip=Zip_DL_and_Install(meta_pack_locaton, containers['db_filename'], 'database', work_path, mc, local_install)

              #do nice notification
              if get_db_zip==True:
                   Notify('small','Metacontainer DB Installation Success','','')
                   
                   #Update meta addons table to indicate meta pack was installed with covers
                   mh.insert_meta_installed(addon_id, last_update=containers['date'])
                   
                   #Re-check meta_installed
                   meta_installed = mh.check_meta_installed(addon_id)
              
              else:
                   Notify('small','Metacontainer DB Installation Failure','','')


def Zip_DL_and_Install(url, filename, installtype, work_folder, mc, local_install=False):

    complete = False
    if local_install:
        #Define local path where zip already exists
        filepath=os.path.normpath(os.path.join(url, filename, ''))
        complete = True

    else:
        #define the path to save it to
        filepath=os.path.normpath(os.path.join(work_folder, filename, ''))

        link = url + filename
        
        #2Shared download
        #import resolvers
        #link = resolvers.SHARED2_HANDLER(url)

        filepath_exists=xbmcvfs.exists(filepath)
         
        #if zip does not already exist, download from url, with nice display name.
        if not filepath_exists:
                        
            addon.log_debug('Downloading zip: %s' % link)
            try:
                complete = Download(link, filepath, installtype)
            except Exception, e:
                addon.log_error('******* ERROR - Download Pack Failed: %s' % e)
                Notify('big','Error Downloading Meta Pack', '%s' % e, '')
                pass
           
        else:
            addon.log_debug('zip already downloaded, attempting extraction')

    #Run zip install
    if complete:
        addon.log_debug('*** Handling meta install')
        return mc.install_metadata_container(filepath, installtype)
    else:
        return False


def create_meta_pack():
       
    # This function will scrape all A-Z categories of the entire site
    
    #Insert starting record to addon table so that all data and images are scraped/downloaded
    mh=metahandlers.MetaData()
    mh.insert_meta_installed(addon_id, last_update='Now', movie_covers='true', tv_covers='true', tv_banners='true', movie_backdrops='true', tv_backdrops='true')
    
    A2Z=[chr(i) for i in xrange(ord('A'), ord('Z')+1)]
    
    #addon.log('### GETTING MOVIE METADATA FOR ALL *MUSIC* ENTRIES')
    #MOVIEINDEX(iceurl + 'music/a-z/1')
    addon.log('### GETTING MOVIE METADATA FOR ALL *STANDUP* ENTRIES')
    MOVIEINDEX(iceurl + 'standup/a-z/1')
    #addon.log('### GETTING MOVIE METADATA FOR ALL *OTHER* ENTRIES')
    #MOVIEINDEX(iceurl + 'other/a-z/1')
    addon.log('### GETTING MOVIE METADATA FOR ALL ENTRIES ON: '+'1')
    MOVIEINDEX(iceurl + 'movies/a-z/1')
    for theletter in A2Z:
         addon.log('### GETTING MOVIE METADATA FOR ALL ENTRIES ON: '+theletter)
         MOVIEINDEX(iceurl + 'movies/a-z/' + theletter)

         
    addon.log('### GETTING TV METADATA FOR ALL ENTRIES ON: '+'1')
    TVINDEX(iceurl + 'tv/a-z/1')
    for theletter in A2Z:
         addon.log('### GETTING TV METADATA FOR ALL ENTRIES ON: '+theletter)
         TVINDEX(iceurl + 'tv/a-z/' + theletter)
    
    #Ensure to reset addon fields to false so database is ready to deploy     
    mh.update_meta_installed(addon_id, movie_covers='false', tv_covers='false', tv_banners='false', movie_backdrops='false', tv_backdrops='false')


def CATEGORIES():  #  (homescreen of addon)

          #run startup stuff
          Startup_Routines()

          #get necessary paths
          homepage=handle_file('homepage','')
          tvshows=handle_file('tvshows','')
          movies=handle_file('movies','')
          music=handle_file('music','')
          standup=handle_file('standup','')
          other=handle_file('other','')
          search=handle_file('search','')

          #add directories

          addDir('Favourites', iceurl, 57, os.path.join(art_path, 'favourites.png'))
          addDir('Watch Queue', '', 'watch_queue', os.path.join(art_path,'favourites.png'))          
          addDir('TV Shows', iceurl+'tv/a-z/1',50,tvshows)
          addDir('Movies', iceurl+'movies/a-z/1',51,movies)
          addDir('Music', iceurl+'music/a-z/1',52,music)
          addDir('Stand Up Comedy', iceurl+'standup/a-z/1',53,standup)
          addDir('Other', iceurl+'other/a-z/1',54,other)
          # addDir('Recently Added Movies', iceurl+'index',60,os.path.join(art_path,'recently added.png'))
          # addDir('Latest Releases', iceurl+'index',61,os.path.join(art_path,'latest releases.png'))
          # addDir('Being Watched Now', iceurl+'index',62,os.path.join(art_path,'being watched now.png'))
          
          if str2bool(addon.get_setting('recent-watched')):
                addDir('Recently Watched', '', 'recent_watched', os.path.join(art_path,'being watched now.png'))
          
          addDir('Search',iceurl,55,search)
          VaddDir('URLResolver Settings', '', 'resolver_settings', '')
          VaddDir('Help', '', 'addon_help', '')
                    
          #Only show if prepare_zip = True - meaning you are creating a meta pack
          if prepare_zip:
              addDir('Create Meta Pack',iceurl,666,'')


def sort_list(list):

    #create new empty list
    stringList = []

    for item in list:
        stringList.append('|'.join(item[1:]))

    #sort list alphabetically and return it.
    tupleList = [(x.lower(), x) for x in stringList]

    articles = ("a","an","the")
    tupleList.sort(key=lambda s: tuple(word for word in s[1].split() if word.lower() not in articles))

    return [x[1] for x in tupleList]


def favRead(string):
     try:
          splitter=re.split('\|+', string)
          name=splitter[0]
          url=splitter[1]
          mode=int(splitter[2])
          try:
               imdb_id=str(splitter[3])
          except:
               imdb_id=''
     except:
          return None
     else:
          return name,url,mode,imdb_id


def FAVOURITES(url):
    #get necessary paths
    tvshows=handle_file('tvshows_fav','')
    movies=handle_file('movies_fav','')

    addDir('TV Shows',iceurl,570,tvshows)
    addDir('Movies',iceurl,571,movies)


def METAFIXER(url, videoType):
    #Icefilms urls passed to me will have their proper names and imdb numbers returned.
    source=GetURL(url)

    #get proper name from the page. (in case it is a weird name)
     
    if videoType==VideoType_Movies:
        #get imdb number.
        match=re.compile('<a class=iframe href=http://www.imdb.com/title/(.+?)/ ').findall(source)      

        #check if it is an episode. 
        epcheck=re.search('<a href=/tv/series/',source)

        #if it is, return the proper series name as opposed to the mirror page name.
        if epcheck is not None:
            tvget=re.compile('<a href=/tv/series/(.+?)>').findall(source)
            tvurl=iceurl+'tv/series/'+str(tvget[0])
            #load ep page and get name from that. sorry icefilms bandwidth!
            tvsource=GetURL(tvurl)
            name=re.compile('<h1>(.+?)<a class').findall(tvsource)

        #return mirror page name.
        if epcheck is None:
            name=re.compile('''<span style="font-size:large;color:white;">(.+?)</span>''').findall(source)
            
        name=CLEANUP(name[0])
        return name,match[0]

    elif videoType==VideoType_TV:
        #TV
        name=re.compile('<h1>(.+?)<a class').findall(source)
        match=re.compile('href="http://www.imdb.com/title/(.+?)/"').findall(source)
        name=CLEANUP(name[0])
        return name,match[0]


def ADD_TO_FAVOURITES(name, url, imdbnum, videoType):

    addon.log_debug('Adding to favourites: name: %s, imdbnum: %s, url: %s' % (name, imdbnum, url))

    try:
        if name and url:

            #fix name and imdb number for Episode List entries in Search.
            if imdbnum == 'nothing':
                metafix=METAFIXER(url, videoType)
                name=metafix[0]
                imdbnum=metafix[1]
             
            addon.log_debug('NAME: %s URL: %s IMDB NUMBER: %s' % (name,url,imdbnum))

            #Delete HD entry from filename. using name as filename makes favourites appear alphabetically.
            adjustedname=Clean_Windows_String(name).strip()

            new_url = parse_url(url)
            db_connection.save_favourite(videoType, name, new_url, imdbnum)
                   
            Notify('small','Icefilms Favourites', name + ' added to favourites','','6000')

            #Rescan Next Aired
            next_aired = str2bool(addon.get_setting('next-aired'))
            if next_aired:
                xbmc.executebuiltin("RunScript(%s, silent=true)" % os.path.join(icepath, 'resources/script.tv.show.next.aired/default.py'))
                
        else:
            raise Exception('Unable to add favourite due to blank name or url')

    except db_connection.db.IntegrityError, e:
        addon.log_error('Favourite already exists: %s' % name)
        Notify('small','Icefilms Favourites', '%s favourite already exists' % name,'','6000')
    except Exception, e:
        addon.log_error('Error adding favourite: %s' % e)
        Notify('small','Icefilms Favourites', 'Unable to add to favourites','','')        


def DELETE_FROM_FAVOURITES(url):
    addon.log_debug('Deleting from favourites: url: %s' % url)
    try:
        new_url = parse_url(url)
        db_connection.delete_favourite(new_url)
        xbmc.executebuiltin("XBMC.Container.Refresh")
    except Exception, e:
        addon.log_error('Error deleting favourite: %s' % e)
        Notify('small','Icefilms Favourites', 'Error while attempting to delete favourite','','')    
    

def CLEAR_FAVOURITES(url):
    dialog = xbmcgui.Dialog()
    ret = dialog.yesno('WARNING!', 'Delete all your favourites?','','','Cancel','Go Nuclear')
    if ret==True:
        db_connection.clear_favourites()
        xbmc.executebuiltin("XBMC.Container.Refresh")


def getFavourites(videoType):

    fav_list = db_connection.get_favourites(videoType)

    new_fav_list = sort_list(fav_list)
      
    if meta_setting=='true':    
        
        meta_installed = metaget.check_meta_installed(addon_id)
    else:
        meta_installed = False

    if videoType == VideoType_TV:
        mode = 12
    if videoType == VideoType_Season:
        mode = 13
    elif videoType == VideoType_Episode:
        mode = 14
    elif videoType == VideoType_Movies:
        mode = 100
         
    #for each string
    for fav_string in new_fav_list:
    
        fav = fav_string.split('|')
    
        new_url = iceurl + fav[1]
                  
        if meta_setting=='true' and meta_installed:
            #return the metadata dictionary
            if fav[2] is not None:
                                   
                #return the metadata dictionary
                meta=metaget.get_meta(videoType, fav[0], imdb_id=fav[2])
                
                if meta is None:
                    #add all the items without meta
                    addDir(fav[0], new_url, mode, '',delfromfav=True, totalItems=len(new_fav_list), favourite=True)
                else:
                    #add directories with meta
                    addDir(fav[0], new_url, mode, '', meta=meta, delfromfav=True, imdb=fav[2], totalItems=len(new_fav_list), meta_install=meta_installed, favourite=True)
            else:
                #add all the items without meta
                addDir(fav[0], new_url, mode, '', delfromfav=True, totalItems=len(new_fav_list), favourite=True)
        else:
            #add all the items without meta
            addDir(fav[0], new_url, mode, '', delfromfav=True, totalItems=len(new_fav_list), favourite=True)


    if videoType == VideoType_TV:
        setView('tvshows', 'tvshows-view')    
    elif videoType == VideoType_Movies:
        setView('movies', 'movies-view')


def check_episode(name):
    #Episode will have eg. 01x15 within the name, else we can assume it's a movie
    if re.search('([0-9]+x[0-9]+)', name):
        return True
    else:
        return False


def get_video_name(name):
    video = {}
    if check_episode(name):
        r = re.search('[0-9]+x[0-9]+ (.+?) [(]([0-9]{4})[)]', name)        
    else:
        r = re.search('(.+?) [(]([0-9]{4})[)]',name)
    if r:
        video['name'] = r.group(1)
        video['year'] = r.group(2)
    else:
        video['name'] = name
        video['year'] = ''
    return video
        

def check_video_meta(name):
    #Determine if it's a movie or tvshow by the title returned - tv show will contain eg. 01x15 to signal season/episode number
    episode = check_episode(name)
    if episode:
        episode_info = re.search('([0-9]+)x([0-9]+)', name)
        season = int(episode_info.group(1))
        episode = int(episode_info.group(2))
        
        #Grab episode title, check for regex on it both ways
        episode_title = re.search('(.+?) [0-9]+x[0-9]+', name)
        if not episode_title:
            episode_title = re.search('[0-9]+x[0-9]+ (.+)', name)

        episode_title = episode_title.group(1)
        tv_meta = metaget.get_meta('tvshow',episode_title)
        meta=metaget.get_episode_meta(episode_title, tv_meta['imdb_id'], season, episode)
    else:
        r=re.search('(.+?) [(]([0-9]{4})[)]',name)
        if r:
            name = r.group(1)
            year = r.group(2)
        else:
            year = ''
        meta = metaget.get_meta('movie',name, year=year)
    return meta


# Quick helper method to check and add listing tag folders - popularity, recently added etc.
def folder_tags(folder_text):
    hide_tags = str2bool(addon.get_setting('hide-tags'))
    if not hide_tags:
        VaddDir(folder_text, '', 0, '', False)
        

def RECENT(url):
        html = GetURL(url)

        #initialise meta class before loop
        if meta_setting=='true':
            meta_installed = metaget.check_meta_installed(addon_id)
        else:
            meta_installed = False
              
        recent_movies = re.search('<h2>Recently Added Movies</h2>(.+?)</div>', html, re.DOTALL)
        if recent_movies:
            
            text = re.compile("<span style='font-size:14px;'>(.+?)<li>").findall(recent_movies.group(1))
            
            #Add the first line
            folder_tags('[COLOR blue]' + text[0] + '[/COLOR]')
            
            mirlinks=re.compile('<a href=/(.+?)>(.+?)</a>[ ]*<(.+?)>').findall(recent_movies.group(1))
            for url,name,hd in mirlinks:
                url=iceurl+url
                name=CLEANUP(name)
                                   
                #Check if it's an HD source and add a tag to the name
                if re.search('color:red', hd):
                    new_name = name + ' [COLOR red]*HD*[/COLOR]'
                else:
                    new_name = name
                    
                if meta_installed and meta_setting=='true':
                    meta = check_video_meta(name)
                    addDir(new_name,url,100,'',meta=meta,disablefav=True, disablewatch=True, meta_install=meta_installed)
                else:
                    addDir(new_name,url,100,'',disablefav=True, disablewatch=True)
        setView('movies', 'movies-view')


def LATEST(url):
        link=GetURL(url)
        
        #initialise meta class before loop
        if meta_setting=='true':
            meta_installed = metaget.check_meta_installed(addon_id)
        else:
            meta_installed = False
                    
        homepage=re.compile('<h1>Recently Added</h1>(.+?)<h1>Statistics</h1>', re.DOTALL).findall(link)
        for scrape in homepage:
            scrape='<h1>Recently Added</h1>'+scrape+'<h1>Statistics</h1>'
            latrel=re.compile('<h1>Latest Releases</h1>(.+?)<h1>Being Watched Now</h1>', re.DOTALL).findall(scrape)
            for scraped in latrel:
                text = re.compile("<span style='font-size:14px;'>(.+?)<li>").findall(scraped)
                
                #Add the first line
                folder_tags('[COLOR blue]' + text[0] + '[/COLOR]')
                
                mirlinks=re.compile('<a href=/(.+?)>(.+?)</a>[ ]*<(.+?)>').findall(scraped)
                for url,name,hd in mirlinks:
                    url=iceurl+url
                    name=CLEANUP(name)

                    if check_episode(name):
                        mode = 14
                    else:
                        mode = 100
                    
                    #Check if it's an HD source and add a tag to the name
                    if re.search('color:red', hd):
                        new_name = name + ' [COLOR red]*HD*[/COLOR]'
                    else:
                        new_name = name
                        
                    if meta_installed and meta_setting=='true':
                        meta = check_video_meta(name)
                        addDir(new_name,url,mode,'',meta=meta,disablefav=True, disablewatch=True, meta_install=meta_installed)
                    else:
                        addDir(new_name,url,mode,'',disablefav=True, disablewatch=True)
        setView(None, 'default-view')


def WATCHINGNOW(url):
        link=GetURL(url)

        #initialise meta class before loop
        if meta_setting=='true':
            meta_installed = metaget.check_meta_installed(addon_id)
        else:
            meta_installed = False
                    
        homepage=re.compile('<h1>Recently Added</h1>(.+?)<h1>Statistics</h1>', re.DOTALL).findall(link)
        for scrape in homepage:
            scrapy='<h1>Recently Added</h1>'+scrape+'<h1>Statistics</h1>'
            watnow=re.compile('<h1>Being Watched Now</h1>(.+?)<h1>Statistics</h1>', re.DOTALL).findall(scrapy)
            for scraped in watnow:
                mirlinks=re.compile('href=/(.+?)>(.+?)</a>[ ]*<(.+?)>').findall(scraped)
                for url,name,hd in mirlinks:
                    url=iceurl+url
                    name=CLEANUP(name)

                    if check_episode(name):
                        mode = 14
                    else:
                        mode = 100

                    #Check if it's an HD source and add a tag to the name
                    if re.search('color:red', hd):
                        new_name = name + ' [COLOR red]*HD*[/COLOR]'
                    else:
                        new_name = name
                                                                                            
                    if meta_installed and meta_setting=='true':
                        meta = check_video_meta(name)
                        addDir(new_name,url,mode,'',meta=meta,disablefav=True, disablewatch=True, meta_install=meta_installed)
                    else:
                        addDir(new_name,url,mode,'',disablefav=True, disablewatch=True) 
        setView(None, 'default-view')


def recently_watched():
    addDir('Movies', '', '572', '', disablewatch=True) 
    addDir('TV Episodes', '', '573','', disablewatch=True)
    VaddDir('[COLOR red]** Clear All Lists[/COLOR]', '', 'clear_watched', '')

    
def get_recent_watched(videoType):

    if meta_setting=='true':    
        meta_installed = metaget.check_meta_installed(addon_id)
    else:
        meta_installed = False

    if videoType == VideoType_TV:
        mode = 12
    if videoType == VideoType_Season:
        mode = 13
    elif videoType == VideoType_Episode:
        mode = 14
    elif videoType == VideoType_Movies:
        mode = 100
        
    watch_list = db_connection.get_watched(videoType)

    #for each string
    for watch in watch_list:

        if watch[8] > 0:
            new_name = '[COLOR blue][' + format_time(watch[8]) + '][/COLOR] - ' + watch[2] + ' [' + watch[3] + ']'
        else:
            new_name = watch[2] + ' [' + watch[3] + ']'
    
        new_url = iceurl + watch[0]

        if meta_setting=='true' and meta_installed:
            #return the metadata dictionary
            if watch[4] is not None:

                #return the metadata dictionary
                if videoType == VideoType_Movies or videoType == VideoType_TV:
                    meta=metaget.get_meta(videoType, watch[2], imdb_id=watch[4])
                elif videoType == VideoType_Episode:
                    meta=metaget.get_episode_meta('', watch[6], watch[4], watch[5], episode_title=watch[2])

                if meta is None:
                    #add all the items without meta
                    addDir(new_name, new_url, mode, '', totalItems=len(watch_list), recentWatched=True)
                else:
                    #add directories with meta
                    addDir(new_name, new_url, mode, '', meta=meta, imdb=watch[4], totalItems=len(watch_list), meta_install=meta_installed, recentWatched=True)
            else:
                #add all the items without meta
                addDir(new_name, new_url, mode, '', totalItems=len(watch_list), recentWatched=True)
        else:
            #add all the items without meta
            addDir(new_name, new_url, mode, '', totalItems=len(watch_list), recentWatched=True)

    if len(watch_list) > 0:
        if videoType == VideoType_TV:
            VaddDir('[COLOR red]** Clear List[/COLOR]', '', 'clear_tv_watched', '')
        elif videoType == VideoType_Movies:
            VaddDir('[COLOR red]** Clear List[/COLOR]', '', 'clear_movie_watched', '')
        elif videoType == VideoType_Episode:
            VaddDir('[COLOR red]** Clear List[/COLOR]', '', 'clear_episode_watched', '')
               
    if videoType == VideoType_TV:
        setView('tvshows', 'tvshows-view')    
    elif videoType == VideoType_Movies:
        setView('movies', 'movies-view')
    elif videoType == VideoType_Episode:
        setView('episodes', 'episodes-view')
    

def clear_watched(videoType=None):

    dialog = xbmcgui.Dialog()
    if videoType:
        ret = dialog.yesno('Delete Watched List?', 'Do you wish to delete the current watched list?', '','This cannot be undone!')
    else:
        ret = dialog.yesno('Delete Watched Lists?', 'Do you wish to delete all of your watched lists?', '','This cannot be undone!')
        
    if ret == True:
        addon.log_debug('Clearing watched list for: %s' % videoType)
        db_connection.flush_watched(videoType)
        xbmc.executebuiltin("XBMC.Container.Refresh")


def remove_watched():
    addon.log_debug('Removing item from watched list: %s' % url)
    db_connection.clear_watched(parse_url(url))
    xbmc.executebuiltin("XBMC.Container.Refresh")


def watch_queue():
    addDir('Movies', '', '574', '', disablewatch=True) 
    addDir('TV Episodes', '', '575','', disablewatch=True)
    VaddDir('[COLOR red]** Clear All Lists[/COLOR]', '', 'clear_queue', '')


def clear_queue(videoType=None):

    dialog = xbmcgui.Dialog()
    if videoType:
        ret = dialog.yesno('Delete Queue List?', 'Do you wish to delete the current queue list?', '','This cannot be undone!')
    else:
        ret = dialog.yesno('Delete Queue Lists?', 'Do you wish to delete all of your queue lists?', '','This cannot be undone!')
        
    if ret == True:
        addon.log_debug('Clearing queue list for: %s' % videoType)
        db_connection.flush_queue(videoType)
        xbmc.executebuiltin("XBMC.Container.Refresh")


def get_queue_list(videoType):

    if meta_setting=='true':    
        meta_installed = metaget.check_meta_installed(addon_id)
    else:
        meta_installed = False

    if videoType == VideoType_TV:
        mode = 12
    if videoType == VideoType_Season:
        mode = 13
    elif videoType == VideoType_Episode:
        mode = 14
    elif videoType == VideoType_Movies:
        mode = 100
        
    queue_list = db_connection.get_queue(videoType)

    #for each string
    for queue in queue_list:
           
        if queue[8] > 0:
            new_name = '[COLOR blue][' + format_time(queue[8]) + '][/COLOR] - ' + queue[2] + ' [' + queue[3] + ']'
        else:
            new_name = queue[2] + ' [' + queue[3] + ']'
    
        new_url = iceurl + queue[0]
                         
        if meta_setting=='true' and meta_installed:
            #return the metadata dictionary
            if queue[4] is not None:
                                   
                #return the metadata dictionary
                if videoType == VideoType_Movies or videoType == VideoType_TV:
                    meta=metaget.get_meta(videoType, queue[2], imdb_id=queue[4])
                elif videoType == VideoType_Episode:
                    meta=metaget.get_episode_meta('', queue[6], queue[4], queue[5], episode_title=queue[2])
                
                if meta is None:
                    #add all the items without meta
                    addDir(new_name, new_url, mode, '', totalItems=len(queue_list), queueList=True)
                else:
                    #add directories with meta
                    addDir(new_name, new_url, mode, '', meta=meta, imdb=queue[4], totalItems=len(queue_list), meta_install=meta_installed, queueList=True)
            else:
                #add all the items without meta
                addDir(new_name, new_url, mode, '', totalItems=len(queue_list), queueList=True)
        else:
            #add all the items without meta
            addDir(new_name, new_url, mode, '', totalItems=len(queue_list), queueList=True)

    if len(queue_list) > 0:
        if videoType == VideoType_TV:
            VaddDir('[COLOR red]** Clear List[/COLOR]', '', 'clear_tv_queue', '')
        elif videoType == VideoType_Movies:
            VaddDir('[COLOR red]** Clear List[/COLOR]', '', 'clear_movie_queue', '')
        elif videoType == VideoType_Episode:
            VaddDir('[COLOR red]** Clear List[/COLOR]', '', 'clear_episode_queue', '')
               
    if videoType == VideoType_TV:
        setView('tvshows', 'tvshows-view')    
    elif videoType == VideoType_Movies:
        setView('movies', 'movies-view')
    elif videoType == VideoType_Episode:
        setView('episodes', 'episodes-view')


def remove_queue():
    addon.log_debug('Removing item from queue list: %s' % url)
    db_connection.clear_queue(parse_url(url))
    xbmc.executebuiltin("XBMC.Container.Refresh")


def add_queue():
    
    try:
        addon.log_debug('Adding item to queue list: %s' % url)
        video = get_video_name(name)
        db_connection.save_queue(parse_url(url), video_type, video['name'], video['year'], season_num, episode_num, imdbnum)    
        Notify('small','Icefilms Watch Queue', name + ' added to Queue list','','6000')
    except db_connection.db.IntegrityError, e:
        addon.log_error('Queue item already exists: %s' % name)
        Notify('small','Icefilms Watch Queue', '%s Queue item already exists' % name,'','6000')
    except Exception, e:
        addon.log_error('Error adding to Queue: %s' % e)
        Notify('small','Icefilms Watch Queue', 'Unable to add Queue item','','') 

    
def SEARCH(url):
    SEARCHBYPAGE(url, 0)


def SEARCHBYPAGE(url, page):
    kb = xbmc.Keyboard('', 'Search Icefilms.info', False)
    kb.doModal()
    if (kb.isConfirmed()):
        search = kb.getText()
        if search != '':
            DoEpListSearch(search)
            DoSearch(url, search, page)
            
    setView('movies', 'movies-view')


def KnownSearch(search, url):
    DoEpListSearch(search)
    DoSearch(url, search, 0)
    
def DoSearch(iurl, search, nextPage):        
        finished = False
        more     = False
        results  = None
        url      = 'site:' + iurl + 'ip '+search+''
        gs       = GoogleSearch(url)
        gs.results_per_page = 10

        while not finished:
            gs.page = nextPage             
            if (results == None):
                results = gs.get_results()
            else:
                finished = True
                local = gs.get_results()                
                for res in local:
                   if not FindSearchResult(res.title, results):
                       finished = False
                       results.append(res)   
                 
            nextPage = nextPage + 1

            results_per_page = int(addon.get_setting('search-results'))
            if len(results) >= results_per_page:
                more     = True
                finished = True

        find_meta_for_search_results(results, 100)

        if more:
            #leading space ensures the menu item always appears at end of list regardless of current sort order
            name = ' Get More...'
            sysname = urllib.quote_plus(name)
            sysurl = urllib.quote_plus(iurl)
            icon = handle_file('search','')

            liz = xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
            liz.setInfo(type="Video", infoLabels={"Title": name})

            u = sys.argv[0] + "?url=" + sysurl + "&mode=" + str(555) + "&name=" + sysname + "&search=" + search + "&nextPage=" + str(nextPage)
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)


def FindSearchResult(name, results):
        for res in results:
            if res.title == name:
                  return True            
        return False


def DoEpListSearch(search):
        tvurl = iceurl + 'tv/series'
        
        # use urllib.quote_plus() on search instead of re.sub ?
        searcher=urllib.quote_plus(search)
        #searcher=re.sub(' ','+',search)
        url='http://www.google.com/search?hl=en&q=site:'+tvurl+'+'+searcher+'&btnG=Search&aq=f&aqi=&aql=&oq='
        link=GetURL(url)
        
        match=re.compile('<h3 class="r"><a href="'+tvurl+'(.+?)"(.+?)">(.+?)</h3>').findall(link)
        match = sorted(match, key=lambda result: result[2])
        if len(match) == 0:
            link = link.replace('<b>', '').replace('</b>', '')
            match=re.compile('<h3 class="r"><a href="/url\?q='+tvurl+'(.+?)&amp;(.+?)">(.+?)</h3>').findall(link)         	
        find_meta_for_search_results(match, 12, search)


def TVCATEGORIES(url):
        caturl = iceurl+'tv/'        
        setmode = '11'
        addDir('A-Z Directories',caturl+'a-z/1',10,os.path.join(art_path,'az directories.png'))            
        ADDITIONALCATS(setmode,caturl)
        
        if str2bool(addon.get_setting('recent-watched')):
            addDir('Recently Watched', '', 'recent_watched_episode', os.path.join(art_path,'being watched now.png'))
        addDir('Watch Queue', '', 'watch_queue_episode', os.path.join(art_path,'favourites.png'))
        addDir('Favourites', iceurl, 570, os.path.join(art_path, 'favourites.png'))        
        setView(None, 'default-view')


def MOVIECATEGORIES(url):
        caturl = iceurl+'movies/'
        setmode = '2'
        addDir('A-Z Directories',caturl+'a-z/1',1,os.path.join(art_path,'az directories.png'))
        ADDITIONALCATS(setmode,caturl)
        
        if str2bool(addon.get_setting('recent-watched')):
            addDir('Recently Watched', '', 'recent_watched_movie', os.path.join(art_path,'being watched now.png'))
        addDir('Watch Queue', '', 'watch_queue_movie', os.path.join(art_path,'favourites.png'))          
        addDir('Favourites', iceurl, 571, os.path.join(art_path, 'favourites.png'))        
        setView(None, 'default-view')


def MUSICCATEGORIES(url):
        caturl = iceurl+'music/'        
        setmode = '2'
        addDir('A-Z List',caturl+'a-z/1',setmode,os.path.join(art_path,'az lists.png'))
        ADDITIONALCATS(setmode,caturl)
        setView(None, 'default-view')


def STANDUPCATEGORIES(url):
        caturl = iceurl+'standup/'        
        setmode = '2'
        addDir('A-Z List',caturl+'a-z/1',setmode,os.path.join(art_path,'az lists.png'))
        ADDITIONALCATS(setmode,caturl)
        setView(None, 'default-view')


def OTHERCATEGORIES(url):
        caturl = iceurl+'other/'        
        setmode = '2'
        addDir('A-Z List',caturl+'a-z/1',setmode,os.path.join(art_path,'az lists.png'))
        ADDITIONALCATS(setmode,caturl)
        setView(None, 'default-view')


def ADDITIONALCATS(setmode,caturl):
        if caturl == iceurl+'movies/':
             addDir('HD 720p',caturl,63,os.path.join(art_path,'HD 720p.png'))
        PopRatLat(setmode,caturl,'1')
        addDir('Genres',caturl,64,os.path.join(art_path,'genres.png'))

def PopRatLat(modeset,caturl,genre):
        if caturl == iceurl+'tv/':
             setmode = '11'
        else:
             setmode = '2'
        addDir('Popular',caturl+'popular/'+genre,setmode,os.path.join(art_path,'popular.png'))
        addDir('Highly Rated',caturl+'rating/'+genre,setmode,os.path.join(art_path,'highly rated.png'))
        addDir('Latest Releases',caturl+'release/'+genre,setmode,os.path.join(art_path,'latest releases.png'))
        addDir('Recently Added',caturl+'added/'+genre,setmode,os.path.join(art_path,'recently added.png'))
        setView(None, 'default-view')


def HD720pCat(url):
        PopRatLat('2',url,'hd')
        setView(None, 'default-view')


def Genres(url):
        addDir('Action',url,70,'')
        addDir('Animation',url,71,'')
        addDir('Comedy',url,72,'')
        addDir('Documentary',url,73,'')
        addDir('Drama',url,74,'')
        addDir('Family',url,75,'')
        addDir('Horror',url,76,'')
        addDir('Romance',url,77,'')
        addDir('Sci-Fi',url,78,'')
        addDir('Thriller',url,79,'')
        setView(None, 'default-view')


def Action(url):
     PopRatLat('2',url,'action')
     setView(None, 'default-view')

def Animation(url):
     PopRatLat('2',url,'animation')
     setView(None, 'default-view')

def Comedy(url):
     PopRatLat('2',url,'comedy')
     setView(None, 'default-view')

def Documentary(url):
     PopRatLat('2',url,'documentary')
     setView(None, 'default-view')

def Drama(url):
     PopRatLat('2',url,'drama')
     setView(None, 'default-view')

def Family(url):
     PopRatLat('2',url,'family')
     setView(None, 'default-view')

def Horror(url):
     PopRatLat('2',url,'horror')
     setView(None, 'default-view')

def Romance(url):
     PopRatLat('2',url,'romance')
     setView(None, 'default-view')

def SciFi(url):
     PopRatLat('2',url,'sci-fi')
     setView(None, 'default-view')

def Thriller(url):
     PopRatLat('2',url,'thriller')
     setView(None, 'default-view')

def MOVIEA2ZDirectories(url):
        setmode = '2'
        caturl = iceurl+'movies/a-z/'
        
        #Generate A-Z list and add directories for all letters.
        A2Z=[chr(i) for i in xrange(ord('A'), ord('Z')+1)]

        #Add number directory
        addDir ('#1234',caturl+'1',setmode,os.path.join(art_path,'letters','1.png'))
        for theletter in A2Z:
             addDir (theletter,caturl+theletter,setmode,os.path.join(art_path,'letters',theletter+'.png'))
        setView(None, 'default-view')


def TVA2ZDirectories(url):
        setmode = '11'
        caturl = iceurl+'tv/a-z/'

        #Generate A-Z list and add directories for all letters.
        A2Z=[chr(i) for i in xrange(ord('A'), ord('Z')+1)]

        #Add number directory
        addDir ('#1234',caturl+'1',setmode,os.path.join(art_path,'letters','1.png'))
        for theletter in A2Z:
            addDir (theletter,caturl+theletter,setmode,os.path.join(art_path,'letters',theletter+'.png'))
        setView(None, 'default-view')


def MOVIEINDEX(url):
    #Indexer for most things. (Movies,Music,Stand-up etc) 
    
    link=GetURL(url)
    
    # we do this to fix the problem when there is no imdb_id. 
    # I have found only one movie with this problem, but we must check this...
    link = re.sub('<a name=i id=>','<a name=i id=None>',link)

    #initialise meta class before loop    
    if meta_setting=='true':
        meta_installed = metaget.check_meta_installed(addon_id)
        
    temp = re.compile('(<h3>|<a class=imdb id=.+?></a><a class=tube></a><i class=star></i><a href=)(.+?)(<div|</h3>|>(.+?)<br>)').findall(link)
    for tag, link, longname, name in temp:

        if tag == '<h3>':
            folder_tags('[COLOR blue]' + link + '[/COLOR]')

        else:
            string = tag + link + longname + name
            scrape=re.compile('<a class=imdb id=(.+?)></a><a class=tube></a><i class=star></i><a href=/(.+?)>(.+?)<br>').findall(string)
            for imdb_id,url,name in scrape:
                if meta_setting=='true':
                    ADD_ITEM(meta_installed,imdb_id,url,name,100, totalitems=len(temp))
                else:
                    #add without metadata -- imdb is still passed for use with Add to Favourites
                    for imdb_id,url,name in scrape:
                        name=CLEANUP(name)
                        addDir(name,iceurl+url,100,'',imdb='tt'+str(imdb_id), totalItems=len(scrape))
 
    # Enable library mode & set the right view for the content
    setView('movies', 'movies-view')


def TVINDEX(url):
    #Indexer for TV Shows only.

    link=GetURL(url)

    #initialise meta class before loop    
    if meta_setting=='true':
        meta_installed = metaget.check_meta_installed(addon_id)
        
    #list scraper now tries to get number of episodes on icefilms for show. this only works in A-Z.
    #match=re.compile('<a name=i id=(.+?)></a><img class=star><a href=/(.+?)>(.+?)</a>').findall(link)
    firstText = re.compile('<h3>(.+?)</h3>').findall(link)
    if firstText:
        if firstText[0].startswith('Rated'):
            firstText[0] = string.split(firstText[0], '<')[0]
            regex = '<h3>(.+?)<div'
        else:
            regex = '<h3>(.+?)</h3>'
        folder_tags('[COLOR blue]' + firstText[0] + '[/COLOR]')
    else:
        regex = '<h3>(.+?)</h3>'
    scrape=re.search('<a class=imdb id=(.+?)></a><a class=tube></a><i class=star></i><a href=/(.+?)>(.+?)<br>', link)

    if meta_setting=='true':
        ADD_ITEM(meta_installed,scrape.group(1),scrape.group(2),scrape.group(3),12, totalitems=1)
    else:
        addDir(scrape.group(3),iceurl + scrape.group(2),12,'',imdb='tt'+str(scrape.group(1)), totalItems=1)

    #Break the remaining source into seperate lines and check if it contains a text entry
    temp = re.compile('r>(.+?)<b').findall(link)
    for entry in temp:
        text = re.compile(regex).findall(entry)
        if text:
            folder_tags('[COLOR blue]' + text[0] + '[/COLOR]')
        scrape=re.compile('<a class=imdb id=(.+?)></a><a class=tube></a><i class=star></i><a href=/(.+?)>(.+?)</a>').findall(entry)
        if scrape:
            for imdb_id,url,name in scrape:
                if meta_setting=='true':
                    ADD_ITEM(meta_installed,imdb_id,url,name,12, totalitems=len(temp))
                else:
                    #add without metadata -- imdb is still passed for use with Add to Favourites
                    for imdb_id,url,name in scrape:
                        name=CLEANUP(name)
                        addDir(name,iceurl+url,12,'',imdb='tt'+str(imdb_id), totalItems=len(scrape))
    
    # Enable library mode & set the right view for the content
    setView('tvshows', 'tvshows-view')


def TVSEASONS(url, imdb_id):
    # displays by seasons. pays attention to settings.

    FlattenSingleSeasons = addon.get_setting('flatten-single-season')
    source=GetURL(url)

    #Save the tv show name for use in special download directories.
    match=re.compile('<h1>.([^<].+?)', re.S).findall(source)
    cache.set('tvshowname',match[0])
    r=re.search('(.+?) [(][0-9]{1,4}[)]',match[0])
    if r:
        showname = r.group(1)
    else:
        showname = match[0]

    # get and save the TV Show poster link
    try:
      imgcheck1 = re.search('<a class=img target=_blank href=', link)
      imgcheck2 = re.search('<iframe src=http://referer.us/f/\?url=', link)
      if imgcheck1 is not None:
           match4=re.compile('<a class=img target=_blank href=(.+?)>').findall(link)
           cache.set('poster',match4[0])
      if imgcheck2 is not None:
           match5=re.compile('<iframe src=http://referer.us/f/\?url=(.+?) width=').findall(link)
           cache.set('poster',match5[0])
    except:
      pass
    
    ep_list = str(BeautifulSoup(source).find("span", { "class" : "list" } ))

    showname = CLEANUP_FOR_META(showname)
    season_list=re.compile('<h3><a name.+?></a>(.+?)<a.+?</a></h3>').findall(ep_list)
    listlength=len(season_list)
    if listlength > 0:
        seasons = str(season_list)
        season_nums = re.compile('Season ([0-9]{1,2}) ').findall(seasons)                        
        
        if meta_setting=='true':
            meta_installed = metaget.check_meta_installed(addon_id)
            if meta_installed:
                season_meta = metaget.get_seasons(showname, imdb_id, season_nums)
        else:
            meta_installed = False
    num = 0
    for seasons in season_list:
        if FlattenSingleSeasons==True and listlength <= 1:             
        
            #proceed straight to adding episodes.
            TVEPISODES(seasons.strip(),source=ep_list,imdb_id=''+str(imdb_id))
        else:
            #save episode page source code
            cache.set('episodesrc',repr(ep_list))
            #add season directories
            if meta_installed and meta_setting=='true' and season_meta:
                temp = season_meta[num]
                addDir(seasons.strip(),'',13,temp['cover_url'],imdb=''+str(imdb_id), meta=season_meta[num], totalItems=len(season_list), meta_install=meta_installed) 
                num = num + 1                     
            else:
                addDir(seasons.strip(),'',13,'', imdb=''+str(imdb_id), totalItems=len(season_list))
            setView('seasons', 'seasons-view')


def TVEPISODES(name,url=None,source=None,imdb_id=None):
    #Save the season name for use in the special download directories.
    cache.set('mediatvseasonname',name)

    #If source wasn't passed to function, open the file it should be saved to.
    if source is None:
        source = eval(cache.get('episodesrc'))
        
    #special hack to deal with annoying re problems when recieving brackets ( )
    if re.search('\(',name) is not None:
        name = str((re.split('\(+', name))[0])
        #name=str(name[0])
    
    #quick hack of source code to simplfy scraping.
    source=re.sub('</span>','<h3>',source)
    
    #get all the source under season heading.
    #Use .+?/h4> not .+?</h4> for The Daily Show et al to work.
    match=re.compile('<h3><a name="[0-9]+?"></a>'+name+'.+?/h3>(.+?)<h3>').findall(source)
    for seasonSRC in match:
        addon.log_debug('Season Source is: %s' % name)
        TVEPLINKS(seasonSRC, name, imdb_id)
    setView('episodes', 'episodes-view')


def TVEPLINKS(source, season, imdb_id):
    
    # displays all episodes in the source it is passed.
    match = re.compile('<i class="star"></i><a href="/(.+?)&amp;">(.+?)</a>([<b>HD</b>]*)<br />').findall(source)
        
    if meta_setting=='true':
        #initialise meta class before loop
        meta_installed = metaget.check_meta_installed(addon_id)
    else:
        meta_installed=False
    for url, name, hd in match:
            name = name + ' ' + hd
            addon.log_debug("TVepLinks name: %s " % name)
            get_episode(season, name, imdb_id, url, meta_installed, totalitems=len(match)) 
    
    # Enable library mode & set the right view for the content
    setView('episodes', 'episodes-view')


def LOADMIRRORS(url):
    # This proceeds from the file page to the separate frame where the mirrors can be found,
    # then executes code to scrape the mirrors
    html=GetURL(url)
    
    video_url = parse_url(url)
      
    #---------------Begin phantom metadata getting--------

    #Save metadata on page to files, for use when playing.
    # Also used for creating the download directory structures.

    ice_meta = {}
    
    #Grab video name
    namematch = re.search('''<span style="font-size:150%;font-weight:bold;color:white;">(.+?)</span>''', html, re.S)
    if not namematch:
        Notify('big','Error Loading Sources','An error occured loading sources.\nCheck your connection and/or the Icefilms site.','')
        callEndOfDirectory = False
        return
    else:
        ice_meta['title'] = namematch.group(1)
        year = re.search('\(([0-9]+)\)', namematch.group(1))
        if year:
            ice_meta['year'] = year.group(1)
        try:
            cache.set('videoname', namematch.group(1))
        except:
            addon.log_error("Failed to save video name")
            pass

    #If meta is enabled, we should have all needed info from previous screen so grab from list item that was clicked
    if meta_setting=='true':
        ice_meta['poster'] = xbmc.getInfoImage('ListItem.Thumb')
        ice_meta['year'] = xbmc.getInfoLabel('ListItem.Year')
        ice_meta['plot'] = xbmc.getInfoLabel('ListItem.Plot')
        ice_meta['plot_outline'] = xbmc.getInfoLabel('ListItem.PlotOutline')
        ice_meta['mpaa'] = xbmc.getInfoLabel('ListItem.Mpaa')

    #Else we just use what we can grab from Icefilms site 'phantom' meta data
    else:
        #Set Plot
        plot = re.search('<th>Description:</th><td>(.+?)<', html)
        if plot:
            ice_meta['plot'] = plot.group(1)
            ice_meta['plot_outline'] = plot.group(1)
        else:
            ice_meta['plot'] = ''
            ice_meta['plot_outline'] = ''
            
        #Set Poster
        imgcheck1 = re.search('<img width=250 src=(.+?) style', html)
        if imgcheck1:
            ice_meta['poster'] = imgcheck1.group(1)
        imgcheck2 = re.search('<iframe src=/noref.php\?url=(.+?) width=', html)
        if imgcheck2:
            ice_meta['poster'] = imgcheck2.group(1)

        #Set MPAA rating
        mpaacheck=re.search('<th>MPAA Rating:</th><td>(.+?)</td>', html)
        if mpaacheck:
            mpaa=re.sub('Rated ','', mpaacheck)
            ice_meta['mpaa'] = mpaa
        else:
            ice_meta['mpaa'] = ''

    ########### get and save potential file path. This is for use in download function later on.
    epcheck1 = re.search('Episodes</a>', html)
    epcheck2 = re.search('Episode</a>', html)
    if epcheck1 or epcheck2:
        if cache.get('mediatvshowname'):
            #open media file if it exists, as that has show name with date.
            showname=cache.get('mediatvshowname')
        else:
            #fall back to scraping show name without date from the page.
            addon.log_debug('USING FALLBACK SHOW NAME')
            fallbackshowname=re.compile("alt\='Show series\: (.+?)'").findall(html)
            showname=fallbackshowname[0]
        try:
            #if season name file exists
            if cache.get('mediatvshowname'):
                seasonname=cache.get('mediatvshowname')
                cache.set('mediapath','TV Shows/'+ Clean_Windows_String(showname) + '/' + Clean_Windows_String(seasonname))
            else:
                cache.set('mediapath','TV Shows/' + Clean_Windows_String(showname))
        except:
            addon.log_error("FAILED TO SAVE TV SHOW FILE PATH!")
    else:
          
        try:
            cache.set('mediapath','Movies/' + Clean_Windows_String(namematch.group(1)))
        except Exception, e:
            addon.log_error('Failed to set cache value: %s' % e)
            pass

    #---------------End phantom metadata getting stuff --------------

    match=re.compile('/membersonly/components/com_iceplayer/(.+?img=).*?" width=').findall(html)
    match[0]=re.sub('%29',')',match[0])
    match[0]=re.sub('%28','(',match[0])
    for link in match:
        mirrorpageurl = iceurl+'membersonly/components/com_iceplayer/' + link
      
    html = GetURL(mirrorpageurl, save_cookie = True, use_cache=False)
             
    #string for all text under hd720p border
    defcat = re.compile('<div class=ripdiv><b>(.+?)</b>(.+?)</div>').findall(html)
    for media_type, scrape in defcat:
        if media_type == 'HD 720p+':
            tag = ' | [COLOR red]HD[/COLOR]'
        elif media_type == 'SD / DVD 480p':
            tag = ' | [COLOR blue]DVD[/COLOR]'
        elif media_type == 'DVD Screener':
            tag = ' | [COLOR yellow]DVDSCR[/COLOR]'
        elif media_type == 'R5/R6 DVDRip':
            tag = ' | [COLOR green]R5/R6[/COLOR]'
        elif media_type == 'Fast Stream / Low Quality':
            tag = ' | [COLOR yellow]Low Quality[/COLOR]'
        else:
            tag = ' | [COLOR white]Other[/COLOR]'
            
        SOURCE(html, scrape, tag, ice_meta, video_url)

    setView(None, 'default-view')


def PART(scrap, sourcenumber, host, args, source_tag, ice_meta=None, video_url=None):
     #check if source exists
     sourcestring='Source #'+sourcenumber
     checkforsource = re.search(sourcestring, scrap)
             
     #if source exists proceed.
     if checkforsource:
          
          hoster = urlresolver.HostedMediaFile(host=host, media_id='dummy')
          
          debrid_tag = ''
#          if hoster:
#			  if debrid_hosts:
#				  if hoster[0] in debrid_hosts:
#					  debrid_tag = ' [COLOR yellow]*RD[/COLOR] '
          
          # find corresponding '<a rel=?' entry and add as a one-link source
          source5=re.compile('<a\s+rel='+sourcenumber+'.+?onclick=\'go\((\d+)\)\'>Source\s+#'+sourcenumber+':').findall(scrap)

          for id in source5:
                
               if hoster:
                   fullname=sourcestring + ' | ' + host + debrid_tag + source_tag + ' | Full '
                   addExecute(fullname, args, get_default_action(), ice_meta, video_url=video_url)


def SOURCE(page, sources, source_tag, ice_meta=None, video_url=None):
    # get settings
    # extract the ingredients used to generate the XHR request
    #
    # set here:
    #
    #     sec: secret identifier: hardwired in the JS
    #     t:   token: hardwired in the JS
    #     id:  source ID in the link's onclick attribute (extracted in PART)    
    #
    # set in GetSource:
    #
    #     iqs: not used?
    #     url: not used?
    #     cap: form field for recaptcha? - always set to empty in the JS    
    #     m:   starts at 0, decremented each time a mousemove event is fired e.g. -123
    #     s:   seconds since page loaded (> 5, < 250)

    args = {}

    match = re.search('lastChild\.value="([^"]+)"(?:\s*\+\s*"([^"]+))?', page)
    args['sec'] = ''.join(match.groups(''))
    args['t'] = re.search('"&t=([^"]+)",', page).group(1)
    args['s'] = re.search('(?:\s+|,)s\s*=(\d+)', page).group(1)
    args['m'] = re.search('(?:\s+|,)m\s*=(\d+)', page).group(1)
    
    #add cached source
    vidname=cache.get('videoname')
    dlDir = Get_Path("noext", "", "")

    listitem=Item_Meta(vidname)

    try:
        fdirs, fnames = xbmcvfs.listdir(dlDir)
        for fname in fnames:
            match = re.match(re.escape(vidname)+' *(.*)\.avi$', fname)
            if match is not None:
                if xbmcvfs.exists(os.path.join(dlDir,fname)+'.dling'):
                    listitem.setLabel("Play Downloading "+match.group(0))
                    addDownloadControls(match.group(0),os.path.join(dlDir,fname), listitem)
                else:
                    listitem.setLabel("Play Local File" + match.group(0))
                    addLocal("Play Local File " + match.group(0), os.path.join(dlDir,fname), listitem)
    except:
        pass
     
    hosts = re.findall('<a\s+rel=[0-9]+.+?onclick=\'go\((\d+)\)\'>Source\s+#([0-9]+): (<span .+?</span>)</a>', sources)
    for id, number, hoster in hosts:
        host = re.sub('</span>', '', re.sub('<span .+?>', '', hoster)).lower()
        args['id'] = id
        PART(sources, number, host, args, source_tag, ice_meta, video_url)
    setView(None, 'default-view')


def GetURL(url, params = None, referrer = ICEFILMS_REFERRER, use_cookie = False, save_cookie = False, use_cache=True):
    addon.log_debug('GetUrl: ' + url)
    addon.log_debug('params: ' + repr(params))
    addon.log_debug('referrer: ' + repr(referrer))
    addon.log_debug('cookie: ' + repr(use_cookie))
    addon.log_debug('save_cookie: ' + repr(save_cookie))

    if addon.get_setting('proxy_enable') == 'true':
        proxy = 'http://' + addon.get_setting('proxy') + ':' + addon.get_setting('proxy_port')
        proxy_handler = urllib2.ProxyHandler({'http': proxy})
        username = addon.get_setting('proxy_user')
        password = addon.get_setting('proxy_pass')
        if username <> '' and password <> '':
            print 'Using authenticated proxy: %s' % proxy
            password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
            password_mgr.add_password(None, proxy, username, password)
            proxy_auth_handler = urllib2.ProxyBasicAuthHandler(password_mgr)
            opener = urllib2.build_opener(proxy_handler, proxy_auth_handler)
        else:
            print 'Using proxy: %s' % proxy
            opener = urllib2.build_opener(proxy_handler)
        
        urllib2.install_opener(opener)
        
    headers = {
        'Referer': referrer,
        'Accept': ACCEPT,
        'User-Agent': USER_AGENT
    }

    page_cache = str2bool(addon.get_setting('use_page_cache'))
    
    try:

        if page_cache and use_cache:
            html = db_connection.get_cached_url(url, 10)
            if html:
                addon.log_debug("Cached URL found for: %s" % url)
                return html
            else:
                addon.log_debug("No cache found for: %s" % url)
        
        
        if use_cookie:
            net.set_cookies(ice_cookie)
            addon.log_debug("Cookie set")

        if params:
            html = net.http_POST(url, params, headers=headers).content
        else:
            html = net.http_GET(url, headers=headers).content

        if  page_cache and use_cache:
            db_connection.cache_url(url, html)
        
        if save_cookie:
            net.save_cookies(ice_cookie)          
            addon.log_debug("Cookie saved")

    except Exception, e:
        addon.log_error('****** ERROR: %s' % e)
        Notify('big','Error Requesting Site','An error has occured communicating with Icefilms', '', '', 'Check your internet connection and the Icefilms site.' )
        html = ''
        pass

    return html


############################################
## Helper Functions
############################################

#Quick helper function used to strip characters that are invalid for Windows filenames/folders
def Clean_Windows_String(string):
     return re.sub('[^\w\-_\. ]', '',  string)


#Helper function to convert strings to boolean values
def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

#Int parse  
def intTryParse(value):
    try:
        return int(value)
    except ValueError:
        return 0


def Get_Path(srcname, vidname, link):
     ##Gets the path the file will be downloaded to, and if necessary makes the folders##
         
     #clean video name of unwanted characters
     vidname = Clean_Windows_String(vidname)
     
     #Get file extension from url
     if link:
        download_url = re.search('(^https?://[^|]*)', link).group(1)
     else:
        download_url = ''
        
     import urlparse
     path = urlparse.urlparse(download_url).path
     ext = os.path.splitext(path)[1]
    
     if xbmcvfs.exists(downloadPath):

          #if source is split into parts, attach part number to the videoname.
          if re.search('Part',srcname) is not None:
               srcname=(re.split('\|+', srcname))[-1]
               vidname=vidname + ' part' + ((re.split('\ +', srcname))[-1])
               #add file extension
               vidname = vidname + ext
          elif srcname is not "noext":
               #add file extension
               vidname = vidname + ext

          #is use special directory structure set to true?
          SpecialDirs=addon.get_setting('use-special-structure')

          if SpecialDirs == 'true':
               mediapath=os.path.normpath(cache.get('mediapath'))
               mediapath=os.path.join(downloadPath, mediapath)              
               
               if not xbmcvfs.exists(mediapath):
                    try:
                        xbmcvfs.mkdir(mediapath)
                    except Exception, e:
                        addon.log_error('Failed to create media path: %s' % mediapath)
                        addon.log_error('With error: %s' % e)
                        pass
               finalpath=os.path.join(mediapath,vidname)
               return finalpath
     
          elif SpecialDirs == 'false':
               mypath=os.path.join(downloadPath,vidname)
               return mypath
     else:
          return 'path not set'


def Item_Meta(name, resume_point=0):
    #Set metadata for playing video - allows trakt and scrobbling
    #Also shows metadata when hitting Info button while playing

    thumb_img = xbmc.getInfoImage('ListItem.Thumb')
    vid_year = xbmc.getInfoLabel('ListItem.Year')
    vid_plot = xbmc.getInfoLabel('ListItem.Plot')
    plot_outline = xbmc.getInfoLabel('ListItem.PlotOutline')
    mpaa = xbmc.getInfoLabel('ListItem.Mpaa')

    #set name and description, unicode cleaned.
    try: open_vidname=cache.get('videoname')
    except:
        vidname = ''
        addon.log_error('OPENING VIDNAME FAILED!')
    else:
        try: get_vidname = htmlcleaner.clean(open_vidname)
        except:
            addon.log_error('CLEANING VIDNAME FAILED! :',open_vidname)
            vidname = open_vidname
        else: vidname = get_vidname

    listitem = xbmcgui.ListItem(name)

    video = get_video_name(vidname)
              
    if video_type == 'movie':
        listitem.setInfo(type="Video", infoLabels={'title': video['name'], 'year': vid_year, 'type': 'movie', 'plotoutline': plot_outline, 'plot': vid_plot, 'mpaa': mpaa})

    if video_type == 'episode':               
        show = cache.get('tvshowname')
        show = get_video_name(show)
        ep_num = intTryParse(episode_num)
        episode_season = intTryParse(season_num)
           
        listitem.setInfo('video', {'title': video['name'], 'tvshowtitle': show['name'], 'year': vid_year, 'episode': episode_num, 'season': episode_season, 'type': 'episode', 'plotoutline': plot_outline, 'plot': vid_plot, 'mpaa': mpaa})

    listitem.setProperty('StartOffset', str(resume_point))
    listitem.setThumbnailImage(thumb_img)
       
    return listitem


def handle_wait(time_to_wait,title,text):

    addon.log_debug('Waiting '+str(time_to_wait)+' secs')

    pDialog = xbmcgui.DialogProgress()
    ret = pDialog.create(' '+title)

    secs=0
    percent=0
    increment = float(100) / time_to_wait
    increment = int(round(increment))

    cancelled = False
    while secs < time_to_wait:
        secs = secs + 1
        percent = increment*secs
        secs_left = str((time_to_wait - secs))
        remaining_display = ' Wait '+secs_left+' seconds for the video stream to activate...'
        pDialog.update(percent,' '+ text, remaining_display)
        xbmc.sleep(1000)
        if (pDialog.iscanceled()):
             cancelled = True
             break
    if cancelled == True:     
         addon.log_debug('Wait Cancelled')
         return False
    else:
         addon.log_debug('Done Waiting')
         return True

   
def Handle_Vidlink(url): 
        hmf = urlresolver.HostedMediaFile(url=url)
        return hmf.resolve()


def PlayFile(name,url):
    
    listitem=Item_Meta(name)
    addon.log_debug('Attempting to play local file')
    try:
        #directly call xbmc player (provides more options)
        play_with_watched(url, listitem, '')
        
        #xbmc.Player( xbmc.PLAYER_CORE_DVDPLAYER ).play( url, listitem )
    except:
        addon.log_error('local file playing failed')


def GetSource():

    t = addon.queries.get('t', '')
    id = addon.queries.get('id', '')
    
    params = {
        'iqs': '',
        'url': '',
        'cap': ' ',
        'sec': addon.queries.get('sec', ''),
        't': t,
        'id': id,
        'm' : int(addon.queries.get('m', '')) + random.randrange(20, 500),
        's' : int(addon.queries.get('s', '')) + random.randrange(2, 500)
    } 
    
    body = GetURL(ICEFILMS_AJAX % (id, t), params = params, referrer = ICEFILMS_AJAX_REFER % t, use_cookie=True, use_cache=False)
    addon.log_debug('GetSource Response: %s' % body)
    source = re.search('url=(http[^&]+)', body)
    
    if source:
        url = urllib.unquote(source.group(1))
    else:
        addon.log_debug('GetSource - URL String not found')
        url = ''
    addon.log_debug('GetSource URL: %s' % url)
    return url


def get_resume_choice(video_id):
    question = 'Resume from %s' % (format_time(db_connection.get_bookmark(video_id)))
    return xbmcgui.Dialog().yesno('Resume?', question, '', '', 'Start from beginning', 'Resume') == 1


def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    if minutes > 60:
        hours, minutes = divmod(minutes, 60)
        return "%02d:%02d:%02d" % (hours, minutes, seconds)
    else:
        return "00:%02d:%02d" % (minutes, seconds)


def Stream_Source(name, download_play=False, download=False, download_jdownloader=False, stacked=False):

    #Grab actual source url
    url = GetSource()
       
    addon.log_debug('Entering Stream Source with options - Name: %s Url: %s DownloadPlay: %s Download: %s Stacked: %s' % (name, url, download_play, download, stacked))
  
    callEndOfDirectory = False
    
    resume = False
    use_resume = str2bool(addon.get_setting('resume-support'))
    if use_resume:
        if db_connection.bookmark_exists(video_url):
            resume = get_resume_choice(video_url)  
                
    resume_point = 0
    if resume:
        resume_point = db_connection.get_bookmark(video_url)    
        addon.log_debug('Resuming video at: %s' % resume_point)    
        
    vidname=cache.get('videoname')
    mypath = Get_Path(name, vidname, url)
    listitem = Item_Meta(name, resume_point)

    video_seeking = str2bool(addon.get_setting('video-seeking'))

    last_part = False
    current_part = 1
    
    resume_threshhold = int(addon.get_setting('resume-threshhold'))
        
    while not last_part:
        
        #If it's a stacked source, grab url one by one
        if stacked == True:
            addon.log_debug('I AM STACKED')
            url = get_stacked_part(name, str(current_part))
            if url:
                current_part += 1
                
                #Check to see if it is the last part by attempting to grab the next
                next_url = get_stacked_part(name, str(current_part))
                if not next_url:
                    last_part = True
            else:
                last_part = True
                break
        else:
            last_part = True
            
        #Grab the final playable link
        try:
            link = Handle_Vidlink(url)
            
            if link == None:
               callEndOfDirectory = False
               break
        except Exception, e:
            addon.log_error('**** Stream error: %s' % e)
            Notify('big','Invalid Source','Unable to play selected source. \n Please try another.','', line3=str(e))
            break


        #Download & Watch
        if download_play:
            addon.log_debug('Starting Download & Play')
            completed = Download_And_Play(name, link, video_seek=False)
            addon.log_debug('Download & Play streaming completed: %s' % completed)
        
        #Download option
        elif download:
            addon.log_debug('Starting Download')
            completed = Download_Source(name, link, url)
            addon.log_debug('Downloading completed: %s' % completed)

        elif download_jdownloader:
            addon.log_debug('Sent %s to JDownloader' % link)
            xbmc.executebuiltin('XBMC.RunPlugin("plugin://plugin.program.jdownloader/?action=addlink&url=%s")' % (link))
            Notify('Download Alert','Sent '+vidname+' to JDownloader','','')
            completed = True


        #Download & Watch - but delete file when done, simulates streaming and allows video seeking
        #elif video_seeking:
        #    addon.log_debug('Starting Video Seeking')
        #    completed = Download_And_Play(name,link, video_seek=video_seeking)
        #    addon.log_debug('Video Seeking streaming completed: %s' % completed)
        #    CancelDownload(name, video_seek=video_seeking)
        
        #Else play the file as normal stream
        else:               
            addon.log_debug('Starting Normal Streaming')
                                  
            completed = play_with_watched(link, listitem, mypath, last_part, resume_point, resume_threshhold)
            addon.log_debug('Normal streaming completed: %s' % completed)

        #Check if video was played until end - else assume user stopped watching video so break from loop
        if not completed:
            break                


def play_with_watched(url, listitem, mypath, last_part=False, resume_point=0, resume_threshhold=1):
    global currentTime
    global totalTime
    global watched_percent
    global finalPart
    
    finalPart = last_part
    watched_percent = get_watched_percent()    

    useAxel = addon.get_setting('axel-proxy')
    
    axelhelper = None
    download_id = None
    if useAxel == 'true':
        import axelproxy as proxy
        axelhelper =  proxy.ProxyHelper()
        url, download_id = axelhelper.create_proxy_url(url)

    enable_recent = str2bool(addon.get_setting('recent-watched'))
        
    mplayer = MyPlayer(axelhelper=axelhelper, download_id=download_id, ice_url=video_url, imdbid = imdbnum, season = season_num, episode=episode_num, resume_point=resume_point, resume_threshhold=resume_threshhold, enableRecent=enable_recent)
    mplayer.play(url, listitem)

    try:
        video_time = mplayer.getTotalTime()
    except Exception:
        xbmc.sleep(20000) #wait 20 seconds until the video is playing before getting totalTime
        try:
            video_time = mplayer.getTotalTime()
        except Exception, e:
            addon.log_error('Error grabbing video time: %s' % e)
            return False

    #For stacked parts totalTime will need to be added up
    temp_total = totalTime
    totalTime = totalTime + video_time
    addon.log_debug('******** VIDEO TIME: %s' % video_time)
    addon.log_debug('******** TOTAL TIME: %s' % totalTime)

    while(1):
        try:
            temp_current_time = mplayer.getTime()
            currentTime= int(temp_current_time + temp_total)
        except Exception:
            addon.log_error('Kodi is not currently playing a media file')
            break
        xbmc.sleep(1000)
    
    addon.log_debug('******** CURRENT TIME: %s' % currentTime)

    #Check if video was played until the end (-1 second)
    if temp_current_time < (video_time - 1):
        return False
    else:
        return True


def get_watched_percent():
     watched_values = [.7, .8, .9]
     return watched_values[int(addon.get_setting('watched-percent'))]


def get_stacked_part(name, part):
    sourcenumber = name[8:9]
    source = eval(cache.get("source"+str(sourcenumber)+"parts"))
    addon.log_debug('**** Stacked parts: %s' % source)
    
    try:
        url=source[part]
        addon.log_debug('**** Stacked Part returning part #%s: %s' % (part, url))
        return url
    except:
        addon.log_error('No more parts found')
        return None


class MyPlayer (xbmc.Player):
    def __init__ (self, axelhelper=None, download_id=None, ice_url=None, imdbid=None, season=None, episode=None, resume_point=0, resume_threshhold=1, enableRecent=False):
        self.dialog = None
        self.axelhelper = axelhelper
        self.download_id = download_id
        self.ice_url = ice_url
        self.imdbid = imdbid
        self.season = season
        self.episode = episode
        self.seek_time = resume_point
        self.resume_threshhold = resume_threshhold
        self.enableRecent = enableRecent
        xbmc.Player.__init__(self)
        
        addon.log_debug('Initializing myPlayer...')
        
    def play(self, url, listitem):
        addon.log_debug('Now im playing... %s' % url)

        xbmc.Player().play(url, listitem)
        
    def isplaying(self):
        xbmc.Player.isPlaying(self)
          
    def onPlayBackEnded(self):
        global currentTime
        global totalTime
        global finalPart

        #Stop Axel Downloader from running
        if self.download_id:
            self.axelhelper.stop_download(self.download_id)        
        
        if finalPart:
            try: percentWatched = currentTime / totalTime
            except: percentWatched = 0
            addon.log_debug('current time: ' + str(currentTime) + ' total time: ' + str(totalTime) + ' percent watched: ' + str(percentWatched))
            vidname=cache.get('videoname')
            video = get_video_name(vidname)

            if percentWatched >= watched_percent:

                #set watched
                addon.log_debug('Auto-Watch - Setting %s to watched' % video)
                ChangeWatched(imdbnum, video_type, video['name'], season_num, episode_num, video['year'], watched=7)

                #Clear bookmark
                db_connection.clear_bookmark(self.ice_url)
                
                #remove from Queue list
                self.removeQueue(video)

            # Set recently watched
            self.setRecentWatched(video)

            
    def onPlayBackStopped(self):
        global currentTime
        global totalTime
        global finalPart
        
        #Stop Axel Downloader from running
        if self.download_id:
            self.axelhelper.stop_download(self.download_id)
        
        if finalPart:
            try: percentWatched = currentTime / totalTime
            except: percentWatched = 0
            addon.log_debug('Playback stopped - current time: ' + str(currentTime) + ' total time: ' + str(totalTime) + ' percent watched: ' + str(percentWatched))
            vidname=cache.get('videoname')
            video = get_video_name(vidname)           
            if percentWatched >= watched_percent and totalTime > 1:
                #set watched
                addon.log_debug('Auto-Watch - Setting %s to watched' % video            )
                ChangeWatched(imdbnum, video_type, video['name'], season_num, episode_num, video['year'], watched=7)

                #Clear bookmark
                db_connection.clear_bookmark(self.ice_url)

                #remove from Queue list
                self.removeQueue(video)
                
            elif currentTime >= (self.resume_threshhold * 60):
                addon.log_debug('Setting resume bookmark: %s' % currentTime)
                db_connection.set_bookmark(self.ice_url, currentTime)
                
            # Set recently watched
            self.setRecentWatched(video)
                

    def setRecentWatched(self, video):
        if self.enableRecent:
            addon.log_debug('Setting recently watched: %s' % video['name'])                    
            db_connection.set_watched(self.ice_url, video_type, video['name'], video['year'], self.season, self.episode, self.imdbid)


    def removeQueue(self, video):
        addon.log_debug('Removing watched Queue item: %s' % video['name'])                    
        db_connection.clear_queue(self.ice_url)
        
    
############## End MyPlayer Class ################


class DownloadThread (threading.Thread):
    def __init__(self, url, dest, vidname=False, video_seek=False):
        self.url = url
        self.dest = dest
        self.vidname = vidname
        self.video_seek = video_seek
        self.dialog = None
        
        threading.Thread.__init__(self)
        
    def run(self):
        #save the thread id to a .tid file. This file can then be read if the user navigates away from the 
        #download info page to get the thread ID again and generate the download info links
        #the tid file will also denote a download in progress
        #Note: if xbmc is killed during a download, the tid file will remain, therefore:
        #TODO: add remove incomplete download link
        
        save(self.dest + '.dling', 'dling')

        #get settings
        save(os.path.join(downloadPath,'Downloading'),self.dest+'\n'+self.vidname)
          
        delete_incomplete = addon.get_setting('delete-incomplete-downloads')
        
        start_time = time.time() 
        try: 
            urllib.urlretrieve(self.url, self.dest, lambda nb, bs, fs: _dlhook(nb, bs, fs, self, start_time))
            if os.path.getsize(self.dest) < 10000:
                addon.log_debug('Got a very small file')
                raise SmallFile('Small File')
            if self.dialog <> None:
                self.dialog.close()
                self.dialog = None
                addon.log_debug('Download finished successfully')
            try:
              xbmcvfs.delete(self.dest + '.dling')
            except:
              pass
            xbmcvfs.delete(os.path.join(downloadPath,'Downloading'))
        
        except:
            if self.dialog <> None:
                self.dialog.close()
                self.dialog = None
                
            addon.log_debug('Download interrupted')
            xbmcvfs.delete(os.path.join(downloadPath,'Downloading'))
            
            #download is killed so remove .dling file
            try:
                xbmcvfs.delete(self.dest + '.dling')
            except:
                pass
            
            if delete_incomplete == 'true':
                #delete partially downloaded file if setting says to.
                while xbmcvfs.exists(self.dest):
                    try:
                        xbmcvfs.delete(self.dest)
                        break
                    except:
                        pass
            
            if sys.exc_info()[0] in (StopDownloading,) and not self.video_seek:
                Notify('big','Download Canceled','Download has been canceled','')
            else:
                raise 


    def show_dialog(self):
        self.dialog = xbmcgui.DialogProgress()
        self.dialog.create('Downloading', '', self.vidname)
    
    def hide_dialog(self):
        self.dialog.close() 
        self.dialog = None

############## End DownloadThread Class ################

class StopDownloading(Exception): 
        def __init__(self, value): 
            self.value = value 
        def __str__(self): 
            return repr(self.value)

class SmallFile(Exception): 
        def __init__(self, value): 
            self.value = value 
        def __str__(self): 
            return repr(self.value)

def Download_And_Play(name,url, video_seek=False):

    #get proper name of vid                                                                                                           
    vidname=cache.get('videoname')

    mypath=Get_Path(name, vidname, url)
     
    addon.log_debug('MYPATH: %s' % mypath)
    if mypath == 'path not set':
        Notify('Download Alert','You have not set the download folder.\n Please access the addon settings and set it.','','')
        return False

    if xbmcvfs.exists(os.path.join(downloadPath, 'Ping')):
        xbmcvfs.rmdir(os.path.join(downloadPath, 'Ping'))
    if xbmcvfs.exists(os.path.join(downloadPath, 'Alive')):
        xbmcvfs.rmdir(os.path.join(downloadPath, 'Alive'))

    if xbmcvfs.exists(os.path.join(downloadPath, 'Downloading')):
      fhPing = open(os.path.join(downloadPath, 'Ping'), 'w')
      fhPing.close()
      xbmc.sleep(1000)
      
      if xbmcvfs.exists(os.path.join(downloadPath, 'Alive')):
          fh = open(os.path.join(downloadPath, 'Alive'))          
          filePathAlive = fh.readline().strip('\n')
          fileNameAlive = fh.readline().strip('\n')
          fh.close()
          
          try:
              xbmcvfs.rmdir(os.path.join(downloadPath, 'Alive'))
          except:
              pass
          
          Notify('Download Alert','Currently downloading '+fileNameAlive,'','')
          addDownloadControls(fileNameAlive, filePathAlive)
          return False

      else:
          xbmcvfs.rmdir(os.path.join(downloadPath, 'Ping'))
          delete_incomplete = addon.get_setting('delete-incomplete-downloads')
          
          if delete_incomplete == 'true':
              if xbmcvfs.exists(os.path.join(downloadPath, 'Downloading')):
                  fh = open(os.path.join(downloadPath, 'Downloading'))          
                  filePathDownloading = fh.readline().strip('\n')
                  fh.close()
                  
                  try:
                      xbmcvfs.rmdir(filePathDownloading)
                  except:
                      pass
                  try:
                      xbmcvfs.rmdir(filePathDownloading + '.dling')
                  except:
                      pass

          if xbmcvfs.exists(os.path.join(downloadPath, 'Downloading')):
              xbmcvfs.rmdir(os.path.join(downloadPath, 'Downloading'))


    if os.path.isfile(mypath) is True:
        if os.path.isfile(mypath + '.dling'):
            try:
                xbmcvfs.delete(mypath)
                xbmcvfs.delete(mypath + '.dling')
            except:
                addon.log_error('download failed: existing incomplete files cannot be removed')
                return False
        else:
            Notify('Download Alert','The video you are trying to download already exists!','','')

    addon.log_debug('Attempting to download and play file')

    try:
        addon.log_debug("Starting Download Thread")
        dlThread = DownloadThread(url, mypath, vidname, video_seek)
        dlThread.start()
        buffer_delay = int(addon.get_setting('buffer-delay'))
        handle_wait(buffer_delay, "Buffering", "Waiting a bit before playing...")
        if not handle_wait:
            return False
        if xbmcvfs.exists(mypath):
            if dlThread.isAlive():
                listitem=Item_Meta(name)
                
                #Play file              
                completed = play_with_watched(mypath, listitem, '')
               
                if video_seek:
                    if xbmcvfs.exists(mypath):
                        try:
                            xbmcvfs.delete(mypath)
                        except:
                            addon.log_error('Failed to delete file after video seeking')
                else:
                    addDownloadControls(name,mypath, listitem)

                #Return if video was played until the end
                if not completed:
                    return False
                else:
                    return True

            else:
                raise
        else:
            raise
    except Exception, e:
        addon.log_error('EXCEPTION %s' % e)
        if sys.exc_info()[0] in (urllib.ContentTooShortError,): 
            Notify('big','Download and Play failed!','Error: Content Too Short','')
        if sys.exc_info()[0] in (OSError,): 
            Notify('big','Download and Play failed!','Error: Cannot write file to disk','')
        if sys.exc_info()[0] in (SmallFile,): 
            Notify('big','Download and Play failed!','Error: Got a file smaller than 10KB','')
        
        callEndOfDirectory = False


def _dlhook(numblocks, blocksize, filesize, dt, start_time):

    if dt.dialog != None:
        
        try: 
            percent = min(numblocks * blocksize * 100 / filesize, 100)
            currently_downloaded = float(numblocks) * blocksize / (1024 * 1024)
            kbps_speed = numblocks * blocksize / (time.time() - start_time)
            
            if kbps_speed > 0: 
                eta = (filesize - numblocks * blocksize) / kbps_speed 
            else: 
                eta = 0 
            
            kbps_speed = kbps_speed / 1024 
            total = float(filesize) / (1024 * 1024) 
            mbs = '%.02f MB of %.02f MB' % (currently_downloaded, total) 
            e = 'Speed: %.02f Kb/s ' % kbps_speed 
            e += 'ETA: %02d:%02d' % divmod(eta, 60)
            dt.dialog.update(percent, mbs, e)
        
        except: 
            percent = 100 
            dt.dialog.update(percent) 
        
        if dt.dialog.iscanceled():
            dt.hide_dialog()
            
    elif xbmcvfs.exists(os.path.join(downloadPath, 'ShowDLInfo')):
        while xbmcvfs.exists(os.path.join(downloadPath, 'ShowDLInfo')):
            
            try:
                xbmcvfs.rmdir(os.path.join(downloadPath, 'ShowDLInfo'))
            except:
                continue
            break
        
        dt.show_dialog()
        
    elif xbmcvfs.exists(os.path.join(downloadPath, 'Cancel')):
        while xbmcvfs.exists(os.path.join(downloadPath, 'Cancel')):
            
            try:
                xbmcvfs.rmdir(os.path.join(downloadPath, 'Cancel'))
            except:
                continue
            break
        
        addon.log_debug("Stopping download")
        raise StopDownloading('Stopped Downloading')
        
    elif xbmcvfs.exists(os.path.join(downloadPath, 'Ping')):
        while xbmcvfs.exists(os.path.join(downloadPath, 'Ping')):
            
            try:
                xbmcvfs.rmdir(os.path.join(downloadPath, 'Ping'))
            except:
                continue
            break
        
        save(os.path.join(downloadPath,'Alive'),dt.dest+'\n'+dt.vidname)


def Download_Source(name, url, referer, stacked=False):
    #get proper name of vid
    vidname=cache.get('videoname')
    
    mypath=Get_Path(name, vidname, url)
           
    if mypath == 'path not set':
        Notify('Download Alert','You have not set the download folder.\n Please access the addon settings and set it.','','')
        return False
    else:
        if os.path.isfile(mypath) is True:
            Notify('Download Alert','The video you are trying to download already exists!','','')
            return False
        else:              
            import commondownloader
            download_url = re.search('(^https?://[^|]*)', url).group(1)
            commondownloader.download(download_url, mypath, 'Icefilms', referer=referer, agent=USER_AGENT)
            #commondownloader.download(url, mypath, 'Icefilms', referer=referer, agent=USER_AGENT)
            
            # DownloadInBack=addon.get_setting('download-in-background')
            # addon.log_debug('attempting to download file, silent = '+ DownloadInBack)
            # try:
                # if DownloadInBack == 'true':
                    # completed = QuietDownload(url, mypath, vidname)
                    # return completed
                # else:
                    # completed = Download(url, mypath, vidname)
                    # return completed
            # except:
                # addon.log_error('download failed')
                # return False


def Kill_Streaming(name,url):
     xbmc.Player().stop()     

class StopDownloading(Exception): 
        def __init__(self, value): 
            self.value = value 
        def __str__(self): 
            return repr(self.value)
          
def Download(url, dest, displayname=False):
         
        if displayname == False:
            displayname=url
        dp = xbmcgui.DialogProgress()
        dp.create('Downloading', '', displayname)
        start_time = time.time() 
        try: 
            urllib.urlretrieve(url, dest, lambda nb, bs, fs: _pbhook(nb, bs, fs, dp, start_time)) 
        except:
            delete_incomplete = addon.get_setting('delete-incomplete-downloads')
            if delete_incomplete == 'true':
                #delete partially downloaded file if setting says to.
                while xbmcvfs.exists(dest): 
                    try: 
                        xbmcvfs.delete(dest) 
                        break 
                    except: 
                        pass 
            #only handle StopDownloading (from cancel), ContentTooShort (from urlretrieve), and OS (from the race condition); let other exceptions bubble 
            if sys.exc_info()[0] in (urllib.ContentTooShortError, StopDownloading, OSError): 
                return False 
            else: 
                raise 
            return False
        return True


def QuietDownload(url, dest, videoname):
    #quote parameters passed to download script     
    q_url = urllib.quote_plus(url)
    q_dest = urllib.quote_plus(dest)
    q_vidname = urllib.quote_plus(videoname)
    
    #Create possible values for notification
    notifyValues = [2, 5, 10, 20, 25, 50, 100]

    # get notify value from settings
    NotifyPercent=int(addon.get_setting('notify-percent'))
    
    try:
        script = os.path.join( icepath, 'resources', 'lib', "DownloadInBackground.py" )
        xbmc.executebuiltin( "RunScript(%s, %s, %s, %s, %s)" % ( script, q_url, q_dest, q_vidname, str(notifyValues[NotifyPercent]) ) )
        return True
    except Exception, e:
        addon.log_error('*** Error in Quiet Download: %s' % e)
        return False
             

def _pbhook(numblocks, blocksize, filesize, dp, start_time):
        try: 
            percent = min(numblocks * blocksize * 100 / filesize, 100) 
            currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
            kbps_speed = numblocks * blocksize / (time.time() - start_time) 
            if kbps_speed > 0: 
                eta = (filesize - numblocks * blocksize) / kbps_speed 
            else: 
                eta = 0 
            kbps_speed = kbps_speed / 1024 
            total = float(filesize) / (1024 * 1024) 
            mbs = '%.02f MB of %.02f MB' % (currently_downloaded, total) 
            e = 'Speed: %.02f Kb/s ' % kbps_speed 
            e += 'ETA: %02d:%02d' % divmod(eta, 60) 
            dp.update(percent, mbs, e)
        except: 
            percent = 100 
            dp.update(percent) 
        if dp.iscanceled(): 
            dp.close() 
            raise StopDownloading('Stopped Downloading')


def addExecute(name, args, mode, ice_meta, stacked=False, video_url=None):

    # A list item that executes the next mode, but doesn't clear the screen of current list items.
    
    #encode url and name, so they can pass through the sys.argv[0] related strings
    sysname = urllib.quote_plus(name)
    sysurl = urllib.quote_plus(ICEFILMS_AJAX)
    argsenc = urllib.urlencode(args)
        
    u = sys.argv[0] + "?url=" + sysurl + "&mode=" + str(mode) + "&name=" + sysname + "&imdbnum=" + urllib.quote_plus(str(imdbnum))  + "&videoType=" + str(video_type) + "&season=" + str(season_num) + "&episode=" + str(episode_num) + "&stackedParts=" + str(stacked) + "&" + str(argsenc) + '&videoUrl=' +  urllib.quote_plus(video_url)
    ok=True

    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=ice_meta['poster'])
    liz.setInfo( type="Video", infoLabels={ "Title": name, 'year': ice_meta['year'], 'type': 'movie', 'plotoutline': ice_meta['plot_outline'], 'plot': ice_meta['plot'], 'mpaa': ice_meta['mpaa']})
    liz.setProperty('totalTime', '1' )
    liz.setProperty('resumeTime', '0')

    #handle adding context menus
    contextMenuItems = []

    contextMenuItems.append(('Play Stream', 'XBMC.RunPlugin(%s?mode=200&name=%s&url=%s&stackedParts=%s&%s)' % (sys.argv[0], sysname, sysurl, stacked, argsenc)))
    contextMenuItems.append(('Download', 'XBMC.RunPlugin(%s?mode=201&name=%s&url=%s&stackedParts=%s&%s)' % (sys.argv[0], sysname, sysurl, stacked, argsenc)))
    contextMenuItems.append(('Download And Watch', 'XBMC.RunPlugin(%s?mode=206&name=%s&url=%s&stackedParts=%s&%s)' % (sys.argv[0], sysname, sysurl, stacked, argsenc)))
    contextMenuItems.append(('Download with jDownloader', 'XBMC.RunPlugin(%s?mode=202&name=%s&url=%s&stackedParts=%s&%s)' % (sys.argv[0], sysname, sysurl, stacked, argsenc)))

    liz.addContextMenuItems(contextMenuItems, replaceItems=True)

    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    return ok


def addDir(name, url, mode, iconimage, meta=False, imdb=False, delfromfav=False, disablefav=False, searchMode=False, totalItems=0, disablewatch=False, meta_install=False, favourite=False, recentWatched=False, queueList=False):
     ###  addDir with context menus and meta support  ###

     #encode url and name, so they can pass through the sys.argv[0] related strings
     sysname = urllib.quote_plus(name.encode('utf8'))
     sysurl = urllib.quote_plus(url.encode('utf8'))
     dirmode=mode

     #get nice unicode name text.
     #name has to pass through lots of weird operations earlier in the script,
     #so it should only be unicodified just before it is displayed.
     name = htmlcleaner.clean(name)
                 
     #handle adding context menus
     contextMenuItems = []
     
     if mode == 12: # TV series
         videoType = 'tvshow'
     elif mode == 13: # TV Season
         videoType = 'season'
     elif mode == 14: # TV Episode
         videoType = 'episode'
     elif mode == 100: # movies
         videoType = 'movie'
     else:
         videoType = video_type
     
     season = ''
     episode = ''
                 
     if season_num:
         season = season_num
     if episode_num:
         episode = episode_num

     #handle adding meta
     if meta == False:
         liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
         liz.setInfo(type="Video", infoLabels={"Title": name})

     else:
                 
         #check covers installed
         covers_url = ''
         if mode == 12:

             #check tv posters vs banners setting 
             tv_posters = addon.get_setting('tv-posters')
             if tv_posters == 'true':
                 #if meta_install['tv_covers'] == 'true':
                 covers_url = meta['cover_url']
             else:
                 #if meta_install['tv_banners'] == 'true':
                 covers_url = meta['banner_url']
         else:
             #if meta_install['movie_covers'] == 'true':
             covers_url = meta['cover_url']

         #Set XBMC list item
         liz = xbmcgui.ListItem(name, iconImage=covers_url, thumbnailImage=covers_url)
         liz.setInfo(type="Video", infoLabels=meta)

         #Set fanart/backdrop setting variables
         movie_fanart = addon.get_setting('movie-fanart')
         tv_fanart = addon.get_setting('tv-fanart')

         # mark as watched or unwatched 
         addWatched = False
         if mode == 12: # TV series
             if int(meta['episode']) > 0:
                 episodes_unwatched = str(int(meta['episode']) - meta['playcount'])
                 liz.setProperty('UnWatchedEpisodes', episodes_unwatched)
                 liz.setProperty('WatchedEpisodes', str(meta['playcount']))
             addWatched = True
             #if tv_fanart == 'true' and tv_fanart_installed == 'true':
             if tv_fanart == 'true':
                 liz.setProperty('fanart_image', meta['backdrop_url'])
             contextMenuItems.append(('Show Information', 'XBMC.Action(Info)'))
             if favourite:
                 next_aired = str2bool(addon.get_setting('next-aired'))
                 if next_aired:
                     contextMenuItems.append(('Show Next Aired', 'RunScript(%s)' % os.path.join(icepath, 'resources/script.tv.show.next.aired/default.py')))
         elif mode == 13: # TV Season
             addWatched = True
             #if tv_fanart == 'true' and tv_fanart_installed == 'true':
             if tv_fanart == 'true':
                 liz.setProperty('fanart_image', meta['backdrop_url'])                
             season = meta['season']
             contextMenuItems.append(('Refresh Info', 'XBMC.RunPlugin(%s?mode=998&name=%s&url=%s&imdbnum=%s&dirmode=%s&videoType=%s&season=%s)' % (sys.argv[0], sysname, sysurl, urllib.quote_plus(str(imdb)), dirmode, videoType, season)))             
         elif mode == 14: # TV Episode
             addWatched = True
             if tv_fanart == 'true':
                 liz.setProperty('fanart_image', meta['backdrop_url'])
             season = meta['season']
             episode = meta['episode']
             
             if not queueList and not recentWatched:
                contextMenuItems.append(('Add to Queue List', 'XBMC.RunPlugin(%s?mode=add_queue&name=%s&url=%s&imdbnum=%s&dirmode=%s&videoType=%s&season=%s&episode=%s)' % (sys.argv[0], sysname, sysurl, urllib.quote_plus(str(imdb)), dirmode, videoType, season, episode)))
                
             contextMenuItems.append(('Episode Information', 'XBMC.Action(Info)'))
             contextMenuItems.append(('Refresh Info', 'XBMC.RunPlugin(%s?mode=997&name=%s&url=%s&imdbnum=%s&dirmode=%s&videoType=%s&season=%s&episode=%s)' % (sys.argv[0], sysname, sysurl, urllib.quote_plus(str(imdb)), dirmode, videoType, season, episode)))
         elif mode == 100: # movies
             addWatched = True
             if movie_fanart == 'true':
                 liz.setProperty('fanart_image', meta['backdrop_url'])

             if not queueList and not recentWatched:
                contextMenuItems.append(('Add to Queue List', 'XBMC.RunPlugin(%s?mode=add_queue&name=%s&url=%s&imdbnum=%s&dirmode=%s&videoType=%s)' % (sys.argv[0], sysname, sysurl, urllib.quote_plus(str(imdb)), dirmode, videoType)))

             contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
             contextMenuItems.append(('Search for Similar', 'XBMC.RunPlugin(%s?mode=991&name=%s&url=%s&tmdbnum=%s&dirmode=%s&videoType=%s)' % (sys.argv[0], sysname, sysurl, urllib.quote_plus(str(meta['tmdb_id'])), dirmode, videoType)))
         #Add Refresh & Trailer Search context menu
         if searchMode==False:
             if mode in (12, 100):
                 contextMenuItems.append(('Refresh Info', 'XBMC.RunPlugin(%s?mode=999&name=%s&url=%s&imdbnum=%s&dirmode=%s&videoType=%s)' % (sys.argv[0], sysname, sysurl, urllib.quote_plus(str(imdb)), dirmode, videoType)))
                 contextMenuItems.append(('Search for trailer', 
                                          'XBMC.RunPlugin(%s?mode=996&name=%s&url=%s&dirmode=%s&imdbnum=%s)' 
                                          % (sys.argv[0], sysname, sysurl, dirmode, urllib.quote_plus(str(imdb))) ))                        
                     
         #Add Watch/Unwatch context menu             
         if addWatched and not disablewatch:
             if meta['overlay'] == 6:
                 watchedMenu='Mark as Watched'
             else:
                 watchedMenu='Mark as Unwatched'
             if searchMode==False:
                 contextMenuItems.append((watchedMenu, 'XBMC.RunPlugin(%s?mode=990&name=%s&url=%s&imdbnum=%s&videoType=%s&season=%s&episode=%s)' 
                     % (sys.argv[0], sysname, sysurl, urllib.quote_plus(str(imdb)), videoType, season, episode)))
    
     # add/delete favourite
     if disablefav is False: # disable fav is necessary for the scrapes in the homepage category.
         if delfromfav is True:
             #settings for when in the Favourites folder
             contextMenuItems.append(('Delete from Ice Favourites', 'XBMC.RunPlugin(%s?mode=111&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
         else:
             #if directory is an tv show or movie NOT and episode
             if mode == 100 or mode == 12:
                 if imdb is not False:
                     sysimdb = urllib.quote_plus(str(imdb))
                 else:
                     #if no imdb number, it will have no metadata in Favourites
                     sysimdb = urllib.quote_plus('nothing')
                 #if searchMode==False:
                 contextMenuItems.append(('Add to Ice Favourites', 'XBMC.RunPlugin(%s?mode=110&name=%s&url=%s&imdbnum=%s&videoType=%s)' % (sys.argv[0], sysname, sysurl, sysimdb, videoType)))

     if recentWatched:
        contextMenuItems.append(('Delete from Watched List', 'XBMC.RunPlugin(%s?mode=remove_watched&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
     
     if queueList:
        contextMenuItems.append(('Delete from Queue List', 'XBMC.RunPlugin(%s?mode=remove_queue&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
     
     if contextMenuItems:
         liz.addContextMenuItems(contextMenuItems, replaceItems=True)

     if mode == 14:
         if check_episode(name):
             episode_info = re.search('([0-9]+)x([0-9]+)', name)
             season = int(episode_info.group(1))
             episode = int(episode_info.group(2))
             mode = 100

     if mode in (12, 13, 100, 101):
         u = sys.argv[0] + "?url=" + sysurl + "&mode=" + str(mode) + "&name=" + sysname + "&imdbnum=" + urllib.quote_plus(str(imdb)) + "&videoType=" + videoType + "&season=" + str(season) + "&episode=" + str(episode)
     else:
         u = sys.argv[0] + "?url=" + sysurl + "&mode=" + str(mode) + "&name=" + sysname
     ok = True

     ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True, totalItems=totalItems)
     return ok


#VANILLA ADDDIR (kept for reference)
def VaddDir(name, url, mode, iconimage, is_folder=False):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=is_folder)
        return ok


def setView(content, viewType):
    
    # set content type so library shows more views and info
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if addon.get_setting('auto-view') == 'true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % addon.get_setting(viewType) )
    
    # set sort methods - probably we don't need all of them
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_PROGRAM_COUNT )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RUNTIME )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_GENRE )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_MPAA_RATING )
    

def cleanUnicode(string):
    try:
        string = string.replace("'","").replace(unicode(u'\u201c'), '"').replace(unicode(u'\u201d'), '"').replace(unicode(u'\u2019'),'').replace(unicode(u'\u2026'),'...').replace(unicode(u'\u2018'),'').replace(unicode(u'\u2013'),'-')
        return string
    except:
        return string


def ADD_ITEM(meta_installed, imdb_id,url,name,mode,num_of_eps=False, totalitems=0):
            #clean name of unwanted stuff
            name=CLEANUP(name)
            if url.startswith('http://www.icefilms.info') == False:
                url=iceurl+url

            #append number of episodes to the display name, AFTER THE NAME HAS BEEN USED FOR META LOOKUP
            if num_of_eps is not False:
                name = name + ' ' + str(num_of_eps)

            if meta_installed and meta_setting=='true':
                #return the metadata dictionary
                #we want a clean name with the year separated for proper meta search and storing
                meta_name = CLEANUP_FOR_META(name)           
                r=re.search('(.+?) [(]([0-9]{4})[)]',meta_name)
                if r:
                    meta_name = r.group(1)
                    year = r.group(2)
                else:
                    year = ''
                if mode==100:
                    #return the metadata dictionary
                    meta=metaget.get_meta('movie', meta_name, imdb_id=imdb_id, year=year)
                elif mode==12:
                    #return the metadata dictionary
                    meta=metaget.get_meta('tvshow', meta_name, imdb_id=imdb_id)
                
                addDir(name,url,mode,'',meta=meta,imdb='tt'+str(imdb_id),totalItems=totalitems, meta_install=meta_installed)  
           
            else:
                #add directories without meta
                if imdb_id == None:
                    imdb_id == ''
                else:
                    imdb_id = 'tt'+str(imdb_id)
                addDir(name,url,mode,'',imdb=imdb_id,totalItems=totalitems)


def REFRESH(videoType, url,imdb_id,name,dirmode):
        #refresh info for a Tvshow or movie
               
        addon.log_debug('In Refresh ' + str(sys.argv[1]))
        imdb_id = imdb_id.replace('tttt','')

        if meta_setting=='true':
            meta_installed = metaget.check_meta_installed(addon_id)          
            
            if meta_installed:
                name=CLEANUP(name)
                r=re.search('(.+?) [(]([0-9]{4})[)]',name)
                if r:
                    name = r.group(1)
                    year = r.group(2)
                else:
                    year = ''
                metaget.update_meta(videoType, name, imdb_id, year=year)
                xbmc.executebuiltin("XBMC.Container.Refresh")           


def episode_refresh(url, imdb_id, name, dirmode, season, episode):
        #refresh info for an episode
               
        addon.log_debug('In Episode Refresh ' + str(sys.argv[1]))
        imdb_id = imdb_id.replace('tttt','')

        if meta_setting=='true':
            meta_installed = metaget.check_meta_installed(addon_id)          
            
            if meta_installed:
                name=CLEANUP(name)
                metaget.update_episode_meta(name, imdb_id, season, episode)
                xbmc.executebuiltin("XBMC.Container.Refresh")


def season_refresh(url, imdb_id, name, dirmode, season):
        #refresh info for an episode
               
        addon.log_debug('In Season Refresh ' + str(sys.argv[1]))
        imdb_id = imdb_id.replace('tttt','')

        if meta_setting=='true':
            meta_installed = metaget.check_meta_installed(addon_id)          
            
            if meta_installed:
                name=CLEANUP(name)            	
                metaget.update_season(name, imdb_id, season)
                xbmc.executebuiltin("XBMC.Container.Refresh")


def get_episode(season, episode, imdb_id, url, meta_installed, tmp_season_num=-1, tmp_episode_num=-1, totalitems=0):
        # displays all episodes in the source it is passed.
        imdb_id = imdb_id.replace('t','')
   
        #add with metadata
        if metaget:
            
            #clean name of unwanted stuff
            episode=CLEANUP(episode)
             
            #Get tvshow name - don't want the year portion
            showname=cache.get('tvshowname')
            r=re.search('(.+?) [(][0-9]{4}[)]',showname)
            if r:
                showname = r.group(1)
                           
            #return the metadata dictionary
            ep = re.search('[0-9]+x([0-9]+)', episode)
            if ep: 
                tmp_episode_num = int(ep.group(1))
            se = re.search('Season ([0-9]{1,2})', season)
            if se:
                tmp_season_num = int(se.group(1))

            meta = {}
            
            if meta_installed and tmp_episode_num >= 0:
                showname = CLEANUP_FOR_META(showname)
                meta=metaget.get_episode_meta(showname, imdb_id, tmp_season_num, tmp_episode_num)
                      
            if meta and meta_installed:
                #add directories with meta
                addDir(episode,iceurl+url,14,'',meta=meta,imdb='tt'+str(imdb_id),totalItems=totalitems, meta_install=meta_installed)
            else:
                #add directories without meta
                addDir(episode,iceurl+url,14,'',imdb='tt'+str(imdb_id),totalItems=totalitems)

        
        #add without metadata -- imdb is still passed for use with Add to Favourites
        else:
            episode=CLEANUP(episode)
            addDir(episode,iceurl+url,14,'',imdb='tt'+str(imdb_id),totalItems=totalitems)                

              
def find_meta_for_search_results(results, mode, search=''):
    
    #initialise meta class before loop
    meta_installed = metaget.check_meta_installed(addon_id)
    
    if mode == 100:        
        for res in results:
            name=res.title.encode('utf8')
            name=CLEANSEARCH(name)
                
            url=res.url.encode('utf8')
            url=re.sub('&amp;','&',url)

            if check_episode(name):
                mode = 14
            else:
                mode = 100
                                                                       
            if meta_installed and meta_setting=='true':
                meta = check_video_meta(name)
                addDir(name,url,mode,'',meta=meta,imdb=meta['imdb_id'],searchMode=True, meta_install=meta_installed)
            else:
                addDir(name,url,mode,'',searchMode=True)

            
    elif mode == 12:
        for myurl,interim,name in results:
            if len(interim) < 180:
                name=CLEANSEARCH(name)                              
                hasnameintitle=re.search(search,name,re.IGNORECASE)
                if hasnameintitle:
                    myurl='http://www.icefilms.info/tv/series'+myurl
                    myurl=re.sub('&amp;','',myurl)
                    if myurl.startswith('http://www.icefilms.info/tv/series'):
                        if meta_installed==True and meta_setting=='true':
                            meta = metaget.get_meta('tvshow',name)
                            addDir(name,myurl,12,'',meta=meta,imdb=meta['imdb_id'],searchMode=True)                           
                        else:
                            addDir(name,myurl,12,'',searchMode=True)
                    else:
                        addDir(name,myurl,12,'',searchMode=True)
 
         
def SearchGoogle(search):
    gs = GoogleSearch(''+search+' site:http://www.youtube.com ')
    gs.results_per_page = 25
    gs.page = 0
    try:
        results = gs.get_results()
    except Exception, e:
        addon.log_error('***** Error: %s' % e)
        Notify('big','Google Search','Error encountered searching.','')
        return None
    return results


def SearchForTrailer(search, imdb_id, type, manual=False):
    search = search.replace(' [COLOR red]*HD*[/COLOR]', '')
    res_name = []
    res_url = []
    res_name.append('Manualy enter search...')
    
    if manual:
        results = SearchGoogle(search)
        for res in results:
            if res.url.encode('utf8').startswith('http://www.youtube.com/watch'):
                res_name.append(res.title.encode('utf8'))
                res_url.append(res.url.encode('utf8'))
    else:
        results = SearchGoogle(search+' official trailer')
        for res in results:
            if res.url.encode('utf8').startswith('http://www.youtube.com/watch'):
                res_name.append(res.title.encode('utf8'))
                res_url.append(res.url.encode('utf8'))
        results = SearchGoogle(search[:(len(search)-7)]+' official trailer')
        for res in results:
            if res.url.encode('utf8').startswith('http://www.youtube.com/watch') and res.url.encode('utf8') not in res_url:
                res_name.append(res.title.encode('utf8'))
                res_url.append(res.url.encode('utf8'))
            
    dialog = xbmcgui.Dialog()
    ret = dialog.select(search + ' trailer search',res_name)
       
    # Manual search for trailer
    if ret == 0:
        if manual:
            default = search
            title = 'Manual Search for '+search
        else:
            default = search+' official trailer'
            title = 'Manual Trailer Search for '+search
        keyboard = xbmc.Keyboard(default, title)
        #keyboard.setHiddenInput(hidden)
        keyboard.doModal()
        
        if keyboard.isConfirmed():
            result = keyboard.getText()
            SearchForTrailer(result, imdb_id, type, manual=True) 
    # Found trailers
    elif ret > 0:
        trailer_url = res_url[ret - 2]
        xbmc.executebuiltin(
            "PlayMedia(plugin://plugin.video.youtube/?action=play_video&videoid=%s&quality=720p)" 
            % str(trailer_url)[str(trailer_url).rfind("v=")+2:] )
        
        if type=='100':
            media_type='movie'
        elif type=='12':
            media_type='tvshow'
        metaget.update_trailer(media_type, imdb_id, trailer_url)
        xbmc.executebuiltin("XBMC.Container.Refresh")
    else:
        res_name.append('Nothing Found. Thanks!!!')


def ChangeWatched(imdb_id, videoType, name, season, episode, year='', watched='', refresh=False):
    metaget.change_watched(videoType, name, imdb_id, season=season, episode=episode, year=year, watched=watched)
    if refresh:
        xbmc.executebuiltin("XBMC.Container.Refresh")


def SimilarMovies(tmdb_id):
    movie_list = metaget.similar_movies(tmdb_id)
    name_list = []
    filtered_movie_list = []
    if movie_list:
        for movie in movie_list:
            if movie['id'] != None:
                filtered_movie_list.append(movie)
                name_list.append(movie['title'])
    
        dialog = xbmcgui.Dialog()
        index = dialog.select('Select a movie to search in Icefilms', name_list)
        if index > -1:
            xbmc.executebuiltin("XBMC.Container.Update(%s?mode=555&url=%s&search=%s&nextPage=0)" % (sys.argv[0], iceurl, name_list[index]))


def addLocal(name,filename, listitem=False):

    if listitem == None:
        liz=xbmcgui.ListItem(name)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
    else:
        liz = listitem
    ok=True
    liz=xbmcgui.ListItem(name)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
 
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=filename,listitem=liz,isFolder=False)
    return ok
     
     
def addDownloadControls(name,localFilePath, listitem=None):
    #encode name
    sysname = urllib.quote_plus(name)
    
    statusUrl = sys.argv[0] + "?mode=207&name=" + sysname
    cancelUrl = sys.argv[0] + "?&mode=208&name=" + sysname
    ok = True
    
    #add Download info
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=statusUrl,listitem=xbmcgui.ListItem("Download Info"),isFolder=False)
    addon.log_debug('Ok: %s' % ok)
          
    #add Cancel Download
    ok = ok and xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=cancelUrl,listitem=xbmcgui.ListItem("Cancel Download"),isFolder=False)
    addon.log_debug('Ok: %s' % ok)

    #add Play File
    ok = ok and addLocal("Play Downloading " + name, localFilePath, listitem)
    addon.log_debug('Ok: %s' % ok)
    
    return ok


def ShowDownloadInfo(name):
    if not xbmcvfs.exists(os.path.join(downloadPath, 'Downloading')):
        Notify('big','Download Inactive!','Download is not active','')
    else:
        save(os.path.join(downloadPath, 'ShowDLInfo'),'ShowDLInfo')
    return True
 

def CancelDownload(name, video_seek=False):
    if not xbmcvfs.exists(os.path.join(downloadPath, 'Downloading')):
        if not video_seek:
            Notify('big','Download Inactive!','Download is not active','')
    else:
        save(os.path.join(downloadPath, 'Cancel'),'Cancel')    
    return True


def get_default_action():
   action_setting = addon.get_setting('play-action')
   addon.log_debug("action_setting =" + action_setting)
   if action_setting == "1":
       return 201
   elif action_setting == "2":
       return 206

   #default is stream
   return 200


def show_addon_help():

    # Import PyXBMCt module.
    import pyxbmct.addonwindow as pyxbmct

    try:
        common_addon_version = 'Unknown'
        from addon import common
        common_addon_version = common.common.addon_version
    except Exception, e:
        addon.log_debug('Failed to import addon.common: %s' % e)
        pass

    try:
        axel_addon_version = 'Unknown'
        from axel import axelcommon
        axel_addon_version = axelcommon.addon_version
    except Exception, e:
        addon.log_debug('Failed to import axelcommon: %s' % e)
        pass        
        
    # Create a window instance.
    window = pyxbmct.AddonDialogWindow('Icefilms XBMC Addon Help')
    # Set the window width, height, rows, columns.
    window.setGeometry(850, 600, 12, 8)

    # Icefilms logo
    image = pyxbmct.Image(addon.get_icon())
    window.placeControl(image, 0, 0, rowspan=3, columnspan=2)      

    # Addon current information
    textBox = pyxbmct.TextBox(textColor='0xFFFFFFFF')
    window.placeControl(textBox, 0, 2, columnspan=5, rowspan=2)
    textBox.setText('[B]Author:[/B] %s\n[B]Current version:[/B] %s\n[B]Support:[/B] www.tvaddons.ag.com' % (addon.get_author(), addon.get_version()))
    
    #Installed dependencies
    textBox = pyxbmct.TextBox(textColor='0xFFFFFFFF')
    window.placeControl(textBox, 3, 0, columnspan=7, rowspan=3)
    textBox.setText('[B]Installed Dependencies:[/B]\n    [B]Metahandlers:[/B] %s \n    [B]Common addon methods:[/B] %s \n    [B]Axel Downloader:[/B] %s' % (metahandler_version, common_addon_version, axel_addon_version))

    # Folder locations      
    label = pyxbmct.Label('[B]Installed location:[/B] \n[B]Data Location:[/B]')
    window.placeControl(label, 6, 0, columnspan=2)

    fadeLabel = pyxbmct.FadeLabel(textColor='0xFFFFFFFF')
    window.placeControl(fadeLabel, 6, 2, columnspan=6)
    fadeLabel.addLabel('%s\n%s' % (addon.get_path(), addon.get_profile()))
    
    #Addon description
    textBox = pyxbmct.TextBox(textColor='0xFFFFFFFF')
    window.placeControl(textBox, 7, 0, columnspan=7, rowspan=4)
    textBox.setText(addon.get_description())
  
    # Create a button.
    button = pyxbmct.Button('Close')
    # Place the button on the window grid.
    window.placeControl(button, 11, 3, columnspan=2)
    # Set initial focus on the button.
    window.setFocus(button)
    # Connect the button to a function.
    window.connect(button, window.close)
    # Connect a key action to a function.
    window.connect(pyxbmct.ACTION_NAV_BACK, window.close)
    # Show the created window.
    window.doModal()

    
def flush_cache():
    dlg = xbmcgui.Dialog()
    ln1 = 'Are you sure you want to '
    ln2 = 'delete the url cache?'
    ln3 = 'This will slow things down until rebuilt'
    yes = 'Keep'
    no = 'Delete'
    if dlg.yesno('Flush web cache', ln1, ln2, ln3, yes, no):
        db_connection.flush_cache()


def reset_db():
    if db_connection.reset_db():
        message='DB Reset Successful'
    else:
        message='Reset only allowed on SQLite DBs'
    
    Notify('small','Icefilms', message,'')


if mode=='main': #or url==None or len(url)<1:
        CATEGORIES()

elif mode=='991':
       addon.log_debug("Mode 991 ******* dirmode is " + str(dirmode) + " *************  url is -> " + url)
       SimilarMovies(tmdbnum)

elif mode=='999':
        addon.log_debug( "Mode 999 ******* dirmode is " + str(dirmode) + " *************  url is -> " + url)
        REFRESH(video_type, url,imdbnum,name,dirmode)

elif mode=='998':
        addon.log_debug( "Mode 998 (season meta refresh) ******* dirmode is " + str(dirmode) + " *************  url is -> "+url)
        season_refresh(url,imdbnum,name,dirmode,season_num)
        
elif mode=='997':
        addon.log_debug( "Mode 997 (episode meta refresh) ******* dirmode is " + str(dirmode) + " *************  url is -> "+url)
        episode_refresh(url,imdbnum,name,dirmode,season_num,episode_num)    

elif mode=='996':
        addon.log_debug( "Mode 996 (trailer search) ******* name is " + str(name) + " *************  url is -> "+url)
        SearchForTrailer(name, imdbnum, dirmode)
        
elif mode=='990':
        addon.log_debug( "Mode 990 (Change watched value) ******* name is " + str(name) + " *************  season is -> '"+season_num+"'" + " *************  episode is -> '"+episode_num+"'")
        ChangeWatched(imdbnum, video_type, name, season_num, episode_num, refresh=True)
 
elif mode=='addon_help':
    show_addon_help()
    
elif mode=='resolver_settings':
    urlresolver.display_settings()

elif mode=='flush_cache':
    flush_cache()
    
elif mode=='reset_db':
    reset_db()

elif mode=='clear_watched':
    clear_watched()
elif mode=='clear_tv_watched':
    clear_watched(VideoType_TV)
elif mode=='clear_movie_watched':
    clear_watched(VideoType_Movies)
elif mode=='clear_episode_watched':
    clear_watched(VideoType_Episode)    

elif mode=='remove_watched':
    remove_watched()

elif mode=='clear_queue':
    clear_queue()
elif mode=='clear_tv_queue':
    clear_queue(VideoType_TV)
elif mode=='clear_movie_queue':
    clear_queue(VideoType_Movies)
elif mode=='clear_episode_queue':
    clear_queue(VideoType_Episode)    

elif mode=='remove_queue':
    remove_queue()    
    
elif mode=='add_queue':
    add_queue()    
    
elif mode=='50':
        TVCATEGORIES(url)

elif mode=='51':
        MOVIECATEGORIES(url)

elif mode=='52':
        MUSICCATEGORIES(url)

elif mode=='53':
        STANDUPCATEGORIES(url)

elif mode=='54':
        OTHERCATEGORIES(url)

elif mode=='55':
        SEARCH(url)

elif mode=='57':
        FAVOURITES(url)

elif mode=='58':
        addon.log_debug( "Metahandler Settings")
        import metahandler
        metahandler.display_settings()
        callEndOfDirectory = False

elif mode=='570':
        getFavourites(VideoType_TV)

elif mode=='571':
        getFavourites(VideoType_Movies)

elif mode=='572':
        get_recent_watched(VideoType_Movies)

elif mode=='573':
        get_recent_watched(VideoType_Episode)

elif mode=='574':
        get_queue_list(VideoType_Movies)

elif mode=='575':
        get_queue_list(VideoType_Episode)
        
elif mode=='58':
        CLEAR_FAVOURITES(url)

elif mode=='60':
        RECENT(url)

elif mode=='61':
        LATEST(url)

elif mode=='62':
        WATCHINGNOW(url)
        
elif mode=='recent_watched':
        recently_watched()
elif mode=='recent_watched_movie':
        get_recent_watched(VideoType_Movies)
elif mode=='recent_watched_tv':
        get_recent_watched(VideoType_TV)
elif mode=='recent_watched_episode':
        get_recent_watched(VideoType_Episode)

elif mode=='watch_queue':
        watch_queue()
elif mode=='watch_queue_movie':
        get_queue_list(VideoType_Movies)
elif mode=='watch_queue_tv':
        get_queue_list(VideoType_TV)
elif mode=='watch_queue_episode':
        get_queue_list(VideoType_Episode)
        
elif mode=='63':
        HD720pCat(url)
        
elif mode=='64':
        Genres(url)

elif mode=='70':
        Action(url)

elif mode=='71':
        Animation(url)

elif mode=='72':
        Comedy(url)

elif mode=='73':
        Documentary(url)

elif mode=='74':
        Drama(url)

elif mode=='75':
        Family(url)

elif mode=='76':
        Horror(url)

elif mode=='77':
        Romance(url)

elif mode=='78':
        SciFi(url)

elif mode=='79':
        Thriller(url)
    
elif mode=='1':
        MOVIEA2ZDirectories(url)

elif mode=='2':
        MOVIEINDEX(url)
        
elif mode=='10':
        TVA2ZDirectories(url)

elif mode=='11':
        TVINDEX(url)

elif mode=='12':
        TVSEASONS(url,imdbnum)

elif mode=='13':
        TVEPISODES(name,url,None,imdbnum)

# Some tv shows will not be correctly identified, so to load their sources need to check on mode==14
elif mode=='14':
        LOADMIRRORS(url)

elif mode=='100':
        LOADMIRRORS(url)

elif mode=='110':
        # if you dont use the "url", "name" params() then you need to define the value# along with the other params.
        ADD_TO_FAVOURITES(name, url, imdbnum, video_type)

elif mode=='111':
        DELETE_FROM_FAVOURITES(url)

elif mode=='200':
        Stream_Source(name, stacked=stacked_parts)

elif mode=='201':
        Stream_Source(name, download=True, stacked=stacked_parts)
        #Download_Source(name,url)

elif mode=='202':
        Stream_Source(name, stacked=stacked_parts, download_jdownloader=True)

elif mode=='203':
        Kill_Streaming(name,url)

elif mode=='205':
        PlayFile(name,url)
        
elif mode=='206':
        Stream_Source(name, download_play=True, stacked=stacked_parts)
        #Download_And_Play(name,url)

elif mode=='207':
        ShowDownloadInfo(name)

elif mode=='208':
        CancelDownload(name)        

elif mode=='555':
        addon.log_debug("Mode 555 (Get More...) ******* search string is " + search + " *************  nextPage is " + nextPage)
        DoSearch(url, search, int(nextPage))
		
elif mode=='5555':
    addon.log_debug("Mode 5555 (Predefined Search...) ******* search string is " + search)
    KnownSearch(search, url)
         
elif mode=='666':
        create_meta_pack()
        
if callEndOfDirectory and int(sys.argv[1]) <> -1:
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
#xbmcplugin.endOfDirectory(int(sys.argv[1]))
