'''
@summary: Log file Persister classes
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
import os
from datetime import datetime

'''
======================================================
            NAMESPACE CONSTANTS
======================================================
@todo: Remove the HACK of hardcoding config values
'''
DEBUG_MODE = True # Logger output Level

class PBLogger(object):
    '''
    @summary: PSYCHOTICALLY BASIC logger
    @ivar: File: File Name of this logger
    @type File:  C{str}
    @ivar: FileMode: Mode this logger runs in. a or w
    @type FileMode:  C{str}
    @ivar: Errors: List of all error messages recorded by this logger
    @type Errors:  C{list}
    @ivar: Warnings: List of all warning messages recorded by this logger
    @type Warnings:  C{list}
    @ivar: IsDebugMode: Flag to turn Debug logging on and off
    @type IsDebugMode:  C{bool}
    @todo: Upgrade this astoundingly basic logger to Python or Twisted logger framework
    @attention: THIS LOGGER IS DESIGNED TO BE TEMPORARY. It will be replaced in the matured framework
    '''
    def __init__(self, isDebugMode = False, fileName = None, fileMode = 'a', log_dir='.', startClean = False, cclog=None):
        self.Errors = []
        self.Warnings = []
        self.IsDebugMode = isDebugMode
        self.FileMode = 'a'
        self.log = cclog
        if fileName is not None:
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            self.File = os.path.normpath(os.path.join(log_dir, fileName))
            if startClean == True and os.path.exists(self.File) == True:
                ''' Force the file to be overwritten before any writing '''
                os.remove(self.File)
        else:
            self.File = None
        
    def __timestamp(self):
        '''
        @summary: Returns the log's current formatted timestamp
        @return: Formatted timestamp string
        @rtype: C{str} 
        '''
        rightNow = datetime.now()
        return ("%d/%d %d:%d:%d" % (rightNow.month,
                                    rightNow.day, 
                                    rightNow.hour, 
                                    rightNow.minute,
                                    rightNow.second))

    def __write(self, message, formatted = True, log_level = ''):
        '''
        @summary: Writes a message to this log file
        @param formatted: Indicates if message applies standard formatting
        @type formatted: C{bool}  
        @return: None
        @rtype: None
        '''
        if formatted:
            logMessage = "%s %s" % (self.__timestamp(), message)
        else:
            ''' Log the raw message '''
            logMessage = "%s" % message
        
        print(logMessage)
        if self.log is not None:
            if log_level == 'warning':
                self.log.warning(logMessage)
            elif log_level == 'info':
                self.log.info(logMessage)
            elif log_level == 'debug':
                self.log.debug(logMessage)
            elif log_level == 'error':
                self.log.error(logMessage)

        if self.File is not None:
            log = open(self.File, self.FileMode)
            log.write("%s\n" % logMessage)
            log.close()
        return

    def logWarning(self, message):
        '''
        @summary: Outputs a formatted WARNING message, updates the internal Warnings stack 
        @param message: Message to report to the log
        @type message: C{str}  
        @return: None  
        @rtype: None
        '''
        self.Warnings.append(message)
        self.__write("WARNING: %s" % message, log_level = 'warning')
        return

    def logError(self, message, isFatal=False):
        '''
        @summary: Outputs a formatted ERROR message, updates the internal Warnings stack 
        @param message: Message to report to the log
        @type message: C{str}  
        @param isFatal: Indicates an error of FATAL severity.
        @type isFatal: C{bool}
        @raise Exception:  Raises message as an Exception if isFatal is True  
        @return: None  
        @rtype: None
        '''
        self.Errors.append(message)
        if isFatal:
            raise Exception, "FATAL: %s" % message
        self.__write("ERROR: %s" % message, log_level = 'error')
        return

    def logMessage(self, message, formatted = True):
        '''
        @summary: Outputs a message with standard formatting
        @param message: Message to report
        @type message: C{str}  
        @param formatted: Indicates if message applies standard formatting
        @type formatted: C{bool}  
        @return: None
        @rtype: None
        '''
        self.__write("%s" % message, formatted, log_level = 'info')
        return

    def logDebug(self, message):
        '''
        @summary: Outputs a message with standard formatting
        @param message: Message to report
        @type message: C{str}  
        @param formatted: Indicates if message applies standard formatting
        @type formatted: C{bool}  
        @return: None
        @rtype: None
        '''
        if self.IsDebugMode:
            self.__write("DEBUG: %s" % message, log_level = 'debug')
        return
