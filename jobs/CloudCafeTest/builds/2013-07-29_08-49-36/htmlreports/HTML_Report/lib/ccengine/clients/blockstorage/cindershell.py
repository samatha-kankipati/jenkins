'''
@summary: Classes and Utilities that provide low level connectivity to the Nova Command Line Client
@note: Should be consumed/exposed by a a L{ccengine.providers} class and rarely be used directly by any other object or process 
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
import re
import os

from ccengine.common.tools import logging_tools
from ccengine.domain.compute.novashell import SEPARATOR, NovaShellResponse
from ccengine.common.connectors.commandline import CommandLineConnector, CommandLineResponse


class CinderShellClient(CommandLineConnector):
    '''
    @summary: Wrapper for driving/parsing the command line Nova Client Process.
    @ivar ClientLogger: This Client's logger instance.
    @type ClientLogger: L{PBLogger}
    @note: This class is dependent on a local installation of the Nova client process.
    '''
    def __init__(self, config=None):
        '''
        @param logger: PBLogger instance to use, Generates private logger if None
        @type logger: L{PBLogger}
        '''

        #CommandLineConnector.__init__(self, "cinder")
        super(CinderShellClient, self).__init__("cinder")
        self.client_log = logging_tools.getLogger(
                            logging_tools.get_object_namespace(self.__class__))

        '''@TODO:  Figure out where to put this chunk of logic so e can reuse
                   it anywhere we need to auto putenv environment vars'''

        #Setup environment variables
        if config is None:
            self.client_log.warning('empty (=None) config recieved in init')
        else:
            env_var = dir(config.cinder_shell)
            good_info = []
            for e in env_var:
                e_value = None
                '''
                @TODO: Having these magic strings here is bad.  We need
                       to define a constant that we put in front of ALL
                       env vars so we can have them all automagically
                       added.  Replace OS_ and NOVA with something like
                       CC_AUTOENV_ or something.
                '''
                if re.search('^OS_', e) or (re.search('^CINDER', e)):
                    e_value = getattr(config.cinder_shell, str(e))
                else:
                    continue

                self.client_log.debug('Found: %s' % e)
                if e_value is None:
                    self.client_log.warning('Environment variable %s is None. Most likely it is not defined in the current config file.' % e)
                else:
                    #Set the environment varibale
                    self.client_log.debug('setting os env var: %s=%s' % (str(e), str(e_value)))
                    os.putenv(str(e), str(e_value))

    def __send__(self, cmd, *args):

        '''
        @summary: Sends commands directly to Nova CMD line
        @param cmd: Command to sent to Nova CMD line
        @type cmd: C{str}
        @param args: Optional list of args to be passed with the command
        @type args: C{tuple} with C{list}
        @return: The response from the Nova Client
        @rtype:  L{NovaShellResponse} 
        @note: PRIVATE
        '''

        command_args = []
        response = CommandLineResponse()

        ''' Account for any arguments we may have received '''
        if (len(args) and len(args[0]) > 0):
            command_args = args[0]

        '''
        Save off the display command for the log files and build the final
        command that adds the custom parsing to the nova client output. This
        adds special CLI parsing to whack the extraneous data and give us a
        useable data structure from the prettytable returned by nova-client
        @todo: WARNING THIS IS *NIX DEPENDANT. It shouldn't be.
        '''
        if (len(command_args) > 0):
            display_command = "%s %s %s" % (self.base_command, cmd, command_args)
        else:
            display_command = "%s %s" % (self.base_command, cmd)

        try:
            ''' Strip out the pretty table formatting and replace with SEPARATOR '''
            command_args.append("| awk -F '|' '{$1=\"\"; OFS=\"%s\"; print $0;}'" % SEPARATOR)

            ''' Strip out spaces, blank lines, etc... '''
            command_args.append("| sed 's/ //g'|grep -v '^$'")

            ''' Handle empty columns by replacing with the string None '''
            command_args.append("| sed 's/^%(0)s//g'|sed 's/%(0)s%(0)s/%(0)sNone%(0)s/g'" % ({'0' : SEPARATOR}))

            ''' Whack any trailing SEPARATOR chars, this could cause false blank rows '''
            command_args.append("| sed 's/%s$//g'" % SEPARATOR)

        except Exception, parse_exception:
            response.ReturnCode = -1000
            response.StandardOut = "Exception Appending Nova Client Formatting to Arguments: %s" % parse_exception
            self.client_log.warning(response.StandardOut)

        try:
            ''' Run the Nova Command using the base classes send method '''
            response = CommandLineConnector.__send__(self, cmd, True, command_args)
            self.client_log.debug("STD OUT/ERR: %s" % response.StandardOut)
        except Exception, kill_exception:
            response.ReturnCode = -1001
            response.StandardOut = "Exception Executing Nova Process: %s" % kill_exception
            self.client_log.warning(response.StandardOut)

        try:
            ''' Report, also could eventually do something more useful '''
            if (response.ReturnCode > 0):
                self.client_log.warning("%s returned Error Code: %s" % (display_command, response.ReturnCode))
            elif (len(response.StandardOut) > 0) and ("Gkr-Message" in response.StandardOut[0].split("~")[0]):
                ''' This is a variant where a Gnome Keyring Error is returned '''
                new_std_out = []
                for line in response.StandardOut:
                    if('Gkr-Message' in line):
                        self.client_log.warning(line)
                    else:
                        new_std_out.append(line)
                response.StandardOut = new_std_out 
                self.client_log.info("%s completed Return Code: %s" % (display_command, response.ReturnCode))
            else:
                self.client_log.info("%s completed Return Code: %s" % (display_command, response.ReturnCode))
        except Exception, parse_exception:
            response.ReturnCode = -1001
            response.StandardOut = "Exception Parsing Nova Output: %s" % parse_exception

        ''' Pass the generated NovaShellResponse back '''
        return NovaShellResponse(response)

    def volume_list(self):
        '''
        @summary: List all the volumes.
        @rtype: L{NovaShellResponse}
        '''
        return(self.__send__("list", []))

    def volume_show(self, volume_name):
        '''
        @summary: List all the volumes.
        @rtype: L{NovaShellResponse}
        '''
        return(self.__send__("show %s" % volume_name, []))

    def volume_type_list(self):
        '''
        @summary: List all the available volume types.
        @rtype: L{NovaShellResponse}
        '''
        return(self.__send__('type-list', []))

    def volume_create(self, display_name=None, volume_type=None, volume_size=None, snapshot_id=None):
        '''
        @summary: Add a new volume.
        @param display_name: Volume Name.  
        @type display_name: C{str}
        @param volume_type: Volume Type ID, (see 'nova volume-type-list').  
        @type volume_type: C{str}
        @param volume_size: Size of volume in GB.  
        @type volume_size: C{str}
        @param snapshot_id: ID of a volume snapshot to create a backup from.
        @type snapshot_id: C{str}
        @rtype: L{NovaShellResponse}
        '''

        novaArgs = []
        novaCommand = "create"
        if (snapshot_id != None):
            novaArgs.append("--snapshot_id %s" % snapshot_id)

        if (display_name != None):
            novaArgs.append("--display_name %s" % display_name)
        ''' VOLUME SIZE MUST BE APPENDED LAST '''

        if (volume_type != None):
            novaArgs.append("--volume_type %s" % volume_type)
        ''' VOLUME SIZE MUST BE APPENDED LAST '''

        if (volume_size != None):
            novaArgs.append("%s" % volume_size)
        return(self.__send__("%s" % (novaCommand), novaArgs))

    def volume_delete(self, volume_id = None):
        '''
        @summary: Remove a volume.
        @param volume_id: ID of the volume to delete. 
        @type volume_id: C{str}
        @rtype: L{NovaShellResponse}
        '''
        novaArgs = []
        novaCommand = "delete"

        '''
        ALL of these commands are required, however, the commands could be
        used for a negative test case so the wrapper proc should expose the 
        ability to NOT pass them if disired.
        '''
        if (volume_id != None):
            novaArgs.append("'%s'" % volume_id)
        return(self.__send__("%s" % (novaCommand), novaArgs))

    def volume_snapshot_create(self, volume_id, force_create=False,
                                 display_name=None, display_description=None):
        '''
        @summary: Create a volume snapshot
        @param volume_id: ID of the volume to create a snapshot of.
        @type volume_id: C{str}
        @param force: Force volume snapshot create.
        @type force: C{bool}
        @param display_name: Display name of new volume snapshot.
        @type display_name: C{str}
        @param display_description: Display description of new volume snapshot.
        @type display_name: C{str}
        @rtype: L{NovaShellResponse}
        '''
        novaArgs = []
        novaCommand = "snapshot-create"

        if (volume_id != None):
            novaArgs.append("'%s'" % volume_id)
        if (force_create != False):
            novaArgs.append("--force '%s'" % force_create)
        if (display_name != None):
            novaArgs.append("--display_name '%s'" % display_name)
        if (display_description != None):
            novaArgs.append("--display_description '%s'" % display_description)
        return(self.__send__("%s" % (novaCommand), novaArgs))

    def volume_snapshot_delete(self, snapshot_id):
        '''
        @summary: Delete a volume snapshot
        @param snapshot_id: ID of the volume snapshot to delete.
        @type snapshot_id: C{str}
        @rtype: L{NovaShellResponse}
        '''
        novaArgs = []
        novaCommand = "snapshot-delete"

        if (snapshot_id != None):
            novaArgs.append("'%s'" % snapshot_id)

        return(self.__send__("%s" % (novaCommand), novaArgs))

    def volume_snapshot_list(self):
        '''
        @summary: List all snapshots
        @rtype: L{NovaShellResponse}
        '''
        novaCommand = "snapshot-list"
        return(self.__send__("%s" % (novaCommand), []))

    def volume_snapshot_show(self, snapshot_id):
        '''
        @summary: Show details about a volume snapshot
        @param snapshot_id: ID or Display Name of the volume snapshot to detail.
        @type snapshot_id: C{str}
        @rtype: L{NovaShellResponse}
        '''
        novaCommand = "snapshot-show %s"%str(snapshot_id)
        return(self.__send__("%s" % (novaCommand), []))
