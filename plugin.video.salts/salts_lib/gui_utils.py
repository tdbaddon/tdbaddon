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
import xbmcgui
import time
import kodi
import random
import json
import urllib2
from utils2 import reset_base_url, i18n
from trakt_api import Trakt_API
from salts_lib import log_utils

INTERVALS = 5

def auth_trakt():
    start = time.time()
    use_https = kodi.get_setting('use_https') == 'true'
    trakt_timeout = int(kodi.get_setting('trakt_timeout'))
    trakt_api = Trakt_API(use_https=use_https, timeout=trakt_timeout)
    result = trakt_api.get_code()
    code, expires, interval = result['device_code'], result['expires_in'], result['interval']
    time_left = expires - int(time.time() - start)
    line1 = i18n('verification_url') % (result['verification_url'])
    line2 = i18n('prompt_code') % (result['user_code'])
    line3 = i18n('code_expires') % (time_left)
    with kodi.ProgressDialog(i18n('trakt_acct_auth'), line1=line1, line2=line2, line3=line3) as pd:
        pd.update(100)
        while time_left:
            for _ in range(INTERVALS):
                kodi.sleep(interval * 1000 / INTERVALS)
                if pd.is_canceled(): return

            try:
                result = trakt_api.get_device_token(code)
                break
            except urllib2.URLError as e:
                # authorization is pending; too fast
                if e.code in [400, 429]:
                    pass
                elif e.code == 418:
                    kodi.notify(msg=i18n('user_reject_auth'), duration=3000)
                    return
                elif e.code == 410:
                    break
                else:
                    raise
                
            time_left = expires - int(time.time() - start)
            progress = time_left * 100 / expires
            pd.update(progress, line3=i18n('code_expires') % (time_left))
        
    try:
        kodi.set_setting('trakt_oauth_token', result['access_token'])
        kodi.set_setting('trakt_refresh_token', result['refresh_token'])
        trakt_api = Trakt_API(result['access_token'], use_https=use_https, timeout=trakt_timeout)
        profile = trakt_api.get_user_profile(cached=False)
        kodi.set_setting('trakt_user', '%s (%s)' % (profile['username'], profile['name']))
        kodi.notify(msg=i18n('trakt_auth_complete'), duration=3000)
    except Exception as e:
        log_utils.log('Trakt Authorization Failed: %s' % (e), log_utils.LOGDEBUG)

