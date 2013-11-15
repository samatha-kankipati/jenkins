'''
@summary: Provider Module for the Compute Nova Shell Command Line Client
@note: Should be the primary interface to a test case or external tool.
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
import re
import sys
import time
import random
from socket import inet_aton
from ccengine.domain.types import NovaServerStatusTypes, \
                                          NovaVolumeStatusTypes, \
                                          NovaVolumeSnapshotStatusTypes
from ccengine.clients.compute.novashell import NovaShellClient
from ccengine.common.reporting.logging import PBLogger, DEBUG_MODE

class NovaShellProvider(object):
    '''
    @summary: Provides an interface to the Nova Command Line Shell Client
    @ivar ClientLogger: This Process' logger instance.
    @type ClientLogger: L{PBLogger}   
    @ivar NovaShellClient: This Process' Nova Shell Client Connection
    @type NovaShellClient: L{BaseCLIProcessConnector}   
    @note: This class is dependent on a local installation of the Nova client process.
    '''
    def __init__(self, logger=None):
        '''
        @param logger: PBLogger instance to use, Generates private logger if None
        @type logger: L{PBLogger}  
        '''
        if (logger == None):
            self.ClientLogger = PBLogger(fileName="%s.log" % ("%s" % (self.__class__.__name__)), 
                                         fileMode='a', 
                                         isDebugMode=DEBUG_MODE)
        else:
            self.ClientLogger = logger
        self.NovaShellClient = NovaShellClient(logger=self.ClientLogger)
     
    # NOTE(clayg): increased build timeout to 10 mins (seems high?)
    def create_server(self, server_name, flavor, image, timeout=600):
        '''
        @summary: Boot a new server, wait for it to return and report result
        @param server_name: server_name for the new server
        @type server_name: C{str}
        @param flavor: Flavor ID (see 'nova flavor-list').
        @type flavor: C{str}
        @param image: Image ID (see 'nova image-list').
        @type image: C{str}
        @param timeout: Wait time in seconds before time-out 
        @type timeout: C{int}
        @return: Valid record on success
        @rtype: C{dict}
        '''
        newServer = {}
        
        try:
            novaResponse = self.NovaShellClient.boot_server(server_name, flavor, image)
        except Exception, boot_exception:
            self.ClientLogger.logMessage("Exception booting server: %s: %s" % (server_name, boot_exception))

        if (novaResponse.IsEmpty == False and novaResponse.IsError == False):
            self.ClientLogger.logMessage("Server %s created, waiting for server to become active . . ." % server_name)
            waitResult = self.wait_for_server_status(server_name, NovaServerStatusTypes.ACTIVE, timeout, True)
            if (waitResult[0] == True):
                ''' Status was found within timeout '''
                newServer = waitResult[2]
            else:
                if (waitResult[1] == True):
                    self.ClientLogger.logMessage("Server %s was created but entered an error state before becoming active. Last Status was: %s" % (server_name, waitResult[2]["Status"]))
                elif (waitResult[2] != {}):
                    self.ClientLogger.logMessage("Server %s was created but timed-out before becoming active. Last Status was: %s" % (server_name, waitResult[2]["Status"]))
                else:
                    self.ClientLogger.logMessage("Server %s was created but never found in the system" % server_name)
        else:
            self.ClientLogger.logMessage("Boot server failed, nova returned:\n%s" % novaResponse)
        return(newServer)
    
    def delete_server(self, server_name, timeout=600):
        '''
        @summary: Delete a server, wait for it to delete and report result
        @param server_name: Display Name of the server to delete. (see 'nova server-list'). 
        @type server_name: C{str}
        @param timeout: Wait time in seconds before time-out 
        @type timeout: C{int}
        @return: True if deleted and removed.
        @rtype: C{bool}
        '''
        wasDeleted = False
        
        try:
            ''' Delete Server requires the ID of the server passed in, look it up first '''
            self.ClientLogger.logMessage("Loading Server %s . . ." % (server_name))
            server = self.get_server(server_name)
        except Exception, search_exception:
            self.ClientLogger.logMessage("Exception loading server: %s: %s" % (server_name, search_exception))

        if (server and server != {}):
            try:
                self.ClientLogger.logMessage("Deleting Server %s . . ." % (server_name))
                novaResponse = self.NovaShellClient.delete_server(server_name)
            except Exception, delete_exception:
                self.ClientLogger.logMessage("Exception deleting server: %s from server: %s: %s" % (server_name, delete_exception))
    
            if (novaResponse.IsEmpty == True and novaResponse.IsError == False):
                self.ClientLogger.logMessage("Server %s deleted, waiting for server to be removed . . ." % server_name)
                waitResult = self.wait_for_server_status(server_name, NovaServerStatusTypes.DELETING, timeout, True)
                if (waitResult[0] == True):
                    ''' Status was found within timeout '''
                    ''' @todo: add back in the final check for deleted '''
                    wasDeleted = True
                    self.ClientLogger.logMessage("Server %s was deleted." % server_name)
#                    if (self.get_server(server_name) == {}):
#                        wasDeleted = True
#                        self.ClientLogger.logMessage("Server %s was deleted." % server_name)
                else:
                    if (waitResult[1] == True):
                        self.ClientLogger.logMessage("Server %s was deleted but entered an error state before being removed. Last Status was: %s" % (server_name, waitResult[2]["Status"]))
                    elif (waitResult[2] != {}):
                        self.ClientLogger.logMessage("Server %s was deleted but timed-out before being removed. Last Status was: %s" % (server_name, waitResult[2]["Status"]))
                    else:
                        '''
                        The server actually vanished before/during the wait for status call,
                        It's acceptable to assume that the delete was successful
                        ''' 
                        wasDeleted = True
                        self.ClientLogger.logMessage("Server %s was deleted." % server_name)
            else:
                self.ClientLogger.logMessage("Delete server failed, nova returned:\n%s" % novaResponse)
        else:
            self.ClientLogger.logMessage("Un-able to locate server: %s" % server_name)
        return(wasDeleted)

    def delete_all_servers(self, server_name_pattern):
        '''
        @summary: Returns the specified server
        @param server_name_pattern: Pattern used to match server. (I.E. Apollo would delete all servers that contain the name Apollo)
        @type server_name_pattern: C{str} 
        @return: Count of servers found and count of servers deleted.
        @rtype: C{tuple}(C{int}, C{int})
        '''
        foundCount = 0
        deletedCount = 0
        novaResponse = None
        try:
            novaResponse = self.NovaShellClient.list_server()
            if (novaResponse.IsEmpty == False and novaResponse.IsError == False):
                self.ClientLogger.logMessage("Searching for pattern %s" % server_name_pattern)
                for row in novaResponse.yield_rows():
                    if(row["Name"].find(server_name_pattern) > -1):
                        self.ClientLogger.logMessage("Found %s . . ." % row["Name"])
                        foundCount += 1
                        if (self.delete_server(row["Name"], 10) == True):
                            deletedCount += 1
            elif (novaResponse.IsError == True):
                self.ClientLogger.logMessage("Error retrieving server list, nova returned:\n%s" % novaResponse)
            else:
                self.ClientLogger.logMessage("No Servers Found.")
        except Exception, server_exception:
            self.ClientLogger.logMessage("Exception searching for server: %s: %s" % (server_name_pattern, server_exception))
        return(foundCount, deletedCount)
    
    def attach_volume(self, server_name, volume_name, device_name, timeout=600):
        '''
        @summary: Attach a volume to a server, wait for it to attach and report result
        @param server_name: Name or ID of server. (see 'nova list').
        @type server_name: C{str}
        @param volume_name: Display Name of the volume to attach. (see 'nova volume-list'). 
        @type volume_name: C{str}
        @param device_name: Name of the attached device e.g. /dev/vdb.  
        @type device_name: C{str}
        @param timeout: Wait time in seconds before time-out 
        @type timeout: C{int}
        @return: Valid record on success
        @rtype: C{dict}
        '''
        attachedVolume = {}
        volume = {}
        
        try:
            ''' Attach Volume requires the ID of the volume passed in, look it up first '''
            self.ClientLogger.logMessage("Searching for Volume %s . . ." % (volume_name))
            volume = self.get_volume(volume_name)
        except Exception, search_exception:
            self.ClientLogger.logMessage("Exception locating volume: %s: %s" % (volume_name, str(search_exception)))

        if (volume and volume != {}):
            try:
                novaResponse = self.NovaShellClient.volume_attach(server_name, volume["ID"], device_name)
            except Exception, attach_exception:
                self.ClientLogger.logMessage("Exception attaching volume: %s to server: %s with device name %s: %s" % (str(volume_name), str(server_name), str(device_name), str(attach_exception)))
    
            if not novaResponse.IsError:
                self.ClientLogger.logMessage("Volume %s created, waiting for volume to become in use . . ." % volume_name)
                isStatusFound, isErrorFound, lastStatus  = self.wait_for_volume_status(volume_name, NovaVolumeStatusTypes.IN_USE, timeout, True)
                if (isStatusFound == True):
                    ''' Status was found within timeout '''
                    try:
                        ''' Attach Volume requires the ID of the volume passed in, look it up first '''
                        self.ClientLogger.logMessage("Searching for Volume %s . . ." % (volume_name))
                        attachedVolume = self.get_volume(volume_name)
                    except Exception, search_exception:
                        self.ClientLogger.logMessage("Exception locating volume: %s: %s" % (volume_name, str(search_exception)))
                else:
                    if (isErrorFound == True):
                        self.ClientLogger.logMessage("Volume %s was attached but entered an error state before becoming in use. Last Status was: %s" % (volume_name, lastStatus))
                    elif (isStatusFound == False):
                        self.ClientLogger.logMessage("Volume %s was attached but timed-out before becoming in use. Last Status was: %s" % (volume_name, lastStatus))
                    else:
                        self.ClientLogger.logMessage("Volume %s was last status was %s, final status %s was not seen." % volume_name)
            else:
                self.ClientLogger.logMessage("Attach volume failed, nova returned:\n%s" % novaResponse)
        else:
            self.ClientLogger.logMessage("Un-able to locate volume: %s" % volume_name)
        
        return attachedVolume

    def create_volume(self, volume_name, volume_type, volume_size, timeout=600):
        '''
        @summary: Boot a new volume, wait for it to return and report result
        @param volume_name: Name for the new volume (Display Name)
        @type volume_name: C{str}
        @param volume_type: Volume Type ID, (see 'nova volume-type-list').  
        @type volume_type: C{str}
        @param volume_size: Size of volume in GB
        @type volume_size: C{int}
        @param timeout: Wait time in seconds before time-out 
        @type timeout: C{int}
        @return: Valid record on success
        @rtype: C{dict}
        '''
        newVolume = {}
        
        try:
            novaResponse = self.NovaShellClient.volume_create(volume_name, volume_type, volume_size)
        except Exception, create_exception:
            self.ClientLogger.logMessage("Exception creating volume: %s: %s" % (volume_name, create_exception))

        if (novaResponse.IsError == False):
            self.ClientLogger.logMessage("Volume %s created, waiting for volume to become available . . ." % volume_name)
            isStatusFound, isErrorFound, lastStatus = self.wait_for_volume_status(volume_name, NovaVolumeStatusTypes.AVAILABLE, timeout, True)
            if (isStatusFound == True):
                newVolume = self.get_volume(volume_name)
                self.ClientLogger.logMessage("Volume %s created, waiting for volume to become available . . ." % volume_name)
            else:
                if (isErrorFound == True):
                    self.ClientLogger.logMessage("Volume %s was created but entered an error state before becoming active. Last Status was: %s" % (volume_name, lastStatus))
                elif (lastStatus != ""):
                    self.ClientLogger.logMessage("Volume %s was created but timed-out before becoming active. Last Status was: %s" % (volume_name, lastStatus))
                else:
                    self.ClientLogger.logMessage("Volume %s was created but never found in the system" % volume_name)
        else:
            self.ClientLogger.logMessage("Create volume failed, nova returned:\n%s" % novaResponse)
        return(newVolume)

    def create_volume_from_snapshot(self, volume_name, volume_snapshot_id, volume_type = None, timeout=600):
        '''
        @summary: Create a new volume from a snapshot, wait for it to return and report result
        @param volume_name: Name for the new volume (Display Name)
        @type volume_name: C{str}
        @param volume_snapshot_id: Volume Snapshot ID, (see 'nova volume-snapshot-list').  
        @type volume_snapshot_id: C{str}
        @param volume_type: Volume Type ID, (see 'nova volume-type-list').  
        @type volume_type: C{str}
        @param timeout: Wait time in seconds before time-out 
        @type timeout: C{int}
        @return: Valid record on success
        @rtype: C{dict}
        '''        
        #Send volume-size = 1, lunr will correct it on the back end.
        newVolume = {}
        
        try:
            novaResponse = self.NovaShellClient.volume_create(display_name = volume_name, volume_type = volume_type, volume_size = 1, snapshot_id = volume_snapshot_id)
        except Exception, create_exception:
            self.ClientLogger.logMessage("Exception creating volume %s from snapshot %s of type %s: %s" % (volume_name, volume_snapshot_id, volume_type, create_exception))

        if (novaResponse.IsError == False):
            self.ClientLogger.logMessage("Volume %s created, waiting for volume to become available . . ." % volume_name)
            isStatusFound, isErrorFound, lastStatus = self.wait_for_volume_status(volume_name, NovaVolumeStatusTypes.AVAILABLE, timeout, True)
            if (isStatusFound == True):
                newVolume = self.get_volume(volume_name)
                self.ClientLogger.logMessage("Volume %s created, waiting for volume to become available . . ." % volume_name)
            else:
                if (isErrorFound == True):
                    self.ClientLogger.logMessage("Volume %s was created but entered an error state before becoming active. Last Status was: %s" % (volume_name, lastStatus))
                elif (lastStatus != ""):
                    self.ClientLogger.logMessage("Volume %s was created but timed-out before becoming active. Last Status was: %s" % (volume_name, lastStatus))
                else:
                    self.ClientLogger.logMessage("Volume %s was created but never found in the system" % volume_name)
        else:
            self.ClientLogger.logMessage("Create volume failed, nova returned:\n%s" % novaResponse)
        return(newVolume)
    
    def delete_volume(self, volume_name, timeout=600):
        '''
        @summary: Delete a volume, wait for it to delete and be removed and report result
        @param volume_name: Display Name of the volume to delete. (see 'nova volume-list'). 
        @type volume_name: C{str}
        @param timeout: Wait time in seconds before time-out 
        @type timeout: C{int}
        @return: True if deleted and removed
        @rtype: C{bool}
        '''
        wasDeleted = False

        try:
            ''' Delete Volume requires the ID of the volume passed in, look it up first '''
            self.ClientLogger.logMessage("Searching for Volume %s . . ." % (volume_name))
            volume = self.get_volume(volume_name)
        except Exception, search_exception:
            self.ClientLogger.logMessage("Exception locating volume: %s: %s" % (volume_name, search_exception))

        if (volume is None) or (volume == {}):
            self.ClientLogger.logMessage("Error locating volume: %s: %s" % (volume_name))
            return False

        #Delete Volume
        try:
            self.ClientLogger.logMessage("Deleting Volume %s . . ." % (volume_name))
            novaResponse = self.NovaShellClient.volume_delete(volume["ID"])
        except Exception, delete_exception:
            self.ClientLogger.logMessage("Exception deleting volume: %s from server: %s: %s" % (volume_name, delete_exception))
    
        #Wait for the 'Deleting' Status at least
        status = None
        timeout = time.time() + 30
        while time.time() < timeout:
            try:
                status = self.get_volume_status(volume_name)
                if status == '':
                    status = 'GONE'
            except Exception as e:
                status = 'UNKNOWN_EXCEPTION'
                pass

            if status == NovaVolumeStatusTypes.DELETING:
                ''' Volume is in deleting state, see if it finishes withing timeout'''
                continue

            elif status is not None:
                timeout = time.time() - 10
                break

        #Check final volume status
        wasDeleted = False
        if (status == NovaVolumeStatusTypes.DELETING):
            ''' Did not finish deleting before timeout '''
            self.ClientLogger.logMessage("Volume %s is in DELETING state." % volume_name)

        elif (status == NovaVolumeStatusTypes.ERROR) or (status == NovaVolumeStatusTypes.ERROR_DELETING):
            ''' Volume ended up in either an ERROR or ERROR DELETING state'''
            self.ClientLogger.logError("Volume did not delete, current status: %s" % str(status))

        elif (status == 'GONE'):
            ''' Volume dissapeard and is presumed deleted'''
            self.ClientLogger.logMessage("Volume is GONE and presumed DELETED")
            wasDeleted = True

        elif (status == 'UNKNOWN_EXCEPTION'):
            self.ClientLogger.logError("An unexpected exception occurred, volume status is unknown")

        elif (status is None) or (status == {}):
            self.ClientLogger.logError("Volume status was not found, and is unknown")

        return(wasDeleted)

    def delete_all_volumes(self, volume_name_pattern):
        '''
        @summary: Returns the specified volume
        @param volume_name_pattern: Pattern used to match volume. (I.E. Apollo would delete all volumes that contain the name Apollo)
        @type volume_name_pattern: C{str} 
        @return: Count of volumes found and count of volumes deleted.
        @rtype: C{tuple}(C{int}, C{int})
        '''
        foundCount = 0
        deletedCount = 0
        novaResponse = None
        try:
            novaResponse = self.NovaShellClient.volume_list()
            if (novaResponse.IsEmpty == False and novaResponse.IsError == False):
                self.ClientLogger.logMessage("Searching for pattern %s" % volume_name_pattern)
                for row in novaResponse.yield_rows():
                    if(row["DisplayName"].find(volume_name_pattern) > -1):
                        self.ClientLogger.logMessage("Found %s . . ." % row["DisplayName"])
                        foundCount += 1
                        if (self.delete_volume(row["DisplayName"], 10) == True):
                            deletedCount += 1
            elif (novaResponse.IsError == True):
                self.ClientLogger.logMessage("Error retrieving volume list, nova returned:\n%s" % novaResponse)
            else:
                self.ClientLogger.logMessage("No Volumes Found.")
        except Exception, volume_exception:
            self.ClientLogger.logMessage("Exception searching for volume: %s: %s" % (volume_name_pattern, volume_exception))
        return(foundCount, deletedCount)
    
    def detach_volume(self, server_name, volume_name, timeout=600):
        '''
        @summary: Detach a volume from a server, wait for it to detach and report result
        @param server_name: Name or ID of server. (see 'nova list').
        @type server_name: C{str}
        @param volume_name: Display Name of the volume to detach. (see 'nova volume-list'). 
        @type volume_name: C{str}
        @param timeout: Wait time in seconds before time-out 
        @type timeout: C{int}
        @return: Valid record on success
        @rtype: C{dict}
        '''
        detachedVolume = {}
        
        try:
            ''' Detach Volume requires the ID of the volume passed in, look it up first '''
            self.ClientLogger.logMessage("Searching for Volume %s . . ." % (volume_name))
            volume = self.get_volume(volume_name)
        except Exception, search_exception:
            self.ClientLogger.logMessage("Exception locating volume: %s: %s" % (volume_name, search_exception))

        if (volume and volume != {}):
            try:
                novaResponse = self.NovaShellClient.volume_detach(server_name, volume["ID"])
            except Exception, detach_exception:
                self.ClientLogger.logMessage("Exception detaching volume: %s from server: %s: %s" % (volume_name, server_name, detach_exception))
    
            if (novaResponse.IsEmpty == True and novaResponse.IsError == False):
                self.ClientLogger.logMessage("Volume %s detached, waiting for volume to become available . . ." % volume_name)
                isStatusFound, isErrorFound, lastStatus  = self.wait_for_volume_status(volume_name, NovaVolumeStatusTypes.AVAILABLE, timeout, True)
                if (isStatusFound == True):
                    ''' Status was found within timeout '''
                    detachedVolume = self.get_volume(volume_name)
                else:
                    if (isErrorFound == True):
                        self.ClientLogger.logMessage("Volume %s was detached but entered an error state before becoming in use. Last Status was: %s" % (volume_name, lastStatus))
                    elif (lastStatus == NovaVolumeStatusTypes.AVAILABLE):
                        self.ClientLogger.logMessage("Volume %s was detached but timed-out before becoming available. Last Status was: %s" % (volume_name, lastStatus))
                    else:
                        self.ClientLogger.logMessage("Volume %s was detached but could not be found in the system" % volume_name)
            else:
                self.ClientLogger.logMessage("Detach volume failed, nova returned:\n%s" % novaResponse)
        else:
            self.ClientLogger.logMessage("Un-able to locate volume: %s" % volume_name)
        return(detachedVolume)

    def get_server(self, server_name=""):
        '''
        @summary: Returns the specified server
        @param server_name: Name of the server 
        @type server_name: C{str} 
        @return: Valid record on success
        @rtype: C{dict}
        '''
        server = {}
        novaResponse = None
        if (server_name != ""):
            try:
                novaResponse = self.NovaShellClient.list_server(server_name)
                if (novaResponse.IsEmpty == False and novaResponse.IsError == False):
                    server = novaResponse.get_row(0)
                elif (novaResponse.IsError == True):
                    self.ClientLogger.logMessage("Error retrieving server, nova returned:\n%s" % novaResponse)
                else:
                    self.ClientLogger.logMessage("Server Not Found.")
            except Exception, server_exception:
                server = {}
                self.ClientLogger.logMessage("Exception searching for server: %s: %s" % (server_name, server_exception))
        return(server)
    
    def get_image_list(self):
        '''
        @summary: Returns the list of all images
        @return: List of valid records on success
        @rtype: C{list} of C{dict}
        '''
        volumeList = []
        novaResponse = None
        try:
            novaResponse = self.NovaShellClient.image_list()
            if (novaResponse.IsEmpty == False and novaResponse.IsError == False):
                '''
                Need to first check if this is a hacker-jack environment
                @todo: This REALLY needs to be a better choice of random flavor
                '''
                volumeList = novaResponse.rows
            elif (novaResponse.IsError == True):
                self.ClientLogger.logMessage("Image list is invalid, nova returned:\n%s" % novaResponse)
            else:
                self.ClientLogger.logMessage("No Images found.")
        except Exception, image_exception:
            volumeList = []
            self.ClientLogger.logMessage("Exception processing Image list: %s" % image_exception)
        return(volumeList)

    def get_flavor_list(self):
        '''
        @summary: Returns the list of all flavors
        @return: List of valid records on success
        @rtype: C{list} of C{dict}
        '''
        flavorList = []
        novaResponse = None
        try:
            novaResponse = self.NovaShellClient.flavor_list()
            if (novaResponse.IsEmpty == False and novaResponse.IsError == False):
                '''
                Need to first check if this is a hacker-jack environment
                @todo: This REALLY needs to be a better choice of random flavor
                '''
                flavorList = novaResponse.rows
            elif (novaResponse.IsError == True):
                self.ClientLogger.logMessage("Flavor list is invalid, nova returned:\n%s" % novaResponse)
            else:
                self.ClientLogger.logMessage("No Flavors found.")
        except Exception, image_exception:
            flavorList = []
            self.ClientLogger.logMessage("Exception processing Flavor list: %s" % image_exception)
        return(flavorList)

    def get_volume(self, volume_name = ""):
        '''
        @summary: Returns the specified volume
        @param volume_name: Name of the volume 
        @type volume_name: C{str} 
        @return: Valid record on success
        @rtype: C{dict}
        '''
        volume = {}
        novaResponse = None
        if (volume_name != ""):
            try:
                novaResponse = self.NovaShellClient.volume_list()
                if (novaResponse.IsEmpty == False and novaResponse.IsError == False):
                    volume = novaResponse.find_row("Display Name", volume_name)
                elif (novaResponse.IsError == True):
                    self.ClientLogger.logMessage("Error retrieving volume, nova returned:\n%s" % novaResponse)
                else:
                    self.ClientLogger.logMessage("volume Not Found.")
            except Exception, volume_exception:
                self.ClientLogger.logMessage("Exception searching for volume: %s: %s" % (volume_name, volume_exception))
        return(volume)
        
    def _get_volume_property(self, volume_name, property_name):
        '''
        @summary: Returns the specified volume property 
        @param volume_name: Name of the volume
        @type volume_name: C{str}
        @param property_name: Name of the volume property
        @type property_name: C{str}         
        @return: Valid record on success
        @rtype: C{dict}
        '''        
        property_value = ""
        novaResponse = None
        if (volume_name != ""):
            try:
                novaResponse = self.NovaShellClient.volume_show(volume_name)
                if (novaResponse.IsEmpty == False and novaResponse.IsError == False):
                    volume_info = novaResponse.find_row("Property", property_name)
                    property_value = volume_info['Value']
                elif (novaResponse.IsError == True):
                    self.ClientLogger.logMessage("Error retrieving volume, nova returned:\n%s" % novaResponse)
                else:
                    self.ClientLogger.logMessage("volume Not Found.")
            except Exception as volume_exception:
                self.ClientLogger.logMessage("Exception searching for volume: %s: %s" % (volume_name, volume_exception))
                raise volume_exception

        return property_value
        
    def get_volume_id(self, volume_name = ""):
        '''
        @summary: Returns the specified volume
        @param volume_name: Name of the volume 
        @type volume_name: C{str} 
        @return: Valid record on success
        @rtype: C{dict}
        '''
        return self._get_volume_property(volume_name, 'id')
        
    def get_volume_status(self, volume_name = ""):
        '''
        @summary: Returns the specified volume
        @param volume_name: Name of the volume 
        @type volume_name: C{str} 
        @return: Valid record on success
        @rtype: C{dict}
        '''
        return self._get_volume_property(volume_name, 'status')
        
    def get_volume_type(self, volume_name = ""):
        '''
        @summary: Returns the specified volume
        @param volume_name: Name of the volume 
        @type volume_name: C{str} 
        @return: Valid record on success
        @rtype: C{dict}
        '''
        return self._get_volume_property(volume_name, 'volume_type')
        
    def get_volume_snapshot(self, snapshot_name = ""):
        '''
        @summary: Returns the specified volume snapshot
        @param snapshot_name: Name of the volume snapshot
        @type snapshot_name: C{str}
        @return: Valid record on success
        @rtype: C{dict}
        '''
        volume_snapshot = {}
        novaResponse = None
        if snapshot_name:
            try:
                novaResponse = self.NovaShellClient.volume_snapshot_list()
                if (novaResponse.IsEmpty == False and novaResponse.IsError == False):
                    volume_snapshot = novaResponse.find_row("Display Name", snapshot_name)
                elif (novaResponse.IsError == True):
                    self.ClientLogger.logMessage("Error retrieving volume snapshot, nova returned:\n%s" % novaResponse)
                else:
                    self.ClientLogger.logMessage("Snapshot %s Not Found." % snapshot_name)
            except Exception, volume_exception:
                volume_snapshot = {}
                self.ClientLogger.logMessage("Exception searching for snapshot: %s: %s" % (snapshot_name, volume_exception))
        
        return(volume_snapshot)
        
    def get_volume_snapshot_info(self, snapshot_id):
        '''
        @summary: Returns the specified volume snapshot
        @param snapshot_id: Name of the volume snapshot
        @type snapshot_id: C{str} 
        @return: Valid record on success
        @rtype: C{dict}
        '''
        volume_snapshot_info = {}
        novaResponse = None
        try:
            novaResponse = self.NovaShellClient.volume_snapshot_show(snapshot_id)
            if (novaResponse.IsEmpty == False and novaResponse.IsError == False):
                return novaResponse
            elif (novaResponse.IsError == True):
                self.ClientLogger.logMessage("Error retrieving volume snapshot info, nova returned:\n%s" % novaResponse)
                return False
            else:
                self.ClientLogger.logMessage("volume snapshot Not Found.")
        except Exception, snapshot_info_exception:
            volume_snapshot = {}
            self.ClientLogger.logMessage("Exception getting info for snapshot %s: %s" % (snapshot_id, snapshot_info_exception))
        
        return novaResponse
    
    def get_volume_snapshot_id(self, snapshot_name):
        novaResponse = self.get_volume_snapshot_info(snapshot_name)
        r = novaResponse.find_row('Property', 'id')
        return r['Value']          

    def select_test_image(self):
        '''
        @summary: Returns a specific smoke test valid image
        @return: Random valid image record
        @rtype: C{dict}
        '''
        returnImage = {}
        novaResponse = None
        try:
            novaResponse = self.NovaShellClient.image_list()
            if (novaResponse.IsEmpty == False and novaResponse.IsError == False):
                '''
                Need to first check if this is a hacker-jack environment
                @todo: This REALLY needs to be a better choice of return image
                '''
                testRow = novaResponse.find_row("Name", "oneiric_ami")
                if (testRow != {}):
                    ''' This is a hacker-jack environment, take this one specifically '''
                    self.ClientLogger.logDebug("Detected Hacker-Jack Environment . . .")
                    returnImage = testRow
                else:
                    ''' This is a huddle environment, hard-code it '''
                    testRow = novaResponse.find_row("Name", "Ubuntu12.04LTS(PrecisePangolin)")
                    returnImage = testRow
                    #returnImage = {'Status': 'ACTIVE', 'Server': 'None', 'ID': '0790c8c7-1bbe-470c-9403-88883982b5fb', 'Name': 'CentOS 6.0'}
            elif (novaResponse.IsError == True):
                self.ClientLogger.logMessage("Image list is invalid, nova returned:\n%s" % novaResponse)
            else:
                self.ClientLogger.logMessage("No Image found.")
        except Exception, image_exception:
            returnImage = {}
            self.ClientLogger.logMessage("Exception parsing Image list: %s" % image_exception)
        return(returnImage)
    
    def select_test_flavor(self):
        '''
        @summary: Returns a specific smoke test valid flavor
        @return: Random valid image record
        @rtype: C{dict}
        '''
        returnFlavor = {}
        novaResponse = None

        try:
            novaResponse = self.NovaShellClient.flavor_list()
            if (novaResponse.IsEmpty == False and novaResponse.IsError == False):
                '''
                Need to first check if this is a hacker-jack environment
                @todo: This REALLY needs to be a better choice of return flavor
                '''
                testRow = novaResponse.find_row("Name", "m1.tiny") 
                if (testRow != {}):
                    ''' This is a hacker-jack environment '''
                    self.ClientLogger.logDebug("Detected Hacker-Jack Environment . . .")
                    returnFlavor = testRow
                else:
                    ''' This is a huddle environment, hard-code it '''
                    testRow = novaResponse.find_row("Name", "512", contains_match=True)
                    returnFlavor = testRow
                    #returnFlavor = {'Name': '512MB instance', 'Ephemeral': 'N/A', 'Memory_MB': '512', 'VCPUs': '4', 'Swap': '1024', 'RXTX_Factor': '2.0', 'Disk': '20', 'ID': '2'}
            elif (novaResponse.IsError == True):
                self.ClientLogger.logMessage("Flavor list is invalid, nova returned:\n%s" % novaResponse)
            else:
                self.ClientLogger.logMessage("No Flavor found.")
        except Exception, flavor_exception:
            returnFlavor = {}
            self.ClientLogger.logMessage("Exception parsing Flavor list: %s" % flavor_exception)
        return(returnFlavor)

    def select_random_flavor(self):
        '''
        @summary: Returns a random valid flavor
        @return: Random valid flavor record
        @rtype: C{dict}
        '''
        minRow = 0
        maxRow = 0
        randomFlavor = {}
        novaResponse = None

        try:
            novaResponse = self.NovaShellClient.flavor_list()
            if (novaResponse.IsEmpty == False and novaResponse.IsError == False):
                '''
                Need to first check if this is a hacker-jack environment
                @todo: This REALLY needs to be a better choice of random flavor
                '''
                if (novaResponse.find_row("Name", "m1.tiny") != {}):
                    ''' This is a hacker-jack environment, force the range '''
                    self.ClientLogger.logDebug("Detected Hacker-Jack Environment . . .")
                    minRow = 1
                    maxRow = 2
                else:
                    ''' This is a huddle environment, pick anything '''
                    minRow = 0
                    maxRow = (len(novaResponse.rows) - 1)
                    
                ''' random.choice can not be used here because of novaResponse.rows format '''
                randomFlavor = novaResponse.get_row(random.randint(minRow, maxRow))
            elif (novaResponse.IsError == True):
                self.ClientLogger.logMessage("Flavor list is invalid, nova returned:\n%s" % novaResponse)
            else:
                self.ClientLogger.logMessage("No Flavor found.")
        except Exception, flavor_exception:
            randomFlavor = {}
            self.ClientLogger.logMessage("Exception parsing Flavor list: %s" % flavor_exception)
        return(randomFlavor)
    
    def select_random_image(self):
        '''
        @summary: Returns a random valid image
        @return: Random valid image record
        @rtype: C{dict}
        '''
        randomImage = {}
        novaResponse = None
        try:
            novaResponse = self.NovaShellClient.image_list()
            if (novaResponse.IsEmpty == False and novaResponse.IsError == False):
                '''
                Need to first check if this is a hacker-jack environment
                @todo: This REALLY needs to be a better choice of random flavor
                '''
                if (novaResponse.find_row("Name", "oneiric_ami") != {}):
                    ''' This is a hacker-jack environment, force the range '''
                    self.ClientLogger.logDebug("Detected Hacker-Jack Environment . . .")
                    randomImage = novaResponse.find_row("Name", "oneiric_ami")
                else:
                    ''' This is a huddle environment, pick anything '''
                    ''' random.choice can not be used here because of novaResponse.rows format '''
                    randomImage = novaResponse.get_row(random.randint(0, (len(novaResponse.rows) - 1)))
            elif (novaResponse.IsError == True):
                self.ClientLogger.logMessage("Image list is invalid, nova returned:\n%s" % novaResponse)
            else:
                self.ClientLogger.logMessage("No Image found.")
        except Exception, image_exception:
            randomImage = {}
            self.ClientLogger.logMessage("Exception parsing Image list: %s" % image_exception)
        return(randomImage)
    
    def select_random_volume_type(self):
        '''
        @summary: Returns a random valid volume type
        @return: Random valid volume type record
        @rtype: C{dict}
        '''
        randomVolumeType = {}
        novaResponse = None
        try:
            novaResponse = self.NovaShellClient.volume_type_list()
            if (novaResponse.IsEmpty == False and novaResponse.IsError == False):
                '''
                Need to first check if this is a hacker-jack environment
                @todo: This REALLY needs to be a better choice of random flavor
                '''
                if (novaResponse.find_row("Name", "vtype") != {}):
                    ''' This is a hacker-jack environment, force the range '''
                    self.ClientLogger.logDebug("Detected Hacker-Jack Environment . . .")
                    randomVolumeType = novaResponse.find_row("Name", "vtype")
                else:
                    ''' This is a huddle environment, pick anything '''
                    ''' random.choice can not be used here because of novaResponse.rows format '''
#                    randomVolumeType = novaResponse.get_row(random.randint(0, (len(novaResponse.rows) - 1)))
                    randomVolumeType = novaResponse.get_row(random.randint(0, 1))
            elif (novaResponse.IsError == True):
                self.ClientLogger.logMessage("Volume Type List is invalid, nova returned:\n%s" % novaResponse)
            else:
                self.ClientLogger.logMessage("No Volume Types found.")
        except Exception, parse_exception:
            randomVolumeType = {}
            self.ClientLogger.logMessage("Exception parsing Volume Type list: %s" % parse_exception)
        return(randomVolumeType)
    
    def validate_server(self, server_record):
        '''
        @summary: Validates that a server exists
        @param server_record: Server record used for validation
        @type server_record: c{dict}
        @todo: Find a better home for validators that are related to but don't belong directly to the Nova Client Proc 
        @return: True if server is valid
        @rtype: C{bool}
        '''
        isValid = False

        '''
        This parsing is based on the table that is returned from the nova client. The example below 
        is the current as of 05/07/2012:         
        Networks: 'public=2001:4801:7808:0052:5f4a:d80e:ff00:002c,50.57.94.4;private=10.182.64.39'
        '''
        public_ipv4_address = None
        ''' @todo: Move the get server public IP to a better global class '''
        addr_strings = server_record["Networks"].split(";")
        for tmp in addr_strings:
            if re.search('public=', tmp):
                addresses = tmp.split(',')
                for address in addresses:
                    address = address.replace('public=','')
                    try:
                        sys.stdout.flush()
                        inet_aton(address)
                    except Exception:
                        sys.exc_clear()
                    else:
                        public_ipv4_address = address
                        break
        self.ClientLogger.logDebug("Public_ipv4_address: %s" % (str(public_ipv4_address)))
        
        try:
            '''
            @todo: REPLACE THE PING VALIDATOR WITH A REAL ONE
            Adjusted to do 10 100 ms pings, this seems to be the sweet spot for detection.
            '''
            isValid = True
#            pingProc = subprocess.Popen("ping -w 10 %s" % public_ipv4_address,
#                                        stdout=subprocess.PIPE, 
#                                        stderr=subprocess.STDOUT, 
#                                        shell=True)
#            pingProc.wait()
#            for line in pingProc.stdout.readlines():
#                if "100% packet loss" in line:
#                    isValid = False
#                    break
#                else:
#                    isValid = True
        except Exception, validate_exception:
            self.ClientLogger.logMessage("Exception validating server: %s: %s" % (server_record, validate_exception))
        return(isValid)


    def wait_for_server_status(self, server_name, status, timeout=600, stop_on_error=False):
        '''
        @summary: Waits for a server to enter a specific status
        @param server_name: Name of the server 
        @type server_name: C{str} 
        @param staus: Server status to expect
        @type status: L{NovaServerStatusTypes}
        @param timeout: Wait time in seconds before time-out 
        @type timeout: C{int}
        @param stop_on_error: Stops if server enters error status (Only if not waiting on error) 
        @type stop_on_error: C{bool}
        @return: Tuple with True/False for status found, error found and the valid or empty record if server is/is not found
        @rtype: C{Tuple} [True/False, True/False, server dictionary]
        '''
        isStatusFound = False
        isErrorFound = False
        timedOut = time.time() + timeout
        server = {}
        
        ''' @todo: Make this wait process more generic and robust '''
        while time.time() < timedOut:
            try:
                server = self.get_server(server_name)
                if (server != {}):
                    self.ClientLogger.logDebug("Waiting for Server %s Status %s, current Status is %s . . ." % (server_name, status, server["Status"]))
                    if (server["Status"] == status):
                        isStatusFound = True
                        break
                    elif (server["Status"] == NovaServerStatusTypes.ERROR and stop_on_error == True):
                        isErrorFound = True
                        break
                else:
                    break
                time.sleep(3)
            except Exception, wait_exception:
                self.ClientLogger.logMessage("Exception waiting for server %s: status %s: %s" % (server_name, status, wait_exception))
                break
        return(isStatusFound, isErrorFound, server)

    def wait_for_volume_status(self, volume_name, status, timeout=600, stop_on_error=True):
        '''
        @summary: Waits for a server to enter a specific status
        @param volume_name: Name of the volume 
        @type volume_name: C{str} 
        @param staus: Volume status to expect
        @type status: L{NovaVolumeStatusTypes}
        @param timeout: Wait time in seconds before time-out 
        @type timeout: C{int}
        @param stop_on_error: Stops if volume enters error status (Only if not waiting on error status type) 
        @type stop_on_error: C{bool}
        @return: Tuple with True/False for status found, error found and the valid or empty record if volume is/is not found
        @rtype: C{Tuple} [True/False, True/False, server dictionary]
        '''
        isStatusFound = False
        isErrorFound = False
        timedOut = time.time() + timeout
        curr_status = None
        
        ''' @todo: Make this wait process more generic and robust '''
        while time.time() < timedOut:
            try:
                curr_status = self.get_volume_status(volume_name)
            except Exception, wait_exception:
                self.ClientLogger.logMessage("Exception waiting for volume %s: status %s: %s" % (volume_name, status, wait_exception))
                timedOut = 0
                break

            self.ClientLogger.logDebug("Waiting for volume %s Status %s, current Status is %s . . ." % (volume_name, status, curr_status))
            if (curr_status == status):
                isStatusFound = True
                break
            elif (((curr_status == NovaVolumeStatusTypes.ERROR) and (stop_on_error == True)) or 
                  ((curr_status == NovaVolumeStatusTypes.ERROR_DELETING) and (stop_on_error == True))):
                isErrorFound = True
                break
            time.sleep(3)

        return(isStatusFound, isErrorFound, curr_status)
        
    def create_volume_snapshot(self, volume_name, display_name=None,
                               force_create=False, display_description=None, timeout=600):
        '''
        @summary: Create a volume snapshot
        @param volume_id: ID of the volume to create a snapshot of.
        @type volume_id: C{str}
        @param force_create: Force volume snapshot create.
        @type force_create: C{bool}
        @param display_name: Display name of new volume snapshot.
        @type display_name: C{str}
        @param display_description: Display description of new volume snapshot.
        @type display_description: C{str}
        @rtype: C{dict}
        '''
        new_volume_snapshot = {}
        try:
            ''' Create Volume Snapshot requires the ID for the volume passed in, look it up first. '''
            self.ClientLogger.logMessage("Searching for Volume %s . . ." % (volume_name))
            volume = self.get_volume(volume_name)
        except Exception, search_exception:
            self.ClientLogger.logMessage("Exception locating volume: %s: %s" % (volume_name, str(search_exception)))

        if volume:
            try:
                novaResponse = self.NovaShellClient.volume_snapshot_create(volume["ID"], force_create, display_name, display_description)
            except Exception, volume_snapshot_create_exception:
                self.ClientLogger.logMessage("Exception creating snapshot of \
                volume %s where force = %s, snapshot_name = %s and \
                snapshot_description = %s: %s" % (str(volume_name), str(force_create),
                str(display_name), str(display_description), volume_snapshot_create_exception))

            snapshot_name = display_name
            if (novaResponse.IsError == False):
                self.ClientLogger.logMessage("Snapshot %s created, waiting for volume to become available . . ." % snapshot_name)
                waitResult = self.wait_for_volume_snapshot_status(snapshot_name, NovaVolumeSnapshotStatusTypes.AVAILABLE, timeout, True)
                if (waitResult[0] == True):
                    new_volume_snapshot = waitResult[2]
                else:
                    if (waitResult[1] == True):
                        self.ClientLogger.logMessage("Volume Snapshot %s was created but entered an error state before becoming active. Last Status was: %s" % (snapshot_name, waitResult[2]["Status"]))
                    elif (waitResult[2] != {}):
                        self.ClientLogger.logMessage("Volume Snapshot %s was created but timed-out before becoming active. Last Status was: %s" % (snapshot_name, waitResult[2]["Status"]))
                    else:
                        self.ClientLogger.logMessage("Volume Snapshot %s was created but never found in the system" % snapshot_name)
            else:
                self.ClientLogger.logMessage("Create volume snapshot failed, nova returned:\n%s" % novaResponse)
        else:
            self.ClientLogger.logMessage("Un-able to locate volume: %s" % volume_name)

        return(new_volume_snapshot)

    def delete_volume_snapshot(self, snapshot_name, timeout=600):
        '''
        @summary: Delete specific snapshot
        @param snapshot_name: Name of the snapshot
        @type snapshot_name: C{str}
        @param timeout: Wait time in seconds before time-out
        @type timeout: C{int}
        @return: True on success, False on failure
        @rtype: C{bool}
        '''      
        wasDeleted = False
        novaResponse = None
        try:
            ''' Delete Snapshot requires the ID of the snapshot passed in, look it up first '''
            self.ClientLogger.logMessage("Searching for Snapshot %s . . ." % (snapshot_name))
            volume_snapshot = self.get_volume_snapshot(snapshot_name)
        except Exception, search_exception:
            self.ClientLogger.logMessage("Exception locating snapshot: %s: %s" % (snapshot_name, search_exception))

        if volume_snapshot:
            self.ClientLogger.logMessage("Deleting snapshot %s"%str(snapshot_name))
            try:
                novaResponse = self.NovaShellClient.volume_snapshot_delete(volume_snapshot["ID"])
            except Exception, delete_exception:
                self.ClientLogger.logMessage("Exception deleting snapshot: %s: %s" % (snapshot_name, delete_exception))

            if (novaResponse.IsError == False):
                self.ClientLogger.logMessage("Snapshot %s deleted, waiting for snapshot to be deleting . . ." % snapshot_name)
                waitResult = self.wait_for_volume_snapshot_status(snapshot_name, NovaVolumeStatusTypes.DELETING, timeout, True)
                if (waitResult[0] == True):
                    ''' Status was found within timeout '''
                    ''' @todo: add back in the final check for deleted '''
                    self.ClientLogger.logMessage("Snapshot %s is deleting, waiting for snapshot to be removed . . ." % snapshot_name)
                    confirmResult = self.wait_for_volume_snapshot_status(snapshot_name, NovaVolumeStatusTypes.AVAILABLE, timeout, True)
                    if ((confirmResult[0] == False) and 
                        (confirmResult[1] == False) and 
                        (confirmResult[2] == {})):
                        wasDeleted = True
                        self.ClientLogger.logMessage("Snapshot %s was deleted." % snapshot_name)
                    else:
                        self.ClientLogger.logMessage("Snapshot %s was NOT deleted." % snapshot_name)
                else:
                    if (waitResult[1] == True):
                        self.ClientLogger.logMessage("Snapshot %s was deleted but entered an error state before being removed. Last Status was: %s" % (snapshot_name, waitResult[2]["Status"]))
                    elif (waitResult[2] != {}):
                        self.ClientLogger.logMessage("Snapshot %s was deleted but timed-out before being removed. Last Status was: %s" % (snapshot_name, waitResult[2]["Status"]))
                    else:
                        '''
                        The snapshot actually vanished before/during the wait for status call,
                        It's acceptable to assume that the delete was successful
                        '''
                        wasDeleted = True
                        self.ClientLogger.logMessage("Volume Snapshot %s vanished before/during the wait for status call, and was assumed deleted." % snapshot_name)
            else:
                self.ClientLogger.logMessage("Delete volume snapshot failed, nova returned:\n%s" % novaResponse)
        else:
            self.ClientLogger.logMessage("Un-able to locate snapshot: %s" % snapshot_name)
        return wasDeleted

    def delete_volume_snapshots(self, volume_id):
        '''
        @summary: Delete all snapshots for a given volume
        @param volume_id: Name of the volume
        @type volume_id: C{str}
        @return: True on success, False on failure
        @rtype: C{bool}
        '''
        volume_snapshots = self.get_volume_snapshot_list(volume_id)
        return_response = True

        for snapshot in volume_snapshots:
            if snapshot['VolumeID'] == volume_id:
                return_response = return_response and self.delete_volume_snapshot(snapshot['ID'])

        return return_response

    def get_volume_snapshot_list(self, volume_id = None):
        '''
        @summary: Returns list of all snapshots for specifified volume, or just all snapshots if volume_id is None
        @param snapshot_id: Name of the volume snapshot
        @type snapshot_id: C{str} 
        @return: Valid record(s) on success
        @rtype: C{list}
        '''
        novaResponse = None
        volume_snapshots = []
        
        try:
            novaResponse = self.NovaShellClient.volume_snapshot_list()
        except Exception, volume_snapshot_exception:
            volume_snapshot = {}
            self.ClientLogger.logMessage("Exception searching for snapshot for volume %s: %s" % (volume_id, volume_snapshot_exception))

        for row in novaResponse.yield_rows():
            volume_snapshots.append(row)
            
        if volume_id is None:
            return volume_snapshots
        else:
            relevant_snapshots = []
            for snapshot in volume_snapshots:
                if snapshot['VolumeID'] == volume_id:
                    relevant_snapshots.append(snapshot)
            return relevant_snapshots

    def wait_for_volume_snapshot_status(self, snapshot_name, status, timeout=600, stop_on_error=False):
        '''
        @summary: Waits for a volume snapshot to enter given status
        @param volume_id id of the volume
        @type volume_id: C{str}
        @param snapshot_display_name snapshot display name
        @type snapshot_display_name: C{str}        
        '''
        isStatusFound = False
        isErrorFound = False
        timedOut = time.time() + timeout
        volume_snapshot = {}
        
        ''' @todo: Make this wait process more generic and robust '''
        while time.time() < timedOut:
            try:
                volume_snapshot = self.get_volume_snapshot(snapshot_name)
                if (volume_snapshot != {}):
                    self.ClientLogger.logDebug("Waiting for volume snapshot %s Status %s, current Status is %s . . ." % (snapshot_name, status, volume_snapshot["Status"]))
                    if (volume_snapshot["Status"] == status):
                        isStatusFound = True
                        break
                    elif ((volume_snapshot["Status"] == NovaVolumeSnapshotStatusTypes.ERROR and stop_on_error == True) or
                          (volume_snapshot["Status"] == NovaVolumeSnapshotStatusTypes.ERROR_DELETING and stop_on_error == True)):
                        isErrorFound = True
                        break
                else:
                    self.ClientLogger.logMessage("Snapshot was not found.")
                    break
                time.sleep(3)
            except Exception, wait_exception:
                self.ClientLogger.logMessage("Exception waiting for volume snapshot %s: status %s: %s" % (snapshot_name, status, wait_exception))
                break

        return(isStatusFound, isErrorFound, volume_snapshot)
