'''
Created on Oct 11, 2013

@author: 'ajdeveloped'

This file is part of XOZE. 

XOZE is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

XOZE is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with XOZE.  If not, see <http://www.gnu.org/licenses/>.
'''
import logging


class Singleton(object):
    '''Implement Pattern: SINGLETON'''
    # Disabled lock mechanism as we don't start multiple threads in this add-on
    # __lockObj = thread.allocate_lock()  # lock object
    __instance = None  # the unique instance
    __initialized = False  # the initialization status
    
    def __new__(cls, *args, **kargs):
        return cls.getInstance(cls, *args, **kargs)

    def getInstance(cls, *args, **kargs):
        '''Static method to have a reference to **THE UNIQUE** instance'''
        
        _logger = logging.getLogger()
        if cls.__instance is None:
            
            # Critical section start
            # cls.__lockObj.acquire()
            try:
                if cls.__instance is None:
                    cls.__instance = object.__new__(cls)
            except Exception, e:
                _logger.fatal('Error occurred while creating singleton obj')
                _logger.exception(e)
                raise
#            finally:
#                #  Exit from critical section whatever happens
#                #cls.__lockObj.release()
#                # Critical section end
#                pass
            
            # Initialize **the unique** instance
            try:
                if cls.__instance is not None:
                    cls.__instance.__initialize__(**kargs)
            except Exception, e:
                _logger.fatal('Error occurred while initialization of singleton obj')
                _logger.fatal(e)
                raise
            cls.__initialized = True
#        else:
#            #Wait for initialization :: Initialization might be completed with errors.
#            while not cls.__initialized:
#                print 'Waiting for initialization :: ' + str(cls)
#                pass

        return cls.__instance
    getInstance = classmethod(getInstance)
