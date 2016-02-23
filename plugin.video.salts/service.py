"""
    SALTS XBMC Addon
    Copyright (C) 2014 tknorris

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import xbmc
import xbmcgui
import xbmcaddon
from salts_lib import kodi
from salts_lib import log_utils
from salts_lib import utils
from salts_lib import utils2
from salts_lib.constants import MODES
from salts_lib.constants import TRIG_DB_UPG
from salts_lib.db_utils import DB_Connection

MAX_ERRORS = 10

log_utils.log('Service: Installed Version: %s' % (kodi.get_version()))
db_connection = DB_Connection()
if kodi.get_setting('use_remote_db') == 'false' or kodi.get_setting('enable_upgrade') == 'true':
    if TRIG_DB_UPG:
        db_version = db_connection.get_db_version()
    else:
        db_version = kodi.get_version()
    db_connection.init_database(db_version)

class Service(xbmc.Player):
    def __init__(self, *args, **kwargs):
        log_utils.log('Service: starting...')
        xbmc.Player.__init__(self, *args, **kwargs)
        self.win = xbmcgui.Window(10000)
        self.reset()

    def reset(self):
        log_utils.log('Service: Resetting...')
        self.win.clearProperty('salts.playing')
        self.win.clearProperty('salts.playing.trakt_id')
        self.win.clearProperty('salts.playing.season')
        self.win.clearProperty('salts.playing.episode')
        self.win.clearProperty('salts.playing.srt')
        self.win.clearProperty('salts.playing.trakt_resume')
        self.win.clearProperty('salts.playing.salts_resume')
        self.tracked = False
        self._totalTime = 999999
        self.trakt_id = None
        self.season = None
        self.episode = None
        self._lastPos = 0

    def onPlayBackStarted(self):
        log_utils.log('Service: Playback started')
        playing = self.win.getProperty('salts.playing') == 'True'
        self.trakt_id = self.win.getProperty('salts.playing.trakt_id')
        self.season = self.win.getProperty('salts.playing.season')
        self.episode = self.win.getProperty('salts.playing.episode')
        srt_path = self.win.getProperty('salts.playing.srt')
        trakt_resume = self.win.getProperty('salts.playing.trakt_resume')
        salts_resume = self.win.getProperty('salts.playing.salts_resume')
        if playing:   # Playback is ours
            log_utils.log('Service: tracking progress...')
            self.tracked = True
            if srt_path:
                log_utils.log('Service: Enabling subtitles: %s' % (srt_path))
                self.setSubtitles(srt_path)
            else:
                self.showSubtitles(False)

        self._totalTime = 0
        while self._totalTime == 0:
            try:
                self._totalTime = self.getTotalTime()
            except RuntimeError:
                self._totalTime = 0
                break
            xbmc.sleep(1000)

        if salts_resume:
            log_utils.log("Salts Local Resume: Resume Time: %s Total Time: %s" % (salts_resume, self._totalTime), log_utils.LOGDEBUG)
            self.seekTime(float(salts_resume))
        elif trakt_resume:
            resume_time = float(trakt_resume) * self._totalTime / 100
            log_utils.log("Salts Trakt Resume: Percent: %s, Resume Time: %s Total Time: %s" % (trakt_resume, resume_time, self._totalTime), log_utils.LOGDEBUG)
            self.seekTime(resume_time)

    def onPlayBackStopped(self):
        log_utils.log('Service: Playback Stopped')
        if self.tracked:
            # clear the playlist if SALTS was playing and only one item in playlist to
            # use playlist to determine playback method in get_sources
            pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
            plugin_url = 'plugin://%s/' % (kodi.get_id())
            if pl.size() == 1 and pl[0].getfilename().lower().startswith(plugin_url):
                log_utils.log('Service: Clearing Single Item SALTS Playlist', log_utils.LOGDEBUG)
                pl.clear()
                
            playedTime = float(self._lastPos)
            try: percent_played = int((playedTime / self._totalTime) * 100)
            except: percent_played = 0  # guard div by zero
            pTime = utils2.format_time(playedTime)
            tTime = utils2.format_time(self._totalTime)
            log_utils.log('Service: Played %s of %s total = %s%%' % (pTime, tTime, percent_played), log_utils.LOGDEBUG)
            if playedTime == 0 and self._totalTime == 999999:
                log_utils.log('Kodi silently failed to start playback', log_utils.LOGWARNING)
            elif playedTime >= 5:
                log_utils.log('Service: Setting bookmark on |%s|%s|%s| to %s seconds' % (self.trakt_id, self.season, self.episode, playedTime), log_utils.LOGDEBUG)
                db_connection.set_bookmark(self.trakt_id, playedTime, self.season, self.episode)
                if percent_played >= 75:
                    if xbmc.getCondVisibility('System.HasAddon(script.trakt)'):
                        run = 'RunScript(script.trakt, action=sync, silent=True)'
                        xbmc.executebuiltin(run)
            self.reset()

    def onPlayBackEnded(self):
        log_utils.log('Service: Playback completed')
        self.onPlayBackStopped()

monitor = Service()
utils.do_startup_task(MODES.UPDATE_SUBS)

was_on = False
def disable_global_cx():
    global was_on
    if xbmc.getCondVisibility('System.HasAddon(plugin.program.super.favourites)'):
        active_plugin = xbmc.getInfoLabel('Container.PluginName')
        sf = xbmcaddon.Addon('plugin.program.super.favourites')
        if active_plugin == kodi.get_id():
            if sf.getSetting('CONTEXT') == 'true':
                log_utils.log('Disabling Global CX while SALTS is active', log_utils.LOGDEBUG)
                was_on = True
                sf.setSetting('CONTEXT', 'false')
        elif was_on:
            log_utils.log('Re-enabling Global CX while SALTS is not active', log_utils.LOGDEBUG)
            sf.setSetting('CONTEXT', 'true')
            was_on = False
    
errors = 0
while not xbmc.abortRequested:
    try:
        isPlaying = monitor.isPlaying()
        utils.do_scheduled_task(MODES.UPDATE_SUBS, isPlaying)
        if monitor.tracked and monitor.isPlayingVideo():
            monitor._lastPos = monitor.getTime()
    except Exception as e:
        errors += 1
        if errors >= MAX_ERRORS:
            log_utils.log('Service: Error (%s) received..(%s/%s)...Ending Service...' % (e, errors, MAX_ERRORS), log_utils.LOGERROR)
            break
        else:
            log_utils.log('Service: Error (%s) received..(%s/%s)...Continuing Service...' % (e, errors, MAX_ERRORS), log_utils.LOGERROR)
    else:
        errors = 0

    xbmc.sleep(1000)
    disable_global_cx()
    
log_utils.log('Service: shutting down...')