def perform_auto_conf(responses):
    length = len(responses)
    TOTAL = 12
    if length < TOTAL:
        responses += [True] * (TOTAL - length)
        
    if responses[0]: kodi.set_setting('trakt_timeout', '60')
    if responses[1]: kodi.set_setting('calendar-day', '-1')
    if responses[2]: kodi.set_setting('calendar_time', '2')
    if responses[3]: kodi.set_setting('source_timeout', '20')
    if responses[4]: kodi.set_setting('include_watchlist_next', 'true')
    if responses[5]: kodi.set_setting('filter_direct', 'true')
    if responses[6]: kodi.set_setting('filter_unusable', 'true')
    if responses[7]: kodi.set_setting('show_debrid', 'true')
    if responses[8]: kodi.set_setting('source_results', '0')
    if responses[9]:
        kodi.set_setting('enable_sort', 'true')
        kodi.set_setting('sort1_field', '2')
        kodi.set_setting('sort2_field', '5')
        kodi.set_setting('sort3_field', '6')
        kodi.set_setting('sort4_field', '1')
        kodi.set_setting('sort5_field', '3')
        kodi.set_setting('sort6_field', '4')

    if responses[10]:
        tiers = ['Local', 'Premiumize.V2', 'Premiumize.me', 'Furk.net', 'EasyNews', 'DD.tv', 'NoobRoom',
                 ['WatchHD', 'IFlix', 'MoviesPlanet', 'TVWTVS', 'MWM', '9Movies', '123Movies', 'niter.tv', 'HDMovie14', 'ororo.tv', 'm4ufree'],
                 ['torba.se', 'StreamLord', 'CyberReel', 'tunemovie', 'MovieMax', 'MovieLocker', 'afdah.org', 'xmovies8', 'xmovies8.v2', 'MovieXK'],
                 ['PelisPedia', 'DayT.se', 'FardaDownload', 'zumvo.com', 'PutMV', 'vivo.to', 'MiraDeTodo', 'FireMoviesHD'],
                 ['SezonLukDizi', 'Dizimag', 'Dizilab', 'Dizigold', 'Dizibox', 'Diziay', 'Dizipas', 'OneClickTVShows', 'OnlineDizi'],
                 ['DiziFilmHD', 'DL-Pars', 'DDLValley', '2DDL', 'ReleaseBB', 'MyVideoLinks.eu', 'OCW', 'TVRelease.Net', 'alluc.com'],
                 ['IceFilms', 'Flixanity', 'Rainierland', 'WatchEpisodes', 'PrimeWire', 'tvonline', 'SantaSeries', 'WatchSeries', 'Putlocker'],
                 ['Ganool', 'MovieWatcher', 'VKFlix', 'WatchFree.to', 'pftv', 'streamallthis.is', 'Movie4K', 'afdah', 'SolarMovie'],
                 ['UFlix.org', 'wso.ch', 'MovieSub', 'MovieHut', 'CouchTunerV1', 'Watch8Now', 'yshows', 'iWatchOnline', 'MerDB'],
                 ['vidics.ch', 'pubfilm', 'eMovies.Pro', 'OnlineMoviesPro', 'movie25', 'viooz.ac', 'view47', 'MoviesHD', 'LosMovies'],
                 ['wmo.ch', 'stream-tv.co', 'clickplay.to', 'MintMovies', 'MovieNight', 'cmz', 'ch131', 'filmikz.ch', 'moviestorm.eu'],
                 ['TheExtopia', 'MovieTube', 'FilmStreaming.in', 'RLSSource.net']]
    
        sso = []
        random_sso = kodi.get_setting('random_sso') == 'true'
        for tier in tiers:
            if isinstance(tier, basestring):
                sso.append(tier)
            else:
                if random_sso:
                    random.shuffle(tier)
                sso += tier
        kodi.set_setting('source_sort_order', '|'.join(sso))
    
    if responses[11]: reset_base_url()
    trigger = [False, True, False, True, False, True, True, False, True, False, False, False]
    if all([t == r for t, r in zip(trigger, responses)]):
        kodi.set_setting('scraper_download', 'true')
        
    kodi.notify(msg=i18n('auto_conf_complete'))

def do_ip_auth(scraper, visit_url, qr_code):
    EXPIRE_DURATION = 60 * 5
    ACTION_PREVIOUS_MENU = 10
    ACTION_BACK = 92
    CANCEL_BUTTON = 200
    INSTR_LABEL = 101
    QR_CODE_CTRL = 102
    PROGRESS_CTRL = 103
    
    class IpAuthDialog(xbmcgui.WindowXMLDialog):
        def onInit(self):
            # log_utils.log('onInit:', log_utils.LOGDEBUG)
            self.cancel = False
            self.getControl(INSTR_LABEL).setLabel(i18n('ip_auth_line1') + visit_url + i18n('ip_auth_line2'))
            self.progress = self.getControl(PROGRESS_CTRL)
            self.progress.setPercent(100)
            if qr_code:
                img = self.getControl(QR_CODE_CTRL)
                img.setImage(qr_code)
            
        def onAction(self, action):
            # log_utils.log('Action: %s' % (action.getId()), log_utils.LOGDEBUG)
            if action == ACTION_PREVIOUS_MENU or action == ACTION_BACK:
                self.cancel = True
                self.close()

        def onControl(self, control):
            # log_utils.log('onControl: %s' % (control), log_utils.LOGDEBUG)
            pass

        def onFocus(self, control):
            # log_utils.log('onFocus: %s' % (control), log_utils.LOGDEBUG)
            pass

        def onClick(self, control):
            # log_utils.log('onClick: %s' % (control), log_utils.LOGDEBUG)
            if control == CANCEL_BUTTON:
                self.cancel = True
                self.close()
        
        def setProgress(self, progress):
            self.progress.setPercent(progress)

    dialog = IpAuthDialog('IpAuthDialog.xml', kodi.get_path())
    dialog.show()
    interval = 5000
    begin = time.time()
    try:
        while True:
            for _ in range(INTERVALS):
                kodi.sleep(interval / INTERVALS)
                elapsed = time.time() - begin
                progress = int((EXPIRE_DURATION - elapsed) * 100 / EXPIRE_DURATION)
                dialog.setProgress(progress)
                if progress <= 0 or dialog.cancel:
                    return False
                
            authorized, result = scraper.check_auth()
            if authorized: return result
    finally:
        del dialog

