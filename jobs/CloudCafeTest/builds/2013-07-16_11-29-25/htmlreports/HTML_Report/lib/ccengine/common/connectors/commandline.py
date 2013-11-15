'''
@summary: Classes and Utilities that provide low level connectivity to a Command Line Client
@note: Primarily intended to serve as base classes for a specific command line connector Class
@note: Should be consumed/exposed by a L{ccengine.persisters}, a L{ccengine.clients} or a L{ccengine.common.connectors} class,
should rarely be used directly by any other object or process 
@see: L{BaseCLIProcessConnector}
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
import sys
import subprocess

from ccengine.domain.commandline import CommandLineResponse
from ccengine.common.connectors.base_connector import BaseConnector


class CommandLineConnector(BaseConnector):
    '''
    @summary: Wrapper for driving/parsing a command line client like nova, git, apt-get, etc...
    @ivar base_command: This processes base command string. (I.E. nova or git)
    @type base_command: C{str}
    @note: This class is dependent on a local installation of the wrapped client process.
    '''
    def __init__(self, base_command=None):
        '''
        @param base_command: This processes base command string. (I.E. nova or git)
        @type base_command: C{str}
        '''
        super(CommandLineConnector, self).__init__()
        self.base_command = base_command

    def __send__(self,
                 cmd,
                 wait_for_process_to_be_complete=True,
                 *args):
        '''
        @summary: Sends a command directly to this instance's CMD line
        @param cmd: Command to sent to CMD line
        @type cmd: C{str}
        @param args: Optional list of args to be passed with the command
        @type args: C{list}
        @raise exception: If unable to close process after running the command
        @return: The full response details from the CMD line
        @rtype: L{CommandLineResponse} 
        @note: PRIVATE. Can be over-ridden in a child class
        '''
        os_process = None
        os_response = CommandLineResponse()

        ''' Process command we received '''
        os_response.Command = "%s %s" % (self.base_command, cmd)
        if (len(args) and len(args[0]) > 0):
            for arg in args[0]:
                os_response.Command += " %s" % (arg)

        ''' Run the Command. '''
        try:
            os_process = subprocess.Popen(os_response.Command, 
                                          stdout=subprocess.PIPE, 
                                          stderr=subprocess.STDOUT, 
                                          shell=True)
        except subprocess.CalledProcessError() as cpe:
            self.connector_log.exception("Exception running commandline command %s\n%s" % (str(os_response.Command), str(cpe)))
            #print "Exception running commandline command %s\n%s"%(str(os_response.Command), str(cpe))
        if not wait_for_process_to_be_complete:
            os_response.ReturnCode = os_process.returncode
            os_response.process_id = os_process.pid
            return os_response
        
        '''
        Wait for the process to complete and then read the lines.
        for some reason if you read each line as the process is running
        and use os_process.Poll() you don't always get all output
        '''
        stdOUT, stdERR = os_process.communicate()
        os_response.ReturnCode = os_process.returncode

        '''
        Pass the full output of the process_command back. It is important to not
        parse, strip or otherwise massage this output in the private send
        since a child class could override and contain actual command processing logic.
        '''
        os_response.StandardOut = stdOUT.splitlines()
        if stdERR is not None:
            os_response.StandardError = str(stdERR).splitlines()

        '''
        Un-comment to see the raw output in debug mode, this is  not needed
        often and can be horrifically verbose, even for debug output, so it 
        is implemented as a nasty print here in order to force a manual step 
        to get it to be output at all. 
        '''
#        print("BaseCLIProcessConnector.__send__ Args...: %s" % (args))
#        print("BaseCLIProcessConnector.__send__ Command: %s" % (os_response.Command))
#        print("BaseCLIProcessConnector.__send__ StandardOut...: %s" % (os_response.StandardOut))

        try:
            ''' Clean up the process to avoid any leakage/wonkiness with stdout/stderr '''
            os_process.kill()
        except OSError:
            ''' 
            An OS Error is valid if the process has exited. We only
            need to be concerned about other exceptions
            '''
            sys.exc_clear()
        except Exception, kill_exception:
            raise Exception("Exception forcing %s Process to close: %s" % (self.base_command, kill_exception))
        finally:
            del os_process
        return(os_response)
