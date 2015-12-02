# -*- coding=utf8 -*-
#******************************************************************************
# ChunkPlayer.py
#------------------------------------------------------------------------------
#
# Copyright (c) 2014 LivingOn <LivingOn@xmail.net>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#******************************************************************************
import re
import sys
import socket
import random
import urllib2
import Queue
import threading
import xbmc
import xbmcgui
import xbmcaddon

from resources.lib.Config import Config
from resources.lib.Recorder import Recorder

class PlaylistAnylyser(object):
    "Ermittelt die URL und Sequenznummer der einzelnen Chunks."

    def get_streamurl_and_sequencenr(self, actor):
        "Liefert die Stream-URL und die Sequenznummer."
        playlist     = self._get_playlist(actor)
        if playlist:
            streambase   = self._get_playlist_url(playlist)
            chunkurl     = self._get_chunk_url(streambase, playlist)
            chunkcontent = self._get_chunk_content(chunkurl)
            sequencenr   = self._get_sequence_nr(chunkcontent)
            mediabase    = self._get_mediabase(streambase, chunkcontent)
            return (mediabase, sequencenr)
        else:
            return (None,None)

    def _get_playlist(self, actor):
        "Liefert die *.m3u8-Playlist."
        url = "%s/%s" % (Config.CHATURBATE_URL, actor)
        data = urllib2.urlopen(url).read()
        try:
            playlist = re.findall(r'(http.*?://.*?.stream.highwebmedia.com:1935.*?m3u8)',data)[0]
            return playlist
        except:
            pass

    def _get_playlist_url(self, playlist):
        "Liefert die URL der Playlist."
        return re.findall(r'(.*)playlist.*', playlist)[0]
    
    def _get_chunk_url(self, streambase, playlist):
        "Liefert die URL zur Chunk-Playlist."
        data = urllib2.urlopen(playlist).read()
        stream = re.findall(r'(chunk.*)',data)[0]
        return "%s%s" % (streambase, stream)

    def _get_chunk_content(self, chunkurl):
        "Liefert die Chunk-Content."
        return urllib2.urlopen(chunkurl).read()
    
    def _get_sequence_nr(self, chunkcontent):
        "Liefert die aktuelle Sequenzummer."
        return int(re.findall(r'EXT-X-MEDIA-SEQUENCE:(\d*)',chunkcontent)[0])

    def _get_mediabase(self, streambase, chunkcontent):
        "Liefert die Basis-URL zum Chunk."
        name = re.findall(r'(media_w.*?_)',chunkcontent)[0]
        return "%s%s" % (streambase, name)


class ChunkGrabber(threading.Thread):
    "Schreibt die Chunks in die Streamqueue."
        
    MILLISECONDS_TO_DELAY_AT_START = 1000
    MILLISECONDS_TO_DELAY_AT_RUN   = 5000 
      
    def __init__(self, streamurl, sequencenr, streamqueue):
        threading.Thread.__init__(self)    
        self._streamurl = streamurl
        self._sequencenr = sequencenr + 1
        self._streamqueue = streamqueue
        self._stop_running_thread = False
        self._seconds_to_delay = self.MILLISECONDS_TO_DELAY_AT_START
          
    def run(self):
        "Lädt Stream von Chaturbate und pumpt sie in die Streamqueue."
        for i in xrange(self._sequencenr, sys.maxint):
            url = "%s%d.ts" %(self._streamurl, i)
            while True:
                daten = self._get_daten(url)
                if (daten):
                    self._streamqueue.put(daten)
                    self._seconds_to_delay = self.MILLISECONDS_TO_DELAY_AT_RUN
                    break
                else:
                    xbmc.sleep(self._seconds_to_delay)
                if self._stop_running_thread:
                    break
            if self._stop_running_thread:
                break
              
    def stop(self):
        "Thread soll beendet werden."
        self._stop_running_thread = True
          
    def _get_daten(self, url):
        "Liefert die Daten des Chunks."
        result = None
        try:
            result = urllib2.urlopen(url).read()
        except:
            pass
        return result

class LocalStreamServer(threading.Thread):
    "Startet einen lokalen Streamserver."
     
    def __init__(self, streamurl, sequencenr, port, recorder):
        threading.Thread.__init__(self)
        self._streamurl = streamurl
        self._sequencenr = sequencenr
        self._port = port
        self._recorder = recorder
        self._streamqueue = Queue.Queue()
        self._chunkgrabber_thread = ChunkGrabber(
            self._streamurl, 
            self._sequencenr, 
            self._streamqueue
        )

    def run(self):
        "Startet lokalen Streamserver und stellt Stream zur Verfügung."
        self._chunkgrabber_thread.start()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_address = ("127.0.0.1", self._port)
        sock.bind(server_address)
        sock.listen(1)
        active = True                       
        while active:
            connection = sock.accept()[0]
            client_header = connection.recv(4096)
            connection.send(self._get_header())
            if client_header.startswith("HEAD"):
                connection.close()
                continue
            else:
                is_initial_call = True
                initial_call_counter = 0
                self._recorder.open()
                while active:
                    if not self._streamqueue.empty():
                        is_initial_call = False
                        try:
                            chunk = self._streamqueue.get()
                            self._recorder.write(chunk)
                            connection.send(chunk)
                        except:
                            self._chunkgrabber_thread.stop()
                            break
                    else:
                        try:
                            connection.send("")
                        except:
                            self._chunkgrabber_thread.stop()
                            break
                        if is_initial_call:
                            initial_call_counter += 1
                            if initial_call_counter > 10:
                                self._chunkgrabber_thread.stop()
                                active = False
                        xbmc.sleep(1000)
                self._recorder.close()
                break

    def _get_header(self):
        return "\r\n".join( [
            "HTTP/1.1 200 OK",
            "Accept-Ranges: bytes",
            "Content-Type: video/mp4",
            "",
            "",
        ]) 
    

class ChunkPlayer(object):
    "Sammelt die Chunks ein und spielt sie ab."
    
    def __init__(self, plugin_id):
        self._plugin_id = plugin_id
     
    def play_stream(self, actor):    
        pa = PlaylistAnylyser()
        
        streamurl, sequencenr =  pa.get_streamurl_and_sequencenr(actor)
        if streamurl and sequencenr:
            recorder = Recorder(actor)
            port = int("49%d" % random.sample(xrange(100,999),1)[0])
            local_stream_server_thread = LocalStreamServer(
                streamurl,
                sequencenr,
                port,
                recorder
            )
            local_stream_server_thread.start()
            listitem = xbmcgui.ListItem(actor)
            xbmc.sleep(1000)
            xbmc.Player(xbmc.PLAYER_CORE_AUTO).play("http://127.0.0.1:%s" % port, listitem)
        else:
            addon = xbmcaddon.Addon(id = Config.PLUGIN_NAME)
            title = addon.getLocalizedString(30180)
            msg = addon.getLocalizedString(30185) % actor
            xbmcgui.Dialog().ok(title, msg)

        