def do_auto_config():
    ACTION_PREVIOUS_MENU = 10
    ACTION_BACK = 92
    CONTINUE_BUTTON = 200
    CANCEL_BUTTON = 201

    starty = 60
    posx = 30
    gap = 35
    RADIO_BUTTONS = [
        i18n('set_trakt_timeout'),
        i18n('set_cal_start'),
        i18n('set_cal_airtime'),
        i18n('set_scraper_timeout'),
        i18n('set_wl_mne'),
        i18n('set_test_direct'),
        i18n('set_filter_unusable'),
        i18n('set_show_debrid'),
        i18n('set_no_limit'),
        i18n('set_source_sort'),
        i18n('set_sso'),
        i18n('set_reset_url'),
        i18n('select_all_none')]
    
    class AutoConfDialog(xbmcgui.WindowXMLDialog):
        def onInit(self):
            log_utils.log('onInit:', log_utils.LOGDEBUG)
            self.OK = False
            self.radio_buttons = []
            posy = starty
            for label in RADIO_BUTTONS:
                self.radio_buttons.append(self.__get_radio_button(posx, posy, label))
                posy += gap
            
            try: responses = json.loads(kodi.get_setting('prev_responses'))
            except: responses = [True] * len(self.radio_buttons)
            if len(responses) < len(self.radio_buttons):
                responses += [True] * (len(self.radio_buttons) - len(responses))
            
            self.addControls(self.radio_buttons)
            last_button = None
            for response, radio_button in zip(responses, self.radio_buttons):
                radio_button.setSelected(response)
                if last_button is not None:
                    radio_button.controlUp(last_button)
                    radio_button.controlLeft(last_button)
                    last_button.controlDown(radio_button)
                    last_button.controlRight(radio_button)
                last_button = radio_button

            continue_ctrl = self.getControl(CONTINUE_BUTTON)
            cancel_ctrl = self.getControl(CANCEL_BUTTON)
            self.radio_buttons[0].controlUp(cancel_ctrl)
            self.radio_buttons[0].controlLeft(cancel_ctrl)
            self.radio_buttons[-1].controlDown(continue_ctrl)
            self.radio_buttons[-1].controlRight(continue_ctrl)
            continue_ctrl.controlUp(self.radio_buttons[-1])
            continue_ctrl.controlLeft(self.radio_buttons[-1])
            cancel_ctrl.controlDown(self.radio_buttons[0])
            cancel_ctrl.controlRight(self.radio_buttons[0])
            
        def __get_radio_button(self, x, y, label):
            kwargs = {'font': 'font12', 'focusTexture': 'button-focus2.png', 'noFocusTexture': 'button-nofocus.png', 'focusOnTexture': 'radiobutton-focus.png',
                      'noFocusOnTexture': 'radiobutton-focus.png', 'focusOffTexture': 'radiobutton-nofocus.png', 'noFocusOffTexture': 'radiobutton-nofocus.png'}
            temp = xbmcgui.ControlRadioButton(x, y, 450, 30, label, **kwargs)
            return temp
            
        def onAction(self, action):
            # log_utils.log('Action: %s' % (action.getId()), log_utils.LOGDEBUG)
            if action == ACTION_PREVIOUS_MENU or action == ACTION_BACK:
                self.close()

        def onControl(self, control):
            # log_utils.log('onControl: %s' % (control), log_utils.LOGDEBUG)
            pass

        def onFocus(self, control):
            # log_utils.log('onFocus: %s' % (control), log_utils.LOGDEBUG)
            pass

        def onClick(self, control):
            # log_utils.log('onClick: %s' % (control), log_utils.LOGDEBUG)
            focus_button = self.getControl(control)
            if focus_button == self.radio_buttons[-1]:
                all_status = focus_button.isSelected()
                for button in self.radio_buttons:
                    button.setSelected(all_status)
            
            if control == CONTINUE_BUTTON:
                self.OK = True
                
            if control == CANCEL_BUTTON:
                self.OK = False

            if control == CONTINUE_BUTTON or control == CANCEL_BUTTON:
                self.close()
        
        def get_responses(self):
            return [bool(button.isSelected()) for button in self.radio_buttons]

    dialog = AutoConfDialog('AutoConfDialog.xml', kodi.get_path())
    dialog.doModal()
    if dialog.OK:
        responses = dialog.get_responses()
        kodi.set_setting('prev_responses', json.dumps(responses))
        perform_auto_conf(responses)
    del dialog
