'''
@summary: Classes and Utilities that provide low level connectivity to the
          Nova Command Line Client
@note: Should be consumed/exposed by a a L{ccengine.providers} class and rarely
       be used directly by any other object or process
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
import os
import re

from ccengine.common.tools import logging_tools
from ccengine.domain.compute.novashell import SEPARATOR, NovaShellResponse
from ccengine.common.connectors.commandline import CommandLineConnector,\
    CommandLineResponse


class NovaShellClient(CommandLineConnector):
    '''
    @summary: Wrapper for driving/parsing the command line Nova Client Process.
    @ivar ClientLogger: This Client's logger instance.
    @type ClientLogger: L{PBLogger}
    @note: This class is dependent on a local installation of the Nova client
           process.
    '''
    def __init__(self, os_env_dict):

        CommandLineConnector.__init__(self, "nova")
        self.client_log = logging_tools.getLogger(
                            logging_tools.get_object_namespace(self.__class__))
        #Set up OS Environment by exporting all env vars passed to client
        self.os_env_dict = os_env_dict
        for key, value in os_env_dict.items():
            self.client_log.debug('setting {0}={1}'.format(key, value))
            os.putenv(str(key), str(value))

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

        '''@TODO: Replace all the external calls to sed and awk with python
                  regular expressions, and move this logic to a domain object
        '''
        try:
            #Strip out the pretty table formatting and replace with SEPARATOR
            command_args.append("| awk -F '|' '{$1=\"\"; OFS=\"%s\"; print $0;}'" % SEPARATOR)

            #Strip out spaces, blank lines, etc...
            command_args.append("| sed 's/ //g'|grep -v '^$'")

            #Handle empty columns by replacing with the string None
            command_args.append("| sed 's/^%(0)s//g'|sed 's/%(0)s%(0)s/%(0)sNone%(0)s/g'" % ({'0' : SEPARATOR}))

            #Whack any trailing SEPARATOR chars, this could cause false blank rows
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

    def boot_server(self, server_name=None, flavor_id=None, image_id=None):
        '''
        @summary: Boot a new server
        @param server_name: Name for the new server  
        @type server_name: C{str}
        @param flavor_id: Flavor ID (see 'nova flavor-list').
        @type flavor_id: C{str}
        @param image_id: Image ID (see 'nova image-list').
        @type image_id: C{str}
        @param args: Optional arguments. (Omit to pass no additional arguments)
        @type args: C{list}
        '''
        novaArgs = []
        novaCommand = "boot"
        if (flavor_id != None):
            novaArgs.append("--flavor %s" % flavor_id)
        if (image_id != None):
            novaArgs.append("--image %s" % image_id)
        ''' SERVER NAME MUST BE APPENDED LAST '''
        if (server_name != None):
            novaArgs.append("%s" % server_name)
        return(self.__send__("%s" % (novaCommand), novaArgs))

    def delete_server(self, server_name=None):
        '''
        @summary: Immediately shut down and delete a server.
        @param server_name: Name or ID of the Server.
        @type server_name: C{str}
        @rtype: L{NovaShellResponse}
        '''
        novaArgs = []
        novaCommand = "delete"

        '''
        ALL of these commands are required, however, the commands could be
        used for a negative test case so the wrapper proc should expose the
        ability to NOT pass them if disired.
        '''
        if (server_name != None):
            novaArgs.append("'%s'" % server_name)
        return(self.__send__("%s" % (novaCommand), novaArgs))

    def list_server(self, server_name=None):
        '''
        @summary: Lists a specific server
        @param server_name: Server to list (See nova list --name)
        @type server_name: C{str}
        @note: Omit to return ALL servers (See nova list)
        @rtype: L{NovaShellResponse}
        '''
        novaArgs = []
        novaCommand = "list"
        ''' SERVER NAME MUST BE APPENDED LAST '''
        if (server_name != None):
            novaArgs.append("--name %s" % server_name)
        return(self.__send__(novaCommand, novaArgs))

    def flavor_list(self):
        '''
        @summary: List available server flavors
        @rtype: L{NovaShellResponse}
        '''
        return(self.__send__("flavor-list", []))

    def image_list(self):
        '''
        @summary: List available server images
        @rtype: L{NovaShellResponse}
        '''
        return(self.__send__("image-list", []))

    def volume_list(self):
        '''
        @summary: List all the volumes.
        @rtype: L{NovaShellResponse}
        '''
        return(self.__send__("volume-list", []))

    def volume_show(self, volume_name):
        '''
        @summary: List all the volumes.
        @rtype: L{NovaShellResponse}
        '''
        return(self.__send__("volume-show %s" % volume_name, []))

    def volume_type_list(self):
        '''
        @summary: List all the available volume types.
        @rtype: L{NovaShellResponse}
        '''
        return(self.__send__("volume-type-list", []))

    def volume_attach(self, server_name = None, volume_id = None, device_name = None):
        '''
        @summary: Attach a volume to a server.
        @param server_name: Name or ID of server.  
        @type server_name: C{str}
        @param volume_id: ID of the volume to attach. 
        @type volume_id: C{str}
        @param device_name: Name of the device e.g. /dev/vdb.  
        @type device_name: C{str}
        @rtype: L{NovaShellResponse}
        '''
        novaArgs = []
        novaCommand = "volume-attach"

        '''
        ALL of these commands are required, however, there commands could be
        used for a negative test case so the wrapper proc should expose the 
        ability to NOT pass them if disired.
        '''
        if (server_name != None):
            novaArgs.append("'%s'" % server_name)
        if (volume_id != None):
            novaArgs.append("'%s'" % volume_id)
        if (device_name != None):
            novaArgs.append("'%s'" % device_name)
        return(self.__send__("%s" % (novaCommand), novaArgs))

    def volume_create(self, display_name = None, volume_type = None, volume_size = None, snapshot_id = None):
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
        novaCommand = "volume-create"
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

    def volume_detach(self, server_name = None, volume_id = None):
        '''
        @summary: Detach a volume from a server.
        @param server_name: Name or ID of server.  
        @type server_name: C{str}
        @param volume_id: ID of the volume to detach. 
        @type volume_id: C{str}
        @rtype: L{NovaShellResponse}
        '''
        novaArgs = []
        novaCommand = "volume-detach"
        
        '''
        ALL of these commands are required, however, the commands could be
        used for a negative test case so the wrapper proc should expose the 
        ability to NOT pass them if disired.
        '''
        if (server_name != None):
            novaArgs.append("'%s'" % server_name)
        if (volume_id != None):
            novaArgs.append("'%s'" % volume_id)
        return(self.__send__("%s" % (novaCommand), novaArgs))
    
    def volume_delete(self, volume_id = None):
        '''
        @summary: Remove a volume.
        @param volume_id: ID of the volume to delete. 
        @type volume_id: C{str}
        @rtype: L{NovaShellResponse}
        '''
        novaArgs = []
        novaCommand = "volume-delete"
        
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
        novaCommand = "volume-snapshot-create"
        
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
        novaCommand = "volume-snapshot-delete"

        if (snapshot_id != None):
            novaArgs.append("'%s'" % snapshot_id)

        return(self.__send__("%s" % (novaCommand), novaArgs))

    def volume_snapshot_list(self):
        '''
        @summary: List all snapshots
        @rtype: L{NovaShellResponse}
        '''
        novaCommand = "volume-snapshot-list"
        return(self.__send__("%s" % (novaCommand), []))

    def volume_snapshot_show(self, snapshot_id):
        '''
        @summary: Show details about a volume snapshot
        @param snapshot_id: ID or Display Name of the volume snapshot to detail.
        @type snapshot_id: C{str}
        @rtype: L{NovaShellResponse}
        '''
        novaCommand = "volume-snapshot-show %s"%str(snapshot_id)
        return(self.__send__("%s" % (novaCommand), []))
