'''
@summary: Generic timer Classes for test timers, thread timers, etc...
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from datetime import datetime

class GenericTimer():
    '''
    @summary: Generic Timer used to track any time span
    @ivar StartTime: Timestamp from the start of the timer
    @type StartTime: C{datetime}
    @ivar StopTime: Timestamp of the end of the timer
    @type StopTime: C{datetime}
    '''
    def __init__(self):
        self.StartTime = None
        self.StopTime = None

    def start(self):
        '''
        @summary: Starts this timer
        @return: None
        @rtype: None
        '''
        self.StartTime = datetime.now()
        
    def stop(self):
        '''
        @summary: Stops this timer
        @return: None
        @rtype: None
        '''
        self.StopTime = datetime.now()
        
    def get_elapsed_time(self):
        '''
        @summary: Convenience method for total elapsed time
        @rtype: C{datetime}
        @return: Elapsed time for this timer. C{None} if timer has not started
        '''
        elapsedTime = None
        if (self.StartTime != None):
            if (self.StopTime != None):
                elapsedTime = (self.StopTime - self.StartTime)
            else:
                elapsedTime = (datetime.now() - self.StartTime)
        else:
            ''' Timer hasn't started, error on the side of caution '''
            rightNow = datetime.now()
            elapsedTime = (rightNow - rightNow)
        return(elapsedTime)
