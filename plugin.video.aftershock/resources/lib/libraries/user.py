# -*- coding: utf-8 -*-

'''
    Copyright (C) 2017 IDev

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
'''


import re,hashlib,time, base64

from fileFetcher import *
import control
import cache

try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database

def validateUser(emailAddress=None, showRegisteration=False):
    try:
        url = None
        if (emailAddress == None or emailAddress == ''):
            emailAddress = control.setting('user.email')
        if (emailAddress == None or emailAddress == '') and showRegisteration:
            control.dialog.ok(control.addonInfo('name'), "User not registered. Please provide the email address used to make the donation")
            t = control.lang(30275).encode('utf-8')
            k = control.keyboard('', t) ; k.doModal()
            emailAddress = k.getText() if k.isConfirmed() else None
        elif (emailAddress == None or emailAddress == ''):
            return (control.INVALID, url)

        valid = cache.get(validate, 168, emailAddress, table='live_cache')
        if valid <= 0 :
            return valid, ''
        url = base64.b64decode('aHR0cHM6Ly9vZmZzaG9yZWdpdC5jb20vdmluZWVndS9hZnRlcnNob2NrLXJlcG8vZ3VpZGVzLw==')
        return (valid, url)

    except Exception as e:
        logger.error(e)
        control.dialog.ok(control.addonInfo('name'), "User not registered. Please make a donation (min. $5) to aftershockpy@gmail.com via PayPal to get access !!")
        control.setSetting('user.email', '')
        return (control.INVALID, url)

def validate(emailAddress):
    fileFetcher = FileFetcher(control.userFile, control.addon)
    retValue = fileFetcher.fetchFile()
    control.makeFile(control.dataPath)

    userFile = os.path.join(control.dataPath, control.userFile.split('/')[-1])
    dbcon = database.connect(userFile)
    dbcur = dbcon.cursor()

    import hashlib
    m = hashlib.md5()
    m.update(emailAddress.lower())
    emailMd5 = m.hexdigest()

    dbcur.execute("SELECT * FROM af_users WHERE email = '%s'" % (emailMd5))
    match = dbcur.fetchone()

    userName = match[0]
    t1 = int(match[3])
    t2 = int(time.time())
    expired = t1 - t2
    expiredDays = expired / (3600 * 24)
    if expired < 0 :
        control.dialog.ok(control.addonInfo('name'), "Your access has expired. Please make a donation (min. $5) to aftershockpy@gmail.com via PayPal to get access !!")
        return control.EXPIRED
    else:
        if control.setting('user.email') == '':
            control.dialog.ok(control.addonInfo('name'), "%s - Thanks for your donation !!" % userName)
        control.setSetting('user.email', emailAddress)
        return control.VALID