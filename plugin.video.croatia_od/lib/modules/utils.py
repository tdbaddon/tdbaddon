# -*- coding: utf-8 -*-
import os,re,sys
from webutils import *
import xbmcvfs,xbmcaddon,xbmcgui,xbmc
from addon.common.addon import Addon
import urllib,urlparse,client


addon = Addon('plugin.video.croatia_od', sys.argv)
my_addon = xbmcaddon.Addon()
addon_path = my_addon.getAddonInfo('path')
addon_id= my_addon.getAddonInfo('id')
subtitles_path = xbmc.translatePath("special://profile/addon_data/"+addon_id+"/subtitles")
if not os.path.exists(subtitles_path):
    os.makedirs(subtitles_path)

def download(name, url):
            my_addon = xbmcaddon.Addon()
            desty= my_addon.getSetting('downloads_folder')
            if not xbmcvfs.exists(desty):
                xbmcvfs.mkdir(desty)

            title=name
            name=re.sub('[^-a-zA-Z0-9_.() ]+', '', name)
            name=name.rstrip('.')
            ext = os.path.splitext(urlparse.urlparse(url).path)[1][1:]
            if not ext in ['mp4', 'mkv', 'flv', 'avi', 'mpg', 'mp3']: ext = 'mp4'
            filename = name + '.' + ext
      
            

            dest = os.path.join(desty, filename)
            new=my_addon.getSetting('new_downloader')
            if  new=='false':
                from lib.modules import commondownloader
                commondownloader.download(url, dest, 'Croatia On Demand')
            else:
                content = int(urllib.urlopen(url).info()['Content-Length'])
                size = 1024 * 1024
                mb   = content / (1024 * 1024)
                if xbmcgui.Dialog().yesno('Croatia On Demand - Potvrda preuzimanja', filename, 'Veličina datoteke je %dMB' % mb, 'Nastaviti s preuzimanjem?', 'Nastavi',  'Prekini') == 1:
                  return
                import SimpleDownloader as downloader
                downloader = downloader.SimpleDownloader()
                params = { "url": url, "download_path": desty, "Title": title }
                downloader.download(filename, params)

def Notify(typeq, box_title, message, times='', line2='', line3=''):
     if box_title == '':
          box_title='Croatia On Demand'
     if typeq == 'small':
          if times == '':
               times='5000'
          smallicon= icon_path('icon.png')
          addon.show_small_popup(title=box_title, msg=message, delay=int(times), image=smallicon)
     elif typeq == 'big':
          addon.show_ok_dialog(message, title=box_title)
     else:
          addon.show_ok_dialog(message, title=box_title)

def titlize(title,length):
  words=title.split(' ')
  new= ''
  for word in words:
    if (len(word)>length):
      word=word.title()
    else:
      word=word.upper()
    new+=' '+ word

  return new

def download_subs(url):
  try:
    srt = client.request(url)
    filename = url.split('/')[-1]
    final_path = os.path.join(subtitles_path, filename)
    final_path = xbmc.translatePath(final_path)
    with open(final_path, 'w') as f:
        f.write(srt)
    return final_path
  except:
    return ''