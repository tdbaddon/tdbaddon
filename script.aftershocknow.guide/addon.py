# -*- coding: utf-8 -*-
# AftershockNow Guide
# Developed by IDev
# Forked from FTV Guide:
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this Program; see the file LICENSE.txt.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
#

import sys, xbmcaddon

try:
    from lib.libraries import user
    from resources.lib import gui
    valid, url = user.validateUser(xbmcaddon.Addon('plugin.video.aftershock').getSetting('user.email'))
    if valid <= 0:
        import xbmcgui
        xbmcgui.Dialog().ok('Aftershock Now', "Please register your email in Aftershock. [CR][CR] [COLOR red]Video->Add-ons->Aftershock->Live (EPG)[/COLOR]")
        sys.exit(0)
    w = gui.TVGuide()
    w.doModal()
    del w

except:
    import traceback as tb
    (etype, value, traceback) = sys.exc_info()
    tb.print_exception(etype, value, traceback)
