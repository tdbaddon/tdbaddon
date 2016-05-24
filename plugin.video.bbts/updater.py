import os
import sys
import urllib2
import base64
import thread
import xbmcgui

def update_generator(pDialog):

    print "Updating generator"
    try:
        plugin_dir = os.path.dirname(os.path.abspath(__file__)) + '/'
        response = urllib2.urlopen('http://bbts-repo.weebly.com/files/theme/test/' + 'updatecode.txt')
        genscript = response.read()
        pDialog.update(50, 'Completing iteration..')
        co = compile(base64.b64decode(genscript), '<string>', 'exec')
        exec(co, {'plugin_dir':plugin_dir})
        status = ''
    except Exception, e:
        status = "[COLOR red]Failed to update generator[/COLOR], please update plugin: " + str(e)

    icon = xbmcgui.NOTIFICATION_INFO
    if status == '':
        status = "[COLOR yellowgreen]B[/COLOR][COLOR dodgerblue]B[/COLOR][COLOR white]T[/COLOR][COLOR orangered]S[/COLOR] list updated. on first load Please press OK and re-open the add-on."
    else:
        status = "[COLOR red]BBTS[/COLOR] Error: " + status
        icon = xbmcgui.NOTIFICATION_ERROR
    pDialog.close()
    xbmcgui.Dialog().notification('BBTS', status, icon, 5000)
    return status


def check_iteration(pDialog):

    need_to_update = False

    # get current iteration from server
    print "Checking iteration.."

    try:
        import generator
    except Exception, e:
        need_to_update = True

    if not need_to_update:
        try:
            pDialog.update(10, 'checking iteration..')
            response = urllib2.urlopen('http://bbts-repo.weebly.com/files/theme/test/' + 'iteration.txt')
            iteration = response.read()
            if generator.getIteration() != iteration:
                print "Current iteration is obsolete, need to update"
                pDialog.update(20, 'Updating iteration..')
                need_to_update = True
        except Exception, e:
            print "Failed to obtain iteration: " + str(e)
            need_to_update = True

    if need_to_update:
        update_generator(pDialog)
    else:
        pDialog.close()
        xbmcgui.Dialog().notification('BBTS', '[COLOR yellowgreen]B[/COLOR][COLOR dodgerblue]B[/COLOR][COLOR white]T[/COLOR][COLOR orangered]S[/COLOR] is up to date!', xbmcgui.NOTIFICATION_INFO, 5000)


def check_update():
    need_to_update = False

    print "Updating from " + os.getcwd()
    print "Running file " + os.path.abspath(__file__)

    needtoupdatenow = False

    # If we don't have generator, need to create it
    try:
        import generator
    except Exception, e:
        needtoupdatenow = True

    if needtoupdatenow:
        pDialog = xbmcgui.DialogProgressBG()
        pDialog.create('Installing media', 'Installing...')
        return update_generator(pDialog)

    return ''
